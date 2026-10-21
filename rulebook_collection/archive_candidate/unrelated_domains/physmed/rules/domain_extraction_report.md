# MedRule Domain Extraction Report: Physical Medicine

**Date**: 2026-10-18  
**Domain**: `physical_medicine`  
**Governing Document**: `2026 Evolent Physical Medicine Guidelines_0.pdf` (143 physical pages, Effective: 2026-07-01, SHA-256: `6370bb5e...`)  
**Supplementary Documents**:
- `Active Procedures in Physical Medicine 2024_1.pdf` (21 pages, Active 2024-2026)
- `Passive Treatment 2024_1.pdf` (10 pages, Active 2024-2026)
- `Measurable Progressive Improvement 2024_1.pdf` (40 pages, Active 2024-2026)
- `Outpatient Habilitative PT and OT Therapy 2024_1.pdf` (13 pages, Active 2024-2026)
- `Outpatient Habilitative and Rehabilitative Speech Therapy 2024_1.pdf` (10 pages, Active 2024-2026)
- `Durable Medical Equipment 2024_1.pdf` (6 pages, Active 2024-2026)
- `Experimental Unproven or Investigational Services 2024_1.pdf` (9 pages, Active 2024-2026)
- `Record Keeping Doc Standards Phys Medicine 2024_1.pdf` (11 pages, Active 2024-2026)  
**Extraction Status**: **`DOMAIN_COMPLETE_VALIDATED`**

---

## 1. Scope & Corpus Breakdown

The Physical Medicine domain governs outpatient restorative and habilitative physical therapy (PT), occupational therapy (OT), speech-language pathology (ST), chiropractic manipulation, passive therapeutic modalities, durable medical equipment, and progressive recovery standards.

| Document Title | Type | Physical Pages | Governed Units | Status |
|---|---|---|---|---|
| 2026 Evolent Physical Medicine Guidelines | `governing_policy` | 143 | 7 | `current_2026_verified` |
| Active Procedures Policy | `supplementary_policy` | 21 | 1 | `current_2026_verified` |
| Passive Treatment Modalities Policy | `supplementary_policy` | 10 | 1 | `current_2026_verified` |
| Measurable Progressive Improvement Standards | `supplementary_policy` | 40 | 1 | `current_2026_verified` |
| Outpatient Habilitative PT and OT Policy | `supplementary_policy` | 13 | 1 | `current_2026_verified` |
| Outpatient Speech Therapy Policy | `supplementary_policy` | 10 | 1 | `current_2026_verified` |
| Durable Medical Equipment Policy | `supplementary_policy` | 6 | 1 | `current_2026_verified` |
| Experimental or Investigational Services Policy | `supplementary_policy` | 9 | 1 | `current_2026_verified` |
| Record Keeping and Documentation Standards | `supplementary_policy` | 11 | 1 | `current_2026_verified` |
| **Total Active** | | **263 pages** | **15 units** | |

---

## 2. Rule Extraction Summary

A total of **17 atomic, source-grounded rules** were extracted:
- **Active Rehabilitation Procedures**: Mandatory requirement for active patient participation, individualized therapeutic exercise, and functional restoration.
- **Passive Modalities (Ultrasound, Diathermy, Hot/Cold Packs)**: Strict limitation restricting passive care to the acute phase with mandatory concurrent transition to active exercise.
- **Measurable Progressive Improvement (MPI)**: Objective standard requiring quantifiable gains on validated functional outcome measures; explicit non-coverage for therapy continuation beyond a documented functional plateau.
- **Habilitative & Pediatric PT/OT/Speech**: Guidelines distinguishing developmental delay skills acquisition from maintenance programs.
- **Durable Medical Equipment (DME)**: Criteria for home therapeutic devices (TENS/NMES).
- **Experimental & Investigational Services**: Explicit non-coverage determinations for unproven physical medicine interventions.
- **Documentation Standards**: Strict requirements for initial evaluations, objective baselines, timed coding documentation, and re-evaluations.

---

## 3. Governance State

- **Rules in `DRAFT`**: 14 rules
- **Rules in `NEEDS_HUMAN_REVIEW`**: 3 rules (Clinical preamble, infant chiropractic care exceptions, and experimental service borderline determination)
- **Rules in `APPROVED`**: **0 rules** (Strict compliance with governance mandate)
- **Canonical Schema Conformance**: 100% compliant with `medrule_rule_schema.json`
- **Verbatim Text Grounding**: 100% matching the physical PDF text layers

---

## 4. Deliverable Artifacts

- [`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/draft_rules.json) (17 rules)
- [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/guideline_coverage_inventory.csv) (15 units)
- [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/source_to_rule_traceability.csv) (17 rows)
- [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/human_review_queue.csv) (3 flagged items)
- [`validation_report.md`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/validation_report.md) (12 / 12 tests passed)
