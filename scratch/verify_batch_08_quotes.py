"""Verify candidate quotes on exact physical pages for Batch 08."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

def check_quote(pno, quote):
    txt = doc[pno-1].get_text()
    if quote in txt:
        print(f"[OK] Page {pno}: '{quote[:50]}...' found verbatim.")
        return True
    else:
        print(f"[FAILED] Page {pno}: '{quote[:50]}...' NOT found!")
        # Print snippet from page
        for line in txt.split('\n')[:25]:
            safe_l = line.encode('ascii', errors='replace').decode('ascii')
            print("   ", safe_l)
        return False

# CG 2056
check_quote(905, "When Thoracic Spine MRI is Contraindicated or cannot be performed")
# CG 2056 back pain
check_quote(906, "Pain lasting > 4 weeks")

# CG 2057
check_quote(925, "INDICATIONS FOR THORACIC SPINE MRI")
check_quote(926, "Pain lasting > 4 weeks")

# CG 2058
check_quote(947, "Positron Emission Tomography (PET) imaging, any site, not otherwise specified, is a non-covered CPT code.")

# CG 2061
check_quote(954, "Unlisted MRI (CPT Code 76498), can be used in the context of:")
check_quote(956, "Unlisted CT (CPT Code 76497), can be used when imaging of the whole body is needed for certain hematologic malignancies:")

# CG 2062
check_quote(965, "Prior completed X-ray showing no clear etiology of joint/extremity pain must precede upper extremity CT evaluation unless otherwise indicated")

# CG 2063
check_quote(989, "Upper Extremity Peripheral Vascular Disease")

# CG 2064
check_quote(1001, "For evaluation of known or suspected upper extremity vascular disease when CTA is contraindicated or cannot be performed:")

# CG 2065
check_quote(1014, "Prior completed X-ray showing no clear etiology of joint/extremity pain must precede upper extremity MRI evaluation unless otherwise indicated")

# CG 2066
check_quote(1036, "The requested study is required to render immediate medical attention needed to prevent loss of life, limb, or risk of significant morbidity/permanent disability such as")
check_quote(1036, "For the evaluation of a condition that requires prompt medical intervention to prevent additional consequences to the health/wellbeing of the member.")
