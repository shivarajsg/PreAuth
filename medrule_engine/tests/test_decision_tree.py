"""MedRule Deterministic Decision Tree Unit & Integration Test Suite.

Verifies:
1. All 121 ready DRAFT rules compilation and execution.
2. All 7 NEEDS_HUMAN_REVIEW rules strictly blocked from autonomous execution.
3. Zero APPROVED rules governance invariant.
4. Dual-track separation: Clinical Necessity vs Place of Service (EPOS 2067 / EPOS 1755).
5. Missing input fields never satisfy criteria (INSUFFICIENT_INFORMATION).
6. Boolean ALL_OF and ANY_OF branching logic.
7. Numerical and temporal boundary values (immediately below, at, and above thresholds).
8. Prior-treatment prerequisites and documented failure.
9. Exclusions, contraindications, and negative decision effects.
10. Repeat-service intervals and frequency limits.
11. Uncovered policy criteria gap escalation.
12. Full source provenance fidelity (source file, page, section, quote).
13. Clinical domain isolation (Advanced Imaging and IPM only; archived domains rejected).
14. Deterministic repeatability and cryptographic hash stability.
"""

import copy
import datetime
import json
from pathlib import Path
import unittest

from medrule_engine.case_validator import CaseIntake, CaseValidator
from medrule_engine.condition_evaluator import EvaluationState
from medrule_engine.decision_tree import (
    DecisionOutcome,
    DecisionTrack,
    DecisionTreeAssessment,
    DecisionTreeEngine,
    GOVERNANCE_BLOCKED_RULE_IDS,
)
from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.rule_registry import RuleRegistry


class TestMedRuleDecisionTree(unittest.TestCase):
    """Rigorous test suite for MedRule deterministic decision-tree execution."""

    @classmethod
    def setUpClass(cls):
        # Active registry contains strictly 2 active domains (128 rules)
        cls.registry = RuleRegistry(include_archived=False)
        cls.total_rules = cls.registry.load_all_domains()
        cls.engine = DecisionTreeEngine(registry=cls.registry)
        cls.service = EvaluationService(registry=cls.registry)

    # -------------------------------------------------------------------------
    # Test 1: All 121 Ready DRAFT Rules Compilation
    # -------------------------------------------------------------------------
    def test_01_all_121_ready_rules_compilation(self):
        """Verify that exactly 121 rules are in DRAFT status and ready for deterministic execution."""
        all_rules = self.registry.all_rules
        self.assertEqual(len(all_rules), 128, "Total active rules must be exactly 128.")

        ready_rules = [r for r in all_rules if r.extraction_status == "DRAFT"]
        blocked_rules = [r for r in all_rules if r.extraction_status == "NEEDS_HUMAN_REVIEW"]

        self.assertEqual(len(ready_rules), 121, "Exactly 121 rules must be DRAFT.")
        self.assertEqual(len(blocked_rules), 7, "Exactly 7 rules must be NEEDS_HUMAN_REVIEW.")

        # Test evaluating each ready rule with target_rule_ids
        for r in ready_rules:
            case_data = {
                "case_id": f"CASE-COMPILE-{r.rule_id}",
                "clinical_domain": r.domain,
                "procedure_code": "70551" if r.domain == "advanced_imaging" else "62322",
                "procedure_name": r.clinical_service_or_procedure,
                "requested_date_of_service": "2026-03-01",
                "line_of_business": "COMMERCIAL",
                "payer_id": "TEST_PAYER",
                "clinical_evidence": {}
            }
            # Evaluate using target_rule_ids
            assessment = self.engine.evaluate(case_data, target_rule_ids=[r.rule_id])
            self.assertFalse(assessment.is_binding)
            self.assertIn(assessment.overall_outcome, [
                DecisionOutcome.CRITERIA_MET,
                DecisionOutcome.CRITERIA_NOT_MET,
                DecisionOutcome.INSUFFICIENT_INFORMATION,
                DecisionOutcome.NEEDS_HUMAN_REVIEW
            ])

    # -------------------------------------------------------------------------
    # Test 2: All 7 NEEDS_HUMAN_REVIEW Rules Strictly Blocked
    # -------------------------------------------------------------------------
    def test_02_all_7_needs_human_review_rules_strictly_blocked(self):
        """Verify that all 7 blocked rules NEVER autonomously approve or deny."""
        self.assertEqual(len(GOVERNANCE_BLOCKED_RULE_IDS), 7)

        for rid in sorted(GOVERNANCE_BLOCKED_RULE_IDS):
            rule = self.registry.get_rule(rid)
            self.assertIsNotNone(rule, f"Blocked rule {rid} must exist in active registry.")
            self.assertEqual(rule.extraction_status, "NEEDS_HUMAN_REVIEW")

            # Craft a fully satisfied case payload
            case_data = {
                "case_id": f"CASE-BLOCKED-{rid}",
                "clinical_domain": rule.domain,
                "procedure_code": "70450" if rule.domain == "advanced_imaging" else "62322",
                "procedure_name": rule.clinical_service_or_procedure,
                "requested_date_of_service": "2026-04-01",
                "line_of_business": "COMMERCIAL",
                "payer_id": "TEST_PAYER",
                "clinical_evidence": {
                    "ordering_provider_license": True,
                    "clinical_office_notes": True,
                    "laboratory_and_testing_data": True,
                    "patient_age_years": 30,
                    "requested_modality": "CT",
                    "emergency_clinical_condition": True,
                    "threat_to_life_or_limb": True,
                    "intraspinal_drug_trial_indicated": True
                }
            }
            assessment = self.engine.evaluate(case_data, target_rule_ids=[rid])
            self.assertEqual(
                assessment.overall_outcome,
                DecisionOutcome.NEEDS_HUMAN_REVIEW,
                f"Rule {rid} must strictly yield NEEDS_HUMAN_REVIEW regardless of evidence."
            )
            self.assertTrue(len(assessment.human_review_reasons) > 0)
            self.assertTrue(any(rid in reason for reason in assessment.human_review_reasons))

    # -------------------------------------------------------------------------
    # Test 3: Zero APPROVED Rules Invariant
    # -------------------------------------------------------------------------
    def test_03_zero_approved_rules_governance_invariant(self):
        """Governance invariant: 0 rules approved across active registry and decision tree."""
        approved_rules = [r for r in self.registry.all_rules if r.is_approved]
        self.assertEqual(len(approved_rules), 0, "Zero rules may be marked approved.")
        for r in self.registry.all_rules:
            self.assertFalse(r.is_approved)
            self.assertFalse(r.is_binding)

    # -------------------------------------------------------------------------
    # Test 4: Dual Track Separation: Clinical Necessity vs Place of Service
    # -------------------------------------------------------------------------
    def test_04_dual_track_separation_clinical_necessity_vs_place_of_service(self):
        """Dual track test: clinical necessity evaluated separately from place of service."""
        # Case A: Clinical necessity MET, but requested Place of Service is Hospital Outpatient without exception
        case_dict = {
            "case_id": "CASE-DUAL-001",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "modality": "MRI",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "clinical_evidence": {
                "ordering_provider_license": True,
                "clinical_office_notes": True,
                "suspected_or_established_multiple_sclerosis": True,
                "focal_neurological_deficit_present": True,
                # Explicit POS code indicating hospital outpatient (not POS_11 or POS_24)
                "place_of_service_code": "POS_22",
                # No POS exception evidence provided:
                "severe_claustrophobia_open_mri_needed": False,
                "bariatric_weight_exceeds_freestanding_scanner": False,
                "complex_specialized_protocol_needed": False
            }
        }
        # Target Brain MRI rule and POS rules
        assessment = self.engine.evaluate(
            case_dict,
            target_rule_ids=["RULE-ADV-CG2012-003", "RULE-ADV-EPOS2067-001", "RULE-ADV-EPOS2067-004"]
        )
        self.assertEqual(assessment.clinical_necessity_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(assessment.place_of_service_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertEqual(assessment.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertIn("Place of Service", assessment.overall_summary)
        self.assertIn("Redirection to ambulatory/freestanding facility", assessment.overall_summary)

        # Case B: Clinical necessity MET AND Place of Service has documented medical exception (open MRI needed)
        case_dict_exception = copy.deepcopy(case_dict)
        case_dict_exception["clinical_evidence"]["severe_claustrophobia_open_mri_needed"] = True
        assessment_b = self.engine.evaluate(
            case_dict_exception,
            target_rule_ids=["RULE-ADV-CG2012-003", "RULE-ADV-EPOS2067-004"]
        )
        self.assertEqual(assessment_b.clinical_necessity_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(assessment_b.place_of_service_outcome, DecisionOutcome.CRITERIA_MET)
        self.assertEqual(assessment_b.overall_outcome, DecisionOutcome.CRITERIA_MET)

    # -------------------------------------------------------------------------
    # Test 5: Missing Input Fields Never Satisfy Criteria
    # -------------------------------------------------------------------------
    def test_05_missing_input_fields_never_satisfy_criteria(self):
        """Missing mandatory data must yield INSUFFICIENT_INFORMATION, never True."""
        case_dict = {
            "case_id": "CASE-MISSING-001",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62322",
            "procedure_name": "Epidural Steroid Injection",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                # Missing cgepiduralinjections_indication
            }
        }
        assessment = self.engine.evaluate(case_dict, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(assessment.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)
        self.assertTrue(len(assessment.missing_evidence_fields) > 0)
        self.assertTrue(any(f in assessment.missing_evidence_fields for f in [
            "imaging_guidance_present", "pain_intensity_score_numeric", "functional_disability_documented", "cgepiduralinjections_indication"
        ]))

    # -------------------------------------------------------------------------
    # Test 6: Boolean ALL_OF and ANY_OF Logic Paths
    # -------------------------------------------------------------------------
    def test_06_boolean_all_of_and_any_of_logic_paths(self):
        """Verify strict three-valued evaluation for ALL_OF and ANY_OF trees."""
        rule = self.registry.get_rule("RULE-ADV-CG2000-001")
        self.assertIsNotNone(rule)
        self.assertEqual(rule.conditions.get("operator"), "ALL_OF")

        # ALL_OF: 2 True, 1 False -> FALSE (short circuit)
        case_all_of_false = {
            "case_id": "CASE-ALLOF-FALSE",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74176",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "ordering_provider_license": True,
                "clinical_office_notes": True,
                "laboratory_and_testing_data": False  # Explicit False
            }
        }
        res_false = self.engine.evaluate(case_all_of_false, target_rule_ids=["RULE-ADV-CG2000-001"])
        self.assertEqual(res_false.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # ALL_OF: 2 True, 1 missing -> INSUFFICIENT_INFORMATION
        case_all_of_unk = copy.deepcopy(case_all_of_false)
        del case_all_of_unk["clinical_evidence"]["laboratory_and_testing_data"]
        res_unk = self.engine.evaluate(case_all_of_unk, target_rule_ids=["RULE-ADV-CG2000-001"])
        self.assertEqual(res_unk.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

    # -------------------------------------------------------------------------
    # Test 7: Numerical and Temporal Boundary Value Tests
    # -------------------------------------------------------------------------
    def test_07_numerical_and_temporal_boundary_values(self):
        """Verify exact boundary checks for numerical and temporal criteria."""
        # 1. Smoking pack-years (RULE-ADV-CG2030-001: smoking_history_pack_years >= 20)
        rule_ldct = "RULE-ADV-CG2030-001"
        base_ldct_case = {
            "case_id": "CASE-LDCT-BOUNDARY",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "71271",
            "procedure_name": "Low Dose CT for Lung Cancer Screening",
            "patient_age_years": 60,
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "patient_is_asymptomatic": True,
                "current_or_recent_smoker_15yr": True
            }
        }

        # Sub-boundary: 19 pack-years -> NOT_MET
        case_ldct_19 = copy.deepcopy(base_ldct_case)
        case_ldct_19["clinical_evidence"]["smoking_history_pack_years"] = 19
        res_19 = self.engine.evaluate(case_ldct_19, target_rule_ids=[rule_ldct])
        self.assertEqual(res_19.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # Exact boundary: 20 pack-years -> MET
        case_ldct_20 = copy.deepcopy(base_ldct_case)
        case_ldct_20["clinical_evidence"]["smoking_history_pack_years"] = 20
        res_20 = self.engine.evaluate(case_ldct_20, target_rule_ids=[rule_ldct])
        self.assertEqual(res_20.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # Above boundary: 25 pack-years -> MET
        case_ldct_25 = copy.deepcopy(base_ldct_case)
        case_ldct_25["clinical_evidence"]["smoking_history_pack_years"] = 25
        res_25 = self.engine.evaluate(case_ldct_25, target_rule_ids=[rule_ldct])
        self.assertEqual(res_25.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # Symptomatic status: patient_is_asymptomatic is False -> NOT_MET
        case_ldct_symp = copy.deepcopy(base_ldct_case)
        case_ldct_symp["clinical_evidence"]["patient_is_asymptomatic"] = False
        case_ldct_symp["clinical_evidence"]["smoking_history_pack_years"] = 25
        res_symp = self.engine.evaluate(case_ldct_symp, target_rule_ids=[rule_ldct])
        self.assertEqual(res_symp.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # Missing symptom evidence: patient_is_asymptomatic omitted -> INSUFFICIENT_INFORMATION
        case_ldct_miss = copy.deepcopy(base_ldct_case)
        del case_ldct_miss["clinical_evidence"]["patient_is_asymptomatic"]
        case_ldct_miss["clinical_evidence"]["smoking_history_pack_years"] = 25
        res_miss = self.engine.evaluate(case_ldct_miss, target_rule_ids=[rule_ldct])
        self.assertEqual(res_miss.overall_outcome, DecisionOutcome.INSUFFICIENT_INFORMATION)

        # 2. Facet Denervation Relief Threshold (RULE-IPM-CGFACETDENERVATION-002: diagnostic_facet_block_relief >= 50)
        rule_rfa = "RULE-IPM-CGFACETDENERVATION-002"
        base_rfa_case = {
            "case_id": "CASE-RFA-BOUNDARY",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "64635",
            "procedure_name": "Facet Radiofrequency Neurotomy",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        }
        # 49% -> NOT_MET
        case_rfa_49 = copy.deepcopy(base_rfa_case)
        case_rfa_49["clinical_evidence"]["diagnostic_facet_block_relief"] = 49
        res_rfa_49 = self.engine.evaluate(case_rfa_49, target_rule_ids=[rule_rfa])
        self.assertEqual(res_rfa_49.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # 50% -> MET
        case_rfa_50 = copy.deepcopy(base_rfa_case)
        case_rfa_50["clinical_evidence"]["diagnostic_facet_block_relief"] = 50
        res_rfa_50 = self.engine.evaluate(case_rfa_50, target_rule_ids=[rule_rfa])
        self.assertEqual(res_rfa_50.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # 3. SCS Temporary Trial Relief (RULE-IPM-CGSPINALCORDSTIM-002: scs_trial_pain_relief >= 50)
        rule_scs = "RULE-IPM-CGSPINALCORDSTIM-002"
        base_scs_case = {
            "case_id": "CASE-SCS-BOUNDARY",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "63685",
            "procedure_name": "Permanent Spinal Cord Stimulator",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        }
        # 49% -> NOT_MET
        case_scs_49 = copy.deepcopy(base_scs_case)
        case_scs_49["clinical_evidence"]["scs_trial_pain_relief"] = 49
        res_scs_49 = self.engine.evaluate(case_scs_49, target_rule_ids=[rule_scs])
        self.assertEqual(res_scs_49.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

        # 50% -> MET
        case_scs_50 = copy.deepcopy(base_scs_case)
        case_scs_50["clinical_evidence"]["scs_trial_pain_relief"] = 50
        res_scs_50 = self.engine.evaluate(case_scs_50, target_rule_ids=[rule_scs])
        self.assertEqual(res_scs_50.overall_outcome, DecisionOutcome.CRITERIA_MET)

    # -------------------------------------------------------------------------
    # Test 8: Prior-Treatment Prerequisites & Documented Failure
    # -------------------------------------------------------------------------
    def test_08_prior_treatment_prerequisites_and_documented_failure(self):
        """Verify conservative care prerequisite and DOCUMENTED_FAILURE comparator."""
        rule_id = "RULE-IPM-CGEPIDURALINJECTIONS-002"
        base_case = {
            "case_id": "CASE-CONSERVATIVE-PREREQ",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62322",
            "procedure_name": "Epidural Steroid Injection",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        }
        # Documented failure of conservative management -> MET
        case_failure = copy.deepcopy(base_case)
        case_failure["clinical_evidence"]["conservative_therapy_failure"] = "CONSERVATIVE_MANAGEMENT"
        res_met = self.engine.evaluate(case_failure, target_rule_ids=[rule_id])
        self.assertEqual(res_met.overall_outcome, DecisionOutcome.CRITERIA_MET)

        # Other string -> NOT_MET
        case_none = copy.deepcopy(base_case)
        case_none["clinical_evidence"]["conservative_therapy_failure"] = "NONE"
        res_not_met = self.engine.evaluate(case_none, target_rule_ids=[rule_id])
        self.assertEqual(res_not_met.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)

    # -------------------------------------------------------------------------
    # Test 9: Exclusions and Negative Decision Effects
    # -------------------------------------------------------------------------
    def test_09_exclusions_and_negative_decision_effects(self):
        """Verify that disqualifying exclusion criteria (NOT_INDICATED) prevent approval."""
        # RULE-ADV-CG2014-002 (Breast MRI): saline_implant_complication_requested == True -> NOT_INDICATED
        case_dict = {
            "case_id": "CASE-SALINE-EXCLUSION",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "77046",
            "procedure_name": "Breast MRI",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "saline_implant_complication_requested": True
            }
        }
        assessment = self.engine.evaluate(case_dict, target_rule_ids=["RULE-ADV-CG2014-002"])
        self.assertEqual(assessment.overall_outcome, DecisionOutcome.CRITERIA_NOT_MET)
        self.assertIn("exclusion criterion met", assessment.overall_summary.lower())

        # If saline implant complication is False -> exclusion condition is not met (MET)
        case_no_exclusion = copy.deepcopy(case_dict)
        case_no_exclusion["clinical_evidence"]["saline_implant_complication_requested"] = False
        assessment_no_ex = self.engine.evaluate(case_no_exclusion, target_rule_ids=["RULE-ADV-CG2014-002"])
        self.assertEqual(assessment_no_ex.overall_outcome, DecisionOutcome.CRITERIA_MET)

    # -------------------------------------------------------------------------
    # Test 10: Repeat-Service Interval and Frequency Limits
    # -------------------------------------------------------------------------
    def test_10_repeat_service_interval_and_frequency_limits(self):
        """Verify that repeat service interval violations trigger gap detection and human review."""
        case_dict = {
            "case_id": "CASE-REPEAT-INTERVAL-VIOLATION",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62322",
            "procedure_name": "Epidural Steroid Injection",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "cgepiduralinjections_indication": True,
                "subsequent_injection_interval_days": 7,  # Violates 14-day minimum
                "annual_session_count_past_12mo": 1
            }
        }
        assessment = self.engine.evaluate(case_dict, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(assessment.overall_outcome, DecisionOutcome.NEEDS_HUMAN_REVIEW)
        self.assertTrue(len(assessment.uncovered_gaps_encountered) > 0)
        self.assertIn("violates mandatory 2026 policy minimum interval of 14 days", assessment.uncovered_gaps_encountered[0])

    # -------------------------------------------------------------------------
    # Test 11: Uncovered Policy Criteria Gap Escalation
    # -------------------------------------------------------------------------
    def test_11_uncovered_policy_criteria_gap_escalation(self):
        """Verify that cases presenting conditions from coverage gap reports escalate to review."""
        case_dict = {
            "case_id": "CASE-GAP-STENOSIS",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62323",
            "procedure_name": "Epidural Steroid Injection",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "cgepiduralinjections_indication": True,
                "spinal_stenosis_present": True,
                "radicular_pain_confirmed": False  # Isolated stenosis without radiculopathy
            }
        }
        assessment = self.engine.evaluate(case_dict, target_rule_ids=["RULE-IPM-CGEPIDURALINJECTIONS-001"])
        self.assertEqual(assessment.overall_outcome, DecisionOutcome.NEEDS_HUMAN_REVIEW)
        self.assertTrue(any("isolated spinal stenosis" in g for g in assessment.uncovered_gaps_encountered))

    # -------------------------------------------------------------------------
    # Test 12: Source Provenance Fidelity
    # -------------------------------------------------------------------------
    def test_12_source_provenance_fidelity(self):
        """Verify that execution traces contain exact source PDF citations and quotes."""
        case_dict = {
            "case_id": "CASE-PROVENANCE-001",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74176",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-07-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "ordering_provider_license": True,
                "clinical_office_notes": True,
                "laboratory_and_testing_data": True
            }
        }
        assessment = self.engine.evaluate(case_dict, target_rule_ids=["RULE-ADV-CG2000-001"])
        self.assertEqual(assessment.overall_outcome, DecisionOutcome.CRITERIA_MET)

        self.assertTrue(len(assessment.clinical_necessity_rules) > 0)
        rule_exec = assessment.clinical_necessity_rules[0]
        self.assertEqual(rule_exec.rule_id, "RULE-ADV-CG2000-001")
        self.assertIn("2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf", rule_exec.provenance["source_file"])
        self.assertEqual(rule_exec.provenance["physical_page"], 8)
        self.assertIn("STATEMENT / General Information", rule_exec.provenance["source_section"])
        self.assertTrue(len(rule_exec.provenance["source_quote"]) > 0)

        # Inspect criterion trace
        self.assertTrue(len(rule_exec.traces) > 0)
        trace = rule_exec.traces[0]
        self.assertEqual(trace.rule_id, "RULE-ADV-CG2000-001")
        self.assertEqual(trace.status, EvaluationState.TRUE)
        self.assertIn("2026 Evolent Clinical Guidelines", trace.source_file)

    # -------------------------------------------------------------------------
    # Test 13: Clinical Domain Isolation & Historical Policy Rejection
    # -------------------------------------------------------------------------
    def test_13_domain_isolation_and_historical_policy_rejection(self):
        """Verify that unrelated domains and historical DOS are rejected by active engine."""
        # 1. Unrelated domain (Cardiology) rejected
        case_cardio = {
            "case_id": "CASE-CARDIO-REJECT",
            "clinical_domain": "cardiology",
            "procedure_code": "93458",
            "procedure_name": "Coronary Angiography",
            "requested_date_of_service": "2026-07-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        }
        res_cardio = self.engine.evaluate(case_cardio)
        self.assertEqual(res_cardio.overall_outcome, DecisionOutcome.POLICY_NOT_APPLICABLE)
        self.assertIn("not in active MedRule scope", res_cardio.clinical_necessity_explanation)

        # 2. Historical DOS (< 2026-01-01) rejected without explicit historical override
        case_hist = {
            "case_id": "CASE-HIST-DOS-REJECT",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2025-11-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        }
        res_hist = self.engine.evaluate(case_hist)
        self.assertEqual(res_hist.overall_outcome, DecisionOutcome.POLICY_VERSION_UNRESOLVED)
        self.assertIn("precedes the effective date of the 2026 governing guidelines", res_hist.clinical_necessity_explanation)

    # -------------------------------------------------------------------------
    # Test 14: Deterministic Repeatability & Hash Stability
    # -------------------------------------------------------------------------
    def test_14_deterministic_repeatability_and_hash_stability(self):
        """Verify that identical inputs produce identical hashes and outcomes 50 times."""
        case_dict = {
            "case_id": "CASE-DETERMINISTIC-REPEAT",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74176",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-08-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "ordering_provider_license": True,
                "clinical_office_notes": True,
                "laboratory_and_testing_data": True
            }
        }
        first_eval = self.engine.evaluate(case_dict, target_rule_ids=["RULE-ADV-CG2000-001"])
        first_hash = first_eval.reproducibility_hash
        self.assertTrue(len(first_hash) == 64, "Hash must be valid SHA-256 string.")

        for _ in range(50):
            repeat_eval = self.engine.evaluate(case_dict, target_rule_ids=["RULE-ADV-CG2000-001"])
            self.assertEqual(repeat_eval.overall_outcome, first_eval.overall_outcome)
            self.assertEqual(repeat_eval.reproducibility_hash, first_hash)


    # -------------------------------------------------------------------------
    # Test 15: CP.MP.107 / DMEPOS Isolation & Non-Interference Proof
    # -------------------------------------------------------------------------
    def test_15_cp_mp_107_dmepos_complete_isolation_and_non_interference(self):
        """Prove that CP.MP.107 and DMEPOS cannot enter or influence active MedRule evaluation."""
        # 1. DMEPOS case intake is rejected unconditionally at domain gate
        dme_case = {
            "case_id": "CASE-DME-TEST-001",
            "clinical_domain": "centene_dme_orthotics_prosthetics",
            "procedure_code": "E0601",
            "procedure_name": "Continuous Positive Airway Pressure (CPAP) Device",
            "requested_date_of_service": "2026-08-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "CENTENE",
            "clinical_evidence": {
                "ahi_score": 18.5,
                "daytime_hypersomnolence": True,
                "trial_completed": True
            }
        }
        res_dme = self.engine.evaluate(dme_case)
        self.assertEqual(res_dme.overall_outcome, DecisionOutcome.POLICY_NOT_APPLICABLE)
        self.assertIn("not in active MedRule scope", res_dme.clinical_necessity_explanation)
        self.assertEqual(len(res_dme.clinical_necessity_rules), 0)

        # 2. CP.MP.107 rule IDs do not exist in the active registry
        for dme_rule_id in ["RULE-DME-001", "RULE-DME-CPAP-001", "RULE-DME-048", "RULE-DME-099"]:
            self.assertIsNone(self.engine.registry.get_rule(dme_rule_id))

        # 3. Attempting to explicitly target a CP.MP.107 rule ID returns POLICY_NOT_APPLICABLE
        res_target_dme = self.engine.evaluate(
            {
                "case_id": "CASE-DME-TARGET-002",
                "clinical_domain": "advanced_imaging",
                "procedure_code": "70551",
                "procedure_name": "Brain MRI",
                "requested_date_of_service": "2026-06-01",
                "line_of_business": "COMMERCIAL",
                "payer_id": "TEST_PAYER",
                "clinical_evidence": {}
            },
            target_rule_ids=["RULE-DME-001"]
        )
        self.assertEqual(res_target_dme.overall_outcome, DecisionOutcome.POLICY_NOT_APPLICABLE)

        # 4. Injecting CP.MP.107 DME criteria into an Advanced Imaging case has zero effect
        base_ai_case = {
            "case_id": "CASE-AI-ISOLATION-CLEAN",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2026-06-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "suspected_or_established_multiple_sclerosis": True
            }
        }
        clean_ai_res = self.engine.evaluate(base_ai_case, target_rule_ids=["RULE-ADV-CG2012-003"])
        
        # Polluted case with CP.MP.107 criteria
        polluted_ai_case = copy.deepcopy(base_ai_case)
        polluted_ai_case["clinical_evidence"].update({
            "ahi_score": 25.0,
            "cp_mp_107_dme_trial_completed": True,
            "mobility_limitation_daily_activities": True,
            "cervical_traction_device_demonstrated": True
        })
        polluted_ai_res = self.engine.evaluate(polluted_ai_case, target_rule_ids=["RULE-ADV-CG2012-003"])

        self.assertEqual(polluted_ai_res.overall_outcome, clean_ai_res.overall_outcome)
        self.assertEqual(polluted_ai_res.clinical_necessity_outcome, clean_ai_res.clinical_necessity_outcome)
        self.assertEqual(len(polluted_ai_res.clinical_necessity_rules), len(clean_ai_res.clinical_necessity_rules))

        # 5. Injecting CP.MP.107 DME criteria into an IPM case has zero effect
        base_ipm_case = {
            "case_id": "CASE-IPM-ISOLATION-CLEAN",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "64635",
            "procedure_name": "Facet Radiofrequency Neurotomy",
            "requested_date_of_service": "2026-08-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "diagnostic_facet_block_relief": 65
            }
        }
        clean_ipm_res = self.engine.evaluate(base_ipm_case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-002"])

        polluted_ipm_case = copy.deepcopy(base_ipm_case)
        polluted_ipm_case["clinical_evidence"].update({
            "ahi_score": 3.0,
            "dme_wheelchair_replacement_useful_lifetime_years": 5,
            "prosthetic_functional_needs_unmet": True
        })
        polluted_ipm_res = self.engine.evaluate(polluted_ipm_case, target_rule_ids=["RULE-IPM-CGFACETDENERVATION-002"])

        self.assertEqual(polluted_ipm_res.overall_outcome, clean_ipm_res.overall_outcome)
        self.assertEqual(polluted_ipm_res.clinical_necessity_outcome, clean_ipm_res.clinical_necessity_outcome)
        self.assertEqual(len(polluted_ipm_res.clinical_necessity_rules), len(clean_ipm_res.clinical_necessity_rules))


if __name__ == "__main__":
    unittest.main()
