import json

with open("scratch/batch3_extracted.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

with open("scratch/batch3_analysis.txt", "w", encoding="utf-8") as out:
    for i, r in enumerate(rules, 21):
        out.write("=" * 80 + "\n")
        out.write(f"[{i:02d}] Rule ID: {r['rule_id']} (Status: {r['existing_status']})\n")
        out.write(f"     Domain: {r['domain']}\n")
        out.write(f"     Source File: {r['source_file']}\n")
        out.write(f"     Page: physical {r['physical_page']} (printed {r['printed_page']})\n")
        out.write(f"     Section: {r['source_section']}\n")
        out.write(f"     Quote: {r['source_quote']}\n")
        out.write(f"     Conditions: {json.dumps(r['conditions'], indent=2)}\n")
        out.write(f"     Decision Effect: {r['decision_effect']}\n\n")
        out.write("--- Page Text Excerpt ---\n")
        for line in r['page_text'].split("\n"):
            if line.strip():
                out.write("  " + line.strip() + "\n")
        out.write("\n")

print("Written scratch/batch3_analysis.txt")
