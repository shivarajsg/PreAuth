import csv
from collections import Counter
from pathlib import Path

with open('rulebook_collection/manifests/coverage_gap_reconciliation.csv', encoding='utf-8') as f:
    recon = list(csv.DictReader(f))

print(f"Total recon rows: {len(recon)}")

# Load audited 43 rules
audited_43 = set()
for b in [1, 2, 3, 4]:
    with open(f'reports/batch_{b:02d}_policy_audit.csv', encoding='utf-8') as f:
        audited_43.update(r['rule_id'] for r in csv.DictReader(f))

# Let's inspect the NOT_COVERED records
not_covered = [r for r in recon if r['coverage_status_in_gap_report'] == 'NOT_COVERED']
print(f"Total NOT_COVERED: {len(not_covered)}")
for nc in not_covered:
    gid = nc['gap_item_id']
    dom = nc['domain']
    pg = nc['physical_page']
    sec = nc['source_section']
    ctype = nc['criterion_type']
    summ = nc['clinical_criterion_summary'][:60]
    print(f"{gid} ({dom}) | p.{pg} | {sec} | {ctype} | {summ}...")

# Check HUMAN_REVIEW_REQUIRED records
hrr = [r for r in recon if r['coverage_status_in_gap_report'] == 'HUMAN_REVIEW_REQUIRED']
print(f"\nTotal HUMAN_REVIEW_REQUIRED: {len(hrr)}")
for h in hrr:
    print(f"{h['gap_item_id']} | {h['source_section']} | {h['clinical_criterion_summary'][:60]}...")
