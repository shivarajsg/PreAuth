# MedRule — Phase 8B.4: Tier 2 Advanced Imaging Evidence Review

**Document ID:** `MEDRULE-REPORT-PHASE-08B4-TIER2-REVIEW`  
**Date:** 2026-10-22  
**Status:** Diagnostic Evidence Review Complete (No Production Edits)  
**Governing Register Records:** `REM-P2-001`, `REM-P2-002`, `REM-P2-003` (Priority 2)  
**Governing Authority:** `2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)`  
**Target Rules Under Review:**  
1. `RULE-ADV-CG2035-002` (Lower Extremity MRI — Knee Orthopedic Signs / CPT 73721–73723)  
2. `RULE-ADV-CG2056-002` (Thoracic Spine CT — Back Pain / CPT 72128–72130)  
3. `RULE-ADV-CG2057-002` (Thoracic Spine MRI — Back Pain / CPT 72146–72147, 72157)  

---

## 1. Executive Summary & Review Scope

In accordance with Phase 8B.4 directives, an in-depth clinical and policy-fidelity review was conducted for the three Tier 2 Advanced Imaging defects identified in `reports/phase_08a_remediation_register.json` and `reports/phase_08a_remediation_plan.md`.

### Strict Operational Invariants Maintained:
- **Zero Production Edits:** Exactly 0 production rules, test suites, schemas, routing tables, databases, policy PDFs, or governance statuses were modified.
- **Zero Rules Approved:** Active registry invariant remains strictly at **0 approved rules** (`APPROVED: 0`, `DRAFT: 121`, `NEEDS_HUMAN_REVIEW: 7`).
- **Governance Gate Isolation:** All 7 canonical governance gates in `GOVERNANCE_BLOCKED_RULE_IDS` remain strictly blocked.
- **Scope Restriction:** Analysis strictly confined to Advanced Imaging Guidelines 2035, 2056, and 2057 in the governing 2026 Evolent policy.
- **Stop for Review:** This phase is diagnostic and planning-only. No implementation will begin without explicit user authorization.

---

## 2. Rule 1: `RULE-ADV-CG2035-002` (Knee MRI — Joint Specific Orthopedic Signs)

### 2.1 Identification & Scope
- **Rule ID:** `RULE-ADV-CG2035-002`
- **Register Record:** `REM-P2-001` (Priority 2 / Incorrectly Restrictive Requirements)
- **Clinical Service / Modality:** Lower Extremity Magnetic Resonance Imaging (MRI) (Knee)
- **Applicable CPT Codes:** 73721 (without contrast), 73722 (with contrast), 73723 (without & with contrast)
- **Governing Policy:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

### 2.2 Authoritative Policy Evidence
- **Physical PDF Pages:** 553–555
- **Printed Pages:** `Page 4 of 22` through `Page 6 of 22`
- **Guideline Header:** `Evolent Clinical Guideline 2035 for Lower Extremity Magnetic Resonance Imaging (MRI)`
- **Section Heading:** `INDICATIONS FOR LOWER EXTREMITY MRI / Joint Specific Orthopedic Signs`

#### Verbatim Policy Passages:

1. **The Overarching Orthopedic Sign Rule & X-Ray Footnote (Physical Page 553, Printed `Page 4 of 22`):**
   > **Joint Specific Orthopedic Signs**\
   > **NOTE: With a positive orthopedic sign from the list below, an initial X-ray is always preferred; however, it is NOT required UNLESS otherwise specified in bold below.**\
   > **NOTE: The joint specific exam testing list below is intended to be thorough but cannot possibly be all inclusive. Advanced imaging is indicated for any orthopedic exam test that clearly suggests joint instability**\
   > **Joint specific advanced imaging is indicated for any positive orthopedic sign listed below:**

2. **The Specific Knee Orthopedic Physical Exam Tests (Physical Pages 554–555):**
   - **Anterior Cruciate Ligament (ACL):** Anterior drawer test, Lachman’s test, Pivot shift test
   - **Meniscus:** Apley’s test, McMurray’s Compression test, Thessaly test
   - **Posterior Cruciate Ligament (PCL):** Posterior drawer test, Posterior tibial sag sign (Godfrey test or step-off test)
   - **Medial Collateral Ligament (MCL):** Positive valgus stress testing/laxity
   - **Lateral Collateral Ligament (LCL):** Positive varus stress testing/laxity
   - **Patellar Dislocation:** Patellofemoral apprehension test

3. **The Bold Specification Requiring Prior X-Ray (Physical Page 555, Printed `Page 6 of 22`):**
   > **● Suspected ACL Rupture - acute knee injury with physical exam limited by pain and swelling AFTER initial X-ray completed that does not show a clear etiology with any ONE of the following (13):**\
   > **○ Extreme mechanism of injury (such as twisting, blunt force)**\
   > **○ Extreme pain with inability to perform physical examination**\
   > **○ Instability to stand (bear full weight)**

4. **Ordinary Joint Pain Without Orthopedic Signs (Physical Page 553, Printed `Page 4 of 22`):**
   > **Joint Specific Pain or Suspected Joint Specific Injury**\
   > **In the absence of a positive joint specific orthopedic sign on exam (see list below)**, advanced imaging is indicated with **prior X-ray showing no clear etiology for the joint pain** with any ONE of the following:\
   > ● Persistent joint pain unresponsive to ACTIVE Conservative Therapy (ACT)... of at least four (4) weeks duration within the last 6 months\
   > ● With progression or worsening of symptoms during the course of active conservative treatment\
   > ● Pediatric patient that is either under the age of 12 years OR cannot comply with the prescribed therapy

---

### 2.3 Detailed Clinical Verification: When Initial X-Rays Are Preferred vs. Mandatory

| Clinical Scenario | Initial X-Ray Status | Policy Rationale & Supporting Citation | Current Encoded Behavior | Remediated Requirement |
| :--- | :--- | :--- | :--- | :--- |
| **A. Positive Knee Orthopedic Sign on Exam** (Lachman, McMurray, drawer, pivot shift, Thessaly, laxity) | **PREFERRED (NOT Mandatory)** | Page 553 explicitly states: *"an initial X-ray is always preferred; however, it is NOT required UNLESS otherwise specified in bold below."* High-specificity physical tests confirm mechanical derangement directly. | **FATALLY DEFECTIVE:** Enforces `prior_xray_completed == True` as a mandatory prerequisite. | **Remove mandatory X-ray requirement.** When `positive_knee_orthopedic_sign == True`, MRI qualifies without requiring prior plain film. |
| **B. Acute Knee Trauma with Physical Exam Limited by Pain/Swelling** (Suspected ACL Rupture without positive exam maneuvers) | **MANDATORY** | Page 555 explicitly specifies in bold: *"AFTER initial X-ray completed that does not show a clear etiology with any ONE of: Extreme mechanism, extreme pain with inability to examine, or inability to stand."* | **UNCODIFIED:** Current rule only checks positive exam signs; patients with unexaminable swollen knees cannot qualify under `CG2035-002`. | **Incorporate as an explicit alternative pathway:** Qualifying if acute injury with limited exam + completed negative X-ray + extreme mechanism/pain/inability to weight-bear. |
| **C. Ordinary Joint Pain / Subacute Knee Ache** (Absence of positive orthopedic signs) | **MANDATORY** | Page 553 mandates prior plain radiographs AND conservative care (>= 4 weeks ACT in prior 6 months, worsening, or pediatric < 12). | Governed by `RULE-ADV-CG2035-001` (successfully remediated in Phase 8B.3). | Preserved under `RULE-ADV-CG2035-001`. Does not qualify under `CG2035-002`. |

---

### 2.4 Current Rule Structure vs. Proposed Remediation

#### Current Encoded Rule (`draft_rules.json`):
```json
{
  "rule_id": "RULE-ADV-CG2035-002",
  "conditions": {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Physical examination demonstrates positive joint-specific sign for meniscal or ligamentous tear (e.g. McMurray test, joint line tenderness, Lachman test, anterior/posterior drawer, pivot shift)",
        "parameter": "positive_knee_orthopedic_sign",
        "comparator": "EQUALS",
        "value": true
      },
      {
        "condition_id": "COND-002",
        "description": "Prior plain radiograph completed showing no clear explanation for mechanical symptoms or acute fracture",
        "parameter": "prior_xray_completed",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
}
```

#### Proposed Remediated Rule Structure:
The rule should encompass the complete clinical intent of the policy section:
- **Operator:** `ANY_OF` across two distinct clinical pathways:
  1. **Pathway 1 (Positive Orthopedic Sign):**  
     `positive_knee_orthopedic_sign == True`  
     *(Plain X-ray is preferred but strictly NOT mandatory; conservative therapy waived).*
  2. **Pathway 2 (Acute Trauma with Limited Exam & Bold X-Ray Prerequisite):**  
     `ALL_OF`:
     - `acute_knee_injury_exam_limited_by_pain_swelling == True`
     - `prior_xray_completed == True`
     - `sub_conditions` (`ANY_OF`):
       - `extreme_mechanism_of_injury == True`
       - `inability_to_perform_physical_exam == True`
       - `inability_to_bear_full_weight == True`

#### Disagreement Analysis Against Phase 8A Register:
- The Phase 8A register (`REM-P2-001`) proposed simply stripping `COND-002` (`prior_xray_completed`), leaving only `positive_knee_orthopedic_sign == True`.
- *Finding:* While stripping `prior_xray_completed` resolves the false-denial defect for patients with positive exam signs, the Phase 8A register completely overlooked the bold exception on page 555 for acute knee injuries where physical exam is precluded by severe pain and swelling.
- *Recommendation:* If `RULE-ADV-CG2035-002` is titled `Joint Specific Orthopedic Signs`, separating the bold exception or incorporating it via an `ANY_OF` structure ensures complete policy fidelity without creating coverage gaps.

---

### 2.5 Risk Analysis: False Denials vs. False Approvals

- **False Denial Risk of Current Logic (High):**  
  Athletes and trauma patients presenting to orthopedic clinics with torn ACLs (screaming positive Lachman) or locked bucket-handle meniscal tears (positive McMurray) are currently denied prior authorization if an X-ray was not performed, in direct defiance of the explicit policy footnote.
- **False Approval Risk of Proposed Logic (None):**  
  Orthopedic maneuvers (Lachman test, pivot shift, Thessaly) have documented clinical specificity exceeding 90–95% for ligamentous and meniscal rupture. Approving knee MRI without preliminary plain films when physical exam confirms structural instability represents standard evidence-based orthopedic practice recognized by the policy.

---

## 3. Rules 2 & 3: `RULE-ADV-CG2056-002` (Thoracic CT) & `RULE-ADV-CG2057-002` (Thoracic MRI)

### 3.1 Identification & Scope
- **Rule IDs:**
  - `RULE-ADV-CG2056-002` (Thoracic Spine CT)
  - `RULE-ADV-CG2057-002` (Thoracic Spine MRI)
- **Register Records:** `REM-P2-002` & `REM-P2-003` (Priority 2 / Conflated Requirements & Thresholds)
- **Applicable CPT Codes:**
  - CT: 72128 (without contrast), 72129 (with contrast), 72130 (without & with contrast)
  - MRI: 72146 (without contrast), 72147 (with contrast), 72157 (without & with contrast)
- **Governing Policy:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

### 3.2 Authoritative Policy Evidence
- **Physical PDF Pages:**
  - CT: Physical page 906 (`Page 4 of 20`)
  - MRI: Physical page 926 (`Page 4 of 23`)
- **Section Headings:**
  - CT: `INDICATIONS FOR THORACIC SPINE CT / Evaluation of Back Pain (1)`
  - MRI: `INDICATIONS FOR THORACIC SPINE MRI / Evaluation of Back Pain (1)`

#### Verbatim Policy Passages:

1. **Adult Thoracic Back Pain Criteria (Physical Page 906 & 926):**
   > **Evaluation of Back Pain (1)**\
   > **With any of the following [when Thoracic Spine MRI is Contraindicated for CT]:**\
   > ● With new or worsening objective neurologic deficits on exam, as above\
   > ● **Failure of conservative treatment\* for a minimum of six (6) weeks within the last six (6) months:**\
   >   **NOTE - Failure of conservative treatment is defined as one of the following:**\
   >   **○ Lack of meaningful improvement after a full course of treatment; OR**\
   >   **○ Progression or worsening of symptoms during treatment; OR**\
   >   **○ Documentation of a medical reason the member is unable to participate in treatment**\
   >   *Closure of medical or therapy offices, patient inconvenience, or noncompliance without explanation does not constitute “inability to complete” treatment.*\
   > ● With progression or worsening of symptoms during the course of conservative treatment\*\
   > ● With an abnormal electromyography (EMG) or nerve conduction study (if performed) indicating a thoracic radiculopathy. (4,5)

2. **Pediatric Thoracic Back Pain Red-Flag Pathway (Physical Page 906 & 926):**
   > **● Isolated back pain in pediatric population when at least ONE of the following red flags are present (6,7) (Note: conservative care not required if red flags are present)**\
   > **○ Age 5 or younger**\
   > **○ Constant pain**\
   > **○ Pain lasting > 4 weeks**\
   > **○ Abnormal neurologic examination**\
   > **○ Early morning stiffness and/or gelling**\
   > **○ Night pain that prevents or disrupts sleep**\
   > **○ Radicular pain**\
   > **○ Fever, weight loss, malaise**\
   > **○ Postural changes (e.g., kyphosis or scoliosis)**\
   > **○ Limp (or refusal to walk in a younger child)**

---

### 3.3 Root-Cause Analysis of the Conflation Defect

A side-by-side comparison reveals how the current draft rules became severely corrupted:

```
[Authoritative Policy Text]
├── Adult Back Pain: Minimum of SIX (6) WEEKS conservative treatment within last 6 months.
└── Pediatric Back Pain: Red flags (including "Pain lasting > 4 weeks") EXCLUDE conservative care!

[Corrupted Current Draft Rule Logic]
├── Cites: "Pain lasting > 4 weeks" (plucked from pediatric red-flag sub-bullet)
├── Imposes: thoracic_pain_duration_weeks > 4 (invented prerequisite for adults)
└── Requires: "4-6 weeks conservative management" (invented compromised threshold)
```

#### Detailed Breakdown of the Conflation:
1. **The Adult Threshold Defect:**
   - The authoritative policy explicitly mandates a **minimum of six (6) weeks** of conservative treatment within the prior six months.
   - The current draft rules encode a vague description of `"4-6 weeks"`. In programmatic evaluation, accepting 4 or 5 weeks of conservative therapy creates **false approvals** for adult thoracic spine scans that have not completed the required 6-week trial.
2. **The Adult Pain Duration Defect:**
   - The current rules require `thoracic_pain_duration_weeks > 4` as a standalone prerequisite in addition to conservative care.
   - The policy does *not* require adults to prove pain duration > 4 weeks if they have completed 6 weeks of conservative therapy. This parameter was lifted entirely from the pediatric red-flag list.
3. **The Pediatric Red-Flag Defect (Severe Clinical Safety Hazard):**
   - In pediatric patients (under age 18), isolated back pain with pain lasting > 4 weeks (or age <= 5, constant pain, night pain, scoliosis, etc.) represents a major red flag for spondylolysis, discitis, osteomyelitis, or spinal cord tumor.
   - The policy explicitly commands: **`(Note: conservative care not required if red flags are present)`**.
   - By conflating the pediatric red flag into the adult conservative care rule, the current draft rule **forces pediatric patients with red-flag symptoms to undergo 4–6 weeks of physical therapy before approving MRI or CT**, creating catastrophic diagnostic delays and risking permanent neurologic harm.

---

### 3.4 Disagreement Analysis Against Phase 8A Register

| Dimension | Phase 8A Register Proposal (`REM-P2-002` / `REM-P2-003`) | Authoritative 2026 Evolent Policy Fact | Required Resolution |
| :--- | :--- | :--- | :--- |
| **Adult Duration Threshold** | Update duration threshold to `>= 6 weeks within prior 6 months`. | Fully aligned: Page 906 and 926 mandate a minimum of 6 weeks within the last 6 months. | Adopt `thoracic_conservative_therapy_weeks >= 6`. |
| **Recency Window** | Explicitly supported (within last 6 months). | Fully aligned: Page 906 and 926 state *"within the last six (6) months"*. | Enforce the 6-month recency window. |
| **Adult Exceptions to 6 Weeks** | Not codified in Phase 8A criteria spec. | Policy explicitly excuses 6 weeks if: (1) progression/worsening during care, (2) documented medical inability, or (3) abnormal EMG/NCS radiculopathy. | Codify conservative care failure alternatives under `ANY_OF`. |
| **Pediatric Red-Flag Separation** | Mentioned in "exceptions" narrative, but **omitted from the proposed criteria spec**. | Policy dedicates a major standalone clinical pathway: pediatric back pain with any of 10 red flags **waives conservative care entirely**. | **Critical Disagreement:** The proposed minimal correction in Phase 8A is incomplete. The rule must explicitly support the pediatric red-flag pathway without conservative care. |

---

### 3.5 Proposed Logical Structure for Remediation

To faithfully reflect the authoritative policy, `RULE-ADV-CG2056-002` and `RULE-ADV-CG2057-002` must be structured as dual-track clinical indications:

#### For Thoracic Spine MRI (`RULE-ADV-CG2057-002`):
- **Operator:** `ANY_OF`
  1. **Pathway A (Adult Thoracic Back Pain with Failed Conservative Care):**
     `ALL_OF`:
     - `patient_age_years >= 18`
     - `thoracic_back_pain_present == True`
     - `sub_conditions` (`ANY_OF`):
       - `thoracic_conservative_therapy_duration_weeks >= 6`
       - `conservative_treatment_worsening == True`
       - `medical_contraindication_to_conservative_therapy == True`
       - `abnormal_emg_ncs_thoracic_radiculopathy == True`
  2. **Pathway B (Pediatric Thoracic Back Pain with Red Flags — Conservative Care Waived):**
     `ALL_OF`:
     - `patient_age_years < 18`
     - `thoracic_back_pain_present == True`
     - `sub_conditions` (`ANY_OF`):
       - `patient_age_years <= 5`
       - `constant_thoracic_pain == True`
       - `thoracic_pain_duration_weeks > 4`
       - `abnormal_neurologic_exam == True`
       - `morning_stiffness_or_gelling == True`
       - `night_pain_disrupting_sleep == True`
       - `radicular_pain_present == True`
       - `constitutional_symptoms_fever_weight_loss == True`
       - `postural_changes_kyphosis_scoliosis == True`
       - `gait_abnormality_or_limp == True`

#### For Thoracic Spine CT (`RULE-ADV-CG2056-002`):
- Exactly identical to `RULE-ADV-CG2057-002`, with the additional mandatory cumulative prerequisite:
  - `thoracic_mri_contraindicated == True`

---

### 3.6 Risk Analysis: False Denials vs. False Approvals

- **Adult False Approval Risk:**  
  Current logic allows approvals at 4 weeks of PT. Raising the threshold to strictly `>= 6 weeks` within the last 6 months eliminates improper adult authorizations.
- **Adult False Denial Risk:**  
  Incorporating the policy-supported exceptions (progression/worsening during care, medical inability to participate, and abnormal EMG radiculopathy) guarantees that deteriorating adult patients are not denied imaging.
- **Pediatric False Denial Risk (Critical Clinical Hazard Eliminated):**  
  Decoupling the pediatric red-flag pathway ensures that children with prolonged pain (> 4 weeks), constant pain, or systemic signs receive immediate imaging without being subjected to unnecessary, potentially harmful conservative physical therapy delays.

---

## 4. Comprehensive Testing & Boundary Specification Plan

When implementation is authorized, the following comprehensive test matrices must be created in a dedicated test suite (e.g., `test_phase8b4_tier2_rules.py`):

### A. Test Cases for `RULE-ADV-CG2035-002` (Knee MRI Orthopedic Signs)

| Test Case ID | Clinical Scenario & Inputs | Key Parameters | Expected Outcome |
| :--- | :--- | :--- | :--- |
| `TC-CG2035-002-PASS-NO-XRAY` | Acute ACL tear: Positive Lachman test, **no X-ray completed** | `positive_knee_orthopedic_sign: True` | `CRITERIA_MET` |
| `TC-CG2035-002-PASS-WITH-XRAY` | Meniscal tear: Positive McMurray test, completed negative X-ray | `positive_knee_orthopedic_sign: True`, `prior_xray_completed: True` | `CRITERIA_MET` |
| `TC-CG2035-002-PASS-DRAWER` | PCL tear: Positive posterior drawer and tibial sag | `positive_knee_orthopedic_sign: True` | `CRITERIA_MET` |
| `TC-CG2035-002-PASS-THESSALY` | Meniscal tear: Positive Thessaly test | `positive_knee_orthopedic_sign: True` | `CRITERIA_MET` |
| `TC-CG2035-002-FAIL-NORMAL-EXAM` | Non-specific ache: Lachman negative, McMurray negative, joint stable | `positive_knee_orthopedic_sign: False` | `CRITERIA_NOT_MET` |
| `TC-CG2035-002-PEND-MISSING-EXAM` | Knee pain noted: Orthopedic physical maneuvers omitted from records | *(Omitted)* | `INSUFFICIENT_INFORMATION` |
| `TC-CG2035-002-PASS-ACUTE-ACL-SWOLLEN` | Acute trauma, exam precluded by swelling, X-ray negative, extreme twisting | `exam_limited_by_swelling: True`, `prior_xray_completed: True`, `extreme_mechanism: True` | `CRITERIA_MET` |
| `TC-CG2035-002-FAIL-ACUTE-ACL-NO-XRAY` | Acute trauma, exam precluded by swelling, **no X-ray performed** | `exam_limited_by_swelling: True`, `prior_xray_completed: False` | `CRITERIA_NOT_MET` |
| `TC-CG2035-002-ROUTING-CG2035-001` | Normal exam signs route to ordinary pain rule requiring 4w ACT and X-ray | `positive_knee_orthopedic_sign: False` | Evaluates under `CG2035-001` |

---

### B. Test Cases for `RULE-ADV-CG2056-002` (CT) & `RULE-ADV-CG2057-002` (MRI)

| Test Case ID | Target Rule | Clinical Scenario & Inputs | Key Parameters | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| `TC-THOR-ADULT-5WKS-FAIL` | MRI / CT | Adult age 45, thoracic back pain, 5 weeks completed physical therapy | `age: 45`, `therapy_weeks: 5` | `CRITERIA_NOT_MET` (Below 6w threshold) |
| `TC-THOR-ADULT-6WKS-PASS` | MRI | Adult age 45, thoracic back pain, exactly 6.0 weeks physical therapy | `age: 45`, `therapy_weeks: 6` | `CRITERIA_MET` (Exact threshold) |
| `TC-THOR-ADULT-8WKS-PASS` | MRI | Adult age 50, thoracic back pain, 8 weeks physical therapy | `age: 50`, `therapy_weeks: 8` | `CRITERIA_MET` (Above threshold) |
| `TC-THOR-ADULT-WORSEN-PASS` | MRI | Adult age 35, 2 weeks therapy with documented neurological worsening | `age: 35`, `therapy_weeks: 2`, `worsening: True` | `CRITERIA_MET` (Exception met) |
| `TC-THOR-ADULT-EMG-PASS` | MRI | Adult age 40, thoracic pain with abnormal EMG radiculopathy | `age: 40`, `abnormal_emg: True` | `CRITERIA_MET` (Exception met) |
| `TC-THOR-PEDS-PAIN-4WKS-PASS` | MRI | Pediatric age 12, isolated back pain lasting > 4 weeks, **0 weeks PT** | `age: 12`, `pain_weeks: 5`, `therapy_weeks: 0` | `CRITERIA_MET` (Red flag waives PT) |
| `TC-THOR-PEDS-AGE-4-PASS` | MRI | Pediatric age 4 (age <= 5), thoracic back pain, **0 weeks PT** | `age: 4`, `therapy_weeks: 0` | `CRITERIA_MET` (Red flag waives PT) |
| `TC-THOR-PEDS-NIGHT-PAIN-PASS` | MRI | Pediatric age 14, night pain waking from sleep, **0 weeks PT** | `age: 14`, `night_pain: True`, `therapy_weeks: 0` | `CRITERIA_MET` (Red flag waives PT) |
| `TC-THOR-PEDS-UNCOMP-FAIL` | MRI | Pediatric age 14, uncomplicated back pain 2 weeks, no red flags, no PT | `age: 14`, `pain_weeks: 2`, `therapy_weeks: 0` | `CRITERIA_NOT_MET` (No red flag) |
| `TC-THOR-ADULT-PAIN-4WKS-FAIL` | MRI | Adult age 30, back pain > 4 weeks, **no conservative care** | `age: 30`, `pain_weeks: 5`, `therapy_weeks: 0` | `CRITERIA_NOT_MET` (Adult requires 6w) |
| `TC-THOR-AGE-18-BOUNDARY` | MRI | Age 18 with pain > 4 weeks, no conservative care | `age: 18`, `pain_weeks: 5`, `therapy_weeks: 0` | `CRITERIA_NOT_MET` (Adult boundary) |
| `TC-THOR-AGE-17-BOUNDARY` | MRI | Age 17 with pain > 4 weeks, no conservative care | `age: 17`, `pain_weeks: 5`, `therapy_weeks: 0` | `CRITERIA_MET` (Pediatric boundary) |
| `TC-THOR-CT-PASS-MRI-CONTRA` | CT | Adult age 55, 6 weeks PT, MRI contraindicated (pacemaker) | `therapy_weeks: 6`, `mri_contra: True` | `CRITERIA_MET` |
| `TC-THOR-CT-FAIL-NO-CONTRA` | CT | Adult age 55, 6 weeks PT, MRI **not contraindicated** | `therapy_weeks: 6`, `mri_contra: False` | `CRITERIA_NOT_MET` (MRI is primary) |
| `TC-THOR-CT-PEND-MISSING-CONTRA`| CT | Adult age 55, 6 weeks PT, MRI contraindication unstated | `therapy_weeks: 6` | `INSUFFICIENT_INFORMATION` |

---

## 5. Summary Table: Current vs. Proposed Policy Criteria

| Rule ID | Clinical Service | Current Encoded Logic | Authoritative Policy Requirement | Proposed Remediation Summary |
| :--- | :--- | :--- | :--- | :--- |
| **`RULE-ADV-CG2035-002`** | Lower Extremity MRI (Knee) | `positive_knee_orthopedic_sign == True` **AND** `prior_xray_completed == True` | Physical p. 553: Plain X-ray is preferred, but **NOT required** for positive orthopedic exam signs. Mandatory X-ray applies only to suspected ACL rupture when physical exam is limited by swelling/pain (p. 555) or ordinary joint pain (p. 553). | **Remove mandatory X-ray prerequisite** from the positive orthopedic signs pathway. Optionally encode the unexaminable acute trauma ACL pathway as an explicit alternative. |
| **`RULE-ADV-CG2056-002`** | Thoracic Spine CT | `thoracic_pain_duration_weeks > 4` **AND** `conservative_therapy_completed == True` (4–6 weeks) **AND** `thoracic_mri_contraindicated == True` | Physical p. 906: Adult back pain requires **minimum of 6 weeks conservative therapy within prior 6 months** (or worsening, or abnormal EMG) + MRI contraindicated. Pediatric back pain with red flags (including pain > 4 weeks) **waives conservative care entirely**. | **Decouple adult and pediatric pathways.** Enforce adult 6-week minimum within 6 months. Codify pediatric red flags as an explicit alternative waiving conservative care. Enforce MRI contraindication. |
| **`RULE-ADV-CG2057-002`** | Thoracic Spine MRI | `thoracic_pain_duration_weeks > 4` **AND** `conservative_therapy_completed == True` (4–6 weeks) | Physical p. 926: Adult back pain requires **minimum of 6 weeks conservative therapy within prior 6 months** (or worsening, or abnormal EMG). Pediatric back pain with red flags (including pain > 4 weeks) **waives conservative care entirely**. | **Decouple adult and pediatric pathways.** Enforce adult 6-week minimum within 6 months. Codify pediatric red flags as an explicit alternative waiving conservative care. |

---

## 6. Phase Review Gate & Explicit Confirmation

- **Files Modified:** Exactly 0 production code, rule definitions, databases, schemas, routing tables, or tests modified.
- **Approved Rules:** Exactly 0 approved rules in `RuleRegistry` and `governance.db`.
- **Governance Gates:** All 7 rules in `GOVERNANCE_BLOCKED_RULE_IDS` remain strictly blocked.
- **Scope Intact:** Active domains remain strictly limited to Advanced Imaging (114 rules) and Interventional Pain Management (14 rules).

**Phase 8B.4 diagnostic evidence review is complete. Execution has halted. Awaiting user authorization before initiating implementation.**
