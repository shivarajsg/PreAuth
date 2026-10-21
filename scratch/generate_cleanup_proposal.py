import json, csv, os

with open('scratch/all_pdfs_scan.json') as f:
    scan = json.load(f)

# Also load master_pdf_inventory to cross-reference document_category, document_title, etc.
master_meta = {}
if os.path.exists('rulebook_collection/manifests/master_pdf_inventory.csv'):
    with open('rulebook_collection/manifests/master_pdf_inventory.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            norm_p = row['local_relative_path'].replace('\\', '/')
            master_meta[norm_p] = row

out_rows = []

for item in scan:
    rel_p = item['rel_path'].replace('\\', '/')
    fname = item['filename']
    sha = item['sha256']
    domain = item['domain']
    pages = item['page_count']
    
    # Defaults
    file_type = "PDF"
    doc_category = "General Source Document"
    scope_classification = "UNVERIFIED_OR_UNRESOLVED"
    dependency_check = "No active clinical rule dependencies detected."
    recommended_action = "REVIEW_MANUALLY"
    reason = ""
    destination_if_moved = "STAY_IN_PLACE"
    verification_status = "VERIFIED_PRESENT"
    
    # 1. Downloaded PDFs (Phase 1 legacy downloads)
    if 'downloaded_pdfs/' in rel_p:
        doc_category = "Phase 1 Raw Download"
        scope_classification = "DUPLICATE_CONTENT"
        recommended_action = "DUPLICATE_CANDIDATE"
        destination_if_moved = f"rulebook_collection/archive_candidate/duplicates/downloaded_pdfs/{fname}"
        reason = "Cryptographic exact duplicate of file already organized under primary domain directories or cross_domain_references."
        dependency_check = "Active clinical rules and Phase 2+ manifests point to organized domain directories, not downloaded_pdfs/."
        
    # 2. Source PDFs
    elif 'source_pdfs/' in rel_p:
        if fname == 'PreauthorizationMRI.pdf':
            doc_category = "Authoritative Scope Specification"
            scope_classification = "ACTIVE_SUPPLEMENTARY_POLICY"
            recommended_action = "KEEP_ACTIVE"
            destination_if_moved = "STAY_IN_PLACE"
            reason = "Authoritative initial seed document defining Section A (Advanced Imaging) and Section B (Interventional Pain Management) prior authorization scope for Georgia."
            dependency_check = "Foundational seed document defining core 2-domain project scope; referenced in root documentation."
        elif 'CP.MP.107' in fname:
            if '(4)' in fname:
                doc_category = "Duplicate Seed Document"
                scope_classification = "DUPLICATE_CONTENT"
                recommended_action = "DUPLICATE_CANDIDATE"
                destination_if_moved = f"rulebook_collection/archive_candidate/duplicates/source_pdfs/{fname}"
                reason = "Exact duplicate of CP.MP.107.pdf seed file."
                dependency_check = "No active imaging or IPM rules reference CP.MP.107(4).pdf."
            else:
                doc_category = "Seed Policy Document (Unrelated Domain)"
                scope_classification = "UNRELATED_DOMAIN"
                recommended_action = "MOVE_TO_ARCHIVE_CANDIDATE"
                destination_if_moved = f"rulebook_collection/archive_candidate/source_pdfs/{fname}"
                reason = "Original seed document for Centene DMEPOS guidelines (Revision 11-24), which is outside the narrowed 2-domain clinical scope."
                dependency_check = "No active imaging or IPM rules reference Centene DMEPOS policy."
                
    # 3. Cross Domain References (CMS / RESNA)
    elif 'cross_domain_references/' in rel_p:
        doc_category = "CMS / Regulatory Standard Reference"
        scope_classification = "EXTERNAL_POLICY_DEPENDENCY"
        recommended_action = "KEEP_SHARED_DEPENDENCY"
        destination_if_moved = f"rulebook_collection/archive_candidate/cross_domain_references/cms/{fname}"
        reason = "Federal CMS claims manual, hospital conditions of participation, or DME quality standards. Retained as shared statutory reference if needed."
        dependency_check = "Mapped in policy_dependency_mapping.csv to Centene DMEPOS (DEP-001..DEP-004); zero active rules in Advanced Imaging or IPM depend on this document."

    # 4. Advanced Imaging Domain
    elif domain == 'advanced_imaging':
        if 'current_2026' in rel_p:
            if 'Advanced Imaging v2.pdf' in fname:
                doc_category = "Governing Clinical Guideline"
                scope_classification = "ACTIVE_GOVERNING_POLICY"
                recommended_action = "KEEP_ACTIVE"
                reason = "Primary authoritative 2026 governing guideline (1,041 pages) establishing medical necessity for CT, MRI, CTA, MRA, and PET/CT."
                dependency_check = "114 active clinical rules and 114 traceability records depend directly on this document."
            elif 'EPOS 2067' in fname:
                doc_category = "Place of Service Policy"
                scope_classification = "ACTIVE_SUPPLEMENTARY_POLICY"
                recommended_action = "KEEP_ACTIVE"
                reason = "Place of Service policy 2067 (11 pages) defining medical necessity for hospital outpatient vs freestanding imaging facilities."
                dependency_check = "Adjudication rules RULE-ADV-EPOS2067-001 through 005 depend directly on this policy."
        elif 'historical_versions' in rel_p:
            doc_category = "Historical Clinical Guideline"
            scope_classification = "HISTORICAL_REFERENCE"
            recommended_action = "KEEP_HISTORICAL"
            reason = "Historical 2025 guideline (1,074 pages) cited in seed file; preserved for version comparison and audit trail."
            dependency_check = "Tracked in policy_versions.csv (effective 2025-01-01 -> superseded 2026-01-01)."
        elif 'supporting_pdfs/checklists' in rel_p:
            doc_category = "Supporting Documentation Checklist"
            scope_classification = "SUPPORTING_CHECKLIST_OR_FORM"
            recommended_action = "KEEP_ACTIVE"
            reason = "Active provider intake checklist defining mandatory clinical submission elements."
            dependency_check = "Referenced in clinical documentation intake validation for imaging authorization."
        elif 'supporting_pdfs/forms' in rel_p:
            if '6.10.25' in fname:
                doc_category = "Supporting Clinical Form"
                scope_classification = "SUPPORTING_CHECKLIST_OR_FORM"
                recommended_action = "KEEP_ACTIVE"
                reason = "Current governing conservative treatment form (Rev 06/10/2025) documenting PT and medication trials."
                dependency_check = "Conservative therapy rules for spine and joint MRI cross-reference trial criteria."
            else:
                doc_category = "Historical Clinical Form"
                scope_classification = "HISTORICAL_REFERENCE"
                recommended_action = "KEEP_HISTORICAL"
                reason = "Superseded 2024 conservative therapy form retained for version traceability."
                dependency_check = "Tracked in policy_versions.csv as superseded by Rev 06/10/2025."
        elif 'supporting_pdfs/tip_sheets' in rel_p:
            if '07.2025' in fname or '4.2026' in fname or '4.27.26' in fname:
                doc_category = "Supporting Tip Sheet"
                scope_classification = "SUPPORTING_TIP_SHEET"
                recommended_action = "KEEP_ACTIVE"
                reason = "Active clinical summary tip sheet detailing expedited review indicators, modality comparison, or documentation shortcuts."
                dependency_check = "Referenced in expedited workflow and modality selection screening logic."
            else:
                doc_category = "Historical Tip Sheet"
                scope_classification = "HISTORICAL_REFERENCE"
                recommended_action = "KEEP_HISTORICAL"
                reason = "Historical 2024 tip sheet retained for version traceability."
                dependency_check = "Tracked in policy_versions.csv as superseded by 2025/2026 editions."

    # 5. Interventional Pain Management Domain
    elif domain == 'interventional_pain_management':
        if 'current_2026' in rel_p:
            if 'Interventional Pain Management Guidelines.pdf' in fname:
                doc_category = "Governing Clinical Guideline"
                scope_classification = "ACTIVE_GOVERNING_POLICY"
                recommended_action = "KEEP_ACTIVE"
                reason = "Primary authoritative 2026 governing guideline (102 pages) covering ESIs, facet blocks, SI joint injections, and neuromodulation."
                dependency_check = "14 active IPM clinical rules and 14 traceability records depend directly on this document."
            elif 'EPOS 1755' in fname:
                doc_category = "Place of Service Policy"
                scope_classification = "ACTIVE_SUPPLEMENTARY_POLICY"
                recommended_action = "KEEP_ACTIVE"
                reason = "Place of Service policy 1755 defining site-of-care requirements (ASC vs hospital outpatient) for pain procedures."
                dependency_check = "Adjudication rules RULE-IPM-EPOS1755-001 and 002 depend directly on this policy."
        elif 'historical_versions' in rel_p:
            doc_category = "Historical Clinical Guideline"
            scope_classification = "HISTORICAL_REFERENCE"
            recommended_action = "KEEP_HISTORICAL"
            reason = "Historical 2025 guideline (75 pages) cited in seed file Section B; preserved for version comparison and audit trail."
            dependency_check = "Tracked in policy_versions.csv (effective 2025-07-01 -> superseded 2026-07-01)."
        elif 'supporting_pdfs/checklists' in rel_p:
            doc_category = "Supporting Documentation Checklist"
            scope_classification = "SUPPORTING_CHECKLIST_OR_FORM"
            recommended_action = "KEEP_ACTIVE"
            reason = "Active provider intake checklist defining mandatory clinical submission elements for pain procedures."
            dependency_check = "Referenced in documentation requirements across epidural, facet, and neuromodulation rules."
        elif 'supporting_pdfs/forms' in rel_p:
            if '08072025' in fname:
                doc_category = "Supporting Clinical Form"
                scope_classification = "SUPPORTING_CHECKLIST_OR_FORM"
                recommended_action = "KEEP_ACTIVE"
                reason = "Current governing conservative treatment form (Rev 08/07/2025) documenting PT/OT, medication trials, and pain relief."
                dependency_check = "Required for conservative treatment verification across all 14 IPM rules."
            else:
                doc_category = "Historical Clinical Form"
                scope_classification = "HISTORICAL_REFERENCE"
                recommended_action = "KEEP_HISTORICAL"
                reason = "Superseded 2024 conservative treatment form retained for version traceability."
                dependency_check = "Tracked in policy_versions.csv as superseded by Rev 08/07/2025."
        elif 'supporting_pdfs/tip_sheets' in rel_p:
            doc_category = "Supporting Tip Sheet"
            scope_classification = "SUPPORTING_TIP_SHEET"
            recommended_action = "KEEP_ACTIVE"
            reason = "Active clinical summary tip sheet detailing injection interval requirements and diagnostic relief thresholds."
            dependency_check = "Guides diagnostic medial branch block relief criteria (80% vs 50%)."

    # 6. Unrelated 7 Domains
    else:
        doc_category = f"Clinical Policy / Reference ({domain.replace('_', ' ').title()})"
        scope_classification = "UNRELATED_DOMAIN"
        recommended_action = "MOVE_TO_ARCHIVE_CANDIDATE"
        destination_if_moved = f"rulebook_collection/archive_candidate/domains/{domain}/{fname}"
        reason = f"Belongs to '{domain}' domain, which is outside the narrowed MedRule project scope (Advanced Imaging & IPM only)."
        dependency_check = "Verified zero active clinical rules, schemas, or tests in Advanced Imaging or IPM depend on this document."

    out_rows.append({
        'relative_path': rel_p,
        'file_type': file_type,
        'domain': domain,
        'document_category': doc_category,
        'scope_classification': scope_classification,
        'sha256': sha,
        'dependency_check': dependency_check,
        'recommended_action': recommended_action,
        'reason': reason,
        'destination_if_moved': destination_if_moved,
        'verification_status': verification_status
    })

fieldnames = [
    'relative_path',
    'file_type',
    'domain',
    'document_category',
    'scope_classification',
    'sha256',
    'dependency_check',
    'recommended_action',
    'reason',
    'destination_if_moved',
    'verification_status'
]

out_path = 'rulebook_collection/manifests/scope_cleanup_proposal.csv'
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(out_rows)

print(f"Generated {out_path} with {len(out_rows)} rows.")
