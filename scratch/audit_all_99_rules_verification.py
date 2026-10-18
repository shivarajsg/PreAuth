"""Forensic audit of all 99 existing rules."""
import fitz
import json
import re

doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')
doc_epos = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/EPOS 2067 for Place of Service - Radiology 2026_final.pdf')

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    rules = json.load(f)

audit_results = []

for r in rules:
    rid = r['rule_id']
    src_file = r['source_file']
    pno = r['source_page']['physical_page']
    quote = r['source_quote']
    sec = r['source_section']
    de = r['decision_effect']
    rt = r['rule_type']
    
    # Choose document
    curr_doc = doc_epos if 'EPOS' in src_file else doc
    
    # Page text
    ptxt = curr_doc[pno - 1].get_text()
    
    # Check quote match
    norm_txt = re.sub(r'\s+', ' ', ptxt).lower()
    norm_q = re.sub(r'\s+', ' ', quote).lower()
    quote_found = norm_q in norm_txt
    
    # Check section title mention
    sec_first = sec.split('/')[0].strip()
    sec_found = sec_first.lower() in norm_txt or any(w.lower() in norm_txt for w in sec_first.split() if len(w) > 4)
    
    # Evaluate Boolean logic and parameters
    conds = r['conditions']
    op = conds.get('operator')
    criteria = conds.get('criteria', [])
    params = [c.get('parameter') for c in criteria]
    
    audit_results.append({
        'rule_id': rid,
        'guideline': rid.split('-')[2],
        'page': pno,
        'quote_found': quote_found,
        'rule_type': rt,
        'decision_effect': de,
        'operator': op,
        'criteria_count': len(criteria),
        'params': params,
        'notes': []
    })

print(f"Audited {len(audit_results)} existing rules.")
failed_quotes = [a for a in audit_results if not a['quote_found']]
print(f"Quote verification failures: {len(failed_quotes)}")

with open('scratch/audited_99_rules.json', 'w', encoding='utf-8') as f:
    json.dump(audit_results, f, indent=2)
