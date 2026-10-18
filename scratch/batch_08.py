"""Batch 08 Extraction: CG 2056 through CG 2066 (Thoracic Spine, Tumor PET, Unlisted Study, Upper Extremity, Urgent/Emergent)."""
import json
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"
GOV_PDF = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
GOV_URL = "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf"

batch_08_rules = [
    # CG 2056 - Thoracic Spine CT
    {
        "rule_id": "RULE-ADV-CG2056-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 905,
            "printed_page": "Page 3 of 20"
        },
        "source_section": "INDICATIONS FOR THORACIC SPINE CT / Evaluation of Neurologic Deficits (1) / When Thoracic Spine MRI is Contraindicated or cannot be performed",
        "source_quote": "When Thoracic Spine MRI is Contraindicated or cannot be performed",
        "clinical_service_or_procedure": "Thoracic Spine CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient has new progressive neurological deficit localizing to the thoracic spine (e.g., extremity weakness, bowel/bladder dysfunction, gait instability)",
                    "parameter": "thoracic_neurologic_deficit_present",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Thoracic spine MRI is contraindicated (e.g. non-MRI-compatible device, severe claustrophobia) or cannot be performed",
                    "parameter": "thoracic_mri_contraindicated_or_unavailable",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical notes detailing progressive thoracic neurological deficits and explicit contraindication to MRI"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72128",
            "CPT 72129",
            "CPT 72130"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Thoracic CT for neurologic deficits when MRI is contraindicated."
    },
    {
        "rule_id": "RULE-ADV-CG2056-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 906,
            "printed_page": "Page 4 of 20"
        },
        "source_section": "INDICATIONS FOR THORACIC SPINE CT / Evaluation of Back Pain (1) / Pain lasting > 4 weeks",
        "source_quote": "Pain lasting > 4 weeks",
        "clinical_service_or_procedure": "Thoracic Spine CT",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Persistent thoracic back pain lasting greater than 4 weeks",
                    "parameter": "thoracic_pain_duration_weeks",
                    "comparator": "GREATER_THAN",
                    "value": 4
                },
                {
                    "condition_id": "COND-002",
                    "description": "Failure of at least 4-6 weeks of conservative management including physical therapy or medications",
                    "parameter": "conservative_therapy_completed",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-003",
                    "description": "Thoracic spine MRI is contraindicated or cannot be performed",
                    "parameter": "thoracic_mri_contraindicated",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Progress notes documenting pain duration, conservative treatment dates and modalities, and MRI contraindication"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72128",
            "CPT 72129",
            "CPT 72130"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Thoracic CT for chronic thoracic pain after failed conservative therapy when MRI contraindicated."
    },
    # CG 2057 - Thoracic Spine MRI
    {
        "rule_id": "RULE-ADV-CG2057-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 925,
            "printed_page": "Page 3 of 23"
        },
        "source_section": "INDICATIONS FOR THORACIC SPINE MRI / Evaluation of Neurologic Deficits (1)",
        "source_quote": "INDICATIONS FOR THORACIC SPINE MRI",
        "clinical_service_or_procedure": "Thoracic Spine MRI",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient has objective physical exam findings of thoracic myelopathy or sensory/motor level deficit",
                    "parameter": "thoracic_myelopathy_or_deficit_present",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurological physical examination documenting motor weakness, sensory level, hyperreflexia, or spastic gait"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72146",
            "CPT 72147",
            "CPT 72157"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Thoracic MRI first-line imaging for thoracic myelopathy and cord compression deficits."
    },
    {
        "rule_id": "RULE-ADV-CG2057-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 926,
            "printed_page": "Page 4 of 23"
        },
        "source_section": "INDICATIONS FOR THORACIC SPINE MRI / Evaluation of Back Pain (1) / Pain lasting > 4 weeks",
        "source_quote": "Pain lasting > 4 weeks",
        "clinical_service_or_procedure": "Thoracic Spine MRI",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Thoracic back pain lasting greater than 4 weeks",
                    "parameter": "thoracic_pain_duration_weeks",
                    "comparator": "GREATER_THAN",
                    "value": 4
                },
                {
                    "condition_id": "COND-002",
                    "description": "Failure of at least 4-6 weeks of conservative management (e.g. physical therapy, chiropractic treatments, home exercise program)",
                    "parameter": "conservative_therapy_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Physical therapy notes or physician progress notes verifying duration of pain and conservative management regimen"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72146",
            "CPT 72147",
            "CPT 72157"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Thoracic MRI for uncomplicated thoracic pain after conservative therapy."
    },
    # CG 2058 - Tumor Imaging PET
    {
        "rule_id": "RULE-ADV-CG2058-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 947,
            "printed_page": "Page 2 of 7"
        },
        "source_section": "SPECIAL NOTE / Non-Covered PET Codes and Indications",
        "source_quote": "Positron Emission Tomography (PET) imaging, any site, not otherwise specified, is a",
        "clinical_service_or_procedure": "PET Scan (Any Site, NOS / Breast Cancer Initial Diagnosis / Non-covered Melanoma)",
        "rule_type": "exclusion_criterion",
        "conditions": {
            "operator": "ANY_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "PET imaging requested using non-specific tumor imaging code (any site, not otherwise specified)",
                    "parameter": "pet_unlisted_nos_requested",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "PET scan requested for initial diagnosis of breast cancer or axillary staging",
                    "parameter": "pet_breast_initial_staging",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Oncology order and clinical notes identifying tumor type, staging intent, and procedure code"
        ],
        "exclusion_conditions": [
            "PET imaging NOS (G0219, G0235, G0252) and initial breast cancer staging are categorically non-covered"
        ],
        "decision_effect": "NOT_INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "HCPCS G0219",
            "HCPCS G0235",
            "HCPCS G0252"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Explicit non-coverage exclusion: PET any site NOS and initial staging of axillary lymph nodes in breast cancer."
    },
    # CG 2061 - Unlisted Study
    {
        "rule_id": "RULE-ADV-CG2061-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 954,
            "printed_page": "Page 2 of 10"
        },
        "source_section": "INDICATIONS FOR UNLISTED MRI / Radiation treatment planning",
        "source_quote": "Unlisted MRI (CPT Code 76498), can be used in the context of:",
        "clinical_service_or_procedure": "Unlisted MRI Procedure (CPT 76498)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "MRI is requested specifically for radiation therapy treatment planning and simulation",
                    "parameter": "radiation_treatment_planning_simulation",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Radiation oncologist treatment planning orders specifying immobilization, tumor target delineation, or fusion protocol"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 76498"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Unlisted MRI indicated for radiation therapy treatment planning."
    },
    {
        "rule_id": "RULE-ADV-CG2061-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 956,
            "printed_page": "Page 4 of 10"
        },
        "source_section": "INDICATIONS FOR UNLISTED CT / Low Dose Whole Body CT",
        "source_quote": "INDICATIONS FOR UNLISTED CT",
        "clinical_service_or_procedure": "Unlisted CT Procedure - Low Dose Whole Body CT (CPT 76497)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ANY_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Evaluation of suspected, initial staging, or restaging of Multiple Myeloma",
                    "parameter": "multiple_myeloma_evaluation",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Evaluation of Monoclonal Gammopathy of Undetermined Significance (MGUS), Solitary Plasmacytoma, or Smoldering Multiple Myeloma",
                    "parameter": "plasma_cell_dyscrasia_evaluation",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Hematology/oncology records showing abnormal monoclonal protein, bone marrow biopsy, or CRAB criteria"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 76497"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Low dose whole-body CT indicated for plasma cell dyscrasias and multiple myeloma."
    },
    # CG 2062 - Upper Extremity CT
    {
        "rule_id": "RULE-ADV-CG2062-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 965,
            "printed_page": "Page 3 of 24"
        },
        "source_section": "INDICATIONS FOR UPPER EXTREMITY CT / Upper Extremity Pain (1,2) / Special Notes",
        "source_quote": "X-rays must precede CT evaluation, unless otherwise indicated",
        "clinical_service_or_procedure": "Upper Extremity CT (Shoulder, Elbow, Wrist, Hand)",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Upper extremity plain X-ray completed showing no definitive diagnostic etiology for joint/extremity pain",
                    "parameter": "prior_xray_negative_or_inconclusive",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Persistent pain unresponsive to at least 4 weeks of active conservative therapy, OR acute complex fracture/arthrogram planning",
                    "parameter": "conservative_therapy_or_bony_injury",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Plain radiograph report and clinical orthopedic exam notes detailing pain localization and conservative treatment"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 73200",
            "CPT 73201",
            "CPT 73202"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Upper extremity CT requires preceding plain X-ray and conservative therapy unless acute fracture/surgical planning."
    },
    # CG 2063 - Upper Extremity CTA
    {
        "rule_id": "RULE-ADV-CG2063-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 989,
            "printed_page": "Page 3 of 12"
        },
        "source_section": "INDICATIONS FOR UPPER EXTREMITY COMPUTED TOMOGRAPHY ANGIOGRAPHY (CTA) / Upper Extremity Peripheral Vascular Disease (1,2)",
        "source_quote": "Upper Extremity Peripheral Vascular Disease (1,2)",
        "clinical_service_or_procedure": "Upper Extremity CTA",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Known or suspected acute upper extremity vascular disease or ischemia with ischemic ulceration or acute sustained loss of perfusion",
                    "parameter": "upper_extremity_vascular_disease_or_ischemia",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Vascular surgery or physical examination documenting pulse deficits, ischemic ulcers, or abnormal arterial Doppler studies"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 73206"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Upper extremity CTA indicated for upper extremity peripheral vascular disease and ischemia."
    },
    # CG 2064 - Upper Extremity MRA
    {
        "rule_id": "RULE-ADV-CG2064-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 1001,
            "printed_page": "Page 3 of 13"
        },
        "source_section": "INDICATIONS FOR UPPER EXTREMITY MAGNETIC RESONANCE ANGIOGRAPHY (MRA) / Special Notes",
        "source_quote": "When a separate MRA and MRI exam is requested, documentation requires a medical reason",
        "clinical_service_or_procedure": "Upper Extremity MRA",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Evaluation of known or suspected upper extremity vascular disease when CTA is contraindicated or cannot be performed (e.g. iodinated contrast allergy or renal insufficiency)",
                    "parameter": "vascular_disease_with_cta_contraindication",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical notes detailing vascular compromise and medical reason why CTA cannot be performed"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 73225"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Upper extremity MRA indicated when CTA is contraindicated or additional soft tissue vascular clarification is needed."
    },
    # CG 2065 - Upper Extremity MRI
    {
        "rule_id": "RULE-ADV-CG2065-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 1014,
            "printed_page": "Page 3 of 23"
        },
        "source_section": "INDICATIONS FOR UPPER EXTREMITY MRI (SHOULDER, ELBOW, OR WRIST) / Upper Extremity Pain (1,2) / Special Notes",
        "source_quote": "Plain X-rays must precede MRI evaluation unless otherwise indicated",
        "clinical_service_or_procedure": "Upper Extremity MRI (Shoulder, Elbow, Wrist, Hand)",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Preceding plain radiograph performed and showing no clear explanation for joint or extremity pain",
                    "parameter": "prior_plain_xray_negative",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Persistent pain unresponsive to active conservative therapy (physical therapy, chiropractic, supervised HEP) of at least 4 weeks duration within last 6 months, OR positive orthopedic joint exam test",
                    "parameter": "active_conservative_therapy_or_positive_sign",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Plain radiograph report, orthopedic exam records, and 4 weeks of conservative therapy documentation"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 73221",
            "CPT 73222",
            "CPT 73223"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Upper extremity MRI requires plain X-ray and 4 weeks conservative therapy unless positive orthopedic exam test."
    },
    # CG 2066 - Urgent/Emergent Criteria
    {
        "rule_id": "RULE-ADV-CG2066-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 1036,
            "printed_page": "Page 2 of 7"
        },
        "source_section": "INDICATIONS FOR EMERGENT STUDIES / Emergent Studies",
        "source_quote": "INDICATIONS FOR EMERGENT STUDIES",
        "clinical_service_or_procedure": "Advanced Imaging (Emergent Retrospective Review)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Requested imaging was required to render immediate medical attention needed to prevent loss of life, limb, or risk of permanent disability (e.g. airway/breathing/circulation compromise, acute compartment syndrome, acute vascular thrombosis/embolus)",
                    "parameter": "emergent_life_or_limb_threat_present",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Emergency department or inpatient records documenting acute life/limb threatening clinical emergency at the time of imaging"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [],
        "human_review_required": True,
        "extraction_status": "NEEDS_HUMAN_REVIEW",
        "review_notes": "Emergent retrospective review requires physician clinical determination of life/limb threat."
    },
    {
        "rule_id": "RULE-ADV-CG2066-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 1036,
            "printed_page": "Page 2 of 7"
        },
        "source_section": "INDICATIONS FOR URGENT STUDIES / Urgent Studies",
        "source_quote": "INDICATIONS FOR URGENT STUDIES",
        "clinical_service_or_procedure": "Advanced Imaging (Urgent Retrospective Review)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Condition required prompt medical intervention to prevent progression to an emergent condition or could not be postponed for 24 hours without substantial risk of harm",
                    "parameter": "urgent_intervention_needed_within_24h",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Physician progress notes documenting urgent clinical progression risk justifying retrospective approval"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [],
        "human_review_required": True,
        "extraction_status": "NEEDS_HUMAN_REVIEW",
        "review_notes": "Urgent retrospective review requires physician clinical evaluation of 24-hour urgency."
    }
]

def main():
    schema_path = RULES_DIR / "schema.json"
    checkpoint_path = CHECKPOINTS_DIR / "batch_08_rules.json"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for i, r in enumerate(batch_08_rules, 1):
        jsonschema.validate(instance=r, schema=schema)
        print(f"Batch 8 Rule {i} ({r['rule_id']}): Schema VALID")

    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(batch_08_rules, f, indent=2)

    print(f"\nSuccessfully validated and saved {len(batch_08_rules)} rules to {checkpoint_path}")

if __name__ == "__main__":
    main()
