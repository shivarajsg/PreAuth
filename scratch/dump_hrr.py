import json
from pathlib import Path

ROOT = Path("d:/PreAuth")
with open(ROOT / "scratch" / "detailed_50_rules_data.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

hrr = [r for r in rules if r["audit_status"] == "HUMAN_REVIEW_REQUIRED"]

with open(ROOT / "scratch" / "hrr_details.txt", "w", encoding="utf-8") as out:
    for r in hrr:
        out.write("=" * 80 + "\n")
        out.write(f"Rule ID: {r['rule_id']}\n")
        out.write(f"Domain: {r['domain']} | Page: {r['physical_page']} | Policy: {r['policy_name']}\n")
        out.write(f"Section: {r['source_section']}\n")
        out.write(f"Issue: {r['issue_description']}\n")
        out.write(f"Source Quote: {r['rule_quote']}\n")
        out.write(f"Conditions: {json.dumps(r['conditions'], indent=2)}\n")
        out.write(f"Decision Effect: {r['decision_effect']}\n")
        out.write("\n--- Relevant PDF Text Excerpt ---\n")
        lines = [line.strip() for line in r['full_page_text'].split("\n") if line.strip()]
        out.write("\n".join(lines[:45]) + "\n\n")

print("Written scratch/hrr_details.txt")
