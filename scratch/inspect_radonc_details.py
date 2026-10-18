import fitz
from pathlib import Path

base = Path("rulebook_collection/domains/radiation_oncology/policy_pdfs/current_2026")
doc1 = fitz.open(base / "ECG 7000 for Radiation Therapy Services 2026_final.pdf")
doc2 = fitz.open(base / "ECG 7001 for Proton Beam Radiation Therapy and Neutron Beam Radiation Therapy Services 2026_final.pdf")
doc3 = fitz.open(base / "2026 Evolent Coding Standards FINAL 121225  L-NIA.pdf")

print("=== ECG 7000 SECTIONS ===")
# Scan pages 1-5 for TOC or headings
for p in range(min(5, len(doc1))):
    text = doc1[p].get_text("text").splitlines()
    print(f"p.{p+1}: {[l.strip().encode('ascii', errors='replace').decode('ascii') for l in text[:6] if l.strip()]}")

print("\n=== ECG 7001 TOC ===")
for item in doc2.get_toc():
    print(f"lvl {item[0]}: {item[1].encode('ascii', errors='replace').decode('ascii')} (p. {item[2]})")

print("\n=== CODING STANDARDS SAMPLE ===")
for p in range(min(3, len(doc3))):
    text = doc3[p].get_text("text").splitlines()
    print(f"p.{p+1}: {[l.strip().encode('ascii', errors='replace').decode('ascii') for l in text[:6] if l.strip()]}")
