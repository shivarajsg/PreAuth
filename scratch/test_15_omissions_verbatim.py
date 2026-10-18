"""Test all 15 omission quotes against the physical PDF text layer."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

test_cases = [
    (151, "Known or suspected trauma or injury to the head with documentation of one or more of"),
    (150, "Evaluation of Headache (1,2)"),
    (176, "Evaluation of Known Intracranial Vascular Disease (1,2)"),
    (232, "Evaluation of Suspected Multiple Sclerosis (61,62)"),
    (232, "New onset of an unprovoked seizure"),
    (361, "Hemoptysis after x-ray completed (25)"),
    (397, "THORACIC AORTIC DISEASE"),
    (501, "Suspected Bone Fracture"),
    (553, "Joint specific advanced imaging is indicated for any positive orthopedic sign listed below:"),
    (550, "OSTEONECROSIS"),
    (592, "EVALUATION OF KNOWN OR SUSPECTED INFECTION"),
    (737, "Primary CNS Lymphoma"),
    (738, "Non-Small Cell Lung Cancer"),
    (811, "Chronic rhinosinusitis (> 12 weeks duration) with ALL of the following:"),
    (1015, "Bear hug test")
]

all_ok = True
for pno, q in test_cases:
    txt = doc[pno-1].get_text()
    if q in txt:
        print(f"[OK] p.{pno}: '{q[:40]}...'")
    else:
        print(f"[FAIL] p.{pno}: '{q[:40]}...' NOT FOUND!")
        all_ok = False

if all_ok:
    print("\nALL 15 OMISSION QUOTES ARE 100% VERBATIM MATCHES ON PHYSICAL PAGES!")
else:
    print("\nSOME QUOTES FAILED!")
