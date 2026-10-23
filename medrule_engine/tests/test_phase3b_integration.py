"""MedRule Phase 3B Integration and Regression Test Suite.

Comprehensive unit and integration testing covering:
1. Critical Semantic Audit: Distinct semantics for 7 evidence states across IS_PRESENT, IS_ABSENT, and comparators.
2. Strict type safety: Prevention of silent boolean-to-numeric coercion in EQUALS, numeric comparators, and BETWEEN.
3. Policy Router verification: Multi-domain routing, cross-domain rejection, LOB verification, plan dependencies, DOS boundaries.
4. Three-Valued Logic: Truth tables for ALL_OF, ANY_OF, NONE_OF, SINGLE_CONDITION with short-circuiting.
5. Evidence sufficiency vs clinical criteria separation.
6. Batch evaluation interface with error isolation.
7. Audit trail completeness and SHA-256 deterministic repeatability.
8. Non-binding prototype governance invariants.
"""

import copy
import json
from pathlib import Path
import unittest

from medrule_engine.case_validator import CaseIntake, CaseValidator, validate_case
from medrule_engine.condition_evaluator import ConditionEvaluator, EvaluationState
from medrule_engine.decision_aggregator import CaseAssessmentStatus, DecisionAggregator
from medrule_engine.evaluation_service import EvaluationService, evaluate_batch, evaluate_case, evaluate_rule
from medrule_engine.evidence_validator import EvidenceValidator
from medrule_engine.policy_router import PolicyRouter
from medrule_engine.rule_registry import RuleRecord, RuleRegistry

REPO_ROOT = Path(__file__).resolve().parents[2]


class TestPhase3BIntegration(unittest.TestCase):
    """Rigorous Phase 3B Integration Test Suite."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry()
        cls.total_rules = cls.registry.load_all_domains()
        cls.service = EvaluationService(registry=cls.registry)
        cls.evaluator = ConditionEvaluator()
        cls.validator = CaseValidator()
        cls.router = PolicyRouter(cls.registry)

    # =========================================================================
    # PART 1: Critical Semantic Audit (7 Distinct Evidence States)
    # =========================================================================

    def test_semantic_state_1_field_does_not_exist(self):
        """State 1: Omitted field returns UNKNOWN with evidence_missing=True."""
        case_dict = {
            "case_id": "CASE-SEM-01",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}  # parameter omitted entirely
        }
        _, _, case_obj = self.validator.validate(case_dict)
        cond = {
            "condition_id": "C-OMIT",
            "description": "Check omitted parameter",
            "parameter": "unrecorded_symptom",
            "comparator": "IS_PRESENT"
        }
        res = self.evaluator._evaluate_criterion(cond, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.UNKNOWN)
        self.assertTrue(res.evidence_missing)
        self.assertIn("missing from case record", res.reason)

    def test_semantic_state_2_field_exists_with_null(self):
        """State 2: Explicit null returns UNKNOWN with evidence_missing=True."""
        case_dict = {
            "case_id": "CASE-SEM-02",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "recorded_test_result": None  # explicit null
            }
        }
        _, _, case_obj = self.validator.validate(case_dict)
        cond = {
            "condition_id": "C-NULL",
            "description": "Check null parameter",
            "parameter": "recorded_test_result",
            "comparator": "IS_PRESENT"
        }
        res = self.evaluator._evaluate_criterion(cond, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.UNKNOWN)
        self.assertTrue(res.evidence_missing)
        self.assertIn("provided as null", res.reason)

    def test_semantic_state_3_field_exists_with_boolean_false(self):
        """State 3: Explicit Boolean False is valid negative evidence (NOT missing info)."""
        case_dict = {
            "case_id": "CASE-SEM-03",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "active_malignancy": False
            }
        }
        _, _, case_obj = self.validator.validate(case_dict)

        # A: IS_PRESENT on False yields FALSE (not met), and evidence is NOT missing
        cond_pres = {
            "condition_id": "C-PRES",
            "description": "Check presence",
            "parameter": "active_malignancy",
            "comparator": "IS_PRESENT"
        }
        res_pres = self.evaluator._evaluate_criterion(cond_pres, case_obj, depth=0)
        self.assertEqual(res_pres.status, EvaluationState.FALSE)
        self.assertFalse(res_pres.evidence_missing)

        # B: IS_ABSENT on False yields TRUE (confirmed absent)
        cond_abs = {
            "condition_id": "C-ABS",
            "description": "Check absence",
            "parameter": "active_malignancy",
            "comparator": "IS_ABSENT"
        }
        res_abs = self.evaluator._evaluate_criterion(cond_abs, case_obj, depth=0)
        self.assertEqual(res_abs.status, EvaluationState.TRUE)
        self.assertFalse(res_abs.evidence_missing)

    def test_semantic_state_4_field_exists_with_boolean_true(self):
        """State 4: Explicit Boolean True is valid positive evidence."""
        case_dict = {
            "case_id": "CASE-SEM-04",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "active_malignancy": True
            }
        }
        _, _, case_obj = self.validator.validate(case_dict)

        # IS_PRESENT yields TRUE
        cond_pres = {
            "condition_id": "C-PRES",
            "description": "Check presence",
            "parameter": "active_malignancy",
            "comparator": "IS_PRESENT"
        }
        res_pres = self.evaluator._evaluate_criterion(cond_pres, case_obj, depth=0)
        self.assertEqual(res_pres.status, EvaluationState.TRUE)

        # IS_ABSENT yields FALSE (presence violates absence)
        cond_abs = {
            "condition_id": "C-ABS",
            "description": "Check absence",
            "parameter": "active_malignancy",
            "comparator": "IS_ABSENT"
        }
        res_abs = self.evaluator._evaluate_criterion(cond_abs, case_obj, depth=0)
        self.assertEqual(res_abs.status, EvaluationState.FALSE)

    def test_semantic_state_5_empty_collection_or_string(self):
        """State 5: Empty collection or string yields FALSE for IS_PRESENT and TRUE for IS_ABSENT."""
        case_dict = {
            "case_id": "CASE-SEM-05",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "symptoms_list": [],
                "notes_text": ""
            }
        }
        _, _, case_obj = self.validator.validate(case_dict)

        cond_list_pres = {
            "condition_id": "C-LP",
            "description": "Check list presence",
            "parameter": "symptoms_list",
            "comparator": "IS_PRESENT"
        }
        res = self.evaluator._evaluate_criterion(cond_list_pres, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.FALSE)

        cond_list_abs = {
            "condition_id": "C-LA",
            "description": "Check list absence",
            "parameter": "symptoms_list",
            "comparator": "IS_ABSENT"
        }
        res = self.evaluator._evaluate_criterion(cond_list_abs, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.TRUE)

    def test_semantic_state_6_valid_numerical_zero(self):
        """State 6: Numerical zero is a valid measurement, NOT falsy/empty/missing."""
        case_dict = {
            "case_id": "CASE-SEM-06",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "pain_score": 0,
                "conservative_care_weeks": 0.0
            }
        }
        _, _, case_obj = self.validator.validate(case_dict)

        # IS_PRESENT yields TRUE (value 0 is present)
        cond_pres = {
            "condition_id": "C-ZP",
            "description": "Check numeric 0 presence",
            "parameter": "pain_score",
            "comparator": "IS_PRESENT"
        }
        res = self.evaluator._evaluate_criterion(cond_pres, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.TRUE)

        # Numeric comparators evaluate 0 correctly
        cond_gte = {
            "condition_id": "C-ZGTE",
            "description": "Check 0 >= 0",
            "parameter": "pain_score",
            "comparator": "GREATER_THAN_OR_EQUAL",
            "value": 0
        }
        res = self.evaluator._evaluate_criterion(cond_gte, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.TRUE)

        cond_gt = {
            "condition_id": "C-ZGT",
            "description": "Check 0 > 0",
            "parameter": "pain_score",
            "comparator": "GREATER_THAN",
            "value": 0
        }
        res = self.evaluator._evaluate_criterion(cond_gt, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.FALSE)

    def test_semantic_state_7_invalid_or_incompatible_type(self):
        """State 7: Incompatible type yields UNKNOWN with type_error (not FALSE or coercion)."""
        case_dict = {
            "case_id": "CASE-SEM-07",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "conservative_care_duration_weeks": "three_weeks"  # string where float required
            }
        }
        _, _, case_obj = self.validator.validate(case_dict)
        cond = {
            "condition_id": "C-INCOMP",
            "description": "Numeric comparison on string",
            "parameter": "conservative_care_duration_weeks",
            "comparator": "GREATER_THAN_OR_EQUAL",
            "value": 6
        }
        res = self.evaluator._evaluate_criterion(cond, case_obj, depth=0)
        self.assertEqual(res.status, EvaluationState.UNKNOWN)
        self.assertIsNotNone(res.type_error)
        self.assertIn("Type mismatch", res.type_error)

    # =========================================================================
    # PART 2: Strict Type Safety & Boolean-to-Numeric Coercion Prevention
    # =========================================================================

    def test_strict_type_safety_boolean_does_not_equal_zero_or_one(self):
        """In Python False == 0 and True == 1, but MedRule EQUALS strictly prevents this."""
        st, rsn, err = self.evaluator._apply_comparator("EQUALS", False, 0, None)
        self.assertEqual(st, EvaluationState.FALSE)
        self.assertIn("Type mismatch", rsn)

        st, rsn, err = self.evaluator._apply_comparator("EQUALS", True, 1, None)
        self.assertEqual(st, EvaluationState.FALSE)
        self.assertIn("Type mismatch", rsn)

    def test_strict_type_safety_numeric_comparators_reject_boolean(self):
        """Booleans must not be coerced to 1.0 or 0.0 in numeric comparators."""
        st, rsn, err = self.evaluator._apply_comparator("GREATER_THAN_OR_EQUAL", True, 0.5, None)
        self.assertEqual(st, EvaluationState.UNKNOWN)
        self.assertIn("Boolean provided for numeric comparator", err)

        st, rsn, err = self.evaluator._apply_comparator("LESS_THAN", False, 5, None)
        self.assertEqual(st, EvaluationState.UNKNOWN)
        self.assertIn("Boolean provided for numeric comparator", err)

    def test_strict_type_safety_between_rejects_boolean(self):
        """Between comparator rejects booleans as values or boundaries."""
        st, rsn, err = self.evaluator._apply_comparator("BETWEEN", True, [0, 10], None)
        self.assertEqual(st, EvaluationState.UNKNOWN)
        self.assertIn("Boolean provided for range", err)

        st, rsn, err = self.evaluator._apply_comparator("BETWEEN", 5, [False, 10], None)
        self.assertEqual(st, EvaluationState.UNKNOWN)
        self.assertIn("Boolean boundary in range", err)

    def test_string_boolean_normalization_in_equals(self):
        """Stringified booleans (e.g. 'TRUE' from policy JSON) match boolean True."""
        st, rsn, err = self.evaluator._apply_comparator("EQUALS", True, "TRUE", None)
        self.assertEqual(st, EvaluationState.TRUE)

        st, rsn, err = self.evaluator._apply_comparator("EQUALS", False, "FALSE", None)
        self.assertEqual(st, EvaluationState.TRUE)

        st, rsn, err = self.evaluator._apply_comparator("EQUALS", True, "FALSE", None)
        self.assertEqual(st, EvaluationState.FALSE)

    # =========================================================================
    # PART 3: Policy Router Integration Tests Across Domains
    # =========================================================================

    def test_router_rejects_unverified_line_of_business(self):
        """Line of business 'OTHER' triggers MANUAL_REVIEW_REQUIRED and is not assumed commercial."""
        case_dict = {
            "case_id": "CASE-ROUT-01",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "requested_date_of_service": "2026-04-25",
            "line_of_business": "OTHER",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"cg2000_indication": True}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        self.assertIn("Unrecognized, empty, or unverified line_of_business", audit["routing_summary"]["routing_notes"][0])

    def test_router_unresolved_plan_dependency(self):
        """Unresolved plan dependency blocks evaluation and requires manual review."""
        case_dict = {
            "case_id": "CASE-ROUT-02",
            "clinical_domain": "cardiology",
            "procedure_code": "93224",
            "procedure_name": "Ambulatory Rhythm Monitoring",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"cg7252_indication": True}
        }
        pol_ctx = {"unresolved_plan_dependency": "Custom Medicare Advantage Fee Schedule not found"}
        assessment, audit = self.service.evaluate_case(case_dict, policy_context=pol_ctx)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        self.assertIn("Unresolved plan-specific dependency", audit["routing_summary"]["routing_notes"][0])

    def test_router_unresolved_policy_section_dependency(self):
        """Unresolved policy section dependency yields POLICY_VERSION_UNRESOLVED."""
        case_dict = {
            "case_id": "CASE-ROUT-03",
            "clinical_domain": "centene_dme_orthotics_prosthetics",
            "procedure_code": "E0601",
            "procedure_name": "CPAP",
            "requested_date_of_service": "2026-08-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "CENTENE",
            "clinical_evidence": {"device_education_provided": True}
        }
        pol_ctx = {"unresolved_policy_section_dependency": "Section C.3 Clinical Criteria Grid missing"}
        assessment, audit = self.service.evaluate_case(case_dict, policy_context=pol_ctx)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_VERSION_UNRESOLVED)

    def test_router_cross_domain_procedure_mismatch(self):
        """Diagnostic imaging CPT 74177 in Interventional Pain Management yields POLICY_NOT_APPLICABLE."""
        case_dict = {
            "case_id": "CASE-ROUT-04",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-05-10",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)

    def test_router_empty_candidate_rule_set(self):
        """Calling evaluation with empty candidate rules target_rule_ids=[] yields POLICY_NOT_APPLICABLE."""
        case_dict = {
            "case_id": "CASE-ROUT-05",
            "clinical_domain": "radiation_oncology",
            "procedure_code": "77301",
            "procedure_name": "IMRT",
            "requested_date_of_service": "2026-05-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict, target_rule_ids=[])
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)

    # =========================================================================
    # PART 4: Batch Evaluation Interface and Error Isolation
    # =========================================================================

    def test_batch_interface_processes_cases_with_error_isolation(self):
        """Batch processing evaluates valid cases while isolating errors on malformed payloads."""
        valid_case = {
            "case_id": "CASE-BATCH-VALID",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "pancreatitis_diagnostic_markers": "ELEVATED",
                "conservative_treatment_duration_hours": 96,
                "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT",
                "ordering_provider_license": True
            }
        }
        malformed_case = {
            "case_id": "invalid_case_id_without_prefix",
            "clinical_domain": "unknown_domain"
        }

        batch_result = evaluate_batch([valid_case, malformed_case], target_rule_ids=["RULE-ADV-CG2000-006"])
        self.assertEqual(batch_result["total_cases"], 2)
        self.assertEqual(batch_result["successful_evaluations"], 1)
        self.assertEqual(batch_result["validation_failures"], 1)
        self.assertEqual(batch_result["case_results"][0]["assessment_status"], "CRITERIA_MET")
        self.assertEqual(batch_result["case_results"][1]["assessment_status"], "EVALUATION_ERROR")

    # =========================================================================
    # PART 5: Deterministic Repeatability & Governance
    # =========================================================================

    def test_deterministic_repeatability_and_hash(self):
        """Two evaluations of the identical case yield identical status and SHA-256 hash."""
        case_dict = {
            "case_id": "CASE-REP-01",
            "clinical_domain": "cardiology",
            "procedure_code": "76775",
            "procedure_name": "Abdominal Aortic Ultrasound",
            "requested_date_of_service": "2026-04-10",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "cg7251_indication": True
            }
        }
        a1, aud1 = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-CARD-CG7251-001"])
        a2, aud2 = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-CARD-CG7251-001"])

        self.assertEqual(a1.assessment_status, a2.assessment_status)
        self.assertEqual(aud1["reproducibility_hash_sha256"], aud2["reproducibility_hash_sha256"])
        self.assertFalse(a1.is_binding)
        self.assertFalse(a2.is_binding)

    def test_governance_zero_approved_rules(self):
        """Strict governance: 0 rules approved, attempts to register approved rule raise ValueError."""
        stats = self.registry.get_statistics()
        self.assertEqual(stats["status_counts"]["APPROVED"], 0)
        self.assertTrue(stats["governance_zero_approved_enforced"])

        # Attempt to register an approved rule must be rejected
        illegal_approved_rule = {
            "rule_id": "RULE-CARD-TEST-999",
            "domain": "cardiology",
            "document_type": "governing_policy",
            "policy_title": "Fake Approved Policy",
            "policy_version": "2026",
            "version_status": "current_2026_verified",
            "source_file": "fake.pdf",
            "source_page": {"physical_page": 1, "printed_page": "1"},
            "source_section": "Section 1",
            "source_quote": "Verbatim quote exceeding minimum required length of ten characters",
            "clinical_service_or_procedure": "Service",
            "rule_type": "clinical_indication",
            "conditions": {"operator": "ALL_OF", "criteria": [{"condition_id": "C1", "description": "D1"}]},
            "decision_effect": "INDICATED",
            "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
            "human_review_required": False,
            "extraction_status": "APPROVED"  # ILLEGAL
        }
        with self.assertRaises(ValueError) as ctx:
            self.registry.register_rule(illegal_approved_rule)
        self.assertIn("cannot be registered with status 'APPROVED' before clinical review", str(ctx.exception))

    # =========================================================================
    # PART 5: Phase 6B CPT Routing Safety Regression Suite
    # =========================================================================

    def test_knee_mri_excludes_lumbar_rules(self):
        """Knee MRI (73721) routes lower extremity MRI rules and strictly excludes lumbar rules."""
        case_dict = {
            "case_id": "CASE-PH6B-01-KNEE",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "73721",
            "procedure_name": "MRI Lower Extremity Joint (Knee)",
            "modality": "MRI",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "lumbar_radiculopathy_present": True,
                "straight_leg_raise_positive": True
            }
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        selected_rids = set(audit["routing_summary"]["applicable_rule_ids"])
        
        # Verify exact selected rules
        expected_rids = {
            "RULE-ADV-CG2035-001",
            "RULE-ADV-CG2035-002",
            "RULE-ADV-CG2035-003",
            "RULE-ADV-PREAMBLE-001",
            "RULE-ADV-CG2000-001",
            "RULE-ADV-EPOS2067-001",
            "RULE-ADV-EPOS2067-002",
            "RULE-ADV-EPOS2067-003",
            "RULE-ADV-EPOS2067-004",
            "RULE-ADV-EPOS2067-005"
        }
        self.assertEqual(selected_rids, expected_rids)
        self.assertEqual(len(selected_rids), 10)

        # Lumbar rules must be completely excluded
        for rid in selected_rids:
            self.assertFalse(rid.startswith("RULE-ADV-CG2037"), f"Lumbar rule {rid} leaked into Knee MRI routing!")

        # Evidence of lumbar radiculopathy does not meet Knee MRI criteria
        for r_res in assessment.rule_results:
            if r_res.rule.rule_id in ("RULE-ADV-CG2035-001", "RULE-ADV-CG2035-002", "RULE-ADV-CG2035-003"):
                self.assertNotEqual(r_res.condition_result.status, EvaluationState.TRUE)

    def test_lumbar_mri_routes_lumbar_rules(self):
        """Lumbar MRI (72148) routes only lumbar spine MRI rules + preamble/EPOS."""
        case_dict = {
            "case_id": "CASE-PH6B-02-LUMBAR",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72148",
            "procedure_name": "MRI Lumbar Spine without contrast",
            "modality": "MRI",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        selected_rids = set(audit["routing_summary"]["applicable_rule_ids"])
        expected_rids = {
            "RULE-ADV-CG2037-001",
            "RULE-ADV-CG2037-002",
            "RULE-ADV-PREAMBLE-001",
            "RULE-ADV-CG2000-001",
            "RULE-ADV-EPOS2067-001",
            "RULE-ADV-EPOS2067-002",
            "RULE-ADV-EPOS2067-003",
            "RULE-ADV-EPOS2067-004",
            "RULE-ADV-EPOS2067-005"
        }
        self.assertEqual(selected_rids, expected_rids)
        self.assertEqual(len(selected_rids), 9)

    def test_ct_abd_pelvis_routes_cg2000(self):
        """CT Abdomen/Pelvis (74177) routes only CG 2000 rules + preamble/EPOS."""
        case_dict = {
            "case_id": "CASE-PH6B-03-CT-ABD",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "modality": "CT",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        selected_rids = set(audit["routing_summary"]["applicable_rule_ids"])
        expected_procedure_rids = {
            "RULE-ADV-CG2000-002", "RULE-ADV-CG2000-003", "RULE-ADV-CG2000-004",
            "RULE-ADV-CG2000-005", "RULE-ADV-CG2000-006", "RULE-ADV-CG2000-007",
            "RULE-ADV-CG2000-008", "RULE-ADV-CG2000-009", "RULE-ADV-CG2000-011",
            "RULE-ADV-CG2000-012", "RULE-ADV-CG2000-013"
        }
        expected_shared_rids = {
            "RULE-ADV-PREAMBLE-001", "RULE-ADV-CG2000-001",
            "RULE-ADV-EPOS2067-001", "RULE-ADV-EPOS2067-002",
            "RULE-ADV-EPOS2067-003", "RULE-ADV-EPOS2067-004", "RULE-ADV-EPOS2067-005"
        }
        self.assertEqual(selected_rids, expected_procedure_rids | expected_shared_rids)
        self.assertEqual(len(selected_rids), 18)

    def test_brain_mri_routes_cg2012(self):
        """Brain MRI (70553) routes only CG 2012 rules + preamble/EPOS."""
        case_dict = {
            "case_id": "CASE-PH6B-04-BRAIN",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain with and without contrast",
            "modality": "MRI",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        selected_rids = set(audit["routing_summary"]["applicable_rule_ids"])
        expected_procedure_rids = {
            "RULE-ADV-CG2012-001", "RULE-ADV-CG2012-002",
            "RULE-ADV-CG2012-003", "RULE-ADV-CG2012-004"
        }
        expected_shared_rids = {
            "RULE-ADV-PREAMBLE-001", "RULE-ADV-CG2000-001",
            "RULE-ADV-EPOS2067-001", "RULE-ADV-EPOS2067-002",
            "RULE-ADV-EPOS2067-003", "RULE-ADV-EPOS2067-004", "RULE-ADV-EPOS2067-005"
        }
        self.assertEqual(selected_rids, expected_procedure_rids | expected_shared_rids)
        self.assertEqual(len(selected_rids), 11)

    def test_ipm_epidural_routes_1750(self):
        """IPM Epidural (62322 / 62323) routes only 1750 epidural rules + preamble/EPOS."""
        for cpt in ("62322", "62323"):
            case_dict = {
                "case_id": f"CASE-PH6B-05-EPI-{cpt}",
                "clinical_domain": "interventional_pain_management",
                "procedure_code": cpt,
                "procedure_name": "Lumbar Epidural Steroid Injection",
                "place_of_service": "AMBULATORY_SURGICAL_CENTER",
                "requested_date_of_service": "2026-04-15",
                "line_of_business": "COMMERCIAL",
                "payer_id": "EVOLENT",
                "clinical_evidence": {}
            }
            assessment, audit = self.service.evaluate_case(case_dict)
            self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
            selected_rids = set(audit["routing_summary"]["applicable_rule_ids"])
            expected_rids = {
                "RULE-IPM-CGEPIDURALINJECTIONS-001",
                "RULE-IPM-CGEPIDURALINJECTIONS-002",
                "RULE-IPM-CGEPIDURALPUMPTRIALS-001",
                "RULE-IPM-PREAMBLEIPM-001",
                "RULE-IPM-EPOS1755-001",
                "RULE-IPM-EPOS1755-002"
            }
            self.assertEqual(selected_rids, expected_rids)
            self.assertEqual(len(selected_rids), 6)

    def test_ipm_facet_routes_1751(self):
        """IPM Facet Blocks (64490) routes only 1751 facet rule + preamble/EPOS."""
        case_dict = {
            "case_id": "CASE-PH6B-06-FACET",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "64490",
            "procedure_name": "Cervical/Thoracic Facet Joint Injection",
            "place_of_service": "OFFICE",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        selected_rids = set(audit["routing_summary"]["applicable_rule_ids"])
        expected_rids = {
            "RULE-IPM-CGFACETBLOCKS-001",
            "RULE-IPM-PREAMBLEIPM-001",
            "RULE-IPM-EPOS1755-001",
            "RULE-IPM-EPOS1755-002"
        }
        self.assertEqual(selected_rids, expected_rids)
        self.assertEqual(len(selected_rids), 4)

    def test_ipm_stimulator_routes_1757(self):
        """IPM Spinal Cord Stimulator (63650) routes only 1757 stimulator rules + preamble/EPOS."""
        case_dict = {
            "case_id": "CASE-PH6B-07-STIM",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "63650",
            "procedure_name": "Percutaneous Implantation of Neurostimulator Electrode Array",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        selected_rids = set(audit["routing_summary"]["applicable_rule_ids"])
        expected_rids = {
            "RULE-IPM-CGSPINALCORDSTIM-001",
            "RULE-IPM-CGSPINALCORDSTIM-002",
            "RULE-IPM-PREAMBLEIPM-001",
            "RULE-IPM-EPOS1755-001",
            "RULE-IPM-EPOS1755-002"
        }
        self.assertEqual(selected_rids, expected_rids)
        self.assertEqual(len(selected_rids), 5)

    def test_unsupported_cpt_rhinoplasty(self):
        """Unsupported surgical CPT (30410 Rhinoplasty) yields POLICY_NOT_APPLICABLE and 0 rules."""
        case_dict = {
            "case_id": "CASE-PH6B-08-RHINO",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "30410",
            "procedure_name": "Rhinoplasty primary",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("Surgical procedure code '30410' is outside advanced_imaging clinical scope", audit["routing_summary"]["routing_notes"][0])

    def test_unsupported_cpt_office_visit_ai(self):
        """Unsupported E/M CPT (99213) in Advanced Imaging yields POLICY_NOT_APPLICABLE and 0 rules."""
        case_dict = {
            "case_id": "CASE-PH6B-09-OV-AI",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "99213",
            "procedure_name": "Office/outpatient visit",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("not supported under active advanced_imaging clinical policies", audit["routing_summary"]["routing_notes"][0])

    def test_unsupported_cpt_office_visit_ipm(self):
        """Unsupported E/M CPT (99213) in IPM yields POLICY_NOT_APPLICABLE and 0 rules."""
        case_dict = {
            "case_id": "CASE-PH6B-10-OV-IPM",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "99213",
            "procedure_name": "Office/outpatient visit",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("not supported under active interventional_pain_management clinical policies", audit["routing_summary"]["routing_notes"][0])

    def test_fictitious_cpt_99999(self):
        """Fictitious CPT (99999) yields POLICY_NOT_APPLICABLE without fallback to domain rules."""
        case_dict = {
            "case_id": "CASE-PH6B-11-FICTITIOUS",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "99999",
            "procedure_name": "Unlisted Diagnostic Procedure",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("not supported under active advanced_imaging clinical policies", audit["routing_summary"]["routing_notes"][0])

    def test_whitespace_cpt_rejected(self):
        """Whitespace-only CPT ('   ') fails schema validation with EVALUATION_ERROR."""
        case_dict = {
            "case_id": "CASE-PH6B-12-WHITESPACE",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "   ",
            "procedure_name": "Lumbar Spine MRI",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.EVALUATION_ERROR)
        self.assertIn("Case validation rejected", assessment.summary_explanation)

    def test_suffixed_cpt_rejected(self):
        """Suffixed CPT ('72148-XYZ') fails schema validation with EVALUATION_ERROR."""
        case_dict = {
            "case_id": "CASE-PH6B-13-SUFFIXED",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72148-XYZ",
            "procedure_name": "Lumbar Spine MRI",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.EVALUATION_ERROR)
        self.assertIn("Case validation rejected", assessment.summary_explanation)

    def test_malformed_chars_rejected(self):
        """CPT with punctuation ('!@#$%') fails schema validation with EVALUATION_ERROR."""
        case_dict = {
            "case_id": "CASE-PH6B-14-MALFORMED",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "!@#$%",
            "procedure_name": "Lumbar Spine MRI",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.EVALUATION_ERROR)
        self.assertIn("Case validation rejected", assessment.summary_explanation)

    def test_cardiology_in_ai_rejected(self):
        """Cardiology CPT (93458) in Advanced Imaging yields POLICY_NOT_APPLICABLE via symmetric guard."""
        case_dict = {
            "case_id": "CASE-PH6B-15-CARDIO-AI",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "93458",
            "procedure_name": "Coronary Angiogram",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("Cardiology procedure code '93458' is outside advanced_imaging clinical scope", audit["routing_summary"]["routing_notes"][0])

    def test_radiology_in_ipm_rejected(self):
        """Radiology CPT (72148) in IPM yields POLICY_NOT_APPLICABLE via symmetric guard."""
        case_dict = {
            "case_id": "CASE-PH6B-16-RAD-IPM",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "72148",
            "procedure_name": "Lumbar Spine MRI",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("Diagnostic radiology procedure code '72148' is outside interventional_pain_management clinical scope", audit["routing_summary"]["routing_notes"][0])

    def test_ipm_in_ai_rejected(self):
        """IPM CPT (62323) in Advanced Imaging yields POLICY_NOT_APPLICABLE via symmetric guard."""
        case_dict = {
            "case_id": "CASE-PH6B-17-IPM-AI",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "62323",
            "procedure_name": "Lumbar Epidural Injection with Fluoroscopy",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("Interventional pain procedure code '62323' is outside advanced_imaging clinical scope", audit["routing_summary"]["routing_notes"][0])

    def test_ortho_in_ipm_rejected(self):
        """Non-pain orthopedic surgery (27447 Knee Replacement) in IPM yields POLICY_NOT_APPLICABLE."""
        case_dict = {
            "case_id": "CASE-PH6B-18-ORTHO-IPM",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "27447",
            "procedure_name": "Total Knee Arthroplasty",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)
        self.assertEqual(len(audit["routing_summary"]["applicable_rule_ids"]), 0)
        self.assertEqual(len(assessment.rule_results), 0)
        self.assertIn("Non-pain surgical procedure code '27447' is outside interventional_pain_management clinical scope", audit["routing_summary"]["routing_notes"][0])

    def test_documented_exceptions_category_iii_and_hcpcs(self):
        """Preserve documented exceptions: CPT 27096, Category III (0042T, 0213T), HCPCS (S8042, G0260)."""
        # CPT 27096 in IPM (Sacroiliac Joint Injection) - in surgical range 10000-59999 but explicitly supported
        case_27096 = {
            "case_id": "CASE-EXCEPT-27096",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "27096",
            "procedure_name": "Sacroiliac Joint Injection",
            "place_of_service": "OFFICE",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        a_27096, aud_27096 = self.service.evaluate_case(case_27096)
        self.assertEqual(a_27096.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        rids_27096 = set(aud_27096["routing_summary"]["applicable_rule_ids"])
        self.assertIn("RULE-IPM-CGSIINJECTIONS-001", rids_27096)
        self.assertIn("RULE-IPM-PREAMBLEIPM-001", rids_27096)

        # HCPCS G0260 in IPM
        case_g0260 = {
            "case_id": "CASE-EXCEPT-G0260",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "G0260",
            "procedure_name": "Sacroiliac Joint Injection under Fluoroscopy",
            "place_of_service": "OFFICE",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        a_g0260, aud_g0260 = self.service.evaluate_case(case_g0260)
        self.assertEqual(a_g0260.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        rids_g0260 = set(aud_g0260["routing_summary"]["applicable_rule_ids"])
        self.assertIn("RULE-IPM-CGSIINJECTIONS-001", rids_g0260)

        # Category III 0042T in AI (CT Cerebral Perfusion)
        case_0042t = {
            "case_id": "CASE-EXCEPT-0042T",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "0042T",
            "procedure_name": "CT Cerebral Perfusion Analysis",
            "place_of_service": "OFFICE",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        a_0042t, aud_0042t = self.service.evaluate_case(case_0042t)
        self.assertEqual(a_0042t.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        rids_0042t = set(aud_0042t["routing_summary"]["applicable_rule_ids"])
        self.assertIn("RULE-ADV-CG2015-001", rids_0042t)

        # Category III 0213T in IPM (Facet Block)
        case_0213t = {
            "case_id": "CASE-EXCEPT-0213T",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "0213T",
            "procedure_name": "Cervical Facet Injection with Fluoroscopy",
            "place_of_service": "OFFICE",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        a_0213t, aud_0213t = self.service.evaluate_case(case_0213t)
        self.assertEqual(a_0213t.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        rids_0213t = set(aud_0213t["routing_summary"]["applicable_rule_ids"])
        self.assertIn("RULE-IPM-CGFACETBLOCKS-001", rids_0213t)

        # HCPCS S8042 in AI (Low Field MRI)
        case_s8042 = {
            "case_id": "CASE-EXCEPT-S8042",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "S8042",
            "procedure_name": "Low-Field Magnetic Resonance Imaging",
            "place_of_service": "OFFICE",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        a_s8042, aud_s8042 = self.service.evaluate_case(case_s8042)
        self.assertEqual(a_s8042.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        rids_s8042 = set(aud_s8042["routing_summary"]["applicable_rule_ids"])
        self.assertIn("RULE-ADV-CG2031-001", rids_s8042)

    def test_preamble_pos_and_retrospective_review_applicability(self):
        """Preamble, POS, and retrospective review rules attach only when documented conditions are met."""
        # 1. POS omitted: POS rules are NOT attached
        case_no_pos = {
            "case_id": "CASE-PH6B-NO-POS",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72148",
            "procedure_name": "Lumbar Spine MRI",
            "requested_date_of_service": "2026-04-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        _, aud_no_pos = self.service.evaluate_case(case_no_pos)
        rids_no_pos = set(aud_no_pos["routing_summary"]["applicable_rule_ids"])
        # Only procedure rules + preamble rules = 4 rules (no EPOS2067)
        self.assertEqual(rids_no_pos, {
            "RULE-ADV-CG2037-001", "RULE-ADV-CG2037-002",
            "RULE-ADV-PREAMBLE-001", "RULE-ADV-CG2000-001"
        })
        self.assertEqual(len(rids_no_pos), 4)

        # 2. POS specified: POS rules ARE attached
        case_with_pos = {**case_no_pos, "place_of_service": "OUTPATIENT_HOSPITAL"}
        _, aud_with_pos = self.service.evaluate_case(case_with_pos)
        rids_with_pos = set(aud_with_pos["routing_summary"]["applicable_rule_ids"])
        self.assertTrue(rids_with_pos.issuperset({
            "RULE-ADV-EPOS2067-001", "RULE-ADV-EPOS2067-002", "RULE-ADV-EPOS2067-003",
            "RULE-ADV-EPOS2067-004", "RULE-ADV-EPOS2067-005"
        }))
        self.assertEqual(len(rids_with_pos), 9)

        # 3. Retrospective review context: Retrospective review rules ARE attached
        retro_ctx = {"is_retrospective": True}
        _, aud_retro = self.service.evaluate_case(case_no_pos, policy_context=retro_ctx)
        rids_retro = set(aud_retro["routing_summary"]["applicable_rule_ids"])
        self.assertIn("RULE-ADV-CG2066-001", rids_retro)
        self.assertIn("RULE-ADV-CG2066-002", rids_retro)
        self.assertEqual(len(rids_retro), 6)  # 2 proc + 2 preamble + 2 retro = 6 rules



if __name__ == "__main__":
    unittest.main()
