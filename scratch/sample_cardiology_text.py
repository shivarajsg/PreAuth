import fitz
from pathlib import Path
import json

base = Path("rulebook_collection/domains/cardiology/policy_pdfs/current_2026")
doc1 = fitz.open(base / "2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf")
doc2 = fitz.open(base / "2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf")
doc3 = fitz.open(base / "Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf")
doc4 = fitz.open(base / "Cardiovascular Service Group Grid_January2026.pdf")

print("--- Diagnostic Cardiology: CG 7275 CCTA (p. 4-6) ---")
for p in range(3, 8):
    text = doc1[p].get_text("text")
    for line in text.splitlines()[:15]:
        if "INDICAT" in line.upper() or "STATEMENT" in line.upper() or "Evolent" in line:
            print(f"p.{p+1}: {line}")

print("\n--- Diagnostic Cardiology: CG 7312 MPI (p. 148-152) ---")
for p in range(147, 153):
    text = doc1[p].get_text("text")
    for line in text.splitlines()[:15]:
        if "INDICAT" in line.upper() or "GENERAL" in line.upper() or "Evolent" in line:
            print(f"p.{p+1}: {line}")

print("\n--- Diagnostic Cardiology: CG 7337 TTE (p. 207-210) ---")
for p in range(206, 211):
    text = doc1[p].get_text("text")
    for line in text.splitlines()[:15]:
        if "INDICAT" in line.upper() or "GENERAL" in line.upper() or "Evolent" in line:
            print(f"p.{p+1}: {line}")

print("\n--- Interventional Cardiology: CG 7254 CABG (p. 28-32) ---")
for p in range(27, 33):
    text = doc2[p].get_text("text")
    for line in text.splitlines()[:15]:
        if "INDICAT" in line.upper() or "GENERAL" in line.upper() or "Evolent" in line:
            print(f"p.{p+1}: {line}")

print("\n--- Interventional Cardiology: CG 7255 AVR (p. 48-52) ---")
for p in range(47, 52):
    text = doc2[p].get_text("text")
    for line in text.splitlines()[:15]:
        if "INDICAT" in line.upper() or "GENERAL" in line.upper() or "Evolent" in line:
            print(f"p.{p+1}: {line}")

print("\n--- Cardiac Claim Edit (p. 2-3) ---")
print(doc3[1].get_text("text")[:400])
print(doc3[2].get_text("text")[:400])
