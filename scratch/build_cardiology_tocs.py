import fitz
import json
from pathlib import Path

base = Path("rulebook_collection/domains/cardiology/policy_pdfs/current_2026")

def parse_cardiology_docs():
    doc1 = fitz.open(base / "2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf")
    doc2 = fitz.open(base / "2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf")
    
    diag_tocs = doc1.get_toc()
    interv_tocs = doc2.get_toc()
    
    print(f"Diag TOC count: {len(diag_tocs)}")
    print(f"Interv TOC count: {len(interv_tocs)}")
    
    units = []
    
    # Preamble Diag
    units.append({
        "doc_id": "DOC-CARD-001",
        "guideline_id": "PREAMBLE-DIAG",
        "title": "Guidelines for Clinical Review Determination Preamble and Development Process (Diagnostic)",
        "physical_start": 2,
        "physical_end": 3
    })
    
    # Diagnostic guidelines
    diag_items = [item for item in diag_tocs if item[0] == 2 and "Evolent Clinical Guideline" in item[1]]
    for i, item in enumerate(diag_items):
        title = item[1].strip()
        p_start = item[2]
        p_end = diag_items[i+1][2] - 1 if i+1 < len(diag_items) else len(doc1)
        # extract CG number
        import re
        m = re.search(r"Guideline\s+(\d+)", title)
        cg_num = m.group(1) if m else f"DIAG_{i+1}"
        units.append({
            "doc_id": "DOC-CARD-001",
            "guideline_id": f"CG-{cg_num}",
            "title": title,
            "physical_start": p_start,
            "physical_end": p_end
        })
        
    # Preamble Interv
    units.append({
        "doc_id": "DOC-CARD-002",
        "guideline_id": "PREAMBLE-INTERV",
        "title": "Guidelines for Clinical Review Determination Preamble and Development Process (Interventional)",
        "physical_start": 2,
        "physical_end": 4
    })
    
    # Interventional guidelines
    interv_items = [item for item in interv_tocs if item[0] == 2 and "Evolent Clinical Guideline" in item[1]]
    for i, item in enumerate(interv_items):
        title = item[1].strip()
        p_start = item[2]
        p_end = interv_items[i+1][2] - 1 if i+1 < len(interv_items) else len(doc2)
        import re
        m = re.search(r"Guideline\s+(\d+)", title)
        cg_num = m.group(1) if m else f"INTERV_{i+1}"
        units.append({
            "doc_id": "DOC-CARD-002",
            "guideline_id": f"CG-{cg_num}",
            "title": title,
            "physical_start": p_start,
            "physical_end": p_end
        })
        
    # Claim edit
    units.append({
        "doc_id": "DOC-CARD-004",
        "guideline_id": "OP-388-01",
        "title": "Cardiac Claim Edit: Stress Echocardiography and Doppler Add-On (OP.388.01)",
        "physical_start": 1,
        "physical_end": 3
    })
    
    # Service group grid
    units.append({
        "doc_id": "DOC-CARD-003",
        "guideline_id": "GRID-CARD-2026",
        "title": "Cardiovascular Service Group Grid (January 2026)",
        "physical_start": 1,
        "physical_end": 9
    })
    
    print(f"Total governed units identified for Cardiology: {len(units)}")
    with open("scratch/cardiology_units.json", "w", encoding="utf-8") as f:
        json.dump(units, f, indent=2)

if __name__ == "__main__":
    parse_cardiology_docs()
