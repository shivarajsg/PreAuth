"""Phase 8B.3: Controlled Tier 1 Implementation Focused Test Suite.

Comprehensive validation of the seven reviewed Advanced Imaging Tier 1 rules:
1. RULE-ADV-CG2054-001 (Sella CT / Pituitary Mass - CPT 70480)
2. RULE-ADV-CG2062-001 (Upper Extremity CT / Joint Pain - CPT 73200)
3. RULE-ADV-CG2055-001 (TMJ MRI / Internal Derangement - CPT 70336)
4. RULE-ADV-CG2032-001 (Lower Extremity CT / Non-Specific Pain - CPT 73700)
5. RULE-ADV-CG2035-001 (Lower Extremity MRI / Joint Pain - CPT 73721)
6. RULE-ADV-CG2030-001 (LDCT Lung Cancer Screening - CPT 71271)
7. RULE-ADV-CG2024-001 (QCT Bone Density Study - CPT 77078)

Mandatory Test Dimensions Covered:
- Qualifying and non-qualifying clinical cases.
- Independent verification of each alternative and exception pathway.
- Three-valued evidence handling (TRUE, FALSE, and missing/UNKNOWN -> INSUFFICIENT_INFORMATION).
- Exact numerical and temporal boundaries (BMI, age, smoking pack-years, therapy duration).
- Preservation of RULE-ADV-CG2035-002's separate orthopedic instability sign pathway.
- Strict domain isolation and candidate-rule selection without cross-domain leakage.
- Zero approved rules and governance gate preservation.
"""

import copy
import unittest

from medrule_engine.condition_evaluator import EvaluationState
from medrule_engine.decision_tree import (
    DecisionOutcome,
    DecisionTreeEngine,
    GOVERNANCE_BLOCKED_RULE_IDS,
)
from medrule_engine.rule_registry import RuleRegistry


class TestPhase8B3Tier1Rules(unittest.TestCase):
    """Focused regression test suite for Phase 8B.3 Tier 1 Advanced Imaging rules."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry(include_archived=False)
        cls.registry.load_all_domains()
        cls.engine = DecisionTreeEngine(registry=cls.registry)

    def _build_case(self, case_id: str, procedure_code: str, procedure_name: str,
                    evidence: dict, age: int = 55, pos: str = "OFFICE") -> dict:
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
    # 1. RULE-ADV-CG2054-001: Sella CT (CPT 70480)
    # =========================================================================
    def test_cg2054_001_sella_ct_qualifying(self):
        """Sella CT qualifies when known mass is present AND MRI is contraindicated."""
        case = self._build_case(
            "CASE-CG2054-PASS", "70480", "CT Sella/Pituitary",
            {
                "sellar_or_parasellar_mass": True,
                "mri_contraindicated": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2054-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2054_001_sella_ct_mri_not_contraindicated(self):
        """Sella CT fails when MRI is not contraindicated (MRI is primary gold standard)."""
        case = self._build_case(
            "CASE-CG2054-FAIL-NOMRI-CONTRA", "70480", "CT Sella/Pituitary",
            {
                "sellar_or_parasellar_mass": True,
                "mri_contraindicated": False
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2054-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2054_001_sella_ct_missing_mri_status(self):
        """Sella CT pends for documentation when MRI contraindication status is unstated."""
        case = self._build_case(
            "CASE-CG2054-PEND-MISSING-CONTRA", "70480", "CT Sella/Pituitary",
            {
                "sellar_or_parasellar_mass": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2054-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2054_001_sella_ct_no_mass(self):
        """Sella CT fails when no sellar/parasellar mass is present."""
        case = self._build_case(
            "CASE-CG2054-FAIL-NOMASS", "70480", "CT Sella/Pituitary",
            {
                "sellar_or_parasellar_mass": False,
                "mri_contraindicated": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2054-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 2. RULE-ADV-CG2062-001: Upper Extremity CT (CPT 73200)
    # =========================================================================
    def test_cg2062_001_upper_ext_ct_alternative_mri_contraindicated(self):
        """Upper Extremity CT qualifies with prior X-ray, conservative care, and MRI contraindication."""
        case = self._build_case(
            "CASE-CG2062-PASS-MRI-CONTRA", "73200", "CT Upper Extremity",
            {
                "prior_xray_negative_or_inconclusive": True,
                "conservative_therapy_or_bony_injury": True,
                "mri_contraindicated": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2062-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2062_001_upper_ext_ct_alternative_ct_arthrogram(self):
        """Upper Extremity CT qualifies when requested as a CT arthrogram even without MRI contraindication."""
        case = self._build_case(
            "CASE-CG2062-PASS-ARTHROGRAM", "73200", "CT Upper Extremity",
            {
                "prior_xray_negative_or_inconclusive": True,
                "conservative_therapy_or_bony_injury": True,
                "mri_contraindicated": False,
                "requested_as_ct_arthrogram": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2062-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2062_001_upper_ext_ct_both_alternatives_false(self):
        """Upper Extremity CT fails when MRI is NOT contraindicated AND not a CT arthrogram."""
        case = self._build_case(
            "CASE-CG2062-FAIL-NO-ALT", "73200", "CT Upper Extremity",
            {
                "prior_xray_negative_or_inconclusive": True,
                "conservative_therapy_or_bony_injury": True,
                "mri_contraindicated": False,
                "requested_as_ct_arthrogram": False
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2062-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2062_001_upper_ext_ct_missing_subconditions(self):
        """Upper Extremity CT pends when MRI contraindication and CT arthrogram status are missing."""
        case = self._build_case(
            "CASE-CG2062-PEND-MISSING-SUB", "73200", "CT Upper Extremity",
            {
                "prior_xray_negative_or_inconclusive": True,
                "conservative_therapy_or_bony_injury": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2062-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2062_001_upper_ext_ct_negative_xray_missing(self):
        """Upper Extremity CT fails when prior plain radiograph requirement is unmet."""
        case = self._build_case(
            "CASE-CG2062-FAIL-NO-XRAY", "73200", "CT Upper Extremity",
            {
                "prior_xray_negative_or_inconclusive": False,
                "conservative_therapy_or_bony_injury": True,
                "mri_contraindicated": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2062-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 3. RULE-ADV-CG2055-001: Temporomandibular Joint MRI (CPT 70336)
    # =========================================================================
    def test_cg2055_001_tmj_mri_qualifying(self):
        """TMJ MRI qualifies with suspected derangement, >= 4 weeks therapy, pharmacotherapy, AND behavioral mod."""
        case = self._build_case(
            "CASE-CG2055-PASS", "70336", "MRI TMJ",
            {
                "suspected_tmj_internal_derangement": True,
                "tmj_conservative_therapy_duration_weeks": 4,
                "tmj_pharmacotherapy_trial_completed": True,
                "tmj_behavioral_modification_completed": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2055-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2055_001_tmj_mri_temporal_boundaries(self):
        """TMJ MRI duration boundary checks: 3 weeks fails, 4 weeks passes, 8 weeks passes."""
        # 3 weeks -> CRITERIA_NOT_MET
        case_3w = self._build_case(
            "CASE-CG2055-3W", "70336", "MRI TMJ",
            {
                "suspected_tmj_internal_derangement": True,
                "tmj_conservative_therapy_duration_weeks": 3,
                "tmj_pharmacotherapy_trial_completed": True,
                "tmj_behavioral_modification_completed": True
            }
        )
        res_3w = self.engine.evaluate(case_3w, target_rule_ids=["RULE-ADV-CG2055-001"])
        self.assertEqual(res_3w.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # 4 weeks (exact threshold) -> CRITERIA_MET
        case_4w = self._build_case(
            "CASE-CG2055-4W", "70336", "MRI TMJ",
            {
                "suspected_tmj_internal_derangement": True,
                "tmj_conservative_therapy_duration_weeks": 4,
                "tmj_pharmacotherapy_trial_completed": True,
                "tmj_behavioral_modification_completed": True
            }
        )
        res_4w = self.engine.evaluate(case_4w, target_rule_ids=["RULE-ADV-CG2055-001"])
        self.assertEqual(res_4w.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # 8 weeks (above threshold) -> CRITERIA_MET
        case_8w = self._build_case(
            "CASE-CG2055-8W", "70336", "MRI TMJ",
            {
                "suspected_tmj_internal_derangement": True,
                "tmj_conservative_therapy_duration_weeks": 8,
                "tmj_pharmacotherapy_trial_completed": True,
                "tmj_behavioral_modification_completed": True
            }
        )
        res_8w = self.engine.evaluate(case_8w, target_rule_ids=["RULE-ADV-CG2055-001"])
        self.assertEqual(res_8w.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2055_001_tmj_mri_missing_either_component(self):
        """TMJ MRI requires BOTH pharmacotherapy AND behavioral modification."""
        # Missing pharmacotherapy
        case_no_rx = self._build_case(
            "CASE-CG2055-NO-RX", "70336", "MRI TMJ",
            {
                "suspected_tmj_internal_derangement": True,
                "tmj_conservative_therapy_duration_weeks": 6,
                "tmj_pharmacotherapy_trial_completed": False,
                "tmj_behavioral_modification_completed": True
            }
        )
        res_no_rx = self.engine.evaluate(case_no_rx, target_rule_ids=["RULE-ADV-CG2055-001"])
        self.assertEqual(res_no_rx.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # Missing behavioral modification
        case_no_beh = self._build_case(
            "CASE-CG2055-NO-BEH", "70336", "MRI TMJ",
            {
                "suspected_tmj_internal_derangement": True,
                "tmj_conservative_therapy_duration_weeks": 6,
                "tmj_pharmacotherapy_trial_completed": True,
                "tmj_behavioral_modification_completed": False
            }
        )
        res_no_beh = self.engine.evaluate(case_no_beh, target_rule_ids=["RULE-ADV-CG2055-001"])
        self.assertEqual(res_no_beh.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2055_001_tmj_mri_missing_evidence(self):
        """TMJ MRI pends when conservative care documentation is absent."""
        case_pend = self._build_case(
            "CASE-CG2055-PEND", "70336", "MRI TMJ",
            {
                "suspected_tmj_internal_derangement": True
            }
        )
        res_pend = self.engine.evaluate(case_pend, target_rule_ids=["RULE-ADV-CG2055-001"])
        self.assertEqual(res_pend.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 4. RULE-ADV-CG2032-001: Lower Extremity CT (CPT 73700)
    # =========================================================================
    def test_cg2032_001_lower_ext_ct_pathway_1_four_weeks_act(self):
        """Lower Extremity CT satisfies conservative therapy via >= 4 weeks ACT in adult."""
        case = self._build_case(
            "CASE-CG2032-PASS-4W", "73700", "CT Lower Extremity",
            {
                "non_specific_lower_extremity_pain": True,
                "prior_xray_completed": True,
                "mri_contraindicated": True,
                "conservative_therapy_duration_weeks": 4
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2032-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2032_001_lower_ext_ct_pathway_2_symptom_worsening(self):
        """Lower Extremity CT satisfies conservative therapy via documented progression/worsening."""
        case = self._build_case(
            "CASE-CG2032-PASS-WORSEN", "73700", "CT Lower Extremity",
            {
                "non_specific_lower_extremity_pain": True,
                "prior_xray_completed": True,
                "mri_contraindicated": True,
                "conservative_treatment_worsening": True
            },
            age=45
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2032-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2032_001_lower_ext_ct_pathway_3_pediatric(self):
        """Lower Extremity CT satisfies conservative therapy for pediatric patient < 12 years."""
        case = self._build_case(
            "CASE-CG2032-PASS-PEDS", "73700", "CT Lower Extremity",
            {
                "non_specific_lower_extremity_pain": True,
                "prior_xray_completed": True,
                "mri_contraindicated": True
            },
            age=8
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2032-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2032_001_lower_ext_ct_temporal_and_age_boundaries(self):
        """Lower Extremity CT boundary checks: age 12 with < 4w ACT fails; age 11 passes."""
        # Age 12, 2 weeks therapy, no worsening -> CRITERIA_NOT_MET
        case_age12 = self._build_case(
            "CASE-CG2032-AGE12", "73700", "CT Lower Extremity",
            {
                "non_specific_lower_extremity_pain": True,
                "prior_xray_completed": True,
                "mri_contraindicated": True,
                "conservative_therapy_duration_weeks": 2,
                "conservative_treatment_worsening": False
            },
            age=12
        )
        res_age12 = self.engine.evaluate(case_age12, target_rule_ids=["RULE-ADV-CG2032-001"])
        self.assertEqual(res_age12.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # Age 11 -> CRITERIA_MET
        case_age11 = self._build_case(
            "CASE-CG2032-AGE11", "73700", "CT Lower Extremity",
            {
                "non_specific_lower_extremity_pain": True,
                "prior_xray_completed": True,
                "mri_contraindicated": True
            },
            age=11
        )
        res_age11 = self.engine.evaluate(case_age11, target_rule_ids=["RULE-ADV-CG2032-001"])
        self.assertEqual(res_age11.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2032_001_lower_ext_ct_missing_prerequisites(self):
        """Lower Extremity CT pends when MRI contraindication or prior X-ray is missing."""
        case_pend = self._build_case(
            "CASE-CG2032-PEND", "73700", "CT Lower Extremity",
            {
                "non_specific_lower_extremity_pain": True,
                "prior_xray_completed": True,
                "conservative_therapy_duration_weeks": 6
            },
            age=45
        )
        res_pend = self.engine.evaluate(case_pend, target_rule_ids=["RULE-ADV-CG2032-001"])
        self.assertEqual(res_pend.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 5. RULE-ADV-CG2035-001: Lower Extremity MRI (CPT 73721)
    # =========================================================================
    def test_cg2035_001_lower_ext_mri_pathway_1_four_weeks_act(self):
        """Lower Extremity MRI qualifies with prior X-ray and >= 4 weeks ACT in adult."""
        case = self._build_case(
            "CASE-CG2035-PASS-4W", "73721", "MRI Knee",
            {
                "joint_specific_injury_or_pain": True,
                "prior_xray_completed": True,
                "conservative_therapy_duration_weeks": 4
            },
            age=35
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_001_lower_ext_mri_pathway_2_worsening(self):
        """Lower Extremity MRI qualifies with prior X-ray and symptom worsening during ACT."""
        case = self._build_case(
            "CASE-CG2035-PASS-WORSEN", "73721", "MRI Knee",
            {
                "joint_specific_injury_or_pain": True,
                "prior_xray_completed": True,
                "conservative_treatment_worsening": True
            },
            age=35
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_001_lower_ext_mri_pathway_3_pediatric(self):
        """Lower Extremity MRI qualifies with prior X-ray for pediatric patient < 12 years."""
        case = self._build_case(
            "CASE-CG2035-PASS-PEDS", "73721", "MRI Knee",
            {
                "joint_specific_injury_or_pain": True,
                "prior_xray_completed": True
            },
            age=9
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2035_001_lower_ext_mri_insufficient_conservative_care(self):
        """Lower Extremity MRI fails in adult when conservative care is under 4 weeks without worsening."""
        case = self._build_case(
            "CASE-CG2035-FAIL-2W", "73721", "MRI Knee",
            {
                "joint_specific_injury_or_pain": True,
                "prior_xray_completed": True,
                "conservative_therapy_duration_weeks": 2,
                "conservative_treatment_worsening": False
            },
            age=35
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2035_001_lower_ext_mri_missing_xray(self):
        """Lower Extremity MRI pends when prior plain radiograph documentation is absent."""
        case = self._build_case(
            "CASE-CG2035-PEND-XRAY", "73721", "MRI Knee",
            {
                "joint_specific_injury_or_pain": True,
                "conservative_therapy_duration_weeks": 6
            },
            age=35
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2035-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 6. Preservation of RULE-ADV-CG2035-002: Orthopedic Sign Exception Pathway
    # =========================================================================
    def test_cg2035_002_preservation_positive_orthopedic_sign_pathway(self):
        """Demonstrate that positive orthopedic sign in CG2035-002 waives conservative care.

        When a positive orthopedic sign (Lachman, McMurray, drawer, pivot shift) is present,
        CG2035-002 evaluates to CRITERIA_MET without conservative therapy, while CG2035-001
        independently requires conservative therapy or exceptions.
        """
        case_ortho = self._build_case(
            "CASE-CG2035-ORTHO-SIGN", "73721", "MRI Knee",
            {
                "positive_knee_orthopedic_sign": True,
                "prior_xray_completed": True
                # Note: No conservative therapy documented
            },
            age=28
        )
        # Evaluate CG2035-002: Should be MET
        res_002 = self.engine.evaluate(case_ortho, target_rule_ids=["RULE-ADV-CG2035-002"])
        self.assertEqual(res_002.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res_002.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

        # Evaluate CG2035-001 on the same case: Should NOT be MET (conservative care missing)
        res_001 = self.engine.evaluate(case_ortho, target_rule_ids=["RULE-ADV-CG2035-001"])
        self.assertNotEqual(res_001.overall_outcome, DecisionOutcome.CRITERIA_MET)

    # =========================================================================
    # 7. RULE-ADV-CG2030-001: LDCT Lung Cancer Screening (CPT 71271)
    # =========================================================================
    def test_cg2030_001_ldct_screening_qualifying(self):
        """LDCT screening qualifies when asymptomatic, age 50-80, >= 20 pk-yr, and current/recent."""
        case = self._build_case(
            "CASE-CG2030-PASS", "71271", "Low Dose CT Lung Screening",
            {
                "patient_is_asymptomatic": True,
                "smoking_history_pack_years": 25,
                "current_or_recent_smoker_15yr": True
            },
            age=65
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2030_001_ldct_screening_symptomatic_fails(self):
        """LDCT screening strictly fails when patient is symptomatic (requires diagnostic chest CT)."""
        case = self._build_case(
            "CASE-CG2030-FAIL-SYMPTOMATIC", "71271", "Low Dose CT Lung Screening",
            {
                "patient_is_asymptomatic": False,
                "smoking_history_pack_years": 30,
                "current_or_recent_smoker_15yr": True
            },
            age=65
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_cg2030_001_ldct_screening_missing_asymptomatic_pends(self):
        """LDCT screening pends when asymptomatic status is missing or ambiguous."""
        case = self._build_case(
            "CASE-CG2030-PEND-SYMPTOM-STATUS", "71271", "Low Dose CT Lung Screening",
            {
                "smoking_history_pack_years": 30,
                "current_or_recent_smoker_15yr": True
            },
            age=65
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_cg2030_001_ldct_screening_age_and_packyear_boundaries(self):
        """LDCT screening boundaries: age 49 fail, age 50 pass, age 80 pass, age 81 fail, 19 pk-yr fail."""
        evidence = {
            "patient_is_asymptomatic": True,
            "smoking_history_pack_years": 20,
            "current_or_recent_smoker_15yr": True
        }
        # Age 49 -> NOT_MET
        res_49 = self.engine.evaluate(self._build_case("CASE-AGE-49", "71271", "LDCT", evidence, age=49),
                                      target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res_49.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # Age 50 -> MET
        res_50 = self.engine.evaluate(self._build_case("CASE-AGE-50", "71271", "LDCT", evidence, age=50),
                                      target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res_50.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # Age 80 -> MET
        res_80 = self.engine.evaluate(self._build_case("CASE-AGE-80", "71271", "LDCT", evidence, age=80),
                                      target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res_80.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # Age 81 -> NOT_MET
        res_81 = self.engine.evaluate(self._build_case("CASE-AGE-81", "71271", "LDCT", evidence, age=81),
                                      target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res_81.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # Pack-years 19 -> NOT_MET
        ev_19 = copy.deepcopy(evidence)
        ev_19["smoking_history_pack_years"] = 19
        res_19 = self.engine.evaluate(self._build_case("CASE-PACK-19", "71271", "LDCT", ev_19, age=60),
                                      target_rule_ids=["RULE-ADV-CG2030-001"])
        self.assertEqual(res_19.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 8. RULE-ADV-CG2024-001: Quantitative CT Bone Density (CPT 77078)
    # =========================================================================
    def test_cg2024_001_qct_alternative_1_dxa_unavailable(self):
        """QCT qualifies via Alternative 1: DXA is insufficient or unavailable."""
        case = self._build_case(
            "CASE-CG2024-ALT1-DXA", "77078", "CT Bone Density Study",
            {
                "suspected_low_bone_mineral_density": True,
                "dxa_insufficient_or_unavailable": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2024-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2024_001_qct_alternative_2_spine_degenerative_changes(self):
        """QCT qualifies via Alternative 2: Advanced spinal degenerative changes."""
        case = self._build_case(
            "CASE-CG2024-ALT2-SPINE", "77078", "CT Bone Density Study",
            {
                "suspected_low_bone_mineral_density": True,
                "advanced_spine_degenerative_changes": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-ADV-CG2024-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2024_001_qct_alternative_3_bmi_strict_boundaries(self):
        """QCT Alternative 3 boundary checks: BMI 34.9 fail, BMI 35.0 fail, BMI 35.1 pass, BMI 40.0 pass.

        Strict requirement: BMI strictly greater than 35 kg/m2 ('> 35.0', NOT '>= 35.0').
        """
        # BMI 34.9 -> NOT_MET
        case_34_9 = self._build_case(
            "CASE-CG2024-BMI-34-9", "77078", "CT Bone Density Study",
            {
                "suspected_low_bone_mineral_density": True,
                "patient_bmi": 34.9,
                "dxa_insufficient_or_unavailable": False,
                "advanced_spine_degenerative_changes": False
            }
        )
        res_34_9 = self.engine.evaluate(case_34_9, target_rule_ids=["RULE-ADV-CG2024-001"])
        self.assertEqual(res_34_9.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(res_34_9.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # BMI 35.0 (exact threshold) -> NOT_MET (must be strictly > 35)
        case_35_0 = self._build_case(
            "CASE-CG2024-BMI-35-0", "77078", "CT Bone Density Study",
            {
                "suspected_low_bone_mineral_density": True,
                "patient_bmi": 35.0,
                "dxa_insufficient_or_unavailable": False,
                "advanced_spine_degenerative_changes": False
            }
        )
        res_35_0 = self.engine.evaluate(case_35_0, target_rule_ids=["RULE-ADV-CG2024-001"])
        self.assertEqual(res_35_0.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(res_35_0.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # BMI 35.1 (immediately above) -> MET
        case_35_1 = self._build_case(
            "CASE-CG2024-BMI-35-1", "77078", "CT Bone Density Study",
            {
                "suspected_low_bone_mineral_density": True,
                "patient_bmi": 35.1
            }
        )
        res_35_1 = self.engine.evaluate(case_35_1, target_rule_ids=["RULE-ADV-CG2024-001"])
        self.assertEqual(res_35_1.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res_35_1.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

        # BMI 40.0 (severe obesity) -> MET
        case_40_0 = self._build_case(
            "CASE-CG2024-BMI-40-0", "77078", "CT Bone Density Study",
            {
                "suspected_low_bone_mineral_density": True,
                "patient_bmi": 40.0
            }
        )
        res_40_0 = self.engine.evaluate(case_40_0, target_rule_ids=["RULE-ADV-CG2024-001"])
        self.assertEqual(res_40_0.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res_40_0.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_cg2024_001_qct_missing_general_prerequisites(self):
        """QCT pends when low BMD is suspected but none of the 3 general prerequisites are stated."""
        case_pend = self._build_case(
            "CASE-CG2024-PEND", "77078", "CT Bone Density Study",
            {
                "suspected_low_bone_mineral_density": True
            }
        )
        res_pend = self.engine.evaluate(case_pend, target_rule_ids=["RULE-ADV-CG2024-001"])
        self.assertEqual(res_pend.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)
        self.assertEqual(res_pend.clinical_necessity_rules[0].outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 9. Candidate Rule Selection & Domain Isolation
    # =========================================================================
    def test_candidate_rule_selection_and_no_cross_domain_leakage(self):
        """Verify exact candidate rule selection for each procedure code and zero IPM leakage."""
        mappings = [
            ("70480", "RULE-ADV-CG2054-001"),
            ("73200", "RULE-ADV-CG2062-001"),
            ("70336", "RULE-ADV-CG2055-001"),
            ("73700", "RULE-ADV-CG2032-001"),
            ("73721", "RULE-ADV-CG2035-001"),
            ("71271", "RULE-ADV-CG2030-001"),
            ("77078", "RULE-ADV-CG2024-001")
        ]
        for cpt, expected_rule in mappings:
            case = self._build_case(f"CASE-ROUTING-{cpt}", cpt, "Test Procedure", {})
            assessment = self.engine.evaluate(case)
            applicable_rules = [r.rule_id for r in assessment.clinical_necessity_rules] + [r.rule_id for r in assessment.place_of_service_rules]

            # Expected target rule must be in applicable rules
            self.assertIn(expected_rule, applicable_rules,
                          f"Expected rule {expected_rule} missing from routing for CPT {cpt}")

            # Zero IPM rules must leak into Advanced Imaging routing
            ipm_leaks = [r for r in applicable_rules if r.startswith("RULE-IPM-")]
            self.assertEqual(len(ipm_leaks), 0,
                             f"IPM rules leaked into Advanced Imaging CPT {cpt}: {ipm_leaks}")

    # =========================================================================
    # 10. Governance Gate & Zero Approved Rules Invariant
    # =========================================================================
    def test_governance_invariants_preserved(self):
        """Verify that zero rules are approved and all 7 governance gates remain blocked."""
        approved_rules = [r for r in self.registry.all_rules if r.extraction_status == "APPROVED"]
        self.assertEqual(len(approved_rules), 0, "Zero rules approved invariant violated!")

        blocked_rules = [r for r in self.registry.all_rules if r.extraction_status == "NEEDS_HUMAN_REVIEW"]
        self.assertEqual(len(blocked_rules), 7, "Governance blocked rules count must be exactly 7.")

        blocked_ids = {r.rule_id for r in blocked_rules}
        self.assertEqual(blocked_ids, set(GOVERNANCE_BLOCKED_RULE_IDS))


if __name__ == "__main__":
    unittest.main()
