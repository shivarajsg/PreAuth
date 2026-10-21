import csv
from pathlib import Path

ROOT = Path(".")
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

csv_file = REPORTS_DIR / "batch_03_policy_audit.csv"

fieldnames = [
    "rule_id",
    "domain",
    "existing_status",
    "source_pdf",
    "pdf_physical_page",
    "printed_page",
    "policy_section",
    "exact_quotation",
    "category_classification",
    "missing_context_or_exceptions",
    "audit_status",
    "explanation_and_recommendation"
]

rows = [
    {
        "rule_id": "RULE-ADV-CG2032-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 504,
        "printed_page": "Page 4 of 23",
        "policy_section": "INDICATIONS FOR LOWER EXTREMITY CT / Non-specific Lower Extremity Pain (1,2)",
        "exact_quotation": "Lower extremity pain with no specific joint identified with MRI contraindicated or cannot be performed AND with prior X-ray showing no clear etiology of extremity pain with any ONE of the following: Persistent musculotendinous lower extremity pain unresponsive to ACTIVE Conservative Therapy (ACT) ... of at least four (4) weeks duration within the last 6 months",
        "category_classification": "Explicit source requirement omitted (4 weeks active conservative care failure); Handled by rule (MRI contraindication & prior X-ray); Advisory context only (definition of ACT modalities)",
        "missing_context_or_exceptions": "Omitted mandatory requirement for documented failure of >= 4 weeks active conservative therapy within last 6 months (or symptom progression, or pediatric < 12yo exception).",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Prior X-ray and MRI contraindication match text. Recommend Clinical SME review to add mandatory >= 4 weeks conservative therapy failure condition."
    },
    {
        "rule_id": "RULE-ADV-CG2035-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 553,
        "printed_page": "Page 4 of 22",
        "policy_section": "INDICATIONS FOR LOWER EXTREMITY MRI / Joint Specific Pain or Suspected Joint Specific Injury",
        "exact_quotation": "In the absence of a positive joint specific orthopedic sign on exam (see list below), advanced imaging is indicated with prior X-ray showing no clear etiology for the joint pain with any ONE of the following: Persistent joint pain unresponsive to ACTIVE Conservative Therapy (ACT) ... of at least four (4) weeks duration within the last 6 months",
        "category_classification": "Explicit source requirement omitted (mandatory prior X-ray and >= 4 weeks active conservative therapy); Handled elsewhere (positive orthopedic signs handled in rule 002); Advisory context (bilateral hip note)",
        "missing_context_or_exceptions": "Rule approves joint pain without requiring prior plain radiograph or failure of >= 4 weeks active conservative therapy.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Overly broad rule. Recommend Clinical SME review to add mandatory prior X-ray and 4-week active conservative therapy failure conditions."
    },
    {
        "rule_id": "RULE-ADV-CG2035-002",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 553,
        "printed_page": "Page 4 of 22",
        "policy_section": "INDICATIONS FOR LOWER EXTREMITY MRI / Joint Specific Orthopedic Signs",
        "exact_quotation": "Joint specific advanced imaging is indicated for any positive orthopedic sign listed below: ... NOTE: With a positive orthopedic sign from the list below, an initial X-ray is always preferred; however, it is NOT required UNLESS otherwise specified in bold below.",
        "category_classification": "Explicit source requirement omitted (specific joint lists ankle/knee/hip); Already handled elsewhere (stricter than policy: rule mandates X-ray whereas note says preferred); Advisory context (instability notes)",
        "missing_context_or_exceptions": "Rule enforces prior X-ray completion, whereas policy note states X-ray is preferred but NOT strictly required for positive orthopedic signs.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Orthopedic exam signs match policy. Recommend Clinical SME review to align prior X-ray requirement with policy note (preferred vs mandatory)."
    },
    {
        "rule_id": "RULE-ADV-CG2036-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 574,
        "printed_page": "Page 3 of 20",
        "policy_section": "INDICATIONS FOR LUMBAR SPINE CT / Evaluation of Neurologic Deficits (1)",
        "exact_quotation": "When Lumbar Spine MRI is Contraindicated or Cannot be performed: With any of the following new neurological deficits documented on physical exam that localizes to the lumbar spine",
        "category_classification": "Explicit source requirement omitted (individual indication parameters); Already handled elsewhere (global MRI contraindications); Advisory context (combination study notes)",
        "missing_context_or_exceptions": "Rule collapses multiple distinct indications (neurologic deficits with MRI contraindicated, trauma, pseudoarthrosis) into single composite boolean.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Indications exist in policy. Recommend Clinical SME review to decompose into discrete rules: (1) Neurologic deficit + MRI contraindicated, and (2) Fusion integrity."
    },
    {
        "rule_id": "RULE-ADV-CG2037-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 594,
        "printed_page": "Page 3 of 22",
        "policy_section": "INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Neurologic Deficits (1)",
        "exact_quotation": "Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months",
        "category_classification": "Explicit source requirement omitted (red flag bypasses foot drop/cancer); Ambiguous or conflicting source (citation discrepancy: cites p. 594 Neurologic Deficits, but criteria are from p. 595 Back Pain); Handled elsewhere (cauda equina in 002)",
        "missing_context_or_exceptions": "Rule cites physical page 594 (Neurologic Deficits), but conservative care criteria are located on page 595 (Evaluation of Back Pain). Red flag bypasses omitted from rule.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Radiculopathy and 6-week conservative care verified on p. 595. Recommend Clinical SME review to update citation page to 595 and codify red flag bypasses."
    },
    {
        "rule_id": "RULE-ADV-CG2037-002",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 595,
        "printed_page": "Page 4 of 22",
        "policy_section": "INDICATIONS FOR LUMBAR SPINE MRI / Evaluation of Neurologic Deficits / Cauda Equina Syndrome",
        "exact_quotation": "Cauda Equina Syndrome as evidence by severe back pain/sciatica along with one of the defined symptoms (see Cauda Equina Syndrome section)",
        "category_classification": "Explicit source requirement omitted (specific cardinal symptom multi-select); Already handled elsewhere (immediate approval without therapy); Advisory context (surgical urgency)",
        "missing_context_or_exceptions": "Uses generic boolean 'suspected_cauda_equina_syndrome' rather than validating at least one documented cardinal symptom (saddle anesthesia, bowel/bladder incontinence).",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Emergent indication verified against source. Recommend Clinical SME review to structure specific cardinal symptoms as multi-select parameters."
    },
    {
        "rule_id": "RULE-ADV-CG2042-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 673,
        "printed_page": "Page 4 of 16",
        "policy_section": "INDICATIONS FOR PELVIS CT / Pelvic Pain for Unknown Etiology",
        "exact_quotation": "For acute pelvic pain in a patient over the age of 65 (2)",
        "category_classification": "Already handled elsewhere (age > 65 directly in rule); Ambiguous or conflicting source (boundary condition: strictly > 65 vs >= 65); Advisory context (elderly pain literature)",
        "missing_context_or_exceptions": "Policy states 'over the age of 65'. Rule checks age > 65. Reverse boundary for females <= 65 requiring ultrasound-first is handled in separate guideline sections.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Indication and age threshold match source text. Recommend Clinical SME review to clarify exact age boundary (> 65 vs >= 65)."
    },
    {
        "rule_id": "RULE-ADV-CG2045-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 718,
        "printed_page": "Page 4 of 22",
        "policy_section": "INDICATIONS FOR PELVIC MRI / Infection and Inflammation",
        "exact_quotation": "Suspected perianal fistula or occult anorectal abscess (6); For patients with recurrent fistula in anal or perianal Crohn’s disease (7); Any history of fistula limited to the pelvis that requires re-evaluation or is suspected to have recurred",
        "category_classification": "Explicit source requirement omitted (Crohn's history / recurrence sub-parameters); Already handled elsewhere (Pelvic MRI modality alignment); Advisory context (T2 sequence protocol)",
        "missing_context_or_exceptions": "Rule uses single parameter for fistula/abscess, omitting explicit parameters for Crohn's disease history or recurrent post-surgical fistula monitoring.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Indication verified against source. Recommend Clinical SME review to structure Crohn's disease history and recurrent fistula as discrete sub-parameters."
    },
    {
        "rule_id": "RULE-ADV-CG2054-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 881,
        "printed_page": "Page 4 of 17",
        "policy_section": "INDICATIONS FOR SELLA CT",
        "exact_quotation": "INDICATIONS FOR SELLA CT / Sella CT (9) / When MRI is contraindicated or cannot be performed: For further evaluation of known sellar and/or parasellar masses",
        "category_classification": "Explicit source requirement omitted (CRITICAL: mandatory prerequisite 'When MRI is contraindicated or cannot be performed'); Advisory context (sellar lesion references)",
        "missing_context_or_exceptions": "Rule approves Sella CT for known mass without verifying that MRI is contraindicated or cannot be performed, violating the explicit section prerequisite.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "CRITICAL FIDELITY GAP. Sella CT is secondary to Brain/Sella MRI. Recommend Clinical SME review to add mandatory prerequisite 'mri_contraindicated == true'."
    },
    {
        "rule_id": "RULE-ADV-CG2055-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 896,
        "printed_page": "Page 2 of 8",
        "policy_section": "INDICATIONS FOR TEMPOROMANDIBULAR JOINT (TMJ) MRI / Suspected Internal TMJ Derangement",
        "exact_quotation": "Suspected Internal TMJ Derangement: Persistent symptoms of facial or jaw pain, restricted range of motion, pain and/or noise with TMJ function (i.e., chewing) (2-4) AND Conservative therapy with a trial of pharmacotherapy* AND behavioral modification** has been unsuccessful for at least four (4) weeks",
        "category_classification": "Explicit source requirement omitted (CRITICAL: mandatory 4-week trial of pharmacotherapy AND behavioral modification); Advisory context (definitions of pharmacotherapy/splints)",
        "missing_context_or_exceptions": "Rule checks clinical symptoms but completely omits the mandatory prerequisite of at least 4 weeks of unsuccessful pharmacotherapy AND behavioral modification.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "CRITICAL FIDELITY GAP. Rule approves TMJ MRI without conservative therapy. Recommend Clinical SME review to add 'conservative_therapy_duration_weeks >= 4'."
    }
]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} audit rows in {csv_file}")
