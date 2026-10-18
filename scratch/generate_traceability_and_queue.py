"""Generate source_to_rule_traceability.csv and human_review_queue.csv for MedRule Phase 2A."""
import json
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"

def main():
    draft_rules_path = RULES_DIR / "draft_rules.json"
    traceability_path = RULES_DIR / "source_to_rule_traceability.csv"
    queue_path = RULES_DIR / "human_review_queue.csv"

    with open(draft_rules_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    # 1. Generate source_to_rule_traceability.csv
    traceability_fields = [
        "rule_id",
        "policy_id",
        "policy_version",
        "document_type",
        "pdf_filename",
        "guideline_section",
        "pdf_page_number",
        "verbatim_source_text",
        "extraction_status",
        "human_reviewer",
        "review_date"
    ]

    traceability_rows = []
    for r in rules:
        # Determine policy_id from rule_id or source_section
        # rule_id is e.g. RULE-ADV-CG2000-001 -> CG-2000
        parts = r["rule_id"].split("-")
        policy_id = parts[2] if len(parts) >= 3 else "CG-2000"

        source_file = r.get("source_file", "")
        pdf_filename = Path(source_file).name if source_file else ""

        page_info = r.get("source_page", {})
        if isinstance(page_info, dict):
            page_num = page_info.get("physical_page", "")
            printed_page = page_info.get("printed_page", "")
            page_str = f"Physical p. {page_num} ({printed_page})" if printed_page else str(page_num)
        else:
            page_str = str(page_info)

        row = {
            "rule_id": r["rule_id"],
            "policy_id": policy_id,
            "policy_version": r.get("policy_version", "2026 v2"),
            "document_type": r.get("document_type", "governing_policy"),
            "pdf_filename": pdf_filename,
            "guideline_section": r.get("source_section", ""),
            "pdf_page_number": page_str,
            "verbatim_source_text": r.get("source_quote", "").replace("\n", " ").strip(),
            "extraction_status": r.get("extraction_status", "DRAFT"),
            "human_reviewer": "",
            "review_date": ""
        }
        traceability_rows.append(row)

    with open(traceability_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=traceability_fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(traceability_rows)
    print(f"Generated {traceability_path} with {len(traceability_rows)} rows.")

    # 2. Generate human_review_queue.csv
    queue_fields = [
        "rule_id",
        "policy_id",
        "issue_category",
        "source_text_excerpt",
        "clinical_ambiguity_description",
        "missing_element",
        "recommended_action",
        "status"
    ]

    queue_rows = [
        {
            "rule_id": "RULE-ADV-CG2000-003",
            "policy_id": "CG2000",
            "issue_category": "advisory_language_vs_binding_criteria",
            "source_text_excerpt": "Magnetic resonance imaging (MRI) should be considered in patients younger than 35 years of age to minimize radiation exposure",
            "clinical_ambiguity_description": (
                "Guideline uses advisory normative term 'should be considered' rather than binding imperative "
                "'is required' or 'is non-covered'. It is clinically ambiguous whether a CT request for an age < 35 patient "
                "must be denied with a recommendation for MR enterography, or if CT remains approvable if clinician explicitly opts for CT."
            ),
            "missing_element": "Payer administrative determination on whether advisory modality redirection triggers formal adverse determination vs clinical peer-to-peer recommendation.",
            "recommended_action": (
                "Clinical Review Committee must clarify policy intent: (1) Configure as hard block requiring MR enterography first "
                "unless contraindication exists, OR (2) Configure as soft advisory alert to ordering provider while allowing CT if clinical rationale documented."
            ),
            "status": "PENDING_CLINICAL_REVIEW"
        },
        {
            "rule_id": "RULE-ADV-CG2000-002",
            "policy_id": "CG2000",
            "issue_category": "ambiguity_in_prior_imaging_modality",
            "source_text_excerpt": "When initial workup with x-ray and/or ultrasound is inconclusive, negative, or does not provide sufficient detail to guide management",
            "clinical_ambiguity_description": (
                "The source guideline uses 'x-ray and/or ultrasound'. Certain clinical sub-indications (e.g. suspected appendicitis vs suspected bowel obstruction) "
                "have distinct clinical standard of care for which prior imaging modality is appropriate (US for pelvic/appendiceal, X-ray for obstruction/free air). "
                "The rule condition allows either (ANY_OF), but individual sub-indications may clinically necessitate an ultrasound specifically."
            ),
            "missing_element": "Indication-specific imaging prerequisite granularity.",
            "recommended_action": (
                "Maintain general prerequisite rule RULE-ADV-CG2000-002 as ANY_OF(x_ray, ultrasound) inconclusive/negative, "
                "and ensure condition-specific child rules (such as RULE-ADV-CG2000-004) mandate ultrasound explicitly when required."
            ),
            "status": "DRAFT_REQUIRES_SECONDARY_REVIEW"
        },
        {
            "rule_id": "RULE-ADV-CG2017-001",
            "policy_id": "CG2017",
            "issue_category": "conservative_therapy_documentation_breadth",
            "source_text_excerpt": "Six (6) consecutive weeks of conservative therapy within the previous six (6) months: Physical therapy, Chiropractic care, Pharmacotherapy (NSAIDs, muscle relaxants, oral steroids), or Activity modification",
            "clinical_ambiguity_description": (
                "The rule models conservative therapy requirement. While the list of acceptable modalities is enumerated, "
                "the guideline does not explicitly specify whether active physical therapy is mandatory or if pharmacotherapy alone across the 6 weeks satisfies the 6-week threshold."
            ),
            "missing_element": "Payer plan-level interpretation regarding whether multimodal conservative care (e.g. PT + medication) is mandatory or unimodal (medication only) suffices.",
            "recommended_action": (
                "Flag for payer contract-specific adjudication rule check during engine configuration. In deterministic schema, model as ANY_OF among listed modalities meeting temporal threshold."
            ),
            "status": "DRAFT_REQUIRES_SECONDARY_REVIEW"
        }
    ]

    with open(queue_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=queue_fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(queue_rows)
    print(f"Generated {queue_path} with {len(queue_rows)} rows.")

if __name__ == "__main__":
    main()
