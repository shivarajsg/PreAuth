"""Compare guideline_coverage_inventory.csv with true physical page starts."""
import csv
import pandas as pd

# Load previous inventory
df_prev = pd.read_csv('rulebook_collection/domains/advanced_imaging/rules/guideline_coverage_inventory.csv')

# Load true page starts from scratch/audit_guideline_page_starts.py
import fitz, re
doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

true_starts = {}
for pno in range(1, len(doc) + 1):
    txt = doc[pno-1].get_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    if not lines: continue
    first_few = " ".join(lines[:4])
    m_p1 = re.search(r'Page\s+1\s+of\s+(\d+)', first_few, re.IGNORECASE)
    if m_p1:
        total_p = int(m_p1.group(1))
        m_cg = re.search(r'Evolent Clinical Guideline\s+(\d+)', first_few, re.IGNORECASE)
        if m_cg:
            gid = f"CG-{m_cg.group(1)}"
            true_starts[gid] = (pno, pno + total_p - 1, total_p)

print(f"{'Guideline':<10} | {'Prev Start':<10} | {'True Start':<10} | {'Prev End':<10} | {'True End':<10} | {'Match?':<6}")
print("-" * 65)
mismatch_count = 0
for idx, row in df_prev.iterrows():
    gid = row['guideline_id']
    if gid in true_starts:
        t_start, t_end, t_len = true_starts[gid]
        p_start = row['physical_start_page']
        p_end = row['physical_end_page']
        match = (t_start == p_start and t_end == p_end)
        if not match:
            mismatch_count += 1
            print(f"{gid:<10} | {p_start:<10} | {t_start:<10} | {p_end:<10} | {t_end:<10} | {'MISMATCH':<6}")

print(f"\nTotal guidelines with physical page boundary mismatches in previous inventory: {mismatch_count}")
