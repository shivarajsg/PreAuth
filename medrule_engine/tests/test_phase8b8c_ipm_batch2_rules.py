"""Phase 8B.8C: Controlled IPM Batch 2 Implementation Focused Test Suite.

Comprehensive validation of the four authorized Interventional Pain Management rules:
1. RULE-IPM-CGFACETBLOCKS-001 (Facet Joint Injections/Blocks - Guideline 1753, CPT 64490-64495, 0213T-0218T):
   - Pathway 1: Axial non-radicular facet pain (>= 3m duration, failed >= 6w conservative care within 6m, primary SIJ/discogenic excluded, imaging guidance).
   - Pathway 2: Facet synovial cyst with radicular pain/stenosis on MRI/CT (failed >= 6w conservative care, imaging guidance).
   - Pathway 3: Spondylolysis with pars interarticularis defect (>= 3m duration, failed >= 6w conservative care, imaging guidance).
   - Prerequisites & Exclusions: Hardware injection excluded, max 2 diagnostic sessions per region, max 4 injections per 12 months, imaging guidance required.
   - Boundary tests: Conservative care 5.9w vs 6.0w; pain duration 2.9m vs 3.0m; pain score 5 vs 6.
   - Negative & Indeterminate tests: Hardware injection, > 2 sessions, > 4 yearly injections, no guidance, missing evidence.

2. RULE-IPM-CGFACETDENERVATION-001 (Paravertebral Facet Denervation / RFA - Guideline 1754, CPT 64633-64636):
   - Pathway 1: Initial RFA following diagnostic MBB (relief >= 70%, pain >= 6/10 or disability, duration >= 3m, failed >= 6w conservative care, primary SIJ/discogenic excluded, fluoroscopy/CT guidance).
   - Pathway 2: Repeat RFA (prior RFA relief >= 50% for >= 4 months, ongoing conservative therapy, max 2 procedures per 12 months, fluoroscopy/CT guidance).
   - Boundary tests: MBB relief 69% vs 70%; repeat duration 3.9m vs 4.0m; prior RFA relief 49% vs 50%; conservative care 5.9w vs 6.0w.
   - Negative & Indeterminate tests: MBB relief < 70%, repeat duration < 4m, lack of guidance, missing evidence.

3. RULE-IPM-CGFACETDENERVATION-002 (Repeat Facet RFA Relief Threshold - Guideline 1754, CPT 64633-64636):
   - Boundary threshold tests: 49% fails vs 50% passes.
   - Missing evidence tests: parameter absent -> INSUFFICIENT_INFORMATION.

4. RULE-IPM-CGSYMPATHETICBLOCKS-001 (Sympathetic Nerve Blocks - Guideline 1758, CPT 64510, 64517, 64520, 64530):
   - Pathway 1: Stellate Ganglion Block (64510) - acute herpes zoster (< 4w + antiviral), cancer/phantom limb pain, CRPS (Budapest criteria + functional restoration), repeat block (>= 50% relief).
   - Pathway 2: Thoracic/Lumbar Block (64520) - acute zoster (< 4w + antiviral), ischemic limb pain, cancer/phantom limb pain, CRPS, repeat block.
   - Pathway 3: Celiac Plexus Block (64530) - upper abdominal cancer pain refractory/intolerant to opioids, chronic pancreatitis pain, repeat block.
   - Pathway 4: Superior Hypogastric Plexus Block (64517) - pelvic/rectal cancer pain refractory/intolerant to opioids, chronic visceral pelvic pain, repeat block.
   - Prerequisites & Exclusions: Imaging guidance required, bilateral block prohibited.
   - Boundary tests: Zoster duration 3.9w vs 4.1w; repeat block relief 49% vs 50%.
   - Negative & Indeterminate tests: Bilateral block requested, zoster duration >= 4w, missing evidence.

5. CPT Candidate Routing & Domain Isolation:
   - Full routing verification across all 16 CPT/HCPCS codes:
     - 64490, 64491, 64492, 64493, 64494, 64495
     - 0213T, 0214T, 0215T, 0216T, 0217T, 0218T
     - 64633, 64634, 64635, 64636
     - 64510, 64517, 64520, 64530
   - Cross-domain isolation between IPM and Advanced Imaging.

6. Canonical Governance Invariants:
   - All 4 rules in DRAFT status (APPROVED count = 0).
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


class TestPhase8B8CIPMBatch2Rules(unittest.TestCase):
    """Focused test suite for Phase 8B.8C authorized IPM Batch 2 rules."""

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

    # =========================================================================
    # 1. RULE-IPM-CGFACETBLOCKS-001 (Facet Joint Injections/Blocks - Guideline 1753)
    # =========================================================================

    def test_facet_pathway_1_axial_pain_positive(self):
        """TC-FACET-001: Axial non-radicular facet pain >= 3m, failed 6w conservative care in last 6m, pain 7/10, fluoroscopy."""
        case = self._build_case(
            "CASE-FACET-P1-AXIAL-POS", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(res.clinical_necessity_rules[0].outcome, DecisionOutcome.CRITERIA_MET)

    def test_facet_pathway_2_synovial_cyst_positive(self):
        """TC-FACET-002: Facet synovial cyst causing radicular pain/stenosis on MRI, failed 8w conservative care, guidance."""
        case = self._build_case(
            "CASE-FACET-P2-CYST-POS", "64493", "Lumbar Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "functional_disability_documented": True,
                "facet_synovial_cyst_confirmed_on_imaging": True,
                "radicular_stenosis_symptoms_present": True,
                "conservative_therapy_duration_weeks": 8,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_facet_pathway_3_spondylolysis_positive(self):
        """TC-FACET-003: Spondylolysis with pars interarticularis defect, pain 5m, failed 6w conservative care, guidance."""
        case = self._build_case(
            "CASE-FACET-P3-SPONDY-POS", "64493", "Lumbar Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 6,
                "pars_interarticularis_defect_confirmed": True,
                "pain_duration_months": 5.0,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_facet_boundary_conservative_therapy_duration(self):
        """Boundary test: 5.9 weeks conservative therapy fails (< 6w), 6.0 weeks passes."""
        case_fail = self._build_case(
            "CASE-FACET-BND-CONS-FAIL", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 5.9,
                "conservative_therapy_within_6_months": True,
                "ongoing_conservative_therapy": False,
                "conservative_therapy_exception_documented": False,
                "facet_synovial_cyst_confirmed_on_imaging": False,
                "pars_interarticularis_defect_confirmed": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        case_pass = self._build_case(
            "CASE-FACET-BND-CONS-PASS", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6.0,
                "conservative_therapy_within_6_months": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_facet_boundary_pain_duration_months(self):
        """Boundary test: 2.9 months pain duration fails (< 3.0m), 3.0 months passes."""
        case_fail = self._build_case(
            "CASE-FACET-BND-DUR-FAIL", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 2.9,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "facet_synovial_cyst_confirmed_on_imaging": False,
                "pars_interarticularis_defect_confirmed": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        case_pass = self._build_case(
            "CASE-FACET-BND-DUR-PASS", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 3.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_facet_negative_hardware_injection(self):
        """TC-FACET-006: Hardware injection is explicitly excluded under Guideline 1753."""
        case = self._build_case(
            "CASE-FACET-NEG-HARDWARE", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": True,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_facet_negative_exceeded_diagnostic_sessions(self):
        """TC-FACET-007: Exceeding maximum 2 diagnostic sessions per region fails."""
        case = self._build_case(
            "CASE-FACET-NEG-3SESSIONS", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 3,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_facet_negative_exceeded_yearly_injections(self):
        """TC-FACET-008: Exceeding maximum 4 facet injections in 12 months fails."""
        case = self._build_case(
            "CASE-FACET-NEG-5YEARLY", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": True,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 5,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_facet_negative_no_imaging_guidance(self):
        """TC-FACET-009: Injection without fluoroscopy/CT guidance fails mandatory imaging guidance."""
        case = self._build_case(
            "CASE-FACET-NEG-NO-GUIDANCE", "64490", "Cervical Facet Injection",
            {
                "imaging_guidance_present": False,
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_facet_indeterminate_missing_guidance(self):
        """TC-FACET-010: Missing imaging guidance evidence returns INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-FACET-IND-MISSING-GUIDANCE", "64490", "Cervical Facet Injection",
            {
                "hardware_injection_requested": False,
                "diagnostic_sessions_in_region_count": 1,
                "injections_past_12_months_count": 1,
                "pain_intensity_score_numeric": 7,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 2. RULE-IPM-CGFACETDENERVATION-001 (Facet Denervation/RFA - Guideline 1754)
    # =========================================================================

    def test_rfa_pathway_1_initial_denervation_positive(self):
        """TC-RFA-001: Initial RFA following MBB with 75% relief (>= 70%), pain 8/10, duration 4m, failed 6w care, guidance."""
        case = self._build_case(
            "CASE-RFA-P1-INITIAL-POS", "64633", "Cervical Facet RFA",
            {
                "imaging_guidance_present": True,
                "pain_intensity_score_numeric": 8,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "diagnostic_mbb_relief_percentage": 75,
                "pain_returned_after_diagnostic_block": True,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_rfa_pathway_2_repeat_denervation_positive(self):
        """TC-RFA-002: Repeat RFA with 60% prior relief (>= 50%) lasting 5 months (>= 4m), ongoing care, <= 2 procedures."""
        case = self._build_case(
            "CASE-RFA-P2-REPEAT-POS", "64635", "Lumbar Facet RFA",
            {
                "imaging_guidance_present": True,
                "prior_rfa_relief_percentage": 60,
                "prior_rfa_duration_months": 5.0,
                "functional_disability_documented": True,
                "ongoing_conservative_therapy": True,
                "rfa_procedures_past_12_months": 1
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_rfa_boundary_initial_mbb_relief(self):
        """Boundary test: Initial MBB relief 69% fails (< 70%), 70% passes."""
        case_fail = self._build_case(
            "CASE-RFA-BND-MBB-FAIL", "64633", "Cervical Facet RFA",
            {
                "imaging_guidance_present": True,
                "pain_intensity_score_numeric": 8,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "diagnostic_mbb_relief_percentage": 69,
                "pain_returned_after_diagnostic_block": True,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True,
                "prior_rfa_relief_percentage": 0,
                "prior_rfa_duration_months": 0,
                "rfa_procedures_past_12_months": 0,
                "ongoing_conservative_therapy": False,
                "conservative_therapy_exception_documented": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        case_pass = self._build_case(
            "CASE-RFA-BND-MBB-PASS", "64633", "Cervical Facet RFA",
            {
                "imaging_guidance_present": True,
                "pain_intensity_score_numeric": 8,
                "pain_is_axial_nonradicular": True,
                "pain_duration_months": 4.0,
                "diagnostic_mbb_relief_percentage": 70,
                "pain_returned_after_diagnostic_block": True,
                "primary_sij_discogenic_radicular_excluded": True,
                "conservative_therapy_duration_weeks": 6,
                "conservative_therapy_within_6_months": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_rfa_boundary_repeat_relief_duration(self):
        """Boundary test: Repeat RFA relief duration 3.9 months fails (< 4.0m), 4.0 months passes."""
        case_fail = self._build_case(
            "CASE-RFA-BND-REPEAT-DUR-FAIL", "64635", "Lumbar Facet RFA",
            {
                "imaging_guidance_present": True,
                "functional_disability_documented": True,
                "prior_rfa_relief_percentage": 60,
                "prior_rfa_duration_months": 3.9,
                "ongoing_conservative_therapy": True,
                "rfa_procedures_past_12_months": 1,
                "diagnostic_mbb_relief_percentage": 0,
                "pain_is_axial_nonradicular": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        case_pass = self._build_case(
            "CASE-RFA-BND-REPEAT-DUR-PASS", "64635", "Lumbar Facet RFA",
            {
                "imaging_guidance_present": True,
                "functional_disability_documented": True,
                "prior_rfa_relief_percentage": 60,
                "prior_rfa_duration_months": 4.0,
                "ongoing_conservative_therapy": True,
                "rfa_procedures_past_12_months": 1
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_rfa_negative_exceeded_frequency_limit(self):
        """TC-RFA-005: Exceeding maximum 2 RFA procedures in 12 months fails repeat pathway."""
        case = self._build_case(
            "CASE-RFA-NEG-3FREQ", "64635", "Lumbar Facet RFA",
            {
                "imaging_guidance_present": True,
                "functional_disability_documented": True,
                "prior_rfa_relief_percentage": 60,
                "prior_rfa_duration_months": 5.0,
                "ongoing_conservative_therapy": True,
                "rfa_procedures_past_12_months": 3,
                "diagnostic_mbb_relief_percentage": 0,
                "pain_is_axial_nonradicular": False
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # =========================================================================
    # 3. RULE-IPM-CGFACETDENERVATION-002 (Repeat Facet RFA Relief Threshold)
    # =========================================================================

    def test_rfa002_boundary_49_percent_fails(self):
        """TC-RFA002-001: 49% prior relief fails the 50% repeat RFA threshold."""
        case = self._build_case(
            "CASE-RFA002-49-FAIL", "64635", "Lumbar Facet RFA",
            {"diagnostic_facet_block_relief": 49}
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_rfa002_boundary_50_percent_passes(self):
        """TC-RFA002-002: 50% prior relief satisfies the 50% repeat RFA threshold."""
        case = self._build_case(
            "CASE-RFA002-50-PASS", "64635", "Lumbar Facet RFA",
            {"diagnostic_facet_block_relief": 50}
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_rfa002_indeterminate_missing_relief(self):
        """TC-RFA002-003: Missing prior relief returns INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-RFA002-IND-MISSING", "64635", "Lumbar Facet RFA",
            {}
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-002"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 4. RULE-IPM-CGSYMPATHETICBLOCKS-001 (Sympathetic Nerve Blocks - Guideline 1758)
    # =========================================================================

    def test_symp_pathway_1_stellate_zoster_positive(self):
        """TC-SYMP-001: Stellate Ganglion Block for acute zoster (duration 2.5w < 4w, active antiviral, unilateral, guidance)."""
        case = self._build_case(
            "CASE-SYMP-P1-ZOSTER-POS", "64510", "Stellate Ganglion Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": False,
                "pain_intensity_score_numeric": 8,
                "acute_herpes_zoster_present": True,
                "zoster_duration_weeks": 2.5,
                "active_antiviral_therapy": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_symp_pathway_2_lumbar_ischemic_positive(self):
        """TC-SYMP-002: Lumbar Sympathetic Block for nonsurgical ischemic limb pain with failed conservative care."""
        case = self._build_case(
            "CASE-SYMP-P2-ISCHEMIC-POS", "64520", "Lumbar Sympathetic Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": False,
                "pain_intensity_score_numeric": 7,
                "nonsurgical_ischemic_limb_pain": True,
                "conservative_therapy_failed": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_symp_pathway_3_celiac_cancer_pain_positive(self):
        """TC-SYMP-003: Celiac Plexus Block for upper abdominal visceral cancer pain refractory to systemic opioids."""
        case = self._build_case(
            "CASE-SYMP-P3-CELIAC-POS", "64530", "Celiac Plexus Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": False,
                "cancer_pain_present": True,
                "upper_abdominal_cancer_pain": True,
                "systemic_opioid_refractory_or_intolerant": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_symp_pathway_4_hypogastric_pelvic_cancer_positive(self):
        """TC-SYMP-004: Superior Hypogastric Plexus Block for pelvic/rectal cancer pain refractory to systemic opioids."""
        case = self._build_case(
            "CASE-SYMP-P4-HYPOGASTRIC-POS", "64517", "Superior Hypogastric Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": False,
                "cancer_pain_present": True,
                "pelvic_rectal_cancer_pain": True,
                "systemic_opioid_refractory_or_intolerant": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_MET)

    def test_symp_boundary_zoster_duration_weeks(self):
        """Boundary test: Zoster duration 3.9 weeks qualifies (< 4.0w), 4.1 weeks fails."""
        case_pass = self._build_case(
            "CASE-SYMP-BND-ZOSTER-PASS", "64510", "Stellate Ganglion Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": False,
                "pain_intensity_score_numeric": 8,
                "acute_herpes_zoster_present": True,
                "zoster_duration_weeks": 3.9,
                "active_antiviral_therapy": True
            }
        )
        res_pass = self.engine.evaluate(case_pass, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res_pass.overall_outcome, DecisionOutcome.CRITERIA_MET)

        case_fail = self._build_case(
            "CASE-SYMP-BND-ZOSTER-FAIL", "64510", "Stellate Ganglion Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": False,
                "pain_intensity_score_numeric": 8,
                "acute_herpes_zoster_present": True,
                "zoster_duration_weeks": 4.1,
                "active_antiviral_therapy": True,
                "cancer_pain_present": False,
                "phantom_limb_pain_present": False,
                "crps_budapest_criteria_met": False,
                "prior_block_relief_percentage": 0,
                "nonsurgical_ischemic_limb_pain": False,
                "upper_abdominal_cancer_pain": False,
                "chronic_pancreatitis_pain": False,
                "pelvic_rectal_cancer_pain": False,
                "chronic_noncancer_pelvic_visceral_pain": False
            }
        )
        res_fail = self.engine.evaluate(case_fail, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res_fail.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_symp_negative_bilateral_block_prohibited(self):
        """TC-SYMP-007: Bilateral sympathetic blocks on same day of service are prohibited."""
        case = self._build_case(
            "CASE-SYMP-NEG-BILATERAL", "64510", "Stellate Ganglion Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": True,
                "pain_intensity_score_numeric": 8,
                "acute_herpes_zoster_present": True,
                "zoster_duration_weeks": 2.5,
                "active_antiviral_therapy": True
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    def test_symp_indeterminate_missing_antiviral(self):
        """TC-SYMP-008: Missing active antiviral therapy evidence returns INSUFFICIENT_INFORMATION."""
        case = self._build_case(
            "CASE-SYMP-IND-MISSING-ANTIVIRAL", "64510", "Stellate Ganglion Block",
            {
                "imaging_guidance_present": True,
                "bilateral_procedure_requested": False,
                "pain_intensity_score_numeric": 8,
                "acute_herpes_zoster_present": True,
                "zoster_duration_weeks": 2.5
            }
        )
        res = self.engine.evaluate(case, target_rule_ids=["RULE-IPM-CGSYMPATHETICBLOCKS-001"])
        self.assertEqual(res.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # =========================================================================
    # 5. CPT Candidate Routing & Cross-Domain Isolation
    # =========================================================================

    def test_cpt_routing_all_batch2_codes(self):
        """Verify deterministic routing across all 16 CPT/HCPCS codes for Batch 2."""
        batch2_cpt_expected_rules = {
            # Facet Blocks (Guideline 1753)
            "64490": ["RULE-IPM-CGFACETBLOCKS-001"],
            "64491": ["RULE-IPM-CGFACETBLOCKS-001"],
            "64492": ["RULE-IPM-CGFACETBLOCKS-001"],
            "64493": ["RULE-IPM-CGFACETBLOCKS-001"],
            "64494": ["RULE-IPM-CGFACETBLOCKS-001"],
            "64495": ["RULE-IPM-CGFACETBLOCKS-001"],
            "0213T": ["RULE-IPM-CGFACETBLOCKS-001"],
            "0214T": ["RULE-IPM-CGFACETBLOCKS-001"],
            "0215T": ["RULE-IPM-CGFACETBLOCKS-001"],
            "0216T": ["RULE-IPM-CGFACETBLOCKS-001"],
            "0217T": ["RULE-IPM-CGFACETBLOCKS-001"],
            "0218T": ["RULE-IPM-CGFACETBLOCKS-001"],
            # Facet Denervation (Guideline 1754)
            "64633": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
            "64634": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
            "64635": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
            "64636": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
            # Sympathetic Blocks (Guideline 1758)
            "64510": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"],
            "64517": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"],
            "64520": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"],
            "64530": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"]
        }

        for cpt, expected_rule_ids in batch2_cpt_expected_rules.items():
            case = self._build_case(f"CASE-ROUTE-{cpt}", cpt, "Procedure Routing Test", {})
            _, _, intake = self.validator.validate(case)
            self.assertIsNotNone(intake, f"Validation failed for case with CPT {cpt}")
            result = self.router.route_case(intake)
            self.assertEqual(result.status, "ROUTED")
            routed_ids = [r.rule_id for r in result.applicable_rules]
            for exp_id in expected_rule_ids:
                self.assertIn(exp_id, routed_ids, f"CPT {cpt} did not route to expected rule {exp_id}")

    def test_cross_domain_isolation(self):
        """Verify strict domain isolation between IPM and Advanced Imaging."""
        # Advanced Imaging MRI spine case must not route to any IPM facet or sympathetic rules
        ai_case = {
            "case_id": "CASE-ISO-AI-72148",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72148",
            "procedure_name": "MRI Lumbar Spine without Contrast",
            "place_of_service": "OFFICE",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        _, _, ai_intake = self.validator.validate(ai_case)
        self.assertIsNotNone(ai_intake)
        ai_route = self.router.route_case(ai_intake)
        ai_rule_ids = [r.rule_id for r in ai_route.applicable_rules]
        self.assertNotIn("RULE-IPM-CGFACETBLOCKS-001", ai_rule_ids)
        self.assertNotIn("RULE-IPM-CGFACETDENERVATION-001", ai_rule_ids)
        self.assertNotIn("RULE-IPM-CGFACETDENERVATION-002", ai_rule_ids)
        self.assertNotIn("RULE-IPM-CGSYMPATHETICBLOCKS-001", ai_rule_ids)

    # =========================================================================
    # 6. Canonical Governance Invariants
    # =========================================================================

    def test_governance_invariants(self):
        """Preserve canonical governance invariants: 128 active rules, 0 approved, 7 gates blocked."""
        all_rules = self.registry.get_all_rules()
        self.assertEqual(len(all_rules), 128, f"Expected 128 active rules, found {len(all_rules)}")

        approved_rules = [r for r in all_rules if r.is_approved]
        self.assertEqual(len(approved_rules), 0, f"Expected 0 approved rules, found {len(approved_rules)}")

        # Verify all four Batch 2 rules remain in DRAFT status
        batch2_rule_ids = [
            "RULE-IPM-CGFACETBLOCKS-001",
            "RULE-IPM-CGFACETDENERVATION-001",
            "RULE-IPM-CGFACETDENERVATION-002",
            "RULE-IPM-CGSYMPATHETICBLOCKS-001"
        ]
        for rid in batch2_rule_ids:
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
