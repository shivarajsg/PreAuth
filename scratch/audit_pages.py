"""Inspect TOC and guideline titles and pages."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

toc = doc.get_toc()
print(f"Total bookmarks: {len(toc)}")
for item in toc:
    lvl, title, page = item
    if lvl <= 2:
        safe_title = title.encode('ascii', errors='replace').decode('ascii')
        print(f"L{lvl} | p.{page:4d} | {safe_title}")
