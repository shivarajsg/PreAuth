"""
Cross-Domain Policy Dependencies Specification for MedRule Phase 2E.
"""

CROSS_DOMAIN_CMS_DOCS = [
    ("DOC-XCMS-001", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
    ("DOC-XCMS-002", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
    ("DOC-XCMS-003", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
    ("DOC-XCMS-004", "EXTERNAL_AUTHORITY", "PUBLIC_ACCESSIBLE"),
]

POLICY_DEPENDENCY_REGISTER = [
    {
        "dependency_id": "DEP-001",
        "primary_domain": "centene_dme_orthotics_prosthetics",
        "primary_document_id": "DOC-CEN-001",
        "dependent_entity_or_domain": "CMS Medicare Claims Manual Chapter 20",
        "target_document_id": "DOC-CEN-010 / DOC-XCMS-001",
        "relationship_nature": "EXTERNAL_STATUTORY_AUTHORITY",
        "clinical_or_operational_impact": "Establishes certificate of medical necessity (CMN) requirements, DMEPOS billing rules, rental caps, and replacement warranties.",
        "resolution_strategy": "Direct citation and reference alignment; statutory standards incorporated into intake criteria.",
        "status": "VERIFIED_EXTERNAL_DEPENDENCY"
    },
    {
        "dependency_id": "DEP-002",
        "primary_domain": "centene_dme_orthotics_prosthetics",
        "primary_document_id": "DOC-CEN-001",
        "dependent_entity_or_domain": "CMS State Operations Manual Appendix A",
        "target_document_id": "DOC-CEN-011 / DOC-XCMS-002",
        "relationship_nature": "EXTERNAL_STATUTORY_AUTHORITY",
        "clinical_or_operational_impact": "Defines hospital discharge planning requirements, non-coverage of home DME during inpatient hospital stays, and delivery timing.",
        "resolution_strategy": "Inpatient facility delivery restrictions enforced deterministically during case intake.",
        "status": "VERIFIED_EXTERNAL_DEPENDENCY"
    },
    {
        "dependency_id": "DEP-003",
        "primary_domain": "centene_dme_orthotics_prosthetics",
        "primary_document_id": "DOC-CEN-004",
        "dependent_entity_or_domain": "RESNA Position Paper on Seat Elevation",
        "target_document_id": "DOC-CEN-012 / DOC-XCMS-003",
        "relationship_nature": "EXTERNAL_CLINICAL_AUTHORITY",
        "clinical_or_operational_impact": "Supplies evidence base and functional transfer criteria for power seat elevation in Group 3/4 complex power wheelchairs.",
        "resolution_strategy": "PT/OT clinical seating evaluation must document transfer independence or reduction in caregiver assistance.",
        "status": "VERIFIED_EXTERNAL_DEPENDENCY"
    },
    {
        "dependency_id": "DEP-004",
        "primary_domain": "centene_dme_orthotics_prosthetics",
        "primary_document_id": "DOC-CEN-001",
        "dependent_entity_or_domain": "CMS DMEPOS Quality Standards",
        "target_document_id": "DOC-CEN-013 / DOC-XCMS-004",
        "relationship_nature": "EXTERNAL_QUALITY_STANDARD",
        "clinical_or_operational_impact": "Mandates supplier accreditation, patient training, equipment maintenance, and 24/7 emergency repair support.",
        "resolution_strategy": "Supplier NPI must match active NSC-accredited DMEPOS provider registry.",
        "status": "VERIFIED_EXTERNAL_DEPENDENCY"
    },
    {
        "dependency_id": "DEP-005",
        "primary_domain": "physical_medicine",
        "primary_document_id": "DOC-PHY-007",
        "dependent_entity_or_domain": "centene_dme_orthotics_prosthetics",
        "target_document_id": "DOC-CEN-001",
        "relationship_nature": "CROSS_DOMAIN_POLICY_INTERACTION",
        "clinical_or_operational_impact": "Clinic-supplied physical medicine equipment (braces, splints, TENS) interacts with DMEPOS coverage rules and benefit caps.",
        "resolution_strategy": "Deterministic check against member's annual DME benefit limit before issuing duplicate therapy-supplied orthotics.",
        "status": "CROSS_DOMAIN_RESOLVED"
    },
    {
        "dependency_id": "DEP-006",
        "primary_domain": "radiation_oncology",
        "primary_document_id": "DOC-RAD-001",
        "dependent_entity_or_domain": "advanced_imaging",
        "target_document_id": "DOC-ADV-002",
        "relationship_nature": "CROSS_DOMAIN_PLACE_OF_SERVICE_HARMONIZATION",
        "clinical_or_operational_impact": "Outpatient hospital place of service restrictions for radiation simulation scans harmonize with EPOS 2067 imaging rules.",
        "resolution_strategy": "Hospital outpatient simulation scans permitted when radiation treatment course itself is authorized in hospital outpatient department.",
        "status": "CROSS_DOMAIN_RESOLVED"
    },
    {
        "dependency_id": "DEP-007",
        "primary_domain": "musculoskeletal_surgery",
        "primary_document_id": "DOC-MSK-002",
        "dependent_entity_or_domain": "CMS Inpatient Only Schedule",
        "target_document_id": "DOC-MSK-MISSING-001",
        "relationship_nature": "REGULATORY_FEE_SCHEDULE_DEPENDENCY",
        "clinical_or_operational_impact": "Annual CMS Inpatient Only (IPO) list determines whether specific complex spinal fusion codes are eligible for ASC setting.",
        "resolution_strategy": "Deterministic IPO code crosswalk applied during surgical site review.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-008",
        "primary_domain": "interventional_pain_management",
        "primary_document_id": "DOC-IPM-001",
        "dependent_entity_or_domain": "State Medicaid Controlled Substance Schedules",
        "target_document_id": "DOC-IPM-MISSING-001",
        "relationship_nature": "STATE_REGULATORY_FREQUENCY_CAP",
        "clinical_or_operational_impact": "Individual state Medicaid plans mandate strict annual frequency limits (e.g. 4 ESIs per year) overriding clinical recurrence.",
        "resolution_strategy": "State contract rule overrides default clinical guidelines when state contract is active.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-009",
        "primary_domain": "advanced_imaging",
        "primary_document_id": "DOC-ADV-001",
        "dependent_entity_or_domain": "State Medicaid Prior Auth Crosswalks",
        "target_document_id": "DOC-ADV-MISSING-001",
        "relationship_nature": "STATE_CONTRACT_SCOPE_DEPENDENCY",
        "clinical_or_operational_impact": "Determines whether specific low-cost CT/MRI scans require prior notification vs full clinical prior authorization.",
        "resolution_strategy": "Case intake routes to state specific contract threshold table.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-010",
        "primary_domain": "cardiology",
        "primary_document_id": "DOC-CARD-001",
        "dependent_entity_or_domain": "Payer Cardiac Stress Testing Tiering Crosswalks",
        "target_document_id": "DOC-CARD-MISSING-001",
        "relationship_nature": "PAYER_CUSTOM_BENEFIT_TIERING",
        "clinical_or_operational_impact": "Governs whether health plan mandates treadmill exercise ECG before stress echo or MPI.",
        "resolution_strategy": "Payer tiering schedule queried at authorization initiation.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-011",
        "primary_domain": "radiation_oncology",
        "primary_document_id": "DOC-RAD-002",
        "dependent_entity_or_domain": "Payer Proton Beam Coverage Threshold Agreements",
        "target_document_id": "DOC-RAD-MISSING-001",
        "relationship_nature": "PAYER_CUSTOM_BENEFIT_SCHEDULE",
        "clinical_or_operational_impact": "Commercial HMO contracts limit adult proton therapy coverage to specific skull base or re-irradiation indications.",
        "resolution_strategy": "Commercial payer contract rules applied prior to medical necessity review.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-012",
        "primary_domain": "physical_medicine",
        "primary_document_id": "DOC-PHY-001",
        "dependent_entity_or_domain": "Health Plan Summary Plan Description (SPD) Caps",
        "target_document_id": "DOC-PHY-MISSING-001",
        "relationship_nature": "CONTRACTUAL_BENEFIT_MAXIMUM",
        "clinical_or_operational_impact": "Hard annual visit caps (e.g. 20-60 visits/year) truncate authorized treatment regardless of ongoing clinical deficit.",
        "resolution_strategy": "Remaining benefit visit balance decremented before clinical authorization issuance.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-013",
        "primary_domain": "sleep_health",
        "primary_document_id": "DOC-SLP-001",
        "dependent_entity_or_domain": "Employer Group HSAT Exemption Lists",
        "target_document_id": "DOC-SLP-MISSING-001",
        "relationship_nature": "EMPLOYER_GROUP_BENEFIT_EXCEPTION",
        "clinical_or_operational_impact": "Allows direct attended in-lab polysomnography without requiring home sleep testing first.",
        "resolution_strategy": "Client plan exemption flag checked during sleep study intake.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-014",
        "primary_domain": "genetic_testing",
        "primary_document_id": "DOC-GEN-001",
        "dependent_entity_or_domain": "Payer Non-Covered Genetic Panel Exclusion Lists",
        "target_document_id": "DOC-GEN-MISSING-001",
        "relationship_nature": "PAYER_EXCLUSION_SCHEDULE",
        "clinical_or_operational_impact": "Excludes specific broad expanded carrier screening or multigene panels from coverage.",
        "resolution_strategy": "Automated code exclusion list checks requested panel before clinical criteria review.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    },
    {
        "dependency_id": "DEP-015",
        "primary_domain": "centene_dme_orthotics_prosthetics",
        "primary_document_id": "DOC-CEN-001",
        "dependent_entity_or_domain": "Centene State Medicaid DMEPOS Fee Schedules & Quantity Limits",
        "target_document_id": "DOC-CEN-MISSING-001",
        "relationship_nature": "STATE_MEDICAID_FEE_SCHEDULE",
        "clinical_or_operational_impact": "Establishes prior authorization dollar thresholds and lifetime/annual replacement limits by state subsidiary.",
        "resolution_strategy": "State Medicaid contract rules supersede general commercial guidelines.",
        "status": "PLAN_SPECIFIC_ACCESS_REQUIRED"
    }
]
