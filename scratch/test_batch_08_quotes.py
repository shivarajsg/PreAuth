"""Examine sections and exact text for Batch 08 guidelines."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

def get_page_text(pno):
    return doc[pno-1].get_text()

# CG 2056: Thoracic CT (pp. 903-922)
print("=== CG 2056 Thoracic Spine CT ===")
for p in range(905, 908):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Evaluation", "Deficits", "Pain", "Trauma", "Deformity"]):
            print(f"p.{p}: {line.strip()[:80]}")

# CG 2057: Thoracic MRI (pp. 923-945)
print("\n=== CG 2057 Thoracic Spine MRI ===")
for p in range(925, 928):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Evaluation", "Deficits", "Pain", "Trauma", "Deformity"]):
            print(f"p.{p}: {line.strip()[:80]}")

# CG 2061: Unlisted Study (pp. 953-962)
print("\n=== CG 2061 Unlisted Study ===")
for p in range(954, 957):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Unlisted", "Multiple Myeloma", "Radiation"]):
            print(f"p.{p}: {line.strip()[:80]}")

# CG 2062: Upper Extremity CT (pp. 963-986)
print("\n=== CG 2062 Upper Extremity CT ===")
for p in range(965, 968):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Upper Extremity Pain", "Joint Specific", "Trauma", "Fracture"]):
            print(f"p.{p}: {line.strip()[:80]}")

# CG 2063: Upper Extremity CTA (pp. 987-998)
print("\n=== CG 2063 Upper Extremity CTA ===")
for p in range(989, 991):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Peripheral Vascular", "Trauma", "Thoracic Outlet"]):
            print(f"p.{p}: {line.strip()[:80]}")

# CG 2064: Upper Extremity MRA (pp. 999-1011)
print("\n=== CG 2064 Upper Extremity MRA ===")
for p in range(1001, 1003):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Peripheral Vascular", "Trauma", "Thoracic Outlet"]):
            print(f"p.{p}: {line.strip()[:80]}")

# CG 2065: Upper Extremity MRI (pp. 1012-1034)
print("\n=== CG 2065 Upper Extremity MRI ===")
for p in range(1014, 1017):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Upper Extremity Pain", "Joint Specific", "Shoulder", "Rotator"]):
            print(f"p.{p}: {line.strip()[:80]}")

# CG 2066: Urgent/Emergent (pp. 1035-1041)
print("\n=== CG 2066 Urgent/Emergent ===")
for p in range(1036, 1038):
    txt = get_page_text(p)
    for line in txt.split("\n"):
        if any(w in line for w in ["INDICATIONS", "Emergent", "Urgent"]):
            print(f"p.{p}: {line.strip()[:80]}")
