import csv
from pathlib import Path

ROOT = Path("d:/PreAuth")
AI_GAPS_FILE = ROOT / "rulebook_collection" / "manifests" / "advanced_imaging_coverage_gap_report.csv"
IPM_GAPS_FILE = ROOT / "rulebook_collection" / "manifests" / "ipm_coverage_gap_report.csv"

with open(AI_GAPS_FILE, "r", encoding="utf-8") as f:
    ai_gaps = list(csv.DictReader(f))
with open(IPM_GAPS_FILE, "r", encoding="utf-8") as f:
    ipm_gaps = list(csv.DictReader(f))

covered = [g for g in ai_gaps + ipm_gaps if g["coverage_status"] == "COVERED"]
print(f"Total COVERED items: {len(covered)}")
for g in covered[:15]:
    print(f"[{g['domain']}] {g['guideline_id']} | p.{g['physical_page']} | Type: {g['criterion_type']}")
    print(f"   Section: {g['section_header']}")
    print(f"   Rules: {g['mapped_rule_ids']}")
    print(f"   Notes: {g['notes_and_gap_analysis'][:90]}")
    print("-" * 60)
