import json
from pathlib import Path

ROOT = Path("d:/PreAuth")
with open(ROOT / "scratch" / "detailed_50_rules_data.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

ai_pv = [r for r in rules if r["domain"] == "advanced_imaging" and r["audit_status"] == "PARTIALLY_VERIFIED"]

print(f"AI PV count: {len(ai_pv)}")

with open(ROOT / "scratch" / "ai_pv_summary.txt", "w", encoding="utf-8") as out:
    for i, r in enumerate(ai_pv, 1):
        out.write(f"[{i:02d}/35] Rule ID: {r['rule_id']}\n")
        out.write(f"    Page: {r['physical_page']} | Section: {r['source_section']}\n")
        out.write(f"    Issue: {r['issue_description']}\n")
        out.write(f"    Conditions: {json.dumps(r['conditions'])}\n")
        out.write(f"    Quote snippet: {r['rule_quote'][:100]}...\n")
        out.write("-" * 70 + "\n")

print("Written scratch/ai_pv_summary.txt")
