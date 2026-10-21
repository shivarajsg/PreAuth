import csv
from pathlib import Path

with open('rulebook_collection/manifests/coverage_gap_reconciliation.csv', encoding='utf-8') as f:
    recon = list(csv.DictReader(f))

special = [r for r in recon if r['coverage_status_in_gap_report'] in ['NOT_COVERED', 'HUMAN_REVIEW_REQUIRED']]
for s in special:
    gid = s['gap_item_id']
    dom = s['domain']
    st = s['coverage_status_in_gap_report']
    sec = s['source_section']
    ctype = s['criterion_type']
    summ = s['clinical_criterion_summary']
    mapped = s['mapped_rule_ids']
    print(f"{gid} | {dom} | {st} | {ctype} | {sec} | Mapped: {mapped}")
    print(f"   {summ}")
