import pymupdf

doc = pymupdf.open("rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf")
# Background of Guideline 2009
for pno in range(176, 180):
    txt = doc[pno].get_text()
    if "background" in txt.lower():
        print(f"=== Background on physical page {pno+1} ===")
        for l in txt.split("\n"):
            if l.strip():
                print("  ", l.strip().encode("ascii", "replace").decode("ascii"))
