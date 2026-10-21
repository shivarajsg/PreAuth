# MedRule Domain Validation Report: Genetic Testing

**Date of Execution**: 2026-10-18  
**Domain Under Test**: `genetic_testing`  
**Governing Document**: `Genetic Testing Guidelines - July 2026.pdf` (174 physical pages)  
**Coding Grid Document**: `Generic GT and Laboratory Matrix 10.01.2026.pdf` (60 physical pages)  
**Test Suite Path**: [`rulebook_collection/domains/genetic_testing/rules/tests/test_gentest_rules.py`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/tests/test_gentest_rules.py)  
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
Ran 12 tests in 0.513s

OK (12 passed, 0 failed, 0 errors, 0 skipped)
```

---

## 2. Key Metrics

- **Governed Units Audited**: 23 units (Preamble, ASD/ID Panel, Bladder Cancer, Breast Cancer Extended Endocrine, Breast Cancer Prognostic Oncotype DX, ctDNA Liquid Biopsy, Hematologic Malignancy NGS, Pregnancy Loss CMA, Prenatal CMA, DD/ID Congenital Anomalies CMA, Colorectal Prognostic, Connective Tissue Multigene, Cutaneous Melanoma, Epilepsy Panel, Solid Organ Transplant cfDNA, Lung Cancer Molecular, Colorectal MRD ctDNA, HBOC BRCA1/2, Lynch Syndrome, Pharmacogenomics, NIPS Cell-Free Fetal DNA, Whole Exome Sequencing, Carrier Screening, Laboratory Coding Matrix)
- **Total Rules Extracted**: 25 rules
- **Canonical Schema Conformance**: 100% (25 / 25 rules)
- **Verbatim Quote Fidelity**: 100% (25 / 25 quotes match PDF text layer)
- **Clinical Governance Safeguard**: Exactly 0 rules marked `APPROVED` (22 `DRAFT`, 3 `NEEDS_HUMAN_REVIEW`)
- **Traceability Matrix Alignment**: 25 rows in [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/source_to_rule_traceability.csv)
- **Coverage Inventory Status**: All 23 rows in [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/genetic_testing/rules/guideline_coverage_inventory.csv) marked `VALIDATED_FOR_REVIEW`.
