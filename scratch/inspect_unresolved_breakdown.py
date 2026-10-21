import json
from pathlib import Path
from collections import Counter

ROOT = Path("d:/PreAuth")
with open(ROOT / "scratch" / "unresolved_rules_extracted.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

print(f"Total rules: {len(rules)}")
hrr = [r for r in rules if r["audit_status"] == "HUMAN_REVIEW_REQUIRED"]
pv = [r for r in rules if r["audit_status"] == "PARTIALLY_VERIFIED"]
print(f"HRR: {len(hrr)}, PV: {len(pv)}")

print("\n--- HRR Rules ---")
for r in hrr:
    print(f"ID: {r['rule_id']}, Domain: {r['domain']}, Page: {r['page_num']}")
    print(f"  Section: {r['source_section']}")
    print(f"  Issue: {r['issue_description']}")

print("\n--- PV Rules grouped by issue ---")
issue_counts = Counter(r['issue_description'] for r in pv)
for issue, count in issue_counts.items():
    print(f"Count: {count} | Issue: {issue}")
