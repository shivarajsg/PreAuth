import os, json

domains_dir = 'rulebook_collection/domains'
summary = {}

for d in sorted(os.listdir(domains_dir)):
    if d == 'advanced_imaging':
        continue
    domain_path = os.path.join(domains_dir, d)
    rules_file = os.path.join(domain_path, 'rules', 'draft_rules.json')
    domain_summary_file = os.path.join(domain_path, 'domain_summary.md')
    
    rules = []
    if os.path.exists(rules_file):
        with open(rules_file, 'r', encoding='utf-8') as f:
            rules = json.load(f)
            
    services = sorted(list(set([r.get('clinical_service_or_procedure') for r in rules if r.get('clinical_service_or_procedure')])))
    rule_types = sorted(list(set([r.get('rule_type') for r in rules if r.get('rule_type')])))
    
    summary[d] = {
        'total_rules': len(rules),
        'services': services[:15],
        'total_services': len(services),
        'rule_types': rule_types
    }

print(json.dumps(summary, indent=2))
