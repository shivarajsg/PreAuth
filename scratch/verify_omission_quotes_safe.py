"""Verify exact verbatim quotes on physical PDF pages for the 15 confirmed omissions safely."""
import fitz
import json

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

def search_text_on_pages(start_p, end_p, keywords):
    for pno in range(start_p, end_p + 1):
        txt = doc[pno-1].get_text()
        for kw in keywords:
            if kw.lower() in txt.lower():
                lines = [l.strip() for l in txt.split('\n') if l.strip()]
                for idx, l in enumerate(lines):
                    if kw.lower() in l.lower() and len(l) > 5 and not l.startswith('Page'):
                        safe_l = l.encode('ascii', errors='replace').decode('ascii')
                        safe_printed = lines[0].encode('ascii', errors='replace').decode('ascii')
                        return {
                            'physical_page': pno,
                            'printed_page': safe_printed,
                            'matched_line': safe_l,
                            'exact_line': l,
                            'context': [sub_l for sub_l in lines[max(0, idx-1):min(len(lines), idx+4)]]
                        }
    return None

omissions = [
    ("CG-2008", "Head Trauma", 146, 171, ["Evaluation of Known or Suspected Trauma", "HEAD TRAUMA"]),
    ("CG-2008", "Thunderclap Headache / Subarachnoid Hemorrhage", 146, 171, ["Sudden onset of severe headache", "subarachnoid hemorrhage"]),
    ("CG-2009", "Brain CTA - Stroke / Large Vessel Occlusion", 172, 191, ["Acute Ischemic Stroke", "mechanical thrombectomy", "Large Vessel"]),
    ("CG-2012", "Brain MRI - Multiple Sclerosis", 220, 269, ["Multiple Sclerosis", "suspected multiple sclerosis"]),
    ("CG-2012", "Brain MRI - Seizures", 220, 269, ["Seizure", "Epilepsy", "unprovoked seizure"]),
    ("CG-2018", "Chest CT - Hemoptysis / Bronchogenic Carcinoma", 353, 382, ["Hemoptysis", "unexplained hemoptysis"]),
    ("CG-2020", "Chest CTA - Thoracic Aortic Dissection / Aneurysm", 397, 415, ["Thoracic Aortic Disease", "Aortic Dissection"]),
    ("CG-2032", "Lower Extremity CT - Fracture / Dislocation", 501, 523, ["Fracture", "Tibial", "Dislocation", "intra-articular"]),
    ("CG-2035", "Lower Extremity MRI - Meniscal / Ligamentous Tear (Orthopedic Signs)", 550, 571, ["Lachman", "McMurray", "positive orthopedic sign"]),
    ("CG-2035", "Lower Extremity MRI - Avascular Necrosis (AVN) Hip", 550, 571, ["Avascular Necrosis", "Osteonecrosis"]),
    ("CG-2037", "Lumbar Spine MRI - Spinal Infection / Malignancy", 592, 613, ["Suspected infection", "Discitis", "Spinal Infection", "malignancy"]),
    ("CG-2046", "Whole Body PET/CT - Lymphoma Staging", 737, 807, ["Hodgkin", "Lymphoma", "Non-Hodgkin"]),
    ("CG-2046", "Whole Body PET/CT - Non-Small Cell Lung Cancer Staging", 737, 807, ["Non-Small Cell Lung Cancer", "Solitary Pulmonary Nodule"]),
    ("CG-2047", "Sinus Maxillofacial CT - Chronic Rhinosinusitis", 808, 825, ["Chronic rhinosinusitis", "failed medical therapy", "Maximal Medical"]),
    ("CG-2065", "Upper Extremity MRI - Rotator Cuff Tear (Orthopedic Signs)", 1012, 1034, ["Bear hug test", "Belly press test", "Drop arm test"])
]

results = []
for gid, desc, start_p, end_p, kws in omissions:
    match = search_text_on_pages(start_p, end_p, kws)
    if match:
        results.append({
            'guideline_id': gid,
            'description': desc,
            'match': match
        })
        print(f"[FOUND] {gid} | {desc} | p.{match['physical_page']} ({match['printed_page']}): {match['matched_line'][:60]}")
    else:
        print(f"[NOT FOUND] {gid} | {desc}")

with open('scratch/omission_matches.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"\nTotal omission criteria confirmed in PDF: {len(results)} / {len(omissions)}")
