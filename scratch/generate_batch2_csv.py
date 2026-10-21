import csv
from pathlib import Path

ROOT = Path(".")
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

csv_file = REPORTS_DIR / "batch_02_policy_audit.csv"

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
        "rule_id": "RULE-ADV-CG2008-003",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 151,
        "printed_page": "Page 6 of 26",
        "policy_section": "Head Trauma / Evaluation of Known or Suspected Trauma (14,15)",
        "exact_quotation": "Known or suspected trauma or injury to the head with documentation of one or more of the following acute, new, or fluctuating: Focal neurologic findings; Motor changes; Mental status changes; Amnesia; Vomiting; Seizures; Headache; Signs of increased intracranial pressure",
        "category_classification": "Category A (Explicit policy requirement omitted: 8 enumerated qualifying signs compressed into single boolean); Category C (Advisory context: Canadian CT Head Rule references)",
        "missing_context_or_exceptions": "The 8 distinct qualifying trauma signs (vomiting, amnesia, seizures, focal deficits) are compressed into single composite boolean without individual parameter validation.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Core trauma indication verified. Recommend Clinical SME review to structure individual post-traumatic qualifying findings into an ANY_OF sub-condition array."
    },
    {
        "rule_id": "RULE-ADV-CG2008-004",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 149,
        "printed_page": "Page 4 of 26",
        "policy_section": "INDICATIONS / Headache / Evaluation of Headache (1,2) / Acute, sudden onset headache",
        "exact_quotation": "Acute, sudden onset headache (< 4 weeks), with any ONE of the following (no contraindication to MRI is needed): ... < 48 hours of 'worst headache in my life' or 'thunderclap' headache",
        "category_classification": "Category A (Explicit policy requirement omitted: < 48h presentation time window parameter); Category B (Handled by routing: no MRI contraindication needed); Category C (Advisory definition of thunderclap intensity)",
        "missing_context_or_exceptions": "Rule verifies thunderclap presentation but does not enforce structured numerical time bounds (symptom duration < 48 hours; overall onset < 4 weeks).",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Criteria verified against source text. Recommend Clinical SME review to add explicit parameter 'hours_since_headache_onset <= 48'."
    },
    {
        "rule_id": "RULE-ADV-CG2009-002",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 176,
        "printed_page": "Page 5 of 20",
        "policy_section": "INDICATIONS FOR BRAIN CT ANGIOGRAPHY / Evaluation of Known Intracranial Vascular Disease (1,2)",
        "exact_quotation": "Evaluation for large vessel occlusion (LVO) in patients with acute stroke who are candidates for mechanical thrombectomy within 24 hours of symptom onset or last known well",
        "category_classification": "Category A (Explicit policy requirement omitted: <= 24h from last known well); Category D / E (Citation discrepancy: clause is on physical page 175, section Stroke, while rule cites p. 176 aneurysm section)",
        "missing_context_or_exceptions": "Time window (<= 24 hours of last known normal) omitted from rule conditions. Citation cites physical page 176 (aneurysm/AVM), but LVO policy text is on page 175.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Clinical intent for thrombectomy LVO is verified in policy, but citation page must be corrected from 176 to 175, and <= 24h time window codified."
    },
    {
        "rule_id": "RULE-ADV-CG2015-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 297,
        "printed_page": "Page 3 of 9",
        "policy_section": "INDICATIONS / Acute Ischemic Stroke",
        "exact_quotation": "For suspected infarct indicated by focal neurological deficit or initial imaging within 24 hours of known ischemic infarct (6)",
        "category_classification": "Category A (Explicit policy requirement omitted: prior non-contrast CT/CTA completion); Category B (Handled by routing: CPT 70473 and Line of Business); Category C (Advisory context: penumbra software)",
        "missing_context_or_exceptions": "Policy background specifies CTP is useful 'after initial CT and/or MR imaging has been obtained'. Rule does not link prior non-contrast CT/CTA completion as an explicit prerequisite.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Core 24-hour window and reperfusion indication verified. Recommend Clinical SME review to confirm whether prior non-contrast CT must be codified as an explicit prerequisite."
    },
    {
        "rule_id": "RULE-ADV-CG2016-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 308,
        "printed_page": "Page 5 of 23",
        "policy_section": "INDICATIONS FOR CERVICAL SPINE CT / Evaluation of Trauma or Acute Injury (13)",
        "exact_quotation": "When office notes specify that the C-spine cannot be clinically cleared because of a high-risk feature such as neurological deficit, midline spinal tenderness, altered mental status, high risk mechanism, unable to rotate neck as described in the NEXUS ... or CCR ... criteria",
        "category_classification": "Category A (Explicit policy requirement omitted: specific individual NEXUS / Canadian C-spine criteria); Category C (Advisory context: MRI when patient obtunded)",
        "missing_context_or_exceptions": "Composite boolean 'acute_cervical_trauma' does not validate individual NEXUS/CCR risk factors (midline tenderness, focal deficit, altered sensorium, rotation inability).",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Trauma indication verified on p. 308. Recommend Clinical SME review to structure discrete NEXUS/CCR checkboxes to improve auditability."
    },
    {
        "rule_id": "RULE-ADV-CG2017-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 330,
        "printed_page": "Page 4 of 26",
        "policy_section": "Evaluation of Neck Pain (5,6)",
        "exact_quotation": "Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months: NOTE - Failure of conservative treatment is defined as one of the following: Lack of meaningful improvement... Progression or worsening... Documentation of a medical reason",
        "category_classification": "Category A (Explicit policy requirement omitted: specific conservative care modalities); Category B (Handled by sibling rules: red flag bypasses handled in rules 002/003); Category C (Advisory text on noncompliance)",
        "missing_context_or_exceptions": "Footnote defines conservative care as active physical therapy or instructed home exercise program plus oral medications. Rule checks generic duration without modality parameters.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "6-week duration, 6-month recency, and failure criteria verified against source. Recommend Clinical SME review to add specific PT and pharmacotherapy parameters."
    },
    {
        "rule_id": "RULE-ADV-CG2017-002",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 331,
        "printed_page": "Page 5 of 26",
        "policy_section": "Evaluation of Suspected Myelopathy (11,12)",
        "exact_quotation": "Evaluation of Suspected Myelopathy (11,12) Progressive symptoms including hand clumsiness, worsening handwriting, difficulty with grasping and holding objects... Any of the neurological deficits as noted above NOTE: Does NOT require conservative care",
        "category_classification": "Category A (Explicit policy requirement omitted: specific reflex findings Babinski/Hoffmann/clonus); Category B (Handled by rule structure: conservative therapy waived); Category C (Advisory functional examples)",
        "missing_context_or_exceptions": "Physical examination signs detailed on adjacent page 330 (Hoffmann sign, Babinski, hyperreflexia, gait ataxia) are compressed into generic boolean.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Indication and conservative care waiver match source. Recommend Clinical SME review to specify objective exam reflex findings."
    },
    {
        "rule_id": "RULE-ADV-CG2017-003",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 330,
        "printed_page": "Page 4 of 26",
        "policy_section": "INDICATIONS / Evaluation of Neck Pain (5,6)",
        "exact_quotation": "Suspected cervical cord compression with any neurological deficits as listed above",
        "category_classification": "Category A (Explicit policy requirement omitted: mandatory documented neurological deficits clause); Category B (Handled by rule structure: immediate approval without therapy); Category C (Advisory surgical urgency)",
        "missing_context_or_exceptions": "Policy explicitly states 'with any neurological deficits as listed above'. The rule only checks suspected cord compression without verifying neurological deficits.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Core indication verified. Recommend Clinical SME review to add condition validating at least one documented objective neurological deficit."
    },
    {
        "rule_id": "RULE-ADV-CG2022-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 436,
        "printed_page": "Page 2 of 7",
        "policy_section": "INDICATIONS (1,2) / For diagnostic evaluation",
        "exact_quotation": "Symptomatic patients when conventional colonoscopy is contraindicated or could not be completed and ONE of the following: Patient had failed or incomplete colonoscopy (1)",
        "category_classification": "Category A (Explicit policy requirement omitted: 'Symptomatic patients' gate and acute diverticulitis/perforation contraindications); Category C (Advisory context on CO2 insufflation)",
        "missing_context_or_exceptions": "Rule checks failed colonoscopy but omits explicit validation that patient is symptomatic (vs screening) and lacks negative exclusion for acute diverticulitis/perforation.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Prerequisite of failed/incomplete colonoscopy verified. Recommend Clinical SME review to add 'patient_is_symptomatic == true' and acute diverticulitis exclusions."
    },
    {
        "rule_id": "RULE-ADV-CG2030-001",
        "domain": "advanced_imaging",
        "existing_status": "DRAFT",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 490,
        "printed_page": "Page 2 of 8",
        "policy_section": "INDICATIONS / For Annual Screening / Group 1 - High Risk for Lung Cancer (3,4)",
        "exact_quotation": "The use of low-dose, non-contrast spiral (helical) multi-detector CT imaging as a screening technique for lung cancer is considered medically necessary ONLY when used to screen for lung cancer for certain high-risk, asymptomatic individuals ... Individual is between 50-80 years of age*; AND There is at least a 20 pack-year history of cigarette** smoking",
        "category_classification": "Category A (Explicit policy requirement omitted: mandatory 'asymptomatic' screening gate); Category B (Handled by routing: CPT 71271 frequency); Category C (Advisory smoking cessation counseling); Category D (Curative candidate exception > 80yo)",
        "missing_context_or_exceptions": "Policy mandates screening ONLY for asymptomatic individuals (symptomatic patients require diagnostic CT 71250). Rule omits mandatory 'asymptomatic_of_lung_disease == true' gate.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Demographic thresholds (50-80yo, >= 20 pack-years, quit <= 15y) verified against source. Recommend Clinical SME review to enforce mandatory asymptomatic gate."
    }
]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} audit rows in {csv_file}")
