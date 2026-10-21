import csv
import json
from pathlib import Path
import pymupdf

ROOT = Path("d:/PreAuth")
AUDIT_CSV = ROOT / "rulebook_collection" / "manifests" / "rule_policy_fidelity_audit.csv"
AI_RULES_FILE = ROOT / "rulebook_collection" / "domains" / "advanced_imaging" / "rules" / "draft_rules.json"
IPM_RULES_FILE = ROOT / "rulebook_collection" / "domains" / "interventional_pain_management" / "rules" / "draft_rules.json"

AI_PDF = ROOT / "rulebook_collection" / "domains" / "advanced_imaging" / "policies" / "current" / "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
AI_EPOS_PDF = ROOT / "rulebook_collection" / "domains" / "advanced_imaging" / "policies" / "current" / "EPOS 2067 for Place of Service - Radiology 2026_final.pdf"
IPM_PDF = ROOT / "rulebook_collection" / "domains" / "interventional_pain_management" / "policies" / "current" / "2026 Evolent Interventional Pain Management Guidelines.pdf"
IPM_EPOS_PDF = ROOT / "rulebook_collection" / "domains" / "interventional_pain_management" / "policies" / "current" / "EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf"

with open(AI_RULES_FILE, "r", encoding="utf-8") as f:
    ai_rules = {r["rule_id"]: r for r in json.load(f)}
with open(IPM_RULES_FILE, "r", encoding="utf-8") as f:
    ipm_rules = {r["rule_id"]: r for r in json.load(f)}
all_rules = {**ai_rules, **ipm_rules}

with open(AUDIT_CSV, "r", encoding="utf-8") as f:
    audit_rows = list(csv.DictReader(f))

unresolved = [r for r in audit_rows if r["audit_status"] in ("PARTIALLY_VERIFIED", "HUMAN_REVIEW_REQUIRED")]

docs = {
    "AI": pymupdf.open(AI_PDF),
    "AI_EPOS": pymupdf.open(AI_EPOS_PDF),
    "IPM": pymupdf.open(IPM_PDF),
    "IPM_EPOS": pymupdf.open(IPM_EPOS_PDF),
}

analysis_records = []

for item in unresolved:
    rid = item["rule_id"]
    rule = all_rules.get(rid, {})
    domain = item["domain"]
    status = item["audit_status"]
    page_num = int(item["physical_page"])
    source_file = item["source_file"]
    
    if "EPOS 2067" in source_file:
        doc = docs["AI_EPOS"]
        policy_name = "EPOS 2067 for Place of Service - Radiology 2026"
    elif "Advanced Imaging" in source_file:
        doc = docs["AI"]
        policy_name = "2026 Evolent Clinical Guidelines - Advanced Imaging v2"
    elif "EPOS 1755" in source_file:
        doc = docs["IPM_EPOS"]
        policy_name = "EPOS 1755 for Place of Service - Interventional Pain Management 2026"
    else:
        doc = docs["IPM"]
        policy_name = "2026 Evolent Interventional Pain Management Guidelines"
        
    page_text = ""
    if 1 <= page_num <= len(doc):
        page_text = doc[page_num - 1].get_text()
        
    analysis_records.append({
        "rule_id": rid,
        "domain": domain,
        "audit_status": status,
        "policy_id": item["policy_id"],
        "policy_version": item["policy_version"],
        "policy_name": policy_name,
        "source_file": source_file,
        "physical_page": page_num,
        "source_section": item["source_section"],
        "issue_description": item["issue_description"],
        "rule_quote": rule.get("source_quote", ""),
        "conditions": rule.get("conditions", {}),
        "decision_effect": rule.get("decision_effect", ""),
        "full_page_text": page_text
    })

with open(ROOT / "scratch" / "detailed_50_rules_data.json", "w", encoding="utf-8") as f:
    json.dump(analysis_records, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(analysis_records)} rules with full PDF text.")
