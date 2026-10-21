import csv
from pathlib import Path

ROOT = Path("d:/PreAuth")
with open(ROOT / "rulebook_collection/manifests/advanced_imaging_coverage_gap_report.csv", "r", encoding="utf-8") as f:
    ai = list(csv.DictReader(f))
with open(ROOT / "rulebook_collection/manifests/ipm_coverage_gap_report.csv", "r", encoding="utf-8") as f:
    ipm = list(csv.DictReader(f))

all_gaps = ai + ipm
not_covered = [g for g in all_gaps if g["coverage_status"] == "NOT_COVERED"]
for i, g in enumerate(not_covered[:11], 1):
    print(f"[{i:02d}] {g['domain']} | {g['guideline_id']} | p.{g['physical_page']} | {g['section_header']} | {g['clinical_criterion_summary'][:70]}")
