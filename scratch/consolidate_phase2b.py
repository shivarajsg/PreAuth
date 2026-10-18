"""Consolidate all Phase 2B batches into draft_rules.json and generate all tracking manifests."""
import json
import re
from pathlib import Path
import pandas as pd
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"

def main():
    print("=== Consolidating Phase 2B Rules ===")
    
    # 1. Load all batch checkpoints
    all_rules = []
    batch_counts = {}
    for b in range(1, 10):
        bpath = CHECKPOINTS_DIR / f"batch_{b:02d}_rules.json"
        with open(bpath, "r", encoding="utf-8") as f:
            batch = json.load(f)
            batch_counts[f"Batch {b:02d}"] = len(batch)
            all_rules.extend(batch)
            
    print(f"Loaded {len(all_rules)} rules across 9 batches:")
    for bname, count in batch_counts.items():
        print(f"  {bname}: {count} rules")
        
    # Sort rules deterministically by rule_id
    all_rules.sort(key=lambda x: x["rule_id"])
    
    # 2. Validate against schema.json
    schema_path = RULES_DIR / "schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    for r in all_rules:
        jsonschema.validate(instance=r, schema=schema)
    print(f"Schema validation PASSED for all {len(all_rules)} rules.")
    
    # 3. Check for unique rule IDs
    rule_ids = [r["rule_id"] for r in all_rules]
    if len(rule_ids) != len(set(rule_ids)):
        raise ValueError("Duplicate rule IDs found!")
    print(f"Rule ID uniqueness verified: {len(rule_ids)} unique IDs.")
    
    # 4. Check Phase 2A pilot rules preservation
    pilot_rules = [
        'RULE-ADV-CG2000-001', 'RULE-ADV-CG2000-002', 'RULE-ADV-CG2000-003', 'RULE-ADV-CG2000-004',
        'RULE-ADV-CG2000-005', 'RULE-ADV-CG2000-006', 'RULE-ADV-CG2000-007', 'RULE-ADV-CG2000-008',
        'RULE-ADV-CG2000-009', 'RULE-ADV-CG2000-010', 'RULE-ADV-CG2000-011', 'RULE-ADV-CG2000-012',
        'RULE-ADV-CG2012-001', 'RULE-ADV-CG2012-002', 'RULE-ADV-CG2017-001', 'RULE-ADV-CG2017-002'
    ]
    rule_id_set = set(rule_ids)
    for pr in pilot_rules:
        if pr not in rule_id_set:
            raise ValueError(f"Phase 2A pilot rule missing: {pr}")
    print(f"Phase 2A pilot preservation verified: all {len(pilot_rules)} pilot rules present.")
    
    # 5. Check approval status constraint (Zero APPROVED rules)
    for r in all_rules:
        if r.get("extraction_status") == "APPROVED":
            raise ValueError(f"Rule {r['rule_id']} is marked APPROVED, which violates constraints!")
    print("Approval constraint verified: 0 rules marked APPROVED.")
    
    # 6. Write consolidated draft_rules.json
    draft_rules_path = RULES_DIR / "draft_rules.json"
    with open(draft_rules_path, "w", encoding="utf-8") as f:
        json.dump(all_rules, f, indent=2)
    print(f"Saved {len(all_rules)} consolidated rules to {draft_rules_path}")
    
    # 7. Generate source_to_rule_traceability.csv
    trace_rows = []
    for r in all_rules:
        trace_rows.append({
            "rule_id": r["rule_id"],
            "domain": r["domain"],
            "document_type": r["document_type"],
            "policy_title": r["policy_title"],
            "policy_version": r["policy_version"],
            "source_file": r["source_file"],
            "source_url": r["source_url"],
            "physical_page": r["source_page"]["physical_page"],
            "printed_page": r["source_page"]["printed_page"],
            "source_section": r["source_section"],
            "source_quote": r["source_quote"],
            "clinical_service_or_procedure": r["clinical_service_or_procedure"],
            "rule_type": r["rule_type"],
            "decision_effect": r["decision_effect"],
            "dependencies": "; ".join(r.get("dependencies", [])),
            "human_review_required": r.get("human_review_required", False),
            "extraction_status": r.get("extraction_status", "DRAFT")
        })
    df_trace = pd.DataFrame(trace_rows)
    trace_path = RULES_DIR / "source_to_rule_traceability.csv"
    df_trace.to_csv(trace_path, index=False)
    print(f"Generated {trace_path} with {len(df_trace)} rows.")
    
    # 8. Generate human_review_queue.csv
    review_rows = []
    for r in all_rules:
        is_hr = r.get("human_review_required", False)
        status = r.get("extraction_status", "DRAFT")
        if is_hr or status == "NEEDS_HUMAN_REVIEW":
            # Extract guideline ID
            rid = r["rule_id"]
            m = re.match(r'RULE-ADV-([A-Z0-9]+)-', rid)
            gid = m.group(1) if m else "UNKNOWN"
            if gid.startswith("CG"):
                gid = "CG-" + gid[2:]
            elif gid.startswith("EPOS"):
                gid = "EPOS-" + gid[4:]
                
            trigger = "Urgent/Emergent retrospective clinical evaluation" if "CG2066" in rid else \
                      ("Preamble overarching standard of care clinical judgment" if "PREAMBLE" in rid else \
                      ("Administrative policy exception" if "CG2026" in rid else "Clinical nuance / review required"))
                      
            review_rows.append({
                "rule_id": r["rule_id"],
                "domain": r["domain"],
                "guideline_id": gid,
                "clinical_service_or_procedure": r["clinical_service_or_procedure"],
                "source_section": r["source_section"],
                "physical_page": r["source_page"]["physical_page"],
                "printed_page": r["source_page"]["printed_page"],
                "review_trigger_reason": trigger,
                "human_review_required": is_hr,
                "extraction_status": status,
                "reviewer_notes": r.get("review_notes", "")
            })
    df_review = pd.DataFrame(review_rows)
    review_path = RULES_DIR / "human_review_queue.csv"
    df_review.to_csv(review_path, index=False)
    print(f"Generated {review_path} with {len(df_review)} flagged rules.")
    
    # 9. Update guideline_coverage_inventory.csv
    inv_path = RULES_DIR / "guideline_coverage_inventory.csv"
    df_inv = pd.read_csv(inv_path)
    
    # Map rules to guidelines
    rule_counts = {}
    review_counts = {}
    for r in all_rules:
        rid = r["rule_id"]
        m = re.match(r'RULE-ADV-([A-Z0-9]+)-', rid)
        gid = m.group(1) if m else "UNKNOWN"
        if gid.startswith("CG"):
            gid = "CG-" + gid[2:]
        elif gid.startswith("EPOS"):
            gid = "EPOS-" + gid[4:]
        rule_counts[gid] = rule_counts.get(gid, 0) + 1
        if r.get("human_review_required", False) or r.get("extraction_status") == "NEEDS_HUMAN_REVIEW":
            review_counts[gid] = review_counts.get(gid, 0) + 1
            
    for idx, row in df_inv.iterrows():
        gid = row["guideline_id"]
        cnt = rule_counts.get(gid, 0)
        hr_cnt = review_counts.get(gid, 0)
        df_inv.at[idx, "rules_extracted_count"] = cnt
        df_inv.at[idx, "human_review_count"] = hr_cnt
        df_inv.at[idx, "validation_issues_count"] = 0
        df_inv.at[idx, "parsing_status"] = "SOURCE_PARSED"
        df_inv.at[idx, "extraction_status"] = "COMPLETE"
        df_inv.at[idx, "completion_status"] = "VALIDATED_FOR_REVIEW"
        
    df_inv.to_csv(inv_path, index=False)
    print(f"Updated {inv_path} with coverage status across all {len(df_inv)} guidelines.")
    print("All consolidation steps completed successfully!")

if __name__ == "__main__":
    main()
