import fitz
from pathlib import Path

base = Path("rulebook_collection/domains/sleep_health/policy_pdfs/current_2026")
doc = fitz.open(base / "2026 Evolent Clinical Guidelines - Sleep Studies.pdf")

print("=== SLEEP HEALTH PAGES ===")
print("Pages:", len(doc))
for p in range(len(doc)):
    text = doc[p].get_text("text").splitlines()
    for l in text[:5]:
        if "CG" in l or "Guideline" in l or "INDICAT" in l.upper() or "STATEMENT" in l.upper():
            print(f"p.{p+1}: {l.encode('ascii', errors='replace').decode('ascii')}")
