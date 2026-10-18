"""Extract every major clinical indication heading and criteria group across all 61 guidelines."""
import fitz
import re
import json

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

# Find start page of each guideline
guideline_starts = []
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
            guideline_starts.append((gid, gtitle, pno, pno + total_p - 1, total_p))

guideline_sections_data = []

for gid, gtitle, start_p, end_p, total_p in guideline_starts:
    # Scan through pages from start_p to end_p
    # Find INDICATIONS and stop at CODING AND STANDARDS or SUMMARY OF EVIDENCE
    indications_text = []
    special_notes_text = []
    statement_text = []
    
    current_sec = "HEADER"
    for p in range(start_p, end_p + 1):
        ptxt = doc[p-1].get_text()
        for line in ptxt.split('\n'):
            line_s = line.strip()
            if not line_s or line_s.startswith('Page ') or 'Evolent Clinical Guideline' in line_s:
                continue
            if line_s == 'STATEMENT':
                current_sec = 'STATEMENT'
            elif line_s in ['Special Note', 'Special Notes', 'SPECIAL NOTE', 'SPECIAL NOTES']:
                current_sec = 'SPECIAL_NOTES'
            elif 'INDICATIONS' in line_s and len(line_s) < 80:
                current_sec = 'INDICATIONS'
            elif line_s in ['CODING AND STANDARDS', 'SUMMARY OF EVIDENCE', 'ANALYSIS OF EVIDENCE', 'POLICY HISTORY', 'LEGAL AND COMPLIANCE', 'REFERENCES']:
                current_sec = 'NON_EXECUTABLE'
                
            if current_sec == 'STATEMENT':
                statement_text.append((p, line_s))
            elif current_sec == 'SPECIAL_NOTES':
                special_notes_text.append((p, line_s))
            elif current_sec == 'INDICATIONS':
                indications_text.append((p, line_s))
                
    # Identify distinct clinical criterion groups in INDICATIONS
    criterion_groups = []
    curr_group = None
    
    for p, l in indications_text:
        # Check if line looks like a clinical heading
        # In Evolent guidelines, indication headings often end with footnote numbers like (1,2) or (1-4) or are uppercase/titlecase
        m_head = re.match(r'^([A-Z][A-Za-z0-9\s,–\-\/\(\)]{3,70}(?:\([0-9,\s–\-]+\))?)$', l)
        is_bullet = l.startswith('?') or l.startswith('•') or l.startswith('o') or l.startswith('-') or l.startswith('–')
        
        if m_head and not is_bullet and not 'INDICATIONS' in l:
            heading_name = m_head.group(1).strip()
            # Exclude generic labels
            if heading_name not in ['NOTE', 'Special Notes', 'Applicable Lines of Business', 'Guideline Number']:
                if curr_group is None or curr_group['heading'] != heading_name:
                    curr_group = {
                        'heading': heading_name,
                        'page': p,
                        'criteria_snippets': []
                    }
                    criterion_groups.append(curr_group)
        elif curr_group and len(l) > 10:
            if len(curr_group['criteria_snippets']) < 6:
                curr_group['criteria_snippets'].append((p, l))
                
    guideline_sections_data.append({
        'guideline_id': f"CG-{gid}",
        'title': gtitle,
        'page_range': f"pp. {start_p}-{end_p}",
        'total_pages': total_p,
        'has_special_notes': len(special_notes_text) > 0,
        'special_notes_sample': [l for p, l in special_notes_text[:5]],
        'criterion_groups_count': len(criterion_groups),
        'criterion_groups': criterion_groups
    })

with open('scratch/all_guideline_criterion_groups.json', 'w', encoding='utf-8') as f:
    json.dump(guideline_sections_data, f, indent=2)

print(f"Audited criterion groups across all {len(guideline_sections_data)} guidelines.")
tot_groups = sum(g['criterion_groups_count'] for g in guideline_sections_data)
print(f"Total distinct clinical indication criterion groups identified: {tot_groups}")
