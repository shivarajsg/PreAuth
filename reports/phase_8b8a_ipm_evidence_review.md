# MedRule — Phase 8B.8A: Interventional Pain Management (IPM) Diagnostic Evidence Review

**Document ID:** `MEDRULE-REPORT-PHASE-08B8A-IPM-EVIDENCE-REVIEW`  
**Date:** 2026-10-22  
**Status:** Diagnostic Evidence Review & Batch Plan Complete (Stage A Diagnostic Review — Zero Production Edits)  
**Remediation Reference:** `REM-P3-001`, `REM-P3-003`, `REM-P3-004`, `REM-P3-005`, `REM-P3-006`, `REM-P3-007`, `REM-P3-008`, `REM-P3-009`, `REM-P3-010` (from `reports/phase_8b6_remaining_remediation_register.json`)  
**Target Rules (9):**
1. `RULE-IPM-CGEPIDURALINJECTIONS-001` (Epidural Spine Injections)
2. `RULE-IPM-CGEPIDURALPUMPTRIALS-001` (Single Injection Trials for Intrathecal Pumps)
3. `RULE-IPM-CGFACETBLOCKS-001` (Paravertebral Facet Joint Injections / Blocks)
4. `RULE-IPM-CGFACETDENERVATION-001` (Paravertebral Facet Joint Denervation / RFA)
5. `RULE-IPM-CGFACETDENERVATION-002` (Facet Denervation Diagnostic Block Relief Threshold)
6. `RULE-IPM-CGSIINJECTIONS-001` (Sacroiliac Joint Injections)
7. `RULE-IPM-CGSPINALCORDSTIM-001` (Spinal Cord Stimulation Trial)
8. `RULE-IPM-CGSYMPATHETICBLOCKS-001` (Sympathetic Nerve Blocks)
9. `RULE-IPM-EPOS1755-001` (Place of Service Policy 1755 Clinical Exceptions)

**Governing Authorities:**
1. `2026 Evolent Clinical Guidelines for Medical Necessity Review: Interventional Pain Management Guidelines` (102 physical pages)
2. `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` (8 physical pages)

---

## 1. Executive Summary & Review Scope

In accordance with Phase 8B.8A directives, this diagnostic review conducts an exhaustive, source-grounded policy verification and logical decomposition analysis for all **nine outstanding Interventional Pain Management (IPM) rules** identified in `reports/phase_8b6_remaining_remediation_register.json`.

Following the complete criteria decomposition and verification of all 107 procedure-specific Advanced Imaging rules in Phase 8B.7, the nine target IPM rules represent the remaining uncompiled single-boolean stubs (and associated threshold alignment items) in the active MedRule rulebook. 

### 1.1 Strict Operational Invariants Maintained During Phase 8B.8A
- **Zero Production Edits:** Exactly 0 modifications were made to production rule definitions (`draft_rules.json`), engine code, test suites, schemas, router tables, databases, policy PDFs, or governance statuses.
- **Zero Approved Rules Invariant:** The canonical governance invariant remains strictly at **`APPROVED: 0`** (`DRAFT: 121`, `NEEDS_HUMAN_REVIEW: 7`, Total Active Rules: 128).
- **Governance Gate Isolation:** All 7 canonical governance gates in `GOVERNANCE_BLOCKED_RULE_IDS` (`decision_tree.py`) remain strictly blocked from autonomous execution, including the two IPM gates (`RULE-IPM-PREAMBLEIPM-001` and `RULE-IPM-CGINFUSIONPUMPS-001`).
- **Domain Scope Preservation:** Active scope remains strictly confined to **Advanced Imaging (114 rules)** and **Interventional Pain Management (14 rules)**. Archived DMEPOS (`CP.MP.107`) remains excluded.
- **Strict Verification of Source Passages:** Every clinical threshold, exclusion, time window, and logical operator proposed in earlier summaries was verified directly against the authoritative 2026 Evolent IPM and EPOS PDFs rather than assumed to be correct.
- **Awaiting Authorization:** Phase 8B.8A concludes with this evidence review and the accompanying batch plan. Execution of any rule changes halts until explicit user authorization is provided.

---

## 2. Authoritative Policy Architecture & Complete IPM Rulebook Inventory

The IPM domain consists of 14 total active rules governed by two authoritative Evolent clinical policies. The table below delineates the full inventory, current statuses, and source citations:

| Rule ID | Clinical Service / Procedure | Current Status | Human Review Gate | Governing PDF | Physical Pages | Printed Pages | Remediation Record ID |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `RULE-IPM-PREAMBLEIPM-001` | Preamble & Guideline Process | `DRAFT` | **BLOCKED (True)** | IPM Guidelines | 2 | Page 2 of 102 | `REM-P5-005` (Gate) |
| `RULE-IPM-CGEPIDURALINJECTIONS-001` | Epidural Spine Injections | `DRAFT` | False (Target 1) | IPM Guidelines | 4–16 (Indications: 6–8) | Pages 3–5 of 13 | `REM-P3-001` (Outstanding) |
| `RULE-IPM-CGEPIDURALINJECTIONS-002` | ESI Conservative Care Failure | `DRAFT` | False | IPM Guidelines | 6–11 (Indications: 7, 11) | Pages 4, 8 of 13 | `REM-P3-002` (Verified 8B.1) |
| `RULE-IPM-CGEPIDURALPUMPTRIALS-001` | Single Injection Pump Trials | `DRAFT` | False (Target 2) | IPM Guidelines | 17–30 (Indications: 20–23)| Pages 4–7 of 14 | `REM-P3-003` (Outstanding) |
| `RULE-IPM-CGFACETBLOCKS-001` | Facet Joint Injections / Blocks | `DRAFT` | False (Target 3) | IPM Guidelines | 31–44 (Indications: 32–34)| Pages 2–4 of 14 | `REM-P3-004` (Outstanding) |
| `RULE-IPM-CGFACETDENERVATION-001` | Facet Joint Denervation / RFA | `DRAFT` | False (Target 4) | IPM Guidelines | 45–56 (Indications: 46–48)| Pages 2–4 of 12 | `REM-P3-005` (Outstanding) |
| `RULE-IPM-CGFACETDENERVATION-002` | Facet RFA Relief Threshold | `DRAFT` | False (Target 5) | IPM Guidelines | 45–56 (Indications: 46–47)| Pages 2–3 of 12 | `REM-P3-006` (Outstanding) |
| `RULE-IPM-CGSIINJECTIONS-001` | Sacroiliac Joint Injections | `DRAFT` | False (Target 6) | IPM Guidelines | 57–67 (Indications: 58–60)| Pages 2–4 of 10 | `REM-P3-007` (Outstanding) |
| `RULE-IPM-CGINFUSIONPUMPS-001` | Implantable Infusion Pump Insert | `DRAFT` | **BLOCKED (True)** | IPM Guidelines | 67–76 (Indications: 68–71)| Pages 2–5 of 10 | `REM-P5-006` (Gate) |
| `RULE-IPM-CGSPINALCORDSTIM-001` | Spinal Cord Stimulation Trial | `DRAFT` | False (Target 7) | IPM Guidelines | 77–88 (Indications: 78–80)| Pages 2–4 of 12 | `REM-P3-008` (Outstanding) |
| `RULE-IPM-CGSPINALCORDSTIM-002` | Permanent SCS Trial Relief | `DRAFT` | False | IPM Guidelines | 77–88 (Indications: 80) | Page 4 of 12 | Retained Prerequisite |
| `RULE-IPM-CGSYMPATHETICBLOCKS-001` | Sympathetic Nerve Blocks | `DRAFT` | False (Target 8) | IPM Guidelines | 89–102 (Indications: 91–96)| Pages 3–8 of 14 | `REM-P3-009` (Outstanding) |
| `RULE-IPM-EPOS1755-001` | EPOS 1755 Clinical Exceptions | `DRAFT` | False (Target 9) | EPOS 1755 PDF | 1–8 (Indications: 3–4) | Pages 3–4 of 8 | `REM-P3-010` (Outstanding) |
| `RULE-IPM-EPOS1755-002` | IPM Site of Care Alignment | `DRAFT` | False | EPOS 1755 PDF | 1–8 (Indications: 3) | Page 3 of 8 | `REM-P3-011` (Verified 8B.1) |

---

## 3. Rule-by-Rule Diagnostic Review & Logic Decomposition

---

### 3.1 RULE-IPM-CGEPIDURALINJECTIONS-001 — Epidural Spine Injections
- **Remediation Reference:** `REM-P3-001` (Priority 3)
- **Clinical Service:** Epidural Spine Injections 2026 (July)
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Evolent Clinical Guideline 1750 for Epidural Spine Injections`
- **Source Citation:** Physical pages 4, 6–8; Printed `Pages 1, 3–5 of 13`
- **Applicable CPT Codes (8 codes):**
  - Cervical/Thoracic Interlaminar: `62320` (without imaging), `62321` (with imaging)
  - Cervical/Thoracic Transforaminal: `64479` (single level), `64480` (each additional level)
  - Lumbar/Sacral Interlaminar: `62322` (without imaging), `62323` (with imaging)
  - Lumbar/Sacral Transforaminal: `64483` (single level), `64484` (each additional level)

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGEPIDURALINJECTIONS-001",
  "source_page": {"physical_page": 4, "printed_page": "Page 4 of 102"},
  "source_section": "Epidural Spine Injections 2026 (July)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-CGEPIDURALINJECTIONS-001",
        "description": "Clinical criteria satisfied for Epidural Spine Injections 2026 (July)",
        "parameter": "cgepiduralinjections_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 6–8):
> **INDICATIONS — General to All Caudal, Interlaminar, and Transforaminal Injections:**  
> - *Fluoroscopic guidance should be used for caudal and interlaminar injections and is necessary for transforaminal injections.*  
> - *For all injections, patients must exhibit pain causing functional disability or average pain level of ≥6 on a scale of 0 to 10 (2–4) related to the requested spinal region.*  
>  
> **Treatment Purposes:**  
> - **Acute pain or exacerbation of chronic radicular pain (all the following must be met):**  
>   - *Neck or back pain with acute radicular symptoms*  
>   - *Duration of pain < 3 months*  
>   - *Failure to respond to non-operative conservative treatment targeting the requested spinal region for a minimum of 2 weeks unless the medical reason this treatment cannot be done is clearly documented (active therapy components not required)*  
> - **Spinal stenosis causing axial or radicular pain (all the following must be met):**  
>   - *Failure to respond to non-operative conservative treatment* targeting the requested spinal region for a minimum of six (6) weeks in the last six (6) months unless the medical reason this treatment cannot be done is clearly documented*  
>   - *OR details of engagement in ongoing non-operative conservative treatment if the individual has had prior spinal injections in the same region*  
> - **Failed back surgery syndrome or epidural fibrosis causing axial or radicular pain (all of the following must be met):**  
>   - *Documentation of a medical reason that clearly indicates why an injection is needed (not typically done immediately post-surgery)*  
>   - *Failure to respond to non-operative conservative treatment* targeting the requested spinal region for a minimum of six (6) weeks in the last six (6) months unless the medical reason this treatment cannot be done is clearly documented*  
>   - *OR details of engagement in ongoing non-operative conservative treatment* if the individual has had prior spinal injections in the same region*  
>  
> **Diagnostic Purposes:**  
> - **Transforaminal injection to identify the pain generator for surgical planning (all the following must be met):**  
>   - *Documentation of a pre-operative evaluation and plan for surgery*  
>   - *NOTE: No more than 2 levels of transforaminal blocks should be done in one day.*  
>  
> **Repeat Injections:**  
> - *Initial Treatment Phase: Up to 3 epidural injections may be performed in the initial treatment phase, no sooner than 2 weeks apart, provided that at least 30% pain relief or significant documented functional improvement is obtained.*  
> - *Therapeutic Phase: Epidural injections may only be repeated after the initial treatment phase if the individual has had at least 50% pain relief or significant documented functional improvement for a minimum of 2 months before each therapeutic injection; patient continues to have moderate to severe pain (≥6/10 or disability); engaged in ongoing active conservative treatment.*  
> - *Frequency limits: Max 6 per spinal region in year 1 (up to 3 initial + 3 therapeutic); max 4 per 12 months thereafter (up to 6 if elderly severe stenosis non-operative candidate). Minimum 7 days between different regions.*  
>  
> **Contraindications:** *Active systemic or spinal infection; Skin infection at site of needle puncture; Severe spinal stenosis resulting in intraspinal obstruction.*

#### Proposed Decomposed Logic Structure:
The rule must evaluate a top-level `ANY_OF` across four valid clinical pathways, each enforcing the mandatory pain baseline (pain score $\ge 6$ OR functional disability) and imaging guidance:

| Pathway | Mandatory Clinical Prerequisites | Conservative Therapy Requirement | Key Distinctive Criteria |
| :--- | :--- | :--- | :--- |
| **Pathway 1: Acute Radicular Pain** | Radicular symptoms present; pain duration < 3 months; pain $\ge 6$ or disability; fluoroscopy | $\ge 2$ weeks conservative therapy (active therapy not required) | Acute radiculopathy with short-duration conservative trial |
| **Pathway 2: Spinal Stenosis** | Spinal stenosis on imaging; axial or radicular pain; pain $\ge 6$ or disability; fluoroscopy | $\ge 6$ weeks in prior 6 months (or ongoing if prior injection) | Stenosis confirmed, standard 6w/6m conservative care |
| **Pathway 3: Failed Back Surgery / Fibrosis** | FBSS / epidural fibrosis diagnosis; axial or radicular pain; pain $\ge 6$ or disability; fluoroscopy | $\ge 6$ weeks in prior 6 months (or ongoing if prior injection) | Post-surgical clinical necessity explanation documented |
| **Pathway 4: Pre-Surgical Diagnostic TFESI** | Transforaminal approach; planned surgery; pain $\ge 6$ or disability; fluoroscopy | N/A (Diagnostic) | Documentation of pre-operative surgical plan; $\le 2$ levels per day |

---

### 3.2 RULE-IPM-CGEPIDURALPUMPTRIALS-001 — Single Injection Pump Trials
- **Remediation Reference:** `REM-P3-003` (Priority 3)
- **Clinical Service:** Epidural Spine Injections Single Injection Trials For Intrathecal Pumps 2026 (July)
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Evolent Clinical Guideline 1751 for Epidural Spine Injections and Single Injection Trials for Intrathecal Pumps`
- **Source Citation:** Physical pages 17, 22–23; Printed `Pages 1, 6–7 of 14`
- **Applicable CPT Codes (8 codes):** `62320`, `62321`, `62322`, `62323`, `64479`, `64480`, `64483`, `64484` (Identical procedure codes used when performing temporary intraspinal single injection trials prior to pump implantation)

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGEPIDURALPUMPTRIALS-001",
  "source_page": {"physical_page": 17, "printed_page": "Page 17 of 102"},
  "source_section": "Epidural Spine Injections Single Injection Trials For Intrathecal Pumps 2026 (July)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-CGEPIDURALPUMPTRIALS-001",
        "description": "Clinical criteria satisfied for Epidural Spine Injections Single Injection Trials For Intrathecal Pumps 2026 (July)",
        "parameter": "cgepiduralpumptrials_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 22–23):
> **INDICATIONS FOR INTRASPINAL DRUG TRIAL:**  
> **Chronic Intractable Pain in Non-Terminal Individuals (ALL the following criteria must be met):**  
> - *Pain causing functional disability that significantly interferes with activities of daily living, including ability to work and overall quality of life OR persistent pain level of ≥ 6 on a scale of 0 to 10 despite treatment*  
> - *Failure to respond to non-operative conservative therapy targeting the requested spinal region for a minimum of 12 weeks unless the medical reason this treatment cannot be done is clearly documented*  
>  
> **Spasticity in Non-Terminal Individuals (ALL the following must be met):**  
> - *Intractable spasticity that results in the individual’s inability to maintain an upright posture, severely impairs balance in ambulation, or significantly interferes with activities of daily living related to ONE of the following conditions:*  
>   - *Spinal cord injury*  
>   - *Multiple sclerosis*  
>   - *Stiff person syndrome*  
>   - *Other medical conditions causing intractable spasms*  
> - *Failure to respond to a minimum of 12 weeks of non-operative conservative therapy (e.g., oral medications, physical therapy, etc.)*  
>  
> **Additional Trials:**  
> - *A second intraspinal drug trial is indicated when documentation of the first trial of intraspinal (intrathecal or epidural) medication administered as a bolus or by continuous infusion resulted in one of the following:*  
>   - *Less than 50% pain relief*  
>   - *Intolerable side effects*  
> - *Limit of two intraspinal drug trials for preliminary consideration of chronic intractable pain or spasticity management with permanent implantable device in non-terminal individuals.*  
> - *NOTE: Intrathecal trials are not indicated in opioid-naïve individuals.*  
>  
> **Contraindications for Intraspinal Drug Trial:** *Active systemic or spinal infection; Body habitus that is insufficient to support the weight and bulk of the device.*  
> **Exclusions:** *Implantation of intrathecal catheters or ports for chemotherapy; Post-operative pain control; Caudal or spinal anesthesia for surgery.*

#### Proposed Decomposed Logic Structure:
The rule must enforce three core pathways under a top-level `ANY_OF`:
1. **Intractable Pain Pathway:** Pain $\ge 6/10$ or functional disability; non-terminal patient; failure of $\ge 12$ weeks conservative therapy; verified **not opioid-naïve** (`patient_is_opioid_naive == False`); trial count $\le 2$.
2. **Intractable Spasticity Pathway:** Non-terminal patient; qualifying underlying etiology (SCI, MS, Stiff Person Syndrome, severe intractable spasticity); functional impairment (inability to maintain upright posture, impaired ambulation balance, ADL interference); failure of $\ge 12$ weeks conservative care; trial count $\le 2$.
3. **Second Trial Qualification:** First trial documented $< 50\%$ relief OR intolerable side effects; total trial count $= 2$.

---

### 3.3 RULE-IPM-CGFACETBLOCKS-001 — Paravertebral Facet Joint Injections / Blocks
- **Remediation Reference:** `REM-P3-004` (Priority 3)
- **Clinical Service:** Paravertebral Facet Joint Injection or Blocks 2026 (July)
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Evolent Clinical Guideline 1753 for Paravertebral Facet Joint Injections or Blocks`
- **Source Citation:** Physical pages 31, 32–34; Printed `Pages 1, 2–4 of 14`
- **Applicable CPT Codes (12 codes):**
  - Cervical/Thoracic: `64490` (single level), `64491` (2nd level), `64492` (3rd+ level); Ultrasound: `0213T`, `0214T`, `0215T`
  - Lumbar/Sacral: `64493` (single level), `64494` (2nd level), `64495` (3rd+ level); Ultrasound: `0216T`, `0217T`, `0218T`

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGFACETBLOCKS-001",
  "source_page": {"physical_page": 31, "printed_page": "Page 31 of 102"},
  "source_section": "Paravertebral Facet Joint Injection or Blocks 2026 (July)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-CGFACETBLOCKS-001",
        "description": "Clinical criteria satisfied for Paravertebral Facet Joint Injection or Blocks 2026 (July)",
        "parameter": "cgfacetblocks_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 32–34):
> **INDICATIONS FOR FACET JOINT INJECTIONS OR MEDIAL BRANCH NERVE BLOCKS:**  
> **Facet Joint Pain (ALL the following must be met):**  
> - *Pain that:*  
>   - *Is causing functional disability or average pain level of ≥ 6 (scale of 0 to 10) related to the requested spinal region*  
>   - *Duration for at least 3 months*  
>   - *Is either:*  
>     - *By history, mainly axial or non-radicular*  
>     - *Is radicular due to stenosis caused by synovial cyst (confirmed on imaging)*  
>   - *Is of primary source that is not sacroiliac joint pain, discogenic pain, disc herniation, or radiculitis*  
> - *If diagnosed chronic lumbar spondylolysis: Imaging studies confirming the presence of a pars interarticularis fracture/defect are required.*  
> - *Failure to respond to non-operative conservative treatment* targeting the requested spinal region for a minimum of six (6) weeks in the last six (6) months unless the medical reason this treatment cannot be done is clearly documented (or details of ongoing conservative treatment if prior spinal injections in the same region).*  
>  
> **Imaging Guidance:**  
> - *ALL procedures must be performed under imaging guidance.*  
> - *The facet joint is commonly identified under image guidance by Computed tomography (CT) or Fluoroscopy. Medial Branch Blocks are commonly identified by Fluoroscopy. Ultrasound guidance can be an effective alternative if CT or fluoroscopy guided techniques are contraindicated; however, individual patient factors... may contribute to substandard image resolution.*  
>  
> **Repeat Injections:**  
> - *Initial Diagnostic Phase: Up to 2 diagnostic injections, no sooner than 2 weeks apart (or 7 days if local anesthetic only), provided at least 50% pain relief or significant documented functional improvement is obtained.*  
> - *Therapeutic Phase: Only after initial diagnostic phase if: initial therapeutic subsequent to successful diagnostic phase providing ≥ 50% relief; ≥ 50% pain relief for minimum 2 months before each repeat; continues pain ≥ 6/10 or disability; ongoing active conservative treatment.*  
> - *Frequency limits: Max 2 diagnostic procedures; max 4 facet procedures per 12 months per spinal region. Interval ≥ 7 days between different regions.*  
>  
> **Exclusions:** *Sacral lateral branch blocks (S1, S2, S3); Atlantoaxial joint injections (C1-2); Occipital nerve blocks; Hardware injection or block for diagnosis or treatment of post-surgical or other spine pain.*

#### Proposed Decomposed Logic Structure:
The rule evaluates three alternative presentation pathways under a top-level `ANY_OF`:
1. **Axial Facetogenic Pain Pathway:** Pain duration $\ge 3$ months; pain score $\ge 6/10$ or functional disability; axial non-radicular pain; exclusion of primary SIJ, discogenic, or radicular pain; conservative therapy failure $\ge 6$ weeks within last 6 months; imaging guidance (fluoroscopy or CT; ultrasound only with documented fluoro/CT contraindication).
2. **Synovial Cyst Radiculopathy Pathway:** Radicular symptoms secondary to facet synovial cyst confirmed on MRI/CT; pain $\ge 6/10$ or disability; failed conservative therapy $\ge 6$ weeks in last 6 months; imaging guidance.
3. **Chronic Spondylolysis Pathway:** Chronic lumbar spondylolysis with confirmed pars interarticularis defect/fracture on imaging; pain $\ge 6/10$ or disability; duration $\ge 3$ months; failed conservative therapy $\ge 6$ weeks; imaging guidance.

---

### 3.4 RULE-IPM-CGFACETDENERVATION-001 — Paravertebral Facet Joint Denervation / RFA
- **Remediation Reference:** `REM-P3-005` (Priority 3)
- **Clinical Service:** Paravertebral Facet Joint Denervation 2026 (July)
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Evolent Clinical Guideline 1754 for Paravertebral Facet Joint Denervation (Radiofrequency Neurolysis)`
- **Source Citation:** Physical pages 45, 46–48; Printed `Pages 1, 2–4 of 12`
- **Applicable CPT Codes (4 codes):**
  - Cervical/Thoracic: `64633` (single facet joint), `64634` (each additional facet joint)
  - Lumbar/Sacral: `64635` (single facet joint), `64636` (each additional facet joint)

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGFACETDENERVATION-001",
  "source_page": {"physical_page": 46, "printed_page": "Page 46 of 102"},
  "source_section": "Paravertebral Facet Joint Denervation 2026 (July)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-CGFACETDENERVATION-001",
        "description": "Clinical criteria satisfied for Paravertebral Facet Joint Denervation 2026 (July)",
        "parameter": "cgfacetdenervation_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 46–48):
> **INDICATIONS FOR PARAVERTEBRAL FACET JOINT DENERVATION (RADIOFREQUENCY NEUROLYSIS):**  
> **Facet Joint Pain (ALL of the following must be met):**  
> - *Pain that:*  
>   - *Is causing functional disability or average pain level of ≥ 6 on a scale of 0 to 10 related to the requested spinal region*  
>   - *Is of at least 3 months duration*  
>   - *For radiofrequency ablation following diagnostic medial branch blocks, a positive response to at least one local anesthetic block of the facet joint nerves (medial branch blocks) with at least 70% pain relief or improved ability to function for a minimal duration at least equal to that of the local anesthetic, but with insufficient sustained relief (less than 3 months duration) documented as:*  
>     - *Continued pain, after the diagnostic relief period, causing functional disability or average pain level of ≥ 6 on a scale of 0 to 10 related to the requested spinal region*  
>   - *Is not primarily sacroiliac joint pain, discogenic pain, disc herniation, or radiculitis*  
> - *Failure of conservative treatment* for a minimum of six (6) weeks in the last six (6) months*  
>  
> **Imaging Guidance:**  
> - *All procedures must be performed using fluoroscopic or CT guidance.*  
>  
> **Repeat Procedures:**  
> - *Positive response to prior radiofrequency denervation procedures with at least 50% pain relief or improved ability to function for at least 4 months.*  
> - *The individual continues to have pain causing functional disability or average pain level ≥ 6 on a scale of 0-10 related to the requested spinal region.*  
> - *The individual is engaged in ongoing non-operative conservative treatment* unless the medical reason this treatment cannot be done is clearly documented.*  
> - *A maximum of 2 facet denervation procedures may be performed in a 12-month period per spinal region.*  
>  
> **Exclusions:** *Radiofrequency denervation of the sacroiliac joint and/or sacral lateral branches (S1, S2, S3).*  
> **Contraindications:** *Active systemic or spinal infection; Skin infection at site of needle puncture.*

#### Proposed Decomposed Logic Structure:
Evaluates two primary pathways:
1. **Initial Facet Radiofrequency Neurolysis:**
   - Axial pain duration $\ge 3$ months; pain $\ge 6/10$ or functional disability;
   - Primary pain is not SIJ, discogenic, disc herniation, or radiculitis;
   - Prior diagnostic medial branch block (MBB) documented with **$\ge 70\%$ pain relief** or functional improvement lasting for duration of local anesthetic;
   - Relief from diagnostic MBB was temporary ($< 3$ months) with return of pain $\ge 6/10$ or disability;
   - Failure of $\ge 6$ weeks conservative care within last 6 months;
   - Fluoroscopic or CT guidance (ultrasound prohibited).
2. **Repeat Facet Radiofrequency Neurolysis:**
   - Prior RFA provided **$\ge 50\%$ pain relief** or functional improvement for **$\ge 4$ months**;
   - Recurrence of pain $\ge 6/10$ or functional disability;
   - Active engagement in ongoing non-operative conservative treatment;
   - Frequency $\le 2$ procedures per 12 months per spinal region;
   - Fluoroscopic or CT guidance.

---

### 3.5 RULE-IPM-CGFACETDENERVATION-002 — Facet Denervation Relief Threshold Alignment
- **Remediation Reference:** `REM-P3-006` (Priority 3)
- **Clinical Service:** Facet Joint Radiofrequency Neurotomy / Denervation
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Paravertebral Facet Joint Denervation 2026 / Diagnostic Block Prerequisites`
- **Source Citation:** Physical pages 46–47; Printed `Pages 2–3 of 12`
- **Target Rule Role:** Standalone prerequisite / threshold rule linked to `RULE-IPM-CGFACETDENERVATION-001`.

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGFACETDENERVATION-002",
  "source_page": {"physical_page": 46, "printed_page": "Page 46 of 102"},
  "source_section": "Paravertebral Facet Joint Denervation 2026 / Diagnostic Block Prerequisites",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-FACET-RFA-DIAG",
        "description": "Documented positive pain relief from prior diagnostic facet joint blocks",
        "parameter": "diagnostic_facet_block_relief",
        "comparator": "GREATER_THAN_OR_EQUAL",
        "value": 50,
        "unit": "%"
      }
    ]
  }
}
```

#### Diagnostic Threshold Analysis & Discrepancy Reconciliation:
- **Historical Register Summary:** The Phase 8A / 8B.6 register proposed: *"confirm dual 80% (initial) vs 50% (repeat) threshold semantics."*
- **Authoritative Text Verification:**
  - Examination of physical page 46 reveals that for initial RFA following diagnostic medial branch blocks, Evolent explicitly mandates **at least 70% pain relief** (*"positive response to at least one local anesthetic block of the facet joint nerves (medial branch blocks) with at least 70% pain relief or improved ability to function"*).
  - Physical page 47 explicitly mandates for repeat procedures **at least 50% pain relief** (*"with at least 50% pain relief or improved ability to function for at least 4 months"*).
  - The 80% figure originates in literature guidelines (e.g. ASIPP Delphi recommendations) but is **not** the threshold codified in the 2026 Evolent policy. Setting the threshold to 80% would cause wrongful denials for clinical requests demonstrating 70%–79% relief.
- **Proposed Logic Realignment:**
  - Structure `RULE-IPM-CGFACETDENERVATION-002` to evaluate either:
    1. **Initial RFA Relief:** `diagnostic_facet_block_relief >= 70%` (or functional improvement documented); OR
    2. **Repeat RFA Relief:** `prior_rfa_relief >= 50%` AND `prior_rfa_relief_duration_months >= 4`.
  - Update citation to Physical Page 46–47; Printed `Pages 2–3 of 12`.

---

### 3.6 RULE-IPM-CGSIINJECTIONS-001 — Sacroiliac Joint Injections
- **Remediation Reference:** `REM-P3-007` (Priority 3)
- **Clinical Service:** Sacroiliac Joint Injections 2026 (July)
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Evolent Clinical Guideline 1756 for Sacroiliac Joint Injections`
- **Source Citation:** Physical pages 57, 58–60; Printed `Pages 1, 2–4 of 10`
- **Applicable CPT Codes (2 codes):** `27096` (fluoroscopy/CT guided), `G0260` (sacroiliac injection)

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGSIINJECTIONS-001",
  "source_page": {"physical_page": 57, "printed_page": "Page 57 of 102"},
  "source_section": "Sacroiliac Joint Injections 2026 (July)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-CGSIINJECTIONS-001",
        "description": "Clinical criteria satisfied for Sacroiliac Joint Injections 2026 (July)",
        "parameter": "cgsiinjections_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 58–60):
> **INDICATIONS FOR SACROILIAC JOINT INJECTIONS (INTRAARTICULAR OR LIGAMENTOUS INJECTIONS ONLY):**  
> **Sacroiliac Joint Pain (ALL of the following must be met):**  
> - *Primarily axial low back pain (below level of L5) which may radiate to the groin or lower extremity*  
> - *Pain causing functional disability or average pain level of ≥ 6 on a scale of 0 to 10 related to the requested spinal region*  
> - *A cluster of any three (3) of the following positive provocation exam findings to suggest the diagnosis (5,6,7):*  
>   1. *Pelvic (SI) distraction test*  
>   2. *Pelvic (SI) compression test*  
>   3. *Sacral Thrust test*  
>   4. *FABER (Patrick’s test)*  
>   5. *Posterior shear test*  
>   6. *Yeoman’s test*  
>   7. *Gaenslen’s test*  
>   8. *Thigh Thrust test*  
> - *Duration of pain of at least 3 months*  
> - *Failure to respond to non-operative conservative treatment targeting the requested spinal region for a minimum of 6 weeks in the last 6 months unless the medical reason this treatment cannot be done is clearly documented (or ongoing if prior injections)*  
>  
> **Spondyloarthropathy (ALL of the following must be met):**  
> - *The individual has experienced ≥ 3 months of low back pain*  
> - *Age of onset < 45 years*  
> - *Comprehensive pain management program is in place including physical therapy, home exercise, patient education, psychosocial support, and/or oral medication*  
> - *Prior history of evidence of sacroiliitis on imaging (i.e., active inflammation on MRI or definite radiographic sacroiliitis grade 2-4 bilaterally or grade 3-4 unilaterally)*  
> - *1 or more spondyloarthropathy features (Inflammatory back pain with ≥4 criteria; Arthritis; Enthesitis of heel; Uveitis; Dactylitis; Psoriasis; Crohn’s/colitis; Good NSAID response; Family history; Positive HLA-B27; Elevated CRP)*  
>  
> **Diagnostic Purposes for Surgical Planning (ALL must be met):**  
> - *Image-guided, contrast-enhanced intra-articular injection*  
> - *At least 75% pain relief for expected duration of anesthetic*  
> - *Continued pain causing disability or pain ≥ 6/10 after relief period*  
> - *No more than 2 diagnostic injections per diagnostic phase*  
> - *Documentation of pre-operative evaluation and plan for SIJ surgery*  
>  
> **Imaging Guidance:** *ALL procedures must be performed under imaging guidance (Fluoroscopy, CT, or Ultrasound if fluoroscopy/CT contraindicated).*  
> **Exclusions:** *Sacral lateral branch blocks (S1, S2, S3); Radiofrequency denervation of the sacroiliac joint.*

#### Proposed Decomposed Logic Structure:
Evaluates three independent pathways under a top-level `ANY_OF`:
1. **Mechanical Sacroiliac Joint Pain Pathway:** Axial pain below L5; pain score $\ge 6/10$ or disability; duration $\ge 3$ months; **$\ge 3$ of 8 positive provocative physical exam tests**; failure of $\ge 6$ weeks conservative therapy in prior 6 months; imaging guidance.
2. **Spondyloarthropathy Sacroiliitis Pathway:** Low back pain $\ge 3$ months; age of onset $< 45$ years; comprehensive conservative pain management in place; imaging evidence of sacroiliitis (MRI active inflammation or X-ray sacroiliitis grade 2–4 bilaterally / 3–4 unilaterally); $\ge 1$ qualifying spondyloarthropathy feature.
3. **Pre-Surgical SIJ Diagnostic Pathway:** Image-guided contrast-enhanced intra-articular injection; documented pre-operative evaluation and surgical plan for SI joint fusion/surgery; relief $\ge 75\%$ from diagnostic block; $\le 2$ diagnostic injections.

---

### 3.7 RULE-IPM-CGSPINALCORDSTIM-001 — Spinal Cord Stimulation Trial
- **Remediation Reference:** `REM-P3-008` (Priority 3)
- **Clinical Service:** Spinal Cord Stimulation 2026 (July)
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Evolent Clinical Guideline 1757 for Spinal Cord Stimulation`
- **Source Citation:** Physical pages 77, 78–80; Printed `Pages 1, 2–4 of 12`
- **Applicable CPT Codes (8 codes):**
  - Percutaneous trial / array: `63650`, Laminectomy paddle: `63655`
  - Array removal: `63661`, `63662`; Array revision: `63663`, `63664`
  - Generator implant: `63685`; Generator revision/removal: `63688`

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGSPINALCORDSTIM-001",
  "source_page": {"physical_page": 78, "printed_page": "Page 78 of 102"},
  "source_section": "Spinal Cord Stimulation 2026 (July)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-CGSPINALCORDSTIM-001",
        "description": "Clinical criteria satisfied for Spinal Cord Stimulation 2026 (July)",
        "parameter": "cgspinalcordstim_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 78–80):
> **INDICATIONS:**  
> *All patients colonized with methicillin-sensitive or methicillin-resistant Staphylococcus aureus (MRSA or MSSA) must have a decolonization plan to be performed no earlier than 10 days prior to the planned procedure.*  
>  
> **Spinal Cord Stimulation (SCS Trial — ALL the following criteria must be met):**  
> - *Pain that:*  
>   - *Is causing functional disability or average pain level of ≥ 6 on a scale of 0 to 10*  
>   - *Is of at least 6 months duration*  
>   - *Is caused by at least one of the following:*  
>     - *Failed spine surgery syndrome (FSSS) / persistent spinal pain syndrome (PSPS) or post-laminectomy syndrome*  
>     - *Complex regional pain syndrome (CRPS), type I or type II, meeting Budapest criteria*  
>     - *Chronic neuropathic pain of certain origins (Lumbosacral arachnoiditis; Post herpetic neuralgia; Radiculopathy; Chronic ischemic leg pain; Diabetic peripheral neuropathy; Phantom limb syndrome [stump pain]; Peripheral neuropathy; Chronic back pain [neuropathic] and not a surgical candidate; Chronic refractory angina pectoris [NYHA III/IV, post-PCI/CABG, not candidate for revascularization, failed optimal meds ≥ 1 month])*  
> - *Failure to respond to non-operative conservative treatment (e.g., medication trials, interventional procedures) for a minimum of 6 months unless the medical reason this treatment cannot be done is clearly documented*  
> - *A completed presurgical psychological assessment that documents ALL four of the following:*  
>   1. *Pain is not due to psychiatric disorders such as depression, anxiety, somatic symptom disorder, or sequelae of substance use*  
>   2. *Satisfactory management of personality and psychiatric disorders*  
>   3. *Satisfactory management of substance use disorder in recovery*  
>   4. *Demonstration of cognitive ability to manage the stimulator*  
>  
> **Dorsal Root Ganglion Stimulator (DRGS Trial — ALL must be met):**  
> - *Pain causing functional disability or average pain level ≥ 6/10; Duration ≥ 6 months; Caused by CRPS affecting the lower limbs (type I or II, meeting Budapest criteria); Failure of conservative treatment for minimum 6 months; Completed presurgical psychological assessment meeting all 4 elements.*  
>  
> **Contraindications:** *Active systemic or spinal infection; Body habitus insufficient to support device; Coagulation disorder; Pregnancy.*

#### Proposed Decomposed Logic Structure:
Evaluates two primary trial pathways under an `ANY_OF`:
1. **Spinal Cord Stimulation (SCS) Trial Pathway:**
   - Pain duration $\ge 6$ months; pain score $\ge 6/10$ or functional disability;
   - Underlying etiology is at least one of: FBSS/PSPS, CRPS Type I/II (Budapest criteria), or qualifying chronic neuropathic pain (radiculopathy, arachnoiditis, DPN, PHN, phantom limb, ischemic leg pain, nonsurgical neuropathic back pain, or refractory angina NYHA III/IV);
   - Failure of $\ge 6$ months conservative treatment;
   - Presurgical psychological clearance documenting all 4 mandatory elements;
   - Staph colonization decolonization protocol adherence documented.
2. **Dorsal Root Ganglion Stimulation (DRGS) Trial Pathway:**
   - Lower limb CRPS Type I or II meeting Budapest criteria; pain duration $\ge 6$ months; pain $\ge 6/10$ or disability; failure of $\ge 6$ months conservative therapy; completed 4-element psychological clearance.

---

### 3.8 RULE-IPM-CGSYMPATHETICBLOCKS-001 — Sympathetic Nerve Blocks
- **Remediation Reference:** `REM-P3-009` (Priority 3)
- **Clinical Service:** Sympathetic Nerve Blocks 2026 (July)
- **Governing Policy:** `2026 Evolent Interventional Pain Management Guidelines.pdf`
- **Section:** `Evolent Clinical Guideline 1758 for Sympathetic Nerve Blocks`
- **Source Citation:** Physical pages 89, 91–96; Printed `Pages 1, 3–8 of 14`
- **Applicable CPT Codes (4 codes):**
  - `64510`: Stellate ganglion block (cervical sympathetic)
  - `64517`: Superior hypogastric plexus block
  - `64520`: Thoracic or lumbar sympathetic block
  - `64530`: Celiac plexus block

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-CGSYMPATHETICBLOCKS-001",
  "source_page": {"physical_page": 89, "printed_page": "Page 89 of 102"},
  "source_section": "Sympathetic Nerve Blocks 2026 (July)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-CGSYMPATHETICBLOCKS-001",
        "description": "Clinical criteria satisfied for Sympathetic Nerve Blocks 2026 (July)",
        "parameter": "cgsympatheticblocks_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 91–96):
> **INDICATIONS — General Indications:**  
> - *Acute or chronic noncancer pain causing functional disability or average pain level of ≥ 6 on a scale of 0 to 10 prior to injection AND continuation of pain or functional disability after the relief period due to the block*  
> - *Cancer pain affecting quality of life prior to injection and continuation after the relief period due to the block*  
> - *Each block must be performed under image guidance (ultrasound NOT permitted for lumbar, thoracic, or superior hypogastric blocks)*  
> - *Interval of at least one week since prior injection. Bilateral blocks will NOT be performed on the same day.*  
>  
> **1. Stellate Ganglion Block (CPT 64510 — Face, upper extremities, upper thorax):**  
> - *Acute Herpes Zoster: Pain duration < 4 weeks AND active antiviral therapy regimen*  
> - *Cancer pain or phantom limb pain: Failure to respond to nonoperative conservative treatment*  
> - *CRPS types I and II (Budapest criteria): Failure to respond to functional restoration modalities (PT, OT, pain psychology) AND active participation in ongoing functional restoration*  
> - *Repeat block: Previous block resulted in ≥ 50% relief or functional improvement for at least the duration of local anesthetic. Max 6 in first 12 weeks; max 4 per 12 months thereafter.*  
>  
> **2. Thoracic or Lumbar Sympathetic Block (CPT 64520 — Lower extremities):**  
> - *Acute Herpes Zoster: Pain duration < 4 weeks AND active antiviral therapy*  
> - *Cancer pain, phantom limb, or nonsurgical ischemic limb pain: Failure of conservative treatment*  
> - *CRPS types I and II (Budapest criteria): Failure of functional restoration and active participation*  
> - *Repeat: Previous block ≥ 50% relief for duration of anesthetic. Max 6 per 12 months (or max 6 in 12 weeks for CRPS).*  
>  
> **3. Celiac Plexus Block (CPT 64530 — Upper abdomen):**  
> - *Malignancy-associated upper abdominal pain: Diagnostic block for planned neurolysis (conservative therapy NOT required; up to 2 diagnostic blocks)*  
> - *Chronic relapsing pancreatitis: Failed conservative treatment; repeat every 3 months if ≥ 50% relief for 3 months.*  
>  
> **4. Superior Hypogastric Plexus Block (CPT 64517 — Pelvis / rectum):**  
> - *Malignancy-associated pelvic or rectal pain: Diagnostic block for planned neurolysis (conservative therapy NOT required; up to 2 diagnostic blocks)*  
> - *Chronic noncancer pelvic/rectal visceral pain: Failed conservative treatment; repeat every 3 months if ≥ 50% relief for 3 months.*  
>  
> **Exclusions:** *Sphenopalatine ganglion block; Ganglion impar block; Other parasympathetic ganglion blocks; Inferior hypogastric block.*

#### Proposed Decomposed Logic Structure:
Evaluates four anatomical block modalities under an `ANY_OF`:
1. **Stellate Ganglion Block (64510):** Pain $\ge 6/10$ or cancer quality-of-life impact; unilateral procedure; image-guided; qualifying indication (acute zoster $<4$w with antivirals, cancer pain, phantom limb, or CRPS with functional restoration).
2. **Thoracic / Lumbar Sympathetic Block (64520):** Pain $\ge 6/10$ or cancer pain; unilateral; fluoroscopy/CT (no ultrasound); qualifying indication (acute zoster $<4$w with antivirals, cancer pain, phantom limb, ischemic limb pain, or CRPS).
3. **Celiac Plexus Block (64530):** Malignancy-associated upper abdominal pain (no conservative therapy required) OR chronic pancreatitis with failed conservative therapy.
4. **Superior Hypogastric Plexus Block (64517):** Pelvic/rectal malignancy-associated pain (no conservative care required) OR chronic visceral pelvic pain with failed conservative care; fluoroscopy/CT guided.

---

### 3.9 RULE-IPM-EPOS1755-001 — Place of Service Policy 1755 Clinical Exceptions
- **Remediation Reference:** `REM-P3-010` (Priority 3)
- **Clinical Service:** Evolent Place of Service Policy 1755 for Interventional Pain Management (2026 Final)
- **Governing Policy:** `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf`
- **Section:** `PATIENT CRITERIA FOR SELECTION OF OUTPATIENT HOSPITAL SETTING`
- **Source Citation:** Physical pages 1, 3–4; Printed `Pages 1, 3–4 of 8`
- **Decision Track:** `PLACE_OF_SERVICE`

#### Current Rule Definition:
```json
{
  "rule_id": "RULE-IPM-EPOS1755-001",
  "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
  "source_section": "Evolent Place of Service Policy 1755 for Interventional Pain Management (2026 Final)",
  "conditions": {
    "operator": "SINGLE_CONDITION",
    "criteria": [
      {
        "condition_id": "COND-IPM-EPOS1755-001",
        "description": "Clinical criteria satisfied for Evolent Place of Service Policy 1755 for Interventional Pain Management (2026 Final)",
        "parameter": "epos1755_indication",
        "comparator": "IS_PRESENT"
      }
    ]
  }
}
```

#### Authoritative Policy Passages (Physical Pages 2–4):
> **LEVEL OF CARE:**  
> *Patients having elective interventional pain management procedures will generally be managed in a physician office or ambulatory surgery center (ASC) setting. It is expected that most patients undergoing these procedures will not require outpatient hospital level care or observation.*  
>  
> **PATIENT CRITERIA FOR SELECTION OF OUTPATIENT HOSPITAL SETTING:**  
> *In certain circumstances, a patient will qualify for care in an outpatient hospital. Outpatient hospital care will be deemed appropriate when ANY of the following criteria are met:*  
> *NOTE: All criteria require additional documentation from the treating physician and/or primary care physician.*  
> - **American Society of Anesthesiologists® Physical Status (ASA® PS) score ≥ 3**  
> - **Body Mass Index (BMI) ≥ 40 with or without obesity-related condition or unmanaged comorbidities**  
> - **Patient has one or more moderate to severe health conditions, including, but not limited to, ANY of the following:**  
>   - *Heart problems (prior heart surgery, heart attack, heart failure, coronary artery disease/stents, arrhythmia, pacemaker, or defibrillator)*  
>   - *Lung problems (COPD or asthma)*  
>   - *Chronic kidney or liver problems (kidney failure or cirrhosis/active hepatitis)*  
>   - *Blood clots or bleeding disorder*  
>   - *Stroke or TIA (transient ischemic attack)*  
>   - *High blood pressure that requires 3 or more drugs to control*  
>   - *Poorly controlled diabetes*  
>   - *Cognitive impairment or dementia*  
>   - *Pregnancy*  
>   - *Substance use disorders (cannabis, hallucinogen, inhalant, opioid, sedative/hypnotic/anxiolytic, stimulant, alcohol)*  
>   - *Prior anesthesia complications (personal or family history)*  
>   - *Difficult airway anticipated*  
>   - *Sleep apnea*  
>   - *History of anaphylaxis to medication, latex, or iodine*

#### Proposed Decomposed Logic Structure:
Evaluates a top-level `ANY_OF` across the source-defined clinical exceptions for Outpatient Hospital care (POS 22 or POS 19):
1. `asa_physical_status_score >= 3`
2. `bmi >= 40` *(reconciled from register error stating 45)*
3. Cardiovascular comorbidity (`heart_problems == True`)
4. Pulmonary disease (`chronic_lung_disease == True`)
5. Renal or hepatic impairment (`chronic_kidney_or_liver_disease == True`)
6. Coagulopathy or bleeding disorder (`bleeding_disorder_or_anticoagulation == True`)
7. Cerebrovascular disease (`stroke_or_tia_history == True`)
8. Resistant hypertension (`hypertension_requiring_3_or_more_drugs == True`)
9. Poorly controlled diabetes (`poorly_controlled_diabetes == True`)
10. Cognitive impairment (`cognitive_impairment_or_dementia == True`)
11. Pregnancy (`pregnancy_status == True`)
12. Substance use disorder (`active_substance_use_disorder == True`)
13. Anesthesia complication history (`prior_anesthesia_complications == True`)
14. Airway risk (`difficult_airway_anticipated == True` or `sleep_apnea == True`)
15. Severe anaphylaxis history (`history_of_anaphylaxis == True`)

---

## 4. Distinction Between Clinical Necessity and Place of Service Decision Tracks

A fundamental architectural distinction within the MedRule engine is the separation of **Clinical Necessity** from **Place of Service (POS)**. 

```
                                  INCOMING IPM PRIOR AUTH REQUEST
                                                 │
                      ┌──────────────────────────┴──────────────────────────┐
                      ▼                                                     ▼
           DECISION TRACK 1:                                     DECISION TRACK 2:
           CLINICAL NECESSITY                                    PLACE OF SERVICE (POS)
  (e.g., RULE-IPM-CGEPIDURALINJECTIONS-001)               (RULE-IPM-EPOS1755-001 & EPOS1755-002)
                      │                                                     │
        Is the procedure medically                           Is the requested facility
        indicated for this patient?                           level appropriate?
                      │                                                     │
         ┌────────────┴────────────┐                           ┌────────────┴────────────┐
         ▼                         ▼                           ▼                         ▼
      INDICATED              NOT INDICATED               AMBULATORY PREFERRED      HOSPITAL REQUESTED
         │                         │                     (POS 11 / POS 24)         (POS 22 / POS 19)
         │                         ▼                           │                         │
         │                  FINAL OUTCOME:                     ▼                         ▼
         │                      DENIED                     SATISFIED           Evaluates EPOS1755-001
         │                                               (RULE-IPM-EPOS1755-002)   Clinical Exceptions
         │                                                     │                         │
         │                                                     │           ┌─────────────┴─────────────┐
         │                                                     │           ▼                           ▼
         │                                                     │      EXCEPTION MET               NO EXCEPTION
         │                                                     │   (ASA≥3, BMI≥40, etc.)       (Healthy patient)
         │                                                     │           │                           │
         │                                                     │           ▼                           ▼
         │                                                     └───► POS INDICATED              POS REDIRECTED
         │                                                             │                         (Deny Hospital POS)
         └──────────────────────────────┬──────────────────────────────┘
                                        ▼
                                  FINAL OUTCOME:
                             APPROVED AT SPECIFIED POS
```

### 4.1 Independent Dual-Track Architecture
1. **Clinical Necessity Track (`DecisionTrack.CLINICAL_NECESSITY`):**
   - Eight of the nine target rules (`CGEPIDURALINJECTIONS-001`, `CGEPIDURALPUMPTRIALS-001`, `CGFACETBLOCKS-001`, `CGFACETDENERVATION-001`, `CGFACETDENERVATION-002`, `CGSIINJECTIONS-001`, `CGSPINALCORDSTIM-001`, `CGSYMPATHETICBLOCKS-001`) belong strictly to this track.
   - They evaluate whether the clinical presentation justifies the interventional procedure itself (e.g. pain severity, pathology, duration, failure of conservative therapy, diagnostic prerequisites).
2. **Place of Service Track (`DecisionTrack.PLACE_OF_SERVICE`):**
   - Rules `RULE-IPM-EPOS1755-001` and `RULE-IPM-EPOS1755-002` belong strictly to this track.
   - They govern **where** the procedure may be performed. Under EPOS 1755, office (POS 11) and ambulatory surgery centers (POS 24) are the preferred ambulatory sites (`RULE-IPM-EPOS1755-002`). If an outpatient hospital setting (POS 22 or POS 19) is requested, `RULE-IPM-EPOS1755-001` evaluates whether patient comorbidities (ASA score, BMI, cardiopulmonary status, bleeding risk) justify hospital-level care.
3. **Decoupled Engine Outcomes:**
   - A clinical request can be `INDICATED` for the procedure but have its facility setting redirected to an ASC or office if hospital exception criteria are not met.
   - Conversely, a patient meeting hospital exception criteria (e.g. ASA 3 with CAD) cannot receive prior authorization if the clinical necessity rule itself fails (e.g. no radiculopathy or inadequate conservative therapy).

---

## 5. Handling Missing, Ambiguous, and Conflicting Evidence (Three-Valued Engine Logic)

The MedRule deterministic engine implements rigorous **three-valued logic** (`MET`, `NOT_MET`, `INDETERMINATE`) across all condition trees.

### 5.1 Representation of Unknowns and Missing Evidence
- **Primary Clinical Parameters:** If an essential evidence parameter (e.g., `conservative_therapy_duration_weeks`, `pain_intensity_score_numeric`, `diagnostic_facet_block_relief`) is absent from the case record, the condition evaluates to `INDETERMINATE`.
- **Three-Valued Operator Semantics:**
  - `AND` / `ALL_OF`: Evaluates to `NOT_MET` if any operand is `NOT_MET`. If no operand is `NOT_MET` but one or more operands are `INDETERMINATE`, the compound expression returns `INDETERMINATE`. It returns `MET` only when all operands evaluate to `MET`.
  - `OR` / `ANY_OF`: Evaluates to `MET` if any operand is `MET`. If no operand is `MET` but one or more operands are `INDETERMINATE`, the compound expression returns `INDETERMINATE`. It returns `NOT_MET` only when all operands evaluate to `NOT_MET`.
- **Pre-Auth Workflow Action:** An overall outcome of `INDETERMINATE` produces a structured `Request for Clinical Information` (RFI) specifying the exact missing fields rather than a clinical denial.

### 5.2 Conflicting Clinical Evidence
- In clinical charts, conflicting records may exist (e.g. clinic notes stating "80% pain relief" while physical therapy documentation notes "no improvement").
- The MedRule engine handles conflicting inputs by detecting parameter value collisions across date-stamped notes. Where conflicts cannot be resolved deterministically, the engine outputs `INDETERMINATE_CONFLICT` and routes the case to `NEEDS_HUMAN_REVIEW`.

---

## 6. Shared Dependencies, Rule Overlaps, and Inter-Procedural Interactions

The 2026 Evolent IPM guidelines contain strict cross-procedure rules and same-day limitations that must be modeled across the rulebook:

### 6.1 Same-Day Multi-Procedure Restrictions
- **General Prohibition:** Across all guidelines (1750, 1751, 1753, 1754, 1756, 1757, 1758), it is explicitly stated: *"It is generally considered not medically necessary to perform multiple interventional pain procedures on the same date of service."*
- **Synovial Cyst Exception:** Guidelines 1750 and 1753 establish an explicit mutual exception: *"Different types of injections in the same spinal region (cervical, thoracic, or lumbar) should not be done on the same day with the exception of a facet injection and epidural steroid injection (ESI) performed during the same session for a synovial cyst confirmed on imaging."*
- **Bilateral Block Prohibitions:** Bilateral stellate ganglion blocks (Guideline 1758, physical page 93) and bilateral thoracic/lumbar sympathetic blocks (physical page 94) are strictly prohibited on the same date of service.

### 6.2 Prior Interventional Procedure Dependencies
- **Repeat SI Joint Testing Prerequisite:** Guideline 1756 (physical page 60) establishes that for patients who have received other lumbar/sacral injections (such as ESI or facet blocks) since their last SIJ injection, repeat authorization requires **at least one repeat positive provocative physical exam finding**.
- **Facet Medial Branch Block vs. Intra-Articular Joint Injection:** Guideline 1753 (physical page 34) and 1754 (physical page 46) mandate that Radiofrequency Ablation (RFA) **cannot be authorized** if the patient only received an intra-articular facet joint injection; prior diagnostic local anesthetic medial branch nerve blocks (MBB) are mandatory.
- **Trial-to-Permanent Progression:**
  - `RULE-IPM-CGSPINALCORDSTIM-001` governs the trial array (CPT 63650 / 63655). `RULE-IPM-CGSPINALCORDSTIM-002` governs the permanent generator implant (CPT 63685), which strictly requires documented trial success ($\ge 50\%$ relief and $\ge 3$ days functional improvement).
  - Similarly, `RULE-IPM-CGEPIDURALPUMPTRIALS-001` governs the single injection drug trial, which serves as a mandatory gate for the permanent implantable infusion pump (`RULE-IPM-CGINFUSIONPUMPS-001`).

---

## 7. Critical Discrepancies, Source Confusions, and Clinical Review Flags

During the rigorous line-by-line examination of the authoritative 2026 PDFs, six key discrepancies and ambiguities were identified between earlier register summaries and the actual authoritative text:

### 🚩 Flag 1: Facet RFA Initial Diagnostic Relief Threshold (70% vs. 80%)
- **Register Summary (`REM-P3-006`):** Proposed confirming *"dual 80% (initial) vs 50% (repeat) threshold semantics."*
- **Authoritative PDF Finding:** In `2026 Evolent Clinical Guideline 1754` (physical page 46), the text explicitly reads:
  > *"positive response to at least one local anesthetic block of the facet joint nerves (medial branch blocks) with at least 70% pain relief or improved ability to function"*
- **Clinical Significance:** While historical literature and certain Medicare LCDs reference 80%, Evolent's 2026 policy sets the threshold at **$\ge 70\%$**. Encoding 80% in the engine would cause inappropriate denials of clinically valid requests.
- **Recommendation:** Implement $\ge 70\%$ for initial RFA diagnostic relief, referencing physical page 46, and document the variance for clinical governance awareness.

### 🚩 Flag 2: Repeat Facet RFA Duration Threshold (4 Months vs. 6 Months)
- **Register Summary:** Older summaries discussed relief lasting $\ge 6$ months for repeat RFA.
- **Authoritative PDF Finding:** In `Guideline 1754` (physical page 47), repeat RFA criteria explicitly state:
  > *"Positive response to prior radiofrequency denervation procedures with at least 50% pain relief or improved ability to function for at least 4 months"*
- **Recommendation:** Implement $\ge 50\%$ relief lasting $\ge 4$ months for repeat RFA, strictly adhering to physical page 47.

### 🚩 Flag 3: Place of Service Morbid Obesity BMI Threshold (BMI $\ge 40$ vs. BMI $\ge 45$)
- **Register Summary (`REM-P3-010`):** Proposed clinical exception for *"BMI >= 45"*.
- **Authoritative PDF Finding:** In `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` (physical page 3), the criterion explicitly reads:
  > *"Body Mass Index (BMI) ≥ 40 with or without obesity-related condition or unmanaged comorbidities"*
- **Clinical Significance:** Class III severe obesity (BMI $\ge 40$) qualifies for outpatient hospital setting under Evolent 2026 policy. Using 45 would inappropriately deny hospital access to patients with BMI 40–44.9.
- **Recommendation:** Encode `bmi >= 40` in accordance with the authoritative EPOS 1755 text.

### 🚩 Flag 4: Acute Radicular ESI Conservative Care Timeframe (2 Weeks vs. 6 Weeks)
- **Authoritative PDF Finding:** In `Guideline 1750` (physical page 7), acute radicular pain ($< 3$ months duration) requires only **a minimum of 2 weeks** of non-operative conservative treatment (and active physical therapy is explicitly not required). In contrast, chronic conditions (stenosis, FBSS) require **a minimum of 6 weeks in the prior 6 months**.
- **Recommendation:** Decompose `RULE-IPM-CGEPIDURALINJECTIONS-001` into distinct pathways so acute patients are not inappropriately held to the 6-week conservative care requirement.

### 🚩 Flag 5: Intraspinal Pump Drug Trials in Opioid-Naïve Individuals
- **Authoritative PDF Finding:** In `Guideline 1751` (physical page 23), an explicit clinical limitation is codified:
  > *"NOTE: Intrathecal trials are not indicated in opioid-naïve individuals"*
- **Recommendation:** Model `patient_is_opioid_naive == False` as a mandatory prerequisite for intraspinal pump trials.

### 🚩 Flag 6: Spinal Cord Stimulation MRSA/MSSA Decolonization Requirement
- **Authoritative PDF Finding:** In `Guideline 1757` (physical page 78), the policy mandates:
  > *"All patients colonized with methicillin-sensitive or methicillin-resistant Staphylococcus aureus (MRSA or MSSA) must have a decolonization plan to be performed no earlier than 10 days prior to the planned procedure."*
- **Recommendation:** Include `staph_colonization_decolonization_plan_met` in the clinical prerequisite criteria for SCS trials.

---

## 8. Comprehensive Risk Analysis

| Risk Category | Specific Risk Description | Severity | Engineered Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Clinical Under-Authorization** | Enforcing obsolete 80% relief for facet RFA or BMI $\ge 45$ for POS exceptions, causing improper denials. | **HIGH** | Strict adherence to verified 2026 PDF text ($\ge 70\%$ MBB relief, BMI $\ge 40$). Documented in Flag 1 and Flag 3. |
| **Clinical Over-Authorization** | Approving RFA after intra-articular facet injection without medial branch blocks, or approving ESI for axial pain without stenosis/FBSS. | **HIGH** | Explicitly encode negative exclusion criteria and mandatory diagnostic MBB prerequisite pathways. |
| **Decision Track Cross-Contamination** | Conflating POS comorbidity exceptions with procedure clinical necessity. | **CRITICAL** | Strict structural decoupling: POS rules execute on `DecisionTrack.PLACE_OF_SERVICE`; injection rules execute on `DecisionTrack.CLINICAL_NECESSITY`. |
| **Governance Invariant Breach** | Accidental mutation of `APPROVED: 0` invariant or unblocking canonical gates (`RULE-IPM-PREAMBLEIPM-001`, `RULE-IPM-CGINFUSIONPUMPS-001`). | **CRITICAL** | All 9 rules remain in `DRAFT` status; `GOVERNANCE_BLOCKED_RULE_IDS` remains untouched; zero production code changes during Phase 8B.8A. |
| **Combinatorial Complexity** | Over-complicating rules with ad-hoc nested trees leading to test maintenance failures. | **MEDIUM** | Standardized condition schema, consistent parameter naming, and clean multi-pathway structures (`ANY_OF` of `ALL_OF` pathways). |

---

## 9. Implementation Batch Planning & First Batch Recommendation

To ensure controlled, test-driven remediation that preserves all system invariants, the nine target rules are divided into three small, logically cohesive implementation batches:

### 9.1 Batch 1: Spine Injections (Epidural & Sacroiliac Joint Injections) — 3 Rules
- **Rules Included:**
  1. `RULE-IPM-CGEPIDURALINJECTIONS-001` (Core ESI clinical decision tree)
  2. `RULE-IPM-CGEPIDURALPUMPTRIALS-001` (Single injection intraspinal trials for IT pumps)
  3. `RULE-IPM-CGSIINJECTIONS-001` (Sacroiliac joint intra-articular injections)
- **Clinical Cohesion:** These rules share common spinal injection delivery mechanics, image guidance requirements (fluoroscopy/CT), pain threshold scales ($\ge 6/10$), and conservative therapy evaluation patterns (2w acute vs 6w chronic vs 12w intraspinal trial).

### 9.2 Batch 2: Facet Interventions & Sympathetic Nerve Blocks — 4 Rules
- **Rules Included:**
  1. `RULE-IPM-CGFACETBLOCKS-001` (Facet joint injections / medial branch blocks)
  2. `RULE-IPM-CGFACETDENERVATION-001` (Facet radiofrequency neurotomy / RFA)
  3. `RULE-IPM-CGFACETDENERVATION-002` (Facet RFA diagnostic relief threshold alignment)
  4. `RULE-IPM-CGSYMPATHETICBLOCKS-001` (Stellate, lumbar, celiac, and hypogastric blocks)
- **Clinical Cohesion:** Tightly couples the facet diagnostic-to-neurotomy continuum (`CGFACETBLOCKS-001` $\rightarrow$ `CGFACETDENERVATION-001` / `002`) and sympathetic diagnostic-to-therapeutic series under unified relief percentage semantics ($\ge 70\%$ initial MBB vs $\ge 50\%$ repeat/sympathetic).

### 9.3 Batch 3: Neuromodulation & Place of Service Exceptions — 2 Rules
- **Rules Included:**
  1. `RULE-IPM-CGSPINALCORDSTIM-001` (Spinal cord stimulation & DRGS trials)
  2. `RULE-IPM-EPOS1755-001` (Place of service outpatient hospital clinical exceptions)
- **Clinical Cohesion:** Highly complex multi-system clinical criteria. SCS requires full 4-element psychological assessment, infection/decolonization protocols, and multi-etiology branches. EPOS 1755 spans systemic cardiopulmonary, morbid obesity, metabolic, and airway comorbidities across the entire IPM CPT catalog.

### 9.4 Recommended First Implementation Batch
**Recommendation:** Authorize implementation of **Batch 1 (Spine Injections — 3 Rules)** first.  
*Justification:* Batch 1 addresses the highest-volume interventional pain procedures (ESI and SI joint injections, CPT 62320–62323, 64479–64484, 27096, G0260). Completing Batch 1 will establish core spinal injection parameter conventions, validate conservative care duration modeling across acute (2w), chronic (6w), and trial (12w) windows, and provide immediate clinical fidelity improvements with minimal cross-rule entanglement.

---

## 10. Conclusion & Stop Point

Stage A diagnostic evidence review for the nine outstanding IPM rules is complete. All authoritative policy pages, verbatim passages, clinical pathways, and threshold realignments have been cataloged.

**Operational Status:** Execution halted. Zero production edits made. Awaiting authorization before proceeding with implementation of Batch 1 or any individual IPM rule.
