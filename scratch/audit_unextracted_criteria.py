"""Scan each guideline's internal Table of Contents and INDICATIONS headers to identify all distinct clinical criteria groups."""
import fitz
import re
import json

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    existing_rules = json.load(f)

# Find start page and TOC of each guideline
guidelines = []
for pno in range(1, len(doc) + 1):
    txt = doc[pno-1].get_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    if not lines: continue
    first_few = " ".join(lines[:4])
    m_p1 = re.search(r'Page\s+1\s+of\s+(\d+)', first_few, re.IGNORECASE)
    if m_p1:
        total_p = int(m_p1.group(1))
        m_cg = re.search(r'Evolent Clinical Guideline\s+(\d+)\s+for\s+(.*)', first_few, re.IGNORECASE)
        if m_cg:
            gid = int(m_cg.group(1))
            gtitle = m_cg.group(2).strip()
            guidelines.append({
                'gid': gid,
                'title': gtitle,
                'start_page': pno,
                'end_page': pno + total_p - 1,
                'total_pages': total_p
            })

print(f"Total guidelines to audit: {len(guidelines)}")

# For each guideline, extract the internal Table of Contents (usually on page 1 or 2 of the guideline)
guideline_criteria_audit = []

for g in guidelines:
    gid = g['gid']
    start_p = g['start_page']
    end_p = g['end_page']
    
    # Existing rules for this guideline
    cg_key = f"CG{gid}"
    rules = [r for r in existing_rules if cg_key in r['rule_id']]
    extracted_sections = [r['source_section'] for r in rules]
    
    # Find all indication sections in the guideline text
    indication_sections = []
    for p in range(start_p, min(start_p + 15, end_p + 1)):
        ptxt = doc[p-1].get_text()
        lines = [l.strip() for l in ptxt.split('\n') if l.strip()]
        for idx, l in enumerate(lines):
            # Check for INDICATIONS headers
            if 'INDICATIONS FOR' in l or (l.startswith('INDICATIONS') and len(l) < 30):
                # Following lines are major indication groups
                for sub_l in lines[idx+1:idx+15]:
                    if len(sub_l) > 4 and len(sub_l) < 65:
                        if not sub_l.startswith('Page') and not sub_l.startswith('Evolent') and not sub_l.startswith('GUIDELINE'):
                            if any(k in sub_l for k in ['Evaluation', 'Known', 'Suspected', 'Pain', 'Injury', 'Trauma', 'Malignan', 'Cancer', 'Nodule', 'Infection', 'Screening', 'Deficit', 'Syndrome', 'Aneurysm', 'Disease', 'Disorder']):
                                if sub_l not in indication_sections:
                                    indication_sections.append(sub_l)
                                    
    guideline_criteria_audit.append({
        'guideline_id': f"CG-{gid}",
        'title': g['title'],
        'page_range': f"pp. {start_p}-{end_p}",
        'total_pages': g['total_pages'],
        'rules_count': len(rules),
        'extracted_rules': [r['rule_id'] for r in rules],
        'extracted_sections': extracted_sections,
        'indication_sections_found': indication_sections[:8]
    })

with open('scratch/guideline_criteria_audit.json', 'w', encoding='utf-8') as f:
    json.dump(guideline_criteria_audit, f, indent=2)

print("Saved criteria audit to scratch/guideline_criteria_audit.json.")
