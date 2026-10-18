"""Batch 01 Extraction: CG 2000 through CG 2006 (Abdomen & Pelvis modalities)."""
import json
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"
GOV_PDF = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
GOV_URL = "https://www1.radmd.com/sites/default/files/2025-12/2026%20Evolent%20Clinical%20Guidelines%20-%20Advanced%20Imaging%20v2.pdf"

# Load the existing 12 CG 2000 rules from draft_rules.json
with open(RULES_DIR / "draft_rules.json", "r", encoding="utf-8") as f:
    existing_rules = json.load(f)

cg2000_rules = [r for r in existing_rules if r["rule_id"].startswith("RULE-ADV-CG2000-")]

batch_01_new_rules = [
    # CG 2000 - Additional criteria
    {
        "rule_id": "RULE-ADV-CG2000-013",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 19,
            "printed_page": "Page 14 of 29"
        },
        "source_section": "PREOPERATIVE OR POSTOPERATIVE ASSESSMENT / Postoperative Evaluation",
        "source_quote": "Known or suspected complications ● A clinical reason is provided how imaging may change management NOTE: This section applies only within the first few months following surgery",
        "clinical_service_or_procedure": "CT Abdomen and Pelvis",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Postoperative evaluation of known or suspected surgical complications",
                    "parameter": "postoperative_complications_suspected",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Surgery occurred within the first few months prior to imaging request",
                    "parameter": "months_since_surgery",
                    "comparator": "LESS_THAN_OR_EQUAL",
                    "value": 3,
                    "unit": "months"
                },
                {
                    "condition_id": "COND-003",
                    "description": "Clinical documentation demonstrates how imaging will alter management",
                    "parameter": "management_change_documented",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Operative report and recent surgical follow-up notes documenting suspected complication"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74176",
            "CPT 74177"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Postoperative assessment window applying within first few months following abdominal/pelvic surgery."
    },

    # CG 2001 - Abdomen CT
    {
        "rule_id": "RULE-ADV-CG2001-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 37,
            "printed_page": "Page 3 of 23"
        },
        "source_section": "STATEMENT / Special Note",
        "source_quote": "When separate requests for CT abdomen and CT Pelvis are encountered for processes involving both the abdomen and pelvis, they need to be resubmitted as Evolent Clinical Guideline 2000 for Abdomen and Pelvis CT (to avoid unbundling; CPT codes 74176, 74177, 74178).",
        "clinical_service_or_procedure": "CT Abdomen (Isolated)",
        "rule_type": "coding_rule",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Separate requests submitted for CT Abdomen and CT Pelvis",
                    "parameter": "separate_abdomen_and_pelvis_requested",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Clinical process or pathology involves both abdominal and pelvic anatomy",
                    "parameter": "pathology_involves_both_cavities",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical indication demonstrating pathology is strictly confined to upper abdomen if isolated CT Abdomen requested"
        ],
        "decision_effect": "ALTERNATIVE_MODALITY_RECOMMENDED",
        "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
        "dependencies": [
            "CPT 74150",
            "CPT 74160",
            "CPT 74170",
            "CG 2000"
        ],
        "human_review_required": True,
        "extraction_status": "NEEDS_HUMAN_REVIEW",
        "review_notes": "Anti-unbundling coding rule mandating combined CT Abdomen/Pelvis codes (74176-74178) when both regions are indicated."
    },
    {
        "rule_id": "RULE-ADV-CG2001-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 39,
            "printed_page": "Page 5 of 23"
        },
        "source_section": "INDICATIONS FOR ABDOMEN CT / Pancreas",
        "source_quote": "After confirmed diagnosis of exocrine pancreatic insufficiency (EPI), one-time imaging to exclude a secondary cause for EPI. (Imaging is not indicated for workup of suspected pancreatic insufficiency; fecal elastase level < 100 µg/g is consistent with EPI)",
        "clinical_service_or_procedure": "CT Abdomen",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Diagnosis of exocrine pancreatic insufficiency confirmed by fecal elastase",
                    "parameter": "fecal_elastase_ug_g",
                    "comparator": "LESS_THAN",
                    "value": 100,
                    "unit": "ug/g"
                },
                {
                    "condition_id": "COND-002",
                    "description": "One-time imaging evaluation to exclude secondary structural etiology",
                    "parameter": "prior_epi_ct_performed",
                    "comparator": "EQUALS",
                    "value": False
                }
            ]
        },
        "required_documentation": [
            "Fecal elastase laboratory report demonstrating < 100 ug/g"
        ],
        "exclusion_conditions": [
            "Imaging requested for initial workup of suspected pancreatic insufficiency prior to fecal elastase confirmation"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74160",
            "CPT 74170"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Diagnostic prerequisite mandating fecal elastase confirmation before one-time diagnostic CT."
    },
    {
        "rule_id": "RULE-ADV-CG2001-003",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 39,
            "printed_page": "Page 5 of 23"
        },
        "source_section": "INDICATIONS FOR ABDOMEN CT / Renal",
        "source_quote": "Indeterminate renal mass on other imaging (13) ● Active surveillance for a solid renal mass(es) at 6 and 12 months, then annually",
        "clinical_service_or_procedure": "CT Abdomen",
        "rule_type": "temporal_threshold",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Known solid renal mass undergoing active surveillance",
                    "parameter": "solid_renal_mass_present",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Surveillance interval matches protocol (6 mo, 12 mo, then annually)",
                    "parameter": "months_since_prior_renal_ct",
                    "comparator": "GREATER_THAN_OR_EQUAL",
                    "value": 6,
                    "unit": "months"
                }
            ]
        },
        "required_documentation": [
            "Prior ultrasound, CT, or MRI report documenting solid renal mass and date of last scan"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74160",
            "CPT 74170"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Surveillance interval rule for solid renal mass active surveillance."
    },
    {
        "rule_id": "RULE-ADV-CG2001-004",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 41,
            "printed_page": "Page 7 of 23"
        },
        "source_section": "Evaluation of Infection and Inflammation / Pancreatitis: Suspected and Known (27)",
        "source_quote": "In patients > 40 years of age who have pancreatitis with no identifiable cause (to exclude neoplasm)",
        "clinical_service_or_procedure": "CT Abdomen",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Patient age strictly greater than 40 years",
                    "parameter": "patient_age_years",
                    "comparator": "GREATER_THAN",
                    "value": 40,
                    "unit": "years"
                },
                {
                    "condition_id": "COND-002",
                    "description": "Documented acute or chronic pancreatitis",
                    "parameter": "pancreatitis_diagnosed",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-003",
                    "description": "No identifiable cause established (idiopathic, no gallstones/alcohol etiology)",
                    "parameter": "pancreatitis_etiology_identified",
                    "comparator": "EQUALS",
                    "value": False
                }
            ]
        },
        "required_documentation": [
            "Clinical notes demonstrating idiopathic pancreatitis in patient over 40 and negative basic etiology workup"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74160",
            "CPT 74170"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Age-stratified oncology exclusion rule for idiopathic pancreatitis in patients over 40."
    },
    {
        "rule_id": "RULE-ADV-CG2001-005",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 41,
            "printed_page": "Page 7 of 23"
        },
        "source_section": "Infection and Inflammation Limited to the Abdomen (27,29) / Hernia (30)",
        "source_quote": "Suspected hernia and one of the following: ○ Deep intraabdominal/pelvic hernia (post-Roux-en-Y) ○ Non-midline ventral hernia (including Spigelian hernia)",
        "clinical_service_or_procedure": "CT Abdomen",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinically suspected abdominal wall hernia",
                    "parameter": "suspected_hernia",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Deep intraabdominal hernia post-gastric bypass OR non-midline ventral/Spigelian hernia",
                    "parameter": "hernia_subtypes",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "HERN-001",
                                "description": "Post-Roux-en-Y gastric bypass with suspected internal hernia",
                                "parameter": "post_roux_en_y_status",
                                "comparator": "EQUALS",
                                "value": True
                            },
                            {
                                "condition_id": "HERN-002",
                                "description": "Suspected non-midline ventral hernia or Spigelian hernia",
                                "parameter": "non_midline_ventral_hernia",
                                "comparator": "EQUALS",
                                "value": True
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Surgical or clinical notes detailing bariatric surgical history or physical examination of non-midline abdominal defect"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74160",
            "CPT 74170"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Complex abdominal wall and internal hernia indication."
    },

    # CG 2002 - Abdomen CTA
    {
        "rule_id": "RULE-ADV-CG2002-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 61,
            "printed_page": "Page 4 of 12"
        },
        "source_section": "INDICATIONS FOR ABDOMEN CTA / Renal Artery Stenosis",
        "source_quote": "In a patient with hypertension AND prior abnormal or inconclusive ultrasound with any ONE of the following (1,2): ● Onset of hypertension prior to the age of 30 without a family history of hypertension and when there is suspicion of fibromuscular dysplasia or a vasculitis ● Failure to obtain adequate blood pressure control on 3 antihypertensive medications, including one diuretic",
        "clinical_service_or_procedure": "CTA Abdomen",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Documented hypertension with prior abnormal or inconclusive renal artery duplex ultrasound",
                    "parameter": "hypertension_with_prior_ultrasound",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Early onset (<30 yr) without family history OR resistant hypertension on 3 medications including diuretic",
                    "parameter": "renovascular_hypertension_features",
                    "comparator": "IS_PRESENT",
                    "sub_conditions": {
                        "operator": "ANY_OF",
                        "criteria": [
                            {
                                "condition_id": "RAS-001",
                                "description": "Onset of hypertension prior to age 30 without family history",
                                "parameter": "hypertension_onset_age",
                                "comparator": "LESS_THAN",
                                "value": 30,
                                "unit": "years"
                            },
                            {
                                "condition_id": "RAS-002",
                                "description": "Refractory hypertension failing 3 concurrent antihypertensive drugs including a diuretic",
                                "parameter": "antihypertensive_medications_count",
                                "comparator": "GREATER_THAN_OR_EQUAL",
                                "value": 3
                            }
                        ]
                    }
                }
            ]
        },
        "required_documentation": [
            "Renal duplex ultrasound report demonstrating abnormal or inconclusive velocity measurements",
            "Medication administration record detailing 3 concurrent antihypertensive agents with diuretic"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74175"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Secondary renovascular hypertension indication requiring prior ultrasound failure."
    },
    {
        "rule_id": "RULE-ADV-CG2002-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 61,
            "printed_page": "Page 4 of 12"
        },
        "source_section": "INDICATIONS FOR ABDOMEN CTA / Other Vascular Abnormalities of the Abdomen",
        "source_quote": "Initial evaluation of inconclusive vascular findings on prior imaging of the abdomen",
        "clinical_service_or_procedure": "CTA Abdomen",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Inconclusive or equivocal vascular finding on prior abdominal ultrasound or CT",
                    "parameter": "prior_vascular_imaging_inconclusive",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Prior abdominal imaging report citing indeterminate vascular abnormality requiring definitive angiography"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74175"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Diagnostic clarification pathway for indeterminate vascular findings."
    },

    # CG 2003 - Abdomen MRA
    {
        "rule_id": "RULE-ADV-CG2003-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 75,
            "printed_page": "Page 6 of 18"
        },
        "source_section": "INDICATIONS FOR ABDOMEN MRA / Other Vascular Abnormalities / Takayasu's Arteritis (15)",
        "source_quote": "Takayasu's Arteritis (15): ○ At initial diagnosis ○ Every 6 months for the first 2 years while on therapy ○ Annually after the first 2 years",
        "clinical_service_or_procedure": "MRA Abdomen",
        "rule_type": "temporal_threshold",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Confirmed diagnosis of Takayasu's arteritis",
                    "parameter": "takayasu_arteritis_diagnosed",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "MRA requested at initial diagnosis, q6 months during first 2 years of active therapy, or annually thereafter",
                    "parameter": "takayasu_surveillance_interval_met",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Rheumatology progress notes documenting Takayasu arteritis diagnosis, active immunosuppressive therapy, and prior imaging dates"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74185"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Radiation-free surveillance intervals for large-vessel vasculitis."
    },
    {
        "rule_id": "RULE-ADV-CG2003-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 73,
            "printed_page": "Page 4 of 18"
        },
        "source_section": "INDICATIONS FOR ABDOMEN MRA / Abdominal Aortic Aneurysm (AAA)",
        "source_quote": "Known or suspected symptomatic AAA when (1,2) ○ Symptoms may include: ■ Abrupt onset of severe sharp or stabbing pain in the chest, back or abdomen (could indicate possible aneurysm rupture) ■ Acute abdominal or back pain with a pulsatile or epigastric mass",
        "clinical_service_or_procedure": "MRA Abdomen",
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
                    "description": "Severe stabbing chest/back/abdominal pain or acute pain with pulsatile mass",
                    "parameter": "acute_aortic_symptoms",
                    "comparator": "IS_PRESENT",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Urgent clinical notes documenting acute abdominal/back pain and clinical rationale for MRA (e.g. severe iodinated contrast allergy precluding CTA)"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74185"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Symptomatic AAA evaluation by MRA when CTA is contraindicated."
    },

    # CG 2004 - Abdomen MRI / MRCP
    {
        "rule_id": "RULE-ADV-CG2004-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 92,
            "printed_page": "Page 5 of 26"
        },
        "source_section": "INDICATIONS / Biliary / Choledochal cyst",
        "source_quote": "Suspected choledochal cyst after ultrasound has been done",
        "clinical_service_or_procedure": "Abdomen MRI / MRCP",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinically suspected choledochal cyst or congenital biliary duct dilatation",
                    "parameter": "suspected_choledochal_cyst",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Initial diagnostic workup with abdominal ultrasound completed",
                    "parameter": "prior_ultrasound_completed",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Abdominal ultrasound report documenting biliary tree visualization prior to MRCP"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74181",
            "CPT 74183"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Prerequisite ultrasound requirement prior to MRCP for congenital biliary cyst."
    },
    {
        "rule_id": "RULE-ADV-CG2004-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 92,
            "printed_page": "Page 5 of 26"
        },
        "source_section": "INDICATIONS / Pancreas",
        "source_quote": "Suspected new onset acute pancreatitis and ALL of the following: ○ Epigastric or upper abdominal pain",
        "clinical_service_or_procedure": "Abdomen MRI / MRCP",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected new onset acute pancreatitis",
                    "parameter": "suspected_acute_pancreatitis",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Documented epigastric or upper abdominal pain",
                    "parameter": "epigastric_pain_present",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Clinical notes detailing epigastric pain and reason for MRI/MRCP (e.g. occult choledocholithiasis, pregnancy, or iodinated contrast allergy)"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74183"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Pancreatitis evaluation by MRI/MRCP for ductal stones."
    },

    # CG 2005 - Abdomen Pelvis CTA
    {
        "rule_id": "RULE-ADV-CG2005-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 118,
            "printed_page": "Page 5 of 15"
        },
        "source_section": "INDICATIONS FOR ABDOMEN PELVIS CTA / Other Vascular Abnormalities of the Abdomen and Pelvis",
        "source_quote": "Evaluation of known or suspected mesenteric ischemia/ischemic colitis",
        "clinical_service_or_procedure": "CTA Abdomen and Pelvis",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Clinical suspicion or known acute or chronic mesenteric ischemia or ischemic colitis",
                    "parameter": "suspected_mesenteric_ischemia",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Urgent clinical notes detailing postprandial pain, bloody stools, or acute severe abdominal pain out of proportion to exam"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74174",
            "CPT 74175"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Urgent vascular mesenteric ischemia indication."
    },
    {
        "rule_id": "RULE-ADV-CG2005-002",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 119,
            "printed_page": "Page 6 of 15"
        },
        "source_section": "INDICATIONS FOR ABDOMEN PELVIS CTA / Other Vascular Abnormalities",
        "source_quote": "Suspected pelvic congestive syndrome (including May-Thurner and nutcracker syndromes) when ultrasound is indeterminant",
        "clinical_service_or_procedure": "CTA Abdomen and Pelvis",
        "rule_type": "clinical_prerequisite",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected pelvic congestion syndrome, May-Thurner, or nutcracker syndrome",
                    "parameter": "suspected_pelvic_venous_syndrome",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "Initial pelvic or vascular ultrasound was indeterminate",
                    "parameter": "prior_ultrasound_indeterminate",
                    "comparator": "EQUALS",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Pelvic or vascular duplex ultrasound report demonstrating indeterminate or incomplete evaluation of venous compression"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 74174"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Diagnostic prerequisite ultrasound requirement for pelvic venous compression syndromes."
    },

    # CG 2006 - Abdominal Aorta CTA with Lower Extremity Runoff
    {
        "rule_id": "RULE-ADV-CG2006-001",
        "domain": "advanced_imaging",
        "document_type": "governing_policy",
        "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2)",
        "policy_version": "2026 v2",
        "version_status": "current_2026_verified",
        "source_file": GOV_PDF,
        "source_url": GOV_URL,
        "source_page": {
            "physical_page": 132,
            "printed_page": "Page 4 of 10"
        },
        "source_section": "INDICATIONS / Peripheral Arterial Disease / Critical Limb Ischemia",
        "source_quote": "For acute critical limb ischemia with any ONE of the below clinical signs of peripheral vascular disease: ○ Ischemic rest pain ○ Tissue loss ○ Gangrene",
        "clinical_service_or_procedure": "CTA Abdominal Aorta with Lower Extremity Runoff",
        "rule_type": "clinical_indication",
        "conditions": {
            "operator": "ALL_OF",
            "criteria": [
                {
                    "condition_id": "COND-001",
                    "description": "Suspected or known peripheral arterial disease with critical limb ischemia",
                    "parameter": "critical_limb_ischemia_present",
                    "comparator": "EQUALS",
                    "value": True
                },
                {
                    "condition_id": "COND-002",
                    "description": "At least one sign: ischemic rest pain, non-healing ischemic ulceration/tissue loss, or gangrene",
                    "parameter": "cli_objective_signs",
                    "comparator": "IS_PRESENT",
                    "value": True
                }
            ]
        },
        "required_documentation": [
            "Vascular surgery or podiatry exam documenting rest pain, tissue ulceration, or gangrene"
        ],
        "decision_effect": "INDICATED",
        "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
        "dependencies": [
            "CPT 75635"
        ],
        "human_review_required": False,
        "extraction_status": "DRAFT",
        "review_notes": "Urgent critical limb ischemia bypasses conservative medical trial."
    }
]

# Combine CG 2000 rules + new rules for batch 1
batch_01_all_rules = cg2000_rules + batch_01_new_rules

def main():
    schema_path = RULES_DIR / "schema.json"
    checkpoint_path = CHECKPOINTS_DIR / "batch_01_rules.json"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for i, r in enumerate(batch_01_all_rules, 1):
        jsonschema.validate(instance=r, schema=schema)
        print(f"Batch 1 Rule {i} ({r['rule_id']}): Schema VALID")

    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(batch_01_all_rules, f, indent=2)

    print(f"\nSuccessfully validated and saved {len(batch_01_all_rules)} rules to {checkpoint_path}")

if __name__ == "__main__":
    main()
