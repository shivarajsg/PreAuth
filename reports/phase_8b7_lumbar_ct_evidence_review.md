# MedRule — Phase 8B.7: Lumbar CT Criteria Decomposition Evidence Review

**Document ID:** `MEDRULE-REPORT-PHASE-08B7-LUMBAR-CT-EVIDENCE-REVIEW`  
**Date:** 2026-10-22  
**Status:** Stage A Evidence Review Complete (Diagnostic & Evidence Review Only — No Production Changes)  
**Remediation Reference:** `REM-P4-003` (Phase 8A Register & Phase 8B.6 Section 4.1)  
**Target Rule:** `RULE-ADV-CG2036-001`  
**Governing Authority:** `2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)`  
**Guideline Title:** `Evolent Clinical Guideline 2036 for Lumbar Spine Computed Tomography (CT)`  
**Physical Policy Pages:** 572–591 (Core Indication Pages: 574–579; Primary Review Page: 575)  
**Applicable CPT Codes:** CPT 72131 (without contrast), CPT 72132 (with contrast), CPT 72133 (without and with contrast)  

---

## 1. Executive Summary & Review Scope

In accordance with Phase 8B.7 directives, this evidence review conducts an exhaustive policy-fidelity and logical decomposition analysis for `RULE-ADV-CG2036-001` (Lumbar Spine CT, CPT 72131–72133). In the current MedRule active catalog, `RULE-ADV-CG2036-001` is the **sole remaining procedure-specific Advanced Imaging rule** whose clinical logic is collapsed into an uncompiled single-boolean stub (`lumbar_ct_indication_met == True`).

### Strict Operational Invariants Maintained During Stage A:
- **Zero Production Edits:** Exactly 0 modifications were made to production rule definitions (`draft_rules.json`), test suites, schemas, router tables, databases, policy PDFs, or governance statuses.
- **Zero Approved Rules Invariant:** The canonical governance invariant remains strictly at **`APPROVED: 0`** (`DRAFT: 121`, `NEEDS_HUMAN_REVIEW: 7`, Total Active Rules: 128).
- **Governance Gate Isolation:** All 7 canonical governance gates in `GOVERNANCE_BLOCKED_RULE_IDS` (`decision_tree.py`) remain strictly blocked from autonomous execution.
- **Domain Scope Preservation:** Active scope remains strictly confined to **Advanced Imaging (114 rules)** and **Interventional Pain Management (14 rules)**. Archived DMEPOS (`CP.MP.107`) remains excluded.
- **Stop for Review:** Stage A is strictly diagnostic and evaluative. No production code edits will be performed without explicit user authorization.

---

## 2. Authoritative Policy Text Verification (Physical Pages 574–581)

A line-by-line examination of `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` was conducted across physical pages 572 through 581 for Guideline 2036 (`Lumbar Spine Computed Tomography (CT)`).

### 2.1 Physical Page 574 (Printed `Page 3 of 20`)

#### Purpose & Clinical Role of Lumbar CT:
> *"Computed tomography is used for the evaluation, assessment of severity, and follow-up of diseases of the spine. CT is often used to study the lumbar spine for conditions such as degenerative disc disease when MRI is contraindicated. CT provides excellent depiction of bone detail and is used in the evaluation of known fractures of the lumbar spine and for evaluation of postoperative patients."*

#### Section: INDICATIONS FOR LUMBAR SPINE CT
#### Subsection: Evaluation of Neurologic Deficits (1)
> **When Lumbar Spine MRI is Contraindicated or Cannot be performed**  
> *● With any of the following new neurological deficits documented on physical exam that localizes to the lumbar spine:*  
> *(Deficits detailed on physical page 575)*

---

### 2.2 Physical Page 575 (Printed `Page 4 of 20`) — The Primary Review Page

Physical page 575 contains the core criteria for neurological deficits and ordinary back pain:

#### 1. Neurological Deficits Localizing to Lumbar Spine (When MRI Contraindicated / Cannot be performed):
> - *Extremity muscular weakness (not likely caused by plexopathy, peripheral neuropathy or neuromuscular disease)*
> - *Pathologic abnormal reflexes (not likely caused by plexopathy, peripheral neuropathy, or neuromuscular disease)*
> - *Absent/decreased sensation along a particular lumbar dermatome (nerve distribution): pin prick, touch, vibration, proprioception, or temperature (and not likely caused by plexopathy, or peripheral neuropathy)*
> - *Lower extremity decreased muscle tone (not likely caused by plexopathy, peripheral neuropathy or neuromuscular disease)*
> - *New onset bowel or bladder dysfunction (e.g., retention or incontinence)—not related to an inherent bowel or bladder process*
> - *Gait abnormalities (see Table 1 below for more details)*
> - *New onset foot drop (not related to a peripheral nerve injury, e.g., peroneal nerve)*
> - *Cauda Equina Syndrome as evidence by severe back pain/sciatica along with one of the defined symptoms (see Cauda Equina Syndrome section)*

#### 2. Evaluation of Back Pain (1):
> **With any of the following when Lumbar Spine MRI is Contraindicated:**  
> - *● With new or worsening objective neurologic deficits on exam, as above*  
> - *● Failure of conservative treatment\* for a minimum of six (6) weeks within the last six (6) months:*  
>   *NOTE - Failure of conservative treatment is defined as one of the following:*  
>   *○ Lack of meaningful improvement after a full course of treatment; OR*  
>   *○ Progression or worsening of symptoms during treatment; OR*  
>   *○ Documentation of a medical reason the member is unable to participate in treatment*  
>   *Closure of medical or therapy offices, patient inconvenience, or noncompliance without explanation does not constitute “inability to complete” treatment.*  
> - *● With progression or worsening of symptoms during the course of conservative treatment\**  
> - *● With an abnormal electromyography (EMG) or nerve conduction study (if performed) indicating a lumbar radiculopathy. (2,3)*  
> - *● Isolated back pain in pediatric population when at least ONE of the following red flags are present (4,5) (Note: conservative care not required if red flags are present):*  
>   *○ Age 5 or younger*  
>   *○ Constant pain*  
>   *○ Pain lasting > 4 weeks*  
>   *○ Abnormal neurologic examination*  
>   *(Red flags continued onto physical page 576)*

---

### 2.3 Physical Page 576 (Printed `Page 5 of 20`)

#### Pediatric Red Flags (Continued from Page 575):
> - *Early morning stiffness and/or gelling*
> - *Night pain that prevents or disrupts sleep*
> - *Radicular pain*
> - *Fever, weight loss, or malaise*
> - *Postural changes (e.g., kyphosis or scoliosis)*
> - *Limp (or refusal to walk in a younger child)*

#### Subsection: Evaluation of Trauma or Acute Injury (6)
*(Notice: Heading does NOT require MRI contraindication)*
> - *● Presents with any of the following neurological deficits as above*
> - *● With progression or worsening of symptoms during the course of conservative treatment*
> - *● History of underlying spinal abnormalities (i.e., ankylosing spondylitis or diffuse idiopathic skeletal hyperostosis) (Both MRI and CT are approvable) (7)*
> - *● When the patient is clinically unevaluable or there are preliminary imaging findings (x-ray or MRI) needing further evaluation*

#### Subsection: Pars Defect (Spondylolysis) or Spondylolisthesis
> - *● Pars defect (spondylolysis) or spondylolisthesis in adults when Flexion/Extension x-rays show instability (8)*
> - *● Clinically suspected pars defect (spondylolysis) after plain films (flexion extension instability not required) in pediatric population (< 18 yr.), or athletes and imaging would change treatment (4) when MRI is contraindicated/cannot be performed or surgeon preference*

#### Subsection: Evaluation of Compression Fractures (9)
*(Notice: Heading does NOT require MRI contraindication)*
> - *● To assess union of a fracture when physical examination, plain radiographs, or prior imaging suggest delayed or non-healing*
> - *● To determine the position of fracture fragments*
> - *● With history of malignancy*
> - *● Fracture on initial imaging in a young patient (<50) with no history of trauma and concern for pathologic fracture*
> - *● Fracture with imaging characteristics concerning for underlying malignancy*
> - *● With an associated new focal neurologic deficit as above*
> - *● Prior to a planned surgery/intervention or if the results of the CT will change management*

---

### 2.4 Physical Page 579 (Printed `Page 8 of 20`)

#### Section: PREOPERATIVE OR POSTOPERATIVE ASSESSMENT
> *When not otherwise specified in the guideline:*  
> **Preoperative evaluation:**  
> - *● CT discogram*  
> - *● Imaging of the area requested is needed to develop a surgical plan (no contraindication to MRI required if ordered by a neurosurgeon or orthopedic surgeon)*  
>  
> **Postoperative Evaluation:**  
> - *● Evaluation of post operative pseudarthrosis, hardware complication and/or extent of fusion after initial x-rays (a contraindication to MRI is not needed)*  
>   *NOTE: For this indication, advanced imaging should not occur until > 6 months after surgery*  
> - *● Surgical infection as evidenced by signs/symptoms, laboratory, or prior imaging findings when MRI is contraindicated or cannot be performed*  
> - *● New or changing neurological deficits or symptoms post-operatively (21) (see neurological deficit section above) when MRI is contraindicated or cannot be performed*  
> - *● Known or suspected complications*  
> - *● A clinical reason is provided how imaging may change management*  
>   *NOTE: This section applies only within the first few months following surgery unless otherwise specified*

---

## 3. Dissection of the 7 Key Clinical Elements & Logical Relationships

The user prompt mandates establishing the exact logical relationships between these 7 clinical elements:
1. **`MRI contraindication or inability to perform MRI`**
2. **`Failure of at least 6 weeks of conservative treatment within prior 6 months`**
3. **`Documented worsening during treatment`**
4. **`Abnormal EMG/NCS demonstrating radiculopathy`**
5. **`Acute trauma`**
6. **`Surgical hardware evaluation`**
7. **`Delayed union`**

### 3.1 Logical Relationship Analysis

```
                              ┌────────────────────────────────────────┐
                              │  LUMBAR SPINE CT (CPT 72131-72133)     │
                              │        TOP-LEVEL: ANY_OF               │
                              └──────────────────┬─────────────────────┘
                                                 │
         ┌──────────────────────────────┬────────┴─────────────────────┬──────────────────────────────┐
         ▼                              ▼                              ▼                              ▼
┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐           ┌──────────────────┐
│  TRACK A: TRAUMA │           │ TRACK B: HARDWARE│           │ TRACK C: BACK    │           │ TRACK D: NEURO   │
│ & DELAYED UNION  │           │   & FUSION >6M   │           │      PAIN        │           │     DEFICITS     │
├──────────────────┤           ├──────────────────┤           ├──────────────────┤           ├──────────────────┤
│ MRI CONTRA:      │           │ MRI CONTRA:      │           │ MRI CONTRA:      │           │ MRI CONTRA:      │
│  NOT REQUIRED    │           │ EXPLICITLY WAIVED│           │  MANDATORY (AND) │           │  MANDATORY (AND) │
├──────────────────┤           ├──────────────────┤           ├──────────────────┤           ├──────────────────┤
│ ANY_OF:          │           │ ALL_OF:          │           │ ALL_OF:          │           │ ALL_OF:          │
│ - Acute trauma   │           │ - Hardware/fusion│           │ - MRI Contra = T │           │ - MRI Contra = T │
│   + prelim x-ray │           │   complication   │           │ - ANY_OF:        │           │ - Focal neuro    │
│ - Delayed union/ │           │ - Prior x-ray = T│           │   * >=6w Tx /6mo │           │   deficit / CES  │
│   non-healing Fx │           │ - Post-op > 6 mo │           │   * Worsening    │           └──────────────────┘
│ - Fragment pos.  │           └──────────────────┘           │   * Med Contra Tx│
└──────────────────┘                                          │   * EMG radiculop│
                                                              │   * Peds Red Flag│
                                                              └──────────────────┘
```

#### Detailed Breakdown of Elements:

1. **Element 1: MRI Contraindication or Inability to Perform MRI**
   - **Where Mandatory:** In the **Back Pain Pathway** (p. 575) and **Neurologic Deficit Pathway** (pp. 574–575). In the absence of an osseous/hardware emergency, MRI is the standard of care for visualizing discs, nerve roots, the spinal canal, and neural elements without ionizing radiation. CT is only indicated if an absolute or relative MRI contraindication exists (e.g., non-conditional cardiac implantable electronic device, metallic intraocular foreign body, severe claustrophobia, or size/weight exceeds scanner bore).
   - **Where NOT Required:** In **Acute Trauma** (p. 576), **Delayed Union** (p. 576), and **Surgical Hardware / Pseudarthrosis** (p. 579).

2. **Element 2: Failure of at Least 6 Weeks of Conservative Treatment Within Prior 6 Months**
   - Standard prerequisite for non-emergent back pain.
   - Evaluated under the Back Pain Pathway (p. 575).
   - **Crucial Dependency:** Conservative care completion alone does **NOT** approve Lumbar CT unless **MRI Contraindication is also True**.

3. **Element 3: Documented Worsening During Conservative Treatment**
   - Explicit alternative to completing the full 6-week duration.
   - Defined in the policy note: *"Progression or worsening of symptoms during treatment"*.
   - **Logical Role:** Bypasses the 6-week temporal waiting period, but **DOES NOT bypass the MRI contraindication prerequisite**.

4. **Element 4: Abnormal EMG/NCS Demonstrating Radiculopathy**
   - Explicit objective neurophysiological alternative.
   - Policy: *"With an abnormal electromyography (EMG) or nerve conduction study (if performed) indicating a lumbar radiculopathy"*.
   - **Logical Role:** Objective proof of acute/subacute nerve root injury waives the conservative care trial, but **DOES NOT bypass the MRI contraindication prerequisite**.

5. **Element 5: Acute Trauma**
   - Policy: `Evaluation of Trauma or Acute Injury (6)` (p. 576).
   - CT is the gold-standard modality for cortical bone fractures, lamina/pedicle disruption, and acute instability.
   - **Logical Role:** **Independent alternative** that operates completely outside the Back Pain / MRI contraindication gate.

6. **Element 6: Surgical Hardware Evaluation / Postoperative Fusion / Pseudarthrosis**
   - Policy: `Postoperative Evaluation` (p. 579).
   - Verbatim statement: **`"(a contraindication to MRI is not needed)"`**.
   - Clinical rationale: Metallic instrumentation (pedicle screws, titanium rods, interbody cages) creates severe magnetic susceptibility artifacts ("blooming artifacts") on MRI, obliterating imaging around the hardware. Thin-slice CT with metal artifact reduction allows precise assessment of screw loosening ("halo" radiolucency), rod fracture, and bony trabecular bridge formation.
   - Prerequisites:
     - Prior initial plain radiographs completed (`prior_lumbar_xray_completed == True`).
     - Postoperative interval $> 6$ months (`postoperative_interval_greater_than_6_months == True`).
   - **Logical Role:** **Independent alternative** with explicit waiver of MRI contraindication.

7. **Element 7: Delayed Union**
   - Policy: `Evaluation of Compression Fractures (9)` (p. 576).
   - Verbatim statement: *"To assess union of a fracture when physical examination, plain radiographs, or prior imaging suggest delayed or non-healing"*.
   - **Logical Role:** **Independent alternative** assessing cortical bone bridging. Does **NOT** require MRI contraindication.

---

## 4. Pathway Classification: MRI Prerequisite vs. Independent Alternatives

The table below classifies every clinical pathway under Guideline 2036, establishing whether MRI contraindication is required or independent:

| Clinical Pathway | Physical Page | MRI Contraindication Required? | Prerequisites / Required Clinical Elements | Clinical & Biophysical Justification |
| :--- | :---: | :---: | :--- | :--- |
| **Lumbar Back Pain (Adult)** | p. 575 | **YES (Mandatory)** | $\ge 6$ weeks conservative therapy in prior 6 months, OR progression/worsening, OR medical inability to participate, OR abnormal EMG/NCS lumbar radiculopathy | MRI is the primary non-ionizing soft-tissue modality; CT is secondary and only indicated if MRI cannot be performed. |
| **Lumbar Back Pain (Pediatric)** | pp. 575–576 | **YES (Mandatory)** | Patient age $< 18$ with at least 1 of 10 red flags (Age $\le 5$, constant pain, pain $> 4$ wks, abnormal neuro exam, morning stiffness, night pain, radicular pain, fever/weight loss, kyphosis/scoliosis, limp) | Pediatric tissue is sensitive to ionizing radiation; MRI is first-line; CT reserved exclusively for MRI contraindication. |
| **Objective Neurologic Deficits** | pp. 574–575 | **YES (Mandatory)** | Objective focal deficit localizing to lumbar spine (foot drop, motor weakness, abnormal reflexes, dermatomal sensory loss, cauda equina syndrome) | Neural compression and spinal cord/cauda equina pathology require soft-tissue resolution of MRI unless contraindicated. |
| **Acute Spinal Trauma / Injury** | p. 576 | **NO (Independent Alternative)** | Preliminary imaging (plain X-ray) needing evaluation, OR clinically unevaluable, OR trauma with neurologic deficit, OR underlying AS/DISH | Thin-slice CT is the gold standard for acute osseous trauma, facet fractures, and spinal column alignment. |
| **Delayed Fracture Union / Non-Healing** | p. 576 | **NO (Independent Alternative)** | Plain radiographs or physical exam suggest delayed union or non-healing; or fragment positioning | CT evaluates trabecular bridging and callus density without magnetic artifact. |
| **Postoperative Hardware / Fusion / Pseudarthrosis** | p. 579 | **NO (Explicitly Waived in Policy)** | Plain radiographs completed AND postoperative interval $> 6$ months | Metal hardware severely degrades MRI; policy literally specifies `"(a contraindication to MRI is not needed)"`. |
| **Preoperative Planning by Spine Surgeon** | p. 579 | **NO (Explicitly Waived in Policy)** | Ordered by neurosurgeon or orthopedic spine surgeon to develop surgical plan | Accurate measurement of pedicle diameter, screw trajectory, and bony morphology for instrumentation. |
| **Adult Pars Defect / Spondylolisthesis** | p. 576 | **NO (Independent Alternative)** | Plain flexion/extension radiographs show motion/instability | Evaluates bony lysis of pars interarticularis and vertebral slippage. |
| **Suspected Spinal Infection (Osteomyelitis/Abscess)** | p. 577 | **YES (Mandatory)** | Signs/symptoms, elevated ESR/CRP, or prior imaging | MRI is far more sensitive for marrow edema and epidural phlegmon/abscess. |
| **Immune Suppression Spine Abnormalities** | p. 578 | **YES (Mandatory)** | HIV, active chemotherapy, leukemia, lymphoma with symptoms | Soft-tissue and marrow involvement require MRI unless contraindicated. |

---

## 5. Current Encoded Defect Analysis & Proposed Condition Tree Architecture

### 5.1 The Current Encoded Rule (`draft_rules.json`)
```json
{
  "rule_id": "RULE-ADV-CG2036-001",
  "domain": "advanced_imaging",
  "source_page": {
    "physical_page": 574,
    "printed_page": "Page 3 of 20"
  },
  "source_section": "INDICATIONS FOR LUMBAR SPINE CT / Evaluation of Neurologic Deficits (1)",
  "source_quote": "INDICATIONS FOR LUMBAR SPINE CT",
  "clinical_service_or_procedure": "Lumbar Spine CT",
  "rule_type": "clinical_indication",
  "conditions": {
    "operator": "ALL_OF",
    "criteria": [
      {
        "condition_id": "COND-001",
        "description": "Evaluation of acute lumbar trauma, surgical fusion integrity/pseudoarthrosis, or lumbar pain when MRI is contraindicated",
        "parameter": "lumbar_ct_indication_met",
        "comparator": "EQUALS",
        "value": true
      }
    ]
  },
  "required_documentation": [
    "Clinical notes documenting spinal trauma, hardware evaluation, or contraindication to lumbar MRI"
  ],
  "decision_effect": "INDICATED",
  "dependencies": [
    "CPT 72131"
  ]
}
```

### 5.2 Defect Impact & Hazards
1. **Citation Inaccuracy:** Cites physical page 574 (general preamble / purpose) instead of physical page 575 where the actual criteria reside.
2. **False Approvals:** Any intake setting `lumbar_ct_indication_met = True` approves Lumbar CT for ordinary back pain without verifying whether lumbar MRI is contraindicated or whether conservative therapy was completed.
3. **Automated Intake Failure:** Upstream EHR extractors providing granular clinical parameters (e.g. `lumbar_conservative_therapy_weeks`, `lumbar_mri_contraindicated`) cannot map to the single composite boolean `lumbar_ct_indication_met`, causing cases to pend or fail.

### 5.3 Proposed Decomposed Condition Tree Architecture
To remediate `RULE-ADV-CG2036-001` while preserving the **128 total active rule count**, the rule should be decomposed into a multi-track condition tree under a top-level `ANY_OF` operator:

```json
{
  "operator": "ANY_OF",
  "criteria": [
    {
      "condition_id": "COND-001",
      "description": "Track A (Trauma & Fracture Assessment): Evaluation of acute lumbar trauma with preliminary imaging, fracture fragment positioning, or delayed union / non-healing fracture",
      "sub_conditions": {
        "operator": "ANY_OF",
        "criteria": [
          {
            "condition_id": "COND-001A",
            "description": "Acute lumbar trauma or acute injury with preliminary imaging findings (e.g., x-ray) needing further evaluation or patient clinically unevaluable",
            "parameter": "acute_lumbar_trauma_with_preliminary_imaging",
            "comparator": "EQUALS",
            "value": true
          },
          {
            "condition_id": "COND-001B",
            "description": "Assessment of compression fracture union when physical exam, plain radiographs, or prior imaging suggest delayed or non-healing",
            "parameter": "delayed_union_or_nonunion_fracture",
            "comparator": "EQUALS",
            "value": true
          },
          {
            "condition_id": "COND-001C",
            "description": "Determination of fracture fragment position following lumbar spine fracture",
            "parameter": "fracture_fragment_position_evaluation",
            "comparator": "EQUALS",
            "value": true
          }
        ]
      }
    },
    {
      "condition_id": "COND-002",
      "description": "Track B (Postoperative Hardware & Fusion): Evaluation of postoperative pseudarthrosis, hardware complication, and/or extent of fusion after initial x-rays and > 6 months post-surgery",
      "sub_conditions": {
        "operator": "ALL_OF",
        "criteria": [
          {
            "condition_id": "COND-002A",
            "description": "Clinical suspicion of postoperative pseudarthrosis, hardware complication, or assessment of extent of fusion",
            "parameter": "postoperative_fusion_hardware_or_pseudarthrosis",
            "comparator": "EQUALS",
            "value": true
          },
          {
            "condition_id": "COND-002B",
            "description": "Preliminary plain radiographs (X-rays) of the lumbar spine have been completed",
            "parameter": "prior_lumbar_xray_completed",
            "comparator": "EQUALS",
            "value": true
          },
          {
            "condition_id": "COND-002C",
            "description": "Postoperative interval is greater than 6 months following lumbar surgery",
            "parameter": "postoperative_interval_greater_than_6_months",
            "comparator": "EQUALS",
            "value": true
          }
        ]
      }
    },
    {
      "condition_id": "COND-003",
      "description": "Track C (Back Pain & Neurologic Deficits with MRI Contraindication): Evaluation of lumbar back pain or new focal neurologic deficit when lumbar MRI is contraindicated or cannot be performed",
      "sub_conditions": {
        "operator": "ALL_OF",
        "criteria": [
          {
            "condition_id": "COND-003A",
            "description": "Lumbar spine MRI is contraindicated (e.g., non-conditional implant, metallic foreign body, severe claustrophobia) or cannot be performed",
            "parameter": "lumbar_mri_contraindicated",
            "comparator": "EQUALS",
            "value": true
          },
          {
            "condition_id": "COND-003B",
            "description": "Clinical indication met for back pain, conservative therapy failure, radiculopathy, or objective neurologic deficit",
            "sub_conditions": {
              "operator": "ANY_OF",
              "criteria": [
                {
                  "condition_id": "COND-003B1",
                  "description": "Objective focal neurologic deficit localizing to lumbar spine (e.g., foot drop, motor weakness, sensory loss, abnormal reflexes) or suspected cauda equina syndrome",
                  "parameter": "objective_neurologic_deficit_lumbar",
                  "comparator": "EQUALS",
                  "value": true
                },
                {
                  "condition_id": "COND-003B2",
                  "description": "Adult pathway: Failure of conservative treatment for >= 6 weeks within last 6 months, OR worsening during treatment, OR medical inability to participate, OR abnormal EMG/NCS lumbar radiculopathy",
                  "sub_conditions": {
                    "operator": "ALL_OF",
                    "criteria": [
                      {
                        "condition_id": "COND-003B2A",
                        "description": "Patient is adult (age >= 18 years)",
                        "parameter": "patient_age_years",
                        "comparator": "GREATER_THAN_OR_EQUAL",
                        "value": 18
                      },
                      {
                        "condition_id": "COND-003B2B",
                        "description": "Adult conservative care trial failed, progressed, medically contraindicated, or verified by abnormal EMG/NCS",
                        "sub_conditions": {
                          "operator": "ANY_OF",
                          "criteria": [
                            {
                              "condition_id": "COND-003B2B1",
                              "description": "Failure of conservative treatment for a minimum of six (6) weeks within the last six (6) months",
                              "parameter": "lumbar_conservative_therapy_weeks",
                              "comparator": "GREATER_THAN_OR_EQUAL",
                              "value": 6,
                              "unit": "weeks"
                            },
                            {
                              "condition_id": "COND-003B2B2",
                              "description": "Progression or worsening of symptoms during the course of conservative treatment",
                              "parameter": "conservative_treatment_worsening",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B2B3",
                              "description": "Documentation of a medical reason the member is unable to participate in conservative treatment",
                              "parameter": "medical_contraindication_to_conservative_therapy",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B2B4",
                              "description": "Abnormal electromyography (EMG) or nerve conduction study indicating a lumbar radiculopathy",
                              "parameter": "abnormal_emg_ncs_lumbar_radiculopathy",
                              "comparator": "EQUALS",
                              "value": true
                            }
                          ]
                        }
                      }
                    ]
                  }
                },
                {
                  "condition_id": "COND-003B3",
                  "description": "Pediatric pathway: Isolated back pain in pediatric population (age < 18) with at least ONE verified red flag (conservative care not required)",
                  "sub_conditions": {
                    "operator": "ALL_OF",
                    "criteria": [
                      {
                        "condition_id": "COND-003B3A",
                        "description": "Patient is pediatric (age < 18 years)",
                        "parameter": "patient_age_years",
                        "comparator": "LESS_THAN",
                        "value": 18
                      },
                      {
                        "condition_id": "COND-003B3B",
                        "description": "At least ONE of ten source-verified pediatric red flags present",
                        "sub_conditions": {
                          "operator": "ANY_OF",
                          "criteria": [
                            {
                              "condition_id": "COND-003B3B01",
                              "description": "Age 5 or younger",
                              "parameter": "patient_age_years",
                              "comparator": "LESS_THAN_OR_EQUAL",
                              "value": 5
                            },
                            {
                              "condition_id": "COND-003B3B02",
                              "description": "Constant lumbar pain",
                              "parameter": "constant_lumbar_pain",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B3B03",
                              "description": "Lumbar pain lasting greater than 4 weeks",
                              "parameter": "lumbar_pain_duration_weeks",
                              "comparator": "GREATER_THAN",
                              "value": 4,
                              "unit": "weeks"
                            },
                            {
                              "condition_id": "COND-003B3B04",
                              "description": "Abnormal neurologic examination",
                              "parameter": "abnormal_neurologic_exam",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B3B05",
                              "description": "Early morning stiffness and/or gelling",
                              "parameter": "morning_stiffness_or_gelling",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B3B06",
                              "description": "Night pain that prevents or disrupts sleep",
                              "parameter": "night_pain_disrupting_sleep",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B3B07",
                              "description": "Radicular pain present",
                              "parameter": "radicular_pain_present",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B3B08",
                              "description": "Constitutional symptoms (fever, weight loss, malaise)",
                              "parameter": "constitutional_symptoms_fever_weight_loss",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B3B09",
                              "description": "Postural changes (e.g., kyphosis or scoliosis)",
                              "parameter": "postural_changes_kyphosis_scoliosis",
                              "comparator": "EQUALS",
                              "value": true
                            },
                            {
                              "condition_id": "COND-003B3B10",
                              "description": "Limp or refusal to walk in a younger child",
                              "parameter": "gait_abnormality_or_limp",
                              "comparator": "EQUALS",
                              "value": true
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    }
  ]
}
```

---

## 6. Engine Schema Representation & Three-Valued Logic Semantics

### 6.1 Representation of Evidence States in `medrule_engine`
The MedRule engine operates on a deterministic, three-valued Boolean logic framework (`EvaluationState.TRUE`, `EvaluationState.FALSE`, `EvaluationState.UNKNOWN`) and maps intake evidence into four criterion states (`CriterionState.MET`, `CriterionState.NOT_MET`, `CriterionState.INSUFFICIENT_DATA`, `CriterionState.NOT_APPLICABLE`).

```
┌─────────────────────────┬──────────────────────┬──────────────────────┬──────────────────────────────┐
│ Clinical Intake State   │ Evidence State       │ Evaluation State     │ Final Decision Outcome       │
├─────────────────────────┼──────────────────────┼──────────────────────┼──────────────────────────────┤
│ Value matches condition │ EXPLICIT_POSITIVE    │ TRUE                 │ CRITERIA_MET (if path true)  │
│ Value negates condition │ EXPLICIT_NEGATIVE    │ FALSE                │ CRITERIA_NOT_MET (if blocked)│
│ Field omitted / None    │ MISSING              │ UNKNOWN              │ INSUFFICIENT_INFORMATION     │
│ Invalid type / range    │ AMBIGUOUS            │ UNKNOWN (Type Error) │ INSUFFICIENT_INFORMATION     │
│ Contradictory records   │ CONFLICTING          │ UNKNOWN              │ INSUFFICIENT_INFORMATION     │
└─────────────────────────┴──────────────────────┴──────────────────────┴──────────────────────────────┘
```

### 6.2 Three-Valued Logic Propagation in the Lumbar CT Condition Tree
Under Kleene's strong three-valued logic implemented in `ConditionEvaluator`:

1. **Top-Level `ANY_OF` Rule:**
   - If any track evaluates to `TRUE`, the top-level outcome is `TRUE` (`CRITERIA_MET`), even if other tracks have missing data (`TRUE or UNKNOWN = TRUE`).
   - If all tracks evaluate to `FALSE`, the top-level outcome is `FALSE` (`CRITERIA_NOT_MET`).
   - If one track evaluates to `UNKNOWN` and all other tracks are `FALSE`, the top-level outcome is `UNKNOWN` (`INSUFFICIENT_INFORMATION`), preventing premature denial.

2. **Track C `ALL_OF` Rule:**
   - Both `lumbar_mri_contraindicated` AND `COND-003B` must be `TRUE`.
   - If `lumbar_mri_contraindicated == False`, Track C immediately evaluates to `FALSE` (`FALSE and UNKNOWN = FALSE`). If Tracks A and B are also `FALSE`, the case deterministically resolves to `CRITERIA_NOT_MET`. **This prevents false approvals for patients who could safely receive an MRI.**
   - If `lumbar_mri_contraindicated` is omitted (`UNKNOWN`), but the patient completed 8 weeks of therapy, Track C evaluates to `UNKNOWN and TRUE = UNKNOWN`. The engine yields `INSUFFICIENT_INFORMATION` and pends the case for clinical documentation of MRI contraindication.

---

## 7. Exhaustive Test Suite Blueprint

Before any implementation, a complete suite of verification cases must be planned to validate all branches, boundaries, and routing permutations:

### 7.1 Positive Test Cases (Expectation: `CRITERIA_MET`)
- **`TC-ADV-2036-POS-01` (Track A — Acute Trauma):**
  - Inputs: `acute_lumbar_trauma_with_preliminary_imaging: True`
  - Validation: Qualifies under Track A. MRI contraindication is NOT required.
- **`TC-ADV-2036-POS-02` (Track A — Delayed Union):**
  - Inputs: `delayed_union_or_nonunion_fracture: True`
  - Validation: Qualifies under Track A for non-healing fracture evaluation.
- **`TC-ADV-2036-POS-03` (Track B — Postoperative Hardware Evaluation > 6 Months):**
  - Inputs: `postoperative_fusion_hardware_or_pseudarthrosis: True`, `prior_lumbar_xray_completed: True`, `postoperative_interval_greater_than_6_months: True`
  - Validation: Qualifies under Track B without requiring MRI contraindication.
- **`TC-ADV-2036-POS-04` (Track C — Adult Back Pain with Conservative Care Failure):**
  - Inputs: `lumbar_mri_contraindicated: True`, `patient_age_years: 45`, `lumbar_conservative_therapy_weeks: 6`
  - Validation: Qualifies under Track C adult pathway.
- **`TC-ADV-2036-POS-05` (Track C — Adult Back Pain with Worsening During Therapy):**
  - Inputs: `lumbar_mri_contraindicated: True`, `patient_age_years: 52`, `conservative_treatment_worsening: True`, `lumbar_conservative_therapy_weeks: 2`
  - Validation: Qualifies immediately under worsening exception.
- **`TC-ADV-2036-POS-06` (Track C — Adult Back Pain with Medical Inability to Participate):**
  - Inputs: `lumbar_mri_contraindicated: True`, `patient_age_years: 67`, `medical_contraindication_to_conservative_therapy: True`
  - Validation: Qualifies under medical contraindication exception.
- **`TC-ADV-2036-POS-07` (Track C — Adult Back Pain with Abnormal EMG/NCS Radiculopathy):**
  - Inputs: `lumbar_mri_contraindicated: True`, `patient_age_years: 38`, `abnormal_emg_ncs_lumbar_radiculopathy: True`
  - Validation: Qualifies on objective EMG electrodiagnostic evidence.
- **`TC-ADV-2036-POS-08` (Track C — Objective Lumbar Neurologic Deficit / Foot Drop):**
  - Inputs: `lumbar_mri_contraindicated: True`, `objective_neurologic_deficit_lumbar: True`
  - Validation: Qualifies on focal neurologic exam deficit with MRI contraindicated.
- **`TC-ADV-2036-POS-09` (Track C — Pediatric Back Pain with Red Flag):**
  - Inputs: `lumbar_mri_contraindicated: True`, `patient_age_years: 4`, `night_pain_disrupting_sleep: True`
  - Validation: Qualifies under pediatric red-flag pathway (< 18 yr) with MRI contraindicated.

### 7.2 Negative Test Cases (Expectation: `CRITERIA_NOT_MET`)
- **`TC-ADV-2036-NEG-01` (Adult Back Pain with MRI NOT Contraindicated — False Approval Prevention):**
  - Inputs: `acute_lumbar_trauma_with_preliminary_imaging: False`, `postoperative_fusion_hardware_or_pseudarthrosis: False`, `lumbar_mri_contraindicated: False`, `patient_age_years: 45`, `lumbar_conservative_therapy_weeks: 8`
  - Validation: Fails Track C because MRI is not contraindicated. Correctly prevents false approval.
- **`TC-ADV-2036-NEG-02` (Adult Back Pain with Insufficient Therapy Duration):**
  - Inputs: `acute_lumbar_trauma_with_preliminary_imaging: False`, `postoperative_fusion_hardware_or_pseudarthrosis: False`, `lumbar_mri_contraindicated: True`, `patient_age_years: 30`, `lumbar_conservative_therapy_weeks: 4`, `conservative_treatment_worsening: False`
  - Validation: Fails because 4 weeks < 6 weeks requirement.
- **`TC-ADV-2036-NEG-03` (Postoperative Hardware Evaluation < 6 Months):**
  - Inputs: `acute_lumbar_trauma_with_preliminary_imaging: False`, `postoperative_fusion_hardware_or_pseudarthrosis: True`, `prior_lumbar_xray_completed: True`, `postoperative_interval_greater_than_6_months: False`
  - Validation: Fails Track B because post-op interval is <= 6 months.
- **`TC-ADV-2036-NEG-04` (Postoperative Hardware Evaluation Missing Prior Plain Radiographs):**
  - Inputs: `acute_lumbar_trauma_with_preliminary_imaging: False`, `postoperative_fusion_hardware_or_pseudarthrosis: True`, `prior_lumbar_xray_completed: False`, `postoperative_interval_greater_than_6_months: True`
  - Validation: Fails Track B because initial plain films were not completed.

### 7.3 Missing Evidence Test Cases (Expectation: `INSUFFICIENT_INFORMATION`)
- **`TC-ADV-2036-MISS-01` (Completely Empty Evidence Payload):**
  - Inputs: `{}`
  - Validation: All parameters missing; yields `INSUFFICIENT_INFORMATION`.
- **`TC-ADV-2036-MISS-02` (Adult Back Pain with 8 Weeks Therapy but Missing MRI Contraindication):**
  - Inputs: `patient_age_years: 45`, `lumbar_conservative_therapy_weeks: 8`
  - Validation: `lumbar_mri_contraindicated` is missing; cannot determine if MRI is contraindicated. Yields `INSUFFICIENT_INFORMATION`.
- **`TC-ADV-2036-MISS-03` (Postoperative Hardware Evaluation Missing Interval):**
  - Inputs: `postoperative_fusion_hardware_or_pseudarthrosis: True`, `prior_lumbar_xray_completed: True`
  - Validation: `postoperative_interval_greater_than_6_months` is missing; yields `INSUFFICIENT_INFORMATION`.

### 7.4 Boundary & Exception Test Cases
- **`TC-ADV-2036-BND-01` (Conservative Care Duration Boundary):**
  - Subcase A: `lumbar_conservative_therapy_weeks: 5.9` $\rightarrow$ Fails (`CRITERIA_NOT_MET`)
  - Subcase B: `lumbar_conservative_therapy_weeks: 6.0` $\rightarrow$ Passes (`CRITERIA_MET`)
- **`TC-ADV-2036-BND-02` (Patient Age Boundary):**
  - Subcase A: `patient_age_years: 17.9` with `constant_lumbar_pain: True` $\rightarrow$ Evaluates via pediatric red flag branch (`CRITERIA_MET`).
  - Subcase B: `patient_age_years: 18.0` with `constant_lumbar_pain: True` and 2 weeks therapy $\rightarrow$ Evaluates via adult branch, fails duration (`CRITERIA_NOT_MET`).

### 7.5 CPT Candidate-Routing Tests
- **`TC-ADV-2036-ROUTING-01` (CPT 72131 Deterministic Routing):**
  - Case: Procedure `72131` (CT Lumbar Spine without contrast) in `advanced_imaging`.
  - Expected Candidates: `RULE-ADV-CG2036-001`, plus shared preamble (`RULE-ADV-PREAMBLE-001`) and POS rules (`RULE-ADV-EPOS2067-001..005`).
- **`TC-ADV-2036-ROUTING-02` (CPT 72132 and 72133 Coverage Check):**
  - Verify that CPT 72132 (with contrast) and CPT 72133 (without and with contrast) have proper guideline alignment in inventory documentation.

---

## 8. Summary of Findings & Implementation Blueprint

### Key Findings Summary:
1. **Physical Page Alignment:** The true clinical indication criteria for Lumbar CT reside on **physical page 575 (printed `Page 4 of 20`)**, not physical page 574 (general preamble/purpose).
2. **Pathway Independence:**
   - **Back Pain & Neurologic Deficits:** Require **mandatory MRI contraindication**.
   - **Acute Trauma / Fracture Assessment:** Operates as an **independent alternative** without requiring MRI contraindication.
   - **Postoperative Hardware / Fusion Evaluation:** Operates as an **independent alternative** with **explicit policy waiver of MRI contraindication** (`"(a contraindication to MRI is not needed)"`), but strictly requires prior X-rays and $> 6$ months post-op interval.
3. **Decomposition Feasibility:** A 3-track / 4-track condition tree under a top-level `ANY_OF` operator completely resolves the collapsed boolean defect while preserving all policy criteria, preventing false approvals, and maintaining the **128 total active rule count**.

### Strict Operational Halt:
In compliance with the user's constraints:
- **No production code, rule definitions, schemas, tests, databases, or governance gates have been modified.**
- **The governance invariant `APPROVED: 0` remains strictly intact.**
- **All 7 governance blockage gates remain sealed.**

**Awaiting user authorization before proceeding to Phase 8B.7 Stage B (Implementation).**
