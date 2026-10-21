import json
from pathlib import Path

with open("scratch/batch1_first10_audit.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

with open("scratch/batch1_inspected.txt", "w", encoding="utf-8") as out:
    for i, r in enumerate(rules, 1):
        out.write("=" * 80 + "\n")
        out.write(f"[{i:02d}] Rule ID: {r['rule_id']}\n")
        out.write(f"     Domain: {r['domain']}\n")
        out.write(f"     Source File: {r['source_file']}\n")
        out.write(f"     Page: physical {r['physical_page']} (printed {r['printed_page']})\n")
        out.write(f"     Section: {r['source_section']}\n")
        out.write(f"     Quote: {r['source_quote']}\n")
        quote_in_page = r['source_quote'].strip() in r['page_text']
        out.write(f"     Quote in PDF text: {quote_in_page}\n")
        out.write(f"     Conditions: {json.dumps(r['conditions'], indent=2)}\n")
        out.write(f"     Decision Effect: {r['decision_effect']}\n\n")

print("Written scratch/batch1_inspected.txt")
