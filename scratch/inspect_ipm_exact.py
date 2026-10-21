import sys
import fitz
from pathlib import Path

doc = fitz.open('rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf')

out = []

def dump_range(name, start_p, end_p):
    out.append("="*70)
    out.append(f"SECTION: {name} (Pages {start_p}-{end_p})")
    for p in range(start_p, end_p + 1):
        out.append(f"\n--- Physical Page {p} (Printed Page {doc[p-1].get_text().splitlines()[0] if doc[p-1].get_text() else ''}) ---")
        lines = [l.strip() for l in doc[p-1].get_text().split('\n') if l.strip()]
        for l in lines:
            out.append(f"  {l}")

dump_range("EPIDURAL PUMP TRIALS (CG 1751)", 17, 21)
dump_range("FACET BLOCKS (CG 1753)", 31, 35)
dump_range("SI INJECTIONS (CG 1756)", 57, 61)
dump_range("SPINAL CORD STIMULATION (CG 1757)", 78, 82)
dump_range("SYMPATHETIC BLOCKS (CG 1758)", 89, 93)

Path('scratch/ipm_exact_indications.txt').write_text('\n'.join(out), encoding='utf-8')
print("Successfully generated scratch/ipm_exact_indications.txt")
