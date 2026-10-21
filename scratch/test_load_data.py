import json
import csv
from pathlib import Path

ROOT = Path("d:/PreAuth")
DATA_FILE = ROOT / "scratch" / "detailed_50_rules_data.json"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    rules = json.load(f)

print(f"Loaded {len(rules)} rules for detailed remediation modeling.")
# Check the 7 HRR rules and 43 PV rules
hrr = [r for r in rules if r["audit_status"] == "HUMAN_REVIEW_REQUIRED"]
pv = [r for r in rules if r["audit_status"] == "PARTIALLY_VERIFIED"]
print(f"HRR: {len(hrr)}, PV: {len(pv)}")
