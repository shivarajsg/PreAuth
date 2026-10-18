"""Audit Step 1: Verify the Source Corpus against master_pdf_inventory.csv."""
import hashlib, csv
from pathlib import Path
import fitz

base = Path('.')
manifest = base / 'rulebook_collection/manifests/master_pdf_inventory.csv'
versions = base / 'rulebook_collection/manifests/policy_versions.csv'

with open(manifest, 'r', encoding='utf-8') as f:
    m_rows = list(csv.DictReader(f))

adv_rows = [r for r in m_rows if r.get('domain') == 'advanced_imaging']
print(f"Advanced imaging rows in master_pdf_inventory.csv: {len(adv_rows)}")
for r in adv_rows:
    p = base / r['local_relative_path']
    exists = p.exists()
    if exists:
        data = p.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        hash_ok = (h.lower() == r['sha256'].lower())
        doc = fitz.open(p)
        pg_cnt = len(doc)
        doc.close()
        print(f"{r['document_id']} | {p.name} | Exists: {exists} | Hash Match: {hash_ok} | Pages: {pg_cnt} (Manifest: {r['page_count']}) | Version: {r['edition_or_version']} | Status: {r['version_status']}")
    else:
        print(f"{r['document_id']} | {r['filename']} | Exists: FALSE")
