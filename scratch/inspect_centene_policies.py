import csv
import fitz

print("=== Centene Documents in Master PDF Inventory ===")
with open('rulebook_collection/manifests/master_pdf_inventory.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['domain'] == 'centene_dme_orthotics_prosthetics':
            print(f"{r['document_id']} | {r['document_type']} | {r['document_title']} | {r['local_relative_path']}")
            if r['document_id'] == 'DOC-CEN-005':
                doc = fitz.open(r['local_relative_path'])
                print("--- First page text of DOC-CEN-005 ---")
                print(doc[0].get_text()[:800])
                print("---------------------------------------")
