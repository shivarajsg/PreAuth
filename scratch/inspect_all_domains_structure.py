import fitz
from pathlib import Path
import json

domains = [
    ("musculoskeletal_surgery", "policy_pdfs/current_2026"),
    ("interventional_pain_management", "policy_pdfs/current_2026"),
    ("radiation_oncology", "policy_pdfs/current_2026"),
    ("physical_medicine", "policy_pdfs/current_2026"),
    ("sleep_health", "policy_pdfs/current_2026"),
    ("genetic_testing", "policy_pdfs/current_2026")
]

for dom_name, rel_dir in domains:
    print(f"\n=======================================================")
    print(f"DOMAIN: {dom_name.upper()}")
    print(f"=======================================================")
    p_dir = Path("rulebook_collection/domains") / dom_name / rel_dir
    for pdf_file in sorted(p_dir.glob("*.pdf")):
        doc = fitz.open(pdf_file)
        toc = doc.get_toc()
        print(f"\nPDF: {pdf_file.name} (pages: {len(doc)}, TOC entries: {len(toc)})")
        if toc:
            for item in toc[:15]:
                print(f"  lvl {item[0]}: {item[1]} (page {item[2]})")
            if len(toc) > 15:
                print(f"  ... and {len(toc) - 15} more TOC entries")
        else:
            # print first few lines of page 1 and page 2
            text_p1 = doc[0].get_text("text").splitlines()
            print("  First page lines:", [l.strip() for l in text_p1[:4] if l.strip()])
            if len(doc) > 1:
                text_p2 = doc[1].get_text("text").splitlines()
                print("  Second page lines:", [l.strip() for l in text_p2[:4] if l.strip()])
        doc.close()
