import json
from pathlib import Path
import pymupdf

ROOT = Path("d:/PreAuth")
with open(ROOT / "scratch" / "unresolved_rules_extracted.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

pv_rules = [r for r in rules if r["audit_status"] == "PARTIALLY_VERIFIED"]

print(f"Total PV rules: {len(pv_rules)}")
for i, r in enumerate(pv_rules, 1):
    print(f"[{i}] {r['rule_id']} (Domain: {r['domain']}, Page: {r['page_num']})")
    print(f"    Section: {r['source_section']}")
    print(f"    Issue: {r['issue_description']}")
    print(f"    Conditions: {r['conditions']}")
    print(f"    Source Quote: {r['source_quote'][:150]}...")
    print("-" * 60)
