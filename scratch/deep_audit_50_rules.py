import csv
import json
from pathlib import Path
import fitz  # PyMuPDF

# Paths
ROOT = Path("d:/PreAuth")
AUDIT_CSV = ROOT / "rulebook_collection" / "manifests" / "rule_policy_fidelity_audit.csv"
AI_RULES_FILE = ROOT / "rulebook_collection" / "domains" / "advanced_imaging" / "rules" / "draft_rules.json"
IPM_RULES_FILE = ROOT / "rulebook_collection" / "domains" / "interventional_pain_management" / "rules" / "draft_rules.json"

AI_PDF = ROOT / "rulebook_collection" / "domains" / "advanced_imaging" / "policies" / "current" / "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
AI_EPOS_PDF = ROOT / "rulebook_collection" / "domains" / "advanced_imaging" / "policies" / "current" / "EPOS 2067 for Place of Service - Radiology 2026_final.pdf"
IPM_PDF = ROOT / "rulebook_collection" / "domains" / "interventional_pain_management" / "policies" / "current" / "2026 Evolent Interventional Pain Management Guidelines.pdf"
IPM_EPOS_PDF = ROOT / "rulebook_collection" / "domains" / "interventional_pain_management" / "policies" / "current" / "EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf"

# Load rules
with open(AI_RULES_FILE, "r", encoding="utf-8") as f:
    ai_rules = {r["rule_id"]: r for r in json.load(f)}
with open(IPM_RULES_FILE, "r", encoding="utf-8") as f:
    ipm_rules = {r["rule_id"]: r for r in json.load(f)}

all_rules = {**ai_rules, **ipm_rules}

# Load audit rows
with open(AUDIT_CSV, "r", encoding="utf-8") as f:
    audit_rows = list(csv.DictReader(f))

unresolved = [r for r in audit_rows if r["audit_status"] in ("PARTIALLY_VERIFIED", "HUMAN_REVIEW_REQUIRED")]

print(f"Total unresolved: {len(unresolved)}")

# Open PDF docs
docs = {
    "AI": fitz.open(AI_PDF),
    "AI_EPOS": fitz.open(AI_EPOS_PDF),
    "IPM": fitz.open(IPM_PDF),
    "IPM_EPOS": fitz.open(IPM_EPOS_PDF),
}

results = []
for item in unresolved:
    rid = item["rule_id"]
    rule = all_rules.get(rid, {})
    domain = item["domain"]
    status = item["audit_status"]
    page_num = int(item["physical_page"])
    source_file = item["source_file"]
    
    # Determine doc
    if "EPOS 2067" in source_file:
        doc = docs["AI_EPOS"]
    elif "Advanced Imaging" in source_file:
        doc = docs["AI"]
    elif "EPOS 1755" in source_file:
        doc = docs["IPM_EPOS"]
    else:
        doc = docs["IPM"]
        
    page_text = ""
    if 1 <= page_num <= len(doc):
        page_text = doc[page_num - 1].get_text()
        
    results.append({
        "rule_id": rid,
        "domain": domain,
        "audit_status": status,
        "page_num": page_num,
        "source_section": item["source_section"],
        "issue_description": item["issue_description"],
        "conditions": rule.get("conditions", {}),
        "source_quote": rule.get("source_quote", ""),
        "decision_effect": rule.get("decision_effect", ""),
        "human_review_required": item["human_review_required"],
        "page_text_len": len(page_text),
        "page_snippet": page_text[:300].replace("\n", " ")
    })

print(f"Loaded {len(results)} rules for deep inspection.")
with open(ROOT / "scratch" / "unresolved_rules_extracted.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Saved scratch/unresolved_rules_extracted.json")
