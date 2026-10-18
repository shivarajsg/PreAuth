# MedRule Phase 3B — Synthetic Benchmarking and Evaluator Integration Report

**Date:** 2026-10-18  
**Status:** **`BENCHMARKS_PASSED`**  
**Evaluator Version:** `3B.1.0`  
**Corpus Rules Loaded:** 372 rules across 9 domains  
**Total Benchmark Cases:** 30 cases (30 passed, 0 failed)  

---

## 1. Executive Summary

> [!IMPORTANT]
> **BENCHMARK EXECUTION STATUS: `BENCHMARKS_PASSED`**  
> All synthetic cases were deterministically evaluated without LLMs, probabilistic models, or neural inferences. 
> The suite achieved a **100.0% pass rate** (30 / 30), 
verifying three-valued logic, policy routing, evidence sufficiency separation, and non-binding prototype governance.

### Key Governance Invariants Verified
- **Approved Rules in Production:** Exactly **0** (Zero rules approved without licensed medical director sign-off).
- **Non-Binding Outputs:** Exactly **100%** of case assessments emit `is_binding: false`.
- **Deterministic Repeatability:** **VERIFIED** (SHA-256 hash match on identical payloads).
- **Batch Interface Error Isolation:** **VERIFIED** (Independent validation and failure containment).

---

## 2. Performance and Latency Profile

- **Platform:** `Windows-10-10.0.26300-SP0`
- **Python Version:** `3.11.5`
- **Total Batch Processing Time:** **5.77 ms**
- **System Throughput:** **5203.1 cases/second**

| Pipeline Stage | Average Latency (ms) | Target Latency (ms) | Compliance Status |
|---|---|---|---|
| **Rule Registry In-Memory Load** | 84.41 ms (all 372 rules) | < 500 ms | PASS |
| **Case Intake JSON Schema Validation** | 0.061 ms | < 5 ms | PASS |
| **Deterministic Policy Router** | 0.003 ms | < 5 ms | PASS |
| **Evidence Sufficiency Auditing** | 0.004 ms | < 5 ms | PASS |
| **Recursive Condition Evaluator** | 0.007 ms | < 5 ms | PASS |
| **End-to-End Per-Case Evaluation** | **0.115 ms** | < 25 ms | PASS |

---

## 3. Clinical Domain Benchmark Coverage

| Clinical Domain | Active Rules in Registry | Benchmark Cases Tested | Coverage Status |
|---|---|---|---|
| `advanced_imaging` | Tested across active corpus | 8 cases | VERIFIED |
| `cardiology` | Tested across active corpus | 4 cases | VERIFIED |
| `centene_dme_orthotics_prosthetics` | Tested across active corpus | 5 cases | VERIFIED |
| `genetic_testing` | Tested across active corpus | 1 cases | VERIFIED |
| `interventional_pain_management` | Tested across active corpus | 6 cases | VERIFIED |
| `musculoskeletal_surgery` | Tested across active corpus | 1 cases | VERIFIED |
| `physical_medicine` | Tested across active corpus | 1 cases | VERIFIED |
| `radiation_oncology` | Tested across active corpus | 2 cases | VERIFIED |
| `sleep_health` | Tested across active corpus | 2 cases | VERIFIED |

---

## 4. Assessment Distribution

| Assessment Status | Frequency | Logical Meaning |
|---|---|---|
| `CRITERIA_MET` | 13 | Deterministic aggregation outcome |
| `CRITERIA_NOT_MET` | 5 | Deterministic aggregation outcome |
| `INSUFFICIENT_INFORMATION` | 2 | Deterministic aggregation outcome |
| `MANUAL_REVIEW_REQUIRED` | 4 | Deterministic aggregation outcome |
| `POLICY_NOT_APPLICABLE` | 3 | Deterministic aggregation outcome |
| `POLICY_VERSION_UNRESOLVED` | 3 | Deterministic aggregation outcome |

---

## 5. Detailed Benchmark Case Inventory

| Case ID | Domain | Procedure | Expected | Actual | Latency | SHA-256 Hash | Status |
|---|---|---|---|---|---|---|---|
| `BM-CASE-01` | `advanced_imaging` | `74177` | `CRITERIA_MET` | `CRITERIA_MET` | 0.277 ms | `0d6b7ad307...` | PASS |
| `BM-CASE-02` | `advanced_imaging` | `74177` | `CRITERIA_NOT_MET` | `CRITERIA_NOT_MET` | 0.152 ms | `7d1d9a6c88...` | PASS |
| `BM-CASE-05` | `advanced_imaging` | `74177` | `CRITERIA_MET` | `CRITERIA_MET` | 0.134 ms | `4b654a63c8...` | PASS |
| `BM-CASE-07` | `advanced_imaging` | `70551` | `CRITERIA_MET` | `CRITERIA_MET` | 0.163 ms | `9e3d724a50...` | PASS |
| `BM-CASE-08` | `advanced_imaging` | `74177` | `MANUAL_REVIEW_REQUIRED` | `MANUAL_REVIEW_REQUIRED` | 0.183 ms | `fea3a11fbf...` | PASS |
| `BM-CASE-09` | `advanced_imaging` | `74177` | `POLICY_VERSION_UNRESOLVED` | `POLICY_VERSION_UNRESOLVED` | 0.199 ms | `005aa382fc...` | PASS |
| `BM-CASE-13` | `advanced_imaging` | `INVALID_CODE_99999` | `POLICY_NOT_APPLICABLE` | `POLICY_NOT_APPLICABLE` | 0.082 ms | `95d2d14514...` | PASS |
| `BM-CASE-14` | `advanced_imaging` | `74177` | `CRITERIA_MET` | `CRITERIA_MET` | 0.2 ms | `89313e8ea0...` | PASS |
| `BM-CASE-10` | `cardiology` | `76775` | `CRITERIA_MET` | `CRITERIA_MET` | 0.103 ms | `2e4f46c64d...` | PASS |
| `BM-CASE-11` | `cardiology` | `93224` | `MANUAL_REVIEW_REQUIRED` | `MANUAL_REVIEW_REQUIRED` | 0.077 ms | `511a8cb0be...` | PASS |
| `BM-CASE-26` | `cardiology` | `93320` | `CRITERIA_MET` | `CRITERIA_MET` | 0.165 ms | `845d70d013...` | PASS |
| `BM-CASE-27` | `cardiology` | `93320` | `CRITERIA_NOT_MET` | `CRITERIA_NOT_MET` | 0.126 ms | `99230a4834...` | PASS |
| `BM-CASE-06D` | `musculoskeletal_surgery` | `27447` | `CRITERIA_MET` | `CRITERIA_MET` | 0.093 ms | `4b19dbf40c...` | PASS |
| `BM-CASE-06A` | `interventional_pain_management` | `64635` | `CRITERIA_NOT_MET` | `CRITERIA_NOT_MET` | 0.098 ms | `ece2d0bd3f...` | PASS |
| `BM-CASE-06B` | `interventional_pain_management` | `64635` | `CRITERIA_MET` | `CRITERIA_MET` | 0.091 ms | `c1a44c5a8b...` | PASS |
| `BM-CASE-06C` | `interventional_pain_management` | `64635` | `CRITERIA_MET` | `CRITERIA_MET` | 0.089 ms | `146c57b7e3...` | PASS |
| `BM-CASE-23` | `interventional_pain_management` | `64635` | `INSUFFICIENT_INFORMATION` | `INSUFFICIENT_INFORMATION` | 0.098 ms | `f60600c8ab...` | PASS |
| `BM-CASE-28` | `interventional_pain_management` | `62322` | `CRITERIA_MET` | `CRITERIA_MET` | 0.087 ms | `5047f6bc58...` | PASS |
| `BM-CASE-21` | `interventional_pain_management` | `74177` | `POLICY_NOT_APPLICABLE` | `POLICY_NOT_APPLICABLE` | 0.074 ms | `c14b3b5399...` | PASS |
| `BM-CASE-30` | `radiation_oncology` | `77301` | `CRITERIA_MET` | `CRITERIA_MET` | 0.086 ms | `295bb4b304...` | PASS |
| `BM-CASE-16` | `radiation_oncology` | `77301` | `POLICY_NOT_APPLICABLE` | `POLICY_NOT_APPLICABLE` | 0.066 ms | `388814c6a3...` | PASS |
| `BM-CASE-04` | `physical_medicine` | `97110` | `CRITERIA_NOT_MET` | `CRITERIA_NOT_MET` | 0.085 ms | `225c291608...` | PASS |
| `BM-CASE-29` | `sleep_health` | `95806` | `CRITERIA_MET` | `CRITERIA_MET` | 0.103 ms | `491545b0b3...` | PASS |
| `BM-CASE-15` | `sleep_health` | `95810` | `MANUAL_REVIEW_REQUIRED` | `MANUAL_REVIEW_REQUIRED` | 0.07 ms | `41a148a046...` | PASS |
| `BM-CASE-18` | `genetic_testing` | `81408` | `CRITERIA_MET` | `CRITERIA_MET` | 0.088 ms | `e9792f2b2c...` | PASS |
| `BM-CASE-03` | `centene_dme_orthotics_prosthetics` | `E0601` | `INSUFFICIENT_INFORMATION` | `INSUFFICIENT_INFORMATION` | 0.105 ms | `fb95f80619...` | PASS |
| `BM-CASE-12` | `centene_dme_orthotics_prosthetics` | `A6501` | `CRITERIA_NOT_MET` | `CRITERIA_NOT_MET` | 0.095 ms | `4b85981a53...` | PASS |
| `BM-CASE-19` | `centene_dme_orthotics_prosthetics` | `E2510` | `MANUAL_REVIEW_REQUIRED` | `MANUAL_REVIEW_REQUIRED` | 0.119 ms | `736f01ce71...` | PASS |
| `BM-CASE-20` | `centene_dme_orthotics_prosthetics` | `K0001` | `POLICY_VERSION_UNRESOLVED` | `POLICY_VERSION_UNRESOLVED` | 0.071 ms | `8bba9662c8...` | PASS |
| `BM-CASE-22` | `centene_dme_orthotics_prosthetics` | `K0001` | `POLICY_VERSION_UNRESOLVED` | `POLICY_VERSION_UNRESOLVED` | 0.073 ms | `1e69f4dceb...` | PASS |

---

## 6. Audit Trail and Provenance Verification

Every evaluated rule audit payload was verified to include:
1. Full policy provenance: `policy_title`, `policy_version`, `version_status`, `source_file`, `physical_page`, and verbatim `source_quote`.
2. Step-by-step condition evaluation tree with condition IDs, comparators, expected thresholds, and actual observed evidence values.
3. Evidence verification reports detailing supplied parameters, missing parameters, and required documentation.
4. Canonical SHA-256 content hash computed over normalized metadata for 100% bitwise audit reproducibility.

---

## 7. Scope and Limitations

> [!NOTE]
> 1. **Synthetic Data Exclusively:** All benchmark cases utilize non-identifiable, synthetic clinical vectors.
> 2. **Non-Binding Prototype Guardrail:** MedRule remains a decision support prototype; no real-world prior authorization decisions are rendered.
> 3. **Payer-Specific Integrations:** Health-plan carve-outs, contract fee schedules, and real-time EHR integrations remain out of scope for Phase 3B.

**Benchmark Auditor:** MedRule Deterministic Engine Integration Team  
**Audit Status:** `BENCHMARKS_PASSED`
