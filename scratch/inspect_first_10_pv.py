import csv
import json
from pathlib import Path

ROOT = Path(".")
audit_csv = ROOT / "rulebook_collection/manifests/rule_policy_fidelity_audit.csv"
with open(audit_csv, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

pv_rules = [r for r in rows if r["audit_status"] == "PARTIALLY_VERIFIED"]

print(f"Total PV rules: {len(pv_rules)}")
print("First 10 PV rules:")
for i, r in enumerate(pv_rules[:10], 1):
    print(f"[{i:02d}] {r['rule_id']} | {r['domain']} | p.{r['physical_page']} | {r['source_section']}")
