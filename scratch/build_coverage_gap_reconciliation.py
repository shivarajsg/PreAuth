import csv
from pathlib import Path
from collections import Counter

ROOT = Path(".")
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

out_file = REPORTS_DIR / "coverage_gap_reconciliation.csv"

# Load the 204 gap records from manifest
with open("rulebook_collection/manifests/coverage_gap_reconciliation.csv", encoding="utf-8") as f:
    raw_recons = list(csv.DictReader(f))

# Load the 43 audited rules
audited_43 = {}
for b in [1, 2, 3, 4]:
    with open(REPORTS_DIR / f"batch_{b:02d}_policy_audit.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            audited_43[r["rule_id"]] = (b, r)

fieldnames = [
    "gap_item_id",
    "domain",
    "guideline_id",
    "source_document",
    "source_section",
    "physical_page",
    "printed_page",
    "criterion_type",
    "clinical_criterion_summary",
    "mapped_rule_ids",
    "coverage_status_in_gap_report",
    "reconciliation_classification",
    "overlap_with_43_audited_rules",
    "reconciliation_rationale"
]

rows_out = []

for r in raw_recons:
    gid = r["gap_item_id"]
    dom = r["domain"]
    gid_guide = r["guideline_id"]
    source_doc = r["governing_policy"]
    sec = r["source_section"]
    p_page = r["physical_page"]
    pr_page = r["printed_page"]
    ctype = r["criterion_type"]
    summ = r["clinical_criterion_summary"]
    mapped = r["mapped_rule_ids"]
    cov_status = r["coverage_status_in_gap_report"]

    # Check overlap with 43 audited rules
    mapped_list = [m.strip() for m in mapped.split(";") if m.strip() and m.strip() != "NONE"]
    overlapping_rules = [m for m in mapped_list if m in audited_43]
    overlap_str = "; ".join(overlapping_rules) if overlapping_rules else "NONE"

    # Determine classification
    classification = ""
    rationale = ""

    # 1. Ambiguous policy language
    if gid in ["GAP-ADV-007", "GAP-ADV-019", "GAP-ADV-082", "GAP-ADV-099"]:
        classification = "ambiguous policy language"
        if gid == "GAP-ADV-007":
            rationale = "Policy contains discretionary wording ('MRI should be considered in young patients') rather than definitive denial; flagged in RULE-ADV-CG2000-003."
        elif gid == "GAP-ADV-019":
            rationale = "Anti-unbundling billing constraint requiring combined CT Abdomen/Pelvis codes; flagged in RULE-ADV-CG2001-001."
        elif gid == "GAP-ADV-082":
            rationale = "Policy note specifies initial X-ray is 'preferred, NOT required', conflicting with strict rule requirement; flagged in RULE-ADV-CG2035-002."
        elif gid == "GAP-ADV-099":
            rationale = "Age boundary condition ('over the age of 65' vs >= 65) requires medical director boundary clarification; flagged in RULE-ADV-CG2042-001."

    # 2. Advisory-only item
    elif ctype in ["NON_EXECUTABLE", "GOVERNANCE_FRAMEWORK"] or "Supporting Document" in sec or \
         "superseded" in summ.lower() or "tip sheet" in summ.lower() or "quick reference" in summ.lower():
        classification = "advisory-only item"
        if ctype == "NON_EXECUTABLE":
            rationale = "Non-executable policy section containing background evidence, societal literature, CPT code descriptions, or legal disclaimers. Cannot generate prior-authorization approvals or denials."
        elif ctype == "GOVERNANCE_FRAMEWORK":
            rationale = "Overarching clinical governance framework requiring physician clinical judgment. Non-deterministic; blocked from automated compilation."
        else:
            rationale = "Provider educational aid, checklist, or superseded historical attestation form. Does not constitute binding clinical criteria."

    # 3. Distinct missing criterion
    elif gid in ["GAP-IPM-005", "GAP-IPM-013", "GAP-IPM-014", "GAP-IPM-020", "GAP-IPM-022", "GAP-IPM-023", "GAP-IPM-026", "GAP-IPM-029", "GAP-IPM-003"]:
        classification = "distinct missing criterion"
        if gid == "GAP-IPM-005":
            rationale = "Epidural steroid injection for spinal stenosis with neurogenic claudication represents an explicit uncodified clinical indication in CG 1750."
        elif gid == "GAP-IPM-013":
            rationale = "Mandatory second confirmatory diagnostic facet block (>= 70% relief) prior to radiofrequency neurotomy is an uncodified clinical prerequisite in CG 1753."
        elif gid == "GAP-IPM-014":
            rationale = "Explicit clinical exclusion: Therapeutic intra-articular facet steroid injections are unproven/non-covered in CG 1753."
        elif gid == "GAP-IPM-020":
            rationale = "Cardinal clinical diagnostic criterion: Cluster of at least 3 of 8 positive provocative physical exam tests for SI joint pain in CG 1756."
        elif gid == "GAP-IPM-022":
            rationale = "Clinical indications for permanent intraspinal drug infusion pump in intractable pain or severe spasticity in CG 1751."
        elif gid == "GAP-IPM-023":
            rationale = "Mandatory prerequisite of successful trial (>= 50% relief) and formal psychological clearance prior to permanent pump in CG 1751."
        elif gid == "GAP-IPM-026":
            rationale = "Specific indication for Dorsal Root Ganglion (DRG) stimulation restricted to CRPS of lower extremities in CG 1757."
        elif gid == "GAP-IPM-029":
            rationale = "Specific differentiated anatomical sympathetic blocks (celiac plexus, superior hypogastric, ganglion impar) in CG 1758."
        elif gid == "GAP-IPM-003":
            rationale = "Clinical exception criteria permitting hospital outpatient setting under EPOS 1755 (cardiopulmonary disease, severe OSA, bleeding disorder)."

    # 4. Shared-rule candidate
    elif ctype in ["DOCUMENTATION_REQUIREMENT", "FREQUENCY_LIMIT", "PROCEDURAL_LIMIT", "CONSERVATIVE_THERAPY"] or \
         gid in ["GAP-IPM-007", "GAP-IPM-008", "GAP-IPM-009", "GAP-IPM-011", "GAP-IPM-015", "GAP-IPM-018", "GAP-IPM-021", "GAP-IPM-027", "GAP-IPM-030", "GAP-ADV-005"]:
        classification = "shared-rule candidate"
        rationale = "Cross-cutting clinical constraint, procedural level limiter, frequency interval, or documentation prerequisite that applies across multiple procedures and should be centralized as a shared engine gate."

    # 5. Duplicate
    elif cov_status == "COVERED" and (not mapped_list or mapped_list == ["NONE"]):
        classification = "duplicate"
        rationale = "Redundant policy entry or duplicate subsection already represented by sibling procedural indication cluster."

    # 6. Already implemented elsewhere
    elif cov_status == "COVERED" and mapped_list and mapped_list != ["NONE"]:
        classification = "already implemented elsewhere"
        if overlap_str != "NONE":
            rationale = f"Policy section is implemented in active rulebook ({mapped}), audited in Phase 2 policy fidelity batch ({overlap_str}). Sub-criteria fidelity gaps tracked in audit report."
        else:
            rationale = f"Policy section is implemented in active rulebook by compiled deterministic rule(s): {mapped}."

    else:
        classification = "already implemented elsewhere"
        rationale = f"Covered by active procedural rule inventory ({mapped})."

    rows_out.append({
        "gap_item_id": gid,
        "domain": dom,
        "guideline_id": gid_guide,
        "source_document": source_doc,
        "source_section": sec,
        "physical_page": p_page,
        "printed_page": pr_page,
        "criterion_type": ctype,
        "clinical_criterion_summary": summ,
        "mapped_rule_ids": mapped,
        "coverage_status_in_gap_report": cov_status,
        "reconciliation_classification": classification,
        "overlap_with_43_audited_rules": overlap_str,
        "reconciliation_rationale": rationale
    })

with open(out_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Generated {len(rows_out)} coverage gap reconciliation rows in {out_file}")
counts = Counter(r["reconciliation_classification"] for r in rows_out)
for c, cnt in counts.items():
    print(f"  {c}: {cnt}")

overlap_count = sum(1 for r in rows_out if r["overlap_with_43_audited_rules"] != "NONE")
print(f"Total rows overlapping with 43 audited rules: {overlap_count}")
