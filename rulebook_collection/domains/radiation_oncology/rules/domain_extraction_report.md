# MedRule Domain Extraction Report: Radiation Oncology

**Date**: 2026-10-18  
**Domain**: `radiation_oncology`  
**Governing Documents**:
- `ECG 7000 for Radiation Therapy Services 2026_final.pdf` (67 physical pages, Effective: 2026-01-01, SHA-256: `18e47451...`)
- `ECG 7001 for Proton Beam Radiation Therapy and Neutron Beam Radiation Therapy Services 2026_final.pdf` (12 physical pages, Effective: 2026-01-01, SHA-256: `b95150a6...`)  
**Coding Grid Document**: `2026 Evolent Coding Standards FINAL 121225  L-NIA.pdf` (26 physical pages, Effective: 2026-01-01, SHA-256: `3b4918e9...`)  
**Extraction Status**: **`DOMAIN_COMPLETE_VALIDATED`**

---

## 1. Scope & Corpus Breakdown

The Radiation Oncology domain encompasses definitive, adjuvant, neoadjuvant, and palliative radiation treatment planning and delivery techniques across 3D Conformal Radiation Therapy (3D-CRT), Intensity Modulated Radiation Therapy (IMRT), Stereotactic Radiosurgery (SRS), Stereotactic Body Radiotherapy (SBRT), Brachytherapy, Proton Beam Radiation Therapy (PBRT), and Neutron Beam Radiation Therapy (NBRT).

| Document Title | Type | Physical Pages | Governed Units | Status |
|---|---|---|---|---|
| ECG 7000 Radiation Therapy Services (2026 Final) | `governing_policy` | 67 | 9 | `current_2026_verified` |
| ECG 7001 Proton Beam & Neutron Beam Services (2026 Final) | `governing_policy` | 12 | 4 | `current_2026_verified` |
| 2026 Evolent Radiation Oncology Coding Standards | `coding_grid` | 26 | 2 | `current_2026_verified` |
| **Total Active** | | **105 pages** | **15 units** | |

---

## 2. Rule Extraction Summary

A total of **15 atomic, source-grounded rules** were extracted:
- **Central Nervous System**: SRS/SBRT indications for brain metastases, meningioma, and acoustic neuroma versus IMRT/3D-CRT.
- **Prostate Cancer**: Risk-stratified EBRT, SBRT (5-fraction regimens), and low-dose/high-dose rate brachytherapy.
- **Breast Cancer**: Whole breast hypofractionation, accelerated partial breast irradiation (APBI), and post-mastectomy radiation.
- **Head and Neck Cancer**: IMRT criteria for normal tissue sparing (salivary glands, optic pathways, brainstem).
- **Lung Cancer**: SBRT for medically inoperable early-stage NSCLC and chemoradiation for locally advanced disease.
- **Particle Beam Therapy (ECG 7001)**: Strictly bounded indications for proton beam therapy (chordomas, chondrosarcomas of skull base, ocular melanoma, pediatric malignancies) and neutron therapy (inoperable salivary gland malignancies).
- **Coding Standards**: Rules governing simulation billing, 3D conformal planning limitations, and inverse-planned IMRT dosimetry billing.

---

## 3. Governance State

- **Rules in `DRAFT`**: 13 rules
- **Rules in `NEEDS_HUMAN_REVIEW`**: 2 rules (PBRT re-irradiation tolerance and NBRT salivary gland exceptions)
- **Rules in `APPROVED`**: **0 rules** (Strict compliance with governance mandate)
- **Canonical Schema Conformance**: 100% compliant with `medrule_rule_schema.json`
- **Verbatim Text Grounding**: 100% matching the physical PDF text layers

---

## 4. Deliverable Artifacts

- [`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/draft_rules.json) (15 rules)
- [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/guideline_coverage_inventory.csv) (15 units)
- [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/source_to_rule_traceability.csv) (15 rows)
- [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/human_review_queue.csv) (2 flagged items)
- [`validation_report.md`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/validation_report.md) (12 / 12 tests passed)
