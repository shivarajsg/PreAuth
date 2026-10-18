import glob
import json
import jsonschema

with open('rulebook_collection/schemas/medrule_rule_schema.json', encoding='utf-8') as f:
    schema = json.load(f)

total_rules = 0
errors = 0
status_counts = {"DRAFT": 0, "NEEDS_HUMAN_REVIEW": 0, "APPROVED": 0}

for path in sorted(glob.glob('rulebook_collection/domains/*/rules/draft_rules.json')):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
        rules = data if isinstance(data, list) else data.get('rules', [])
        dname = path.replace('\\', '/').split('/')[2]
        print(f"Domain {dname}: validating {len(rules)} rules...")
        for r in rules:
            total_rules += 1
            st = r.get("status") or r.get("extraction_status", "DRAFT")
            status_counts[st] = status_counts.get(st, 0) + 1
            try:
                jsonschema.validate(instance=r, schema=schema)
            except jsonschema.ValidationError as e:
                print(f"  Schema error in {r.get('rule_id')}: {e.message}")
                errors += 1

print(f"\nTotal rules validated: {total_rules}")
print(f"Total schema errors: {errors}")
print(f"Status distribution: {status_counts}")
