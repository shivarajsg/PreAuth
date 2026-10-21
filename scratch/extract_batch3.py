import json
from pathlib import Path
import pymupdf

ROOT = Path(".")
ai_rules_file = ROOT / "rulebook_collection/domains/advanced_imaging/rules/draft_rules.json"
with open(ai_rules_file, "r", encoding="utf-8") as f:
    ai_rules = {r["rule_id"]: r for r in json.load(f)}

ai_pdf_path = ROOT / "rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
doc = pymupdf.open(ai_pdf_path)

batch3_ids = [
    "RULE-ADV-CG2032-001",
    "RULE-ADV-CG2035-001",
    "RULE-ADV-CG2035-002",
    "RULE-ADV-CG2036-001",
    "RULE-ADV-CG2037-001",
    "RULE-ADV-CG2037-002",
    "RULE-ADV-CG2042-001",
    "RULE-ADV-CG2045-001",
    "RULE-ADV-CG2054-001",
    "RULE-ADV-CG2055-001",
]

extracted = []
for rid in batch3_ids:
    rule = ai_rules[rid]
    page_info = rule.get("source_page", {})
    phys_page = page_info.get("physical_page") if isinstance(page_info, dict) else int(page_info)
    printed_page = page_info.get("printed_page", "") if isinstance(page_info, dict) else ""
    
    page_text = doc[phys_page - 1].get_text()
    
    extracted.append({
        "rule_id": rid,
        "existing_status": rule.get("extraction_status", "DRAFT"),
        "domain": rule.get("domain", "advanced_imaging"),
        "source_file": rule.get("source_file", ""),
        "physical_page": phys_page,
        "printed_page": printed_page,
        "source_section": rule.get("source_section", ""),
        "source_quote": rule.get("source_quote", ""),
        "conditions": rule.get("conditions", {}),
        "decision_effect": rule.get("decision_effect", ""),
        "page_text": page_text
    })

with open("scratch/batch3_extracted.json", "w", encoding="utf-8") as f:
    json.dump(extracted, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(extracted)} rules for Batch 3.")
