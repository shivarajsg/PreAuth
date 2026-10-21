import sys
from pathlib import Path
txt = Path('scratch/batch4_policy_pages.txt').read_text(encoding='utf-8')

out = []
sections = [
    ("EPIDURAL INJECTIONS", "=== EPIDURAL INJECTIONS (CG-EPIDURAL) ===", "=== EPIDURAL PUMP TRIALS"),
    ("EPIDURAL PUMP TRIALS", "=== EPIDURAL PUMP TRIALS (CG-EPIDURAL-PUMPS) ===", "=== FACET BLOCKS"),
    ("FACET BLOCKS", "=== FACET BLOCKS (CG-FACET) ===", "=== SACROILIAC INJECTIONS"),
    ("SACROILIAC INJECTIONS", "=== SACROILIAC INJECTIONS (CG-SI) ===", "=== SPINAL CORD STIMULATION"),
    ("SPINAL CORD STIMULATION", "=== SPINAL CORD STIMULATION (CG-SCS) ===", "=== SYMPATHETIC BLOCKS"),
    ("SYMPATHETIC BLOCKS", "=== SYMPATHETIC BLOCKS (CG-SYMPATHETIC) ===", None)
]

for name, start_m, end_m in sections:
    out.append("="*60)
    out.append(f"SECTION: {name}")
    s_idx = txt.find(start_m)
    if s_idx != -1:
        if end_m:
            e_idx = txt.find(end_m, s_idx)
            chunk = txt[s_idx:e_idx]
        else:
            chunk = txt[s_idx:]
        out.append(chunk.strip())
    else:
        out.append(f"Could not find marker {start_m}")

Path('scratch/ipm_pages_out.txt').write_text('\n'.join(out), encoding='utf-8')
print("Written to scratch/ipm_pages_out.txt")
