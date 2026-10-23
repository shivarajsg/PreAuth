# MedRule — Phase 2: Full-Suite Test Failure Analysis

**Audit Date:** 2026-10-21T23:15:00+05:30  
**Phase Objective:** Reproduce and classify the three full-suite test failures with root-cause evidence without modifying application code, rules, or databases.  
**Constraint Adherence:** Read-only diagnostic phase. Zero code or test modifications applied. No packages installed or changed. No database resets or migrations executed.

---

## 1. Test Suite Execution & Reproduction Status

* **Test Command:**
  ```powershell
  .venv\Scripts\python.exe -m pytest -v --tb=short
  ```
* **Execution Results:**
  * **Total Tests Collected:** 183
  * **Passed:** 180 (98.36%)
  * **Failed:** 3 (1.64%)
  * **Execution Time:** 38.08 seconds
* **Reproduction Finding:**
  The three failures are **100% reproducible** and exactly match the failures identified in Phase 0.

---

## 2. Detailed Root-Cause Analysis by Test

### Failure 1: `test_router_rejects_unverified_line_of_business`

* **Test Location:** [`medrule_engine/tests/test_phase3b_integration.py:329-344`](file:///d:/PreAuth/medrule_engine/tests/test_phase3b_integration.py#L329-L344)
* **Class:** `TestPhase3BIntegration`
* **Test Method:** `test_router_rejects_unverified_line_of_business`
* **Assertion Failure:**
  ```text
  AssertionError: POLICY_NOT_APPLICABLE != MANUAL_REVIEW_REQUIRED
  ```
* **Exact Traceback:**
  ```python
  medrule_engine\tests\test_phase3b_integration.py:342: in test_router_rejects_unverified_line_of_business
      self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
  E   AssertionError: POLICY_NOT_APPLICABLE != MANUAL_REVIEW_REQUIRED
  ```
* **Investigation & Evidence:**
  1. The test constructs a case payload intended to verify line-of-business (LOB) boundary enforcement:
     ```python
     case_dict = {
         "case_id": "CASE-ROUT-01",
         "clinical_domain": "sleep_health",
         "procedure_code": "95810",
         "line_of_business": "OTHER",
         ...
     }
     ```
  2. In [`medrule_engine/policy_router.py:98-105`](file:///d:/PreAuth/medrule_engine/policy_router.py#L98-L105), the router enforces a strict sequence of validation gates:
     * **Step 3 (Clinical Domain Check):** Verifies that the requested clinical domain has active rules configured in the active registry:
       ```python
       domain_rules = self.registry.get_rules_by_domain(domain)
       if not domain_rules:
           return RoutingResult(status="POLICY_NOT_APPLICABLE", routing_notes=[f"No active rules configured for clinical domain '{domain}'."])
       ```
     * **Step 5 (Line of Business Check):** Verifies that the LOB is recognized (`COMMERCIAL`, `MEDICARE_ADVANTAGE`, `MEDICAID`) and returns `MANUAL_REVIEW_REQUIRED` for `OTHER`:
       ```python
       if not lob or lob == "OTHER" or lob not in valid_lobs:
           return RoutingResult(status="MANUAL_REVIEW_REQUIRED", routing_notes=[f"Unrecognized, empty, or unverified line_of_business '{case.line_of_business}'."])
       ```
  3. When this test was written in Phase 3B, `sleep_health` was an active domain. However, in the scoped MedRule architecture, active domains are strictly restricted to **Advanced Imaging** and **Interventional Pain Management (IPM)**.
  4. Because `sleep_health` is archived, Step 3 triggers first, returning `POLICY_NOT_APPLICABLE` before Step 5 is ever reached.
  5. **Verification of Correct Behavior:** When evaluated with an active domain (`advanced_imaging`, procedure `74177`, `line_of_business: "OTHER"`), the router immediately executes Step 5 as intended, returning `CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED`.
* **Classification:** **Obsolete test expectation due to the deliberate two-domain scope**.
* **Safest Proposed Fix (For Phase 4):**
  Update the fixture in `test_phase3b_integration.py` to use an active domain procedure (e.g., `clinical_domain: "advanced_imaging"`, `procedure_code: "74177"`) so the test exercises the LOB boundary without requiring out-of-scope archived domains.

---

### Failure 2: `test_pilot_runner_execution_and_pass_rate`

* **Test Location:** [`medrule_engine/tests/test_phase3d_pilot.py:148-156`](file:///d:/PreAuth/medrule_engine/tests/test_phase3d_pilot.py#L148-L156)
* **Function:** `test_pilot_runner_execution_and_pass_rate`
* **Assertion Failure:**
  ```text
  assert summary["passed_cases"] == 36
  E   assert 14 == 36
  ```
* **Exact Traceback:**
  ```python
  medrule_engine\tests\test_phase3d_pilot.py:153: in test_pilot_runner_execution_and_pass_rate
      assert summary["passed_cases"] == 36
  E   assert 14 == 36
  ```
* **Investigation & Evidence:**
  1. The test executes `run_pilot()` from [`medrule_engine/pilot/run_pilot.py`](file:///d:/PreAuth/medrule_engine/pilot/run_pilot.py), which iterates over 36 historical synthetic cases in [`synthetic_pilot_cases.json`](file:///d:/PreAuth/medrule_engine/pilot/synthetic_pilot_cases.json).
  2. These 36 cases span all 9 clinical domains (4 cases per domain $\times$ 9 domains).
  3. In `run_pilot.py:76-77`, the evaluation engine is instantiated with default active scope:
     ```python
     registry = RuleRegistry()
     registry.load_all_domains()
     ```
     `RuleRegistry()` defaults to `include_archived=False`. Consequently, only the 128 active rules from **Advanced Imaging** (114) and **IPM** (14) are loaded.
  4. Breakdown of the 36 pilot evaluations:
     * **14 cases passed:** All 8 active cases (`advanced_imaging` and `interventional_pain_management`) plus 6 historical cases where expected fallback status coincided with unconfigured handling.
     * **22 cases failed:** Exactly the 22 cases belonging to the 7 archived domains (`cardiology`: 3, `musculoskeletal_surgery`: 4, `radiation_oncology`: 3, `physical_medicine`: 3, `sleep_health`: 3, `genetic_testing`: 3, `centene_dme_orthotics_prosthetics`: 3).
     * For all 22 cases, the active engine returned `POLICY_NOT_APPLICABLE`, while `pilot_expected_results.json` expected evaluation outcomes from the archived domain rulebooks.
* **Classification:** **Obsolete test expectation due to the deliberate two-domain scope**.
* **Safest Proposed Fix (For Phase 4):**
  In Phase 4, adjust the test either to assert a 100% pass rate across the 8 active-domain cases (`advanced_imaging` and `interventional_pain_management`), or configure `run_pilot()` to pass `RuleRegistry(include_archived=True)` when running legacy multi-domain regression benchmarks.

---

### Failure 3: `TestPhase4AGovernanceAudit.test_05_core_safety_invariants`

* **Test Location:** [`medrule_engine/tests/test_phase4a_governance_audit.py:165-181`](file:///d:/PreAuth/medrule_engine/tests/test_phase4a_governance_audit.py#L165-L181)
* **Class:** `TestPhase4AGovernanceAudit`
* **Test Method:** `test_05_core_safety_invariants`
* **Assertion Failure:**
  ```text
  AssertionError: 1 != 0 : review_records in default database must be 0
  ```
* **Exact Traceback:**
  ```python
  medrule_engine\tests\test_phase4a_governance_audit.py:180: in test_05_core_safety_invariants
      self.assertEqual(c.fetchone()[0], 0, "review_records in default database must be 0")
  E   AssertionError: 1 != 0 : review_records in default database must be 0
  ```
* **Investigation & Evidence:**
  1. The test connects to the project SQLite database [`medrule_engine/governance/data/governance.db`](file:///d:/PreAuth/medrule_engine/governance/data/governance.db) and asserts:
     ```python
     c.execute("SELECT COUNT(*) FROM review_records")
     self.assertEqual(c.fetchone()[0], 0, "review_records in default database must be 0")
     ```
  2. Querying `governance.db` reveals exactly 1 record in `review_records`:
     * `review_id`: `REV-8BA6C791A7F8`
     * `rule_id`: `RULE-ADV-CG2000-001`
     * `reviewer_id`: `USR-SME-01`
     * `reviewer_role`: `CLINICAL_SME_REVIEWER`
     * `action`: `START_REVIEW`
     * `previous_status`: `DRAFT`
     * `resulting_status`: `IN_REVIEW`
     * `timestamp`: `2026-10-19T06:17:22.629945+00:00`
     * `comments`: `"Commencing formal Clinical SME review of rule RULE-ADV-CG2034-001 for Lower Extremity MRA (CPT 73725)..."`
  3. This single audit record was committed as part of a formal governance workflow demonstration on Oct 19. It confirms that the rule was transitioned to `IN_REVIEW` (not `APPROVED`).
  4. The safety invariant under test is that **no rules are approved** (`APPROVED == 0`), which passes (`SELECT COUNT(*) FROM rule_governance_state WHERE workflow_status = 'APPROVED'` is `0`).
  5. The secondary assertion that `review_records == 0` assumed a completely wiped, sterile database, which conflicts with the persisted audit trail in version control.
* **Classification:** **Historical governance database state**.
* **Safest Proposed Fix (For Phase 4):**
  In Phase 4, adjust the test assertion to verify that `review_records` contains only valid non-approval actions (`action != 'APPROVE'`), or assert `COUNT(*) <= 1`, or execute the test against an ephemeral in-memory database fixture (`sqlite3.connect(':memory:')`) rather than the persistent repository database.

---

## 3. Summary of Failure Classifications & Proposed Fixes

| # | Test Name | Root Cause | Evidence-Based Classification | Safest Proposed Fix (For Phase 4) |
|---|---|---|---|---|
| **1** | `test_router_rejects_unverified_line_of_business` | Case uses archived domain `sleep_health` (CPT `95810`), causing router to reject at domain boundary before checking LOB. | **Obsolete test expectation due to deliberate two-domain scope** | Change fixture `clinical_domain` to active `advanced_imaging` (CPT `74177`). |
| **2** | `test_pilot_runner_execution_and_pass_rate` | `run_pilot()` evaluates 36 cases across 9 domains; the 22 cases in the 7 archived domains return `POLICY_NOT_APPLICABLE`. | **Obsolete test expectation due to deliberate two-domain scope** | Filter pilot assertions to the 8 active-domain cases or set `include_archived=True` for multi-domain benchmark. |
| **3** | `test_05_core_safety_invariants` | Test expects 0 review records, but DB contains 1 legitimate historical `START_REVIEW` audit record from Oct 19. | **Historical governance database state** | Update assertion to permit legitimate non-approval audit records or use in-memory DB fixture. |

---

## 4. Preservation of Constraints

* No code, tests, rules, configuration, or database records were modified during this diagnostic investigation.
* Core engine verification suite remains at **100% pass rate** (52/52 passed).
* All findings and proposed fixes are documented and held for review before Phase 3 and Phase 4 execution.
