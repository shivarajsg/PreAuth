import fitz
import json
from pathlib import Path

base = Path("rulebook_collection/domains/musculoskeletal_surgery/policy_pdfs/current_2026")
doc1 = fitz.open(base / "2026 Evolent Musculoskeletal Surgery Guidelines.pdf")
doc2 = fitz.open(base / "EPOS 1773 for Place of Service - Musculoskeletal Surgery 2026_final_0.pdf")

print("=== MSK GUIDELINE TOC ===")
toc = doc1.get_toc()
for item in toc:
    print(f"lvl {item[0]}: {item[1]} (p. {item[2]})")

print("\n=== EPOS 1773 SAMPLE PAGES ===")
for p in range(min(4, len(doc2))):
    text = doc2[p].get_text("text").splitlines()
    print(f"p.{p+1}: {[l.strip() for l in text[:6] if l.strip()]}")
