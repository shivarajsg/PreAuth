# MedRule Domain Extraction Report: Interventional Pain Management

**Date**: 2026-10-18  
**Domain**: `interventional_pain_management`  
**Governing Document**: `2026 Evolent Interventional Pain Management Guidelines.pdf` (102 physical pages, Effective: 2026-07-01, SHA-256: `6b7d15f3...`)  
**Supplementary Document**: `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` (8 physical pages, Effective: 2026-08-01, SHA-256: `18e4ba43...`)  
**Historical Documents Quarantined**: `2025 Evolent Interventional Pain Management Guidelines.pdf` (75 pages, `historical` — excluded from active rulebase)  
**Extraction Status**: **`DOMAIN_COMPLETE_VALIDATED`**

---

## 1. Scope & Corpus Breakdown

The Interventional Pain Management domain governs invasive diagnostic blocks, therapeutic injections, neuromodulation, and intrathecal drug delivery procedures for chronic axial spine, radicular, and complex regional pain syndromes.

| Document Title | Type | Physical Pages | Governed Units | Status |
|---|---|---|---|---|
| 2026 Evolent Interventional Pain Management Guidelines | `governing_policy` | 102 | 9 | `current_2026_verified` |
| Evolent Place of Service Policy 1755 for IPM | `supplementary_policy` | 8 | 1 | `current_2026_verified` |
| **Total Active** | | **110 pages** | **10 units** | |

---

## 2. Rule Extraction Summary

A total of **14 atomic, source-grounded rules** were extracted:
- **Epidural Spine Injections (ESI)**: Medical necessity criteria for interlaminar, transforaminal, and caudal injections for radicular pain refractory to conservative therapy.
- **Facet Joint Injections & Denervation (RFA)**: Structured criteria establishing dual consecutive diagnostic medial branch blocks demonstrating $\ge 50\%$ relief prior to radiofrequency neurotomy.
- **Sacroiliac Joint Injections**: Fluoroscopically or CT-guided diagnostic and therapeutic block thresholds.
- **Implantable Infusion Pumps**: Indications for intractable malignant pain or severe chronic non-malignant refractory pain.
- **Spinal Cord Stimulation (SCS)**: Explicit prerequisite for a successful temporary trial achieving $\ge 50\%$ objective pain and functional relief prior to permanent neurostimulator implantation.
- **Sympathetic Nerve Blocks**: Criteria for Complex Regional Pain Syndrome (CRPS) types I and II.
- **Place of Service (EPOS 1755)**: Freestanding office / ambulatory surgery center alignment and hospital outpatient exception handling.

---

## 3. Governance State

- **Rules in `DRAFT`**: 12 rules
- **Rules in `NEEDS_HUMAN_REVIEW`**: 2 rules (Preamble clinical judgment framework and Intrathecal Infusion Pump clinical exceptions)
- **Rules in `APPROVED`**: **0 rules** (Strict compliance with governance mandate)
- **Canonical Schema Conformance**: 100% compliant with `medrule_rule_schema.json`
- **Verbatim Text Grounding**: 100% matching the physical PDF text layers

---

## 4. Deliverable Artifacts

- [`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json) (14 rules)
- [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/guideline_coverage_inventory.csv) (10 units)
- [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/source_to_rule_traceability.csv) (14 rows)
- [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/human_review_queue.csv) (2 flagged items)
- [`validation_report.md`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/validation_report.md) (12 / 12 tests passed)
