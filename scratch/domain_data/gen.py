"""
Genetic Testing Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-GEN-002", "CODING_OR_BILLING_REFERENCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-GEN-003", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-GEN-004", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-GEN-001",
        "document_id": "DOC-GEN-002",
        "policy_id": "2026 Evolent Genetic Testing Matrix",
        "rule_id": "RULE-GEN-PREAMBLEGEN-001",
        "physical_page_or_section": "pp. 1-14 / Master CPT Matrix",
        "relationship_type": "SUPPORTS_CODE_INTERPRETATION",
        "evidence_description": "Cross-references CPT, PLA, and HCPCS codes against designated clinical guideline policies and authorization requirements.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-GEN-002",
        "document_id": "DOC-GEN-003",
        "policy_id": "2026 Evolent Genetic Testing Guidelines",
        "rule_id": "RULE-GEN-PREAMBLEGEN-001",
        "physical_page_or_section": "pp. 1-2 / Program Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Intake checklist for generic genetic and molecular testing capturing 3-generation pedigree, pre-test counseling, CLIA lab NPI, and actionability.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-GEN-003",
        "document_id": "DOC-GEN-003",
        "policy_id": "2026 Evolent Genetic Testing Guidelines",
        "rule_id": "RULE-GEN-CGGENHBOCBRCA-001",
        "physical_page_or_section": "Page 1 / Hereditary Cancer",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing personal/family history of early-onset breast cancer (<50), ovarian cancer, pancreatic cancer, or male breast cancer for BRCA testing.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-GEN-004",
        "document_id": "DOC-GEN-003",
        "policy_id": "2026 Evolent Genetic Testing Guidelines",
        "rule_id": "RULE-GEN-CGGENEXOMEWES-001",
        "physical_page_or_section": "Page 2 / Whole Exome Sequencing",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing unexplained developmental delay, congenital anomalies, and geneticist consultation required for Whole Exome Sequencing (WES).",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-GEN-005",
        "document_id": "DOC-GEN-004",
        "policy_id": "2026 Evolent Genetic Testing Guidelines",
        "rule_id": "RULE-GEN-CGBREASTPROGNOSTIC-002",
        "physical_page_or_section": "pp. 1-55 / Solid Tumor Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Comprehensive oncology molecular checklist capturing tumor stage, histology, hormone receptor status, and gene expression profiling criteria.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-GEN-006",
        "document_id": "DOC-GEN-004",
        "policy_id": "2026 Evolent Genetic Testing Guidelines",
        "rule_id": "RULE-GEN-CGGENLYNCHSYNDROME-001",
        "physical_page_or_section": "pp. 12-18 / Colorectal & MMR Biomarkers",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Captures MSI/MMR immunohistochemistry and BRAF/KRAS somatic tumor testing directing germline Lynch syndrome testing.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-GEN-003-01",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Patient Identification",
        "field_label": "Member Full Name & Health Plan ID",
        "field_meaning": "Patient identifier for genetic testing prior authorization lookup",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Genetic Testing Intake",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for member matching and benefit plan lookup"
    },
    {
        "field_id": "FIELD-GEN-003-02",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Ordering Clinician",
        "field_label": "Ordering Clinician Name, Specialty & NPI",
        "field_meaning": "National Provider Identifier of ordering geneticist, oncologist, or physician",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Genetic Testing Intake",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates licensed ordering physician credentials"
    },
    {
        "field_id": "FIELD-GEN-003-03",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Laboratory Details",
        "field_label": "Performing CLIA-Certified Testing Laboratory NPI & Legal Name",
        "field_meaning": "Laboratory performing the genetic assay, including CLIA certificate number",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Genetic Testing Intake",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates in-network CLIA-accredited testing facility"
    },
    {
        "field_id": "FIELD-GEN-003-04",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Test Identification",
        "field_label": "Requested CPT / PLA Code & Proprietary Test / Panel Name",
        "field_meaning": "CPT code (e.g. 81211, 81519, 81415) and proprietary test name (e.g. Oncotype DX Breast, FoundationOne)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Genetic Testing Intake",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Selects corresponding specific clinical criteria algorithm"
    },
    {
        "field_id": "FIELD-GEN-003-05",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Clinical Records",
        "field_label": "Detailed Clinical Notes & 3-Generation Family Pedigree",
        "field_meaning": "Office notes detailing affected family relatives, ages at cancer diagnosis, and maternal/paternal lineage",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Hereditary Cancer / Germline Intake",
        "linked_policy_or_rule": "RULE-GEN-CGGENHBOCBRCA-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory objective pedigree documentation"
    },
    {
        "field_id": "FIELD-GEN-003-06",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Genetic Counseling",
        "field_label": "Pre-Test Genetic Counseling Documentation",
        "field_meaning": "Documented face-to-face or telehealth genetic counseling by a Certified Genetic Counselor (CGC) or qualified provider",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Hereditary / Predictive Testing",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Required counseling prerequisite prior to specimen submission"
    },
    {
        "field_id": "FIELD-GEN-003-07",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Clinical Actionability",
        "field_label": "Documented Clinical Actionability / Impact on Medical Management",
        "field_meaning": "Explicit plan detailing how test results directly determine chemotherapy, targeted biologic, prophylactic surgery, or surveillance",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Genetic Testing Intake",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory medical necessity requirement; purely informational testing is excluded"
    },
    {
        "field_id": "FIELD-GEN-004-01",
        "document_id": "DOC-GEN-004",
        "source_page_or_section": "Page 1 / Oncology Staging",
        "field_label": "Tumor Histology & AJCC Pathologic Stage",
        "field_meaning": "Surgical pathology report documenting tumor type, size, nodal status, and histologic grade",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Somatic Tumor Testing",
        "linked_policy_or_rule": "RULE-GEN-CGBREASTPROGNOSTIC-002",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Prerequisite for tumor molecular profiling eligibility"
    },
    {
        "field_id": "FIELD-GEN-004-02",
        "document_id": "DOC-GEN-004",
        "source_page_or_section": "Page 2 / Biomarker Status",
        "field_label": "Hormone Receptor (ER/PR) & HER2 Status",
        "field_meaning": "Immunohistochemical quantification of estrogen receptor, progesterone receptor, and HER2/neu amplification",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Breast Cancer Gene Expression",
        "linked_policy_or_rule": "RULE-GEN-CGBREASTPROGNOSTIC-002",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Required ER+/HER2- status for Oncotype DX / Mammaprint eligibility"
    },
    {
        "field_id": "FIELD-GEN-004-03",
        "document_id": "DOC-GEN-004",
        "source_page_or_section": "Page 3 / Specimen Integrity",
        "field_label": "Specimen Type & Tumor Cellularity Percentage",
        "field_meaning": "FFPE tissue block with verified viable tumor percentage (>= 20-30% cellularity required for NGS)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Somatic Tumor Profiling",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Technical adequacy standard for next-generation sequencing assays"
    },
    {
        "field_id": "FIELD-GEN-003-08",
        "document_id": "DOC-GEN-003",
        "source_page_or_section": "Page 1 / Attestation",
        "field_label": "Ordering Clinician Genetic Attestation Signature",
        "field_meaning": "Ordering provider legal affirmation confirming necessity and documented medical chart verification",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Genetic Testing Intake",
        "linked_policy_or_rule": "RULE-GEN-PREAMBLEGEN-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory signed legal attestation"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-GEN-MISSING-001",
        "domain": "genetic_testing",
        "document_title": "Payer-Specific Non-Covered Genetic Panel Exclusion Lists",
        "document_category": "Plan benefit exclusion schedule",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PLAN_SPECIFIC_ACCESS_REQUIRED",
        "unmapped_reason": "Proprietary commercial insurer fee schedules exclude specific expanded carrier panels (>500 genes) or direct-to-consumer tests.",
        "evidentiary_limitation": "Restricted commercial payer schedule requiring individual plan contract verification.",
        "human_review_required": True
    }
]
