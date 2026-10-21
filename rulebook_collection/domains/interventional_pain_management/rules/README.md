# Interventional Pain Management — Verified Rules & Clinical Directory

This directory contains verified, structured prior-authorization rules partitioned according to clinical procedure categories, derived from the **2026 Evolent Clinical Guidelines for Interventional Pain Management** (102 pages, updated from the 2025 baseline) and **Evolent Place of Service Policy EPOS-1755**.

---

## 1. Directory Tree & Procedure Crosswalk

```text
interventional_pain_management/rules/
│
├── epidural_injections/
│   ├── epidural_spine_injections_62321_62323.json       # CPT 62320–62323, 64479–64484 (ESI & Conservative Therapy)
│   └── epidural_pump_trials_62321.json                 # CPT 62320–62323 (Single Injection Trials for Intrathecal Pumps)
│
├── facet_interventions/
│   ├── facet_joint_blocks_64490_64493.json             # CPT 64490–64495, 0213T–0218T (Facet Injections & Medial Branch Blocks)
│   └── facet_radiofrequency_neurotomy_64633_64635.json # CPT 64633–64636 (Facet Denervation & Diagnostic Relief Threshold)
│
├── sacroiliac_joint/
│   └── sacroiliac_joint_injections_27096.json          # CPT 27096, HCPCS G0260 (SI Joint Injections)
│
├── neuromodulation_pumps/
│   ├── spinal_cord_stimulation_63650_63685.json        # CPT 63650, 63655, 63685, 63688 (SCS Trial & Permanent Implant)
│   └── implantable_infusion_pumps_62350_62362.json     # CPT 62350–62362 (Intrathecal Drug Delivery Pump Insertion)
│
├── sympathetic_blocks/
│   └── sympathetic_nerve_blocks_64510_64530.json       # CPT 64510, 64517, 64520, 64530 (Stellate, Celiac, Lumbar)
│
└── cross_cutting/
    ├── ipm_clinical_review_preamble.json               # Evidence-based review standards & hierarchy
    └── epos_1755_site_of_care.json                     # EPOS-1755 Ambulatory Surgery Center / Office vs Outpatient Hospital
```

---

## 2. Verification Metrics
- **Total Rules:** 14
- **Schema Validation:** 100% compliant with [`../../../schemas/medrule_rule_schema.json`](file:///d:/PreAuth/rulebook_collection/schemas/medrule_rule_schema.json)
- **Source Verification:** Every rule quotes directly from governing PDFs with page citations.
- **Automated Unit Tests:** Validated by [`tests/test_organized_ipm_rules.py`](file:///d:/PreAuth/rulebook_collection/domains/interventional_pain_management/rules/tests/test_organized_ipm_rules.py).
