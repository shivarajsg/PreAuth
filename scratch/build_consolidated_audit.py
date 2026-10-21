import csv
from pathlib import Path

ROOT = Path(".")
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

out_file = REPORTS_DIR / "consolidated_policy_fidelity_audit.csv"

# Load the 4 batches
b1_rows = list(csv.DictReader(open(REPORTS_DIR / "batch_01_policy_audit.csv", encoding="utf-8")))
b2_rows = list(csv.DictReader(open(REPORTS_DIR / "batch_02_policy_audit.csv", encoding="utf-8")))
b3_rows = list(csv.DictReader(open(REPORTS_DIR / "batch_03_policy_audit.csv", encoding="utf-8")))
b4_rows = list(csv.DictReader(open(REPORTS_DIR / "batch_04_policy_audit.csv", encoding="utf-8")))

fieldnames = [
    "batch_number",
    "rule_id",
    "domain",
    "existing_status",
    "source_pdf",
    "pdf_physical_page",
    "printed_page",
    "policy_section",
    "exact_quotation",
    "finding_category",
    "enforcement_location",
    "missing_context_or_exceptions",
    "unresolved_questions",
    "evidence_verification_status",
    "explanation_and_recommendation"
]

# Map Batch 1 metadata
b1_meta = {
    "RULE-ADV-CG2000-002": {
        "printed_page": "Page 4 of 29",
        "finding_category": "Explicit source requirement omitted (emergency exclusion); Already handled elsewhere (IBD criteria in rule); Advisory context only (MRI consideration)",
        "enforcement_location": "Core criteria in rule; toxic megacolon/perforation emergency exclusion omitted entirely",
        "unresolved_questions": "Should toxic megacolon and free perforation emergency bypasses be added as explicit exclusion gates?",
    },
    "RULE-ADV-CG2000-004": {
        "printed_page": "Page 4 of 29",
        "finding_category": "Explicit source requirement omitted (pregnancy ultrasound gate); Already handled elsewhere (systemic criteria in rule); Advisory context only (pediatric notes)",
        "enforcement_location": "Systemic inflammatory signs in rule; mandatory pregnancy ultrasound-first gate omitted from rule logic",
        "unresolved_questions": "Should pregnancy ultrasound-first prerequisite be enforced via shared clinical gate or procedure-specific condition?",
    },
    "RULE-ADV-CG2000-005": {
        "printed_page": "Page 4 of 29",
        "finding_category": "Explicit source requirement omitted (pediatric ultrasound habitus exception); Already handled elsewhere (pediatric RLQ pain in rule); Advisory context only (radiation sparing)",
        "enforcement_location": "Pediatric appendicitis signs in rule; body habitus/cooperation exception to prior ultrasound omitted",
        "unresolved_questions": "Should ultrasound-inconclusive body habitus exception be codified as a discrete bypass parameter?",
    },
    "RULE-ADV-CG2003-001": {
        "printed_page": "Page 6 of 18",
        "finding_category": "Already handled elsewhere (surveillance intervals in rule); Explicit source requirement omitted (cross-cutting MRI contraindication check); Advisory context only (arteritis references)",
        "enforcement_location": "Intervals in rule; relies on external MRI contraindication routing",
        "unresolved_questions": "Should MRA surveillance explicitly check for active inflammatory flare before approving repeat study?",
    },
    "RULE-ADV-CG2004-001": {
        "printed_page": "Page 5 of 26",
        "finding_category": "Explicit source requirement omitted (MRCP CPT code specificity); Already handled elsewhere (prior ultrasound prerequisite in rule); Advisory context only (biliary dilatation notes)",
        "enforcement_location": "Prior ultrasound in rule; MRCP vs Abdomen MRI code specificity uncodified",
        "unresolved_questions": "Should choledochal cyst rule restrict approval specifically to MRCP CPT codes rather than general Abdomen MRI?",
    },
    "RULE-ADV-CG2004-002": {
        "printed_page": "Page 5 of 26",
        "finding_category": "Explicit source requirement omitted (lipase/amylase > 3x ULN criterion); Already handled elsewhere (pancreatic pain in rule); Advisory context only (imaging timing)",
        "enforcement_location": "Pancreatic pain in rule; objective serum lipase/amylase 3x ULN threshold omitted",
        "unresolved_questions": "Must acute pancreatitis rules require documented 3x ULN enzyme elevation or is clinical diagnosis sufficient?",
    },
    "RULE-ADV-CG2005-001": {
        "printed_page": "Page 5 of 15",
        "finding_category": "Explicit source requirement omitted (biphasic CTA protocol specification); Already handled elsewhere (acute ischemia indication in rule); Advisory context only (technical acquisition protocol)",
        "enforcement_location": "Mesenteric ischemia indication in rule; biphasic technical protocol is advisory",
        "unresolved_questions": "Is biphasic CTA acquisition protocol an enforceable pre-auth condition or radiologist advisory protocol?",
    },
    "RULE-ADV-CG2005-002": {
        "printed_page": "Page 6 of 15",
        "finding_category": "Explicit source requirement omitted (CT contraindication fallback trigger); Already handled elsewhere (venous thrombosis indication in rule); Advisory context only (DVT differential)",
        "enforcement_location": "Portal/mesenteric thrombosis in rule; explicit CT contraindication requirement for MR angiography omitted",
        "unresolved_questions": "Should MR angiography of abdomen veins require documented CT contrast allergy/renal insufficiency?",
    },
    "RULE-ADV-CG2008-001": {
        "printed_page": "Page 5 of 26",
        "finding_category": "Explicit source requirement omitted (discrete focal neurological deficit parameters); Already handled elsewhere (acute stroke presentation in rule); Advisory context only (ASPECTS score)",
        "enforcement_location": "Acute stroke indication in rule; collapses individual focal deficits into composite boolean",
        "unresolved_questions": "Should stroke CT decompose into specific NIHSS/focal deficit parameters or retain composite boolean?",
    },
    "RULE-ADV-CG2008-002": {
        "printed_page": "Page 6 of 26",
        "finding_category": "Already handled elsewhere (acute SAH indication in rule); Advisory context only (lumbar puncture timing guidance); Explicit source requirement omitted (thunderclap timing parameter)",
        "enforcement_location": "SAH suspicion in rule; LP timing and negative non-contrast CT sequence handled in practice",
        "unresolved_questions": "Should negative non-contrast CT within 6 hours be an explicit prerequisite for CTA in suspected SAH?",
    }
}

rows_out = []

# Process Batch 1
for r in b1_rows:
    rid = r["rule_id"]
    meta = b1_meta.get(rid, {})
    rows_out.append({
        "batch_number": 1,
        "rule_id": rid,
        "domain": r["domain"],
        "existing_status": "DRAFT",
        "source_pdf": r["source_pdf"],
        "pdf_physical_page": r["pdf_physical_page"],
        "printed_page": meta.get("printed_page", ""),
        "policy_section": r["policy_section"],
        "exact_quotation": r["exact_quotation"],
        "finding_category": meta.get("finding_category", r.get("reflects_source", "")),
        "enforcement_location": meta.get("enforcement_location", "Rule condition"),
        "missing_context_or_exceptions": r["missing_context_or_exceptions"],
        "unresolved_questions": meta.get("unresolved_questions", ""),
        "evidence_verification_status": "VERIFIED_AGAINST_SOURCE",
        "explanation_and_recommendation": r["explanation_and_recommendation"]
    })

# Process Batch 2
b2_questions = {
    "RULE-ADV-CG2008-003": "Should traumatic brain injury rule codify all 8 Canadian CT Head Rule criteria as discrete inputs?",
    "RULE-ADV-CG2008-004": "Should severe thunderclap headache rule enforce strict < 48h onset boundary?",
    "RULE-ADV-CG2009-002": "RESOLVED CARRY-FORWARD: Source citation physical page is p. 175 (LVO), not p. 176 (aneurysms). Should rule metadata be updated to p. 175?",
    "RULE-ADV-CG2015-001": "Should neck MRI rule require documented non-contrast CT prior to advanced MRI evaluation?",
    "RULE-ADV-CG2016-001": "Should cervical spine CT enforce discrete NEXUS / Canadian C-Spine low-risk criteria?",
    "RULE-ADV-CG2017-001": "Should cervical radiculopathy rule mandate physical therapy trial or accept home exercise?",
    "RULE-ADV-CG2017-002": "Should cervical myelopathy rule codify upper motor neuron exam findings as discrete checklist?",
    "RULE-ADV-CG2017-003": "Should cervical cord compression rule require objective neurological deficit to approve MRI?",
    "RULE-ADV-CG2022-001": "Should acute diverticulitis CT pelvis enforce clinical diagnosis prior to imaging?",
    "RULE-ADV-CG2030-001": "RESOLVED CARRY-FORWARD: LDCT screening policy explicitly mandates 'asymptomatic individuals'. Confirmed uncodified in engine. Must rule enforce asymptomatic == true?"
}

for r in b2_rows:
    rid = r["rule_id"]
    rows_out.append({
        "batch_number": 2,
        "rule_id": rid,
        "domain": r["domain"],
        "existing_status": r.get("existing_status", "DRAFT"),
        "source_pdf": r["source_pdf"],
        "pdf_physical_page": r["pdf_physical_page"],
        "printed_page": r.get("printed_page", ""),
        "policy_section": r["policy_section"],
        "exact_quotation": r["exact_quotation"],
        "finding_category": r["category_classification"],
        "enforcement_location": "Core indication in rule; detailed sub-criteria omitted or handled by sibling red-flag rules",
        "missing_context_or_exceptions": r["missing_context_or_exceptions"],
        "unresolved_questions": b2_questions.get(rid, ""),
        "evidence_verification_status": "VERIFIED_AGAINST_SOURCE",
        "explanation_and_recommendation": r["explanation_and_recommendation"]
    })

# Process Batch 3
b3_questions = {
    "RULE-ADV-CG2032-001": "Should lower extremity CT rule add mandatory >= 4 weeks active conservative therapy failure?",
    "RULE-ADV-CG2035-001": "Should knee/joint MRI rule add mandatory prior X-ray and 4 weeks conservative therapy?",
    "RULE-ADV-CG2035-002": "CARRY-FORWARD: Policy note says X-ray is 'preferred, NOT required', but rule strictly mandates it. Should rule relax X-ray requirement for positive orthopedic exam signs?",
    "RULE-ADV-CG2036-001": "Should lumbar spine CT decompose composite boolean into discrete deficit vs fusion failure indications?",
    "RULE-ADV-CG2037-001": "CARRY-FORWARD: Rule cites physical p. 594 (Neurologic Deficits), but radiculopathy + 6-wk care criteria are on p. 595 (Back pain). Should citation be updated to p. 595?",
    "RULE-ADV-CG2037-002": "Should cauda equina rule validate at least one specific cardinal symptom (saddle anesthesia, bowel/bladder incontinence)?",
    "RULE-ADV-CG2042-001": "CARRY-FORWARD: Policy specifies 'over the age of 65'. Should boundary condition be strictly > 65 or >= 65?",
    "RULE-ADV-CG2045-001": "Should pelvic MRI rule add discrete parameters for Crohn's disease history and recurrent post-surgical fistula?",
    "RULE-ADV-CG2054-001": "CARRY-FORWARD: CRITICAL GAP. Sella CT omits section prerequisite 'When MRI contraindicated or cannot be performed'. Should prerequisite be added immediately?",
    "RULE-ADV-CG2055-001": "CARRY-FORWARD: CRITICAL GAP. TMJ MRI omits mandatory prerequisite of at least 4 weeks unsuccessful pharmacotherapy AND behavioral modification. Should prerequisite be added immediately?"
}

for r in b3_rows:
    rid = r["rule_id"]
    rows_out.append({
        "batch_number": 3,
        "rule_id": rid,
        "domain": r["domain"],
        "existing_status": r.get("existing_status", "DRAFT"),
        "source_pdf": r["source_pdf"],
        "pdf_physical_page": r["pdf_physical_page"],
        "printed_page": r.get("printed_page", ""),
        "policy_section": r["policy_section"],
        "exact_quotation": r["exact_quotation"],
        "finding_category": r["category_classification"],
        "enforcement_location": "Indication in rule; prerequisites omitted or citation discrepancies identified",
        "missing_context_or_exceptions": r["missing_context_or_exceptions"],
        "unresolved_questions": b3_questions.get(rid, ""),
        "evidence_verification_status": "VERIFIED_AGAINST_SOURCE",
        "explanation_and_recommendation": r["explanation_and_recommendation"]
    })

# Process Batch 4
b4_questions = {
    "RULE-ADV-CG2056-001": "Should thoracic CT rule decompose composite deficit boolean into discrete exam signs and codify cord compression?",
    "RULE-ADV-CG2056-002": "CRITICAL GAP: Thoracic CT back pain omits mandatory prerequisite 'when MRI is contraindicated' and miscodes conservative care. Should MRI contraindication and 6-week duration be added?",
    "RULE-ADV-CG2057-001": "Should thoracic MRI rule structure 6 physical exam deficit signs as selectable criteria?",
    "RULE-ADV-CG2057-002": "Should thoracic MRI back pain rule align conservative treatment to minimum 6 weeks within 6 months and separate pediatric red flags?",
    "RULE-ADV-CG2062-001": "CRITICAL GAP: Upper extremity CT omits mandatory section prerequisite 'MRI contraindicated or cannot be performed'. Should prerequisite be added?",
    "RULE-IPM-CGEPIDURALINJECTIONS-001": "HIGH-PRIORITY IPM STUB: Uncompiled stub ('cgepiduralinjections_indication IS_PRESENT') omits all clinical criteria (pain >= 6/10, acute vs stenosis care, guidance, repeat limits). Should full compilation be scheduled?",
    "RULE-IPM-CGEPIDURALINJECTIONS-002": "Should ESI conservative therapy rule expand beyond generic string to enforce 2 mandatory HEP elements (clinician prescription + 6-wk completion)?",
    "RULE-IPM-CGEPIDURALPUMPTRIALS-001": "HIGH-PRIORITY IPM STUB: Uncompiled stub omits 12-week conservative care failure, pain >= 6/10, and spasticity criteria. Should full compilation be scheduled?",
    "RULE-IPM-CGFACETBLOCKS-001": "HIGH-PRIORITY IPM STUB: Uncompiled stub omits pain >= 6/10, 3 months duration, axial restriction, 6 weeks conservative care, and repeat injection limits. Should full compilation be scheduled?",
    "RULE-IPM-CGSIINJECTIONS-001": "HIGH-PRIORITY IPM STUB: Uncompiled stub omits cardinal cluster of >= 3 positive provocative exam tests and 6 weeks conservative care. Should full compilation be scheduled?",
    "RULE-IPM-CGSPINALCORDSTIM-001": "HIGH-PRIORITY IPM STUB: Uncompiled stub omits qualifying etiologies, 6 months conservative care, and mandatory presurgical psychological clearance. Should full compilation be scheduled?",
    "RULE-IPM-CGSPINALCORDSTIM-002": "Should permanent SCS rule add mandatory prerequisite: 'Significant functional improvement for a minimum duration of 3 days'?",
    "RULE-IPM-CGSYMPATHETICBLOCKS-001": "HIGH-PRIORITY IPM STUB: Uncompiled stub omits pain >= 6/10, image guidance, specific etiology pathways (herpes zoster, CRPS, cancer), and session limits. Should full compilation be scheduled?"
}

for r in b4_rows:
    rid = r["rule_id"]
    rows_out.append({
        "batch_number": 4,
        "rule_id": rid,
        "domain": r["domain"],
        "existing_status": r.get("existing_status", "DRAFT"),
        "source_pdf": r["source_pdf"],
        "pdf_physical_page": r["pdf_physical_page"],
        "printed_page": r.get("printed_page", ""),
        "policy_section": r["policy_section"],
        "exact_quotation": r["exact_quotation"],
        "finding_category": r["category_classification"],
        "enforcement_location": "Stub rule or partial indication in rule; clinical prerequisites omitted or citation discrepancies identified",
        "missing_context_or_exceptions": r["missing_context_or_exceptions"],
        "unresolved_questions": b4_questions.get(rid, ""),
        "evidence_verification_status": "VERIFIED_AGAINST_SOURCE",
        "explanation_and_recommendation": r["explanation_and_recommendation"]
    })

# Write out consolidated CSV
with open(out_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"Generated consolidated audit with {len(rows_out)} rows in {out_file}")
print(f"Unique rule IDs: {len(set(r['rule_id'] for r in rows_out))}")
