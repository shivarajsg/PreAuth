import sys, os
sys.path.insert(0, os.path.abspath('.'))
import csv, json
from pathlib import Path
from medrule_engine.decision_tree import DecisionTreeEngine, DecisionOutcome
from medrule_engine.rule_registry import RuleRegistry
from medrule_engine.case_validator import CaseValidator

sys.stdout.reconfigure(encoding='utf-8')

engine = DecisionTreeEngine()

scenarios = [
    {
        "scenario_id": "SCEN-01-AI-CLINICAL",
        "description": "Advanced Imaging request routing to AI clinical policy (POL-ADV-2026-V2)",
        "case": {
            "case_id": "CASE-SCEN-01",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "modality": "MRI",
            "place_of_service": "OFFICE",
            "clinical_evidence": {
                "suspected_or_established_multiple_sclerosis": True,
                "place_of_service_code": "POS_11"
            }
        },
        "target_rules": ["RULE-ADV-CG2012-003"],
        "expected_policies": "POL-ADV-2026-V2",
        "expected_result": "CRITERIA_MET",
        "source_evidence": "2026 Evolent Advanced Imaging v2 (p. 232, CPT 70551)"
    },
    {
        "scenario_id": "SCEN-02-AI-POS",
        "description": "Imaging request requiring Radiology Place of Service policy (POL-ADV-EPOS2067-2026)",
        "case": {
            "case_id": "CASE-SCEN-02",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "72148",
            "procedure_name": "Lumbar Spine MRI",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "modality": "MRI",
            "place_of_service": "AMBULATORY_SURGICAL_CENTER",
            "clinical_evidence": {
                "place_of_service_code": "POS_24"
            }
        },
        "target_rules": ["RULE-ADV-EPOS2067-001"],
        "expected_policies": "POL-ADV-EPOS2067-2026",
        "expected_result": "CRITERIA_MET",
        "source_evidence": "EPOS 2067 for Place of Service - Radiology 2026 (p. 3)"
    },
    {
        "scenario_id": "SCEN-03-IPM-CLINICAL",
        "description": "IPM request routing to IPM clinical policy (POL-IPM-2026)",
        "case": {
            "case_id": "CASE-SCEN-03",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "64635",
            "procedure_name": "Facet Radiofrequency Neurotomy",
            "requested_date_of_service": "2026-08-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "diagnostic_facet_block_relief": 60
            }
        },
        "target_rules": ["RULE-IPM-CGFACETDENERVATION-002"],
        "expected_policies": "POL-IPM-2026",
        "expected_result": "CRITERIA_MET",
        "source_evidence": "2026 Evolent IPM Guidelines (p. 25, CPT 64635)"
    },
    {
        "scenario_id": "SCEN-04-IPM-POS",
        "description": "IPM request requiring IPM Place of Service policy (POL-IPM-EPOS1755-2026)",
        "case": {
            "case_id": "CASE-SCEN-04",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62322",
            "procedure_name": "Epidural Steroid Injection",
            "requested_date_of_service": "2026-08-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "place_of_service": "OFFICE",
            "clinical_evidence": {
                "epos1755_indication": True,
                "place_of_service_code": "POS_11"
            }
        },
        "target_rules": ["RULE-IPM-EPOS1755-001"],
        "expected_policies": "POL-IPM-EPOS1755-2026",
        "expected_result": "CRITERIA_MET",
        "source_evidence": "EPOS 1755 for Place of Service - IPM 2026 (p. 3)"
    },
    {
        "scenario_id": "SCEN-05-OUT-OF-SCOPE-DOMAIN",
        "description": "Request outside the two supported active clinical domains",
        "case": {
            "case_id": "CASE-SCEN-05",
            "clinical_domain": "cardiology",
            "procedure_code": "93306",
            "procedure_name": "Transthoracic Echocardiogram",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        },
        "target_rules": None,
        "expected_policies": "NONE (Domain Rejected)",
        "expected_result": "POLICY_NOT_APPLICABLE",
        "source_evidence": "Scope boundary: Advanced Imaging & IPM only"
    },
    {
        "scenario_id": "SCEN-06-UNSUPPORTED-PROC-CODE",
        "description": "Request with an unsupported or unmapped procedure code",
        "case": {
            "case_id": "CASE-SCEN-06",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "INVALID_CODE_999",
            "procedure_name": "Unknown Diagnostic Study",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        },
        "target_rules": None,
        "expected_policies": "NONE (Malformed Code)",
        "expected_result": "POLICY_NOT_APPLICABLE",
        "source_evidence": "PolicyRouter procedure validation check"
    },
    {
        "scenario_id": "SCEN-07-MISSING-APPLICABILITY-LOB",
        "description": "Request with missing information needed to determine policy applicability (LOB 'OTHER')",
        "case": {
            "case_id": "CASE-SCEN-07",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "OTHER",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        },
        "target_rules": None,
        "expected_policies": "POL-ADV-2026-V2 (Unresolved LOB)",
        "expected_result": "NEEDS_HUMAN_REVIEW",
        "source_evidence": "PolicyRouter LOB applicability guard (requires Commercial/MA/Medicaid)"
    },
    {
        "scenario_id": "SCEN-08-DATE-PRE-2026-BOUNDARY",
        "description": "Case with date that raises policy-version applicability question (DOS in 2025)",
        "case": {
            "case_id": "CASE-SCEN-08",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2025-05-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        },
        "target_rules": None,
        "expected_policies": "POL-ADV-2026-V2 (Boundary Rejection)",
        "expected_result": "POLICY_VERSION_UNRESOLVED",
        "source_evidence": "2026 Evolent Guidelines effective boundary: 2026-01-01"
    },
    {
        "scenario_id": "SCEN-09-HISTORICAL-REJECTION",
        "description": "Case where historical policy must not silently replace current policy",
        "case": {
            "case_id": "CASE-SCEN-09",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62322",
            "procedure_name": "Epidural Steroid Injection",
            "requested_date_of_service": "2025-11-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        },
        "target_rules": None,
        "expected_policies": "POL-IPM-2026 (Historical Fallback Prevented)",
        "expected_result": "POLICY_VERSION_UNRESOLVED",
        "source_evidence": "PolicyRouter version status filter (excludes historical_superseded)"
    },
    {
        "scenario_id": "SCEN-10-GOVERNANCE-BLOCKED-RULE",
        "description": "Case touching one of the seven governance-blocked rules (RULE-ADV-PREAMBLE-001)",
        "case": {
            "case_id": "CASE-SCEN-10",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {}
        },
        "target_rules": ["RULE-ADV-PREAMBLE-001"],
        "expected_policies": "POL-ADV-2026-V2",
        "expected_result": "NEEDS_HUMAN_REVIEW",
        "source_evidence": "Strict Governance Gate: GOVERNANCE_BLOCKED_RULE_IDS"
    },
    {
        "scenario_id": "SCEN-11-UNCODIFIED-COVERAGE-GAP",
        "description": "Case touching a known uncodified coverage gap (Spinal Stenosis without radiculopathy)",
        "case": {
            "case_id": "CASE-SCEN-11",
            "clinical_domain": "interventional_pain_management",
            "procedure_code": "62322",
            "procedure_name": "Epidural Steroid Injection",
            "requested_date_of_service": "2026-08-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "clinical_evidence": {
                "spinal_stenosis_present": True,
                "radicular_pain_confirmed": False
            }
        },
        "target_rules": None,
        "expected_policies": "POL-IPM-2026",
        "expected_result": "NEEDS_HUMAN_REVIEW",
        "source_evidence": "IPM CG 1750 Coverage Gap Detector"
    },
    {
        "scenario_id": "SCEN-12-CN-MET-POS-NOT-MET",
        "description": "Case where Clinical Necessity is met but Place of Service criteria are not met",
        "case": {
            "case_id": "CASE-SCEN-12",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "70551",
            "procedure_name": "Brain MRI",
            "requested_date_of_service": "2026-05-01",
            "line_of_business": "COMMERCIAL",
            "payer_id": "TEST_PAYER",
            "modality": "MRI",
            "place_of_service": "OUTPATIENT_HOSPITAL",
            "clinical_evidence": {
                "suspected_or_established_multiple_sclerosis": True,
                "place_of_service_code": "POS_22",
                "severe_claustrophobia_open_mri_needed": False,
                "bariatric_weight_exceeds_freestanding_scanner": False,
                "complex_specialized_protocol_needed": False
            }
        },
        "target_rules": ["RULE-ADV-CG2012-003", "RULE-ADV-EPOS2067-001", "RULE-ADV-EPOS2067-004"],
        "expected_policies": "POL-ADV-2026-V2, POL-ADV-EPOS2067-2026",
        "expected_result": "CRITERIA_NOT_MET",
        "source_evidence": "Dual Track Architecture: CN=MET, POS=NOT_MET -> Redirection to POS 11/24"
    }
]

rows = []
for sc in scenarios:
    case_dict = sc["case"]
    target_rules = sc["target_rules"]
    assessment = engine.evaluate(case_dict, target_rule_ids=target_rules)
    
    actual_res = assessment.overall_outcome.value if hasattr(assessment.overall_outcome, "value") else str(assessment.overall_outcome)
    
    # Identify actual selected policies from executed rules
    all_rules_evaluated = assessment.clinical_necessity_rules + assessment.place_of_service_rules
    selected_pols = set()
    for rx in all_rules_evaluated:
        pol_title = rx.provenance.get("policy_title", "")
        if "Advanced Imaging" in pol_title:
            selected_pols.add("POL-ADV-2026-V2")
        elif "2067" in pol_title:
            selected_pols.add("POL-ADV-EPOS2067-2026")
        elif "Interventional Pain" in pol_title:
            selected_pols.add("POL-IPM-2026")
        elif "1755" in pol_title:
            selected_pols.add("POL-IPM-EPOS1755-2026")
    
    if not selected_pols:
        actual_pols_str = "NONE (" + actual_res + ")"
    else:
        actual_pols_str = ", ".join(sorted(selected_pols))
        
    passed = (actual_res == sc["expected_result"])
    
    # Check unresolved applicability assumptions
    notes = []
    if sc["scenario_id"] == "SCEN-07-MISSING-APPLICABILITY-LOB":
        notes.append("LOB 'OTHER' requires manual payer product verification")
    if "SCEN-08" in sc["scenario_id"] or "SCEN-09" in sc["scenario_id"]:
        notes.append("Historical policy retrieval requires explicit override context")
    if sc["scenario_id"] == "SCEN-11-UNCODIFIED-COVERAGE-GAP":
        notes.append("Canal diameter and claudication thresholds uncodified; medical director review mandatory")
    if sc["scenario_id"] == "SCEN-12-CN-MET-POS-NOT-MET":
        notes.append("Site-of-care redirection notice issued; clinical necessity preserved as MET")
    
    unresolved_notes = "; ".join(notes) if notes else "None (fully resolved by governing policy)"
    
    input_summary = f"Domain={case_dict.get('clinical_domain')}, Code={case_dict.get('procedure_code')}, DOS={case_dict.get('requested_date_of_service')}, LOB={case_dict.get('line_of_business')}"

    rows.append({
        "scenario_id": sc["scenario_id"],
        "description": sc["description"],
        "input_fields": input_summary,
        "expected_policies": sc["expected_policies"],
        "actual_selected_policies": actual_pols_str,
        "expected_result": sc["expected_result"],
        "actual_result": actual_res,
        "source_evidence": sc["source_evidence"],
        "test_status": "PASS" if passed else "FAIL",
        "unresolved_applicability_assumptions": unresolved_notes
    })
    print(f"[{'PASS' if passed else 'FAIL'}] {sc['scenario_id']}: expected {sc['expected_result']}, got {actual_res}")

fieldnames = [
    "scenario_id", "description", "input_fields", "expected_policies",
    "actual_selected_policies", "expected_result", "actual_result",
    "source_evidence", "test_status", "unresolved_applicability_assumptions"
]

out_path = Path("rulebook_collection/manifests/policy_routing_test_matrix.csv")
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\nWrote {len(rows)} test scenario records to {out_path}")
