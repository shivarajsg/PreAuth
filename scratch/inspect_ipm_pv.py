import json
from pathlib import Path

ROOT = Path("d:/PreAuth")
with open(ROOT / "scratch" / "detailed_50_rules_data.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

ipm_pv = [r for r in rules if r["domain"] == "interventional_pain_management" and r["audit_status"] == "PARTIALLY_VERIFIED"]

print(f"IPM PV count: {len(ipm_pv)}")
for r in ipm_pv:
    print("=" * 60)
    print(f"ID: {r['rule_id']} | Page: {r['physical_page']} | Section: {r['source_section']}")
    print(f"Issue: {r['issue_description']}")
    print(f"Conditions: {json.dumps(r['conditions'])}")
    print(f"Quote: {r['rule_quote'][:120]}...")
