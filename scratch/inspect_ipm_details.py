import fitz
from pathlib import Path

base = Path("rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026")
doc1 = fitz.open(base / "2026 Evolent Interventional Pain Management Guidelines.pdf")
doc2 = fitz.open(base / "EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf")

print("=== IPM GUIDELINE TOC ===")
toc = doc1.get_toc()
for item in toc:
    print(f"lvl {item[0]}: {item[1].encode('ascii', errors='replace').decode('ascii')} (p. {item[2]})")

print("\n=== EPOS 1755 PAGES ===")
print(f"EPOS pages: {len(doc2)}")
for p in range(min(3, len(doc2))):
    txt = doc2[p].get_text("text").splitlines()
    print(f"p.{p+1}: {[l.strip().encode('ascii', errors='replace').decode('ascii') for l in txt[:4] if l.strip()]}")
