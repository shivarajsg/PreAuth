import json
import csv
from pathlib import Path
import pymupdf

def run():
    with open('rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)
        
    print(f"Total IPM rules: {len(rules)}")
    for r in rules:
        print(f"  {r['rule_id']}: {r.get('rule_name', '')} | pg: {r['source_page']['physical_page']} | sec: {r.get('source_section', '')}")

if __name__ == '__main__':
    run()
