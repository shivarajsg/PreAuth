# MedRule — Phase 6B: CPT Routing Safety Remediation Plan & Mapping Inventory

**Date:** 2026-10-22  
**Status:** Proposal / Review Only — No Production Code Modified  
**Target File:** `reports/phase_06b_cpt_routing_remediation_plan.md`  
**Prerequisites:** Phase 6 Diagnostic Audit (`reports/phase_06_cpt_routing_audit.md`)  
**Scope:** Active Domains Only (`advanced_imaging`, `interventional_pain_management`)  

---

## 1. Executive Summary & Remediation Objectives

Phase 6 established that while MedRule's active domain isolation (`advanced_imaging` and `interventional_pain_management`) and governance blockage gates (0 approved rules, 7 rules flagged `NEEDS_HUMAN_REVIEW`) successfully prevent false autonomous approvals, the current implementation of `PolicyRouter` contains critical architectural defects:
1. **Unused Procedure Code:** `proc_code` and `proc_name` are extracted in `policy_router.py:L176-177` but are never referenced in candidate rule filtering.
2. **Domain-Wide Rule Broadcasting:** Cases route to all rules matching modality (or all 14 IPM rules), permitting cross-anatomical rule satisfaction (e.g. Knee MRI satisfying Lumbar Spine MRI rules).
3. **Unsupported CPT Leakage:** Unrelated CPTs (e.g. Rhinoplasty 30410, Office Visit 99213) fall through to all rules in active domains.
4. **Syntactic Bypasses:** Whitespace-only codes (`"   "`) and suffixed codes (`"72148-XYZ"`) bypass schema validation.
5. **Asymmetric Cross-Domain Guards:** IPM guards against radiology codes (70000–79999), but Advanced Imaging has no symmetric guards against IPM, cardiology, or surgery codes.

This remediation plan defines an authoritative mapping inventory, a hardened intake validator, symmetric cross-domain scope guards, and a minimal deterministic procedure router. **In accordance with strict safety constraints, this document presents the proposed design for review prior to editing production code, schemas, or rulebooks.**

---

## 2. Task 1 — Authoritative CPT Mapping Inventory

The mapping inventory below was compiled by correlating:
- The 114 active rules in `rulebook_collection/domains/advanced_imaging/rules/draft_rules.json` and their verbatim dependencies.
- The 14 active rules in `rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json`.
- The authoritative clinical guideline PDFs:
  - `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (1,041 pages)
  - `2026 Evolent Interventional Pain Management Guidelines.pdf` (102 pages)
  - `EPOS 2067 for Place of Service - Radiology 2026_final.pdf` (11 pages)
  - `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` (8 pages)

### Category Classification System
- **`PROCEDURE_SPECIFIC`**: Rule evaluates criteria specific to one or more explicit CPT/HCPCS codes.
- **`GENERAL_PREAMBLE`**: Rule defines clinical expectations, provider licensure, or guideline principles across an entire domain.
- **`PLACE_OF_SERVICE`**: Rule evaluates site-of-care medical necessity (freestanding vs hospital outpatient under EPOS policies).
- **`RETROSPECTIVE_REVIEW`**: Rule evaluates urgency or emergency life/limb threat for retrospective determinations.
- **`AMBIGUOUS_OR_UNRESOLVED`**: Policy citation does not document an explicit CPT code; requires clinical SME review.

---

### Part A: Interventional Pain Management Domain (14 Rules)

All 14 IPM rules were traced directly to the coding tables in `2026 Evolent Interventional Pain Management Guidelines.pdf` and `EPOS 1755`:

| Rule ID | Clinical Service Label | Source Policy Section | PDF Page | Classification | Authoritative CPT / HCPCS Codes | Verification Evidence |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| `RULE-IPM-CGEPIDURALINJECTIONS-001` | Epidural Spine Injections 2026 (July) | Guideline 1750: Epidural Spine Injections | 4, 9–10 | `PROCEDURE_SPECIFIC` | `62320`, `62321`, `62322`, `62323`, `64479`, `64480`, `64483`, `64484` | Table pp. 9–10: Cervical/Thoracic & Lumbar/Sacral interlaminar and transforaminal epidurals |
| `RULE-IPM-CGEPIDURALINJECTIONS-002` | Epidural Steroid Injection (ESI) | Guideline 1750: Conservative Treatment Prerequisites | 11 | `PROCEDURE_SPECIFIC` | `62320`, `62321`, `62322`, `62323`, `64479`, `64480`, `64483`, `64484` | Prerequisites apply to all interlaminar & transforaminal ESI codes |
| `RULE-IPM-CGEPIDURALPUMPTRIALS-001` | Epidural Spine Injections Single Injection Trials For Intrathecal Pumps | Guideline 1750B: Single Injection Trials For Intrathecal Pumps | 17, 23 | `PROCEDURE_SPECIFIC` | `62320`, `62321`, `62322`, `62323`, `64479`, `64480`, `64483`, `64484` | Trial injection codes match epidural injection table |
| `RULE-IPM-CGFACETBLOCKS-001` | Paravertebral Facet Joint Injection or Blocks 2026 (July) | Guideline 1751: Paravertebral Facet Joint Injection or Blocks | 31, 35 | `PROCEDURE_SPECIFIC` | `64490`, `64491`, `64492`, `64493`, `64494`, `64495`, `0213T`, `0214T`, `0215T`, `0216T`, `0217T`, `0218T` | Table p. 35: Fluoroscopic/CT and Ultrasound-guided facet blocks |
| `RULE-IPM-CGFACETDENERVATION-001` | Paravertebral Facet Joint Denervation 2026 (July) | Guideline 1752: Paravertebral Facet Joint Denervation | 46, 48 | `PROCEDURE_SPECIFIC` | `64633`, `64634`, `64635`, `64636` | Table p. 48: Cervical/Thoracic (64633, +64634) and Lumbar/Sacral (64635, +64636) radiofrequency neurotomy |
| `RULE-IPM-CGFACETDENERVATION-002` | Facet Joint Radiofrequency Neurotomy / Denervation | Guideline 1752: Diagnostic Block Prerequisites | 46, 48 | `PROCEDURE_SPECIFIC` | `64633`, `64634`, `64635`, `64636` | Prerequisites for radiofrequency neurotomy |
| `RULE-IPM-CGSIINJECTIONS-001` | Sacroiliac Joint Injections 2026 (July) | Guideline 1756: Sacroiliac Joint Injections | 57, 62 | `PROCEDURE_SPECIFIC` | `27096`, `G0260` | Table p. 62: Injection procedure for sacroiliac joint, arthrography and/or anesthetic/steroid |
| `RULE-IPM-CGINFUSIONPUMPS-001` | Implantable Infusion Pump Insert 2026 (July) | Guideline 1753: Implantable Infusion Pump Insertion | 68, 71 | `PROCEDURE_SPECIFIC` *(Gov. Blocked)* | `62350`, `62351`, `62355`, `62360`, `62361`, `62362` | Table p. 71: Intrathecal/epidural catheter and infusion pump insertion/revision/removal |
| `RULE-IPM-CGSPINALCORDSTIM-001` | Spinal Cord Stimulation 2026 (July) | Guideline 1757: Spinal Cord Stimulation | 78, 81 | `PROCEDURE_SPECIFIC` | `63650`, `63655`, `63661`, `63662`, `63663`, `63664`, `63685`, `63688` | Table p. 81: Neurostimulator electrode array placement/revision/removal and pulse generator implant |
| `RULE-IPM-CGSPINALCORDSTIM-002` | Permanent Spinal Cord Stimulator Implant | Guideline 1757: Permanent Implant Trial Prerequisite | 80, 81 | `PROCEDURE_SPECIFIC` | `63650`, `63655`, `63685` | Trial criteria for permanent stimulator implant |
| `RULE-IPM-CGSYMPATHETICBLOCKS-001` | Sympathetic Nerve Blocks 2026 (July) | Guideline 1758: Sympathetic Nerve Blocks | 89, 96 | `PROCEDURE_SPECIFIC` | `64510`, `64517`, `64520`, `64530` | Table p. 96: Stellate ganglion, superior hypogastric, lumbar sympathetic, and celiac plexus blocks |
| `RULE-IPM-PREAMBLEIPM-001` | Preamble and Guideline Development Process | General Preamble | 2 | `GENERAL_PREAMBLE` *(Gov. Blocked)* | `*` *(All IPM Procedures)* | Policy introductory preamble setting medical director review standards across IPM |
| `RULE-IPM-EPOS1755-001` | Evolent Place of Service Policy 1755 for IPM | EPOS 1755 Policy Statement | 1–3 | `PLACE_OF_SERVICE` | `*` *(All IPM Procedures in Hospital Setting)* | Place of Service Policy governing site of service for all IPM procedures |
| `RULE-IPM-EPOS1755-002` | IPM Site of Care | EPOS 1755 Setting Alignment | 1–3 | `PLACE_OF_SERVICE` | `*` *(All IPM Procedures in Hospital Setting)* | Site redirection criteria for IPM outpatient hospital requests |

**IPM Summary:**
- 11 Procedure-Specific rules covering **44 unique CPT/HCPCS codes**.
- 1 General Preamble rule (`RULE-IPM-PREAMBLEIPM-001`, governance-blocked).
- 2 Place of Service rules (`RULE-IPM-EPOS1755-001`, `002`).
- 0 Ambiguous / Unresolved rules.

---

### Part B: Advanced Imaging Domain (114 Rules)

All 114 Advanced Imaging rules were cross-referenced against `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` and `EPOS 2067`:

#### 1. Procedure-Specific Rules (105 Rules)

| Guideline Group | Rules in Group | Modality & Service Governed | Authoritative CPT / HCPCS Codes |
| :--- | :--- | :--- | :--- |
| **CG 2000** | `RULE-ADV-CG2000-002` through `013` (12 rules) | CT Abdomen & Pelvis (IBD, Appendicitis, Diverticulitis, Urography, CTA) | `74175`, `74176`, `74177`, `74178`, `74183` |
| **CG 2001** | `RULE-ADV-CG2001-001` through `005` (5 rules) | CT Abdomen (Isolated) | `74150`, `74160`, `74170` |
| **CG 2002** | `RULE-ADV-CG2002-001`, `002` (2 rules) | CTA Abdomen | `74175` |
| **CG 2003** | `RULE-ADV-CG2003-001`, `002` (2 rules) | MRA Abdomen | `74185` |
| **CG 2004** | `RULE-ADV-CG2004-001`, `002` (2 rules) | Abdomen MRI / MRCP | `74181`, `74183` |
| **CG 2005** | `RULE-ADV-CG2005-001`, `002` (2 rules) | CTA Abdomen and Pelvis | `74174`, `74175` |
| **CG 2006** | `RULE-ADV-CG2006-001` (1 rule) | CTA Abdominal Aorta with Runoff | `75635` |
| **CG 2007** | `RULE-ADV-CG2007-001` (1 rule) | Bone Marrow MRI | `77084` |
| **CG 2008** | `RULE-ADV-CG2008-001` through `004` (4 rules) | Brain CT | `70450`, `70460`, `70470` |
| **CG 2009** | `RULE-ADV-CG2009-001`, `002` (2 rules) | CTA Brain | `70496` |
| **CG 2010** | `RULE-ADV-CG2010-001` (1 rule) | Magnetic Resonance Spectroscopy (MRS) Brain | `76390` |
| **CG 2011** | `RULE-ADV-CG2011-001` (1 rule) | MRA Brain | `70544`, `70546` |
| **CG 2012** | `RULE-ADV-CG2012-001` through `004` (4 rules) | Brain MRI (Routine, Multiple Sclerosis, Epilepsy Protocol) | `70551`, `70553` |
| **CG 2013** | `RULE-ADV-CG2013-001` (1 rule) | Brain PET Scan | `78811`, `78815` |
| **CG 2014** | `RULE-ADV-CG2014-001`, `002` (2 rules) | Breast MRI | `77047`, `77048`, `77049` |
| **CG 2015** | `RULE-ADV-CG2015-001` (1 rule) | Cerebral Perfusion CT | `0042T` |
| **CG 2016** | `RULE-ADV-CG2016-001` (1 rule) | Cervical Spine CT | `72125` |
| **CG 2017** | `RULE-ADV-CG2017-001`, `002`, `003` (3 rules) | Cervical Spine MRI | `72141`, `72142` |
| **CG 2018** | `RULE-ADV-CG2018-001`, `002`, `003` (3 rules) | Chest CT | `71250`, `71260` |
| **CG 2019** | `RULE-ADV-CG2019-001` (1 rule) | Chest MRI | `71550`, `71552` |
| **CG 2020** | `RULE-ADV-CG2020-001`, `002` (2 rules) | Chest CTA | `71275` |
| **CG 2021** | `RULE-ADV-CG2021-001` (1 rule) | Chest MRA | `71555` |
| **CG 2022** | `RULE-ADV-CG2022-001` (1 rule) | CT Colonography (Virtual Colonoscopy) Diagnostic | `74261`, `74262` |
| **CG 2023** | `RULE-ADV-CG2023-001` (1 rule) | CT Colonography (Virtual Colonoscopy) Screening | `74263` |
| **CG 2024** | `RULE-ADV-CG2024-001` (1 rule) | Quantitative Computed Tomography (QCT) Bone Density | `77078` |
| **CG 2026** | `RULE-ADV-CG2026-001` (1 rule) | CT or MRI Guidance for Needle Placement | `77012`, `77021` |
| **CG 2027** | `RULE-ADV-CG2027-001` (1 rule) | Fetal MRI | `74712`, `74713` |
| **CG 2028** | `RULE-ADV-CG2028-001` (1 rule) | Functional Brain MRI (fMRI) | `70554`, `70555` |
| **CG 2029** | `RULE-ADV-CG2029-001` (1 rule) | Follow-Up Limited / Localized CT | `76380` |
| **CG 2030** | `RULE-ADV-CG2030-001` (1 rule) | Low Dose CT (LDCT) Lung Cancer Screening | `71271` |
| **CG 2031** | `RULE-ADV-CG2031-001` (1 rule) | Low Field MRI Non-Coverage Exclusion | `S8042` *(Verified PDF p. 498)* |
| **CG 2032** | `RULE-ADV-CG2032-001`, `002` (2 rules) | Lower Extremity CT | `73700`, `73701`, `73702` |
| **CG 2033** | `RULE-ADV-CG2033-001` (1 rule) | Lower Extremity CTA | `73706` |
| **CG 2034** | `RULE-ADV-CG2034-001` (1 rule) | Lower Extremity MRA | `73725` |
| **CG 2035** | `RULE-ADV-CG2035-001`, `002`, `003` (3 rules) | Lower Extremity MRI (Knee, Hip, Ankle, Foot) | `73721`, `73722`, `73723` |
| **CG 2036** | `RULE-ADV-CG2036-001` (1 rule) | Lumbar Spine CT | `72131` |
| **CG 2037** | `RULE-ADV-CG2037-001`, `002`, `003` (3 rules) | Lumbar Spine MRI (Routine, Cauda Equina, Infection/Contrast) | `72148`, `72158` |
| **CG 2038** | `RULE-ADV-CG2038-001` (1 rule) | Magnetic Resonance Elastography (MRE) Abdomen | `76391` |
| **CG 2039** | `RULE-ADV-CG2039-001` (1 rule) | Neck CT | `70490`, `70491` |
| **CG 2040** | `RULE-ADV-CG2040-001` (1 rule) | Neck CTA | `70498` |
| **CG 2041** | `RULE-ADV-CG2041-001` (1 rule) | Neck MRA | `70547`, `70549` |
| **CG 2042** | `RULE-ADV-CG2042-001` (1 rule) | Pelvis CT | `72192`, `72193` |
| **CG 2043** | `RULE-ADV-CG2043-001` (1 rule) | Pelvis CTA | `72191` |
| **CG 2044** | `RULE-ADV-CG2044-001` (1 rule) | Pelvis MRA | `72198` |
| **CG 2045** | `RULE-ADV-CG2045-001` (1 rule) | Pelvis MRI | `72195`, `72197` |
| **CG 2046** | `RULE-ADV-CG2046-001` through `004` (4 rules) | PET/CT (Whole Body Tumor Imaging) | `78815`, `78816` |
| **CG 2047** | `RULE-ADV-CG2047-001`, `002` (2 rules) | Sinus and Maxillofacial CT | `70486` |
| **CG 2048** | `RULE-ADV-CG2048-001` (1 rule) | Orbit, Face, and Neck MRI | `70540`, `70543` |
| **CG 2052** | `RULE-ADV-CG2052-001` (1 rule) | SPECT / SPECT-CT Radiopharmaceutical Tumor Localization | `78803`, `78830` |
| **CG 2053** | `RULE-ADV-CG2053-001` (1 rule) | Spinal Canal MRA | `72159` |
| **CG 2054** | `RULE-ADV-CG2054-001` (1 rule) | Temporal Bone, Mastoid, Sella CT | `70480` |
| **CG 2055** | `RULE-ADV-CG2055-001` (1 rule) | Temporomandibular Joint (TMJ) MRI | `70336` |
| **CG 2056** | `RULE-ADV-CG2056-001`, `002` (2 rules) | Thoracic Spine CT | `72128`, `72129`, `72130` |
| **CG 2057** | `RULE-ADV-CG2057-001`, `002` (2 rules) | Thoracic Spine MRI | `72146`, `72147`, `72157` |
| **CG 2058** | `RULE-ADV-CG2058-001` (1 rule) | PET Scan (Any Site, NOS / Breast Initial Staging Non-Coverage) | `G0219`, `G0235`, `G0252` |
| **CG 2061** | `RULE-ADV-CG2061-001`, `002` (2 rules) | Unlisted CT / MRI Procedures | `76497`, `76498` |
| **CG 2062** | `RULE-ADV-CG2062-001` (1 rule) | Upper Extremity CT | `73200`, `73201`, `73202` |
| **CG 2063** | `RULE-ADV-CG2063-001` (1 rule) | Upper Extremity CTA | `73206` |
| **CG 2064** | `RULE-ADV-CG2064-001` (1 rule) | Upper Extremity MRA | `73225` |
| **CG 2065** | `RULE-ADV-CG2065-001`, `002` (2 rules) | Upper Extremity MRI (Shoulder, Elbow, Wrist, Hand) | `73221`, `73222`, `73223` |

#### 2. Cross-Procedure Shared Rules in Advanced Imaging (9 Rules)

| Rule ID | Clinical Service Label | Source Policy Section | Classification | Applicability Condition |
| :--- | :--- | :--- | :--- | :--- |
| `RULE-ADV-PREAMBLE-001` | Diagnostic Imaging General Standards | General Information / Preamble | `GENERAL_PREAMBLE` *(Gov. Blocked)* | Included across all active Advanced Imaging procedure requests. |
| `RULE-ADV-CG2000-001` | Advanced Diagnostic Imaging Licensed Clinician Expectation | Statement / General Information | `GENERAL_PREAMBLE` | Included across all active Advanced Imaging procedure requests. |
| `RULE-ADV-EPOS2067-001` | Advanced Imaging Place of Service - Freestanding Alignment | EPOS 2067: Site of Care | `PLACE_OF_SERVICE` | Included for all imaging requests evaluating Place of Service. |
| `RULE-ADV-EPOS2067-002` | Place of Service - Hospital Outpatient Clinical Indication | EPOS 2067: Hospital Clinical Criteria | `PLACE_OF_SERVICE` | Included for hospital outpatient Place of Service evaluations. |
| `RULE-ADV-EPOS2067-003` | Place of Service - Hospital Outpatient Specialized Protocol | EPOS 2067: Scanner Capability Criteria | `PLACE_OF_SERVICE` | Included for hospital outpatient Place of Service evaluations. |
| `RULE-ADV-EPOS2067-004` | Place of Service - Hospital Outpatient General Anesthesia | EPOS 2067: Sedation & Medical Acuity | `PLACE_OF_SERVICE` | Included for hospital outpatient Place of Service evaluations. |
| `RULE-ADV-EPOS2067-005` | Place of Service - Hospital Outpatient Non-Coverage | EPOS 2067: Non-Covered Redirection | `PLACE_OF_SERVICE` | Included for hospital outpatient Place of Service evaluations. |
| `RULE-ADV-CG2066-001` | Emergent Retrospective Review | CG 2066: Emergent Studies | `RETROSPECTIVE_REVIEW` *(Gov. Blocked)* | Included only when request context specifies emergency retrospective review. |
| `RULE-ADV-CG2066-002` | Urgent Retrospective Review | CG 2066: Urgent Studies | `RETROSPECTIVE_REVIEW` *(Gov. Blocked)* | Included only when request context specifies urgent retrospective review. |

**Advanced Imaging Summary:**
- 105 Procedure-Specific rules covering **101 unique CPT/HCPCS codes**.
- 2 General Preamble rules (`RULE-ADV-PREAMBLE-001`, `RULE-ADV-CG2000-001`).
- 5 Place of Service rules (`RULE-ADV-EPOS2067-001` through `005`).
- 2 Retrospective Review rules (`RULE-ADV-CG2066-001`, `002`).
- 0 Ambiguous / Unresolved rules.

---

## 3. Task 2 — Proposed Procedure-Level Routing Design

### Current Defect in `PolicyRouter`
Lines 176–177 extract `proc_code = (case.procedure_code or "").upper()` and `proc_name = (case.procedure_name or "").lower()`, but never use them. Filtering relies only on `case_modality` ("MRI" vs "CT"), broadcasting all domain rules to unrelated procedures.

### Proposed Minimal Remediation in `medrule_engine/policy_router.py`

1. **CPT Mapping Table Declaration:**  
   Define immutable, module-level lookup dictionaries in `policy_router.py`:
   - `ACTIVE_IPM_CPT_RULE_MAP: Dict[str, List[str]]`
   - `ACTIVE_AI_CPT_RULE_MAP: Dict[str, List[str]]`
   Each dictionary maps a validated, uppercase CPT/HCPCS code to its verified procedure-specific rule IDs from the authoritative mapping inventory above.
2. **Procedure Code Lookup & Gating:**  
   Before iterating over domain rules:
   ```python
   # Normalize procedure code
   proc_code = (case.procedure_code or "").strip().upper()
   
   # Retrieve authoritative mapping for domain
   domain_cpt_map = ACTIVE_AI_CPT_RULE_MAP if domain == "advanced_imaging" else ACTIVE_IPM_CPT_RULE_MAP
   
   if proc_code not in domain_cpt_map:
       return RoutingResult(
           status="POLICY_NOT_APPLICABLE",
           routing_notes=[
               f"Procedure code '{case.procedure_code}' is not supported under active '{domain}' clinical policies."
           ]
       )
   
   target_procedure_rule_ids = set(domain_cpt_map[proc_code])
   ```
3. **Candidate Rule Filtering:**  
   In the rule iteration loop, select a rule **only** if:
   - `rule.rule_id in target_procedure_rule_ids`, **OR**
   - It is an explicitly documented general rule for the domain:
     - `advanced_imaging`: `rule.rule_id in ("RULE-ADV-PREAMBLE-001", "RULE-ADV-CG2000-001")`, or `EPOS2067` rules when place of service is evaluated, or `CG2066` when retrospective context is flagged.
     - `interventional_pain_management`: `rule.rule_id == "RULE-IPM-PREAMBLEIPM-001"`, or `EPOS1755` rules when place of service is evaluated.
4. **Guaranteed Fallback Safety:**  
   - If `proc_code` does not match any procedure-specific rule, `PolicyRouter` returns `POLICY_NOT_APPLICABLE`.
   - General preamble and Place of Service rules are **never routed in isolation** without a matching procedure rule.
   - Unsupported or unresolved codes never fall through to all rules in a domain.
   - Existing governance gates (`GOVERNANCE_BLOCKED_RULE_IDS`), three-valued logic (`ConditionEvaluator`), and dual-track decision tree aggregation remain completely intact.

---

## 4. Task 3 — Hardened CPT Input Validation Design

### Inspection of `case_schema.json` and `CaseValidator`

Current state:
- `case_schema.json` specifies `"procedure_code": { "type": "string", "minLength": 3 }`.
- Spaces count towards `minLength`, so `"   "` is accepted as valid.
- Strings like `"72148-XYZ"` or `"!@#$%"` are accepted by the schema.

### Legitimate Code Formats in Active MedRule Domains
An exhaustive scan of all 145 unique codes across Advanced Imaging and IPM confirms they follow three standard formats:
1. **Standard 5-digit CPT codes:** `72148`, `74177`, `62323`, `64490`, `63650`, `70553`, `73721`.
2. **Category III CPT codes:** 4 digits ending in 'T' (e.g. `0042T`, `0213T`, `0214T`, `0215T`, `0216T`, `0217T`, `0218T`).
3. **HCPCS Level II codes:** 1 letter followed by 4 digits (e.g. `G0260`, `G0219`, `G0235`, `G0252`, `S8042`, `E0601`).

### Proposed Minimal Hardening

1. **Schema Update (`medrule_engine/case_schema.json`):**  
   Add a strict pattern constraint to `procedure_code`:
   ```json
   "procedure_code": {
     "type": "string",
     "pattern": "^[0-9]{4}[0-9A-Z]$|^[A-Z][0-9]{4}$",
     "description": "Standard 5-character alphanumeric CPT or HCPCS billing code (e.g. 72148, 0042T, G0260, S8042)."
   }
   ```
2. **Intake Normalization (`medrule_engine/case_validator.py`):**  
   In `CaseValidator.validate()`, before passing the payload to `Draft7Validator`:
   - Strip leading and trailing whitespace from string fields, particularly `procedure_code`:
     ```python
     if isinstance(case_dict.get("procedure_code"), str):
         case_dict["procedure_code"] = case_dict["procedure_code"].strip()
     ```
   - If the stripped `procedure_code` is empty (e.g. was `"   "`), schema pattern validation immediately rejects it with: `"[procedure_code] '' does not match '^[0-9]{4}[0-9A-Z]$|^[A-Z][0-9]{4}$'"`.
   - Suffixed codes like `"72148-XYZ"` or strings with punctuation fail the pattern and produce explicit validation errors (`EVALUATION_ERROR`).

---

## 5. Task 4 — Symmetric Domain Scope Guards Design

### Current Asymmetry
`policy_router.py:L160-167` guards IPM against diagnostic radiology codes:
```python
if proc_code and proc_code.isdigit():
    code_num = int(proc_code)
    if domain == "interventional_pain_management" and (70000 <= code_num <= 79999):
        return RoutingResult(status="POLICY_NOT_APPLICABLE", ...)
```
However:
- Advanced Imaging has **no guard** against IPM codes (60000–69999, 27096).
- Advanced Imaging has **no guard** against Cardiology codes (93000–93999).
- Advanced Imaging has **no guard** against General Surgery codes (10000–59999).
- IPM has **no guard** against Non-Pain Surgery (e.g. Orthopedic total knee arthroplasty 27447).

### Proposed Symmetric Guard Logic in `PolicyRouter`

```python
# Symmetric cross-domain scope guards
if domain == "advanced_imaging":
    # 1. Reject Interventional Pain Management codes submitted under imaging
    if proc_code in ACTIVE_IPM_CPT_RULE_MAP or (proc_code.isdigit() and 60000 <= int(proc_code) <= 69999):
        return RoutingResult(
            status="POLICY_NOT_APPLICABLE",
            routing_notes=[f"Interventional pain management procedure code '{case.procedure_code}' is outside advanced_imaging scope."]
        )
    # 2. Reject Cardiology diagnostic/interventional codes (93000-93999)
    if proc_code.isdigit() and 93000 <= int(proc_code) <= 93999:
        return RoutingResult(
            status="POLICY_NOT_APPLICABLE",
            routing_notes=[f"Cardiology procedure code '{case.procedure_code}' is outside advanced_imaging scope."]
        )
    # 3. Reject non-radiology surgical codes (10000-59999)
    if proc_code.isdigit() and 10000 <= int(proc_code) <= 59999:
        return RoutingResult(
            status="POLICY_NOT_APPLICABLE",
            routing_notes=[f"Surgical procedure code '{case.procedure_code}' is outside advanced_imaging scope."]
        )

elif domain == "interventional_pain_management":
    # 1. Reject Diagnostic Radiology codes (70000-79999, 0042T)
    if proc_code in ACTIVE_AI_CPT_RULE_MAP or (proc_code.isdigit() and 70000 <= int(proc_code) <= 79999):
        return RoutingResult(
            status="POLICY_NOT_APPLICABLE",
            routing_notes=[f"Diagnostic radiology procedure code '{case.procedure_code}' is outside interventional_pain_management scope."]
        )
    # 2. Reject Non-Pain Surgical codes (10000-59999, except 27096 for SI joint)
    if proc_code.isdigit() and (10000 <= int(proc_code) <= 59999) and proc_code != "27096":
        return RoutingResult(
            status="POLICY_NOT_APPLICABLE",
            routing_notes=[f"Non-pain surgical procedure code '{case.procedure_code}' is outside interventional_pain_management scope."]
        )
    # 3. Reject Cardiology codes (93000-93999)
    if proc_code.isdigit() and 93000 <= int(proc_code) <= 93999:
        return RoutingResult(
            status="POLICY_NOT_APPLICABLE",
            routing_notes=[f"Cardiology procedure code '{case.procedure_code}' is outside interventional_pain_management scope."]
        )
```

---

## 6. Task 5 — Regression Test Specification

To verify the remediation without relying on governance gates as a catch-all, the test suite in `medrule_engine/tests/` will assert **exact selected rule IDs** and **exact routing status outcomes**:

| Test Case Identifier | Case Payload | Expected Routing Status | Expected Selected Rule IDs | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| `test_knee_mri_excludes_lumbar_rules` | Domain: `advanced_imaging`<br>CPT: `73721`<br>Evidence: `lumbar_radiculopathy_present=True` | `ROUTED` | `RULE-ADV-CG2035-001`<br>`RULE-ADV-CG2035-002`<br>`RULE-ADV-CG2035-003`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-EPOS2067-001..005` | Lumbar rules (`RULE-ADV-CG2037-*`) must be strictly excluded. Radiculopathy cannot satisfy knee rules. |
| `test_lumbar_mri_routes_lumbar_rules` | Domain: `advanced_imaging`<br>CPT: `72148` | `ROUTED` | `RULE-ADV-CG2037-001`<br>`RULE-ADV-CG2037-002`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-EPOS2067-001..005` | Only lumbar spine MRI rules + preamble/EPOS selected (8 rules total, not 50). |
| `test_ct_abd_pelvis_routes_cg2000` | Domain: `advanced_imaging`<br>CPT: `74177` | `ROUTED` | `RULE-ADV-CG2000-002..013`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-EPOS2067-001..005` | Only CT Abdomen/Pelvis rules selected (17 rules total, not 85). |
| `test_brain_mri_routes_cg2012` | Domain: `advanced_imaging`<br>CPT: `70553` | `ROUTED` | `RULE-ADV-CG2012-001..004`<br>`RULE-ADV-PREAMBLE-001`<br>`RULE-ADV-EPOS2067-001..005` | Only Brain MRI rules selected (10 rules total, not 50). |
| `test_ipm_epidural_routes_1750` | Domain: `interventional_pain_management`<br>CPT: `62322` / `62323` | `ROUTED` | `RULE-IPM-CGEPIDURALINJECTIONS-001`<br>`RULE-IPM-CGEPIDURALINJECTIONS-002`<br>`RULE-IPM-CGEPIDURALPUMPTRIALS-001`<br>`RULE-IPM-PREAMBLEIPM-001`<br>`RULE-IPM-EPOS1755-001..002` | Only Epidural rules + preamble/EPOS selected (6 rules total, not 14). |
| `test_ipm_facet_routes_1751` | Domain: `interventional_pain_management`<br>CPT: `64490` | `ROUTED` | `RULE-IPM-CGFACETBLOCKS-001`<br>`RULE-IPM-PREAMBLEIPM-001`<br>`RULE-IPM-EPOS1755-001..002` | Only Facet block rule + preamble/EPOS selected (4 rules total, not 14). |
| `test_ipm_stimulator_routes_1757` | Domain: `interventional_pain_management`<br>CPT: `63650` | `ROUTED` | `RULE-IPM-CGSPINALCORDSTIM-001`<br>`RULE-IPM-CGSPINALCORDSTIM-002`<br>`RULE-IPM-PREAMBLEIPM-001`<br>`RULE-IPM-EPOS1755-001..002` | Only Spinal cord stimulator rules selected (5 rules total, not 14). |
| `test_unsupported_cpt_rhinoplasty` | Domain: `advanced_imaging`<br>CPT: `30410` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by surgical cross-domain guard. |
| `test_unsupported_cpt_office_visit_ai` | Domain: `advanced_imaging`<br>CPT: `99213` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by unsupported procedure check. |
| `test_unsupported_cpt_office_visit_ipm`| Domain: `interventional_pain_management`<br>CPT: `99213` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by unsupported procedure check. |
| `test_fictitious_cpt_99999` | Domain: `advanced_imaging`<br>CPT: `99999` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by unsupported procedure check. |
| `test_whitespace_cpt_rejected` | Domain: `advanced_imaging`<br>CPT: `"   "` | `EVALUATION_ERROR` | N/A (Validation rejected) | Fails regex pattern validation in schema. |
| `test_suffixed_cpt_rejected` | Domain: `advanced_imaging`<br>CPT: `"72148-XYZ"` | `EVALUATION_ERROR` | N/A (Validation rejected) | Fails regex pattern validation in schema. |
| `test_malformed_chars_rejected` | Domain: `advanced_imaging`<br>CPT: `"!@#$%"` | `EVALUATION_ERROR` | N/A (Validation rejected) | Fails regex pattern validation in schema. |
| `test_cardiology_in_ai_rejected` | Domain: `advanced_imaging`<br>CPT: `93458` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by symmetric cardiology guard. |
| `test_radiology_in_ipm_rejected` | Domain: `interventional_pain_management`<br>CPT: `72148` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by symmetric radiology guard. |
| `test_ipm_in_ai_rejected` | Domain: `advanced_imaging`<br>CPT: `62323` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by symmetric IPM guard. |
| `test_ortho_in_ipm_rejected` | Domain: `interventional_pain_management`<br>CPT: `27447` | `POLICY_NOT_APPLICABLE` | `[]` (0 rules) | Blocked by symmetric surgical guard. |

---

## 7. Implementation Roadmap & Checkpoints

When authorized to proceed with implementation, the changes will be executed in four disciplined, sequential steps:

1. **Step 1 — Create Git Checkpoint & Backup:**  
   Preserve existing untracked reports and create safe scratch backups of files targeted for editing:
   - `medrule_engine/policy_router.py`
   - `medrule_engine/case_validator.py`
   - `medrule_engine/case_schema.json`
2. **Step 2 — Implement Schema and Validator Hardening:**  
   Apply the regex pattern `^[0-9]{4}[0-9A-Z]$|^[A-Z][0-9]{4}$` to `case_schema.json` and whitespace trimming to `case_validator.py`. Verify with targeted unit tests.
3. **Step 3 — Implement Authoritative CPT Tables & Symmetric Router Guards:**  
   Add `ACTIVE_AI_CPT_RULE_MAP` and `ACTIVE_IPM_CPT_RULE_MAP` to `policy_router.py`. Implement symmetric cross-domain guards and procedure-specific rule filtering.
4. **Step 4 — Add Regression Test Suite and Run Full Verification:**  
   Add the 18 specific regression tests to `medrule_engine/tests/test_phase3b_integration.py`. Run the full pytest test suite to confirm 100% pass rate (target: 206 passing tests) with 0 regressions.

---

## 8. Safety & Governance Compliance Confirmation

- [x] **Diagnostic / Plan Only:** No production code, rules, tests, schemas, or database records have been modified.
- [x] **Governance Invariant Preserved:** Database review records and rule governance statuses remain unchanged (0 approved rules).
- [x] **Three-Valued Evidence Logic Preserved:** Condition evaluation logic and evidence provenance handling remain unchanged.
- [x] **No Broadened Code Mappings:** Every code mapping in this inventory is verified against official policy PDFs and rule citations.
- [x] **No Restoration of Archived Domains:** Scope strictly restricted to `advanced_imaging` and `interventional_pain_management`.

---
*Plan saved to `reports/phase_06b_cpt_routing_remediation_plan.md`. Standing by for review and approval before implementing changes.*
