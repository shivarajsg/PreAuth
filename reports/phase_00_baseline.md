# MedRule — Phase 0: Read-Only Baseline Audit

**Audit Date:** 2026-10-21T23:05:00+05:30  
**Repository Path:** `d:\PreAuth`  
**Audit Type:** Read-Only Baseline Inspection (Phase 0 Deliverable)

---

## 1. Git Branch, Commit, and Working Tree Status

* **Current Branch:** `main` (synchronized with `origin/main`).
* **Current HEAD Commit:** `086d286dd02f5f5180b7a844344000ce78904c6c`
  * Commit Subject: `docs(verification): perform manual extraction check 1 on synthetic lumbar MRI note and archive audit scripts`
  * Commit Date: `Wed Oct 21 19:15:35 2026 +0530`
* **Uncommitted Changes:**
  * `modified: medrule_engine/governance/data/governance.db` (transient audit/pilot connector event logs updated during test executions).
  * `modified: medrule_engine/pilot/pilot_run_results.json` (transient pilot runner execution statistics).
  * `untracked: docs/MedRule_Consolidated_Audit_and_Final_Plan.md` (newly placed consolidated audit specification document).
  * *Verification Command:* `git status --porcelain` and `git log -1`.

---

## 2. Python Environment and Version

* **Python Version:** Python `3.11.5`
* **Active Virtual Environment:** `d:\PreAuth\.venv`
* **Executable Path:** `d:\PreAuth\.venv\Scripts\python.exe`
* **Base Interpreter:** `C:\Users\Shrinidhi Bijapur\AppData\Local\Programs\Python\Python311`
* *Verification Command:* `.venv\Scripts\python.exe -c "import sys; print(sys.version, sys.executable, sys.prefix)"`

---

## 3. Dependency Declaration vs. Installed Status

* **Manifest:** [`requirements.txt`](file:///d:/PreAuth/requirements.txt)
* **Declared vs Installed Comparison:**

| Package | Declared Version in `requirements.txt` | Installed Version in `.venv` | Status | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `Flask` | `>=3.0.0` | `3.1.3` | **Installed & Verified** | Core web framework |
| `jsonschema` | `>=4.20.0` | `4.26.0` | **Installed & Verified** | Rule & intake schema validator |
| `PyMuPDF` (`fitz`) | `>=1.23.0` | `1.28.2` | **Installed & Verified** | Clinical PDF document extraction |
| `pytest` | `>=8.0.0` | `9.1.1` | **Installed & Verified** | Automated test runner |
| `gunicorn` | `>=21.2.0` | *None* | **Not Installed (Expected)** | Unix WSGI server declared for Render deployment (`render.yaml`/`Procfile`); not used on Windows local dev. |

> [!NOTE]
> The earlier reported issue regarding `jsonschema` and `pymupdf` missing was due to invoking Python outside the virtual environment. Both packages are installed and functional in `.venv`.

---

## 4. Test Configuration and Execution Results

* **Test Configuration:** [`pytest.ini`](file:///d:/PreAuth/pytest.ini) defines:
  * `pythonpath = .`
  * `testpaths = medrule_engine/tests rulebook_collection/tests`
  * `norecursedirs = archive_candidate scratch .venv .git __pycache__`
* **Collection Result:**
  * Command: `pytest --collect-only`
  * Result: **183 tests collected successfully in 3.01s** (0 collection errors).
* **Execution Results:**
  1. **Core Verification Suite (Decision Tree, Extraction, Schema, Scope Integrity):**
     * Command: `pytest medrule_engine/tests/test_step2_clinical_extraction_and_evaluation.py medrule_engine/tests/test_pdf_extractor.py medrule_engine/tests/test_decision_tree.py rulebook_collection/tests/test_scope_integrity.py`
     * Result: **52 passed in 2.72s (100% pass rate)**.
  2. **Full Repository Suite (`pytest` across all legacy modules):**
     * Result: **180 passed, 3 failed in 34.63s**.
     * The 3 failures are documented legacy expectations:
       - `test_router_rejects_unverified_line_of_business`: router returns `POLICY_NOT_APPLICABLE` for unconfigured sleep health procedure `95810` instead of `MANUAL_REVIEW_REQUIRED`.
       - `test_pilot_runner_execution_and_pass_rate`: asserts 36 legacy pilot cases pass across all 9 domains; in the active 2-domain scope, only 14 match.
       - `test_05_core_safety_invariants`: asserts `review_records` count in DB is 0, but DB contains 1 record from previous review demo.

---

## 5. Active Rule Counts Grouped by Status

Verified directly from active canonical rule files ([`rulebook_collection/domains/advanced_imaging/rules/draft_rules.json`](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json) and [`rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json)) and `RuleRegistry.get_statistics()`:

| Clinical Domain | Total Rules | `DRAFT` | `NEEDS_HUMAN_REVIEW` | `APPROVED` |
| :--- | :--- | :--- | :--- | :--- |
| **Advanced Imaging** | 114 | 109 | 5 | 0 |
| **Interventional Pain Management (IPM)** | 14 | 12 | 2 | 0 |
| **Total Active Rules** | **128** | **121** | **7** | **0** |

* **Zero Approved Invariant:** Strict governance invariant `APPROVED = 0` is actively enforced.
* **Governance Blocked Rules:** The 7 `NEEDS_HUMAN_REVIEW` rules correspond exactly to the 7 hard-blocked safety gates (`RULE-ADV-PREAMBLE-001`, `RULE-ADV-CG2000-003`, `RULE-ADV-CG2001-001`, `RULE-ADV-CG2066-001`, `RULE-ADV-CG2066-002`, `RULE-IPM-PREAMBLEIPM-001`, `RULE-IPM-CGINFUSIONPUMPS-001`).

---

## 6. SQLite Governance Database Rule Counts & Mismatch Analysis

Verified by direct SQL queries on [`medrule_engine/governance/data/governance.db`](file:///d:/PreAuth/medrule_engine/governance/data/governance.db) (`rule_governance_state` table):

* **Database Totals Across All Records:**
  * By `extraction_status`: **322 `DRAFT`**, **50 `NEEDS_HUMAN_REVIEW`**, **0 `APPROVED`** (Total: 372).
  * By `workflow_status`: **371 `DRAFT`**, **1 `IN_REVIEW`**, **0 `APPROVED`** (Total: 372).
* **Database Breakdown by Domain:**

| Domain | Records in DB | Extraction Status in DB | Workflow Status in DB | Active in Filesystem? |
| :--- | :--- | :--- | :--- | :--- |
| `advanced_imaging` | 114 | 109 DRAFT, 5 NEEDS_HUMAN_REVIEW | 113 DRAFT, 1 IN_REVIEW | **Yes (114 rules in files)** |
| `interventional_pain_management` | 14 | 12 DRAFT, 2 NEEDS_HUMAN_REVIEW | 14 DRAFT | **Yes (14 rules in files)** |
| `cardiology` | 61 | 55 DRAFT, 6 NEEDS_HUMAN_REVIEW | 61 DRAFT | No (Archived/Excluded) |
| `centene_dme_orthotics_prosthetics` | 99 | 82 DRAFT, 17 NEEDS_HUMAN_REVIEW | 99 DRAFT | No (Archived/Excluded) |
| `genetic_testing` | 25 | 22 DRAFT, 3 NEEDS_HUMAN_REVIEW | 25 DRAFT | No (Archived/Excluded) |
| `musculoskeletal_surgery` | 19 | 16 DRAFT, 3 NEEDS_HUMAN_REVIEW | 19 DRAFT | No (Archived/Excluded) |
| `physical_medicine` | 17 | 14 DRAFT, 3 NEEDS_HUMAN_REVIEW | 17 DRAFT | No (Archived/Excluded) |
| `radiation_oncology` | 15 | 13 DRAFT, 2 NEEDS_HUMAN_REVIEW | 15 DRAFT | No (Archived/Excluded) |
| `sleep_health` | 8 | 1 DRAFT, 7 NEEDS_HUMAN_REVIEW | 8 DRAFT | No (Archived/Excluded) |
| **Total in Database** | **372** | **322 DRAFT, 50 NEEDS_HUMAN_REVIEW** | **371 DRAFT, 1 IN_REVIEW** | **128 Active / 244 Inactive** |

* **Mismatch Root Cause:**
  * For the two active domains (**Advanced Imaging** and **IPM**), there is a **100% exact match** between rule files (128 rules: 121 DRAFT, 7 NEEDS_HUMAN_REVIEW) and the database records (128 records: 121 DRAFT, 7 NEEDS_HUMAN_REVIEW).
  * The remaining **244 records** in the database belong to the 7 out-of-scope domains archived during scope cleanup.

---

## 7. Governing Policy PDFs and Rule JSON Presence

All four governing policy PDFs and rule JSON files were verified on disk:

1. **Advanced Imaging Clinical Guidelines:**
   * Path: [`rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/policies/current/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf)
   * Size: `13,644,257 bytes` | Status: **Present & Verified**
2. **Advanced Imaging Place of Service:**
   * Path: [`rulebook_collection/domains/advanced_imaging/policies/current/EPOS 2067 for Place of Service - Radiology 2026_final.pdf`](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/policies/current/EPOS%202067%20for%20Place%20of%20Service%20-%20Radiology%202026_final.pdf)
   * Size: `275,858 bytes` | Status: **Present & Verified**
3. **Interventional Pain Management Clinical Guidelines:**
   * Path: [`rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/policies/current/2026%20Evolent%20Interventional%20Pain%20Management%20Guidelines.pdf)
   * Size: `2,423,668 bytes` | Status: **Present & Verified**
4. **Interventional Pain Management Place of Service:**
   * Path: [`rulebook_collection/domains/interventional_pain_management/policies/current/EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/policies/current/EPOS%201755%20for%20Place%20of%20Service%20-%20Interventional%20Pain%20Management%202026_final.pdf)
   * Size: `251,294 bytes` | Status: **Present & Verified**
5. **Rule JSON Files:**
   * [`rulebook_collection/domains/advanced_imaging/rules/draft_rules.json`](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json) (114 rules) | Status: **Present & Verified**
   * [`rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json) (14 rules) | Status: **Present & Verified**
   * Categorical section subfolders (CT, MRI, CTA, MRA, PET/SPECT, Epidural, Facet, Neuromodulation, SI Joint, Sympathetic Blocks) | Status: **Present & Verified**

---

## 8. Immediate Blockers & Discrepancies Summary

1. **No Operational Blockers for Core Engine:**
   * Core decision tree engine, clinical PDF extraction, schema validation, and scope integrity tests pass with 100% success (52/52 passed).
   * All 4 required 2026 governing policy PDFs exist and match rule citations.
2. **Identified Discrepancies:**
   * **Database Scope Lag:** `governance.db` retains 244 legacy rule-state rows for the 7 archived domains. For the 2 active domains, it matches rule files 100%.
   * **Legacy Test Expectations:** 3 legacy integration/pilot tests in `test_phase3b_integration.py`, `test_phase3d_pilot.py`, and `test_phase4a_governance_audit.py` expect 9-domain coverage or an unreviewed DB state.
   * **Deployment Dependency:** `gunicorn` is listed in `requirements.txt` for cloud deployment but is not installed or needed in local Windows development.
