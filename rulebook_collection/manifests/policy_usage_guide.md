# MedRule Clinical Policy Usage Guide

**Document ID:** MEDRULE-GUIDE-POLICY-USAGE-001  
**Audit & Implementation Date:** 2026-10-21  
**Target Audience:** Clinical informaticists, software engineers, and utilization management system operators  
**System Classification:** Non-binding clinical decision-support prototype  

---

## 1. Where to Find the Governing Clinical Policies

All clinical policies and supporting references are located within the `rulebook_collection/` directory:

### 1.1 Clinical Necessity Governing Documents
These documents define whether a diagnostic imaging test or interventional pain procedure is clinically indicated:

- **Advanced Imaging (CT, MRI, CTA, MRA, PET/CT):**  
  [`rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/policies/current/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf)  
  *Page Count: 1,041 pages | Effective: January 1, 2026 – December 31, 2026*
- **Interventional Pain Management (ESI, Facet, SCS, SI Joint):**  
  [`rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/policies/current/2026%20Evolent%20Interventional%20Pain%20Management%20Guidelines.pdf)  
  *Page Count: 102 pages | Effective: July 1, 2026 – July 1, 2027*

### 1.2 Place of Service (Site of Care) Documents
These documents govern facility reimbursement and dictate whether a service can be performed in a hospital outpatient setting versus a preferred freestanding office or ambulatory surgery center:

- **Radiology Place of Service Policy (EPOS 2067):**  
  [`rulebook_collection/domains/advanced_imaging/policies/current/EPOS 2067 for Place of Service - Radiology 2026_final.pdf`](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/policies/current/EPOS%202067%20for%20Place%20of%20Service%20-%20Radiology%202026_final.pdf)  
  *Page Count: 11 pages | Revised: November 2025*
- **Interventional Pain Management Place of Service Policy (EPOS 1755):**  
  [`rulebook_collection/domains/interventional_pain_management/policies/current/EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/policies/current/EPOS%201755%20for%20Place%20of%20Service%20-%20Interventional%20Pain%20Management%202026_final.pdf)  
  *Page Count: 8 pages | Revised: December 2025*

### 1.3 Supporting References (Non-Governing)
Supporting forms, checklists, and tip sheets reside in `supporting_documents/` under each domain:
- **Checklists & History Forms:** Clinical intake aids (e.g. `LDCT Form Evolent 02162024_0.pdf`, `Conservative Treatment Form - IPM Evolent 08072025.pdf`).
- **Tip Sheets:** Advisory educational summaries (e.g. `Brain MRI vs CT Tip Sheet 4.27.26.pdf`, `IPM Tip Sheet Evolent 04262024.pdf`).  
  > [!IMPORTANT]
  > Supporting documents are clinical tools only. They have zero authority to override the governing clinical policy text.

---

## 2. Case Intake & Required Input Fields

Case payloads submitted to MedRule must conform to [`medrule_engine/case_schema.json`](file:///d:/PreAuth/medrule_engine/case_schema.json).

### Required Fields
1. `case_id`: Unique synthetic identifier matching `^CASE-[A-Z0-9_-]+$`.
2. `clinical_domain`: Must be `"advanced_imaging"` or `"interventional_pain_management"`.
3. `procedure_code`: Standard CPT/HCPCS code (e.g. `"70551"`, `"62322"`).
4. `procedure_name`: Human-readable label (e.g. `"Brain MRI"`, `"Epidural Steroid Injection"`).
5. `requested_date_of_service`: ISO date string `YYYY-MM-DD` (must be `>= 2026-01-01` for 2026 guidelines).
6. `line_of_business`: Must be `"COMMERCIAL"`, `"MEDICARE_ADVANTAGE"`, or `"MEDICAID"`.
7. `payer_id`: Payer identifier string (e.g. `"EVOLENT"`).
8. `clinical_evidence`: Key-value dictionary containing structured patient findings, prior treatments, lab results, and place of service details.

---

## 3. How to Run an Evaluation

### 3.1 Via Command-Line Interface (CLI)
Use the `--tree` flag to invoke the deterministic decision-tree layer:

```bash
# Evaluate a case JSON file using the decision tree engine with formatted output
python -m medrule_engine.cli evaluate --case path/to/case.json --tree --pretty

# Save evaluation audit JSON to file
python -m medrule_engine.cli evaluate --case path/to/case.json --tree --output audit_result.json
```

### 3.2 Via Python Service Interface
```python
from medrule_engine.evaluation_service import EvaluationService

service = EvaluationService()

# Evaluate case dictionary
assessment = service.evaluate_decision_tree(case_dict)

print(f"Overall Outcome: {assessment.overall_outcome.value}")
print(f"Clinical Necessity: {assessment.clinical_necessity_outcome.value}")
if assessment.place_of_service_outcome:
    print(f"Place of Service: {assessment.place_of_service_outcome.value}")
print(f"Reproducibility Hash: {assessment.reproducibility_hash}")
```

---

## 4. Understanding Evaluation Outcomes & Audit Traces

### 4.1 Outcome Values
- `CRITERIA_MET`: All mandatory clinical necessity and place of service criteria were evaluated and satisfied by documented evidence.
- `CRITERIA_NOT_MET`: At least one mandatory condition evaluated to `FALSE` (failed criteria) or a disqualifying exclusion criterion evaluated to `TRUE` (contraindication present).
- `INSUFFICIENT_INFORMATION`: Required mandatory criteria lack evidence in `clinical_evidence`. The engine pends the case for clinical documentation.
- `NEEDS_HUMAN_REVIEW`: Autonomous adjudication halted. Triggered when the case touches a governance-blocked rule, advisory wording, or an uncodified clinical coverage gap.
- `POLICY_NOT_APPLICABLE`: Case domain or procedure code is outside the scope of active policies.
- `POLICY_VERSION_UNRESOLVED`: Date of service precedes policy effective date boundary (`2026-01-01`).

### 4.2 Inspecting Provenance Traces
Every evaluated rule attaches full source-level provenance. Access traces via `assessment.clinical_necessity_rules` or `assessment.place_of_service_rules`:

```python
for rule_exec in assessment.clinical_necessity_rules:
    print(f"Rule ID: {rule_exec.rule_id} -> Outcome: {rule_exec.outcome.value}")
    print(f"  Source File: {rule_exec.provenance['source_file']}")
    print(f"  Physical Page: {rule_exec.provenance['physical_page']}")
    print(f"  Source Section: {rule_exec.provenance['source_section']}")
    print(f"  Source Quote: \"{rule_exec.provenance['source_quote']}\"")
    for trace in rule_exec.traces:
        print(f"    Criterion {trace.condition_id}: {trace.parameter} {trace.comparator} {trace.expected_value} | Actual={trace.actual_value} -> {trace.status.value}")
```

### 4.3 Identifying Blocked Rules and Coverage Gaps
- **Blocked Rules:** Check `assessment.human_review_reasons`. Blocked rules (e.g. `RULE-ADV-PREAMBLE-001`, `RULE-ADV-CG2000-003`) have `rule_exec.is_blocked_by_governance == True`.
- **Coverage Gaps:** Check `assessment.uncovered_gaps_encountered`. Gaps list the exact policy section where criteria remain uncodified (e.g. IPM CG 1750 spinal stenosis canal diameter thresholds).

---

## 5. Dual-Track Place of Service Handling

Clinical Necessity and Place of Service are evaluated on separate tracks:
- **Both MET:** Overall outcome is `CRITERIA_MET`.
- **Clinical Necessity MET, Place of Service NOT MET:**  
  The engine preserves `clinical_necessity_outcome = CRITERIA_MET`, but sets `overall_outcome = CRITERIA_NOT_MET` with a mandatory redirection note:  
  *"Clinical necessity criteria satisfied, but requested Place of Service does not meet policy guidelines. Redirection to ambulatory/freestanding facility required."*

---

## 6. Real Reproducible Synthetic Test Examples

### 6.1 Domain 1: Advanced Imaging Synthetic Case
**File:** `synthetic_mri_brain_ms.json`
```json
{
  "case_id": "CASE-SYNTH-AI-001",
  "clinical_domain": "advanced_imaging",
  "procedure_code": "70551",
  "procedure_name": "Brain MRI",
  "requested_date_of_service": "2026-06-15",
  "line_of_business": "COMMERCIAL",
  "payer_id": "EVOLENT",
  "modality": "MRI",
  "place_of_service": "OFFICE",
  "clinical_evidence": {
    "suspected_or_established_multiple_sclerosis": true,
    "place_of_service_code": "POS_11"
  }
}
```
**Expected Deterministic Output:**
- `clinical_necessity_outcome`: `CRITERIA_MET`
- `place_of_service_outcome`: `CRITERIA_MET`
- `overall_outcome`: `CRITERIA_MET`
- `governing_policy`: `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (p. 232)

### 6.2 Domain 2: Interventional Pain Management Synthetic Case
**File:** `synthetic_ipm_facet_denervation.json`
```json
{
  "case_id": "CASE-SYNTH-IPM-001",
  "clinical_domain": "interventional_pain_management",
  "procedure_code": "64635",
  "procedure_name": "Facet Radiofrequency Neurotomy",
  "requested_date_of_service": "2026-08-01",
  "line_of_business": "COMMERCIAL",
  "payer_id": "EVOLENT",
  "place_of_service": "OFFICE",
  "clinical_evidence": {
    "diagnostic_facet_block_relief": 70,
    "place_of_service_code": "POS_11",
    "epos1755_indication": true
  }
}
```
**Expected Deterministic Output:**
- `clinical_necessity_outcome`: `CRITERIA_MET` (relief 70% >= 50% threshold)
- `place_of_service_outcome`: `CRITERIA_MET`
- `overall_outcome`: `CRITERIA_MET`
- `governing_policy`: `2026 Evolent Interventional Pain Management Guidelines.pdf` (p. 25)

---

## 7. How to Safely Introduce a New Policy Version

To introduce a new policy version (e.g. 2027 Guidelines) without allowing historical criteria to corrupt evaluations:

1. **Deposit New PDF:** Place new governing PDF in `rulebook_collection/domains/{domain}/policies/current/`.
2. **Relocate Preceding PDF:** Move previous PDF to `policies/historical/`.
3. **Set Version Metadata:** Tag new rules with `version_status = "current_2027_verified"`. Update preceding rules to `version_status = "historical_superseded"`.
4. **Update Router Date Boundary:** Update `PolicyRouter` effective date checks to recognize the new version's implementation date.
5. **Execute Integrity & Regression Tests:**
   ```bash
   pytest rulebook_collection/tests/test_scope_integrity.py -v
   pytest medrule_engine/tests/test_decision_tree.py -v
   ```
6. **Governance Rule:** Never promote any new rule to `APPROVED` without formal clinical leadership vetting.

---

## 8. What the System Cannot Currently Determine

The operator must understand the current technical and clinical boundaries:
1. **Uncodified Clinical Criteria:** Uncodified coverage gaps (e.g. spinal stenosis without radiculopathy, DRG stimulation outside lower extremities) cannot be adjudicated autonomously and are escalated to human review.
2. **Proprietary Health Plan Variations:** The system operates against the national Evolent clinical baseline and does not codify custom carve-outs for specific employer groups or payers.
3. **Subjective Clinical Judgment:** Preamble language mandating holistic physician medical necessity overrides cannot be calculated algorithmically.
4. **Legal / Binding Determination:** This system is a non-binding prototype. `is_binding = False` is hardcoded across all assessments.
