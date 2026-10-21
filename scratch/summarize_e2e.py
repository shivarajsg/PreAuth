import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/e2e_investigation_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for k, v in data.items():
    print(f"=== Case: {k} ===")
    print(f"  Extraction Status: {v.get('extraction_status')}")
    if v.get('extraction_status') != 'SUCCESS':
        print(f"  Diagnostics: {v.get('diagnostics')}")
        continue
    fields = v.get('extracted_fields', {})
    print(f"  Domain: {fields.get('clinical_domain')}, CPT: {fields.get('procedure_code')}, LOB: {fields.get('line_of_business')}")
    val = v.get('validation', {})
    print(f"  Validation: Valid={val.get('is_valid')}, Errors={val.get('errors')}")
    rout = v.get('routing', {})
    print(f"  Routing: Status={rout.get('status')}, ApplicableRules={rout.get('applicable_rule_count')}")
    assmt = v.get('assessment', {})
    print(f"  Whole-Domain Assessment: {assmt.get('status')}")
    pr = v.get('procedure_rule_evaluation', {})
    print(f"  Target Rule Evaluation ({pr.get('target_rule_id')}):")
    print(f"    Overall Outcome: {pr.get('overall_outcome')}")
    print(f"    Clinical Necessity Outcome: {pr.get('clinical_necessity_outcome')}")
    print(f"    Place of Service Outcome: {pr.get('place_of_service_outcome')}")
    print(f"    Criteria MET ({len(pr.get('criteria_met', []))}): {pr.get('criteria_met')}")
    print(f"    Criteria NOT_MET ({len(pr.get('criteria_not_met', []))}): {pr.get('criteria_not_met')}")
    print(f"    Criteria INSUFFICIENT_DATA ({len(pr.get('criteria_insufficient_data', []))}): {pr.get('criteria_insufficient_data')}")
    print(f"    Criteria NOT_APPLICABLE ({len(pr.get('criteria_not_applicable', []))}): {pr.get('criteria_not_applicable')}")
    print(f"    Provenance: {pr.get('provenance_source')} | Page {pr.get('provenance_page')}")
    print(f"    Quote: {pr.get('provenance_quote')}\n")
