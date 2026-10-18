# MedRule Domain Validation Report: Cardiology

**Date of Execution**: 2026-10-18  
**Domain Under Test**: `cardiology`  
**Governing Documents**:
- `2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf` (243 physical pages)
- `2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf` (440 physical pages)  
**Supplementary Documents**:
- `Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf` (3 physical pages)
- `Cardiovascular Service Group Grid_January2026.pdf` (9 physical pages)  
**Test Suite Path**: [`rulebook_collection/domains/cardiology/rules/tests/test_cardiology_rules.py`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/tests/test_cardiology_rules.py)  
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
Ran 12 tests in 1.626s

OK (12 passed, 0 failed, 0 errors, 0 skipped)
```

---

## 2. Key Metrics

- **Governed Units Audited**: 57 units (12 Diagnostic CGs, 41 Interventional CGs, 2 Preambles, 1 Claim Edit, 1 Service Group Grid)
- **Total Rules Extracted**: 61 rules
- **Canonical Schema Conformance**: 100% (61 / 61 rules)
- **Verbatim Quote Fidelity**: 100% (61 / 61 quotes match PDF text layer)
- **Clinical Governance Safeguard**: Exactly 0 rules marked `APPROVED` (58 `DRAFT`, 3 `NEEDS_HUMAN_REVIEW`)
- **Traceability Matrix Alignment**: 61 rows in [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/source_to_rule_traceability.csv)
- **Coverage Inventory Status**: All 57 rows in [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/cardiology/rules/guideline_coverage_inventory.csv) marked `VALIDATED_FOR_REVIEW`.
