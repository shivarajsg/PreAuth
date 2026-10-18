import fitz
from pathlib import Path
import json

base = Path("rulebook_collection/domains/cardiology/policy_pdfs/current_2026")

diag_pdf = base / "2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf"
interv_pdf = base / "2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf"
edit_pdf = base / "Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf"
grid_pdf = base / "Cardiovascular Service Group Grid_January2026.pdf"

print("=== DIAGNOSTIC CARDIOLOGY BOOKMARKS / SECTIONS ===")
doc1 = fitz.open(diag_pdf)
print(f"Diag pages: {len(doc1)}")
toc1 = doc1.get_toc()
print(f"Diag TOC entries: {len(toc1)}")
for item in toc1[:30]:
    print(f"  lvl {item[0]}: {item[1]} (page {item[2]})")

print("\n=== INTERVENTIONAL CARDIOLOGY BOOKMARKS / SECTIONS ===")
doc2 = fitz.open(interv_pdf)
print(f"Interv pages: {len(doc2)}")
toc2 = doc2.get_toc()
print(f"Interv TOC entries: {len(toc2)}")
for item in toc2[:30]:
    print(f"  lvl {item[0]}: {item[1]} (page {item[2]})")

print("\n=== CARDIAC CLAIM EDIT ===")
doc3 = fitz.open(edit_pdf)
print(f"Edit pages: {len(doc3)}")
for p in range(len(doc3)):
    text = doc3[p].get_text("text")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    print(f"Page {p+1}: {lines[:5]}")

print("\n=== SERVICE GROUP GRID ===")
doc4 = fitz.open(grid_pdf)
print(f"Grid pages: {len(doc4)}")
for p in range(min(3, len(doc4))):
    text = doc4[p].get_text("text")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    print(f"Page {p+1}: {lines[:5]}")
