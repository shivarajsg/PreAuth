# MedRule Prior-Authorization Decision Support System

MedRule is a deterministic, policy-based clinical decision support (CDS) system designed to evaluate healthcare prior-authorization requests against machine-readable clinical guideline criteria across nine medical specialties.

The engine executes 100% deterministic, three-valued logic (`TRUE`, `FALSE`, `UNKNOWN`) without large language models (LLMs), generative AI, probabilistic inference, or neural weights.

---

## What's New in this Release

1. **Automated Clinical PDF Intake & Evidence Extraction**:
   - Integrates local, high-performance PDF text parsing powered by PyMuPDF.
   - Extracts structured intake attributes directly from uploaded EHR chart notes, physician orders, and clinical consult reports.
   - Auto-populates Patient ID, CPT/HCPCS procedure codes, ICD-10 diagnostic codes, ordering physician notes, dates of service, and domain-specific clinical criteria.

2. **Included Sample Test PDFs**:
   - Two pre-formatted clinical test PDFs are included in the repository root for immediate hands-on verification:
     - `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`: Evaluates an active policy match (CPT 72148) with extracted conservative therapy evidence.
     - `Test_Case_Policy_Unresolved_Experimental_Spine.pdf`: Evaluates an unmapped/experimental procedure (CPT 99999) triggering the `POLICY_CONTEXT_UNRESOLVED` workflow.

3. **Streamlined Web Navigation & UI Layout**:
   - Compact single-line navigation header with left-aligned links, vertical brand title, and right-aligned persona switcher.
   - Collapsible list controls ("Show More / Show Less") across the 372-rule catalog, evaluated condition breakdown cards, and missing evidence summaries.
   - Live PDF source documentation cards displaying verbatim narrative excerpts and extracted findings on evaluation reports.

4. **Multi-Payer Guideline Compatibility**:
   - Pre-configured policy schedules for **Evolent Health** and **Centene Corporation** (CP.MP.107).
   - Mock verification connectors for active eligibility, plan coverage schedules, and local review locking.

---

## Safety Invariants and Operating Principles

The system strictly enforces four hard architectural invariants across all execution paths:

- **Zero Generative AI**: All policy rules are evaluated through explicit boolean and threshold conditions. No generative models or probabilistic neural engines are utilized.
- **Strictly Non-Binding**: Every evaluation output unconditionally asserts `is_binding: false`. This prototype provides decision-support information only and does not render binding legal or payer determinations.
- **Zero Approved Rules**: Exactly 0 of the 372 extracted policy rules are marked `APPROVED`. Rules are partitioned into `DRAFT` (322 rules) and `NEEDS_HUMAN_REVIEW` (50 rules), enforcing mandatory human-in-the-loop oversight.
- **Outbound Transmission Disabled**: Payer connectors operate in simulated (`MOCK`) mode for eligibility, benefits, and authorization requirements. Outbound submission adapters are permanently locked (`DISABLED`).

---

## Medical Domains Covered

The rulebook collection indexes 372 clinical policy rules across nine clinical specialties:

| Specialty Domain | Rule Count | Key Procedures & Guidelines Covered |
| :--- | :--- | :--- |
| **Advanced Imaging** | 114 rules | CT, MRI, PET, place-of-service radiology guidelines |
| **Cardiology** | 37 rules | Cardiac catheterization, stress echocardiography, SPECT imaging |
| **Centene DME, Orthotics & Prosthetics** | 99 rules | CP.MP.107 wheelchairs, mobility devices, prosthetics |
| **Genetic Testing** | 25 rules | Oncology molecular panels, hereditary cancer, pharmacogenomics |
| **Interventional Pain Management** | 14 rules | Epidural steroid injections, facet interventions, neurostimulators |
| **Musculoskeletal Surgery** | 34 rules | Spine surgery, knee/hip arthroplasty, total joint replacements |
| **Physical Medicine** | 17 rules | Physical therapy, occupational therapy, chiropractic caps |
| **Radiation Oncology** | 24 rules | IMRT, stereotactic body radiation therapy (SBRT), brachytherapy |
| **Sleep Health** | 8 rules | Polysomnography, home sleep apnea tests, CPAP titration |

---

## Included Sample Test PDFs

To enable immediate testing of the intake and evaluation pipelines, two synthetic clinical chart notes are provided in the repository root:

### 1. `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`
- **File Location**: `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`
- **Clinical Scenario**: Patient presenting with severe lower back pain and lumbar radiculopathy following 6 weeks of conservative therapy (physical therapy and oral NSAIDs), with clinical red flags evaluated.
- **Target Procedure**: CPT `72148` (MRI Lumbar Spine without contrast)
- **Clinical Domain**: `advanced_imaging`
- **Diagnosis**: ICD-10 `M62.838` (Muscle spasm / Lumbar radicular syndrome)
- **Payer**: `CENTENE` (Commercial Choice Plus)
- **Expected Outcome**:
  - The PDF extractor automatically extracts patient demographics, procedure code, diagnosis code, and 8 structured clinical evidence parameters.
  - The policy router identifies the governing clinical coverage policy (`POLICY RESOLVED`).
  - The deterministic engine evaluates all relevant rules, providing criterion-level three-valued logic outcomes.

### 2. `Test_Case_Policy_Unresolved_Experimental_Spine.pdf`
- **File Location**: `Test_Case_Policy_Unresolved_Experimental_Spine.pdf`
- **Clinical Scenario**: Request for an unlisted/experimental lumbar intervertebral disc procedure where no active clinical coverage policy exists in the 2026 Evolent or Centene catalog.
- **Target Procedure**: CPT `99999` (Unlisted / Experimental Spine Intervention)
- **Clinical Domain**: `musculoskeletal_surgery`
- **Diagnosis**: ICD-10 `M54.89` (Other dorsalgia / Spinal degeneration)
- **Payer**: `EVOLENT` (Commercial Choice Plus)
- **Expected Outcome**:
  - The case enters the `POLICY_CONTEXT_UNRESOLVED` lifecycle state.
  - An amber warning banner alerts the reviewer that the procedure does not match any active guideline catalog.
  - Outbound automation is withheld, routing the case for manual Medical Director contract review.

---

## Prerequisites

- **Python**: Version 3.10, 3.11, or 3.12 (Python 3.11 recommended)
- **Git**: For version control
- **Web Browser**: Chrome, Edge, Firefox, or Safari

---

## Environment Setup and Installation

### 1. Clone or Open the Repository
Ensure your terminal working directory is the repository root:
```bash
cd PreAuth
```

### 2. Create a Virtual Environment
Create an isolated virtual environment (`.venv`):

On Windows (PowerShell):
```powershell
python -m venv .venv
```

On Linux or macOS:
```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

On Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

On Windows (Command Prompt):
```cmd
.\.venv\Scripts\activate.bat
```

On Linux or macOS:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Core dependencies installed:
- `flask` (v3.0+): Local web review workbench, intake portal, and dashboard
- `jsonschema` (v4.20+): Draft-07 case schema validation
- `PyMuPDF` (v1.23+): High-fidelity PDF rendering and text extraction
- `pytest` (v8.0+): Automated testing framework

---

## Step-by-Step Learning Guide: How to Use the Repository

### Step 1: Launch the Local Web Portal
Start the Flask web server:
```bash
python -m medrule_engine.cli serve --host 127.0.0.1 --port 5000
```
Open your browser to `http://127.0.0.1:5000`.

---

### Step 2: Testing with Sample PDF Uploads (Tutorial)

#### Tutorial A: Testing a Policy-Resolved Prior-Authorization Case
1. In the top navigation bar, click **Case Intake** (`/intake`).
2. Locate the top card: **Upload Physician Chart Notes / Prior-Auth Request PDF**.
3. Click **Choose File** and select `Test_Case_Policy_Resolved_Lumbar_MRI.pdf` from the repository root.
4. Click **Upload & Analyze Clinical Document**.
5. Observe the automated extraction results:
   - Patient ID is populated (e.g., `MEM-88219`).
   - Clinical Domain is set to `Advanced Imaging`.
   - Procedure Code is set to `72148` (MRI Lumbar Spine).
   - ICD-10 Diagnosis is set to `M62.838`.
   - The structured clinical evidence JSON block is populated with extracted findings (conservative therapy duration, radiculopathy indicators).
6. Click **Submit Prior-Authorization Case**.
7. You are redirected to the **Case Evaluation Report** (`/cases/<case_id>`):
   - Notice the **Clinical Documentation & PDF Source Evidence** card showing the verbatim chart excerpt, ordering provider, and key findings.
   - Inspect the **Primary Clinical Determination** banner (`INDICATION MET` or `REVIEW REQUIRED`).
   - Review the **Evaluated Clinical Rules & Condition Breakdown** section.
   - Click **Show More Rules** or **Show More Items** to expand rule trees and evidence items.

#### Tutorial B: Testing an Unresolved Policy Case
1. Navigate back to **Case Intake** (`/intake`).
2. In the PDF upload box, select `Test_Case_Policy_Unresolved_Experimental_Spine.pdf`.
3. Click **Upload & Analyze Clinical Document**.
4. Notice that CPT `99999` and Musculoskeletal Surgery are detected.
5. Click **Submit Prior-Authorization Case**.
6. On the Case Detail page, observe:
   - Lifecycle state badge: `POLICY_CONTEXT_UNRESOLVED`.
   - Governing Clinical Guideline card displays `POLICY UNRESOLVED`.
   - Amber alert banner explains that no automated coverage rule applies and routes the case for Medical Director manual review.

---

### Step 3: Manual Case Submission via Presets
If you do not have a PDF document to upload, you can submit cases manually using built-in clinical presets:
1. Navigate to **Case Intake** (`/intake`).
2. Scroll to the **Quick Clinical Presets** section.
3. Click any of the preset buttons:
   - **Preset 1: Lumbar Spine MRI (Radiculopathy)**: Pre-loads CPT 72148 with conservative therapy findings.
   - **Preset 2: Cardiac Catheterization**: Pre-loads CPT 93458 with ischemic symptoms.
   - **Preset 3: Knee Arthroplasty**: Pre-loads CPT 27447 with Grade IV osteoarthritis findings.
   - **Preset 4: Wheelchair (Centene DME CP.MP.107)**: Pre-loads HCPCS K0823 with mobility criteria.
4. Click **Submit Prior-Authorization Case** to evaluate the case against the rulebook.

---

### Step 4: Exploring the Rule Catalog & SME Review Workbench
1. Click **Rule Catalog** (`/rules`) in the navigation bar.
2. Filter rules by domain using the dropdown or search by keyword (e.g., `MRI`, `Spine`, `Biopsy`).
3. Click any Rule ID (e.g., `EVOLENT-ADV-001` or `CENTENE-DME-001`) to open the **SME Review Workbench**:
   - Left side: Deterministic condition tree with logical operators (`AND`, `OR`, `NOT`) and threshold comparisons.
   - Right side: Split-pane PDF viewer showing the exact governing guideline document with the relevant physical page and section citation.

---

### Step 5: Triage and Role-Based Governance Simulation
The navigation bar includes a development persona switcher:
- **Viewer**: Read-only access to audit logs and rule catalogs.
- **Clinical SME Reviewer (Dr. Sarah Chen / Dr. James Wilson)**:
  - Access the **Review Queue** (`/queue`).
  - Propose rule adjustments or request additional documentation.
- **Medical Director (Dr. Eleanor Vance)**:
  - Review proposed corrections on the **Corrections** page (`/corrections`).
  - Perform authorized sign-offs satisfying governance safety prerequisites.
- **Administrator**:
  - Monitor invariant audits and system telemetry.

---

## Running via Command-Line Interface (CLI)

The `medrule` CLI provides direct access to evaluation, intake orchestration, pilot benchmarking, and safety audits.

### 1. System Health and Safety Invariant Audit
Verify database connectivity, rulebook integrity, and zero-approved invariant enforcement:
```bash
python -m medrule_engine.cli health
```

### 2. Prior-Authorization Case Intake
Execute a case through the 10-stage production intake pipeline (schema validation, payer plan matching, mock connectors, deterministic rule routing, and SQLite event logging):
```bash
python -m medrule_engine.cli intake --case medrule_engine/examples/sample_intake_case.json
```

Optional flags:
- `--output <path>`: Write the resulting intake record JSON to disk.
- `--pretty`: Format console JSON output with indentation.

### 3. Direct Deterministic Policy Evaluation
Evaluate a structured clinical case directly against the policy engine:
```bash
python -m medrule_engine.cli evaluate --case medrule_engine/examples/case_01_adv_ct_pancreatitis_met.json --pretty
```

Optional flags:
- `--output <path>`: Export evaluation audit record to JSON.
- `--target-rules RULE_ID_1 RULE_ID_2`: Limit evaluation to specific rule IDs.
- `--quiet`: Suppress verbose console output.

### 4. Pilot Benchmark Adjudication
Execute the 36-case clinical benchmark suite comparing engine findings against expert SME ground truth:
```bash
python -m medrule_engine.cli pilot
```

Optional flags:
- `--output <path>`: Export pilot adjudication results to JSON.

---

## Running Automated Test Suites

The test suite validates schema compliance, rule logic integrity, citation accuracy, intake orchestration, and security sandboxing.

### Run All Tests
```bash
pytest
```
*(Executes 252 tests across both the engine and rulebook collections).*

### Run Engine-Specific Tests
```bash
pytest medrule_engine/tests/ -v
```

Focused test suites:
- **PDF Extraction Module**: `pytest medrule_engine/tests/test_pdf_extractor.py -v`
- **End-to-End Integration**: `pytest medrule_engine/tests/test_phase3f_end_to_end.py -v`
- **Intake Pipeline & Connectors**: `pytest medrule_engine/tests/test_phase3e_intake_connectors.py -v`
- **Pilot Adjudication Runner**: `pytest medrule_engine/tests/test_phase3d_pilot.py -v`
- **SME Review Workflow**: `pytest medrule_engine/tests/test_phase3c_review_workflow.py -v`
- **Deterministic Core Engine**: `pytest medrule_engine/tests/test_deterministic_engine.py -v`

### Run Domain Rule Integrity Tests
```bash
pytest rulebook_collection/ -v
```
Validates JSON schema adherence, verbatim quote alignment against source PDFs, and unique rule identifier invariants across all nine domains.

---

## Repository Structure

```text
PreAuth/
├── Test_Case_Policy_Resolved_Lumbar_MRI.pdf             # Sample clinical test PDF (Policy Resolved)
├── Test_Case_Policy_Unresolved_Experimental_Spine.pdf   # Sample clinical test PDF (Policy Unresolved)
├── HOW_TO_RUN.md                                        # Quick reference cheat-sheet
├── README.md                                            # Comprehensive project manual
├── pytest.ini                                           # Pytest configuration & pythonpath
├── requirements.txt                                     # Python package dependencies
│
├── medrule_engine/                                      # Core deterministic decision engine & web app
│   ├── benchmarks/                                      # Synthetic benchmark cases and reporting
│   ├── examples/                                        # Sample clinical cases for CLI and API testing
│   ├── governance/                                      # SQLite persistence, audit trails, review workflow
│   ├── integrations/                                    # Case intake pipeline, payer configs, connectors
│   │   ├── intake_service.py                            # 10-stage case intake orchestrator
│   │   ├── mock_connectors.py                           # Payer eligibility & benefit adapters
│   │   ├── payer_config.py                              # Evolent & Centene plan schedules
│   │   ├── pdf_extractor.py                             # PyMuPDF clinical document extraction module
│   │   └── submission.py                                # Locked outbound submission stub
│   ├── pilot/                                           # 36-case pilot adjudication runner and datasets
│   ├── tests/                                           # Unit, integration, and end-to-end test suites
│   ├── web/                                             # Flask app, HTML templates, CSS styles, static assets
│   │   ├── static/css/style.css                         # Layout tokens, responsive navbar, component styles
│   │   └── templates/                                   # Jinja2 review templates (intake, case_detail, etc.)
│   ├── case_schema.json                                 # Draft-07 JSON Schema for prior-auth cases
│   ├── case_validator.py                                # Schema and semantic validator
│   ├── cli.py                                           # Unified command-line interface entrypoint
│   ├── condition_evaluator.py                           # Three-valued boolean and comparison logic engine
│   ├── decision_aggregator.py                           # Rollup aggregator for case determinations
│   ├── evaluation_service.py                            # Multi-rule evaluation orchestrator
│   ├── evidence_validator.py                            # Clinical parameter validation utilities
│   ├── policy_router.py                                 # Rule matching and domain routing logic
│   └── rule_registry.py                                 # In-memory catalog of all 372 clinical policy rules
│
└── rulebook_collection/                                 # Authoritative policy rules, schemas, and PDFs
    ├── cross_domain_references/                         # CMS manuals, DMEPOS standards, RESNA papers
    ├── domains/                                         # Nine clinical domains containing rules and PDFs
    ├── downloaded_pdfs/                                 # Clinical policy documentation downloads
    ├── manifests/                                       # Master inventories and audit trails
    ├── schemas/                                         # Canonical JSON schemas for policy rules
    └── source_pdfs/                                     # Governing clinical guideline PDFs
```

---

## Security Architecture

1. **Path Traversal Sandboxing**: The `/pdf/<path:pdf_path>` route sanitizes incoming paths, rejecting parent references (`..`), URL-encoded tokens (`%2e`), null bytes (`\x00`), and any path outside the repository root.
2. **Strict File Type Enforcement**: Only files with a `.pdf` extension are served by the PDF viewer. Requests for code (`.py`), data (`.json`, `.db`), or environment variables (`.env`) return HTTP 400.
3. **HTTP Security Headers**: Web responses enforce `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and strict `Content-Security-Policy` directives.
4. **Input Schema Validation**: Case payloads submitted through the web form, API, or CLI are strictly validated against `case_schema.json` using JSON Schema Draft-07.
5. **Simulated Payer Integration**: External network calls are blocked. Connectors run in simulated mode, and outbound prior-authorization submission adapters are permanently disabled.
