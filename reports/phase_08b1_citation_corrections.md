# MedRule — Phase 8B.1: Citation-Only Corrections Report

**Document ID:** `MEDRULE-REPORT-PHASE-08B1`  
**Execution Date:** 2026-10-22  
**Status:** Completed & Fully Verified  
**Governing Plan:** `reports/phase_08a_remediation_plan.md`  
**Remediation Register:** `reports/phase_08a_remediation_register.json`  

---

## 1. Executive Summary & Strict Constraints Adherence

Phase 8B.1 implements the four citation-only corrections identified during Phase 8A (`REM-P4-001`, `REM-P4-002`, `REM-P3-002`, `REM-P3-011`).

### Strict Constraint Adherence
- **Citation-Only Changes:** Modifications were strictly confined to `source_page.physical_page`, `source_page.printed_page`, `source_section`, and `source_quote` in the two draft rule files. Zero clinical criteria, conditions, parameters, comparators, values, operators, decision effects, or routing dependencies were altered.
- **Zero Approved Rules Invariant:** Zero rules were approved. The active registry retains exactly 0 approved rules (`APPROVED: 0`, `DRAFT: 121`, `NEEDS_HUMAN_REVIEW: 7`).
- **Governance Gate Preservation:** All 7 existing governance gates in `GOVERNANCE_BLOCKED_RULE_IDS` remain strictly blocked from autonomous decision execution.
- **Scope Restriction:** Scope remains strictly confined to Advanced Imaging (114 rules) and Interventional Pain Management (14 rules). Historical documents and archived candidate domains were not altered.
- **Independent PDF Verification:** Every citation and verbatim quote was independently verified using PyMuPDF directly against the authoritative 2026 governing PDF documents in `policies/current/`.
- **Pre-Remediation Backup:** Pristine copies of both rule files were created at `scratch/phase8b1_backups/` before any edits were performed.

---

## 2. Itemized Citation Corrections & Authoritative Evidence

### Correction 1: `RULE-ADV-CG2009-002` (Brain CTA / Acute Stroke & LVO)
- **Remediation Register ID:** `REM-P4-001` (Priority 4 / Citation Alignment)
- **Domain:** Advanced Imaging
- **Procedure / Service:** Brain Computed Tomography Angiography (CTA) (CPT 70496)
- **Governing PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`
- **Previous Citation:**
  - `physical_page`: 176
  - `printed_page`: `"Page 5 of 20"`
  - `source_section`: `"INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Evaluation of Known Intracranial Vascular Disease (1,2)"`
  - `source_quote`: `"Evaluation of Known Intracranial Vascular Disease (1,2)"`
- **Issue Identified:** Physical page 176 governs hemorrhagic vascular conditions (subarachnoid hemorrhage, intracranial hemorrhage) and venous thrombosis. Acute ischemic stroke and Large Vessel Occlusion (LVO) mechanical thrombectomy criteria reside on physical page 175.
- **Authoritative Source Evidence (Verified via PyMuPDF):**
  - **Physical Page:** 175
  - **Printed Header:** `Page 4 of 20`
  - **Guideline Heading:** `Evolent Clinical Guideline 2009 for Brain Computed Tomography Angiography (CTA)`
  - **Section:** `INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Cerebrovascular Disease / Ischemic`
  - **Verbatim Passage:**
    > *"Cerebrovascular Disease*\
    > *Ischemic*\
    > *● Recent ischemic stroke or transient ischemic attack (See background section) (16,17)"*
  - **Reference Cross-Reference:** Reference (17) on physical page 184 (printed page 13 of 20) explicitly documents the ACR Appropriateness Criteria covering intracranial large vessel occlusion and stroke interventions.
- **Corrected Citation Encoded:**
  ```json
  "source_page": {
    "physical_page": 175,
    "printed_page": "Page 4 of 20"
  },
  "source_section": "INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Cerebrovascular Disease / Ischemic",
  "source_quote": "Recent ischemic stroke or transient ischemic attack (See background section) (16,17)"
  ```

---

### Correction 2: `RULE-ADV-CG2037-001` (Lumbar Spine MRI / Back Pain & Radiculopathy)
- **Remediation Register ID:** `REM-P4-002` (Priority 4 / Citation Alignment)
- **Domain:** Advanced Imaging
- **Procedure / Service:** Lumbar Spine MRI (CPT 72148, 72158)
- **Governing PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`
- **Previous Citation:**
  - `physical_page`: 594
  - `printed_page`: `"Page 3 of 22"`
  - `source_section`: `"INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Neurologic Deficits (1)"`
  - `source_quote`: `"INDICATIONS FOR LUMBAR SPINE MRI"`
- **Issue Identified:** Physical page 594 contains only general preamble statements and purpose declarations. The actual clinical indications for back pain, lumbosacral radiculopathy, and conservative treatment duration reside on physical page 595.
- **Authoritative Source Evidence (Verified via PyMuPDF):**
  - **Physical Page:** 595
  - **Printed Header:** `Page 4 of 22`
  - **Guideline Heading:** `Evolent Clinical Guideline 2037 for Lumbar Spine Magnetic Resonance Imaging (MRI)`
  - **Section:** `INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Back Pain (1)`
  - **Verbatim Passage:**
    > *"Evaluation of Back Pain (1)*\
    > *With any of the Following:*\
    > *● With new or worsening objective neurologic deficits on exam, as above*\
    > *● Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months:*\
    > *NOTE - Failure of conservative treatment is defined as one of the following:*\
    > *○ Lack of meaningful improvement after a full course of treatment; OR*\
    > *○ Progression or worsening of symptoms during treatment; OR...*"
- **Corrected Citation Encoded:**
  ```json
  "source_page": {
    "physical_page": 595,
    "printed_page": "Page 4 of 22"
  },
  "source_section": "INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Back Pain (1)",
  "source_quote": "Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months:"
  ```

---

### Correction 3: `RULE-IPM-CGEPIDURALINJECTIONS-002` (ESI Conservative Care Failure)
- **Remediation Register ID:** `REM-P3-002` (Priority 3 / Incomplete Criteria Citation Alignment)
- **Domain:** Interventional Pain Management
- **Procedure / Service:** Epidural Steroid Injection (ESI) (CPT 62320–62323)
- **Governing PDF:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Previous Citation:**
  - `physical_page`: 11
  - `printed_page`: `"Page 11 of 102"`
  - `source_section`: `"Epidural Spine Injections 2026 / Conservative Treatment Prerequisites"`
  - `source_quote`: `"The following two elements are required to meet conservative therapy guidelines for HEP:"`
- **Issue Identified:** Physical page 11 (printed page 8 of 13) describes modality definitions (multimodality therapy, HEP prescription rules). Furthermore, `"Page 11 of 102"` conflated the total PDF document page count with the guideline's internal pagination (`Page 8 of 13`). The clinical criteria specifying the requirement and duration of conservative treatment failure (6 weeks within the prior 6 months) reside under `INDICATIONS / Treatment Purposes` on physical page 7 (printed page 4 of 13).
- **Authoritative Source Evidence (Verified via PyMuPDF):**
  - **Physical Page:** 7 (Note: Section header `INDICATIONS` starts at bottom of physical page 6; the explicit 6-week conservative treatment criteria appear at lines 23–25 on physical page 7).
  - **Printed Header:** `Page 4 of 13`
  - **Guideline Heading:** `Evolent Clinical Guideline 1750 for Epidural Spine Injections`
  - **Section:** `Evolent Clinical Guideline 1750 for Epidural Spine Injections / INDICATIONS / Treatment Purposes`
  - **Verbatim Passage:**
    > *"● Failure to respond to non-operative conservative treatment* targeting the requested spinal region for a minimum of six (6) weeks in the last six (6) months unless the medical reason this treatment cannot be done is clearly documented*\
    > *○ Failure of conservative treatment is defined as one of the following:*\
    > *■ Lack of meaningful improvement after a full course of treatment; OR*\
    > *■ Progression or worsening of symptoms during treatment; OR...*"
- **Corrected Citation Encoded:**
  ```json
  "source_page": {
    "physical_page": 7,
    "printed_page": "Page 4 of 13"
  },
  "source_section": "Evolent Clinical Guideline 1750 for Epidural Spine Injections / INDICATIONS / Treatment Purposes",
  "source_quote": "Failure to respond to non-operative conservative treatment* targeting the requested spinal region for a minimum of six (6) weeks in the last six (6) months unless the medical reason this treatment cannot be done is clearly documented"
  ```

---

### Correction 4: `RULE-IPM-EPOS1755-002` (IPM Site of Care / Outpatient Hospital Alignment)
- **Remediation Register ID:** `REM-P3-011` (Priority 3 / Place of Service Citation Alignment)
- **Domain:** Interventional Pain Management
- **Procedure / Service:** Interventional Pain Management Site of Care (Place of Service Policy 1755)
- **Governing PDF:** `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf`
- **Previous Citation:**
  - `physical_page`: 1
  - `printed_page`: `"Page 1 of 8"`
  - `source_section`: `"Place of Service Policy Statement / Setting Alignment"`
  - `source_quote`: `"PATIENT CRITERIA FOR SELECTION OF OUTPATIENT HOSPITAL SETTING ........................................................ 3"`
- **Issue Identified:** Physical page 1 is the policy cover and table of contents; the quote cited was the table of contents entry pointing to page 3. The actual substantive patient clinical criteria for selecting an outpatient hospital setting reside on physical page 3.
- **Authoritative Source Evidence (Verified via PyMuPDF):**
  - **Physical Page:** 3
  - **Printed Header:** `Page 3 of 8`
  - **Policy Heading:** `Evolent Place of Service Policy 1755 for Interventional Pain Management`
  - **Section:** `PATIENT CRITERIA FOR SELECTION OF OUTPATIENT HOSPITAL SETTING`
  - **Verbatim Passage:**
    > *"Patient Criteria for Selection of Outpatient Hospital Setting*\
    > *In certain circumstances, a patient will qualify for care in an outpatient hospital. Outpatient hospital care will be deemed appropriate when ANY of the following criteria are met:*\
    > *NOTE: All criteria require additional documentation from the treating physician and/or primary care physician.*"
- **Corrected Citation Encoded:**
  ```json
  "source_page": {
    "physical_page": 3,
    "printed_page": "Page 3 of 8"
  },
  "source_section": "PATIENT CRITERIA FOR SELECTION OF OUTPATIENT HOSPITAL SETTING",
  "source_quote": "Patient Criteria for Selection of Outpatient Hospital Setting"
  ```

---

## 3. Exact Files Changed and Git Diff Analysis

Only two files were modified in the repository:
1. `rulebook_collection/domains/advanced_imaging/rules/draft_rules.json`
2. `rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json`

### Complete Git Diff
```diff
diff --git a/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json b/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json
index bb0c73e..1eb417e 100644
--- a/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json
+++ b/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json
@@ -1815,11 +1815,11 @@
     "source_file": "rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
     "source_url": "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf",
     "source_page": {
-      "physical_page": 176,
-      "printed_page": "Page 5 of 20"
+      "physical_page": 175,
+      "printed_page": "Page 4 of 20"
     },
-    "source_section": "INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Evaluation of Known Intracranial Vascular Disease (1,2)",
-    "source_quote": "Evaluation of Known Intracranial Vascular Disease (1,2)",
+    "source_section": "INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Cerebrovascular Disease / Ischemic",
+    "source_quote": "Recent ischemic stroke or transient ischemic attack (See background section) (16,17)",
     "clinical_service_or_procedure": "Brain CTA",
     "rule_type": "clinical_indication",
     "conditions": {
@@ -3695,11 +3695,11 @@
     "source_file": "rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
     "source_url": "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf",
     "source_page": {
-      "physical_page": 594,
-      "printed_page": "Page 3 of 22"
+      "physical_page": 595,
+      "printed_page": "Page 4 of 22"
     },
-    "source_section": "INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Neurologic Deficits (1)",
-    "source_quote": "INDICATIONS FOR LUMBAR SPINE MRI",
+    "source_section": "INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Back Pain (1)",
+    "source_quote": "Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months:",
     "clinical_service_or_procedure": "Lumbar Spine MRI",
     "rule_type": "clinical_prerequisite",
     "conditions": {
diff --git a/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json b/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json
index 1da6558..605e5ad 100644
--- a/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json
+++ b/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json
@@ -46,11 +46,11 @@
     "source_file": "rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf",
     "source_url": "https://www.evolent.com/clinical-guidelines",
     "source_page": {
-      "physical_page": 11,
-      "printed_page": "Page 11 of 102"
+      "physical_page": 7,
+      "printed_page": "Page 4 of 13"
     },
-    "source_section": "Epidural Spine Injections 2026 / Conservative Treatment Prerequisites",
-    "source_quote": "The following two elements are required to meet conservative therapy guidelines for HEP:",
+    "source_section": "Evolent Clinical Guideline 1750 for Epidural Spine Injections / INDICATIONS / Treatment Purposes",
+    "source_quote": "Failure to respond to non-operative conservative treatment* targeting the requested spinal region for a minimum of six (6) weeks in the last six (6) months unless the medical reason this treatment cannot be done is clearly documented",
     "clinical_service_or_procedure": "Epidural Steroid Injection (ESI)",
     "rule_type": "clinical_prerequisite",
     "conditions": {
@@ -449,11 +449,11 @@
     "source_file": "rulebook_collection/domains/interventional_pain_management/policies/current/EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf",
     "source_url": "https://www.evolent.com/clinical-guidelines",
     "source_page": {
-      "physical_page": 1,
-      "printed_page": "Page 1 of 8"
+      "physical_page": 3,
+      "printed_page": "Page 3 of 8"
     },
-    "source_section": "Place of Service Policy Statement / Setting Alignment",
-    "source_quote": "PATIENT CRITERIA FOR SELECTION OF OUTPATIENT HOSPITAL SETTING ........................................................ 3",
+    "source_section": "PATIENT CRITERIA FOR SELECTION OF OUTPATIENT HOSPITAL SETTING",
+    "source_quote": "Patient Criteria for Selection of Outpatient Hospital Setting",
     "clinical_service_or_procedure": "Interventional Pain Management Site of Care",
     "rule_type": "place_of_service",
     "conditions": {
```

---

## 4. Verification and Test Results

### 1. JSON Schema Conformance
- Validated all 114 Advanced Imaging rules and 14 Interventional Pain Management rules against `rulebook_collection/schemas/medrule_rule_schema.json` using `jsonschema`.
- **Result:** 100% compliant. Zero schema validation errors.

### 2. PDF Physical Page Bounds Check (`scratch/test_sources.py`)
- Verified all 128 active rules against the physical page limits of their cited PDF files:
  - `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`: 1,041 pages (p. 175 and p. 595 within bounds)
  - `2026 Evolent Interventional Pain Management Guidelines.pdf`: 102 pages (p. 7 within bounds)
  - `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf`: 8 pages (p. 3 within bounds)
- **Result:** 0 missing source files; 0 out-of-bounds citations.

### 3. Verbatim Source Passage Verification
- Executed `scratch/verify_phase8b1.py` utilizing `pymupdf` to confirm that all four quotes exist as verbatim substrings within the text of the exact cited physical pages.
  - Quote 1 (`RULE-ADV-CG2009-002`) on AI p. 175: **True**
  - Quote 2 (`RULE-ADV-CG2037-001`) on AI p. 595: **True**
  - Quote 3 (`RULE-IPM-CGEPIDURALINJECTIONS-002`) on IPM p. 7: **True**
  - Quote 4 (`RULE-IPM-EPOS1755-002`) on POS p. 3: **True**

### 4. Full Test Suite Regression (`pytest`)
- Ran complete engine and rulebook test suite (`pytest medrule_engine/tests rulebook_collection/tests -v`).
- **Result:** **208 passed in 14.95s** (100% pass rate).
- Key passed test suites include:
  - `rulebook_collection/tests/test_scope_integrity.py` (14/14 passed)
  - `medrule_engine/tests/test_phase3b_integration.py` (37/37 passed)
  - `medrule_engine/tests/test_step2_clinical_extraction_and_evaluation.py` (22/22 passed)
  - `medrule_engine/tests/test_phase4a_governance_audit.py` (6/6 passed)
  - `medrule_engine/tests/test_decision_tree.py` (15/15 passed)
  - `medrule_engine/tests/test_phase3f_end_to_end.py` (25/25 passed)

---

## 5. Governance Checks & Safety Invariants

| Governance Dimension | Requirement | Verified Result | Status |
| :--- | :--- | :--- | :---: |
| **Approved Rules Count** | Exactly 0 rules approved | `APPROVED: 0` in RuleRegistry and `governance.db` | **ENFORCED** |
| **Governance Gates** | Exactly 7 blocked rules in `GOVERNANCE_BLOCKED_RULE_IDS` | 7 blocked gates verified (`RULE-ADV-PREAMBLE-001`, `RULE-ADV-CG2000-003`, `RULE-ADV-CG2001-001`, `RULE-ADV-CG2066-001`, `RULE-ADV-CG2066-002`, `RULE-IPM-PREAMBLEIPM-001`, `RULE-IPM-CGINFUSIONPUMPS-001`) | **ENFORCED** |
| **Database Approval Records** | 0 approval records in `rule_governance_state` and `review_records` | `SELECT COUNT(*)` yields 0 | **ENFORCED** |
| **Non-Binding Evaluation** | `is_binding: false` unconditionally present | Confirmed via engine regression assertions | **ENFORCED** |
| **Domain Scope Isolation** | Only Advanced Imaging and IPM active | AI (114 rules), IPM (14 rules); zero archive leaks | **ENFORCED** |

---

## 6. Unresolved Issues & Next Steps

### Unresolved Issues
- **None.** All four target citation corrections were verified against authoritative text, applied without side effects, and verified by 208 passing regression tests.

### Next Steps
- In accordance with the prompt's instructions: **Stop after this batch. Do not begin clinical-criteria remediation until separately authorized.**
- The Phase 8B.2 clinical-criteria remediation batch will be addressed once authorized.
