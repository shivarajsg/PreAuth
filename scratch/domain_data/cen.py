"""
Centene DME, Orthotics and Prosthetics Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-CEN-002", "HISTORICAL_DOCUMENT_COMPARISON", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-003", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-004", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-005", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-006", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-007", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-008", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-009", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-010", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-011", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-012", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
    ("DOC-CEN-013", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-CEN-001",
        "document_id": "DOC-CEN-002",
        "policy_id": "CP.MP.107 (Rev. 11/24)",
        "rule_id": "",
        "physical_page_or_section": "pp. 1-21 / Entire Policy",
        "relationship_type": "HISTORICAL_COMPARISON_ONLY",
        "evidence_description": "Historical 2024 revision baseline preserved for longitudinal audit comparison; quarantined from active 2026 rule execution.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "Historical document; cannot govern 2026 authorizations"
    },
    {
        "mapping_id": "MAP-CEN-002",
        "document_id": "DOC-CEN-003",
        "policy_id": "CP.MP.48",
        "rule_id": "RULE-DME-048-001",
        "physical_page_or_section": "pp. 1-6 / Clinical Criteria",
        "relationship_type": "REFERENCES_GOVERNING_POLICY",
        "evidence_description": "Governs neuromuscular electrical stimulation (NMES) and functional electrical stimulation (FES) for upper/lower motor neuron rehabilitation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-003",
        "document_id": "DOC-CEN-004",
        "policy_id": "CP.MP.99",
        "rule_id": "RULE-DME-099-001",
        "physical_page_or_section": "pp. 1-12 / Seating Criteria",
        "relationship_type": "REFERENCES_GOVERNING_POLICY",
        "evidence_description": "Governs specialized wheelchair seating, tilt-in-space, dynamic recline, and custom contoured cushions based on specialty PT/OT seating evaluation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-004",
        "document_id": "DOC-CEN-005",
        "policy_id": "CP.MP.173",
        "rule_id": "RULE-DME-173-001",
        "physical_page_or_section": "pp. 1-10 / Section I-II",
        "relationship_type": "REFERENCES_GOVERNING_POLICY",
        "evidence_description": "Governs permanent implantable intrathecal or epidural pain pumps for chronic intractable malignant or non-malignant pain following successful preliminary opioid trial.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-005",
        "document_id": "DOC-CEN-006",
        "policy_id": "CP.MP.184",
        "rule_id": "RULE-DME-184-001",
        "physical_page_or_section": "pp. 1-10 / Ventilator Criteria",
        "relationship_type": "REFERENCES_GOVERNING_POLICY",
        "evidence_description": "Governs invasive and non-invasive mechanical home ventilators (HCPCS E0465, E0466) for chronic respiratory failure, neuromuscular disorders, and severe COPD.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-006",
        "document_id": "DOC-CEN-007",
        "policy_id": "CP.MP.185",
        "rule_id": "RULE-DME-185-001",
        "physical_page_or_section": "pp. 1-16 / Tissue Substitute Criteria",
        "relationship_type": "REFERENCES_GOVERNING_POLICY",
        "evidence_description": "Governs bioengineered skin and soft tissue substitutes for chronic non-healing diabetic foot ulcers and venous stasis ulcers failing >= 4 weeks standard care.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-007",
        "document_id": "DOC-CEN-008",
        "policy_id": "CP.MP.203",
        "rule_id": "RULE-DME-203-001",
        "physical_page_or_section": "pp. 1-6 / Phrenic Nerve Criteria",
        "relationship_type": "REFERENCES_GOVERNING_POLICY",
        "evidence_description": "Governs diaphragmatic pacing and phrenic nerve stimulation systems for high cervical spinal cord injury and congenital central hypoventilation syndrome.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-008",
        "document_id": "DOC-CEN-009",
        "policy_id": "CP.MP.243",
        "rule_id": "RULE-DME-243-001",
        "physical_page_or_section": "pp. 1-8 / ILR Criteria",
        "relationship_type": "REFERENCES_GOVERNING_POLICY",
        "evidence_description": "Governs insertable cardiac monitors / implantable loop recorders for recurrent unexplained syncope, cryptogenic stroke, and suspected occult atrial fibrillation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-009",
        "document_id": "DOC-CEN-010",
        "policy_id": "CP.MP.107",
        "rule_id": "RULE-DME-107-001",
        "physical_page_or_section": "pp. 1-120 / Chapter 20",
        "relationship_type": "REFERENCES_EXTERNAL_AUTHORITY",
        "evidence_description": "CMS Claims Processing Manual Chapter 20 establishes billing, certificate of medical necessity (CMN), rental-to-purchase rules, and warranty standards.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-010",
        "document_id": "DOC-CEN-011",
        "policy_id": "CP.MP.107",
        "rule_id": "RULE-DME-107-001",
        "physical_page_or_section": "pp. 1-616 / Appendix A",
        "relationship_type": "REFERENCES_EXTERNAL_AUTHORITY",
        "evidence_description": "CMS State Operations Manual establishes hospital discharge planning standards, inpatient vs home DME delivery rules, and transfer requirements.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-011",
        "document_id": "DOC-CEN-012",
        "policy_id": "CP.MP.99",
        "rule_id": "RULE-DME-099-001",
        "physical_page_or_section": "pp. 1-39 / RESNA Position",
        "relationship_type": "REFERENCES_EXTERNAL_AUTHORITY",
        "evidence_description": "RESNA Position Paper establishes evidence-based clinical indications for power seat elevation devices to facilitate transfers and reach in wheelchair users.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-CEN-012",
        "document_id": "DOC-CEN-013",
        "policy_id": "CP.MP.107",
        "rule_id": "RULE-DME-107-001",
        "physical_page_or_section": "pp. 1-19 / Quality Standards",
        "relationship_type": "REFERENCES_EXTERNAL_AUTHORITY",
        "evidence_description": "CMS DMEPOS Quality Standards mandate supplier accreditation, product delivery confirmation, patient equipment training, and 24/7 emergency service.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-CEN-107-01",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Intake Standards",
        "field_label": "Member Full Name & Medicaid/Medicare ID",
        "field_meaning": "Patient identifier for Centene DMEPOS authorization and benefit eligibility lookup",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All DMEPOS Intake",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for member matching and state benefit lookup"
    },
    {
        "field_id": "FIELD-CEN-107-02",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Prescribing Clinician",
        "field_label": "Ordering Clinician Name, NPI & Signed Order (WOPD)",
        "field_meaning": "Written Order Prior to Delivery (WOPD) signed and dated by treating physician",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All DMEPOS Intake",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory regulatory prerequisite before equipment delivery"
    },
    {
        "field_id": "FIELD-CEN-107-03",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Supplier Accreditation",
        "field_label": "DMEPOS Supplier Name, NPI & CMS Accreditation Status",
        "field_meaning": "Supplying entity meeting CMS Quality Standards and enrolled with state plan",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All DMEPOS Intake",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates accredited supplier status"
    },
    {
        "field_id": "FIELD-CEN-107-04",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Item Specification",
        "field_label": "Requested HCPCS Item Code, Make, Model & Purchase/Rental Status",
        "field_meaning": "Standard HCPCS code (e.g. E0465, E0483, K0823, E0260) and manufacturer details",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All DMEPOS Intake",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Identifies target medical equipment item"
    },
    {
        "field_id": "FIELD-CEN-107-05",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Face-to-Face Visit",
        "field_label": "Face-to-Face Clinical Evaluation Within Past 6 Months",
        "field_meaning": "Recent physician clinical examination directly addressing functional limitation justifying DME",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All DMEPOS Intake",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Federal statutory requirement for power mobility and respiratory DME"
    },
    {
        "field_id": "FIELD-CEN-107-06",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Medical Necessity",
        "field_label": "Primary ICD-10 Medical Diagnosis Justifying DME Necessity",
        "field_meaning": "Specific chronic underlying disease, disability, or injury necessitating equipment",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All DMEPOS Intake",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Primary clinical indication anchor"
    },
    {
        "field_id": "FIELD-CEN-107-07",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Environmental Safety",
        "field_label": "Home Assessment Report (Doorway Width, Ramps, Electrical)",
        "field_meaning": "Verification that patient's residence can accommodate and safely operate requested equipment",
        "data_type": "file_attachment",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Mobility & Respiratory Equipment",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory for power wheelchairs and mechanical ventilators"
    },
    {
        "field_id": "FIELD-CEN-099-01",
        "document_id": "DOC-CEN-004",
        "source_page_or_section": "pp. 1-4 / PT/OT Seating Eval",
        "field_label": "Licensed PT/OT Specialty Wheelchair Seating Evaluation Report",
        "field_meaning": "Specialized assessment of postural alignment, skin integrity, transfer ability, and custom seating need",
        "data_type": "file_attachment",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Complex Rehab Mobility (Group 3/4 PWC)",
        "linked_policy_or_rule": "RULE-DME-099-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory independent seating evaluation requirement"
    },
    {
        "field_id": "FIELD-CEN-184-01",
        "document_id": "DOC-CEN-006",
        "source_page_or_section": "pp. 1-4 / Respiratory Lab Data",
        "field_label": "Arterial Blood Gas (ABG) PaCO2 >= 45 mmHg or Severe Nocturnal Desaturation",
        "field_meaning": "Laboratory blood gas demonstrating chronic hypercapnic respiratory failure",
        "data_type": "file_attachment",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Home Mechanical Ventilator",
        "linked_policy_or_rule": "RULE-DME-184-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Objective clinical threshold for non-invasive / invasive ventilation"
    },
    {
        "field_id": "FIELD-CEN-173-01",
        "document_id": "DOC-CEN-005",
        "source_page_or_section": "pp. 1-3 / Section I Preliminary Trial",
        "field_label": "Successful Preliminary Trial of Intrathecal/Epidural Opioid (>= 50% Relief)",
        "field_meaning": "Documented trial with temporary catheter demonstrating at least 50% reduction in intractable pain",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Implantable Pain Pumps",
        "linked_policy_or_rule": "RULE-DME-173-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory clinical trial benchmark prior to permanent pump implantation"
    },
    {
        "field_id": "FIELD-CEN-185-01",
        "document_id": "DOC-CEN-007",
        "source_page_or_section": "pp. 1-4 / Wound Documentation",
        "field_label": "Chronic Wound Staging, Surface Area & >= 4-Week Conventional Care Failure",
        "field_meaning": "Wound measurements (length x width x depth), exudate, and documented failure of standard wound care",
        "data_type": "file_attachment",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Skin & Soft Tissue Substitutes",
        "linked_policy_or_rule": "RULE-DME-185-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Prerequisite standard ulcer therapy failure threshold"
    },
    {
        "field_id": "FIELD-CEN-107-08",
        "document_id": "DOC-CEN-001",
        "source_page_or_section": "Section II / Attestation",
        "field_label": "Ordering Clinician DME Medical Necessity Attestation Signature",
        "field_meaning": "Physician signature certifying item is medically necessary, non-convenience, and suitable for home use",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All DMEPOS Intake",
        "linked_policy_or_rule": "RULE-DME-107-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory legal medical certification"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-CEN-002",
        "domain": "centene_dme_orthotics_prosthetics",
        "document_title": "Clinical Policy CP.MP.107: Durable Medical Equipment and Orthotics and Prosthetics Guidelines (Rev. 11/24)",
        "document_type": "governing_policy",
        "version_status": "historical",
        "disposition_status": "HISTORICAL_QUARANTINE",
        "unmapped_reason": "Historical November 2024 revision baseline preserved for audit comparison. Current authorizations governed by Rev. 11/25 (DOC-CEN-001).",
        "evidentiary_limitation": "Superseded 2024 policy version; quarantined from active 2026 rule evaluation.",
        "human_review_required": False
    },
    {
        "document_id": "DOC-CEN-MISSING-001",
        "domain": "centene_dme_orthotics_prosthetics",
        "document_title": "Centene State Medicaid Specific DMEPOS Fee Schedules & Quantity Limits",
        "document_category": "State Medicaid contract manual",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PLAN_SPECIFIC_ACCESS_REQUIRED",
        "unmapped_reason": "State-specific fee schedules and quantity limit manuals determine dollar thresholds and replacement intervals.",
        "evidentiary_limitation": "Accessible only via secure state health plan subsidiary provider portals.",
        "human_review_required": True
    }
]
