# MedRule Phase 1.5 — Reconciled Master Collection & Provenance Summary

## 1. Executive Summary
This report reconciles and verifies all collection metrics, physical files, cryptographic checksums, and document classifications across the MedRule corpus. 

All 85 manifested documents have been audited against the physical files on disk. Every document's metadata has been decoupled into orthogonal fields: **`document_type`** (clinical role) and **`version_status`** (temporal governance status), fully resolving any previous conflation between historical governing policies and historical supporting documents.

## 2. Definitive High-Level Metrics
- **Total Physical PDF Files in Workspace:** **103** (101 inside `rulebook_collection/` + 2 seed files in root).
- **Total Physical PDF Files in `rulebook_collection/`:** **101** (81 domain PDFs + 4 CMS reference PDFs + 13 legacy Phase 1 downloads + 3 seed files in `source_pdfs/`).
- **Total Unique Cryptographic Hashes (SHA-256):** **82** (81 unique hashes among manifested documents + 1 unique hash for `PreauthorizationMRI.pdf`).
- **Total Manifested Documents:** **85** (81 domain-categorized files + 4 centralized CMS cross-domain reference files).
- **Total Current 2026 Policy Documents:** **33** (18 governing policies + 12 supplementary policies + 3 coding grids).
- **Total Historical Documents Retained:** **6** (3 historical governing policies + 3 historical supporting documents).
- **Total Supporting Clinical Documents:** **41** (16 checklists + 7 forms [5 current, 2 historical] + 18 tip sheets [17 current, 1 historical]).
  - *Current 2026 Verified Supporting Documents:* **38**
  - *Historical Retained Supporting Documents:* **3**
- **Total Referenced External Sources:** **8** document entries (representing **4 unique statutory/clinical standards**, mirrored between Centene `referenced_sources/` and `cross_domain_references/cms/`).

## 3. Reconciled Document Classification Matrix

| Clinical Domain | Total PDFs | Governing Policies (Cur / Hist) | Supplementary Policies | Coding Grids | Checklists | Clinical Forms (Cur / Hist) | Tip Sheets (Cur / Hist) | External References | Minimum Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **advanced_imaging** | 11 | 1 / 1 | 1 | 0 | 2 | 1 / 1 | 3 / 1 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **cardiology** | 11 | 2 / 0 | 1 | 1 | 1 | 0 / 0 | 6 / 0 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **musculoskeletal_surgery** | 11 | 1 / 0 | 1 | 0 | 2 | 2 / 0 | 5 / 0 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **interventional_pain_management** | 7 | 1 / 1 | 1 | 0 | 1 | 1 / 1 | 1 / 0 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **radiation_oncology** | 9 | 2 / 0 | 0 | 1 | 6 | 0 / 0 | 0 / 0 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **physical_medicine** | 12 | 1 / 0 | 8 | 0 | 0 | 1 / 0 | 2 / 0 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **sleep_health** | 3 | 1 / 0 | 0 | 0 | 2 | 0 / 0 | 0 / 0 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **genetic_testing** | 4 | 1 / 0 | 0 | 1 | 2 | 0 / 0 | 0 / 0 | 0 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **centene_dme_orthotics_prosthetics** | 13 | 8 / 1 | 0 | 0 | 0 | 0 / 0 | 0 / 0 | 4 | `MINIMUM_PUBLIC_COLLECTION_COMPLETE` |
| **cross_domain_references/cms** | 4 | 0 / 0 | 0 | 0 | 0 | 0 / 0 | 0 / 0 | 4 | `CORE_STANDARDS_VERIFIED` |
| **TOTALS** | **85** | **18 / 3** | **12** | **3** | **16** | **5 / 2** | **17 / 1** | **8** | **9 of 9 Complete** |

## 4. Reconciliation of Sums
- By Document Type: $21 \\text{ governing} + 12 \\text{ supplementary} + 3 \\text{ coding grids} + 16 \\text{ checklists} + 7 \\text{ forms} + 18 \\text{ tip sheets} + 8 \\text{ references} = \\mathbf{{85}}$.
- By Version Status: $79 \\text{ current\\_2026\\_verified} + 6 \\text{ historical} = \\mathbf{{85}}$.
- Current Policies: $18 \\text{ governing} + 12 \\text{ supplementary} + 3 \\text{ coding grids} = \\mathbf{{33}}$.
- Historical Documents: $3 \\text{ governing} + 3 \\text{ supporting (2 forms + 1 tip sheet)} = \\mathbf{{6}}$.
- Supporting Documents: $16 \\text{ checklists} + 7 \\text{ forms} + 18 \\text{ tip sheets} = \\mathbf{{41}}$ (38 current + 3 historical).
