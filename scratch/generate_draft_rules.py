"""Generate and validate 16 draft rules for MedRule Phase 2A pilot."""
import json
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"

GOVERNING_PDF = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
GOVERNING_URL = "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf"

rules = [
    # 1. CG 2000 - General Documentation Requirement
    {
        "rule_id": "RULE-ADV-CG2000-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 8,
            "printed_page": "Page 3 of 29"
        },
        "source_section": "STATEMENT / General Information",
        "source_quote": "It is an expectation that all patients receive care/services from a licensed clinician. All appropriate supporting documentation, including recent pertinent office visit notes, laboratory data, and results of any special testing must be provided. If applicable: All prior relevant imaging results and the reason that alternative imaging cannot be performed must be included in the documentation submitted.",
        "clinical_service_or_procedure": "Advanced Diagnostic Imaging (CT, MRI, PET, Nuclear Medicine)",
        "rule_type": "documentation_requirement",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Care and services ordered or provided by a licensed clinician",
                    "parameter": "ordering_provider_license",
                    "comparator": "IS_PRESENT",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Submission of recent pertinent office visit clinical notes",
                    "parameter": "clinical_office_notes",
                    "comparator": "IS_PRESENT",
                    "value": True
                },
                {
                    "condition_id": "COND-003",
                    "description": "Submission of relevant laboratory data and special testing results",
                    "parameter": "laboratory_and_testing_data",
                    "comparator": "IS_PRESENT",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Recent pertinent office visit notes",
            "Laboratory data",
            "Prior relevant imaging reports",
            "Clinical rationale why alternative imaging cannot be performed"
        ],
        "decision_effect": "DOCUMENTATION_DEFICIENT",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "rulebook_collection/domains/advanced_imaging/supporting_pdfs/checklists/Evolent Generic Prior Authorization Checklist (non cardiac) 11112024.pdf"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Universal baseline clinical intake requirement applying across all Evolent imaging guidelines."
    },

    # 2. CG 2000 - IBD Workup Prerequisite
    {
        "rule_id": "RULE-ADV-CG2000-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 9,
            "printed_page": "Page 4 of 29"
        },
        "source_section": "Inflammatory Bowel Disease (3–5)",
        "source_quote": "For suspected inflammatory bowel disease after complete work up including physical exam, labs, and recent colonoscopy",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis (or CT Enterography)",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Physical examination documented in medical records",
                    "parameter": "physical_exam_completed",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Diagnostic laboratory workup completed",
                    "parameter": "lab_workup_completed",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-003",
                    "description": "Recent colonoscopy completed prior to advanced imaging request",
                    "parameter": "recent_colonoscopy_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Physical examination notes",
            "Laboratory results",
            "Recent colonoscopy report"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74176",
            "CPT 74177",
            "CPT 74178"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Prerequisite workup rule for suspected new onset IBD."
    },

    # 3. CG 2000 - MR Enterography Advisory / Age Redirection (FLAGGED FOR HUMAN REVIEW)
    {
        "rule_id": "RULE-ADV-CG2000-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 9,
            "printed_page": "Page 4 of 29"
        },
        "source_section": "Inflammatory Bowel Disease (3–5)",
        "source_quote": "For evaluation of Inflammatory Bowel Disease (IBD) such as Crohn's or Ulcerative Colitis (includes CT enterography, however, MRI should be considered for age < 35 to reduce radiation exposure)",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis / CT Enterography",
        "rule_type": "conditional_modality_selection",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Requested procedure is CT enterography or CT abdomen/pelvis for IBD",
                    "parameter": "requested_modality",
                    "comparator": "EQUALS",
                    "value": "CT"
                },
                {
                    "condition_id": "COND-002",
                    "description": "Patient age is strictly less than 35 years",
                    "parameter": "patient_age_years",
                    "comparator": "LESS_THAN",
                    "value": 35,
                    "unit": "years"
                }
            ]
        },
        "required_documentation": [
            "Documentation of contraindication to MRI (if CT requested for age < 35)"
        ],
        "decision_effect": "ALTERNATIVE_MODALITY_RECOMMENDED",
        "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
        "dependencies": [
            "CPT 74177",
            "CPT 74183"
        ],
        "human_review_required": True,
        "extraction_status": "NEEDS_HUMAN_REVIEW",
        "review_notes": "Advisory wording ('MRI should be considered'). Flagged for medical director determination regarding whether this constitutes a mandatory denial of CT or peer-to-peer advisory suggestion."
    },

    # 4. CG 2000 - Suspected Diverticulitis or Appendicitis
    {
        "rule_id": "RULE-ADV-CG2000-004",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 9,
            "printed_page": "Page 4 of 29"
        },
        "source_section": "Diverticulitis or Acute Appendicitis (8,9)",
        "source_quote": "Suspected diverticulitis or acute appendicitis for initial imaging with at least ONE of the following (10): ○ WBC Elevated ○ Fever ○ Anorexia ○ Nausea and vomiting",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected acute diverticulitis or acute appendicitis for initial diagnostic evaluation",
                    "parameter": "provisional_diagnosis",
                    "comparator": "CONTAINS",
                    "value": [
                        "Diverticulitis",
                        "Acute Appendicitis"
                    ]
                },
                {
                    "condition_id": "COND-002",
                    "description": "At least one objective inflammatory or systemic clinical sign present",
                    "parameter": "clinical_signs_group",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "SIGN-001",
                                "description": "Elevated white blood cell count (leukocytosis)",
                                "parameter": "wbc_count",
                                "comparator": "EQUALS",
                                "value": "ELEVATED"
                            },
                            {
                                "condition_id": "SIGN-002",
                                "description": "Documented fever",
                                "parameter": "fever_present",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "SIGN-003",
                                "description": "Documented anorexia",
                                "parameter": "anorexia_present",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "SIGN-004",
                                "description": "Documented nausea and vomiting",
                                "parameter": "nausea_and_vomiting_present",
                                "comparator": "EQUALS",
                                "value": True
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Clinical notes detailing acute abdominal pain",
            "Vital signs showing temperature/fever or CBC report showing elevated WBC"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74176",
            "CPT 74177"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Initial imaging indication with disjunctive clinical symptom checklist."
    },

    # 5. CG 2000 - Pediatric Suspected Appendicitis Ultrasound Prerequisite
    {
        "rule_id": "RULE-ADV-CG2000-005",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 9,
            "printed_page": "Page 4 of 29"
        },
        "source_section": "Diverticulitis or Acute Appendicitis (8,9)",
        "source_quote": "Suspected appendicitis in a child (< age 18) (12) when ultrasound is inconclusive or cannot be completed (due to body habitus or inability to cooperate) OR when peritoneal signs are present (guarding, rebound) or other red flags",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis (Pediatric)",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient age is strictly less than 18 years",
                    "parameter": "patient_age_years",
                    "comparator": "LESS_THAN",
                    "value": 18,
                    "unit": "years"
                },
                {
                    "condition_id": "COND-002",
                    "description": "Provisional diagnosis is suspected acute appendicitis",
                    "parameter": "provisional_diagnosis",
                    "comparator": "EQUALS",
                    "value": "Appendicitis"
                },
                {
                    "condition_id": "COND-003",
                    "description": "Ultrasound inconclusive/incomplete OR peritoneal signs present",
                    "parameter": "ultrasound_or_peritoneal_signs",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "US-001",
                                "description": "Prior ultrasound inconclusive or incomplete",
                                "parameter": "prior_ultrasound_status",
                                "comparator": "CONTAINS",
                                "value": ["INCONCLUSIVE", "INCOMPLETE"]
                            },
                            {
                                "condition_id": "US-002",
                                "description": "Peritoneal signs documented (guarding, rebound) or other red flags",
                                "parameter": "peritoneal_signs_present",
                                "comparator": "EQUALS",
                                "value": True
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Ultrasound report demonstrating inconclusive results or documentation of inability to complete ultrasound",
            "Physical examination notes documenting peritoneal signs (guarding, rebound) if ultrasound was bypassed"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74176",
            "CPT 74177"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Pediatric appendicitis radiation sparing protocol mandating ultrasound prior to CT unless peritoneal signs are present."
    },

    # 6. CG 2000 - Acute Pancreatitis 72-Hour Threshold
    {
        "rule_id": "RULE-ADV-CG2000-006",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 10,
            "printed_page": "Page 5 of 29"
        },
        "source_section": "Pancreatitis (14)",
        "source_quote": "Initial imaging for suspected acute pancreatitis due to epigastric pain with elevated amylase and/or lipase: ○ Mild presentation when symptom improvement is not seen after 72 hours of treatment and either: ■ Ultrasound has been performed and did not show an abnormality such as gallstones, dilated bile duct ■ Ultrasound suggests complications (such as fluid collection)",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis",
        "rule_type": "temporal_threshold",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected acute pancreatitis with epigastric pain and elevated amylase and/or lipase",
                    "parameter": "pancreatitis_diagnostic_markers",
                    "comparator": "EQUALS",
                    "value": "ELEVATED"
                },
                {
                    "condition_id": "COND-002",
                    "description": "Mild presentation without symptom improvement after at least 72 hours of treatment",
                    "parameter": "conservative_treatment_duration_hours",
                    "comparator": "GREATER_THAN_OR_EQUAL",
                    "value": 72,
                    "unit": "hours"
                },
                {
                    "condition_id": "COND-003",
                    "description": "Prior ultrasound completed showing no gallstones/ductal dilation OR suggesting complications",
                    "parameter": "ultrasound_findings",
                    "comparator": "CONTAINS",
                    "value": [
                        "NO_GALLSTONES_OR_DILATED_DUCT",
                        "SUGGESTS_COMPLICATIONS"
                    ]
                }
            ]
        },
        "required_documentation": [
            "Serum amylase and lipase laboratory reports",
            "Clinical notes demonstrating persistent symptoms at or beyond 72 hours",
            "Abdominal ultrasound report"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74177",
            "CPT 74178"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Temporal constraint requiring 72 hours of conservative care in mild pancreatitis before early CT is medically indicated."
    },

    # 7. CG 2000 - Severe Acute Pancreatitis (Immediate Imaging)
    {
        "rule_id": "RULE-ADV-CG2000-007",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 10,
            "printed_page": "Page 5 of 29"
        },
        "source_section": "Pancreatitis (14)",
        "source_quote": "Severe presentation (such as fever, elevated WBC) ○ Decline in clinical status and/or suspected complication",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ANY_OF",
            "criteria": [
                {
                    "condition_id": "SEV-001",
                    "description": "Severe presentation with fever and elevated WBC count",
                    "parameter": "severe_pancreatitis_signs",
                    "comparator": "IS_PRESENT",
                    "value": True
                },
                {
                    "condition_id": "SEV-002",
                    "description": "Decline in clinical status or suspected organ complication",
                    "parameter": "clinical_status_decline",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Vital signs showing fever",
            "CBC showing leukocytosis",
            "Clinical notes documenting rapid clinical decline or suspected necrosis/phlegmon"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74177"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Severe acute pancreatitis indication bypassing the 72-hour observation window."
    },

    # 8. CG 2000 - Hematuria Initial Exclusion and Gross / >25 RBC
    {
        "rule_id": "RULE-ADV-CG2000-008",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 11,
            "printed_page": "Page 6 of 29"
        },
        "source_section": "Evaluation of Hematuria (20)",
        "source_quote": "Kidney Stone is NOT suspected AND ● Urinalysis is negative for infection or hematuria persists on urine microscopy following treatment of urinary tract infection AND ● At least one of the following: ○ Gross hematuria ○ > 25 RBC/hpf on urine microscopy",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis (CT Urography)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Kidney stone is NOT suspected",
                    "parameter": "suspected_nephrolithiasis",
                    "comparator": "EQUALS",
                    "value": False
                },
                {
                    "condition_id": "COND-002",
                    "description": "Urinalysis negative for infection OR hematuria persists following UTI treatment",
                    "parameter": "urinary_infection_ruled_out",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-003",
                    "description": "Gross hematuria OR > 25 RBC/hpf on urine microscopy",
                    "parameter": "high_grade_hematuria",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "HEM-001",
                                "description": "Documented gross hematuria",
                                "parameter": "gross_hematuria_present",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "HEM-002",
                                "description": "Greater than 25 RBC per high power field on urine microscopy",
                                "parameter": "urine_rbc_count",
                                "comparator": "GREATER_THAN",
                                "value": 25,
                                "unit": "RBC/hpf"
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Urinalysis microscopy report showing RBC count or gross hematuria",
            "Urine culture or documentation showing UTI ruled out or treated"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74177",
            "CPT 74178"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "High-risk hematuria branch based on American Urological Association (AUA) guidelines."
    },

    # 9. CG 2000 - Microscopic Hematuria (3-25 RBC/hpf) with Risk Factors
    {
        "rule_id": "RULE-ADV-CG2000-009",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 11,
            "printed_page": "Page 6 of 29"
        },
        "source_section": "Evaluation of Hematuria (20)",
        "source_quote": "3-25 RBC/hpf on urine microscopy AND ONE or more of the following: ■ >30 pack year smoking history ■ Male ≥ age 60 ■ Abnormal renal ultrasound ■ Negative renal ultrasound and repeat sample shows persistence of ≥ 3 RBC/hpf",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis (CT Urography)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "3 to 25 RBC/hpf documented on urine microscopy",
                    "parameter": "urine_rbc_count",
                    "comparator": "BETWEEN",
                    "value": [3, 25],
                    "unit": "RBC/hpf"
                },
                {
                    "condition_id": "COND-002",
                    "description": "At least one established urologic malignancy risk factor present",
                    "parameter": "urologic_risk_factors",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "RISK-001",
                                "description": "Greater than 30 pack-year smoking history",
                                "parameter": "smoking_history_pack_years",
                                "comparator": "GREATER_THAN",
                                "value": 30,
                                "unit": "pack_years"
                            },
                            {
                                "condition_id": "RISK-002",
                                "description": "Male patient aged 60 or older",
                                "parameter": "male_patient_age",
                                "comparator": "GREATER_THAN_OR_EQUAL",
                                "value": 60,
                                "unit": "years"
                            },
                            {
                                "condition_id": "RISK-003",
                                "description": "Abnormal renal ultrasound finding",
                                "parameter": "renal_ultrasound_abnormal",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "RISK-004",
                                "description": "Negative renal ultrasound with persistence of >= 3 RBC/hpf on repeat sample",
                                "parameter": "persistent_microscopic_hematuria",
                                "comparator": "EQUALS",
                                "value": True
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Urine microscopy lab report showing 3-25 RBC/hpf",
            "Clinical notes documenting smoking history, renal ultrasound report, or repeat UA"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74177",
            "CPT 74178"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Intermediate risk microscopic hematuria indication."
    },

    # 10. CG 2000 - AAA Surveillance Interval Threshold (5.0 - 5.4 cm)
    {
        "rule_id": "RULE-ADV-CG2000-010",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 13,
            "printed_page": "Page 8 of 29"
        },
        "source_section": "Abdominal Aortic Aneurysm (AAA)",
        "source_quote": "Aneurysm size 5.0-5.4 cm, every 6 months",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis / CT Angiography Abdomen",
        "rule_type": "temporal_threshold",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Known abdominal aortic aneurysm with maximum diameter between 5.0 and 5.4 cm",
                    "parameter": "aaa_diameter_cm",
                    "comparator": "BETWEEN",
                    "value": [5.0, 5.4],
                    "unit": "cm"
                },
                {
                    "condition_id": "COND-002",
                    "description": "At least 6 months elapsed since previous aortic imaging evaluation",
                    "parameter": "months_since_last_aortic_imaging",
                    "comparator": "GREATER_THAN_OR_EQUAL",
                    "value": 6,
                    "unit": "months"
                }
            ]
        },
        "required_documentation": [
            "Prior imaging report demonstrating AAA size 5.0 - 5.4 cm",
            "Date of last prior aortic imaging study"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74175",
            "CPT 74176"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Surveillance frequency rule for pre-surgical threshold aneurysms."
    },

    # 11. CG 2000 - Symptomatic AAA Urgent Indication
    {
        "rule_id": "RULE-ADV-CG2000-011",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 13,
            "printed_page": "Page 8 of 29"
        },
        "source_section": "Abdominal Aortic Aneurysm (AAA)",
        "source_quote": "Known or suspected symptomatic AAA (30,31) ○ Symptoms may include: ■ Abrupt onset of severe sharp or stabbing pain in the chest, back or abdomen (could indicate possible aneurysm rupture) ■ Acute abdominal or back pain with a pulsatile or epigastric mass ■ Acute abdominal or back pain and at high risk for aortic aneurysm and/or aortic syndrome (risk factors include hypertension, atherosclerosis, prior cardiac or aortic surgery, underlying aneurysm, connective tissue disorder (Such as Marfan syndrome, vascular form of Ehlers-Danlos syndrome, Loeys-Dietz syndrome), and bicuspid aortic valve) (32)",
        "clinical_service_or_procedure": "CT Angiography / CT Abdomen and Pelvis",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Known or clinically suspected symptomatic abdominal aortic aneurysm",
                    "parameter": "symptomatic_aaa_suspected",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Documentation of acute rupture symptoms, pulsatile mass, or high-risk features",
                    "parameter": "acute_aortic_symptoms",
                    "comparator": "IS_PRESENT",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Emergency department or urgent clinical evaluation note",
            "Physical examination documenting pain characteristics, pulsatile mass, or hemodynamic instability"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74175",
            "CPT 74177"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Urgent indication for suspected rupture or acute expansion."
    },

    # 12. CG 2000 - Asymptomatic Cancer Surveillance Explicit Exclusion
    {
        "rule_id": "RULE-ADV-CG2000-012",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 19,
            "printed_page": "Page 14 of 29"
        },
        "source_section": "Surveillance / General Cancer Follow-up",
        "source_quote": "When a cancer is not listed above, Abdomen and Pelvis CT is not routinely a part of surveillance for that cancer in an asymptomatic patient. There would need to be a sign or symptom of recurrence to consider Abdomen and Pelvis CT.",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis",
        "rule_type": "exclusion_criterion",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Primary cancer diagnosis is not specifically listed in guideline surveillance table",
                    "parameter": "cancer_in_surveillance_table",
                    "comparator": "EQUALS",
                    "value": False
                },
                {
                    "condition_id": "COND-002",
                    "description": "Patient is asymptomatic without signs or symptoms of recurrence",
                    "parameter": "patient_is_asymptomatic",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Oncology progress notes demonstrating active signs or symptoms of disease recurrence if CT is requested"
        ],
        "exclusion_conditions": [
            "Routine routine surveillance CT in asymptomatic patients whose cancer type is not enumerated in guideline table"
        ],
        "decision_effect": "NOT_INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74176",
            "CPT 74177",
            "CPT 74178"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Explicit policy exclusion barring routine unlisted cancer surveillance in asymptomatic individuals."
    },

    # 13. CG 2012 - Brain MRI Acute Sudden Severe Headache / Thunderclap Indication
    {
        "rule_id": "RULE-ADV-CG2012-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 224,
            "printed_page": "Page 5 of 50"
        },
        "source_section": "INDICATIONS / Headache (1,2) / Evaluation of Headache",
        "source_quote": "Acute, sudden onset headache (< 4 weeks), with any ONE of the following: ○ A personal or family history (brother, sister, parent, or child) of brain aneurysm or AVM (arteriovenous malformation) ○ < 48 hours of “worst headache in my life” or “thunderclap” headache (Sudden onset new headache reaching maximum intensity within 2-3 minutes, lasting more than 5 minutes) ○ Prior history of stroke or intracranial bleed ○ Known coagulopathy or on anticoagulation",
        "clinical_service_or_procedure": "Brain MRI (With or Without Contrast)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Acute sudden onset headache with duration less than 4 weeks",
                    "parameter": "headache_duration_weeks",
                    "comparator": "LESS_THAN",
                    "value": 4,
                    "unit": "weeks"
                },
                {
                    "condition_id": "COND-002",
                    "description": "At least one high-risk vascular or intracranial red flag feature present",
                    "parameter": "acute_headache_risk_factor",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "RED-001",
                                "description": "Personal or first-degree family history of brain aneurysm or AVM",
                                "parameter": "aneurysm_or_avm_history",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "RED-002",
                                "description": "Thunderclap onset or worst headache of life within 48 hours",
                                "parameter": "thunderclap_onset_48h",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "RED-003",
                                "description": "Prior history of stroke or intracranial bleed",
                                "parameter": "prior_stroke_or_intracranial_bleed",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "RED-004",
                                "description": "Known coagulopathy or currently on active anticoagulation therapy",
                                "parameter": "active_anticoagulation_or_coagulopathy",
                                "comparator": "EQUALS",
                                "value": True
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Neurology or ED consultation notes detailing headache onset and duration",
            "Medication list or family history notes documenting specific high risk feature"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70551",
            "CPT 70553"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Emergency and acute high-risk headache indication for Brain MRI."
    },

    # 14. CG 2012 - Brain MRI Pediatric Persistent Headache Red Flags
    {
        "rule_id": "RULE-ADV-CG2012-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 225,
            "printed_page": "Page 6 of 50"
        },
        "source_section": "Additional Indications in the Pediatric Population (<18) When None of the Above Apply",
        "source_quote": "Persistent headache and any ONE of the following (8–10): ○ Immune deficiency ○ History of neoplasm ○ History of congenital heart disease ○ See Imaging in Known Genetic Conditions for additional indications ○ Coagulopathy ○ Occipital location ○ Age < 6 years",
        "clinical_service_or_procedure": "Brain MRI (With or Without Contrast)",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient age strictly less than 18 years",
                    "parameter": "patient_age_years",
                    "comparator": "LESS_THAN",
                    "value": 18,
                    "unit": "years"
                },
                {
                    "condition_id": "COND-002",
                    "description": "Persistent headache documented",
                    "parameter": "headache_persistence",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-003",
                    "description": "At least one pediatric red flag condition present",
                    "parameter": "pediatric_headache_red_flag",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "PED-001",
                                "description": "Documented immune deficiency",
                                "parameter": "immune_deficiency",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "PED-002",
                                "description": "Personal history of neoplasm",
                                "parameter": "history_of_neoplasm",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "PED-003",
                                "description": "History of congenital heart disease",
                                "parameter": "congenital_heart_disease",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "PED-004",
                                "description": "Coagulopathy present",
                                "parameter": "coagulopathy_present",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "PED-005",
                                "description": "Headache localized to occipital region",
                                "parameter": "headache_location",
                                "comparator": "EQUALS",
                                "value": "OCCIPITAL"
                            },
                            {
                                "condition_id": "PED-006",
                                "description": "Patient age younger than 6 years",
                                "parameter": "patient_age_years",
                                "comparator": "LESS_THAN",
                                "value": 6,
                                "unit": "years"
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Pediatrician or pediatric neurologist clinical consultation note",
            "Medical history validating presence of red flag feature"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 70551",
            "CPT 70553"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Pediatric red flag headache criteria."
    },

    # 15. CG 2017 - Cervical Spine MRI Conservative Treatment Failure
    {
        "rule_id": "RULE-ADV-CG2017-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 330,
            "printed_page": "Page 4 of 26"
        },
        "source_section": "Evaluation of Neck Pain (5,6)",
        "source_quote": "Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months: NOTE - Failure of conservative treatment is defined as one of the following: ○ Lack of meaningful improvement after a full course of treatment; OR ○ Progression or worsening of symptoms during treatment; OR ○ Documentation of a medical reason the member is unable to participate in treatment",
        "clinical_service_or_procedure": "Cervical Spine MRI",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Evaluation of non-emergent neck pain without acute progressive cord compression",
                    "parameter": "clinical_indication",
                    "comparator": "EQUALS",
                    "value": "NECK_PAIN"
                },
                {
                    "condition_id": "COND-002",
                    "description": "Completion of at least six (6) consecutive weeks of conservative therapy within the prior six (6) months",
                    "parameter": "conservative_care_duration_weeks",
                    "comparator": "GREATER_THAN_OR_EQUAL",
                    "value": 6,
                    "unit": "weeks"
                },
                {
                    "condition_id": "COND-003",
                    "description": "Conservative therapy completed within the preceding 6 months",
                    "parameter": "conservative_care_recency_months",
                    "comparator": "LESS_THAN_OR_EQUAL",
                    "value": 6,
                    "unit": "months"
                },
                {
                    "condition_id": "COND-004",
                    "description": "Documented failure (lack of improvement, progression, or medically documented contraindication)",
                    "parameter": "conservative_therapy_outcome",
                    "comparator": "DOCUMENTED_FAILURE",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Physical therapy notes with attendance logs showing 6 weeks of active therapy",
            "Physician clinical follow-up notes documenting persistence of symptoms post-therapy"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72141",
            "CPT 72142"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Standard conservative care prerequisite with 6-week trial within last 6 months."
    },

    # 16. CG 2017 - Suspected Myelopathy Bypasses Conservative Care
    {
        "rule_id": "RULE-ADV-CG2017-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOVERNING_PDF,
        "source_url": GOVERNING_URL,
        "source_page": {
            "physical_page": 331,
            "printed_page": "Page 5 of 26"
        },
        "source_section": "Evaluation of Suspected Myelopathy (11,12)",
        "source_quote": "Evaluation of Suspected Myelopathy (11,12) ● Progressive symptoms including hand clumsiness, worsening handwriting, difficulty with grasping and holding objects, diffuse numbness in the hands, pins and needles sensation, increasing difficulty with balance and ambulation ● Any of the neurological deficits as noted above NOTE: Does NOT require conservative care",
        "clinical_service_or_procedure": "Cervical Spine MRI",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical suspicion of cervical myelopathy with progressive upper extremity dysfunction or balance difficulty",
                    "parameter": "suspected_cervical_myelopathy",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Objective neurological exam findings (hyperreflexia, clonus, gait instability, Babinski)",
                    "parameter": "myelopathic_neurologic_deficits",
                    "comparator": "IS_PRESENT",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Neurological or orthopedic physical examination documenting myelopathic signs (hyperreflexia, Hoffman, Babinski, gait disturbance)"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 72141",
            "CPT 72142"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Explicit policy exception stating cervical myelopathy does NOT require conservative treatment prior to advanced MRI."
    }
]

def main():
    schema_path = RULES_DIR / "schema.json"
    output_path = RULES_DIR / "draft_rules.json"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for i, r in enumerate(rules, 1):
        jsonschema.validate(instance=r, schema=schema)
        print(f"Rule {i} ({r['rule_id']}): Schema VALID")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)

    print(f"\nSuccessfully validated and saved {len(rules)} draft rules to {output_path}")

if __name__ == "__main__":
    main()
