import pymupdf
import re

doc = pymupdf.open("rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf")

# Guideline 2009 is physical pages 172 to 191
print("Searching Guideline 2009 (pp. 172-191):")
for pno in range(171, 191):
    txt = doc[pno].get_text()
    if "thrombectomy" in txt.lower() or "occlusion" in txt.lower() or "ischemic" in txt.lower():
        print(f"Physical Page {pno+1}:")
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ["thrombectomy", "occlusion", "ischemic", "stroke"]):
                print("  ", line.strip())
