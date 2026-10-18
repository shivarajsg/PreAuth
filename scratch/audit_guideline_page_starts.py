"""Verify exact physical start page of each guideline."""
import fitz
import re

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

guideline_starts = []

for pno in range(1, len(doc) + 1):
    txt = doc[pno-1].get_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    if not lines:
        continue
    # Check if page has 'Page 1 of' in first 3 lines
    first_few = " ".join(lines[:4])
    m_p1 = re.search(r'Page\s+1\s+of\s+(\d+)', first_few, re.IGNORECASE)
    if m_p1:
        total_p = int(m_p1.group(1))
        # Look for Guideline number
        m_cg = re.search(r'Evolent Clinical Guideline\s+(\d+)\s+for\s+(.*)', first_few, re.IGNORECASE)
        m_pos = re.search(r'Place of Service Policy\s+(\d+)', first_few, re.IGNORECASE)
        m_pre = re.search(r'Preamble', first_few, re.IGNORECASE)
        
        name = "Unknown"
        gid = None
        if m_cg:
            gid = int(m_cg.group(1))
            name = m_cg.group(2)
        elif m_pos:
            gid = int(m_pos.group(1))
            name = "Place of Service"
        elif m_pre:
            name = "Preamble"
            
        guideline_starts.append({
            'physical_page': pno,
            'gid': gid,
            'printed_page': f"Page 1 of {total_p}",
            'total_printed': total_p,
            'name': name,
            'header': lines[1] if len(lines) > 1 else lines[0]
        })

print(f"Total 'Page 1 of X' section starts found: {len(guideline_starts)}")
for s in guideline_starts:
    gid_str = f"CG {s['gid']}" if s['gid'] else "PREAMBLE"
    print(f"p.{s['physical_page']:4d} | {gid_str:10s} | {s['printed_page']:15s} | {s['name'][:45]}")
