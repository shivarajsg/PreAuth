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
not_covered = [g for g in all_gaps if g["coverage_status"] == "NOT_COVERED"]

print(f"Total NOT_COVERED: {len(not_covered)}")
for i, g in enumerate(not_covered, 1):
    print(f"[{i:02d}] Domain: {g['domain']} | Guideline: {g['guideline_id']} | Page: {g['physical_page']} | Type: {g['criterion_type']}")
    print(f"     Source Doc: {g['source_document']}")
    print(f"     Section: {g['section_header']}")
    print(f"     Summary: {g['clinical_criterion_summary']}")
    print(f"     Notes: {g['notes_and_gap_analysis']}")
    print("-" * 75)
