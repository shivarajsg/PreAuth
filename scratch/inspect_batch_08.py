"""Inspect text for Batch 08: CG 2056 through CG 2066."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

def examine(pno, count=45):
    lines = [l.strip() for l in doc[pno-1].get_text().split('\n') if l.strip()]
    hdr = lines[0] if lines else 'empty'
    print(f"\n================ Physical Page {pno} (Printed: {hdr}) ================")
    for l in lines[:count]:
        # sanitize for console output
        safe_l = l.encode('ascii', errors='replace').decode('ascii')
        print("  ", safe_l)

targets = [
    # CG 2056: Thoracic Spine CT
    905, 906,
    # CG 2057: Thoracic Spine MRI
    925, 926,
    # CG 2058: Tumor Imaging PET
    947, 948,
    # CG 2061: Unlisted Study
    954, 955, 956,
    # CG 2062: Upper Extremity CT
    965, 966,
    # CG 2063: Upper Extremity CTA
    989, 990,
    # CG 2064: Upper Extremity MRA
    1001, 1002,
    # CG 2065: Upper Extremity MRI
    1014, 1015,
    # CG 2066: Urgent/Emergent Criteria
    1036, 1037
]

for t in targets:
    examine(t)
