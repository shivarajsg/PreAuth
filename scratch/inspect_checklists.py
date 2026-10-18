import fitz
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('rulebook_collection/manifests/master_pdf_inventory.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['document_id'] in ['DOC-CARD-005', 'DOC-GEN-003', 'DOC-GEN-004', 'DOC-PHY-010', 'DOC-PHY-012']:
            print(f"=== {r['document_id']} | {r['domain']} | {r['document_title']} ===")
            doc = fitz.open(r['local_relative_path'])
            for p in range(len(doc)):
                print(f"--- P{p+1} ---")
                print(doc[p].get_text()[:600])
