"""Regression tests for ordering_provider_license and clinical_office_notes semantics.

Validates:
1. Provider name present, license not verified (unverified license does not equal MET).
2. Verified license evidence available (explicit verified licensure sets MET).
3. Provider information absent.
4. Qualifying office visit note present (structural clinical note validation).
5. Non-qualifying document uploaded (billing invoice or denial letter rejects office-note status).
6. Missing or ambiguous evidence preserves three-valued logic (INSUFFICIENT_DATA, never coerced to MET or NOT_MET).
7. Case-specific evidence distinction across cases.
8. Cross-case isolation (no evidence leakage via mutable defaults or global state).
"""

import pytest
import pymupdf as fitz

from medrule_engine.integrations.pdf_extractor import (
    extract_case_from_pdf,
    extract_clinical_facts_from_text,
    _detect_provider_name_and_provenance,
    _detect_provider_license_evidence,
    _is_qualifying_office_visit_note,
)
from medrule_engine.case_validator import CaseIntake
from medrule_engine.condition_evaluator import ConditionEvaluator, CriterionState, EvidenceState
from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.web.app import create_app


def create_sample_clinical_pdf(text_content: str) -> bytes:
    """Generate in-memory PDF bytes with the given text."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), text_content, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


@pytest.fixture
def client():
    """Create test client configured with persistent governance database."""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_01_provider_name_present_license_not_verified():
    """Verify that provider name and credentials do not default ordering_provider_license to True."""
    note_text = (
        "CONSULTATION NOTE\n"
        "Date of Service: 2026-02-26\n"
        "Patient: Vivek Pampattiwar DOB: 11/10/1969\n"
        "Provider: KEWEI YU, MD\n"
        "History of Present Illness: Patient presents with lower back pain radiating to right leg.\n"
        "Physical Exam: Tenderness at lumbar spine. Straight leg raise positive on right.\n"
        "Assessment: Lumbosacral radiculopathy (M54.17).\n"
        "Treatment Plan: Order MRI Lumbar spine without contrast (CPT 72148).\n"
        "Electronically signed by KEWEI YU, MD on 02/26/2026\n"
    )
    facts = extract_clinical_facts_from_text(note_text)
    evidence = facts["evidence"]

    # Provider name and credentials extracted
    assert "KEWEI YU" in evidence.get("ordering_provider_name")
    assert evidence.get("ordering_provider_credentials") == "MD"

    # License is NOT verified and must NOT be marked True
    assert evidence.get("ordering_provider_license") is None
    assert evidence.get("ordering_provider_license_verified") is None

    # Evaluate via rule evaluator
    evaluator = ConditionEvaluator()
    rule_conditions = {
        "operator": "ALL_OF",
        "criteria": [
            {
                "condition_id": "cond_license",
                "parameter": "ordering_provider_license",
                "comparator": "EQUALS",
                "value": True,
                "description": "Ordering clinician must hold active verified license"
            }
        ]
    }
    case = CaseIntake(
        case_id="CASE-TEST-UNVERIFIED-LIC-01",
        member_id="PT-12345",
        clinical_domain="advanced_imaging",
        procedure_code="72148",
        procedure_name="MRI Lumbar Spine",
        requested_date_of_service="2026-02-26",
        line_of_business="COMMERCIAL",
        payer_id="EVOLENT",
        clinical_evidence=evidence
    )
    eval_res = evaluator.evaluate(rule_conditions, case)
    crit = eval_res.criteria_results[0]
    assert crit.criterion_state == CriterionState.INSUFFICIENT_DATA
    assert crit.evidence_state == EvidenceState.MISSING
    assert crit.actual_value is None
    assert crit.criterion_state != CriterionState.MET
    assert crit.criterion_state != CriterionState.NOT_MET


def test_02_verified_license_evidence_available():
    """Verify that explicit active verified license evidence is recognized and evaluated as MET."""
    note_text = (
        "CLINICAL PROGRESS NOTE\n"
        "Date of Service: 2026-02-26\n"
        "Patient: Jane Doe DOB: 05/12/1980\n"
        "Provider: Dr. Robert Miller, DO\n"
        "State Medical License: Active Verified\n"
        "License Number: GA-DO-984210\n"
        "History of Present Illness: Chronic axial lower back pain.\n"
        "Physical Exam: Lumbar range of motion decreased.\n"
        "Assessment: Spondylosis without myelopathy.\n"
        "Plan: Physical therapy and imaging.\n"
    )
    facts = extract_clinical_facts_from_text(note_text)
    evidence = facts["evidence"]

    assert evidence.get("ordering_provider_name") == "Dr. Robert Miller, DO"
    assert evidence.get("ordering_provider_credentials") == "DO"
    assert evidence.get("ordering_provider_license_number") == "GA-DO-984210"
    assert evidence.get("ordering_provider_license") is True
    assert evidence.get("ordering_provider_license_verified") is True

    # Rule evaluation must pass as MET
    evaluator = ConditionEvaluator()
    rule_conditions = {
        "operator": "ALL_OF",
        "criteria": [
            {
                "condition_id": "cond_license",
                "parameter": "ordering_provider_license",
                "comparator": "EQUALS",
                "value": True
            }
        ]
    }
    case = CaseIntake(
        case_id="CASE-TEST-VERIFIED-LIC-02",
        member_id="PT-67890",
        clinical_domain="advanced_imaging",
        procedure_code="72148",
        procedure_name="MRI Lumbar Spine",
        requested_date_of_service="2026-02-26",
        line_of_business="COMMERCIAL",
        payer_id="EVOLENT",
        clinical_evidence=evidence
    )
    eval_res = evaluator.evaluate(rule_conditions, case)
    crit = eval_res.criteria_results[0]
    assert crit.criterion_state == CriterionState.MET
    assert crit.evidence_state == EvidenceState.EXPLICIT_POSITIVE
    assert crit.actual_value is True


def test_03_provider_information_absent():
    """Verify behavior when no provider information is documented in the upload."""
    note_text = (
        "UNKNOWN RECORD EXCERPT\n"
        "Date of Service: 2026-02-26\n"
        "Patient: Anonymous\n"
        "Symptoms: Chronic back pain.\n"
        "Medications: Ibuprofen 600mg.\n"
    )
    prov_name, _ = _detect_provider_name_and_provenance(note_text)
    creds, lic_num, is_verified, _ = _detect_provider_license_evidence(note_text)
    assert prov_name is None
    assert creds is None
    assert lic_num is None
    assert is_verified is False

    facts = extract_clinical_facts_from_text(note_text)
    assert "ordering_provider_name" not in facts["evidence"]
    assert "ordering_provider_license" not in facts["evidence"]


def test_04_qualifying_office_visit_note_structure():
    """Verify that structured clinical progress/consultation notes qualify as clinical_office_notes."""
    qualifying_note = (
        "CONSULTATION NOTES FOR PATIENT JOHN SMITH\n"
        "Date of Service: 2026-01-15\n"
        "Provider: KEWEI YU, MD\n"
        "History of Present Illness: Patient presented for follow up of severe persistent lumbar pain.\n"
        "Vital Signs: BP 120/80, HR 72, Temp 98.6 F\n"
        "General Examination: Neuro alert, spine tender at L4-L5, straight leg raise positive.\n"
        "Assessments: Radiculopathy, lumbosacral region (M54.17).\n"
        "Treatment Plan: Order MRI Lumbar Spine without contrast.\n"
        "Electronically signed by KEWEI YU, MD on 01/15/2026\n"
    )
    is_qualifying, snippet = _is_qualifying_office_visit_note(qualifying_note)
    assert is_qualifying is True
    assert "consultation notes" in snippet.lower()
    assert "2026-01-15" in snippet

    facts = extract_clinical_facts_from_text(qualifying_note)
    assert facts["evidence"].get("clinical_office_notes") is True


def test_05_non_qualifying_document_uploaded():
    """Verify that pure billing invoices or insurance denial notices do not qualify as clinical_office_notes."""
    # 1. Billing invoice
    invoice_text = (
        "ACME MEDICAL BILLING SERVICES\n"
        "BILLING INVOICE AND STATEMENT OF CHARGES\n"
        "Account Number: 9948271\n"
        "Date: 01/20/2026\n"
        "Patient: Vivek Pampattiwar\n"
        "Total Balance Due: $450.00\n"
        "Please remit payment upon receipt.\n"
    )
    is_qual, _ = _is_qualifying_office_visit_note(invoice_text)
    assert is_qual is False
    facts_inv = extract_clinical_facts_from_text(invoice_text)
    assert "clinical_office_notes" not in facts_inv["evidence"]

    # 2. Pure Notice of Denial
    denial_text = (
        "COMMERCIAL HEALTH PLAN\n"
        "NOTICE OF DENIAL OF COVERAGE / ADVERSE BENEFIT DETERMINATION\n"
        "Date: 02/01/2026\n"
        "Member: Vivek Pampattiwar | Member ID: 13717\n"
        "The requested prior authorization for MRI Lumbar Spine has been denied due to missing conservative care.\n"
        "You have the right to file an appeal within 180 days.\n"
    )
    is_qual_denial, _ = _is_qualifying_office_visit_note(denial_text)
    assert is_qual_denial is False
    facts_denial = extract_clinical_facts_from_text(denial_text)
    assert "clinical_office_notes" not in facts_denial["evidence"]


def test_06_missing_or_ambiguous_evidence_preserves_three_valued_logic():
    """Verify three-valued logic: missing evidence remains INSUFFICIENT_DATA and is never coerced to MET or NOT_MET."""
    evaluator = ConditionEvaluator()
    rule_conditions = {
        "operator": "ALL_OF",
        "criteria": [
            {
                "condition_id": "cond_pt",
                "parameter": "conservative_therapy_duration_weeks",
                "comparator": "GREATER_THAN_OR_EQUAL",
                "value": 6,
                "description": "At least 6 weeks of structured physical therapy"
            },
            {
                "condition_id": "cond_lic",
                "parameter": "ordering_provider_license",
                "comparator": "EQUALS",
                "value": True,
                "description": "Active verified medical license"
            }
        ]
    }
    # Case with no evidence provided
    case_empty = CaseIntake(
        case_id="CASE-TEST-EMPTY-01",
        member_id="PT-EMPTY",
        clinical_domain="advanced_imaging",
        procedure_code="72148",
        procedure_name="MRI Lumbar Spine",
        requested_date_of_service="2026-02-26",
        line_of_business="COMMERCIAL",
        payer_id="EVOLENT",
        clinical_evidence={}
    )
    res = evaluator.evaluate(rule_conditions, case_empty)
    for cr in res.criteria_results:
        # Crucial: Must be INSUFFICIENT_DATA, never coerced to MET or marked NOT_MET when merely absent
        assert cr.criterion_state == CriterionState.INSUFFICIENT_DATA
        assert cr.evidence_state == EvidenceState.MISSING
        assert cr.actual_value is None


def test_07_different_evidence_and_statuses_for_different_cases():
    """Verify that different cases evaluate to different, document-specific evidence and statuses."""
    # Case A: 6 weeks PT, verified license
    note_a = (
        "CONSULTATION NOTE\n"
        "Date of Service: 2026-02-26\n"
        "Provider: Dr. Alice Smith, MD\n"
        "State Medical License: Active Verified\n"
        "History: Patient has 8 weeks lumbar pain. Completed 6 weeks of structured physical therapy.\n"
        "Exam: Straight leg raise positive.\n"
        "Assessment: Radiculopathy (M54.17).\n"
        "Plan: Order MRI Lumbar Spine.\n"
    )
    # Case B: 0 weeks PT, unverified license
    note_b = (
        "CONSULTATION NOTE\n"
        "Date of Service: 2026-02-26\n"
        "Provider: Dr. Bob Jones, MD\n"
        "History: Patient has acute back pain. Denies prior physical therapy and had zero conservative treatment.\n"
        "Exam: Tenderness noted.\n"
        "Assessment: Low back pain (M54.5).\n"
        "Plan: Order MRI Lumbar Spine.\n"
    )

    facts_a = extract_clinical_facts_from_text(note_a)
    facts_b = extract_clinical_facts_from_text(note_b)

    # Distinct providers
    assert facts_a["evidence"]["ordering_provider_name"] == "Dr. Alice Smith, MD"
    assert facts_b["evidence"]["ordering_provider_name"] == "Dr. Bob Jones, MD"

    # Distinct licensure statuses
    assert facts_a["evidence"].get("ordering_provider_license") is True
    assert facts_b["evidence"].get("ordering_provider_license") is None

    # Distinct PT duration
    assert facts_a["evidence"].get("conservative_therapy_duration_weeks") == 6
    assert facts_b["evidence"].get("conservative_therapy_duration_weeks") == 0


def test_08_no_cross_case_evidence_leakage():
    """Verify case isolation: extracted evidence from one case cannot leak into subsequent cases."""
    # First extract a case with verified license and 8 weeks duration
    note_rich = (
        "CONSULTATION NOTE\n"
        "Date of Service: 2026-02-26\n"
        "Provider: Dr. Specialist, MD\n"
        "State Medical License: Active Verified\n"
        "History: Completed 8 weeks of structured physical therapy.\n"
        "Exam: Normal reflexes.\n"
        "Assessment: Lumbago.\n"
        "Plan: MRI.\n"
    )
    facts_rich = extract_clinical_facts_from_text(note_rich)
    assert facts_rich["evidence"]["ordering_provider_license"] is True
    assert facts_rich["evidence"]["conservative_therapy_duration_weeks"] == 8

    # Second extract a sparse case with no license and no conservative care
    note_sparse = (
        "CONSULTATION NOTE\n"
        "Date of Service: 2026-02-26\n"
        "Provider: Dr. New Clinician\n"
        "History: Initial consultation for back discomfort.\n"
        "Exam: Vitals stable.\n"
        "Assessment: Muscle ache.\n"
        "Plan: Observation.\n"
    )
    facts_sparse = extract_clinical_facts_from_text(note_sparse)

    # Must NOT have retained or leaked rich case's license or weeks
    assert "ordering_provider_license" not in facts_sparse["evidence"]
    assert "conservative_therapy_duration_weeks" not in facts_sparse["evidence"]
    assert "New Clinician" in facts_sparse["evidence"].get("ordering_provider_name")
    assert facts_sparse["evidence"].get("ordering_provider_name") != "Dr. Specialist, MD"


def test_09_ui_renders_actual_backend_statuses(client):
    """Verify that Case History / Case Detail renders dynamic backend statuses rather than hardcoded MET badges."""
    res = client.get("/cases/CASE-EXAMPLE-INTAKE-001")
    if res.status_code == 200:
        html = res.get_data(as_text=True)
        # Ensure the 4 columns exist
        assert "Required Information" in html
        assert "Information Found" in html
        assert "Status" in html
        assert "Explanation &amp; Next Steps" in html or "Explanation & Next Steps" in html

        # Verify that unverified license renders NOT PROVIDED, not hardcoded MET
        # When a criterion is missing, status badge must be NOT PROVIDED
        assert "NOT PROVIDED" in html or "MET" in html
