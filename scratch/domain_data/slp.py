"""
Sleep Health Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-SLP-002", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-SLP-003", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-SLP-001",
        "document_id": "DOC-SLP-002",
        "policy_id": "2026 Evolent Sleep Studies Guidelines",
        "rule_id": "RULE-SLP-CG2050-001",
        "physical_page_or_section": "pp. 1-2 / General Sleep Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Comprehensive prior authorization checklist capturing Epworth score, witnessed apneas, comorbidities, and HSAT vs attended lab PSG indications.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-SLP-002",
        "document_id": "DOC-SLP-002",
        "policy_id": "2026 Evolent Sleep Studies Guidelines",
        "rule_id": "RULE-SLP-CG2051-001",
        "physical_page_or_section": "Page 1 / Pediatric Criteria",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing pediatric tonsillar hypertrophy, failure to thrive, and parasomnias requiring attended in-laboratory polysomnography.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-SLP-003",
        "document_id": "DOC-SLP-002",
        "policy_id": "2026 Evolent Sleep Studies Guidelines",
        "rule_id": "RULE-SLP-CG2050-004",
        "physical_page_or_section": "Page 2 / PAP Titration",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Captures diagnostic AHI >= 15 or AHI 5-14 with symptoms justifying full-night or split-night CPAP/BiPAP titration study.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-SLP-004",
        "document_id": "DOC-SLP-003",
        "policy_id": "2026 Evolent Sleep Studies Guidelines",
        "rule_id": "RULE-SLP-CG2050-001",
        "physical_page_or_section": "pp. 1-2 / No-HST Benefit Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Specialized intake checklist for health plans lacking home sleep test coverage, collecting adult clinical suspicion of OSA for direct attended lab PSG.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-SLP-002-01",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Member Demographics",
        "field_label": "Member Full Name & Health Plan ID",
        "field_meaning": "Patient identifier for sleep health prior authorization lookup",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Sleep Study Intake",
        "linked_policy_or_rule": "RULE-SLP-PREAMBLE-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for member matching and benefit plan lookup"
    },
    {
        "field_id": "FIELD-SLP-002-02",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Ordering Clinician",
        "field_label": "Ordering Clinician Name & NPI",
        "field_meaning": "National Provider Identifier of ordering sleep specialist or physician",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Sleep Study Intake",
        "linked_policy_or_rule": "RULE-SLP-PREAMBLE-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates licensed ordering physician"
    },
    {
        "field_id": "FIELD-SLP-002-03",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Requested Study",
        "field_label": "Requested Procedure CPT Code (HSAT vs Attended PSG)",
        "field_meaning": "Specific sleep test code (e.g. 95806/95800 HSAT Type III/IV, 95810 Diagnostic PSG, 95811 Titration)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Sleep Study Intake",
        "linked_policy_or_rule": "RULE-SLP-PREAMBLE-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Selects corresponding clinical criteria algorithm"
    },
    {
        "field_id": "FIELD-SLP-002-04",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Clinical Notes",
        "field_label": "Comprehensive Sleep Evaluation Office Visit Notes",
        "field_meaning": "Recent face-to-face physician notes documenting sleep complaints, airway exam, BMI, and neck circumference",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Sleep Study Intake",
        "linked_policy_or_rule": "RULE-SLP-PREAMBLE-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory objective medical documentation"
    },
    {
        "field_id": "FIELD-SLP-002-05",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Sleepiness Scale",
        "field_label": "Epworth Sleepiness Scale (ESS) Score or STOP-BANG",
        "field_meaning": "Validated quantified measure of daytime sleepiness (ESS score >= 10 indicates excessive sleepiness)",
        "data_type": "numeric",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Adult Sleep Testing",
        "linked_policy_or_rule": "RULE-SLP-CG2050-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Objective clinical symptom score"
    },
    {
        "field_id": "FIELD-SLP-002-06",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / OSA Symptoms",
        "field_label": "Witnessed Apneas, Habitual Snoring, or Nocturnal Choking",
        "field_meaning": "Bed partner or self-reported cardinal symptoms of obstructive sleep apnea",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Adult Sleep Testing",
        "linked_policy_or_rule": "RULE-SLP-CG2050-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Primary clinical symptom indication"
    },
    {
        "field_id": "FIELD-SLP-002-07",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Comorbidities",
        "field_label": "Moderate to Severe Pulmonary Disease (COPD / Hypoventilation)",
        "field_meaning": "Presence of severe lung disease or daytime hypercapnia requiring attended in-lab PSG monitoring",
        "data_type": "boolean",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Attended PSG Qualification",
        "linked_policy_or_rule": "RULE-SLP-CG2050-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Clinical exception bypassing home sleep testing requirement"
    },
    {
        "field_id": "FIELD-SLP-002-08",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Comorbidities",
        "field_label": "Congestive Heart Failure (NYHA Class III-IV)",
        "field_meaning": "Symptomatic advanced heart failure carrying risk of Cheyne-Stokes central breathing",
        "data_type": "boolean",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Attended PSG Qualification",
        "linked_policy_or_rule": "RULE-SLP-CG2050-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Justifies attended PSG over home testing"
    },
    {
        "field_id": "FIELD-SLP-002-09",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Comorbidities",
        "field_label": "Neuromuscular Disease Affecting Respiratory Muscles",
        "field_meaning": "Diagnosis such as ALS, muscular dystrophy, or myasthenia gravis",
        "data_type": "boolean",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Attended PSG Qualification",
        "linked_policy_or_rule": "RULE-SLP-CG2050-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Justifies attended PSG over home testing"
    },
    {
        "field_id": "FIELD-SLP-002-10",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Prior Testing",
        "field_label": "Prior Home Sleep Test Inconclusive or Technically Inadequate",
        "field_meaning": "Documented failure of previous HSAT due to sensor detachment, insufficient recording time (<4 hours), or negative result with persistent high symptoms",
        "data_type": "boolean",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Attended PSG Qualification",
        "linked_policy_or_rule": "RULE-SLP-CG2050-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Qualifies patient for secondary attended PSG"
    },
    {
        "field_id": "FIELD-SLP-002-11",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Cognitive / Motor Ability",
        "field_label": "Physical or Cognitive Inability to Self-Administer HSAT Device",
        "field_meaning": "Severe dementia, quadriplegia, or absence of caregiver to place sensors",
        "data_type": "boolean",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Attended PSG Qualification",
        "linked_policy_or_rule": "RULE-SLP-CG2050-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Directs patient to laboratory attended PSG"
    },
    {
        "field_id": "FIELD-SLP-002-12",
        "document_id": "DOC-SLP-002",
        "source_page_or_section": "Page 1 / Attestation",
        "field_label": "Ordering Clinician Sleep Attestation Signature",
        "field_meaning": "Ordering physician confirmation of documented medical record evidence",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Sleep Study Intake",
        "linked_policy_or_rule": "RULE-SLP-PREAMBLE-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory signed legal attestation"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-SLP-MISSING-001",
        "domain": "sleep_health",
        "document_title": "Commercial Employer Group Home Sleep Test Exemption Lists",
        "document_category": "Employer benefit exception list",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PLAN_SPECIFIC_ACCESS_REQUIRED",
        "unmapped_reason": "Specific self-insured employer health plans exempt members from home sleep test requirements, allowing direct attended PSG.",
        "evidentiary_limitation": "Available only in confidential employer benefit schedules.",
        "human_review_required": True
    }
]
