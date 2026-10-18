"""Verify exact verbatim quotes on physical PDF pages for the 15 confirmed omissions."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

def search_text_on_pages(start_p, end_p, keywords):
    for pno in range(start_p, end_p + 1):
        txt = doc[pno-1].get_text()
        for kw in keywords:
            if kw.lower() in txt.lower():
                lines = [l.strip() for l in txt.split('\n') if l.strip()]
                for idx, l in enumerate(lines):
                    if kw.lower() in l.lower():
                        print(f"p.{pno} [Printed: {lines[0]}]: {l}")
                        for sub_l in lines[max(0, idx-1):min(len(lines), idx+4)]:
                            safe = sub_l.encode('ascii', errors='replace').decode('ascii')
                            print(f"   {safe}")
                        print()
                        return pno, l
    return None, None

print("=== 1. CG 2008 Brain CT Trauma ===")
search_text_on_pages(146, 171, ["Acute Head Trauma", "Trauma", "Glasgow"])

print("=== 2. CG 2008 Brain CT Thunderclap Headache ===")
search_text_on_pages(146, 171, ["Thunderclap", "Worst Headache", "Subarachnoid"])

print("=== 3. CG 2009 Brain CTA Stroke / LVO ===")
search_text_on_pages(172, 191, ["Acute Ischemic Stroke", "Thrombectomy", "Large Vessel"])

print("=== 4. CG 2012 Brain MRI Multiple Sclerosis ===")
search_text_on_pages(220, 269, ["Multiple Sclerosis", "Demyelinating"])

print("=== 5. CG 2012 Brain MRI Seizures ===")
search_text_on_pages(220, 269, ["Seizure", "Epilepsy"])

print("=== 6. CG 2018 Chest CT Hemoptysis / Malignancy ===")
search_text_on_pages(353, 382, ["Hemoptysis", "Bronchogenic"])

print("=== 7. CG 2020 Chest CTA Aortic Dissection ===")
search_text_on_pages(397, 415, ["Aortic Dissection", "Thoracic Aortic"])

print("=== 8. CG 2032 Lower Extremity CT Fracture ===")
search_text_on_pages(501, 523, ["Fracture", "Tibial", "Dislocation"])

print("=== 9. CG 2035 Lower Extremity MRI Knee Meniscal / Cruciate ===")
search_text_on_pages(550, 571, ["Lachman", "McMurray", "Meniscal"])

print("=== 10. CG 2035 Lower Extremity MRI AVN / Hip ===")
search_text_on_pages(550, 571, ["Avascular", "Osteonecrosis"])

print("=== 11. CG 2037 Lumbar Spine MRI Infection / Malignancy ===")
search_text_on_pages(592, 613, ["Infection", "Discitis", "Osteomyelitis", "Malignancy"])

print("=== 12. CG 2046 Whole Body PET/CT Lymphoma ===")
search_text_on_pages(737, 807, ["Lymphoma", "Hodgkin"])

print("=== 13. CG 2046 Whole Body PET/CT Lung Cancer ===")
search_text_on_pages(737, 807, ["Non-Small Cell", "Lung Cancer", "Solitary Pulmonary"])

print("=== 14. CG 2047 Sinus CT Chronic Rhinosinusitis ===")
search_text_on_pages(808, 825, ["Chronic", "Rhinosinusitis", "Maximal Medical"])

print("=== 15. CG 2065 Upper Extremity MRI Rotator Cuff Positive Signs ===")
search_text_on_pages(1012, 1034, ["Bear hug", "Drop arm", "Empty can"])
