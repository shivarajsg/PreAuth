import json
from pathlib import Path

ROOT = Path("d:/PreAuth")
with open(ROOT / "scratch" / "detailed_50_rules_data.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

pv = [r for r in rules if r["audit_status"] == "PARTIALLY_VERIFIED"]

with open(ROOT / "scratch" / "pv_details.txt", "w", encoding="utf-8") as out:
    for i, r in enumerate(pv, 1):
        out.write("=" * 80 + "\n")
        out.write(f"[{i}/43] Rule ID: {r['rule_id']}\n")
        out.write(f"Domain: {r['domain']} | Page: {r['physical_page']} | Policy: {r['policy_name']}\n")
        out.write(f"Section: {r['source_section']}\n")
        out.write(f"Issue: {r['issue_description']}\n")
        out.write(f"Source Quote: {r['rule_quote']}\n")
        out.write(f"Conditions: {json.dumps(r['conditions'], indent=2)}\n")
        out.write(f"Decision Effect: {r['decision_effect']}\n")
        out.write("\n--- Relevant PDF Text Excerpt ---\n")
        lines = [line.strip() for line in r['full_page_text'].split("\n") if line.strip()]
        out.write("\n".join(lines[:35]) + "\n\n")

print(f"Written {len(pv)} PV details to scratch/pv_details.txt")
