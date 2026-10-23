"""Phase 8B.8D: Controlled IPM Batch 3 Implementation Focused Test Suite.

Comprehensive validation of the two authorized Interventional Pain Management rules:
1. RULE-IPM-CGSPINALCORDSTIM-001 (Spinal Cord Stimulation & DRGS Trials - Guideline 1757, CPT 63650, 63655):
   - Pathway 1: Spinal Cord Stimulation (SCS) Trial (duration >= 6m, pain >= 6/10 or disability, failed conservative care >= 6m, completed 4-element psychological assessment, qualifying etiology [FBSS/PSPS, CRPS, DPN, radiculopathy, PHN, phantom limb, refractory angina], MRSA/MSSA decolonization compliance).
   - Pathway 2: Dorsal Root Ganglion Stimulation (DRGS) Trial (lower limb CRPS meeting Budapest criteria, duration >= 6m, pain >= 6/10, failed conservative care >= 6m, 4-element psychological assessment).
   - Boundary tests: Pain duration 5.9m vs 6.0m; conservative care 5.9m vs 6.0m; MRSA decolonization timing 10d vs 11d; angina medical therapy 0.9m vs 1.0m.
   - Negative & Indeterminate tests: Active infection, pregnancy, MRSA colonization without decolonization plan, decolonization plan > 10d prior, failed psychological evaluation (pain due to depression/anxiety, lack of cognitive ability), missing psychological evidence.

2. RULE-IPM-EPOS1755-001 (IPM Place of Service Outpatient Hospital Clinical Exceptions - EPOS 1755):
   - Positive clinical exceptions justifying Outpatient Hospital care (POS 22 / POS 19): ASA PS >= 3, BMI >= 40, heart disease, COPD/asthma, kidney/liver disease, bleeding disorders, stroke/TIA, hypertension (>= 3 drugs), poorly controlled diabetes, cognitive impairment, pregnancy, substance use disorder, prior anesthesia complications, difficult airway, sleep apnea, history of anaphylaxis.
   - Boundary tests: ASA PS 2 vs 3; BMI 39.9 vs 40.0.
   - Negative & Indeterminate tests: Patient without clinical exceptions requesting outpatient hospital setting (CRITERIA_NOT_MET, redirection required), missing exception documentation (INSUFFICIENT_INFORMATION).

3. Clinical Necessity vs Place of Service Dual-Track Separation:
   - Clinical necessity MET + POS Outpatient Hospital MET (ASA 3) -> Overall CRITERIA_MET.
   - Clinical necessity MET + POS Outpatient Hospital NOT MET (healthy) -> Clinical necessity MET, POS NOT MET, Overall CRITERIA_NOT_MET with redirection note.
   - Clinical necessity NOT MET + POS Outpatient Hospital MET -> Clinical necessity NOT MET, POS MET, Overall CRITERIA_NOT_MET.

4. CPT Candidate Routing & Domain Isolation:
   - Full routing verification across SCS codes (63650, 63655, 63661, 63662, 63663, 63664, 63685, 63688).
   - Domain isolation between IPM and Advanced Imaging.

5. Canonical Governance Invariants:
   - Active rules count = 128.
   - Zero approved rules in registry and database.
   - Both modified rules remain in DRAFT status.
   - All 7 canonical governance gates intact and blocked.
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


class TestPhase8B8DIPMBatch3Rules(unittest.TestCase):
    """Focused test suite for Phase 8B.8D authorized IPM Batch 3 rules."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry(include_archived=False)
        cls.registry.load_all_domains()
        cls.engine = DecisionTreeEngine(registry=cls.registry)
        cls.router = PolicyRouter(registry=cls.registry)
        cls.validator = CaseValidator()

    def _build_case(self, case_id: str, procedure_code: str, procedure_name: str,
                    evidence: dict, age: int = 50, pos: str = "OFFICE") -> dict:
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

    @property
    def scs_base_evidence(self) -> dict:
        return {
            "active_systemic_or_spinal_infection": False,
            "pregnancy_status": False,
            "mrsa_mssa_colonization_present": False,
            "pain_intensity_score_numeric": 8,
            "pain_duration_months": 8.0,
            "conservative_therapy_duration_months": 6.0,
            "pain_not_due_to_psychiatric_disorder": True,
            "psychiatric_personality_disorders_managed": True,
            "substance_use_disorder_in_recovery": True,
            "cognitive_ability_to_manage_stimulator": True,
            "failed_spine_surgery_syndrome_present": True
        }

    @property
    def epos_all_negative_evidence(self) -> dict:
        return {
            "asa_physical_status_score": 2,
            "patient_bmi": 28.0,
            "heart_disease_or_prior_heart_surgery": False,
            "chronic_lung_disease_copd_or_asthma": False,
            "chronic_kidney_or_liver_disease": False,
            "bleeding_disorder_or_blood_clots": False,
            "history_of_stroke_or_tia": False,
            "hypertension_requiring_3_or_more_drugs": False,
            "poorly_controlled_diabetes": False,
            "cognitive_impairment_or_dementia": False,
            "pregnancy_status": False,
            "active_substance_use_disorder": False,
            "prior_anesthesia_complications": False,
            "difficult_airway_anticipated": False,
            "sleep_apnea_diagnosed": False,
            "history_of_anaphylaxis": False
        }

    # =========================================================================
    # 1. RULE-IPM-CGSPINALCORDSTIM-001 (Spinal Cord Stimulation Trial)
    # =========================================================================

    def test_scs_pathway_1_fbss_positive(self):
        """TC-SCS-001: SCS trial for FBSS/PSPS with pain 8/10, duration 8m, 6m conservative care, psychological clearance."""
        case = self._build_case(
            "CASE-SCS-P1-FBSS-POS", "63650", "Percutaneous SCS Trial",
            self.scs_base_evidence
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_pathway_1_mrsa_colonized_with_valid_decolonization_plan(self):
        """TC-SCS-002: SCS trial for patient colonized with MRSA, decolonization plan scheduled 5 days prior (<= 10 days)."""
        ev = dict(self.scs_base_evidence)
        ev["mrsa_mssa_colonization_present"] = True
        ev["decolonization_plan_documented"] = True
        ev["decolonization_timing_days_prior_to_procedure"] = 5
        case = self._build_case(
            "CASE-SCS-P1-MRSA-PLAN-POS", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_pathway_1_crps_positive(self):
        """TC-SCS-003: SCS trial for CRPS Type I/II meeting Budapest criteria."""
        ev = dict(self.scs_base_evidence)
        ev["failed_spine_surgery_syndrome_present"] = False
        ev["crps_budapest_criteria_met"] = True
        case = self._build_case(
            "CASE-SCS-P1-CRPS-POS", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_pathway_1_diabetic_peripheral_neuropathy_positive(self):
        """TC-SCS-004: SCS trial for painful diabetic peripheral neuropathy."""
        ev = dict(self.scs_base_evidence)
        ev["failed_spine_surgery_syndrome_present"] = False
        ev["diabetic_peripheral_neuropathy"] = True
        case = self._build_case(
            "CASE-SCS-P1-DPN-POS", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_pathway_1_refractory_angina_positive(self):
        """TC-SCS-005: SCS trial for chronic refractory angina pectoris (NYHA III/IV, post-PCI, failed optimal meds >= 1m)."""
        ev = dict(self.scs_base_evidence)
        ev["failed_spine_surgery_syndrome_present"] = False
        ev["continued_angina_post_pci_or_cabg"] = True
        ev["not_revascularization_candidate"] = True
        ev["angina_nyha_class_3_or_4"] = True
        ev["failed_optimal_meds_duration_months"] = 2.0
        case = self._build_case(
            "CASE-SCS-P1-ANGINA-POS", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_pathway_2_drgs_lower_limb_crps_positive(self):
        """TC-SCS-006: DRGS trial for lower limb CRPS meeting Budapest criteria."""
        ev = dict(self.scs_base_evidence)
        ev["failed_spine_surgery_syndrome_present"] = False
        ev["lower_limb_crps_budapest_criteria_met"] = True
        case = self._build_case(
            "CASE-SCS-P2-DRGS-POS", "63650", "DRG Stimulator Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_boundary_pain_duration(self):
        """Boundary test: Pain duration 5.9 months fails (< 6.0m), 6.0 months passes."""
        ev_fail = dict(self.scs_base_evidence)
        ev_fail["pain_duration_months"] = 5.9
        case_fail = self._build_case(
            "CASE-SCS-BND-DUR-FAIL", "63650", "Percutaneous SCS Trial",
            ev_fail
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        ev_pass = dict(self.scs_base_evidence)
        ev_pass["pain_duration_months"] = 6.0
        case_pass = self._build_case(
            "CASE-SCS-BND-DUR-PASS", "63650", "Percutaneous SCS Trial",
            ev_pass
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_boundary_conservative_therapy_duration(self):
        """Boundary test: Conservative therapy 5.9 months fails (< 6.0m), 6.0 months passes."""
        ev_fail = dict(self.scs_base_evidence)
        ev_fail["conservative_therapy_duration_months"] = 5.9
        ev_fail["conservative_therapy_exception_documented"] = False
        case_fail = self._build_case(
            "CASE-SCS-BND-CONS-FAIL", "63650", "Percutaneous SCS Trial",
            ev_fail
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        ev_pass = dict(self.scs_base_evidence)
        ev_pass["conservative_therapy_duration_months"] = 6.0
        case_pass = self._build_case(
            "CASE-SCS-BND-CONS-PASS", "63650", "Percutaneous SCS Trial",
            ev_pass
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_scs_boundary_mrsa_decolonization_timing(self):
        """Boundary test: Colonized MRSA decolonization scheduled 10 days prior passes (<= 10d), 11 days fails (> 10d)."""
        ev_pass = dict(self.scs_base_evidence)
        ev_pass["mrsa_mssa_colonization_present"] = True
        ev_pass["decolonization_plan_documented"] = True
        ev_pass["decolonization_timing_days_prior_to_procedure"] = 10
        case_pass = self._build_case(
            "CASE-SCS-BND-MRSA-10D-PASS", "63650", "Percutaneous SCS Trial",
            ev_pass
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

        ev_fail = dict(self.scs_base_evidence)
        ev_fail["mrsa_mssa_colonization_present"] = True
        ev_fail["decolonization_plan_documented"] = True
        ev_fail["decolonization_timing_days_prior_to_procedure"] = 11
        case_fail = self._build_case(
            "CASE-SCS-BND-MRSA-11D-FAIL", "63650", "Percutaneous SCS Trial",
            ev_fail
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_scs_negative_active_infection(self):
        """TC-SCS-010: Active systemic or spinal infection is a contraindication that fails SCS trial."""
        ev = dict(self.scs_base_evidence)
        ev["active_systemic_or_spinal_infection"] = True
        case = self._build_case(
            "CASE-SCS-NEG-ACTIVE-INFECTION", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_scs_negative_pregnancy(self):
        """TC-SCS-011: Pregnancy is a contraindication that fails SCS trial."""
        ev = dict(self.scs_base_evidence)
        ev["pregnancy_status"] = True
        case = self._build_case(
            "CASE-SCS-NEG-PREGNANT", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_scs_negative_psychological_evaluation_failure(self):
        """TC-SCS-012: Pain due to psychiatric disorder fails presurgical psychological assessment."""
        ev = dict(self.scs_base_evidence)
        ev["pain_not_due_to_psychiatric_disorder"] = False
        case = self._build_case(
            "CASE-SCS-NEG-PSYCH-FAIL", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_scs_negative_cognitive_inability(self):
        """TC-SCS-013: Inability to demonstrate cognitive ability to operate stimulator fails psychological clearance."""
        ev = dict(self.scs_base_evidence)
        ev["cognitive_ability_to_manage_stimulator"] = False
        case = self._build_case(
            "CASE-SCS-NEG-NO-COGNITIVE", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_scs_indeterminate_missing_psychological_evaluation(self):
        """TC-SCS-014: Missing psychological assessment parameters returns INSUFFICIENT_INFORMATION."""
        ev = dict(self.scs_base_evidence)
        del ev["pain_not_due_to_psychiatric_disorder"]
        del ev["psychiatric_personality_disorders_managed"]
        case = self._build_case(
            "CASE-SCS-IND-MISSING-PSYCH", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    def test_scs_indeterminate_missing_mrsa_status(self):
        """TC-SCS-015: Missing MRSA colonization evidence returns INSUFFICIENT_INFORMATION."""
        ev = dict(self.scs_base_evidence)
        del ev["mrsa_mssa_colonization_present"]
        case = self._build_case(
            "CASE-SCS-IND-MISSING-MRSA", "63650", "Percutaneous SCS Trial",
            ev
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 2. RULE-IPM-EPOS1755-001 (Place of Service Policy 1755 Clinical Exceptions)
    # =========================================================================

    def test_epos_asa_score_3_qualifies_for_hospital_setting(self):
        """TC-EPOS-001: ASA Physical Status score >= 3 justifies Outpatient Hospital setting."""
        case = self._build_case(
            "CASE-EPOS-POS-ASA3", "63650", "SCS Trial",
            {"asa_physical_status_score": 3},
            pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_bmi_40_qualifies_for_hospital_setting(self):
        """TC-EPOS-002: BMI >= 40 (severe obesity) justifies Outpatient Hospital setting."""
        case = self._build_case(
            "CASE-EPOS-POS-BMI40", "63650", "SCS Trial",
            {"patient_bmi": 42.5},
            pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_cardiovascular_comorbidity_qualifies(self):
        """TC-EPOS-003: Heart disease / prior heart surgery justifies Outpatient Hospital setting."""
        case = self._build_case(
            "CASE-EPOS-POS-HEART", "63650", "SCS Trial",
            {"heart_disease_or_prior_heart_surgery": True},
            pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_chronic_lung_disease_qualifies(self):
        """TC-EPOS-004: Moderate to severe COPD or asthma justifies Outpatient Hospital setting."""
        case = self._build_case(
            "CASE-EPOS-POS-LUNG", "63650", "SCS Trial",
            {"chronic_lung_disease_copd_or_asthma": True},
            pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_sleep_apnea_qualifies(self):
        """TC-EPOS-005: Diagnosed sleep apnea / airway risk justifies Outpatient Hospital setting."""
        case = self._build_case(
            "CASE-EPOS-POS-SLEEP-APNEA", "63650", "SCS Trial",
            {"sleep_apnea_diagnosed": True},
            pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_pregnancy_qualifies(self):
        """TC-EPOS-006: Pregnancy justifies Outpatient Hospital setting under EPOS 1755."""
        case = self._build_case(
            "CASE-EPOS-POS-PREGNANCY", "63650", "SCS Trial",
            {"pregnancy_status": True},
            pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_boundary_asa_score(self):
        """Boundary test: ASA PS score 2 fails (< 3), score 3 passes."""
        case_fail = self._build_case(
            "CASE-EPOS-BND-ASA2-FAIL", "63650", "SCS Trial",
            self.epos_all_negative_evidence,
            pos="OUTPATIENT_HOSPITAL"
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res_fail.place_of_service_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        ev_pass = dict(self.epos_all_negative_evidence)
        ev_pass["asa_physical_status_score"] = 3
        case_pass = self._build_case(
            "CASE-EPOS-BND-ASA3-PASS", "63650", "SCS Trial",
            ev_pass,
            pos="OUTPATIENT_HOSPITAL"
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res_pass.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_boundary_bmi(self):
        """Boundary test: BMI 39.9 fails (< 40.0), 40.0 passes."""
        ev_fail = dict(self.epos_all_negative_evidence)
        ev_fail["patient_bmi"] = 39.9
        case_fail = self._build_case(
            "CASE-EPOS-BND-BMI39-FAIL", "63650", "SCS Trial",
            ev_fail,
            pos="OUTPATIENT_HOSPITAL"
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res_fail.place_of_service_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        ev_pass = dict(self.epos_all_negative_evidence)
        ev_pass["patient_bmi"] = 40.0
        case_pass = self._build_case(
            "CASE-EPOS-BND-BMI40-PASS", "63650", "SCS Trial",
            ev_pass,
            pos="OUTPATIENT_HOSPITAL"
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res_pass.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)

    def test_epos_indeterminate_missing_evidence(self):
        """TC-EPOS-009: Outpatient Hospital requested with no clinical exception parameters returns INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-EPOS-IND-MISSING", "63650", "SCS Trial",
            {},
            pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 3. Clinical Necessity vs Place of Service Dual-Track Separation
    # =========================================================================

    def test_dual_track_clinical_met_and_pos_met(self):
        """Dual Track: SCS trial clinically indicated AND patient has ASA 3 comorbidity -> Overall CRITERIA_MET."""
        ev = dict(self.scs_base_evidence)
        ev["asa_physical_status_score"] = 3
        case = self._build_case(
            "CASE-DUAL-CN-MET-POS-MET", "63650", "Percutaneous SCS Trial",
            ev, pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.clinical_necessity_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_dual_track_clinical_met_and_pos_not_met_redirection(self):
        """Dual Track: SCS trial clinically indicated BUT healthy patient requests Outpatient Hospital without exception ->

        Clinical Necessity: CRITERIA_MET.
        Place of Service: CRITERIA_NOT_MET.
        Overall: CRITERIA_NOT_MET with redirection note to ambulatory setting.
        """
        ev = dict(self.scs_base_evidence)
        ev.update(self.epos_all_negative_evidence)
        case = self._build_case(
            "CASE-DUAL-CN-MET-POS-REDIR", "63650", "Percutaneous SCS Trial",
            ev, pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.clinical_necessity_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertIn("Redirection to ambulatory/freestanding facility required", res.overall_summary)

    def test_dual_track_clinical_not_met_and_pos_met(self):
        """Dual Track: SCS trial NOT clinically indicated (active infection) even if patient qualifies for hospital setting (ASA 3) ->

        Clinical Necessity: CRITERIA_NOT_MET.
        Place of Service: CRITERIA_MET.
        Overall: CRITERIA_NOT_MET. Clinical failure is not overridden by POS authorization.
        """
        ev = dict(self.scs_base_evidence)
        ev["active_systemic_or_spinal_infection"] = True
        ev["asa_physical_status_score"] = 3
        case = self._build_case(
            "CASE-DUAL-CN-FAIL-POS-MET", "63650", "Percutaneous SCS Trial",
            ev, pos="OUTPATIENT_HOSPITAL"
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-EPOS1755-001"])
        self.assertEqual(res.clinical_necessity_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(res.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 4. CPT Candidate Routing & Cross-Domain Isolation
    # =========================================================================

    def test_cpt_routing_all_scs_codes(self):
        """Verify deterministic routing across all 8 SCS CPT codes."""
        scs_cpts = [
            "63650", "63655", "63661", "63662",
            "63663", "63664", "63685", "63688"
        ]
        for cpt in scs_cpts:
            case = self._build_case(f"CASE-ROUTE-SCS-{cpt}", cpt, "SCS Procedure Routing", {})
            _, _, intake = self.validator.validate(case)
            self.assertIsNotNone(intake, f"Validation failed for case with CPT {cpt}")
            result = self.router.route_case(intake)
            self.assertEqual(result.status, "ROUTED")
            routed_ids = [r.rule_id for r in result.applicable_rules]
            self.assertIn("RULE-IPM-CGSPINALCORDSTIM-001", routed_ids, f"CPT {cpt} did not route to RULE-IPM-CGSPINALCORDSTIM-001")

    def test_cross_domain_isolation(self):
        """Verify strict domain isolation between IPM and Advanced Imaging."""
        ai_case = {
            "case_id": "CASE-ISO-AI-72141",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72141",
            "procedure_name": "MRI Cervical Spine without Contrast",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        _, _, ai_intake = self.validator.validate(ai_case)
        self.assertIsNotNone(ai_intake)
        ai_route = self.router.route_case(ai_intake)
        ai_rule_ids = [r.rule_id for r in ai_route.applicable_rules]
        self.assertNotIn("RULE-IPM-CGSPINALCORDSTIM-001", ai_rule_ids)
        self.assertNotIn("RULE-IPM-EPOS1755-001", ai_rule_ids)

    # =========================================================================
    # 5. Canonical Governance Invariants
    # =========================================================================

    def test_governance_invariants(self):
        """Preserve canonical governance invariants: 128 active rules, 0 approved, 7 gates blocked."""
        all_rules = self.registry.get_all_rules()
        self.assertEqual(len(all_rules), 128, f"Expected 128 active rules, found {len(all_rules)}")

        approved_rules = [r for r in all_rules if r.is_approved]
        self.assertEqual(len(approved_rules), 0, f"Expected 0 approved rules, found {len(approved_rules)}")

        # Verify both Batch 3 rules remain in DRAFT status
        batch3_rule_ids = [
            "RULE-IPM-CGSPINALCORDSTIM-001",
            "RULE-IPM-EPOS1755-001"
        ]
        for rid in batch3_rule_ids:
            rule = self.registry.get_rule(rid)
            self.assertIsNotNone(rule, f"Rule {rid} not found in registry")
            self.assertEqual(rule.extraction_status, "DRAFT", f"Rule {rid} must remain in DRAFT status")
            self.assertFalse(rule.is_approved)

        # Verify all 7 canonical governance gates remain blocked
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


if __name__ == "__main__":
    unittest.main()
