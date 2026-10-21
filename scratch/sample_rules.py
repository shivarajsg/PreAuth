import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

for r in rules:
    proc = r.get('clinical_service_or_procedure', '')
    if any(k in proc.lower() for k in ['brain ct', 'brain mri', 'lumbar spine mri', 'cervical spine mri', 'chest ct']):
        print('='*70)
        print(f"{r['rule_id']} | {r['clinical_service_or_procedure']} | Page {r['source_page']}")
        print(f"Section: {r['source_section']}")
        print(f"Quote: {r['source_quote'][:150]}...")
        print(f"Conditions Operator: {r['conditions']['operator']}")
        for c in r['conditions']['criteria'][:3]:
            print(f"  - Condition: {c.get('description')}")
        print(f"Required Doc: {r.get('required_documentation')}")
        print(f"Exclusions: {r.get('exclusion_conditions')}")
