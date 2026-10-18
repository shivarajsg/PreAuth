import fitz
import json
import jsonschema
from pathlib import Path
from build_rules_data_referenced import get_referenced_rules

base_dir = Path(r"c:\Users\KumarShiva\Downloads\PreAuth")
rules = get_referenced_rules()
print(f"Total referenced rules loaded: {len(rules)}")

schema_path = base_dir / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"
with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

for r in rules:
    jsonschema.validate(instance=r, schema=schema)
print("ALL 41 referenced rules passed JSON schema validation!")

fail_count = 0
pdf_cache = {}
for r in rules:
    sf = str(base_dir / r["source_file"])
    if sf not in pdf_cache:
        pdf_cache[sf] = fitz.open(sf)
    doc = pdf_cache[sf]
    p_num = r["source_page"]["physical_page"]
    p_text = " ".join(doc[p_num - 1].get_text().split())
    q_norm = " ".join(r["source_quote"].split())
    if q_norm not in p_text:
        print(f"QUOTE FAIL {r['rule_id']} in {r['source_file'].split('/')[-1]} P{p_num}: {q_norm[:70]}...")
        fail_count += 1

for doc in pdf_cache.values():
    doc.close()

print(f"Referenced Quote verification result: {len(rules) - fail_count}/{len(rules)} passed!")
