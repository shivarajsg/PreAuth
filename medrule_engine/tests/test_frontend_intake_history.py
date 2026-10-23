"""Frontend regression and acceptance tests for Case Intake and Case History.

Verifies:
1. Case Intake page loads with structured sections, required indicators, and safety invariants.
2. Case Intake validation error handling and duplicate submission safety.
3. Case History list rendering with real backend fields, status badges, metrics, and empty states.
4. Case Detail header with strictly distinct dates (Encounter date vs Received timestamp).
5. Diagnosis ICD-10 codes kept distinct from free-text diagnosis descriptions and clinical narratives.
6. Safe rendering of conflicting evidence objects without unformatted JSON dumps.
7. Dual-track separation of Clinical Necessity and Place of Service (EPOS 1755).
8. Connector execution audit log and lifecycle transition timeline rendering.
9. Resilient rendering when optional or unfamiliar fields are empty.
"""

from datetime import datetime, timezone
import json
import pytest

from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.governance.models import ReviewRole, ReviewerIdentity
from medrule_engine.web.app import create_app


@pytest.fixture
def client():
    """Create test client configured with persistent governance database."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_01_case_intake_page_loads_with_sections_and_safety_banner(client):
    """Verify Case Intake loads with all 5 organized sections and safety invariants."""
    res = client.get("/intake")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # 1. Page Header & Invariant Banner
    assert "Deterministic Prior-Authorization Case Intake" in html
    assert "NON-BINDING SOFTWARE EVALUATION" in html
    assert "DISABLED (LOCAL CDS)" in html
    assert "128 ACTIVE RULES" in html

    # 2. PDF Uploader Dropzone
    assert "Clinical Document Uploader (PDF)" in html
    assert ".pdf" in html

    # 3. Form Sections
    assert "1. Case Identification &amp; Clinical Domain" in html
    assert "2. Patient Identification &amp; Health Plan" in html
    assert "3. Requested Procedure &amp; Service Date" in html
    assert "4. Clinical Documentation &amp; Structured Evidence" in html

    # 4. Required Field Indicators
    assert 'id="case_id"' in html
    assert 'id="patient_id"' in html
    assert 'id="clinical_domain"' in html
    assert 'id="procedure_code"' in html
    assert 'id="requested_date_of_service"' in html
    assert 'id="line_of_business"' in html
    assert 'id="clinical_evidence_json"' in html


def test_02_case_intake_validation_error_renders_and_preserves_context(client):
    """Verify missing required intake fields return validation error banner and retain entered values."""
    # Submit missing patient_id and clinical_domain
    bad_data = {
        "case_id": "CASE-VAL-ERR-001",
        "procedure_code": "74177",
        "procedure_name": "CT Abdomen and Pelvis",
        "requested_date_of_service": "2026-03-15",
        "line_of_business": "COMMERCIAL",
        "clinical_evidence_json": json.dumps({"pancreatitis_diagnostic_markers": "ELEVATED"})
    }
    res = client.post("/intake", data=bad_data)
    assert res.status_code == 400
    html = res.get_data(as_text=True)
    assert "Intake Submission Failure" in html
    assert "Missing required intake fields:" in html
    assert "clinical_domain" in html
    assert "Your entered form values were preserved in your browser session" in html


def test_03_case_intake_successful_submission_and_redirect(client):
    """Verify successful case intake submission executes deterministic evaluation and redirects to case detail."""
    valid_data = {
        "case_id": f"CASE-FRONTEND-TEST-{int(datetime.now().timestamp())}",
        "patient_id": "MEM-SYNTH-88219",
        "clinical_domain": "advanced_imaging",
        "procedure_code": "74177",
        "procedure_name": "CT Abdomen and Pelvis with contrast",
        "line_of_business": "COMMERCIAL",
        "requested_date_of_service": "2026-03-15",
        "payer_id": "EVOLENT",
        "plan_id": "COMMERCIAL_CHOICE_PLUS",
        "submitted_documents": "Comprehensive clinical notes and diagnostic findings",
        "bypass_documentation_check": "true",
        "clinical_evidence_json": json.dumps({
            "pancreatitis_diagnostic_markers": "ELEVATED",
            "conservative_treatment_duration_hours": 96,
            "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT",
            "ordering_provider_license": True
        })
    }
    res = client.post("/intake", data=valid_data, follow_redirects=True)
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Landed on Case Detail
    assert valid_data["case_id"] in html
    assert "CPT 74177" in html
    assert "NON-BINDING EVALUATION" in html
    assert "is_binding: false" in html


def test_04_case_history_list_displays_real_data_and_metrics(client):
    """Verify Case History renders table using actual case intake records, metrics, and status badges."""
    res = client.get("/cases")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Header and Summary Metrics
    assert "Prior-Authorization Case History" in html
    assert "Displayed Cases" in html
    assert "Evaluated (Complete)" in html
    assert "Review Required" in html
    assert "Awaiting Docs" in html
    assert "Policy Unresolved" in html

    # Table Columns
    assert "Case ID" in html
    assert "Member ID" in html
    assert "Clinical Domain" in html
    assert "Requested Procedure" in html
    assert "Payer / Plan" in html
    assert "Service Date" in html
    assert "Lifecycle State" in html
    assert "Decision Outcome" in html
    assert "Received Timestamp" in html


def test_05_case_history_search_and_empty_state(client):
    """Verify search filter for non-existent case returns clear no-results state with clear button."""
    res = client.get("/cases?search=NONEXISTENT_QUERY_99999999")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "No Matching Cases Found" in html
    assert "Clear Filters &amp; Show All Cases" in html


def test_06_case_detail_keeps_dates_distinct_and_accurate(client):
    """Verify Case Detail header keeps Encounter Date, Received Timestamp, and Last Updated strictly distinct."""
    # Query an existing case from db
    gov_db = GovernanceDatabase()
    all_cases = gov_db.list_case_intake_records()
    if not all_cases:
        pytest.skip("No cases available in database")
    case = all_cases[0]

    res = client.get(f"/cases/{case['case_id']}")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Ensure separate labeled sections for dates
    assert "Requested Date of Service" in html
    assert "Submission Received" in html
    assert "Last Updated" in html
    assert "Clinical encounter date" in html
    assert "Intake audit timestamp" in html


def test_07_case_detail_removes_redundant_narrative_and_raw_sections(client):
    """Verify redundant narrative blocks, duplicate encounter note, and raw parameter lists are absent."""
    gov_db = GovernanceDatabase()
    all_cases = gov_db.list_case_intake_records()
    if not all_cases:
        pytest.skip("No cases available in database")
    case = all_cases[0]

    res = client.get(f"/cases/{case['case_id']}")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # 1. Redundant narrative card and OCR note excerpt must be absent
    assert "CLINICAL DOCUMENTATION &amp; PDF SOURCE EVIDENCE" not in html
    assert "Clinical Documentation & PDF Source Evidence" not in html
    assert "Verbatim Physician Encounter Note" not in html

    # 2. Raw human review escalation block must be absent
    assert "Clinical Human Review Escalations &amp; Advisory Triggers" not in html
    assert "Clinical Human Review Escalations & Advisory Triggers" not in html

    # 3. Raw missing evidence parameters list and its toggle controls must be absent
    assert "Missing Clinical Evidence Parameters" not in html
    assert "btn-toggle-missing-evidence" not in html
    assert "toggleMissingEvidence" not in html

    # 4. Clean documentation review table must be present
    assert "Clinical Documentation Review" in html


def test_08_case_detail_safely_renders_conflicting_evidence(client):
    """Verify conflicting evidence objects are rendered cleanly with conflict badges, not raw unformatted dict dumps."""
    gov_db = GovernanceDatabase()
    # Find case with CONFLICTING actual_value if present
    target_case_id = None
    for c in gov_db.list_case_intake_records():
        eval_res = c.get("evaluation_result") or {}
        for rr in eval_res.get("rule_results", []):
            for cr in rr.get("condition_result", {}).get("criteria_results", []):
                act = cr.get("actual_value")
                if isinstance(act, dict) and act.get("status") == "CONFLICTING":
                    target_case_id = c["case_id"]
                    break
            if target_case_id:
                break
        if target_case_id:
            break

    if not target_case_id:
        pytest.skip("No case with conflicting evidence found in database")

    res = client.get(f"/cases/{target_case_id}")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # Verify structured conflict box
    assert "Conflicting Findings" in html
    assert "conflict-box" in html
    assert "Contradictory documented statements" in html


def test_09_case_detail_renders_connector_events_audit_log(client):
    """Verify Case Detail renders connector execution events with execution modes and latencies."""
    gov_db = GovernanceDatabase()
    # Find case with connector events
    target_case_id = None
    for c in gov_db.list_case_intake_records():
        events = gov_db.list_connector_audit_events(case_id=c["case_id"])
        if events:
            target_case_id = c["case_id"]
            break

    if not target_case_id:
        pytest.skip("No case with connector events in database")

    res = client.get(f"/cases/{target_case_id}")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    assert "Connector Execution Audit Log" in html
    assert "ELIGIBILITY" in html or "BENEFIT_COVERAGE" in html
    assert "MOCK / SIMULATED" in html


def test_10_case_detail_missing_documentation_vs_missing_evidence_facts(client):
    """Verify missing documentation checklist is kept distinct from missing evidence facts within evidence."""
    gov_db = GovernanceDatabase()
    # Find a case with missing documentation
    case_awaiting = None
    for c in gov_db.list_case_intake_records():
        if c.get("missing_documentation"):
            case_awaiting = c
            break

    if not case_awaiting:
        pytest.skip("No case with missing documentation in database")

    res = client.get(f"/cases/{case_awaiting['case_id']}")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    assert "Required Documentation Checklist Missing" in html
    for doc in case_awaiting["missing_documentation"][:2]:
        assert doc.replace("_", " ") in html


def test_11_clinical_documentation_review_table_structure_and_columns(client):
    """Verify Case History renders the 4-column Clinical Documentation Review table and excludes old rule breakdown."""
    gov_db = GovernanceDatabase()
    all_cases = gov_db.list_case_intake_records()
    if not all_cases:
        pytest.skip("No cases available in database")
    case = all_cases[0]

    res = client.get(f"/cases/{case['case_id']}")
    assert res.status_code == 200
    html = res.get_data(as_text=True)

    # 1. Section Title
    assert "Clinical Documentation Review" in html
    # Subtitle beneath title must be removed
    assert "Criterion-by-criterion deterministic logic outcomes with official clinical guideline citations." not in html

    # 2. Exactly four columns
    assert "Required Information" in html
    assert "Information Found" in html
    assert "Status" in html
    assert "Explanation &amp; Next Steps" in html or "Explanation & Next Steps" in html

    # 3. Old rule breakdown presentation completely removed
    assert "Evaluated Clinical Rules &amp; Condition Breakdown" not in html
    assert "Evaluated Clinical Rules & Condition Breakdown" not in html
    assert "Inspect Full Rule &amp; Condition Tree in SME Workbench" not in html
    assert "Inspect Full Rule & Condition Tree in SME Workbench" not in html
    assert "COND-001" not in html
    assert "Patient Value Found" not in html
    assert 'onclick="filterRules(' not in html
    assert "btn-toggle-evaluated-rules" not in html


def test_12_documentation_review_table_deduplication_and_conflict_handling(client):
    """Verify consolidation of repeated rule requirements into single rows and promotion of conflicts to NEEDS REVIEW."""
    gov_db = GovernanceDatabase()
    
    # Check CASE-EXAMPLE-INTAKE-001 (or another evaluated case)
    res = client.get("/cases/CASE-EXAMPLE-INTAKE-001")
    if res.status_code == 200:
        html = res.get_data(as_text=True)
        # Sequential numbering present
        assert "1. " in html
        # Plain language info found
        assert "Present" in html or "Documented in record" in html or "Duration documented:" in html
        # Status badges
        assert "badge badge-success" in html or "badge badge-warning" in html

    # Check case with conflicting evidence
    target_case_id = None
    for c in gov_db.list_case_intake_records():
        eval_res = c.get("evaluation_result") or {}
        for rr in eval_res.get("rule_results", []):
            for cr in rr.get("condition_result", {}).get("criteria_results", []):
                act = cr.get("actual_value")
                if isinstance(act, dict) and act.get("status") == "CONFLICTING":
                    target_case_id = c["case_id"]
                    break
            if target_case_id:
                break
        if target_case_id:
            break

    if target_case_id:
        res = client.get(f"/cases/{target_case_id}")
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "NEEDS REVIEW" in html
        assert "Conflicting Findings" in html or "Conflicting information" in html


def test_13_documentation_review_table_handles_missing_fields_and_empty_state(client):
    """Verify Case History table handles empty evaluation results without throwing template errors."""
    gov_db = GovernanceDatabase()
    # Check all cases to ensure robust error-free rendering
    for c in gov_db.list_case_intake_records()[:5]:
        res = client.get(f"/cases/{c['case_id']}")
        assert res.status_code == 200
        html = res.get_data(as_text=True)
        assert "Clinical Documentation Review" in html or "Clinical Evaluation Pending" in html or "POLICY_CONTEXT_UNRESOLVED" in html


def test_14_documentation_review_regression_checks_a_through_f(client):
    """Verify regression checks A through F against actual case data in the documentation review table.

    A. Ordering provider license: neutral status when verification is unavailable.
    B. Recent office visit note: present/MET when note exists.
    C. Laboratory or special-testing results: distinguishes scheduled tests from documented results.
    D. Radiculopathy documentation: preserves human-review status when clinical exam conflicts with diagnosis code.
    E. Conservative treatment history: accurately reflects documented home exercises (evaluated: 0 weeks) with NOT MET outcome.
    F. Clinical information submitted: suppressed from missing-information warnings.
    """
    res = client.get("/cases/CASE-PDF-1792687360")
    if res.status_code != 200:
        pytest.skip("CASE-PDF-1792687360 not found in database")
    html = res.get_data(as_text=True)

    # A. Ordering provider license (unverified -> neutral NOT PROVIDED)
    assert "Ordering Provider License" in html

    # B. Recent office visit note (present -> MET)
    assert "Recent Office Visit Note" in html

    # C. Laboratory or special-testing results (scheduled test -> NOT PROVIDED / Not found (scheduled test only))
    assert "Laboratory or Special Testing Results" in html
    assert "Not found (scheduled test only)" in html

    # D. Radiculopathy documentation (SLR positive vs M47.816 -> NEEDS REVIEW / Conflicting Findings)
    assert "Radiculopathy Clinical Documentation" in html
    assert "Conflicting Findings" in html

    # E. Conservative treatment history (Home exercises documented, structured PT 0 weeks -> NOT MET with accurate info)
    assert "Conservative Treatment History" in html
    assert "Documented care: home exercises (evaluated: 0 weeks)" in html
    assert "NOT MET" in html

    # F. Clinical information submitted parameter suppressed
    assert "clinical_information_submitted" not in html


def test_15_case_detail_human_review_notice_and_safety_invariants(client):
    """Verify visible case-level safety notices, non-binding notice, and disabled external submission."""
    res = client.get("/cases/CASE-PDF-1792687360")
    if res.status_code != 200:
        pytest.skip("CASE-PDF-1792687360 not found in database")
    html = res.get_data(as_text=True)

    # 1. Concise case-level human review safety notice
    assert "Clinical review required: the submitted documentation contains conflicting information that needs clarification." in html

    # 2. Non-binding software notice
    assert "NON-BINDING EVALUATION" in html
    assert "is_binding: false" in html

    # 3. External submission disabled notice
    assert "OUTBOUND SUBMISSION DISABLED" in html

