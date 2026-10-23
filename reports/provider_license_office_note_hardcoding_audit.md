# MedRule Audit Report: Investigation of Potential Hardcoded Documentation Evidence

## 1. Executive Summary & Objective

An end-to-end investigation was conducted into MedRule's PDF extraction, case evidence construction, rule evaluation engine, and Case History / Case Detail UI rendering. The goal was to determine whether the backend hardcoded or defaulted the evidence/status for `"ordering_provider_license"` and `"clinical_office_notes"`, causing these requirements to appear universally as `MET` across uploaded clinical PDFs.

### Audit Verdict: **Hardcoding Defect Confirmed and Remediated**
The investigation confirmed that the backend **did hardcode** `"ordering_provider_license": True` whenever any provider name was detected in a PDF, and defaulted `"clinical_office_notes": True` based on loose sentence keywords. In addition, a Jinja2 template scoping defect in `case_detail.html` and a fallback promoting any non-None value to `MET` caused the UI to mask underlying evidence states and display misleading `MET` badges.

Both criteria have now been refactored to enforce strict three-valued evidence semantics, structural document validation, case isolation, and accurate UI rendering.

---

## 2. Root Cause & Exact Code Locations

### Root Cause 1: Hardcoded Ordering Provider Licensure
- **File**: `medrule_engine/integrations/pdf_extractor.py` (formerly lines 621–626)
- **Defect**: The extractor executed:
  ```python
  # Former code:
  if prov_name:
      record_fact("ordering_provider_name", prov_name, prov_snippet)
      # Hardcoded fact: any doctor name was assumed to be an active verified license
      record_fact("ordering_provider_license", True, prov_snippet)
  ```
- **Impact**: Any PDF with a clinician name (e.g., "KEWEI YU, MD") automatically asserted `ordering_provider_license = True`, bypassing actual license verification.

### Root Cause 2: Loose & Unstructured Office Note Defaulting
- **File**: `medrule_engine/integrations/pdf_extractor.py` (formerly lines 641–651)
- **Defect**: Sentence-by-sentence keyword matching marked `clinical_office_notes = True` if any isolated sentence contained loose terms like `"consultation"`, `"follow up"`, `"pre-certification"`, or `"hpi"`, without verifying document structure, date of service, clinical exam, or provider signature.
- **Impact**: Even non-clinical or administrative documents containing those words were defaulted to qualifying office visit notes.

### Root Cause 3: Template Scoping & UI Fallback Promotion
- **File**: `medrule_engine/web/templates/case_detail.html` (formerly lines 358–363 & line 416)
- **Defect**:
  1. `{% set has_val = false %}` declared outside `{% for cr in crits %}` could not be updated by an inner `{% set has_val = true %}` due to Jinja2 block scoping. As a result, evaluated rules with `UNKNOWN` status (such as `RULE-ADV-CG2037-001` containing conflicting radiculopathy evidence) were skipped from the Clinical Documentation Review table, leaving only `CG2000-001`.
  2. Line 416 contained:
     ```jinja2
     {% elif act_val is not none %}
         {% set final_stat = 'MET' %}
     ```
     This coerced any non-None value (even `0`, `False`, or unverified text) into a `MET` badge in the UI.

### Root Cause 4: Provider Specialty & Facility Mock Defaults
- **File**: `medrule_engine/integrations/pdf_extractor.py` (`_detect_provider_details`)
- **Defect**: Defaulted missing provider specialty to `"Spine & Orthopedics"` and facility to `"Specialty Outpatient Clinic"`.
- **Impact**: Replaced real data gaps with fictional defaults.

---

## 3. Correct Evidence Semantics Applied

1. **Provider Licensure Distinction**:
   - A provider name is **not** proof of verified licensure.
   - Provider name (`ordering_provider_name`), credentials (`ordering_provider_credentials`), license number (`ordering_provider_license_number`), and verified license status (`ordering_provider_license`) are now strictly distinct fields.
   - `ordering_provider_license` is **only** asserted as `True` when explicit active verified licensure text is present in the record (e.g. `"State Medical License: Active Verified"`).
   - If a license number is present (e.g. `"GAA-NP000612"` or `"MD-12345"`) but unverified, `ordering_provider_license_number` is recorded while `ordering_provider_license` remains `None` (`INSUFFICIENT_DATA`), rendering as neutral `NOT PROVIDED`.

2. **Qualifying Office Visit Note Structure**:
   - Implemented `_is_qualifying_office_visit_note(text)`.
   - Requires four distinct structural components:
     1. Encounter header/type (consultation note, progress note, clinic visit note).
     2. Encounter Date / Date of Service (supports ISO `YYYY-MM-DD` and standard `MM/DD/YYYY`).
     3. Clinical substance: at least 2 of History/HPI, Physical Exam/Vitals, Assessment/Plan.
     4. Documented provider identification / signature.
   - Pure administrative documents (billing invoices, fee sheets, insurance denial notices) are explicitly disqualified.

3. **Three-Valued Logic & Human Review**:
   - Missing evidence remains `INSUFFICIENT_DATA` / `UNKNOWN`.
   - Missing evidence is never coerced to `MET` and is never falsely marked `NOT_MET`.
   - Conflicting clinical statements (e.g. positive SLR on exam vs ICD-10 M47.816 without radiculopathy) are recorded as `CONFLICTING` and flagged for human clinical review (`NEEDS REVIEW`).

4. **Case Isolation**:
   - All extracted facts are scoped strictly to per-call dictionaries; no global caches or mutable module defaults exist.

---

## 4. Before-and-After Comparison Across Test Documents

| Document | Pre-Remediation Behavior | Post-Remediation Behavior | Status Correctness |
| :--- | :--- | :--- | :--- |
| **`DrYuNotesForMRIPre-certificationA.pdf`**<br>(DOS: 2025-02-26, Provider: Haiyan Wang, Signer: KEWEI YU, MD, GAA-NP000612) | - Ordering Provider License: `MET` (hardcoded)<br>- Recent Office Visit Note: `MET` (loose keyword)<br>- Table: Only `CG2000-001` shown; conflict hidden | - Ordering Provider License: `NOT PROVIDED` (unverified; license `GAA-NP000612` & credentials `MD` captured)<br>- Recent Office Visit Note: `MET` (qualifying note verified)<br>- Radiculopathy: `NEEDS REVIEW` (Conflicting SLR vs M47.816) | **CORRECT** |
| **`Dr-Yu-NeurologyDoctorNotesD.pdf`**<br>(DOS: 2025-01-09, Provider: KEWEI YU, MD, Signer: KEWEI YU, MD) | - Ordering Provider License: `MET` (hardcoded)<br>- Recent Office Visit Note: `MET` (loose keyword)<br>- Table: Only `CG2000-001` shown | - Ordering Provider License: `NOT PROVIDED` (unverified; credentials `MD` captured, no license number)<br>- Recent Office Visit Note: `MET` (qualifying note verified)<br>- PT Duration: `INSUFFICIENT_DATA` / `NOT PROVIDED` (0 wks) | **CORRECT** |
| **Negative Fixture: Anonymous Record**<br>(No provider information in text) | - Ordering Provider License: `NOT PROVIDED` (unmatched) | - Provider Name: `None`<br>- Provider License: `NOT PROVIDED` (absent) | **CORRECT** |
| **Negative Fixture: Billing Invoice / Denial**<br>(Pure billing statement / denial notice) | - Recent Office Visit Note: `MET` (if "invoice" or "denial" sentence matched loose keyword) | - Recent Office Visit Note: `NOT PROVIDED` (disqualified as non-clinical administrative document) | **CORRECT** |
| **Positive Fixture: Verified Licensure**<br>(Explicit "State Medical License: Active Verified") | - Ordering Provider License: `MET` | - Ordering Provider License: `MET` (supported by explicit provenance: `"State Medical License: Active Verified"`) | **CORRECT** |

---

## 5. Files Changed & Summary of Modifications

1. [pdf_extractor.py](file:///d:/PreAuth/medrule_engine/integrations/pdf_extractor.py):
   - Removed hardcoded `ordering_provider_license = True` from `prov_name` detection.
   - Added `_detect_provider_name_and_provenance` with horizontal-only whitespace (`[^\S\r\n]+`) and electronic signature support.
   - Added `_detect_provider_license_evidence` extracting credentials, license number, and verified status separately.
   - Added `_is_qualifying_office_visit_note` enforcing structural document validation and rejecting billing/denial forms.
   - Updated `_detect_provider_details` to return empty defaults rather than hardcoded `"Spine & Orthopedics"` and `"Specialty Outpatient Clinic"`.
   - Updated `conservative_therapy` denial regex to detect `"denies completing physical therapy"` and `"zero conservative treatment"`.
   - Fixed duplicate NSAID regex matching for Meloxicam.
   - Injected `"ordering_provider": provider_info` into `extracted_fields`.

2. [case_validator.py](file:///d:/PreAuth/medrule_engine/case_validator.py):
   - In `CaseIntake.get_evidence("ordering_provider_license")`, safely checked `self.ordering_provider.get("is_licensed")` when non-None.

3. [case_detail.html](file:///d:/PreAuth/medrule_engine/web/templates/case_detail.html):
   - Fixed Jinja2 variable scoping by introducing `val_ns = namespace(has_val=false)`.
   - Included rules with `UNKNOWN` status that contain extracted values or conflicts into the Clinical Documentation Review table.
   - Corrected `final_stat` status mapping: `UNKNOWN` and `INSUFFICIENT_DATA` evaluate to `NOT PROVIDED`, preventing unverified actual values from being coerced to `MET`.

4. [test_pdf_extractor.py](file:///d:/PreAuth/medrule_engine/tests/test_pdf_extractor.py):
   - Updated synthetic Dr. Yu test fixture to include verified license text and matching 2026 DOS.

5. [test_provider_license_office_notes.py](file:///d:/PreAuth/medrule_engine/tests/test_provider_license_office_notes.py):
   - Created comprehensive 9-test regression suite covering unverified license, verified license, absent provider, qualifying office note, non-qualifying billing/denial note, three-valued logic, multi-case variance, cross-case isolation, and UI table status rendering.

---

## 6. Test Suite Verification Results

- **Focused Regression Suite**:
  ```
  pytest medrule_engine/tests/test_provider_license_office_notes.py
  ====== 9 passed in 3.71s ======
  ```
- **Full Existing Regression Suite**:
  ```
  pytest medrule_engine/tests/
  ====== 410 passed in 51.65s ======
  ```
  **Zero failures across all 410 unit, integration, pilot, benchmark, and acceptance tests.**

---

## 7. Remaining Limitations Requiring Policy or Clinical Review

1. **External Licensure Verification Integration**:
   - The system evaluates licensure evidence based solely on text present within the uploaded document. To verify licenses for clinical notes lacking explicit `"State Medical License: Active Verified"` text, an outbound connector to state medical board APIs or NPPES/NPI registry would be required. (Currently, outbound submission adapters and live network calls are intentionally disabled per safety invariants).
2. **Historical Date of Service Policy Context**:
   - Dates of service prior to 2026-01-01 evaluate to `POLICY_VERSION_UNRESOLVED` under 2026 governing guidelines unless the intake payload includes `policy_context={"allow_historical_evaluation": True}`. A clinical policy decision is required on whether past-year DOS submissions should automatically route to historical guidelines or prompt for reviewer confirmation.
3. **Clinical Judgment for Contradictory Clinical Findings**:
   - Documents noting positive physical examination findings (e.g. straight leg raise positive, radicular pain) paired with conflicting diagnosis codes (e.g. M47.816 spondylosis without radiculopathy) are flagged as `NEEDS REVIEW`. This escalation requires physician reviewer evaluation and cannot be deterministically resolved by software alone.
