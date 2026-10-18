"""Batch 02 Extraction: CG 2007 through CG 2015 (Bone Marrow, Neuro/Brain, Breast MRI, Perfusion)."""
import json
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"
GOV_PDF = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
GOV_URL = "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf"

# Load the existing 2 CG 2012 pilot rules
with open(RULES_DIR / "draft_rules.json", "r", encoding="utf-8") as f:
    existing_rules = json.load(f)

cg2012_pilot_rules = [r for r in existing_rules if r["rule_id"].startswith("RULE-ADV-CG2012-")]

batch_02_new_rules = [
    # CG 2007 - Bone Marrow MRI
    {
        "rule_id": "RULE-ADV-CG2007-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 141,
            "printed_page": "Page 3 of 7"
        },
        "source_section": "INDICATIONS FOR BONE MARROW MRI / Multiple Myeloma",
        "source_quote": "Initial Staging of Known Disease ○ Restaging on Active Treatment ○ Surveillance ■ Annually if asymptomatic",
        "clinical_service_or_procedure": "Bone Marrow MRI",
        "rule_type": "temporal_threshold",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Confirmed diagnosis of multiple myeloma",
                    "parameter": "multiple_myeloma_diagnosed",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Requested for initial staging, restaging on active therapy, or annual asymptomatic surveillance",
                    "parameter": "myeloma_mri_interval_met",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Hematology/oncology consultation note documenting multiple myeloma staging, active chemotherapy/immunotherapy, or annual surveillance date"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 77084"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Surveillance interval and staging indication for multiple myeloma bone marrow MRI."
    },

    # CG 2008 - Brain CT
    {
        "rule_id": "RULE-ADV-CG2008-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 150,
            "printed_page": "Page 5 of 26"
        },
        "source_section": "Stroke and Vascular Disease / Evaluation of Known or Suspected Stroke (11,12)",
        "source_quote": "Evaluation of Known or Suspected Stroke (11,12)",
        "clinical_service_or_procedure": "Brain CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Known or clinically suspected acute ischemic stroke or intracranial hemorrhage",
                    "parameter": "suspected_acute_stroke",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Emergency medical records documenting focal neurologic deficit, NIH Stroke Scale, or last known normal time"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70450",
            "CPT 70460"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Emergency stroke evaluation pathway for non-contrast brain CT."
    },
    {
        "rule_id": "RULE-ADV-CG2008-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 151,
            "printed_page": "Page 6 of 26"
        },
        "source_section": "Evaluation of Known or Suspected Vascular Disease (13)",
        "source_quote": "Evaluation of suspected acute subarachnoid hemorrhage (SAH)",
        "clinical_service_or_procedure": "Brain CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical suspicion of acute subarachnoid hemorrhage",
                    "parameter": "suspected_acute_sah",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical notes documenting sudden onset severe thunderclap headache or signs of meningismus"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70450"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Urgent non-contrast CT for acute subarachnoid hemorrhage."
    },

    # CG 2009 - Brain CTA
    {
        "rule_id": "RULE-ADV-CG2009-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 175,
            "printed_page": "Page 4 of 20"
        },
        "source_section": "INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Aneurysm Screening",
        "source_quote": "For one first degree relative with aneurysm, asymptomatic screening is not indicated and would require a neurological sign or symptom supporting clinical concern for aneurysm",
        "clinical_service_or_procedure": "CTA Brain",
        "rule_type": "exclusion_criterion",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient has only one first-degree relative with intracranial aneurysm",
                    "parameter": "first_degree_aneurysm_relatives_count",
                    "comparator": "EQUALS",
                    "value": 1
                },
                {
                    "condition_id": "COND-002",
                    "description": "Patient is entirely asymptomatic without focal neurological signs or symptoms",
                    "parameter": "patient_is_asymptomatic",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurological evaluation notes documenting active symptoms if CTA is requested with single affected relative"
        ],
        "exclusion_conditions": [
            "Routine asymptomatic intracranial aneurysm screening in patients with only one affected first-degree relative"
        ],
        "decision_effect": "NOT_INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70496"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Explicit policy exclusion requiring at least two first-degree relatives or neurological symptoms for aneurysm screening."
    },

    # CG 2010 - Magnetic Resonance Spectroscopy (MRS)
    {
        "rule_id": "RULE-ADV-CG2010-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 194,
            "printed_page": "Page 3 of 8"
        },
        "source_section": "INDICATIONS FOR BRAIN MRS (2) / Tumor Recurrence vs. Radiation Necrosis (3)",
        "source_quote": "Tumor Recurrence vs. Radiation Necrosis (3)",
        "clinical_service_or_procedure": "Magnetic Resonance Spectroscopy (MRS) Brain",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Known history of treated primary brain tumor or brain metastasis following radiation therapy",
                    "parameter": "prior_brain_radiation_therapy",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Equivocal enlarging or enhancing lesion on conventional MRI where tumor recurrence cannot be distinguished from radiation necrosis",
                    "parameter": "recurrence_vs_necrosis_indeterminate",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Prior brain MRI report demonstrating indeterminate enhancing lesion and neuro-oncology / radiation oncology consultation notes"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 76390"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Specialized MRS indication for differentiating recurrent glioma/metastasis from post-treatment radiation necrosis."
    },

    # CG 2011 - Brain MRA
    {
        "rule_id": "RULE-ADV-CG2011-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 203,
            "printed_page": "Page 4 of 20"
        },
        "source_section": "INDICATIONS FOR BRAIN MR ANGIOGRAPHY / Aneurysm Screening",
        "source_quote": "Repeat study is recommended every 5-7 years",
        "clinical_service_or_procedure": "MRA Brain",
        "rule_type": "temporal_threshold",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "High-risk individual undergoing periodic surveillance for intracranial aneurysm (e.g. 2+ first-degree relatives)",
                    "parameter": "high_risk_aneurysm_screening_qualified",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Interval of at least 5 to 7 years elapsed since prior negative intracranial vascular screening",
                    "parameter": "years_since_prior_aneurysm_screening",
                    "comparator": "GREATER_THAN_OR_EQUAL",
                    "value": 5,
                    "unit": "years"
                }
            ]
        },
        "required_documentation": [
            "Family history verifying two or more first-degree relatives with intracranial aneurysm and prior negative MRA report"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70544",
            "CPT 70546"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "5-7 year periodic interval threshold for high-risk familial aneurysm surveillance."
    },

    # CG 2013 - Brain PET
    {
        "rule_id": "RULE-ADV-CG2013-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 271,
            "printed_page": "Page 2 of 10"
        },
        "source_section": "INDICATIONS FOR BRAIN PET SCAN / Known Brain Tumor or Cancer (1,2)",
        "source_quote": "Evaluation of primary brain lymphoma",
        "clinical_service_or_procedure": "Brain PET Scan",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Confirmed or clinically suspected primary central nervous system lymphoma (PCNSL)",
                    "parameter": "primary_brain_lymphoma",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurology / oncology consultation notes and MRI findings consistent with suspected primary CNS lymphoma"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 78811",
            "CPT 78815"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Oncology metabolic imaging indication for primary central nervous system lymphoma."
    },

    # CG 2014 - Breast MRI
    {
        "rule_id": "RULE-ADV-CG2014-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 282,
            "printed_page": "Page 3 of 15"
        },
        "source_section": "INDICATIONS / High-Risk Breast Cancer Screening (1,2)",
        "source_quote": "Annual screening with Breast MRI for any ONE of the following:",
        "clinical_service_or_procedure": "Breast MRI",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient qualifies for annual high-risk breast cancer screening (e.g., BRCA mutation, lifetime risk > 20%, prior mantle radiation)",
                    "parameter": "high_risk_breast_cancer_screening",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Genetic testing report documenting deleterious BRCA1/BRCA2 mutation or formal risk model calculation showing >= 20% lifetime risk"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 77048",
            "CPT 77049"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "High risk screening indication for breast MRI."
    },
    {
        "rule_id": "RULE-ADV-CG2014-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 285,
            "printed_page": "Page 6 of 15"
        },
        "source_section": "INDICATIONS / Breast Implants",
        "source_quote": "MRI is not indicated for evaluation of saline implant complications",
        "clinical_service_or_procedure": "Breast MRI",
        "rule_type": "exclusion_criterion",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Imaging requested for evaluation of suspected saline breast implant complication or rupture",
                    "parameter": "saline_implant_complication_requested",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Documentation verifying implant composition (saline vs silicone)"
        ],
        "exclusion_conditions": [
            "Breast MRI requested to evaluate suspected rupture or complications of saline implants"
        ],
        "decision_effect": "NOT_INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 77047"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Explicit non-covered policy exclusion barring MRI for saline implant deflation/rupture."
    },

    # CG 2015 - Cerebral Perfusion CT
    {
        "rule_id": "RULE-ADV-CG2015-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 297,
            "printed_page": "Page 3 of 9"
        },
        "source_section": "INDICATIONS / Acute Ischemic Stroke",
        "source_quote": "within 24 hours of known ischemic infarct",
        "clinical_service_or_procedure": "Cerebral Perfusion CT",
        "rule_type": "temporal_threshold",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Acute ischemic stroke being evaluated for endovascular thrombectomy or reperfusion therapy",
                    "parameter": "acute_ischemic_stroke_reperfusion",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Evaluation performed within 24 hours of symptom onset or last known normal",
                    "parameter": "hours_since_stroke_onset",
                    "comparator": "LESS_THAN_OR_EQUAL",
                    "value": 24,
                    "unit": "hours"
                }
            ]
        },
        "required_documentation": [
            "Emergency stroke code progress note detailing time of onset/last known normal within 24-hour window"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 0042T"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "24-hour therapeutic window for cerebral CT perfusion penumbra evaluation."
    }
]

# Combine CG 2012 pilot rules + new rules for batch 2
batch_02_all_rules = cg2012_pilot_rules + batch_02_new_rules

def main():
    schema_path = RULES_DIR / "schema.json"
    checkpoint_path = CHECKPOINTS_DIR / "batch_02_rules.json"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for i, r in enumerate(batch_02_all_rules, 1):
        jsonschema.validate(instance=r, schema=schema)
        print(f"Batch 2 Rule {i} ({r['rule_id']}): Schema VALID")

    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(batch_02_all_rules, f, indent=2)

    print(f"\nSuccessfully validated and saved {len(batch_02_all_rules)} rules to {checkpoint_path}")

if __name__ == "__main__":
    main()
