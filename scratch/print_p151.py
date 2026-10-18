import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')
lines = doc[150].get_text().split('\n')
for i, l in enumerate(lines[10:40]):
    safe = l.encode('ascii', errors='replace').decode('ascii')
    print(f"[{i:2d}] {safe}")
