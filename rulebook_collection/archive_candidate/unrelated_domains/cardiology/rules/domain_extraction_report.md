# MedRule Domain Extraction Report: Cardiology

**Date**: 2026-10-18  
**Domain**: `cardiology`  
**Governing Documents**:
- `2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf` (243 physical pages, Version 2026, SHA-256: `41eb4f01...`)
- `2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf` (440 physical pages, Version 2026 v2, SHA-256: `ce458a26...`)  
**Supplementary Documents**:
- `Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf` (3 physical pages, Rev. 03/2024, OP.388.01)
- `Cardiovascular Service Group Grid_January2026.pdf` (9 physical pages, January 2026)  
**Extraction Status**: **`DOMAIN_COMPLETE_VALIDATED`**

---

## 1. Scope & Corpus Breakdown

The Cardiology domain encompasses comprehensive medical necessity guidelines for non-invasive diagnostic cardiac testing, electrophysiology, catheterization, percutaneous interventions, cardiac surgery, and vascular procedures.

| Document Title | Type | Physical Pages | Governed Units | Status |
|---|---|---|---|---|
| 2026 Evolent Diagnostic Cardiology Guidelines | `governing_policy` | 243 | 13 (Preamble + 12 CGs) | `current_2026_verified` |
| 2026 Evolent Interventional Cardiology Guidelines (v2) | `governing_policy` | 440 | 42 (Preamble + 41 CGs) | `current_2026_verified` |
| Cardiac Claim Edit: Stress Echo & Doppler (OP.388.01) | `supplementary_policy` | 3 | 1 | `current_2026_verified` |
| Cardiovascular Service Group Grid (January 2026) | `coding_grid` | 9 | 1 | `current_2026_verified` |
| **Total** | | **695 pages** | **57 units** | |

---

## 2. Rule Extraction Summary

A total of **61 atomic, source-grounded rules** were extracted:
- **Diagnostic Cardiology Guidelines (CG 7275 - CG 7337)**: 16 rules covering CCTA (pretest probability, Duke treadmill criteria), Calcium Scoring (ASCVD risk ranges), FFR-CT, Heart PET, Heart CT, Heart MRI, MUGA, MPI, Stress Echocardiogram, TEE, and TTE (valvular indications).
- **Interventional Cardiology Guidelines (CG 7251 - CG 7340)**: 41 rules covering Aortic Ultrasound, Ambulatory Monitoring, ABI, CABG, AVR, Carotid Endarterectomy/Stenting, Pacemakers, ICDs, GDMT, AFib Ablation, PCI, MitraClip, Watchman LAAO, and Peripheral Interventions.
- **Preambles & Administrative Criteria**: 2 rules establishing good medical practice clinical judgment standards.
- **Claim Edits & Coding Grids**: 2 rules governing Doppler add-on billing denial conditions (OP.388.01) and service group coding prerequisites.

---

## 3. Governance State

- **Rules in `DRAFT`**: 58 rules
- **Rules in `NEEDS_HUMAN_REVIEW`**: 3 rules (Clinical preambles and claim edit clinical exceptions)
- **Rules in `APPROVED`**: **0 rules** (Strict compliance with governance mandate)
- **Canonical Schema Conformance**: 100% compliant with `medrule_rule_schema.json`
- **Verbatim Text Grounding**: 100% matching the physical PDF text layers

---

## 4. Deliverable Artifacts

- [`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/draft_rules.json) (61 rules)
- [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/guideline_coverage_inventory.csv) (57 units)
- [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/source_to_rule_traceability.csv) (61 rows)
- [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/human_review_queue.csv) (3 flagged items)
- [`validation_report.md`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/validation_report.md) (12 / 12 tests passed)
