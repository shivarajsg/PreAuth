"""Remediate the 15 confirmed omission criteria by adding structured rules."""
import json
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
GOV_PDF = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
GOV_URL = "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf"

remediated_rules = [
    # 1. CG-2008 Brain CT - Head Trauma
    {
        "rule_id": "RULE-ADV-CG2008-003",
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
        "source_section": "INDICATIONS / Head Trauma / Evaluation of Known or Suspected Trauma (14,15)",
        "source_quote": "Known or suspected trauma or injury to the head with documentation of one or more of",
        "clinical_service_or_procedure": "Brain CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Known or suspected acute head trauma with acute, new, or fluctuating focal neurologic findings, motor changes, or mental status changes",
                    "parameter": "acute_head_trauma_with_neurologic_deficit",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Emergency department notes or trauma physical examination documenting mechanism of head injury and acute neurological deficits"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70450",
            "CPT 70460",
            "CPT 70470"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Brain CT is the primary modality for acute head trauma evaluation."
    },
    # 2. CG-2008 Brain CT - Thunderclap Headache
    {
        "rule_id": "RULE-ADV-CG2008-004",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 149,
            "printed_page": "Page 4 of 26"
        },
        "source_section": "INDICATIONS / Evaluation of Headache (1,2) / Acute, sudden onset headache",
        "source_quote": "Acute, sudden onset headache (< 4 weeks), with any ONE of the following",
        "clinical_service_or_procedure": "Brain CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Acute sudden onset severe headache presenting within 48 hours of onset ('worst headache of life' or 'thunderclap' headache) concerning for acute subarachnoid hemorrhage",
                    "parameter": "thunderclap_or_worst_headache_of_life",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical notes documenting acute peak headache onset within seconds to minutes and physical examination"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70450"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Non-contrast Brain CT is initial test of choice for acute sudden severe headache / suspected SAH."
    },
    # 3. CG-2009 Brain CTA - Acute Stroke / LVO
    {
        "rule_id": "RULE-ADV-CG2009-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 176,
            "printed_page": "Page 5 of 20"
        },
        "source_section": "INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Evaluation of Known Intracranial Vascular Disease (1,2)",
        "source_quote": "Evaluation of Known Intracranial Vascular Disease (1,2)",
        "clinical_service_or_procedure": "Brain CTA",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Acute ischemic stroke presentation being evaluated for large vessel occlusion (LVO) or mechanical thrombectomy eligibility",
                    "parameter": "acute_stroke_lvo_evaluation",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Emergency neurological exam documenting NIHSS score, last known well time, and acute focal deficits"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70496"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Brain CTA indicated for acute stroke large vessel occlusion evaluation."
    },
    # 4. CG-2012 Brain MRI - Multiple Sclerosis
    {
        "rule_id": "RULE-ADV-CG2012-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 232,
            "printed_page": "Page 13 of 50"
        },
        "source_section": "INDICATIONS / Multiple Sclerosis / Evaluation of Suspected Multiple Sclerosis (61,62)",
        "source_quote": "Evaluation of Suspected Multiple Sclerosis (61,62)",
        "clinical_service_or_procedure": "Brain MRI (With and Without Contrast)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical presentation suspicious for CNS demyelinating disease (e.g. optic neuritis, acute transverse myelitis, brainstem/cerebellar syndrome) or surveillance of established Multiple Sclerosis",
                    "parameter": "suspected_or_established_multiple_sclerosis",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurology clinic notes documenting demyelinating signs, prior CSF oligoclonal bands, or DMT therapy monitoring"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70553"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Brain MRI with/without contrast indicated for multiple sclerosis diagnosis and monitoring."
    },
    # 5. CG-2012 Brain MRI - Seizures
    {
        "rule_id": "RULE-ADV-CG2012-004",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 232,
            "printed_page": "Page 13 of 50"
        },
        "source_section": "INDICATIONS / Seizure Disorders / Evaluation of Known or Suspected Seizure Disorder (54–60)",
        "source_quote": "New onset of an unprovoked seizure",
        "clinical_service_or_procedure": "Brain MRI (Epilepsy Protocol)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ANY_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient has experienced a new-onset unprovoked seizure",
                    "parameter": "new_onset_unprovoked_seizure",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Patient has medically refractory epilepsy or newly identified change in seizure semiology",
                    "parameter": "refractory_epilepsy_or_pattern_change",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurology consultation notes and EEG findings documenting seizure semiology"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70551",
            "CPT 70553"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Brain MRI is the primary modality for unprovoked seizures and epilepsy."
    },
    # 6. CG-2018 Chest CT - Hemoptysis
    {
        "rule_id": "RULE-ADV-CG2018-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 361,
            "printed_page": "Page 9 of 30"
        },
        "source_section": "INDICATIONS FOR CHEST CT / Signs and Symptoms / Hemoptysis",
        "source_quote": "Hemoptysis after x-ray completed (25)",
        "clinical_service_or_procedure": "Chest CT",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient presents with unexplained hemoptysis",
                    "parameter": "unexplained_hemoptysis_present",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Preceding plain chest radiograph has been completed",
                    "parameter": "prior_chest_xray_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Chest radiograph report and clinical notes detailing duration and severity of hemoptysis"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 71250",
            "CPT 71260"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Chest CT indicated for hemoptysis after chest X-ray completed."
    },
    # 7. CG-2020 Chest CTA - Thoracic Aortic Dissection
    {
        "rule_id": "RULE-ADV-CG2020-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 397,
            "printed_page": "Page 1 of 19"
        },
        "source_section": "INDICATIONS FOR CHEST COMPUTED TOMOGRAPHY ANGIOGRAPHY (CTA) / THORACIC AORTIC DISEASE",
        "source_quote": "THORACIC AORTIC DISEASE",
        "clinical_service_or_procedure": "Chest CTA",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected acute thoracic aortic syndrome (aortic dissection, intramural hematoma, penetrating atherosclerotic ulcer) or evaluation of thoracic aortic aneurysm",
                    "parameter": "acute_aortic_syndrome_or_aneurysm",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical notes detailing acute chest/back tearing pain, widened mediastinum on X-ray, or known aneurysm surveillance"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 71275"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Chest CTA is the reference standard for acute thoracic aortic syndrome."
    },
    # 8. CG-2032 Lower Extremity CT - Fracture
    {
        "rule_id": "RULE-ADV-CG2032-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 501,
            "printed_page": "Page 1 of 23"
        },
        "source_section": "INDICATIONS FOR LOWER EXTREMITY CT / Suspected Bone Fracture",
        "source_quote": "Suspected Bone Fracture",
        "clinical_service_or_procedure": "Lower Extremity CT",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Evaluation of complex, intra-articular, or comminuted lower extremity fracture (e.g. tibial plateau, pilon, calcaneus) or nonunion where plain radiographs are insufficient for pre-operative planning",
                    "parameter": "complex_lower_extremity_fracture_preop",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Plain radiograph report demonstrating intra-articular fracture and orthopedic surgical consultation notes"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 73700",
            "CPT 73701",
            "CPT 73702"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Lower extremity CT indicated for complex fracture characterization and surgical reconstruction planning."
    },
    # 9. CG-2035 Lower Extremity MRI - Knee Positive Signs
    {
        "rule_id": "RULE-ADV-CG2035-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 553,
            "printed_page": "Page 4 of 22"
        },
        "source_section": "INDICATIONS FOR LOWER EXTREMITY MRI / Joint Specific Orthopedic Signs",
        "source_quote": "Joint specific advanced imaging is indicated for any positive orthopedic sign listed below:",
        "clinical_service_or_procedure": "Lower Extremity MRI (Knee)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Physical examination demonstrates positive joint-specific sign for meniscal or ligamentous tear (e.g. McMurray test, joint line tenderness, Lachman test, anterior/posterior drawer, pivot shift)",
                    "parameter": "positive_knee_orthopedic_sign",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Prior plain radiograph completed showing no clear explanation for mechanical symptoms or acute fracture",
                    "parameter": "prior_xray_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Orthopedic physical examination documenting specific positive knee exam signs and plain radiograph report"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 73721",
            "CPT 73722",
            "CPT 73723"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "With positive orthopedic knee exam signs, active conservative therapy is waived."
    },
    # 10. CG-2035 Lower Extremity MRI - AVN Hip
    {
        "rule_id": "RULE-ADV-CG2035-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 550,
            "printed_page": "Page 1 of 22"
        },
        "source_section": "INDICATIONS FOR LOWER EXTREMITY MRI / OSTEONECROSIS",
        "source_quote": "OSTEONECROSIS",
        "clinical_service_or_procedure": "Lower Extremity MRI (Hip)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical suspicion of osteonecrosis / avascular necrosis (AVN) of the femoral head with risk factors (e.g. chronic steroid therapy, sickle cell disease, alcoholism) and normal or inconclusive plain radiographs",
                    "parameter": "suspected_femoral_head_osteonecrosis",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical notes detailing hip pain, AVN risk factors, and negative/indeterminate plain radiographs"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 73721"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "MRI is the most sensitive diagnostic modality for early avascular necrosis of the hip."
    },
    # 11. CG-2037 Lumbar Spine MRI - Infection / Malignancy
    {
        "rule_id": "RULE-ADV-CG2037-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 592,
            "printed_page": "Page 1 of 22"
        },
        "source_section": "INDICATIONS FOR LUMBAR SPINE MRI / EVALUATION OF KNOWN OR SUSPECTED INFECTION",
        "source_quote": "EVALUATION OF KNOWN OR SUSPECTED INFECTION",
        "clinical_service_or_procedure": "Lumbar Spine MRI (With and Without Contrast)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected spinal infection (discitis, osteomyelitis, epidural abscess) with fever, elevated inflammatory markers (ESR/CRP), or recent bacteremia, OR red flags for spinal malignancy/metastasis with known cancer history",
                    "parameter": "suspected_spinal_infection_or_malignancy",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical documentation of fever, laboratory inflammatory markers, or oncology records documenting primary malignancy"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72158"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Contrast-enhanced lumbar MRI indicated immediately for spinal infection or neoplastic cord threat (conservative therapy waived)."
    },
    # 12. CG-2046 Whole Body PET/CT - Lymphoma
    {
        "rule_id": "RULE-ADV-CG2046-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 737,
            "printed_page": "Page 1 of 71"
        },
        "source_section": "INDICATIONS / Lymphoma / Primary CNS Lymphoma and Systemic Lymphoma",
        "source_quote": "Primary CNS Lymphoma",
        "clinical_service_or_procedure": "PET/CT (Whole Body)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Biopsy-proven Hodgkin Lymphoma or FDG-avid Non-Hodgkin Lymphoma undergoing initial staging, mid-treatment response evaluation, or end-of-treatment remission assessment",
                    "parameter": "biopsy_proven_lymphoma_staging_or_response",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Pathology report confirming lymphoma subtype and oncology treatment plan"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 78815",
            "CPT 78816"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Whole-body PET/CT is reference standard for staging and Lugano response assessment in lymphoma."
    },
    # 13. CG-2046 Whole Body PET/CT - Lung Cancer
    {
        "rule_id": "RULE-ADV-CG2046-004",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 738,
            "printed_page": "Page 2 of 71"
        },
        "source_section": "INDICATIONS / Lung Cancer / Non-Small Cell Lung Cancer",
        "source_quote": "Non-Small Cell Lung Cancer",
        "clinical_service_or_procedure": "PET/CT (Whole Body)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Proven or suspected Non-Small Cell Lung Cancer (NSCLC) with solid nodule >= 8 mm or indeterminate solitary pulmonary nodule being evaluated for initial staging or distant metastasis",
                    "parameter": "nsclc_or_spn_metabolic_staging",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Diagnostic Chest CT report documenting nodule/mass characteristics and oncology consult notes"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 78815",
            "CPT 78816"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Whole-body PET/CT indicated for initial staging and nodal assessment of NSCLC."
    },
    # 14. CG-2047 Sinus CT - Chronic Rhinosinusitis
    {
        "rule_id": "RULE-ADV-CG2047-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 811,
            "printed_page": "Page 4 of 18"
        },
        "source_section": "INDICATIONS / Rhinosinusitis / Chronic Rhinosinusitis",
        "source_quote": "Chronic rhinosinusitis (> 12 weeks duration) with ALL of the following",
        "clinical_service_or_procedure": "Sinus and Maxillofacial CT",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Chronic rhinosinusitis persisting for greater than 12 weeks duration",
                    "parameter": "rhinosinusitis_duration_weeks",
                    "comparator": "GREATER_THAN",
                    "value": 12
                },
                {
                    "condition_id": "COND-002",
                    "description": "Failure of at least 4 weeks of maximal medical therapy including oral antibiotics and intranasal corticosteroids",
                    "parameter": "maximal_medical_therapy_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "ENT clinic notes documenting symptoms duration, failed medical therapy medications and dates, and nasal endoscopy"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70486"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Sinus CT indicated for chronic rhinosinusitis after failed 4 weeks maximal medical therapy."
    },
    # 15. CG-2065 Upper Extremity MRI - Shoulder Rotator Cuff
    {
        "rule_id": "RULE-ADV-CG2065-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 1015,
            "printed_page": "Page 4 of 23"
        },
        "source_section": "INDICATIONS FOR UPPER EXTREMITY MRI / Joint Specific Orthopedic Signs / Shoulder",
        "source_quote": "Bear hug test",
        "clinical_service_or_procedure": "Upper Extremity MRI (Shoulder)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Physical examination demonstrates positive joint-specific sign for rotator cuff tear (Bear hug test, Belly press test, Drop arm test, Empty can test, or External rotation lag sign)",
                    "parameter": "positive_rotator_cuff_orthopedic_sign",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Preceding plain radiograph completed showing no clear explanation for pain (active conservative therapy waived)",
                    "parameter": "prior_xray_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Orthopedic physical exam documentation of positive rotator cuff exam maneuvers and plain radiograph report"
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
        "review_notes": "Positive orthopedic shoulder signs waive the 4-week active conservative therapy prerequisite."
    }
]

def main():
    schema_path = RULES_DIR / "schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for i, r in enumerate(remediated_rules, 1):
        jsonschema.validate(instance=r, schema=schema)
        print(f"Remediated Rule {i} ({r['rule_id']}): Schema VALID")

    with open(RULES_DIR / "checkpoints" / "batch_remediated_omissions.json", "w", encoding="utf-8") as f:
        json.dump(remediated_rules, f, indent=2)

    print(f"\nSuccessfully validated and saved {len(remediated_rules)} remediated rules.")

if __name__ == "__main__":
    main()
