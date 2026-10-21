import fitz
from pathlib import Path

doc_ai = fitz.open('rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')
doc_ipm = fitz.open('rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf')

out = []

def dump_pages(doc, pages, title):
    out.append(f"=== {title} ===")
    for p in pages:
        out.append(f"\n--- Physical Page {p} (idx {p-1}) ---")
        lines = [l.strip() for l in doc[p-1].get_text().split('\n') if l.strip()]
        for l in lines:
            out.append(l)

# AI pages
dump_pages(doc_ai, [904, 905, 906, 907], "THORACIC SPINE CT (CG2056)")
dump_pages(doc_ai, [924, 925, 926, 927], "THORACIC SPINE MRI (CG2057)")
dump_pages(doc_ai, [964, 965, 966, 967], "UPPER EXTREMITY CT (CG2062)")

# IPM pages
dump_pages(doc_ipm, [3, 4, 5, 10, 11, 12], "EPIDURAL INJECTIONS (CG-EPIDURAL)")
dump_pages(doc_ipm, [16, 17, 18], "EPIDURAL PUMP TRIALS (CG-EPIDURAL-PUMPS)")
dump_pages(doc_ipm, [30, 31, 32, 33], "FACET BLOCKS (CG-FACET)")
dump_pages(doc_ipm, [56, 57, 58, 59], "SACROILIAC INJECTIONS (CG-SI)")
dump_pages(doc_ipm, [77, 78, 79, 80, 81], "SPINAL CORD STIMULATION (CG-SCS)")
dump_pages(doc_ipm, [88, 89, 90, 91], "SYMPATHETIC BLOCKS (CG-SYMPATHETIC)")

Path('scratch/batch4_policy_pages.txt').write_text('\n'.join(out), encoding='utf-8')
print("Dumped all relevant pages to scratch/batch4_policy_pages.txt")
