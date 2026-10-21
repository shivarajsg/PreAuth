import csv
import json

with open('rulebook_collection/manifests/rule_policy_fidelity_audit.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")
hrr = [r for r in rows if r['audit_status'] == 'HUMAN_REVIEW_REQUIRED']
pv = [r for r in rows if r['audit_status'] == 'PARTIALLY_VERIFIED']

print("\n=== 7 HUMAN_REVIEW_REQUIRED RULES ===")
for r in hrr:
    print(f"Rule: {r['rule_id']} | Domain: {r['domain']} | Page: {r['physical_page']} | File: {r['source_file']}")
    print(f"   Section: {r['source_section']}")
    print(f"   Issue: {r['issue_description']}")

print(f"\n=== 43 PARTIALLY_VERIFIED RULES ({len(pv)}) ===")
for r in pv[:10]:
    print(f"Rule: {r['rule_id']} | Domain: {r['domain']} | Page: {r['physical_page']}")
    print(f"   Section: {r['source_section']}")
    print(f"   Issue: {r['issue_description']}")
