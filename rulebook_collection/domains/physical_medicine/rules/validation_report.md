# MedRule Domain Validation Report: Physical Medicine

**Date of Execution**: 2026-10-18  
**Domain Under Test**: `physical_medicine`  
**Governing Document**: `2026 Evolent Physical Medicine Guidelines_0.pdf` (143 physical pages)  
**Supplementary Documents**:
- `Active Procedures in Physical Medicine 2024_1.pdf` (21 physical pages)
- `Passive Treatment 2024_1.pdf` (10 physical pages)
- `Measurable Progressive Improvement 2024_1.pdf` (40 physical pages)
- `Outpatient Habilitative PT and OT Therapy 2024_1.pdf` (13 physical pages)
- `Outpatient Habilitative and Rehabilitative Speech Therapy 2024_1.pdf` (10 physical pages)
- `Durable Medical Equipment 2024_1.pdf` (6 physical pages)
- `Experimental Unproven or Investigational Services 2024_1.pdf` (9 physical pages)
- `Record Keeping Doc Standards Phys Medicine 2024_1.pdf` (11 physical pages)  
**Test Suite Path**: [`rulebook_collection/domains/physical_medicine/rules/tests/test_physmed_rules.py`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/tests/test_physmed_rules.py)  
**Overall Validation Result**: **PASSED (12 / 12 ASSERTION GATES SATISFIED — 100% SUCCESS)**

---

## 1. Test Execution Summary

```
test_01_total_rule_count_and_coverage ... ok
test_02_unique_rule_ids_and_naming_pattern ... ok
test_03_schema_compliance ... ok
test_04_source_pdf_resolution ... ok
test_05_page_bounds_and_validity ... ok
test_06_verbatim_quote_fidelity ... ok
test_07_no_rule_marked_approved ... ok
test_08_decision_effects_valid ... ok
test_09_condition_tree_integrity ... ok
test_10_traceability_alignment ... ok
test_11_human_review_queue_accuracy ... ok
test_12_coverage_inventory_completion ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.476s

OK (12 passed, 0 failed, 0 errors, 0 skipped)
```

---

## 2. Key Metrics

- **Governed Units Audited**: 15 units (Preamble, ECG 1512 Habilitative PT/OT/ST, ECG 1510 PT Record Keeping, ECG 1501 Infant Chiro, ECG 1509 Chiro Record Keeping, ECG 1511 Active/Passive/Exp, ECG 1504 Measurable Improvement, Active Procedures Policy, Passive Treatment Policy, Measurable Progressive Improvement Standards, Outpatient Habilitative PT/OT, Outpatient Speech Therapy, DME Policy, Experimental Services Policy, Record Keeping Standards Policy)
- **Total Rules Extracted**: 17 rules
- **Canonical Schema Conformance**: 100% (17 / 17 rules)
- **Verbatim Quote Fidelity**: 100% (17 / 17 quotes match PDF text layer)
- **Clinical Governance Safeguard**: Exactly 0 rules marked `APPROVED` (14 `DRAFT`, 3 `NEEDS_HUMAN_REVIEW`)
- **Traceability Matrix Alignment**: 17 rows in [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/source_to_rule_traceability.csv)
- **Coverage Inventory Status**: All 15 rows in [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/physical_medicine/rules/guideline_coverage_inventory.csv) marked `VALIDATED_FOR_REVIEW`.
