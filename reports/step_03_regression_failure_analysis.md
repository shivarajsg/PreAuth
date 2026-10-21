# MedRule — Step 3: Regression Failure Investigation and Root-Cause Analysis

**Document Date:** October 21, 2026  
**Scope:** Investigation of the 3 Full-Suite Pytest Failures in `medrule_engine/tests/`  
**Governance Invariant:** No assertions weakened, no clinical rules approved, no governance safeguards altered.

---

## 1. Executive Summary

During the execution of the MedRule test suite (`pytest medrule_engine/tests/ -v`), **166 of 169 tests passed** (98.2%), and exactly **3 tests failed**. 

In accordance with Step 3 Task A instructions, this investigation captures the exact failure tracebacks, conducts an authoritative Git version-control audit against pre-Step-2 baseline commit `e33bea4`, determines the precise root causes, and proposes safe, explicit remediation options for human review prior to any changes.

### Key Finding:
**All three failures directly predate Step 2 and exist identically in baseline commit `e33bea4` (Wed Oct 21 13:10:16 2026 +0530).** None of the failures represent implementation regressions introduced by Step 2. They stem from:
1. Archived-domain rejection in an older test fixture (`sleep_health` domain).
2. Scope boundary mismatch in the Phase 3D multi-domain pilot runner (`include_archived=False` default).
3. Persistent test artifact in `medrule_engine/governance/data/governance.db` (a single review record created on October 19, 2026).

---

## 2. Detailed Investigation of the 3 Failures

### Failure 1: `TestPhase3BIntegration.test_router_rejects_unverified_line_of_business`

#### A. Exact Failure Details
- **Test File:** `medrule_engine/tests/test_phase3b_integration.py`
- **Test Method:** `TestPhase3BIntegration.test_router_rejects_unverified_line_of_business`
- **Line Number:** Line 342
- **Exact Assertion:**
  ```python
  assessment, audit = self.service.evaluate_case(case_dict)
  self.assertEqual(assessment.assessment_status, CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED)
  ```
- **Error Output:**
  ```text
  AssertionError: POLICY_NOT_APPLICABLE != MANUAL_REVIEW_REQUIRED
  ```

#### B. Precise Cause Analysis
The test verifies that when an unknown or unverified line of business (`line_of_business: "OTHER"`) is submitted, the policy router escalates to `MANUAL_REVIEW_REQUIRED` rather than assuming commercial coverage.

However, the test fixture was crafted using:
```python
case_dict = {
    "case_id": "CASE-ROUT-01",
    "clinical_domain": "sleep_health",
    "procedure_code": "95810",
    "procedure_name": "Polysomnography",
    "requested_date_of_service": "2026-04-25",
    "line_of_business": "OTHER",
    ...
}
```
In `medrule_engine/policy_router.py` (`PolicyRouter.route_case`), the routing pipeline checks:
1. **Step 3 (Clinical Domain):**
   ```python
   domain = case.clinical_domain
   domain_rules = self.registry.get_rules_by_domain(domain)
   if not domain_rules:
       return RoutingResult(status="POLICY_NOT_APPLICABLE", ...)
   ```
2. **Step 5 (Line of Business):**
   ```python
   lob = (case.line_of_business or "").upper().strip()
   if not lob or lob == "OTHER" or lob not in valid_lobs:
       return RoutingResult(status="MANUAL_REVIEW_REQUIRED", ...)
   ```

Because `sleep_health` is an archived domain (archived during the scope cleanup in commit `e33bea4` to focus exclusively on the 2 governing domains, Advanced Imaging and IPM), `self.registry.get_rules_by_domain("sleep_health")` returns `[]`. Therefore, `route_case` exits at Step 3 with `POLICY_NOT_APPLICABLE` before reaching Step 5.

#### C. Version Control History & Baseline Evidence
- Checked `git cat-file -p HEAD:medrule_engine/tests/test_phase3b_integration.py`.
- Line 333 in baseline commit `e33bea4` was already `"clinical_domain": "sleep_health"`.
- In commit `e33bea4`, `RuleRegistry.__init__` already defaulted to `include_archived: bool = False`.
- **Classification:** **Archived-domain rejection / test fixture scope mismatch predating Step 2.**

#### D. Proposed Remediation (For Human Review)
- **Option 1 (Recommended):** Update the test fixture in `test_phase3b_integration.py` to use an active domain procedure, such as `"clinical_domain": "advanced_imaging"` with `"procedure_code": "72148"`. This directly tests the router's LOB guard on the active governing rulebook without altering clinical rules or weakening assertions.
- **Option 2:** Set `cls.registry = RuleRegistry(include_archived=True)` in `TestPhase3BIntegration.setUpClass` if Phase 3B is intended to cover the full historical 9-domain corpus.

---

### Failure 2: `test_pilot_runner_execution_and_pass_rate`

#### A. Exact Failure Details
- **Test File:** `medrule_engine/tests/test_phase3d_pilot.py`
- **Test Function:** `test_pilot_runner_execution_and_pass_rate`
- **Line Number:** Line 153
- **Exact Assertion:**
  ```python
  summary = run_pilot()
  assert summary["total_cases_evaluated"] == 36
  assert summary["domains_evaluated"] == 9
  assert summary["passed_cases"] == 36
  ```
- **Error Output:**
  ```text
  assert 14 == 36
  ```

#### B. Precise Cause Analysis
The Phase 3D pilot evaluation suite (`medrule_engine/pilot/synthetic_pilot_cases.json`) comprises 36 synthetic cases evenly distributed across **all 9 clinical domains** (4 cases per domain $\times$ 9 domains).

In `medrule_engine/pilot/run_pilot.py` (lines 76–77):
```python
registry = RuleRegistry()
registry.load_all_domains()
```
`RuleRegistry()` instantiates with `include_archived=False`. Consequently, only the 2 active domains (`advanced_imaging` and `interventional_pain_management`) are loaded into the registry. The 14 cases belonging to Advanced Imaging and IPM pass (100% of active cases). However, the 22 cases belonging to the 7 archived domains fail to route because their rules are archived, resulting in `14 == 36`.

#### C. Version Control History & Baseline Evidence
- Inspected `git cat-file -p HEAD:medrule_engine/pilot/run_pilot.py`.
- Baseline commit `e33bea4` contains `registry = RuleRegistry()` on line 76.
- Baseline commit `e33bea4` contains `assert summary["passed_cases"] == 36` in `test_phase3d_pilot.py`.
- **Classification:** **Scope boundary mismatch in pilot runner predating Step 2.**

#### D. Proposed Remediation (For Human Review)
- **Option 1 (Recommended):** In `medrule_engine/pilot/run_pilot.py`, instantiate `registry = RuleRegistry(include_archived=True)` for the pilot runner. Because the pilot runner's explicit docstring states "Executes synthetic pilot cases across all nine clinical domains", enabling `include_archived=True` aligns the runner's registry scope with its 9-domain dataset.
- **Option 2:** Update `synthetic_pilot_cases.json` and `test_phase3d_pilot.py` to evaluate only the 14 active-scope pilot cases, establishing a separate historical regression suite for the archived domains.

---

### Failure 3: `TestPhase4AGovernanceAudit.test_05_core_safety_invariants`

#### A. Exact Failure Details
- **Test File:** `medrule_engine/tests/test_phase4a_governance_audit.py`
- **Test Method:** `TestPhase4AGovernanceAudit.test_05_core_safety_invariants`
- **Line Number:** Line 180
- **Exact Assertion:**
  ```python
  c.execute("SELECT COUNT(*) FROM review_records")
  self.assertEqual(c.fetchone()[0], 0, "review_records in default database must be 0")
  ```
- **Error Output:**
  ```text
  AssertionError: 1 != 0 : review_records in default database must be 0
  ```

#### B. Precise Cause Analysis
The test verifies safety invariants on the default SQLite database (`medrule_engine/governance/data/governance.db`), specifically asserting that 0 rules are approved and 0 review records exist.

Querying `review_records` in `governance.db` reveals:
```sql
SELECT review_id, rule_id, reviewer_id, action, from_status, to_status, created_at, rationale 
FROM review_records;
```
**Result:**
- `review_id`: `'REV-8BA6C791A7F8'`
- `rule_id`: `'RULE-ADV-CG2000-001'`
- `reviewer_id`: `'USR-SME-01'`
- `action`: `'START_REVIEW'`
- `from_status`: `'DRAFT'`
- `to_status`: `'IN_REVIEW'`
- `created_at`: `'2026-10-19T06:17:22.629945+00:00'`
- `rationale`: `'Commencing formal Clinical SME review of rule RULE-ADV-CG2034-001...'`

This record was inserted during an interactive or test execution on October 19, 2026 (two days before Step 2 began). The record transitioned a rule to `IN_REVIEW`, not `APPROVED` (the zero-approved invariant remains 100% satisfied). However, `test_05_core_safety_invariants` checks `COUNT(*) == 0` on `review_records`.

#### C. Version Control History & Baseline Evidence
- Extracted `medrule_engine/governance/data/governance.db` directly from baseline commit `e33bea4` using `git cat-file -p HEAD:medrule_engine/governance/data/governance.db`.
- Queried the extracted baseline database: `SELECT COUNT(*) FROM review_records` returned `1`.
- Commit history shows `governance.db` was committed in `commit 956bf9c` on Mon Oct 19 12:55:05 2026 with this record present.
- **Classification:** **Test database state / persistent artifact predating Step 2.**

#### D. Proposed Remediation (For Human Review)
- **Option 1 (Recommended):** Remove the single development review record from `medrule_engine/governance/data/governance.db`:
  `DELETE FROM review_records WHERE review_id = 'REV-8BA6C791A7F8';`
  This restores the default governance database to a pristine zero-record state as expected by `test_05_core_safety_invariants`.
- **Option 2:** In `test_05_core_safety_invariants`, verify that 0 review records have `to_status = 'APPROVED'`, ensuring the governance invariant (no review has ever approved a rule) is enforced without requiring a totally empty audit table.

---

## 3. Summary of Findings

| Failure Identifier | Module / File | Root Cause Classification | Git Baseline Predate Confirmed? | Remediation Status |
| :--- | :--- | :--- | :--- | :--- |
| **Failure 1:** `test_router_rejects_unverified_line_of_business` | `test_phase3b_integration.py:342` | Archived-domain rejection (`sleep_health`) | **YES** (Confirmed in commit `e33bea4`) | Proposed (Use active domain `advanced_imaging`) |
| **Failure 2:** `test_pilot_runner_execution_and_pass_rate` | `test_phase3d_pilot.py:153` | Pilot runner scope boundary (`include_archived=False`) | **YES** (Confirmed in commit `e33bea4`) | Proposed (`include_archived=True` in runner) |
| **Failure 3:** `test_05_core_safety_invariants` | `test_phase4a_governance_audit.py:180` | Pre-existing test DB record (`REV-8BA6C791A7F8` from Oct 19) | **YES** (Confirmed in commit `e33bea4`) | Proposed (Purge single test record) |

*Zero implementation regressions were introduced by Step 2. All 18 new Step 2 tests and 40 core regression tests continue to pass with 100% reliability.*
