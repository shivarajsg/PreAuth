"""Script to execute and verify the 9 clinical synthetic test cases for Step 3 Task B and Task C."""

import json
from pathlib import Path
import pymupdf as fitz

from medrule_engine.case_validator import CaseValidator
from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.integrations.pdf_extractor import extract_case_from_pdf
from medrule_engine.policy_router import PolicyRouter
from medrule_engine.rule_registry import RuleRegistry
from medrule_engine.decision_tree import DecisionTreeEngine, DecisionOutcome, DecisionTrack

def create_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), text, fontsize=11)
    b = doc.tobytes()
    doc.close()
    return b

# Define the 9 synthetic clinical test cases
CASES = {
    "1_lumbar_mri_supported": {
        "text": (
            "PRE-CERTIFICATION CLINICAL NOTE\n"
            "Patient: John Smith | ID: MEM-LUMB-0101 | DOB: 1978-04-12\n"
            "Date of Service: 2026-03-15 | Provider: Dr. Alan Grant, MD\n"
            "Facility: Outpatient Diagnostic Center\n"
            "Diagnosis: Lumbar radiculopathy (M54.16)\n"
            "Clinical History: 48-year-old male with severe lower back pain radiating into right lower extremity past knee for 8 weeks.\n"
            "Exam: Positive straight leg raise on right, diminished right Achilles reflex.\n"
            "Conservative Management: Completed 8 weeks of supervised physical therapy and oral NSAIDs (Meloxicam) without improvement.\n"
            "Red Flags: No bowel or bladder dysfunction, no cauda equina syndrome, no progressive motor deficit.\n"
            "Request: MRI Lumbar Spine without contrast (CPT 72148).\n"
            "Insurance: Commercial PPO Centene\n"
        ),
        "expected_domain": "advanced_imaging",
        "expected_cpt": "72148",
        "expected_evidence": {
            "lumbar_radiculopathy_present": True,
            "conservative_therapy_duration_weeks": 8,
            "suspected_cauda_equina_syndrome": False
        }
    },
    "2_knee_mri_supported": {
        "text": (
            "ORTHOPEDIC CLINICAL NOTE\n"
            "Patient: Sarah Walker | ID: MEM-KNEE-0202 | DOB: 1985-09-20\n"
            "Date of Service: 2026-04-10 | Provider: Dr. Rebecca Sterling, MD\n"
            "Diagnosis: Internal derangement of left knee (M23.92)\n"
            "History: Patient sustained twisting injury during tennis match 5 weeks ago.\n"
            "Exam: Moderate joint effusion present in left knee. Tenderness along medial joint line.\n"
            "Positive McMurray test indicating medial meniscal tear.\n"
            "Failed 4 weeks of structured physical therapy, rest, and ibuprofen.\n"
            "Prior Imaging: Weight-bearing radiographs completed showing no fracture or advanced joint space narrowing.\n"
            "Order: MRI Left Knee without contrast (CPT 73721).\n"
            "Coverage: Medicare Advantage\n"
        ),
        "expected_domain": "advanced_imaging",
        "expected_cpt": "73721",
        "expected_evidence": {
            "laterality": "LEFT",
            "anatomy_region": "KNEE",
            "meniscal_tear_suspected": True,
            "joint_effusion_present": True,
            "weight_bearing_radiographs_completed": True
        }
    },
    "3_brain_mri_supported": {
        "text": (
            "NEUROLOGY PROGRESS NOTE\n"
            "Patient: Thomas Anderson | ID: MEM-BRAIN-0303 | DOB: 1970-11-05\n"
            "Date of Service: 2026-03-25 | Provider: Dr. Charles Xavier, MD\n"
            "Chief Complaint: Progressive unilateral temporal headache with new right arm weakness.\n"
            "Physical Exam: Right-sided focal neurological deficit present (3/5 upper extremity weakness).\n"
            "Assessment: Subacute focal neurological deficit, suspected intracranial neoplasm or demyelinating process.\n"
            "History of 1 new-onset adult generalized seizure last week.\n"
            "Request: MRI Brain without and with IV contrast (CPT 70553).\n"
            "Insurance: Commercial PPO Choice Plus\n"
        ),
        "expected_domain": "advanced_imaging",
        "expected_cpt": "70553",
        "expected_evidence": {
            "headache_documented": True,
            "focal_neurological_deficit_present": True,
            "seizures_documented": True
        }
    },
    "4_ct_imaging_supported": {
        "text": (
            "EMERGENCY MEDICINE / GASTROENTEROLOGY NOTE\n"
            "Patient: Maria Santos | ID: MEM-CT-0404 | DOB: 1968-07-14\n"
            "Date of Service: 2026-03-22 | Provider: Dr. Gregory House, MD\n"
            "Chief Complaint: Severe persistent epigastric abdominal pain radiating to back.\n"
            "Labs: Serum lipase > 3x upper limit of normal (pancreatitis diagnostic markers elevated).\n"
            "Clinical Course: Observation and conservative IV fluid resuscitation continued for 72 hours without clinical improvement.\n"
            "Right upper quadrant ultrasound performed showing no gallstones or dilated common bile duct.\n"
            "Request: CT Abdomen and Pelvis with IV contrast (CPT 74177).\n"
            "Insurance: Medicaid Complete\n"
        ),
        "expected_domain": "advanced_imaging",
        "expected_cpt": "74177",
        "expected_evidence": {
            "abdominal_pain_documented": True,
            "pancreatitis_diagnostic_markers": "ELEVATED",
            "conservative_treatment_duration_hours": 72,
            "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT"
        }
    },
    "5_interventional_pain_supported": {
        "text": (
            "INTERVENTIONAL PAIN MANAGEMENT CONSULT\n"
            "Patient: David Bowman | ID: MEM-IPM-0505 | DOB: 1975-02-18\n"
            "Date of Service: 2026-04-05 | Provider: Dr. Leonard McCoy, MD\n"
            "Diagnosis: Lumbar disc herniation with L5-S1 radiculopathy (M54.16).\n"
            "History: Radicular pain persisting for 12 weeks refractory to conservative measures.\n"
            "Completed 8 weeks of physical therapy and oral analgesics without functional relief.\n"
            "Prior MRI shows L5-S1 disc herniation with nerve root compression.\n"
            "Recommendation: Lumbar interlaminar epidural steroid injection with fluoroscopy (CPT 62323).\n"
            "Place of Service: Ambulatory Surgical Center (POS 24)\n"
            "Insurance: Commercial PPO Centene\n"
        ),
        "expected_domain": "interventional_pain_management",
        "expected_cpt": "62323",
        "expected_evidence": {
            "lumbar_radiculopathy_present": True,
            "conservative_therapy_duration_weeks": 8,
            "place_of_service_code": "POS_24"
        }
    },
    "6_missing_required_info": {
        "text": (
            "CLINICAL PROGRESS NOTE\n"
            "Patient: Incomplete Case | ID: MEM-MISS-0606 | DOB: 1982-01-01\n"
            "Date of Service: 2026-03-20 | Provider: Dr. Jane Doe, MD\n"
            "Chief Complaint: Patient has low back pain.\n"
            "Exam: Mild back tenderness.\n"
            "Request: Pre-certification for MRI Lumbar Spine (CPT 72148).\n"
            "Insurance: Commercial PPO Centene\n"
        ),
        "expected_domain": "advanced_imaging",
        "expected_cpt": "72148",
        "expected_missing": ["lumbar_radiculopathy_present", "conservative_therapy_duration_weeks"]
    },
    "7_explicit_negative_findings": {
        "text": (
            "CLINICAL NOTE - EXPLICIT NEGATIVE EVIDENCE\n"
            "Patient: Robert Stone | ID: MEM-NEG-0707 | DOB: 1979-05-12\n"
            "Date of Service: 2026-03-18 | Provider: Dr. Mark Sloan, MD\n"
            "Chief Complaint: Localized axial lower back pain.\n"
            "Review of Systems: Patient denies radiculopathy, denies radiating leg pain, denies numbness or tingling.\n"
            "Exam: Motor strength 5/5 bilateral lower extremities. Reflexes symmetric. Negative straight leg raise.\n"
            "No neurological deficit. No cauda equina syndrome.\n"
            "Conservative Management: Patient has not completed any physical therapy.\n"
            "Request: MRI Lumbar Spine without contrast (CPT 72148).\n"
            "Coverage: Commercial PPO Centene\n"
        ),
        "expected_domain": "advanced_imaging",
        "expected_cpt": "72148",
        "expected_evidence": {
            "lumbar_radiculopathy_present": False,
            "radicular_pain_confirmed": False,
            "suspected_cauda_equina_syndrome": False,
            "conservative_therapy_duration_weeks": 0
        }
    },
    "8_contradictory_statements": {
        "text": (
            "CLINICAL NOTE - CONTRADICTORY DOCUMENTATION\n"
            "Patient: Arthur Dent | ID: MEM-CONTRA-0808 | DOB: 1984-03-11\n"
            "Date of Service: 2026-03-22 | Provider: Dr. Stephen Strange, MD\n"
            "Review of Systems: Patient denies radiculopathy and denies radiating pain into lower extremities.\n"
            "Physical Exam: Patient has severe lower extremity radiculopathy radiating down right leg past knee.\n"
            "Request: MRI Lumbar Spine (CPT 72148).\n"
            "Coverage: Commercial PPO Centene\n"
        ),
        "expected_domain": "advanced_imaging",
        "expected_cpt": "72148",
        "expected_conflicting": ["lumbar_radiculopathy_present"]
    },
    "9_unreadable_scanned_document": {
        "bytes": b"%PDF-1.4 Empty document with no text layer\n%%EOF",
        "expected_status": "UNREADABLE_OR_SCANNED_DOCUMENT"
    }
}

def run_investigation():
    registry = RuleRegistry(include_archived=False)
    registry.load_all_domains()
    validator = CaseValidator()
    router = PolicyRouter(registry)
    service = EvaluationService(registry=registry)
    tree_engine = DecisionTreeEngine(registry=registry)

    results = {}

    for case_name, case_info in CASES.items():
        print(f"--- Processing: {case_name} ---")
        if "bytes" in case_info:
            pdf_bytes = case_info["bytes"]
        else:
            pdf_bytes = create_pdf_bytes(case_info["text"])

        extracted = extract_case_from_pdf(pdf_bytes, filename=f"{case_name}.pdf")
        status = extracted["status"]
        fields = extracted.get("extracted_fields", {})
        evidence = fields.get("evidence", {})
        provenance = fields.get("evidence_provenance", {})

        case_res = {
            "extraction_status": status,
            "extracted_fields": {
                "patient_id": fields.get("patient_id"),
                "clinical_domain": fields.get("clinical_domain"),
                "procedure_code": fields.get("procedure_code"),
                "procedure_name": fields.get("procedure_name"),
                "line_of_business": fields.get("line_of_business"),
                "place_of_service": fields.get("place_of_service")
            },
            "evidence": evidence,
            "provenance_keys": list(provenance.keys())
        }

        if status == "SUCCESS":
            # Validate case intake
            clean_case_id = f"CASE-E2E-{case_name.upper().replace('_', '-')}"
            intake_payload = {
                "case_id": clean_case_id,
                "member_id": fields.get("patient_id", "MEM-SYNTH-01"),
                "clinical_domain": fields["clinical_domain"],
                "procedure_code": fields["procedure_code"],
                "procedure_name": fields["procedure_name"],
                "line_of_business": fields["line_of_business"],
                "requested_date_of_service": fields["requested_date_of_service"],
                "payer_id": fields["payer_id"],
                "place_of_service": fields.get("place_of_service", "OFFICE"),
                "clinical_evidence": evidence,
                "evidence_provenance": provenance
            }
            is_valid, val_errs, case_obj = validator.validate(intake_payload)
            case_res["validation"] = {"is_valid": is_valid, "errors": val_errs}

            if is_valid and case_obj:
                # Routing
                routing = router.route_case(case_obj)
                case_res["routing"] = {
                    "status": routing.status,
                    "applicable_rule_count": len(routing.applicable_rules),
                    "rule_ids": [r.rule_id for r in routing.applicable_rules],
                    "routing_notes": routing.routing_notes
                }

                # Evaluate using service
                assessment, audit = service.evaluate_case(case_obj)
                case_res["assessment"] = {
                    "status": assessment.assessment_status.value,
                    "is_binding": assessment.is_binding,
                    "summary": assessment.summary_explanation,
                    "human_review_escalations": assessment.human_review_escalations,
                    "missing_evidence": assessment.missing_evidence_summary
                }

                # Procedure-specific matching rule mapping
                rule_targets = {
                    "1_lumbar_mri_supported": "RULE-ADV-CG2037-001",
                    "2_knee_mri_supported": "RULE-ADV-CG2035-002",
                    "3_brain_mri_supported": "RULE-ADV-CG2012-003",
                    "4_ct_imaging_supported": "RULE-ADV-CG2000-006",
                    "5_interventional_pain_supported": "RULE-IPM-CGEPIDURALINJECTIONS-001",
                    "6_missing_required_info": "RULE-ADV-CG2037-001",
                    "7_explicit_negative_findings": "RULE-ADV-CG2037-001",
                    "8_contradictory_statements": "RULE-ADV-CG2037-001"
                }
                target_rid = rule_targets.get(case_name)
                if target_rid:
                    target_rule = registry.get_rule(target_rid)
                    tree_eval = tree_engine.evaluate(case_obj, target_rule_ids=[target_rid])
                    case_res["procedure_rule_evaluation"] = {
                        "target_rule_id": target_rid,
                        "overall_outcome": tree_eval.overall_outcome.value if tree_eval.overall_outcome else None,
                        "clinical_necessity_outcome": tree_eval.clinical_necessity_outcome.value if tree_eval.clinical_necessity_outcome else None,
                        "place_of_service_outcome": tree_eval.place_of_service_outcome.value if tree_eval.place_of_service_outcome else None,
                        "criteria_met": tree_eval.criteria_met,
                        "criteria_not_met": tree_eval.criteria_not_met,
                        "criteria_insufficient_data": tree_eval.criteria_insufficient_data,
                        "criteria_not_applicable": tree_eval.criteria_not_applicable,
                        "provenance_source": target_rule.source_file if target_rule else None,
                        "provenance_page": target_rule.physical_page if target_rule else None,
                        "provenance_quote": target_rule.source_quote if target_rule else None
                    }
        else:
            case_res["diagnostics"] = extracted.get("diagnostics")

        results[case_name] = case_res

    out_file = Path("scratch/e2e_investigation_results.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Results written to {out_file}")

if __name__ == "__main__":
    run_investigation()
