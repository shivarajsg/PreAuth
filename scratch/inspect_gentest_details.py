import fitz
from pathlib import Path

base = Path("rulebook_collection/domains/genetic_testing/policy_pdfs/current_2026")
doc1 = fitz.open(base / "Genetic Testing Guidelines - July 2026.pdf")
doc2 = fitz.open(base / "Generic GT and Laboratory Matrix 10.01.2026.pdf")

print("=== GENETIC TESTING GUIDELINE TOC (sample) ===")
toc = doc1.get_toc()
print(f"Total TOC entries: {len(toc)}")
for item in toc[:25]:
    print(f"lvl {item[0]}: {item[1].encode('ascii', errors='replace').decode('ascii')} (p. {item[2]})")

print("\n=== GENETIC TESTING MATRIX SAMPLE ===")
print(f"Matrix pages: {len(doc2)}")
for p in range(min(3, len(doc2))):
    txt = doc2[p].get_text("text").splitlines()
    print(f"p.{p+1}: {[l.strip().encode('ascii', errors='replace').decode('ascii') for l in txt[:5] if l.strip()]}")
