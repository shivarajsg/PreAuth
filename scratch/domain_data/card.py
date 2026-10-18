"""
Cardiology Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-CARD-003", "CODING_OR_BILLING_REFERENCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-004", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-005", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-006", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-007", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-008", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-009", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-010", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-CARD-011", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-CARD-001",
        "document_id": "DOC-CARD-003",
        "policy_id": "2026 Evolent Cardiology Guidelines",
        "rule_id": "RULE-CARD-PREAMBLEDIAG-001",
        "physical_page_or_section": "pp. 1-8 / CPT Groupings",
        "relationship_type": "SUPPORTS_CODE_INTERPRETATION",
        "evidence_description": "Defines prior-authorization scope and CPT clusters across diagnostic echocardiography, nuclear MPI, cardiac CT/MR, and catheterization.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-002",
        "document_id": "DOC-CARD-004",
        "policy_id": "OP38801",
        "rule_id": "RULE-CARD-OP38801-001",
        "physical_page_or_section": "pp. 1-2 / Policy Guidelines",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Enforces procedural bundling edits preventing separate reimbursement for spectral/color Doppler with stress echo unless distinct resting valve indications exist.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-003",
        "document_id": "DOC-CARD-005",
        "policy_id": "2026 Evolent Diagnostic Cardiology Guidelines",
        "rule_id": "RULE-CARD-PREAMBLEDIAG-001",
        "physical_page_or_section": "pp. 1-2 / Information Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Comprehensive cardiac intake checklist capturing member demographics, NPI, clinical notes, resting ECG, LVEF, symptom status, and medical therapy.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-004",
        "document_id": "DOC-CARD-005",
        "policy_id": "2026 Evolent Diagnostic Cardiology Guidelines",
        "rule_id": "RULE-CARD-CG7252-001",
        "physical_page_or_section": "Page 1 / Stress Testing Evidence",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Captures treadmill exercise tolerance, baseline ECG interpretability, and angina symptoms for stress echocardiography qualification.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-005",
        "document_id": "DOC-CARD-005",
        "policy_id": "2026 Evolent Diagnostic Cardiology Guidelines",
        "rule_id": "RULE-CARD-CG7253-001",
        "physical_page_or_section": "Page 1 / Nuclear MPI Evidence",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Captures LBBB, pacemaker dependency, or uninterpretable baseline ECG necessitating myocardial perfusion imaging over treadmill stress echo.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-006",
        "document_id": "DOC-CARD-006",
        "policy_id": "2026 Evolent Cardiology Solution",
        "rule_id": "RULE-CARD-PREAMBLEDIAG-001",
        "physical_page_or_section": "pp. 1-3 / Solution Overview",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Procedural guidance detailing clinical decision support workflow, provider portal navigation, and peer-to-peer escalation pathways.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-007",
        "document_id": "DOC-CARD-007",
        "policy_id": "2026 Evolent Interventional Cardiology Guidelines",
        "rule_id": "RULE-CARD-CG7254-001",
        "physical_page_or_section": "pp. 1-2 / Cath Indications",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Outlines high-risk non-invasive stress test findings, refractory angina CCS III/IV, or acute coronary syndrome criteria justifying diagnostic heart catheterization.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-008",
        "document_id": "DOC-CARD-008",
        "policy_id": "2026 Evolent Diagnostic Cardiology Guidelines",
        "rule_id": "RULE-CARD-CG7253-001",
        "physical_page_or_section": "pp. 1-2 / Modality Selection Matrix",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Comparative clinical algorithm for selecting between Nuclear MPI and Stress Echocardiography based on patient mobility, body habitus, and baseline ECG.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-009",
        "document_id": "DOC-CARD-009",
        "policy_id": "2026 Evolent Diagnostic Cardiology Guidelines",
        "rule_id": "RULE-CARD-CG7253-001",
        "physical_page_or_section": "pp. 1-2 / MPI Criteria Summary",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Summarizes pharmacologic vasodilator stress indications (adenosine, regadenoson) and ischemic risk stratification benchmarks for MPI.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-010",
        "document_id": "DOC-CARD-010",
        "policy_id": "2026 Evolent Diagnostic Cardiology Guidelines",
        "rule_id": "RULE-CARD-CG7252-001",
        "physical_page_or_section": "pp. 1-2 / Stress Echo Criteria Summary",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Summarizes treadmill exercise and dobutamine stress echocardiography indications, target heart rate calculations, and wall motion abnormality criteria.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CARD-011",
        "document_id": "DOC-CARD-011",
        "policy_id": "2026 Evolent Diagnostic Cardiology Guidelines",
        "rule_id": "RULE-CARD-CG7251-001",
        "physical_page_or_section": "pp. 1-2 / TTE Criteria Summary",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Summarizes resting transthoracic echocardiography indications for heart failure, valvular heart disease, syncope, and cardioembolic stroke evaluation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-CARD-005-01",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Member Demographics",
        "field_label": "Member Full Legal Name",
        "field_meaning": "Patient identifier for cardiology health plan benefit verification",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for patient eligibility lookup"
    },
    {
        "field_id": "FIELD-CARD-005-02",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Member Demographics",
        "field_label": "Member Insurance ID & Policy Number",
        "field_meaning": "Cardiovascular benefit subscriber identification number",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Determines payer line of business"
    },
    {
        "field_id": "FIELD-CARD-005-03",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Member Demographics",
        "field_label": "Date of Birth",
        "field_meaning": "Patient age verification for pediatric vs adult cardiology guidelines",
        "data_type": "date",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Routes to adult vs pediatric guideline algorithms"
    },
    {
        "field_id": "FIELD-CARD-005-04",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Provider Information",
        "field_label": "Ordering Clinician Name & NPI",
        "field_meaning": "National Provider Identifier of ordering cardiologist or primary physician",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates licensed ordering physician credentials"
    },
    {
        "field_id": "FIELD-CARD-005-05",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Facility Setting",
        "field_label": "Servicing Place of Service Facility NPI & Setting",
        "field_meaning": "Requested imaging setting (freestanding cardiology clinic vs hospital outpatient)",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Evaluates place of service medical necessity"
    },
    {
        "field_id": "FIELD-CARD-005-06",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Procedure Requested",
        "field_label": "Requested Procedure CPT Code(s)",
        "field_meaning": "Specific CPT code (e.g., 93306 TTE, 93350/93351 Stress Echo, 78452 MPI, 93458 Cath)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Selects corresponding clinical criteria branch"
    },
    {
        "field_id": "FIELD-CARD-005-07",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Clinical Indication",
        "field_label": "Primary ICD-10 Cardiac Diagnosis Code",
        "field_meaning": "Diagnostic diagnosis code (e.g., I25.10 CAD, I50.9 Heart Failure, R07.9 Chest Pain)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Establishes clinical diagnostic indication"
    },
    {
        "field_id": "FIELD-CARD-005-08",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Clinical Records",
        "field_label": "Cardiovascular Progress Notes & Physical Exam",
        "field_meaning": "Recent clinical notes detailing cardiac symptoms, vital signs, and cardiovascular exam",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Required objective source record"
    },
    {
        "field_id": "FIELD-CARD-005-09",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Diagnostic Testing",
        "field_label": "Baseline 12-Lead Electrocardiogram (ECG) Report",
        "field_meaning": "Resting 12-lead ECG findings (normal, ST-T changes, LBBB, LVH, WPW, pacemaker rhythm)",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Stress Testing & Cath Intake",
        "linked_policy_or_rule": "RULE-CARD-CG7252-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Critical for stress test modality selection (interpretable vs uninterpretable baseline)"
    },
    {
        "field_id": "FIELD-CARD-005-10",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Diagnostic Testing",
        "field_label": "Prior Left Ventricular Ejection Fraction (LVEF) %",
        "field_meaning": "Documented resting ejection fraction from prior echo, nuclear scan, or cath within past 12 months",
        "data_type": "numeric",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Heart Failure & Ischemia",
        "linked_policy_or_rule": "RULE-CARD-CG7251-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Threshold evaluation for systolic dysfunction (LVEF <= 40% or <= 50%)"
    },
    {
        "field_id": "FIELD-CARD-005-11",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Diagnostic Testing",
        "field_label": "Prior Stress Test Modality, Date, and Result",
        "field_meaning": "Results of previous stress testing within 12-24 months and reason for repeat testing",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Repeat Stress Testing",
        "linked_policy_or_rule": "RULE-CARD-CG7252-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Frequency restriction check against guideline surveillance intervals"
    },
    {
        "field_id": "FIELD-CARD-005-12",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Diagnostic Testing",
        "field_label": "Prior Coronary Angiogram / PCI / CABG History",
        "field_meaning": "History of anatomical coronary revascularization or documented coronary artery disease",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Ischemic Evaluation",
        "linked_policy_or_rule": "RULE-CARD-CG7254-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Determines established vs suspected CAD diagnostic pathway"
    },
    {
        "field_id": "FIELD-CARD-005-13",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Symptom Profile",
        "field_label": "Anginal Symptom Status & CCS Angina Class",
        "field_meaning": "Typical angina, atypical angina, or non-cardiac chest pain; CCS Class I through IV",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "CAD Stress & Cath",
        "linked_policy_or_rule": "RULE-CARD-CG7252-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Pre-test probability determination anchor"
    },
    {
        "field_id": "FIELD-CARD-005-14",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Symptom Profile",
        "field_label": "Dyspnea / NYHA Functional Class",
        "field_meaning": "Exertional dyspnea classified by New York Heart Association functional class (I-IV)",
        "data_type": "enum",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Heart Failure & Valvular Disease",
        "linked_policy_or_rule": "RULE-CARD-CG7251-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Evaluates decompensation or functional progression"
    },
    {
        "field_id": "FIELD-CARD-005-15",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Functional Capacity",
        "field_label": "Patient Physical Ability to Perform Treadmill Exercise",
        "field_meaning": "Ability to walk on a motorized treadmill >= 3 minutes (>= 5 METs) without severe orthopedic limitation",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Stress Testing Intake",
        "linked_policy_or_rule": "RULE-CARD-CG7252-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Required to authorize pharmacologic stress vs exercise stress testing"
    },
    {
        "field_id": "FIELD-CARD-005-16",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Medical Therapy",
        "field_label": "Guideline-Directed Medical Therapy (GDMT) Trial Documentation",
        "field_meaning": "Trial of antianginal medications (beta-blockers, nitrates, CCBs, ranolazine) and statins",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Cath & Advanced Stress",
        "linked_policy_or_rule": "RULE-CARD-CG7254-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory prior conservative medical therapy for elective catheterization"
    },
    {
        "field_id": "FIELD-CARD-005-17",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 2 / Pediatric Indications",
        "field_label": "Pediatric Congenital or Acquired Heart Disease Documentation",
        "field_meaning": "Structural anomaly, cyanosis, Kawasaki disease, or cardiotoxic drug exposure in pediatric patient",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Pediatric Cardiology",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Triggers specialized pediatric congenital heart disease review"
    },
    {
        "field_id": "FIELD-CARD-005-18",
        "document_id": "DOC-CARD-005",
        "source_page_or_section": "Page 1 / Attestation",
        "field_label": "Ordering Provider Clinical Attestation Signature",
        "field_meaning": "Affirmation that submitted clinical details are true and present in the permanent medical record",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Cardiology Intake",
        "linked_policy_or_rule": "RULE-CARD-PREAMBLEDIAG-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Legal clinical attestation required on file"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-CARD-MISSING-001",
        "domain": "cardiology",
        "document_title": "Plan-Specific Cardiac Stress Testing Tiering Crosswalk Grids",
        "document_category": "Plan custom grid",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PLAN_SPECIFIC_ACCESS_REQUIRED",
        "unmapped_reason": "Health-plan specific benefit schedules establish whether treadmill exercise ECG is required before stress echo or MPI.",
        "evidentiary_limitation": "Restricted commercial payer schedule requiring contracted plan administrator verification.",
        "human_review_required": True
    }
]
