import fitz
import json
import jsonschema
from pathlib import Path
from build_rules_data_107 import get_cp_mp_107_rules

base_dir = Path(r"c:\Users\KumarShiva\Downloads\PreAuth")
rules = get_cp_mp_107_rules()
print(f"Total CP.MP.107 rules loaded: {len(rules)}")

schema_path = base_dir / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"
with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

for r in rules:
    jsonschema.validate(instance=r, schema=schema)
print("ALL 58 CP.MP.107 rules passed JSON schema validation!")

doc = fitz.open(str(base_dir / rules[0]["source_file"]))
fail_count = 0
for r in rules:
    p_num = r["source_page"]["physical_page"]
    p_text = " ".join(doc[p_num - 1].get_text().split())
    q_norm = " ".join(r["source_quote"].split())
    if q_norm not in p_text:
        print(f"QUOTE FAIL {r['rule_id']} P{p_num}: {q_norm[:70]}...")
        fail_count += 1

print(f"CP.MP.107 Quote verification result: {len(rules) - fail_count}/{len(rules)} passed!")
