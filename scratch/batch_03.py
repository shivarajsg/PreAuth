"""Batch 03 Extraction: CG 2016 through CG 2021 (Cervical Spine, Chest CT/MRI/CTA/MRA)."""
import json
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"
GOV_PDF = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
GOV_URL = "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf"

# Load the existing 2 CG 2017 pilot rules
with open(RULES_DIR / "draft_rules.json", "r", encoding="utf-8") as f:
    existing_rules = json.load(f)

cg2017_pilot_rules = [r for r in existing_rules if r["rule_id"].startswith("RULE-ADV-CG2017-")]

batch_03_new_rules = [
    # CG 2016 - Cervical Spine CT
    {
        "rule_id": "RULE-ADV-CG2016-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 308,
            "printed_page": "Page 5 of 23"
        },
        "source_section": "INDICATIONS FOR CERVICAL SPINE CT / Evaluation of Trauma or Acute Injury (13)",
        "source_quote": "Evaluation of Trauma or Acute Injury (13)",
        "clinical_service_or_procedure": "Cervical Spine CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Acute high-impact blunt cervical trauma or acute injury meeting Canadian C-Spine Rule or NEXUS criteria",
                    "parameter": "acute_cervical_trauma",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Emergency department notes documenting high-risk injury mechanism, midline neck tenderness, or focal neurological deficit"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72125"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Acute cervical trauma pathway for rapid bony fracture evaluation."
    },

    # CG 2017 - Additional Cervical Spine MRI rule
    {
        "rule_id": "RULE-ADV-CG2017-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 330,
            "printed_page": "Page 4 of 26"
        },
        "source_section": "INDICATIONS / Evaluation of Neck Pain (5,6)",
        "source_quote": "Suspected cervical cord compression with any neurological deficits as listed above",
        "clinical_service_or_procedure": "Cervical Spine MRI",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected acute cervical spinal cord compression with objective neurological deficit",
                    "parameter": "suspected_cervical_cord_compression",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurology or spine surgery physical exam documenting motor weakness, sensory level, or hyperreflexia"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72141",
            "CPT 72142"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Urgent cervical cord compression indication bypassing conservative treatment."
    },

    # CG 2018 - Chest CT
    {
        "rule_id": "RULE-ADV-CG2018-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 355,
            "printed_page": "Page 3 of 30"
        },
        "source_section": "INDICATIONS FOR CHEST CT / Follow-Up of Lung Nodules",
        "source_quote": "Incidental pulmonary nodule on x-ray",
        "clinical_service_or_procedure": "Chest CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Incidental solitary or multiple pulmonary nodules identified on recent chest radiograph",
                    "parameter": "incidental_nodule_on_xray",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Chest X-ray report identifying newly discovered pulmonary nodule requiring CT characterization"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 71250",
            "CPT 71260"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Diagnostic follow-up of radiographic pulmonary nodule per Fleischner criteria."
    },
    {
        "rule_id": "RULE-ADV-CG2018-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 357,
            "printed_page": "Page 5 of 30"
        },
        "source_section": "INDICATIONS FOR CHEST CT / Diffuse Lung Disease (DLD) / Interstitial Lung Disease (ILD)",
        "source_quote": "For suspected sarcoidosis after initial workup including Chest x-ray",
        "clinical_service_or_procedure": "Chest CT",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical suspicion of pulmonary sarcoidosis",
                    "parameter": "suspected_sarcoidosis",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Initial diagnostic workup with baseline chest radiograph completed",
                    "parameter": "chest_xray_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Chest X-ray report and clinical evaluation notes detailing respiratory symptoms or lymphadenopathy"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 71260"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Diagnostic prerequisite chest X-ray before high-resolution CT for sarcoidosis."
    },

    # CG 2019 - Chest MRI
    {
        "rule_id": "RULE-ADV-CG2019-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 387,
            "printed_page": "Page 5 of 14"
        },
        "source_section": "INDICATIONS FOR CHEST MRI / Evaluation of Tumor",
        "source_quote": "Evaluation for suspected thymoma in Myasthenia Gravis patients (19)",
        "clinical_service_or_procedure": "Chest MRI",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Confirmed diagnosis of myasthenia gravis",
                    "parameter": "myasthenia_gravis_diagnosed",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Evaluation of the anterior mediastinum to assess for suspected thymoma or thymic hyperplasia",
                    "parameter": "anterior_mediastinal_mass_suspected",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurology consultation note verifying myasthenia gravis diagnosis and positive acetylcholine receptor antibody or EMG findings"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 71550",
            "CPT 71552"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Anterior mediastinal thymoma screening in myasthenia gravis."
    },

    # CG 2020 - Chest CTA
    {
        "rule_id": "RULE-ADV-CG2020-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 399,
            "printed_page": "Page 3 of 19"
        },
        "source_section": "INDICATIONS FOR CHEST COMPUTED TOMOGRAPHY ANGIOGRAPHY (CTA) / Known or Suspected Pulmonary Embolism (PE) (1–5)",
        "source_quote": "Known or Suspected Pulmonary Embolism (PE) (1–5)",
        "clinical_service_or_procedure": "Chest CTA",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical suspicion of acute pulmonary embolism with high pre-test probability (Wells/Geneva score) or positive D-dimer",
                    "parameter": "suspected_pulmonary_embolism",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical evaluation notes documenting Wells score, oxygen saturation, tachycardia, or quantitative D-dimer assay"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 71275"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Emergency and outpatient pulmonary embolism protocol CTA."
    },

    # CG 2021 - Chest MRA
    {
        "rule_id": "RULE-ADV-CG2021-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 418,
            "printed_page": "Page 3 of 19"
        },
        "source_section": "INDICATIONS FOR CHEST MAGNETIC RESONANCE ANGIOGRAPHY (MRA) / Known or Suspected Pulmonary Embolism (PE) (1–5)",
        "source_quote": "Suspected pulmonary embolism when CTA is contraindicated or cannot be",
        "clinical_service_or_procedure": "Chest MRA",
        "rule_type": "conditional_modality_selection",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical suspicion of acute pulmonary embolism",
                    "parameter": "suspected_pulmonary_embolism",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Chest CTA is contraindicated due to severe iodinated contrast allergy or severe renal insufficiency",
                    "parameter": "cta_contraindicated",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Medical documentation detailing severe contrast anaphylaxis history or eGFR precluding iodinated contrast"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 71555"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Alternative modality selection when first-line CTA cannot be safely performed."
    }
]

# Combine CG 2017 pilot rules + new rules for batch 3
batch_03_all_rules = cg2017_pilot_rules + batch_03_new_rules

def main():
    schema_path = RULES_DIR / "schema.json"
    checkpoint_path = CHECKPOINTS_DIR / "batch_03_rules.json"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for i, r in enumerate(batch_03_all_rules, 1):
        jsonschema.validate(instance=r, schema=schema)
        print(f"Batch 3 Rule {i} ({r['rule_id']}): Schema VALID")

    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(batch_03_all_rules, f, indent=2)

    print(f"\nSuccessfully validated and saved {len(batch_03_all_rules)} rules to {checkpoint_path}")

if __name__ == "__main__":
    main()
