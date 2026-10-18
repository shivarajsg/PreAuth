"""
Physical Medicine Domain Specification for MedRule Phase 2E.
"""

DOCS = [
    ("DOC-PHY-002", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-003", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-004", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-005", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-006", "SEPARATELY_GOVERNED_POLICY", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-007", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-008", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-009", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-010", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-011", "SUPPLEMENTARY_PROCEDURAL_GUIDANCE", "PUBLIC_ACCESSIBLE"),
    ("DOC-PHY-012", "INTAKE_OR_DOCUMENTATION_AID", "PUBLIC_ACCESSIBLE"),
]

MAPPINGS = [
    {
        "mapping_id": "MAP-PHY-001",
        "document_id": "DOC-PHY-002",
        "policy_id": "2026 Evolent Active Procedures Policy",
        "rule_id": "RULE-PHY-PREAMBLEPHY-001",
        "physical_page_or_section": "pp. 1-6 / Active Interventions",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Defines active physical medicine interventions (therapeutic exercises 97110, neuromuscular re-ed 97112) requiring active patient participation and skilled therapist supervision.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-002",
        "document_id": "DOC-PHY-003",
        "policy_id": "2026 Evolent Passive Treatment Modalities Policy",
        "rule_id": "RULE-PHY-PREAMBLEPHY-001",
        "physical_page_or_section": "pp. 1-5 / Modality Restrictions",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Restricts passive modalities (hot/cold packs, ultrasound, electrical stimulation) to adjunctive role during initial 2-4 weeks; non-covered as standalone maintenance.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-003",
        "document_id": "DOC-PHY-004",
        "policy_id": "2026 Evolent Measurable Progressive Improvement Policy",
        "rule_id": "RULE-PHY-POLICYMEASURABLEIMPROV-001",
        "physical_page_or_section": "pp. 1-4 / Progress Measurement Standards",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Mandates objective, quantifiable improvements in pain, range of motion, muscle strength, or standardized functional scales documented at least every two weeks.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-004",
        "document_id": "DOC-PHY-005",
        "policy_id": "2026 Evolent Outpatient Habilitative PT/OT Policy",
        "rule_id": "RULE-PHY-POLICYHABILITATIVEPTOT-001",
        "physical_page_or_section": "pp. 1-8 / Habilitative Standards",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Governs habilitative therapy for developmental delays, requiring standardized norm-referenced assessment scores (>1.5 SD below mean) establishing skilled need.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-005",
        "document_id": "DOC-PHY-006",
        "policy_id": "2026 Evolent Outpatient Speech Therapy Policy",
        "rule_id": "RULE-PHY-POLICYHABREHABSPEECH-001",
        "physical_page_or_section": "pp. 1-8 / Speech Therapy Criteria",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Establishes clinical criteria for rehabilitative and habilitative speech language pathology, swallowing dysfunction, and cognitive communication therapy.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-006",
        "document_id": "DOC-PHY-007",
        "policy_id": "2026 Evolent DME in Physical Medicine Policy",
        "rule_id": "RULE-PHY-PREAMBLEPHY-001",
        "physical_page_or_section": "pp. 1-6 / DME Provisioning",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Governs outpatient clinic-supplied physical therapy equipment, bracing, and TENS units; establishes medical necessity crossover with DME coverage policies.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "Cross-domain reference to Centene CP.MP.107 DMEPOS policy"
    },
    {
        "mapping_id": "MAP-PHY-007",
        "document_id": "DOC-PHY-008",
        "policy_id": "2026 Evolent Experimental/Investigational Services Policy",
        "rule_id": "RULE-PHY-ECG1501CHIROINFANT-001",
        "physical_page_or_section": "pp. 1-7 / Excluded Interventions",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Classifies unproven physical medicine interventions (dry needling, spinal decompression tables, chiropractic manipulation for non-musculoskeletal pediatric conditions) as investigational.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-008",
        "document_id": "DOC-PHY-009",
        "policy_id": "2026 Evolent Record Keeping Standards",
        "rule_id": "RULE-PHY-PREAMBLEPHY-001",
        "physical_page_or_section": "pp. 1-5 / Documentation Rules",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Sets professional documentation standards including signed evaluation, treatment dates, time-based code recording, and progress note retention.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-009",
        "document_id": "DOC-PHY-010",
        "policy_id": "2026 Evolent Physical Medicine Guidelines",
        "rule_id": "RULE-PHY-POLICYMEASURABLEIMPROV-001",
        "physical_page_or_section": "pp. 1-4 / Intake Checklist & Tip Sheet",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Checklist capturing prior level of function, initial evaluation, measurable goals, treatment response, standardized testing, and discharge criteria.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-010",
        "document_id": "DOC-PHY-011",
        "policy_id": "2026 Evolent Physical Medicine Guidelines",
        "rule_id": "RULE-PHY-POLICYPASSIVETREATMENT-001",
        "physical_page_or_section": "pp. 1-2 / Maintenance & Episodic Care",
        "relationship_type": "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
        "evidence_description": "Distinguishes restorative care from non-covered maintenance therapy; outlines episodic care criteria for acute functional flare-ups.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    },
    {
        "mapping_id": "MAP-PHY-011",
        "document_id": "DOC-PHY-012",
        "policy_id": "2026 Evolent Physical Medicine Guidelines",
        "rule_id": "RULE-PHY-PREAMBLEPHY-001",
        "physical_page_or_section": "Page 1 / Attestation Form",
        "relationship_type": "SUPPORTS_DOCUMENTATION_COLLECTION",
        "evidence_description": "Standardized patient attestation form affirming termination of therapy at previous facility to prevent overlapping or duplicate authorizations across clinics.",
        "verification_status": "VERIFIED_MAPPING",
        "unresolved_dependencies": "None"
    }
]

FIELDS = [
    {
        "field_id": "FIELD-PHY-010-01",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 1 / Member Demographics",
        "field_label": "Member Full Name & Health Plan ID",
        "field_meaning": "Patient identifier for physical medicine therapy benefit verification",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Required for member matching and benefit plan lookup"
    },
    {
        "field_id": "FIELD-PHY-010-02",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 1 / Treating Therapist",
        "field_label": "Treating Clinician Name, Discipline & NPI",
        "field_meaning": "Licensed Physical Therapist (PT), Occupational Therapist (OT), Speech Pathologist (SLP), or Chiropractor (DC) NPI",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Validates licensed therapy professional"
    },
    {
        "field_id": "FIELD-PHY-010-03",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 1 / Therapy Discipline",
        "field_label": "Therapy Discipline (PT / OT / ST / Chiropractic)",
        "field_meaning": "Therapeutic specialty and requested billing CPT codes (e.g. 97110, 97530, 92507, 98940)",
        "data_type": "enum",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Determines discipline-specific clinical evaluation pathway"
    },
    {
        "field_id": "FIELD-PHY-010-04",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 1 / Clinical History",
        "field_label": "Date of Onset of Current Condition / Surgery / Exacerbation",
        "field_meaning": "Date injury occurred, surgery was performed, or acute functional decline began",
        "data_type": "date",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Determines rehabilitative acuity vs chronic maintenance status"
    },
    {
        "field_id": "FIELD-PHY-010-05",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 1 / Prior Function",
        "field_label": "Prior Level of Function (PLOF)",
        "field_meaning": "Detailed description of patient's functional abilities and independence prior to current episode",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Benchmark to measure potential restorative gains"
    },
    {
        "field_id": "FIELD-PHY-010-06",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 1 / Initial Evaluation",
        "field_label": "Initial Evaluation with Objective Baseline Measurements",
        "field_meaning": "Quantified baseline ROM degrees, manual muscle test (MMT 0-5), balance scores, gait metrics",
        "data_type": "file_attachment",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-POLICYMEASURABLEIMPROV-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory objective clinical baseline; general subjective statements prohibited"
    },
    {
        "field_id": "FIELD-PHY-010-07",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 1 / Plan of Care",
        "field_label": "Requested Treatment Frequency and Duration",
        "field_meaning": "Number of sessions per week (e.g. 2x/week) and total requested weeks of care (e.g. 4 weeks)",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Defines authorized treatment envelope"
    },
    {
        "field_id": "FIELD-PHY-010-08",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 2 / Treatment Goals",
        "field_label": "Specific, Measurable, Time-Framed Treatment Goals (STGs / LTGs)",
        "field_meaning": "Target functional metrics achievable within authorization period with anticipated discharge timeline",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-POLICYMEASURABLEIMPROV-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Goals must be functional, measurable, and realistic"
    },
    {
        "field_id": "FIELD-PHY-010-09",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 3 / Progress Monitoring",
        "field_label": "Documented Measurable Functional Progress in Past 2 Weeks",
        "field_meaning": "Demonstrated objective improvement in pain and functional metrics compared to baseline",
        "data_type": "boolean",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Concurrent / Continuation Requests",
        "linked_policy_or_rule": "RULE-PHY-POLICYMEASURABLEIMPROV-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Mandatory for authorizing continuing therapy sessions"
    },
    {
        "field_id": "FIELD-PHY-010-10",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 3 / Home Program",
        "field_label": "Home Exercise Program (HEP) Prescribed and Documented",
        "field_meaning": "Written independent home program provided to patient with documented patient/caregiver compliance",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "All Physical Medicine Intake",
        "linked_policy_or_rule": "RULE-PHY-POLICYPASSIVETREATMENT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Transition to self-management required when plateau is reached"
    },
    {
        "field_id": "FIELD-PHY-010-11",
        "document_id": "DOC-PHY-010",
        "source_page_or_section": "Page 4 / Habilitative Testing",
        "field_label": "Age-Appropriate Standardized Norm-Referenced Test Scores",
        "field_meaning": "Standard scores, percentiles, or standard deviations from validated pediatric motor/speech tests (e.g. Peabody, BOT-2, PLS-5)",
        "data_type": "string",
        "requirement_level": "CONDITIONAL",
        "clinical_scope": "Pediatric Habilitative Therapy",
        "linked_policy_or_rule": "RULE-PHY-POLICYHABILITATIVEPTOT-001",
        "clinical_vs_administrative": "CLINICAL_EVIDENCE",
        "review_notes": "Must establish presence of significant developmental functional delay"
    },
    {
        "field_id": "FIELD-PHY-012-01",
        "document_id": "DOC-PHY-012",
        "source_page_or_section": "Page 1 / Member Confirmation",
        "field_label": "Attestation of Discontinued Care at Prior Facility",
        "field_meaning": "Affirmation that member is no longer receiving physical, occupational, or speech therapy at another clinic",
        "data_type": "boolean",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Transfer / Overlapping Therapy Requests",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Prevents double billing / duplicate concurrent prior authorizations"
    },
    {
        "field_id": "FIELD-PHY-012-02",
        "document_id": "DOC-PHY-012",
        "source_page_or_section": "Page 1 / Signature",
        "field_label": "Patient / Parent / Guardian Signature & Date",
        "field_meaning": "Legal signature confirming termination of care at external facility",
        "data_type": "string",
        "requirement_level": "REQUIRED",
        "clinical_scope": "Transfer / Overlapping Therapy Requests",
        "linked_policy_or_rule": "RULE-PHY-PREAMBLEPHY-001",
        "clinical_vs_administrative": "ADMINISTRATIVE_INTAKE",
        "review_notes": "Mandatory signed member legal statement"
    }
]

UNMAPPED = [
    {
        "document_id": "DOC-PHY-MISSING-001",
        "domain": "physical_medicine",
        "document_title": "Health Plan Summary Plan Description (SPD) Annual Therapy Benefit Caps",
        "document_category": "Member benefit contract",
        "document_type": "other_supporting_document",
        "version_status": "current_2026_verified",
        "disposition_status": "PLAN_SPECIFIC_ACCESS_REQUIRED",
        "unmapped_reason": "Employer group certificates of coverage define hard annual financial or visit caps (e.g. 20-60 visits/year) overriding medical necessity.",
        "evidentiary_limitation": "Available only in individual commercial plan evidence of coverage contracts.",
        "human_review_required": True
    }
]
