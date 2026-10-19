"""Unit and integration tests for clinical PDF extraction and intake auto-fill."""

import io
import json
import pymupdf as fitz
import pytest

from medrule_engine.integrations.pdf_extractor import extract_case_from_pdf
from medrule_engine.web.app import create_app


def create_sample_clinical_pdf(text_content: str) -> bytes:
    """Generate in-memory PDF bytes with the given text."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), text_content, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_extract_case_from_pancreatitis_notes():
    """Verify extraction of imaging criteria from doctor's progress notes."""
    sample_text = (
        "CLINICAL PROGRESS NOTE\n"
        "Patient: Jane Doe | Member ID: MEM-SYNTH-88219\n"
        "Date of Service: 2026-03-20 | Provider: Dr. Michael Vance, MD\n"
        "Diagnosis: Acute Pancreatitis (K85.90)\n"
        "Clinical Narrative:\n"
        "Patient presents with severe epigastric abdominal pain and elevated pancreatitis markers.\n"
        "Conservative therapy continued for 96 hours without resolution.\n"
        "Right upper quadrant ultrasound performed showing no gallstones or dilated common bile duct.\n"
        "Requesting: CPT 74177 - CT Abdomen and Pelvis with IV contrast.\n"
        "Coverage: Commercial PPO Choice Plus\n"
    )
    pdf_bytes = create_sample_clinical_pdf(sample_text)
    result = extract_case_from_pdf(pdf_bytes, filename="jane_doe_clinical_note.pdf")

    assert result["status"] == "SUCCESS"
    assert result["filename"] == "jane_doe_clinical_note.pdf"
    assert result["pages_analyzed"] == 1

    fields = result["extracted_fields"]
    assert fields["patient_id"] == "MEM-SYNTH-88219"
    assert fields["clinical_domain"] == "advanced_imaging"
    assert fields["procedure_code"] == "74177"
    assert "CT Abdomen and Pelvis" in fields["procedure_name"]
    assert fields["line_of_business"] == "COMMERCIAL"
    assert fields["requested_date_of_service"] == "2026-03-20"
    assert fields["evidence"]["pancreatitis_diagnostic_markers"] == "ELEVATED"
    assert fields["evidence"]["conservative_treatment_duration_hours"] == 96
    assert fields["evidence"]["ultrasound_findings"] == "NO_GALLSTONES_OR_DILATED_DUCT"


def test_extract_case_from_cardiology_notes():
    """Verify extraction of cardiology catheterization criteria."""
    sample_text = (
        "CARDIOLOGY CONSULTATION\n"
        "Member: MEM-CARD-99120 | DOB: 1964-05-12\n"
        "Date: 2026-04-10 | Attending: Dr. Robert Taylor, MD\n"
        "Chief Complaint: Progressive chest pressure.\n"
        "Assessment: Coronary Artery Disease. Exercise stress test revealed high risk ischemia.\n"
        "Patient describes Canadian Class III/IV angina symptoms despite medical therapy.\n"
        "Plan: Proceed with Left Heart Catheterization (CPT 93458) and coronary angiogram.\n"
        "Insurance: Medicare Advantage Premier\n"
    )
    pdf_bytes = create_sample_clinical_pdf(sample_text)
    result = extract_case_from_pdf(pdf_bytes, filename="cardiology_consult.pdf")

    assert result["status"] == "SUCCESS"
    fields = result["extracted_fields"]
    assert fields["clinical_domain"] == "cardiology"
    assert fields["procedure_code"] == "93458"
    assert fields["line_of_business"] == "MEDICARE_ADVANTAGE"
    assert fields["evidence"]["stress_test_findings"] == "HIGH_RISK_ISCHEMIA"
    assert fields["evidence"]["angina_symptoms"] == "CANADIAN_CLASS_III_IV"


def test_api_extract_pdf_endpoint():
    """Test web endpoint /api/cases/extract-pdf."""
    app = create_app()
    client = app.test_client()

    sample_text = (
        "ORTHOPEDIC NOTE\n"
        "Patient: MEM-SYNTH-55123\n"
        "Dr. Wilson | Date: 2026-03-15\n"
        "Severe tricompartmental osteoarthritis of right knee (Grade IV advanced).\n"
        "Failed conservative therapy over past 6 months including physical therapy and injections.\n"
        "Severe functional impairment in activities of daily living.\n"
        "Procedure: Total Knee Arthroplasty (CPT 27447)\n"
    )
    pdf_bytes = create_sample_clinical_pdf(sample_text)

    # Valid PDF upload
    data = {
        "pdf_file": (io.BytesIO(pdf_bytes), "orthopedic_tka_note.pdf")
    }
    resp = client.post("/api/cases/extract-pdf", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    res_json = resp.get_json()
    assert res_json["status"] == "SUCCESS"
    assert res_json["extracted_fields"]["procedure_code"] == "27447"
    assert res_json["extracted_fields"]["clinical_domain"] == "musculoskeletal_surgery"
    assert "details" in res_json
    assert res_json["details"]["procedure_code"] == "27447"

    # Invalid file type
    data_invalid = {
        "pdf_file": (io.BytesIO(b"not a pdf"), "test.txt")
    }
    resp_invalid = client.post("/api/cases/extract-pdf", data=data_invalid, content_type="multipart/form-data")
    assert resp_invalid.status_code == 400
    assert "Only PDF files" in resp_invalid.get_json()["error"]


def test_extract_and_evaluate_dr_yu_lumbar_mri_note():
    """Verify extraction and full deterministic evaluation of Dr. Yu Lumbar Spine MRI note."""
    sample_text = (
        "PRE-CERTIFICATION CLINICAL PROGRESS NOTE\n"
        "Provider: Dr. Yu, MD | Specialty: Spine & Orthopedics\n"
        "Date of Service: 2025-02-26\n"
        "Patient: John Smith | Coverage: Commercial PPO Centene Ambetter\n"
        "Diagnosis: Muscle spasm of back (M62.838) with lumbosacral radiculopathy.\n"
        "Clinical Summary:\n"
        "Patient has experienced lower back pain with right lower extremity radiating pain for 8 weeks.\n"
        "Patient completed 6 weeks of structured physical therapy and oral NSAIDs without functional improvement.\n"
        "No evidence of acute cauda equina syndrome, bladder or bowel incontinence.\n"
        "Order: Pre-certification for MRI Lumbar Spine without contrast (CPT 72148).\n"
    )
    pdf_bytes = create_sample_clinical_pdf(sample_text)
    result = extract_case_from_pdf(pdf_bytes, filename="DrYuNotesForMRIPre-certificationA.pdf")

    assert result["status"] == "SUCCESS"
    assert result["filename"] == "DrYuNotesForMRIPre-certificationA.pdf"
    
    fields = result["extracted_fields"]
    assert fields["clinical_domain"] == "advanced_imaging"
    assert fields["procedure_code"] == "72148"
    assert "MRI Lumbar Spine" in fields["procedure_name"]
    assert fields["line_of_business"] == "COMMERCIAL"
    assert fields["requested_date_of_service"] == "2026-02-26"
    assert fields["evidence"]["lumbar_radiculopathy_present"] is True
    assert fields["evidence"]["conservative_therapy_duration_weeks"] >= 6
    assert fields["evidence"]["ordering_provider_license"] is True

    # Check details object for UI
    details = result["details"]
    assert "Dr. Yu" in details["ordering_provider"]
    assert "72148" in details["procedure_code"]
    assert "M62.838" in details["diagnosis_icd10"]
    assert len(details["key_findings"]) >= 3

    # Now verify that intake service evaluates it into EVALUATED_NON_BINDING without POLICY_CONTEXT_UNRESOLVED
    app = create_app()
    client = app.test_client()
    intake_payload = {
        "case_id": "CASE-TEST-DR-YU-001",
        "patient_id": fields["patient_id"],
        "clinical_domain": fields["clinical_domain"],
        "procedure_code": fields["procedure_code"],
        "procedure_name": fields["procedure_name"],
        "line_of_business": fields["line_of_business"],
        "requested_date_of_service": fields["requested_date_of_service"],
        "payer_id": fields["payer_id"],
        "plan_id": fields["plan_id"],
        "submitted_documents": [fields["submitted_documents"]],
        "clinical_evidence": fields["evidence"],
        "bypass_documentation_check": True
    }
    resp = client.post("/api/cases/intake", json=intake_payload)
    assert resp.status_code == 201
    intake_res = resp.get_json()
    assert intake_res["lifecycle_state"] in ("EVALUATED_NON_BINDING", "MANUAL_REVIEW_REQUIRED")
    assert intake_res["evaluation_result"] is not None
    assert intake_res["evaluation_result"]["assessment_status"] in ("NON_BINDING_MEETS_CRITERIA", "NON_BINDING_DOES_NOT_MEET_CRITERIA", "NON_BINDING_MANUAL_REVIEW_REQUIRED", "MANUAL_REVIEW_REQUIRED")


def test_intake_form_submission_renders_full_pdf_details():
    """Verify that submitting the intake form with extracted PDF details renders full details on case evaluation page."""
    app = create_app()
    client = app.test_client()

    form_data = {
        "case_id": "CASE-FORM-TEST-001",
        "patient_id": "PT-DR-YU-88219",
        "clinical_domain": "advanced_imaging",
        "procedure_code": "72148",
        "procedure_name": "MRI Lumbar Spine without contrast",
        "line_of_business": "COMMERCIAL",
        "requested_date_of_service": "2026-02-26",
        "payer_id": "CENTENE",
        "plan_id": "COMMERCIAL_CHOICE_PLUS",
        "submitted_documents": "DrYuNotesForMRIPre-certificationA.pdf, Comprehensive clinical notes",
        "clinical_evidence_json": json.dumps({
            "lumbar_radiculopathy_present": True,
            "conservative_therapy_duration_weeks": 6,
            "ordering_provider_license": True,
            "suspected_cauda_equina_syndrome": False
        }),
        "bypass_documentation_check": "true",
        "ordering_provider": "Dr. Yu, MD",
        "diagnosis_icd10": "M62.838",
        "diagnosis_description": "Other muscle spasm / Lumbar radicular syndrome",
        "source_pdf_filename": "DrYuNotesForMRIPre-certificationA.pdf",
        "clinical_narrative_excerpt": "Patient has severe radiating back pain for 8 weeks. Completed 6 weeks physical therapy.",
        "key_findings_json": json.dumps([
            "Diagnosis: Other muscle spasm / Lumbar radicular syndrome (ICD-10 M62.838)",
            "Ordering Physician: Dr. Yu, MD",
            "Requested Procedure: MRI Lumbar Spine without contrast (CPT 72148)",
            "Prior conservative therapy completed (6 weeks)"
        ]),
        "pdf_details_json": json.dumps({
            "patient_id": "PT-DR-YU-88219",
            "patient_age": "54 years",
            "patient_gender": "Male",
            "ordering_provider": "Dr. Yu, MD",
            "provider_specialty": "Spine & Orthopedics",
            "facility_name": "Regional Spine Center",
            "procedure_code": "72148",
            "procedure_name": "MRI Lumbar Spine without contrast",
            "diagnosis_icd10": "M62.838",
            "diagnosis_description": "Other muscle spasm / Lumbar radicular syndrome",
            "filename": "DrYuNotesForMRIPre-certificationA.pdf",
            "narrative_excerpt": "Patient has severe radiating back pain for 8 weeks. Completed 6 weeks physical therapy."
        })
    }

    resp = client.post("/intake", data=form_data, follow_redirects=True)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)

    # Verify clinical determination and absence of unresolved state
    assert "POLICY_CONTEXT_UNRESOLVED" not in html
    assert "Clinical Evaluation Pending" not in html

    # Verify PDF details card rendered on evaluation report
    assert "CLINICAL DOCUMENTATION &amp; PDF SOURCE EVIDENCE" in html
    assert "DrYuNotesForMRIPre-certificationA.pdf" in html
    assert "Dr. Yu, MD" in html
    assert "M62.838" in html
    assert "MRI Lumbar Spine without contrast" in html
    assert "Prior conservative therapy completed (6 weeks)" in html
    assert "Patient has severe radiating back pain for 8 weeks" in html


