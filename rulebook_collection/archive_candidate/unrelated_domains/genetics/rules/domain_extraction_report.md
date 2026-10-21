# MedRule Domain Extraction Report: Genetic Testing

**Date**: 2026-10-18  
**Domain**: `genetic_testing`  
**Governing Document**: `Genetic Testing Guidelines - July 2026.pdf` (174 physical pages, Effective: 2026-07-01, SHA-256: `60ebf009...`)  
**Coding Grid Document**: `Generic GT and Laboratory Matrix 10.01.2026.pdf` (60 physical pages, Effective: 2026-10-01, SHA-256: `f84df3a3...`)  
**Extraction Status**: **`DOMAIN_COMPLETE_VALIDATED`**

---

## 1. Scope & Corpus Breakdown

The Genetic Testing domain encompasses diagnostic and prognostic molecular genetic assays, chromosomal microarray analysis (CMA), next-generation sequencing (NGS) multigene panels, liquid biopsy circulating tumor DNA (ctDNA), minimal residual disease (MRD), pharmacogenomics, reproductive genetics, and whole exome sequencing (WES).

| Document Title | Type | Physical Pages | Governed Units | Status |
|---|---|---|---|---|
| 2026 Evolent Genetic Testing Guidelines (July 2026) | `governing_policy` | 174 | 22 | `current_2026_verified` |
| Generic Genetic Tests and Laboratory Matrix | `coding_grid` | 60 | 1 | `current_2026_verified` |
| **Total Active** | | **234 pages** | **23 units** | |

---

## 2. Rule Extraction Summary

A total of **25 atomic, source-grounded rules** were extracted:
- **Oncology Molecular Profiling**: Strict indications for tumor gene expression profiling (Oncotype DX 21-gene breast cancer recurrence score in ER+/HER2- early-stage disease), ctDNA liquid biopsy when tissue is unavailable, hematologic malignancy panels (AML/MDS), and targeted lung cancer therapies (EGFR, ALK, ROS1, BRAF, KRAS).
- **Cytogenomic Microarray (CMA)**: First-tier indications for developmental delay, intellectual disability, autism spectrum disorder, and fetal structural abnormalities on prenatal ultrasound.
- **Hereditary Cancer Syndromes**: High-risk personal and family history criteria for BRCA1/2 (HBOC) and mismatch repair genes (Lynch syndrome).
- **Reproductive Genetics**: Non-invasive prenatal screening (NIPS) via cell-free fetal DNA for common fetal trisomies (21, 18, 13) and single-gene carrier screening.
- **Advanced Diagnostics & Non-Covered Services**: Whole Exome Sequencing (WES) for rare undiagnosed pediatric phenotypes, pharmacogenomic CPIC Level A indications, and explicit non-coverage / investigational determinations for cutaneous melanoma gene expression profiling (DecisionDx).
- **Laboratory Coding Matrix**: Rules governing CPT coding, billing authorization thresholds, and molecular pathology code matching.

---

## 3. Governance State

- **Rules in `DRAFT`**: 22 rules
- **Rules in `NEEDS_HUMAN_REVIEW`**: 3 rules (Clinical preamble, Whole Exome Sequencing clinical exception, and Melanoma algorithmic assay exclusion)
- **Rules in `APPROVED`**: **0 rules** (Strict compliance with governance mandate)
- **Canonical Schema Conformance**: 100% compliant with `medrule_rule_schema.json`
- **Verbatim Text Grounding**: 100% matching the physical PDF text layers

---

## 4. Deliverable Artifacts

- [`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/draft_rules.json) (25 rules)
- [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/guideline_coverage_inventory.csv) (23 units)
- [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/source_to_rule_traceability.csv) (25 rows)
- [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/human_review_queue.csv) (3 flagged items)
- [`validation_report.md`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/validation_report.md) (12 / 12 tests passed)
