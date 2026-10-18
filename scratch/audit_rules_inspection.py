"""Inspect existing rules and their coverage."""
import json

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

for r in rules:
    if any(k in r['rule_id'] for k in ['CG2008', 'CG2012', 'CG2016', 'CG2017', 'CG2020', 'CG2035', 'CG2037', 'CG2038']):
        print(f"{r['rule_id']} | {r['clinical_service_or_procedure']} | {r['source_section'][:45]} | p.{r['source_page']['physical_page']}")
