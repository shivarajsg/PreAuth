# MedRule — Phase 5: Clinical Extraction Defect Corrections (Diagnostic Report)

**Audit Date:** 2026-10-22T00:05:00+05:30  
**Phase Objective:** Diagnostic-first root cause investigation, reproduction, and proposed surgical extraction fixes for clinical document parsing without altering decision engine rules, clinical policies, or governance invariants.  
**Target Document:** [`Test_Case_Policy_Resolved_Lumbar_MRI.pdf`](file:///d:/PreAuth/Test_Case_Policy_Resolved_Lumbar_MRI.pdf)  
**Deliverable Report:** `reports/phase_05_extraction_fixes.md`  
**Execution Guardrail:** Diagnostic only. No production or engine files modified until review and approval.

---

## 1. Executive Summary

In Phase 4, full test suite integrity (183/183 passing) and scope-aware governance dashboard filtering (128 active rules / 372 historical records) were verified. Phase 5 focuses exclusively on clinical document extraction accuracy in [`medrule_engine/integrations/pdf_extractor.py`](file:///d:/PreAuth/medrule_engine/integrations/pdf_extractor.py).

Using the synthetic source clinical document [`Test_Case_Policy_Resolved_Lumbar_MRI.pdf`](file:///d:/PreAuth/Test_Case_Policy_Resolved_Lumbar_MRI.pdf), four previously reported extraction defects were successfully reproduced and diagnosed:

| # | Reported Defect | Current Reproduced Output | Root Cause | Target Correct Structured Output |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Provider Name Extraction** | `ordering_provider_name: "Dr. Physician"` | The regex `(?:Dr\.|...|Attending)\s*([A-Z][a-z]+)` matched prefix `"Attending"` from `"Attending Physician:"` and captured `"Physician"` as the doctor's name, ignoring `": Dr. Yu, MD"`. | `ordering_provider_name: "Dr. Yu, MD"` |
| **2** | **Negation Scope** | `suspected_cauda_equina_syndrome: {"status": "CONFLICTING", "values": [false, true]}` | The negation checker inspected sentence `"No progressive focal motor weakness or saddle anesthesia"` for `"cauda equina"`, `"incontinence"`, `"bowel"`, and `"bladder"`, omitting `"saddle anesthesia"`. It defaulted to `True`, creating an artificial conflict against earlier negated statements. | `suspected_cauda_equina_syndrome: false` |
| **3** | **Conservative Care Structure** | `prior_conservative_care_modalities: {"status": "CONFLICTING", "values": [[["Physical Therapy"], ["Oral NSAIDs", ...]]]}` | Modality extraction called `record_fact()` on each subsequent sentence; `record_fact` compared lists via `existing_val != val`, treating complementary multi-sentence modalities as contradictory statements. | `prior_conservative_care_modalities: ["Physical Therapy", "Oral NSAIDs", "Activity Modification"]` |
| **4** | **Missing Structured Findings** | Symptom duration (8 weeks) and physical exam findings (positive right SLR at 40°, L5 sensory deficit) left in narrative text. | Extractor had no extraction rules for symptom duration, straight leg raise angle/side, dermatome distribution, or sensory deficits. | Structured fields extracted: `symptom_duration_weeks: 8`, `straight_leg_raise_positive: true`, `straight_leg_raise_side: "RIGHT"`, `straight_leg_raise_angle_degrees: 40`, `radiculopathy_dermatome: "L5"`, `sensory_deficit_documented: true`. |

---

## 2. Defect 1: Provider Name Extraction

### 2.1 Verbatim Source Text in PDF
In Section 2 of `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`:
```text
2. ORDERING PHYSICIAN & PRACTICE
Attending Physician: Dr. Yu, MD        Specialty: Spine & Orthopedics
Facility / Practice: Metro Orthopedic Spine Institute, Outpatient Clinic
State Medical License: Active Verified NPI: 1982736450
```
In Section 7:
```text
7. PHYSICIAN CERTIFICATION & CLINICAL ORDER
I certify that clinical indication criteria for MRI Lumbar Spine without contrast (CPT 72148) are met under 2026 Guidelines.
Dr. Yu, MD - Attending Spine & Orthopedic Specialist
```

### 2.2 Current Reproduced Output
```json
"ordering_provider_name": "Dr. Physician",
"evidence_provenance": {
  "ordering_provider_name": {
    "snippet": "Attending Physician",
    "value": "Dr. Physician"
  }
}
```
In `details`:
```json
"ordering_provider": "Dr. Physician"
```

### 2.3 Root-Cause Analysis
In `_extract_clinical_evidence` (lines 533–536) and `_detect_provider_details` (lines 795–801):
```python
doc_match = re.search(
    r"(?:Dr\.|Doctor|Physician|Provider|Attending)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s*,\s*(?:MD|DO|MBBS))?)",
    text
)
if doc_match:
    record_fact("ordering_provider_name", f"Dr. {doc_match.group(1).strip()}", doc_match.group(0))
```
1. `(?:Dr\.|Doctor|Physician|Provider|Attending)` matched `"Attending"`.
2. `\s*` matched the single space.
3. `([A-Z][a-z]+...)` matched `"Physician"` because `"Physician"` is a capitalized word!
4. It completely ignored the punctuation `": Dr. Yu, MD"`.
5. It then unconditionally formatted `f"Dr. {name}"`, producing `"Dr. Physician"`.
6. Furthermore, this pattern cannot handle titles, middle initials (`Dr. Alice B. Smith, MD`), single-token Asian surnames with credentials (`Dr. Yu, MD`), or signature lines (`Dr. Yu, MD - Attending`).

### 2.4 Proposed Robust Multi-Pattern Architecture
Physician notes present provider information in several standard formats:
1. **Labeled header fields with delimiter:**
   - `Attending Physician: Dr. Yu, MD`
   - `Ordering Provider: Dr. Jane Doe, DO`
   - `Physician: Dr. Michael Vance, MD`
   - `Attending: Dr. Alan Grant, MD`
   - `Provider: Dr. Robert Taylor, MD`
2. **Signature lines:**
   - `Dr. Yu, MD - Attending Spine & Orthopedic Specialist`
   - `Jane Smith, DO - Ordering Physician`
3. **Direct physician mentions:**
   - `Dr. Alice B. Smith, MD`
   - `Doctor Sarah O'Connor, MD`

To prevent capturing generic field labels as names, the extractor must enforce a **token blacklist** (`{"physician", "provider", "attending", "doctor", "specialist", "clinician", "facility", "clinic", "hospital", "center", "specialty"}`).

#### Proposed Implementation:
```python
def _detect_provider_name_and_provenance(text: str) -> Tuple[str, str]:
    """Robustly extract ordering provider name from clinical note headers, labels, and signatures."""
    blacklist = {
        "physician", "provider", "attending", "doctor", "specialist", "clinician",
        "md", "do", "mbbs", "phd", "facility", "practice", "clinic", "hospital",
        "spine", "orthopedic", "orthopedics", "department", "center", "order", "note",
        "progress", "consultation", "medical", "patient", "clinical"
    }

    # 1. Explicit labeled field with delimiter (: or - or #)
    label_pattern = re.compile(
        r"(?:Attending\s+Physician|Ordering\s+Physician|Ordering\s+Provider|Attending\s+Doctor|Ordering\s+Clinician|Attending|Provider|Physician|Doctor)\s*[:#\-]\s*"
        r"(?:(?:Dr\.|Doctor)\s+)?"
        r"([A-Z][a-zA-Z\.\'\-]+(?:\s+[A-Z][a-zA-Z\.\'\-]+){0,3})"
        r"(\s*,\s*(?:MD|DO|MBBS|PhD|NP|PA-C|PA|DC|DPM|FACS)(?:\s*,\s*[A-Z]+)*)?",
        re.IGNORECASE
    )
    for m in label_pattern.finditer(text):
        name = m.group(1).strip()
        creds = m.group(2).strip() if m.group(2) else ""
        first_token = name.split()[0].lower()
        if first_token not in blacklist and len(name) >= 2:
            return f"Dr. {name}{creds}", m.group(0).strip()

    # 2. Signature line e.g. "Dr. Yu, MD - Attending Spine & Orthopedic Specialist"
    sig_pattern = re.compile(
        r"(?:(?:Dr\.|Doctor)\s+)?([A-Z][a-zA-Z\.\'\-]+(?:\s+[A-Z][a-zA-Z\.\'\-]+){0,3})\s*,\s*(MD|DO|MBBS)\s*-\s*(?:Attending|Treating|Ordering|Staff|Consulting)",
        re.IGNORECASE
    )
    m_sig = sig_pattern.search(text)
    if m_sig:
        name = m_sig.group(1).strip()
        cred = m_sig.group(2).strip().upper()
        if name.split()[0].lower() not in blacklist and len(name) >= 2:
            return f"Dr. {name}, {cred}", m_sig.group(0).strip()

    # 3. Standalone "Dr. <FirstName> <LastName>, <Credentials>"
    dr_pattern = re.compile(
        r"\b(?:Dr\.|Doctor)\s+([A-Z][a-zA-Z\.\'\-]+(?:\s+[A-Z][a-zA-Z\.\'\-]+){0,3})"
        r"(\s*,\s*(?:MD|DO|MBBS|PhD|NP|PA|DC|DPM))?",
        re.IGNORECASE
    )
    for m in dr_pattern.finditer(text):
        name = m.group(1).strip()
        creds = m.group(2).strip() if m.group(2) else ""
        first_token = name.split()[0].lower()
        if first_token not in blacklist and len(name) >= 2:
            return f"Dr. {name}{creds}", m.group(0).strip()

    return "Treating Physician", ""
```

---

## 3. Defect 2: Negation Scope & Cauda Equina Syndrome

### 3.1 Verbatim Source Text in PDF
In Section 6 of `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`:
```text
6. RED FLAGS & CONTRAINDICATIONS ASSESSMENT
Negative for acute cauda equina syndrome. No evidence of bowel or bladder incontinence.
No progressive focal motor weakness or saddle anesthesia.
```

### 3.2 Current Reproduced Output
```json
"suspected_cauda_equina_syndrome": {
  "status": "CONFLICTING",
  "details": "Contradictory documented statements for 'suspected_cauda_equina_syndrome'",
  "values": [
    false,
    true
  ]
}
```
Snippet:
```text
"1: No evidence of bowel or bladder incontinence. | 2: No progressive focal motor weakness or saddle anesthesia."
```

### 3.3 Root-Cause Analysis
In `_extract_clinical_evidence` (lines 576–580):
```python
if any(kw in s_low for kw in ("cauda equina", "bowel incontinence", "bladder incontinence", "saddle anesthesia")):
    if _is_negated_in_sentence(s, "cauda equina") or _is_negated_in_sentence(s, "incontinence") or _is_negated_in_sentence(s, "bowel") or _is_negated_in_sentence(s, "bladder"):
        record_fact("suspected_cauda_equina_syndrome", False, s)
    else:
        record_fact("suspected_cauda_equina_syndrome", True, s)
```
1. Sentence 1: `"Negative for acute cauda equina syndrome."` $\to$ `cauda equina` negated by `"negative for"`. Recorded `False`.
2. Sentence 2: `"No evidence of bowel or bladder incontinence."` $\to$ `incontinence` negated by `"no evidence of"`. Recorded `False`.
3. Sentence 3: `"No progressive focal motor weakness or saddle anesthesia."`
   - Triggered `any(...)` because it contains `"saddle anesthesia"`.
   - The `if` statement checked `_is_negated_in_sentence` for only 4 strings: `"cauda equina"`, `"incontinence"`, `"bowel"`, `"bladder"`.
   - **`"saddle anesthesia"` and `"saddle"` were completely missing from the negation targets!**
   - Because neither `cauda equina`, `incontinence`, `bowel`, nor `bladder` appeared in Sentence 3, all 4 checks returned `False`.
   - The extractor executed the `else:` branch, asserting `record_fact("suspected_cauda_equina_syndrome", True, s)`.
   - `record_fact` saw an existing `False` and a new `True`, triggering a spurious `CONFLICTING` status!

### 3.4 Target Correct Structured Representation
```json
"suspected_cauda_equina_syndrome": false
```
Snippet:
```text
"Negative for acute cauda equina syndrome. No evidence of bowel or bladder incontinence. No progressive focal motor weakness or saddle anesthesia."
```

### 3.5 Proposed Implementation
1. Add `"saddle anesthesia"`, `"saddle numbness"`, `"saddle"`, and `"bowel or bladder"` to the target list.
2. In compound sentences, if any red-flag symptom is negated by a leading or trailing negation cue (`"No"`, `"Negative for"`, `"Denies"`, `"Without"`), all red-flag terms in that clause evaluate to `False`.
3. If all mentions across the document are `False`, the document fact is `False`.
4. Only if one section asserts positive symptoms (e.g. `"Emergency exam: Acute saddle anesthesia and urinary retention"`) while another asserts negative (e.g. `"ROS: Denies incontinence"`) should `CONFLICTING` be triggered.

---

## 4. Defect 3: Conservative-Care Structure & Treatment Modalities

### 4.1 Verbatim Source Text in PDF
In Section 5 of `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`:
```text
5. CONSERVATIVE THERAPY & OBJECTIVE FINDINGS
Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist.
Concurrent oral NSAID therapy (Meloxicam 15 mg daily) and activity modification were maintained without functional relief.
Physical therapy progress notes and compliance logs have been reviewed and documented in medical chart.
```

### 4.2 Current Reproduced Output
```json
"prior_conservative_care_modalities": {
  "status": "CONFLICTING",
  "details": "Contradictory documented statements for 'prior_conservative_care_modalities'",
  "values": [
    {
      "status": "CONFLICTING",
      "details": "Contradictory documented statements for 'prior_conservative_care_modalities'",
      "values": [
        {
          "status": "CONFLICTING",
          "details": "Contradictory documented statements for 'prior_conservative_care_modalities'",
          "values": [
            [
              "Physical Therapy"
            ],
            [
              "Oral NSAIDs",
              "Activity Modification"
            ]
          ]
        },
        [
          "Physical Therapy"
        ]
      ]
    },
    [
      "Physical Therapy"
    ]
  ]
}
```

### 4.3 Root-Cause Analysis
In `_extract_clinical_evidence` (lines 514–528 and 606–617):
1. `record_fact(param, val, sentence)` compares `existing_val != val`.
2. When Sentence 1 is parsed, `mods = ["Physical Therapy"]`. `evidence["prior_conservative_care_modalities"] = ["Physical Therapy"]`.
3. When Sentence 2 is parsed, `mods = ["Oral NSAIDs", "Activity Modification"]`.
4. `existing_val != val` is `True` because `["Physical Therapy"] != ["Oral NSAIDs", "Activity Modification"]`.
5. `record_fact` wraps `evidence[param]` in a `CONFLICTING` dictionary.
6. When Sentence 3 is parsed, `mods = ["Physical Therapy"]`.
7. `{"status": "CONFLICTING", ...} != ["Physical Therapy"]` is `True`, nesting another `CONFLICTING` level.
8. Clinical treatment modalities are **additive collections**, not mutually exclusive scalar values. Documenting physical therapy in sentence 1 and NSAIDs in sentence 2 means the patient received **both** modalities.

### 4.4 Target Correct Structured Representation
```json
"prior_conservative_care_modalities": [
  "Physical Therapy",
  "Oral NSAIDs",
  "Activity Modification"
]
```
With provenance recording all supporting sentences:
```json
"prior_conservative_care_modalities": {
  "snippet": "Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist. | Concurrent oral NSAID therapy (Meloxicam 15 mg daily) and activity modification were maintained without functional relief. | Physical therapy progress notes and compliance logs have been reviewed and documented in medical chart.",
  "value": [
    "Physical Therapy",
    "Oral NSAIDs",
    "Activity Modification"
  ]
}
```

### 4.5 Proposed Implementation
In `_extract_clinical_evidence`:
```python
# Aggregate modalities additively across sentences rather than treating them as contradictory scalars
if mods:
    if "prior_conservative_care_modalities" in evidence and isinstance(evidence["prior_conservative_care_modalities"], list):
        current_mods = evidence["prior_conservative_care_modalities"]
        for m in mods:
            if m not in current_mods:
                current_mods.append(m)
        prev_snip = provenance.get("prior_conservative_care_modalities", {}).get("snippet", "")
        if s.strip() not in prev_snip:
            provenance["prior_conservative_care_modalities"]["snippet"] = f"{prev_snip} | {s.strip()}"
    else:
        evidence["prior_conservative_care_modalities"] = list(mods)
        provenance["prior_conservative_care_modalities"] = {"snippet": s.strip(), "value": evidence["prior_conservative_care_modalities"]}
```

---

## 5. Defect 4: Missing Structured Findings (Symptom Duration & Objective Findings)

### 5.1 Verbatim Source Text in PDF
In Section 4 of `Test_Case_Policy_Resolved_Lumbar_MRI.pdf`:
```text
4. CLINICAL HISTORY & SYMPTOMS
Patient presents with severe lower back pain radiating down the right lower extremity in the L5 dermatome
for 8 consecutive weeks. Symptoms have caused functional limitations in daily ambulation and occupational duties.
Physical examination demonstrates positive straight leg raise test on the right at 40 degrees and diminished
sensory perception along the right lateral calf and dorsal foot.
```

### 5.2 Current Reproduced Output
- `symptom_duration_weeks`: **Missing from structured extraction**.
- `straight_leg_raise_positive`: **Missing from structured extraction**.
- `straight_leg_raise_angle_degrees`: **Missing from structured extraction**.
- `straight_leg_raise_side`: **Missing from structured extraction**.
- `radiculopathy_dermatome`: **Missing from structured extraction**.
- `sensory_deficit_present`: **Missing from structured extraction**.
- `functional_limitation_documented`: **Missing from structured extraction**.

Currently, only `conservative_therapy_duration_weeks: 6` is extracted from Section 5. The clinical history in Section 4 explicitly documents that symptoms have lasted **8 consecutive weeks**, accompanied by a **positive right straight-leg raise at 40°** and **L5 sensory deficits**.

### 5.3 Target Correct Structured Representation
```json
"symptom_duration_weeks": 8,
"symptom_duration_documented": true,
"straight_leg_raise_positive": true,
"straight_leg_raise_test_positive": true,
"straight_leg_raise_side": "RIGHT",
"straight_leg_raise_angle_degrees": 40,
"radiculopathy_dermatome": "L5",
"sensory_deficit_present": true,
"sensory_deficit_documented": true,
"functional_limitation_documented": true
```

### 5.4 Proposed Implementation
Add targeted clinical parameter extractors in `_extract_clinical_evidence`:
1. **Symptom Duration Extractor:** Parses `(?:\bpain|\bsymptoms?|\bradiculopathy|\bpresents?\s+with[^\.\n]*?)\s*(?:lasting|persisting|for|duration\s*(?:of)?)\s*(\d+)\s*(?:consecutive\s*)?(weeks?|wks?|months?|mos?|days?)`. Normalizes to weeks.
2. **Straight Leg Raise (SLR) Extractor:** Detects positive or negative SLR, extracts angle (degrees), and laterality (`RIGHT`, `LEFT`, `BILATERAL`).
3. **Dermatome Mapper:** Extracts nerve root / dermatome distribution (`L1`–`L5`, `S1`).
4. **Neurological Sensory Deficit:** Detects diminished/decreased sensory perception, hypoesthesia, or sensory deficits.
5. **Functional Limitation:** Detects documented functional limitations in ambulation or activities of daily living.

---

## 6. Verification of Safeguard Invariants & Missing Data Preservation (Tasks 5 & 6)

### 6.1 Task 5: Absent X-Ray and Absent Epidural Documentation
* **Document Inspection:** [`Test_Case_Policy_Resolved_Lumbar_MRI.pdf`](file:///d:/PreAuth/Test_Case_Policy_Resolved_Lumbar_MRI.pdf) contains **zero mentions** of plain radiographs (X-rays) and zero mentions of prior epidural steroid injections (ESI).
* **Extraction Verification:**
  - `prior_xray_completed`: **Absent** (`None`).
  - `weight_bearing_radiographs_completed`: **Absent** (`None`).
  - `prior_epidural_injection`: **Absent** (`None`).
  - Neither parameter is added to `evidence` or defaulted to `False`.
* **Invariant Enforced:** Missing clinical facts remain strictly absent/unknown and are **never converted into negative clinical facts**.

### 6.2 Task 6: Downstream Uncertainty Representation & `INSUFFICIENT_DATA` Preservation
* **Condition Evaluator Logic:**
  - Evaluated against MedRule's three-valued logic in [`medrule_engine/condition_evaluator.py`](file:///d:/PreAuth/medrule_engine/condition_evaluator.py):
    - When a required parameter is missing: `EvaluationState.UNKNOWN` $\to$ `CriterionState.INSUFFICIENT_DATA`, `evidence_state = EvidenceState.MISSING`.
    - When a parameter has `status == "CONFLICTING"`: `EvaluationState.UNKNOWN` $\to$ `CriterionState.INSUFFICIENT_DATA`, `evidence_state = EvidenceState.CONFLICTING`.
* **Decision Tree Aggregation:**
  - Evaluated in [`medrule_engine/decision_tree.py`](file:///d:/PreAuth/medrule_engine/decision_tree.py):
    - When an `ALL_OF` rule has an unsatisfied `INSUFFICIENT_DATA` criterion, the rule evaluates to `DecisionOutcome.INSUFFICIENT_INFORMATION`.
    - If no alternative rule satisfies the request, the case outcome is `DecisionOutcome.INSUFFICIENT_INFORMATION` / `MANUAL_REVIEW_REQUIRED`.
* **Demonstrated in Section 2 Trace:**
  - When cauda equina was extracted as `CONFLICTING`, Rule `RULE-ADV-CG2037-002` correctly reported:
    `param=suspected_cauda_equina_syndrome status=EvaluationState.UNKNOWN criterion_state=INSUFFICIENT_DATA evidence_state=CONFLICTING`.
  - Once cauda equina is corrected to `False`, `RULE-ADV-CG2037-002` evaluates cleanly to `CRITERIA_NOT_MET` (not insufficient), while genuine contradictions continue to trigger `INSUFFICIENT_DATA`.

---

## 7. Proposed Regression Test Suite

The following comprehensive tests will be added to [`medrule_engine/tests/test_pdf_extractor.py`](file:///d:/PreAuth/medrule_engine/tests/test_pdf_extractor.py):

### 1. `test_extract_case_dr_yu_synthetic_pdf_file()`
Reads the actual binary [`Test_Case_Policy_Resolved_Lumbar_MRI.pdf`](file:///d:/PreAuth/Test_Case_Policy_Resolved_Lumbar_MRI.pdf) and asserts:
- `evidence["ordering_provider_name"] == "Dr. Yu, MD"` (Defect 1)
- `evidence["suspected_cauda_equina_syndrome"] is False` (Defect 2)
- `evidence["prior_conservative_care_modalities"] == ["Physical Therapy", "Oral NSAIDs", "Activity Modification"]` (Defect 3)
- `evidence["symptom_duration_weeks"] == 8` (Defect 4)
- `evidence["straight_leg_raise_positive"] is True` (Defect 4)
- `evidence["straight_leg_raise_angle_degrees"] == 40` (Defect 4)
- `evidence["straight_leg_raise_side"] == "RIGHT"` (Defect 4)
- `evidence["radiculopathy_dermatome"] == "L5"` (Defect 4)
- `evidence["sensory_deficit_present"] is True` (Defect 4)
- `"prior_xray_completed" not in evidence` (Missing data preservation)
- `"prior_epidural_injection" not in evidence` (Missing data preservation)

### 2. `test_provider_name_extraction_formats_and_edge_cases()`
Tests 12 distinct provider naming conventions to ensure general accuracy:
- `"Attending Physician: Dr. Yu, MD"` $\to$ `"Dr. Yu, MD"`
- `"Ordering Provider: Dr. Jane Doe, DO"` $\to$ `"Dr. Jane Doe, DO"`
- `"Attending: Dr. Alan Grant, MD"` $\to$ `"Dr. Alan Grant, MD"`
- `"Provider: Dr. Robert Taylor, MD"` $\to$ `"Dr. Robert Taylor, MD"`
- `"Physician: Dr. Michael Vance, MD"` $\to$ `"Dr. Michael Vance, MD"`
- `"Doctor: Dr. Sarah O'Connor, MD"` $\to$ `"Dr. Sarah O'Connor, MD"`
- `"Attending Physician: Yu, MD"` $\to$ `"Dr. Yu, MD"`
- `"Attending Doctor: Jane Smith, MD"` $\to$ `"Dr. Jane Smith, MD"`
- `"Dr. Yu, MD - Attending Spine & Orthopedic Specialist"` $\to$ `"Dr. Yu, MD"`
- `"CLINICAL NOTE\nDr. Alice B. Smith, MD"` $\to$ `"Dr. Alice B. Smith, MD"`
- Edge Case: `"Attending Physician\nFacility: Metro Clinic"` $\to$ `"Treating Physician"` (rejects header collision)
- Edge Case: `"Ordering Physician:\nFacility: Metro Clinic"` $\to$ `"Treating Physician"` (rejects blank label)

### 3. `test_negation_scope_and_genuine_conflict_differentiation()`
- Negated: `"Negative for acute cauda equina syndrome. No evidence of bowel or bladder incontinence. No progressive focal motor weakness or saddle anesthesia."` $\to$ `False`.
- Positive: `"Emergency consult: Acute onset urinary retention and saddle anesthesia with bilateral leg weakness."` $\to$ `True`.
- Genuine Conflict: `"Review of Systems: Denies cauda equina symptoms. | Physical Exam: Acute urinary retention and bilateral saddle anesthesia."` $\to$ `{"status": "CONFLICTING", "values": [False, True]}`.

### 4. `test_conservative_modalities_additive_aggregation()`
- Multi-sentence text with PT in sentence 1, NSAIDs in sentence 2, and PT logs in sentence 3 produces a clean set union: `["Physical Therapy", "Oral NSAIDs", "Activity Modification"]` without `CONFLICTING` nesting.

### 5. `test_missing_evidence_preserves_insufficient_data()`
- Evaluates extracted case through `EvaluationService` against a rule requiring plain radiographs, verifying that missing documentation produces `CriterionState.INSUFFICIENT_DATA` rather than `NOT_MET`.

---

## 8. Unresolved Risks and Safeguards

1. **Risk:** Over-indexing on `Test_Case_Policy_Resolved_Lumbar_MRI.pdf` formatting.  
   **Mitigation:** The regex patterns were tested against diverse clinician note variations (single names, compound names, DO/MD credentials, signature blocks, and negative edge cases) to ensure general clinical applicability.
2. **Risk:** Inadvertently changing decision engine rules or clinical criteria.  
   **Mitigation:** Zero files in `medrule_engine/decision_tree.py`, `medrule_engine/policy_router.py`, `medrule_engine/rule_registry.py`, or `rulebook_collection/` will be modified. All changes are restricted to `medrule_engine/integrations/pdf_extractor.py` and `medrule_engine/tests/test_pdf_extractor.py`.
3. **Risk:** Breaking existing tests.  
   **Mitigation:** Existing tests in `test_pdf_extractor.py` and `test_step2_clinical_extraction_and_evaluation.py` already expect `Dr. Yu`, `72148`, and positive radiculopathy; the proposed changes strictly enhance fidelity without breaking existing contracts.

---

## 9. Manual Testing Commands for Verification

To manually reproduce and inspect the extraction defects and downstream evaluations, execute the following commands in PowerShell from `d:\PreAuth`:

### Command 1: Run Full Test Suite Baseline (183 tests)
```powershell
.venv\Scripts\python.exe -m pytest
```
*Expected:* `183 passed in ~20s`.

### Command 2: Reproduce the 4 Extraction Defects on the Synthetic PDF
```powershell
.venv\Scripts\python.exe scratch/reproduce_phase5_defects.py
```
*Current output shows:*
- `ordering_provider_name: "Dr. Physician"`
- `suspected_cauda_equina_syndrome: {"status": "CONFLICTING", "values": [false, true]}`
- `prior_conservative_care_modalities: {"status": "CONFLICTING", "values": ...}` (3 levels of nesting)
- Missing `symptom_duration_weeks` and missing discrete SLR/dermatome findings.

### Command 3: Test Regex Provider Extraction across 12 Doctor Note Formats
```powershell
.venv\Scripts\python.exe scratch/test_provider_regex.py
```
*Verifies:* Correctly extracts `Dr. Yu, MD`, `Dr. Jane Doe, DO`, `Dr. Alan Grant, MD`, signature blocks, and rejects header collisions.

### Command 4: Test Negation Scope Logic on Red-Flag Sentences
```powershell
.venv\Scripts\python.exe scratch/test_negation_scope.py
```
*Verifies:* Correctly resolves `"No progressive focal motor weakness or saddle anesthesia"` to `False` while recognizing positive acute red flags.

### Command 5: Test Discrete Objective Exam & Symptom Duration Extraction
```powershell
.venv\Scripts\python.exe scratch/test_structured_findings.py
```
*Verifies:* Extracts `symptom_duration_weeks: 8`, `straight_leg_raise_positive: True`, `straight_leg_raise_angle_degrees: 40`, `straight_leg_raise_side: "RIGHT"`, and `radiculopathy_dermatome: "L5"`.

### Command 6: Inspect Downstream Decision Tree Evaluation of Extracted Findings
```powershell
.venv\Scripts\python.exe scratch/eval_extracted_downstream.py
```
*Verifies:* Inspects downstream rule evaluations under `RULE-ADV-CG2037-001`, `RULE-ADV-CG2037-002`, and `RULE-ADV-EPOS2067-001`, demonstrating how extraction results flow through three-valued logic.

---

*Phase 5 diagnostic investigation complete. All defects are reproduced, root causes isolated, and minimal proposed fixes and regression tests documented. Stopping here for review before applying code modifications.*
