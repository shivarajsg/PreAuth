"""Analyze indications sections across all 61 clinical guidelines."""
import fitz
import re
import json

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    existing_rules = json.load(f)

# Group existing rules by guideline
rules_by_cg = {}
for r in existing_rules:
    rid = r['rule_id']
    m = re.match(r'RULE-ADV-([A-Z0-9]+)-', rid)
    if m:
        cg = m.group(1)
        rules_by_cg.setdefault(cg, []).append(r)

# Find start pages
guideline_starts = []
for pno in range(1, len(doc) + 1):
    txt = doc[pno-1].get_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    if not lines: continue
    first_few = " ".join(lines[:4])
    m_p1 = re.search(r'Page\s+1\s+of\s+(\d+)', first_few, re.IGNORECASE)
    if m_p1:
        total_p = int(m_p1.group(1))
        m_cg = re.search(r'Evolent Clinical Guideline\s+(\d+)', first_few, re.IGNORECASE)
        if m_cg:
            gid = int(m_cg.group(1))
            guideline_starts.append((gid, pno, pno + total_p - 1, total_p))

print(f"Total clinical guidelines in PDF: {len(guideline_starts)}")
print(f"{'CG ID':<8} | {'Pages':<12} | {'Rules':<6} | {'Major Sections Found in Text'}")
print("-" * 80)

for gid, start_p, end_p, total_p in guideline_starts:
    cg_key = f"CG{gid}"
    rule_list = rules_by_cg.get(cg_key, [])
    
    # Scan for major headings in INDICATIONS
    headings = []
    in_indications = False
    for p in range(start_p, end_p + 1):
        ptxt = doc[p-1].get_text()
        for line in ptxt.split('\n'):
            line_s = line.strip()
            if 'INDICATIONS' in line_s:
                in_indications = True
            elif 'CODING' in line_s or 'SUMMARY OF EVIDENCE' in line_s or 'BACKGROUND' in line_s:
                in_indications = False
            elif in_indications:
                # Look for bold or uppercase or numbered sections
                if len(line_s) > 4 and len(line_s) < 60 and not line_s.startswith('Page') and not line_s.startswith('Evolent'):
                    if line_s.isupper() or re.match(r'^[A-Z][a-zA-Z\s,–\-\(\)\/]{4,50}\s*\(\d', line_s):
                        if line_s not in headings and 'INDICATIONS' not in line_s:
                            headings.append(line_s)
                            
    print(f"CG {gid:<5d} | pp.{start_p:4d}-{end_p:4d} | {len(rule_list):<5d} | {headings[:3]}")
