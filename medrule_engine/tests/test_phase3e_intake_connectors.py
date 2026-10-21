"""MedRule Phase 3E Test Suite: Production Intake Architecture, Payer Adapters & Benefit Configuration.

Verifies:
  1. Intake and lifecycle schema conformance and state transition rules.
  2. Payer & Plan Configuration Manager loading 22 grounded configs with schema validation.
  3. High-fidelity mock connectors covering all 13 specified test scenarios:
     - Scenario 1: Active verified eligibility
     - Scenario 2: Ineligible member (invalid ID)
     - Scenario 3: Terminated coverage
     - Scenario 4: Eligibility effective period mismatch
     - Scenario 5: External service outage (simulated 503)
     - Scenario 6: Network timeout with retry exhaustion
     - Scenario 7: Malformed payload response
     - Scenario 8: Covered benefit with standard limits
     - Scenario 9: Non-covered/excluded procedure (DEP-015)
     - Scenario 10: Benefit limits exhausted (DEP-013 visit caps)
     - Scenario 11: Tiering / step-therapy requirement (DEP-010)
     - Scenario 12: Prior authorization required with required documents checklist
     - Scenario 13: Prior authorization exempt / notification only
  4. Clinical data intake adapter data minimization (PHI scrubbing).
  5. Absolute absence of real outbound network transmission; submission adapter disabled guard.
  6. Secure case and connector state persistence in SQLite governance datastore.
  7. Strict preservation of non-binding flag (is_binding = False) and 0 approved rules in knowledge base.
"""

from dataclasses import asdict
import json
from pathlib import Path
import tempfile
from typing import Any, Dict
import pytest

from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.rule_registry import RuleRegistry
from medrule_engine.integrations.base import (
    AuthenticationError,
    BaseConnector,
    ConnectorCategory,
    ConnectorMode,
    ConnectorResult,
    IntegrationError,
    InvalidConnectorResponseError,
    SecurityContext,
    ServiceUnavailableError,
    TimeoutExhaustedError,
    UnauthorizedActivationError,
)
from medrule_engine.integrations.eligibility import (
    EligibilityConnector,
    EligibilityRequest,
    EligibilityResponse,
)
from medrule_engine.integrations.benefits import (
    BenefitConnector,
    BenefitRequest,
    BenefitResponse,
)
from medrule_engine.integrations.authorization_requirements import (
    AuthorizationRequirementsConnector,
    AuthRequirementRequest,
    AuthRequirementResponse,
)
from medrule_engine.integrations.clinical_data import ClinicalDataIntakeAdapter
from medrule_engine.integrations.submission import (
    AuthorizationSubmissionAdapter,
    SubmissionDisabledError,
)
from medrule_engine.integrations.payer_config import (
    PayerPlanConfig,
    PayerPlanConfigManager,
)
from medrule_engine.integrations.intake_service import (
    CaseLifecycleManager,
    IllegalLifecycleTransitionError,
    LifecycleState,
    PriorAuthIntakeOrchestrator,
)
from medrule_engine.integrations.mock_connectors import (
    MockAuthorizationRequirementsConnector,
    MockBenefitConnector,
    MockClinicalDataAdapter,
    MockEligibilityConnector,
    MockSubmissionAdapter,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture(scope="module")
def payer_config_mgr():
    mgr = PayerPlanConfigManager()
    count = mgr.load_from_matrix()
    assert count == 22, f"Expected 22 configs loaded from matrix, got {count}"
    return mgr


@pytest.fixture(scope="module")
def rule_registry():
    reg = RuleRegistry(include_archived=True)
    reg.load_all_domains()
    return reg


@pytest.fixture(scope="module")
def eval_service(rule_registry):
    return EvaluationService(registry=rule_registry)


@pytest.fixture
def temp_gov_db():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_phase3e_governance.db"
        db = GovernanceDatabase(db_path=db_path)
        yield db


@pytest.fixture
def default_security_context():
    return SecurityContext(
        caller_id="TEST-AGENT-01",
        role="INTAKE_COORDINATOR",
        scopes={
            "connectors:eligibility:read",
            "connectors:benefits:read",
            "connectors:auth_requirements:read",
            "connectors:clinical_data:ingest"
        },
        is_authenticated=True
    )


# ==============================================================================
# 1. Payer & Plan Configuration Manager Tests
# ==============================================================================

def test_payer_plan_config_loading_and_schema(payer_config_mgr):
    """Verify all 22 configurations load and validate against JSON schema."""
    configs = payer_config_mgr.list_configs()
    assert len(configs) == 22

    # Check PAM-ADV-001
    cfg_adv = payer_config_mgr.get_config("PAM-ADV-001")
    assert cfg_adv is not None
    assert cfg_adv.payer_id == "EVOLENT"
    assert cfg_adv.procedure_code == "74177"
    assert cfg_adv.line_of_business == "COMMERCIAL"
    assert cfg_adv.governing_policy_id == "DOC-ADV-001"
    assert "DEP-009" in cfg_adv.required_dependencies

    # Check DME Centene configuration
    cfg_dme = payer_config_mgr.get_config("PAM-DME-001")
    assert cfg_dme is not None
    assert cfg_dme.payer_id == "CENTENE"
    assert cfg_dme.procedure_code == "E0601"
    assert cfg_dme.clinical_domain == "centene_dme_orthotics_prosthetics"
    assert cfg_dme.governing_policy_id == "DOC-CEN-001"
    assert "DEP-001" in cfg_dme.required_dependencies


def test_payer_plan_config_lookup_matching(payer_config_mgr):
    """Verify lookup matching by domain, procedure, LOB, and date of service."""
    # Exact match for Advanced Imaging
    matched, notes = payer_config_mgr.lookup_config(
        clinical_domain="advanced_imaging",
        procedure_code="74177",
        line_of_business="COMMERCIAL",
        date_of_service="2026-06-15",
        payer_id="EVOLENT"
    )
    assert matched is not None
    assert matched.config_id == "CFG-PAM-ADV-001"
    assert len(notes) == 0

    # Unmatched LOB returns helpful error notes
    unmatched_lob, notes_lob = payer_config_mgr.lookup_config(
        clinical_domain="advanced_imaging",
        procedure_code="74183",
        line_of_business="MEDICAID",
        date_of_service="2026-06-15"
    )
    assert unmatched_lob is None
    assert any("No configuration found for LOB 'MEDICAID'" in n for n in notes_lob)

    # Date outside effective range
    outdated, notes_date = payer_config_mgr.lookup_config(
        clinical_domain="advanced_imaging",
        procedure_code="74177",
        line_of_business="COMMERCIAL",
        date_of_service="2024-01-01"
    )
    assert outdated is None
    assert any("outside effective windows" in n for n in notes_date)


# ==============================================================================
# 2. Case Lifecycle State Machine Tests
# ==============================================================================

def test_case_lifecycle_valid_transitions():
    """Verify valid state progression and schema conformance."""
    mgr = CaseLifecycleManager("CASE-VALID-01")
    mgr.metadata = {
        "payer_id": "EVOLENT",
        "plan_id": "Commercial Comprehensive",
        "line_of_business": "COMMERCIAL",
        "clinical_domain": "advanced_imaging",
        "procedure_code": "74177"
    }

    # Step 1: Received
    mgr.transition(LifecycleState.RECEIVED, "API submission received")
    assert mgr.current_state == LifecycleState.RECEIVED

    # Step 2: Advance to Payer Context Pending
    mgr.transition(LifecycleState.PAYER_CONTEXT_PENDING, "Payload schema validated")
    assert mgr.current_state == LifecycleState.PAYER_CONTEXT_PENDING

    # Step 3: Advance to Ready for Evaluation
    mgr.transition(LifecycleState.READY_FOR_NON_BINDING_EVALUATION, "Eligibility & benefits verified")
    assert mgr.current_state == LifecycleState.READY_FOR_NON_BINDING_EVALUATION

    # Step 4: Advance to Evaluated Non-Binding
    mgr.transition(LifecycleState.EVALUATED_NON_BINDING, "Evaluation complete")
    assert mgr.current_state == LifecycleState.EVALUATED_NON_BINDING

    # Export and validate against canonical schema
    data = mgr.to_dict()
    assert data["case_id"] == "CASE-VALID-01"
    assert data["lifecycle_state"] == "EVALUATED_NON_BINDING"
    assert data["is_binding"] is False
    assert len(data["state_history"]) == 4


def test_case_lifecycle_illegal_transitions():
    """Verify illegal jumps are blocked by IllegalLifecycleTransitionError."""
    mgr = CaseLifecycleManager("CASE-ILLEGAL-01")

    # Cannot transition before RECEIVED
    with pytest.raises(IllegalLifecycleTransitionError):
        mgr.transition(LifecycleState.EVALUATED_NON_BINDING, "Illegal jump")

    mgr.transition(LifecycleState.RECEIVED, "Received")

    # Cannot jump directly from RECEIVED to EVALUATED_NON_BINDING
    with pytest.raises(IllegalLifecycleTransitionError):
        mgr.transition(LifecycleState.EVALUATED_NON_BINDING, "Illegal jump")

    # Fail validation
    mgr.transition(LifecycleState.VALIDATION_FAILED, "Missing required fields")

    # VALIDATION_FAILED is terminal: cannot advance to READY_FOR_NON_BINDING_EVALUATION
    with pytest.raises(IllegalLifecycleTransitionError):
        mgr.transition(LifecycleState.READY_FOR_NON_BINDING_EVALUATION, "Illegal advance from failed")


# ==============================================================================
# 3. Mock Connectors — 13 Scenarios Tests
# ==============================================================================

def test_scenario_01_verified_active_eligibility(default_security_context):
    """Scenario 1: Verified active member eligibility."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    req = EligibilityRequest(
        member_id="MEM-SYNTH-001",
        payer_id="EVOLENT",
        date_of_service="2026-05-15"
    )
    res = connector.check_eligibility(req, security_context=default_security_context)
    assert res.is_eligible is True
    assert res.eligibility_status == "ACTIVE_COVERAGE"
    assert res.verification_reference is not None


def test_scenario_02_ineligible_member_not_found(default_security_context):
    """Scenario 2: Ineligible member ID not found."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    req = EligibilityRequest(
        member_id="MEM-INVALID-999",
        payer_id="EVOLENT",
        date_of_service="2026-05-15"
    )
    res = connector.check_eligibility(req, security_context=default_security_context)
    assert res.is_eligible is False
    assert res.eligibility_status == "INELIGIBLE_MEMBER_NOT_FOUND"
    assert "not found" in res.ineligibility_reason.lower()


def test_scenario_03_terminated_coverage(default_security_context):
    """Scenario 3: Member coverage terminated prior to date of service."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    req = EligibilityRequest(
        member_id="MEM-TERMINATED-001",
        payer_id="EVOLENT",
        date_of_service="2026-05-15"
    )
    res = connector.check_eligibility(req, security_context=default_security_context)
    assert res.is_eligible is False
    assert res.eligibility_status == "COVERAGE_TERMINATED"


def test_scenario_04_period_mismatch(default_security_context):
    """Scenario 4: Date of service outside member effective coverage window."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    req = EligibilityRequest(
        member_id="MEM-PERIOD-MISMATCH-001",
        payer_id="EVOLENT",
        date_of_service="2026-11-01"  # Coverage ended 2026-06-30
    )
    res = connector.check_eligibility(req, security_context=default_security_context)
    assert res.is_eligible is False
    assert res.eligibility_status == "DATE_OUTSIDE_COVERAGE_PERIOD"


def test_scenario_05_service_outage_simulation(default_security_context):
    """Scenario 5: External payer gateway outage (503 Service Unavailable)."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    req = EligibilityRequest(
        member_id="MEM-SIM-OUTAGE",
        payer_id="EVOLENT",
        date_of_service="2026-05-15"
    )
    with pytest.raises(ServiceUnavailableError):
        connector.check_eligibility(req, security_context=default_security_context)


def test_scenario_06_timeout_retry_exhaustion(default_security_context):
    """Scenario 6: Network timeout with retry exhaustion."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    req = EligibilityRequest(
        member_id="MEM-SIM-TIMEOUT",
        payer_id="EVOLENT",
        date_of_service="2026-05-15"
    )
    with pytest.raises(TimeoutExhaustedError):
        connector.check_eligibility(req, security_context=default_security_context)


def test_scenario_07_malformed_response_simulation(default_security_context):
    """Scenario 7: Malformed or non-conforming payload response."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    req = EligibilityRequest(
        member_id="MEM-SIM-MALFORMED",
        payer_id="EVOLENT",
        date_of_service="2026-05-15"
    )
    with pytest.raises(InvalidConnectorResponseError):
        connector.check_eligibility(req, security_context=default_security_context)


def test_scenario_08_covered_benefit_standard(default_security_context):
    """Scenario 8: Standard covered benefit under health plan."""
    connector = MockBenefitConnector(mode=ConnectorMode.MOCK)
    req = BenefitRequest(
        member_id="MEM-SYNTH-001",
        plan_id="COMMERCIAL_CHOICE_PLUS",
        procedure_code="74177",
        clinical_domain="advanced_imaging",
        date_of_service="2026-05-15"
    )
    res = connector.check_benefits(req, security_context=default_security_context)
    assert res.is_covered_benefit is True
    assert res.benefit_status == "COVERED_BENEFIT"
    assert res.preauth_mandatory is True


def test_scenario_09_non_covered_excluded_procedure(default_security_context):
    """Scenario 9: Non-covered/excluded procedure schedule (DEP-015)."""
    connector = MockBenefitConnector(mode=ConnectorMode.MOCK)
    req = BenefitRequest(
        member_id="MEM-SYNTH-001",
        plan_id="COMMERCIAL_CUSTOM_HMO",
        procedure_code="81432",
        clinical_domain="genetic_testing",
        date_of_service="2026-05-15"
    )
    res = connector.check_benefits(req, security_context=default_security_context)
    assert res.is_covered_benefit is False
    assert res.benefit_status == "NON_COVERED_EXCLUSION"
    assert "DEP-015" in (res.non_coverage_reason or "")


def test_scenario_10_benefit_limits_exhausted(default_security_context):
    """Scenario 10: Annual visit maximums exhausted (DEP-013 visit caps)."""
    connector = MockBenefitConnector(mode=ConnectorMode.MOCK)
    req = BenefitRequest(
        member_id="MEM-SYNTH-001",
        plan_id="COMMERCIAL_CHOICE_PLUS",
        procedure_code="97110",
        clinical_domain="physical_medicine",
        date_of_service="2026-05-15"
    )
    # Payload trigger: 30 visits used out of 30 cap
    payload = asdict(req)
    payload["visits_used_to_date"] = 30
    exec_res = connector.execute(payload, default_security_context)
    data = exec_res.data
    assert data["benefit_status"] == "BENEFIT_MAXIMUM_EXHAUSTED"
    assert data["remaining_visits"] == 0


def test_scenario_11_tiering_step_therapy_requirement(default_security_context):
    """Scenario 11: Tiering / step-therapy required (DEP-010)."""
    connector = MockBenefitConnector(mode=ConnectorMode.MOCK)
    req = BenefitRequest(
        member_id="MEM-SYNTH-001",
        plan_id="COMMERCIAL_CUSTOM_HMO",
        procedure_code="78452",
        clinical_domain="cardiology",
        date_of_service="2026-05-15"
    )
    res = connector.check_benefits(req, security_context=default_security_context)
    assert res.benefit_status == "TIERING_STEP_THERAPY_REQUIRED"
    assert res.step_therapy_protocol_id == "DEP-010"


def test_scenario_12_prior_auth_mandatory_checklist(default_security_context):
    """Scenario 12: Prior authorization mandatory with required documentation checklist."""
    connector = MockAuthorizationRequirementsConnector(mode=ConnectorMode.MOCK)
    req = AuthRequirementRequest(
        payer_id="EVOLENT",
        procedure_code="74177",
        clinical_domain="advanced_imaging"
    )
    res = connector.check_requirements(req, security_context=default_security_context)
    assert res.auth_required is True
    assert res.requirement_status == "PRIOR_AUTH_MANDATORY"
    assert "CLINICAL_OFFICE_NOTES" in res.documentation_checklist
    assert len(res.documentation_checklist) >= 3


def test_scenario_13_prior_auth_exempt_or_notification(default_security_context):
    """Scenario 13: Prior authorization exempt / notification only."""
    connector = MockAuthorizationRequirementsConnector(mode=ConnectorMode.MOCK)
    req = AuthRequirementRequest(
        payer_id="EVOLENT",
        procedure_code="76775",
        clinical_domain="cardiology",
        line_of_business="MEDICARE_ADVANTAGE"
    )
    res = connector.check_requirements(req, security_context=default_security_context)
    assert res.auth_required is False
    assert res.requirement_status == "PRIOR_NOTIFICATION_ONLY"


# ==============================================================================
# 4. Clinical Data Intake Adapter Tests (PHI Minimization)
# ==============================================================================

def test_clinical_data_intake_minimization():
    """Verify adapter strips direct patient identifiers while preserving clinical variables."""
    adapter = ClinicalDataIntakeAdapter(mode=ConnectorMode.MOCK)
    raw_evidence = {
        "patient_name": "John Doe",
        "ssn": "000-11-2222",
        "phone": "555-0199",
        "email": "johndoe@example.com",
        "patient_address": "123 Elm St, Metropolis",
        "mrn_raw": "MRN-998877",
        # Legitimate clinical variables
        "patient_age": 52,
        "unexplained_weight_loss": True,
        "fever_of_unknown_origin": True,
        "prior_conservative_therapy_duration_weeks": 8
    }

    minimized, removed = adapter.minimize_and_extract(raw_evidence, clinical_domain="advanced_imaging")

    # Assert all sensitive fields scrubbed
    for field_name in ("patient_name", "ssn", "phone", "email", "patient_address", "mrn_raw"):
        assert field_name not in minimized
        assert field_name in removed

    # Assert clinical variables preserved
    assert minimized["patient_age"] == 52
    assert minimized["unexplained_weight_loss"] is True
    assert minimized["fever_of_unknown_origin"] is True
    assert minimized["prior_conservative_therapy_duration_weeks"] == 8


# ==============================================================================
# 5. Outbound Adapter Guard & Safety Tests
# ==============================================================================

def test_submission_adapter_disabled_safety():
    """Verify authorization submission adapter is strictly disabled and rejects activation."""
    adapter = AuthorizationSubmissionAdapter()
    assert adapter.is_disabled() is True
    assert adapter.mode == ConnectorMode.DISABLED

    admin_sec = SecurityContext(
        caller_id="ADMIN-01",
        role="ADMINISTRATOR",
        scopes={"connectors:admin:configure"},
        is_authenticated=True,
        is_admin=True
    )

    # Attempt to change mode to MOCK or LIVE must be rejected
    with pytest.raises(SubmissionDisabledError):
        adapter.set_mode(ConnectorMode.MOCK, security_context=admin_sec)

    with pytest.raises(SubmissionDisabledError):
        adapter.set_mode(ConnectorMode.LIVE_AUTHORIZED, security_context=admin_sec)

    # Submitting an authorization must return disabled failure
    res = adapter.submit_authorization(
        case_id="CASE-SAFE-01",
        evaluation_result={"test": True},
        security_context=admin_sec
    )
    assert res.is_success is False
    assert res.status_code == "SUBMISSION_DISABLED"
    assert res.provenance_metadata["is_binding"] is False


def test_unauthorized_activation_error_on_live_mode(default_security_context):
    """Verify live authorized mode cannot be activated by non-admins or in Phase 3E."""
    connector = MockEligibilityConnector(mode=ConnectorMode.MOCK)
    with pytest.raises(UnauthorizedActivationError):
        connector.set_mode(ConnectorMode.LIVE_AUTHORIZED, security_context=default_security_context)


# ==============================================================================
# 6. PriorAuthIntakeOrchestrator End-to-End Workflow Tests
# ==============================================================================

def test_intake_orchestrator_full_workflow(eval_service, temp_gov_db):
    """Verify end-to-end 10-stage intake workflow with attached evaluation and governance DB."""
    orch = PriorAuthIntakeOrchestrator(
        evaluation_service=eval_service,
        governance_db=temp_gov_db
    )

    case_payload = {
        "case_id": "CASE-ORCH-ADV-01",
        "patient_id": "MEM-SYNTH-001",
        "clinical_domain": "advanced_imaging",
        "procedure_code": "74177",
        "procedure_name": "CT Abdomen and Pelvis with contrast",
        "line_of_business": "COMMERCIAL",
        "payer_id": "EVOLENT",
        "plan_id": "Commercial Comprehensive",
        "requested_date_of_service": "2026-05-15",
        "submitted_documents": [
            "CLINICAL_OFFICE_NOTES",
            "ABDOMINAL_ULTRASOUND_REPORT",
            "LABORATORY_LIPASE_AMYLASE_PANEL"
        ],
        "clinical_evidence": {
            "patient_age": 45,
            "unexplained_weight_loss": True,
            "fever_of_unknown_origin": True,
            "ssn": "000-00-1234",
            "phone": "555-9876"
        }
    }

    result = orch.process_intake(case_payload)

    # Assert lifecycle state
    assert result["case_id"] == "CASE-ORCH-ADV-01"
    assert result["lifecycle_state"] in ("EVALUATED_NON_BINDING", "MANUAL_REVIEW_REQUIRED")
    assert result["is_binding"] is False
    assert len(result["state_history"]) >= 4

    # Assert PHI was stripped
    assert "ssn" in result["metadata"]["removed_phi_fields"]
    assert "phone" in result["metadata"]["removed_phi_fields"]

    # Assert evaluation result present and non-binding
    eval_res = result["evaluation_result"]
    assert eval_res["is_binding"] is False

    # Assert persisted in governance DB
    saved_record = temp_gov_db.get_case_intake_record("CASE-ORCH-ADV-01")
    assert saved_record is not None
    assert saved_record["case_id"] == "CASE-ORCH-ADV-01"
    assert saved_record["is_binding"] is False

    # Assert connector audit events recorded in DB
    events = temp_gov_db.list_connector_audit_events("CASE-ORCH-ADV-01")
    assert len(events) >= 3
    event_types = set(e["connector_type"] for e in events)
    assert {"ELIGIBILITY", "BENEFIT_COVERAGE", "AUTH_REQUIREMENTS"}.issubset(event_types)
    for evt in events:
        assert len(evt["request_hash_sha256"]) == 64
        assert len(evt["response_hash_sha256"]) == 64


def test_intake_orchestrator_ineligible_member(eval_service, temp_gov_db):
    """Verify intake halts and transitions to MANUAL_REVIEW_REQUIRED when member is ineligible."""
    orch = PriorAuthIntakeOrchestrator(
        evaluation_service=eval_service,
        governance_db=temp_gov_db
    )

    case_payload = {
        "case_id": "CASE-ORCH-INELIGIBLE",
        "patient_id": "MEM-INVALID-999",
        "clinical_domain": "advanced_imaging",
        "procedure_code": "74177",
        "line_of_business": "COMMERCIAL",
        "payer_id": "EVOLENT",
        "requested_date_of_service": "2026-05-15"
    }

    result = orch.process_intake(case_payload)
    assert result["lifecycle_state"] == "MANUAL_REVIEW_REQUIRED"
    assert any("eligibility" in n.lower() for n in result["notes"])


def test_intake_orchestrator_excluded_procedure(eval_service, temp_gov_db):
    """Verify intake halts and records DEP-015 dependency when procedure is excluded."""
    orch = PriorAuthIntakeOrchestrator(
        evaluation_service=eval_service,
        governance_db=temp_gov_db
    )

    case_payload = {
        "case_id": "CASE-ORCH-EXCLUDED",
        "patient_id": "MEM-SYNTH-001",
        "clinical_domain": "genetic_testing",
        "procedure_code": "81432",
        "line_of_business": "COMMERCIAL",
        "payer_id": "EVOLENT",
        "plan_id": "COMMERCIAL_CUSTOM_HMO",
        "requested_date_of_service": "2026-05-15"
    }

    result = orch.process_intake(case_payload)
    assert result["lifecycle_state"] == "MANUAL_REVIEW_REQUIRED"
    assert any("DEP-015" in d for d in result["unresolved_dependencies"])


def test_intake_orchestrator_service_outage(eval_service, temp_gov_db):
    """Verify intake transitions to INTEGRATION_ERROR when connector encounters service outage."""
    orch = PriorAuthIntakeOrchestrator(
        evaluation_service=eval_service,
        governance_db=temp_gov_db
    )

    case_payload = {
        "case_id": "CASE-ORCH-OUTAGE",
        "patient_id": "MEM-SIM-OUTAGE",
        "clinical_domain": "advanced_imaging",
        "procedure_code": "74177",
        "line_of_business": "COMMERCIAL",
        "payer_id": "EVOLENT",
        "requested_date_of_service": "2026-05-15"
    }

    result = orch.process_intake(case_payload)
    assert result["lifecycle_state"] == "INTEGRATION_ERROR"
    assert len(result["errors"]) > 0


# ==============================================================================
# 7. Knowledge Base Integrity Assertion (Strict Corpus Constraints)
# ==============================================================================

def test_knowledge_base_rule_counts_and_zero_approvals(rule_registry):
    """Corpus must strictly contain exactly 372 rules, 322 draft, 50 review, 0 approved."""
    rules = rule_registry.get_all_rules()
    assert len(rules) == 372, f"Expected 372 rules, got {len(rules)}"

    approved = [r for r in rules if r.extraction_status == "APPROVED" or r.is_approved]
    assert len(approved) == 0, f"Zero rules may be marked APPROVED in Phase 3E, found {len(approved)}"

    draft = [r for r in rules if r.extraction_status == "DRAFT"]
    assert len(draft) == 322, f"Expected 322 DRAFT rules, got {len(draft)}"

    review = [r for r in rules if r.extraction_status == "NEEDS_HUMAN_REVIEW"]
    assert len(review) == 50, f"Expected 50 NEEDS_HUMAN_REVIEW rules, got {len(review)}"
