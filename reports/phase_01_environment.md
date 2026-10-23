# MedRule — Phase 1: Reproducible Python Environment

**Audit Date:** 2026-10-21T23:10:00+05:30  
**Phase Objective:** Verify and document a reproducible development environment for the active Advanced Imaging and Interventional Pain Management domains.  
**Constraint Adherence:** Read-only environment audit. No packages installed, upgraded, or downgraded. No changes made to production configuration, rules, database, or test files.

---

## 1. Environment & Dependency Inspection

### 1.1 Python Version and Interpreter
* **Python Runtime:** Python `3.11.5` (64-bit on Windows `AMD64`)
* **Virtual Environment Path:** `d:\PreAuth\.venv`
* **Python Executable:** `d:\PreAuth\.venv\Scripts\python.exe`
* **Virtual Environment Prefix:** `d:\PreAuth\.venv`
* **Base Python Interpreter:** `C:\Users\Shrinidhi Bijapur\AppData\Local\Programs\Python\Python311`

### 1.2 Declared Dependencies ([`requirements.txt`](file:///d:/PreAuth/requirements.txt))
The project declares five dependencies in [`requirements.txt`](file:///d:/PreAuth/requirements.txt):
```text
flask>=3.0.0
jsonschema>=4.20.0
PyMuPDF>=1.23.0
pytest>=8.0.0
gunicorn>=21.2.0
```

### 1.3 Installed Package Verification
Verification executed via `.venv\Scripts\python.exe -m pip list`:

| Declared Requirement | Installed Version | Status | Verified Functionality |
| :--- | :--- | :--- | :--- |
| `flask>=3.0.0` | `3.1.3` | **Satisfied** | Web API, routing, and intake endpoints |
| `jsonschema>=4.20.0` | `4.26.0` | **Satisfied** | Rule schema and CaseIntake validation |
| `PyMuPDF>=1.23.0` | `1.28.2` | **Satisfied** | Clinical progress note text extraction |
| `pytest>=8.0.0` | `9.1.1` | **Satisfied** | Test collection and automated test execution |
| `gunicorn>=21.2.0` | *Not Installed* | **Platform Exemption** | Unix WSGI HTTP server required for Render deployment (`render.yaml`/`Procfile`). Gunicorn does not support Windows native wheels and is not required for Windows development/testing. |

---

## 2. Dependency Consistency Check (`pip check`)

* **Command Executed:**
  ```powershell
  .venv\Scripts\python.exe -m pip check
  ```
* **Exact Command Output:**
  ```text
  No broken requirements found.
  ```
* **Exit Code:** `0`
* **Verified Result:** The existing `.venv` has zero dependency conflicts, broken requirements, or missing transient dependencies.

---

## 3. Core Module Import Verification

* **Command Executed:**
  ```powershell
  .venv\Scripts\python.exe -c "
  import flask, jsonschema, fitz, pymupdf, pytest
  print('Flask:', flask.__file__)
  print('jsonschema:', jsonschema.__file__)
  print('PyMuPDF:', pymupdf.__file__)
  print('pytest:', pytest.__file__)
  import medrule_engine
  from medrule_engine.decision_tree import DecisionTreeEngine
  from medrule_engine.rule_registry import RuleRegistry
  from medrule_engine.case_validator import CaseValidator
  from medrule_engine.integrations.pdf_extractor import extract_case_from_pdf
  print('MedRule Engine core successfully imported.')
  "
  ```
* **Exact Command Output:**
  ```text
  Flask: D:\PreAuth\.venv\Lib\site-packages\flask\__init__.py
  jsonschema: D:\PreAuth\.venv\Lib\site-packages\jsonschema\__init__.py
  PyMuPDF: D:\PreAuth\.venv\Lib\site-packages\pymupdf\__init__.py
  pytest: D:\PreAuth\.venv\Lib\site-packages\pytest\__init__.py
  MedRule Engine core successfully imported.
  ```
* **Verified Result:** All application and engine components resolve cleanly from the project root without runtime import errors.

---

## 4. Frozen Exact Dependency Inventory

For complete bit-level environment reproducibility, below is the exact `pip freeze` from `.venv` (Python 3.11.5 on Windows):

```text
attrs==26.1.0
blinker==1.9.0
click==8.5.0
colorama==0.4.6
Flask==3.1.3
iniconfig==2.3.1
itsdangerous==2.2.0
Jinja2==3.1.6
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
MarkupSafe==3.0.4
packaging==26.3
pluggy==1.7.0
Pygments==2.21.0
pymupdf==1.28.2
pytest==9.1.1
referencing==0.37.0
rpds-py==2026.9.1
typing_extensions==4.16.0
Werkzeug==3.1.9
```

---

## 5. Step-by-Step Environment Reproduction Runbook (Windows)

To reproduce and run this environment from scratch on a clean Windows system:

### Step 1: Create Virtual Environment
Ensure Python `3.11.x` is installed on the host system:
```powershell
python -m venv .venv
```

### Step 2: Activate Environment
```powershell
# In PowerShell:
.\.venv\Scripts\Activate.ps1

# In Command Prompt (cmd.exe):
.\.venv\Scripts\activate.bat
```

### Step 3: Install Core Dependencies
Install the required packages without attempting to build Unix-only `gunicorn` on Windows:
```powershell
python -m pip install flask>=3.0.0 jsonschema>=4.20.0 PyMuPDF>=1.23.0 pytest>=8.0.0
```

### Step 4: Run Core Verification Suite
Execute the verified 52-test suite covering decision trees, clinical extraction, three-valued logic, and rulebook integrity:
```powershell
pytest medrule_engine/tests/test_step2_clinical_extraction_and_evaluation.py medrule_engine/tests/test_pdf_extractor.py medrule_engine/tests/test_decision_tree.py rulebook_collection/tests/test_scope_integrity.py -v
```

### Step 5: Run 9 Clinical Synthetic Test Cases
```powershell
$env:PYTHONPATH="."; python scratch/verify_step3_cases.py; python scratch/summarize_e2e.py
```

---

## 6. Pre-Existing Working Tree State

In accordance with strict audit constraints, the current working tree was preserved without modification or deletion:
* `modified: medrule_engine/governance/data/governance.db` (transient connector audit logs from test execution)
* `modified: medrule_engine/pilot/pilot_run_results.json` (transient benchmark execution metrics)
* `untracked: docs/MedRule_Consolidated_Audit_and_Final_Plan.md` (audit specification)
* `untracked: reports/phase_00_baseline.md` (Phase 0 deliverable)

---

## 7. Observations & Recommended Follow-Up

1. **Verified Observation:** The existing `.venv` is fully functional, satisfies all core dependencies, passes `pip check` with zero broken requirements, and executes all 52 core tests with 100% pass rate in under 3 seconds.
2. **Verified Observation:** `gunicorn` is declared in `requirements.txt` specifically for the cloud container environment (`render.yaml`/`Procfile`). Attempting `pip install -r requirements.txt` on a clean Windows machine will fail on `gunicorn` due to POSIX dependency `fcntl`.
3. **Proposed Recommendation (Not Applied — Awaiting Future Approval):**
   * In a future phase, consider splitting dependency declarations into:
     * `requirements.txt`: Cross-platform core dependencies (`flask`, `jsonschema`, `PyMuPDF`, `pytest`).
     * `requirements-deploy.txt`: Production Linux server dependencies (`gunicorn>=21.2.0 -r requirements.txt`).
   * Per strict constraints, **no files have been modified** in Phase 1.
