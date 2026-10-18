"""Extract exact verbatim quotes from physical PDF pages for the 15 omission rules."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

def examine_lines(pno, start_idx, count):
    lines = doc[pno-1].get_text().split('\n')
    for i, l in enumerate(lines[start_idx:start_idx+count]):
        safe = l.encode('ascii', errors='replace').decode('ascii')
        print(f"[{start_idx+i:3d}] {safe}")

# 1. CG-2008 Trauma (p.151)
print("=== CG-2008 Trauma p.151 ===")
examine_lines(151, 10, 20)

# 2. CG-2008 Thunderclap (p.149-150)
print("\n=== CG-2008 Thunderclap p.150 ===")
examine_lines(150, 15, 20)

# 3. CG-2009 Stroke / LVO (p.174-175)
print("\n=== CG-2009 Stroke p.175 ===")
examine_lines(175, 10, 20)

# 4. CG-2012 MS (p.226)
print("\n=== CG-2012 MS p.226 ===")
examine_lines(226, 10, 20)

# 5. CG-2012 Seizure (p.228)
print("\n=== CG-2012 Seizure p.228 ===")
examine_lines(228, 10, 20)

# 6. CG-2018 Hemoptysis (p.361)
print("\n=== CG-2018 Hemoptysis p.361 ===")
examine_lines(361, 10, 20)

# 7. CG-2020 Aortic Dissection (p.400)
print("\n=== CG-2020 Aortic Dissection p.400 ===")
examine_lines(400, 10, 20)

# 8. CG-2032 Fracture (p.504)
print("\n=== CG-2032 Fracture p.504 ===")
examine_lines(504, 10, 20)

# 9. CG-2035 Knee Meniscal / Lachman (p.553)
print("\n=== CG-2035 Knee p.553 ===")
examine_lines(553, 10, 20)

# 10. CG-2035 AVN Hip (p.554)
print("\n=== CG-2035 AVN Hip p.554 ===")
examine_lines(554, 10, 20)

# 11. CG-2037 Spine Infection / Malignancy (p.596)
print("\n=== CG-2037 Spine Infection p.596 ===")
examine_lines(596, 10, 20)

# 12. CG-2046 Lymphoma (p.742)
print("\n=== CG-2046 Lymphoma p.742 ===")
examine_lines(742, 10, 20)

# 13. CG-2046 Lung Cancer (p.744)
print("\n=== CG-2046 Lung Cancer p.744 ===")
examine_lines(744, 10, 20)

# 14. CG-2047 Chronic Sinusitis (p.811)
print("\n=== CG-2047 Chronic Sinusitis p.811 ===")
examine_lines(811, 10, 20)

# 15. CG-2065 Rotator cuff positive signs (p.1015)
print("\n=== CG-2065 Rotator Cuff p.1015 ===")
examine_lines(1015, 10, 20)
