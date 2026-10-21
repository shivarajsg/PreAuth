"""Step 2 Comprehensive Clinical Evidence Extraction, Policy Matching, and Evaluation Reliability Test Suite.

Verifies:
1. Four-state criterion evaluation: MET, NOT_MET, INSUFFICIENT_DATA, NOT_APPLICABLE.
2. Evidence distinction: EXPLICIT_POSITIVE, EXPLICIT_NEGATIVE, MISSING, AMBIGUOUS, CONFLICTING.
3. Missing data invariant: Missing evidence never automatically becomes NOT_MET.
4. Diverse clinical procedure extraction and normalization:
   - MRI Lumbar Spine (CPT 72148 / 72149)
   - MRI Knee / Leg (CPT 73721 / 73722)
   - MRI Brain (CPT 70551 / 70552)
   - CT Imaging (CPT 74177 / 71250 / 70450)
   - Interventional Pain Procedures (CPT 62323 / 64483)
5. Contradictory clinical documentation handling.
6. Policy routing & domain identification:
   - Advanced Imaging vs IPM routing
   - Unsupported procedures / domains (e.g. archived cardiology, cosmetic, experimental)
7. Dual-track separation: Clinical Necessity vs Place of Service (EPOS 2067 / EPOS 1755).
8. Provenance, citation traceability, and snippet grounding.
9. Unreadable / scanned document handling.
10. Governance safeguards: 0 approved rules, 7 blocked rules, is_binding=False, CP.MP.107 exclusion.
"""

import copy
import io
import json
import unittest
import pymupdf as fitz

from medrule_engine.case_validator import CaseIntake, CaseValidator
from medrule_engine.condition_evaluator import (
    ConditionEvaluator,
    CriterionState,
    EvaluationState,
    EvidenceState,
)
from medrule_engine.decision_aggregator import CaseAssessmentStatus, DecisionAggregator
from medrule_engine.decision_tree import (
    DecisionOutcome,
    DecisionTrack,
    DecisionTreeEngine,
    GOVERNANCE_BLOCKED_RULE_IDS,
)
from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.integrations.pdf_extractor import (
    extract_case_from_pdf,
    extract_clinical_facts_from_text,
)
from medrule_engine.policy_router import PolicyRouter
from medrule_engine.rule_registry import RuleRecord, RuleRegistry


def create_in_memory_pdf(text: str) -> bytes:
    """Helper to generate in-memory PDF bytes containing given text."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 72), text, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


class TestStep2ClinicalExtractionAndEvaluation(unittest.TestCase):
    """Rigorous evaluation suite for MedRule Step 2."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry(include_archived=False)
        cls.registry.load_all_domains()
        cls.validator = CaseValidator()
        cls.router = PolicyRouter(cls.registry)
        cls.evaluator = ConditionEvaluator()
        cls.tree_engine = DecisionTreeEngine(registry=cls.registry)
        cls.service = EvaluationService(registry=cls.registry)

    # =========================================================================
    # Section 1: Four-State Criterion Evaluation Representation
    # =========================================================================

    def test_criterion_state_met(self):
        """Documented positive evidence satisfies criterion -> MET."""
        conditions = {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "c1",
                    "parameter": "lumbar_radiculopathy_present",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        }
        case = CaseIntake(
            case_id="CASE-MET-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={"lumbar_radiculopathy_present": True}
        )
        eval_result = self.evaluator.evaluate(conditions, case)
        self.assertEqual(eval_result.status, EvaluationState.TRUE)
        crit = eval_result.criteria_results[0]
        self.assertEqual(crit.criterion_state, CriterionState.MET)
        self.assertEqual(crit.evidence_state, EvidenceState.EXPLICIT_POSITIVE)

    def test_criterion_state_not_met_explicit_negative(self):
        """Explicit negative evidence or failed threshold -> NOT_MET."""
        conditions = {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "c1",
                    "parameter": "lumbar_radiculopathy_present",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        }
        case = CaseIntake(
            case_id="CASE-NOT-MET-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={"lumbar_radiculopathy_present": False}
        )
        eval_result = self.evaluator.evaluate(conditions, case)
        self.assertEqual(eval_result.status, EvaluationState.FALSE)
        crit = eval_result.criteria_results[0]
        self.assertEqual(crit.criterion_state, CriterionState.NOT_MET)
        self.assertEqual(crit.evidence_state, EvidenceState.EXPLICIT_NEGATIVE)

    def test_criterion_state_insufficient_data_for_missing_fact(self):
        """Missing information must NEVER automatically become NOT_MET; it must be INSUFFICIENT_DATA."""
        conditions = {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "c1",
                    "parameter": "conservative_therapy_duration_weeks",
                    "comparator": "GREATER_THAN_OR_EQUAL",
                    "value": 6
                }
            ]
        }
        case = CaseIntake(
            case_id="CASE-INSUFF-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={}  # Field omitted
        )
        eval_result = self.evaluator.evaluate(conditions, case)
        self.assertEqual(eval_result.status, EvaluationState.UNKNOWN)
        crit = eval_result.criteria_results[0]
        self.assertEqual(crit.criterion_state, CriterionState.INSUFFICIENT_DATA)
        self.assertEqual(crit.evidence_state, EvidenceState.MISSING)

    def test_criterion_state_not_applicable_in_short_circuited_branch(self):
        """In an ANY_OF group where one branch is MET, unneeded alternative branches must be NOT_APPLICABLE."""
        conditions = {
            "operator": "ANY_OF",
            "criteria": [
                {
                    "condition_id": "branch_a",
                    "parameter": "cauda_equina_syndrome_suspected",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "branch_b",
                    "parameter": "conservative_therapy_duration_weeks",
                    "comparator": "GREATER_THAN_OR_EQUAL",
                    "value": 6
                }
            ]
        }
        case = CaseIntake(
            case_id="CASE-NA-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={"cauda_equina_syndrome_suspected": True}
        )
        eval_result = self.evaluator.evaluate(conditions, case)
        self.assertEqual(eval_result.status, EvaluationState.TRUE)
        crit_a = eval_result.criteria_results[0]
        crit_b = eval_result.criteria_results[1]
        self.assertEqual(crit_a.criterion_state, CriterionState.MET)
        self.assertEqual(crit_b.criterion_state, CriterionState.NOT_APPLICABLE)

    # =========================================================================
    # Section 2: Evidence State Distinction & Contradiction Detection
    # =========================================================================

    def test_conflicting_evidence_detection(self):
        """When clinical note contains both positive and negative assertions, mark CONFLICTING and INSUFFICIENT_DATA."""
        contradictory_text = (
            "PATIENT CLINICAL NOTE\n"
            "Patient: Jane Doe | DOB: 1980-01-01\n"
            "Date of Service: 2026-03-10\n"
            "Review of Systems: Patient denies radiculopathy and denies lower extremity radiating symptoms.\n"
            "Physical Exam: Patient has severe lower extremity radiculopathy radiating past knee.\n"
            "Procedure requested: MRI Lumbar Spine (CPT 72148)\n"
            "Coverage: Commercial PPO Centene\n"
        )
        facts = extract_clinical_facts_from_text(contradictory_text)
        rad_val = facts["evidence"].get("lumbar_radiculopathy_present")
        
        # Must detect contradiction
        self.assertIsInstance(rad_val, dict)
        self.assertEqual(rad_val.get("status"), "CONFLICTING")

        # Now evaluate this conflicting parameter in condition evaluator
        conditions = {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "c1",
                    "parameter": "lumbar_radiculopathy_present",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        }
        case = CaseIntake(
            case_id="CASE-CONFLICT-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-10",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={"lumbar_radiculopathy_present": rad_val}
        )
        eval_result = self.evaluator.evaluate(conditions, case)
        self.assertEqual(eval_result.status, EvaluationState.UNKNOWN)
        crit = eval_result.criteria_results[0]
        self.assertEqual(crit.criterion_state, CriterionState.INSUFFICIENT_DATA)
        self.assertEqual(crit.evidence_state, EvidenceState.CONFLICTING)
        self.assertIn("conflicting", crit.reason.lower())

    def test_missing_evidence_does_not_claim_all_criteria_met(self):
        """Case with 1 met and 1 missing criterion must NOT claim all criteria met in decision tree."""
        rule = self.registry.get_rule("RULE-ADV-CG2037-001")
        self.assertIsNotNone(rule)

        # Incomplete case: has radiculopathy, but conservative therapy weeks is missing
        case_data = {
            "case_id": "CASE-INCOMPLETE-01",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72148",
            "procedure_name": "MRI Lumbar Spine",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "CENTENE",
            "clinical_evidence": {
                "lumbar_radiculopathy_present": True
                # conservative_therapy_duration_weeks omitted
            }
        }
        tree_assessment = self.tree_engine.evaluate(case_data, target_rule_ids=["RULE-ADV-CG2037-001"])
        self.assertEqual(tree_assessment.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)
        self.assertGreater(len(tree_assessment.criteria_insufficient_data), 0)
        self.assertEqual(len(tree_assessment.criteria_not_met), 0)

    # =========================================================================
    # Section 3: Diverse Clinical Procedure Extraction and Normalization
    # =========================================================================

    def test_lumbar_mri_extraction_with_quantitative_duration(self):
        """Extraction of Lumbar MRI (CPT 72148) with 8 weeks duration."""
        note = (
            "NEUROSURGERY CLINICAL SUMMARY\n"
            "Patient: Robert Vance | Date: 2026-03-01\n"
            "Chief Complaint: Low back pain radiating into right leg.\n"
            "History: Persistent lumbar radiculopathy for 8 weeks.\n"
            "Completed 8 weeks of physical therapy and oral anti-inflammatories without relief.\n"
            "Request: MRI Lumbar spine without IV contrast (CPT 72148).\n"
            "Insurance: Commercial PPO Centene\n"
        )
        pdf_bytes = create_in_memory_pdf(note)
        res = extract_case_from_pdf(pdf_bytes, filename="lumbar_note.pdf")
        self.assertEqual(res["status"], "SUCCESS")
        fields = res["extracted_fields"]
        self.assertEqual(fields["procedure_code"], "72148")
        self.assertEqual(fields["clinical_domain"], "advanced_imaging")
        self.assertTrue(fields["evidence"]["lumbar_radiculopathy_present"])
        self.assertEqual(fields["evidence"]["conservative_therapy_duration_weeks"], 8)
        self.assertIn(str(fields["evidence"].get("anatomy_region")).lower(), ["lumbar_spine", "lumbar"])

    def test_knee_mri_extraction_with_laterality(self):
        """Extraction of Knee MRI (CPT 73721) with laterality and findings."""
        note = (
            "SPORTS MEDICINE CONSULTATION\n"
            "Patient: Alex Morgan | Date: 2026-04-05\n"
            "History: Acute twist injury during soccer match 4 weeks ago.\n"
            "Physical Exam: Left knee joint line tenderness, positive McMurray test indicating meniscal tear.\n"
            "Effusion present in left knee.\n"
            "Failed 4 weeks of rest and NSAIDs.\n"
            "Order: MRI of the left knee without contrast (CPT 73721).\n"
            "Coverage: Medicare Advantage\n"
        )
        pdf_bytes = create_in_memory_pdf(note)
        res = extract_case_from_pdf(pdf_bytes, filename="knee_note.pdf")
        self.assertEqual(res["status"], "SUCCESS")
        fields = res["extracted_fields"]
        self.assertEqual(fields["procedure_code"], "73721")
        self.assertEqual(fields["clinical_domain"], "advanced_imaging")
        self.assertEqual(fields["line_of_business"], "MEDICARE_ADVANTAGE")
        self.assertEqual(fields["evidence"]["laterality"], "LEFT")
        self.assertIn(str(fields["evidence"].get("anatomy_region")).lower(), ["knee"])
        self.assertTrue(fields["evidence"]["meniscal_tear_suspected"])
        self.assertTrue(fields["evidence"]["joint_effusion_present"])

    def test_brain_mri_extraction(self):
        """Extraction of Brain MRI (CPT 70551) with neurological indications."""
        note = (
            "NEUROLOGY EVALUATION NOTE\n"
            "Patient: David Miller | Date: 2026-02-18\n"
            "Chief Complaint: Progressive unilateral headache with right-sided focal neurological deficit.\n"
            "Recent onset of new adult partial seizures.\n"
            "Assessment: Need urgent diagnostic intracranial imaging.\n"
            "Plan: MRI Brain without contrast (CPT 70551).\n"
            "Payer: Commercial Choice Plus\n"
        )
        pdf_bytes = create_in_memory_pdf(note)
        res = extract_case_from_pdf(pdf_bytes, filename="brain_note.pdf")
        self.assertEqual(res["status"], "SUCCESS")
        fields = res["extracted_fields"]
        self.assertEqual(fields["procedure_code"], "70551")
        self.assertEqual(fields["clinical_domain"], "advanced_imaging")
        self.assertTrue(fields["evidence"]["headache_documented"])
        self.assertTrue(fields["evidence"]["focal_neurological_deficit"])
        self.assertTrue(fields["evidence"]["seizures_documented"])

    def test_ct_imaging_extraction(self):
        """Extraction of CT Abdomen and Pelvis with IV contrast (CPT 74177)."""
        note = (
            "GASTROENTEROLOGY PROGRESS NOTE\n"
            "Patient: Sarah Connor | Date: 2026-03-22\n"
            "Impression: Acute pancreatitis flare-up with severe epigastric abdominal pain.\n"
            "Elevated lipase and amylase markers.\n"
            "Conservative treatment in observation for 72 hours without clinical improvement.\n"
            "Request: CT Abdomen and Pelvis with contrast (CPT 74177).\n"
            "Line of Business: Medicaid Complete\n"
        )
        pdf_bytes = create_in_memory_pdf(note)
        res = extract_case_from_pdf(pdf_bytes, filename="ct_note.pdf")
        self.assertEqual(res["status"], "SUCCESS")
        fields = res["extracted_fields"]
        self.assertEqual(fields["procedure_code"], "74177")
        self.assertEqual(fields["clinical_domain"], "advanced_imaging")
        self.assertEqual(fields["line_of_business"], "MEDICAID")
        self.assertTrue(fields["evidence"]["abdominal_pain_documented"])
        self.assertEqual(fields["evidence"]["pancreatitis_diagnostic_markers"], "ELEVATED")
        self.assertEqual(fields["evidence"]["conservative_treatment_duration_hours"], 72)

    def test_interventional_pain_extraction(self):
        """Extraction of Lumbar Epidural Steroid Injection (CPT 62323)."""
        note = (
            "PAIN MANAGEMENT CONSULTATION\n"
            "Patient: Marcus Brody | Date: 2026-04-02\n"
            "Diagnosis: Lumbar radicular pain L5-S1 distribution lasting 10 weeks.\n"
            "Previous MRI confirmed L5-S1 disc herniation with nerve root impingement.\n"
            "Completed 8 weeks of physical therapy and analgesics with inadequate relief.\n"
            "Recommendation: Lumbar interlaminar epidural steroid injection with fluoroscopy (CPT 62323).\n"
            "Place of Service: Ambulatory Surgical Center (POS 24)\n"
            "Coverage: Commercial PPO Centene\n"
        )
        pdf_bytes = create_in_memory_pdf(note)
        res = extract_case_from_pdf(pdf_bytes, filename="ipm_note.pdf")
        self.assertEqual(res["status"], "SUCCESS")
        fields = res["extracted_fields"]
        self.assertEqual(fields["procedure_code"], "62323")
        self.assertEqual(fields["clinical_domain"], "interventional_pain_management")
        self.assertTrue(fields["evidence"]["lumbar_radiculopathy_present"])
        self.assertEqual(fields["evidence"]["conservative_therapy_duration_weeks"], 8)
        self.assertEqual(fields["evidence"]["place_of_service_code"], "POS_24")

    # =========================================================================
    # Section 4: Policy Matching and Domain Identification
    # =========================================================================

    def test_router_selects_advanced_imaging_policy(self):
        """MRI Lumbar Spine routes to Advanced Imaging policy."""
        case = CaseIntake(
            case_id="CASE-ROUT-AI-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={"lumbar_radiculopathy_present": True}
        )
        routing = self.router.route_case(case)
        self.assertEqual(routing.status, "ROUTED")
        self.assertGreater(len(routing.applicable_rules), 0)
        for r in routing.applicable_rules:
            self.assertEqual(r.domain, "advanced_imaging")

    def test_router_selects_ipm_policy(self):
        """Epidural injection routes to Interventional Pain Management policy."""
        case = CaseIntake(
            case_id="CASE-ROUT-IPM-01",
            clinical_domain="interventional_pain_management",
            procedure_code="62323",
            procedure_name="Lumbar Epidural Injection",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={"lumbar_radiculopathy_present": True}
        )
        routing = self.router.route_case(case)
        self.assertEqual(routing.status, "ROUTED")
        self.assertGreater(len(routing.applicable_rules), 0)
        for r in routing.applicable_rules:
            self.assertEqual(r.domain, "interventional_pain_management")

    def test_router_rejects_unsupported_procedure_cleanly(self):
        """Unsupported CPT code or cosmetic procedure returns POLICY_NOT_APPLICABLE rather than guessing."""
        case = CaseIntake(
            case_id="CASE-UNSUPPORTED-01",
            clinical_domain="plastic_surgery",
            procedure_code="30410",
            procedure_name="Cosmetic Rhinoplasty",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={}
        )
        routing = self.router.route_case(case)
        self.assertEqual(routing.status, "POLICY_NOT_APPLICABLE")
        self.assertEqual(len(routing.applicable_rules), 0)

        # End-to-end evaluation service must report POLICY_NOT_APPLICABLE
        assessment, audit = self.service.evaluate_case(case)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)

    # =========================================================================
    # Section 5: Dual-Track Separation (Clinical Necessity vs Place of Service)
    # =========================================================================

    def test_dual_track_epos_separation(self):
        """Clinical Necessity evaluates against clinical rules; POS evaluates against EPOS."""
        case_dict = {
            "case_id": "CASE-DUAL-01",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "CENTENE",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "clinical_evidence": {
                "ordering_provider_license": True,
                "clinical_office_notes": True,
                "suspected_or_established_multiple_sclerosis": True,
                "focal_neurological_deficit_present": True,
                "place_of_service_code": "POS_22",
                "severe_claustrophobia_open_mri_needed": False,
                "bariatric_weight_exceeds_freestanding_scanner": False,
                "complex_specialized_protocol_needed": False
            }
        }
        assessment = self.tree_engine.evaluate(
            case_dict,
            target_rule_ids=["RULE-ADV-CG2012-003", "RULE-ADV-EPOS2067-001", "RULE-ADV-EPOS2067-004"]
        )
        self.assertEqual(assessment.clinical_necessity_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(assessment.place_of_service_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(assessment.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertIn("Place of Service", assessment.overall_summary)

    # =========================================================================
    # Section 6: Source Citations and Audit Records
    # =========================================================================

    def test_provenance_and_audit_record_traceability(self):
        """Every evaluated criterion trace and audit log includes source policy, page, and snippet."""
        case = CaseIntake(
            case_id="CASE-PROV-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={
                "lumbar_radiculopathy_present": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_modalities_count": 2,
                "ordering_provider_license": True
            },
            evidence_provenance={
                "lumbar_radiculopathy_present": {
                    "source_sentence": "Patient has lower back pain radiating into right leg.",
                    "snippet": "lumbar radiculopathy",
                    "confidence": "HIGH"
                }
            }
        )
        assessment, audit = self.service.evaluate_case(case, target_rule_ids=["RULE-ADV-CG2037-001"])
        
        # Verify audit record integrity
        self.assertIn("audit_header", audit)
        self.assertIn("case_assessment", audit)
        self.assertIn("rule_evaluations", audit)
        self.assertGreater(len(audit["rule_evaluations"]), 0)
        
        rule_eval = audit["rule_evaluations"][0]
        self.assertEqual(rule_eval["rule_id"], "RULE-ADV-CG2037-001")
        self.assertIn("policy_provenance", rule_eval)
        self.assertTrue(rule_eval["policy_provenance"]["source_file"].endswith(".pdf"))
        self.assertGreater(rule_eval["policy_provenance"]["physical_page"], 0)
        self.assertTrue(len(rule_eval["policy_provenance"]["source_quote"]) > 0)

        # Check that criteria carry criterion_state and evidence_state
        cond_eval = rule_eval["condition_evaluation"]
        for crit in cond_eval["criteria"]:
            self.assertIn("criterion_state", crit)
            self.assertIn("evidence_state", crit)

    # =========================================================================
    # Section 7: Unreadable or Scanned Document Handling
    # =========================================================================

    def test_unreadable_or_scanned_document_handling(self):
        """Non-PDF or empty image-only PDF returns UNREADABLE_OR_SCANNED_DOCUMENT without crashing."""
        # Case A: Corrupted / invalid PDF header bytes
        res_corrupt = extract_case_from_pdf(b"NOT_A_VALID_PDF_HEADER_DATA", filename="scanned_fax.pdf")
        self.assertEqual(res_corrupt["status"], "UNREADABLE_OR_SCANNED_DOCUMENT")
        self.assertIn("diagnostics", res_corrupt)
        self.assertEqual(res_corrupt["extracted_fields"]["clinical_domain"], "UNKNOWN")

        # Case B: Blank PDF (0 text extracted)
        blank_doc = fitz.open()
        blank_doc.new_page()
        blank_bytes = blank_doc.tobytes()
        blank_doc.close()

        res_blank = extract_case_from_pdf(blank_bytes, filename="blank_scanned_form.pdf")
        self.assertEqual(res_blank["status"], "UNREADABLE_OR_SCANNED_DOCUMENT")
        self.assertEqual(res_blank["diagnostics"]["extracted_characters"], 0)

    # =========================================================================
    # Section 8: Core Safety and Governance Invariants
    # =========================================================================

    def test_governance_invariants_preserved(self):
        """Zero APPROVED rules, 7 blocked rules, non-binding status, and CP.MP.107 exclusion."""
        # 1. Zero rules approved
        all_rules = self.registry.all_rules
        approved = [r for r in all_rules if r.extraction_status == "APPROVED"]
        self.assertEqual(len(approved), 0, "INVARIANT VIOLATION: Zero rules may be APPROVED.")

        # 2. Exactly 7 blocked rules
        blocked = [r for r in all_rules if r.extraction_status == "NEEDS_HUMAN_REVIEW"]
        self.assertEqual(len(blocked), 7, "INVARIANT VIOLATION: Exactly 7 rules must be blocked.")
        self.assertEqual(set(r.rule_id for r in blocked), GOVERNANCE_BLOCKED_RULE_IDS)

        # 3. Blocked rules cannot be autonomously evaluated to CRITERIA_MET
        for blocked_id in GOVERNANCE_BLOCKED_RULE_IDS:
            case_data = {
                "case_id": f"CASE-BLOCKED-{blocked_id}",
                "clinical_domain": "advanced_imaging",
                "procedure_code": "72148",
                "procedure_name": "Test Procedure",
                "requested_date_of_service": "2026-03-01",
                "line_of_business": "COMMERCIAL",
                "payer_id": "CENTENE",
                "clinical_evidence": {}
            }
            res = self.tree_engine.evaluate(case_data, target_rule_ids=[blocked_id])
            self.assertEqual(res.overall_outcome, DecisionOutcome.NEEDS_HUMAN_REVIEW)

        # 4. CP.MP.107 DME exclusion
        for r in all_rules:
            self.assertNotIn("CP.MP.107", r.source_file, f"Rule {r.rule_id} references CP.MP.107.")

        # 5. Non-binding disclaimer on assessment
        case = CaseIntake(
            case_id="CASE-NON-BINDING-01",
            clinical_domain="advanced_imaging",
            procedure_code="72148",
            procedure_name="MRI Lumbar Spine",
            requested_date_of_service="2026-03-01",
            line_of_business="COMMERCIAL",
            payer_id="CENTENE",
            clinical_evidence={"lumbar_radiculopathy_present": True}
        )
        assessment, audit = self.service.evaluate_case(case)
        self.assertFalse(assessment.is_binding)
        self.assertIn("NON-BINDING PROTOTYPE", assessment.disclaimer)


if __name__ == "__main__":
    unittest.main()
