import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

print(f'Total IPM rules: {len(rules)}')
for r in rules:
    print(f"{r['rule_id']} | {r['clinical_service_or_procedure']} | Page {r['source_page']['physical_page']} | {r['source_section']}")
    print(f"  Quote: {r['source_quote'][:120]}...")
    print(f"  Conditions Operator: {r['conditions']['operator']}")
    for c in r['conditions']['criteria']:
        print(f"    - {c.get('description')}")
    print()
