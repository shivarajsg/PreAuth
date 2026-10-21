import pymupdf
import re
from pathlib import Path

ROOT = Path(".")
ai_pdf_path = ROOT / "rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
doc = pymupdf.open(ai_pdf_path)

print("Total pages in PDF:", len(doc))

# Search for Takayasu
matches = []
for pno in range(len(doc)):
    text = doc[pno].get_text()
    if "takayasu" in text.lower():
        matches.append(pno + 1)
print("Takayasu found on physical pages:", matches)

# Check page 74, 75, 76 text
for p in matches[:5]:
    t = doc[p-1].get_text()
    print(f"\n--- Page {p} excerpt ---")
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    for l in lines[:15]:
        print("  ", l.encode('ascii', 'replace').decode('ascii'))
