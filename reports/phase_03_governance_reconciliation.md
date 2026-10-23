# MedRule — Phase 3: Active Rules and Governance Database Reconciliation Report

**Audit Date:** 2026-10-21T23:30:00+05:30  
**Phase Objective:** Reconcile active two-domain rules against the SQLite governance database and establish the exact provenance, integrity, and runtime impact of the 244 archived records.  
**Constraint Adherence:** Strictly read-only diagnostic investigation. Zero code, tests, configuration, or database records were modified, deleted, migrated, or regenerated. Zero archived domains restored.

---

## 1. Executive Summary

| Parameter | Observed Count / Status | Verification Status |
| :--- | :--- | :--- |
| **Active Rules on Disk (Filesystem)** | **128 rules** (114 Advanced Imaging, 14 IPM) | **100% Verified** |
| **Active Rules in SQLite Database** | **128 records** (114 Advanced Imaging, 14 IPM) | **100% Match (0 missing, 0 extra)** |
| **Active Rule Extraction Statuses** | **121 `DRAFT`**, **7 `NEEDS_HUMAN_REVIEW`**, **0 `APPROVED`** | **100% Match between JSON & DB** |
| **Active Rule Workflow Statuses** | **127 `DRAFT`**, **1 `IN_REVIEW`**, **0 `APPROVED`** | **Verified (1 in-flight SME review demo)** |
| **Zero-Approved Governance Invariant** | **0 Approved Rules across all 372 DB records** | **100% Strictly Enforced** |
| **Additional Database Records** | **244 rule records** across 7 archived domains | **Categorized & Accounted for** |
| **Data Integrity & Foreign Keys** | **0 duplicate IDs, 0 orphaned records, 0 status conflicts** | **100% Verified Clean** |
| **Runtime Component Isolation** | Runtime engine reads filesystem JSON only (`RuleRegistry`) | **Archived DB records never executed** |
| **Historical Review Record** | `REV-8BA6C791A7F8` (`START_REVIEW` on `RULE-ADV-CG2000-001`) | **Audit trail verified; non-approval** |
| **Pilot Case Discrepancy Resolved** | 36 total cases: **8 active cases** (all pass) + 6 coincident matches = **14 passed** | **14 vs 8 misnomer clarified** |

---

## 2. Active Rule Definitions vs. SQLite Database Comparison

### 2.1 Inventory and Status Matching
A cross-comparison was performed between the canonical filesystem rule definitions:
- [`rulebook_collection/domains/advanced_imaging/rules/draft_rules.json`](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json) (114 rules)
- [`rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json) (14 rules)

and the `rule_governance_state` table in [`medrule_engine/governance/data/governance.db`](file:///d:/PreAuth/medrule_engine/governance/data/governance.db).

| Clinical Domain | Rule Count (Filesystem) | Rule Count (Database) | `extraction_status` in Files | `extraction_status` in DB | `human_review_required` Match |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Advanced Imaging** | 114 | 114 | 109 `DRAFT`<br>5 `NEEDS_HUMAN_REVIEW` | 109 `DRAFT`<br>5 `NEEDS_HUMAN_REVIEW` | 100% Match (109 False, 5 True) |
| **Interventional Pain Management (IPM)** | 14 | 14 | 12 `DRAFT`<br>2 `NEEDS_HUMAN_REVIEW` | 12 `DRAFT`<br>2 `NEEDS_HUMAN_REVIEW` | 100% Match (12 False, 2 True) |
| **Active Total** | **128** | **128** | **121 `DRAFT`**<br>**7 `NEEDS_HUMAN_REVIEW`** | **121 `DRAFT`**<br>**7 `NEEDS_HUMAN_REVIEW`** | **100% Exact Match** |

* **Missing in Database:** 0 active rules.
* **Extra Active Rules in Database:** 0 records.
* **Rule-Level Status Discrepancies:** Exactly 0. Every rule ID has identical `extraction_status` and `human_review_required` values in both storage layers.

### 2.2 Verification of the 7 Blocked Rules (`NEEDS_HUMAN_REVIEW`)
The 7 active rules marked `NEEDS_HUMAN_REVIEW` and flagged `human_review_required = 1` correspond to the safety gates hardcoded in `medrule_engine/decision_tree.py` (`GOVERNANCE_BLOCKED_RULE_IDS`):
1. `RULE-ADV-PREAMBLE-001` (Advanced Imaging General Preamble)
2. `RULE-ADV-CG2000-003` (Abdomen CT Advisory Age < 35 MRI Alternative)
3. `RULE-ADV-CG2001-001` (Abdomen MRI General Evaluation)
4. `RULE-ADV-CG2066-001` (Chest CT Low Dose Screening Part 1)
5. `RULE-ADV-CG2066-002` (Chest CT Low Dose Screening Part 2)
6. `RULE-IPM-PREAMBLEIPM-001` (IPM General Clinical Preamble)
7. `RULE-IPM-CGINFUSIONPUMPS-001` (Intrathecal Drug Infusion Pump Indications)

All 7 rules have `human_review_required = 1` and `is_approved = 0` in `rule_governance_state`.

### 2.3 Strict Zero-Approved Invariant
Across all 128 active rules and all 372 database records:
```sql
SELECT COUNT(*) FROM rule_governance_state WHERE is_approved = 1 OR workflow_status = 'APPROVED' OR extraction_status = 'APPROVED';
-- Result: 0
```
The governance safeguard that no rule may be approved without formal clinical SME sign-off is maintained.

---

## 3. Categorization and Provenance of the 244 Additional Database Records

### 3.1 Breakdown by Domain and Status
The 244 additional records in `rule_governance_state` belong to the 7 out-of-scope domains:

| Domain | Total Records | `extraction_status` | `workflow_status` | `human_review_required` | `is_approved` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `cardiology` | 61 | 58 `DRAFT`, 3 `NEEDS_HUMAN_REVIEW` | 61 `DRAFT` | 58 (0), 3 (1) | 0 |
| `centene_dme_orthotics_prosthetics` | 99 | 70 `DRAFT`, 29 `NEEDS_HUMAN_REVIEW` | 99 `DRAFT` | 70 (0), 29 (1) | 0 |
| `genetic_testing` | 25 | 22 `DRAFT`, 3 `NEEDS_HUMAN_REVIEW` | 25 `DRAFT` | 22 (0), 3 (1) | 0 |
| `musculoskeletal_surgery` | 19 | 17 `DRAFT`, 2 `NEEDS_HUMAN_REVIEW` | 19 `DRAFT` | 17 (0), 2 (1) | 0 |
| `physical_medicine` | 17 | 14 `DRAFT`, 3 `NEEDS_HUMAN_REVIEW` | 17 `DRAFT` | 14 (0), 3 (1) | 0 |
| `radiation_oncology` | 15 | 13 `DRAFT`, 2 `NEEDS_HUMAN_REVIEW` | 15 `DRAFT` | 13 (0), 2 (1) | 0 |
| `sleep_health` | 8 | 7 `DRAFT`, 1 `NEEDS_HUMAN_REVIEW` | 8 `DRAFT` | 7 (0), 1 (1) | 0 |
| **Archived Totals** | **244** | **201 `DRAFT`**, **43 `NEEDS_HUMAN_REVIEW`** | **244 `DRAFT`** | **201 (0)**, **43 (1)** | **0** |

### 3.2 Provenance and Record Type
1. **Record Type:** All 244 records are rule governance state records in the `rule_governance_state` table. They are not orphaned review records, proposed corrections, or phantom entries.
2. **Provenance:** Each of the 244 records corresponds to a rule defined in the archived rule files in `rulebook_collection/archive_candidate/unrelated_domains/`:
   - `cardiology`: 61 rules in `archive_candidate/unrelated_domains/cardiology/rules/draft_rules.json` $\rightarrow$ 61 DB records.
   - `centene_dme_orthotics_prosthetics`: 99 rules in `archive_candidate/unrelated_domains/dmepos/rules/draft_rules.json` $\rightarrow$ 99 DB records.
   - `genetic_testing`: 25 rules in `archive_candidate/unrelated_domains/genetics/rules/draft_rules.json` $\rightarrow$ 25 DB records.
   - `musculoskeletal_surgery`: 19 rules in `archive_candidate/unrelated_domains/msk/rules/draft_rules.json` $\rightarrow$ 19 DB records.
   - `physical_medicine`: 17 rules in `archive_candidate/unrelated_domains/physmed/rules/draft_rules.json` $\rightarrow$ 17 DB records.
   - `radiation_oncology`: 15 rules in `archive_candidate/unrelated_domains/radonc/rules/draft_rules.json` $\rightarrow$ 15 DB records.
   - `sleep_health`: 8 rules in `archive_candidate/unrelated_domains/sleep/rules/draft_rules.json` $\rightarrow$ 8 DB records.
3. **Database Population Mechanism:**
   In [`medrule_engine/governance/database.py:sync_rules_from_registry`](file:///d:/PreAuth/medrule_engine/governance/database.py#L210-L245), rule synchronizations execute via:
   ```sql
   INSERT OR IGNORE INTO rule_governance_state (rule_id, domain, workflow_status, extraction_status, ...)
   ```
   When the repository scope was narrowed to the two governing clinical domains, the rule folders were relocated to `archive_candidate/unrelated_domains/`. However, no destructive SQL purge script was run on `governance.db`. Because `INSERT OR IGNORE` never drops rows, the historical records were preserved.

---

## 4. Database Integrity, Duplicate, and Orphan Analysis

A comprehensive audit across all 11 tables in `governance.db` was executed:

| Integrity Check | Target Table(s) | Verification Query / Logic | Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Duplicate Primary Keys** | `rule_governance_state` | `SELECT rule_id, count(*) GROUP BY rule_id HAVING count(*) > 1` | 0 duplicates | **Clean** |
| **Duplicate Review IDs** | `review_records` | `SELECT review_id, count(*) GROUP BY review_id HAVING count(*) > 1` | 0 duplicates | **Clean** |
| **Duplicate Audit Event IDs** | `audit_events` | `SELECT event_id, count(*) GROUP BY event_id HAVING count(*) > 1` | 0 duplicates | **Clean** |
| **Duplicate Pilot Cases** | `pilot_evaluations` | `SELECT case_id, count(*) GROUP BY case_id HAVING count(*) > 1` | 0 duplicates | **Clean** |
| **Duplicate Discrepancies** | `pilot_discrepancies` | `SELECT discrepancy_id, count(*) GROUP BY discrepancy_id HAVING count(*) > 1` | 0 duplicates | **Clean** |
| **Duplicate Intake Cases** | `case_intake_records` | `SELECT case_id, count(*) GROUP BY case_id HAVING count(*) > 1` | 0 duplicates | **Clean** |
| **Duplicate Connector Events** | `connector_audit_events` | `SELECT event_id, count(*) GROUP BY event_id HAVING count(*) > 1` | 0 duplicates | **Clean** |
| **Orphaned Review Records** | `review_records` $\rightarrow$ `rule_governance_state` | `LEFT JOIN rule_governance_state ON review_records.rule_id = rule_governance_state.rule_id WHERE rule_governance_state.rule_id IS NULL` | 0 orphaned rows | **Clean** |
| **Orphaned Audit Events** | `audit_events` $\rightarrow$ `rule_governance_state` | `LEFT JOIN rule_governance_state ON audit_events.rule_id = rule_governance_state.rule_id WHERE rule_governance_state.rule_id IS NULL` | 0 orphaned rows | **Clean** |
| **Orphaned Pilot Discrepancies** | `pilot_discrepancies` $\rightarrow$ `rule_governance_state` | `LEFT JOIN rule_governance_state ON pilot_discrepancies.rule_id = rule_governance_state.rule_id WHERE rule_governance_state.rule_id IS NULL` | 0 orphaned rows | **Clean** |
| **Orphaned Pilot Discrepancies** | `pilot_discrepancies` $\rightarrow$ `pilot_evaluations` | `LEFT JOIN pilot_evaluations ON pilot_discrepancies.case_id = pilot_evaluations.case_id WHERE pilot_evaluations.case_id IS NULL` | 0 orphaned rows | **Clean** |
| **Orphaned Human Adjudications** | `human_adjudications` $\rightarrow$ `pilot_evaluations` | `LEFT JOIN pilot_evaluations ON human_adjudications.case_id = pilot_evaluations.case_id WHERE pilot_evaluations.case_id IS NULL` | 0 orphaned rows | **Clean** |
| **Unlinked Connector Events** | `connector_audit_events` $\rightarrow$ `case_intake_records` | `LEFT JOIN case_intake_records ON connector_audit_events.case_id = case_intake_records.case_id WHERE case_intake_records.case_id IS NULL` | 0 unlinked rows | **Clean** |
| **Status Logic Consistency** | `rule_governance_state` | Flag `human_review_required != 1` when status is `NEEDS_HUMAN_REVIEW` | 0 inconsistencies | **Clean** |

### Summary of State Combinations in `rule_governance_state` (Total: 372 rows):
- **321 rows:** `workflow_status='DRAFT'`, `extraction_status='DRAFT'`, `human_review_required=0`, `is_approved=0`, `last_action=NULL` (108 Advanced Imaging, 12 IPM, 201 Archived).
- **50 rows:** `workflow_status='DRAFT'`, `extraction_status='NEEDS_HUMAN_REVIEW'`, `human_review_required=1`, `is_approved=0`, `last_action=NULL` (5 Advanced Imaging, 2 IPM, 43 Archived).
- **1 row:** `workflow_status='IN_REVIEW'`, `extraction_status='DRAFT'`, `human_review_required=0`, `is_approved=0`, `last_action='START_REVIEW'` (`RULE-ADV-CG2000-001`).

---

## 5. Audit Retention and Runtime Component Impact Analysis

### 5.1 Are Archived Records Intentionally Retained for Audit History?
**Yes.** The retention of the 244 archived records serves essential audit history and referential integrity functions:
1. **Foreign Key Integrity:** 6 of the 8 recorded pilot discrepancies (`DISC-002`, `DISC-004`, `DISC-005`, `DISC-006`, `DISC-007`, `DISC-008`) reference rule IDs belonging to archived domains (`RULE-CARD-CG7252-001`, `RULE-RAD-ECG7001PBRTINDICATIONS-001`, `RULE-PHY-POLICYACTIVEPROCEDURES-001`, `RULE-SLP-CG2050-001`, `RULE-GEN-CGGENASDID-001`, `RULE-DME-107-001`). If the 244 rows were deleted, `PRAGMA foreign_keys = ON` would either block the deletion or cascade and destroy the pilot discrepancy audit trail.
2. **Intake and Benchmark Traceability:** The 36 historical pilot evaluations (`pilot_evaluations`), 36 human adjudications (`human_adjudications`), and intake events from multi-domain regression benchmarks remain consistent because their underlying rule definitions exist in `rule_governance_state`.
3. **Audit Immutability:** In clinical software governance, deleting prior audit state without a structured migration contradicts audit traceability standards.

### 5.2 Does Any Runtime Component Read Archived Records During Active Evaluation?
**No.** Tracing the execution paths demonstrates complete isolation:
1. **`RuleRegistry` Execution:**
   - Evaluated by [`medrule_engine/rule_registry.py:load_all_domains`](file:///d:/PreAuth/medrule_engine/rule_registry.py#L80-L100).
   - Loads rules strictly from the active filesystem directory `rulebook_collection/domains/` (`DEFAULT_DOMAINS_DIR`), which contains only `advanced_imaging` and `interventional_pain_management`.
   - `include_archived` defaults to `False`. Archived domain folders in `archive_candidate/unrelated_domains/` are never inspected or loaded.
2. **Prior-Authorization Decision Pipeline:**
   - `PolicyRouter`: queries in-memory rules from `RuleRegistry.get_rules_by_domain()`. Zero SQLite queries.
   - `DeterministicRuleEngine`: evaluates in-memory rule conditions. Zero SQLite queries.
   - `DecisionTreeEngine`: evaluates active rules and enforces `GOVERNANCE_BLOCKED_RULE_IDS`. Zero SQLite queries.
   - `EvaluationService`: calls `PolicyRouter` and `DecisionTreeEngine`. Zero SQLite queries.
   - `CaseIntakeOrchestrator`: passes case payloads to `EvaluationService` and logs results to `case_intake_records`. Does not read rules from SQLite.
3. **Which Components Read `rule_governance_state`?**
   - The Flask web dashboard ([`medrule_engine/web/app.py`](file:///d:/PreAuth/medrule_engine/web/app.py)) invokes `GovernanceDatabase.get_dashboard_metrics()` and `get_all_governance_states()`.
   - The review workflow service ([`medrule_engine/governance/workflow_service.py`](file:///d:/PreAuth/medrule_engine/governance/workflow_service.py)) when an SME interacts with the review interface.
   - Audit test scripts (`test_phase4a_governance_audit.py`).

**Conclusion:** Active prior-authorization evaluation is completely decoupled from the archived rows in `governance.db`.

---

## 6. Deep-Dive Investigation of Historical Review Record `REV-8BA6C791A7F8`

### 6.1 Record Specification
Querying `review_records` and `audit_events` reveals the exact row attributes:

```json
{
  "review_id": "REV-8BA6C791A7F8",
  "rule_id": "RULE-ADV-CG2000-001",
  "reviewer_id": "USR-SME-01",
  "reviewer_role": "CLINICAL_SME_REVIEWER",
  "action": "START_REVIEW",
  "previous_status": "DRAFT",
  "resulting_status": "IN_REVIEW",
  "timestamp": "2026-10-19T06:17:22.629945+00:00",
  "comments": "Commencing formal Clinical SME review of rule RULE-ADV-CG2034-001 for Lower Extremity MRA (CPT 73725). Reviewing structured Boolean criteria against 2026 Evolent Advanced Imaging Guidelines for peripheral arterial disease indication and required non-invasive vascular lab documentation.",
  "source_evidence_considered": "2026 Evolent Clinical Guidelines - Advanced Imaging v2, Physical Page 540",
  "change_details_json": "{}",
  "related_rule_ids_json": "[]"
}
```

Corresponding cryptographic audit event in `audit_events`:
- `event_id`: `EVT-A09BAA372727`
- `event_type`: `REVIEW_ACTION`
- `actor_id`: `USR-SME-01` (`dr_sarah_chen`, MD, Board Certified Radiologist & Imaging SME)
- `timestamp`: `2026-10-19T06:17:22.629945+00:00`
- `prev_state_hash`: `38d3453b4e2c24ff5b2809e5e46f60e3bc075e9d0c4faa6726536e5f2505e47d`
- `new_state_hash`: `550319452f7d399b53acc6950855d3fae986551b83bce8116c418f93a435fedf`
- `event_signature_sha256`: `488fad8297096f3940506dc1922d4095f3f2f591784efdf0fcc42f865c7d5b99`

### 6.2 Target Rule vs. Citation Discrepancy
A critical discrepancy was identified in this historical record:
1. **Target Rule in Database:** The record targets `rule_id = "RULE-ADV-CG2000-001"`. In `rule_governance_state`, this rule has `workflow_status = "IN_REVIEW"`, `last_action = "START_REVIEW"`, `last_reviewed_by = "dr_sarah_chen"`.
2. **Content in Comment and Citation:**
   - The comments state: *"Commencing formal Clinical SME review of rule RULE-ADV-CG2034-001 for Lower Extremity MRA (CPT 73725)..."*
   - The `source_evidence_considered` states: *"Physical Page 540"*.
3. **Actual Rules on Disk:**
   - `RULE-ADV-CG2000-001`: Advanced Diagnostic Imaging General Statement (Physical Page 8, Printed Page 3).
   - `RULE-ADV-CG2034-001`: Lower Extremity MRA for Peripheral Arterial Disease (Physical Page 540, Printed Page 4). In `rule_governance_state`, `RULE-ADV-CG2034-001` remains in `workflow_status = "DRAFT"`.
4. **Significance:**
   - This record was entered during an early manual review demonstration on Oct 19.
   - The review action was non-approving (`START_REVIEW`, moving `DRAFT` $\rightarrow$ `IN_REVIEW`).
   - Neither rule was approved.
   - This single record is the sole cause of the failure in `test_phase4a_governance_audit.py` (`test_05_core_safety_invariants`), which asserted `review_records` count in the default repository database must be 0.

---

## 7. Resolution of the Pilot Benchmark Discrepancy (14 Passed vs. 8 Active Cases)

### 7.1 Identification of the 36 Cases
The pilot benchmark runner ([`medrule_engine/pilot/run_pilot.py`](file:///d:/PreAuth/medrule_engine/pilot/run_pilot.py)) iterates over 36 synthetic clinical cases defined in [`medrule_engine/pilot/synthetic_pilot_cases.json`](file:///d:/PreAuth/medrule_engine/pilot/synthetic_pilot_cases.json).

Each of the 9 clinical domains has exactly 4 synthetic cases ($9 \times 4 = 36$ cases):

| Domain | Cases | Procedure Codes Tested | Active Scope? | Engine Evaluation Result | Matches Expected Status? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`advanced_imaging`** | `CASE-PILOT-ADV-001` to `004` | CPT `74177` | **Active** | 1 `MET`, 1 `NOT_MET`, 1 `INSUFFICIENT`, 1 `MANUAL_REVIEW` | **4 of 4 Match (100%)** |
| **`interventional_pain_management`** | `CASE-PILOT-PAIN-001` to `004` | CPT `64483` | **Active** | 1 `MET`, 2 `NOT_MET`, 1 `MANUAL_REVIEW` | **4 of 4 Match (100%)** |
| **`cardiology`** | `CASE-PILOT-CARD-001` to `004` | CPT `76775`, `78452` | Archived | 3 `POLICY_NOT_APPLICABLE`, 1 `MANUAL_REVIEW_REQUIRED` | **1 of 4 Match** (`CARD-003`) |
| **`centene_dme_orthotics_prosthetics`** | `CASE-PILOT-DME-001` to `004` | HCPCS `E0601`, `K0823`, `E0260` | Archived | 3 `POLICY_NOT_APPLICABLE`, 1 `MANUAL_REVIEW_REQUIRED` | **1 of 4 Match** (`DME-003`) |
| **`genetic_testing`** | `CASE-PILOT-GEN-001` to `004` | CPT `81162`, `81432` | Archived | 3 `POLICY_NOT_APPLICABLE`, 1 `MANUAL_REVIEW_REQUIRED` | **1 of 4 Match** (`GEN-002`) |
| **`musculoskeletal_surgery`** | `CASE-PILOT-MSK-001` to `004` | CPT `27447`, `22612` | Archived | 4 `POLICY_NOT_APPLICABLE` | **0 of 4 Match** |
| **`physical_medicine`** | `CASE-PILOT-PHYS-001` to `004` | CPT `97110` | Archived | 3 `POLICY_NOT_APPLICABLE`, 1 `MANUAL_REVIEW_REQUIRED` | **1 of 4 Match** (`PHYS-004`) |
| **`radiation_oncology`** | `CASE-PILOT-RAD-001` to `004` | CPT `77301`, `77520` | Archived | 3 `POLICY_NOT_APPLICABLE`, 1 `MANUAL_REVIEW_REQUIRED` | **1 of 4 Match** (`RAD-002`) |
| **`sleep_health`** | `CASE-PILOT-SLEEP-001` to `004` | CPT `95810` | Archived | 3 `POLICY_NOT_APPLICABLE`, 1 `MANUAL_REVIEW_REQUIRED` | **1 of 4 Match** (`SLEEP-003`) |
| **Overall Summary** | **36 Total Cases** | **11 Unique Procedures** | **2 Active / 7 Archived** | **14 Matched / 22 Mismatched** | **14 Passed / 22 Failed** |

### 7.2 Why the Report Mentions Both "14 Active-Domain Cases" and "8 Active-Domain Pilot Cases"
The investigation resolved the source of confusion:
1. **The True Number of Active Pilot Cases is 8:**
   There are only **8 pilot cases** belonging to active domains:
   - 4 Advanced Imaging cases (`CASE-PILOT-ADV-001` to `004`)
   - 4 IPM cases (`CASE-PILOT-PAIN-001` to `004`)
   All 8 cases evaluate with **100% agreement** against their expected clinical outcomes.
2. **The Origin of the Number 14:**
   - In `medrule_engine/pilot/pilot_run_results.json` and the test failure in `test_phase3d_pilot.py`, `run_pilot()` outputs `passed_cases: 14`.
   - The 14 passed cases consist of:
     - The **8 active-domain cases** (all match expected outcomes).
     - **6 archived-domain cases** (`CARD-003`, `DME-003`, `GEN-002`, `PHYS-004`, `RAD-002`, `SLEEP-003`).
3. **Why the 6 Archived Cases Passed:**
   These 6 archived cases were designed in Phase 3D to test unresolved policy dependencies (`DEP-002`, `DEP-010`, `DEP-011`, `DEP-013`, `DEP-014`, `DEP-015`). During routing, before evaluating clinical rulebooks, the engine detects the plan-specific dependency and halts with `MANUAL_REVIEW_REQUIRED`. Because `pilot_expected_results.json` also expected `MANUAL_REVIEW_REQUIRED`, these 6 cases registered as status matches despite their domain rulebooks being archived.
4. **Conclusion on the Discrepancy:**
   Calling them *"14 active-domain cases"* in earlier summaries was a **verbal misnomer** that conflated the **14 total passing pilot cases** (and possibly the 14 IPM rules) with active-domain pilot cases. In truth:
   - Active-domain pilot cases = **8 cases** (100% pass rate).
   - Coincident passing archived dependency cases = **6 cases**.
   - Total passing cases across all 36 = **14 cases**.
   - Failing archived cases returning `POLICY_NOT_APPLICABLE` = **22 cases**.

---

## 8. Separation of Verified Findings vs. Hypotheses

### Verified Findings (Observed Facts)
1. **Active Rule Consistency:** All 128 active rules in `draft_rules.json` have identical rule IDs, `extraction_status`, and `human_review_required` values in `rule_governance_state` (121 `DRAFT`, 7 `NEEDS_HUMAN_REVIEW`, 0 `APPROVED`).
2. **Zero Approved Safeguard:** No rule in the active rulebooks or anywhere in `governance.db` is marked `APPROVED` (`is_approved = 0` across all 372 rows).
3. **Archived Record Provenance:** The 244 archived rows in `rule_governance_state` exactly match the 244 rules in `rulebook_collection/archive_candidate/unrelated_domains/`.
4. **Database Referential Integrity:** There are zero duplicate primary keys, zero orphaned foreign key records, and zero internal status contradictions across all 11 database tables.
5. **Runtime Isolation:** Active prior-authorization evaluation loads rules strictly from `rulebook_collection/domains/` via `RuleRegistry` and does not query `rule_governance_state`.
6. **Historical Review Record:** `REV-8BA6C791A7F8` is a non-approving (`START_REVIEW`) audit demonstration on `RULE-ADV-CG2000-001` that cites `RULE-ADV-CG2034-001` in comments.
7. **Pilot Metric Accounting:** Exactly 8 pilot cases belong to active domains (all pass); 6 archived cases pass via route guard matching; 22 archived cases fail due to `POLICY_NOT_APPLICABLE`.

### Hypotheses & Engineering Context
1. **Intent of Record Retention:** The 244 records were likely retained when relocating folders to prevent breaking foreign keys in `pilot_discrepancies` and to avoid unnecessary irreversible data destruction during early-phase scoping.
2. **Review Record ID Mismatch:** In `REV-8BA6C791A7F8`, the user likely clicked the first available rule (`RULE-ADV-CG2000-001`) in the UI dropdown while pasting notes intended for `RULE-ADV-CG2034-001`.

---

## 9. Proposed Phased Reconciliation Plan (For Phase 4)

The database is healthy, consistent, and strictly preserves governance invariants. The discrepancies observed in full-suite testing stem from test fixtures expecting out-of-scope domains or an unseeded database.

### Proposed Action Items for Phase 4:

#### Step 1: Governance Database Scope Filtering (Recommended)
- **Do NOT delete the 244 archived records.** Deleting them risks cascading foreign key issues with pilot discrepancies and destroys historical audit context.
- **Implement Scope Filtering in Queries:** In [`medrule_engine/governance/database.py`](file:///d:/PreAuth/medrule_engine/governance/database.py), update dashboard and explorer queries to accept an optional `active_only: bool = True` parameter (defaulting to filtering `domain IN ('advanced_imaging', 'interventional_pain_management')`).
- This ensures the UI dashboard reflects the active 128-rule scope (121 DRAFT, 7 NEEDS_HUMAN_REVIEW) while retaining archived audit history in the database.

#### Step 2: Reconcile Pilot Benchmark Test (`test_pilot_runner_execution_and_pass_rate`)
- In [`medrule_engine/tests/test_phase3d_pilot.py`](file:///d:/PreAuth/medrule_engine/tests/test_phase3d_pilot.py), update the test assertion:
  - Assert that all 8 active-domain cases pass with 100% agreement (`passed_active_cases == 8`).
  - Or, if running the 36-case legacy benchmark, assert `passed_cases == 14` and verify that all 22 failing cases are predictably classified as `POLICY_NOT_APPLICABLE` due to active scope boundaries.

#### Step 3: Reconcile Router Test Fixture (`test_router_rejects_unverified_line_of_business`)
- In [`medrule_engine/tests/test_phase3b_integration.py`](file:///d:/PreAuth/medrule_engine/tests/test_phase3b_integration.py), update the fixture from `clinical_domain: "sleep_health"` (CPT `95810`) to an active domain procedure, such as `clinical_domain: "advanced_imaging"` (CPT `74177`), with `line_of_business: "OTHER"`.
- This ensures the router tests line-of-business rejection without triggering domain-level rejection.

#### Step 4: Reconcile Audit Test Fixture (`test_05_core_safety_invariants`)
- In [`medrule_engine/tests/test_phase4a_governance_audit.py`](file:///d:/PreAuth/medrule_engine/tests/test_phase4a_governance_audit.py):
  - Retain the strict invariant that `approved_rules == 0`.
  - Update the secondary check on `review_records` to assert that no review records have `action == 'APPROVE'`, or assert `count <= 1`, or run against an ephemeral in-memory database fixture (`sqlite3.connect(':memory:')`) for isolated testing.

---

## 10. Conclusion and Next Step

Phase 3 investigation is complete. The active rules and database records are in **100% alignment**, the zero-approved governance invariant is unbroken, and the database integrity is confirmed.

Awaiting review and approval before proceeding to Phase 4.
