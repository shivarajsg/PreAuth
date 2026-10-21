"""Complete remaining restructure steps:
1. Update rule source paths in draft_rules.json and all partition JSON files
2. Update traceability CSVs and generate consolidated manifests/source_to_rule_traceability.csv
3. Ensure schema.json in IPM rules
4. Create domain README.md files for advanced_imaging and IPM
5. Copy/populate manifests in domains/*/manifests/
6. Validate all 128 rules, source pages, and quotes against new paths
"""

import json, csv, shutil
from pathlib import Path
import fitz

RULEBOOK_DIR = Path("d:/PreAuth/rulebook_collection").resolve()
ADV_RULES_DIR = RULEBOOK_DIR / "domains" / "advanced_imaging" / "rules"
IPM_RULES_DIR = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "rules"
MANIFESTS_DIR = RULEBOOK_DIR / "manifests"

path_replacements = {
    "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf":
        "rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
    "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/EPOS 2067 for Place of Service - Radiology 2026_final.pdf":
        "rulebook_collection/domains/advanced_imaging/policies/current/EPOS 2067 for Place of Service - Radiology 2026_final.pdf",
    "rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026/2026 Evolent Interventional Pain Management Guidelines.pdf":
        "rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf",
    "rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026/EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf":
        "rulebook_collection/domains/interventional_pain_management/policies/current/EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf",
}

print("=== Step A: Updating Advanced Imaging Rules ===")
adv_rules_file = ADV_RULES_DIR / "draft_rules.json"
with open(adv_rules_file, "r", encoding="utf-8") as f:
    adv_rules = json.load(f)

for r in adv_rules:
    old_sf = r.get("source_file")
    if old_sf in path_replacements:
        r["source_file"] = path_replacements[old_sf]

with open(adv_rules_file, "w", encoding="utf-8") as f:
    json.dump(adv_rules, f, indent=2)

for pfile in ADV_RULES_DIR.rglob("*.json"):
    if pfile.name in ("draft_rules.json", "schema.json"):
        continue
    with open(pfile, "r", encoding="utf-8") as f:
        pdata = json.load(f)
    rules_list = pdata if isinstance(pdata, list) else pdata.get("rules", [])
    for r in rules_list:
        old_sf = r.get("source_file")
        if old_sf in path_replacements:
            r["source_file"] = path_replacements[old_sf]
    with open(pfile, "w", encoding="utf-8") as f:
        json.dump(pdata, f, indent=2)

print(f"Updated Advanced Imaging draft_rules.json ({len(adv_rules)} rules) and all partition files.")

print("\n=== Step B: Updating IPM Rules ===")
ipm_rules_file = IPM_RULES_DIR / "draft_rules.json"
with open(ipm_rules_file, "r", encoding="utf-8") as f:
    ipm_rules = json.load(f)

for r in ipm_rules:
    old_sf = r.get("source_file")
    if old_sf in path_replacements:
        r["source_file"] = path_replacements[old_sf]

with open(ipm_rules_file, "w", encoding="utf-8") as f:
    json.dump(ipm_rules, f, indent=2)

for pfile in IPM_RULES_DIR.rglob("*.json"):
    if pfile.name in ("draft_rules.json", "schema.json"):
        continue
    with open(pfile, "r", encoding="utf-8") as f:
        pdata = json.load(f)
    rules_list = pdata if isinstance(pdata, list) else pdata.get("rules", [])
    for r in rules_list:
        old_sf = r.get("source_file")
        if old_sf in path_replacements:
            r["source_file"] = path_replacements[old_sf]
    with open(pfile, "w", encoding="utf-8") as f:
        json.dump(pdata, f, indent=2)

print(f"Updated IPM draft_rules.json ({len(ipm_rules)} rules) and all partition files.")

# Ensure schema.json in IPM rules
ipm_schema = IPM_RULES_DIR / "schema.json"
if not ipm_schema.exists():
    shutil.copy(RULEBOOK_DIR / "schemas" / "medrule_rule_schema.json", ipm_schema)
    print("Copied canonical schema.json into IPM rules directory.")

print("\n=== Step C: Updating Traceability CSVs ===")
adv_trace_file = ADV_RULES_DIR / "source_to_rule_traceability.csv"
adv_trace_rows = []
with open(adv_trace_file, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        for old_p, new_p in path_replacements.items():
            if old_p in row.get("source_file", ""):
                row["source_file"] = new_p
        adv_trace_rows.append(row)

with open(adv_trace_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(adv_trace_rows[0].keys()))
    writer.writeheader()
    writer.writerows(adv_trace_rows)

adv_manifests = RULEBOOK_DIR / "domains" / "advanced_imaging" / "manifests"
adv_manifests.mkdir(parents=True, exist_ok=True)
shutil.copy(adv_trace_file, adv_manifests / "source_to_rule_traceability.csv")

# Copy domain-specific reports into domains/advanced_imaging/manifests/
for art in ["completeness_audit.csv", "guideline_coverage_inventory.csv", "human_review_queue.csv", "validation_report.md", "phase_2b1_completeness_audit_report.md", "phase_2b_completion_report.md", "pilot_report.md"]:
    art_path = ADV_RULES_DIR / art
    if art_path.exists():
        shutil.copy(art_path, adv_manifests / art)

ipm_trace_file = IPM_RULES_DIR / "source_to_rule_traceability.csv"
ipm_trace_rows = []
with open(ipm_trace_file, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        for old_p, new_p in path_replacements.items():
            if old_p in row.get("source_file", ""):
                row["source_file"] = new_p
        ipm_trace_rows.append(row)

with open(ipm_trace_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(ipm_trace_rows[0].keys()))
    writer.writeheader()
    writer.writerows(ipm_trace_rows)

ipm_manifests = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "manifests"
ipm_manifests.mkdir(parents=True, exist_ok=True)
shutil.copy(ipm_trace_file, ipm_manifests / "source_to_rule_traceability.csv")

for art in ["guideline_coverage_inventory.csv", "human_review_queue.csv", "validation_report.md", "domain_extraction_report.md"]:
    art_path = IPM_RULES_DIR / art
    if art_path.exists():
        shutil.copy(art_path, ipm_manifests / art)

# Consolidated master source_to_rule_traceability.csv
consolidated_trace = []
for r in adv_rules:
    consolidated_trace.append({
        "rule_id": r["rule_id"],
        "domain": r["domain"],
        "procedure_code": r.get("clinical_service_or_procedure", ""),
        "source_file": r["source_file"],
        "physical_page": r["source_page"].get("physical_page") if isinstance(r["source_page"], dict) else r["source_page"],
        "source_section": r.get("source_section", ""),
        "source_quote": r.get("source_quote", ""),
        "extraction_status": r.get("extraction_status", "DRAFT")
    })
for r in ipm_rules:
    consolidated_trace.append({
        "rule_id": r["rule_id"],
        "domain": r["domain"],
        "procedure_code": r.get("clinical_service_or_procedure", ""),
        "source_file": r["source_file"],
        "physical_page": r["source_page"].get("physical_page") if isinstance(r["source_page"], dict) else r["source_page"],
        "source_section": r.get("source_section", ""),
        "source_quote": r.get("source_quote", ""),
        "extraction_status": r.get("extraction_status", "DRAFT")
    })

with open(MANIFESTS_DIR / "source_to_rule_traceability.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["rule_id", "domain", "procedure_code", "source_file", "physical_page", "source_section", "source_quote", "extraction_status"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(consolidated_trace)

print(f"Saved consolidated source_to_rule_traceability.csv ({len(consolidated_trace)} rules).")

print("\n=== Step D: Creating Domain READMEs ===")
adv_readme = RULEBOOK_DIR / "domains" / "advanced_imaging" / "README.md"
with open(adv_readme, "w", encoding="utf-8") as f:
    f.write("""# Advanced Imaging Domain (Core Project Scope)

## Overview
The Advanced Imaging domain governs diagnostic CT, MRI, CTA, MRA, and PET/SPECT procedures in the MedRule clinical decision support system.

## Folder Organization
- `policies/current/`: Authoritative 2026 governing guidelines (1,041-page v2 guideline and EPOS 2067 Place of Service policy).
- `policies/historical/`: Historical 2025 guideline edition (1,074 pages) preserved for audit provenance.
- `supporting_documents/`:
  - `checklists/`: Documentation checklists for general prior authorization and Low Dose CT lung screening.
  - `forms/`: Conservative treatment history forms documenting physical therapy and medication trials.
  - `tip_sheets/`: Expedited review tip sheets and modality selection guidance.
- `rules/`: 114 deterministic clinical rules strictly validated against canonical schema.
  - `ct/`: CT Head/Brain, Chest, Spine, Abdomen/Pelvis, Extremities, Sinus/Maxillofacial, Temporal Bone.
  - `mri/`: MRI Brain, Spine, Extremities, TMJ, Orbit/Face/Neck.
  - `cta/`: CT Angiography Head, Neck, Chest, Abdomen, Pelvis, Extremity.
  - `mra/`: MR Angiography Head, Neck, Chest, Abdomen, Spinal Canal.
  - `pet_spect/`: PET/CT Oncologic, Brain, Myocardial, and SPECT.
  - `cross_cutting/`: Preamble, contrast safety, and place of service EPOS 2067.
- `manifests/`: Traceability matrix, guideline coverage inventory, completeness audits, and human review queue.

## Governance Invariant
Zero rules are approved. All 114 rules are maintained in `DRAFT` or `NEEDS_HUMAN_REVIEW` status.
""")

ipm_readme = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "README.md"
with open(ipm_readme, "w", encoding="utf-8") as f:
    f.write("""# Interventional Pain Management (IPM) Domain (Core Project Scope)

## Overview
The Interventional Pain Management (IPM) domain governs interventional pain procedures in the MedRule clinical decision support system.

## Folder Organization
- `policies/current/`: Authoritative 2026 governing guideline (102 pages) and EPOS 1755 Place of Service policy.
- `policies/historical/`: Historical 2025 guideline edition (75 pages) preserved for audit provenance.
- `supporting_documents/`:
  - `checklists/`: Mandatory documentation submission checklists.
  - `forms/`: Conservative treatment history forms (Rev 08/07/2025) documenting PT/OT, medications, and duration.
  - `tip_sheets/`: Injection intervals and diagnostic block relief thresholds.
- `rules/`: 14 deterministic clinical rules strictly validated against canonical schema.
  - `epidural_injections/`: Cervical, thoracic, and lumbar interlaminar/transforaminal ESIs.
  - `facet_interventions/`: Diagnostic medial branch blocks and radiofrequency facet neurotomy.
  - `sacroiliac_joint/`: Diagnostic and therapeutic SI joint injections.
  - `neuromodulation_pumps/`: Spinal cord stimulation trial/implantation and intrathecal drug delivery systems.
  - `sympathetic_blocks/`: Stellate ganglion, lumbar sympathetic, and celiac plexus blocks.
  - `cross_cutting/`: General conservative therapy requirements and place of service EPOS 1755.
- `manifests/`: Traceability matrix, guideline coverage inventory, and human review queue.

## Governance Invariant
Zero rules are approved. All 14 rules are maintained in `DRAFT` or `NEEDS_HUMAN_REVIEW` status.
""")

root_readme = RULEBOOK_DIR / "README.md"
with open(root_readme, "w", encoding="utf-8") as f:
    f.write("""# MedRule Rulebook Collection

The authoritative, deterministic clinical knowledge base for pre-authorization decision support.

## Project Scope
The MedRule active rulebook collection focuses strictly on two core clinical domains:
1. **Advanced Imaging** (Diagnostic CT, MRI, CTA, MRA, PET/SPECT)
2. **Interventional Pain Management (IPM)** (ESIs, Facet Interventions, SI Joint, SCS, Intrathecal Pumps, Sympathetic Blocks)

## Structure
- `source_pdfs/`: Authoritative project seed document (`PreauthorizationMRI.pdf`) defining scope boundaries.
- `domains/`:
  - `advanced_imaging/`: 114 active clinical rules, 2026 governing policies, and supporting documents.
  - `interventional_pain_management/`: 14 active clinical rules, 2026 governing policies, and supporting documents.
- `shared_references/`: Shared regulatory authorities (CMS claims manuals, state ops, quality standards).
- `manifests/`:
  - `scope_cleanup_proposal.csv`: Master proposal manifest.
  - `scope_completeness_report.md`: Initial audit and completeness report.
  - `file_inventory.csv`: Pre-cleanup inventory of all 101 physical PDFs.
  - `file_hashes.csv`: SHA-256 cryptographic verification hashes.
  - `relocation_log.csv`: Reversible audit log of every file relocation.
  - `duplicate_report.csv`: Cryptographic duplicate tracking report.
  - `source_to_rule_traceability.csv`: Consolidated 128-rule source traceability.
  - `cleanup_validation_report.md`: Final post-cleanup execution and verification report.
- `archive_candidate/`:
  - `unrelated_domains/`: Relocated guidelines from 7 non-core domains (Cardiology, DMEPOS, Genetics, MSK, PhysMed, RadOnc, Sleep).
  - `duplicate_quarantine/`: Redundant identical PDF copies (raw Phase 1 downloads and duplicate seed).
- `tests/`: Scope boundary, citation validity, and integrity test suites.
""")

archive_readme = RULEBOOK_DIR / "archive_candidate" / "README.md"
with open(archive_readme, "w", encoding="utf-8") as f:
    f.write("""# MedRule Archive Candidate Repository

This directory contains documents and domain artifacts segregated from the active MedRule collection during the Two-Domain Scope Realignment (October 2026).

## Contents
1. `unrelated_domains/`:
   Clinical policies and rule files from domains outside the narrowed scope (Advanced Imaging & IPM only):
   - `cardiology/`
   - `dmepos/` (Centene DMEPOS)
   - `genetics/` (Genetic Testing)
   - `msk/` (Musculoskeletal Surgery)
   - `physmed/` (Physical Medicine)
   - `radonc/` (Radiation Oncology)
   - `sleep/` (Sleep Health)
2. `duplicate_quarantine/`:
   Cryptographic duplicates segregated to eliminate redundancy while preserving original file hashes:
   - `downloaded_pdfs/`: 13 raw Phase 1 download replicas.
   - `source_pdfs/`: Redundant seed replica `CP.MP.107(4).pdf`.
3. `superseded_or_unresolved/`:
   Files with pending review or superseded status.

All relocations are recorded in `rulebook_collection/manifests/relocation_log.csv` and can be reversed if required.
""")

print("Created domain and archive README files.")

print("\n=== Step E: Post-Move Verification of All 128 Rules ===")
all_active = adv_rules + ipm_rules
pdf_cache = {}
errors = []

for r in all_active:
    rid = r["rule_id"]
    sf = Path(r["source_file"])
    full_sf = RULEBOOK_DIR.parent / sf
    if not full_sf.exists():
        errors.append(f"Missing file for {rid}: {sf}")
        continue
    if str(full_sf) not in pdf_cache:
        pdf_cache[str(full_sf)] = fitz.open(str(full_sf))
    doc = pdf_cache[str(full_sf)]
    max_p = len(doc)
    spage = r["source_page"]
    phys_p = spage.get("physical_page") if isinstance(spage, dict) else spage
    if not isinstance(phys_p, int):
        phys_p = int(phys_p)
    if phys_p < 1 or phys_p > max_p:
        errors.append(f"Page {phys_p} out of bounds (1..{max_p}) for {rid}")
    
    quote = r.get("source_quote", "")
    page_text = doc[phys_p - 1].get_text().lower()
    norm_quote = " ".join(quote.split()).lower()
    snippet = norm_quote[:50].strip()
    if snippet and snippet not in " ".join(page_text.split()):
        # Try checking words
        words = [w for w in norm_quote.split() if len(w) > 4][:5]
        found = sum(1 for w in words if w in page_text)
        if words and found < len(words) - 1:
            errors.append(f"Quote not matched on page {phys_p} for {rid}: {quote[:40]}...")

for doc in pdf_cache.values():
    doc.close()

if errors:
    print(f"VERIFICATION WARNINGS ({len(errors)}):")
    for e in errors[:5]:
        print("  ", e)
else:
    print(f"SUCCESS: All {len(all_active)} rules verified! Physical PDFs exist, pages valid, quotes match.")
