# MedRule — Phase 2 Human Review Queue

## Overview & Governance Notice
This human-review queue consolidates all policy discrepancies, clinical prerequisite omissions, uncompiled stubs, citation errors, and interpretive ambiguities identified across the 43 audited clinical rules and 204 coverage-gap records.

> [!IMPORTANT]
> **Governance Notice:** Priority labels (P1, P2, P3) are clinical engineering triage aids for sequencing review. They do not constitute formal clinical risk determinations or medical director approvals. No automated edits or status promotions have been applied.

---

## Priority 1: Critical Missing Clinical Prerequisites (MRI Contraindications)

### 1. `RULE-ADV-CG2054-001` — Sella CT Evaluation of Sellar/Parasellar Mass
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 881 (Printed Page 4 of 17), section `INDICATIONS FOR SELLA CT / Sella CT (9)`.
- **Exact Verbatim Source:** *"When MRI is contraindicated or cannot be performed: For further evaluation of known sellar and/or parasellar masses"*
- **Issue:** The active rule approves Sella CT for known masses on clinical indication alone, completely omitting the mandatory section prerequisite: `mri_contraindicated_or_cannot_be_performed == true`. Sella CT is secondary to Brain/Sella MRI.
- **Evidence:** Rule condition `COND-001` checks only `known_sellar_or_parasellar_mass == true`.
- **Question for Reviewer:** Must `mri_contraindicated == true` be added as a mandatory prerequisite gating condition for all Sella CT indications?

### 2. `RULE-ADV-CG2056-002` — Thoracic Spine CT for Back Pain
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 906 (Printed Page 4 of 20), section `INDICATIONS FOR THORACIC SPINE CT / Evaluation of Back Pain (1)`.
- **Exact Verbatim Source:** *"With any of the following when Thoracic Spine MRI is Contraindicated: ... Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months"*
- **Issue:** The rule approves Thoracic CT for back pain without verifying that Thoracic MRI is contraindicated. Thoracic MRI is first-line; CT is strictly a fallback modality.
- **Evidence:** Rule conditions check duration > 4 weeks and conservative therapy completion, with zero check for MRI contraindications.
- **Question for Reviewer:** Should `thoracic_mri_contraindicated == true` be added as a mandatory condition for `RULE-ADV-CG2056-002`?

### 3. `RULE-ADV-CG2062-001` — Upper Extremity CT for Extremity Pain
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical pp. 965–966 (Printed Pages 3–4 of 24), section `Special Notes` & `Non-specific Upper Extremity Pain`.
- **Exact Verbatim Source:** *"When specifically indicated below, MRI is the preferred study for the evaluation of the extremities and CT is indicated only when MRI is contraindicated or cannot be performed ... If MRI is contraindicated or cannot be performed, or requested as a CT arthrogram"*
- **Issue:** The rule approves Upper Extremity CT for persistent pain after negative X-ray without checking whether MRI is contraindicated or unavailable, bypassing MRI as the preferred modality.
- **Evidence:** Rule checks only `prior_xray_negative_or_inconclusive` and `conservative_therapy_or_bony_injury`.
- **Question for Reviewer:** Must `mri_contraindicated_or_cannot_be_performed == true` (or CT arthrogram intent) be enforced as a mandatory prerequisite?

---

## Priority 2: Critical Missing Conservative Treatment Prerequisites

### 4. `RULE-ADV-CG2055-001` — TMJ MRI for Suspected Internal Derangement
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 896 (Printed Page 2 of 8), section `INDICATIONS FOR TEMPOROMANDIBULAR JOINT (TMJ) MRI`.
- **Exact Verbatim Source:** *"Suspected Internal TMJ Derangement: Persistent symptoms of facial or jaw pain, restricted range of motion, pain and/or noise with TMJ function (i.e., chewing) (2-4) AND Conservative therapy with a trial of pharmacotherapy* AND behavioral modification** has been unsuccessful for at least four (4) weeks"*
- **Issue:** The rule checks clinical symptoms (pain, restricted ROM, noise with chewing) but completely omits the mandatory prerequisite of at least 4 weeks of unsuccessful dual conservative therapy (pharmacotherapy AND behavioral modification/splints).
- **Evidence:** Rule logic evaluates symptoms alone, potentially authorizing advanced TMJ MRI without required conservative therapy.
- **Question for Reviewer:** Should `conservative_therapy_duration_weeks >= 4` (incorporating pharmacotherapy and behavioral modification) be added as an mandatory gate?

### 5. `RULE-ADV-CG2032-001` — Lower Extremity CT for Non-Specific Pain
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 504 (Printed Page 4 of 23), section `Non-specific Lower Extremity Pain`.
- **Exact Verbatim Source:** *"Persistent musculotendinous lower extremity pain unresponsive to ACTIVE Conservative Therapy (ACT) ... of at least four (4) weeks duration within the last 6 months"*
- **Issue:** The rule enforces prior X-ray and MRI contraindication, but omits the mandatory 4-week active conservative therapy failure requirement.
- **Question for Reviewer:** Should the 4-week ACT failure condition be added to `RULE-ADV-CG2032-001`?

### 6. `RULE-ADV-CG2035-001` — Lower Extremity MRI for Joint-Specific Pain
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 553 (Printed Page 4 of 22), section `Joint Specific Pain or Suspected Joint Specific Injury`.
- **Exact Verbatim Source:** *"In the absence of a positive joint specific orthopedic sign on exam (see list below), advanced imaging is indicated with prior X-ray showing no clear etiology for the joint pain with any ONE of the following: Persistent joint pain unresponsive to ACTIVE Conservative Therapy (ACT) ... of at least four (4) weeks duration within the last 6 months"*
- **Issue:** Overly broad rule approves joint pain on symptom alone, omitting mandatory plain radiograph and >= 4 weeks active conservative therapy.
- **Question for Reviewer:** Should mandatory prior X-ray and 4-week ACT failure conditions be added?

### 7. `RULE-ADV-CG2056-002` & `RULE-ADV-CG2057-002` — Conservative Therapy Duration & Pediatric Conflation
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical pp. 906, 926, section `Evaluation of Back Pain (1)`.
- **Exact Verbatim Source:** *"Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months ... Isolated back pain in pediatric population when at least ONE of the following red flags are present ... Pain lasting > 4 weeks"*
- **Issue:** Both rules miscode adult conservative therapy duration as "4-6 weeks" (policy specifies minimum 6 weeks within last 6 months) and cite pediatric red flag phrasing ("Pain lasting > 4 weeks") for adult back pain.
- **Question for Reviewer:** Should conservative care duration be standardized to `duration_weeks >= 6 within last 6 months` and isolated pediatric red flags segregated into a distinct rule?

---

## Priority 3: Six Uncompiled IPM Procedural Stubs

### 8. `RULE-IPM-CGEPIDURALINJECTIONS-001` — Epidural Spine Injections (ESI)
- **Domain:** Interventional Pain Management
- **Source Citation:** `2026 Evolent Interventional Pain Management Guidelines.pdf`, physical pp. 6–8 (Printed Pages 3–5 of 13), section `INDICATIONS / General to All Caudal, Interlaminar, and Transforaminal Injections`.
- **Exact Verbatim Source:** *"For all injections, patients must exhibit pain causing functional disability or average pain level of ≥ 6 on a scale of 0 to 10 ... Acute pain or exacerbation of chronic radicular pain ... Duration of pain < 3 months ... Failure to respond to non-operative conservative treatment ... for a minimum of 2 weeks ... Spinal stenosis ... minimum of six (6) weeks in the last six (6) months"*
- **Issue:** Rule is an uncompiled stub checking single parameter `cgepiduralinjections_indication IS_PRESENT`. Omits pain severity (>= 6/10), acute radicular care (2 weeks), chronic/stenosis care (6 weeks), fluoroscopic guidance, and repeat injection limits.
- **Question for Reviewer:** Should clinical engineering decompose this stub into discrete deterministic decision trees for acute radiculopathy, spinal stenosis, and failed back surgery syndrome?

### 9. `RULE-IPM-CGEPIDURALINJECTIONS-002` — ESI Conservative Treatment & HEP Requirements
- **Domain:** Interventional Pain Management
- **Source Citation:** `2026 Evolent Interventional Pain Management Guidelines.pdf`, physical p. 11 (Printed Page 8 of 13), section `Conservative Treatment* / Home Exercise Program (HEP)**`.
- **Exact Verbatim Source:** *"The following two elements are required to meet conservative therapy guidelines for HEP: Documentation of an exercise prescription/plan provided by a physician, physical therapist, or chiropractor AND Follow-up documentation regarding completion of HEP after the required 6-week timeframe or inability to complete HEP due to a documented medical reason"*
- **Issue:** Rule evaluates generic string `'CONSERVATIVE_MANAGEMENT'`, omitting the 2 mandatory policy elements (clinician prescription + follow-up completion after 6 weeks) and multimodality (1 active + 1 inactive) requirement.
- **Question for Reviewer:** Should rule parameters be expanded to validate clinician prescription, 6-week timeframe, and active/inactive components?

### 10. `RULE-IPM-CGEPIDURALPUMPTRIALS-001` — Intrathecal Pump Single Injection Trials
- **Domain:** Interventional Pain Management
- **Source Citation:** `2026 Evolent Interventional Pain Management Guidelines.pdf`, physical p. 22 (Printed Page 6 of 14), section `INDICATIONS FOR INTRASPINAL DRUG TRIAL`.
- **Exact Verbatim Source:** *"For the treatment of chronic intractable pain in non-terminal individuals ... persistent pain level of ≥ 6 ... Failure to respond to non-operative conservative therapy ... for a minimum of 12 weeks ... Spasticity ... minimum of 12 weeks of non-operative conservative therapy"*
- **Issue:** Stub rule (`cgepiduralpumptrials_indication IS_PRESENT`) omits 12-week conservative therapy failure and diagnostic criteria for intractable pain vs severe spasticity.
- **Question for Reviewer:** Should separate decision branches be compiled for non-terminal chronic pain vs intractable spasticity?

### 11. `RULE-IPM-CGFACETBLOCKS-001` — Paravertebral Facet Joint Injections / Medial Branch Blocks
- **Domain:** Interventional Pain Management
- **Source Citation:** `2026 Evolent Interventional Pain Management Guidelines.pdf`, physical pp. 32–34 (Printed Pages 2–4 of 14), section `INDICATIONS FOR FACET JOINT INJECTIONS OR MEDIAL BRANCH NERVE BLOCKS`.
- **Exact Verbatim Source:** *"Pain that: Is causing functional disability or average pain level of ≥ 6 ... Duration for at least 3 months ... By history, mainly axial or non-radicular ... Is of primary source that is not sacroiliac joint pain, discogenic pain, disc herniation, or radiculitis ... Failure to respond to non-operative conservative treatment ... for a minimum of six (6) weeks in the last six (6) months"*
- **Issue:** Stub rule (`cgfacetblocks_indication IS_PRESENT`) omits pain >= 6/10, duration >= 3 months, axial restriction, alternative source exclusions, 6 weeks conservative care, mandatory imaging guidance, and 2-session diagnostic limit with >= 50% relief.
- **Question for Reviewer:** Should full decision tree be implemented with discrete diagnostic and therapeutic repeat gates?

### 12. `RULE-IPM-CGSIINJECTIONS-001` — Sacroiliac Joint Injections
- **Domain:** Interventional Pain Management
- **Source Citation:** `2026 Evolent Interventional Pain Management Guidelines.pdf`, physical pp. 58–60 (Printed Pages 2–4 of 10), section `INDICATIONS FOR SACROILIAC JOINT INJECTIONS`.
- **Exact Verbatim Source:** *"Primarily axial low back pain (below level of L5) ... Pain causing functional disability or average pain level of ≥ 6 ... A cluster of any three (3) of the following positive provocation exam findings ... Duration of pain of at least 3 months ... Failure to respond to non-operative conservative treatment ... for a minimum of six (6) weeks in the last six (6) months"*
- **Issue:** Stub rule (`cgsiinjections_indication IS_PRESENT`) omits the cardinal clinical requirement: documentation of a cluster of at least 3 of 8 positive provocative physical exam tests (FABER, distraction, compression, sacral thrust, thigh thrust, Gaenslen, Yeoman, posterior shear).
- **Question for Reviewer:** Should the 3-of-8 provocative test cluster be codified as a multi-select condition?

### 13. `RULE-IPM-CGSPINALCORDSTIM-001` & `002` — Spinal Cord Stimulation Trial & Permanent Implant
- **Domain:** Interventional Pain Management
- **Source Citation:** `2026 Evolent Interventional Pain Management Guidelines.pdf`, physical pp. 78–81 (Printed Pages 2–5 of 12), section `INDICATIONS / Spinal Cord Stimulation` & `Permanent Stimulator`.
- **Exact Verbatim Source:** *"Pain that: Is causing functional disability or average pain level of ≥ 6 ... duration of at least 6 months ... Failed spine surgery syndrome ... CRPS ... Chronic neuropathic pain ... Failure to respond to non-operative conservative treatment ... for a minimum of 6 months ... A completed presurgical psychological assessment ... Permanent: Documentation of a successful trial ... providing at least 50% reduction in pain; Significant functional improvement for a minimum duration of 3 days"*
- **Issue:** Rule 001 is a generic stub omitting 6-month therapy duration, qualifying diagnoses, and psychological clearance. Rule 002 encodes >= 50% relief but omits the mandatory companion requirement: "Significant functional improvement for a minimum duration of 3 days".
- **Question for Reviewer:** Should Rule 001 be fully compiled and Rule 002 augmented with `functional_improvement_trial_duration_days >= 3`?

### 14. `RULE-IPM-CGSYMPATHETICBLOCKS-001` — Sympathetic Nerve Blocks
- **Domain:** Interventional Pain Management
- **Source Citation:** `2026 Evolent Interventional Pain Management Guidelines.pdf`, physical pp. 91–93 (Printed Pages 3–5 of 14), section `INDICATIONS / General Indications / Stellate Ganglion Block`.
- **Exact Verbatim Source:** *"Acute or chronic noncancer pain ... average pain level of ≥ 6 ... Each block must be performed under image guidance ... Stellate: Acute Herpes Zoster ... duration less than 4 weeks AND Active antiviral therapy ... CRPS types I and II ... Failure to respond to functional restoration modalities"*
- **Issue:** Stub rule (`cgsympatheticblocks_indication IS_PRESENT`) omits pain >= 6/10, mandatory image guidance, and specific diagnostic branches (shingles, CRPS, phantom limb, cancer).
- **Question for Reviewer:** Should full branching logic be compiled for specific sympathetic blocks?

---

## Priority 4: Citation Mismatches & Page Discrepancies

### 15. `RULE-ADV-CG2009-002` — Head CTA/CTP for Large Vessel Occlusion (LVO)
- **Domain:** Advanced Imaging
- **Reported Issue:** Rule metadata cites physical page 176 (`Evaluation of Known Intracranial Vascular Disease` - aneurysms, AVMs). The actual policy for mechanical thrombectomy / LVO stroke evaluation is located on physical page 175 (`Cerebrovascular Disease / Ischemic`).
- **Question for Reviewer:** Approve administrative update of rule metadata citation from p. 176 to p. 175?

### 16. `RULE-ADV-CG2037-001` — Lumbar Spine MRI for Radiculopathy & Back Pain
- **Domain:** Advanced Imaging
- **Reported Issue:** Rule metadata cites physical page 594 (`Evaluation of Neurologic Deficits`). The actual policy criteria for radiculopathy and failure of conservative treatment for a minimum of 6 weeks within the last 6 months are located on physical page 595 (`Evaluation of Back Pain`).
- **Question for Reviewer:** Approve administrative update of rule metadata citation from p. 594 to p. 595?

### 17. Five IPM Rules Citing Table of Contents Pages
- **Rules Affected:** `RULE-IPM-CGEPIDURALINJECTIONS-001` (cites p. 4), `RULE-IPM-CGEPIDURALPUMPTRIALS-001` (cites p. 17), `RULE-IPM-CGFACETBLOCKS-001` (cites p. 31), `RULE-IPM-CGSIINJECTIONS-001` (cites p. 57), `RULE-IPM-CGSYMPATHETICBLOCKS-001` (cites p. 89).
- **Reported Issue:** All 5 rules cite the first page of their respective guideline sections in `2026 Evolent Interventional Pain Management Guidelines.pdf`, which are Table of Contents pages, rather than the pages containing the actual clinical indications (pp. 6–8, 22, 32–34, 58–60, 91–93).
- **Question for Reviewer:** Approve administrative update of citation page metadata to point directly to clinical indication sections?

---

## Priority 5: Ambiguous Policy Phrasing & Discretionary Boundaries

### 18. `RULE-ADV-CG2030-001` — LDCT Lung Cancer Screening Asymptomatic Gate
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 490 (Printed Page 4 of 12).
- **Exact Verbatim Source:** *"Medically necessary ONLY when used to screen for lung cancer in asymptomatic individuals"*
- **Issue:** Policy explicitly restricts screening to asymptomatic patients. Symptomatic patients require diagnostic CT. Active decision tree currently does not evaluate patient symptom status.
- **Question for Reviewer:** Should `patient_is_asymptomatic == true` be added as an explicit gating condition?

### 19. `RULE-ADV-CG2035-002` — Lower Extremity MRI Initial X-Ray (Preferred vs Mandatory)
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 553 (Printed Page 4 of 22).
- **Exact Verbatim Source:** *"NOTE: With a positive orthopedic sign from the list below, an initial X-ray is always preferred; however, it is NOT required UNLESS otherwise specified in bold below."*
- **Issue:** Active rule condition strictly enforces `prior_xray_performed == true`, whereas the policy note specifies it is preferred but NOT required for positive orthopedic exam signs.
- **Question for Reviewer:** Should the rule condition be relaxed to match the policy note, or should the engine maintain the stricter prior X-ray requirement?

### 20. `RULE-ADV-CG2042-001` — Pelvis CT Acute Pain Age Boundary
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 673 (Printed Page 4 of 16).
- **Exact Verbatim Source:** *"For acute pelvic pain in a patient over the age of 65 (2)"*
- **Issue:** Policy specifies "over the age of 65". The rule condition enforces `patient_age > 65`.
- **Question for Reviewer:** Confirm whether patients aged exactly 65 years and 0 days qualify (`>= 65`) or must strictly exceed 65 (`> 65`).

### 21. `RULE-ADV-CG2000-003` / `GAP-ADV-007` — IBD CT Enterography Advisory Consideration
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 9.
- **Exact Verbatim Source:** *"MRI should be considered in young patients to avoid radiation"*
- **Issue:** Blocked governance rule (`NEEDS_HUMAN_REVIEW`). Wording is advisory ("should be considered") rather than an absolute contraindication.
- **Question for Reviewer:** Does this statement constitute a binding denial of CT enterography in young patients, or an advisory recommendation?

### 22. `RULE-ADV-CG2001-001` / `GAP-ADV-019` — CT Abdomen/Pelvis Anti-Unbundling Rule
- **Domain:** Advanced Imaging
- **Source Citation:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`, physical p. 37.
- **Issue:** Blocked governance rule (`NEEDS_HUMAN_REVIEW`). Coding bundling rule requiring combined CPT codes (74176–74178) when both regions are requested.
- **Question for Reviewer:** Should coding bundling rules be enforced at intake/routing or remain in clinical decision logic?
