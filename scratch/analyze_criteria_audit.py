"""Analyze unextracted criteria groups across all guidelines."""
import json

with open('scratch/guideline_criteria_audit.json', 'r', encoding='utf-8') as f:
    audit = json.load(f)

print(f"{'Guideline':<10} | {'Rules':<5} | {'Pages':<15} | {'Extracted Sections vs Indication Sections Found'}")
print("-" * 85)

low_rule_guidelines = []
for a in audit:
    gid = a['guideline_id']
    cnt = a['rules_count']
    p_range = a['page_range']
    tot_p = a['total_pages']
    ext_secs = a['extracted_sections']
    found_secs = a['indication_sections_found']
    
    if cnt <= 2 and tot_p >= 15:
        low_rule_guidelines.append(a)
        print(f"{gid:<10} | {cnt:<5} | {p_range:<15} ({tot_p}p) | Extracted: {len(ext_secs)} | Found in text: {len(found_secs)}")
        for s in ext_secs:
            safe_s = s[:60].encode('ascii', errors='replace').decode('ascii')
            print(f"   [EXTRACTED] {safe_s}")
        for s in found_secs[:4]:
            safe_s = s[:60].encode('ascii', errors='replace').decode('ascii')
            print(f"   [FOUND IN TEXT] {safe_s}")
        print()

print(f"Total large guidelines (>=15 pages) with <=2 extracted rules: {len(low_rule_guidelines)}")
