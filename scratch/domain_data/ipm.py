"""
Interventional Pain Management Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-IPM-002", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-IPM-003", "HISTORICAL_DOCUMENT_COMPARISON", "PUBLIC_ACCESSIBLE"),
    ("DOC-IPM-004", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-IPM-005", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-IPM-006", "HISTORICAL_DOCUMENT_COMPARISON", "PUBLIC_ACCESSIBLE"),
    ("DOC-IPM-007", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-IPM-001",
        "document_id": "DOC-IPM-002",
        "policy_id": "EPOS 1755",
        "rule_id": "RULE-IPM-EPOS1755-001",
        "physical_page_or_section": "pp. 1-8 / Section I-III",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Establishes site of service guidelines directing epidural and facet injections to physician offices or ASCs, restricting hospital outpatient facilities to high-risk clinical exceptions.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-IPM-002",
        "document_id": "DOC-IPM-003",
        "policy_id": "2025 Evolent Interventional Pain Guidelines",
        "rule_id": "",
        "physical_page_or_section": "pp. 1-285 / Entire Policy",
        "relationship_type": "HISTORICAL_COMPARISON_ONLY",
        "evidence_description": "Historical 2025 guideline retained for longitudinal comparison; quarantined from active 2026 rule evaluation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "Historical version; cannot be used for 2026 prior authorization"
    },
    {
        "mapping_id": "MAP-IPM-003",
        "document_id": "DOC-IPM-004",
        "policy_id": "2026 Evolent Interventional Pain Management Guidelines",
        "rule_id": "RULE-IPM-CGEPIDURALINJECTIONS-001",
        "physical_page_or_section": "pp. 1-2 / ESI Documentation",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Prior authorization checklist capturing pain intensity, radicular exam findings, conservative therapy duration, and imaging concordance for epidural steroid injections.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-IPM-004",
        "document_id": "DOC-IPM-004",
        "policy_id": "2026 Evolent Interventional Pain Management Guidelines",
        "rule_id": "RULE-IPM-CGFACETBLOCKS-001",
        "physical_page_or_section": "pp. 1-2 / Facet Block Documentation",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing axial non-radicular spine pain, absence of neurological deficit, and prior diagnostic medial branch block relief percentages for radiofrequency neurotomy.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-IPM-005",
        "document_id": "DOC-IPM-005",
        "policy_id": "2026 Evolent Interventional Pain Management Guidelines",
        "rule_id": "RULE-IPM-PREAMBLEIPM-001",
        "physical_page_or_section": "pp. 1-2 / Conservative Treatment Details",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Standardized conservative treatment form detailing physical therapy trial dates, medication trials, prior injection relief percentage and duration, and clinician attestation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-IPM-006",
        "document_id": "DOC-IPM-006",
        "policy_id": "2024 Evolent Pain Forms",
        "rule_id": "",
        "physical_page_or_section": "pp. 1-2 / Historical Form",
        "relationship_type": "HISTORICAL_COMPARISON_ONLY",
        "evidence_description": "Historical 2024 conservative treatment form superseded by Rev. July 2025 edition (DOC-IPM-005).",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "Historical document; quarantined"
    },
    {
        "mapping_id": "MAP-IPM-007",
        "document_id": "DOC-IPM-007",
        "policy_id": "2026 Evolent Interventional Pain Management Guidelines",
        "rule_id": "RULE-IPM-PREAMBLEIPM-001",
        "physical_page_or_section": "pp. 1-2 / Clinical Guidance",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Clinical tip sheet detailing imaging requirements, timing intervals between injections, maximum lifetime/annual injection limits, and fluoroscopy standards.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-IPM-004-01",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Member Information",
        "field_label": "Member Full Name & Health Plan ID",
        "field_meaning": "Patient identifier for interventional pain authorization",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Pain Management Intake",
        "linked_policy_or_rule": "RULE-IPM-PREAMBLEIPM-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for member matching and benefit plan lookup"
    },
    {
        "field_id": "FIELD-IPM-004-02",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Provider Information",
        "field_label": "Ordering Clinician Name & NPI",
        "field_meaning": "National Provider Identifier of ordering pain specialist or physician",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Pain Management Intake",
        "linked_policy_or_rule": "RULE-IPM-PREAMBLEIPM-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates licensed ordering physician credentials"
    },
    {
        "field_id": "FIELD-IPM-004-03",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Setting",
        "field_label": "Place of Service Setting (Office vs ASC vs Hospital Outpatient)",
        "field_meaning": "Requested facility setting for EPOS 1755 place of service compliance",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Pain Management Intake",
        "linked_policy_or_rule": "RULE-IPM-EPOS1755-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Enforces ambulatory place of service redirect"
    },
    {
        "field_id": "FIELD-IPM-004-04",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Procedure Requested",
        "field_label": "Requested Procedure CPT Code(s)",
        "field_meaning": "Specific CPT code (e.g., 62323 lumbar interlaminar ESI, 64493 lumbar facet block, 64635 RFA)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Pain Management Intake",
        "linked_policy_or_rule": "RULE-IPM-PREAMBLEIPM-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Routes request to procedural criteria branch"
    },
    {
        "field_id": "FIELD-IPM-004-05",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Clinical Documentation",
        "field_label": "Comprehensive Pain Management Office Notes & Physical Exam",
        "field_meaning": "Recent clinical notes documenting pain severity, distribution, physical exam maneuvers, and functional impairment",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Pain Management Intake",
        "linked_policy_or_rule": "RULE-IPM-PREAMBLEIPM-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory objective medical record documentation"
    },
    {
        "field_id": "FIELD-IPM-004-06",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Pain Characteristics",
        "field_label": "Pain Distribution (Radicular vs Axial/Non-Radicular)",
        "field_meaning": "Differentiation between dermatomal radiating nerve pain and midline axial skeletal pain",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "ESI vs Facet Selection",
        "linked_policy_or_rule": "RULE-IPM-CGEPIDURALINJECTIONS-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Directs case to epidural vs facet injection algorithm"
    },
    {
        "field_id": "FIELD-IPM-004-07",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Image Guidance",
        "field_label": "Fluoroscopic or CT Guidance Affirmation",
        "field_meaning": "Affirmation that injection will be performed with active real-time image guidance and contrast",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Spinal Injections",
        "linked_policy_or_rule": "RULE-IPM-PREAMBLEIPM-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Image guidance is mandatory; blind spinal injections are non-covered"
    },
    {
        "field_id": "FIELD-IPM-004-08",
        "document_id": "DOC-IPM-004",
        "source_page_or_section": "Page 1 / Spinal Imaging",
        "field_label": "Spine MRI or CT Within Past 12 Months",
        "field_meaning": "Cross-sectional imaging report demonstrating nerve root compromise or canal stenosis correlating with pain level",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Epidural Steroid Injections",
        "linked_policy_or_rule": "RULE-IPM-CGEPIDURALINJECTIONS-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Required anatomical concordance verification"
    },
    {
        "field_id": "FIELD-IPM-005-01",
        "document_id": "DOC-IPM-005",
        "source_page_or_section": "Page 1 / Prior Injections",
        "field_label": "Prior Injection History and Percentage Pain Relief",
        "field_meaning": "Date, anatomical level, and documented percentage pain relief (>= 50% for therapeutic ESI, >= 80% for diagnostic MBB)",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Repeat Spinal Injections",
        "linked_policy_or_rule": "RULE-IPM-CGEPIDURALINJECTIONS-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Critical efficacy benchmark for repeat interventions"
    },
    {
        "field_id": "FIELD-IPM-005-02",
        "document_id": "DOC-IPM-005",
        "source_page_or_section": "Page 1 / Prior Relief Duration",
        "field_label": "Duration of Pain Relief from Prior Injection",
        "field_meaning": "Number of weeks or months relief persisted (minimum 2 months required for repeat therapeutic injection)",
        "data_type": "numeric",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Repeat Spinal Injections",
        "linked_policy_or_rule": "RULE-IPM-CGEPIDURALINJECTIONS-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Verifies minimum relief duration threshold"
    },
    {
        "field_id": "FIELD-IPM-005-03",
        "document_id": "DOC-IPM-005",
        "source_page_or_section": "Page 1 / Frequency Caps",
        "field_label": "Number of Spinal Injections in Past 12 Months",
        "field_meaning": "Total count of spinal injections received in preceding 12-month window (maximum 4 per anatomical region)",
        "data_type": "numeric",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Spinal Injections",
        "linked_policy_or_rule": "RULE-IPM-PREAMBLEIPM-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Enforces annual safety frequency cap"
    },
    {
        "field_id": "FIELD-IPM-005-04",
        "document_id": "DOC-IPM-005",
        "source_page_or_section": "Page 1 / Conservative Physical Therapy",
        "field_label": "Supervised Physical Therapy Trial (>= 6 Weeks)",
        "field_meaning": "Documentation of at least 6 weeks of structured physical therapy completed within past 6 months",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Initial Injection Requests",
        "linked_policy_or_rule": "RULE-IPM-CGEPIDURALINJECTIONS-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory prior non-interventional conservative trial"
    },
    {
        "field_id": "FIELD-IPM-005-05",
        "document_id": "DOC-IPM-005",
        "source_page_or_section": "Page 1 / Conservative Medications",
        "field_label": "Prescription NSAID or Neuropathic Medication Trial Details",
        "field_meaning": "Medication agent, daily dosage, and duration of non-steroidal or neuropathic medication trial",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Initial Injection Requests",
        "linked_policy_or_rule": "RULE-IPM-CGEPIDURALINJECTIONS-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Verifies active pharmacologic trial failure or contraindication"
    },
    {
        "field_id": "FIELD-IPM-005-06",
        "document_id": "DOC-IPM-005",
        "source_page_or_section": "Page 2 / Attestation",
        "field_label": "Ordering Clinician Pain Conservative Attestation Signature",
        "field_meaning": "Licensed physician affirmation confirming documented treatment history and chart verification",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Pain Management Intake",
        "linked_policy_or_rule": "RULE-IPM-PREAMBLEIPM-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory signed legal clinical attestation"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-IPM-003",
        "domain": "interventional_pain_management",
        "document_title": "2025 Evolent Clinical Guidelines for Medical Necessity Review: Interventional Pain Management Guidelines",
        "document_type": "governing_policy",
        "version_status": "historical",
        "disposition_status": "HISTORICAL_QUARANTINE",
        "unmapped_reason": "Historical 2025 guideline retained for longitudinal audit comparison only. Active authorizations governed by 2026 guideline.",
        "evidentiary_limitation": "Superseded by 2026 edition; cannot be linked to active decision rules.",
        "human_review_required": False
    },
    {
        "document_id": "DOC-IPM-006",
        "domain": "interventional_pain_management",
        "document_title": "Conservative Treatment History Form: Interventional Pain Management (Rev. 01/11/2024)",
        "document_type": "form",
        "version_status": "historical",
        "disposition_status": "HISTORICAL_QUARANTINE",
        "unmapped_reason": "Historical 2024 conservative treatment form superseded by Rev. July 2025 form (DOC-IPM-005).",
        "evidentiary_limitation": "Superseded intake format; preserved for historical audit only.",
        "human_review_required": False
    },
    {
        "document_id": "DOC-IPM-MISSING-001",
        "domain": "interventional_pain_management",
        "document_title": "State Medicaid Controlled Substance & Injection Frequency Limitations",
        "document_category": "State administrative policy",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PLAN_SPECIFIC_ACCESS_REQUIRED",
        "unmapped_reason": "Individual state Medicaid provider manuals impose hard session caps and co-prescribing limits.",
        "evidentiary_limitation": "Requires state-specific Medicaid fee-for-service / managed care provider manual verification.",
        "human_review_required": True
    }
]
