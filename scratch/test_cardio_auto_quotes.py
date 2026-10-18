import fitz
import json
import re
from pathlib import Path

BASE_DIR = Path(".")
CARDIO_DIR = BASE_DIR / "rulebook_collection" / "domains" / "cardiology"
base_pdf = CARDIO_DIR / "policy_pdfs" / "current_2026"

doc_diag = fitz.open(base_pdf / "2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf")
doc_interv = fitz.open(base_pdf / "2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf")
doc_edit = fitz.open(base_pdf / "Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf")
doc_grid = fitz.open(base_pdf / "Cardiovascular Service Group Grid_January2026.pdf")

with open("scratch/cardiology_units.json", "r", encoding="utf-8") as f:
    units = json.load(f)

def norm(text):
    text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()

results = []

for u in units:
    gid = u["guideline_id"]
    doc_id = u["doc_id"]
    doc = doc_diag if doc_id == "DOC-CARD-001" else doc_interv if doc_id == "DOC-CARD-002" else doc_edit if doc_id == "DOC-CARD-004" else doc_grid
    p_start = u["physical_start"]
    p_end = u["physical_end"]
    
    best_quote = None
    best_page = None
    
    # 1. Look for clinical criteria lines
    for p in range(p_start - 1, min(p_end, p_start + 12)):
        page_text = doc[p].get_text("text")
        lines = page_text.splitlines()
        for idx, line in enumerate(lines):
            l = line.strip()
            if any(k in l.lower() for k in ["indicated", "evaluation of", "suspected", "symptoms", "criteria", "documentation", "coverage", "testing"]):
                if len(l) >= 30 and not l.startswith("http") and not l.startswith("Page ") and not "Evolent" in l:
                    if norm(l) in norm(page_text):
                        best_quote = l
                        best_page = p + 1
                        break
        if best_quote:
            break
            
    if not best_quote:
        for p in range(p_start - 1, min(p_end, p_start + 5)):
            page_text = doc[p].get_text("text")
            for line in page_text.splitlines():
                l = line.strip()
                if len(l) >= 35 and not l.startswith("http") and not l.startswith("Page ") and not "All rights" in l:
                    if norm(l) in norm(page_text):
                        best_quote = l
                        best_page = p + 1
                        break
            if best_quote:
                break
                
    results.append({
        "guideline_id": gid,
        "title": u["title"],
        "doc_id": doc_id,
        "page": best_page,
        "quote": best_quote
    })

print(f"Scanned {len(results)} units. Missing quote count: {sum(1 for r in results if not r['quote'])}")
for r in results[:10]:
    print(f"[{r['guideline_id']}] p.{r['page']}: {r['quote'][:80] if r['quote'] else 'NONE'}")
