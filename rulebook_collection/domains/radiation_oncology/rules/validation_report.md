# MedRule Domain Validation Report: Radiation Oncology

**Date of Execution**: 2026-10-18  
**Domain Under Test**: `radiation_oncology`  
**Governing Documents**:
- `ECG 7000 for Radiation Therapy Services 2026_final.pdf` (67 physical pages)
- `ECG 7001 for Proton Beam Radiation Therapy and Neutron Beam Radiation Therapy Services 2026_final.pdf` (12 physical pages)  
**Coding Grid Document**: `2026 Evolent Coding Standards FINAL 121225  L-NIA.pdf` (26 physical pages)  
**Test Suite Path**: [`rulebook_collection/domains/radiation_oncology/rules/tests/test_radonc_rules.py`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/tests/test_radonc_rules.py)  
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
Ran 12 tests in 0.402s

OK (12 passed, 0 failed, 0 errors, 0 skipped)
```

---

## 2. Key Metrics

- **Governed Units Audited**: 15 units (General Documentation, CNS SRS, Prostate Cancer, Breast Cancer, Head & Neck IMRT, Lung Cancer SBRT, Colorectal Neoadjuvant, Gynecologic, Bone Palliation, PBRT Indications, Pediatric PBRT, Re-irradiation PBRT, NBRT Salivary, 3D Planning Standards, IMRT Planning Standards)
- **Total Rules Extracted**: 15 rules
- **Canonical Schema Conformance**: 100% (15 / 15 rules)
- **Verbatim Quote Fidelity**: 100% (15 / 15 quotes match PDF text layer)
- **Clinical Governance Safeguard**: Exactly 0 rules marked `APPROVED` (13 `DRAFT`, 2 `NEEDS_HUMAN_REVIEW`)
- **Traceability Matrix Alignment**: 15 rows in [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/source_to_rule_traceability.csv)
- **Coverage Inventory Status**: All 15 rows in [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/radiation_oncology/rules/guideline_coverage_inventory.csv) marked `VALIDATED_FOR_REVIEW`.
