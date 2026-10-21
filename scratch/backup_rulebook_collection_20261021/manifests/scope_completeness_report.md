# MedRule — Rulebook Collection Scope Audit, Cleanup Proposal & Completeness Report

**Audit Date:** October 21, 2026  
**Scope Focus:** Two Core Clinical Domains: **Advanced Imaging** & **Interventional Pain Management (IPM)**  
**Auditor:** Deterministic Rulebook Verification Subsystem  
**Manifest Artifact:** [scope_cleanup_proposal.csv](file:///d:/PreAuth/rulebook_collection/manifests/scope_cleanup_proposal.csv)  
**Verification Suite:** [test_scope_integrity.py](file:///d:/PreAuth/rulebook_collection/tests/test_scope_integrity.py)

---

## Executive Summary

Pursuant to the objective of narrowing the MedRule project scope strictly to **Advanced Imaging** and **Interventional Pain Management (IPM)**, an exhaustive audit and cryptographic verification of `rulebook_collection/` was conducted.

The audit established that:
1. **Repository Inventory:** There are **101 physical PDF files** on disk representing **82 unique cryptographic contents (SHA-256)** and **15 duplicate content groups**.
2. **Two-Domain Core:** Exactly **18 domain PDFs** belong directly to the two core domains (11 in Advanced Imaging, 7 in IPM), supported by **1 foundational seed document** (`PreauthorizationMRI.pdf`).
3. **Active Clinical Rules:** Exactly **128 active clinical rules** are authored across the two domains (114 in Advanced Imaging, 14 in IPM). Every single rule has been verified to reference an existing physical PDF and valid physical page, with **100% (128/128) verbatim quote fidelity** and **100% (128/128) source-to-rule traceability**.
4. **Governance Invariant:** **Zero (0) rules are marked `APPROVED`**. All rules remain in `DRAFT` or `NEEDS_HUMAN_REVIEW` status.
5. **No Immediate File Movement or Deletion:** Under strict safety rules, no PDF has been deleted, overwritten, or moved. A detailed, non-destructive cleanup proposal has been generated in [scope_cleanup_proposal.csv](file:///d:/PreAuth/rulebook_collection/manifests/scope_cleanup_proposal.csv) mapping 64 unrelated documents and 14 redundant duplicates for safe archival pending user confirmation.

---

## 1. Physical PDF Census & Content Totals

A complete cryptographic scan of all PDF files under `rulebook_collection/` yielded the following verified counts:

| Inventory Dimension | Physical Count | Unique SHA-256 Hashes | Redundant Copies |
| :--- | :---: | :---: | :---: |
| **Advanced Imaging (`domains/advanced_imaging/`)** | 11 | 11 | 0 (internal) |
| **Interventional Pain Management (`domains/interventional_pain_management/`)** | 7 | 7 | 0 (internal) |
| **Authoritative Seed & Project Inputs (`source_pdfs/`)** | 3 | 2 | 1 duplicate (`CP.MP.107(4).pdf`) |
| **Cross-Domain Reference Standards (`cross_domain_references/cms/`)** | 4 | 4 | 4 duplicated in DMEPOS |
| **Legacy Phase 1 Downloads (`downloaded_pdfs/`)** | 13 | 13 | 13 duplicated in domain folders |
| **Unrelated Domains (7 Domains in `domains/`)** | 63 | 61 | 2 internal duplicates |
| **Total Rulebook Collection PDF Census** | **101** | **82** | **19 redundant physical instances** |

### Breakdown of the 7 Unrelated Domains (63 PDFs)
- **Cardiology:** 11 PDFs (1 governing guideline, 1 supplementary EPOS 2068, 1 historical 2025 edition, 3 checklists, 2 forms, 3 tip sheets)
- **Centene DMEPOS:** 13 PDFs (1 governing Rev 08-26, 1 historical Rev 11-24, 4 CMS/RESNA referenced sources, 1 checklist, 3 forms, 3 tip sheets)
- **Genetic Testing:** 4 PDFs (1 governing guideline, 1 historical 2025 edition, 1 checklist, 1 tip sheet)
- **Musculoskeletal Surgery:** 11 PDFs (1 governing guideline, 1 supplementary EPOS 2069, 1 historical 2025 edition, 3 checklists, 2 forms, 3 tip sheets)
- **Physical Medicine:** 12 PDFs (1 governing guideline, 1 supplementary EPOS 2070, 1 historical 2025 edition, 3 checklists, 3 forms, 3 tip sheets)
- **Radiation Oncology:** 9 PDFs (1 governing guideline, 1 supplementary EPOS 2071, 1 historical 2025 edition, 2 checklists, 2 forms, 2 tip sheets)
- **Sleep Health:** 3 PDFs (1 governing guideline, 1 historical 2025 edition, 1 checklist)

---

## 2. Cryptographic Duplicate Analysis (SHA-256)

Duplicate detection was performed strictly via SHA-256 content hashes, identifying 15 duplicate hash groups encompassing 34 file instances (82 unique contents across 101 files):

1. **Hash `2c63e4136e44...` (3 copies):** `clm104c20.pdf` (in `cross_domain_references/cms`, `centene_dme_orthotics_prosthetics/referenced_sources`, and `downloaded_pdfs`).
2. **Hash `93dab0069bae...` (3 copies):** `RESNA_App of Seat Elevation Devices 2019.pdf` (in `cross_domain_references/cms`, `centene_dme_orthotics_prosthetics/referenced_sources`, and `downloaded_pdfs`).
3. **Hash `20ecc8d6150f...` (3 copies):** `som107ap_a_hospitals.pdf` (in `cross_domain_references/cms`, `centene_dme_orthotics_prosthetics/referenced_sources`, and `downloaded_pdfs`).
4. **Hash `9ef5e7dbf19a...` (3 copies):** `CP.MP.107 (Revision 11-24).pdf` (in `centene_dme_orthotics_prosthetics/historical_versions`, `source_pdfs/CP.MP.107.pdf`, and `source_pdfs/CP.MP.107(4).pdf`).
5. **Hash `6658c022bba7...` (2 copies):** `dmepos-quality-standards.pdf` (in `cross_domain_references/cms` and `centene_dme_orthotics_prosthetics/referenced_sources`).
6. **Hash `8155ca0b284e...` (2 copies):** `2025 Evolent Advanced Imaging Guidelines_0.pdf` (in `domains/advanced_imaging/policy_pdfs/historical_versions` and `downloaded_pdfs`).
7. **Hash `750ff5f05b2f...` (2 copies):** `Evolent Generic Prior Authorization Checklist (non cardiac) 11112024.pdf` (in `domains/advanced_imaging/supporting_pdfs/checklists` and `downloaded_pdfs`).
8. **Hash `e68bf16c1784...` (2 copies):** `LDCT Form Evolent 02162024_0.pdf` (in `domains/advanced_imaging/supporting_pdfs/checklists` and `downloaded_pdfs`).
9. **Hash `e4907326e796...` (2 copies):** `Conservative Treatment Form - Imaging Evolent 01112024.pdf` (in `domains/advanced_imaging/supporting_pdfs/forms` and `downloaded_pdfs`).
10. **Hash `0dc27ede4d30...` (2 copies):** `Evolent Tip Sheet Advanced Imaging 2.16.24.pdf` (in `domains/advanced_imaging/supporting_pdfs/tip_sheets` and `downloaded_pdfs`).
11. **Hash `dc0177d8ae96...` (2 copies):** `Evolent Tip Sheet Pediatric Imaging 2.16.24.pdf` (in `domains/advanced_imaging/supporting_pdfs/tip_sheets` and `downloaded_pdfs`).
12. **Hash `873a262a6252...` (2 copies):** `2025 Evolent Interventional Pain Management Guidelines.pdf` (in `domains/interventional_pain_management/policy_pdfs/historical_versions` and `downloaded_pdfs`).
13. **Hash `b5834ce89ea8...` (2 copies):** `IPM Checklist Evolent 04262024.pdf` (in `domains/interventional_pain_management/supporting_pdfs/checklists` and `downloaded_pdfs`).
14. **Hash `7b3ea1c859d5...` (2 copies):** `Conservative Treatment Form - IPM Evolent 01112024.pdf` (in `domains/interventional_pain_management/supporting_pdfs/forms` and `downloaded_pdfs`).
15. **Hash `e4f4cc7970fd...` (2 copies):** `IPM Tip Sheet Evolent 04262024.pdf` (in `domains/interventional_pain_management/supporting_pdfs/tip_sheets` and `downloaded_pdfs`).

---

## 3. Scope Classification of Core & Supporting Documents

### Core Domain 1: Advanced Imaging (11 PDFs + Seed Dependency)

| Document Filename | Category | Scope Classification | Recommended Action | Pages | SHA-256 (Prefix) |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` | Governing Guideline | `ACTIVE_GOVERNING_POLICY` | `KEEP_ACTIVE` | 1,041 | `b607a1b4b2b7` |
| `EPOS 2067 for Place of Service - Radiology 2026_final.pdf` | Place of Service Policy | `ACTIVE_SUPPLEMENTARY_POLICY` | `KEEP_ACTIVE` | 11 | `c2f609bb286a` |
| `PreauthorizationMRI.pdf` (in `source_pdfs/`) | Scope Matrix Seed | `ACTIVE_SUPPLEMENTARY_POLICY` | `KEEP_ACTIVE` | 2 | `09c690feb5d8` |
| `Evolent Generic Prior Authorization Checklist (non cardiac) 11112024.pdf` | Checklist | `SUPPORTING_CHECKLIST_OR_FORM` | `KEEP_ACTIVE` | 1 | `750ff5f05b2f` |
| `LDCT Form Evolent 02162024_0.pdf` | Form / Checklist | `SUPPORTING_CHECKLIST_OR_FORM` | `KEEP_ACTIVE` | 1 | `e68bf16c1784` |
| `Conservative Treatment Form - Advanced Imaging 6.10.25_0.pdf` | Clinical Trial Form | `SUPPORTING_CHECKLIST_OR_FORM` | `KEEP_ACTIVE` | 2 | `3c621816508b` |
| `Advanced Imaging Tip Sheet 07.2025.pdf` | Tip Sheet | `SUPPORTING_TIP_SHEET` | `KEEP_ACTIVE` | 6 | `9b039c3ceb8b` |
| `Brain MRI vs CT Tip Sheet 4.27.26.pdf` | Tip Sheet | `SUPPORTING_TIP_SHEET` | `KEEP_ACTIVE` | 2 | `a9e6ea3e4307` |
| `2025 Evolent Advanced Imaging Guidelines_0.pdf` | Historical Edition | `HISTORICAL_REFERENCE` | `KEEP_HISTORICAL` | 1,074 | `8155ca0b284e` |
| `Conservative Treatment Form - Imaging Evolent 01112024.pdf` | Superseded Form | `HISTORICAL_REFERENCE` | `KEEP_HISTORICAL` | 2 | `e4907326e796` |
| `Evolent Tip Sheet Advanced Imaging 2.16.24.pdf` | Superseded Tip Sheet | `HISTORICAL_REFERENCE` | `KEEP_HISTORICAL` | 6 | `0dc27ede4d30` |
| `Evolent Tip Sheet Pediatric Imaging 2.16.24.pdf` | Superseded Tip Sheet | `HISTORICAL_REFERENCE` | `KEEP_HISTORICAL` | 6 | `dc0177d8ae96` |

### Core Domain 2: Interventional Pain Management (7 PDFs)

| Document Filename | Category | Scope Classification | Recommended Action | Pages | SHA-256 (Prefix) |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `2026 Evolent Interventional Pain Management Guidelines.pdf` | Governing Guideline | `ACTIVE_GOVERNING_POLICY` | `KEEP_ACTIVE` | 102 | `a931ef18ba45` |
| `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` | Place of Service Policy | `ACTIVE_SUPPLEMENTARY_POLICY` | `KEEP_ACTIVE` | 8 | `ce55ddbcfe60` |
| `IPM Checklist Evolent 04262024.pdf` | Checklist | `SUPPORTING_CHECKLIST_OR_FORM` | `KEEP_ACTIVE` | 3 | `b5834ce89ea8` |
| `Conservative Treatment Form - IPM Evolent 08072025.pdf` | Clinical Trial Form | `SUPPORTING_CHECKLIST_OR_FORM` | `KEEP_ACTIVE` | 2 | `9b42217c050b` |
| `IPM Tip Sheet Evolent 04262024.pdf` | Tip Sheet | `SUPPORTING_TIP_SHEET` | `KEEP_ACTIVE` | 4 | `e4f4cc7970fd` |
| `2025 Evolent Interventional Pain Management Guidelines.pdf` | Historical Edition | `HISTORICAL_REFERENCE` | `KEEP_HISTORICAL` | 75 | `873a262a6252` |
| `Conservative Treatment Form - IPM Evolent 01112024.pdf` | Superseded Form | `HISTORICAL_REFERENCE` | `KEEP_HISTORICAL` | 1 | `7b3ea1c859d5` |

---

## 4. Current vs. Historical Policy Version Analysis

The transition between historical 2024/2025 policy documents and active 2026 editions has been verified and documented:

| Domain | Historical Baseline Document | Active 2026 Governing Document | Page Transition | Key Clinical & Structural Differences |
| :--- | :--- | :--- | :---: | :--- |
| **Advanced Imaging** | `2025 Evolent Advanced Imaging Guidelines_0.pdf` (Effective 2025-01-01) | `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (Effective 2026-01-01) | 1,074 pp → 1,041 pp | Cardiac imaging procedures were split into standalone Cardiology guidelines; updated oncologic PET/CT criteria; refined MRI red flag neurological criteria. |
| **Advanced Imaging Form** | `Conservative Treatment Form - Imaging Evolent 01112024.pdf` (Rev. 01/11/2024) | `Conservative Treatment Form - Advanced Imaging 6.10.25_0.pdf` (Rev. 06/10/2025) | 2 pp → 2 pp | Added granular physical therapy modality tracking and non-opioid medication trial checkboxes. |
| **Advanced Imaging Tip Sheet** | `Evolent Tip Sheet Advanced Imaging 2.16.24.pdf` (Rev. 02/16/2024) | `Advanced Imaging Tip Sheet 07.2025.pdf` (Rev. 07/2025) | 6 pp → 6 pp | Refined extremity MRI trial duration thresholds (6 weeks vs 4 weeks). |
| **Interventional Pain** | `2025 Evolent Interventional Pain Management Guidelines.pdf` (Effective 2025-07-01) | `2026 Evolent Interventional Pain Management Guidelines.pdf` (Effective 2026-07-01) | 75 pp → 102 pp | Expansion of diagnostic medial branch block relief criteria (explicit 80% dual block requirement vs 50%); added spinal cord stimulator permanent trial prerequisites. |
| **Interventional Pain Form** | `Conservative Treatment Form - IPM Evolent 01112024.pdf` (Rev. 01/11/2024) | `Conservative Treatment Form - IPM Evolent 08072025.pdf` (Rev. 08/07/2025) | 1 p → 2 pp | Expanded from 1 to 2 pages; mandated recording of specific medication classes (NSAIDs, SNRIs, gabapentinoids) and injection response duration. |

---

## 5. Active Rule Completeness & Traceability Verification

An audit of all active rules across Advanced Imaging and IPM confirmed complete structural integrity and source alignment:

| Domain | Total Rules | DRAFT Status | NEEDS_HUMAN_REVIEW | APPROVED Status | Traceability Rows | Verbatim Quote Match | Out-of-Bounds Pages |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Advanced Imaging** | 114 | 107 | 7 | **0** | 114 / 114 (100%) | 114 / 114 (100%) | **0** |
| **Interventional Pain** | 14 | 12 | 2 | **0** | 14 / 14 (100%) | 14 / 14 (100%) | **0** |
| **Total Active Corpus** | **128** | **119** | **9** | **0** | **128 / 128 (100%)** | **128 / 128 (100%)** | **0** |

### Procedural Partitioning of Active Rules
- **Advanced Imaging (114 Rules):**
  - `rules/ct/`: 43 rules (Head/Brain, Chest, Spine, Abdomen/Pelvis, Extremities, Sinus/Maxillofacial, Temporal Bone)
  - `rules/mri/`: 39 rules (Brain, Cervical/Thoracic/Lumbar Spine, Knee, Shoulder, Hip, TMJ, Orbit/Face/Neck)
  - `rules/cta/`: 11 rules (Head, Neck, Chest, Abdomen, Pelvis, Extremity)
  - `rules/mra/`: 9 rules (Head, Neck, Chest, Abdomen, Spinal Canal)
  - `rules/pet_spect/`: 6 rules (PET Oncology, PET Brain/Myocardial, SPECT)
  - `rules/cross_cutting/`: 6 rules (General preamble, contrast safety, place of service EPOS 2067)
- **Interventional Pain Management (14 Rules):**
  - `rules/epidural_injections/`: 2 rules (Cervical/Thoracic/Lumbar interlaminar & transforaminal ESIs)
  - `rules/facet_interventions/`: 3 rules (Diagnostic medial branch blocks, radiofrequency facet neurotomy)
  - `rules/sacroiliac_joint/`: 1 rule (SI joint diagnostic & therapeutic injections)
  - `rules/neuromodulation_pumps/`: 4 rules (Spinal cord stimulation trial/implant, intrathecal drug delivery pump)
  - `rules/sympathetic_blocks/`: 1 rule (Stellate ganglion, lumbar sympathetic, celiac plexus)
  - `rules/cross_cutting/`: 3 rules (IPM general conservative therapy, place of service EPOS 1755)

---

## 6. Policy Dependency Analysis & External Boundaries

A rigorous check of cross-domain and external dependencies was performed:

1. **Self-Containment of Core Domains:**
   - Neither Advanced Imaging nor IPM depends on any clinical guidelines from Cardiology, Centene DMEPOS, Genetic Testing, Musculoskeletal Surgery, Physical Medicine, Radiation Oncology, or Sleep Health.
   - Cross-domain dependency `DEP-006` in `policy_dependency_mapping.csv` records that Radiation Oncology depends on Advanced Imaging EPOS 2067 (hospital outpatient simulation scan rules). Advanced Imaging has **no reciprocal dependency** on Radiation Oncology.
2. **Shared CMS Regulatory Standards:**
   - The 4 PDFs in `cross_domain_references/cms/` (`clm104c20.pdf`, `som107ap_a_hospitals.pdf`, `RESNA_App of Seat Elevation Devices 2019.pdf`, `dmepos-quality-standards.pdf`) are statutory authorities cited exclusively by Centene DMEPOS (`DEP-001` through `DEP-004`). Zero active rules in Imaging or IPM cite these documents.
3. **Unresolved / Plan-Specific Boundary Dependencies (from `missing_documents.csv`):**
   - `DOC-ADV-MISSING-001`: State Medicaid Prior Authorization CPT Crosswalks (determines prior notification vs prior authorization in select state contracts).
   - `DOC-IPM-MISSING-001`: State Medicaid Controlled Substance Schedules & Frequency Caps (mandates statutory hard limits such as maximum 4 ESIs per 12 rolling months, overriding clinical recurrence).

---

## 7. Actionable Scope Cleanup Proposal Summary

The complete row-by-row classification of all 101 PDFs is recorded in [scope_cleanup_proposal.csv](file:///d:/PreAuth/rulebook_collection/manifests/scope_cleanup_proposal.csv). Below is the reconciled action summary:

```text
Action Class Distribution:
├── KEEP_ACTIVE ................................ 13 files (Governing, POS, Checklists, Forms, Tip Sheets, Seed)
├── KEEP_HISTORICAL ............................  6 files (2025 Baseline Editions & Superseded Forms/Sheets)
├── KEEP_SHARED_DEPENDENCY .....................  4 files (CMS Manuals & RESNA in cross_domain_references/)
├── MOVE_TO_ARCHIVE_CANDIDATE .................. 64 files (63 PDFs in 7 unrelated domains + 1 seed CP.MP.107.pdf)
└── DUPLICATE_CANDIDATE ........................ 14 files (13 Phase 1 raw downloads + 1 duplicate seed)
──────────────────────────────────────────────────────────
TOTAL PHYSICAL PDFS AUDITED .................... 101 files
```

### Proposed Repository Target Structure

```text
rulebook_collection/
├── README.md
├── source_pdfs/
│   └── PreauthorizationMRI.pdf                            # Retained: Authoritative seed scope definition
├── domains/
│   ├── advanced_imaging/
│   │   ├── policy_pdfs/
│   │   │   ├── current_2026/                              # Retained active governing & POS guidelines
│   │   │   └── historical_versions/                       # Retained 2025 baseline
│   │   ├── supporting_pdfs/                               # Retained checklists, forms, tip sheets
│   │   └── rules/                                         # 114 active validated rules
│   └── interventional_pain_management/
│       ├── policy_pdfs/
│       │   ├── current_2026/                              # Retained active governing & POS guidelines
│       │   └── historical_versions/                       # Retained 2025 baseline
│       ├── supporting_pdfs/                               # Retained checklists, forms, tip sheets
│       └── rules/                                         # 14 active validated rules
├── shared_references/
│   └── cms/                                               # Retained shared regulatory references
├── manifests/
│   ├── scope_cleanup_proposal.csv                         # Master 101-file classification manifest
│   ├── scope_completeness_report.md                       # This comprehensive report
│   ├── master_pdf_inventory.csv
│   └── policy_dependency_mapping.csv
├── archive_candidate/                                     # Target destination for 64 unrelated + 14 duplicate files
│   ├── README.md
│   ├── domains/ (cardiology, centene_dme, etc.)
│   └── duplicates/ (downloaded_pdfs/)
└── tests/
    └── test_scope_integrity.py                            # Scope boundary & integrity test suite
```

---

## 8. Test Execution & Verification Results

All tests were executed using the workspace Python virtual environment (`.venv\Scripts\pytest.exe`).

### 1. Scope Integrity Test Suite (`rulebook_collection/tests/test_scope_integrity.py`)
- **Status:** **PASSED** (12 passed in 2.27s)
- **Detailed Results:**
  - `test_01_primary_active_domains_restriction`: **PASSED** (verifies active domain set is strictly `{"advanced_imaging", "interventional_pain_management"}`)
  - `test_02_every_active_rule_references_existing_pdf`: **PASSED** (all 128 active rules resolve to physical PDFs on disk)
  - `test_03_every_referenced_pdf_has_valid_inventory_entry`: **PASSED** (all referenced PDFs exist in proposal inventory)
  - `test_04_every_referenced_source_page_within_pdf_bounds`: **PASSED** (all physical page references verified within PDF boundaries)
  - `test_05_rule_id_uniqueness_across_active_knowledge_base`: **PASSED** (all 128 rule IDs globally unique)
  - `test_06_rule_schema_conformance`: **PASSED** (all rules strictly validate against MedRule canonical JSON schema)
  - `test_07_every_active_rule_has_traceability_record`: **PASSED** (100% alignment between active rules and traceability rows)
  - `test_08_historical_documents_cannot_silently_enter_active_registry`: **PASSED** (no historical policy cited as active governing guideline)
  - `test_09_shared_dependencies_retained_and_explicitly_mapped`: **PASSED** (cross-domain dependencies explicitly documented)
  - `test_10_cryptographic_duplicate_detection_by_sha256`: **PASSED** (all 14 duplicate contents identified via SHA-256)
  - `test_11_no_rules_automatically_promoted_to_approved`: **PASSED** (zero rules marked APPROVED; governance safety preserved)
  - `test_12_existing_rule_logic_and_counts_preserved`: **PASSED** (exact baselines of 114 imaging and 14 IPM rules preserved)

### 2. Domain Unit Suites
- `rulebook_collection/domains/advanced_imaging/rules/tests/test_organized_rules.py`: **PASSED** (schema conformance, count verification)
- `rulebook_collection/domains/interventional_pain_management/rules/tests/test_organized_ipm_rules.py`: **PASSED** (schema conformance, count verification)
- `rulebook_collection/manifests/tests/test_phase_2e_mappings.py`: **PASSED** (9 passed)

### 3. Full Repository Test Suite
- **Total Tests Collected:** 282
- **Passed:** 271
- **Skipped:** 10
- **Failed:** 1 (`test_phase4a_governance_audit.py::test_05_core_safety_invariants` due to an existing pre-recorded review log `REV-8BA6C791A7F8` in `medrule_engine/governance/data/governance.db`; left strictly untouched per rule 3).

---

## 9. Explicit Limitations & Items Requiring Manual Verification

1. **Human Review Queue:**
   - **9 rules** across the corpus remain flagged as `NEEDS_HUMAN_REVIEW` (7 in Advanced Imaging, 2 in IPM).
   - In Advanced Imaging: `RULE-ADV-CG2025-001` (Breast MRI high-risk threshold definition), `RULE-ADV-CG2030-001` (Cardiac CT fractional flow reserve threshold), and several complex oncology PET/CT scenarios.
   - In IPM: `RULE-IPM-CGFACETDENERVATION-001` (Facet radiofrequency denervation 12-month interval restrictions) and `RULE-IPM-CGSPINALCORDSTIM-002` (Permanent SCS trial relief threshold: 50% vs 80%).
2. **State-Contract Specific Prior Auth Requirements:**
   - As documented in `missing_documents.csv`, certain state Medicaid plans exempt low-cost extremity CTs or mandate maximum annual session caps (e.g., maximum 4 epidural steroid injections per year). These rules require integration with payer-specific contract tables during engine intake.
3. **Strict Adherence to Safety Rules:**
   - In accordance with instructions, **zero files have been relocated or deleted** during this audit. The physical movement of files to `archive_candidate/` will occur only after user review and explicit authorization of [scope_cleanup_proposal.csv](file:///d:/PreAuth/rulebook_collection/manifests/scope_cleanup_proposal.csv).
