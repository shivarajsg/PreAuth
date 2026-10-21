import json
from pathlib import Path
import pymupdf

ROOT = Path(".")
ai_rules_file = ROOT / "rulebook_collection/domains/advanced_imaging/rules/draft_rules.json"
with open(ai_rules_file, "r", encoding="utf-8") as f:
    ai_rules = {r["rule_id"]: r for r in json.load(f)}

ai_pdf_path = ROOT / "rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
doc = pymupdf.open(ai_pdf_path)

batch2_ids = [
    "RULE-ADV-CG2008-003",
    "RULE-ADV-CG2008-004",
    "RULE-ADV-CG2009-002",
    "RULE-ADV-CG2015-001",
    "RULE-ADV-CG2016-001",
    "RULE-ADV-CG2017-001",
    "RULE-ADV-CG2017-002",
    "RULE-ADV-CG2017-003",
    "RULE-ADV-CG2022-001",
    "RULE-ADV-CG2030-001",
]

extracted = []
for rid in batch2_ids:
    rule = ai_rules[rid]
    page_info = rule.get("source_page", {})
    phys_page = page_info.get("physical_page") if isinstance(page_info, dict) else int(page_info)
    printed_page = page_info.get("printed_page", "") if isinstance(page_info, dict) else ""
    
    # Extract page text
    page_text = doc[phys_page - 1].get_text()
    # Also extract adjacent page if needed (prev and next)
    prev_text = doc[phys_page - 2].get_text() if phys_page > 1 else ""
    next_text = doc[phys_page].get_text() if phys_page < len(doc) else ""
    
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
        "page_text": page_text,
        "prev_page_text": prev_text[:500],
        "next_page_text": next_text[:500]
    })

with open("scratch/batch2_extracted.json", "w", encoding="utf-8") as f:
    json.dump(extracted, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(extracted)} rules for Batch 2 deep inspection.")
