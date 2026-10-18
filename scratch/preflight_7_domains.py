import csv
from pathlib import Path
import pandas as pd
import fitz

BASE_DIR = Path(".")
MANIFESTS_DIR = BASE_DIR / "rulebook_collection" / "manifests"
DOMAINS_DIR = BASE_DIR / "rulebook_collection" / "domains"

domains = [
    "cardiology",
    "musculoskeletal_surgery",
    "interventional_pain_management",
    "radiation_oncology",
    "physical_medicine",
    "sleep_health",
    "genetic_testing"
]

df_master = pd.read_csv(MANIFESTS_DIR / "master_pdf_inventory.csv")

for d in domains:
    print(f"\n=======================================================")
    print(f"DOMAIN: {d.upper()}")
    print(f"=======================================================")
    
    sub = df_master[df_master["domain"] == d]
    print(f"Total documents in master inventory: {len(sub)}")
    for _, row in sub.iterrows():
        rel_path = row.get("local_relative_path", "")
        doc_path = BASE_DIR / rel_path
        exists = doc_path.exists()
        pages = 0
        if exists:
            try:
                doc = fitz.open(doc_path)
                pages = len(doc)
                doc.close()
            except Exception as e:
                pages = -1
        print(f"[{row.get('document_id')}] Type: {row.get('document_type')} | Ver: {row.get('edition_or_version')} | Pages: {pages} (manifest: {row.get('page_count')})")
        print(f"  Title: {row.get('document_title')}")
        print(f"  Path: {rel_path} (exists={exists})")
        print(f"  Effective: {row.get('effective_from')} | Status: {row.get('version_status')}")
