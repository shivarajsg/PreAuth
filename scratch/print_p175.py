import pymupdf

doc = pymupdf.open("rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf")
txt = doc[174].get_text() # physical page 175
for l in txt.split("\n"):
    if l.strip():
        print("  ", l.strip().encode("ascii", "replace").decode("ascii"))
