+# MedRule — Authoritative Policy Selection, Source Fidelity & Runtime Usage Audit Report

**Document ID:** MEDRULE-REP-POLICY-AUDIT-001  
**Audit Date:** 2026-10-21  
**Auditor:** Automated Clinical Governance & Engine Verification Agent  
**Active Scope:** Advanced Imaging & Interventional Pain Management (IPM)  
**Approved Rules:** 0 (Zero-Approval Invariant Enforced)  
**System Status:** Non-binding clinical decision-support software prototype  

---

## 1. Executive Summary

This independent audit evaluated how the MedRule Prior Authorization Engine discovers, inventories, selects, routes, and applies clinical and place-of-service policies. The audit inspected actual Python source code, JSON Schema specifications, active rule databases, and the physical PDF policies on disk.

### Key Audit Findings
1. **Authoritative Sources Inventoried (101 Physical PDFs):**
   - 2 Current governing clinical policies (1,041-page Advanced Imaging v2; 102-page IPM Guidelines).
   - 2 Current place-of-service policies (EPOS 2067 Radiology; EPOS 1755 IPM).
   - 2 Historical superseded clinical policies (2025 Advanced Imaging; 2025 IPM).
   - 12 Supporting clinical forms, checklists, and tip sheets.
   - 4 Shared CMS statutory reference manuals.
   - 1 Original seed link manifest (`PreauthorizationMRI.pdf`).
   - 78 Quarantined or archived PDFs (14 redundant duplicate copies; 64 unrelated clinical domain policies).
2. **Policy Selection & Execution Architecture:**
   - Case intake validates against strict JSON Schema ([`case_schema.json`](file:///d:/PreAuth/medrule_engine/case_schema.json)).
   - Domain gate isolates execution strictly to `advanced_imaging` and `interventional_pain_management`.
   - [`PolicyRouter`](file:///d:/PreAuth/medrule_engine/policy_router.py) evaluates Line of Business, Date of Service boundaries, modality, and version status.
   - Dual-track architecture evaluates Clinical Necessity independently from Place of Service.
   - Zero silent fallbacks: Historical policies and out-of-scope domains cannot silently enter active routing.
3. **Rule-to-Policy Fidelity Audit (128 Active Rules):**
   - **78 Rules VERIFIED:** Criteria, operators, numerical thresholds, prerequisites, and source quotes fully match the cited governing policy text and surrounding section without uncodified exceptions.
   - **43 Rules PARTIALLY_VERIFIED:** Source quote, physical page, and atomic criteria are verified, but surrounding policy sections contain broader clinical context, multi-week conservative therapy modalities, or uncodified footnote exceptions.
   - **7 Rules HUMAN_REVIEW_REQUIRED:** Blocked at the engine gate (`GOVERNANCE_BLOCKED_RULE_IDS`) due to advisory wording or clinical judgment override frameworks.
   - **0 Rules CONFLICT:** No contradictions between active rules and cited source text.
   - **0 Rules NOT_VERIFIED:** Every active rule references an existing physical PDF page with exact verbatim text confirmed.
4. **Deterministic Policy Routing Test Matrix (12 / 12 Scenarios Passing):**
   - Verified expected policy selection across Advanced Imaging, IPM, Place of Service, boundary dates, out-of-scope domains, blocked rules, and coverage gaps.

---

## 2. Policy Source Inventory & Classification

All 101 physical PDFs across designated directories were cataloged in [`policy_source_registry.csv`](file:///d:/PreAuth/rulebook_collection/manifests/policy_source_registry.csv).

| Classification Category | PDF Count | Key Documents | Active Engine Status |
| :--- | :---: | :--- | :---: |
| **Current governing clinical policy** | 2 | `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (1,041 pp.)<br>`2026 Evolent Interventional Pain Management Guidelines.pdf` (102 pp.) | `ACTIVE_GOVERNING` |
| **Current place-of-service policy** | 2 | `EPOS 2067 for Place of Service - Radiology 2026_final.pdf` (11 pp.)<br>`EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` (8 pp.) | `ACTIVE_GOVERNING` |
| **Historical policy** | 2 | `2025 Evolent Advanced Imaging Guidelines_0.pdf` (1,074 pp.)<br>`2025 Evolent Interventional Pain Management Guidelines.pdf` (75 pp.) | `HISTORICAL_SUPERSEDED` (Quarantined) |
| **Supporting form or checklist** | 7 | Generic PA Checklist, LDCT History Form, Conservative Treatment Forms (AI & IPM 2024/2025 revisions) | `ACTIVE_SUPPORTING` |
| **Supporting tip sheet** | 5 | Brain MRI vs CT Tip Sheet, Spine Imaging Tip Sheet, Pediatric Tip Sheet, IPM Tip Sheet | `ACTIVE_SUPPORTING` |
| **Shared reference** | 4 | CMS Claims Processing Manual Ch. 20, DMEPOS Quality Standards, RESNA Wheelchair Standard, CMS SOM Hospital Survey Protocol | `ACTIVE_REFERENCE` |
| **Unrelated or archived policy** | 78 | 14 Quarantined duplicate copies<br>64 Unrelated domain policies (Cardiology, MSK, Physical Med, RadOnc, Sleep, DMEPOS) | `ARCHIVED_UNRELATED` / `QUARANTINED` |
| **Unresolved source** | 1 | `PreauthorizationMRI.pdf` (Seed document containing original GA state URLs) | `UNRESOLVED` |
| **Total Physical PDFs** | **101** | | |

---

## 3. Policy Selection & Execution Flow Audit

The execution path was traced from case intake to audit output. Detailed flowcharts and code references are documented in [`policy_selection_flow.md`](file:///d:/PreAuth/rulebook_collection/manifests/policy_selection_flow.md).

### 3.1 Key Runtime Behaviors Verified in Code
1. **Domain Detection:** Determined strictly by `case_dict["clinical_domain"]`. Enforced by `decision_tree.py:186-204`. If domain is not `advanced_imaging` or `interventional_pain_management`, engine returns `POLICY_NOT_APPLICABLE`.
2. **Procedure Matching:** `PolicyRouter.route_case()` matches `case.modality` and `case.procedure_code` against rule service descriptions. Incompatible radiology codes in IPM are rejected.
3. **Date of Service Boundary:** Dates prior to `2026-01-01` return `POLICY_VERSION_UNRESOLVED`. Historical policies are never silently selected.
4. **Line of Business Guard:** Cases with `line_of_business == "OTHER"` or missing LOB return `MANUAL_REVIEW_REQUIRED`. The system does not assume commercial applicability.
5. **Dual-Track Separation:** Rules with `rule_type == "place_of_service"` or `EPOS` in their metadata route to `DecisionTrack.PLACE_OF_SERVICE`. Clinical indication rules route to `DecisionTrack.CLINICAL_NECESSITY`. When Clinical Necessity is MET but Place of Service fails, the engine returns `CRITERIA_NOT_MET` with a redirection notice to freestanding facilities (POS 11/24) while preserving Clinical Necessity as MET.
6. **Zero Hardcoded Criteria in Python:** All clinical thresholds, comparators, and Boolean logic are loaded from JSON rule files. Python code only provides the deterministic execution engine and coverage gap escalation guard.

---

## 4. Rule-to-Policy Fidelity Audit Results

All 128 active rules were audited against physical PDF pages in [`rule_policy_fidelity_audit.csv`](file:///d:/PreAuth/rulebook_collection/manifests/rule_policy_fidelity_audit.csv).

```
Total Active Rules Audited: 128
├── Advanced Imaging: 114
└── Interventional Pain Management: 14

Audit Status Breakdown:
├── VERIFIED:                  78 rules (60.9%)
├── PARTIALLY_VERIFIED:        43 rules (33.6%)
├── HUMAN_REVIEW_REQUIRED:      7 rules ( 5.5%)
├── CONFLICT:                   0 rules ( 0.0%)
└── NOT_VERIFIED:               0 rules ( 0.0%)
```

### 4.1 Detailed Status Justification
- **VERIFIED (78 Rules):**
  - Physical PDF page confirmed.
  - Verbatim source quote confirmed on page.
  - AND/OR operators, parameters, and comparators match policy specifications.
  - Specific numerical thresholds (e.g. LDCT pack-years >= 20, Facet block relief >= 50%, SCS trial relief >= 50%) match policy numbers exactly.
  - Surrounding policy section contains no uncodified clinical carve-outs or exceptions for that specific indication.
- **PARTIALLY_VERIFIED (43 Rules):**
  - Physical page and quote are verified.
  - However, the surrounding section contains detailed clinical footnotes, broad multi-week conservative therapy protocols (e.g. physical therapy modalities, anti-inflammatory medications), or red-flag bypass exceptions that are only partially codified in the atomic rule schema.
  - These rules are safe for deterministic compilation of their specific criteria, but operators must recognize that they represent atomic clinical criteria rather than holistic guidelines.
- **HUMAN_REVIEW_REQUIRED (7 Rules):**
  - Strictly blocked at the engine gate (`GOVERNANCE_BLOCKED_RULE_IDS`).
  - Includes clinical preambles (`RULE-ADV-PREAMBLE-001`, `RULE-IPM-PREAMBLEIPM-001`), advisory language (`RULE-ADV-CG2000-003` "MRI should be considered"), billing anti-unbundling mandates (`RULE-ADV-CG2001-001`), retrospective reviews (`RULE-ADV-CG2066-001`, `RULE-ADV-CG2066-002`), and high-acuity pump trials (`RULE-IPM-CGINFUSIONPUMPS-001`).

---

## 5. Policy Routing Test Matrix Results

The 12 deterministic test scenarios were executed against the runtime engine. Results are recorded in [`policy_routing_test_matrix.csv`](file:///d:/PreAuth/rulebook_collection/manifests/policy_routing_test_matrix.csv).

| Scenario ID | Test Scope / Condition | Expected Result | Actual Result | Status |
| :--- | :--- | :---: | :---: | :---: |
| `SCEN-01-AI-CLINICAL` | Brain MRI MS Indication (POL-ADV-2026-V2) | `CRITERIA_MET` | `CRITERIA_MET` | **PASS** |
| `SCEN-02-AI-POS` | Spine MRI Ambulatory Site of Care (POL-ADV-EPOS2067-2026) | `CRITERIA_MET` | `CRITERIA_MET` | **PASS** |
| `SCEN-03-IPM-CLINICAL` | Facet Denervation 60% Relief (POL-IPM-2026) | `CRITERIA_MET` | `CRITERIA_MET` | **PASS** |
| `SCEN-04-IPM-POS` | Epidural Injection Freestanding Site (POL-IPM-EPOS1755-2026) | `CRITERIA_MET` | `CRITERIA_MET` | **PASS** |
| `SCEN-05-OUT-OF-SCOPE-DOMAIN` | Cardiology Request (Cardiology Domain Rejection) | `POLICY_NOT_APPLICABLE` | `POLICY_NOT_APPLICABLE` | **PASS** |
| `SCEN-06-UNSUPPORTED-PROC-CODE` | Malformed Procedure Code (`INVALID_CODE_999`) | `POLICY_NOT_APPLICABLE` | `POLICY_NOT_APPLICABLE` | **PASS** |
| `SCEN-07-MISSING-APPLICABILITY-LOB`| Line of Business `OTHER` (Unverified Commercial Benefit) | `NEEDS_HUMAN_REVIEW` | `NEEDS_HUMAN_REVIEW` | **PASS** |
| `SCEN-08-DATE-PRE-2026-BOUNDARY`| Date of Service in 2025 (Pre-2026 Boundary Rejection) | `POLICY_VERSION_UNRESOLVED` | `POLICY_VERSION_UNRESOLVED` | **PASS** |
| `SCEN-09-HISTORICAL-REJECTION` | Date of Service in 2025 (Historical Fallback Prevented) | `POLICY_VERSION_UNRESOLVED` | `POLICY_VERSION_UNRESOLVED` | **PASS** |
| `SCEN-10-GOVERNANCE-BLOCKED-RULE`| Governance-Blocked Rule (`RULE-ADV-PREAMBLE-001`) | `NEEDS_HUMAN_REVIEW` | `NEEDS_HUMAN_REVIEW` | **PASS** |
| `SCEN-11-UNCODIFIED-COVERAGE-GAP`| Spinal Stenosis without Radiculopathy (IPM CG 1750 Gap) | `NEEDS_HUMAN_REVIEW` | `NEEDS_HUMAN_REVIEW` | **PASS** |
| `SCEN-12-CN-MET-POS-NOT-MET` | CN Met, POS Hospital Outpatient Not Met (Site Redirection)| `CRITERIA_NOT_MET` | `CRITERIA_NOT_MET` | **PASS** |

---

## 6. Reality Check: Verified Facts vs Claims vs Limitations

| Topic / Feature | Real Implementation Status | Reality Check / Audit Finding |
| :--- | :---: | :--- |
| **Authoritative Policies** | **VERIFIED** | 101 PDFs physically present, hashed, and classified. 2026 Evolent Guidelines are the sole governing clinical standard. |
| **Zero Approved Rules Invariant** | **VERIFIED** | 0 rules are approved (`is_approved == False` everywhere). System is strictly a non-binding decision-support prototype. |
| **Domain Isolation** | **VERIFIED** | Advanced Imaging and IPM are strictly isolated. All other 7 domains are archived and blocked from runtime execution. |
| **Dual-Track Evaluation** | **VERIFIED** | Clinical necessity and Place of Service are evaluated on separate tracks without cross-contamination. |
| **Silent Historical Fallback** | **VERIFIED (PREVENTED)**| Engine strictly blocks historical policies from active evaluation. Dates < 2026-01-01 yield `POLICY_VERSION_UNRESOLVED`. |
| **Multi-Payer Customization** | **PARTIAL / NOT CODIFIED** | Case schema supports `payer_id`, but rules codify national Evolent baseline only. Custom plan-specific exclusions are uncodified. |
| **State Jurisdictional Deviations**| **NOT CODIFIED** | State-specific prompt-pay mandates or administrative variations are not codified in rule logic. |
| **Complete Clinical Coverage** | **PARTIALLY VERIFIED** | 78 rules fully verified; 43 rules cover atomic criteria but omit broad clinical footnotes; 204 coverage gap items remain uncodified. |

---

## 7. Final Assessment by Category

### `POLICY SOURCES IDENTIFIED` — **VERIFIED**
All 101 physical PDFs on disk across active, supporting, shared, and archived directories have been cataloged, cryptographically hashed with SHA-256, and mapped to authoritative classifications in [`policy_source_registry.csv`](file:///d:/PreAuth/rulebook_collection/manifests/policy_source_registry.csv).

### `POLICY ROUTING VERIFIED` — **VERIFIED**
The runtime routing pipeline in [`policy_router.py`](file:///d:/PreAuth/medrule_engine/policy_router.py) and [`decision_tree.py`](file:///d:/PreAuth/medrule_engine/decision_tree.py) deterministically maps case intake payloads to governing policies based on domain, modality, LOB, and DOS. All 12 test scenarios in [`policy_routing_test_matrix.csv`](file:///d:/PreAuth/rulebook_collection/manifests/policy_routing_test_matrix.csv) passed with 100% fidelity.

### `RULE-TO-POLICY FIDELITY VERIFIED` — **VERIFIED / PARTIALLY VERIFIED**
100% of the 128 active rules reference valid physical PDF pages with exact verbatim quotes confirmed. 78 rules are fully verified. 43 rules are partially verified due to uncodified surrounding footnotes and broader clinical context. 7 rules are flagged `HUMAN_REVIEW_REQUIRED` and strictly blocked at the gate. Zero conflicts or unverified citations exist.

### `POLICY APPLICABILITY CONTROLS VERIFIED` — **VERIFIED WITH DOCUMENTED LIMITATIONS**
Line of business safeguards (`COMMERCIAL`, `MEDICARE_ADVANTAGE`, `MEDICAID`) and Date of Service boundaries (`2026-01-01`) are enforced. The system assumes the single national Evolent policy set; multi-payer and state-specific variations are not codified and must be reviewed manually if applicable.

### `READY FOR CONTROLLED TESTING` — **READY FOR SYNTHETIC TESTING ONLY**
The deterministic decision-tree engine is ready for synthetic test cases and regression benchmarking in Advanced Imaging and IPM. It is **NOT** ready for real clinical authorization, clinical claims adjudication, or live medical deployment.

### `BLOCKERS`
1. **Zero Approved Rules Invariant:** All 128 active rules remain `DRAFT` or `NEEDS_HUMAN_REVIEW`. No rule may be marked `APPROVED` without formal clinical leadership review.
2. **7 Governance-Blocked Rules:** Autonomous evaluation remains permanently blocked until clinician sign-off is completed.
3. **204 Uncodified Coverage Gaps:** Gaps in Advanced Imaging (170 items) and IPM (34 items) cannot be evaluated autonomously and must continue to escalate to medical director review.
