import os
import hashlib
from collections import Counter, defaultdict

pdf_files = []
for root, dirs, files in os.walk("rulebook_collection"):
    for f in files:
        if f.lower().endswith(".pdf"):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, "rulebook_collection").replace("\\", "/")
            pdf_files.append((full_path, rel_path))

print(f"Total physical PDF files in rulebook_collection: {len(pdf_files)}")

# Group by top directory under rulebook_collection
top_dirs = Counter(p[1].split("/")[0] for p in pdf_files)
for k, v in sorted(top_dirs.items()):
    print(f"  rulebook_collection/{k}: {v} files")

# Group by domains if under domains/
domain_counts = Counter(p[1].split("/")[1] for p in pdf_files if p[1].startswith("domains/"))
print(f"\nPDFs across 9 domains ({sum(domain_counts.values())} total):")
for d, c in sorted(domain_counts.items()):
    print(f"  domains/{d}: {c} files")

# Calculate SHA-256 for all 101 physical PDFs
hash_to_files = defaultdict(list)
file_to_hash = {}
for full_path, rel_path in pdf_files:
    h = hashlib.sha256()
    with open(full_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    digest = h.hexdigest()
    hash_to_files[digest].append(rel_path)
    file_to_hash[rel_path] = digest

print(f"\nTotal unique SHA-256 hashes across 101 files: {len(hash_to_files)}")

duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
print(f"Number of content hashes with multiple physical copies: {len(duplicates)}")
for h, files in duplicates.items():
    print(f"  Hash {h[:12]}... has {len(files)} copies:")
    for f in files:
        print(f"    - rulebook_collection/{f}")
