import json
import fitz # PyMuPDF
from pathlib import Path

data = json.loads(Path('scratch/batch4_extracted.json').read_text(encoding='utf-8'))

pdf_ai = fitz.open('rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')
pdf_ipm = fitz.open('rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf')

lines_out = []
lines_out.append("=== TOTAL RULES TO AUDIT: 13 ===")

for rid, info in data.items():
    lines_out.append("="*80)
    lines_out.append(f"RULE ID: {rid}")
    lines_out.append(f"Title: {info['title']}")
    lines_out.append(f"Status: {info['extraction_status']}")
    lines_out.append(f"Source Citation: {info['source_citation']}")
    lines_out.append(f"Source Page: {info['source_page']}")
    lines_out.append(f"Source Quote in rule: {info['source_quote']}")
    lines_out.append(f"Conditions: {json.dumps(info['conditions'], indent=2)}")
    lines_out.append(f"Indications: {json.dumps(info['indications'], indent=2)}")
    lines_out.append(f"Prerequisites: {json.dumps(info['prerequisites'], indent=2)}")
    lines_out.append(f"Exclusions: {json.dumps(info['exclusions'], indent=2)}")
    lines_out.append(f"Rule Logic: {json.dumps(info['rule_logic'], indent=2)}")
    
    if rid.startswith('RULE-ADV'):
        doc = pdf_ai
    else:
        doc = pdf_ipm
        
    pg_num = info['source_page']
    if isinstance(pg_num, int):
        target_idx = pg_num - 1
        if 0 <= target_idx < len(doc):
            page_text = doc[target_idx].get_text()
            lines_out.append(f"\n--- PDF TEXT (Physical Page {pg_num}, 0-indexed {target_idx}) ---")
            lines = [line.strip() for line in page_text.split('\n') if line.strip()]
            for l in lines:
                lines_out.append(f"   {l}")
        else:
            lines_out.append(f"ERROR: Page {pg_num} out of bounds (doc len: {len(doc)})")
    else:
        lines_out.append(f"Source page is not int: {pg_num}")

Path('scratch/batch4_output.txt').write_text('\n'.join(lines_out), encoding='utf-8')
print("Successfully generated scratch/batch4_output.txt")
