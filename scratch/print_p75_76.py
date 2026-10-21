import pymupdf
from pathlib import Path

ROOT = Path(".")
ai_pdf_path = ROOT / "rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
doc = pymupdf.open(ai_pdf_path)

for p in [75, 76]:
    print(f"=== PHYSICAL PAGE {p} ===")
    lines = doc[p-1].get_text().split("\n")
    for l in lines:
        if l.strip():
            print("  ", l.strip().encode('ascii', 'replace').decode('ascii'))
