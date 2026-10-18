"""MedRule Phase 3A Comprehensive Evaluator Test Suite.

Verifies all 20 required test scenarios specified in Step Six:
1. Fully satisfied condition
2. Clearly unsatisfied condition
3. Missing mandatory information
4. Invalid input types
5. Unknown Boolean operands (Three-valued logic truth tables)
6. Nested ALL_OF conditions
7. Nested ANY_OF conditions
8. NONE_OF conditions with false and unknown children
9. Numerical thresholds immediately below, equal to, and above boundary
10. Date-of-service policy applicability
11. Historical versus current policy selection
12. Unavailable plan-specific dependency
13. Rule marked NEEDS_HUMAN_REVIEW
14. Non-binding draft rule execution
15. Conflicting or duplicate applicable rules
16. Empty or unavailable applicable rule set
17. Invalid policy version
18. Source traceability in final result
19. Regression checks across all nine domains
20. Deterministic repeatability for identical inputs
"""

import copy
import datetime
import json
from pathlib import Path
import unittest

from medrule_engine.case_validator import CaseValidator, validate_case
from medrule_engine.condition_evaluator import ConditionEvaluator, EvaluationState
from medrule_engine.decision_aggregator import CaseAssessmentStatus, DecisionAggregator
from medrule_engine.evaluation_service import EvaluationService, evaluate_case, evaluate_rule
from medrule_engine.evidence_validator import EvidenceValidator
from medrule_engine.policy_router import PolicyRouter
from medrule_engine.rule_registry import RuleRecord, RuleRegistry

BASE_DIR = Path(__file__).resolve().parents[2]


class TestMedRuleDeterministicEngine(unittest.TestCase):
    """Rigorous deterministic unit test suite for MedRule Phase 3A."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry()
        cls.total_rules = cls.registry.load_all_domains()
        cls.service = EvaluationService(registry=cls.registry)
        cls.evaluator = ConditionEvaluator()
        cls.validator = CaseValidator()

    # -------------------------------------------------------------------------
    # Test 1: Fully satisfied condition (CRITERIA_MET)
    # -------------------------------------------------------------------------
    def test_01_fully_satisfied_condition(self):
        """Check 1: Complete case evidence meeting all criteria yields CRITERIA_MET."""
        case_dict = {
            "case_id": "CASE-TEST-001",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "modality": "CT",
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
        assessment, audit = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.CRITERIA_MET)
        self.assertFalse(assessment.is_binding)
        self.assertEqual(len(assessment.rule_results), 1)
        self.assertEqual(assessment.rule_results[0].condition_result.status, EvaluationState.TRUE)

    # -------------------------------------------------------------------------
    # Test 2: Clearly unsatisfied condition (CRITERIA_NOT_MET)
    # -------------------------------------------------------------------------
    def test_02_clearly_unsatisfied_condition(self):
        """Check 2: Evidence violating a mandatory threshold yields CRITERIA_NOT_MET."""
        case_dict = {
            "case_id": "CASE-TEST-002",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "modality": "CT",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "pancreatitis_diagnostic_markers": "ELEVATED",
                "conservative_treatment_duration_hours": 24,  # Violates >= 72h
                "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT"
            }
        }
        assessment, audit = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.CRITERIA_NOT_MET)
        self.assertFalse(assessment.is_binding)
        self.assertEqual(assessment.rule_results[0].condition_result.status, EvaluationState.FALSE)

    # -------------------------------------------------------------------------
    # Test 3: Missing mandatory information (INSUFFICIENT_INFORMATION)
    # -------------------------------------------------------------------------
    def test_03_missing_mandatory_information(self):
        """Check 3: Missing mandatory evidence parameters yields INSUFFICIENT_INFORMATION."""
        case_dict = {
            "case_id": "CASE-TEST-003",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "modality": "CT",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "pancreatitis_diagnostic_markers": "ELEVATED"
                # Missing conservative_treatment_duration_hours and ultrasound_findings
            }
        }
        assessment, audit = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.INSUFFICIENT_INFORMATION)
        self.assertGreaterEqual(len(assessment.missing_evidence_summary), 2)
        self.assertFalse(assessment.is_binding)

    # -------------------------------------------------------------------------
    # Test 4: Invalid input types (validation error / EVALUATION_ERROR)
    # -------------------------------------------------------------------------
    def test_04_invalid_input_types(self):
        """Check 4: Invalid payload types rejected by validator with EVALUATION_ERROR."""
        invalid_cases = [
            {"case_id": "CASE-INVALID-001", "clinical_domain": "UNKNOWN_DOMAIN"},  # Invalid domain enum
            {"case_id": "INVALID_ID_FORMAT", "clinical_domain": "advanced_imaging"},  # Pattern failure
            "NOT_A_DICTIONARY"  # Primitive type
        ]
        for bad_case in invalid_cases:
            if isinstance(bad_case, dict):
                is_valid, errs, _ = self.validator.validate(bad_case)
                self.assertFalse(is_valid)
                self.assertGreater(len(errs), 0)
                assessment, audit = self.service.evaluate_case(bad_case)
                self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.EVALUATION_ERROR)
            else:
                is_valid, errs, _ = self.validator.validate(bad_case)
                self.assertFalse(is_valid)

    # -------------------------------------------------------------------------
    # Test 5: Three-Valued Logic Truth Table Permutations
    # -------------------------------------------------------------------------
    def test_05_three_valued_logic_truth_tables(self):
        """Check 5: Exhaustive verification of TRUE, FALSE, UNKNOWN over ALL_OF, ANY_OF, NONE_OF."""
        # Helper to construct dummy case with specified parameter states
        def make_test_case(evidence_dict):
            return self.validator.validate({
                "case_id": "CASE-TEST-LOGIC",
                "clinical_domain": "advanced_imaging",
                "procedure_code": "70553",
                "procedure_name": "MRI Brain",
                "requested_date_of_service": "2026-03-01",
                "line_of_business": "COMMERCIAL",
                "payer_id": "EVOLENT",
                "clinical_evidence": evidence_dict
            })[2]

        # Criteria: A (equals 10), B (equals 20)
        def make_group(op):
            return {
                "operator": op,
                "criteria": [
                    {"condition_id": "C1", "description": "Param A", "parameter": "p_a", "comparator": "EQUALS", "value": 10},
                    {"condition_id": "C2", "description": "Param B", "parameter": "p_b", "comparator": "EQUALS", "value": 20}
                ]
            }

        # 1. ALL_OF permutations:
        # [T, T] -> T
        res = self.evaluator.evaluate(make_group("ALL_OF"), make_test_case({"p_a": 10, "p_b": 20}))
        self.assertEqual(res.status, EvaluationState.TRUE)
        # [T, F] -> F
        res = self.evaluator.evaluate(make_group("ALL_OF"), make_test_case({"p_a": 10, "p_b": 99}))
        self.assertEqual(res.status, EvaluationState.FALSE)
        # [F, U] -> F (short-circuit on F)
        res = self.evaluator.evaluate(make_group("ALL_OF"), make_test_case({"p_a": 99}))
        self.assertEqual(res.status, EvaluationState.FALSE)
        # [T, U] -> U
        res = self.evaluator.evaluate(make_group("ALL_OF"), make_test_case({"p_a": 10}))
        self.assertEqual(res.status, EvaluationState.UNKNOWN)
        # [U, U] -> U
        res = self.evaluator.evaluate(make_group("ALL_OF"), make_test_case({}))
        self.assertEqual(res.status, EvaluationState.UNKNOWN)

        # 2. ANY_OF permutations:
        # [T, F] -> T (short-circuit on T)
        res = self.evaluator.evaluate(make_group("ANY_OF"), make_test_case({"p_a": 10, "p_b": 99}))
        self.assertEqual(res.status, EvaluationState.TRUE)
        # [T, U] -> T (short-circuit on T)
        res = self.evaluator.evaluate(make_group("ANY_OF"), make_test_case({"p_a": 10}))
        self.assertEqual(res.status, EvaluationState.TRUE)
        # [F, F] -> F
        res = self.evaluator.evaluate(make_group("ANY_OF"), make_test_case({"p_a": 99, "p_b": 99}))
        self.assertEqual(res.status, EvaluationState.FALSE)
        # [F, U] -> U
        res = self.evaluator.evaluate(make_group("ANY_OF"), make_test_case({"p_a": 99}))
        self.assertEqual(res.status, EvaluationState.UNKNOWN)
        # [U, U] -> U
        res = self.evaluator.evaluate(make_group("ANY_OF"), make_test_case({}))
        self.assertEqual(res.status, EvaluationState.UNKNOWN)

        # 3. NONE_OF permutations:
        # [F, F] -> T (none hold)
        res = self.evaluator.evaluate(make_group("NONE_OF"), make_test_case({"p_a": 99, "p_b": 99}))
        self.assertEqual(res.status, EvaluationState.TRUE)
        # [T, F] -> F (disqualifier holds, short-circuit)
        res = self.evaluator.evaluate(make_group("NONE_OF"), make_test_case({"p_a": 10, "p_b": 99}))
        self.assertEqual(res.status, EvaluationState.FALSE)
        # [T, U] -> F (disqualifier holds, short-circuit)
        res = self.evaluator.evaluate(make_group("NONE_OF"), make_test_case({"p_a": 10}))
        self.assertEqual(res.status, EvaluationState.FALSE)
        # [F, U] -> U (cannot confirm none hold)
        res = self.evaluator.evaluate(make_group("NONE_OF"), make_test_case({"p_a": 99}))
        self.assertEqual(res.status, EvaluationState.UNKNOWN)
        # [U, U] -> U
        res = self.evaluator.evaluate(make_group("NONE_OF"), make_test_case({}))
        self.assertEqual(res.status, EvaluationState.UNKNOWN)

    # -------------------------------------------------------------------------
    # Test 6: Nested ALL_OF conditions
    # -------------------------------------------------------------------------
    def test_06_nested_all_of_conditions(self):
        """Check 6: Tree with nested ALL_OF sub-condition evaluated accurately."""
        tree = {
            "operator": "ALL_OF",
            "criteria": [
                {"condition_id": "ROOT-1", "description": "Root prerequisite", "parameter": "root_param", "comparator": "EQUALS", "value": "A"},
                {
                    "condition_id": "ROOT-2",
                    "description": "Nested group",
                    "sub_conditions": {
                        "operator": "ALL_OF",
                        "criteria": [
                            {"condition_id": "SUB-1", "description": "Sub 1", "parameter": "sub_param_1", "comparator": "EQUALS", "value": 1},
                            {"condition_id": "SUB-2", "description": "Sub 2", "parameter": "sub_param_2", "comparator": "EQUALS", "value": 2}
                        ]
                    }
                }
            ]
        }
        case = self.validator.validate({
            "case_id": "CASE-NESTED-ALL",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"root_param": "A", "sub_param_1": 1, "sub_param_2": 2}
        })[2]
        res = self.evaluator.evaluate(tree, case)
        self.assertEqual(res.status, EvaluationState.TRUE)

        # Fails if one sub-condition fails
        case_fail = self.validator.validate({
            "case_id": "CASE-NESTED-ALL-FAIL",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"root_param": "A", "sub_param_1": 1, "sub_param_2": 999}
        })[2]
        res_fail = self.evaluator.evaluate(tree, case_fail)
        self.assertEqual(res_fail.status, EvaluationState.FALSE)

    # -------------------------------------------------------------------------
    # Test 7: Nested ANY_OF conditions
    # -------------------------------------------------------------------------
    def test_07_nested_any_of_conditions(self):
        """Check 7: ALL_OF containing nested ANY_OF alternatives."""
        tree = {
            "operator": "ALL_OF",
            "criteria": [
                {"condition_id": "ROOT-1", "description": "Mandatory diagnosis", "parameter": "has_dx", "comparator": "EQUALS", "value": True},
                {
                    "condition_id": "ROOT-2",
                    "description": "Either conservative therapy or red flag",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {"condition_id": "ALT-1", "description": "PT completed", "parameter": "pt_completed", "comparator": "EQUALS", "value": True},
                            {"condition_id": "ALT-2", "description": "Red flag neurological deficit", "parameter": "red_flag", "comparator": "EQUALS", "value": True}
                        ]
                    }
                }
            ]
        }
        # Satisfied via alternative 2 (red flag) without alternative 1 (PT)
        case = self.validator.validate({
            "case_id": "CASE-NESTED-ANY",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"has_dx": True, "pt_completed": False, "red_flag": True}
        })[2]
        res = self.evaluator.evaluate(tree, case)
        self.assertEqual(res.status, EvaluationState.TRUE)

    # -------------------------------------------------------------------------
    # Test 8: NONE_OF conditions with false and unknown children
    # -------------------------------------------------------------------------
    def test_08_none_of_with_false_and_unknown_children(self):
        """Check 8: NONE_OF returns TRUE only when all children are FALSE, UNKNOWN if any child unknown."""
        tree = {
            "operator": "NONE_OF",
            "criteria": [
                {"condition_id": "EXCL-1", "description": "Active infection", "parameter": "active_infection", "comparator": "EQUALS", "value": True},
                {"condition_id": "EXCL-2", "description": "Absolute contraindication", "parameter": "contraindicated", "comparator": "EQUALS", "value": True}
            ]
        }
        # Both exclusions FALSE -> NONE_OF is TRUE
        case_clean = self.validator.validate({
            "case_id": "CASE-NONE-CLEAN",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"active_infection": False, "contraindicated": False}
        })[2]
        self.assertEqual(self.evaluator.evaluate(tree, case_clean).status, EvaluationState.TRUE)

        # One exclusion UNKNOWN -> NONE_OF is UNKNOWN
        case_unk = self.validator.validate({
            "case_id": "CASE-NONE-UNK",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"active_infection": False}  # contraindicated missing
        })[2]
        self.assertEqual(self.evaluator.evaluate(tree, case_unk).status, EvaluationState.UNKNOWN)

    # -------------------------------------------------------------------------
    # Test 9: Numerical thresholds immediately below, equal to, and above boundary
    # -------------------------------------------------------------------------
    def test_09_numerical_threshold_boundaries(self):
        """Check 9: Exact boundary testing on verified clinical thresholds (< 35, >= 72, > 25, BETWEEN [3, 25])."""
        # Threshold 1: GREATER_THAN_OR_EQUAL 72 (RULE-ADV-CG2000-006)
        crit_gte_72 = {"condition_id": "C", "description": "Duration >= 72h", "parameter": "dur", "comparator": "GREATER_THAN_OR_EQUAL", "value": 72}
        tree_gte = {"operator": "SINGLE_CONDITION", "criteria": [crit_gte_72]}
        
        # 71 (below) -> FALSE
        c71 = self.validator.validate({"case_id": "CASE-THRESH-71", "clinical_domain": "advanced_imaging", "procedure_code": "74177", "procedure_name": "CT Abdomen", "requested_date_of_service": "2026-03-01", "line_of_business": "COMMERCIAL", "payer_id": "EVOLENT", "clinical_evidence": {"dur": 71}})[2]
        self.assertEqual(self.evaluator.evaluate(tree_gte, c71).status, EvaluationState.FALSE)
        # 72 (equal) -> TRUE
        c72 = self.validator.validate({"case_id": "CASE-THRESH-72", "clinical_domain": "advanced_imaging", "procedure_code": "74177", "procedure_name": "CT Abdomen", "requested_date_of_service": "2026-03-01", "line_of_business": "COMMERCIAL", "payer_id": "EVOLENT", "clinical_evidence": {"dur": 72}})[2]
        self.assertEqual(self.evaluator.evaluate(tree_gte, c72).status, EvaluationState.TRUE)
        # 73 (above) -> TRUE
        c73 = self.validator.validate({"case_id": "CASE-THRESH-73", "clinical_domain": "advanced_imaging", "procedure_code": "74177", "procedure_name": "CT Abdomen", "requested_date_of_service": "2026-03-01", "line_of_business": "COMMERCIAL", "payer_id": "EVOLENT", "clinical_evidence": {"dur": 73}})[2]
        self.assertEqual(self.evaluator.evaluate(tree_gte, c73).status, EvaluationState.TRUE)

        # Threshold 2: LESS_THAN 35 (RULE-ADV-CG2000-003)
        crit_lt_35 = {"condition_id": "C", "description": "Age < 35", "parameter": "patient_age_years", "comparator": "LESS_THAN", "value": 35}
        tree_lt = {"operator": "SINGLE_CONDITION", "criteria": [crit_lt_35]}
        
        # 34 -> TRUE
        c34 = self.validator.validate({"case_id": "CASE-THRESH-34", "clinical_domain": "advanced_imaging", "procedure_code": "74177", "procedure_name": "CT Abdomen", "requested_date_of_service": "2026-03-01", "line_of_business": "COMMERCIAL", "payer_id": "EVOLENT", "clinical_evidence": {"patient_age_years": 34}})[2]
        self.assertEqual(self.evaluator.evaluate(tree_lt, c34).status, EvaluationState.TRUE)
        # 35 -> FALSE (strictly less than)
        c35 = self.validator.validate({"case_id": "CASE-THRESH-35", "clinical_domain": "advanced_imaging", "procedure_code": "74177", "procedure_name": "CT Abdomen", "requested_date_of_service": "2026-03-01", "line_of_business": "COMMERCIAL", "payer_id": "EVOLENT", "clinical_evidence": {"patient_age_years": 35}})[2]
        self.assertEqual(self.evaluator.evaluate(tree_lt, c35).status, EvaluationState.FALSE)
        # 36 -> FALSE
        c36 = self.validator.validate({"case_id": "CASE-THRESH-36", "clinical_domain": "advanced_imaging", "procedure_code": "74177", "procedure_name": "CT Abdomen", "requested_date_of_service": "2026-03-01", "line_of_business": "COMMERCIAL", "payer_id": "EVOLENT", "clinical_evidence": {"patient_age_years": 36}})[2]
        self.assertEqual(self.evaluator.evaluate(tree_lt, c36).status, EvaluationState.FALSE)

        # Threshold 3: BETWEEN [3, 25] (RULE-ADV-CG2000-009)
        crit_btw = {"condition_id": "C", "description": "RBC 3-25", "parameter": "rbc", "comparator": "BETWEEN", "value": [3, 25]}
        tree_btw = {"operator": "SINGLE_CONDITION", "criteria": [crit_btw]}
        
        for val, exp_st in [(2, EvaluationState.FALSE), (3, EvaluationState.TRUE), (14, EvaluationState.TRUE), (25, EvaluationState.TRUE), (26, EvaluationState.FALSE)]:
            c = self.validator.validate({"case_id": f"CASE-THRESH-RBC-{val}", "clinical_domain": "advanced_imaging", "procedure_code": "74177", "procedure_name": "CT Abdomen", "requested_date_of_service": "2026-03-01", "line_of_business": "COMMERCIAL", "payer_id": "EVOLENT", "clinical_evidence": {"rbc": val}})[2]
            self.assertEqual(self.evaluator.evaluate(tree_btw, c).status, exp_st, f"Failed BETWEEN for value {val}")

    # -------------------------------------------------------------------------
    # Test 10: Date-of-service policy applicability
    # -------------------------------------------------------------------------
    def test_10_date_of_service_applicability(self):
        """Check 10: Dates of service outside active 2026 policy effective range yield POLICY_VERSION_UNRESOLVED."""
        case_dict = {
            "case_id": "CASE-DOS-HISTORICAL",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2024-06-15",  # Historical date
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_VERSION_UNRESOLVED)

    # -------------------------------------------------------------------------
    # Test 11: Historical versus current policy selection
    # -------------------------------------------------------------------------
    def test_11_historical_vs_current_policy_selection(self):
        """Check 11: Registry enforces current_2026_verified policies and isolates historical baselines."""
        # Active Centene CP.MP.107 is Rev. 08/26
        rule_active = self.registry.get_rule("RULE-DME-107-001")
        self.assertIsNotNone(rule_active)
        self.assertEqual(rule_active.version_status, "current_2026_verified")
        self.assertEqual(rule_active.policy_version, "Revision 08/26")

        # Quarantined historical DOC-CEN-002 has no active rules loaded in draft_rules.json
        for r in self.registry.get_rules_by_domain("centene_dme_orthotics_prosthetics"):
            self.assertNotEqual(r.policy_version, "Revision 11/24", "Historical policy leaked into active rule registry!")

    # -------------------------------------------------------------------------
    # Test 12: Unavailable plan-specific dependency
    # -------------------------------------------------------------------------
    def test_12_unavailable_plan_dependency(self):
        """Check 12: Unknown line of business triggers MANUAL_REVIEW_REQUIRED."""
        case_dict = {
            "case_id": "CASE-LOB-OTHER",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "OTHER",  # Unresolved statutory benefit LOB
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)

    # -------------------------------------------------------------------------
    # Test 13: Rule marked NEEDS_HUMAN_REVIEW
    # -------------------------------------------------------------------------
    def test_13_rule_marked_needs_human_review(self):
        """Check 13: Applicable rule flagged NEEDS_HUMAN_REVIEW escalates to MANUAL_REVIEW_REQUIRED."""
        case_dict = {
            "case_id": "CASE-HUMAN-REVIEW",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis / CT Enterography",
            "modality": "CT",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "requested_modality": "CT",
                "patient_age_years": 25  # Meets criteria of RULE-ADV-CG2000-003
            }
        }
        assessment, audit = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-003"])
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
        self.assertGreater(len(assessment.human_review_escalations), 0)

    # -------------------------------------------------------------------------
    # Test 14: Draft rule non-binding governance
    # -------------------------------------------------------------------------
    def test_14_draft_rule_non_binding_governance(self):
        """Check 14: Verified that all evaluations are strictly non-binding with is_binding=False."""
        all_rules = self.registry.get_all_rules()
        self.assertEqual(len(all_rules), 372)
        # 100% of rules must have is_binding False and is_approved False
        for r in all_rules:
            self.assertFalse(r.is_binding, f"Rule {r.rule_id} marked binding!")
            self.assertFalse(r.is_approved, f"Rule {r.rule_id} marked approved!")

        case_dict = {
            "case_id": "CASE-GOV-TEST",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED", "conservative_treatment_duration_hours": 90, "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT"}
        }
        assessment, audit = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])
        self.assertFalse(assessment.is_binding)
        self.assertIn("NON-BINDING", assessment.disclaimer)
        self.assertFalse(audit["audit_header"]["is_binding_adjudication"])

    # -------------------------------------------------------------------------
    # Test 15: Conflicting or duplicate applicable rules
    # -------------------------------------------------------------------------
    def test_15_conflicting_or_duplicate_rules(self):
        """Check 15: Registry prevents duplicate rule ID registration."""
        reg = RuleRegistry()
        reg.load_all_domains()
        dup_rule = {
            "rule_id": "RULE-ADV-CG2000-001",  # Already loaded
            "domain": "advanced_imaging",
            "document_type": "governing_policy",
            "policy_title": "Test Duplicate",
            "policy_version": "2026",
            "version_status": "current_2026_verified",
            "source_file": "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/test.pdf",
            "source_page": {"physical_page": 1},
            "source_section": "Sec 1",
            "source_quote": "Exact verbatim quote exceeding ten chars",
            "clinical_service_or_procedure": "MRI",
            "rule_type": "clinical_indication",
            "conditions": {"operator": "ALL_OF", "criteria": [{"condition_id": "C1", "description": "D", "parameter": "p", "comparator": "EQUALS", "value": 1}]},
            "decision_effect": "INDICATED",
            "missing_information_behavior": "CANNOT_DETERMINE",
            "human_review_required": False,
            "extraction_status": "DRAFT"
        }
        with self.assertRaises(ValueError) as ctx:
            reg.register_rule(dup_rule)
        self.assertIn("Duplicate global rule ID detected", str(ctx.exception))

    # -------------------------------------------------------------------------
    # Test 16: Empty or unavailable applicable rule set
    # -------------------------------------------------------------------------
    def test_16_empty_applicable_rule_set(self):
        """Check 16: Requesting evaluation with empty applicable rules yields POLICY_NOT_APPLICABLE."""
        case_dict = {
            "case_id": "CASE-NO-RULES",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "00000",
            "procedure_name": "Nonexistent Procedure",
            "modality": "HYPERBARIC_CHAMBER",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict, applicable_rules=[])
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_NOT_APPLICABLE)

    # -------------------------------------------------------------------------
    # Test 17: Invalid policy version
    # -------------------------------------------------------------------------
    def test_17_invalid_policy_version(self):
        """Check 17: Date of service preceding policy effective date yields POLICY_VERSION_UNRESOLVED."""
        case_dict = {
            "case_id": "CASE-BAD-DOS",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70553",
            "procedure_name": "MRI Brain",
            "requested_date_of_service": "2024-06-15",  # Historical date outside 2026 guidelines
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment, audit = self.service.evaluate_case(case_dict)
        self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.POLICY_VERSION_UNRESOLVED)

    # -------------------------------------------------------------------------
    # Test 18: Source traceability in final result
    # -------------------------------------------------------------------------
    def test_18_source_traceability_in_audit_output(self):
        """Check 18: Every evaluated rule carries complete source citation, page, and verbatim quote."""
        case_dict = {
            "case_id": "CASE-TRACE-TEST",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen",
            "requested_date_of_service": "2026-03-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED", "conservative_treatment_duration_hours": 90, "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT"}
        }
        _, audit = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])
        eval_record = audit["rule_evaluations"][0]
        prov = eval_record["policy_provenance"]
        self.assertTrue(prov["policy_title"])
        self.assertTrue(prov["policy_version"])
        self.assertTrue(prov["source_file"].endswith(".pdf"))
        self.assertGreater(prov["physical_page"], 0)
        self.assertGreater(len(prov["source_quote"]), 10)

    # -------------------------------------------------------------------------
    # Test 19: Regression checks across all nine domains
    # -------------------------------------------------------------------------
    def test_19_regression_across_all_nine_domains(self):
        """Check 19: Successfully loads and evaluates candidate rules across all nine clinical domains."""
        domain_sample_rules = {
            "advanced_imaging": "RULE-ADV-CG2000-006",
            "cardiology": "RULE-CARD-CG7251-001",
            "centene_dme_orthotics_prosthetics": "RULE-DME-107-002",
            "genetic_testing": "RULE-GEN-CGBREASTPROGNOSTIC-002",
            "interventional_pain_management": "RULE-IPM-CGEPIDURALINJECTIONS-001",
            "musculoskeletal_surgery": "RULE-MSK-CGCERVICALLUMBAR-002",
            "physical_medicine": "RULE-PHY-ECG1501CHIROINFANT-001",
            "radiation_oncology": "RULE-RAD-ECG7000BONEPALLIATION-001",
            "sleep_health": "RULE-SLP-CG2050-001"
        }
        for domain, rid in domain_sample_rules.items():
            rule = self.registry.get_rule(rid)
            self.assertIsNotNone(rule, f"Sample rule {rid} not found in domain {domain}")
            self.assertEqual(rule.domain, domain)
            
            case_dict = {
                "case_id": f"CASE-REGRESS-{domain.upper()[:4]}",
                "clinical_domain": domain,
                "procedure_code": "00001",
                "procedure_name": f"Regression test for {domain}",
                "requested_date_of_service": "2026-08-15",
                "line_of_business": "COMMERCIAL",
                "payer_id": "TEST_PAYER",
                "clinical_evidence": {}
            }
            assessment, audit = self.service.evaluate_case(case_dict, target_rule_ids=[rid])
            self.assertIn(
                assessment.assessment_status,
                (CaseAssessmentStatus.INSUFFICIENT_INFORMATION, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED, CaseAssessmentStatus.CRITERIA_MET, CaseAssessmentStatus.CRITERIA_NOT_MET),
                f"Domain {domain} evaluation crashed or returned unexpected error: {assessment.summary_explanation}"
            )
            self.assertEqual(len(audit["rule_evaluations"]), 1)

    # -------------------------------------------------------------------------
    # Test 20: Deterministic repeatability for identical inputs
    # -------------------------------------------------------------------------
    def test_20_deterministic_repeatability(self):
        """Check 20: Multiple runs with identical inputs produce identical evaluations and SHA-256 hashes."""
        case_dict = {
            "case_id": "CASE-REPEATABLE-001",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "modality": "CT",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "pancreatitis_diagnostic_markers": "ELEVATED",
                "conservative_treatment_duration_hours": 96,
                "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT"
            }
        }
        _, audit_run_1 = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])
        _, audit_run_2 = self.service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])

        hash1 = audit_run_1["reproducibility_hash_sha256"]
        hash2 = audit_run_2["reproducibility_hash_sha256"]
        self.assertEqual(hash1, hash2, "Deterministic hash mismatch between identical evaluation runs!")
        self.assertEqual(
            audit_run_1["case_assessment"]["assessment_status"],
            audit_run_2["case_assessment"]["assessment_status"]
        )


if __name__ == "__main__":
    unittest.main()
