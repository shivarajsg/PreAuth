# MedRule — Phase 8B.2: Tier 1 Advanced Imaging Evidence Review

**Document ID:** `MEDRULE-REPORT-PHASE-08B2-REVIEW`  
**Review Date:** 2026-10-22  
**Status:** Stage A & B Completed (Diagnostic Evidence Review Only — No Production Edits)  
**Governing Register:** `reports/phase_08a_remediation_register.json`  
**Governing Plan:** `reports/phase_08a_remediation_plan.md`  
**Governing Authority:** `2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)`  

---

## 1. Executive Summary & Review Scope

In accordance with Phase 8B.2 instructions, this report provides a comprehensive, source-grounded evidence validation of the seven Tier 1 Advanced Imaging policy-fidelity defects identified in `reports/phase_08a_remediation_register.json`.

### Strict Operational Invariants Preserved
- **Zero Production Edits:** No production rules, logic, schemas, routing tables, test suites, or database records were modified during this phase.
- **Zero Approved Rules:** Active registry invariant remains strictly at **0 approved rules** (`APPROVED: 0`, `DRAFT: 121`, `NEEDS_HUMAN_REVIEW: 7`).
- **Governance Gate Isolation:** All 7 existing governance gates in `GOVERNANCE_BLOCKED_RULE_IDS` remain strictly blocked from autonomous execution.
- **Domain Scope:** Scope remains strictly restricted to Advanced Imaging and Interventional Pain Management.
- **Stop for Review Gate:** This phase concludes at Stage B. Implementation will not commence until explicit user authorization is granted.

---

## 2. Comprehensive Rule-by-Rule Evidence Dossiers

---

### Rule 1: `RULE-ADV-CG2054-001` (Sella CT / Pituitary Mass)

#### 1. Identification
- **Rule ID:** `RULE-ADV-CG2054-001`
- **Register Record ID:** `REM-P1-001` (Priority 1 / Missing Prerequisites)
- **Clinical Service / Modality:** Temporal Bone, Mastoid, Orbits, Sella, Internal Auditory Canal Computed Tomography (CT)
- **Applicable CPT Code:** 70480 (CT Sella / Pituitary)
- **Governing Policy PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

#### 2. Authoritative Source Evidence
- **Physical PDF Page:** 881
- **Printed Page:** `Page 4 of 17`
- **Guideline Header:** `Evolent Clinical Guideline 2054 for Temporal Bone, Mastoid, Orbits, Sella, Internal Auditory Canal Computed Tomography (CT)`
- **Section Heading:** `INDICATIONS FOR SELLA CT / Sella CT (9)`
- **Verbatim Policy Passage (Physical Page 881):**
  > **INDICATIONS FOR SELLA CT**\
  > **Sella CT (9)**\
  > **When MRI is contraindicated or cannot be performed:**\
  > ● For further evaluation of known sellar and/or parasellar masses\
  > ● Suspected pituitary gland disorder based on any ONE of the following:\
  >   ○ Documented visual field defect suggesting compression of the optic chiasm\
  >   ○ Laboratory findings suggesting pituitary dysfunction (such as abnormal levels of prolactin, growth hormone, cortisol, testosterone, oxytocin, TSH, ACTH, LH, FSH, ADH)\
  >   ○ Pituitary apoplexy (sudden loss of pituitary function often due ischemia or hemorrhage) with acute onset of neurological and hormonal symptoms\
  >   ○ Prior imaging suggesting sella (pituitary) mass

#### 3. Current Rule Definition
- **Rule Type:** `clinical_indication`
- **Current Operator:** `ALL_OF`
- **Current Conditions:**
  ```json
  {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Known sellar, suprasellar, or parasellar mass requiring bony evaluation of sella turcica or surgical planning",
        "parameter": "sellar_or_parasellar_mass",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
  ```
- **Current Citation:** Physical page 881, Printed page `Page 4 of 17`, Section `INDICATIONS FOR SELLA CT`, Quote: `"For further evaluation of known sellar and/or parasellar masses"`.

#### 4. Clinical Logic Gap & Risk Analysis
- **Current Flaw:** The encoded rule approves Sella CT solely if `sellar_or_parasellar_mass == True`, omitting the mandatory governing header condition: `"When MRI is contraindicated or cannot be performed:"`.
- **False Approval Risk (High):** Brain/Pituitary MRI is the undisputed clinical gold standard for sellar and parasellar soft-tissue evaluation. CT exposes the patient (and the radiosensitive ocular lens) to ionizing radiation while offering inferior soft-tissue contrast. Approving primary CT without verifying that MRI is medically contraindicated or unavailable violates medical necessity standards.
- **False Denial Risk (Low):** Patients with documented MRI contraindications (e.g., non-conditional pacemakers, metallic orbital fragments, severe claustrophobia, or body dimensions exceeding scanner limits) are approved cleanly.

#### 5. Policy-Supported Requirements & Structural Logic
- **Explicit Requirements:** Presence of a sellar/parasellar mass **AND** (MRI is contraindicated **OR** MRI cannot be performed).
- **Logical Connective:** Conjunction (`ALL_OF`) between the lesion finding and the modality prerequisite.

#### 6. Proposed Logic Specification
- **Operator:** `ALL_OF`
- **Criteria:**
  1. `sellar_or_parasellar_mass == True`
  2. `mri_contraindicated_or_unavailable == True` (or `mri_contraindicated == True`)
- **Missing Information Behavior:** `PEND_FOR_DOCUMENTATION`. If MRI contraindication status is unstated, evaluation returns `INSUFFICIENT_INFORMATION`.

#### 7. Discrepancies & Field Analysis
- **Phase 8A Text Discrepancy:** The Phase 8A register narrative mentioned `(Guideline 2056, physical p. 881)`. Guideline 2056 is Thoracic Spine MRI. The physical header on page 881 is `Evolent Clinical Guideline 2054 for Temporal Bone, Mastoid, Orbits, Sella, Internal Auditory Canal Computed Tomography (CT)`. The guideline number is 2054, matching `RULE-ADV-CG2054-001`.
- **Field Availability:** `mri_contraindicated` already exists in `draft_rules.json` (used in lower extremity and spine rules).

---

### Rule 2: `RULE-ADV-CG2062-001` (Upper Extremity CT / Joint Pain)

#### 1. Identification
- **Rule ID:** `RULE-ADV-CG2062-001`
- **Register Record ID:** `REM-P1-002` (Priority 1 / Missing Prerequisites)
- **Clinical Service / Modality:** Upper Extremity Computed Tomography (CT) (Shoulder, Elbow, Wrist, Hand)
- **Applicable CPT Codes:** 73200, 73201, 73202
- **Governing Policy PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

#### 2. Authoritative Source Evidence
- **Physical PDF Pages:** 965–966
- **Printed Pages:** `Page 3 of 24` and `Page 4 of 24`
- **Guideline Header:** `Evolent Clinical Guideline 2062 for Upper Extremity Computed Tomography (CT)`
- **Section Headings:**
  - `Special Notes` (p. 965)
  - `INDICATIONS FOR UPPER EXTREMITY CT (SHOULDER, ELBOW, OR WRIST) / Upper Extremity Pain (1,2)` (p. 965)
  - `Non-specific Upper Extremity Pain` (p. 966)
  - `Joint Specific Pain or Suspected Joint Specific Injury` (p. 966)
- **Verbatim Policy Passages:**
  - *Physical Page 965 (`Page 3 of 24`):*
    > `● X-rays must precede CT evaluation, unless otherwise indicated`\
    > `● Some indications are for magnetic resonance imaging (MRI), CT, or MR or CT Arthrogram (more than one should not be approved at the same time)`\
    > `● If a CT Arthrogram fits approvable criteria below, approve as CT`\
    > `● When specifically indicated below, MRI is the preferred study for the evaluation of the extremities and CT is indicated only when MRI is contraindicated or cannot be performed`
  - *Physical Page 966 (`Page 4 of 24`):*
    > `Non-specific Upper Extremity Pain`\
    > `If MRI is contraindicated or cannot be performed, or requested as a CT arthrogram`\
    > `Upper extremity pain with no specific joint identified with prior X-ray showing no clear etiology of joint/extremity pain with any ONE of the following:`\
    > `● Persistent joint or musculotendinous upper extremity pain unresponsive to ACTIVE Conservative Therapy (ACT) which includes physical therapy, chiropractic treatments, and/or physician supervised Home Exercise Program (HEP) of at least four (4) weeks duration within the last 6 months`\
    > `● With progression or worsening of symptoms during the course of active conservative treatment`\
    > `● Pediatric patient that is either under the age of 12 years OR cannot comply with the prescribed therapy`\
    > `Joint Specific Pain or Suspected Joint Specific Injury`\
    > `If MRI is contraindicated or cannot be performed, or requested as a CT arthrogram`\
    > `In the absence of a positive joint specific orthopedic sign on exam (see list below), advanced imaging is indicated with prior X-ray showing no clear etiology for the joint pain with any ONE of the following: [same 3 bullets]`

#### 3. Current Rule Definition
- **Rule Type:** `clinical_prerequisite`
- **Current Operator:** `ALL_OF`
- **Current Conditions:**
  ```json
  {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Upper extremity plain X-ray completed showing no definitive diagnostic etiology for joint/extremity pain",
        "parameter": "prior_xray_negative_or_inconclusive",
        "comparator": "EQUALS",
        "value": true
      },
      {
        "condition_id": "COND-002",
        "description": "Persistent pain unresponsive to at least 4 weeks of active conservative therapy, OR acute complex fracture/arthrogram planning",
        "parameter": "conservative_therapy_or_bony_injury",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
  ```

#### 4. Clinical Logic Gap & Risk Analysis
- **Current Flaw:** The rule checks for a negative prior X-ray and conservative therapy, but completely omits the mandatory prerequisite: `"If MRI is contraindicated or cannot be performed, or requested as a CT arthrogram"`.
- **False Approval Risk (High):** Upper extremity joint pain (rotator cuff tear, labral detachment, TFCC injury) is routinely approved for diagnostic CT without requiring that MRI be contraindicated or that the procedure be ordered as an arthrogram.
- **False Denial Risk (Low):** Patients with MRI contraindications or orders for CT arthrography are approved.

#### 5. Policy-Supported Requirements & Structural Logic
- Cumulative requirements:
  1. Prior completed X-ray showing no clear etiology.
  2. Conservative therapy failure (>= 4 weeks in prior 6 months) OR documented clinical progression/worsening OR pediatric < 12 yrs.
  3. Modality prerequisite: (MRI contraindicated **OR** MRI cannot be performed **OR** requested as CT arthrogram).

#### 6. Proposed Logic Specification
- **Operator:** `ALL_OF`
- **Criteria:**
  1. `prior_xray_negative_or_inconclusive == True`
  2. `conservative_therapy_or_bony_injury == True` (retained or aligned with 4-week active therapy)
  3. `mri_contraindicated_or_ct_arthrogram == True` (evaluating whether MRI is contraindicated/cannot be performed OR request is for CT arthrogram)

#### 7. Discrepancies & Field Analysis
- **Page Citation Refinement:** The header condition `"If MRI is contraindicated or cannot be performed, or requested as a CT arthrogram"` and the conservative therapy details appear on **physical page 966 (`Page 4 of 24`)**, while page 965 contains general Special Notes. The citation should cite physical page 966.
- **Field Availability:** `mri_contraindicated` is an established field. To cleanly support the arthrogram exception, `mri_contraindicated_or_ct_arthrogram` or a disjunction between `mri_contraindicated` and `requested_as_ct_arthrogram` must be supported.

---

### Rule 3: `RULE-ADV-CG2055-001` (Temporomandibular Joint MRI / Internal Derangement)

#### 1. Identification
- **Rule ID:** `RULE-ADV-CG2055-001`
- **Register Record ID:** `REM-P1-003` (Priority 1 / Missing Prerequisites)
- **Clinical Service / Modality:** Temporomandibular Joint (TMJ) Magnetic Resonance Imaging (MRI)
- **Applicable CPT Code:** 70336
- **Governing Policy PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

#### 2. Authoritative Source Evidence
- **Physical PDF Page:** 896
- **Printed Page:** `Page 2 of 8`
- **Guideline Header:** `Evolent Clinical Guideline 2055 for Temporomandibular Joint (TMJ) Magnetic Resonance Imaging (MRI)`
- **Section Heading:** `INDICATIONS FOR TEMPOROMANDIBULAR JOINT (TMJ) MRI / Evaluation of Temporomandibular Disorders (TMD) (1) / Suspected Internal TMJ Derangement`
- **Verbatim Policy Passage (Physical Page 896):**
  > **Suspected Internal TMJ Derangement**\
  > ● Persistent symptoms of facial or jaw pain, restricted range of motion, pain and/or noise with TMJ function (i.e., chewing) (2–4) **AND**\
  > ● Conservative therapy with a trial of pharmacotherapy* **AND** behavioral modification** has been unsuccessful for at least four (4) weeks\
  > *\*Pharmacotherapy typically includes analgesics, anti-inflammatories (NSAIDs), and/or muscle relaxants. In chronic cases, antidepressants and benzodiazepines may be used.*\
  > *\*\*Behavioral modification may include patient education, self-care, cognitive behavior therapy, physical therapy, and/or occlusal devices*

#### 3. Current Rule Definition
- **Rule Type:** `clinical_indication`
- **Current Operator:** `ALL_OF`
- **Current Conditions:**
  ```json
  {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Suspected internal derangement of the temporomandibular joint with mechanical locking, persistent pain, or limitation of mouth opening",
        "parameter": "suspected_tmj_internal_derangement",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
  ```

#### 4. Clinical Logic Gap & Risk Analysis
- **Current Flaw:** The rule checks only for symptoms of internal derangement (`suspected_tmj_internal_derangement == True`), omitting the required prerequisite trial of conservative therapy.
- **False Approval Risk (High):** High false-approval rate for acute or self-limiting TMJ pain. TMJ disorders frequently resolve with initial non-invasive measures (NSAIDs, soft diet, warm compresses, night guards). Approving MRI without conservative treatment leads to premature high-cost imaging.
- **False Denial Risk (Low):** Patients with refractory symptoms who completed 4 weeks of medications and behavioral modification are approved.

#### 5. Policy-Supported Requirements & Structural Logic
- Cumulative requirements:
  1. Symptoms of internal derangement (facial/jaw pain, restricted ROM, noise with chewing).
  2. Conservative therapy failure for at least four (4) weeks.
  3. Conservative care must include **both** pharmacotherapy (NSAIDs, muscle relaxants, analgesics) **and** behavioral modification (soft diet, jaw rest, PT, occlusal splint).

#### 6. Proposed Logic Specification
- **Operator:** `ALL_OF`
- **Criteria:**
  1. `suspected_tmj_internal_derangement == True`
  2. `tmj_conservative_therapy_duration_weeks >= 4` (or `tmj_conservative_therapy_unsuccessful == True`)

#### 7. Discrepancies & Field Analysis
- **Critical Policy Text Discrepancy:** The Phase 8A register proposed adding `"for at least 4 weeks within the prior 6 months without meaningful improvement"`. The authoritative PDF text on physical page 896 literally states:
  > `"Conservative therapy with a trial of pharmacotherapy* AND behavioral modification** has been unsuccessful for at least four (4) weeks"`
  It **does NOT specify a 6-month recency window**. Unlike extremity and spine guidelines (CG2032, CG2035, CG2037), Guideline 2055 has no "in the last 6 months" requirement. In accordance with strict instructions not to invent requirements, the 6-month window must NOT be imposed on TMJ MRI.

---

### Rule 4: `RULE-ADV-CG2032-001` (Lower Extremity CT / Non-Specific Pain)

#### 1. Identification
- **Rule ID:** `RULE-ADV-CG2032-001`
- **Register Record ID:** `REM-P1-004` (Priority 1 / Missing Prerequisites)
- **Clinical Service / Modality:** Lower Extremity Computed Tomography (CT) (Hip, Knee, Ankle, Foot)
- **Applicable CPT Codes:** 73700, 73701, 73702
- **Governing Policy PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

#### 2. Authoritative Source Evidence
- **Physical PDF Page:** 504
- **Printed Page:** `Page 4 of 23`
- **Guideline Header:** `Evolent Clinical Guideline 2032 for Lower Extremity Computed Tomography (CT)`
- **Section Heading:** `INDICATIONS FOR LOWER EXTREMITY CT / Non-specific Lower Extremity Pain (1,2)`
- **Verbatim Policy Passage (Physical Page 504):**
  > **Non-specific Lower Extremity Pain (1,2)**\
  > Lower extremity pain with no specific joint identified with MRI contraindicated or cannot be performed **AND** with prior X-ray showing no clear etiology of extremity pain with **any ONE** of the following:\
  > ● Persistent musculotendinous lower extremity pain unresponsive to **ACTIVE Conservative Therapy (ACT)** which includes physical therapy, chiropractic treatments, and/or physician supervised Home Exercise Program (HEP) of **at least four (4) weeks duration within the last 6 months**\
  > ● With **progression or worsening of symptoms** during the course of active conservative treatment\
  > ● Pediatric patient that is either **under the age of 12 years OR cannot comply** with the prescribed therapy

#### 3. Current Rule Definition
- **Rule Type:** `conditional_modality_selection`
- **Current Operator:** `ALL_OF`
- **Current Conditions:**
  ```json
  {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Lower extremity pain without specific localized joint involvement",
        "parameter": "non_specific_lower_extremity_pain",
        "comparator": "EQUALS",
        "value": true
      },
      {
        "condition_id": "COND-002",
        "description": "Prior plain radiographs (X-ray) completed of the symptomatic region",
        "parameter": "prior_xray_completed",
        "comparator": "EQUALS",
        "value": true
      },
      {
        "condition_id": "COND-003",
        "description": "MRI is medically contraindicated or cannot be performed",
        "parameter": "mri_contraindicated",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
  ```

#### 4. Clinical Logic Gap & Risk Analysis
- **Current Flaw:** Evaluates symptom, prior X-ray, and MRI contraindication, but completely omits the conservative therapy trial requirement.
- **False Approval Risk (High):** Approves CT for non-specific lower extremity pain immediately upon establishing that an X-ray was taken and MRI is contraindicated, bypassing the required 4-week trial of physical therapy or supervised HEP.
- **False Denial Risk (Low):** Preserves access when 4 weeks of therapy, clinical worsening during care, or pediatric status (< 12 years) is documented.

#### 5. Policy-Supported Requirements & Structural Logic
- Cumulative structure:
  1. Non-specific lower extremity pain (`non_specific_lower_extremity_pain == True`).
  2. Prior completed X-ray showing no clear etiology (`prior_xray_completed == True`).
  3. MRI contraindicated or cannot be performed (`mri_contraindicated == True`).
  4. **Any ONE of three alternative clinical pathways:**
     - Unresponsive to active conservative therapy >= 4 weeks within the last 6 months, OR
     - Progression or worsening during conservative therapy, OR
     - Pediatric patient (< 12 years or unable to comply).

#### 6. Proposed Logic Specification
- **Operator:** `ALL_OF`
- **Criteria:**
  1. `non_specific_lower_extremity_pain == True`
  2. `prior_xray_completed == True`
  3. `mri_contraindicated == True`
  4. `lower_extremity_conservative_therapy_met == True` (evaluating >= 4 weeks ACT in prior 6 months OR clinical worsening OR age < 12)

#### 7. Discrepancies & Field Analysis
- **Alternative Pathways:** Phase 8A register proposed a single numeric criterion: `lower_extremity_conservative_therapy_weeks >= 4`. However, the policy explicitly includes two alternative exceptions: symptom worsening during care and pediatric age < 12. A Boolean compound parameter (`lower_extremity_conservative_therapy_met`) or explicit sub-clause prevents false denials of pediatric patients or deteriorating cases.

---

### Rule 5: `RULE-ADV-CG2035-001` (Lower Extremity MRI / Joint Pain)

#### 1. Identification
- **Rule ID:** `RULE-ADV-CG2035-001`
- **Register Record ID:** `REM-P1-005` (Priority 1 / Missing Prerequisites)
- **Clinical Service / Modality:** Lower Extremity Magnetic Resonance Imaging (MRI) (Knee, Hip, Ankle, Foot)
- **Applicable CPT Codes:** 73718, 73719, 73720, 73721, 73722, 73723
- **Governing Policy PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

#### 2. Authoritative Source Evidence
- **Physical PDF Pages:** 553–555
- **Printed Pages:** `Page 4 of 22` through `Page 6 of 22`
- **Guideline Header:** `Evolent Clinical Guideline 2035 for Lower Extremity Magnetic Resonance Imaging (MRI)`
- **Section Heading:** `INDICATIONS FOR LOWER EXTREMITY MRI / Joint Specific Pain or Suspected Joint Specific Injury` (p. 553)
- **Verbatim Policy Passage (Physical Page 553):**
  > **Joint Specific Pain or Suspected Joint Specific Injury**\
  > **In the absence of a positive joint specific orthopedic sign on exam (see list below)**, advanced imaging is indicated with **prior X-ray showing no clear etiology for the joint pain** with **any ONE** of the following:\
  > ● Persistent joint pain unresponsive to **ACTIVE Conservative Therapy (ACT)** which includes physical therapy, chiropractic treatments, and/or physician supervised Home Exercise Program (HEP) of **at least four (4) weeks duration within the last 6 months**\
  > ● With **progression or worsening of symptoms** during the course of active conservative treatment\
  > ● Pediatric patient that is either **under the age of 12 years OR cannot comply** with the prescribed therapy
- *Distinction from Joint Specific Orthopedic Signs (Physical Page 553):*
  > `Joint Specific Orthopedic Signs`\
  > `NOTE: With a positive orthopedic sign from the list below, an initial X-ray is always preferred; however, it is NOT required UNLESS otherwise specified in bold below.`\
  > `NOTE: The joint specific exam testing list below is intended to be thorough but cannot possibly be all inclusive. Advanced imaging is indicated for any orthopedic exam test that clearly suggests joint instability`\
  > `Joint specific advanced imaging is indicated for any positive orthopedic sign listed below: [Lachman, McMurray, Anterior Drawer, Pivot Shift, etc.]`

#### 3. Current Rule Definition
- **Rule Type:** `clinical_indication`
- **Current Operator:** `ALL_OF`
- **Current Conditions:**
  ```json
  {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Evaluation of joint-specific pain, mechanical locking, instability, or suspected internal derangement (ligament/meniscal tear)",
        "parameter": "joint_specific_injury_or_pain",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
  ```

#### 4. Clinical Logic Gap & Risk Analysis
- **Current Flaw:** Approves knee, hip, ankle, and foot MRI based solely on `joint_specific_injury_or_pain == True`, omitting both prior plain radiograph completion and conservative therapy requirements.
- **False Approval Risk (Severe):** CPT 73721 (Knee MRI) is one of the highest-volume imaging codes in clinical practice. Approving lower extremity joint MRI upon symptom check alone causes widespread false approvals for uncomplicated knee and ankle sprains before standard plain radiographs or 4 weeks of physical therapy are performed.
- **False Denial Risk (Low):** Patients with plain X-rays and 4 weeks of therapy (or clinical worsening) are approved. Furthermore, patients with acute joint instability or positive orthopedic exam signs qualify under `RULE-ADV-CG2035-002` without conservative therapy.

#### 5. Policy-Supported Requirements & Structural Logic
- For patients **without a positive joint-specific orthopedic sign**:
  1. Joint-specific pain present (`joint_specific_injury_or_pain == True`).
  2. Prior completed X-ray showing no clear etiology (`prior_xray_completed == True`).
  3. **Any ONE of:**
     - Failure of >= 4 weeks active conservative therapy in the last 6 months, OR
     - Progression or worsening during therapy, OR
     - Pediatric < 12 years or unable to comply.
- **Inter-Rule Relationship:** If a positive orthopedic sign (Lachman, McMurray, drawer, pivot shift, laxity) is present, the patient is adjudicated under `RULE-ADV-CG2035-002`, where conservative care is not required.

#### 6. Proposed Logic Specification
- **Operator:** `ALL_OF`
- **Criteria:**
  1. `joint_specific_injury_or_pain == True`
  2. `prior_xray_completed == True`
  3. `lower_extremity_conservative_therapy_met == True` (evaluating >= 4 weeks ACT in prior 6 months OR clinical worsening OR pediatric)

#### 7. Discrepancies & Field Analysis
- **Acute Locking Terminology:** Phase 8A register proposed `conservative_therapy_or_acute_locking`. The actual policy text on page 553 structures the requirement as prior X-ray AND (4 weeks conservative care OR progression/worsening OR pediatric). Mechanical signs indicating joint instability qualify directly under the positive orthopedic sign list on physical pages 554–555 (`RULE-ADV-CG2035-002`).

---

### Rule 6: `RULE-ADV-CG2030-001` (LDCT Lung Cancer Screening)

#### 1. Identification
- **Rule ID:** `RULE-ADV-CG2030-001`
- **Register Record ID:** `REM-P1-006` (Priority 1 / Missing Prerequisites)
- **Clinical Service / Modality:** Low Dose Computed Tomography (LDCT) for Lung Cancer Screening
- **Applicable CPT Code:** 71271
- **Governing Policy PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

#### 2. Authoritative Source Evidence
- **Physical PDF Pages:** 490–491
- **Printed Pages:** `Page 2 of 8` and `Page 3 of 8`
- **Guideline Header:** `Evolent Clinical Guideline 2030 for Low Dose Computed Tomography (CT) for Lung Cancer Screening`
- **Section Heading:** `INDICATIONS / For Annual Screening / Group 1 - High Risk for Lung Cancer (3,4)`
- **Verbatim Policy Passage (Physical Page 490):**
  > **INDICATIONS**\
  > **For Annual Screening**\
  > The use of low-dose, non-contrast spiral (helical) multi-detector CT imaging as a screening technique for lung cancer is considered **medically necessary ONLY when used to screen for lung cancer for certain high-risk, asymptomatic individuals (i.e., no acute lung-related symptoms, when ALL of the following criteria are met)**\
  > **NOTE: Screening should be discontinued once a person develops a health problem that limits the willingness or ability to have curative intent treatment. (2)**\
  > **Group 1 - High Risk for Lung Cancer (3,4)**\
  > ● Individual is between 50-80 years of age*; **AND**\
  > ● There is at least a 20 pack-year history of cigarette** smoking\
  > *\*May approve for individuals over the age limit if the individual is a candidate for and willing to undergo curative treatment upon diagnosis.*\
  > *\*\* Only personal cigarette smoking history as above places an individual at high risk; secondhand smoke exposure and other forms of smoking (such as pipe, cigar, marijuana, vaping) do NOT factor into current recommendations for LDCT Screening.*

#### 3. Current Rule Definition
- **Rule Type:** `clinical_indication`
- **Current Operator:** `ALL_OF`
- **Current Conditions:**
  ```json
  {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Patient age is between 50 and 80 years old",
        "parameter": "patient_age_years",
        "comparator": "BETWEEN",
        "value": [50, 80],
        "unit": "years"
      },
      {
        "condition_id": "COND-002",
        "description": "Documented smoking history of at least 20 pack-years",
        "parameter": "smoking_history_pack_years",
        "comparator": "GREATER_THAN_OR_EQUAL",
        "value": 20,
        "unit": "pack_years"
      },
      {
        "condition_id": "COND-003",
        "description": "Patient is currently smoking or has quit smoking within the past 15 years",
        "parameter": "current_or_recent_smoker_15yr",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
  ```

#### 4. Clinical Logic Gap & Risk Analysis
- **Current Flaw:** Evaluates age 50–80, >= 20 pack-years, and current/recent smoking, but completely omits the mandatory prerequisite restriction that the individual must be **asymptomatic**.
- **False Approval Risk (Severe Patient Safety Hazard):** If a symptomatic smoker presenting with hemoptysis, persistent cough, or unexplained weight loss is evaluated, this rule inappropriately approves a screening low-dose non-contrast CT (CPT 71271). In clinical practice, symptomatic patients require a Diagnostic Chest CT with IV contrast (CPT 71260, Guideline 2018) to evaluate for central obstructing tumors, vascular involvement, and mediastinal staging. Approving screening LDCT for a symptomatic patient risks diagnostic inadequacy and delay in appropriate care.
- **False Denial Risk (Low):** Asymptomatic high-risk screening candidates meeting USPSTF/CMS criteria approve cleanly.

#### 5. Policy-Supported Requirements & Structural Logic
- Cumulative requirements:
  1. Patient is asymptomatic (no acute lung-related signs or symptoms: `patient_is_asymptomatic == True`).
  2. Age 50 to 80 years (`patient_age_years BETWEEN [50, 80]`).
  3. Cigarette smoking history >= 20 pack-years (`smoking_history_pack_years >= 20`).
  4. Currently smoking or quit within past 15 years (`current_or_recent_smoker_15yr == True`).

#### 6. Proposed Logic Specification
- **Operator:** `ALL_OF`
- **Criteria:**
  1. `patient_is_asymptomatic == True`
  2. `patient_age_years BETWEEN [50, 80]`
  3. `smoking_history_pack_years >= 20`
  4. `current_or_recent_smoker_15yr == True`

#### 7. Discrepancies & Field Analysis
- **Field Availability:** `patient_is_asymptomatic` is an established parameter across the MedRule codebase.
- **Regression Test Impact:** `medrule_engine/tests/test_decision_tree.py` (`test_07_numerical_and_temporal_boundary_values`) tests boundary values for `RULE-ADV-CG2030-001` (19, 20, and 25 pack-years). The test fixture currently omits `patient_is_asymptomatic: True`. When `patient_is_asymptomatic` is added to the rule, `test_decision_tree.py` must include `patient_is_asymptomatic: True` in the test case; otherwise, evaluation will return `INSUFFICIENT_INFORMATION`.

---

### Rule 7: `RULE-ADV-CG2024-001` (Quantitative CT / Bone Density Study)

#### 1. Identification
- **Rule ID:** `RULE-ADV-CG2024-001`
- **Register Record ID:** `REM-P1-007` (Priority 1 / Missing Prerequisites)
- **Clinical Service / Modality:** Quantitative Computed Tomography (QCT) Bone Density Study
- **Applicable CPT Code:** 77078
- **Governing Policy PDF:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`

#### 2. Authoritative Source Evidence
- **Physical PDF Pages:** 451–452
- **Printed Pages:** `Page 2 of 11` and `Page 3 of 11`
- **Guideline Header:** `Evolent Clinical Guideline 2024 for Computed Tomography (CT) Bone Density Study`
- **Section Headings:**
  - `INDICATIONS FOR CT BONE DENSITY STUDY (QUANTITATIVE CT (QCT))` (p. 451)
  - `Screening for Asymptomatic Low Bone Mineral Density (BMD) (1)` (p. 451)
  - `Suspected Low Bone Mineral Density (Osteopenia or Osteoporosis) (1–3)` (p. 452)
- **Verbatim Policy Passages (Physical Pages 451–452):**
  > **INDICATIONS FOR CT BONE DENSITY STUDY (QUANTITATIVE CT (QCT))**\
  > `NOTE: Dual x-ray absorptiometry (DXA)... is the gold standard initial study for measuring bone mineral density (BMD). A CT Bone density Study (Quantitative CT (QCT)) is an enhanced technique that is indicated to measure BMD when DXA is expected to be insufficient OR is not available. Indications are the same for QCT as DXA; however, DXA is recommended as the first-line test in most cases as it requires less radiation exposure and is less expensive.`\
  > **Screening for Asymptomatic Low Bone Mineral Density (BMD) (1)**\
  > `A CT bone density study (Quantitative CT (QCT)) is indicated for screening for asymptomatic low BMD after meeting any ONE of the following general criteria:`\
  > `● Dual x-ray absorptiometry (DXA)... scanning is insufficient OR not available`\
  > `● Patients with advanced degenerative changes of the spine (may falsely elevate bone marrow density measurements)`\
  > `● Severe obesity (BMI > 35 kg/m2) (may limit the accuracy of DXA scans)`\
  > `● After meeting any one of the general criteria above, a CT bone density study (QCT) is indicated for any ONE of the following clinical criteria for asymptomatic screening:`\
  > `  ○ Women ≥ 65 years of age`\
  > `  ○ Men ≥ 70 years of age`\
  > **Suspected Low Bone Mineral Density (Osteopenia or Osteoporosis) (1–3)**\
  > `A CT bone density study (Quantitative CT (QCT)) is indicated for suspected osteopenia or osteoporosis after meeting any ONE of the following general criteria:`\
  > `● Dual x-ray absorptiometry (DXA)... scanning is insufficient OR not available`\
  > `● Patients with advanced degenerative changes of the spine`\
  > `● Severe obesity (BMI > 35 kg/m2)`\
  > `● After meeting any one of the general criteria above, a CT bone density study (QCT) is indicated for any ONE of the clinical criteria associated with increased risk...`

#### 3. Current Rule Definition
- **Rule Type:** `clinical_indication`
- **Current Operator:** `ALL_OF`
- **Current Conditions:**
  ```json
  {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Screening or diagnostic assessment of low bone mineral density (osteopenia or osteoporosis)",
        "parameter": "suspected_low_bone_mineral_density",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  }
  ```

#### 4. Clinical Logic Gap & Risk Analysis
- **Current Flaw:** Evaluates only `suspected_low_bone_mineral_density == True`, omitting both the mandatory general prerequisites and the clinical age/risk criteria.
- **False Approval Risk (High):** Approves QCT (which delivers substantial radiation dose) for any patient with suspected osteopenia/osteoporosis without verifying that standard first-line DXA is insufficient, unavailable, or impeded by BMI > 35 or spinal degenerative changes.
- **False Denial Risk (Low):** If any one of the three general prerequisites is documented, the patient qualifies.

#### 5. Critical Policy Constraint Regarding Alternatives
- **Strict Non-Collapsing Rule:** The prompt explicitly mandates:
  > *"QCT eligibility alternatives; do not collapse policy alternatives into a stricter requirement than the source supports."*
- The source policy establishes **three disjunctive alternatives** as general prerequisites:
  - **Alternative A:** DXA is expected to be insufficient OR is not available; **OR**
  - **Alternative B:** Advanced degenerative changes of the spine; **OR**
  - **Alternative C:** Severe obesity (BMI > 35 kg/m2).
- Meeting **ANY ONE** of these three alternatives fulfills the general prerequisite. An implementation that required all three, or that required DXA unavailability even when BMI > 35 or spine degeneration is present, would violate policy fidelity.

#### 6. Proposed Logic Specification
- **Operator:** `ALL_OF`
- **Criteria:**
  1. Low bone mineral density assessment: `suspected_low_bone_mineral_density == True`
  2. General prerequisite fulfilled via any of the 3 alternatives: `qct_general_prerequisite_met == True` (satisfiable by DXA unavailable, spinal degeneration, OR BMI > 35).

#### 7. Discrepancies & Field Analysis
- **Scope Alignment:** Guideline 2024 uses identical general prerequisites for both asymptomatic screening (p. 451) and suspected osteoporosis (p. 452). `RULE-ADV-CG2024-001` correctly captures the shared general prerequisite structure.

---

## 3. Special Attention Focus Areas Synthesis

| Focus Area | Governing Policy Requirement | Critical Policy Nuance | Proposed Implementation Guardrail |
| :--- | :--- | :--- | :--- |
| **1. MRI Contraindication / Unavailability & CT Arthrogram Alternatives** | Required for Sella CT (`CG2054-001`), Upper Extremity CT (`CG2062-001`), and Lower Extremity CT (`CG2032-001`). | For extremity CT, CT is approvable if MRI is contraindicated/cannot be performed **OR** if specifically requested as a CT arthrogram. | Must recognize `requested_as_ct_arthrogram == True` as an equal valid pathway alongside MRI contraindication. |
| **2. TMJ Conservative Care & Time Windows** | TMJ MRI (`CG2055-001`) requires failure of at least 4 weeks of conservative care. | Conservative care must include **both** pharmacotherapy (NSAIDs, analgesics) **and** behavioral modification (diet, rest, splint). **No 6-month recency window is specified in the policy.** | Reject Phase 8A's artificial 6-month window proposal; enforce 4 weeks dual-modality trial only. |
| **3. Lower Extremity Conservative Care & Time Windows** | Lower Extremity CT (`CG2032-001`) and Lower Extremity MRI (`CG2035-001`) require >= 4 weeks active conservative care within the last 6 months. | Both guidelines explicitly allow two alternative exceptions: (1) progression or worsening during care, and (2) pediatric age < 12 years. | Do not require 4 weeks if clinical worsening during therapy or pediatric age < 12 is documented. |
| **4. Lower Extremity MRI X-Ray Requirements & Exceptions** | Lower Extremity MRI (`CG2035-001`) requires prior plain X-ray in the absence of a positive orthopedic sign. | If a **positive joint-specific orthopedic sign** is present (Lachman, McMurray, drawer, pivot shift), initial X-ray is preferred but **NOT required**, and conservative care is not required. | Harmonize with `RULE-ADV-CG2035-002`; ensure `CG2035-001` applies to joint pain in the absence of positive instability signs. |
| **5. Asymptomatic LDCT Screening vs. Diagnostic Chest CT** | LDCT (`CG2030-001`) is medically necessary **ONLY** for asymptomatic individuals. | Symptomatic patients (cough, hemoptysis, weight loss) require Diagnostic Chest CT with contrast (`CG2018`). | Enforce `patient_is_asymptomatic == True`. Update `test_decision_tree.py` test fixtures to prevent false test failures. |
| **6. QCT Bone Density Eligibility Alternatives** | QCT (`CG2024-001`) requires meeting **any ONE** general prerequisite. | Three distinct alternatives: (1) DXA insufficient/unavailable, (2) advanced spine degeneration, (3) BMI > 35 kg/m2. | **Do not collapse alternatives into a conjunction.** Meeting any single alternative satisfies the general prerequisite. |

---

## 4. Test Suite Impact & Regression Verification Plan

A complete audit of the test suite was conducted to identify any existing tests referencing these seven rules:

1. **`medrule_engine/tests/test_decision_tree.py` (Line 250):**
   - Contains `test_07_numerical_and_temporal_boundary_values` testing `RULE-ADV-CG2030-001` with smoking pack-years (19, 20, 25).
   - *Impact:* The current test case fixture (`base_ldct_case`) does not include `"patient_is_asymptomatic": True`. When criteria remediation is authorized, `"patient_is_asymptomatic": True` must be added to `base_ldct_case` so the 20 and 25 pack-year assertions continue to evaluate to `CRITERIA_MET` instead of `INSUFFICIENT_INFORMATION`.
2. **`medrule_engine/tests/test_phase3b_integration.py` (Line 524 & 544):**
   - Contains `test_knee_mri_routes_knee_rules`, which asserts that knee rules (`RULE-ADV-CG2035-001`, `-002`, `-003`) are selected for CPT 73721 and evaluate to `NOT EvaluationState.TRUE` when only lumbar radiculopathy is present.
   - *Impact:* Stricter criteria on `RULE-ADV-CG2035-001` (adding X-ray and conservative care) will continue to pass this test cleanly.
3. **Other Five Rules:**
   - `RULE-ADV-CG2054-001`, `RULE-ADV-CG2062-001`, `RULE-ADV-CG2055-001`, `RULE-ADV-CG2032-001`, and `RULE-ADV-CG2024-001` are not explicitly targeted by name in unit tests, ensuring zero negative test regressions upon logic remediation. New positive, negative, and missing-evidence test fixtures will be constructed as part of implementation.

---

## 5. Stage B Review Gate & Explicit Confirmation

### Operational Confirmation
- **Files Modified:** Exactly 0 files modified in `medrule_engine/` or `rulebook_collection/`.
- **Approved Rules:** Exactly 0 approved rules in `RuleRegistry` and `governance.db`.
- **Governance Gates:** All 7 rules in `GOVERNANCE_BLOCKED_RULE_IDS` remain strictly blocked.
- **Active Scope:** Advanced Imaging (114 rules) and Interventional Pain Management (14 rules) only.

**Stage B is complete. Execution has halted. Implementation will await explicit user authorization.**
