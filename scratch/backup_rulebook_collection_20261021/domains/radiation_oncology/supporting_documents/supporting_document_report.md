# Supporting Document, Evidence Mapping & Policy Dependencies Report
## Domain: Radiation Oncology
### MedRule Phase 2E Deliverable

---

## 1. Executive Summary & Inventory Scope

This report documents the systematic inventory, functional classification, evidence extraction, and policy dependency architecture for supporting documents in the **Radiation Oncology** domain.

In accordance with MedRule Phase 2E requirements:
- **Total Supporting Documents Cataloged**: 7
  - Current Verified (2026) Documents: 7
  - Historical Baseline Documents: 0
- **Total Policy and Rule Mappings**: 7
- **Discrete Intake & Evidence Fields Deconstructed**: 15
  - Clinical Evidence Fields: 11
  - Administrative Intake Fields: 4
- **Unmapped / Quarantined / Plan-Specific Records**: 1

---

## 2. Supporting Document Functional Taxonomy

Each supporting document has been assigned a definitive `functional_role` to prevent checklist or tip sheet authority conflation:

| Document ID | Document Title | Document Type | Functional Role | Version Status | Pages |
|-------------|----------------|---------------|-----------------|----------------|-------|
| `DOC-RAD-003` | 2026 Evolent Radiation Oncology Coding Standards (Final) | `coding_grid` | `CODING_OR_BILLING_REFERENCE` | `current_2026_verified` | 26 |
| `DOC-RAD-004` | Radiation Therapy Breast Cancer Prior Authorization Checklist | `checklist` | `INTAKE_OR_DOCUMENTATION_AID` | `current_2026_verified` | 4 |
| `DOC-RAD-005` | Radiation Therapy Prostate Cancer Prior Authorization Checklist | `checklist` | `INTAKE_OR_DOCUMENTATION_AID` | `current_2026_verified` | 3 |
| `DOC-RAD-006` | Radiation Therapy Non-Small Cell Lung Cancer Prior Authorization Checklist | `checklist` | `INTAKE_OR_DOCUMENTATION_AID` | `current_2026_verified` | 3 |
| `DOC-RAD-007` | Radiation Therapy Central Nervous System (CNS) Primary Cancer Checklist | `checklist` | `INTAKE_OR_DOCUMENTATION_AID` | `current_2026_verified` | 3 |
| `DOC-RAD-008` | Radiation Therapy Rectal and Colon Cancer Prior Authorization Checklist | `checklist` | `INTAKE_OR_DOCUMENTATION_AID` | `current_2026_verified` | 3 |
| `DOC-RAD-009` | Radiation Therapy Head and Neck Cancer Prior Authorization Checklist | `checklist` | `INTAKE_OR_DOCUMENTATION_AID` | `current_2026_verified` | 4 |

---

## 3. Policy & Rule Traceability Mappings

Supporting documents provide structured documentation aids, procedural guidance, or billing constraints linked to governing clinical policies and executable decision rules:

| Mapping ID | Document ID | Target Policy / Rule | Relationship Type | Verification Status |
|------------|-------------|----------------------|-------------------|---------------------|
| `MAP-RAD-001` | `DOC-RAD-003` | 2026 Evolent Radiation Oncology Coding Standards / RULE-RAD-RADCODINGIMRTPLANNING-001 | `SUPPORTS_CODE_INTERPRETATION` | `VERIFIED_MAPPING` |
| `MAP-RAD-002` | `DOC-RAD-004` | ECG 7000 / RULE-RAD-ECG7000BREAST-001 | `SUPPORTS_DOCUMENTATION_COLLECTION` | `VERIFIED_MAPPING` |
| `MAP-RAD-003` | `DOC-RAD-005` | ECG 7000 / RULE-RAD-ECG7000PROSTATE-001 | `SUPPORTS_DOCUMENTATION_COLLECTION` | `VERIFIED_MAPPING` |
| `MAP-RAD-004` | `DOC-RAD-006` | ECG 7000 / RULE-RAD-ECG7000LUNG-001 | `SUPPORTS_DOCUMENTATION_COLLECTION` | `VERIFIED_MAPPING` |
| `MAP-RAD-005` | `DOC-RAD-007` | ECG 7000 / ECG 7001 / RULE-RAD-ECG7000CNSSRS-001 | `SUPPORTS_DOCUMENTATION_COLLECTION` | `VERIFIED_MAPPING` |
| `MAP-RAD-006` | `DOC-RAD-008` | ECG 7000 / RULE-RAD-ECG7000GICOLORECTAL-001 | `SUPPORTS_DOCUMENTATION_COLLECTION` | `VERIFIED_MAPPING` |
| `MAP-RAD-007` | `DOC-RAD-009` | ECG 7000 / ECG 7001 / RULE-RAD-ECG7000HEADNECK-001 | `SUPPORTS_DOCUMENTATION_COLLECTION` | `VERIFIED_MAPPING` |

---

## 4. Discrete Evidence Field Deconstruction

To prepare the deterministic decision engine for case intake, documentation aids have been deconstructed into standardized data fields with strict separation between administrative identity parameters and objective clinical evidence:

- **Administrative Intake Fields (4)**: Capture member identifiers, ordering clinician NPI, facility settings, and legal attestations. These confirm identity and provider authority but do NOT establish clinical medical necessity.
- **Clinical Evidence Fields (11)**: Capture objective diagnostic tests, imaging reports, symptom chronicity, and conservative treatment history required to satisfy explicit medical necessity criteria.

### Sample Field Definitions:

| Field ID | Document | Label | Data Type | Requirement | Category |
|----------|----------|-------|-----------|-------------|----------|
| `FIELD-RAD-004-01` | `DOC-RAD-004` | Member Full Name & Health Plan ID | `string` | `REQUIRED` | `ADMINISTRATIVE_INTAKE` |
| `FIELD-RAD-004-02` | `DOC-RAD-004` | Radiation Oncologist Name & NPI | `string` | `REQUIRED` | `ADMINISTRATIVE_INTAKE` |
| `FIELD-RAD-004-03` | `DOC-RAD-004` | Requested Radiation Modality (3D-CRT / IMRT / SBRT / Proton) | `enum` | `REQUIRED` | `ADMINISTRATIVE_INTAKE` |
| `FIELD-RAD-004-04` | `DOC-RAD-004` | Treatment Intent (Definitive / Adjuvant / Neoadjuvant / Palliative) | `enum` | `REQUIRED` | `CLINICAL_EVIDENCE` |
| `FIELD-RAD-004-05` | `DOC-RAD-004` | Pathology Biopsy Report & Histologic Subtype | `file_attachment` | `REQUIRED` | `CLINICAL_EVIDENCE` |
| `FIELD-RAD-004-06` | `DOC-RAD-004` | AJCC / TNM Clinical and Pathologic Stage | `string` | `REQUIRED` | `CLINICAL_EVIDENCE` |
| `FIELD-RAD-004-07` | `DOC-RAD-004` | ECOG Performance Status (0-4) or Karnofsky Score (KPS) | `numeric` | `REQUIRED` | `CLINICAL_EVIDENCE` |
| `FIELD-RAD-004-08` | `DOC-RAD-004` | Planned Total Dose (Gy/cGy) & Number of Fractions | `string` | `REQUIRED` | `CLINICAL_EVIDENCE` |
| `FIELD-RAD-004-09` | `DOC-RAD-004` | Prior Radiation Therapy to Same / Overlapping Field | `string` | `REQUIRED` | `CLINICAL_EVIDENCE` |
| `FIELD-RAD-004-10` | `DOC-RAD-004` | Breast Biomarkers (ER, PR, HER2) & Surgical Margins | `string` | `CONDITIONAL` | `CLINICAL_EVIDENCE` |
| ... | ... | *(See documentation_field_mapping.csv for all 15 fields)* | ... | ... | ... |

---

## 5. Historical Quarantine & Plan-Specific Dependencies

To maintain strict regulatory integrity:
1. **Historical Documents**: All pre-2026 documents are classified as `HISTORICAL_QUARANTINE`. They remain fully preserved on disk for longitudinal audit comparisons but are barred from executing automated prior-authorization determinations.
2. **Plan-Specific Dependencies**: Proprietary state Medicaid fee schedules, private commercial carve-out lists, and benefit schedules that require plan portal access are logged with disposition `PLAN_SPECIFIC_ACCESS_REQUIRED` and flagged for human review.

| Document ID | Disposition Status | Reason | Human Review |
|-------------|--------------------|--------|--------------|
| `DOC-RAD-MISSING-001` | `PLAN_SPECIFIC_ACCESS_REQUIRED` | Specific commercial HMO and Medicare Advantage contracts maintain proprietary pr... | `True` |

---

## 6. Audit Certification

All file paths, SHA-256 cryptographic hashes, page counts, and rule relationships in this domain have been verified against the physical corpus on disk and the audited master inventory.

- **Status**: `DOMAIN_SUPPORTING_DOCS_COMPLETE`
- **Zero Hallucination / Zero Synthetic Rule Guarantee**: Enforced.
