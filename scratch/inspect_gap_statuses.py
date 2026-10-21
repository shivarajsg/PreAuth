import csv
from pathlib import Path

ROOT = Path("d:/PreAuth")
AI_GAPS_FILE = ROOT / "rulebook_collection" / "manifests" / "advanced_imaging_coverage_gap_report.csv"
IPM_GAPS_FILE = ROOT / "rulebook_collection" / "manifests" / "ipm_coverage_gap_report.csv"

with open(AI_GAPS_FILE, "r", encoding="utf-8") as f:
    ai_gaps = list(csv.DictReader(f))
with open(IPM_GAPS_FILE, "r", encoding="utf-8") as f:
    ipm_gaps = list(csv.DictReader(f))

all_gaps = ai_gaps + ipm_gaps

print(f"Total: {len(all_gaps)}")

# Check NOT_COVERED items
not_covered = [g for g in all_gaps if g["coverage_status"] == "NOT_COVERED"]
print(f"NOT_COVERED count: {len(not_covered)}")
for g in not_covered[:10]:
    print(f"[{g['domain']}] {g['guideline_id']} | p.{g['physical_page']} | Type: {g['criterion_type']}")
    print(f"   Section: {g['section_header']}")
    print(f"   Summary: {g['clinical_criterion_summary'][:100]}")
    print(f"   Notes: {g['notes_and_gap_analysis'][:100]}")

# Check HUMAN_REVIEW_REQUIRED items
hrr_gaps = [g for g in all_gaps if g["coverage_status"] == "HUMAN_REVIEW_REQUIRED"]
print(f"\nHUMAN_REVIEW_REQUIRED count: {len(hrr_gaps)}")
for g in hrr_gaps:
    print(f"[{g['domain']}] {g['guideline_id']} | p.{g['physical_page']} | Type: {g['criterion_type']}")
    print(f"   Section: {g['section_header']}")
    print(f"   Summary: {g['clinical_criterion_summary'][:100]}")
    print(f"   Notes: {g['notes_and_gap_analysis'][:100]}")
