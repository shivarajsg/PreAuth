# MedRule — Phase 6B: CPT Mapping Validation & Implementation Approval Gate

**Date:** 2026-10-22  
**Status:** Pre-Implementation Validation Complete — Awaiting Final Edit Approval  
**Deliverable:** `reports/phase_06b_mapping_validation.md`  
**Scope:** Active Domains Only (`advanced_imaging`, `interventional_pain_management`)  
**Safety Invariant:** Zero production code, rules, tests, schemas, or database records modified during this step.  

---

## 1. Executive Summary

This validation gate report resolves all five requirements specified in the Phase 6B approval gate before initiating edits to production code:
1. **Mapping Validation:** Every proposed CPT/HCPCS code was verified against the governing policy PDFs and rule definitions. Exactly **145 unique codes** (101 in Advanced Imaging, 44 in IPM) map to the **116 procedure-specific rules**, while the remaining **12 rules** are rigorously classified as shared preambles (3), Place of Service (7), or retrospective reviews (2).
2. **Zero Overlaps or Contradictions:** Cross-domain verification confirmed exactly **0 overlapping CPT codes** between Advanced Imaging and Interventional Pain Management. 100% of the 128 active rules are fully accounted for, with zero orphaned or unmapped rules.
3. **Regex Pattern Verification:** The proposed regex `^[0-9]{4}[0-9A-Z]$|^[A-Z][0-9]{4}$` was tested against all 145 unique mapped codes, achieving a **100% pass rate**. It was confirmed to accept all legitimate formats (133 standard 5-digit CPTs, 7 Category III CPTs, and 5 HCPCS Level II codes) while rejecting whitespace-only, suffixed, and malformed inputs.
4. **Primary Mapping with Secondary Guards:** Exact verified mappings are established as the primary routing authority, guaranteeing that exceptions (such as CPT `27096` in the surgical 20000 series routing to IPM Sacroiliac Joint Injection) are resolved directly without broad range interference.
5. **Shared-Rule Determinism:** Clear, documented inclusion criteria are defined for preamble, Place of Service, and retrospective rules. Shared rules are never returned in isolation without an applicable procedure rule.

---

## 2. Step 1 — Verified Mappings & Supporting Citations

A machine-readable inventory has been generated and validated at `scratch/authoritative_cpt_inventory.json`. Below is the complete authoritative mapping.

### Domain 1: Interventional Pain Management (14 Active Rules)

Source Guidelines:
- `2026 Evolent Clinical Guidelines for Medical Necessity Review: Interventional Pain Management Guidelines.pdf` (102 pages)
- `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` (8 pages)

| Guideline & Service | Active Rule IDs | Authoritative CPT / HCPCS Codes | PDF Citation & Coding Table | Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Guideline 1750:**<br>Epidural Spine Injections | `RULE-IPM-CGEPIDURALINJECTIONS-001`<br>`RULE-IPM-CGEPIDURALINJECTIONS-002` | `62320`, `62321`, `62322`, `62323`, `64479`, `64480`, `64483`, `64484` | PDF pp. 9–10 (printed pp. 6–7), Table: Interlaminar and Transforaminal Epidural injections | `PROCEDURE_SPECIFIC` |
| **Guideline 1750B:**<br>Single Injection Trials for Intrathecal Pumps | `RULE-IPM-CGEPIDURALPUMPTRIALS-001` | `62320`, `62321`, `62322`, `62323`, `64479`, `64480`, `64483`, `64484` | PDF p. 23 (printed p. 7), Table: Epidural trial injections for pump evaluation | `PROCEDURE_SPECIFIC` |
| **Guideline 1751:**<br>Paravertebral Facet Joint Injection / Blocks | `RULE-IPM-CGFACETBLOCKS-001` | `64490`, `64491`, `64492`, `64493`, `64494`, `64495`, `0213T`, `0214T`, `0215T`, `0216T`, `0217T`, `0218T` | PDF p. 35 (printed p. 5), Table: Fluoroscopic/CT and Ultrasound-guided facet blocks | `PROCEDURE_SPECIFIC` |
| **Guideline 1752:**<br>Paravertebral Facet Joint Denervation / Neurotomy | `RULE-IPM-CGFACETDENERVATION-001`<br>`RULE-IPM-CGFACETDENERVATION-002` | `64633`, `64634`, `64635`, `64636` | PDF p. 48 (printed p. 4), Table: Cervical/Thoracic and Lumbar/Sacral radiofrequency neurotomy | `PROCEDURE_SPECIFIC` |
| **Guideline 1756:**<br>Sacroiliac Joint Injections | `RULE-IPM-CGSIINJECTIONS-001` | `27096`, `G0260` | PDF p. 62 (printed p. 6), Table: Sacroiliac joint injection with imaging guidance | `PROCEDURE_SPECIFIC` |
| **Guideline 1753:**<br>Implantable Infusion Pump Insertion | `RULE-IPM-CGINFUSIONPUMPS-001` | `62350`, `62351`, `62355`, `62360`, `62361`, `62362` | PDF p. 71 (printed p. 5), Table: Intrathecal/epidural pump insertion, revision, removal | `PROCEDURE_SPECIFIC`<br>*(Gov. Blocked)* |
| **Guideline 1757:**<br>Spinal Cord Stimulation | `RULE-IPM-CGSPINALCORDSTIM-001`<br>`RULE-IPM-CGSPINALCORDSTIM-002` | `63650`, `63655`, `63661`, `63662`, `63663`, `63664`, `63685`, `63688` | PDF p. 81 (printed p. 5), Table: Neurostimulator array placement, revision, removal, pulse generator | `PROCEDURE_SPECIFIC` |
| **Guideline 1758:**<br>Sympathetic Nerve Blocks | `RULE-IPM-CGSYMPATHETICBLOCKS-001` | `64510`, `64517`, `64520`, `64530` | PDF p. 96 (printed p. 8), Table: Stellate ganglion, hypogastric, lumbar, celiac blocks | `PROCEDURE_SPECIFIC` |
| **Preamble:**<br>Guideline Development Process | `RULE-IPM-PREAMBLEIPM-001` | `*` *(All IPM Procedures)* | PDF p. 2 (printed p. 2), General Medical Director Review Principles | `GENERAL_PREAMBLE`<br>*(Gov. Blocked)* |
| **EPOS 1755:**<br>Place of Service for IPM | `RULE-IPM-EPOS1755-001`<br>`RULE-IPM-EPOS1755-002` | `*` *(All IPM Procedures in Hospital Setting)* | EPOS 1755 PDF pp. 1–3, Outpatient Hospital vs ASC Site of Care Alignment | `PLACE_OF_SERVICE` |

---

### Domain 2: Advanced Diagnostic Imaging (114 Active Rules)

Source Guidelines:
- `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (1,041 pages)
- `EPOS 2067 for Place of Service - Radiology 2026_final.pdf` (11 pages)

#### Procedure-Specific Rules (105 Rules mapping to 101 Unique CPTs)

| Guideline Group | Active Rule IDs | Service Governed | Authoritative CPT / HCPCS Codes | Supporting Citation / Raw Dependencies |
| :--- | :--- | :--- | :--- | :--- |
| **CG 2000** | `RULE-ADV-CG2000-002` to `013` (12 rules) | CT Abdomen and Pelvis | `74175`, `74176`, `74177`, `74178`, `74183` | Guidelines pp. 8–36; verbatim dependencies in `draft_rules.json` |
| **CG 2001** | `RULE-ADV-CG2001-001` to `005` (5 rules) | CT Abdomen (Isolated) | `74150`, `74160`, `74170` | Guidelines pp. 37–52; coding rule & indication dependencies |
| **CG 2002** | `RULE-ADV-CG2002-001`, `002` (2 rules) | CTA Abdomen | `74175` | Guidelines pp. 53–61; CTA abdomen dependencies |
| **CG 2003** | `RULE-ADV-CG2003-001`, `002` (2 rules) | MRA Abdomen | `74185` | Guidelines pp. 62–70; MRA abdomen dependencies |
| **CG 2004** | `RULE-ADV-CG2004-001`, `002` (2 rules) | Abdomen MRI / MRCP | `74181`, `74183` | Guidelines pp. 71–85; MRI abdomen & MRCP dependencies |
| **CG 2005** | `RULE-ADV-CG2005-001`, `002` (2 rules) | CTA Abdomen and Pelvis | `74174`, `74175` | Guidelines pp. 86–95; combined CTA dependencies |
| **CG 2006** | `RULE-ADV-CG2006-001` (1 rule) | CTA Abdominal Aorta with Runoff | `75635` | Guidelines pp. 96–104; aortofemoral runoff dependencies |
| **CG 2007** | `RULE-ADV-CG2007-001` (1 rule) | Bone Marrow MRI | `77084` | Guidelines pp. 105–112; bone marrow blood supply dependencies |
| **CG 2008** | `RULE-ADV-CG2008-001` to `004` (4 rules) | Brain CT | `70450`, `70460`, `70470` | Guidelines pp. 113–138; non-contrast, contrast, with/without CT |
| **CG 2009** | `RULE-ADV-CG2009-001`, `002` (2 rules) | CTA Brain | `70496` | Guidelines pp. 139–148; intracranial CTA dependencies |
| **CG 2010** | `RULE-ADV-CG2010-001` (1 rule) | Magnetic Resonance Spectroscopy (MRS) | `76390` | Guidelines pp. 149–156; MRS brain dependencies |
| **CG 2011** | `RULE-ADV-CG2011-001` (1 rule) | MRA Brain | `70544`, `70546` | Guidelines pp. 157–166; intracranial MRA dependencies |
| **CG 2012** | `RULE-ADV-CG2012-001` to `004` (4 rules) | Brain MRI | `70551`, `70553` | Guidelines pp. 167–205; routine, MS, epilepsy MRI dependencies |
| **CG 2013** | `RULE-ADV-CG2013-001` (1 rule) | Brain PET Scan | `78811`, `78815` | Guidelines pp. 206–218; metabolic brain PET dependencies |
| **CG 2014** | `RULE-ADV-CG2014-001`, `002` (2 rules) | Breast MRI | `77047`, `77048`, `77049` | Guidelines pp. 219–235; unilateral and bilateral breast MRI |
| **CG 2015** | `RULE-ADV-CG2015-001` (1 rule) | Cerebral Perfusion CT | `0042T` | Guidelines pp. 236–244; acute ischemic stroke perfusion CPT |
| **CG 2016** | `RULE-ADV-CG2016-001` (1 rule) | Cervical Spine CT | `72125` | Guidelines pp. 245–258; acute trauma cervical CT dependencies |
| **CG 2017** | `RULE-ADV-CG2017-001` to `003` (3 rules) | Cervical Spine MRI | `72141`, `72142` | Guidelines pp. 259–285; neck pain, myelopathy, cord compression |
| **CG 2018** | `RULE-ADV-CG2018-001` to `003` (3 rules) | Chest CT | `71250`, `71260` | Guidelines pp. 286–315; pulmonary nodule, hemoptysis, infection |
| **CG 2019** | `RULE-ADV-CG2019-001` (1 rule) | Chest MRI | `71550`, `71552` | Guidelines pp. 316–328; mediastinal mass & chest wall MRI |
| **CG 2020** | `RULE-ADV-CG2020-001`, `002` (2 rules) | Chest CTA | `71275` | Guidelines pp. 329–345; pulmonary embolism & aortic dissection |
| **CG 2021** | `RULE-ADV-CG2021-001` (1 rule) | Chest MRA | `71555` | Guidelines pp. 346–355; thoracic aortic MRA dependencies |
| **CG 2022** | `RULE-ADV-CG2022-001` (1 rule) | CT Colonography (Diagnostic) | `74261`, `74262` | Guidelines pp. 356–368; virtual colonoscopy diagnostic dependencies |
| **CG 2023** | `RULE-ADV-CG2023-001` (1 rule) | CT Colonography (Screening) | `74263` | Guidelines pp. 369–378; virtual colonoscopy screening dependencies |
| **CG 2024** | `RULE-ADV-CG2024-001` (1 rule) | Quantitative CT (QCT) Bone Density | `77078` | Guidelines pp. 379–388; QCT spine/hip bone density dependencies |
| **CG 2026** | `RULE-ADV-CG2026-001` (1 rule) | CT/MRI Guidance for Needle Placement | `77012`, `77021` | Guidelines pp. 389–400; biopsy/aspiration imaging guidance |
| **CG 2027** | `RULE-ADV-CG2027-001` (1 rule) | Fetal MRI | `74712`, `74713` | Guidelines pp. 401–415; fetal anatomic MRI dependencies |
| **CG 2028** | `RULE-ADV-CG2028-001` (1 rule) | Functional Brain MRI (fMRI) | `70554`, `70555` | Guidelines pp. 416–428; presurgical eloquent cortex mapping |
| **CG 2029** | `RULE-ADV-CG2029-001` (1 rule) | Follow-Up Limited CT | `76380` | Guidelines pp. 429–438; limited localized CT scan dependencies |
| **CG 2030** | `RULE-ADV-CG2030-001` (1 rule) | Low Dose CT (LDCT) Lung Screening | `71271` | Guidelines pp. 439–455; annual lung cancer screening CT |
| **CG 2031** | `RULE-ADV-CG2031-001` (1 rule) | Low Field MRI Non-Coverage Exclusion | `S8042` | Guidelines PDF p. 498, Coding Section: HCPCS S8042 |
| **CG 2032** | `RULE-ADV-CG2032-001`, `002` (2 rules) | Lower Extremity CT | `73700`, `73701`, `73702` | Guidelines pp. 499–520; hip, knee, ankle, foot CT |
| **CG 2033** | `RULE-ADV-CG2033-001` (1 rule) | Lower Extremity CTA | `73706` | Guidelines pp. 521–535; peripheral arterial disease CTA |
| **CG 2034** | `RULE-ADV-CG2034-001` (1 rule) | Lower Extremity MRA | `73725` | Guidelines pp. 536–548; peripheral arterial disease MRA |
| **CG 2035** | `RULE-ADV-CG2035-001` to `003` (3 rules) | Lower Extremity MRI (Knee/Hip/Ankle) | `73721`, `73722`, `73723` | Guidelines pp. 549–590; knee meniscal, ligament, osteonecrosis |
| **CG 2036** | `RULE-ADV-CG2036-001` (1 rule) | Lumbar Spine CT | `72131` | Guidelines pp. 591–605; lumbar trauma / MRI contraindicated |
| **CG 2037** | `RULE-ADV-CG2037-001` to `003` (3 rules) | Lumbar Spine MRI | `72148`, `72158` | Guidelines pp. 606–635; radiculopathy, cauda equina, infection |
| **CG 2038** | `RULE-ADV-CG2038-001` (1 rule) | MR Elastography (MRE) Abdomen | `76391` | Guidelines pp. 636–648; liver fibrosis staging MRE |
| **CG 2039** | `RULE-ADV-CG2039-001` (1 rule) | Neck CT | `70490`, `70491` | Guidelines pp. 649–668; soft tissue neck CT dependencies |
| **CG 2040** | `RULE-ADV-CG2040-001` (1 rule) | Neck CTA | `70498` | Guidelines pp. 669–682; carotid/vertebral artery CTA |
| **CG 2041** | `RULE-ADV-CG2041-001` (1 rule) | Neck MRA | `70547`, `70549` | Guidelines pp. 683–695; extracranial carotid/vertebral MRA |
| **CG 2042** | `RULE-ADV-CG2042-001` (1 rule) | Pelvis CT | `72192`, `72193` | Guidelines pp. 696–710; isolated pelvis CT dependencies |
| **CG 2043** | `RULE-ADV-CG2043-001` (1 rule) | Pelvis CTA | `72191` | Guidelines pp. 711–722; pelvic vascular CTA dependencies |
| **CG 2044** | `RULE-ADV-CG2044-001` (1 rule) | Pelvis MRA | `72198` | Guidelines pp. 723–734; pelvic vascular MRA dependencies |
| **CG 2045** | `RULE-ADV-CG2045-001` (1 rule) | Pelvis MRI | `72195`, `72197` | Guidelines pp. 735–755; perianal fistula, rectal cancer MRI |
| **CG 2046** | `RULE-ADV-CG2046-001` to `004` (4 rules) | PET/CT (Whole Body Oncology) | `78815`, `78816` | Guidelines pp. 756–790; lymphoma, NSCLC, melanoma staging |
| **CG 2047** | `RULE-ADV-CG2047-001`, `002` (2 rules) | Sinus Maxillofacial CT | `70486` | Guidelines pp. 791–810; rhinosinusitis, facial trauma CT |
| **CG 2048** | `RULE-ADV-CG2048-001` (1 rule) | Orbit, Face, Neck MRI | `70540`, `70543` | Guidelines pp. 811–828; optic neuritis, orbital mass MRI |
| **CG 2052** | `RULE-ADV-CG2052-001` (1 rule) | SPECT / SPECT-CT Radiopharmaceutical | `78803`, `78830` | Guidelines pp. 829–845; tumor localization SPECT/CT |
| **CG 2053** | `RULE-ADV-CG2053-001` (1 rule) | Spinal Canal MRA | `72159` | Guidelines pp. 846–855; spinal dural AVM / vascular lesion MRA |
| **CG 2054** | `RULE-ADV-CG2054-001` (1 rule) | Temporal Bone CT | `70480` | Guidelines pp. 856–868; mastoiditis, cholesteatoma CT |
| **CG 2055** | `RULE-ADV-CG2055-001` (1 rule) | TMJ MRI | `70336` | Guidelines pp. 869–880; temporomandibular internal derangement |
| **CG 2056** | `RULE-ADV-CG2056-001`, `002` (2 rules) | Thoracic Spine CT | `72128`, `72129`, `72130` | Guidelines pp. 881–900; thoracic spine trauma / pain CT |
| **CG 2057** | `RULE-ADV-CG2057-001`, `002` (2 rules) | Thoracic Spine MRI | `72146`, `72147`, `72157` | Guidelines pp. 901–925; thoracic myelopathy / back pain MRI |
| **CG 2058** | `RULE-ADV-CG2058-001` (1 rule) | PET Scan Non-Coverage Exclusion | `G0219`, `G0235`, `G0252` | Guidelines pp. 926–935; non-indicated PET screening codes |
| **CG 2061** | `RULE-ADV-CG2061-001`, `002` (2 rules) | Unlisted CT / MRI Procedures | `76497`, `76498` | Guidelines pp. 936–950; unlisted low-dose whole body CT, unlisted MRI |
| **CG 2062** | `RULE-ADV-CG2062-001` (1 rule) | Upper Extremity CT | `73200`, `73201`, `73202` | Guidelines pp. 951–970; shoulder, elbow, wrist, hand CT |
| **CG 2063** | `RULE-ADV-CG2063-001` (1 rule) | Upper Extremity CTA | `73206` | Guidelines pp. 971–982; upper extremity vascular CTA |
| **CG 2064** | `RULE-ADV-CG2064-001` (1 rule) | Upper Extremity MRA | `73225` | Guidelines pp. 983–995; upper extremity vascular MRA |
| **CG 2065** | `RULE-ADV-CG2065-001`, `002` (2 rules) | Upper Extremity MRI | `73221`, `73222`, `73223` | Guidelines pp. 996–1034; rotator cuff, labral tear, joint MRI |

#### Cross-Procedure Shared Rules in Advanced Imaging (9 Rules)

| Rule ID | Clinical Service Label | Policy Section Citation | Classification | Inclusion Condition |
| :--- | :--- | :--- | :--- | :--- |
| `RULE-ADV-PREAMBLE-001` | Diagnostic Imaging General Standards | General Information p. 8 | `GENERAL_PREAMBLE` *(Gov. Blocked)* | Evaluated for all valid active Advanced Imaging CPT requests. |
| `RULE-ADV-CG2000-001` | Clinician Expectation & Documentation | Statement / General Information p. 8 | `GENERAL_PREAMBLE` | Evaluated for all valid active Advanced Imaging CPT requests. |
| `RULE-ADV-EPOS2067-001` | Advanced Imaging Place of Service - Freestanding | EPOS 2067 Policy pp. 1–3 | `PLACE_OF_SERVICE` | Evaluated when case specifies outpatient Place of Service. |
| `RULE-ADV-EPOS2067-002` | POS - Hospital Outpatient Clinical Criteria | EPOS 2067 Policy pp. 3–5 | `PLACE_OF_SERVICE` | Evaluated when case specifies outpatient Place of Service. |
| `RULE-ADV-EPOS2067-003` | POS - Hospital Scanner Capabilities | EPOS 2067 Policy pp. 5–6 | `PLACE_OF_SERVICE` | Evaluated when case specifies outpatient Place of Service. |
| `RULE-ADV-EPOS2067-004` | POS - Hospital Anesthesia / Sedation | EPOS 2067 Policy pp. 6–7 | `PLACE_OF_SERVICE` | Evaluated when case specifies outpatient Place of Service. |
| `RULE-ADV-EPOS2067-005` | POS - Hospital Non-Coverage Redirection | EPOS 2067 Policy pp. 7–9 | `PLACE_OF_SERVICE` | Evaluated when case specifies outpatient Place of Service. |
| `RULE-ADV-CG2066-001` | Emergent Retrospective Review | CG 2066 pp. 1035–1037 | `RETROSPECTIVE_REVIEW` *(Gov. Blocked)* | Evaluated only when case context specifies emergency retrospective review. |
| `RULE-ADV-CG2066-002` | Urgent Retrospective Review | CG 2066 pp. 1037–1040 | `RETROSPECTIVE_REVIEW` *(Gov. Blocked)* | Evaluated only when case context specifies urgent retrospective review. |

---

## 3. Step 2 — Regex Syntax Validation Results

The proposed regex pattern:
```
^[0-9]{4}[0-9A-Z]$|^[A-Z][0-9]{4}$
```
was rigorously tested against:
1. Every one of the 145 unique verified codes in the active inventory.
2. Syntactically valid unsupported codes.
3. Whitespace, suffix, and punctuation edge cases.

### Test Results

```
Total unique mapped codes tested: 145
Failures: 0 (100% pass rate)

Breakdown by Code Format:
- Standard 5-digit CPT codes (133 codes): 100% match (e.g., 72148, 74177, 62323, 64490, 63650, 70553, 73721)
- CPT Category III codes (7 codes): 100% match (0042T, 0213T, 0214T, 0215T, 0216T, 0217T, 0218T)
- HCPCS Level II codes (5 codes): 100% match (G0219, G0235, G0252, G0260, S8042)
```

### Boundary & Rejection Verification

| Input String | Normalized Value | Syntactic Validity (`pattern.match`) | Active Policy Supported | Result Rationale |
| :--- | :--- | :---: | :---: | :--- |
| `""` | `""` | **False** | False | Empty string rejected at schema intake (`EVALUATION_ERROR`). |
| `"   "` | `""` | **False** | False | Whitespace stripped before evaluation; empty string rejected at schema intake. |
| `" 72148 "` | `"72148"` | **True** | **True** | Surrounding whitespace trimmed; valid active CPT code. |
| `"72148-XYZ"` | `"72148-XYZ"` | **False** | False | Hyphenated suffix rejected as syntactically malformed (`EVALUATION_ERROR`). |
| `"7214826"` | `"7214826"` | **False** | False | Length exceeds 5 characters; rejected (`EVALUATION_ERROR`). |
| `"7214"` | `"7214"` | **False** | False | Length under 5 characters; rejected (`EVALUATION_ERROR`). |
| `"!@#$%"` | `"!@#$%"` | **False** | False | Non-alphanumeric punctuation rejected (`EVALUATION_ERROR`). |
| `"30410"` | `"30410"` | **True** | **False** | Syntactically valid CPT; rejected at routing as unsupported (`POLICY_NOT_APPLICABLE`). |
| `"99213"` | `"99213"` | **True** | **False** | Syntactically valid CPT; rejected at routing as unsupported (`POLICY_NOT_APPLICABLE`). |
| `"93458"` | `"93458"` | **True** | **False** | Syntactically valid archived cardio CPT; rejected as cross-domain / unsupported. |
| `"27447"` | `"27447"` | **True** | **False** | Syntactically valid archived ortho CPT; rejected as non-pain surgical code in IPM. |
| `"E0601"` | `"E0601"` | **True** | **False** | Syntactically valid archived DME HCPCS; rejected as unsupported in active domains. |

**Confirmation:** Syntactic validity is completely decoupled from active policy support. A code must first be syntactically valid to pass intake; it is then deterministically checked against the domain's authoritative mapping.

---

## 4. Step 3 — Domain Guards & Documented Exceptions

### Exact Mapping Priority Rule
In accordance with Step 3 instructions, **broad numeric ranges are not the primary authority for clinical domain selection**. 

The routing sequence enforces:
1. **Primary Authority:** Exact lookup in `ACTIVE_AI_CPT_RULE_MAP` or `ACTIVE_IPM_CPT_RULE_MAP`. If a code is present in the domain's verified map, it routes to its exact procedure rules regardless of broad numeric series.
2. **Secondary Safeguards:** If a code is **not** present in the requested domain's map, secondary guards classify the mismatch using explicit evidence-backed cross-domain logic rather than broadcasting to all rules.

### Handled Documented Exceptions

| Exception Code | Standard Numeric Series | Actual Clinical Guideline & Domain | How Handled Under Primary Authority |
| :--- | :--- | :--- | :--- |
| **`27096`** | Surgical / Musculoskeletal (20000 series) | IPM Guideline 1756 (Sacroiliac Joint Injections) | Verified in `ACTIVE_IPM_CPT_RULE_MAP`. When submitted under IPM, it routes directly to [RULE-IPM-CGSIINJECTIONS-001](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json). Never rejected by surgical range guards. |
| **`G0260`** | HCPCS Level II temporary code | IPM Guideline 1756 (Sacroiliac Joint Injections) | Verified in `ACTIVE_IPM_CPT_RULE_MAP`. Routes directly to [RULE-IPM-CGSIINJECTIONS-001](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json). |
| **`0042T`** | Category III tracking code | Advanced Imaging CG 2015 (Cerebral Perfusion CT) | Verified in `ACTIVE_AI_CPT_RULE_MAP`. Routes directly to [RULE-ADV-CG2015-001](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json). |
| **`0213T–0218T`** | Category III tracking code | IPM Guideline 1751 (Ultrasound Facet Joint Blocks) | Verified in `ACTIVE_IPM_CPT_RULE_MAP`. Routes directly to [RULE-IPM-CGFACETBLOCKS-001](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json). |
| **`S8042`** | HCPCS Level II private payer code | Advanced Imaging CG 2031 (Low Field MRI Exclusion) | Verified in `ACTIVE_AI_CPT_RULE_MAP`. Routes directly to [RULE-ADV-CG2031-001](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json). |
| **`G0219, G0235, G0252`** | HCPCS Level II codes | Advanced Imaging CG 2058 (PET Scan NOS Exclusion) | Verified in `ACTIVE_AI_CPT_RULE_MAP`. Routes directly to [RULE-ADV-CG2058-001](file:///d:/PreAuth/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json). |

### Secondary Cross-Domain Guard Rules

If the code is **not** in the domain's primary mapping table:
- **In `advanced_imaging`:**
  - If code is in `ACTIVE_IPM_CPT_RULE_MAP` or `60000 <= int(code) <= 69999` -> `POLICY_NOT_APPLICABLE` (*Interventional pain procedure outside imaging scope*).
  - If code is in cardiology range `93000 <= int(code) <= 93999` -> `POLICY_NOT_APPLICABLE` (*Cardiology procedure outside imaging scope*).
  - If code is in surgical range `10000 <= int(code) <= 59999` -> `POLICY_NOT_APPLICABLE` (*Surgical procedure outside imaging scope*).
  - Otherwise -> `POLICY_NOT_APPLICABLE` (*Unsupported procedure under active imaging policies*).
- **In `interventional_pain_management`:**
  - If code is in `ACTIVE_AI_CPT_RULE_MAP` or `70000 <= int(code) <= 79999` -> `POLICY_NOT_APPLICABLE` (*Diagnostic radiology code outside IPM scope*).
  - If code is in surgical range `10000 <= int(code) <= 59999` (and not `27096`) -> `POLICY_NOT_APPLICABLE` (*Non-pain surgical code outside IPM scope*).
  - If code is in cardiology range `93000 <= int(code) <= 93999` -> `POLICY_NOT_APPLICABLE` (*Cardiology code outside IPM scope*).
  - Otherwise -> `POLICY_NOT_APPLICABLE` (*Unsupported procedure under active IPM policies*).

---

## 5. Step 4 — Confirmed Expected Rule Selections & Counts

Expected rule counts must be derived from the inventory, not arbitrary expectations.

### Rule Selection Composition Formulas

$$\text{Total Routed Rules} = N_{\text{procedure-specific}} + N_{\text{preamble}} + N_{\text{place-of-service}}$$

- In **Advanced Imaging**:
  - $N_{\text{preamble}} = 2$ (`RULE-ADV-PREAMBLE-001` + `RULE-ADV-CG2000-001`).  
    *(Note: If only `RULE-ADV-PREAMBLE-001` is classified as preamble, $N_{\text{preamble}} = 1$. Both options are shown below).*
  - $N_{\text{place-of-service}} = 5$ (`RULE-ADV-EPOS2067-001` through `005`) when outpatient Place of Service is evaluated; $0$ if Place of Service is not evaluated.
- In **Interventional Pain Management**:
  - $N_{\text{preamble}} = 1$ (`RULE-IPM-PREAMBLEIPM-001`).
  - $N_{\text{place-of-service}} = 2$ (`RULE-IPM-EPOS1755-001`, `002`) when outpatient Place of Service is evaluated; $0$ if Place of Service is not evaluated.

### Confirmed Count Matrix for Regression Cases

| Procedure Code | Requested Service | Domain | Procedure Rules ($N_{\text{proc}}$) | Preamble Rules ($N_{\text{preamble}}$) | Place of Service ($N_{\text{pos}}$) | Confirmed Total Count (with POS) | Exact Selected Rule IDs |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **`72148`** | Lumbar Spine MRI | `advanced_imaging` | **2** | 2 | 5 | **9** *(or 8 if CG2000-1 excluded)* | `RULE-ADV-CG2037-001`<br>`RULE-ADV-CG2037-002`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-CG2000-001`<br>`RULE-ADV-EPOS2067-001..005` |
| **`74177`** | CT Abdomen & Pelvis | `advanced_imaging` | **11** | 2 | 5 | **18** *(or 17 if CG2000-1 excluded)* | `RULE-ADV-CG2000-002..009, 011..013`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-CG2000-001`<br>`RULE-ADV-EPOS2067-001..005` |
| **`70553`** | Brain MRI | `advanced_imaging` | **4** | 2 | 5 | **11** *(or 10 if CG2000-1 excluded)* | `RULE-ADV-CG2012-001..004`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-CG2000-001`<br>`RULE-ADV-EPOS2067-001..005` |
| **`73721`** | Knee MRI | `advanced_imaging` | **3** | 2 | 5 | **10** *(or 9 if CG2000-1 excluded)* | `RULE-ADV-CG2035-001..003`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-CG2000-001`<br>`RULE-ADV-EPOS2067-001..005` |
| **`62322`** | Lumbar Epidural | `interventional_pain_management` | **3** | 1 | 2 | **6** | `RULE-IPM-CGEPIDURALINJECTIONS-001`<br>`RULE-IPM-CGEPIDURALINJECTIONS-002`<br>`RULE-IPM-CGEPIDURALPUMPTRIALS-001`<br>`RULE-IPM-PREAMBLEIPM-001`<br>`RULE-IPM-EPOS1755-001..002` |
| **`62323`** | Lumbar Epidural w/ fluoro | `interventional_pain_management` | **3** | 1 | 2 | **6** | *(Same as 62322)* |
| **`64490`** | Facet Joint Block | `interventional_pain_management` | **1** | 1 | 2 | **4** | `RULE-IPM-CGFACETBLOCKS-001`<br>`RULE-IPM-PREAMBLEIPM-001`<br>`RULE-IPM-EPOS1755-001..002` |
| **`63650`** | Spinal Cord Stimulator | `interventional_pain_management` | **2** | 1 | 2 | **5** | `RULE-IPM-CGSPINALCORDSTIM-001`<br>`RULE-IPM-CGSPINALCORDSTIM-002`<br>`RULE-IPM-PREAMBLEIPM-001`<br>`RULE-IPM-EPOS1755-001..002` |
| **`30410`** | Rhinoplasty | `advanced_imaging` | **0** | 0 | 0 | **0** (`POLICY_NOT_APPLICABLE`) | None |
| **`99213`** | Office Visit | Either Active Domain | **0** | 0 | 0 | **0** (`POLICY_NOT_APPLICABLE`) | None |
| **`99999`** | Fictitious CPT | Either Active Domain | **0** | 0 | 0 | **0** (`POLICY_NOT_APPLICABLE`) | None |

### Elimination of Keyword Collision Confirmed
When `73721` (Knee MRI) is requested with lumbar radiculopathy clinical evidence:
- The router selects **only** the 3 Knee MRI rules from `CG 2035` (`RULE-ADV-CG2035-001..003`) plus general preamble/EPOS.
- Lumbar Spine MRI rules (`RULE-ADV-CG2037-*`) are **not** in the candidate set.
- Consequently, Lumbar Spine MRI criteria cannot be evaluated or satisfied.
- The defect reported in Phase 6 is eliminated at the routing stage.

---

## 6. Implementation Plan Identifying Exact Files & Changes

Following your review and final authorization, the remediation will be executed according to this exact plan:

### 1. Checkpoint & Backup Creation
- Create timestamped backups in `scratch/phase6b_backups/` for:
  - `medrule_engine/case_schema.json`
  - `medrule_engine/case_validator.py`
  - `medrule_engine/policy_router.py`
  - `medrule_engine/tests/test_phase3b_integration.py`

### 2. Schema Hardening in `medrule_engine/case_schema.json`
- In `case_schema.json`, update `procedure_code` property:
  ```json
  "procedure_code": {
    "type": "string",
    "pattern": "^[0-9]{4}[0-9A-Z]$|^[A-Z][0-9]{4}$",
    "description": "Standard 5-character alphanumeric CPT or HCPCS billing code."
  }
  ```

### 3. Intake Normalization in `medrule_engine/case_validator.py`
- In `CaseValidator.validate()`:
  - Strip surrounding whitespace from `procedure_code` before schema validation:
    ```python
    if isinstance(case_dict.get("procedure_code"), str):
        case_dict["procedure_code"] = case_dict["procedure_code"].strip()
    ```

### 4. Authoritative Mapping & Symmetric Guards in `medrule_engine/policy_router.py`
- Define module-level immutable mapping dictionaries:
  - `ACTIVE_IPM_CPT_RULE_MAP: Dict[str, List[str]]`
  - `ACTIVE_AI_CPT_RULE_MAP: Dict[str, List[str]]`
- Replace dead code in lines 176–215 with:
  1. Primary authoritative CPT-to-rule lookup.
  2. Symmetric cross-domain guards for non-matching codes.
  3. Safe fallback returning `POLICY_NOT_APPLICABLE` for unsupported CPTs.
  4. Explicit inclusion of general preamble and Place of Service rules only when applicable.

### 5. Automated Regression Test Suite in `medrule_engine/tests/test_phase3b_integration.py`
- Add dedicated test methods asserting exact selected rule IDs and routing outcomes for:
  - Knee MRI 73721 (excludes lumbar rules)
  - Lumbar MRI 72148 (selects exact lumbar rules)
  - CT Abd/Pelvis 74177 (selects exact CT rules)
  - Brain MRI 70553 (selects exact brain rules)
  - IPM CPTs 62322, 62323, 64490, 63650 (selects exact IPM rules)
  - Unsupported CPTs 30410, 99213, 99999 (`POLICY_NOT_APPLICABLE`)
  - Whitespace-only, suffixed, and malformed codes (validation rejection)
  - Symmetric cross-domain misrouting (rejected with `POLICY_NOT_APPLICABLE`)
- Run full pytest test suite to confirm 100% pass rate (target: 206 passing tests).

---

## 7. Approval Request & Stop Condition

All mapping validation checks have passed. No ambiguous or contradictory mappings remain.

**I am stopping here in accordance with instructions. Please review this validation report and confirm your approval to proceed with editing production files.**
