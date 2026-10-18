"""
Musculoskeletal Surgery Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-MSK-002", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-003", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-004", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-005", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-006", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-007", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-008", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-009", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-010", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-MSK-011", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-MSK-001",
        "document_id": "DOC-MSK-002",
        "policy_id": "EPOS 1773",
        "rule_id": "RULE-MSK-EPOS1773-001",
        "physical_page_or_section": "pp. 1-8 / Section I-III",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Establishes clinical exception criteria directing joint arthroplasty and outpatient spine surgery to ambulatory surgery centers (ASC) unless hospital admission criteria are met.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-002",
        "document_id": "DOC-MSK-003",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "physical_page_or_section": "pp. 1-2 / Required Documentation",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Intake checklist for hip, knee, and shoulder surgery collecting weight-bearing radiographs, conservative therapy duration, injections, and functional limitation.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-003",
        "document_id": "DOC-MSK-004",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-CGCERVICALLUMBAR-002",
        "physical_page_or_section": "pp. 1-2 / Spine Surgery Checklist",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Intake checklist for cervical and lumbar spine surgery collecting MRI/CT evidence, concordant neurologic deficit exam findings, and conservative therapy history.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-004",
        "document_id": "DOC-MSK-005",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-CGCERVICALLUMBAR-002",
        "physical_page_or_section": "pp. 1-2 / Spine Conservative Form",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Standardized clinical form capturing >= 6 weeks of active physical therapy, medication trials, epidural steroid injections, and provider attestation for spine surgery.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-005",
        "document_id": "DOC-MSK-006",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "physical_page_or_section": "pp. 1-2 / Major Joints Conservative Form",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Standardized clinical form capturing >= 12 weeks of non-operative therapy, home exercise, assistive devices, NSAID trials, and joint injections for arthroplasty.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-006",
        "document_id": "DOC-MSK-007",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "physical_page_or_section": "pp. 1-2 / Commercial Arthroplasty Guidance",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Clinical tip sheet detailing commercial health plan medical necessity requirements for total hip and total knee arthroplasty, including Kellgren-Lawrence Grade III/IV.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-007",
        "document_id": "DOC-MSK-008",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "physical_page_or_section": "pp. 1-2 / Medicare Arthroplasty Guidance",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Clinical tip sheet aligning Medicare Advantage arthroplasty criteria with CMS Local Coverage Determinations (LCDs) and national clinical benchmarks.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-008",
        "document_id": "DOC-MSK-009",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-PREAMBLEMSK-001",
        "physical_page_or_section": "pp. 1-2 / Knee Arthroscopy Guidance",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Tip sheet establishing indications for therapeutic knee arthroscopy (meniscectomy, loose body removal) and non-coverage of arthroscopy for uncomplicated osteoarthritis.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-009",
        "document_id": "DOC-MSK-010",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "physical_page_or_section": "pp. 1-2 / Shoulder Arthroplasty Guidance",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Tip sheet outlining anatomic vs reverse total shoulder arthroplasty indications, rotator cuff tear arthropathy criteria, and imaging benchmarks.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-MSK-010",
        "document_id": "DOC-MSK-011",
        "policy_id": "2026 Evolent Musculoskeletal Surgery Guidelines",
        "rule_id": "RULE-MSK-PREAMBLEMSK-001",
        "physical_page_or_section": "pp. 1-2 / Shoulder Arthroscopy Guidance",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Tip sheet summarizing rotator cuff repair, labral repair, and subacromial decompression indications and prior conservative treatment standards.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-MSK-003-01",
        "document_id": "DOC-MSK-003",
        "source_page_or_section": "Page 1 / Patient Identification",
        "field_label": "Member Full Name & Health Plan ID",
        "field_meaning": "Patient identifier for musculoskeletal surgical authorization",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Joint Surgery Intake",
        "linked_policy_or_rule": "RULE-MSK-PREAMBLEMSK-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for member matching and benefit plan verification"
    },
    {
        "field_id": "FIELD-MSK-003-02",
        "document_id": "DOC-MSK-003",
        "source_page_or_section": "Page 1 / Surgeon & Facility",
        "field_label": "Requesting Surgeon Name & NPI",
        "field_meaning": "National Provider Identifier of operating orthopedic surgeon",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Joint Surgery Intake",
        "linked_policy_or_rule": "RULE-MSK-PREAMBLEMSK-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates licensed orthopedic surgeon"
    },
    {
        "field_id": "FIELD-MSK-003-03",
        "document_id": "DOC-MSK-003",
        "source_page_or_section": "Page 1 / Facility Setting",
        "field_label": "Place of Service Setting (ASC vs Outpatient Hospital)",
        "field_meaning": "Surgical facility setting for Place of Service EPOS 1773 evaluation",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Joint Surgery Intake",
        "linked_policy_or_rule": "RULE-MSK-EPOS1773-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Determines whether hospital outpatient setting is clinically justified"
    },
    {
        "field_id": "FIELD-MSK-003-04",
        "document_id": "DOC-MSK-003",
        "source_page_or_section": "Page 1 / Procedure Scope",
        "field_label": "Proposed Surgical Procedure CPT Code(s)",
        "field_meaning": "Requested surgical CPT codes (e.g., 27447 TKA, 27130 THA, 23472 TSA)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Joint Surgery Intake",
        "linked_policy_or_rule": "RULE-MSK-PREAMBLEMSK-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Triggers joint-specific surgical policy criteria"
    },
    {
        "field_id": "FIELD-MSK-003-05",
        "document_id": "DOC-MSK-003",
        "source_page_or_section": "Page 1 / Clinical Records",
        "field_label": "Orthopedic Surgical Consultation Progress Notes",
        "field_meaning": "Detailed office visit notes by operating surgeon documenting physical examination",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Joint Surgery Intake",
        "linked_policy_or_rule": "RULE-MSK-PREAMBLEMSK-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory objective record of examination findings"
    },
    {
        "field_id": "FIELD-MSK-003-06",
        "document_id": "DOC-MSK-003",
        "source_page_or_section": "Page 1 / Diagnostic Imaging",
        "field_label": "Weight-Bearing Radiograph Reports & Radiographic Grade",
        "field_meaning": "Standing plain radiographs demonstrating joint space narrowing, subchondral sclerosis, osteophytes (Kellgren-Lawrence Grade 3-4)",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Hip & Knee Arthroplasty",
        "linked_policy_or_rule": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Objective structural evidence of severe end-stage osteoarthritis"
    },
    {
        "field_id": "FIELD-MSK-003-07",
        "document_id": "DOC-MSK-003",
        "source_page_or_section": "Page 1 / Clinical Chronicity",
        "field_label": "Joint Symptom Chronicity >= 3 Months",
        "field_meaning": "Pain and functional limitation persistent for at least 3 consecutive months",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Hip & Knee Arthroplasty",
        "linked_policy_or_rule": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory chronic symptom duration benchmark"
    },
    {
        "field_id": "FIELD-MSK-004-01",
        "document_id": "DOC-MSK-004",
        "source_page_or_section": "Page 1 / Spine Exam",
        "field_label": "Neurological Deficit Physical Exam Concordance",
        "field_meaning": "Objective motor weakness, sensory deficit, or reflex depression correlating to spinal root level",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Spine Decompression / Fusion",
        "linked_policy_or_rule": "RULE-MSK-CGCERVICALLUMBAR-002",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Physical exam must correlate with radiographic imaging nerve root compression"
    },
    {
        "field_id": "FIELD-MSK-004-02",
        "document_id": "DOC-MSK-004",
        "source_page_or_section": "Page 1 / Spine Imaging",
        "field_label": "Spine MRI or CT Within Past 12 Months",
        "field_meaning": "High-resolution cross-sectional imaging demonstrating spinal canal stenosis or neural foraminal impingement",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Spine Decompression / Fusion",
        "linked_policy_or_rule": "RULE-MSK-CGCERVICALLUMBAR-002",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Objective anatomical proof of compression"
    },
    {
        "field_id": "FIELD-MSK-004-03",
        "document_id": "DOC-MSK-004",
        "source_page_or_section": "Page 2 / Red Flags",
        "field_label": "Cauda Equina Syndrome or Rapidly Progressive Deficit Present",
        "field_meaning": "Bowel/bladder dysfunction, saddle anesthesia, or foot drop qualifying for urgent surgical decompression",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Urgent Spine Surgery",
        "linked_policy_or_rule": "RULE-MSK-CGCERVICALLUMBAR-002",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Emergency exception bypassing conservative therapy requirements"
    },
    {
        "field_id": "FIELD-MSK-005-01",
        "document_id": "DOC-MSK-005",
        "source_page_or_section": "Page 1 / Spine Physical Therapy",
        "field_label": "Supervised Physical Therapy Trial (>= 6 Consecutive Weeks)",
        "field_meaning": "Completion of formal supervised physical therapy within preceding 6 months",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Elective Spine Surgery",
        "linked_policy_or_rule": "RULE-MSK-CGCERVICALLUMBAR-002",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Prerequisite non-operative rehabilitation trial"
    },
    {
        "field_id": "FIELD-MSK-005-02",
        "document_id": "DOC-MSK-005",
        "source_page_or_section": "Page 1 / Spine Medication",
        "field_label": "Prescription NSAID or Non-Opioid Analgesic Trial Details",
        "field_meaning": "Medication name, dosage, and duration of anti-inflammatory or neuropathic trial",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Elective Spine Surgery",
        "linked_policy_or_rule": "RULE-MSK-CGCERVICALLUMBAR-002",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Pharmacologic conservative treatment verification"
    },
    {
        "field_id": "FIELD-MSK-005-03",
        "document_id": "DOC-MSK-005",
        "source_page_or_section": "Page 2 / Attestation",
        "field_label": "Surgeon Spine Conservative Attestation Signature",
        "field_meaning": "Operating surgeon affirmation of documented conservative treatment failure",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Elective Spine Surgery",
        "linked_policy_or_rule": "RULE-MSK-PREAMBLEMSK-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory signed legal attestation"
    },
    {
        "field_id": "FIELD-MSK-006-01",
        "document_id": "DOC-MSK-006",
        "source_page_or_section": "Page 1 / Joint Injections",
        "field_label": "Intra-Articular Joint Injection History",
        "field_meaning": "Corticosteroid or viscosupplementation injection dates, joint injected, and percentage/duration of relief",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Joint Arthroplasty",
        "linked_policy_or_rule": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Documentation of interventional conservative trial"
    },
    {
        "field_id": "FIELD-MSK-006-02",
        "document_id": "DOC-MSK-006",
        "source_page_or_section": "Page 1 / Assistive Devices",
        "field_label": "Trial of Assistive Ambulation Device (Cane/Walker)",
        "field_meaning": "Use of cane, crutch, or walker to unload arthritic joint during ambulation",
        "data_type": "boolean",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Hip & Knee Arthroplasty",
        "linked_policy_or_rule": "RULE-MSK-CGKNEEARTHROPLASTY-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Component of comprehensive non-operative management"
    },
    {
        "field_id": "FIELD-MSK-006-03",
        "document_id": "DOC-MSK-006",
        "source_page_or_section": "Page 2 / Attestation",
        "field_label": "Surgeon Joint Conservative Attestation Signature",
        "field_meaning": "Surgeon affirmation of documented joint conservative treatment failure",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Joint Arthroplasty",
        "linked_policy_or_rule": "RULE-MSK-PREAMBLEMSK-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory signed legal attestation"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-MSK-MISSING-001",
        "domain": "musculoskeletal_surgery",
        "document_title": "Payer-Specific Inpatient Only Surgical Procedure Carve-Out List",
        "document_category": "Place of service schedule",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PUBLIC_ANNUAL_FEE_SCHEDULE",
        "unmapped_reason": "Annual CMS Inpatient Only (IPO) schedule and commercial payer bulletins dictate mandatory inpatient stay criteria.",
        "evidentiary_limitation": "External annual regulatory fee schedule; informs place of service routing rather than clinical necessity.",
        "human_review_required": True
    }
]
