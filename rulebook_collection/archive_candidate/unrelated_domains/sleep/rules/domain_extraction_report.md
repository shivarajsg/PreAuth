# MedRule Domain Extraction Report: Sleep Health

**Date**: 2026-10-18  
**Domain**: `sleep_health`  
**Governing Document**: `2026 Evolent Clinical Guidelines - Sleep Studies.pdf` (36 physical pages, Effective: 2026-01-01, SHA-256: `6370bb5e...`)  
**Extraction Status**: **`DOMAIN_COMPLETE_VALIDATED`**

---

## 1. Scope & Corpus Breakdown

The Sleep Health domain governs attended in-laboratory polysomnography (PSG), multiple sleep latency testing (MSLT), split-night studies, and unattended home sleep apnea testing (HST) for pediatric and adult sleep-disordered breathing and sleep disorders.

| Document Title | Type | Physical Pages | Governed Units | Status |
|---|---|---|---|---|
| 2026 Evolent Sleep Studies Guidelines | `governing_policy` | 36 | 3 | `current_2026_verified` |
| **Total Active** | | **36 pages** | **3 units** | |

---

## 2. Rule Extraction Summary

A total of **8 atomic, source-grounded rules** were extracted:
- **Attended In-Lab Polysomnography (CG 2050)**: Detailed indications covering high-risk medical comorbidities that make unattended HST unsafe or inaccurate (moderate-to-severe COPD, hypoventilation, neuromuscular disorders, congestive heart failure NYHA III/IV); non-respiratory sleep disorder indications (suspected narcolepsy requiring daytime MSLT, parasomnias with violent behaviors); and pediatric sleep apnea evaluations (<18 years).
- **Unattended Home Sleep Testing (CG 2051)**: Standard indication criteria for adult patients with a high pretest probability of uncomplicated obstructive sleep apnea based on validated scoring tools and clinical signs (witnessed apneas, habitual snoring, Epworth Sleepiness Scale); and explicit contraindications redirecting complicated patients to attended PSG.
- **Documentation & Governance**: Mandatory requirements for comprehensive sleep evaluations, physical examination notes, and clinical judgment framework.

---

## 3. Governance State

- **Rules in `DRAFT`**: 7 rules
- **Rules in `NEEDS_HUMAN_REVIEW`**: 1 rule (Clinical preamble governance)
- **Rules in `APPROVED`**: **0 rules** (Strict compliance with governance mandate)
- **Canonical Schema Conformance**: 100% compliant with `medrule_rule_schema.json`
- **Verbatim Text Grounding**: 100% matching the physical PDF text layers

---

## 4. Deliverable Artifacts

- [`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/draft_rules.json) (8 rules)
- [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/guideline_coverage_inventory.csv) (3 units)
- [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/source_to_rule_traceability.csv) (8 rows)
- [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/human_review_queue.csv) (1 flagged item)
- [`validation_report.md`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/validation_report.md) (12 / 12 tests passed)
