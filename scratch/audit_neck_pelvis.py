"""Audit physical pages between 638 and 737."""
import fitz

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

def scan_range(start, end):
    for p in range(start, end + 1):
        txt = doc[p-1].get_text()
        for line in txt.split('\n'):
            line_s = line.strip()
            if 'Guideline' in line_s and ('2040' in line_s or '2041' in line_s or '2042' in line_s or '2043' in line_s):
                safe_l = line_s.encode('ascii', errors='replace').decode('ascii')
                print(f"p.{p:4d}: {safe_l}")
                break

scan_range(635, 740)
