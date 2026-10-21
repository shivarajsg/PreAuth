import json
import csv
from pathlib import Path
import pymupdf

def analyze_policies():
    ai_doc = pymupdf.open('rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')
    ipm_doc = pymupdf.open('rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf')
    
    with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
        ai_rules = json.load(f)
    with open('rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json', 'r', encoding='utf-8') as f:
        ipm_rules = json.load(f)
        
    print(f"AI 2026 doc pages: {ai_doc.page_count}, active AI rules: {len(ai_rules)}")
    print(f"IPM 2026 doc pages: {ipm_doc.page_count}, active IPM rules: {len(ipm_rules)}")

if __name__ == '__main__':
    analyze_policies()
