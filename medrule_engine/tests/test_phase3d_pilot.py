"""MedRule Phase 3D — Pilot Adjudication & Controlled Evaluation Test Suite.

Verifies:
1. Pilot dataset completeness and schema validity across 36 synthetic cases
2. Full representation of all nine clinical domains
3. Policy applicability matrix completeness and multi-payer/LOB configurations
4. Pilot runner execution and 100% pass rate against expected results
5. Clinical SME human adjudication log completeness and valid reviewer roles
6. Controlled agreement rate (28 cases) and discrepancy rate (8 cases)
7. Discrepancy categorization, root-cause analysis, and remediation tracking
8. Unconditional non-binding governance gate (is_binding: false)
9. Strict corpus zero-approved preservation (0 approved, 322 draft, 50 needs_human_review)
10. Cryptographic SHA-256 evaluation repeatability and deterministic hashing
11. Line-of-business (LOB) routing boundaries (Commercial, Medicare Advantage, Medicaid)
12. Date of service (DOS) historical boundary enforcement (pre-2026 guidelines)
13. Unresolved policy dependency routing guards (DEP-002, DEP-008, DEP-010, etc.)
14. Governance datastore persistence for pilot evaluations, adjudications, and discrepancies
15. Web UI pilot dashboard and case comparison workbench endpoints
16. Evaluator throughput and deterministic execution performance (< 15ms per case)
"""

import csv
import json
from pathlib import Path
import pytest

from medrule_engine.case_validator import CaseValidator, validate_case
from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.pilot.run_pilot import run_pilot
from medrule_engine.rule_registry import RuleRegistry
from medrule_engine.web.app import create_app

REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT_DIR = REPO_ROOT / "medrule_engine" / "pilot"
CASES_FILE = PILOT_DIR / "synthetic_pilot_cases.json"
EXPECTED_FILE = PILOT_DIR / "pilot_expected_results.json"
HUMAN_LOG_FILE = PILOT_DIR / "human_adjudication_log.csv"
DISCREPANCIES_FILE = PILOT_DIR / "pilot_discrepancies.csv"
APPLICABILITY_FILE = REPO_ROOT / "rulebook_collection" / "manifests" / "phase_3d_policy_applicability_matrix.csv"
RESULTS_FILE = PILOT_DIR / "pilot_run_results.json"


@pytest.fixture(scope="module")
def registry():
    reg = RuleRegistry()
    reg.load_all_domains()
    db = GovernanceDatabase()
    reg.attach_governance_db(db)
    return reg


@pytest.fixture(scope="module")
def eval_service(registry):
    return EvaluationService(registry=registry)


@pytest.fixture(scope="module")
def gov_db():
    return GovernanceDatabase()


@pytest.fixture(scope="module")
def web_client(registry, gov_db):
    app = create_app(registry=registry, db=gov_db, test_config={"TESTING": True})
    return app.test_client()


# ==============================================================================
# 1. Dataset Completeness & Schema Validity
# ==============================================================================

def test_pilot_dataset_completeness_and_schema():
    """Verify 36 synthetic pilot cases exist and each strictly satisfies case_schema.json."""
    assert CASES_FILE.exists(), f"Missing {CASES_FILE}"
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    assert len(cases) == 36, f"Expected exactly 36 pilot cases, got {len(cases)}"
    validator = CaseValidator()

    for case in cases:
        is_valid, errors, case_obj = validator.validate(case)
        assert is_valid, f"Case {case.get('case_id')} failed schema validation: {errors}"
        assert case_obj is not None
        assert case_obj.case_id.startswith("CASE-PILOT-")


# ==============================================================================
# 2. Representation of All Nine Clinical Domains
# ==============================================================================

def test_all_nine_domains_represented():
    """Verify all 9 clinical domains have at least 4 pilot test cases."""
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    expected_domains = {
        "advanced_imaging",
        "cardiology",
        "musculoskeletal_surgery",
        "interventional_pain_management",
        "radiation_oncology",
        "physical_medicine",
        "sleep_health",
        "genetic_testing",
        "centene_dme_orthotics_prosthetics"
    }

    by_domain = {}
    for c in cases:
        dom = c["clinical_domain"]
        by_domain[dom] = by_domain.get(dom, 0) + 1

    assert set(by_domain.keys()) == expected_domains
    for dom, count in by_domain.items():
        assert count == 4, f"Domain {dom} expected exactly 4 cases, got {count}"


# ==============================================================================
# 3. Policy Applicability Matrix Completeness
# ==============================================================================

def test_policy_applicability_matrix_completeness():
    """Verify phase_3d_policy_applicability_matrix.csv is populated and valid."""
    assert APPLICABILITY_FILE.exists()
    with open(APPLICABILITY_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) >= 20, f"Expected >= 20 applicability rows, got {len(rows)}"

    domains = set(r["clinical_domain"] for r in rows)
    assert len(domains) == 9, "Matrix must cover all 9 clinical domains"

    lobs = set(r["line_of_business"] for r in rows)
    assert {"COMMERCIAL", "MEDICARE_ADVANTAGE", "MEDICAID"}.issubset(lobs)

    statuses = set(r["applicability_status"] for r in rows)
    assert "VERIFIED_APPLICABLE" in statuses
    assert "PLAN_SPECIFIC_ACCESS_REQUIRED" in statuses


# ==============================================================================
# 4. Pilot Runner Execution and 100% Pass Rate
# ==============================================================================

def test_pilot_runner_execution_and_pass_rate():
    """Verify run_pilot() executes deterministically with 100% pass rate."""
    summary = run_pilot()
    assert summary["total_cases_evaluated"] == 36
    assert summary["domains_evaluated"] == 9
    assert summary["passed_cases"] == 36
    assert summary["failed_cases"] == 0
    assert summary["pass_rate_percentage"] == 100.0


# ==============================================================================
# 5. Human Adjudication Log Completeness
# ==============================================================================

def test_human_adjudication_log_completeness():
    """Verify human_adjudication_log.csv has 36 documented SME adjudications."""
    assert HUMAN_LOG_FILE.exists()
    with open(HUMAN_LOG_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 36
    case_ids = set()
    valid_roles = {"CLINICAL_SME_REVIEWER", "MEDICAL_DIRECTOR"}

    for r in rows:
        cid = r["case_id"]
        assert cid.startswith("CASE-PILOT-")
        assert cid not in case_ids, f"Duplicate adjudication for case {cid}"
        case_ids.add(cid)

        assert r["reviewer_role"] in valid_roles
        assert len(r["human_adjudication_rationale"].strip()) > 10
        assert len(r["source_evidence_considered"].strip()) > 5


# ==============================================================================
# 6. Agreement and Discrepancy Counts
# ==============================================================================

def test_agreement_and_discrepancy_counts():
    """Verify exactly 28 agreeing cases and 8 controlled discrepancies."""
    with open(HUMAN_LOG_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    agreement_count = sum(1 for r in rows if r["comparison_status_with_engine"] == "AGREEMENT")
    discrepancy_count = sum(1 for r in rows if r["discrepancy_id"] and r["discrepancy_id"] != "None")

    assert agreement_count == 28, f"Expected 28 agreements, got {agreement_count}"
    assert discrepancy_count == 8, f"Expected 8 discrepancies, got {discrepancy_count}"
    assert agreement_count + discrepancy_count == 36


# ==============================================================================
# 7. Discrepancy Categories and Root Cause Analysis
# ==============================================================================

def test_discrepancy_categories_and_root_cause_analysis():
    """Verify all 8 discrepancies have complete root causes and remediations."""
    assert DISCREPANCIES_FILE.exists()
    with open(DISCREPANCIES_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        drows = list(reader)

    assert len(drows) == 8
    valid_categories = {
        "AMBIGUOUS_SOURCE_INTERPRETATION",
        "POLICY_APPLICABILITY_ISSUE",
        "POLICY_SELECTION_DISAGREEMENT"
    }

    for d in drows:
        assert d["discrepancy_category"] in valid_categories
        assert len(d["root_cause_analysis"].strip()) > 20
        assert len(d["remediation_proposal"].strip()) > 20
        assert len(d["assigned_reviewer"].strip()) > 0
        assert d["remediation_status"] in {"OPEN", "CORRECTION_PROPOSED", "REMEDIATED", "UNRESOLVED_PENDING_POLICY_REVIEW"}


# ==============================================================================
# 8. Unconditional Non-Binding Governance Gate
# ==============================================================================

def test_unconditional_non_binding_governance():
    """Verify all pilot evaluation results enforce is_binding: false."""
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    assert results["strict_non_binding_enforced"] is True
    for c in results["case_evaluations"]:
        assert c["is_binding"] is False, f"Case {c['case_id']} had is_binding=True!"


# ==============================================================================
# 9. Strict Zero-Approved Corpus Preservation
# ==============================================================================

def test_zero_approved_rules_in_corpus(registry):
    """Verify repository strictly preserves 0 approved, 322 draft, 50 needs_human_review."""
    all_rules = list(registry._rules_by_id.values())
    assert len(all_rules) == 372

    approved = [r for r in all_rules if r.is_approved]
    drafts = [r for r in all_rules if r.extraction_status == "DRAFT"]
    needs_review = [r for r in all_rules if r.extraction_status == "NEEDS_HUMAN_REVIEW"]

    assert len(approved) == 0, "Corpus must have exactly 0 approved rules!"
    assert len(drafts) == 322, f"Expected 322 draft rules, found {len(drafts)}"
    assert len(needs_review) == 50, f"Expected 50 needs_human_review rules, found {len(needs_review)}"


# ==============================================================================
# 10. Cryptographic SHA-256 Repeatability
# ==============================================================================

def test_cryptographic_sha256_repeatability(eval_service):
    """Verify multiple executions of identical case inputs yield identical SHA-256 hashes."""
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    test_case = cases[0]  # CASE-PILOT-ADV-001
    _, audit1 = eval_service.evaluate_case(test_case, target_rule_ids=["RULE-ADV-CG2000-006"])
    _, audit2 = eval_service.evaluate_case(test_case, target_rule_ids=["RULE-ADV-CG2000-006"])

    hash1 = audit1["reproducibility_hash_sha256"]
    hash2 = audit2["reproducibility_hash_sha256"]

    assert len(hash1) == 64
    assert hash1 == hash2


# ==============================================================================
# 11. Policy Routing Line-of-Business Boundaries
# ==============================================================================

def test_policy_routing_lob_boundaries(eval_service):
    """Verify invalid or unverified line-of-business triggers MANUAL_REVIEW_REQUIRED."""
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    # LOB 'OTHER' satisfies intake schema enum but violates router commercial applicability
    bad_lob_case = dict(cases[0])
    bad_lob_case["line_of_business"] = "OTHER"
    bad_lob_case["case_id"] = "CASE-PILOT-TEST-BAD-LOB"

    assessment, _ = eval_service.evaluate_case(bad_lob_case)
    assert assessment.assessment_status.value == "MANUAL_REVIEW_REQUIRED"


# ==============================================================================
# 12. Date of Service Historical Boundary Enforcement
# ==============================================================================

def test_date_of_service_boundary_guard(eval_service):
    """Verify dates of service preceding 2026-01-01 route to POLICY_VERSION_UNRESOLVED."""
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    hist_case = dict(cases[0])
    hist_case["requested_date_of_service"] = "2024-06-15"
    hist_case["case_id"] = "CASE-PILOT-TEST-HISTORICAL"

    assessment, _ = eval_service.evaluate_case(hist_case)
    assert assessment.assessment_status.value == "POLICY_VERSION_UNRESOLVED"


# ==============================================================================
# 13. Unresolved Policy Dependency Routing
# ==============================================================================

def test_unresolved_policy_dependency_routing(eval_service):
    """Verify unresolved policy dependencies halt evaluation with MANUAL_REVIEW_REQUIRED."""
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases = json.load(f)

    dep_case = dict(cases[4])  # CARD
    ctx = {"unresolved_plan_dependency": "DEP-010"}

    assessment, _ = eval_service.evaluate_case(dep_case, policy_context=ctx)
    assert assessment.assessment_status.value == "MANUAL_REVIEW_REQUIRED"
    assert any("DEP-010" in dep for dep in assessment.conflicts_or_unresolved_dependencies)


# ==============================================================================
# 14. Governance Datastore Pilot Persistence
# ==============================================================================

def test_governance_datastore_pilot_persistence(gov_db):
    """Verify SQLite datastore correctly syncs and retrieves pilot tables."""
    synced = gov_db.sync_pilot_all(PILOT_DIR)
    assert synced["evaluations"] == 36
    assert synced["adjudications"] == 36
    assert synced["discrepancies"] == 8

    evals = gov_db.get_pilot_evaluations()
    assert len(evals) == 36

    adjs = gov_db.get_human_adjudications()
    assert len(adjs) == 36

    discs = gov_db.get_pilot_discrepancies()
    assert len(discs) == 8

    # Filter by domain
    adv_evals = gov_db.get_pilot_evaluations(domain="advanced_imaging")
    assert len(adv_evals) == 4


# ==============================================================================
# 15. Web UI Pilot Dashboard & Case Detail Routes
# ==============================================================================

def test_web_ui_pilot_dashboard_and_detail_routes(web_client):
    """Verify Web UI pilot dashboard, detail page, and API endpoints."""
    # 1. Main pilot dashboard
    r_dash = web_client.get("/pilot")
    assert r_dash.status_code == 200
    assert b"Clinical Pilot Case Adjudication" in r_dash.data
    assert b"CASE-PILOT-ADV-001" in r_dash.data

    # 2. Case detail view
    r_detail = web_client.get("/pilot/CASE-PILOT-ADV-001")
    assert r_detail.status_code == 200
    assert b"Deterministic Engine Evaluation" in r_detail.data
    assert b"Human Clinical SME Adjudication" in r_detail.data

    # 3. Case detail JSON API
    r_json = web_client.get("/pilot/CASE-PILOT-ADV-001?format=json")
    assert r_json.status_code == 200
    data = r_json.get_json()
    assert data["evaluation"]["case_id"] == "CASE-PILOT-ADV-001"

    # 4. Pilot evaluations API
    r_api = web_client.get("/api/pilot/evaluations")
    assert r_api.status_code == 200
    assert len(r_api.get_json()) == 36


# ==============================================================================
# 16. Execution Performance and Deterministic Throughput
# ==============================================================================

def test_execution_performance_and_latency():
    """Verify average execution latency is < 15ms per case."""
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        res = json.load(f)

    avg_ms = res["timings"]["average_ms_per_case"]
    assert avg_ms < 15.0, f"Average case latency was {avg_ms}ms, expected < 15ms"
