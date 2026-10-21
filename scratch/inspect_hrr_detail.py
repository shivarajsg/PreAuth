import json
from pathlib import Path

ROOT = Path("d:/PreAuth")
with open(ROOT / "scratch" / "detailed_50_rules_data.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

hrr = [r for r in rules if r["audit_status"] == "HUMAN_REVIEW_REQUIRED"]

for r in hrr:
    print("=" * 80)
    print(f"Rule ID: {r['rule_id']}")
    print(f"Domain: {r['domain']} | Page: {r['physical_page']} | Policy: {r['policy_name']}")
    print(f"Section: {r['source_section']}")
    print(f"Issue: {r['issue_description']}")
    print(f"Source Quote: {r['rule_quote']}")
    print(f"Conditions: {json.dumps(r['conditions'], indent=2)}")
    print(f"Decision Effect: {r['decision_effect']}")
    print("\n--- Relevant PDF Text Excerpt ---")
    lines = [line.strip() for line in r['full_page_text'].split("\n") if line.strip()]
    print("\n".join(lines[:35]))
