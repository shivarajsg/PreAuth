from medrule_engine.rule_registry import RuleRegistry
import json

reg = RuleRegistry(include_archived=False)
reg.load_all_domains()

for r in reg.all_rules:
    for c in r.conditions.get('criteria', []):
        if c.get('comparator') in ['GREATER_THAN', 'LESS_THAN', 'GREATER_THAN_OR_EQUAL', 'LESS_THAN_OR_EQUAL']:
            print(f"{r.rule_id}: param={c.get('parameter')}, comp={c.get('comparator')}, val={c.get('value')}, unit={c.get('unit')}")
