# MedRule — Clinical Governance Human Review Queue
**Document Identifier:** `MEDRULE-GOV-HRQ-PHASE2`  
**Evaluation Status:** NON-BINDING CLINICAL REVIEW QUEUE  
**Corpus Invariant:** Zero Rules Approved (`APPROVED == 0`). All 128 Active Rules are `DRAFT` (121) or `NEEDS_HUMAN_REVIEW` (7).  
**Generated Date:** 2026-10-21  
**Governing Authority:** MedRule Clinical Governance Board & Medical Directorate  

---

## 1. Executive Summary and Governance Context

This prioritized Human Review Queue contains all unresolved clinical rules, ambiguous policy interpretations, uncodified criteria, and coverage gaps identified during the **Phase 2 Policy Fidelity Remediation and Validation Audit** of the MedRule Prior Authorization Decision-Support Engine.

### Strict Governance Constraints
1. **Zero Autonomous Approvals:** In compliance with MedRule Clinical Safety Standard Section 4.2, no rule in this queue is approved. No automated system change may promote any rule to `APPROVED` without explicit, authenticated Medical Director sign-off.
2. **Absolute Domain Scope Isolation:** Active clinical scope is strictly restricted to **Advanced Imaging** (114 rules) and **Interventional Pain Management (IPM)** (14 rules).
3. **Traceability Guarantee:** Every item in this queue maps directly to verified physical pages within the current 2026 governing clinical policies:
   - `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (1,041 pages)
   - `EPOS 2067 for Place of Service - Radiology 2026_final.pdf` (11 pages)
   - `2026 Evolent Interventional Pain Management Guidelines.pdf` (102 pages)
   - `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` (8 pages)
4. **CP.MP.107 Quarantine:** DME/O&P policy CP.MP.107 remains fully isolated and has 0% runtime influence on any active rule.

---

## 2. Prioritized Review Tiers

| Priority Tier | Category | Item Count | Target Reviewer | Adjudication Action |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | Governance-Blocked Rules | 7 rules | Medical Director | Affirm permanent exclusion from autonomous tree or reclassify to manual intake triage |
| **Tier 2** | Partially Verified Active Rules | 43 rules | Clinical Specialty SME | Review proposed condition refinements (conservative care, red flags, exclusions, footnotes) |
| **Tier 3** | Reconciled Coverage Gaps (New Rules) | 16 gap clusters | Clinical Policy Owner | Authorize drafting of new deterministic rule criteria for uncodified mandatory guidelines |
| **Tier 4** | Coverage Gap Policy Clarifications | 76 items | Medical Director / Legal | Resolve policy ambiguities, advisory vs mandatory wording, and operational billing boundaries |
| **Tier 5** | Secondary Provider Instruments | 14 items | Operations / Compliance | Confirm secondary guidance status (non-governing; no rule modification required) |

---

## 3. Tier 1: Governance-Blocked Rules (7 Rules)

The following 7 rules are unconditionally blocked from autonomous execution by the MedRule engine (`GOVERNANCE_BLOCKED_RULE_IDS`). They cannot generate authorization decisions without prior human review.

```
+---------------------------------------------------------------------------------------------------+
| RULE ID: RULE-ADV-PREAMBLE-001                                                                    |
| Domain: Advanced Imaging | Policy: 2026 Evolent Clinical Guidelines - Advanced Imaging v2 (p. 2)  |
| Section: Preamble / Guidelines for Clinical Review Determination                                  |
+---------------------------------------------------------------------------------------------------+
- Implemented Condition: clinical_information_submitted == true -> INDICATED
- Verbatim Policy Text:
  "In all cases, clinical judgment consistent with the standards of good medical practice will
   be used when applying the guidelines. Determinations are made based on both the guideline and
   clinical information provided at the time of the request... The treating clinician has final
   authority and responsibility for treatment decisions regarding the care of the patient."
- Audit Critique:
  Overly broad logic. The draft rule implemented a pseudo-rule that would approve any imaging request
  if clinical notes were submitted, completely bypassing procedure-specific medical necessity criteria.
- Clinical Review Question:
  Confirm that the Preamble remains permanently excluded from the deterministic decision tree and
  functions solely as an overarching administrative statement rather than an approval rule.
- Recommended Decision: REJECT AS DECISION-TREE RULE; RETAIN IN BLOCKED NON-EXECUTABLE REGISTRY.
```

```
+---------------------------------------------------------------------------------------------------+
| RULE ID: RULE-IPM-PREAMBLEIPM-001                                                                 |
| Domain: Interventional Pain Management | Policy: 2026 Evolent IPM Guidelines (p. 2)               |
| Section: Preamble and Guideline Development Process                                               |
+---------------------------------------------------------------------------------------------------+
- Implemented Condition: preambleipm_indication IS_PRESENT -> INDICATED
- Verbatim Policy Text:
  "In all cases, clinical judgment consistent with the standards of good medical practice will
   be used when applying the guidelines... Determinations are made based on both the guideline and
   clinical information provided at the time of the request."
- Audit Critique:
  Overly broad logic identical to the Advanced Imaging preamble. A single placeholder parameter
  bypasses all procedural prerequisites (conservative care, MRI correlation, frequency limits).
- Clinical Review Question:
  Confirm that the IPM Preamble is non-executable and cannot be evaluated to satisfy prior auth criteria.
- Recommended Decision: REJECT AS DECISION-TREE RULE; RETAIN IN BLOCKED NON-EXECUTABLE REGISTRY.
```

```
+---------------------------------------------------------------------------------------------------+
| RULE ID: RULE-ADV-CG2000-003                                                                      |
| Domain: Advanced Imaging | Policy: 2026 Evolent Clinical Guidelines - Advanced Imaging v2 (p. 9)  |
| Section: Inflammatory Bowel Disease (3-5)                                                         |
+---------------------------------------------------------------------------------------------------+
- Implemented Condition: requested_modality == 'CT' AND patient_age_years < 35 -> ALTERNATIVE_MODALITY_RECOMMENDED (MR Enterography)
- Verbatim Policy Text:
  "For evaluation of Inflammatory Bowel Disease (IBD) such as Crohn's or Ulcerative Colitis
   (includes CT enterography, however, MRI should be considered for age < 35 to reduce radiation exposure)"
- Audit Critique:
  Advisory language converted to mandatory redirection. The policy explicitly uses advisory phrasing
  ("MRI should be considered"), but the rule issued an autonomous redirection denying CT.
- Clinical Review Question:
  Does payer contract policy mandate automated denial/redirection of CT enterography in members < 35,
  or should CT enterography be approved if adult clinical criteria are met, with an informational advisory
  regarding MRI radiation sparing provided to the provider?
- Recommended Decision: CLARIFY POLICY; IF ADVISORY, EMIT INFORMATIONAL FLAG WITHOUT DENYING CT.
```

```
+---------------------------------------------------------------------------------------------------+
| RULE ID: RULE-ADV-CG2001-001                                                                      |
| Domain: Advanced Imaging | Policy: 2026 Evolent Clinical Guidelines - Advanced Imaging v2 (p. 37) |
| Section: STATEMENT / Special Note                                                                 |
+---------------------------------------------------------------------------------------------------+
- Implemented Condition: separate_abdomen_and_pelvis_requested == true AND pathology_involves_both == true -> ALTERNATIVE_MODALITY_RECOMMENDED (74176-74178)
- Verbatim Policy Text:
  "When separate requests for CT abdomen and CT Pelvis are encountered for processes involving both
   the abdomen and pelvis, they need to be resubmitted as Evolent Clinical Guideline 2000 for Abdomen
   and Pelvis CT (to avoid unbundling; CPT codes 74176, 74177, 74178)."
- Audit Critique:
  Claims billing / coding rule conflated with clinical necessity. Unbundling edits represent claims
  integrity pre-checks rather than medical necessity determinations.
- Clinical Review Question:
  Should anti-unbundling code combinations (74176 vs 74150+72192) be handled upstream by the EDI/claims
  intake pre-processor rather than inside the clinical necessity decision tree?
- Recommended Decision: RECLASSIFY AS CLAIMS PRE-PROCESSING VALIDATION EDIT; EXCLUDE FROM CLINICAL NECESSITY TREE.
```

```
+---------------------------------------------------------------------------------------------------+
| RULE ID: RULE-ADV-CG2066-001                                                                      |
| Domain: Advanced Imaging | Policy: 2026 Evolent Clinical Guidelines - Advanced Imaging v2 (p. 1036)|
| Section: INDICATIONS FOR EMERGENT STUDIES / Emergent Studies                                      |
+---------------------------------------------------------------------------------------------------+
- Implemented Condition: emergent_life_or_limb_threat_present == true -> INDICATED
- Verbatim Policy Text:
  "The requested study is required to render immediate medical attention needed to prevent loss of
   life, limb, or risk of significant morbidity/permanent disability such as... Conditions that
   impair bodily functions that support life (airway, breathing & circulation)... This type of
   medical necessity review is only conducted for those requests where the date of service has passed
   (a retrospective review)."
- Audit Critique:
  Subjective retrospective determination. Evaluating whether a retrospective emergency met life/limb
  threat criteria requires qualitative physician review of emergency room documentation.
- Clinical Review Question:
  Can retrospective emergency imaging ever be safely approved deterministically without physician
  review, or must all retrospective emergency claims automatically route to Medical Director adjudication?
- Recommended Decision: RETAIN IN BLOCKED STATUS; ENFORCE MANDATORY PHYSICIAN ROUTING FOR RETROSPECTIVE CLAIMS.
```

```
+---------------------------------------------------------------------------------------------------+
| RULE ID: RULE-ADV-CG2066-002                                                                      |
| Domain: Advanced Imaging | Policy: 2026 Evolent Clinical Guidelines - Advanced Imaging v2 (p. 1036)|
| Section: INDICATIONS FOR URGENT STUDIES / Urgent Studies                                          |
+---------------------------------------------------------------------------------------------------+
- Implemented Condition: urgent_intervention_needed_within_24h == true -> INDICATED
- Verbatim Policy Text:
  "For the evaluation of a condition that requires prompt medical intervention to prevent additional
   consequences to the health/wellbeing of the member... Any condition that cannot be postponed for
   a period of time (24 hours) without risking progression to an emergent condition... This type of
   medical necessity review is only conducted for those requests where the date of service has passed
   (a retrospective review)."
- Audit Critique:
  Subjective 24-hour urgency determination on retrospective claims requires clinical judgment.
- Clinical Review Question:
  Confirm that retrospective urgent claims (CG 2066) cannot be determined by algorithmic rules and
  require clinical nurse reviewer / medical director chart review.
- Recommended Decision: RETAIN IN BLOCKED STATUS; ROUTE TO HUMAN CLINICAL ADJUDICATION.
```

```
+---------------------------------------------------------------------------------------------------+
| RULE ID: RULE-IPM-CGINFUSIONPUMPS-001                                                             |
| Domain: Interventional Pain Management | Policy: 2026 Evolent IPM Guidelines (p. 68-72)            |
| Section: Implantable Infusion Pump Insertion 2026 (July)                                          |
+---------------------------------------------------------------------------------------------------+
- Implemented Condition: cginfusionpumps_indication IS_PRESENT -> INDICATED
- Verbatim Policy Text:
  "For the treatment of chronic intractable pain in non-terminal individuals (ALL the following criteria
   must be met): Pain causing functional disability... persistent pain level >= 6 on scale 0-10...
   Failure of non-operative conservative therapy for a minimum of 12 weeks... MRSA/MSSA decolonization plan
   no earlier than 10 days prior... Intraspinal drug trial producing >= 50% relief... Psychological evaluation
   within 12 months clearing patient..."
- Audit Critique:
  Severe oversimplification. Single placeholder condition ignores multi-step prerequisites (12 weeks
  conservative care, psychological eval, MRSA decolonization, temporary trial >= 50% relief).
- Clinical Review Question:
  Should Intrathecal Drug Delivery Systems be split into two distinct authorizations:
  (1) Intraspinal Temporary Trial Authorization (CG 1751/1752), and
  (2) Permanent Pump Implantation Authorization (CG 1752)?
- Recommended Decision: MAINTAIN BLOCKED STATUS; AUTHOR DECOMPOSED CRITERIA MODEL IN PHASE 3.
```

---

## 4. Tier 2: Partially Verified Active Rules (43 Rules Grouped by Clinical Domain)

### Group 1: Spine Advanced Imaging — Conservative Therapy & Red Flag Bypasses (7 Rules)
The current rules enforce conservative therapy durations (e.g. `conservative_care_duration_weeks >= 6`), but omit uncodified red flag bypasses and specific therapy modality requirements documented in policy footnotes.

| Rule ID | Policy & Page | Implemented Logic | Uncodified Policy Context | Proposed Remediation | Clinical Question for Review |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`RULE-ADV-CG2016-001`** | Adv Imaging p. 308 (Cervical CT) | `acute_cervical_trauma == true` | Canadian C-Spine Rule / NEXUS criteria elements (age >= 65, midline tenderness, dangerous mechanism) | Structure NEXUS / CCR criteria parameters explicitly | Should individual NEXUS elements be required fields in trauma intake? |
| **`RULE-ADV-CG2017-001`** | Adv Imaging p. 330 (Cervical MRI) | `conservative_care_duration_weeks >= 6` in last 6m | Footnote 5: Red flag bypass for progressive neurological deficit, myelopathy, or cancer history | Add `ANY_OF` bypass condition: progressive weakness or cancer waives 6w conservative care | Confirm progressive motor deficit waives the 6-week conservative care rule for cervical MRI. |
| **`RULE-ADV-CG2017-002`** | Adv Imaging p. 331 (Cervical MRI) | `myelopathic_neurologic_deficits == true` | Specific objective signs: hyperreflexia, clonus, gait instability, Hoffmann sign | Add multi-select parameter for objective upper motor neuron signs | Are Hoffmann reflex and gait ataxia sufficient without electrodiagnostic studies? |
| **`RULE-ADV-CG2017-003`** | Adv Imaging p. 330 (Cervical MRI) | `suspected_cervical_cord_compression == true` | Emergent surgical condition; immediate imaging without conservative care delay | Validate immediate indication; clarify exclusion of stable chronic neck pain | Confirm acute cord compression is an immediate approval without prior X-ray. |
| **`RULE-ADV-CG2036-001`** | Adv Imaging p. 574 (Lumbar CT) | Composite indication for trauma, fusion, or MRI contraindication | Footnote 1: Plain radiographs required; documented non-conditional implant reason | Separate post-fusion integrity from MRI-contraindicated lumbar pain | Should lumbar fusion evaluation CT be decoupled from MRI-contraindicated pain? |
| **`RULE-ADV-CG2037-001`** | Adv Imaging p. 594 (Lumbar MRI) | `conservative_care_duration_weeks >= 6` | Footnote 1: Red flag exceptions (foot drop, progressive deficit, active cancer with back pain) | Add explicit bypass: progressive motor deficit or active malignancy waives 6w therapy | Confirm foot drop / progressive weakness waives 6-week conservative care. |
| **`RULE-ADV-CG2037-002`** | Adv Imaging p. 595 (Lumbar MRI) | `suspected_cauda_equina_syndrome == true` | Emergent same-day surgical decompression urgency; saddle anesthesia, bowel/bladder incontinence | Retain immediate autonomous approval; confirm non-requirement of prior plain X-rays | Confirm acute cauda equina syndrome does not require prior plain radiographs. |

### Group 2: Abdominal & Pelvic Advanced Imaging — Exclusions & Bypasses (9 Rules)

| Rule ID | Policy & Page | Implemented Logic | Uncodified Policy Context | Proposed Remediation | Clinical Question for Review |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`RULE-ADV-CG2000-002`** | Adv Imaging p. 9 (Abdomen CT) | Exam, labs, recent colonoscopy completed | Contraindication note: Suspected perforation or toxic megacolon requires emergency surgical triage | Add exclusion: `suspected_perforation_or_toxic_megacolon == true` -> Emergency Triage | Should suspected free air / toxic megacolon trigger emergency redirection? |
| **`RULE-ADV-CG2000-004`** | Adv Imaging p. 9 (Abdomen CT) | Appendicitis/diverticulitis with systemic signs | Pregnant woman note: US insufficient AND MRI contraindicated. Pediatric note: US required first | Add pregnancy and pediatric gate routing to US/MRI before CT approval | Should pregnancy and pediatric age gates be mandatory before evaluating CT diverticulitis? |
| **`RULE-ADV-CG2000-005`** | Adv Imaging p. 9 (Abdomen CT) | Pediatric appendicitis: US inconclusive OR peritoneal signs | Policy also allows CT if ultrasound cannot be completed due to body habitus or lack of cooperation | Add sub-condition: `ultrasound_cannot_be_completed_due_to_cooperation_or_habitus == true` | Confirm inability to complete ultrasound due to body habitus permits pediatric CT. |
| **`RULE-ADV-CG2003-001`** | Adv Imaging p. 75 (Abdomen MRA) | Takayasu's: initial, q6m x 2yr, annual | MRA safety: GFR >= 30 for gadolinium, absence of non-conditional metallic implants | Add safety cross-checks for renal clearance and MRI-compatible hardware | Confirm MRA surveillance intervals for Takayasu's arteritis. |
| **`RULE-ADV-CG2004-001`** | Adv Imaging p. 92 (Abdomen MRI/CT) | Suspected choledochal cyst; ultrasound completed | MRCP is preferred over CT for biliary tree anatomy and cyst classification | Clarify whether MRCP should be favored over CT when ultrasound is indeterminate | Does policy prefer MRCP over CT for choledochal cyst evaluation? |
| **`RULE-ADV-CG2004-002`** | Adv Imaging p. 92 (Abdomen CT) | Epigastric pain; suspected acute pancreatitis | Atlanta criteria: Lipase > 3x ULN; CT recommended >= 48-72h after onset to detect necrosis | Add Atlanta criteria alignment: lipase threshold and >= 48-72h delay unless diagnosis unclear | Should acute pancreatitis CT criteria enforce Atlanta diagnostic criteria and timing? |
| **`RULE-ADV-CG2005-001`** | Adv Imaging p. 118 (Abdomen/Pelvis CTA) | Suspected acute or chronic mesenteric ischemia | Biphasic CTA protocol advisory note; arterial thromboembolism vs non-occlusive ischemia | Retain indication; add protocol guidance note for biphasic CTA acquisition | Confirm clinical suspicion of acute mesenteric ischemia justifies CTA without ultrasound. |
| **`RULE-ADV-CG2005-002`** | Adv Imaging p. 119 (Abdomen/Pelvis CTA) | Pelvic congestion syndrome; US indeterminate | Chronic pelvic pain duration (> 6 months), lower extremity swelling, varicosities | Add symptom duration requirement (> 6 months) and venous physical exam findings | Should pelvic congestion CTA require documentation of pelvic pain > 6 months? |
| **`RULE-ADV-CG2022-001`** | Adv Imaging p. 436 (CT Colonography) | Diagnostic colon evaluation; prior failed colonoscopy | Contraindications on p. 436: Active diverticulitis flare, acute obstruction, recent biopsy < 2-4w | Add explicit exclusion conditions: active diverticulitis flare or acute bowel obstruction | Must CT Colonography explicitly exclude patients with acute diverticulitis flare? |

### Group 3: Neurovascular, Head & Neck, and Thoracic Imaging (11 Rules)

| Rule ID | Policy & Page | Implemented Logic | Uncodified Policy Context | Proposed Remediation | Clinical Question for Review |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`RULE-ADV-CG2008-001`** | Adv Imaging p. 150 (Head CT) | Acute stroke or intracranial hemorrhage | Emergency non-contrast CT protocol; acute (< 24h) vs subacute/chronic where MRI is preferred | Add time window parameter: `symptom_onset_hours <= 24` to separate from subacute MRI | Should non-contrast head CT for stroke be bounded by symptom onset < 24 hours? |
| **`RULE-ADV-CG2008-002`** | Adv Imaging p. 151 (Head CT) | Suspected acute subarachnoid hemorrhage | CT sensitivity highest in first 6-24h; negative CT after 6h may require lumbar puncture | Add advisory note regarding lumbar puncture correlation if CT is negative > 6h | Confirm acute SAH suspicion approves non-contrast head CT without prior LP. |
| **`RULE-ADV-CG2008-003`** | Adv Imaging p. 151 (Head CT) | Head trauma with acute neurologic deficit | Canadian CT Head Rule: GCS < 15, suspected skull fracture, >= 2 vomiting episodes, age >= 65 | Structure criteria according to Canadian CT Head high-risk factors | Should head trauma CT criteria be explicitly mapped to Canadian CT Head Rule elements? |
| **`RULE-ADV-CG2008-004`** | Adv Imaging p. 149 (Head CT) | Sudden onset 'worst headache of life' < 48h | Differentiates thunderclap headache from new onset headache with fever or papilledema | Retain focused thunderclap rule; map other headache presentations to separate rules | Confirm thunderclap headache criteria boundary is restricted to onset within 48 hours. |
| **`RULE-ADV-CG2009-002`** | Adv Imaging p. 176 (Brain CTA) | Acute stroke evaluated for LVO / thrombectomy | Time window on p. 176: LVO evaluation within 24 hours of last known normal | Add parameter: `hours_since_last_known_well <= 24` aligned with thrombectomy eligibility | Should Brain CTA for LVO explicitly enforce time window <= 24 hours? |
| **`RULE-ADV-CG2015-001`** | Adv Imaging p. 297 (CT/MR Perfusion) | Stroke reperfusion evaluation <= 24h of onset | Automated mismatch software (DAWN/DEFUSE 3 protocol); core infarct volume thresholds | Add baseline NIHSS >= 6 requirement and consideration for mechanical thrombectomy | Does CT perfusion require distinct prior auth, or should it be bundled with CTA? |
| **`RULE-ADV-CG2030-001`** | Adv Imaging p. 490 (LDCT Screening) | Age 50-80, >= 20 pack-years, smoker within 15y | Footnote criteria: Shared decision-making visit; patient must be asymptomatic of lung cancer | Add mandatory prerequisite: `symptomatic_of_lung_disease == false` (redirect symptomatic to 71250) | Must LDCT screening rule enforce 'patient is asymptomatic' to prevent miscoding? |
| **`RULE-ADV-CG2042-001`** | Adv Imaging p. 673 (Pelvis CT) | Acute severe pelvic pain; Age > 65 years | In females < 65, pelvic ultrasound is mandatory first-line imaging for acute pelvic pain | Codify reverse boundary: females < 65 require ultrasound before pelvic CT | Confirm that females < 65 with acute pelvic pain require pelvic ultrasound prior to CT. |
| **`RULE-ADV-CG2045-001`** | Adv Imaging p. 718 (Pelvis MRI) | Suspected perianal fistula or occult abscess | Pelvic MRI is gold standard for perianal fistula tract and sphincter anatomy | Codify Pelvic MRI as first-line indication for perianal Crohn's fistula | Confirm Pelvic MRI is indicated for complex perianal fistula without prior CT. |
| **`RULE-ADV-CG2054-001`** | Adv Imaging p. 881 (Sella CT) | Known sellar/parasellar mass for bony evaluation | MRI is primary diagnostic test; CT is reserved for transsphenoidal surgical bony planning | Add condition: Brain MRI completed or contraindicated, and surgical planning documented | Should Sella CT require prior Brain MRI or documented transsphenoidal surgical planning? |
| **`RULE-ADV-CG2055-001`** | Adv Imaging p. 896 (TMJ MRI) | Suspected internal TMJ derangement | Plain radiographs / panorex completed; failure of 4-6 weeks conservative therapy (splint, diet) | Add conditions: `prior_xray_completed == true` AND `conservative_care_weeks >= 4` | Must TMJ MRI require documented completion of at least 4-6 weeks of conservative care? |

### Group 4: Thoracic Spine & Extremity Imaging (8 Rules)

| Rule ID | Policy & Page | Implemented Logic | Uncodified Policy Context | Proposed Remediation | Clinical Question for Review |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`RULE-ADV-CG2032-001`** | Adv Imaging p. 504 (Lower Ext CT) | Non-specific leg pain; X-ray done; MRI contraindicated | Conservative care requirement: 4-6 weeks conservative therapy required for chronic pain | Add condition: documented failure of 4-6 weeks conservative care unless acute trauma | Should lower extremity CT for non-specific pain require 4-6 weeks conservative therapy? |
| **`RULE-ADV-CG2035-001`** | Adv Imaging p. 553 (Lower Ext MRI) | Joint pain, mechanical locking, internal derangement | Plain X-rays required; 4-6 weeks conservative care required if no acute mechanical locking | Branch criteria: acute locking -> immediate MRI; chronic pain -> 4-6w therapy + X-ray | Should knee/joint MRI separate acute locking (immediate) from chronic pain (4-6w care)? |
| **`RULE-ADV-CG2035-002`** | Adv Imaging p. 553 (Lower Ext MRI) | Positive knee orthopedic sign; prior X-ray done | Weight-bearing X-ray showing advanced tri-compartmental osteoarthritis excludes routine MRI | Add exclusion: `xray_shows_bone_on_bone_advanced_oa == true` -> MRI NOT INDICATED | Does policy exclude routine knee MRI when X-rays show bone-on-bone advanced OA? |
| **`RULE-ADV-CG2056-001`** | Adv Imaging p. 905 (Thoracic CT) | Thoracic neurologic deficit; MRI contraindicated | Footnote: Documented specific medical contraindication to MRI required | Validate structured MRI contraindication parameter against standard device list | Should MRI contraindications for spine CT be validated against enumerated device list? |
| **`RULE-ADV-CG2056-002`** | Adv Imaging p. 906 (Thoracic CT) | Thoracic pain > 4w; failure 4-6w therapy; MRI contraindicated | Footnote 1: Plain thoracic radiographs must precede advanced imaging | Add condition: `prior_thoracic_xray_completed == true` | Confirm thoracic CT for subacute pain requires prior plain X-rays in addition to therapy. |
| **`RULE-ADV-CG2057-001`** | Adv Imaging p. 925 (Thoracic MRI) | Thoracic myelopathy or sensory/motor level deficit | Emergent/urgent condition; no conservative therapy delay required | Retain immediate approval for myelopathy; clarify non-applicability to axial pain | Confirm thoracic myelopathy with UMN signs is an immediate indication without therapy. |
| **`RULE-ADV-CG2057-002`** | Adv Imaging p. 926 (Thoracic MRI) | Thoracic pain > 4w; failure 4-6w conservative therapy | Prior thoracic X-rays required; red flag exceptions (fever, cancer) waiving therapy | Add `prior_xray_completed == true` and red flag bypass for active malignancy or infection | Should thoracic spine MRI require prior plain radiographs for pain > 4 weeks? |
| **`RULE-ADV-CG2062-001`** | Adv Imaging p. 965 (Upper Ext CT) | Prior X-ray done; failure >= 4w therapy OR complex fracture | CT is restricted to complex bony injury/fracture; soft tissue/tendon derangements require MRI | Refine condition: `bony_injury_or_surgical_planning == true` or redirect soft tissue to MRI | Does policy restrict Upper Extremity CT to bony pathology, redirecting tendons to MRI? |

### Group 5: Interventional Pain Management Procedural Rules (8 Rules)

| Rule ID | Policy & Page | Implemented Logic | Uncodified Policy Context | Proposed Remediation | Clinical Question for Review |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`RULE-IPM-CGEPIDURALINJECTIONS-001`** | IPM Guidelines p. 4 (ESI) | Placeholder parameter `cgepiduralinjections_indication` | Detailed criteria pp. 4-10: Radiculopathy conforming to dermatome, MRI correlation, 6w therapy | Decompose into: (1) Radicular pain, (2) Concordant imaging, (3) 6w conservative care failure | Should ESI be decomposed into separate rules for Initial Injection vs Subsequent Injections? |
| **`RULE-IPM-CGEPIDURALINJECTIONS-002`** | IPM Guidelines p. 11 (ESI Conservative Care) | Generic `conservative_therapy_failure` parameter | Specific criteria p. 11: Active PT (>= 6 sessions over 6w) OR instructed HEP + oral medications | Codify specific parameters: `conservative_care_weeks >= 6` AND `active_pt_or_hep == true` | Confirm conservative care for ESI requires >= 6 weeks of active PT/HEP and oral analgesics. |
| **`RULE-IPM-CGEPIDURALPUMPTRIALS-001`** | IPM Guidelines p. 17 (Pump Trial ESI) | Placeholder parameter `cgepiduralpumptrials_indication` | Criteria pp. 17-23: Refractory pain/spasticity failing oral therapies; multidisciplinary clearance | Decompose into: failed oral therapies, psychological clearance, continuous monitoring | Should Single Injection Epidural Pump Trials require distinct prior auth from permanent pump? |
| **`RULE-IPM-CGFACETBLOCKS-001`** | IPM Guidelines p. 31 (Facet Blocks) | Placeholder parameter `cgfacetblocks_indication` | Criteria pp. 31-36: Axial pain >= 3m, no radiculopathy, 6w therapy, max 3 levels, fluoroscopy | Decompose into: (1) Axial pain without radiculopathy, (2) 6w therapy failure, (3) Max 3 levels | Should Facet Block rules enforce dual diagnostic blocks (>= 50% relief) prior to RFA approval? |
| **`RULE-IPM-CGSIINJECTIONS-001`** | IPM Guidelines p. 57 (SI Joint Injections) | Placeholder parameter `cgsiinjections_indication` | Criteria pp. 57-62: Pain below L5, 3 of 5 positive provocative tests, 6w therapy, max 4/year | Decompose into: (1) 3-of-5 provocative tests, (2) 6w therapy, (3) Fluoroscopy, (4) Max 4/year | Should SI Joint Injection rules mandate documentation of 3 of 5 positive provocative maneuvers? |
| **`RULE-IPM-CGSPINALCORDSTIM-001`** | IPM Guidelines p. 78 (SCS Trial) | Placeholder parameter `cgspinalcordstim_indication` | Criteria pp. 78-83: Intractable neuropathic pain failing 6m care; psychological eval within 12m | Decompose into: trial lead placement vs permanent generator, with psychological clearance | Should Spinal Cord Stimulation be split into separate rules for Trial vs Permanent Implant? |
| **`RULE-IPM-CGSPINALCORDSTIM-002`** | IPM Guidelines p. 80 (SCS Permanent) | `scs_trial_pain_relief >= 50%` | Detailed trial criteria p. 80: Trial duration 3-7 days; objective functional ADL improvement | Add parameter: `scs_trial_duration_days between 3 and 7` AND `functional_adls_improved == true` | Should permanent SCS criteria validate trial duration of at least 3-7 days? |
| **`RULE-IPM-CGSYMPATHETICBLOCKS-001`** | IPM Guidelines p. 89 (Sympathetic Blocks) | Placeholder parameter `cgsympatheticblocks_indication` | Anatomic criteria pp. 89-100: Stellate, Lumbar, Celiac, Hypogastric, Impar; objective signs | Decompose into anatomic procedure rules with site-specific objective monitoring criteria | Should sympathetic blocks be partitioned into distinct rules by anatomic site? |

---

## 5. Tier 3: Reconciled Coverage Gaps — New Rule Candidates (16 Items)

These 16 items represent genuine, enforceable clinical policy requirements identified in governing policies that are currently uncodified in active rules. They are candidate additions for future Phase 3 clinical authoring.

```
1. Central Spinal Stenosis Epidural Injections (CG-1750, pp. 6-7)
   - Indication: Central or lateral spinal canal stenosis with neurogenic claudication refractory to >= 6w conservative care.
   - Proposed Rule ID: RULE-IPM-CG1750-STENOSIS-001

2. Epidural Repeat Injections Frequency & Relief Threshold (CG-1750, pp. 7-8)
   - Indication: Subsequent ESI requires documented >= 50% pain relief for >= 6 weeks; minimum 14-day interval; max 3 per 12m.
   - Proposed Rule ID: RULE-IPM-CG1750-REPEAT-001

3. Epidural Procedural Constraints & Fluoroscopy Mandate (CG-1750, pp. 8-9)
   - Indication: Maximum 2 spinal levels per session; fluoroscopic or CT guidance mandatory. Blind injections excluded.
   - Proposed Rule ID: RULE-IPM-CG1750-LEVELS-001

4. Epidural Absolute Contraindications & Coagulopathy Thresholds (CG-1750, pp. 9-10)
   - Indication: Platelets < 50,000/mcL or INR > 1.5; systemic or local spine infection; pregnancy (fluoroscopy).
   - Proposed Rule ID: RULE-IPM-CG1750-CONTRA-001

5. Intraspinal Single Injection Pump Trial Monitoring Protocol (CG-1751, pp. 19-23)
   - Indication: Inpatient or continuous monitored outpatient observation; documented baseline and post-injection pain scores.
   - Proposed Rule ID: RULE-IPM-CG1751-TRIAL-001

6. Facet Dual Comparative Diagnostic Block Protocol (CG-1753, pp. 33-35)
   - Indication: Two diagnostic blocks with different local anesthetics; >= 50% pain relief required for each before RFA.
   - Proposed Rule ID: RULE-IPM-CG1753-DUALBLOCK-001

7. Facet Therapeutic Intra-Articular Steroid Injection Non-Coverage (CG-1753, pp. 35-36)
   - Indication: Therapeutic intra-articular facet steroid injections non-covered due to lack of RCT efficacy over medial branch blocks.
   - Proposed Rule ID: RULE-IPM-CG1753-EXCLUSION-001

8. Facet Level Limits & Fluoroscopy Mandate (CG-1753, pp. 34-35)
   - Indication: Maximum 3 contiguous joint levels per anatomic region per session; fluoroscopic guidance mandatory.
   - Proposed Rule ID: RULE-IPM-CG1753-LEVELS-001

9. Radiofrequency Facet Neurotomy Repeat Interval & Relief (CG-1754, pp. 48-50)
   - Indication: Repeat RFA permitted >= 6 months after prior RFA if initial procedure produced >= 50% relief for >= 6 months; max 2/yr.
   - Proposed Rule ID: RULE-IPM-CG1754-REPEAT-001

10. Sacroiliac Joint Provocative Physical Exam Maneuvers (CG-1756, pp. 59-60)
    - Indication: Documentation of at least 3 of 5 positive provocative tests (FABER, Gaenslen, Distraction, Compression, Thigh Thrust).
    - Proposed Rule ID: RULE-IPM-CG1756-EXAM-001

11. Sacroiliac Joint Injection Frequency Limits & Pre-Fusion Blocks (CG-1756, pp. 60-62)
    - Indication: Max 4 therapeutic injections per 12 months; minimum 60 days between injections; pre-fusion dual blocks >= 75% relief.
    - Proposed Rule ID: RULE-IPM-CG1756-LIMITS-001

12. Intrathecal Drug Infusion Pump Trial Threshold & Psych Evaluation (CG-1752, pp. 69-73)
    - Indication: Trial >= 50% pain relief; psychological evaluation within 12 months; spasticity Ashworth score >= 3.
    - Proposed Rule ID: RULE-IPM-CG1752-TRIAL-001

13. Dorsal Root Ganglion (DRG) Stimulator Anatomic Restriction (CG-1757, pp. 82-84)
    - Indication: DRG stimulation restricted to CRPS Type I or Type II of the lower extremity.
    - Proposed Rule ID: RULE-IPM-CG1757-DRG-001

14. Spinal Cord Stimulation Generator Replacement Criteria (CG-1757, pp. 84-87)
    - Indication: Battery depletion or confirmed hardware malfunction; psychological clearance within 12 months.
    - Proposed Rule ID: RULE-IPM-CG1757-REPLACEMENT-001

15. Anatomically Differentiated Sympathetic Nerve Blocks (CG-1758, pp. 91-99)
    - Indication: Distinct rules for Stellate (UE CRPS), Lumbar (LE CRPS), Celiac (pancreatic cancer), Hypogastric (pelvic pain), Impar (perineal).
    - Proposed Rule ID: RULE-IPM-CG1758-ANATOMIC-001

16. Sympathetic Nerve Block Objective Monitoring Signs (CG-1758, pp. 99-100)
    - Indication: Documented Horner syndrome (stellate) or skin temperature rise > 1.5-2 deg C (lumbar); >= 50% pain relief.
    - Proposed Rule ID: RULE-IPM-CG1758-MONITORING-001
```

---

## 6. Tier 4: Reconciled Coverage Gaps — Policy Clarifications (76 Items)

The 76 policy clarification items represent secondary clinical subsections or advisory notes across Advanced Imaging and IPM.
- **Advanced Imaging Subsections (70 items):** Organ-specific subsections within established guidelines (e.g., CT chest for hemoptysis vs pulmonary embolism; CT neck for lymphadenopathy vs deep neck infection). These are currently handled under parent guideline rules and should be clarified with the Clinical Policy Owner on whether fine-grained sub-rules are required.
- **Hospital Outpatient Exceptions under EPOS 1755 (1 item):** EPOS 1755 pp. 3-6 details high-risk clinical conditions (ASA III/IV, BMI >= 50, severe OSA) permitting IPM in a hospital outpatient setting. Requires operational definition of structured intake questions.
- **Advisory Modality Language (5 items):** Advisory suggestions ("MRI should be considered") requiring health plan confirmation of non-binding advisory vs mandatory prior auth denial.

---

## 7. Tier 5: Secondary Provider Supporting Instruments (14 Items)

The 14 provider checklists, tip sheets, and historical attestation forms are classified as **SUPPORTING_GUIDANCE** or **NON_APPLICABLE_ISSUE**:
- **Advanced Imaging Supporting Instruments (8 items):**
  - Imaging Provider Checklist (p. 1)
  - Historical Conservative Therapy Form (pp. 1-2)
  - Provider Tip Sheets (pp. 1-6 x 3)
  - Ultrasound / MRI Radiation Sparing Tip Sheet
- **IPM Supporting Instruments (6 items):**
  - IPM Clinical Documentation Checklist (pp. 1-3)
  - IPM Conservative Therapy Attestation Form (p. 1)
  - IPM Provider Tip Sheet (pp. 1-4)

**Adjudication Finding:** These documents are educational and intake aids. They do not supersede the governing 2026 clinical guidelines. **No rule change is required.**

---

## 8. Clinical Adjudication Sign-Off Form

| Adjudication Field | Reviewer Entry |
| :--- | :--- |
| **Reviewing Medical Director:** | __________________________________________________ |
| **Medical License Number & State:** | __________________________________________________ |
| **Review Date:** | __________________________________________________ |
| **Tier 1 Governance Decision:** | [  ] Concur with Blocked Status [  ] Modify Workflow |
| **Tier 2 Proposed Changes Decision:** | [  ] Approve Proposed Corrections [  ] Request Modifications |
| **Tier 3 New Rule Authoring:** | [  ] Authorize Phase 3 Authoring [  ] Defer |
| **Director Signature:** | __________________________________________________ |

---
*End of Human Review Queue — MedRule Phase 2*
