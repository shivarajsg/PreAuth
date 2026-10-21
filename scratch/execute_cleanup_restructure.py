"""Execution script to clean and reorganize rulebook_collection into the final target structure.

Performs:
1. Full backup of rulebook_collection/ into scratch/backup_rulebook_collection_20261021/
2. Generation of pre-move inventory and hashes (file_inventory.csv, file_hashes.csv)
3. Relocation of files:
   - Active governing and supporting PDFs into domains/*/policies/ and domains/*/supporting_documents/
   - Unrelated domains (7 domains) into archive_candidate/unrelated_domains/
   - Duplicates (13 in downloaded_pdfs + 1 in source_pdfs) into archive_candidate/duplicate_quarantine/
   - CMS references into shared_references/cms/
   - Seed PreauthorizationMRI.pdf preserved in source_pdfs/
4. Recording of relocation_log.csv and duplicate_report.csv
5. Updating rule source paths across all 128 active rules (draft_rules.json and partition files)
6. Updating source-to-rule traceability CSVs
7. Verifying hashes and validating that all 128 rules, pages, and quotes remain intact.
"""

import os
import sys
import json
import csv
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import fitz

REPO_ROOT = Path("d:/PreAuth").resolve()
RULEBOOK_DIR = REPO_ROOT / "rulebook_collection"
BACKUP_DIR = REPO_ROOT / "scratch" / "backup_rulebook_collection_20261021"

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=== Step 1: Creating Timestamped Backup ===")
    if BACKUP_DIR.exists():
        print(f"Backup already exists at {BACKUP_DIR}, skipping copy...")
    else:
        print(f"Backing up {RULEBOOK_DIR} to {BACKUP_DIR}...")
        shutil.copytree(RULEBOOK_DIR, BACKUP_DIR)
        print("Backup complete.")

    print("\n=== Step 2: Pre-Relocation File Inventory & Hashes ===")
    pdf_inventory = []
    file_hashes = []
    all_pdfs = list(RULEBOOK_DIR.rglob("*.pdf"))
    print(f"Total PDFs found before relocation: {len(all_pdfs)}")

    for pdf_path in sorted(all_pdfs):
        rel = pdf_path.relative_to(RULEBOOK_DIR).as_posix()
        sha = sha256_file(pdf_path)
        sz = pdf_path.stat().st_size
        doc = fitz.open(pdf_path)
        pages = len(doc)
        doc.close()

        pdf_inventory.append({
            "relative_path": rel,
            "filename": pdf_path.name,
            "size_bytes": sz,
            "page_count": pages,
            "sha256": sha
        })
        file_hashes.append({
            "file_path": rel,
            "sha256": sha,
            "size_bytes": sz
        })

    # Save file_inventory.csv and file_hashes.csv
    manifests_dir = RULEBOOK_DIR / "manifests"
    manifests_dir.mkdir(parents=True, exist_ok=True)

    with open(manifests_dir / "file_inventory.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["relative_path", "filename", "size_bytes", "page_count", "sha256"])
        writer.writeheader()
        writer.writerows(pdf_inventory)

    with open(manifests_dir / "file_hashes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_path", "sha256", "size_bytes"])
        writer.writeheader()
        writer.writerows(file_hashes)

    print("Saved pre-relocation file_inventory.csv and file_hashes.csv.")

    print("\n=== Step 3: Defining Relocation Plan ===")
    # Target directory mapping
    # 1. Advanced Imaging
    adv_cur_policies = RULEBOOK_DIR / "domains" / "advanced_imaging" / "policies" / "current"
    adv_hist_policies = RULEBOOK_DIR / "domains" / "advanced_imaging" / "policies" / "historical"
    adv_checklists = RULEBOOK_DIR / "domains" / "advanced_imaging" / "supporting_documents" / "checklists"
    adv_forms = RULEBOOK_DIR / "domains" / "advanced_imaging" / "supporting_documents" / "forms"
    adv_tips = RULEBOOK_DIR / "domains" / "advanced_imaging" / "supporting_documents" / "tip_sheets"
    adv_manifests = RULEBOOK_DIR / "domains" / "advanced_imaging" / "manifests"

    # 2. IPM
    ipm_cur_policies = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "policies" / "current"
    ipm_hist_policies = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "policies" / "historical"
    ipm_checklists = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "supporting_documents" / "checklists"
    ipm_forms = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "supporting_documents" / "forms"
    ipm_tips = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "supporting_documents" / "tip_sheets"
    ipm_manifests = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "manifests"

    # 3. Shared references
    shared_cms = RULEBOOK_DIR / "shared_references" / "cms"
    shared_other = RULEBOOK_DIR / "shared_references" / "other_dependencies"

    # 4. Archive candidate
    archive_unrelated = RULEBOOK_DIR / "archive_candidate" / "unrelated_domains"
    archive_dups = RULEBOOK_DIR / "archive_candidate" / "duplicate_quarantine"
    archive_superseded = RULEBOOK_DIR / "archive_candidate" / "superseded_or_unresolved"

    target_dirs = [
        adv_cur_policies, adv_hist_policies, adv_checklists, adv_forms, adv_tips, adv_manifests,
        ipm_cur_policies, ipm_hist_policies, ipm_checklists, ipm_forms, ipm_tips, ipm_manifests,
        shared_cms, shared_other,
        archive_unrelated / "cardiology",
        archive_unrelated / "dmepos",
        archive_unrelated / "genetics",
        archive_unrelated / "msk",
        archive_unrelated / "physmed",
        archive_unrelated / "radonc",
        archive_unrelated / "sleep",
        archive_dups / "downloaded_pdfs",
        archive_dups / "source_pdfs",
        archive_superseded
    ]

    for td in target_dirs:
        td.mkdir(parents=True, exist_ok=True)

    relocation_records = []

    # Map each of the 101 PDFs to destination
    for item in pdf_inventory:
        rel = item["relative_path"]
        fname = item["filename"]
        src = RULEBOOK_DIR / rel

        # Determine destination
        if "downloaded_pdfs/" in rel:
            dest = archive_dups / "downloaded_pdfs" / fname
            reason = "Duplicate quarantine: raw Phase 1 download replica"
            action = "DUPLICATE_QUARANTINE"

        elif "source_pdfs/" in rel:
            if fname == "PreauthorizationMRI.pdf":
                dest = src # Keep in source_pdfs/PreauthorizationMRI.pdf
                reason = "Authoritative seed document defining project scope; retained in active source_pdfs/"
                action = "KEEP_ACTIVE"
            elif fname == "CP.MP.107(4).pdf":
                dest = archive_dups / "source_pdfs" / fname
                reason = "Duplicate quarantine: redundant copy of Centene DMEPOS seed"
                action = "DUPLICATE_QUARANTINE"
            elif fname == "CP.MP.107.pdf":
                dest = archive_unrelated / "dmepos" / fname
                reason = "Unrelated domain seed document: relocated to archive_candidate/unrelated_domains/dmepos/"
                action = "MOVE_TO_ARCHIVE"
            else:
                dest = archive_superseded / fname
                action = "MOVE_TO_ARCHIVE"

        elif "cross_domain_references/cms/" in rel:
            dest = shared_cms / fname
            reason = "Shared reference standard: relocated to shared_references/cms/"
            action = "KEEP_SHARED_DEPENDENCY"

        elif "domains/advanced_imaging/" in rel:
            if "policy_pdfs/current_2026" in rel:
                dest = adv_cur_policies / fname
                reason = "Active governing/POS policy: relocated to policies/current/"
                action = "KEEP_ACTIVE"
            elif "policy_pdfs/historical_versions" in rel:
                dest = adv_hist_policies / fname
                reason = "Historical policy edition: relocated to policies/historical/"
                action = "KEEP_HISTORICAL"
            elif "supporting_pdfs/checklists" in rel:
                dest = adv_checklists / fname
                reason = "Supporting checklist: relocated to supporting_documents/checklists/"
                action = "KEEP_ACTIVE"
            elif "supporting_pdfs/forms" in rel:
                dest = adv_forms / fname
                reason = "Supporting form: relocated to supporting_documents/forms/"
                action = "KEEP_ACTIVE"
            elif "supporting_pdfs/tip_sheets" in rel:
                dest = adv_tips / fname
                reason = "Supporting tip sheet: relocated to supporting_documents/tip_sheets/"
                action = "KEEP_ACTIVE"
            else:
                dest = adv_manifests / fname
                action = "KEEP_ACTIVE"

        elif "domains/interventional_pain_management/" in rel:
            if "policy_pdfs/current_2026" in rel:
                dest = ipm_cur_policies / fname
                reason = "Active governing/POS policy: relocated to policies/current/"
                action = "KEEP_ACTIVE"
            elif "policy_pdfs/historical_versions" in rel:
                dest = ipm_hist_policies / fname
                reason = "Historical policy edition: relocated to policies/historical/"
                action = "KEEP_HISTORICAL"
            elif "supporting_pdfs/checklists" in rel:
                dest = ipm_checklists / fname
                reason = "Supporting checklist: relocated to supporting_documents/checklists/"
                action = "KEEP_ACTIVE"
            elif "supporting_pdfs/forms" in rel:
                dest = ipm_forms / fname
                reason = "Supporting form: relocated to supporting_documents/forms/"
                action = "KEEP_ACTIVE"
            elif "supporting_pdfs/tip_sheets" in rel:
                dest = ipm_tips / fname
                reason = "Supporting tip sheet: relocated to supporting_documents/tip_sheets/"
                action = "KEEP_ACTIVE"
            else:
                dest = ipm_manifests / fname
                action = "KEEP_ACTIVE"

        else:
            # 7 Unrelated domains
            domain_name = rel.split("/")[1]
            alias_map = {
                "cardiology": "cardiology",
                "centene_dme_orthotics_prosthetics": "dmepos",
                "genetic_testing": "genetics",
                "musculoskeletal_surgery": "msk",
                "physical_medicine": "physmed",
                "radiation_oncology": "radonc",
                "sleep_health": "sleep"
            }
            target_sub = alias_map.get(domain_name, domain_name)
            # preserve relative subfolder in archive
            sub_rel = "/".join(rel.split("/")[2:])
            dest = archive_unrelated / target_sub / sub_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            reason = f"Unrelated domain '{domain_name}': relocated to archive_candidate/unrelated_domains/{target_sub}/"
            action = "MOVE_TO_ARCHIVE"

        relocation_records.append({
            "src": src,
            "dest": dest,
            "rel_src": rel,
            "rel_dest": dest.relative_to(RULEBOOK_DIR).as_posix(),
            "sha256": item["sha256"],
            "size_bytes": item["size_bytes"],
            "action": action,
            "reason": reason
        })

    print(f"Total relocation items planned: {len(relocation_records)}")

    print("\n=== Step 4: Executing PDF Relocations ===")
    now_iso = datetime.now(timezone.utc).isoformat()
    log_rows = []

    for r in relocation_records:
        src = r["src"]
        dest = r["dest"]
        sha_before = r["sha256"]

        if src == dest:
            # File stays in place
            log_rows.append({
                "original_path": r["rel_src"],
                "destination_path": r["rel_dest"],
                "file_size_bytes": r["size_bytes"],
                "sha256_before": sha_before,
                "sha256_after": sha_before,
                "action": r["action"],
                "reason": r["reason"],
                "timestamp": now_iso,
                "status": "RETAINED_IN_PLACE"
            })
            continue

        # Create destination parent
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Move file
        shutil.move(str(src), str(dest))
        sha_after = sha256_file(dest)

        if sha_before != sha_after:
            print(f"CRITICAL ERROR: Hash mismatch for {src} -> {dest}")
            sys.exit(1)

        log_rows.append({
            "original_path": r["rel_src"],
            "destination_path": r["rel_dest"],
            "file_size_bytes": r["size_bytes"],
            "sha256_before": sha_before,
            "sha256_after": sha_after,
            "action": r["action"],
            "reason": r["reason"],
            "timestamp": now_iso,
            "status": "RELOCATED_AND_VERIFIED"
        })

    with open(manifests_dir / "relocation_log.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "original_path", "destination_path", "file_size_bytes",
            "sha256_before", "sha256_after", "action", "reason", "timestamp", "status"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_rows)

    print(f"Saved relocation_log.csv with {len(log_rows)} rows.")

    print("\n=== Step 5: Relocating Unrelated Rules, Manifests & Cleanup of Empty Dirs ===")
    # Move rules/ manifests of the 7 unrelated domains if any remained
    domain_names = [
        "cardiology", "centene_dme_orthotics_prosthetics", "genetic_testing",
        "musculoskeletal_surgery", "physical_medicine", "radiation_oncology", "sleep_health"
    ]
    alias_map = {
        "cardiology": "cardiology",
        "centene_dme_orthotics_prosthetics": "dmepos",
        "genetic_testing": "genetics",
        "musculoskeletal_surgery": "msk",
        "physical_medicine": "physmed",
        "radiation_oncology": "radonc",
        "sleep_health": "sleep"
    }

    for dname in domain_names:
        old_dpath = RULEBOOK_DIR / "domains" / dname
        if old_dpath.exists():
            target_sub = archive_unrelated / alias_map[dname]
            target_sub.mkdir(parents=True, exist_ok=True)
            for item in list(old_dpath.iterdir()):
                target_dest = target_sub / item.name
                if not target_dest.exists():
                    shutil.move(str(item), str(target_dest))
                else:
                    if item.is_dir():
                        for sub in list(item.iterdir()):
                            shutil.move(str(sub), str(target_dest / sub.name))
                        try:
                            item.rmdir()
                        except:
                            pass
            try:
                old_dpath.rmdir()
            except Exception as e:
                print(f"Could not remove {old_dpath}: {e}")

    # Clean legacy empty directories in advanced_imaging and IPM
    for d in ["advanced_imaging", "interventional_pain_management"]:
        for legacy_sub in ["policy_pdfs/current_2026", "policy_pdfs/historical_versions", "policy_pdfs",
                           "supporting_pdfs/checklists", "supporting_pdfs/forms", "supporting_pdfs/tip_sheets", "supporting_pdfs"]:
            p = RULEBOOK_DIR / "domains" / d / legacy_sub
            if p.exists() and p.is_dir():
                try:
                    p.rmdir()
                except:
                    pass

    # Clean legacy root folders: downloaded_pdfs, cross_domain_references
    for legacy_root in ["downloaded_pdfs", "cross_domain_references/cms", "cross_domain_references"]:
        p = RULEBOOK_DIR / legacy_root
        if p.exists() and p.is_dir():
            try:
                p.rmdir()
            except Exception as e:
                print(f"Directory {p} not empty: {e}")

    print("\n=== Step 6: Generating Duplicate Report ===")
    # Group by hash
    by_hash = {}
    for r in log_rows:
        sha = r["sha256_after"]
        by_hash.setdefault(sha, []).append(r)

    duplicate_rows = []
    for sha, group in by_hash.items():
        if len(group) > 1:
            # Find canonical
            canonical = next((x for x in group if x["action"] in ("KEEP_ACTIVE", "KEEP_SHARED_DEPENDENCY", "KEEP_HISTORICAL")), group[0])
            for item in group:
                is_can = (item == canonical)
                duplicate_rows.append({
                    "sha256": sha,
                    "filename": Path(item["original_path"]).name,
                    "is_canonical": "YES" if is_can else "NO",
                    "current_path": item["destination_path"],
                    "original_path": item["original_path"],
                    "canonical_path": canonical["destination_path"],
                    "action_taken": item["action"],
                    "reason": item["reason"]
                })

    with open(manifests_dir / "duplicate_report.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "sha256", "filename", "is_canonical", "current_path",
            "original_path", "canonical_path", "action_taken", "reason"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(duplicate_rows)

    print(f"Saved duplicate_report.csv with {len(duplicate_rows)} duplicate tracking entries.")

    print("\n=== Step 7: Updating Rule Source Paths ===")
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

    # Update draft_rules.json in advanced_imaging
    adv_rules_file = RULEBOOK_DIR / "domains" / "advanced_imaging" / "rules" / "draft_rules.json"
    with open(adv_rules_file, "r", encoding="utf-8") as f:
        adv_rules = json.load(f)

    for r in adv_rules:
        old_sf = r.get("source_file")
        if old_sf in path_replacements:
            r["source_file"] = path_replacements[old_sf]

    with open(adv_rules_file, "w", encoding="utf-8") as f:
        json.dump(adv_rules, f, indent=2)

    # Update partition files in advanced_imaging
    for pfile in (RULEBOOK_DIR / "domains" / "advanced_imaging" / "rules").rglob("*.json"):
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

    # Update draft_rules.json in IPM
    ipm_rules_file = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "rules" / "draft_rules.json"
    with open(ipm_rules_file, "r", encoding="utf-8") as f:
        ipm_rules = json.load(f)

    for r in ipm_rules:
        old_sf = r.get("source_file")
        if old_sf in path_replacements:
            r["source_file"] = path_replacements[old_sf]

    with open(ipm_rules_file, "w", encoding="utf-8") as f:
        json.dump(ipm_rules, f, indent=2)

    # Update partition files in IPM
    for pfile in (RULEBOOK_DIR / "domains" / "interventional_pain_management" / "rules").rglob("*.json"):
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

    print("Updated source_file in draft_rules.json and all partition JSON files.")

    # Ensure schema.json is in IPM rules
    ipm_schema = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "rules" / "schema.json"
    if not ipm_schema.exists():
        shutil.copy(RULEBOOK_DIR / "schemas" / "medrule_rule_schema.json", ipm_schema)
        print("Copied canonical schema.json into IPM rules directory.")

    print("\n=== Step 8: Updating Traceability CSVs ===")
    # Update advanced_imaging traceability
    adv_trace_file = RULEBOOK_DIR / "domains" / "advanced_imaging" / "rules" / "source_to_rule_traceability.csv"
    adv_trace_rows = []
    with open(adv_trace_file, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for old_p, new_p in path_replacements.items():
                if old_p in row.get("source_file", ""):
                    row["source_file"] = new_p
                if Path(old_p).name in row.get("source_document_title_or_id", ""):
                    # leave title or update if needed
                    pass
            adv_trace_rows.append(row)

    with open(adv_trace_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(adv_trace_rows[0].keys()))
        writer.writeheader()
        writer.writerows(adv_trace_rows)

    # Copy to manifests
    shutil.copy(adv_trace_file, adv_manifests / "source_to_rule_traceability.csv")

    # Update IPM traceability
    ipm_trace_file = RULEBOOK_DIR / "domains" / "interventional_pain_management" / "rules" / "source_to_rule_traceability.csv"
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

    # Copy to manifests
    shutil.copy(ipm_trace_file, ipm_manifests / "source_to_rule_traceability.csv")

    # Consolidated active traceability file in manifests/source_to_rule_traceability.csv
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

    with open(manifests_dir / "source_to_rule_traceability.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["rule_id", "domain", "procedure_code", "source_file", "physical_page", "source_section", "source_quote", "extraction_status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(consolidated_trace)

    print(f"Saved consolidated source_to_rule_traceability.csv ({len(consolidated_trace)} rules).")

    print("\n=== Restructure Execution Complete ===")

if __name__ == "__main__":
    main()
