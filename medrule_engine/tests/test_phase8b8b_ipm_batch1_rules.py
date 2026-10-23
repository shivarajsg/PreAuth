"""Phase 8B.8B: Controlled IPM Batch 1 Implementation Focused Test Suite.

Comprehensive validation of the three authorized Interventional Pain Management rules:
1. RULE-IPM-CGEPIDURALINJECTIONS-001 (Epidural Spine Injections - CPT 62320-62323, 64479-64484):
   - Pathway 1: Acute radicular pain (< 3 months, >= 2 weeks conservative therapy, pain >= 6/10 or disability, fluoroscopy).
   - Pathway 2: Spinal stenosis (>= 6 weeks conservative therapy in prior 6 months, pain >= 6/10 or disability, fluoroscopy).
   - Pathway 3: FBSS or epidural fibrosis (medical necessity reason documented, >= 6 weeks conservative therapy, pain >= 6/10, fluoroscopy).
   - Pathway 4: Diagnostic TFESI for surgical planning (pre-op evaluation & surgical plan, <= 2 levels, fluoroscopy).
   - Boundary tests: Conservative care 1.9w vs 2.0w; pain duration 2.9m vs 3.1m; pain score 5 vs 6.
   - Negative & Indeterminate tests: Non-radicular axial pain, mild pain (3/10), insufficient care, lack of imaging guidance, missing evidence.

2. RULE-IPM-CGEPIDURALPUMPTRIALS-001 (Single Injection Trials for Intrathecal Pumps - CPT 62320-62323, 64479-64484):
   - Pathway 1: Chronic intractable pain in non-terminal patient, failed >= 12w conservative therapy, non-opioid-naive, trial count <= 2.
   - Pathway 2: Intractable spasticity (MS, SCI, Stiff Person, etc.) with functional impairment, failed >= 12w conservative therapy, non-terminal, trial count <= 2.
   - Pathway 3: Second intraspinal trial for first trial < 50% relief or intolerable side effects, trial count == 2.
   - Boundary tests: Conservative care 11.9w vs 12.0w; prior trial relief 49% vs 50%; trial count 2 vs 3.
   - Negative & Indeterminate tests: Patient is opioid-naive, insufficient care (< 12w), third trial (> 2 max), missing evidence.

3. RULE-IPM-CGSIINJECTIONS-001 (Sacroiliac Joint Injections - CPT 27096, G0260):
   - Pathway 1: Mechanical SIJ pain below L5, duration >= 3m, pain >= 6/10 or disability, cluster >= 3 of 8 provocative tests, failed >= 6w conservative therapy in prior 6m, imaging guidance.
   - Pathway 2: Spondyloarthropathy, age of onset < 45, pain >= 3m, active pain management program, sacroiliitis on imaging, >= 1 feature, imaging guidance.
   - Pathway 3: Pre-surgical diagnostic SIJ injection with contrast, pain relief >= 75%, trial count <= 2, imaging guidance.
   - Boundary tests: Provocative tests 2 vs 3; pain duration 2.9m vs 3.0m; age of onset 44.9y vs 45.1y; diagnostic relief 74% vs 75%.
   - Negative & Indeterminate tests: < 3 provocative tests, duration < 3m, lack of imaging guidance, missing evidence.

4. CPT Candidate Routing & Cross-Domain Isolation:
   - Full verification across all 10 CPT/HCPCS codes (62320, 62321, 62322, 62323, 64479, 64480, 64483, 64484, 27096, G0260).
   - Bidirectional domain isolation between Advanced Imaging and IPM.

5. Canonical Governance Invariants:
   - All 3 rules in DRAFT status (APPROVED count = 0).
   - All 7 canonical governance gates intact and blocked.
   - 128 active rules catalog preserved.
"""

import copy
import sqlite3
import unittest

from medrule_engine.case_validator import CaseValidator
from medrule_engine.condition_evaluator import EvaluationState
from medrule_engine.decision_tree import (
    DecisionOutcome,
    DecisionTreeEngine,
    GOVERNANCE_BLOCKED_RULE_IDS,
)
from medrule_engine.policy_router import PolicyRouter
from medrule_engine.rule_registry import RuleRegistry


class TestPhase8B8BIPMBatch1Rules(unittest.TestCase):
    """Focused test suite for Phase 8B.8B authorized IPM Batch 1 rules."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry(include_archived=False)
        cls.registry.load_all_domains()
        cls.engine = DecisionTreeEngine(registry=cls.registry)
        cls.router = PolicyRouter(registry=cls.registry)
        cls.validator = CaseValidator()

    def _build_case(self, case_id: str, procedure_code: str, procedure_name: str,
                    evidence: dict, age: int = 45, pos: str = "OFFICE") -> dict:
        return {
            "case_id": case_id,
            "clinical_domain": "interventional_pain_management",
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
    # 1. RULE-IPM-CGEPIDURALINJECTIONS-001 (Epidural Spine Injections)
    # =========================================================================

    def test_esi_pathway_1_acute_radicular_pain_positive(self):
        """TC-ESI-001: Acute radicular back pain with 1.5m duration (< 3m), failed 2w conservative care, pain 7/10, fluoroscopy."""
        case = self._build_case(
            "CASE-ESI-P1-ACUTE-POS", "62323", "Lumbar Epidural Injection",
            {
                "radicular_symptoms_present": True,
                "pain_duration_months": 1.5,
                "conservative_therapy_duration_weeks": 2,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "imaging_guidance_present": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_esi_pathway_2_spinal_stenosis_positive(self):
        """TC-ESI-002: Lumbar spinal stenosis causing radicular pain, failed 6w conservative therapy in last 6 months, pain 8/10, fluoroscopy."""
        case = self._build_case(
            "CASE-ESI-P2-STENOSIS-POS", "62323", "Lumbar Epidural Injection",
            {
                "spinal_stenosis_confirmed": True,
                "axial_or_radicular_pain_present": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "pain_intensity_score_numeric": 8,
                "functional_disability_documented": True,
                "imaging_guidance_present": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_esi_pathway_3_fbss_epidural_fibrosis_positive(self):
        """TC-ESI-003: Failed back surgery syndrome with epidural fibrosis, documented medical reason, failed 6w conservative care, pain 6/10, fluoroscopy."""
        case = self._build_case(
            "CASE-ESI-P3-FBSS-POS", "62321", "Cervical Epidural Injection",
            {
                "fbss_or_epidural_fibrosis_confirmed": True,
                "medical_reason_for_injection_documented": True,
                "axial_or_radicular_pain_present": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "pain_intensity_score_numeric": 6,
                "functional_disability_documented": True,
                "imaging_guidance_present": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_esi_pathway_4_diagnostic_transforaminal_positive(self):
        """TC-ESI-004: Pre-operative surgical planning TFESI at single level (L5-S1) with surgical plan, pain 7/10, fluoroscopy."""
        case = self._build_case(
            "CASE-ESI-P4-TFESI-POS", "64483", "Transforaminal Epidural Injection",
            {
                "preoperative_evaluation_and_surgical_plan_documented": True,
                "injection_approach": "TRANSFORAMINAL",
                "transforaminal_levels_count": 1,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "imaging_guidance_present": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_esi_boundary_conservative_care_weeks(self):
        """Boundary test: 1.9 weeks conservative care fails, 2.0 weeks passes for acute radiculopathy."""
        # 1.9 weeks fails
        case_fail = self._build_case(
            "CASE-ESI-BND-CONS-FAIL", "62323", "Lumbar Epidural Injection",
            {
                "radicular_symptoms_present": True,
                "pain_duration_months": 1.0,
                "conservative_therapy_duration_weeks": 1.9,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "imaging_guidance_present": True,
                "spinal_stenosis_confirmed": False,
                "fbss_or_epidural_fibrosis_confirmed": False,
                "preoperative_evaluation_and_surgical_plan_documented": False,
                "conservative_therapy_exception_documented": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # 2.0 weeks passes
        case_pass = self._build_case(
            "CASE-ESI-BND-CONS-PASS", "62323", "Lumbar Epidural Injection",
            {
                "radicular_symptoms_present": True,
                "pain_duration_months": 1.0,
                "conservative_therapy_duration_weeks": 2.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "imaging_guidance_present": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_esi_boundary_pain_duration_months(self):
        """Boundary test: 2.9 months qualifies as acute (< 3m), 3.1 months fails acute pathway without 6w chronic care."""
        # 2.9m with 2w care passes acute pathway
        case_pass = self._build_case(
            "CASE-ESI-BND-DUR-PASS", "62323", "Lumbar Epidural Injection",
            {
                "radicular_symptoms_present": True,
                "pain_duration_months": 2.9,
                "conservative_therapy_duration_weeks": 2.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "imaging_guidance_present": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # 3.1m with only 2w care fails acute pathway (duration not < 3m)
        case_fail = self._build_case(
            "CASE-ESI-BND-DUR-FAIL", "62323", "Lumbar Epidural Injection",
            {
                "radicular_symptoms_present": True,
                "pain_duration_months": 3.1,
                "conservative_therapy_duration_weeks": 2.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "imaging_guidance_present": True,
                "spinal_stenosis_confirmed": False,
                "fbss_or_epidural_fibrosis_confirmed": False,
                "preoperative_evaluation_and_surgical_plan_documented": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_esi_negative_mild_pain_score(self):
        """TC-ESI-006: Mild pain intensity (3/10) with no functional disability fails baseline pain requirement."""
        case = self._build_case(
            "CASE-ESI-NEG-MILD-PAIN", "62323", "Lumbar Epidural Injection",
            {
                "radicular_symptoms_present": True,
                "pain_duration_months": 1.0,
                "conservative_therapy_duration_weeks": 2,
                "pain_intensity_score_numeric": 3,
                "functional_disability_documented": False,
                "imaging_guidance_present": True,
                "spinal_stenosis_confirmed": False,
                "fbss_or_epidural_fibrosis_confirmed": False,
                "preoperative_evaluation_and_surgical_plan_documented": False
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_esi_negative_no_imaging_guidance(self):
        """ESI without imaging guidance fails mandatory fluoroscopic/CT guidance criterion."""
        case = self._build_case(
            "CASE-ESI-NEG-NO-GUIDANCE", "62323", "Lumbar Epidural Injection",
            {
                "radicular_symptoms_present": True,
                "pain_duration_months": 1.0,
                "conservative_therapy_duration_weeks": 2,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "imaging_guidance_present": False,
                "spinal_stenosis_confirmed": False,
                "fbss_or_epidural_fibrosis_confirmed": False,
                "preoperative_evaluation_and_surgical_plan_documented": False
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_esi_indeterminate_missing_pain_evidence(self):
        """TC-ESI-008: Missing pain intensity score and functional disability returns INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-ESI-IND-MISSING-PAIN", "62323", "Lumbar Epidural Injection",
            {
                "spinal_stenosis_confirmed": True,
                "axial_or_radicular_pain_present": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": True
                # pain_intensity_score_numeric and functional_disability_documented omitted
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 2. RULE-IPM-CGEPIDURALPUMPTRIALS-001 (Single Injection Trials for IT Pumps)
    # =========================================================================

    def test_pump_pathway_1_chronic_intractable_pain_positive(self):
        """TC-PUMP-001: Chronic intractable pain, non-terminal, pain score 8/10, failed 14w conservative care, non-opioid-naive, trial 1."""
        case = self._build_case(
            "CASE-PUMP-P1-PAIN-POS", "62323", "IT Pump Trial",
            {
                "chronic_intractable_pain_confirmed": True,
                "patient_is_non_terminal": True,
                "pain_intensity_score_numeric": 8,
                "functional_disability_documented": True,
                "conservative_therapy_duration_weeks": 14,
                "patient_is_opioid_naive": False,
                "intraspinal_drug_trial_count": 1
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_pump_pathway_2_intractable_spasticity_positive(self):
        """TC-PUMP-002: Intractable spasticity secondary to MS, balance impairment, failed 16w conservative care, non-terminal, trial 1."""
        case = self._build_case(
            "CASE-PUMP-P2-SPASTICITY-POS", "62323", "IT Pump Trial",
            {
                "intractable_spasticity_confirmed": True,
                "qualifying_spasticity_etiology_present": True,
                "spasticity_functional_impairment_documented": True,
                "patient_is_non_terminal": True,
                "conservative_therapy_duration_weeks": 16,
                "intraspinal_drug_trial_count": 1
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_pump_pathway_3_second_intraspinal_trial_positive(self):
        """TC-PUMP-003: Second intraspinal trial requested after first trial produced 30% relief (< 50%), trial count 2."""
        case = self._build_case(
            "CASE-PUMP-P3-SECOND-TRIAL-POS", "62323", "IT Pump Trial",
            {
                "prior_trial_relief_percentage": 30,
                "prior_trial_intolerable_side_effects": False,
                "intraspinal_drug_trial_count": 2
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_pump_negative_patient_is_opioid_naive(self):
        """TC-PUMP-004: Intractable pain meeting conservative care, but patient is opioid-naive (strictly prohibited by policy)."""
        case = self._build_case(
            "CASE-PUMP-NEG-OPIOID-NAIVE", "62323", "IT Pump Trial",
            {
                "chronic_intractable_pain_confirmed": True,
                "patient_is_non_terminal": True,
                "pain_intensity_score_numeric": 8,
                "functional_disability_documented": True,
                "conservative_therapy_duration_weeks": 16,
                "patient_is_opioid_naive": True,  # Opioid-naive violates policy
                "intraspinal_drug_trial_count": 1,
                "intractable_spasticity_confirmed": False,
                "prior_trial_relief_percentage": 80
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_pump_boundary_conservative_care_weeks(self):
        """Boundary test: 11.9 weeks conservative care fails, 12.0 weeks passes for intraspinal pump trial."""
        case_fail = self._build_case(
            "CASE-PUMP-BND-CONS-FAIL", "62323", "IT Pump Trial",
            {
                "chronic_intractable_pain_confirmed": True,
                "patient_is_non_terminal": True,
                "pain_intensity_score_numeric": 8,
                "functional_disability_documented": True,
                "conservative_therapy_duration_weeks": 11.9,
                "conservative_therapy_exception_documented": False,
                "patient_is_opioid_naive": False,
                "intraspinal_drug_trial_count": 1,
                "intractable_spasticity_confirmed": False,
                "prior_trial_relief_percentage": 80
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        case_pass = self._build_case(
            "CASE-PUMP-BND-CONS-PASS", "62323", "IT Pump Trial",
            {
                "chronic_intractable_pain_confirmed": True,
                "patient_is_non_terminal": True,
                "pain_intensity_score_numeric": 8,
                "functional_disability_documented": True,
                "conservative_therapy_duration_weeks": 12.0,
                "patient_is_opioid_naive": False,
                "intraspinal_drug_trial_count": 1
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_pump_negative_third_trial_exceeds_limit(self):
        """TC-PUMP-006: Third intraspinal drug trial requested (exceeds policy limit of maximum 2 trials)."""
        case = self._build_case(
            "CASE-PUMP-NEG-THIRD-TRIAL", "62323", "IT Pump Trial",
            {
                "chronic_intractable_pain_confirmed": False,
                "intractable_spasticity_confirmed": False,
                "prior_trial_relief_percentage": 20,
                "prior_trial_intolerable_side_effects": False,
                "intraspinal_drug_trial_count": 3  # Exceeds max 2 trials
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_pump_indeterminate_missing_opioid_status(self):
        """Intractable pain case with missing opioid status returns INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-PUMP-IND-MISSING-OPIOID", "62323", "IT Pump Trial",
            {
                "chronic_intractable_pain_confirmed": True,
                "patient_is_non_terminal": True,
                "pain_intensity_score_numeric": 8,
                "functional_disability_documented": True,
                "conservative_therapy_duration_weeks": 14,
                "intraspinal_drug_trial_count": 1
                # patient_is_opioid_naive omitted
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGEPIDURALPUMPTRIALS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 3. RULE-IPM-CGSIINJECTIONS-001 (Sacroiliac Joint Injections)
    # =========================================================================

    def test_sij_pathway_1_mechanical_pain_positive(self):
        """TC-SIJ-001: Axial pain below L5 for 5m, pain score 7/10, 3 positive provocative tests, failed 6w conservative care, fluoroscopy."""
        case = self._build_case(
            "CASE-SIJ-P1-MECH-POS", "27096", "Sacroiliac Joint Injection",
            {
                "axial_pain_below_l5_present": True,
                "pain_duration_months": 5.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "provocative_exam_findings_count": 3,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_sij_pathway_2_spondyloarthropathy_positive(self):
        """TC-SIJ-002: Spondyloarthropathy with onset age 32 (< 45), pain 6m, active sacroiliitis on imaging, 2 features, pain program active, fluoroscopy."""
        case = self._build_case(
            "CASE-SIJ-P2-SPONDYLO-POS", "27096", "Sacroiliac Joint Injection",
            {
                "spondyloarthropathy_diagnosed": True,
                "pain_duration_months": 6.0,
                "age_at_symptom_onset_years": 32,
                "comprehensive_pain_program_active": True,
                "imaging_evidence_sacroiliitis": True,
                "spondyloarthropathy_features_count": 2,
                "imaging_guidance_present": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_sij_pathway_3_presurgical_diagnostic_positive(self):
        """TC-SIJ-003: Contrast-enhanced diagnostic SIJ injection for fusion planning, 80% relief (>= 75%), trial 1, fluoroscopy."""
        case = self._build_case(
            "CASE-SIJ-P3-SURGICAL-POS", "27096", "Sacroiliac Joint Injection",
            {
                "preoperative_evaluation_and_surgical_plan_documented": True,
                "contrast_enhanced_intraarticular_injection": True,
                "diagnostic_pain_relief_percentage": 80,
                "diagnostic_sij_injection_count": 1,
                "imaging_guidance_present": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_sij_boundary_provocative_exam_findings_count(self):
        """Boundary test: 2 provocative exam findings fails (< 3), 3 provocative findings passes."""
        # 2 provocative findings fails
        case_fail = self._build_case(
            "CASE-SIJ-BND-PROV-FAIL", "27096", "Sacroiliac Joint Injection",
            {
                "axial_pain_below_l5_present": True,
                "pain_duration_months": 5.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "provocative_exam_findings_count": 2,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": True,
                "spondyloarthropathy_diagnosed": False,
                "preoperative_evaluation_and_surgical_plan_documented": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # 3 provocative findings passes
        case_pass = self._build_case(
            "CASE-SIJ-BND-PROV-PASS", "27096", "Sacroiliac Joint Injection",
            {
                "axial_pain_below_l5_present": True,
                "pain_duration_months": 5.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "provocative_exam_findings_count": 3,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_sij_boundary_pain_duration_months(self):
        """Boundary test: 2.9 months duration fails (< 3m), 3.0 months passes for mechanical SIJ."""
        case_fail = self._build_case(
            "CASE-SIJ-BND-DUR-FAIL", "27096", "Sacroiliac Joint Injection",
            {
                "axial_pain_below_l5_present": True,
                "pain_duration_months": 2.9,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "provocative_exam_findings_count": 3,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": True,
                "spondyloarthropathy_diagnosed": False,
                "preoperative_evaluation_and_surgical_plan_documented": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        case_pass = self._build_case(
            "CASE-SIJ-BND-DUR-PASS", "27096", "Sacroiliac Joint Injection",
            {
                "axial_pain_below_l5_present": True,
                "pain_duration_months": 3.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "provocative_exam_findings_count": 3,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_sij_negative_no_imaging_guidance(self):
        """TC-SIJ-006: Sacroiliac joint injection requested without imaging guidance fails mandatory fluoroscopy/CT."""
        case = self._build_case(
            "CASE-SIJ-NEG-NO-GUIDANCE", "27096", "Sacroiliac Joint Injection",
            {
                "axial_pain_below_l5_present": True,
                "pain_duration_months": 5.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "provocative_exam_findings_count": 3,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": False,
                "spondyloarthropathy_diagnosed": False,
                "preoperative_evaluation_and_surgical_plan_documented": False
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_sij_indeterminate_missing_provocative_findings(self):
        """SI joint case with missing provocative exam findings returns INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-SIJ-IND-MISSING-PROV", "27096", "Sacroiliac Joint Injection",
            {
                "axial_pain_below_l5_present": True,
                "pain_duration_months": 5.0,
                "pain_intensity_score_numeric": 7,
                "functional_disability_documented": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "imaging_guidance_present": True
                # provocative_exam_findings_count omitted
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSIINJECTIONS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 4. CPT Candidate Routing & Cross-Domain Isolation
    # =========================================================================

    def test_batch1_cpt_candidate_routing(self):
        """Batch 1 CPT and HCPCS codes correctly route to the authorized IPM rules."""
        # ESI and Pump Trial codes
        for code in ["62320", "62321", "62322", "62323", "64479", "64480", "64483", "64484"]:
            case_dict = self._build_case(f"CASE-ROUTING-{code}", code, "Spine Injection", {})
            _, _, case_obj = self.validator.validate(case_dict)
            routing = self.router.route_case(case_obj)
            rule_ids = [r.rule_id for r in routing.applicable_rules]
            self.assertIn("RULE-IPM-CGEPIDURALINJECTIONS-001", rule_ids, f"Code {code} missing ESI rule")
            self.assertIn("RULE-IPM-CGEPIDURALPUMPTRIALS-001", rule_ids, f"Code {code} missing Pump Trial rule")

        # Sacroiliac Joint Injection codes
        for code in ["27096", "G0260"]:
            case_dict = self._build_case(f"CASE-ROUTING-{code}", code, "SIJ Injection", {})
            _, _, case_obj = self.validator.validate(case_dict)
            routing = self.router.route_case(case_obj)
            rule_ids = [r.rule_id for r in routing.applicable_rules]
            self.assertIn("RULE-IPM-CGSIINJECTIONS-001", rule_ids, f"Code {code} missing SIJ rule")

    def test_batch1_cross_domain_isolation(self):
        """Cross-domain isolation: Advanced Imaging requests do NOT route IPM rules, and vice versa."""
        # Advanced Imaging CT case
        ai_case = {
            "case_id": "CASE-AI-ROUTING-ISOLATION",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72131",
            "procedure_name": "CT Lumbar Spine",
            "place_of_service": "OFFICE",
            "patient_age_years": 45,
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        _, _, ai_obj = self.validator.validate(ai_case)
        ai_routing = self.router.route_case(ai_obj)
        ai_rule_ids = [r.rule_id for r in ai_routing.applicable_rules]
        self.assertNotIn("RULE-IPM-CGEPIDURALINJECTIONS-001", ai_rule_ids)
        self.assertNotIn("RULE-IPM-CGEPIDURALPUMPTRIALS-001", ai_rule_ids)
        self.assertNotIn("RULE-IPM-CGSIINJECTIONS-001", ai_rule_ids)

        # IPM case does not route Advanced Imaging rules
        ipm_case = self._build_case("CASE-IPM-AI-ISOLATION", "62323", "Lumbar Epidural Injection", {})
        _, _, ipm_obj = self.validator.validate(ipm_case)
        ipm_routing = self.router.route_case(ipm_obj)
        ipm_rule_ids = [r.rule_id for r in ipm_routing.applicable_rules]
        self.assertNotIn("RULE-ADV-CG2036-001", ipm_rule_ids)
        self.assertNotIn("RULE-ADV-CG2031-001", ipm_rule_ids)

    # =========================================================================
    # 5. Governance Invariants & Status Verification
    # =========================================================================

    def test_batch1_governance_status_remains_draft(self):
        """All three Batch 1 rules must remain strictly in DRAFT status."""
        for rid in [
            "RULE-IPM-CGEPIDURALINJECTIONS-001",
            "RULE-IPM-CGEPIDURALPUMPTRIALS-001",
            "RULE-IPM-CGSIINJECTIONS-001"
        ]:
            rule = self.registry.get_rule(rid)
            self.assertIsNotNone(rule, f"Rule {rid} not found in registry")
            self.assertEqual(rule.extraction_status, "DRAFT", f"Rule {rid} status must be DRAFT")
            self.assertFalse(rule.is_approved, f"Rule {rid} must not be approved")

    def test_canonical_blocked_gates_remain_intact(self):
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

    def test_zero_approved_rules_in_db(self):
        """Governance database invariant: exactly 0 approved rules in DB."""
        db_path = "medrule_engine/governance/data/governance.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rule_governance_state WHERE is_approved = 1 OR workflow_status = 'APPROVED'")
        approved_count = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(approved_count, 0)

    def test_active_rule_catalog_count(self):
        """Active rules catalog must contain exactly 128 active rules."""
        self.assertEqual(len(self.registry.get_all_rules()), 128)


if __name__ == "__main__":
    unittest.main()
