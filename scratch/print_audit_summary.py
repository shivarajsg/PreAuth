import json
with open('scratch/audit_summary_initial.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for item in data:
    ids_str = ', '.join(item['rule_ids'])
    print(f"{item['guideline_id']:10s} | {item['pages']:22s} | Rules: {item['rules_count']:2d} | IDs: {ids_str}")
