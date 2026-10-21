from pathlib import Path
txt = Path('scratch/batch4_policy_pages.txt').read_text(encoding='utf-8')

out = []
for p in [905, 906, 925, 926, 965]:
    marker = f'--- Physical Page {p}'
    idx = txt.find(marker)
    if idx != -1:
        next_idx = txt.find('--- Physical Page', idx + len(marker))
        out.append('='*50)
        out.append(f'PHYSICAL PAGE {p}:')
        if next_idx != -1:
            out.append(txt[idx:next_idx].strip())
        else:
            out.append(txt[idx:idx+2000].strip())

Path('scratch/ai_pages_out.txt').write_text('\n'.join(out), encoding='utf-8')
print("Written to scratch/ai_pages_out.txt")
