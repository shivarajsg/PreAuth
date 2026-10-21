# MedRule Policy Collection Repository

This repository contains the official, verified prior-authorization clinical guidelines, coding standards, place-of-service policies, and supporting documentation for **MedRule**, an initiative to construct a deterministic, rule-based medical prior-authorization decision engine without reliance on third-party LLM APIs or external AI inference services.

---

## 1. Directory Structure

```text
rulebook_collection/
│
├── source_pdfs/
│   ├── PreauthorizationMRI.pdf                               # Original Phase 1 Seed PDF 1 (Evolent / NIA)
│   ├── CP.MP.107(4).pdf                                      # Original Phase 1 Seed PDF 2 (Centene DMEPOS)
│   └── CP.MP.107.pdf                                         # Working copy of Seed PDF 2
│
├── downloaded_pdfs/                                          # Intact historical downloads from Phase 1 (13 files)
│
├── domains/                                                  # Nine domain-specific policy stores
│   ├── advanced_imaging/
│   ├── cardiology/
│   ├── musculoskeletal_surgery/
│   ├── interventional_pain_management/
│   ├── radiation_oncology/
│   ├── physical_medicine/
│   ├── sleep_health/
│   ├── genetic_testing/
│   └── centene_dme_orthotics_prosthetics/
│
├── cross_domain_references/                                  # Multi-domain external standards
│   └── cms/                                                  # CMS manuals, DMEPOS quality standards, RESNA papers
│
├── manifests/                                                # Master inventories and audit trails
│   ├── master_pdf_inventory.csv                              # 25-column master catalog of all 85 PDFs
│   ├── domain_inventory.csv                                  # Domain summary statistics and completion statuses
│   ├── policy_versions.csv                                   # 2025 vs 2026 edition and revision diffs
│   ├── missing_documents.csv                                 # Plan-specific access limitations and gaps
│   ├── duplicate_documents.csv                               # Cross-domain shared references and hash tracking
│   ├── download_summary.md                                   # Reconciled Phase 1.5 markdown summary report
│   ├── final_audit_report.md                                 # Final audit report and Phase 2 readiness gate verdict
│   ├── pdf_inventory.csv                                     # Phase 1 seed link download inventory
│   └── download_summary.txt                                  # Phase 1 link discovery report
│
└── README.md                                                 # Top-level repository documentation
```

---

## 2. Standardized Domain Directory Architecture

Each domain directory under `domains/<domain_name>/` adheres strictly to this standardized layout:

```text
domains/<domain>/
│
├── policy_pdfs/
│   ├── current_2026/                                         # Active, governing 2026 clinical guidelines & coding policies
│   └── historical_versions/                                  # Superseded 2025/2024 editions retained for version diffing
│
├── supporting_pdfs/
│   ├── checklists/                                           # Provider prior-authorization clinical intake checklists
│   ├── forms/                                                # Standardized conservative treatment and attestation forms
│   └── tip_sheets/                                           # Clinical decision algorithms and CPT crosswalk guidance
│
├── referenced_sources/                                       # Official external manuals and statutory citations
│
├── rules/
│   └── README.md                                             # Placeholder stating criteria JSON is deferred to Phase 2
│
├── policies_index.csv                                        # Domain-level document inventory with types & dates
└── domain_summary.md                                         # Narrative summary addressing domain scope & metrics
```

---

## 3. Scope Separation and Phase Boundaries

- **Phase 1 (Completed):** Discovered all URLs embedded in the two seed documents (`PreauthorizationMRI.pdf` and `CP.MP.107.pdf`), downloaded all 13 directly linked PDFs into `downloaded_pdfs/`, and generated `manifests/pdf_inventory.csv`.
- **Phase 1.5 (Completed):** Expanded the collection domain-wise across 9 clinical specialties, downloaded current 2026 governing guidelines from official publishers (Evolent/RadMD, Centene, CMS), preserved historical editions, organized supporting clinical forms/checklists/tip sheets, and compiled comprehensive audit manifests.
- **Phase 2 (Next Phase):** Deterministic extraction of medical necessity criteria, clinical indications, diagnostic thresholds, contraindications, and conservative treatment rules into machine-readable JSON schemas inside each domain's `rules/` directory. **No rule extraction or evaluator coding is performed in Phase 1.5.**

---

## 4. Manifest Descriptions

1. `master_pdf_inventory.csv`: Complete catalog of all 85 documents across 25 standardized metadata fields, including SHA-256 hashes, file sizes, page counts, PyMuPDF validation statuses, publication dates, effective dates, and official source URLs.
2. `domain_inventory.csv`: High-level overview of the 9 domains, quantifying current policies, historical versions, supporting documents, and assigned minimum public collection completion status.
3. `policy_versions.csv`: Detailed version tracking comparing 2025/2024 editions against 2026 governing policies (e.g. Advanced Imaging 2025 vs 2026, IPM 2025 vs 2026, Centene CP.MP.107 Revision 11/24 vs 08/26).
4. `missing_documents.csv`: Rigorous log of plan-specific access requirements, state Medicaid fee schedules, and proprietary commercial health plan authorization grids that require provider portal logins.
5. `duplicate_documents.csv`: Tracking of shared cross-domain references (such as CMS manuals shared between Centene and Cross-Domain stores) confirming cryptographic integrity and zero unmanaged file collisions.
6. `download_summary.md`: Detailed narrative report summarizing totals, findings, and verification results.
7. `final_audit_report.md`: Forensic audit report validating physical files, hashes, reconciled classifications, and Phase 2 readiness gate verdict.
