import os, sys, hashlib, json, csv
from pathlib import Path
import fitz

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path('.')
RULEBOOK_DIR = ROOT_DIR / 'rulebook_collection'

# 1. Scan all PDFs
pdf_paths = sorted(list(RULEBOOK_DIR.rglob('*.pdf')))
print(f"Total PDFs found: {len(pdf_paths)}")

inventory = []
hashes = {}

for p in pdf_paths:
    rel_path = p.relative_to(ROOT_DIR).as_posix()
    size = p.stat().st_size
    with open(p, 'rb') as f:
        file_bytes = f.read()
        sha = hashlib.sha256(file_bytes).hexdigest()
    
    try:
        doc = fitz.open(p)
        page_count = len(doc)
        title = doc.metadata.get('title', '')
        author = doc.metadata.get('author', '')
        doc.close()
    except Exception as e:
        page_count = -1
        title = f"Error: {e}"
        author = ""
        
    parts = p.relative_to(RULEBOOK_DIR).parts
    top_folder = parts[0]
    domain = parts[1] if top_folder == 'domains' else top_folder
    
    if sha in hashes:
        hashes[sha].append(rel_path)
    else:
        hashes[sha] = [rel_path]
        
    inventory.append({
        'rel_path': rel_path,
        'filename': p.name,
        'size_bytes': size,
        'sha256': sha,
        'page_count': page_count,
        'top_folder': top_folder,
        'domain': domain,
        'pdf_title': title
    })

print(f"Unique SHA-256 hashes: {len(hashes)}")
duplicates = {k: v for k, v in hashes.items() if len(v) > 1}
print(f"Hashes with multiple files (duplicates): {len(duplicates)}")
for sha, files in duplicates.items():
    print(f"  Hash {sha[:12]}... ({len(files)} files):")
    for f in files:
        print(f"    - {f}")

# Save detailed scan
with open('scratch/all_pdfs_scan.json', 'w', encoding='utf-8') as f:
    json.dump(inventory, f, indent=2)
