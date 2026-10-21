import csv
from collections import Counter
from pathlib import Path

ROOT = Path("d:/PreAuth")
AI_GAPS_FILE = ROOT / "rulebook_collection" / "manifests" / "advanced_imaging_coverage_gap_report.csv"
IPM_GAPS_FILE = ROOT / "rulebook_collection" / "manifests" / "ipm_coverage_gap_report.csv"

with open(AI_GAPS_FILE, "r", encoding="utf-8") as f:
    ai_gaps = list(csv.DictReader(f))
with open(IPM_GAPS_FILE, "r", encoding="utf-8") as f:
    ipm_gaps = list(csv.DictReader(f))

all_gaps = ai_gaps + ipm_gaps
print(f"Total gap items: {len(all_gaps)} (AI: {len(ai_gaps)}, IPM: {len(ipm_gaps)})")

print("\nAI Guidelines breakdown:")
ai_guidelines = Counter(r["guideline_id"] for r in ai_gaps)
for gid, cnt in sorted(ai_guidelines.items()):
    print(f"  {gid}: {cnt} items")

print("\nIPM Guidelines breakdown:")
ipm_guidelines = Counter(r["guideline_id"] for r in ipm_gaps)
for gid, cnt in sorted(ipm_guidelines.items()):
    print(f"  {gid}: {cnt} items")

print("\nCoverage status breakdown across all 204 items:")
print(Counter(r["coverage_status"] for r in all_gaps))

print("\nCriterion types breakdown:")
print(Counter(r["criterion_type"] for r in all_gaps))
