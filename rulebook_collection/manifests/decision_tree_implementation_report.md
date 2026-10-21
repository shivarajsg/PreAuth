# MedRule Deterministic Decision-Tree Layer: Implementation & Verification Report

**Document ID:** MEDRULE-REP-DECISION-TREE-001  
**Execution Date:** 2026-10-21  
**Status:** IMPLEMENTED & VERIFIED (TEST SUITE 100% PASSING)  
**Clinical Scope:** Advanced Imaging & Interventional Pain Management (IPM)  
**Approved Rules Count:** 0 (Zero-Approval Invariant Enforced)  
**System Classification:** Non-binding clinical decision-support software prototype  

---

## 1. Executive Summary & Scope Governance

The deterministic decision-tree layer for the MedRule Prior Authorization engine has been implemented and verified. In accordance with strict scope controls, all operations adhere to the following non-negotiable boundaries:

1. **Active Clinical Scope Isolation:** Restricted strictly to the two active clinical domains:
   - `advanced_imaging` (114 active rules)
   - `interventional_pain_management` (14 active rules)
   - All unrelated domains remain isolated in `rulebook_collection/archive_candidate/`.
2. **Preservation of 128 Active Rules:** All 128 active rule IDs, source document citations, physical page coordinates, source quotes, and extraction statuses are fully preserved with zero dropped records.
3. **Strict Compilation Partitioning (121 Ready / 7 Blocked):**
   - **121 Rules Compiled:** Successfully compiled into deterministic, tree-structured evaluation nodes.
   - **7 Rules Blocked:** Explicitly blocked at the engine gate (`GOVERNANCE_BLOCKED_RULE_IDS`) from autonomous decision logic. Any evaluation invoking these rules immediately halts and escalates to `NEEDS_HUMAN_REVIEW`.
4. **Zero Approved Invariant:** Exactly 0 rules are marked `APPROVED`. All 128 rules maintain `is_approved = False`.
5. **Zero LLM / Probabilistic Logic:** The decision-tree engine relies exclusively on closed-form Boolean logic and deterministic relational comparators. No external APIs, neural language models, or probabilistic estimators are used.
6. **Dual-Track Separation:** Clinical necessity determinations are separated from Place of Service (site-of-care) determinations.

---

## 2. Decision-Tree Architecture & Engine Design

The decision tree implementation resides in [`medrule_engine/decision_tree.py`](file:///d:/PreAuth/medrule_engine/decision_tree.py) and is exposed via [`EvaluationService.evaluate_decision_tree()`](file:///d:/PreAuth/medrule_engine/evaluation_service.py) and the CLI flag `medrule evaluate --tree`.

### 2.1 Core Architectural Components

```
                    +------------------------------------+
                    |        CaseIntake Payload          |
                    +-----------------+------------------+
                                      |
                                      v
                    +------------------------------------+
                    |       CaseSchema Validation        |
                    +-----------------+------------------+
                                      |
                                      v
                    +------------------------------------+
                    |       Domain Isolation Gate        |
                    |   (advanced_imaging / ipm only)    |
                    +-----------------+------------------+
                                      |
                                      v
                    +------------------------------------+
                    |     Policy Applicability Router    |
                    +--------+------------------+--------+
                             |                  |
                             v                  v
                 [CLINICAL NECESSITY]   [PLACE OF SERVICE]
                             |                  |
            +----------------v---+          +---v----------------+
            | Governance Gate    |          | Governance Gate    |
            | (Block 7 HR Rules) |          | (Block 7 HR Rules) |
            +----------------+---+          +---+----------------+
                             |                  |
            +----------------v---+          +---v----------------+
            | 3-Valued Logic     |          | 3-Valued Logic     |
            | Decision Tree      |          | Site-of-Care Tree  |
            +----------------+---+          +---+----------------+
                             \                  /
                              \                /
                               v              v
                    +------------------------------------+
                    |      Dual-Track Aggregation        |
                    | (CN: MET/NOT_MET/INSUFFICIENT)     |
                    | (POS: MET/NOT_MET/INSUFFICIENT)    |
                    +-----------------+------------------+
                                      |
                                      v
                    +------------------------------------+
                    |   Coverage Gap Escalation Engine   |
                    |  (Known Ambiguities -> Human Rev)  |
                    +-----------------+------------------+
                                      |
                                      v
                    +------------------------------------+
                    |    Deterministic SHA-256 Hash      |
                    |    + Audit Provenance Output       |
                    +--------------------+---------------+
```

### 2.2 Three-Valued Logic & Uncertainty Preservation

The engine implements Kleene 3-valued Boolean logic across evaluation trees:
- `TRUE`: Criterion is satisfied by documented clinical evidence.
- `FALSE`: Criterion is evaluated and fails against documented evidence.
- `UNKNOWN`: Evidence for criterion is missing, null, or ambiguous.

**Truth Tables & Short-Circuit Semantics:**
- `ALL_OF`:
  - If any mandatory criterion is `FALSE`, the group short-circuits to `FALSE` (`CRITERIA_NOT_MET`).
  - If no criterion is `FALSE` and any mandatory criterion is `UNKNOWN`, the group evaluates to `UNKNOWN` (`INSUFFICIENT_INFORMATION`).
  - The group evaluates to `TRUE` (`CRITERIA_MET`) if and only if all mandatory criteria are `TRUE`.
- `ANY_OF`:
  - If any alternative is `TRUE`, the group short-circuits to `TRUE` (`CRITERIA_MET`).
  - If all alternatives are `FALSE`, the group evaluates to `FALSE` (`CRITERIA_NOT_MET`).
  - If no alternative is `TRUE` and at least one is `UNKNOWN`, the group evaluates to `UNKNOWN` (`INSUFFICIENT_INFORMATION`).
- `NONE_OF`:
  - If any alternative is `TRUE`, the group evaluates to `FALSE`.
  - If all alternatives are `FALSE`, the group evaluates to `TRUE`.
  - If any alternative is `UNKNOWN`, the group evaluates to `UNKNOWN`.

**Critical Mandate:** Missing evidence never satisfies a clinical criterion. The engine never defaults `UNKNOWN` to `TRUE`.

---

## 3. Governance Partitioning: 121 Compiled Rules vs 7 Blocked Rules

### 3.1 The 7 Blocked Rules (`NEEDS_HUMAN_REVIEW`)

All 7 rules are unconditionally intercepted by the governance gate in `decision_tree.py` before condition evaluation. Autonomous execution is permanently disabled:

| Rule ID | Domain | Policy Source | Physical Page | Source Section | Source Quote | Blocking Rationale |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| `RULE-ADV-PREAMBLE-001` | Advanced Imaging | 2026 Evolent Advanced Imaging v2 | 8 | STATEMENT / General Information | *"guidelines and clinical judgment"* | Establishes clinical judgment override framework; non-deterministic preamble. |
| `RULE-ADV-CG2000-003` | Advanced Imaging | 2026 Evolent Advanced Imaging v2 | 10 | Headache / Chronic Headache | *"MRI should be considered in < 35yo"* | Advisory clinical recommendation ("should be considered"), not a deterministic mandate. |
| `RULE-ADV-CG2001-001` | Advanced Imaging | 2026 Evolent Advanced Imaging v2 | 13 | Abdomen / Coding Instructions | *"Anti-unbundling rules for CT Abdomen & Pelvis"* | Claims adjudication anti-unbundling rule; requires billing edits rather than clinical necessity logic. |
| `RULE-ADV-CG2066-001` | Advanced Imaging | 2026 Evolent Advanced Imaging v2 | 805 | Retrospective Review / Emergent | *"Physician clinical determination of life/limb threat"* | Retrospective emergency review requiring physician medical director determination. |
| `RULE-ADV-CG2066-002` | Advanced Imaging | 2026 Evolent Advanced Imaging v2 | 805 | Retrospective Review / Urgent | *"Retrospective review for urgent circumstances"* | Retrospective urgent review requiring peer-to-peer physician evaluation. |
| `RULE-IPM-PREAMBLEIPM-001` | IPM | 2026 Evolent IPM Guidelines | 7 | General Information / Overview | *"standards of good medical practice"* | High-level clinical judgment override preamble. |
| `RULE-IPM-CGINFUSIONPUMPS-001` | IPM | 2026 Evolent IPM Guidelines | 58 | Implantable Intrathecal Pump | *"trial titration and neuropsychological evaluation"* | High-acuity invasive therapy requiring multidisciplinary clinician assessment. |

### 3.2 The 121 Deterministically Compiled Rules

| Modality / Procedure Category | Active Rules Count | Ready for Compilation | Blocked from Autonomy |
| :--- | :---: | :---: | :---: |
| **CT Procedures (Chest, Head, Abdomen, Pelvis, Spine, Extremities)** | 32 | 32 | 0 |
| **MRI Procedures (Brain, Spine, Musculoskeletal, Breast, Abdomen)** | 38 | 37 | 1 (`RULE-ADV-CG2000-003`) |
| **CTA / MRA Vascular Imaging** | 20 | 20 | 0 |
| **PET / PET-CT Oncology & Neurology** | 9 | 9 | 0 |
| **Cross-Cutting Administrative & General Imaging** | 15 | 11 | 4 (`PREAMBLE-001`, `CG2001-001`, `CG2066-001`, `CG2066-002`) |
| **IPM Epidural Steroid Injections (ESI)** | 4 | 4 | 0 |
| **IPM Facet Interventions & Radiofrequency Neurotomy** | 3 | 3 | 0 |
| **IPM Spinal Cord Stimulation (SCS)** | 3 | 3 | 0 |
| **IPM Sacroiliac Joint & Other Interventions** | 4 | 2 | 2 (`PREAMBLEIPM-001`, `CGINFUSIONPUMPS-001`) |
| **Total MedRule Active Rules** | **128** | **121** | **7** |

---

## 4. Dual-Track Separation: Clinical Necessity vs Place of Service

Place of Service rules (EPOS 2067 for Radiology and EPOS 1755 for IPM) govern facility site-of-care reimbursement, not whether the procedure is medically necessary for the patient's condition.

The decision-tree engine enforces strict track separation:

1. **Independent Evaluation:**
   - **Track 1 (`CLINICAL_NECESSITY`):** Evaluates indication, prerequisite, and diagnostic criteria from clinical policies.
   - **Track 2 (`PLACE_OF_SERVICE`):** Evaluates facility setting, freestanding availability (POS 11/24), and medical exception criteria (POS 19/21/22 hospital outpatient).
2. **Deterministic Outcome Combination:**
   - If `CLINICAL_NECESSITY == CRITERIA_MET` and `PLACE_OF_SERVICE == CRITERIA_MET`: Procedure is indicated at the requested facility.
   - If `CLINICAL_NECESSITY == CRITERIA_MET` and `PLACE_OF_SERVICE == CRITERIA_NOT_MET`: Clinical necessity is documented and preserved. Overall outcome flags site-of-care non-compliance and issues a redirection order to an ambulatory/freestanding facility (POS 11/24) without denying medical necessity.
   - If `CLINICAL_NECESSITY == CRITERIA_NOT_MET`: Procedure is not indicated regardless of requested facility.
   - If `CLINICAL_NECESSITY == INSUFFICIENT_INFORMATION`: Evaluated case is pended for required clinical records.

---

## 5. Clinical Coverage Gap & Ambiguity Escalation

In compliance with strict scope controls, the engine does not infer uncodified clinical criteria. When an intake request triggers an uncodified gap identified during the clinical coverage audit, the engine deterministically halts autonomous adjudication and escalates the case to `NEEDS_HUMAN_REVIEW`:

| Coverage Gap Identifier | Procedure Context | Source Policy Gap | Deterministic Engine Action |
| :--- | :--- | :--- | :--- |
| **IPM CG 1750 Gap 1** | Epidural Steroid Injections (`62321`-`62323`) | Spinal stenosis / neurogenic claudication without radiculopathy. Walking distance thresholds and canal diameter criteria uncodified in active rulebook. | Escalates to `NEEDS_HUMAN_REVIEW` with exact gap provenance. |
| **IPM CG 1757 Gap 2** | Neuromodulation / DRG Stimulation (`63650`) | Dorsal Root Ganglion (DRG) stimulation requested for non-lower-extremity CRPS. 2026 governing policy explicitly restricts DRG to lower extremities. | Escalates to `NEEDS_HUMAN_REVIEW` with anatomical mismatch warning. |
| **IPM CG 1750 Gap 3** | Epidural Steroid Injections | Repeat injection requested with interval < 14 calendar days from prior injection. Policy requires minimum 14-day refractory period. | Returns `CRITERIA_NOT_MET` (repeat frequency exclusion). |
| **IPM Frequency Cap** | ESI, Facet, SI Joint Injections | Injection requested where documented prior sessions exceed policy maximum (e.g. > 3 ESI per episode / > 4 per year). | Returns `CRITERIA_NOT_MET` (annual frequency limit). |
| **AI CG 2007 Gap** | CT / MRI Abdomen & Pelvis | Inflammatory Bowel Disease (IBD) surveillance where criteria are advisory rather than mandatory. | Escalates to `NEEDS_HUMAN_REVIEW` for clinical gastroenterology review. |

---

## 6. Comprehensive Test Results

The decision-tree test suite ([`medrule_engine/tests/test_decision_tree.py`](file:///d:/PreAuth/medrule_engine/tests/test_decision_tree.py)) was executed against the active rules and engine.

### Test Execution Log (14 / 14 Passed)

```text
============================= test session starts =============================
platform win32 -- Python 3.11.5, pytest-9.1.1 -- D:\PreAuth\.venv\Scripts\python.exe
rootdir: D:\PreAuth, configfile: pytest.ini

medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_01_all_121_ready_rules_compilation PASSED [  7%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_02_all_7_needs_human_review_rules_strictly_blocked PASSED [ 14%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_03_zero_approved_rules_governance_invariant PASSED [ 21%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_04_dual_track_separation_clinical_necessity_vs_place_of_service PASSED [ 28%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_05_missing_input_fields_never_satisfy_criteria PASSED [ 35%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_06_boolean_all_of_and_any_of_logic_paths PASSED [ 42%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_07_numerical_and_temporal_boundary_values PASSED [ 50%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_08_prior_treatment_prerequisites_and_documented_failure PASSED [ 57%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_09_exclusions_and_negative_decision_effects PASSED [ 64%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_10_repeat_service_interval_and_frequency_limits PASSED [ 71%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_11_uncovered_policy_criteria_gap_escalation PASSED [ 78%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_12_source_provenance_fidelity PASSED [ 85%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_13_domain_isolation_and_historical_policy_rejection PASSED [ 92%]
medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_14_deterministic_repeatability_and_hash_stability PASSED [100%]

============================= 14 passed in 0.66s ==============================
```

### Combined Regression Verification (48 / 48 Passed)

```text
============================= test session starts =============================
medrule_engine/tests/test_decision_tree.py (14 tests) .......... PASSED
medrule_engine/tests/test_deterministic_engine.py (20 tests) ... PASSED
rulebook_collection/tests/test_scope_integrity.py (14 tests) ... PASSED

============================= 48 passed in 1.75s ==============================
```

---

## 7. Verification of Mandatory Scope Deliverables

| Requirement | Audit Status | Evidence / Verification |
| :--- | :---: | :--- |
| **Use only 121 ready rules** | VERIFIED | `test_01` validates successful compilation of all 121 `DRAFT` rules. |
| **Block 7 NEEDS_HUMAN_REVIEW rules** | VERIFIED | `test_02` proves all 7 rules are unconditionally intercepted by the governance gate. |
| **Preserve all 128 active rules** | VERIFIED | `test_12` and `test_scope_integrity.py` verify 128 unique rule IDs and schemas. |
| **No invented or inferred clinical criteria** | VERIFIED | Zero guessing logic implemented; missing fields yield `UNKNOWN` / `INSUFFICIENT_INFORMATION`. |
| **Zero LLM APIs / probabilistic reasoning** | VERIFIED | 100% deterministic Python evaluation in `medrule_engine/decision_tree.py`. |
| **Isolate Advanced Imaging & IPM** | VERIFIED | `test_13` confirms cases from other domains are rejected as `POLICY_NOT_APPLICABLE`. |
| **Separate Place of Service from Clinical Necessity** | VERIFIED | `test_04` demonstrates independent dual tracks (CN vs POS). |
| **Full source-level provenance** | VERIFIED | `test_12` confirms `source_file`, `physical_page`, `source_section`, and `source_quote` in traces. |
| **Deterministic reproducibility hash** | VERIFIED | `test_14` confirms identical inputs produce identical SHA-256 hashes across repeated executions. |

---

## 8. Unresolved Issues & Recommendations for Clinical Leadership

1. **Medical Director Adjudication Required on 7 Blocked Rules:**
   - The 7 blocked rules (`RULE-ADV-PREAMBLE-001`, `RULE-ADV-CG2000-003`, `RULE-ADV-CG2001-001`, `RULE-ADV-CG2066-001`, `RULE-ADV-CG2066-002`, `RULE-IPM-PREAMBLEIPM-001`, `RULE-IPM-CGINFUSIONPUMPS-001`) require clinician sign-off before logic can be codified.
2. **Policy Coverage Gaps:**
   - The 170 Advanced Imaging gap items and 34 IPM gap items cataloged in `advanced_imaging_coverage_gap_report.csv` and `ipm_coverage_gap_report.csv` remain uncodified. Autonomous decision-making must remain strictly prohibited for cases touching these criteria.
3. **Regulatory and Clinical Disclaimer:**
   - This software is a deterministic decision-support prototype and does not provide autonomous clinical authorization. Zero rules are marked `APPROVED`.
