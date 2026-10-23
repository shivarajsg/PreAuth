"""Phase 8B.5: Controlled Tier 2 Implementation Focused Test Suite.

Comprehensive validation of the three reviewed Advanced Imaging Tier 2 rules:
1. RULE-ADV-CG2035-002 (Lower Extremity MRI / Knee Orthopedic Signs - CPT 73721, 73722, 73723)
2. RULE-ADV-CG2056-002 (Thoracic Spine CT / Back Pain - CPT 72128, 72129, 72130)
3. RULE-ADV-CG2057-002 (Thoracic Spine MRI / Back Pain - CPT 72146, 72147, 72157)

Mandatory Test Dimensions Covered:
- Qualifying positive orthopedic signs without requiring prior X-ray or conservative care.
- Preserved distinct acute ACL trauma pathway requiring initial negative X-ray when physical exam is limited by swelling/pain.
- Adult thoracic back pain standard of at least six (6) weeks conservative treatment within the prior six (6) months.
- All source-verified adult conservative-care exceptions (worsening, medical inability, abnormal EMG radiculopathy).
- All ten (10) source-verified pediatric thoracic-spine red flags waiving conservative care.
- Exact age boundary threshold at 17/18 years.
- Conservative-care duration boundaries below, at, and above six weeks (5 weeks, 6.0 weeks, 8 weeks).
- Mandatory thoracic MRI contraindication prerequisite for CT (CG2056-002) in both adult and pediatric cases.
- Three-valued evidence handling (TRUE, FALSE, and missing/UNKNOWN -> INSUFFICIENT_INFORMATION).
- Exact CPT candidate selection and clinical domain isolation.
- Zero approved rules invariant and canonical governance gate preservation.
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


class TestPhase8B5Tier2Rules(unittest.TestCase):
    """Focused test suite for Phase 8B.5 Tier 2 Advanced Imaging rules."""

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
    # 1. RULE-ADV-CG2035-002: Lower Extremity MRI (Knee Orthopedic Signs)
    # =========================================================================

    def test_cg2035_002_positive_orthopedic_sign_without_xray(self):
        """Positive knee orthopedic signs (e.g. Lachman, McMurray) qualify without prior X-ray."""
        case = self._build_case(
            "CASE-KNEE-POS-NO-XRAY", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": True
                # Note: prior_xray_completed is omitted (preferred, not mandatory)
            },
            age=25
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_002_positive_orthopedic_sign_with_xray(self):
        """Positive knee orthopedic sign with completed negative X-ray qualifies."""
        case = self._build_case(
            "CASE-KNEE-POS-WITH-XRAY", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": True,
                "prior_xray_completed": True
            },
            age=32
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_002_acute_acl_limited_exam_extreme_mechanism(self):
        """Acute trauma with swelling limiting exam + completed negative X-ray + extreme mechanism qualifies."""
        case = self._build_case(
            "CASE-KNEE-TRAUMA-EXTREME-MECH", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": True,
                "prior_xray_completed": True,
                "extreme_mechanism_of_injury": True
            },
            age=22
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_002_acute_acl_limited_exam_extreme_pain(self):
        """Acute trauma with swelling limiting exam + completed negative X-ray + extreme pain qualifies."""
        case = self._build_case(
            "CASE-KNEE-TRAUMA-EXTREME-PAIN", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": True,
                "prior_xray_completed": True,
                "inability_to_perform_physical_exam": True
            },
            age=28
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_002_acute_acl_limited_exam_inability_to_stand(self):
        """Acute trauma with swelling limiting exam + completed negative X-ray + inability to stand qualifies."""
        case = self._build_case(
            "CASE-KNEE-TRAUMA-INABILITY-STAND", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": True,
                "prior_xray_completed": True,
                "inability_to_bear_full_weight": True
            },
            age=35
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_002_normal_orthopedic_exam_and_no_acute_trauma(self):
        """Normal orthopedic exam and absence of acute trauma fails CG2035-002."""
        case = self._build_case(
            "CASE-KNEE-NORMAL-EXAM", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": False
            },
            age=40
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2035_002_acute_acl_without_prior_xray_fails(self):
        """Acute knee injury with unexaminable joint strictly requires prior X-ray; fails if not done."""
        case = self._build_case(
            "CASE-KNEE-TRAUMA-NO-XRAY", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": True,
                "prior_xray_completed": False,
                "extreme_mechanism_of_injury": True
            },
            age=24
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2035_002_acute_acl_with_xray_but_no_qualifying_condition_fails(self):
        """Acute trauma with exam limited by swelling and X-ray done, but no extreme mechanism/pain/inability to stand."""
        case = self._build_case(
            "CASE-KNEE-TRAUMA-NO-SUBQUALIFIER", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": True,
                "prior_xray_completed": True,
                "extreme_mechanism_of_injury": False,
                "inability_to_perform_physical_exam": False,
                "inability_to_bear_full_weight": False
            },
            age=30
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2035_002_missing_all_evidence_pends(self):
        """Omission of orthopedic exam and trauma evidence yields INSUFFICIENT_INFORMATION."""
        case = self._build_case("CASE-KNEE-MISSING", "73721", "MRI Knee", {}, age=30)
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2035_002_acute_acl_missing_xray_pends(self):
        """Acute injury with exam limited by swelling but unrecorded X-ray status pends for documentation."""
        case = self._build_case(
            "CASE-KNEE-TRAUMA-XRAY-UNRECORDED", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": True,
                "extreme_mechanism_of_injury": True
                # prior_xray_completed is missing
            },
            age=21
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2035_inter_rule_harmonization(self):
        """Harmonization check: normal exam routes to CG2035-001 where 4w conservative care and X-ray are required."""
        case_conservative = self._build_case(
            "CASE-KNEE-CONSERVATIVE", "73721", "MRI Knee",
            {
                "joint_specific_injury_or_pain": True,
                "prior_xray_completed": True,
                "conservative_therapy_duration_weeks": 4,
                "positive_knee_orthopedic_sign": False,
                "acute_knee_injury_exam_limited_by_pain_swelling": False
            },
            age=45
        )
        # Evaluates to MET under CG2035-001
        res_001 = self.engine.evaluate(case_conservative, target_rule_ids=["RULE-ADV-CG2035-001"])
        self.assertEqual(res_001.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # Evaluates to NOT_MET under CG2035-002
        res_002 = self.engine.evaluate(case_conservative, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res_002.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 2. RULE-ADV-CG2056-002 (Thoracic CT) & RULE-ADV-CG2057-002 (Thoracic MRI)
    #    Adult Conservative Care Duration Boundaries and Exceptions
    # =========================================================================

    def test_thoracic_adult_duration_under_6_weeks_fails(self):
        """Adult thoracic back pain with 5 weeks of PT (below 6-week threshold) fails."""
        case = self._build_case(
            "CASE-THOR-5WKS-FAIL", "72146", "Thoracic Spine MRI",
            {
                "thoracic_conservative_therapy_weeks": 5,
                "conservative_treatment_worsening": False,
                "medical_contraindication_to_conservative_therapy": False,
                "abnormal_emg_ncs_thoracic_radiculopathy": False
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_thoracic_adult_duration_exact_6_weeks_qualifies(self):
        """Adult thoracic back pain with exactly 6.0 weeks of conservative therapy qualifies."""
        case = self._build_case(
            "CASE-THOR-6WKS-PASS", "72146", "Thoracic Spine MRI",
            {
                "thoracic_conservative_therapy_weeks": 6
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_adult_duration_over_6_weeks_qualifies(self):
        """Adult thoracic back pain with 8 weeks of conservative therapy qualifies."""
        case = self._build_case(
            "CASE-THOR-8WKS-PASS", "72146", "Thoracic Spine MRI",
            {
                "thoracic_conservative_therapy_weeks": 8
            },
            age=52
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_adult_exception_worsening_qualifies(self):
        """Adult thoracic back pain with 2 weeks PT and documented clinical worsening qualifies."""
        case = self._build_case(
            "CASE-THOR-WORSEN", "72146", "Thoracic Spine MRI",
            {
                "thoracic_conservative_therapy_weeks": 2,
                "conservative_treatment_worsening": True
            },
            age=38
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_adult_exception_medical_inability_qualifies(self):
        """Adult thoracic back pain with documented medical reason unable to participate qualifies."""
        case = self._build_case(
            "CASE-THOR-MED-INABILITY", "72146", "Thoracic Spine MRI",
            {
                "medical_contraindication_to_conservative_therapy": True
            },
            age=62
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_adult_exception_abnormal_emg_radiculopathy_qualifies(self):
        """Adult thoracic back pain with abnormal EMG/NCS indicating thoracic radiculopathy qualifies."""
        case = self._build_case(
            "CASE-THOR-EMG-RADIC", "72146", "Thoracic Spine MRI",
            {
                "abnormal_emg_ncs_thoracic_radiculopathy": True
            },
            age=48
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_adult_missing_therapy_and_exceptions_pends(self):
        """Adult thoracic back pain with unrecorded conservative therapy duration and exceptions pends."""
        case = self._build_case("CASE-THOR-ADULT-MISSING", "72146", "Thoracic Spine MRI", {}, age=45)
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 3. RULE-ADV-CG2057-002: Pediatric Red Flag Pathways (All 10 Red Flags)
    # =========================================================================

    def test_thoracic_peds_redflag_01_age_5_or_younger(self):
        """Pediatric patient age 4 (age <= 5) qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-AGE4", "72146", "Thoracic Spine MRI",
            {
                "thoracic_conservative_therapy_weeks": 0
            },
            age=4
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_02_constant_pain(self):
        """Pediatric patient (age 10) with constant thoracic pain qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-CONSTANT", "72146", "Thoracic Spine MRI",
            {
                "constant_thoracic_pain": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=10
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_03_pain_over_4_weeks(self):
        """Pediatric patient (age 12) with pain lasting > 4 weeks qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-PAIN-4WKS", "72146", "Thoracic Spine MRI",
            {
                "thoracic_pain_duration_weeks": 5,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=12
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_04_abnormal_neuro_exam(self):
        """Pediatric patient (age 14) with abnormal neurologic examination qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-ABN-NEURO", "72146", "Thoracic Spine MRI",
            {
                "abnormal_neurologic_exam": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=14
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_05_morning_stiffness_gelling(self):
        """Pediatric patient (age 15) with early morning stiffness/gelling qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-STIFFNESS", "72146", "Thoracic Spine MRI",
            {
                "morning_stiffness_or_gelling": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=15
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_06_night_pain_disrupting_sleep(self):
        """Pediatric patient (age 13) with night pain disrupting sleep qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-NIGHT-PAIN", "72146", "Thoracic Spine MRI",
            {
                "night_pain_disrupting_sleep": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=13
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_07_radicular_pain(self):
        """Pediatric patient (age 16) with radicular pain qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-RADICULAR", "72146", "Thoracic Spine MRI",
            {
                "radicular_pain_present": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=16
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_08_constitutional_fever_weightloss(self):
        """Pediatric patient (age 11) with fever, weight loss, or malaise qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-CONSTITUTIONAL", "72146", "Thoracic Spine MRI",
            {
                "constitutional_symptoms_fever_weight_loss": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=11
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_09_postural_kyphosis_scoliosis(self):
        """Pediatric patient (age 13) with postural changes (kyphosis/scoliosis) qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-POSTURE", "72146", "Thoracic Spine MRI",
            {
                "postural_changes_kyphosis_scoliosis": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=13
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_redflag_10_limp_refusal_to_walk(self):
        """Pediatric patient (age 7) with limp or refusal to walk qualifies without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-LIMP", "72146", "Thoracic Spine MRI",
            {
                "gait_abnormality_or_limp": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=7
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_peds_no_red_flags_fails(self):
        """Pediatric patient (age 14) with uncomplicated back pain and no red flags fails without conservative care."""
        case = self._build_case(
            "CASE-THOR-PEDS-NO-REDFLAGS", "72146", "Thoracic Spine MRI",
            {
                "constant_thoracic_pain": False,
                "thoracic_pain_duration_weeks": 2,
                "abnormal_neurologic_exam": False,
                "morning_stiffness_or_gelling": False,
                "night_pain_disrupting_sleep": False,
                "radicular_pain_present": False,
                "constitutional_symptoms_fever_weight_loss": False,
                "postural_changes_kyphosis_scoliosis": False,
                "gait_abnormality_or_limp": False,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=14
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_thoracic_peds_missing_red_flags_pends(self):
        """Pediatric patient (age 14) with unrecorded red flags pends for documentation."""
        case = self._build_case(
            "CASE-THOR-PEDS-UNRECORDED", "72146", "Thoracic Spine MRI",
            {
                "thoracic_pain_duration_weeks": 2,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=14
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 4. Age Boundaries: 17 vs 18 Years
    # =========================================================================

    def test_thoracic_age_17_pediatric_boundary(self):
        """Patient age 17 with pain > 4 weeks qualifies under pediatric red-flag pathway without PT."""
        case = self._build_case(
            "CASE-THOR-AGE17-BOUNDARY", "72146", "Thoracic Spine MRI",
            {
                "thoracic_pain_duration_weeks": 5,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=17
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_age_18_adult_boundary(self):
        """Patient age 18 with pain > 4 weeks and 0 weeks PT fails; adult 6-week conservative care standard enforced."""
        case = self._build_case(
            "CASE-THOR-AGE18-BOUNDARY", "72146", "Thoracic Spine MRI",
            {
                "thoracic_pain_duration_weeks": 5,
                "thoracic_conservative_therapy_weeks": 0,
                "conservative_treatment_worsening": False,
                "medical_contraindication_to_conservative_therapy": False,
                "abnormal_emg_ncs_thoracic_radiculopathy": False
            },
            age=18
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2057-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 5. RULE-ADV-CG2056-002: Thoracic CT MRI Contraindication Prerequisite
    # =========================================================================

    def test_thoracic_ct_adult_mri_contraindicated_qualifies(self):
        """Adult thoracic CT with 6 weeks PT and pacemaker (MRI contraindicated) qualifies."""
        case = self._build_case(
            "CASE-THOR-CT-PASS", "72128", "Thoracic Spine CT",
            {
                "thoracic_mri_contraindicated": True,
                "thoracic_conservative_therapy_weeks": 6
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2056-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_ct_adult_no_mri_contraindicated_fails(self):
        """Adult thoracic CT with 6 weeks PT but MRI NOT contraindicated fails (MRI is primary modality)."""
        case = self._build_case(
            "CASE-THOR-CT-NO-CONTRA", "72128", "Thoracic Spine CT",
            {
                "thoracic_mri_contraindicated": False,
                "thoracic_conservative_therapy_weeks": 6
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2056-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_thoracic_ct_missing_mri_contraindication_pends(self):
        """Thoracic CT with unrecorded MRI contraindication pends for documentation."""
        case = self._build_case(
            "CASE-THOR-CT-MISSING-CONTRA", "72128", "Thoracic Spine CT",
            {
                "thoracic_conservative_therapy_weeks": 6
            },
            age=55
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2056-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_thoracic_ct_peds_mri_contraindicated_qualifies(self):
        """Pediatric thoracic CT with constant pain + MRI contraindicated qualifies."""
        case = self._build_case(
            "CASE-THOR-CT-PEDS-PASS", "72128", "Thoracic Spine CT",
            {
                "thoracic_mri_contraindicated": True,
                "constant_thoracic_pain": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=10
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2056-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_thoracic_ct_peds_no_mri_contraindication_fails(self):
        """Pediatric thoracic CT with constant pain but MRI NOT contraindicated fails."""
        case = self._build_case(
            "CASE-THOR-CT-PEDS-FAIL", "72128", "Thoracic Spine CT",
            {
                "thoracic_mri_contraindicated": False,
                "constant_thoracic_pain": True,
                "thoracic_conservative_therapy_weeks": 0
            },
            age=10
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2056-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 6. Candidate Selection, Routing, and Domain Isolation
    # =========================================================================

    def test_cpt_routing_and_domain_isolation(self):
        """Verify CPT routing isolation: CPT 73721 routes to Knee rules, 72128 to Thoracic CT, 72146 to Thoracic MRI."""
        mappings = [
            ("73721", "RULE-ADV-CG2035-002", ["RULE-ADV-CG2056-002", "RULE-ADV-CG2057-002"]),
            ("72128", "RULE-ADV-CG2056-002", ["RULE-ADV-CG2035-002", "RULE-ADV-CG2057-002"]),
            ("72146", "RULE-ADV-CG2057-002", ["RULE-ADV-CG2035-002", "RULE-ADV-CG2056-002"]),
        ]
        for cpt, expected_rule, excluded_rules in mappings:
            case = self._build_case(f"CASE-ROUTING-{cpt}", cpt, "Test Procedure", {})
            assessment = self.engine.evaluate(case)
            applicable_rules = [r.rule_id for r in assessment.clinical_necessity_rules] + [
                r.rule_id for r in assessment.place_of_service_rules
            ]

            # Expected target rule must be in applicable rules
            self.assertIn(
                expected_rule,
                applicable_rules,
                f"Expected rule {expected_rule} missing from routing for CPT {cpt}",
            )

            # Excluded rules must not be in applicable rules
            for excluded in excluded_rules:
                self.assertNotIn(
                    excluded,
                    applicable_rules,
                    f"Rule {excluded} unexpectedly routed for CPT {cpt}",
                )

            # Zero IPM rules must leak into Advanced Imaging routing
            ipm_leaks = [r for r in applicable_rules if r.startswith("RULE-IPM-")]
            self.assertEqual(
                len(ipm_leaks),
                0,
                f"IPM rules leaked into Advanced Imaging CPT {cpt}: {ipm_leaks}",
            )

    # =========================================================================
    # 7. Governance Invariants Preservation
    # =========================================================================

    def test_governance_invariants_preserved(self):
        """Verify that zero rules are approved and canonical governance gates remain strictly blocked."""
        # 1. Check registry approved rules count
        approved_rules = [r for r in self.registry.all_rules if r.extraction_status == "APPROVED"]
        self.assertEqual(len(approved_rules), 0, f"Expected 0 approved rules in registry, found {len(approved_rules)}")

        # 2. Check governance database approved rules count
        conn = sqlite3.connect("medrule_engine/governance/data/governance.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM rule_governance_state WHERE is_approved = 1 OR workflow_status = 'APPROVED'")
        db_approved = c.fetchone()[0]
        conn.close()
        self.assertEqual(db_approved, 0, f"Expected 0 approved rules in database, found {db_approved}")

        # 3. Check that the canonical 7 blocked rules remain in GOVERNANCE_BLOCKED_RULE_IDS
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

        blocked_rules = [r for r in self.registry.all_rules if r.extraction_status == "NEEDS_HUMAN_REVIEW"]
        self.assertEqual(len(blocked_rules), 7, "Governance blocked rules count must be exactly 7.")
        blocked_ids = {r.rule_id for r in blocked_rules}
        self.assertEqual(blocked_ids, expected_blocked)


if __name__ == "__main__":
    unittest.main()
