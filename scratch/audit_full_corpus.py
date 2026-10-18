"""Comprehensive audit of all 61 clinical guidelines + Preamble + EPOS 2067."""
import fitz
import re
import json
from pathlib import Path

doc_guidelines = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')
doc_epos = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/EPOS 2067 for Place of Service - Radiology 2026_final.pdf')

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', 'r', encoding='utf-8') as f:
    existing_rules = json.load(f)

# Group rules by guideline ID
rules_by_gid = {}
for r in existing_rules:
    rid = r['rule_id']
    m = re.match(r'RULE-ADV-([A-Z0-9]+)-', rid)
    if m:
        pfx = m.group(1)
        if pfx.startswith('CG'):
            gid = 'CG-' + pfx[2:]
        elif pfx.startswith('EPOS'):
            gid = 'EPOS-' + pfx[4:]
        else:
            gid = pfx
        rules_by_gid.setdefault(gid, []).append(r)

# Map of true physical start pages
guideline_starts = []
for pno in range(1, len(doc_guidelines) + 1):
    txt = doc_guidelines[pno-1].get_text()
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    if not lines: continue
    first_few = " ".join(lines[:4])
    m_p1 = re.search(r'Page\s+1\s+of\s+(\d+)', first_few, re.IGNORECASE)
    if m_p1:
        total_p = int(m_p1.group(1))
        m_cg = re.search(r'Evolent Clinical Guideline\s+(\d+)', first_few, re.IGNORECASE)
        if m_cg:
            gid = f"CG-{m_cg.group(1)}"
            title = m_cg.group(0)
            guideline_starts.append((gid, pno, pno + total_p - 1, total_p))

output_data = []

# Audit Preamble
output_data.append({
    'guideline_id': 'PREAMBLE',
    'title': 'Guidelines for Clinical Review Determination Preamble and Development Process',
    'pages': 'pp. 2-3',
    'rules_count': len(rules_by_gid.get('PREAMBLE', [])),
    'rule_ids': [r['rule_id'] for r in rules_by_gid.get('PREAMBLE', [])]
})

# Audit all 61 guidelines
for gid, start_p, end_p, total_p in guideline_starts:
    g_rules = rules_by_gid.get(gid, [])
    output_data.append({
        'guideline_id': gid,
        'title': f'Evolent Clinical Guideline {gid[3:]}',
        'pages': f'pp. {start_p}-{end_p} ({total_p} pgs)',
        'rules_count': len(g_rules),
        'rule_ids': [r['rule_id'] for r in g_rules]
    })

# Audit EPOS 2067
output_data.append({
    'guideline_id': 'EPOS-2067',
    'title': 'Evolent Place of Service Policy 2067 for Radiology',
    'pages': 'pp. 1-11 (11 pgs)',
    'rules_count': len(rules_by_gid.get('EPOS-2067', [])),
    'rule_ids': [r['rule_id'] for r in rules_by_gid.get('EPOS-2067', [])]
})

with open('scratch/audit_summary_initial.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2)

print(f"Audited {len(output_data)} governed units.")
for item in output_data[:10]:
    print(f"{item['guideline_id']:10s} | {item['pages']:20s} | Rules: {item['rules_count']:2d} | IDs: {item['rule_ids']}")
