import json
from pathlib import Path

rules_13 = [
    'RULE-ADV-CG2056-001', 'RULE-ADV-CG2056-002', 'RULE-ADV-CG2057-001', 'RULE-ADV-CG2057-002', 'RULE-ADV-CG2062-001',
    'RULE-IPM-CGEPIDURALINJECTIONS-001', 'RULE-IPM-CGEPIDURALINJECTIONS-002', 'RULE-IPM-CGEPIDURALPUMPTRIALS-001',
    'RULE-IPM-CGFACETBLOCKS-001', 'RULE-IPM-CGSIINJECTIONS-001', 'RULE-IPM-CGSPINALCORDSTIM-001',
    'RULE-IPM-CGSPINALCORDSTIM-002', 'RULE-IPM-CGSYMPATHETICBLOCKS-001'
]

rule_files = list(Path('rulebook_collection').glob('**/*.json'))
found = {}
for rf in rule_files:
    if 'node_modules' in str(rf): continue
    try:
        data = json.loads(rf.read_text(encoding='utf-8'))
        rules_list = []
        if isinstance(data, list):
            rules_list = data
        elif isinstance(data, dict):
            rules_list = data.get('rules', [])
        for r in rules_list:
            rid = r.get('rule_id')
            if rid in rules_13:
                found[rid] = (str(rf), r)
    except Exception as e:
        pass

output = {}
for rid in rules_13:
    if rid in found:
        file_path, r = found[rid]
        output[rid] = {
            'file_path': file_path,
            'title': r.get('title'),
            'source_citation': r.get('source_citation'),
            'source_page': r.get('source_page'),
            'source_quote': r.get('source_quote'),
            'extraction_status': r.get('extraction_status'),
            'conditions': r.get('conditions'),
            'indications': r.get('indications'),
            'prerequisites': r.get('prerequisites'),
            'exclusions': r.get('exclusions'),
            'rule_logic': r.get('rule_logic')
        }
        print(f"FOUND: {rid} in {file_path}")
    else:
        print(f"NOT FOUND: {rid}")

Path('scratch/batch4_extracted.json').write_text(json.dumps(output, indent=2), encoding='utf-8')
print("Saved to scratch/batch4_extracted.json")
