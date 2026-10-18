import json

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

for r in rules:
    if 'CG2017' in r['rule_id']:
        print(f"=== {r['rule_id']} ===")
        print(f"Section: {r['source_section']}")
        safe_q = r['source_quote'].encode('ascii', errors='replace').decode('ascii')
        print(f"Quote: {safe_q[:100]}")
        print(f"Rule Type: {r['rule_type']}")
        print(f"Decision Effect: {r['decision_effect']}")
        print(f"Conditions: {json.dumps(r['conditions'])[:150]}")
