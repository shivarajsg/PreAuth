"""Phase 8B.7: Lumbar CT Decomposed Criteria Focused Test Suite.

Comprehensive validation of RULE-ADV-CG2036-001 (Lumbar Spine CT - CPT 72131, 72132, 72133):
- Track A: Independent Acute Trauma, Delayed Union, and Fracture Fragment Positioning (No MRI Contraindication required).
- Track B: Independent Postoperative Hardware / Pseudarthrosis / Extent of Fusion (> 6 months after X-ray; MRI Contraindication explicitly waived).
- Track C: Back Pain & Focal Neurologic Deficits with Mandatory MRI Contraindication:
  - Adult Conservative Care Trial (>= 6 weeks within prior 6 months).
  - Adult Conservative Care Exceptions (worsening, medical inability, abnormal EMG radiculopathy).
  - Complete Pediatric Red-Flag Criteria (10 red flags waiving conservative care for age < 18).
  - Focal Neurological Deficits and Suspected Cauda Equina Syndrome.
- Strict Boundary Testing:
  - Postoperative interval immediately below (5.9m), exactly at (6.0m), and above (6.1m, 8m) six months.
  - Conservative care duration immediately below (5.9w) and at (6.0w, 8w) six weeks.
  - Patient age boundary at 17.9 / 18.0 years.
- Three-Valued Logic Handling (Missing, Ambiguous, Conflicting Evidence -> INSUFFICIENT_INFORMATION).
- Exact CPT Candidate Routing & Active Domain Isolation.
- Governance Invariants (Zero Approved Rules, 7 Blocked Gates, Status DRAFT).
"""

import copy
import sqlite3
import unittest

from medrule_engine.condition_evaluator import EvaluationState
from medrule_engine.decision_tree import (
    DecisionOutcome,
    DecisionTreeEngine,
    GOVERNANCE_BLOCKED_RULE_IDS,
)
from medrule_engine.rule_registry import RuleRegistry


class TestPhase8B7LumbarCTRules(unittest.TestCase):
    """Focused test suite for Phase 8B.7 decomposed RULE-ADV-CG2036-001."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry(include_archived=False)
        cls.registry.load_all_domains()
        cls.engine = DecisionTreeEngine(registry=cls.registry)

    def _build_case(self, case_id: str, procedure_code: str, procedure_name: str,
                    evidence: dict, age: int = 45, pos: str = "OFFICE") -> dict:
        return {
            "case_id": case_id,
            "clinical_domain": "advanced_imaging",
            "procedure_code": procedure_code,
            "procedure_name": procedure_name,
            "place_of_service": pos,
            "patient_age_years": age,
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": evidence
        }

    # =========================================================================
    # 1. Track A: Acute Trauma, Fracture Fragment, & Delayed Union (No MRI Contra)
    # =========================================================================

    def test_cg2036_001_acute_trauma_with_preliminary_imaging_positive(self):
        """Acute lumbar trauma with preliminary imaging qualifies without MRI contraindication."""
        case = self._build_case(
            "CASE-LUMBAR-TRAUMA-POS", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": True
                # Note: lumbar_mri_contraindicated is omitted (not required for acute trauma)
            },
            age=34
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_delayed_union_compression_fracture_positive(self):
        """Assessment of compression fracture delayed union qualifies without MRI contraindication."""
        case = self._build_case(
            "CASE-LUMBAR-DELAYED-UNION-POS", "72131", "CT Lumbar Spine",
            {
                "delayed_union_or_nonunion_fracture": True
            },
            age=68
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_fracture_fragment_position_positive(self):
        """Determination of fracture fragment positioning qualifies without MRI contraindication."""
        case = self._build_case(
            "CASE-LUMBAR-FRAGMENT-POS", "72131", "CT Lumbar Spine",
            {
                "fracture_fragment_position_evaluation": True
            },
            age=42
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    # =========================================================================
    # 2. Track B: Postoperative Hardware / Fusion / Pseudarthrosis
    # =========================================================================

    def test_cg2036_001_postop_hardware_greater_than_6_months_positive(self):
        """Postoperative hardware evaluation > 6 months after initial X-ray qualifies (MRI contra waived)."""
        case = self._build_case(
            "CASE-LUMBAR-POSTOP-POS", "72131", "CT Lumbar Spine",
            {
                "postoperative_fusion_hardware_or_pseudarthrosis": True,
                "prior_lumbar_xray_completed": True,
                "postoperative_interval_months": 8.0,
                # MRI contraindication explicitly false to verify exception waiver
                "lumbar_mri_contraindicated": False
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_postop_hardware_boolean_flag_positive(self):
        """Postoperative hardware evaluation with boolean interval flag qualifies."""
        case = self._build_case(
            "CASE-LUMBAR-POSTOP-BOOL-POS", "72131", "CT Lumbar Spine",
            {
                "postoperative_fusion_hardware_or_pseudarthrosis": True,
                "prior_lumbar_xray_completed": True,
                "postoperative_interval_greater_than_6_months": True
            },
            age=58
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_postop_hardware_boundary_immediately_below_6_months_negative(self):
        """Postoperative hardware evaluation at 5.9 months fails (> 6 months required)."""
        case = self._build_case(
            "CASE-LUMBAR-POSTOP-5-9M-NEG", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": True,
                "prior_lumbar_xray_completed": True,
                "postoperative_interval_months": 5.9,
                "postoperative_interval_greater_than_6_months": False,
                "lumbar_mri_contraindicated": False
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2036_001_postop_hardware_boundary_exactly_at_6_months_negative(self):
        """Postoperative hardware evaluation at exactly 6.0 months fails (> 6 months required)."""
        case = self._build_case(
            "CASE-LUMBAR-POSTOP-6-0M-NEG", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": True,
                "prior_lumbar_xray_completed": True,
                "postoperative_interval_months": 6.0,
                "postoperative_interval_greater_than_6_months": False,
                "lumbar_mri_contraindicated": False
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2036_001_postop_hardware_boundary_immediately_above_6_months_positive(self):
        """Postoperative hardware evaluation at 6.1 months qualifies (> 6 months satisfied)."""
        case = self._build_case(
            "CASE-LUMBAR-POSTOP-6-1M-POS", "72131", "CT Lumbar Spine",
            {
                "postoperative_fusion_hardware_or_pseudarthrosis": True,
                "prior_lumbar_xray_completed": True,
                "postoperative_interval_months": 6.1
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_postop_hardware_missing_xray_negative(self):
        """Postoperative hardware evaluation without preliminary plain X-rays fails."""
        case = self._build_case(
            "CASE-LUMBAR-POSTOP-NO-XRAY-NEG", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": True,
                "prior_lumbar_xray_completed": False,
                "postoperative_interval_months": 8.0,
                "lumbar_mri_contraindicated": False
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 3. Track C: Adult Back Pain Pathway (MRI Contraindicated)
    # =========================================================================

    def test_cg2036_001_adult_back_pain_6_weeks_conservative_care_positive(self):
        """Adult back pain with 6 weeks conservative care AND MRI contraindication qualifies."""
        case = self._build_case(
            "CASE-LUMBAR-PAIN-6W-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 45,
                "lumbar_conservative_therapy_weeks": 6.0
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_adult_back_pain_duration_boundary_5_9_weeks_negative(self):
        """Adult back pain with 5.9 weeks conservative therapy fails (>= 6 weeks required)."""
        case = self._build_case(
            "CASE-LUMBAR-PAIN-5-9W-NEG", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": False,
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 45,
                "lumbar_conservative_therapy_weeks": 5.9,
                "conservative_treatment_worsening": False,
                "medical_contraindication_to_conservative_therapy": False,
                "abnormal_emg_ncs_lumbar_radiculopathy": False,
                "objective_neurologic_deficit_lumbar": False,
                "suspected_cauda_equina_syndrome": False
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2036_001_adult_back_pain_mri_not_contraindicated_prevents_false_approval(self):
        """Adult back pain with 8 weeks therapy BUT MRI is NOT contraindicated correctly fails."""
        case = self._build_case(
            "CASE-LUMBAR-PAIN-NO-MRI-CONTRA-NEG", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": False,
                "lumbar_mri_contraindicated": False,
                "patient_age_years": 45,
                "lumbar_conservative_therapy_weeks": 8.0
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2036_001_adult_back_pain_exception_worsening_positive(self):
        """Adult back pain with progression/worsening during care waives 6-week duration."""
        case = self._build_case(
            "CASE-LUMBAR-PAIN-WORSENING-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 48,
                "lumbar_conservative_therapy_weeks": 2.0,
                "conservative_treatment_worsening": True
            },
            age=48
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_adult_back_pain_exception_medical_inability_positive(self):
        """Adult back pain with documented medical inability to participate in therapy qualifies."""
        case = self._build_case(
            "CASE-LUMBAR-PAIN-MED-INABILITY-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 72,
                "medical_contraindication_to_conservative_therapy": True
            },
            age=72
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_adult_back_pain_exception_abnormal_emg_radiculopathy_positive(self):
        """Adult back pain with abnormal EMG/NCS showing lumbar radiculopathy waives 6 weeks therapy."""
        case = self._build_case(
            "CASE-LUMBAR-PAIN-EMG-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 40,
                "abnormal_emg_ncs_lumbar_radiculopathy": True
            },
            age=40
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    # =========================================================================
    # 4. Track C: Objective Neurologic Deficits & Cauda Equina Syndrome
    # =========================================================================

    def test_cg2036_001_focal_neurologic_deficit_positive(self):
        """Objective focal neurologic deficit (e.g. foot drop) with MRI contraindicated qualifies."""
        case = self._build_case(
            "CASE-LUMBAR-NEURO-DEFICIT-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "objective_neurologic_deficit_lumbar": True
            },
            age=50
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_cauda_equina_syndrome_positive(self):
        """Clinical suspicion of cauda equina syndrome with MRI contraindicated qualifies."""
        case = self._build_case(
            "CASE-LUMBAR-CAUDA-EQUINA-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "suspected_cauda_equina_syndrome": True
            },
            age=39
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    # =========================================================================
    # 5. Track C: Pediatric Red Flags (< 18 yr) & Age Boundaries
    # =========================================================================

    def test_cg2036_001_pediatric_red_flag_age_under_5_positive(self):
        """Pediatric patient age <= 5 with MRI contraindicated qualifies without conservative care."""
        case = self._build_case(
            "CASE-LUMBAR-PEDS-AGE4-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 4
            },
            age=4
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_pediatric_all_red_flags_qualify(self):
        """Verify each of the remaining 9 pediatric red flags waives conservative care."""
        red_flags = [
            ("constant_lumbar_pain", True),
            ("lumbar_pain_duration_weeks", 5.0),
            ("abnormal_neurologic_exam", True),
            ("morning_stiffness_or_gelling", True),
            ("night_pain_disrupting_sleep", True),
            ("radicular_pain_present", True),
            ("constitutional_symptoms_fever_weight_loss", True),
            ("postural_changes_kyphosis_scoliosis", True),
            ("gait_abnormality_or_limp", True),
        ]
        for param, val in red_flags:
            with self.subTest(red_flag=param):
                case = self._build_case(
                    f"CASE-LUMBAR-PEDS-{param.upper()}", "72131", "CT Lumbar Spine",
                    {
                        "lumbar_mri_contraindicated": True,
                        "patient_age_years": 12,
                        param: val
                    },
                    age=12
                )
                res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
                self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_age_boundary_at_17_9_years_positive(self):
        """Patient age 17.9 with constant pain qualifies via pediatric red-flag branch."""
        case = self._build_case(
            "CASE-LUMBAR-AGE-17-9-POS", "72131", "CT Lumbar Spine",
            {
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 17.9,
                "constant_lumbar_pain": True
            },
            age=17.9
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2036_001_age_boundary_at_18_0_years_evaluates_adult_branch_negative(self):
        """Patient age 18.0 with constant pain and 2 weeks therapy evaluates adult branch and fails."""
        case = self._build_case(
            "CASE-LUMBAR-AGE-18-0-NEG", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": False,
                "lumbar_mri_contraindicated": True,
                "patient_age_years": 18.0,
                "constant_lumbar_pain": True,
                "lumbar_conservative_therapy_weeks": 2.0,
                "conservative_treatment_worsening": False,
                "medical_contraindication_to_conservative_therapy": False,
                "abnormal_emg_ncs_lumbar_radiculopathy": False,
                "objective_neurologic_deficit_lumbar": False,
                "suspected_cauda_equina_syndrome": False
            },
            age=18.0
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 6. Missing, Ambiguous, and Conflicting Evidence (Three-Valued Logic)
    # =========================================================================

    def test_cg2036_001_completely_empty_evidence_yields_insufficient_information(self):
        """Completely empty clinical evidence yields INSUFFICIENT_INFORMATION."""
        case = self._build_case("CASE-LUMBAR-EMPTY", "72131", "CT Lumbar Spine", {})
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2036_001_missing_mri_contraindication_yields_insufficient_information(self):
        """Adult back pain with 8 weeks therapy but omitted MRI contraindication yields INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-LUMBAR-MISSING-MRI-CONTRA", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": False,
                "patient_age_years": 45,
                "lumbar_conservative_therapy_weeks": 8.0
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2036_001_missing_postop_interval_yields_insufficient_information(self):
        """Hardware evaluation with X-ray completed but missing interval yields INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-LUMBAR-MISSING-INTERVAL", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": True,
                "prior_lumbar_xray_completed": True,
                "lumbar_mri_contraindicated": False
            },
            age=60
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2036_001_conflicting_evidence_yields_insufficient_information(self):
        """Explicit conflicting documentation for MRI contraindication yields INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-LUMBAR-CONFLICTING-MRI", "72131", "CT Lumbar Spine",
            {
                "acute_lumbar_trauma_with_preliminary_imaging": False,
                "delayed_union_or_nonunion_fracture": False,
                "fracture_fragment_position_evaluation": False,
                "postoperative_fusion_hardware_or_pseudarthrosis": False,
                "lumbar_mri_contraindicated": {
                    "status": "CONFLICTING",
                    "details": "Cardiologist notes non-conditional pacemaker; surgical note states MRI conditional"
                },
                "patient_age_years": 50,
                "lumbar_conservative_therapy_weeks": 8.0
            },
            age=50
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2036-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 7. CPT Candidate Routing & Domain Isolation
    # =========================================================================

    def test_cg2036_001_cpt_72131_candidate_routing(self):
        """CPT 72131 routes deterministically to RULE-ADV-CG2036-001."""
        case = self._build_case(
            "CASE-LUMBAR-ROUTING-72131", "72131", "CT Lumbar Spine",
            {"acute_lumbar_trauma_with_preliminary_imaging": True}
        )
        assessment = self.engine.evaluate(case)
        applicable_rules = [r.rule_id for r in assessment.clinical_necessity_rules]
        self.assertIn("RULE-ADV-CG2036-001", applicable_rules)
        self.assertIn("RULE-ADV-PREAMBLE-001", applicable_rules)

    def test_cg2036_001_domain_isolation_cross_domain_rejection(self):
        """Interventional pain management procedure code 62322 does NOT route to RULE-ADV-CG2036-001."""
        case = {
            "case_id": "CASE-IPM-ROUTING-ISOLATION",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62322",
            "procedure_name": "Lumbar Epidural Injection",
            "place_of_service": "AMBULATORY_SURGICAL_CENTER",
            "patient_age_years": 45,
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        assessment = self.engine.evaluate(case)
        applicable_rules = [r.rule_id for r in assessment.clinical_necessity_rules]
        self.assertNotIn("RULE-ADV-CG2036-001", applicable_rules)

    # =========================================================================
    # 8. Governance Invariants & Status Verification
    # =========================================================================

    def test_cg2036_001_governance_status_remains_draft(self):
        """RULE-ADV-CG2036-001 extraction status must remain strictly DRAFT."""
        rule = self.registry.get_rule("RULE-ADV-CG2036-001")
        self.assertIsNotNone(rule)
        self.assertEqual(rule.extraction_status, "DRAFT")
        self.assertFalse(rule.is_approved)

    def test_cg2036_001_canonical_blocked_gates_remain_blocked(self):
        """All 7 canonical governance gates must remain strictly blocked."""
        expected_blocked = {
            "RULE-ADV-PREAMBLE-001",
            "RULE-ADV-CG2000-003",
            "RULE-ADV-CG2001-001",
            "RULE-ADV-CG2066-001",
            "RULE-ADV-CG2066-002",
            "RULE-IPM-PREAMBLEIPM-001",
            "RULE-IPM-CGINFUSIONPUMPS-001",
        }
        self.assertEqual(GOVERNANCE_BLOCKED_RULE_IDS, expected_blocked)

    def test_cg2036_001_zero_approved_rules_in_db(self):
        """Governance database invariant: exactly 0 approved rules in DB."""
        db_path = "medrule_engine/governance/data/governance.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rule_governance_state WHERE is_approved = 1 OR workflow_status = 'APPROVED'")
        approved_count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(approved_count, 0)


if __name__ == "__main__":
    unittest.main()
