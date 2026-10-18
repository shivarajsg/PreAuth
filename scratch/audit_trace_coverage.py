import glob
import csv
import os

print("=== Domain Artifact Audits ===")
for path in sorted(glob.glob('rulebook_collection/domains/*/rules/draft_rules.json')):
    dname = path.replace('\\', '/').split('/')[2]
    r_dir = os.path.dirname(path)
    
    # Traceability
    trace_path = os.path.join(r_dir, 'source_to_rule_traceability.csv')
    trace_count = len(list(csv.DictReader(open(trace_path, encoding='utf-8')))) if os.path.isfile(trace_path) else 'MISSING'
    
    # Coverage
    cov_path = os.path.join(r_dir, 'guideline_coverage_inventory.csv')
    cov_count = len(list(csv.DictReader(open(cov_path, encoding='utf-8')))) if os.path.isfile(cov_path) else 'MISSING'
    
    # Completeness audit if present
    comp_path = os.path.join(r_dir, 'completeness_audit.csv')
    comp_count = len(list(csv.DictReader(open(comp_path, encoding='utf-8')))) if os.path.isfile(comp_path) else 'N/A'
    
    print(f"{dname:35} | Traceability: {trace_count:3} | Coverage: {cov_count:3} | Completeness: {comp_count}")
