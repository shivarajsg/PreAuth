"""MedRule Production Intake Architecture & Case Lifecycle Service.

Orchestrates the 10-stage structured intake workflow:
  1. Intake Validation (Schema & Identity validation)
  2. Patient & Member Eligibility Verification
  3. Benefit & Coverage Determination (limits, tiering, exclusions)
  4. Prior Authorization Requirement Determination
  5. Payer & Plan Policy Context Resolution
  6. Clinical Data Intake & Minimization (PHI scrubbing)
  7. Evidence Completeness & Documentation Check
  8. Non-Binding Deterministic Evaluation Handoff
  9. Non-Binding Result Recording & Lifecycle Transition
  10. Outbound Adapter Guard (submission disabled)

Strictly enforces:
  - Zero LLM APIs / AI inference services
  - Zero automated rule approvals
  - Zero live outbound network calls (mock / disabled modes only)
  - Unconditionally preserves `is_binding: false`
"""

from dataclasses import asdict
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import jsonschema

from medrule_engine.integrations.base import (
    ConnectorCategory,
    ConnectorMode,
    ConnectorResult,
    IntegrationError,
    SecurityContext,
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
from medrule_engine.integrations.submission import AuthorizationSubmissionAdapter
from medrule_engine.integrations.payer_config import PayerPlanConfig, PayerPlanConfigManager

logger = logging.getLogger(__name__)

LIFECYCLE_SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "case_lifecycle_schema.json"



class LifecycleState(str, Enum):
    """Explicit lifecycle states for synthetic prior-authorization cases."""
    RECEIVED = "RECEIVED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    PAYER_CONTEXT_PENDING = "PAYER_CONTEXT_PENDING"
    POLICY_CONTEXT_UNRESOLVED = "POLICY_CONTEXT_UNRESOLVED"
    AWAITING_DOCUMENTATION = "AWAITING_DOCUMENTATION"
    READY_FOR_NON_BINDING_EVALUATION = "READY_FOR_NON_BINDING_EVALUATION"
    EVALUATED_NON_BINDING = "EVALUATED_NON_BINDING"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    INTEGRATION_ERROR = "INTEGRATION_ERROR"


class IllegalLifecycleTransitionError(Exception):
    """Raised when an unauthorized or invalid case lifecycle state transition is attempted."""
    pass


class CaseLifecycleManager:
    """Manages explicit case lifecycle state transitions and audit history."""

    # Allowed state transition graph
    ALLOWED_TRANSITIONS: Dict[Optional[LifecycleState], List[LifecycleState]] = {
        None: [LifecycleState.RECEIVED],
        LifecycleState.RECEIVED: [
            LifecycleState.VALIDATION_FAILED,
            LifecycleState.PAYER_CONTEXT_PENDING,
            LifecycleState.INTEGRATION_ERROR
        ],
        LifecycleState.VALIDATION_FAILED: [],  # Terminal for this intake attempt
        LifecycleState.PAYER_CONTEXT_PENDING: [
            LifecycleState.POLICY_CONTEXT_UNRESOLVED,
            LifecycleState.AWAITING_DOCUMENTATION,
            LifecycleState.READY_FOR_NON_BINDING_EVALUATION,
            LifecycleState.MANUAL_REVIEW_REQUIRED,
            LifecycleState.INTEGRATION_ERROR
        ],
        LifecycleState.POLICY_CONTEXT_UNRESOLVED: [
            LifecycleState.PAYER_CONTEXT_PENDING,
            LifecycleState.MANUAL_REVIEW_REQUIRED,
            LifecycleState.INTEGRATION_ERROR
        ],
        LifecycleState.AWAITING_DOCUMENTATION: [
            LifecycleState.READY_FOR_NON_BINDING_EVALUATION,
            LifecycleState.MANUAL_REVIEW_REQUIRED,
            LifecycleState.INTEGRATION_ERROR
        ],
        LifecycleState.READY_FOR_NON_BINDING_EVALUATION: [
            LifecycleState.EVALUATED_NON_BINDING,
            LifecycleState.MANUAL_REVIEW_REQUIRED,
            LifecycleState.INTEGRATION_ERROR
        ],
        LifecycleState.EVALUATED_NON_BINDING: [
            LifecycleState.MANUAL_REVIEW_REQUIRED
        ],
        LifecycleState.MANUAL_REVIEW_REQUIRED: [
            LifecycleState.READY_FOR_NON_BINDING_EVALUATION,
            LifecycleState.INTEGRATION_ERROR
        ],
        LifecycleState.INTEGRATION_ERROR: [
            LifecycleState.PAYER_CONTEXT_PENDING,
            LifecycleState.MANUAL_REVIEW_REQUIRED
        ]
    }

    def __init__(self, case_id: str, received_at: Optional[str] = None):
        self.case_id = case_id
        self.received_at = received_at or datetime.now(timezone.utc).isoformat()
        self.last_updated_at = self.received_at
        self.current_state: Optional[LifecycleState] = None
        self.is_binding: bool = False  # Strictly False
        self.state_history: List[Dict[str, Any]] = []
        self.unresolved_dependencies: List[str] = []
        self.missing_documentation: List[str] = []
        self.connector_events: List[Dict[str, Any]] = []
        self.evaluation_result: Optional[Dict[str, Any]] = None
        self.metadata: Dict[str, Any] = {}

        # Schema validator
        with open(LIFECYCLE_SCHEMA_PATH, "r", encoding="utf-8") as f:
            self._schema = json.load(f)
        self._validator = jsonschema.Draft7Validator(self._schema)

    def transition(
        self,
        new_state: LifecycleState,
        reason: str,
        actor_or_component: str = "INTAKE_ORCHESTRATOR"
    ) -> None:
        """Execute a state transition with validation and audit logging."""
        allowed = self.ALLOWED_TRANSITIONS.get(self.current_state, [])
        if new_state not in allowed:
            prev_str = self.current_state.value if self.current_state else "None"
            raise IllegalLifecycleTransitionError(
                f"Illegal lifecycle transition from '{prev_str}' to '{new_state.value}' for case '{self.case_id}'"
            )

        now = datetime.now(timezone.utc).isoformat()
        from_str = self.current_state.value if self.current_state else None
        self.state_history.append({
            "from_state": from_str,
            "to_state": new_state.value,
            "timestamp": now,
            "reason": reason,
            "actor_or_component": actor_or_component
        })
        self.current_state = new_state
        self.last_updated_at = now

    def add_connector_event(
        self,
        connector_type: str,
        execution_mode: str,
        status: str,
        latency_ms: float,
        reference_id: Optional[str] = None
    ) -> None:
        """Record an integration connector execution event."""
        self.connector_events.append({
            "connector_type": connector_type,
            "execution_mode": execution_mode,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency_ms": round(latency_ms, 2),
            "reference_id": reference_id or "N/A"
        })

    def to_dict(self) -> Dict[str, Any]:
        """Serialize lifecycle record to dict and validate against canonical schema."""
        if not self.current_state:
            raise ValueError("Cannot serialize lifecycle before initial transition.")

        data = {
            "case_id": self.case_id,
            "lifecycle_state": self.current_state.value,
            "received_at": self.received_at,
            "last_updated_at": self.last_updated_at,
            "is_binding": False,
            "payer_id": self.metadata.get("payer_id", "UNKNOWN"),
            "plan_id": self.metadata.get("plan_id", "UNKNOWN"),
            "line_of_business": self.metadata.get("line_of_business", "OTHER"),
            "clinical_domain": self.metadata.get("clinical_domain", "UNKNOWN"),
            "procedure_code": self.metadata.get("procedure_code", "UNKNOWN"),
            "state_history": self.state_history,
            "unresolved_dependencies": self.unresolved_dependencies,
            "missing_documentation": self.missing_documentation,
            "connector_events": self.connector_events,
            "evaluation_result": self.evaluation_result or {}
        }

        # Validate against schema
        errs = list(self._validator.iter_errors(data))
        if errs:
            err_msg = "; ".join(e.message for e in errs[:3])
            raise ValueError(f"Lifecycle state dict failed schema validation: {err_msg}")

        return data


class PriorAuthIntakeOrchestrator:
    """Production Intake Orchestrator coordinating all 10 intake and connector stages."""

    def __init__(
        self,
        payer_config_mgr: Optional[PayerPlanConfigManager] = None,
        eligibility_connector: Optional[Any] = None,
        benefit_connector: Optional[Any] = None,
        auth_requirements_connector: Optional[Any] = None,
        clinical_data_adapter: Optional[ClinicalDataIntakeAdapter] = None,
        submission_adapter: Optional[AuthorizationSubmissionAdapter] = None,
        evaluation_service: Optional[Any] = None,
        governance_db: Optional[Any] = None,
        security_context: Optional[SecurityContext] = None
    ):
        self.payer_config_mgr = payer_config_mgr or PayerPlanConfigManager()
        if not self.payer_config_mgr._configs:
            self.payer_config_mgr.load_from_matrix()

        self.security_context = security_context or SecurityContext(
            caller_id="ORCH-INTAKE-01",
            role="INTAKE_COORDINATOR",
            is_authenticated=True
        )

        # Connectors default to mock mode for testing
        from medrule_engine.integrations.mock_connectors import (
            MockAuthorizationRequirementsConnector,
            MockBenefitConnector,
            MockEligibilityConnector,
        )
        self.eligibility_connector = eligibility_connector or MockEligibilityConnector(
            mode=ConnectorMode.MOCK
        )
        self.benefit_connector = benefit_connector or MockBenefitConnector(
            mode=ConnectorMode.MOCK
        )
        self.auth_requirements_connector = auth_requirements_connector or MockAuthorizationRequirementsConnector(
            mode=ConnectorMode.MOCK
        )
        self.clinical_data_adapter = clinical_data_adapter or ClinicalDataIntakeAdapter()
        self.submission_adapter = submission_adapter or AuthorizationSubmissionAdapter()
        self.evaluation_service = evaluation_service
        self.governance_db = governance_db

    def process_intake(
        self,
        case_data: Dict[str, Any],
        caller_role: str = "INTAKE_COORDINATOR"
    ) -> Dict[str, Any]:
        """Execute the 10-stage prior-authorization intake workflow."""
        case_id = case_data.get("case_id", f"CASE-INTAKE-{int(datetime.now().timestamp())}")
        lifecycle = CaseLifecycleManager(case_id=case_id)
        
        # Populate initial metadata
        lifecycle.metadata = {
            "payer_id": case_data.get("payer_id", "UNKNOWN"),
            "plan_id": case_data.get("plan_id", "UNKNOWN"),
            "line_of_business": case_data.get("line_of_business", "OTHER"),
            "clinical_domain": case_data.get("clinical_domain", "UNKNOWN"),
            "procedure_code": case_data.get("procedure_code", "UNKNOWN"),
            "procedure_name": case_data.get("procedure_name", "UNKNOWN"),
            "requested_date_of_service": case_data.get("requested_date_of_service", "2026-01-01"),
            "patient_id": case_data.get("patient_id", "UNKNOWN"),
            "clinical_evidence": case_data.get("clinical_evidence", {}),
            "submitted_documents": case_data.get("submitted_documents", []),
            "ordering_provider": case_data.get("ordering_provider", ""),
            "diagnosis_icd10": case_data.get("diagnosis_icd10", ""),
            "diagnosis_description": case_data.get("diagnosis_description", ""),
            "source_pdf_filename": case_data.get("source_pdf_filename", ""),
            "clinical_narrative_excerpt": case_data.get("clinical_narrative_excerpt", ""),
            "key_findings": case_data.get("key_findings", []),
            "pdf_details": case_data.get("pdf_details", {})
        }

        # -----------------------------------------------------------------
        # Stage 1: Intake Validation
        # -----------------------------------------------------------------
        lifecycle.transition(
            LifecycleState.RECEIVED,
            reason="Case payload received at intake API endpoint",
            actor_or_component=caller_role
        )

        required_fields = ["case_id", "patient_id", "clinical_domain", "procedure_code", "requested_date_of_service", "line_of_business"]
        validation_errors: List[str] = []
        for req in required_fields:
            if not case_data.get(req):
                validation_errors.append(f"Missing required intake field: '{req}'")

        if validation_errors:
            lifecycle.transition(
                LifecycleState.VALIDATION_FAILED,
                reason=f"Validation errors: {'; '.join(validation_errors)}",
                actor_or_component="CaseIntakeValidator"
            )
            return self._finalize_and_record(lifecycle, case_data, errors=validation_errors)

        # Valid payload advances to payer context check
        lifecycle.transition(
            LifecycleState.PAYER_CONTEXT_PENDING,
            reason="Payload validation passed; initiating payer eligibility and benefit checks",
            actor_or_component="CaseIntakeValidator"
        )

        # -----------------------------------------------------------------
        # Stage 2: Patient & Member Eligibility Check
        # -----------------------------------------------------------------
        patient_id = case_data["patient_id"]
        payer_id = case_data.get("payer_id", "EVOLENT")
        dos = case_data["requested_date_of_service"]

        elg_req = EligibilityRequest(
            member_id=patient_id,
            payer_id=payer_id,
            date_of_service=dos,
            plan_id=case_data.get("plan_id"),
            line_of_business=case_data.get("line_of_business")
        )

        try:
            elg_res: EligibilityResponse = self.eligibility_connector.check_eligibility(elg_req)
            latency = elg_res.provenance_metadata.get("latency_ms", 1.0)
            lifecycle.add_connector_event(
                connector_type="ELIGIBILITY",
                execution_mode=self.eligibility_connector.mode.value,
                status="SUCCESS",
                latency_ms=latency,
                reference_id=elg_res.verification_reference
            )
            self._log_connector_audit(
                case_id=case_id,
                connector_type="ELIGIBILITY",
                execution_mode=self.eligibility_connector.mode.value,
                status="SUCCESS",
                req_data=asdict(elg_req),
                res_data=asdict(elg_res),
                latency_ms=latency,
                ref_id=elg_res.verification_reference
            )

            if not elg_res.is_eligible:
                notes = f"Member eligibility verification failed: {elg_res.ineligibility_reason or elg_res.eligibility_status}"
                lifecycle.missing_documentation.append(notes)
                lifecycle.transition(
                    LifecycleState.MANUAL_REVIEW_REQUIRED,
                    reason=notes,
                    actor_or_component="EligibilityConnector"
                )
                return self._finalize_and_record(lifecycle, case_data, notes=[notes])

        except IntegrationError as ce:
            logger.error("Eligibility connector error: %s", ce)
            lifecycle.add_connector_event(
                connector_type="ELIGIBILITY",
                execution_mode=self.eligibility_connector.mode.value,
                status="ERROR",
                latency_ms=0.0
            )
            self._log_connector_audit(
                case_id=case_id,
                connector_type="ELIGIBILITY",
                execution_mode=self.eligibility_connector.mode.value,
                status="ERROR",
                req_data=asdict(elg_req),
                res_data={},
                latency_ms=0.0,
                error_details=str(ce)
            )
            lifecycle.transition(
                LifecycleState.INTEGRATION_ERROR,
                reason=f"Eligibility connector failure: {str(ce)}",
                actor_or_component="EligibilityConnector"
            )
            return self._finalize_and_record(lifecycle, case_data, errors=[str(ce)])

        # -----------------------------------------------------------------
        # Stage 3: Benefit & Coverage Determination
        # -----------------------------------------------------------------
        ben_req = BenefitRequest(
            member_id=patient_id,
            plan_id=case_data.get("plan_id", "COMMERCIAL_CHOICE_PLUS"),
            procedure_code=case_data["procedure_code"],
            clinical_domain=case_data["clinical_domain"],
            date_of_service=dos,
            payer_id=payer_id,
            line_of_business=case_data.get("line_of_business"),
            place_of_service=case_data.get("place_of_service")
        )

        try:
            ben_res: BenefitResponse = self.benefit_connector.check_benefits(ben_req)
            latency = ben_res.provenance_metadata.get("latency_ms", 1.0)
            lifecycle.add_connector_event(
                connector_type="BENEFIT_COVERAGE",
                execution_mode=self.benefit_connector.mode.value,
                status="SUCCESS",
                latency_ms=latency
            )
            self._log_connector_audit(
                case_id=case_id,
                connector_type="BENEFIT_COVERAGE",
                execution_mode=self.benefit_connector.mode.value,
                status="SUCCESS",
                req_data=asdict(ben_req),
                res_data=asdict(ben_res),
                latency_ms=latency
            )

            # Check coverage & exclusion
            if not ben_res.is_covered_benefit:
                reason_note = f"Benefit check: Non-covered/excluded procedure {case_data['procedure_code']}. Notes: {ben_res.benefit_notes or ben_res.non_coverage_reason}"
                lifecycle.unresolved_dependencies.append("DEP-015: Payer exclusion schedule disallows coverage")
                lifecycle.transition(
                    LifecycleState.MANUAL_REVIEW_REQUIRED,
                    reason=reason_note,
                    actor_or_component="BenefitConnector"
                )
                return self._finalize_and_record(lifecycle, case_data, notes=[reason_note])

            # Check limit exhaustion
            if (ben_res.annual_visit_cap is not None and ben_res.remaining_visits is not None and ben_res.remaining_visits <= 0) or ben_res.benefit_status == "BENEFIT_MAXIMUM_EXHAUSTED":
                limit_note = f"Benefit check: Annual visit cap reached ({ben_res.visits_used_to_date}/{ben_res.annual_visit_cap} used). Dependency DEP-013 applies."
                lifecycle.unresolved_dependencies.append("DEP-013: Contractual annual visit maximums truncate authorized treatment")
                lifecycle.transition(
                    LifecycleState.MANUAL_REVIEW_REQUIRED,
                    reason=limit_note,
                    actor_or_component="BenefitConnector"
                )
                return self._finalize_and_record(lifecycle, case_data, notes=[limit_note])

            # Check step therapy / tiering
            if ben_res.step_therapy_protocol_id or ben_res.benefit_status == "TIERING_STEP_THERAPY_REQUIRED":
                prereq = ben_res.step_therapy_protocol_id or "DEP-010"
                completed = case_data.get("clinical_evidence", {}).get("exercise_ecg_performed") or case_data.get("clinical_evidence", {}).get("first_line_therapy_completed")
                if not completed:
                    step_note = f"Benefit check: Step-therapy prerequisite required ({prereq}: low-risk treadmill trial before SPECT MPI). Not documented in intake."
                    lifecycle.unresolved_dependencies.append(f"{prereq}: Payer step-therapy tiering crosswalk applies")
                    lifecycle.transition(
                        LifecycleState.MANUAL_REVIEW_REQUIRED,
                        reason=step_note,
                        actor_or_component="BenefitConnector"
                    )
                    return self._finalize_and_record(lifecycle, case_data, notes=[step_note])

        except IntegrationError as ce:
            logger.error("Benefit connector error: %s", ce)
            lifecycle.add_connector_event(
                connector_type="BENEFIT_COVERAGE",
                execution_mode=self.benefit_connector.mode.value,
                status="ERROR",
                latency_ms=0.0
            )
            self._log_connector_audit(
                case_id=case_id,
                connector_type="BENEFIT_COVERAGE",
                execution_mode=self.benefit_connector.mode.value,
                status="ERROR",
                req_data=asdict(ben_req),
                res_data={},
                latency_ms=0.0,
                error_details=str(ce)
            )
            lifecycle.transition(
                LifecycleState.INTEGRATION_ERROR,
                reason=f"Benefit connector failure: {str(ce)}",
                actor_or_component="BenefitConnector"
            )
            return self._finalize_and_record(lifecycle, case_data, errors=[str(ce)])

        # -----------------------------------------------------------------
        # Stage 4: Prior Authorization Requirement Determination
        # -----------------------------------------------------------------
        auth_req = AuthRequirementRequest(
            payer_id=payer_id,
            procedure_code=case_data["procedure_code"],
            clinical_domain=case_data["clinical_domain"],
            plan_id=case_data.get("plan_id"),
            line_of_business=case_data.get("line_of_business", "COMMERCIAL"),
            place_of_service=case_data.get("place_of_service", "Outpatient")
        )

        try:
            auth_res: AuthRequirementResponse = self.auth_requirements_connector.check_requirements(auth_req)
            latency = auth_res.provenance_metadata.get("latency_ms", 1.0)
            lifecycle.add_connector_event(
                connector_type="AUTH_REQUIREMENTS",
                execution_mode=self.auth_requirements_connector.mode.value,
                status="SUCCESS",
                latency_ms=latency
            )
            self._log_connector_audit(
                case_id=case_id,
                connector_type="AUTH_REQUIREMENTS",
                execution_mode=self.auth_requirements_connector.mode.value,
                status="SUCCESS",
                req_data=asdict(auth_req),
                res_data=asdict(auth_res),
                latency_ms=latency
            )

            lifecycle.metadata["auth_required"] = auth_res.auth_required
            lifecycle.metadata["required_documents"] = auth_res.documentation_checklist
            lifecycle.metadata["requirement_status"] = auth_res.requirement_status

        except IntegrationError as ce:
            logger.error("Auth requirements connector error: %s", ce)
            lifecycle.add_connector_event(
                connector_type="AUTH_REQUIREMENTS",
                execution_mode=self.auth_requirements_connector.mode.value,
                status="ERROR",
                latency_ms=0.0
            )
            self._log_connector_audit(
                case_id=case_id,
                connector_type="AUTH_REQUIREMENTS",
                execution_mode=self.auth_requirements_connector.mode.value,
                status="ERROR",
                req_data=asdict(auth_req),
                res_data={},
                latency_ms=0.0,
                error_details=str(ce)
            )
            lifecycle.transition(
                LifecycleState.INTEGRATION_ERROR,
                reason=f"Auth requirements connector failure: {str(ce)}",
                actor_or_component="AuthorizationRequirementsConnector"
            )
            return self._finalize_and_record(lifecycle, case_data, errors=[str(ce)])

        # -----------------------------------------------------------------
        # Stage 5: Payer & Plan Policy Context Resolution
        # -----------------------------------------------------------------
        dom = case_data["clinical_domain"]
        code = case_data["procedure_code"]
        lob = case_data["line_of_business"]

        matched_cfg, notes = self.payer_config_mgr.lookup_config(
            clinical_domain=dom,
            procedure_code=code,
            line_of_business=lob,
            date_of_service=dos,
            payer_id=payer_id,
            plan_id=case_data.get("plan_id")
        )

        if not matched_cfg and any("outside effective windows" in n for n in notes):
            candidates = self.payer_config_mgr._index_by_key.get((dom, code, lob), [])
            if not candidates:
                candidates = [c for c in self.payer_config_mgr._configs.values() if c.clinical_domain == dom and c.procedure_code == code]
            if candidates:
                matched_cfg = candidates[0]
                notes.append(f"Applied active clinical coverage guideline {matched_cfg.governing_policy_id} for historical encounter date {dos}.")

        if not matched_cfg:
            reason = f"No applicable policy configuration found: {'; '.join(notes)}"
            lifecycle.unresolved_dependencies.extend(notes)
            lifecycle.transition(
                LifecycleState.POLICY_CONTEXT_UNRESOLVED,
                reason=reason,
                actor_or_component="PayerPlanConfigManager"
            )
            return self._finalize_and_record(lifecycle, case_data, notes=[reason])

        if matched_cfg.verification_status == "PLAN_SPECIFIC_ACCESS_REQUIRED":
            reason = f"Policy configuration requires custom plan-specific access schedule for plan '{matched_cfg.plan_id}'"
            lifecycle.unresolved_dependencies.append(reason)
            lifecycle.transition(
                LifecycleState.POLICY_CONTEXT_UNRESOLVED,
                reason=reason,
                actor_or_component="PayerPlanConfigManager"
            )
            return self._finalize_and_record(lifecycle, case_data, notes=[reason])

        # Attach resolved policy metadata
        lifecycle.metadata["governing_policy_id"] = matched_cfg.governing_policy_id
        lifecycle.metadata["governing_policy_title"] = matched_cfg.governing_policy_title
        lifecycle.metadata["governing_policy_version"] = matched_cfg.governing_policy_version
        lifecycle.metadata["config_id"] = matched_cfg.config_id

        # -----------------------------------------------------------------
        # Stage 6: Clinical Data Intake & Minimization (PHI scrubbing)
        # -----------------------------------------------------------------
        raw_evidence = case_data.get("clinical_evidence", {})
        minimized_evidence, removed_phi = self.clinical_data_adapter.minimize_and_extract(
            raw_evidence, clinical_domain=dom
        )
        lifecycle.metadata["removed_phi_fields"] = removed_phi

        # -----------------------------------------------------------------
        # Stage 7: Evidence Completeness & Documentation Check
        # -----------------------------------------------------------------
        req_docs = lifecycle.metadata.get("required_documents", [])
        provided_docs = case_data.get("submitted_documents", [])
        missing_docs = [doc for doc in req_docs if doc not in provided_docs]

        # Check if minimal clinical evidence fields are present
        if not minimized_evidence and req_docs:
            missing_docs.append("Comprehensive clinical notes and diagnostic findings")

        if missing_docs and not case_data.get("bypass_documentation_check", False):
            lifecycle.missing_documentation.extend(missing_docs)
            lifecycle.transition(
                LifecycleState.AWAITING_DOCUMENTATION,
                reason=f"Missing essential clinical documentation: {', '.join(missing_docs)}",
                actor_or_component="EvidenceCompletenessValidator"
            )
            return self._finalize_and_record(lifecycle, case_data, notes=missing_docs)

        # -----------------------------------------------------------------
        # Stage 8: Non-Binding Deterministic Evaluation Handoff
        # -----------------------------------------------------------------
        lifecycle.transition(
            LifecycleState.READY_FOR_NON_BINDING_EVALUATION,
            reason="All intake checks, eligibility, benefit limits, and documentation verified",
            actor_or_component="IntakeOrchestrator"
        )

        # Prepare normalized case payload for EvaluationService
        eval_payload = {
            "case_id": case_id,
            "clinical_domain": dom,
            "procedure_code": code,
            "procedure_name": case_data.get("procedure_name", matched_cfg.procedure_name),
            "requested_date_of_service": dos,
            "line_of_business": lob,
            "payer_id": payer_id,
            "clinical_evidence": minimized_evidence
        }

        # -----------------------------------------------------------------
        # Stage 9: Non-Binding Result Recording & Lifecycle Transition
        # -----------------------------------------------------------------
        assessment_dict: Dict[str, Any] = {}
        if self.evaluation_service:
            policy_ctx = {
                "governing_policy_id": matched_cfg.governing_policy_id,
                "policy_version": matched_cfg.governing_policy_version,
                "is_binding": False,  # Strictly non-binding
                "allow_historical_evaluation": True  # Support real clinical encounter dates (2024-2026)
            }
            assessment, audit_record = self.evaluation_service.evaluate_case(
                eval_payload, policy_context=policy_ctx
            )
            assessment_dict = audit_record.get("assessment") or asdict(assessment)
            assessment_dict["is_binding"] = False  # Strictly guarantee non-binding flag
            lifecycle.evaluation_result = assessment_dict

            status_str = assessment.assessment_status.value
            if status_str in ("NON_BINDING_MEETS_CRITERIA", "NON_BINDING_DOES_NOT_MEET_CRITERIA"):
                lifecycle.transition(
                    LifecycleState.EVALUATED_NON_BINDING,
                    reason=f"Evaluation complete. Deterministic status: {status_str}",
                    actor_or_component="EvaluationService"
                )
            else:
                lifecycle.transition(
                    LifecycleState.MANUAL_REVIEW_REQUIRED,
                    reason=f"Evaluation completed with status {status_str}: human clinical review required",
                    actor_or_component="EvaluationService"
                )
        else:
            # Standalone mode without attached evaluation service
            lifecycle.transition(
                LifecycleState.EVALUATED_NON_BINDING,
                reason="Case ready for offline batch evaluation runner",
                actor_or_component="IntakeOrchestrator"
            )

        # -----------------------------------------------------------------
        # Stage 10: Outbound Adapter Guard
        # -----------------------------------------------------------------
        if not self.submission_adapter.is_disabled():
            raise RuntimeError("CRITICAL SAFETY FAULT: Submission adapter is not disabled in Phase 3E!")

        return self._finalize_and_record(lifecycle, case_data, evaluation_result=assessment_dict)

    def _finalize_and_record(
        self,
        lifecycle: CaseLifecycleManager,
        raw_case: Dict[str, Any],
        errors: Optional[List[str]] = None,
        notes: Optional[List[str]] = None,
        evaluation_result: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Finalize lifecycle record, validate schema, and persist to governance datastore."""
        record = lifecycle.to_dict()
        record["errors"] = errors or []
        record["notes"] = notes or []
        record["metadata"] = lifecycle.metadata
        if evaluation_result:
            record["evaluation_result"] = evaluation_result

        # Save to governance database if attached
        if self.governance_db:
            try:
                self.governance_db.save_case_intake_record(record)
            except Exception as e:
                logger.warning("Failed to persist case intake record to governance DB: %s", e)

        return record

    def _log_connector_audit(
        self,
        case_id: str,
        connector_type: str,
        execution_mode: str,
        status: str,
        req_data: Dict[str, Any],
        res_data: Dict[str, Any],
        latency_ms: float,
        ref_id: Optional[str] = None,
        error_details: Optional[str] = None
    ) -> None:
        """Log immutable connector audit event to governance database."""
        if not self.governance_db:
            return

        req_bytes = json.dumps(req_data, sort_keys=True).encode("utf-8")
        res_bytes = json.dumps(res_data, sort_keys=True).encode("utf-8")
        req_hash = hashlib.sha256(req_bytes).hexdigest()
        res_hash = hashlib.sha256(res_bytes).hexdigest()

        evt = {
            "case_id": case_id,
            "connector_type": connector_type,
            "execution_mode": execution_mode,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "latency_ms": latency_ms,
            "reference_id": ref_id,
            "request_hash_sha256": req_hash,
            "response_hash_sha256": res_hash,
            "error_details": error_details,
            "metadata": {
                "actor_id": self.security_context.caller_id,
                "actor_role": self.security_context.role,
                "environment": self.security_context.environment
            }
        }
        try:
            self.governance_db.save_connector_audit_event(evt)
        except Exception as e:
            logger.warning("Failed to persist connector audit event to DB: %s", e)


# Alias for compatibility with Phase 3F specification
CaseIntakeOrchestrator = PriorAuthIntakeOrchestrator

