# MedRule Domain Validation Report: Sleep Health

**Date of Execution**: 2026-10-18  
**Domain Under Test**: `sleep_health`  
**Governing Document**: `2026 Evolent Clinical Guidelines - Sleep Studies.pdf` (36 physical pages)  
**Test Suite Path**: [`rulebook_collection/domains/sleep_health/rules/tests/test_sleep_rules.py`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/tests/test_sleep_rules.py)  
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
Ran 12 tests in 0.219s

OK (12 passed, 0 failed, 0 errors, 0 skipped)
```

---

## 2. Key Metrics

- **Governed Units Audited**: 3 units (Clinical Preamble, CG 2050 Attended Polysomnography, CG 2051 Unattended Home Sleep Test)
- **Total Rules Extracted**: 8 rules
- **Canonical Schema Conformance**: 100% (8 / 8 rules)
- **Verbatim Quote Fidelity**: 100% (8 / 8 quotes match PDF text layer)
- **Clinical Governance Safeguard**: Exactly 0 rules marked `APPROVED` (7 `DRAFT`, 1 `NEEDS_HUMAN_REVIEW`)
- **Traceability Matrix Alignment**: 8 rows in [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/source_to_rule_traceability.csv)
- **Coverage Inventory Status**: All 3 rows in [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/sleep_health/rules/guideline_coverage_inventory.csv) marked `VALIDATED_FOR_REVIEW`.
