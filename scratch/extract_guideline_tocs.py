"""Extract the complete internal Table of Contents for every clinical guideline in the PDF."""
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

guideline_tocs = {}

for gid, gtitle, start_p, end_p, total_p in guideline_starts:
    # TOC is typically on page 1 or 2 of the guideline
    toc_text = ""
    for p in range(start_p, min(start_p + 3, end_p + 1)):
        txt = doc[p-1].get_text()
        if 'TABLE OF CONTENTS' in txt:
            idx = txt.find('TABLE OF CONTENTS')
            toc_text = txt[idx:]
            # If it continues to next page or ends at STATEMENT / CODING
            break
            
    # Parse TOC lines
    sections = []
    for line in toc_text.split('\n'):
        line_s = line.strip()
        if not line_s or 'TABLE OF CONTENTS' in line_s:
            continue
        # Check if line has dotted leader or page number (e.g. .... 3)
        m_sec = re.match(r'^(.*?)(?:\.{2,}|\s{3,})(\d+)$', line_s)
        if m_sec:
            sec_name = m_sec.group(1).strip()
            sec_page = int(m_sec.group(2))
            if sec_name:
                sections.append({'section': sec_name, 'printed_page': sec_page})
        elif len(line_s) > 3 and not line_s.startswith('Page') and not line_s.startswith('Evolent'):
            # It might be a section heading without dots
            if any(k in line_s for k in ['INDICATIONS', 'STATEMENT', 'CODING', 'SUMMARY', 'BACKGROUND', 'POLICY', 'REFERENCES', 'GENERAL INFORMATION', 'SPECIAL NOTE']):
                sections.append({'section': line_s, 'printed_page': None})

    guideline_tocs[f"CG-{gid}"] = {
        'guideline_id': f"CG-{gid}",
        'title': gtitle,
        'physical_start': start_p,
        'physical_end': end_p,
        'total_pages': total_p,
        'toc_sections': sections
    }

with open('scratch/all_guideline_tocs.json', 'w', encoding='utf-8') as f:
    json.dump(guideline_tocs, f, indent=2)

print(f"Extracted internal TOC for {len(guideline_tocs)} guidelines.")
for gid in ['CG-2000', 'CG-2008', 'CG-2012', 'CG-2017', 'CG-2020', 'CG-2035', 'CG-2037', 'CG-2046', 'CG-2065']:
    info = guideline_tocs[gid]
    print(f"\n=== {gid}: {info['title'][:40]} ({info['total_pages']} pgs) ===")
    for s in info['toc_sections'][:8]:
        print(f"  - {s['section']} (p.{s['printed_page']})")
