import json
import csv
from pathlib import Path
import pymupdf

def run_ipm_audit():
    doc26 = pymupdf.open('rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf')
    doc25 = pymupdf.open('rulebook_collection/domains/interventional_pain_management/policies/historical/2025 Evolent Interventional Pain Management Guidelines.pdf')
    
    print(f"2026 IPM pages: {doc26.page_count}, 2025 IPM pages: {doc25.page_count}")
    
    def find_guidelines(doc):
        gls = []
        for p in range(1, doc.page_count + 1):
            txt = doc[p-1].get_text('text')
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            for l in lines[:10]:
                if "guideline" in l.lower() and ("for" in l.lower() or "table of contents" in l.lower()):
                    if not gls or gls[-1]['title'] != l:
                        gls.append({'title': l, 'start_page': p})
                    break
        return gls

    g26 = find_guidelines(doc26)
    g25 = find_guidelines(doc25)
    
    print("\n=== 2026 IPM Guidelines ===")
    for g in g26:
        print(f"  Page {g['start_page']}: {g['title']}")
        
    print("\n=== 2025 IPM Guidelines ===")
    for g in g25:
        print(f"  Page {g['start_page']}: {g['title']}")

if __name__ == '__main__':
    run_ipm_audit()
