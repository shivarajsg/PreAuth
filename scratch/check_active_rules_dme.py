import json
from pathlib import Path

ai_rules_file = Path('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json')
ipm_rules_file = Path('rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json')

with open(ai_rules_file, 'r', encoding='utf-8') as f:
    ai_rules = json.load(f)
with open(ipm_rules_file, 'r', encoding='utf-8') as f:
    ipm_rules = json.load(f)

all_active = ai_rules + ipm_rules
print(f'Total active rules loaded from draft_rules: {len(all_active)}')

terms = [
    'CP.MP.107',
    'CP.MP',
    'DME and O&P',
    'Durable Medical Equipment',
    '9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29',
    'e67ca165b078fdb32caea282ca6b5a486c39f12d0633fb52b8e7e7199c212fb4'
]

for t in terms:
    matches = []
    for r in all_active:
        r_str = json.dumps(r)
        if t.lower() in r_str.lower():
            matches.append(r.get('rule_id'))
    print(f'Term "{t}": {len(matches)} matches in active rules: {matches}')
