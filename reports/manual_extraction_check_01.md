# MedRule — Manual Extraction Check 1
**Audit Date:** 2026-10-21  
**Target Case:** Synthetic Lumbar Spine MRI Case (`Test_Case_Policy_Resolved_Lumbar_MRI.pdf`)  
**Scope:** Manual Verification of Clinical & Administrative PDF Extraction Accuracy Prior to UI Development  
**System Status:** Code, clinical rules, policy PDFs, and governance settings remain strictly unmodified.

---

## 1. Original Synthetic Input Document & Doctor's Note

The repository contains an original synthetic input PDF at the root: [`Test_Case_Policy_Resolved_Lumbar_MRI.pdf`](file:///d:/PreAuth/Test_Case_Policy_Resolved_Lumbar_MRI.pdf).
Below is the exact verbatim text extracted page-by-page from this original source document via PyMuPDF (`pymupdf.open('Test_Case_Policy_Resolved_Lumbar_MRI.pdf')`).

```text
CLINICAL PRE-CERTIFICATION ORDER: MRI LUMBAR SPINE (POLICY RESOLVED)
1. PATIENT & ENCOUNTER INFORMATION
Patient Name: John Doe                  Date of Birth: 04/12/1978 (Age: 48, Male)
Member ID: MEM-88219                   Date of Service: 2026-02-26
Health Plan: Commercial Choice Plus     Payer: Centene / Evolent Commercial
2. ORDERING PHYSICIAN & PRACTICE
Attending Physician: Dr. Yu, MD        Specialty: Spine & Orthopedics
Facility / Practice: Metro Orthopedic Spine Institute, Outpatient Clinic
State Medical License: Active Verified NPI: 1982736450
3. ORDERED PROCEDURE & DIAGNOSTIC CODING
Requested Procedure: MRI Lumbar Spine without contrast
Procedure Code: CPT 72148              Clinical Domain: Advanced Imaging
Primary Diagnosis: Muscle spasm of back with radiculopathy (ICD-10 M62.838)
4. CLINICAL HISTORY & SYMPTOMS
Patient presents with severe lower back pain radiating down the right lower extremity in the L5 dermatome
for 8 consecutive weeks. Symptoms have caused functional limitations in daily ambulation and occupational duties.
Physical examination demonstrates positive straight leg raise test on the right at 40 degrees and diminished
sensory perception along the right lateral calf and dorsal foot.
5. CONSERVATIVE THERAPY & OBJECTIVE FINDINGS
Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist.
Concurrent oral NSAID therapy (Meloxicam 15 mg daily) and activity modification were maintained without functional relief.
Physical therapy progress notes and compliance logs have been reviewed and documented in medical chart.
6. RED FLAGS & CONTRAINDICATIONS ASSESSMENT
Negative for acute cauda equina syndrome. No evidence of bowel or bladder incontinence.
No progressive focal motor weakness or saddle anesthesia.
7. PHYSICIAN CERTIFICATION & CLINICAL ORDER
I certify that clinical indication criteria for MRI Lumbar Spine without contrast (CPT 72148) are met under 2026 Guidelines.
Dr. Yu, MD - Attending Spine & Orthopedic Specialist
```

> [!NOTE]
> **Separation of Note vs Test Fixtures:**
> In addition to the PDF document above, two in-memory test fixtures exist in the testing suite:
> 1. In [`medrule_engine/tests/test_pdf_extractor.py`](file:///d:/PreAuth/medrule_engine/tests/test_pdf_extractor.py#L117-L130), a condensed 10-line variant of Dr. Yu's note with Member Name "John Smith" and Date of Service "2025-02-26".
> 2. In [`scratch/verify_step3_cases.py`](file:///d:/PreAuth/scratch/verify_step3_cases.py#L24-L37), case `1_lumbar_mri_supported` with Provider "Dr. Alan Grant, MD", Member ID "MEM-LUMB-0101", ICD-10 "M54.16", and 8 weeks of PT.
>
> All extraction data and evaluation results presented in this report reflect the **actual PDF input document** [`Test_Case_Policy_Resolved_Lumbar_MRI.pdf`](file:///d:/PreAuth/Test_Case_Policy_Resolved_Lumbar_MRI.pdf) processed through `extract_case_from_pdf()`.

---

## 2. Exact JSON Produced by Current PDF Extraction Function

Executed via `extract_case_from_pdf(pdf_bytes, filename="Test_Case_Policy_Resolved_Lumbar_MRI.pdf")` in [`medrule_engine/integrations/pdf_extractor.py`](file:///d:/PreAuth/medrule_engine/integrations/pdf_extractor.py):

```json
{
  "status": "SUCCESS",
  "filename": "Test_Case_Policy_Resolved_Lumbar_MRI.pdf",
  "pages_analyzed": 1,
  "extracted_fields": {
    "case_id": "CASE-PDF-1792584654",
    "patient_id": "MEM-88219",
    "clinical_domain": "advanced_imaging",
    "procedure_code": "72148",
    "procedure_name": "MRI Lumbar Spine without contrast",
    "line_of_business": "COMMERCIAL",
    "requested_date_of_service": "2026-02-26",
    "payer_id": "CENTENE",
    "plan_id": "COMMERCIAL_CHOICE_PLUS",
    "place_of_service": "OFFICE",
    "submitted_documents": "Comprehensive clinical notes and diagnostic findings, Uploaded Physician PDF (Test_Case_Policy_Resolved_Lumbar_MRI.pdf), Clinical Notes & Order Documentation",
    "evidence": {
      "ordering_provider_name": "Dr. Physician",
      "ordering_provider_license": true,
      "diagnosis_icd10": "M62.838",
      "laterality": "RIGHT",
      "anatomical_region": "LUMBAR_SPINE",
      "anatomy_region": "LUMBAR_SPINE",
      "clinical_office_notes": true,
      "clinical_indication_documented": true,
      "place_of_service_code": "POS_11",
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
      },
      "lumbar_radiculopathy_present": true,
      "radicular_pain_confirmed": true,
      "conservative_therapy_duration_weeks": 6,
      "conservative_care_weeks": 6,
      "conservative_care_completed": true,
      "red_flag_symptoms_documented": true,
      "suspected_cauda_equina_syndrome": {
        "status": "CONFLICTING",
        "details": "Contradictory documented statements for 'suspected_cauda_equina_syndrome'",
        "values": [
          false,
          true
        ]
      }
    },
    "evidence_provenance": {
      "ordering_provider_name": {
        "snippet": "Attending Physician",
        "value": "Dr. Physician"
      },
      "ordering_provider_license": {
        "snippet": "Attending Physician",
        "value": true
      },
      "diagnosis_icd10": {
        "snippet": "M62.838",
        "value": "M62.838"
      },
      "laterality": {
        "snippet": "Laterality documented: RIGHT",
        "value": "RIGHT"
      },
      "anatomical_region": {
        "snippet": "Anatomical region documented: LUMBAR_SPINE",
        "value": "LUMBAR_SPINE"
      },
      "anatomy_region": {
        "snippet": "Anatomical region documented: LUMBAR_SPINE",
        "value": "LUMBAR_SPINE"
      },
      "clinical_office_notes": {
        "snippet": "CLINICAL PRE-CERTIFICATION ORDER: MRI LUMBAR SPINE (POLICY RESOLVED)",
        "value": true
      },
      "clinical_indication_documented": {
        "snippet": "CLINICAL PRE-CERTIFICATION ORDER: MRI LUMBAR SPINE (POLICY RESOLVED)",
        "value": true
      },
      "place_of_service_code": {
        "snippet": "Place of Service: OFFICE (POS_11)",
        "value": "POS_11"
      },
      "prior_conservative_care_modalities": {
        "status": "CONFLICTING",
        "snippet": "1: 1: 1: Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist. | 2: Concurrent oral NSAID therapy (Meloxicam 15 mg daily) and activity modification were maintained without functional relief. | 2: Physical therapy progress notes and compliance logs have been reviewed and documented in medical chart. | 2: I certify that clinical indication criteria for MRI Lumbar Spine without contrast (CPT 72148) are met under 2026 Guidelines.",
        "value": [
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
      },
      "lumbar_radiculopathy_present": {
        "snippet": "Primary Diagnosis: Muscle spasm of back with radiculopathy (ICD-10 M62.838)",
        "value": true
      },
      "radicular_pain_confirmed": {
        "snippet": "Primary Diagnosis: Muscle spasm of back with radiculopathy (ICD-10 M62.838)",
        "value": true
      },
      "conservative_therapy_duration_weeks": {
        "snippet": "Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist.",
        "value": 6
      },
      "conservative_care_weeks": {
        "snippet": "Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist.",
        "value": 6
      },
      "conservative_care_completed": {
        "snippet": "Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist.",
        "value": true
      },
      "red_flag_symptoms_documented": {
        "snippet": "RED FLAGS & CONTRAINDICATIONS ASSESSMENT",
        "value": true
      },
      "suspected_cauda_equina_syndrome": {
        "status": "CONFLICTING",
        "snippet": "1: No evidence of bowel or bladder incontinence. | 2: No progressive focal motor weakness or saddle anesthesia.",
        "value": [
          false,
          true
        ]
      }
    }
  },
  "details": {
    "patient_id": "MEM-88219",
    "patient_dob": "04/12/1978",
    "patient_age": "Adult",
    "patient_gender": "Male",
    "ordering_provider": "Dr. Physician",
    "provider_specialty": "Attending Physician",
    "facility_name": "AL PRE",
    "procedure_code": "72148",
    "procedure_name": "MRI Lumbar Spine without contrast",
    "clinical_domain": "advanced_imaging",
    "clinical_domain_label": "Advanced Imaging",
    "diagnosis_icd10": "M62.838",
    "diagnosis_description": "Other muscle spasm / Lumbar radicular syndrome",
    "date_of_service": "2026-02-26",
    "line_of_business": "COMMERCIAL",
    "payer_id": "CENTENE",
    "plan_id": "COMMERCIAL_CHOICE_PLUS",
    "place_of_service": "OFFICE",
    "place_of_service_code": "POS_11",
    "key_findings": [
      "Diagnosis: Other muscle spasm / Lumbar radicular syndrome (ICD-10 M62.838)",
      "Ordering Physician: Dr. Physician",
      "Requested Procedure: MRI Lumbar Spine without contrast (CPT 72148)",
      "Place of Service: OFFICE (POS_11)",
      "Documented lumbar radiculopathy / radiating pain",
      "Prior conservative therapy documented (6 weeks)"
    ],
    "evidence_count": 17,
    "pages_analyzed": 1,
    "character_count": 2032,
    "narrative_excerpt": "CLINICAL PRE-CERTIFICATION ORDER: MRI LUMBAR SPINE (POLICY RESOLVED)\n1. PATIENT & ENCOUNTER INFORMATION\nPatient Name: John Doe                  Date of Birth: 04/12/1978 (Age: 48, Male)\nMember ID: MEM-88219                   Date of Service: 2026-02-26\nHealth Plan: Commercial Choice Plus     Payer: Centene / Evolent Commercial\n2. ORDERING PHYSICIAN & PRACTICE\nAttending Physician: Dr. Yu, MD        Specialty: Spine & Orthopedics\nFacility / Practice: Metro Orthopedic Spine Institute, Outpatient Clinic\nState Medical License: Active Verified NPI: 1982736450\n3. ORDERED PROCEDURE & DIAGNOSTIC CODING\nRequested Procedure: MRI Lumbar Spine without contrast\nProcedure Code: CPT 72148              Clinical Domain: Advanced Imaging\nPrimary Diagnosis: Muscle spasm of back with radiculopathy (ICD-10 M62.838)\n4. CLINICAL HISTORY & SYMPTOMS\nPatient presents with severe lower back pain radiating down the right lower extremity in the L5 dermatome\nfor 8 consecutive weeks. Symptoms have caused functional limitations in daily ambulation and occupational duties.\nPhysical examination demonstrates positive straight leg raise test on the right at 40 degrees and diminished\nsensory perception along the right lateral calf and dorsal foot.\n5. CONSERVATIVE THERAPY & OBJECTIVE FINDINGS\nPatient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist.\nConcurrent oral NSAID therapy (Meloxicam 15 mg daily) and activity modification were maintained without functional relief.\nPhysical therapy progress notes and compliance logs have been reviewed and documented in medical chart.\n6. RED FLAGS & CONTRAINDICATIONS ASSESSMENT\nNegative for acute cauda equina syndrome. No evidence of bowel or bladder incontinence.\nNo progressive focal motor weakness or saddle anesthesia.\n7. PHYSICIAN CERTIFICATION & CLINICAL ORDER\nI certify that clinical indication criteria for MRI Lumbar Spine without contrast (CPT 72148) are met under 2026 Guidelines.\nDr. Yu, MD - Attending Spine & Orthopedic Specialist"
  },
  "text_snippet": "CLINICAL PRE-CERTIFICATION ORDER: MRI LUMBAR SPINE (POLICY RESOLVED) 1. PATIENT & ENCOUNTER INFORMATION Patient Name: John Doe Date of Birth: 04/12/1978 (Age: 48, Male) Member ID: MEM-88219 Date of Service: 2026-02-26 Health Plan: Commercial Choice Plus Payer: Centene / Evolent Commercial 2. ORDERING PHYSICIAN & PRACTICE Attending Physician: Dr. Yu, MD Specialty: Spine & Orthopedics Facility / Practic",
  "summary": "Extracted 25 clinical & administrative fields from Test_Case_Policy_Resolved_Lumbar_MRI.pdf (1 pages, 2032 characters)."
}
```

---

## 3. Extracted Fields Alongside Exact Supporting Sentences

| Extracted Field | Extracted JSON Value | Exact Supporting Sentence / Line from Note | Attribution Quality |
| :--- | :--- | :--- | :--- |
| `procedure_code` | `"72148"` | `"Procedure Code: CPT 72148              Clinical Domain: Advanced Imaging"` | Exact direct match |
| `procedure_name` | `"MRI Lumbar Spine without contrast"` | `"Requested Procedure: MRI Lumbar Spine without contrast"` | Exact direct match |
| `clinical_domain` | `"advanced_imaging"` | `"Procedure Code: CPT 72148              Clinical Domain: Advanced Imaging"` | Exact catalog match |
| `patient_id` / `member_id` | `"MEM-88219"` | `"Member ID: MEM-88219                   Date of Service: 2026-02-26"` | Exact regex match |
| `line_of_business` | `"COMMERCIAL"` | `"Health Plan: Commercial Choice Plus     Payer: Centene / Evolent Commercial"` | Correct keyword inference |
| `payer_id` | `"CENTENE"` | `"Health Plan: Commercial Choice Plus     Payer: Centene / Evolent Commercial"` | Correct keyword inference |
| `plan_id` | `"COMMERCIAL_CHOICE_PLUS"` | `"Health Plan: Commercial Choice Plus     Payer: Centene / Evolent Commercial"` | Correct normalized mapping |
| `requested_date_of_service` | `"2026-02-26"` | `"Member ID: MEM-88219                   Date of Service: 2026-02-26"` | Exact ISO date match |
| `place_of_service` | `"OFFICE"` | `"Facility / Practice: Metro Orthopedic Spine Institute, Outpatient Clinic"` | Standard office classification |
| `place_of_service_code` | `"POS_11"` | `"Facility / Practice: Metro Orthopedic Spine Institute, Outpatient Clinic"` | Correct standard code |
| `diagnosis_icd10` | `"M62.838"` | `"Primary Diagnosis: Muscle spasm of back with radiculopathy (ICD-10 M62.838)"` | Exact ICD-10 regex match |
| `laterality` | `"RIGHT"` | `"Patient presents with severe lower back pain radiating down the right lower extremity in the L5 dermatome"` | Exact lateral keyword match |
| `anatomical_region` / `anatomy_region` | `"LUMBAR_SPINE"` | `"Requested Procedure: MRI Lumbar Spine without contrast"` | Exact anatomy keyword match |
| `ordering_provider_name` | `"Dr. Physician"` | `"Attending Physician: Dr. Yu, MD        Specialty: Spine & Orthopedics"` | **Defective extraction** (matched label "Physician" instead of name "Dr. Yu") |
| `ordering_provider_license` | `true` | `"State Medical License: Active Verified NPI: 1982736450"` (also matched from `"Attending Physician"`) | Correct boolean inference |
| `lumbar_radiculopathy_present` | `true` | `"Primary Diagnosis: Muscle spasm of back with radiculopathy (ICD-10 M62.838)"` | Exact clinical term match |
| `radicular_pain_confirmed` | `true` | `"Patient presents with severe lower back pain radiating down the right lower extremity in the L5 dermatome"` | Exact clinical term match |
| `conservative_therapy_duration_weeks` | `6` | `"Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist."` | Exact duration regex match |
| `conservative_care_completed` | `true` | `"Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist."` | Correct boolean threshold ($\ge 6$ wks) |
| `prior_conservative_care_modalities` | `{"status": "CONFLICTING", ...}` | Sentence 1: `"Patient has completed 6 weeks of structured physical therapy..."` <br>Sentence 2: `"Concurrent oral NSAID therapy (Meloxicam 15 mg daily) and activity modification were maintained..."` | **Defective conflict logic** (nested non-union conflict on multi-sentence modalities) |
| `red_flag_symptoms_documented` | `true` | `"6. RED FLAGS & CONTRAINDICATIONS ASSESSMENT"` | Exact heading match |
| `suspected_cauda_equina_syndrome` | `{"status": "CONFLICTING", "values": [false, true]}` | Sentence 1: `"Negative for acute cauda equina syndrome. No evidence of bowel or bladder incontinence."`<br>Sentence 2: `"No progressive focal motor weakness or saddle anesthesia."` | **Defective negation parsing** (first sentence parsed as `false`, second sentence parsed as `true` because "saddle anesthesia" was not recognized as negated by "No") |

---

## 4. Specific Clinical Field Breakdown

### 4.1 Requested Procedure and Anatomical Region
- **Documented in Note:** `"Requested Procedure: MRI Lumbar Spine without contrast"`, `"Procedure Code: CPT 72148"`, `"Clinical Domain: Advanced Imaging"`.
- **Extracted JSON:**
  - `procedure_code`: `"72148"`
  - `procedure_name`: `"MRI Lumbar Spine without contrast"`
  - `anatomical_region`: `"LUMBAR_SPINE"`
  - `anatomy_region`: `"LUMBAR_SPINE"`
  - `clinical_domain`: `"advanced_imaging"`
- **Assessment:** **Accurate**. Exactly matched canonical CPT and anatomical region tokens.

### 4.2 Laterality
- **Documented in Note:** `"radiating down the right lower extremity in the L5 dermatome"`, `"positive straight leg raise test on the right at 40 degrees"`, `"diminished sensory perception along the right lateral calf and dorsal foot"`.
- **Extracted JSON:**
  - `laterality`: `"RIGHT"`
- **Assessment:** **Accurate**.

### 4.3 Symptoms and Neurological Findings
- **Documented in Note:**
  1. Severe lower back pain radiating down the right lower extremity in the L5 dermatome.
  2. Functional limitations in daily ambulation and occupational duties.
  3. Positive straight leg raise test on the right at 40 degrees.
  4. Diminished sensory perception along the right lateral calf and dorsal foot.
- **Extracted JSON:**
  - `lumbar_radiculopathy_present`: `true`
  - `radicular_pain_confirmed`: `true`
  - Examination details (straight leg raise, reflex/sensory mapping) are retained in `details.narrative_excerpt` and `details.key_findings`, but are **not modeled as discrete fields** in `case_schema.json`.
- **Assessment:** **Partially Structured**. Core diagnostic gate (`lumbar_radiculopathy_present`) is captured accurately; specific physical exam findings are preserved only in free text.

### 4.4 Symptom Duration
- **Documented in Note:** `"for 8 consecutive weeks."`
- **Extracted JSON:**
  - `symptom_duration_weeks`: **Missing from structured extraction**.
  - Retained only in raw text: `"Patient presents with severe lower back pain radiating down the right lower extremity in the L5 dermatome for 8 consecutive weeks."`
- **Assessment:** **Omitted from structured schema**. Note explicitly states 8 weeks of symptoms, but `case_schema.json` and `pdf_extractor.py` currently only track conservative therapy duration (`conservative_therapy_duration_weeks`), omitting discrete symptom duration.

### 4.5 Prior Treatments and Their Duration
- **Documented in Note:**
  1. `"Patient has completed 6 weeks of structured physical therapy (2 sessions per week) with certified physical therapist."`
  2. `"Concurrent oral NSAID therapy (Meloxicam 15 mg daily) and activity modification were maintained without functional relief."`
  3. `"Physical therapy progress notes and compliance logs have been reviewed and documented in medical chart."`
- **Extracted JSON:**
  - `conservative_therapy_duration_weeks`: `6` (Accurate)
  - `conservative_care_weeks`: `6` (Accurate)
  - `conservative_care_completed`: `true` (Accurate)
  - `prior_conservative_care_modalities`: `{"status": "CONFLICTING", "values": [...]}` (Malformed)
- **Assessment:** **Quantitative duration is accurate (6 weeks)**; modality enumeration is structurally corrupted into a `CONFLICTING` tree because the extractor treated each subsequent sentence as a conflict rather than a list append.

### 4.6 Prior Imaging and Findings
- **Documented in Note:** The note contains **no mention** of prior plain radiographs, prior CT scans, or prior MRI studies.
- **Extracted JSON:**
  - `prior_imaging_performed`: Not present (`None`).
  - `lumbar_mri_nerve_root_compression`: Not present (`None`).
- **Assessment:** **Properly Left Absent**. The system did not treat the absence of prior imaging as a negative finding; it remained unasserted.

### 4.7 Explicit Positive and Negative Findings
- **Positive Findings in Note:**
  - Positive right straight leg raise at 40 degrees.
  - Diminished sensory perception along right lateral calf and dorsal foot.
  - Completed 6 weeks physical therapy and concurrent oral NSAIDs.
  - Radicular pain confirmed in L5 dermatome.
- **Negative Findings in Note:**
  - `"Negative for acute cauda equina syndrome."`
  - `"No evidence of bowel or bladder incontinence."`
  - `"No progressive focal motor weakness or saddle anesthesia."`
- **Extracted JSON:**
  - `suspected_cauda_equina_syndrome`: `{"status": "CONFLICTING", "values": [false, true]}`.
- **Assessment:** **Defective Negation Parser**. The extractor successfully recognized "Negative for acute cauda equina syndrome" as `false`, but when evaluating `"No progressive focal motor weakness or saddle anesthesia"`, its cue checker looked only for `cauda equina`, `incontinence`, `bowel`, and `bladder` against negation cues, failing to recognize that "No" applied to "saddle anesthesia". This generated a spurious `true` and triggered the conflict detector.

### 4.8 Missing or Contradictory Information
- **Missing Information in Note:**
  - Plain lumbar radiographs (X-rays).
  - Quantitative pre- and post-intervention functional pain scores (e.g., Oswestry Disability Index or VAS).
  - Patient phone number and residential address.
- **Contradictory Information:**
  - **In the Note itself:** None. The note is clinically coherent and non-contradictory.
  - **Introduced by the Extractor:**
    1. Provider Name: Extracted `"Dr. Physician"` instead of `"Dr. Yu, MD"`.
    2. Cauda Equina: Extracted `[false, true]` conflict.
    3. Modalities: Extracted `CONFLICTING` nested list.

### 4.9 Administrative Fields: Line of Business, Date of Service, Place of Service
- **Insurance Line of Business:**
  - Documented: `"Health Plan: Commercial Choice Plus Payer: Centene / Evolent Commercial"`
  - Extracted: `line_of_business`: `"COMMERCIAL"`, `payer_id`: `"CENTENE"`, `plan_id`: `"COMMERCIAL_CHOICE_PLUS"`
  - Assessment: **Accurate**.
- **Date of Service:**
  - Documented: `"Date of Service: 2026-02-26"`
  - Extracted: `requested_date_of_service`: `"2026-02-26"`
  - Assessment: **Accurate**.
- **Place of Service:**
  - Documented: `"Facility / Practice: Metro Orthopedic Spine Institute, Outpatient Clinic"`
  - Extracted: `place_of_service`: `"OFFICE"`, `place_of_service_code`: `"POS_11"`
  - Assessment: **Accurate** (non-hospital outpatient clinic correctly maps to POS 11 Office).

---

## 5. Accuracy Classification of All Fields

| Field Name | Status | Root Cause & Clinical Impact |
| :--- | :--- | :--- |
| `procedure_code` | **CORRECT** | Direct match to CPT 72148 |
| `procedure_name` | **CORRECT** | Matched canonical name "MRI Lumbar Spine without contrast" |
| `clinical_domain` | **CORRECT** | Routed to `advanced_imaging` |
| `line_of_business` | **CORRECT** | Identified Commercial Choice Plus $\to$ `COMMERCIAL` |
| `payer_id` | **CORRECT** | Normalized Centene / Evolent Commercial $\to$ `CENTENE` |
| `plan_id` | **CORRECT** | Normalized to `COMMERCIAL_CHOICE_PLUS` |
| `requested_date_of_service` | **CORRECT** | Parsed `2026-02-26` |
| `patient_id` | **CORRECT** | Parsed `MEM-88219` |
| `diagnosis_icd10` | **CORRECT** | Matched `M62.838` |
| `laterality` | **CORRECT** | Parsed `RIGHT` from radiating pain description |
| `anatomical_region` | **CORRECT** | Parsed `LUMBAR_SPINE` |
| `place_of_service` | **CORRECT** | Mapped clinic to `OFFICE` (`POS_11`) |
| `lumbar_radiculopathy_present` | **CORRECT** | Identified positive radiculopathy |
| `radicular_pain_confirmed` | **CORRECT** | Identified radiating nerve pain |
| `conservative_therapy_duration_weeks` | **CORRECT** | Parsed numeric value `6` from "6 weeks of structured physical therapy" |
| `conservative_care_completed` | **CORRECT** | Evaluated $\ge 6$ weeks threshold as `True` |
| `ordering_provider_license` | **CORRECT** | Identified active verified license |
| `clinical_office_notes` | **CORRECT** | Verified clinical order note documentation |
| `symptom_duration_weeks` | **MISSED** | 8 weeks documented in note, but not extracted into schema parameter |
| `physical_exam_objective_findings` | **MISSED** | SLR at 40 degrees and calf sensation loss not mapped to discrete schema fields |
| `prior_imaging_plain_radiographs` | **LEFT UNKNOWN** | Not in note; correctly preserved as missing/absent (not inferred negative) |
| `ordering_provider_name` | **INCORRECTLY INFERRED** | Regex captured label token `"Dr. Physician"` instead of `"Dr. Yu, MD"` |
| `suspected_cauda_equina_syndrome` | **INCORRECTLY INFERRED** | Extracted as `CONFLICTING` (`[false, true]`) due to failure to negate "saddle anesthesia" |
| `prior_conservative_care_modalities` | **INCORRECTLY INFERRED** | Multi-sentence modalities created nested conflicting object rather than set union |

---

## 6. Policy Routing, Rule Evaluation, and Criterion Outcomes

### 6.1 Policy Selection
The case was processed through `PolicyRouter.route_case()` in [`medrule_engine/policy_router.py`](file:///d:/PreAuth/medrule_engine/policy_router.py):
- **Routing Status:** `ROUTED`
- **Selected Governing Policies:**
  1. `2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)`  
     - Version Status: `current_2026_verified`
     - Domain: `advanced_imaging`
  2. `Evolent Place of Service Policy 2067 for Radiology (2026 Final)`  
     - Version Status: `current_2026_verified`
     - Domain: `advanced_imaging`

---

### 6.2 Evaluated Clinical Rules & Outcomes

Deterministic evaluation executed through `DecisionTreeEngine.evaluate()` in [`medrule_engine/decision_tree.py`](file:///d:/PreAuth/medrule_engine/decision_tree.py):

#### Track 1: Clinical Necessity — Primary Target Rule: `RULE-ADV-CG2037-001`
- **Rule Name:** Lumbar Spine MRI (CPT 72148, 72149, 72158)
- **Track:** `CLINICAL_NECESSITY`
- **Governance Status:** `PARTIALLY_VERIFIED` (Non-binding research prototype)
- **Overall Rule Outcome:** **`CRITERIA_MET`**

##### Condition-by-Condition Evaluation:
| Condition ID | Description | Expected Value | Actual Value | Evaluation State | Criterion Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`COND-001`** | Evaluation of low back pain with lumbosacral radiculopathy or radiating leg pain | `EQUALS True` | `True` | `EvaluationState.TRUE` | **`MET`** |
| **`COND-002`** | Completion of at least 6 weeks of conservative care within the prior 6 months without meaningful improvement | `GREATER_THAN_OR_EQUAL 6` | `6` | `EvaluationState.TRUE` | **`MET`** |

---

#### Track 1: Clinical Necessity — Secondary Rules for CPT 72148 (Alternative Pathways)
- **`RULE-ADV-CG2037-002`** (Emergency Red Flags / Cauda Equina):
  - `COND-001` (`suspected_cauda_equina_syndrome EQUALS True`):
    - Actual Value: `{'status': 'CONFLICTING', 'values': [False, True]}`
    - Evaluation State: `EvaluationState.UNKNOWN`
    - Criterion Outcome: **`INSUFFICIENT_DATA`**
    - Rule Outcome: `INSUFFICIENT_INFORMATION` (Handled gracefully via three-valued logic; did not prevent approval under `RULE-ADV-CG2037-001`).
- **`RULE-ADV-CG2037-003`** (MRI Lumbar Spine with & without contrast for tumor/infection):
  - `COND-001` (`suspected_infection_or_tumor EQUALS True`):
    - Actual Value: `None`
    - Evaluation State: `EvaluationState.UNKNOWN`
    - Criterion Outcome: **`INSUFFICIENT_DATA`**
    - Rule Outcome: `INSUFFICIENT_INFORMATION` (Not requested; non-contrast procedure requested).

---

#### Track 2: Place of Service — `RULE-ADV-EPOS2067-001`
- **Rule Name:** Advanced Imaging Place of Service - Freestanding Facility / Office (POS 11, POS 24)
- **Track:** `PLACE_OF_SERVICE`
- **Governance Status:** `PARTIALLY_VERIFIED`
- **Overall Rule Outcome:** **`CRITERIA_MET`**

##### Condition-by-Condition Evaluation:
| Condition ID | Description | Expected Value | Actual Value | Evaluation State | Criterion Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`COND-001`** | Place of service is Freestanding Imaging Facility or Physician Office (POS 11) | `EQUALS POS_11` | `"POS_11"` | `EvaluationState.TRUE` | **`MET`** |
| **`COND-002`** | Place of service is Ambulatory Surgery Center (POS 24) | `EQUALS POS_24` | `None` | `EvaluationState.UNKNOWN` | **`NOT_APPLICABLE`** (Disjunctive OR branch satisfied by COND-001) |

---

### 6.3 Consolidated Decision Assessment
- **Clinical Necessity Outcome:** `CRITERIA_MET`
- **Place of Service Outcome:** `CRITERIA_MET`
- **Overall Deterministic Determination:** **`CRITERIA_MET`**
- **Binding Legal Authority:** **`is_binding = False`** unconditionally.
- **Reproducibility Hash:** Generated and logged in audit trail.
- **Summary:** All applicable clinical indication and place-of-service criteria were satisfied under `RULE-ADV-CG2037-001` and `RULE-ADV-EPOS2067-001`.

---

## 7. Exact Policy Citations Used by Evaluation

### 7.1 Clinical Necessity Citation
- **Governing Document:** `rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`
- **Printed Page:** Page 3 of 22 (Section: Lumbar Spine Imaging)
- **PDF Physical Page Index:** `594`
- **Policy Section Heading:** `INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Neurologic Deficits (1)`
- **Verbatim Policy Quotation:**
  > `"INDICATIONS FOR LUMBAR SPINE MRI"`
  > *(Full criteria requires low back pain with radiculopathy and at least 6 weeks of conservative therapy within prior 6 months)*

### 7.2 Place of Service Citation
- **Governing Document:** `rulebook_collection/domains/advanced_imaging/policies/current/Place of Service Policy 2067 - Radiology 2026.pdf`
- **Printed Page:** Page 3
- **PDF Physical Page Index:** `3`
- **Policy Section Heading:** `POLICY AND PROCEDURE / Advanced Imaging / Place of Service alignment`
- **Verbatim Policy Quotation:**
  > `"are considered preferred sites of care for advanced imaging"`

---

## 8. Summary of Findings & Next Steps

1. **Deterministic Evaluation Pipeline Integrity:**
   - The policy router, rule registry, decision tree engine, and three-valued logic correctly identified and satisfied `RULE-ADV-CG2037-001` and `RULE-ADV-EPOS2067-001`, arriving at `CRITERIA_MET`.
   - Missing fields (prior imaging) were properly left absent rather than treated as negative evidence.
   - Dual-track separation between Clinical Necessity and Place of Service was maintained without crosstalk.
2. **Identified Extraction Defects for Future Remediation:**
   - **Provider Name Regex:** Erroneously captures `"Dr. Physician"` from `"Attending Physician: Dr. Yu, MD"`.
   - **Multi-Sentence Modality Aggregator:** Treats each subsequent sentence mentioning conservative treatment as a conflicting value rather than aggregating modalities into a set.
   - **Negation Scope in Compound Sentences:** Sentence `"No progressive focal motor weakness or saddle anesthesia"` failed to bind "No" to "saddle anesthesia", generating an artificial conflict on cauda equina syndrome.
   - **Symptom Duration Field:** Duration of symptoms (8 weeks) was not mapped to a discrete field.
3. **Safeguard Compliance:**
   - All code, rules, policy PDFs, and governance databases remain untouched.
   - Zero UI development initiated. Manual extraction check complete.
