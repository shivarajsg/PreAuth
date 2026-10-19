# MedRule Prior-Authorization Decision Support System — Quickstart Guide

This package contains the complete, locally runnable **MedRule Decision Support System** and the 372-rule clinical policy knowledge base across nine medical domains.

---

## 1. Prerequisites & Setup

- **Python**: Version 3.10 or higher (recommended Python 3.11+)
- **Operating System**: Windows, macOS, or Linux

### Install Dependencies
Open a terminal / command prompt in this folder and run:
```bash
pip install -r requirements.txt
```

---

## 2. Running the Application

### Launch the Web Interface
Start the local server:
```bash
python -m medrule_engine.cli serve --host 127.0.0.1 --port 5000
```
Then open your browser to **http://127.0.0.1:5000**:
- **Executive Dashboard**: `http://127.0.0.1:5000/`
- **Case Intake Portal**: `http://127.0.0.1:5000/intake`
- **Case History**: `http://127.0.0.1:5000/cases`
- **Rule Catalog (372 rules)**: `http://127.0.0.1:5000/rules`
- **Clinical SME Review Queue**: `http://127.0.0.1:5000/queue`
- **Pilot Adjudication Workbench**: `http://127.0.0.1:5000/pilot`
- **System Health**: `http://127.0.0.1:5000/health`

---

## 3. Testing with Included Clinical PDFs

Two test PDFs are provided in this directory for immediate testing at `http://127.0.0.1:5000/intake`:
1. `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`: Tests policy-resolved intake (CPT 72148) with automated criteria extraction and rule evaluation.
2. `Test_Case_Policy_Unresolved_Experimental_Spine.pdf`: Tests unlisted procedure handling (CPT 99999) triggering the `POLICY_CONTEXT_UNRESOLVED` governance workflow.

Upload either file in the PDF upload card on `/intake`, click **Upload & Analyze**, then click **Submit Prior-Authorization Case**.

---

## 4. Running via Command Line (CLI)

```bash
# 1. System Health Check & Safety Invariant Audit
python -m medrule_engine.cli health

# 2. Submit a Prior-Auth Case via Intake Pipeline
python -m medrule_engine.cli intake --case medrule_engine/examples/sample_intake_case.json

# 3. Direct Deterministic Policy Evaluation
python -m medrule_engine.cli evaluate --case medrule_engine/examples/case_01_adv_ct_pancreatitis_met.json

# 4. Run the 36-Case Pilot Benchmark Suite
python -m medrule_engine.cli pilot

# 5. Run the Full Test Suite (252 passed)
python -m pytest medrule_engine/tests/ rulebook_collection/ -q
```

---

## 4. Safety Invariants & Mode
- **Zero Generative AI**: 100% deterministic condition evaluation; no LLM APIs or neural models.
- **Strictly Non-Binding**: All outputs unconditionally enforce `is_binding: false`.
- **Zero Approved Rules**: All 372 rules remain in `DRAFT` (322) or `NEEDS_HUMAN_REVIEW` (50).
- **Outbound Submissions**: Permanently `DISABLED`.
