"""Exhaustive scan of all 1,041 physical pages for guideline headers."""
import fitz
import re

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

guidelines_found = {}

for pno in range(1, len(doc) + 1):
    txt = doc[pno-1].get_text()
    for line in txt.split('\n'):
        line_s = line.strip()
        m = re.search(r'Evolent Clinical Guideline\s+(\d+)\s+for\s+(.*)', line_s, re.IGNORECASE)
        if m:
            gid = int(m.group(1))
            gtitle = m.group(2).strip()
            if gid not in guidelines_found:
                guidelines_found[gid] = {
                    'title': gtitle,
                    'start_page': pno,
                    'end_page': pno
                }
            else:
                guidelines_found[gid]['end_page'] = pno

print(f"Total unique clinical guidelines found by text header: {len(guidelines_found)}")
for gid in sorted(guidelines_found.keys()):
    info = guidelines_found[gid]
    pg_count = info['end_page'] - info['start_page'] + 1
    print(f"CG {gid:4d} | pp. {info['start_page']:4d} - {info['end_page']:4d} ({pg_count:2d} pgs) | {info['title'][:55]}")

# Also check for numbers between 2000 and 2066 that were NOT found
missing_numbers = [n for n in range(2000, 2067) if n not in guidelines_found]
print(f"\nNumbers in [2000, 2066] NOT found in text headers ({len(missing_numbers)}): {missing_numbers}")
