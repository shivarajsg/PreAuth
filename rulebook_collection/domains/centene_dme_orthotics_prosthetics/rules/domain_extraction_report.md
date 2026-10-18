# MedRule Domain Extraction Report: Centene DME, Orthotics and Prosthetics

**Date**: 2026-10-18  
**Domain**: `centene_dme_orthotics_prosthetics`  
**Governing Documents**:
- `CP.MP.107 (Revision 08-26).pdf` (24 physical pages, Version Revision 08/26, SHA-256: `e67ca1655fa6f1577a760c681283e74ff217a6c6ec29a6745582f3c306dae251`)  
**Referenced Centene Clinical Policies**:
- `CP.MP.48.pdf` (NMES/FES, 7 physical pages, Revision 04/26, SHA-256: `4132be04d9e365612f0dfba0285a7bb91147e8fc99a538d3885d1e2e50529d63`)
- `CP.MP.99.pdf` (Wheelchair Seating, 49 physical pages, Revision 01/24, SHA-256: `a9ae0e53a2538df0bfe1bb23473138b725c4ef9d73d6118d04294ca81eb1626f`)
- `CP.MP.173.pdf` (Intrathecal/Epidural Pain Pump, 10 physical pages, Revision 11/25, SHA-256: `93a61bfcf0e51be58b73d843815049302e1c390aeb35443a6d6540b621e78453`)
- `CP.MP.184.pdf` (Home Mechanical Ventilators, 8 physical pages, Revision 03/25, SHA-256: `c830eb873f55403e05a889ecae7b6cf7a4149095bb47ee93060cf4769ae67571`)
- `CP.MP.185.pdf` (Skin and Soft Tissue Substitutes, 31 physical pages, Revision 09/26, SHA-256: `7ae4585cbbd6d3118cf94ce1dc6cff70a59b6fe6fa513e9a59b668f4e24ebcbb`)
- `CP.MP.203.pdf` (Diaphragmatic/Phrenic Nerve Stimulation, 7 physical pages, Revision 07/26, SHA-256: `8db018bb0bf6d246c4f03932ff82cbf382bf28b2ce3fa3a91b9331003f0b2f3d`)
- `CP.MP.243.pdf` (Implantable Loop Recorder, 8 physical pages, Revision 11/25, SHA-256: `b9150ab4a44b1c55bc1f69d3e5aa4a4753f20815cb53b341fbebf58ca1fcbe90`)  
**External Supporting Authorities**:
- `clm104c20.pdf` (CMS Medicare Claims Processing Manual Ch. 20, 120 physical pages)
- `som107ap_a_hospitals.pdf` (CMS State Operations Manual App A, 616 physical pages)
- `dmepos-quality-standards.pdf` (CMS DMEPOS Quality Standards, 19 physical pages)
- `RESNA_App of Seat Elevation Devices 2019.pdf` (RESNA Position Paper, 39 physical pages)  
**Extraction Status**: **`DOMAIN_COMPLETE_VALIDATED`**

---

## 1. Scope & Corpus Breakdown

The Centene Durable Medical Equipment, Orthotics and Prosthetics (DMEPOS) domain governs coverage criteria, medical necessity guidelines, documentation requirements, and exclusions across durable medical equipment, mobility systems, specialized sensory/speech devices, compression garments, respiratory therapy, and implantable/wearable therapeutic technologies.

| Document Identifier | Policy / Authority Title | Version / Revision | Physical Pages | Governed Unit Role | Status |
|---|---|---|---|---|---|
| `CP.MP.107` | Durable Medical Equipment, Orthotics and Prosthetics | Revision 08/26 | 24 | Primary Governing Policy | `current_2026_verified` |
| `CP.MP.48` | Neuromuscular and Functional Electrical Stimulation | Revision 04/26 | 7 | Referenced Clinical Policy | `current_2026_verified` |
| `CP.MP.99` | Wheelchair Seating and Positioning | Revision 01/24 | 49 | Referenced Clinical Policy | `current_2026_verified` |
| `CP.MP.173` | Implantable Intrathecal and Epidural Pain Pumps | Revision 11/25 | 10 | Referenced Clinical Policy | `current_2026_verified` |
| `CP.MP.184` | Home Mechanical Ventilators | Revision 03/25 | 8 | Referenced Clinical Policy | `current_2026_verified` |
| `CP.MP.185` | Skin and Soft Tissue Substitutes / CTPs | Revision 09/26 | 31 | Referenced Clinical Policy | `current_2026_verified` |
| `CP.MP.203` | Diaphragmatic / Phrenic Nerve Stimulation | Revision 07/26 | 7 | Referenced Clinical Policy | `current_2026_verified` |
| `CP.MP.243` | Implantable Loop Recorder | Revision 11/25 | 8 | Referenced Clinical Policy | `current_2026_verified` |
| `CMS-CPM-CH20` | CMS Claims Processing Manual Ch. 20 (`clm104c20.pdf`) | Rev. 12557 | 120 | External Supporting Authority | `active_reference` |
| `CMS-SOM-APPA` | CMS State Operations Manual App A (`som107ap_a_hospitals.pdf`) | Rev. 248 | 616 | External Supporting Authority | `active_reference` |
| `CMS-DMEPOS-QS`| CMS DMEPOS Quality Standards (`dmepos-quality-standards.pdf`) | 2024 Active | 19 | External Supporting Authority | `active_reference` |
| `RESNA-SEAT` | RESNA Seat Elevation (`RESNA_App of Seat Elevation Devices 2019.pdf`) | 2019 Position | 39 | External Supporting Authority | `active_reference` |
| **Total** | | | **938 pages** | **12 authorities** | |

---

## 2. Rule Extraction Summary

A total of **99 atomic, source-grounded rules** were extracted:

### A. Primary Governing Policy `CP.MP.107` (58 Rules)
1. **Batch 1: General Principles & Standards (`RULE-DME-107-001` to `004`)**:
   - Medical necessity general standard (physician prescription, meaningful contribution to illness/injury treatment).
   - Member upgrades and deluxe features non-coverage (financial responsibility/upgrade liability).
   - Experimental, investigational, or unproven DMEPOS non-coverage standard.
   - Standard wheelchair repair vs replacement (cost comparison threshold and useful lifetime).
2. **Batch 2: Airway Clearance & Respiratory Therapy (`RULE-DME-107-005` to `013`)**:
   - Mechanical insufflation-exsufflation (cough assist, E0482) for neuromuscular disease.
   - High-frequency chest wall compression (HFCWC, E0483 - Vest / AffloVest) daily secretion criteria.
   - Oscillating positive expiratory pressure (OPEP, E0484) and newly added 2026 oscillating lung expansion (OLE, E0469 / Metaneb) devices.
   - Intermittent positive pressure breathing (IPPB, E0500) and tracheostomy suction pumps.
3. **Batch 3: Compression Therapy & Lymphedema Pumps (`RULE-DME-107-014` to `023`)**:
   - Non-segmented and segmented pneumatic compression devices (E0650, E0651, E0652) with calibrated pressure gradient criteria.
   - 2026 newly covered non-pneumatic compression appliances (E0680, E0681) requiring documented 6-month trial failure of standard compression garments.
   - Custom gradient pressure garments (A6549, S8420-S8428) for severe refractory lymphedema.
4. **Batch 4: Specialized Mobility, External Pumps & Cardiac Devices (`RULE-DME-107-024` to `037`)**:
   - Standing systems (E0638, E0641, E0642) for severe fixed flexion contracture and non-ambulatory members.
   - Wearable cardioverter defibrillators (WCD, K0606) for sudden cardiac death prevention (30-day initial limit, 90-day post-CABG waiting period).
   - Walkasins peripheral neuropathy gait sensory sensory orthosis (L8720, L8721).
   - External ambulatory infusion pumps (E0781, E0784) for continuous chemotherapy or specialized insulin infusion.
   - Electrical bone growth stimulators for nonunion of fractures.
5. **Batch 5: Speech, Sensory & Safety Equipment (`RULE-DME-107-038` to `048`)**:
   - Speech generating devices (E2500 - E2510) and alternative access accessories (E2511 - E2599) with prerequisite SLP evaluation.
   - Video magnification systems (E1660) requiring best-corrected visual acuity $\le 20/200$ and clinical visual rehabilitation.
   - Cranial remodeling orthosis (S1040) requiring cephalic index / diagonal asymmetry $> 2$ standard deviations and age 3–18 months.
   - Enclosed safety beds (E0300) requiring documented persistent self-injurious behavior or elopement risk.
6. **Batch 6: General DMEPOS Non-Covered Exclusions (`RULE-DME-107-049` to `058`)**:
   - Cold therapy units, hydrotherapy whirlpools, air conditioners/cleaners, home exercise equipment, seat lift mechanisms, bedboards, and non-medical comfort accessories.

### B. Referenced Centene Clinical Policies (41 Rules)
1. **`CP.MP.48`: NMES & FES (3 Rules, `RULE-DME-048-001` to `003`)**:
   - NMES for disuse muscle atrophy with intact peripheral nerve conduction.
   - FES for spinal cord injury ambulation/transfers following successful clinical trial.
   - Explicit exclusion of NMES/FES in lower motor neuron lesions and peripheral denervation.
2. **`CP.MP.99`: Wheelchair Seating & Positioning (7 Rules, `RULE-DME-099-001` to `007`)**:
   - Comprehensive multidisciplinary PT/OT seating evaluation standards.
   - Custom-fitted planar and contoured seat and back cushions for postural instability and skin breakdown prevention.
   - Dynamic seating components and headrests for severe cervical hyperextension/dystonia.
   - Thoracic lateral supports and foot positioning systems.
   - Power tilt/recline and seat elevation mechanisms (aligning with RESNA seat elevation principles).
   - Comfort cushion exclusions.
3. **`CP.MP.173`: Implantable Intrathecal & Epidural Pain Pumps (6 Rules, `RULE-DME-173-001` to `006`)**:
   - Mandatory preliminary screening trial requirement ($\ge 50\%$ pain or spasticity reduction).
   - Permanent programmable pump implantation for refractory chronic non-malignant pain.
   - Permanent pump implantation for intractable malignant cancer pain.
   - Intrathecal baclofen pump for severe refractory spasticity of cerebral or spinal origin.
   - Psychological evaluation clearance prerequisite.
   - Non-covered contraindications and exclusions.
4. **`CP.MP.184`: Home Mechanical Ventilators (7 Rules, `RULE-DME-184-001` to `007`)**:
   - Non-invasive mechanical ventilators for neuromuscular disease ($\text{PaCO}_2 \ge 45\text{ mmHg}$).
   - Non-invasive mechanical ventilators for thoracic restrictive disorders.
   - Non-invasive mechanical ventilators for severe chronic COPD ($\text{PaCO}_2 \ge 52\text{ mmHg}$ or persistent nocturnal desaturation).
   - Non-invasive mechanical ventilators for obesity hypoventilation syndrome (OHS) initial 3-month trial.
   - Continuation criteria after initial 3-month trial based on clinical compliance and improved ventilation.
   - Invasive mechanical home ventilators via tracheostomy tube.
   - Strict non-coverage exclusion prohibiting ventilator use simply to deliver RAD or CPAP therapy.
5. **`CP.MP.185`: Skin and Soft Tissue Substitutes / CTPs (9 Rules, `RULE-DME-185-001` to `009`)**:
   - Initial 4-week application for diabetic foot ulcers (DFU) failing conservative wound care.
   - Initial 4-week application for venous leg ulcers (VLU) failing standard compression therapy.
   - Non-covered DFU/VLU scenarios (ulcer $> 12$ weeks, $> 8$ applications per episode, uninfected wound bed prerequisite).
   - Post-mastectomy breast reconstruction soft tissue support.
   - Second- and third-degree severe burn wound management.
   - Post-Mohs micrographic surgical defect reconstruction.
   - Complex abdominal wall reconstruction and hernia repair.
   - General limitations, 12-week episode caps, and wastage documentation standards.
   - Mandatory smoking cessation counseling and ruler-scaled photographic documentation.
6. **`CP.MP.203`: Diaphragmatic / Phrenic Nerve Stimulation (3 Rules, `RULE-DME-203-001` to `003`)**:
   - High spinal cord injury / quadriplegia diaphragmatic pacing with documented bilateral intact phrenic nerve conduction.
   - Congenital central hypoventilation syndrome (CCHS / Ondine's curse) pacing.
   - Explicit non-coverage contraindication for Amyotrophic Lateral Sclerosis (ALS) due to motor neuron degeneration.
7. **`CP.MP.243`: Implantable Loop Recorder (6 Rules, `RULE-DME-243-001` to `006`)**:
   - Recurrent unexplained syncope with high risk or recurrent episodes after non-diagnostic external monitoring.
   - Cryptogenic ischemic stroke or TIA evaluation in members aged $\ge 40$ years without documented atrial fibrillation.
   - Recurrent unexplained palpitations with documented structural heart disease.
   - High-risk ventricular arrhythmias and post-infarction evaluation.
   - Non-diagnostic Holter / event monitoring documentation prerequisite.
   - Exclusions for transient reversible causes or non-syncopal falls.

---

## 3. Current vs Historical Policy Version Isolation

Centene revised `CP.MP.107` between **Revision 11/24** (21 pages) and **Revision 08/26** (24 pages). The MedRule Phase 2D extraction enforces strict version isolation:

| Clinical / Coverage Area | Revision 11/24 (Historical) | Revision 08/26 (`current_2026_verified`) | Extraction Treatment in Phase 2D |
|---|---|---|---|
| **General Necessity Standard** | Section I general text | Explicit Section I.A.1 standard added | Extracted as `RULE-DME-107-001` |
| **Non-Pneumatic Compression** | Not listed | Added coverage for E0680, E0681 | Extracted as `RULE-DME-107-021`, `022` |
| **Oscillating Lung Expansion** | Not listed | Added coverage for E0469 (OLE / Metaneb) | Extracted as `RULE-DME-107-009` |
| **Walkasins Neuropathy Device** | Not listed | Added coverage for L8720, L8721 | Extracted as `RULE-DME-107-028` |
| **Wearable Defibrillator (WCD)** | General 90-day text | 30-day initial increment limit added | Extracted as `RULE-DME-107-033`, `034` |
| **Video Magnification System** | General visual acuity | Strict $\le 20/200$ acuity threshold added | Extracted as `RULE-DME-107-040` |
| **AFO & Prosthetic Codes** | Contained L1933, L1952, L8030 | Removed; deferred to dedicated policies | Excluded from CP.MP.107 rules |

All 99 extracted rules strictly reference `current_2026_verified` policy versions and physical PDF text layers. Zero historical contamination exists.

---

## 4. Governance & Human Review Queue Analysis

In accordance with strict clinical safety standards:
- **Zero rules marked `APPROVED`**.
- **70 rules** marked `DRAFT` (deterministic criteria fully modeled with objective parameters and comparators).
- **29 rules** marked `NEEDS_HUMAN_REVIEW` and cataloged in [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/human_review_queue.csv).

Key reasons for human review routing include:
1. **Medical Director / Peer Review Discretion**: Upgraded equipment requests, convenience determinations, and experimental/unproven equipment exceptions (`RULE-DME-107-002`, `003`).
2. **Multidisciplinary Evaluation Sign-Off**: Wheelchair seating evaluations by PT/OT and ATP-certified providers (`RULE-DME-099-001`).
3. **Psychological Clearance & Trial Verification**: Intrathecal pain pump preliminary trial relief ($\ge 50\%$) and psychological stability assessment (`RULE-DME-173-001`, `005`).
4. **Ventilator vs RAD Boundary Adjudication**: Verification that home ventilator requests are not being utilized to deliver RAD or CPAP therapy (`RULE-DME-184-001`, `007`).
5. **Wound Healing & Wastage Verification**: Episode duration tracking ($\le 12$ weeks), repeat application responsiveness, and open package wastage verification for skin substitutes (`RULE-DME-185-001`, `008`).
6. **Cryptogenic Stroke Neurological Workup**: Verification that comprehensive cardiovascular and neurological etiologies have been excluded prior to ILR implantation (`RULE-DME-243-002`).

---

## 5. Artifact Manifest

All generated artifacts reside in the canonical domain rules directory:

1. **Checkpoint Rules**:
   - `checkpoints/batch_01_cpmp107_general_standards.json` (4 rules)
   - `checkpoints/batch_02_cpmp107_respiratory_therapy.json` (9 rules)
   - `checkpoints/batch_03_cpmp107_compression_therapy.json` (10 rules)
   - `checkpoints/batch_04_cpmp107_mobility_specialized.json` (14 rules)
   - `checkpoints/batch_05_cpmp107_speech_sensory_safety.json` (11 rules)
   - `checkpoints/batch_06_cpmp107_general_exclusions.json` (10 rules)
   - `checkpoints/batch_07_cpmp48_nmes_fes.json` (3 rules)
   - `checkpoints/batch_08_cpmp99_wheelchair_seating.json` (7 rules)
   - `checkpoints/batch_09_cpmp173_intrathecal_pump.json` (6 rules)
   - `checkpoints/batch_10_cpmp184_home_ventilators.json` (7 rules)
   - `checkpoints/batch_11_cpmp185_skin_substitutes.json` (9 rules)
   - `checkpoints/batch_12_cpmp203_phrenic_stimulation.json` (3 rules)
   - `checkpoints/batch_13_cpmp243_implantable_loop_recorder.json` (6 rules)
2. **Consolidated Rules Knowledge Base**:
   - [`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/draft_rules.json) (99 rules, Draft-07 compliant)
3. **Traceability Matrix**:
   - [`source_to_rule_traceability.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/source_to_rule_traceability.csv) (99 rows)
4. **Human Review Queue**:
   - [`human_review_queue.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/human_review_queue.csv) (29 rows)
5. **Guideline Coverage Inventory**:
   - [`guideline_coverage_inventory.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/guideline_coverage_inventory.csv) (17 sections and authorities tracked)
6. **Completeness Audit**:
   - [`completeness_audit.csv`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/completeness_audit.csv) (13 audit entries)
7. **Deterministic Quality Test Suite**:
   - [`tests/test_centene_dme_rules.py`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/tests/test_centene_dme_rules.py) (14 tests, 100% passing)
8. **Validation Report**:
   - [`validation_report.md`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/centene_dme_orthotics_prosthetics/rules/validation_report.md)
