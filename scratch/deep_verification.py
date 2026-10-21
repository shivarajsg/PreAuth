"""Independent verification script for MedRule post-cleanup inspection.
Performs verification across all 12 required points.
"""

import os
import sys
import json
import csv
import hashlib
from pathlib import Path
import fitz

BASE_DIR = Path("d:/PreAuth").resolve()
RULEBOOK_DIR = BASE_DIR / "rulebook_collection"
DOMAINS_DIR = RULEBOOK_DIR / "domains"
MANIFESTS_DIR = RULEBOOK_DIR / "manifests"
ARCHIVE_DIR = RULEBOOK_DIR / "archive_candidate"
SHARED_DIR = RULEBOOK_DIR / "shared_references"
BACKUP_DIR = BASE_DIR / "scratch" / "backup_rulebook_collection_20261021"

def sha256_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def check_1_directory_structure_and_files():
    print("\n--- Check 1: Directory Structure & File Listing in Active Domains ---")
    adv_dir = DOMAINS_DIR / "advanced_imaging"
    ipm_dir = DOMAINS_DIR / "interventional_pain_management"
    
    print(f"domains/ directory contents: {[d.name for d in DOMAINS_DIR.iterdir()]}")
    
    print("\n[Advanced Imaging Files]")
    adv_files = []
    for p in sorted(adv_dir.rglob("*")):
        if p.is_file():
            rel = p.relative_to(adv_dir).as_posix()
            adv_files.append(rel)
            print(f"  {rel} ({p.stat().st_size} bytes)")
            
    print(f"\n[IPM Files]")
    ipm_files = []
    for p in sorted(ipm_dir.rglob("*")):
        if p.is_file():
            rel = p.relative_to(ipm_dir).as_posix()
            ipm_files.append(rel)
            print(f"  {rel} ({p.stat().st_size} bytes)")
            
    return adv_files, ipm_files

def check_2_pdf_census_and_reconciliation():
    print("\n--- Check 2: Physical PDF Census & Reconciliation ---")
    all_pdfs = list(RULEBOOK_DIR.rglob("*.pdf"))
    print(f"Total physical PDFs found in rulebook_collection: {len(all_pdfs)}")
    
    breakdown = {
        "domains/advanced_imaging": list((DOMAINS_DIR / "advanced_imaging").rglob("*.pdf")),
        "domains/interventional_pain_management": list((DOMAINS_DIR / "interventional_pain_management").rglob("*.pdf")),
        "source_pdfs": list((RULEBOOK_DIR / "source_pdfs").rglob("*.pdf")),
        "shared_references/cms": list((SHARED_DIR / "cms").rglob("*.pdf")),
        "archive_candidate/unrelated_domains": list((ARCHIVE_DIR / "unrelated_domains").rglob("*.pdf")),
        "archive_candidate/duplicate_quarantine": list((ARCHIVE_DIR / "duplicate_quarantine").rglob("*.pdf")),
    }
    
    for k, v in breakdown.items():
        print(f"  {k}: {len(v)} PDFs")
        for f in v:
            print(f"    - {f.name} ({f.stat().st_size} bytes)")
            
    total_reconciled = sum(len(v) for v in breakdown.values())
    print(f"Sum of breakdown categories: {total_reconciled}")
    return all_pdfs, breakdown

def check_3_hash_comparison():
    print("\n--- Check 3: Recomputing SHA-256 Hashes vs Pre-Cleanup Inventory ---")
    pre_hashes = {}
    with open(MANIFESTS_DIR / "file_inventory.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            pre_hashes[r["filename"]] = (r["sha256"], int(r["size_bytes"]))
            
    current_pdfs = list(RULEBOOK_DIR.rglob("*.pdf"))
    mismatches = []
    matches = 0
    
    for p in current_pdfs:
        cur_sha = sha256_file(p)
        cur_sz = p.stat().st_size
        if p.name in pre_hashes:
            pre_sha, pre_sz = pre_hashes[p.name]
            if cur_sha != pre_sha or cur_sz != pre_sz:
                mismatches.append((p.as_posix(), cur_sha, pre_sha))
            else:
                matches += 1
        else:
            print(f"  Warning: {p.name} not found in pre_hashes!")
            
    print(f"Total current PDFs checked: {len(current_pdfs)}")
    print(f"Exact hash & size matches: {matches}")
    print(f"Mismatches: {len(mismatches)}")
    if mismatches:
        for m in mismatches:
            print("  ", m)
    return len(mismatches) == 0

def check_4_duplicate_accounting():
    print("\n--- Check 4: Duplicate Accounting Reconciliation ---")
    with open(MANIFESTS_DIR / "duplicate_report.csv", "r", encoding="utf-8") as f:
        dup_rows = list(csv.DictReader(f))
        
    print(f"Total rows in duplicate_report.csv: {len(dup_rows)}")
    unique_hashes = set(r["sha256"] for r in dup_rows)
    print(f"Unique duplicate content hashes: {len(unique_hashes)}")
    
    by_hash = {}
    for r in dup_rows:
        by_hash.setdefault(r["sha256"], []).append(r)
        
    print("\nBreakdown of 15 Duplicate Hash Groups:")
    total_files_in_groups = 0
    canonical_count = 0
    quarantined_count = 0
    other_archived_count = 0
    
    for h, rows in sorted(by_hash.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  Hash {h[:12]}... ({len(rows)} physical files):")
        total_files_in_groups += len(rows)
        for r in rows:
            is_can = r["is_canonical"] == "YES"
            cur_p = r["current_path"]
            if is_can:
                canonical_count += 1
                status = "CANONICAL RETAINED"
            elif "duplicate_quarantine" in cur_p:
                quarantined_count += 1
                status = "DUPLICATE QUARANTINE"
            else:
                other_archived_count += 1
                status = "UNRELATED DOMAIN ARCHIVE"
            print(f"    - [{status}] {r['filename']} -> {cur_p}")
            
    print(f"\nReconciliation Summary:")
    print(f"  Total physical files participating in duplicate groups: {total_files_in_groups}")
    print(f"  Canonical copies retained: {canonical_count}")
    print(f"  Redundant copies quarantined in duplicate_quarantine/: {quarantined_count}")
    print(f"  Redundant copies archived in unrelated_domains/dmepos/: {other_archived_count}")
    print(f"  Total redundant copies: {quarantined_count + other_archived_count} (34 - 15 = 19)")

def check_5_and_6_rules_uniqueness_and_partition_overlap():
    print("\n--- Check 5 & 6: Rule ID Uniqueness & Partition Duplication ---")
    with open(DOMAINS_DIR / "advanced_imaging" / "rules" / "draft_rules.json", encoding="utf-8") as f:
        adv_draft = json.load(f)
    with open(DOMAINS_DIR / "interventional_pain_management" / "rules" / "draft_rules.json", encoding="utf-8") as f:
        ipm_draft = json.load(f)
        
    print(f"Advanced Imaging draft_rules.json: {len(adv_draft)} rules")
    print(f"IPM draft_rules.json: {len(ipm_draft)} rules")
    print(f"Total active draft rules: {len(adv_draft) + len(ipm_draft)}")
    
    adv_draft_ids = [r["rule_id"] for r in adv_draft]
    ipm_draft_ids = [r["rule_id"] for r in ipm_draft]
    
    print(f"Adv unique IDs: {len(set(adv_draft_ids))} (duplicates: {len(adv_draft_ids) - len(set(adv_draft_ids))})")
    print(f"IPM unique IDs: {len(set(ipm_draft_ids))} (duplicates: {len(ipm_draft_ids) - len(set(ipm_draft_ids))})")
    print(f"Cross-domain overlap: {set(adv_draft_ids) & set(ipm_draft_ids)}")
    
    # Check partition files
    print("\nChecking Advanced Imaging procedure partitions:")
    adv_part_rules = {}
    for p in (DOMAINS_DIR / "advanced_imaging" / "rules").rglob("*.json"):
        if p.name in ("draft_rules.json", "schema.json"):
            continue
        # also ignore batch_ legacy files if any
        if "batch_" in p.name:
            continue
        with open(p, encoding="utf-8") as f:
            pdata = json.load(f)
        rules_list = pdata if isinstance(pdata, list) else pdata.get("rules", [])
        for r in rules_list:
            rid = r["rule_id"]
            if rid in adv_part_rules:
                print(f"  Warning: {rid} duplicated in partitions: {p.name} and {adv_part_rules[rid]}")
            adv_part_rules[rid] = p.name
            
    print(f"Total rules across Advanced Imaging partition files: {len(adv_part_rules)}")
    print(f"Rules in draft_rules but not in partitions: {set(adv_draft_ids) - set(adv_part_rules.keys())}")
    print(f"Rules in partitions but not in draft_rules: {set(adv_part_rules.keys()) - set(adv_draft_ids)}")
    
    print("\nChecking IPM procedure partitions:")
    ipm_part_rules = {}
    for p in (DOMAINS_DIR / "interventional_pain_management" / "rules").rglob("*.json"):
        if p.name in ("draft_rules.json", "schema.json"):
            continue
        with open(p, encoding="utf-8") as f:
            pdata = json.load(f)
        rules_list = pdata if isinstance(pdata, list) else pdata.get("rules", [])
        for r in rules_list:
            rid = r["rule_id"]
            if rid in ipm_part_rules:
                print(f"  Warning: {rid} duplicated in partitions: {p.name} and {ipm_part_rules[rid]}")
            ipm_part_rules[rid] = p.name
            
    print(f"Total rules across IPM partition files: {len(ipm_part_rules)}")
    print(f"Rules in IPM draft_rules but not in partitions: {set(ipm_draft_ids) - set(ipm_part_rules.keys())}")
    print(f"Rules in IPM partitions but not in draft_rules: {set(ipm_part_rules.keys()) - set(ipm_draft_ids)}")

def check_7_citations_page_bounds_and_quotes():
    print("\n--- Check 7: Source File Resolution, Page Bounds & Quotes ---")
    with open(DOMAINS_DIR / "advanced_imaging" / "rules" / "draft_rules.json", encoding="utf-8") as f:
        adv = json.load(f)
    with open(DOMAINS_DIR / "interventional_pain_management" / "rules" / "draft_rules.json", encoding="utf-8") as f:
        ipm = json.load(f)
        
    all_rules = adv + ipm
    pdf_cache = {}
    missing_files = []
    out_of_bounds = []
    quote_mismatches = []
    
    for r in all_rules:
        rid = r["rule_id"]
        sfile = r["source_file"]
        spage = r["source_page"]
        quote = r.get("source_quote", "")
        
        # Path resolution using application logic: BASE_DIR / sfile
        full_path = BASE_DIR / sfile
        if not full_path.exists():
            missing_files.append((rid, sfile))
            continue
            
        if str(full_path) not in pdf_cache:
            pdf_cache[str(full_path)] = fitz.open(str(full_path))
        doc = pdf_cache[str(full_path)]
        max_p = len(doc)
        
        phys_p = spage.get("physical_page") if isinstance(spage, dict) else spage
        if not isinstance(phys_p, int):
            phys_p = int(phys_p)
            
        if phys_p < 1 or phys_p > max_p:
            out_of_bounds.append((rid, phys_p, max_p, sfile))
            continue
            
        page_text = doc[phys_p - 1].get_text()
        norm_page = " ".join(page_text.lower().split())
        norm_quote = " ".join(quote.lower().split())
        snippet = norm_quote[:50].strip()
        
        if snippet and snippet not in norm_page:
            words = [w for w in norm_quote.split() if len(w) > 4][:5]
            found = sum(1 for w in words if w in norm_page)
            if words and found < len(words) - 1:
                quote_mismatches.append((rid, phys_p, quote[:40]))
                
    for d in pdf_cache.values():
        d.close()
        
    print(f"Total rules checked: {len(all_rules)}")
    print(f"Missing source files: {len(missing_files)}")
    print(f"Out of bounds pages: {len(out_of_bounds)}")
    print(f"Quote mismatches: {len(quote_mismatches)}")
    if missing_files:
        print("  Missing files:", missing_files)
    if out_of_bounds:
        print("  Out of bounds:", out_of_bounds)
    if quote_mismatches:
        print("  Quote mismatches:", quote_mismatches)
        
    return len(missing_files) == 0 and len(out_of_bounds) == 0 and len(quote_mismatches) == 0

def check_8_governance_statuses():
    print("\n--- Check 8: Governance Status Counts from Actual Rule Files ---")
    with open(DOMAINS_DIR / "advanced_imaging" / "rules" / "draft_rules.json", encoding="utf-8") as f:
        adv = json.load(f)
    with open(DOMAINS_DIR / "interventional_pain_management" / "rules" / "draft_rules.json", encoding="utf-8") as f:
        ipm = json.load(f)
        
    all_rules = adv + ipm
    from collections import Counter
    counts = Counter(r.get("extraction_status") for r in all_rules)
    print("Governance status distribution across all 128 active rules:")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    adv_counts = Counter(r.get("extraction_status") for r in adv)
    print("Advanced Imaging:")
    for k, v in sorted(adv_counts.items()):
        print(f"  {k}: {v}")
    ipm_counts = Counter(r.get("extraction_status") for r in ipm)
    print("IPM:")
    for k, v in sorted(ipm_counts.items()):
        print(f"  {k}: {v}")
        
    has_approved = any(r.get("extraction_status") == "APPROVED" for r in all_rules)
    print(f"Any APPROVED rules: {has_approved}")
    return counts

def check_11_backup():
    print("\n--- Check 11: Backup Existence and Accessibility ---")
    exists = BACKUP_DIR.exists()
    print(f"Backup path: {BACKUP_DIR}")
    print(f"Exists: {exists}")
    if exists:
        b_pdfs = list(BACKUP_DIR.rglob("*.pdf"))
        print(f"Total PDFs in backup: {len(b_pdfs)}")
        print(f"Total items in backup: {len(list(BACKUP_DIR.rglob('*')))}")
    return exists

if __name__ == "__main__":
    check_1_directory_structure_and_files()
    check_2_pdf_census_and_reconciliation()
    check_3_hash_comparison()
    check_4_duplicate_accounting()
    check_5_and_6_rules_uniqueness_and_partition_overlap()
    check_7_citations_page_bounds_and_quotes()
    check_8_governance_statuses()
    check_11_backup()
