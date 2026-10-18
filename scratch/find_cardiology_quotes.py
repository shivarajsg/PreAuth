import fitz
import json
import re
from pathlib import Path

base = Path("rulebook_collection/domains/cardiology/policy_pdfs/current_2026")
doc1 = fitz.open(base / "2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf")
doc2 = fitz.open(base / "2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf")
doc3 = fitz.open(base / "Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf")
doc4 = fitz.open(base / "Cardiovascular Service Group Grid_January2026.pdf")

with open("scratch/cardiology_units.json", "r", encoding="utf-8") as f:
    units = json.load(f)

extracted_quotes = {}

for u in units:
    gid = u["guideline_id"]
    doc_id = u["doc_id"]
    doc = doc1 if doc_id == "DOC-CARD-001" else doc2 if doc_id == "DOC-CARD-002" else doc3 if doc_id == "DOC-CARD-004" else doc4
    p_start = u["physical_start"]
    p_end = u["physical_end"]
    
    # search pages for "INDICAT" or "General Statement" or "Policy Statement"
    found_indications = []
    for p in range(p_start - 1, min(p_end, p_start + 8)):
        page_text = doc[p].get_text("text")
        lines = page_text.splitlines()
        for idx, line in enumerate(lines):
            l_strip = line.strip()
            if any(k in l_strip.upper() for k in ["INDICAT", "CRITERIA", "POLICY STATEMENT", "GENERAL STATEMENT"]):
                # grab a chunk of next 10 lines
                chunk = " ".join([l.strip() for l in lines[idx:idx+8] if l.strip()])
                found_indications.append({
                    "page": p + 1,
                    "heading": l_strip,
                    "snippet": chunk[:250]
                })
    extracted_quotes[gid] = {
        "title": u["title"],
        "p_start": p_start,
        "p_end": p_end,
        "indications": found_indications[:3]
    }

with open("scratch/cardiology_sample_indications.json", "w", encoding="utf-8") as f:
    json.dump(extracted_quotes, f, indent=2)

print(f"Scanned {len(extracted_quotes)} units for indication sections.")
