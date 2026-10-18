"""
Radiation Oncology Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-RAD-003", "CODING_OR_BILLING_REFERENCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-RAD-004", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-RAD-005", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-RAD-006", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-RAD-007", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-RAD-008", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-RAD-009", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-RAD-001",
        "document_id": "DOC-RAD-003",
        "policy_id": "2026 Evolent Radiation Oncology Coding Standards",
        "rule_id": "RULE-RAD-RADCODINGIMRTPLANNING-001",
        "physical_page_or_section": "pp. 1-12 / Section 1-4",
        "relationship_type": "SUPPORTS_CODE_INTERPRETATION",
        "evidence_description": "Establishes coding standards, simulation bundling rules, dosimetry constraints, and daily treatment verification CPT edits.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-RAD-002",
        "document_id": "DOC-RAD-004",
        "policy_id": "ECG 7000",
        "rule_id": "RULE-RAD-ECG7000BREAST-001",
        "physical_page_or_section": "pp. 1-2 / Breast Cancer Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Prior authorization checklist collecting TNM stage, lumpectomy/mastectomy margins, nodal status, receptor status, and hypofractionation eligibility for breast radiation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-RAD-003",
        "document_id": "DOC-RAD-005",
        "policy_id": "ECG 7000",
        "rule_id": "RULE-RAD-ECG7000PROSTATE-001",
        "physical_page_or_section": "pp. 1-2 / Prostate Cancer Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing baseline PSA, Gleason score, clinical T stage, NCCN risk category, and ADT therapy for definitive/adjuvant prostate radiation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-RAD-004",
        "document_id": "DOC-RAD-006",
        "policy_id": "ECG 7000",
        "rule_id": "RULE-RAD-ECG7000LUNG-001",
        "physical_page_or_section": "pp. 1-2 / Lung Cancer Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist collecting histology, TNM stage, pulmonary function (FEV1/DLCO), medically inoperable status, and SBRT eligibility for non-small cell lung cancer.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-RAD-005",
        "document_id": "DOC-RAD-007",
        "policy_id": "ECG 7000 / ECG 7001",
        "rule_id": "RULE-RAD-ECG7000CNSSRS-001",
        "physical_page_or_section": "pp. 1-2 / CNS Primary Cancer Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing brain/spine histology, WHO grade, surgical resection extent, KPS score, and SRS/SRT vs IMRT/Proton beam qualification.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-RAD-006",
        "document_id": "DOC-RAD-008",
        "policy_id": "ECG 7000",
        "rule_id": "RULE-RAD-ECG7000GICOLORECTAL-001",
        "physical_page_or_section": "pp. 1-2 / Colorectal Cancer Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing rectal cancer distance from anal verge, clinical T/N stage, neoadjuvant chemoradiation vs short-course radiation, and surgical plan.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-RAD-007",
        "document_id": "DOC-RAD-009",
        "policy_id": "ECG 7000 / ECG 7001",
        "rule_id": "RULE-RAD-ECG7000HEADNECK-001",
        "physical_page_or_section": "pp. 1-2 / Head & Neck Cancer Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing primary site, HPV/p16 status, nodal involvement, critical organ sparing (parotids, optic chiasm, brainstem), and IMRT medical necessity.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-RAD-004-01",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Patient Identification",
        "field_label": "Member Full Name & Health Plan ID",
        "field_meaning": "Patient identifier for radiation oncology prior authorization",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for member matching and oncology benefit verification"
    },
    {
        "field_id": "FIELD-RAD-004-02",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Treating Physician",
        "field_label": "Radiation Oncologist Name & NPI",
        "field_meaning": "National Provider Identifier of attending radiation oncologist",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates board-certified radiation oncology specialist"
    },
    {
        "field_id": "FIELD-RAD-004-03",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Modality Selection",
        "field_label": "Requested Radiation Modality (3D-CRT / IMRT / SBRT / Proton)",
        "field_meaning": "Target radiation delivery technique and planned billing CPT codes",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Determines applicable guideline technology branch"
    },
    {
        "field_id": "FIELD-RAD-004-04",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Clinical Intent",
        "field_label": "Treatment Intent (Definitive / Adjuvant / Neoadjuvant / Palliative)",
        "field_meaning": "Primary therapeutic objective of requested radiation therapy course",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Directs case to curative vs palliative dose-fractionation schedules"
    },
    {
        "field_id": "FIELD-RAD-004-05",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Histopathology",
        "field_label": "Pathology Biopsy Report & Histologic Subtype",
        "field_meaning": "Definitive histological diagnosis confirming malignancy and grade",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory objective proof of cancer diagnosis"
    },
    {
        "field_id": "FIELD-RAD-004-06",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Cancer Staging",
        "field_label": "AJCC / TNM Clinical and Pathologic Stage",
        "field_meaning": "Tumor size, nodal involvement, and distant metastatic staging classification",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Primary clinical anchor for NCCN/guideline compliance"
    },
    {
        "field_id": "FIELD-RAD-004-07",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Performance Status",
        "field_label": "ECOG Performance Status (0-4) or Karnofsky Score (KPS)",
        "field_meaning": "Standardized functional assessment of cancer patient physical independence",
        "data_type": "numeric",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Threshold evaluation for curative intent vs supportive care"
    },
    {
        "field_id": "FIELD-RAD-004-08",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 2 / Dose Fractionation",
        "field_label": "Planned Total Dose (Gy/cGy) & Number of Fractions",
        "field_meaning": "Prescribed radiation dose to planning target volume and number of daily treatment fractions",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Evaluated against guideline hypofractionation standards"
    },
    {
        "field_id": "FIELD-RAD-004-09",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 2 / Prior Radiation",
        "field_label": "Prior Radiation Therapy to Same / Overlapping Field",
        "field_meaning": "Dates, total dose, and field of prior course; critical for re-irradiation toxicity assessment",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Requires re-irradiation safety audit and normal organ tolerance review"
    },
    {
        "field_id": "FIELD-RAD-004-10",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Breast Pathology",
        "field_label": "Breast Biomarkers (ER, PR, HER2) & Surgical Margins",
        "field_meaning": "Estrogen/progesterone receptor, HER2 status, and negative vs close/positive surgical margins",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Breast Radiation",
        "linked_policy_or_rule": "RULE-RAD-ECG7000BREAST-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Directs boost and regional nodal irradiation criteria"
    },
    {
        "field_id": "FIELD-RAD-005-01",
        "document_id": "DOC-RAD-005",
        "source_page_or_section": "Page 1 / Prostate Risk Group",
        "field_label": "Baseline PSA (ng/mL) & Biopsy Gleason Score",
        "field_meaning": "Pre-treatment PSA concentration and histologic Gleason grade group (1-5)",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Prostate Radiation",
        "linked_policy_or_rule": "RULE-RAD-ECG7000PROSTATE-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Stratifies into low, intermediate, or high NCCN risk category"
    },
    {
        "field_id": "FIELD-RAD-006-01",
        "document_id": "DOC-RAD-006",
        "source_page_or_section": "Page 1 / Pulmonary Function",
        "field_label": "Pulmonary Function Tests (FEV1 and DLCO % Predicted)",
        "field_meaning": "Spirometry values establishing medically inoperable status for thoracic surgery",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Lung Cancer SBRT",
        "linked_policy_or_rule": "RULE-RAD-ECG7000LUNG-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Justifies stereotactic body radiation over surgical lobectomy"
    },
    {
        "field_id": "FIELD-RAD-007-01",
        "document_id": "DOC-RAD-007",
        "source_page_or_section": "Page 1 / Brain Imaging",
        "field_label": "Brain MRI with Contrast (Number & Diameter of Lesions)",
        "field_meaning": "High-resolution brain MRI documenting size, location, and lesion count for SRS/SRT",
        "data_type": "file_attachment",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "CNS Stereotactic Radiosurgery",
        "linked_policy_or_rule": "RULE-RAD-ECG7000CNSSRS-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Lesion count <= 4 or <= 10 threshold for SRS vs whole brain radiotherapy"
    },
    {
        "field_id": "FIELD-RAD-004-11",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 2 / Dosimetric Comparison",
        "field_label": "Comparative 3D vs IMRT/Proton Dosimetric Plan",
        "field_meaning": "Treatment plan comparison demonstrating normal tissue tolerance violation with conventional 3D",
        "data_type": "file_attachment",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Advanced Modality Justification",
        "linked_policy_or_rule": "RULE-RAD-ECG7001PROTON-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory requirement when requesting IMRT or Proton over 3D conformal radiation"
    },
    {
        "field_id": "FIELD-RAD-004-12",
        "document_id": "DOC-RAD-004",
        "source_page_or_section": "Page 1 / Attestation",
        "field_label": "Attending Radiation Oncologist Attestation Signature",
        "field_meaning": "Physician signature confirming clinical necessity and chart concordance",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Radiation Oncology Intake",
        "linked_policy_or_rule": "RULE-RAD-ECG7000STATEMENT-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory clinical legal attestation"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-RAD-MISSING-001",
        "domain": "radiation_oncology",
        "document_title": "Payer-Specific Proton Beam Coverage Threshold Agreements",
        "document_category": "Plan benefit schedule",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PLAN_SPECIFIC_ACCESS_REQUIRED",
        "unmapped_reason": "Specific commercial HMO and Medicare Advantage contracts maintain proprietary proton beam coverage restrictions.",
        "evidentiary_limitation": "Available only to participating oncology networks via secure payer portals.",
        "human_review_required": True
    }
]
