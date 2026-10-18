"""Test exact verbatim quotes for Batch 08."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

test_cases = [
    # CG 2056
    (905, "When Thoracic Spine MRI is Contraindicated or cannot be performed"),
    (906, "Pain lasting > 4 weeks"),
    # CG 2057
    (925, "INDICATIONS FOR THORACIC SPINE MRI"),
    (926, "Pain lasting > 4 weeks"),
    # CG 2058
    (947, "Positron Emission Tomography (PET) imaging, any site, not otherwise specified, is a non-covered CPT code."),
    # CG 2061
    (954, "Unlisted MRI (CPT Code 76498), can be used in the context of:"),
    (956, "Unlisted CT (CPT Code 76497), can be used when imaging of the whole body is needed for certain hematologic malignancies:"),
    # CG 2062
    (965, "X-rays must precede CT evaluation, unless otherwise indicated"),
    # CG 2063
    (989, "Upper Extremity Peripheral Vascular Disease (1,2)"),
    # CG 2064
    (1001, "When a separate MRA and MRI exam is requested, documentation requires a medical reason that clearly indicates why additional MRI imaging of the upper extremity is needed."),
    # CG 2065
    (1014, "Plain X-rays must precede MRI evaluation unless otherwise indicated"),
    # CG 2066
    (1036, "INDICATIONS FOR EMERGENT STUDIES"),
    (1036, "INDICATIONS FOR URGENT STUDIES"),
]

all_passed = True
for pno, q in test_cases:
    txt = doc[pno-1].get_text()
    if q in txt:
        print(f"[PASS] p.{pno}: '{q[:45]}...'")
    else:
        print(f"[FAIL] p.{pno}: '{q[:45]}...'")
        all_passed = False

if all_passed:
    print("\nALL 13 BATCH 08 QUOTES VERIFIED VERBATIM!")
else:
    print("\nSOME QUOTES FAILED!")
