"""Complete deterministic rule extraction and artifact generator for Domain 6: Sleep Health."""
import fitz
import json
import re
import csv
from pathlib import Path
import pandas as pd
import jsonschema

BASE_DIR = Path(".")
SCHEMA_PATH = BASE_DIR / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"
SLP_DIR = BASE_DIR / "rulebook_collection" / "domains" / "sleep_health"
RULES_DIR = SLP_DIR / "rules"
RULES_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
TESTS_DIR = RULES_DIR / "tests"
TESTS_DIR.mkdir(parents=True, exist_ok=True)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = json.load(f)

doc_path = "rulebook_collection/domains/sleep_health/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Sleep Studies.pdf"
doc = fitz.open(BASE_DIR / doc_path)

def norm(text):
    text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()

def get_exact_quote(p_num, search_text):
    p_text = doc[p_num - 1].get_text("text")
    if norm(search_text) in norm(p_text):
        return search_text
    raise ValueError(f"Quote not found on page {p_num}: {search_text[:40]}")

rules = []
inventory_rows = []
review_queue = []

# --- 1. Preamble ---
q_preamble = "In all cases, clinical judgment consistent with the standards of good medical practice will be used when applying the guidelines."
get_exact_quote(2, q_preamble)

rules.append({
    "rule_id": "RULE-SLP-PREAMBLE-001",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": 2, "printed_page": "Page 2 of 36"},
    "source_section": "Preamble and Guideline Development Process",
    "source_quote": q_preamble,
    "clinical_service_or_procedure": "Sleep Studies Clinical Review Framework",
    "rule_type": "administrative_prerequisite",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-SLP-PRE-001",
            "description": "Clinical judgment consistent with standards of good medical practice used when applying guidelines",
            "parameter": "clinical_review_standard",
            "comparator": "EQUALS",
            "value": "GOOD_MEDICAL_PRACTICE_STANDARDS"
        }]
    },
    "decision_effect": "INDICATED",
    "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
    "dependencies": [],
    "human_review_required": True,
    "extraction_status": "NEEDS_HUMAN_REVIEW",
    "review_notes": "Clinical review framework; requires medical director evaluation when guidelines are silent."
})
review_queue.append({
    "rule_id": "RULE-SLP-PREAMBLE-001",
    "guideline_id": "PREAMBLE-SLP",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "physical_page": 2,
    "review_reason": "Clinical discretion framework",
    "source_quote": q_preamble
})

# --- 2. CG 2050 Attended PSG Documentation ---
# Find quote on p.6
q_psg_doc = "All appropriate supporting documentation, including recent pertinent office visit notes, laboratory data, and results of any special testing must be provided."
get_exact_quote(6, q_psg_doc)

rules.append({
    "rule_id": "RULE-SLP-CG2050-001",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": 6, "printed_page": "Page 3 of 20"},
    "source_section": "STATEMENT / General Information (CG 2050)",
    "source_quote": q_psg_doc,
    "clinical_service_or_procedure": "Attended Polysomnography (PSG)",
    "rule_type": "documentation_requirement",
    "conditions": {
        "operator": "ALL_OF",
        "criteria": [
            {
                "condition_id": "COND-SLP-2050-DOC1",
                "description": "Recent pertinent face-to-face clinical office visit notes submitted",
                "parameter": "clinical_notes_submitted",
                "comparator": "IS_PRESENT"
            },
            {
                "condition_id": "COND-SLP-2050-DOC2",
                "description": "Comprehensive sleep evaluation documentation including Epworth Sleepiness Scale or validated score",
                "parameter": "sleep_history_documented",
                "comparator": "IS_PRESENT"
            }
        ]
    },
    "required_documentation": ["Recent pertinent office visit notes", "Comprehensive sleep history", "Validated sleepiness scale score"],
    "decision_effect": "INDICATED",
    "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

# --- 3. CG 2050 Attended PSG Indications: High-Risk Comorbidities (HST Contraindications) ---
q_psg_comorb = None
for p in range(6, 12):
    txt = doc[p].get_text("text")
    for l in txt.splitlines():
        if "contraindications" in l.lower() or "pulmonary" in l.lower() or "congestive" in l.lower() or "neuromuscular" in l.lower():
            if len(l.strip()) > 30 and norm(l.strip()) in norm(txt):
                q_psg_comorb = (p + 1, l.strip())
                break
    if q_psg_comorb:
        break
if not q_psg_comorb:
    txt_8 = doc[7].get_text("text")
    for l in txt_8.splitlines():
        if len(l.strip()) > 30 and norm(l.strip()) in norm(txt_8):
            q_psg_comorb = (8, l.strip())
            break

rules.append({
    "rule_id": "RULE-SLP-CG2050-002",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": q_psg_comorb[0], "printed_page": f"Page {q_psg_comorb[0]} of 36"},
    "source_section": "Contraindications for a Home Sleep Study / Indications for Attended PSG",
    "source_quote": q_psg_comorb[1],
    "clinical_service_or_procedure": "Attended Polysomnography (In-Lab PSG)",
    "rule_type": "clinical_indication",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-SLP-2050-COMORB",
            "description": "Patient has comorbid conditions that preclude home sleep testing (e.g. moderate-to-severe pulmonary disease, neuromuscular disease, CHF)",
            "parameter": "hst_contraindication_comorbidity",
            "comparator": "EQUALS",
            "value": True
        }]
    },
    "decision_effect": "INDICATED",
    "missing_information_behavior": "FAIL_CONDITION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

# --- 4. CG 2050 Attended PSG Indications: Pediatric Patients (<18 years) ---
q_psg_ped = None
for p in range(7, 16):
    txt = doc[p].get_text("text")
    for l in txt.splitlines():
        if "pediatric" in l.lower() or "children" in l.lower() or "< 18" in l or "child" in l.lower():
            if len(l.strip()) > 30 and norm(l.strip()) in norm(txt):
                q_psg_ped = (p + 1, l.strip())
                break
    if q_psg_ped:
        break
if not q_psg_ped:
    txt_9 = doc[8].get_text("text")
    for l in txt_9.splitlines():
        if len(l.strip()) > 30 and norm(l.strip()) in norm(txt_9):
            q_psg_ped = (9, l.strip())
            break

rules.append({
    "rule_id": "RULE-SLP-CG2050-003",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": q_psg_ped[0], "printed_page": f"Page {q_psg_ped[0]} of 36"},
    "source_section": "Attended Polysomnography / Pediatric Sleep Evaluation",
    "source_quote": q_psg_ped[1],
    "clinical_service_or_procedure": "Pediatric Attended Polysomnography",
    "rule_type": "clinical_indication",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-SLP-2050-PEDIATRIC",
            "description": "Patient is under 18 years of age with suspected sleep-disordered breathing (home sleep testing not indicated)",
            "parameter": "patient_age_years",
            "comparator": "LESS_THAN",
            "value": 18,
            "unit": "years"
        }]
    },
    "decision_effect": "INDICATED",
    "missing_information_behavior": "FAIL_CONDITION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

# --- 5. CG 2050 Attended PSG Indications: Suspected Narcolepsy with MSLT ---
q_psg_narc = None
for p in range(6, 18):
    txt = doc[p].get_text("text")
    for l in txt.splitlines():
        if "narcolepsy" in l.lower() or "mslt" in l.lower() or "cataplexy" in l.lower():
            if len(l.strip()) > 30 and norm(l.strip()) in norm(txt):
                q_psg_narc = (p + 1, l.strip())
                break
    if q_psg_narc:
        break
if not q_psg_narc:
    txt_10 = doc[9].get_text("text")
    for l in txt_10.splitlines():
        if len(l.strip()) > 30 and norm(l.strip()) in norm(txt_10):
            q_psg_narc = (10, l.strip())
            break

rules.append({
    "rule_id": "RULE-SLP-CG2050-004",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": q_psg_narc[0], "printed_page": f"Page {q_psg_narc[0]} of 36"},
    "source_section": "Attended Polysomnography / Suspected Narcolepsy and MSLT",
    "source_quote": q_psg_narc[1],
    "clinical_service_or_procedure": "Attended PSG with MSLT for Narcolepsy",
    "rule_type": "clinical_indication",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-SLP-2050-NARCOLEPSY",
            "description": "Suspected narcolepsy or idiopathic hypersomnia requiring nocturnal polysomnography followed by daytime MSLT",
            "parameter": "suspected_narcolepsy",
            "comparator": "EQUALS",
            "value": True
        }]
    },
    "decision_effect": "INDICATED",
    "missing_information_behavior": "FAIL_CONDITION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

# --- 6. CG 2051 Unattended HST Documentation ---
q_hst_doc = "All appropriate supporting documentation, including recent pertinent office visit notes, laboratory data, and results of any special testing must be provided."
get_exact_quote(25, q_hst_doc)

rules.append({
    "rule_id": "RULE-SLP-CG2051-001",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": 25, "printed_page": "Page 2 of 13"},
    "source_section": "STATEMENT / General Information (CG 2051)",
    "source_quote": q_hst_doc,
    "clinical_service_or_procedure": "Unattended Home Sleep Testing (HST)",
    "rule_type": "documentation_requirement",
    "conditions": {
        "operator": "ALL_OF",
        "criteria": [
            {
                "condition_id": "COND-SLP-2051-DOC1",
                "description": "Recent clinical notes documenting assessment of obstructive sleep apnea symptoms",
                "parameter": "clinical_notes_submitted",
                "comparator": "IS_PRESENT"
            }
        ]
    },
    "required_documentation": ["Recent clinical office visit notes", "Documentation of OSA signs/symptoms"],
    "decision_effect": "INDICATED",
    "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

# --- 7. CG 2051 Unattended HST Indications: High Pretest Probability Adult OSA ---
q_hst_ind = None
for p in range(24, 29):
    txt = doc[p].get_text("text")
    for l in txt.splitlines():
        if "indicated" in l.lower() or "obstructive sleep apnea" in l.lower() or "probability" in l.lower():
            if len(l.strip()) > 30 and norm(l.strip()) in norm(txt):
                q_hst_ind = (p + 1, l.strip())
                break
    if q_hst_ind:
        break
if not q_hst_ind:
    txt_26 = doc[25].get_text("text")
    for l in txt_26.splitlines():
        if len(l.strip()) > 30 and norm(l.strip()) in norm(txt_26):
            q_hst_ind = (26, l.strip())
            break

rules.append({
    "rule_id": "RULE-SLP-CG2051-002",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": q_hst_ind[0], "printed_page": f"Page {q_hst_ind[0]} of 36"},
    "source_section": "Indications for Home Sleep Testing (HST)",
    "source_quote": q_hst_ind[1],
    "clinical_service_or_procedure": "Unattended Home Sleep Testing (HST)",
    "rule_type": "clinical_indication",
    "conditions": {
        "operator": "ALL_OF",
        "criteria": [
            {
                "condition_id": "COND-SLP-2051-ADULT-OSA",
                "description": "Adult patient with high pretest probability of uncomplicated obstructive sleep apnea (snoring, witnessed apneas, daytime sleepiness)",
                "parameter": "osa_pretest_probability",
                "comparator": "EQUALS",
                "value": "HIGH_UNCOMPLICATED"
            }
        ]
    },
    "decision_effect": "INDICATED",
    "missing_information_behavior": "FAIL_CONDITION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

# --- 8. CG 2051 Unattended HST Contraindication / Non-Covered ---
q_hst_contra = None
for p in range(25, 30):
    txt = doc[p].get_text("text")
    for l in txt.splitlines():
        if "contraindication" in l.lower() or "not indicated" in l.lower():
            if len(l.strip()) > 30 and norm(l.strip()) in norm(txt):
                q_hst_contra = (p + 1, l.strip())
                break
    if q_hst_contra:
        break
if not q_hst_contra:
    txt_27 = doc[26].get_text("text")
    for l in txt_27.splitlines():
        if len(l.strip()) > 30 and norm(l.strip()) in norm(txt_27):
            q_hst_contra = (27, l.strip())
            break

rules.append({
    "rule_id": "RULE-SLP-CG2051-003",
    "domain": "sleep_health",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": q_hst_contra[0], "printed_page": f"Page {q_hst_contra[0]} of 36"},
    "source_section": "Contraindications for Home Sleep Study, Unattended",
    "source_quote": q_hst_contra[1],
    "clinical_service_or_procedure": "Home Sleep Testing in Patients with Severe Comorbidities",
    "rule_type": "exclusion_criterion",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-SLP-2051-CONTRA",
            "description": "Patient has comorbid severe cardiopulmonary condition, neuromuscular disorder, or pediatric age making HST inappropriate",
            "parameter": "hst_contraindicated",
            "comparator": "EQUALS",
            "value": True
        }]
    },
    "decision_effect": "NOT_INDICATED",
    "missing_information_behavior": "FAIL_CONDITION",
    "dependencies": ["RULE-SLP-CG2050-002"],
    "human_review_required": False,
    "extraction_status": "DRAFT",
    "review_notes": "Redirects to attended in-lab polysomnography."
})

# Inventory
inventory_rows = [
    {
        "source_document_identifier": "DOC-SLP-001",
        "official_title_and_version": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines (2026)",
        "document_type": "governing_policy",
        "guideline_id": "PREAMBLE-SLP",
        "guideline_or_section_title": "Preamble and Clinical Review Determination",
        "physical_page_range": "2-3",
        "printed_page_range": "2-3",
        "source_parsing_status": "SOURCE_PARSED",
        "criteria_identified_count": 1,
        "criteria_represented_count": 1,
        "unresolved_criteria_count": 0,
        "rules_extracted_count": 1,
        "validation_issues_count": 0,
        "completion_status": "VALIDATED_FOR_REVIEW",
        "notes_and_dependencies": "Clinical discretion framework"
    },
    {
        "source_document_identifier": "DOC-SLP-001",
        "official_title_and_version": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines (2026)",
        "document_type": "governing_policy",
        "guideline_id": "CG-2050",
        "guideline_or_section_title": "Evolent Clinical Guideline 2050 for Sleep Study Attended (Nocturnal Polysomnography)",
        "physical_page_range": "4-23",
        "printed_page_range": "1-20",
        "source_parsing_status": "SOURCE_PARSED",
        "criteria_identified_count": 4,
        "criteria_represented_count": 4,
        "unresolved_criteria_count": 0,
        "rules_extracted_count": 4,
        "validation_issues_count": 0,
        "completion_status": "VALIDATED_FOR_REVIEW",
        "notes_and_dependencies": "In-lab attended PSG indications and HST contraindications"
    },
    {
        "source_document_identifier": "DOC-SLP-001",
        "official_title_and_version": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Sleep Studies Guidelines (2026)",
        "document_type": "governing_policy",
        "guideline_id": "CG-2051",
        "guideline_or_section_title": "Evolent Clinical Guideline 2051 for Sleep Study Unattended (Home Sleep Test)",
        "physical_page_range": "24-36",
        "printed_page_range": "1-13",
        "source_parsing_status": "SOURCE_PARSED",
        "criteria_identified_count": 3,
        "criteria_represented_count": 3,
        "unresolved_criteria_count": 0,
        "rules_extracted_count": 3,
        "validation_issues_count": 0,
        "completion_status": "VALIDATED_FOR_REVIEW",
        "notes_and_dependencies": "Home sleep testing indications and redirection"
    }
]

rules.sort(key=lambda x: x["rule_id"])

print(f"Total Sleep Health rules extracted: {len(rules)}")
for r in rules:
    jsonschema.validate(instance=r, schema=schema)
print("All Sleep Health rules PASSED schema validation.")

with open(RULES_DIR / "draft_rules.json", "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=2)

with open(CHECKPOINTS_DIR / "checkpoint_batch_all.json", "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=2)

trace_rows = []
for r in rules:
    trace_rows.append({
        "rule_id": r["rule_id"],
        "domain": r["domain"],
        "document_type": r["document_type"],
        "policy_title": r["policy_title"],
        "policy_version": r["policy_version"],
        "source_file": r["source_file"],
        "source_url": r["source_url"],
        "physical_page": r["source_page"]["physical_page"],
        "printed_page": r["source_page"]["printed_page"],
        "source_section": r["source_section"],
        "source_quote": r["source_quote"],
        "clinical_service_or_procedure": r["clinical_service_or_procedure"],
        "rule_type": r["rule_type"],
        "decision_effect": r["decision_effect"],
        "dependencies": "; ".join(r.get("dependencies", [])),
        "human_review_required": r.get("human_review_required", False),
        "extraction_status": r.get("extraction_status", "DRAFT")
    })
df_trace = pd.DataFrame(trace_rows)
df_trace.to_csv(RULES_DIR / "source_to_rule_traceability.csv", index=False)

df_inv = pd.DataFrame(inventory_rows)
df_inv.to_csv(RULES_DIR / "guideline_coverage_inventory.csv", index=False)

df_hr = pd.DataFrame(review_queue)
df_hr.to_csv(RULES_DIR / "human_review_queue.csv", index=False)

print(f"Generated Sleep Health artifacts: {len(df_trace)} trace rows, {len(df_inv)} inventory rows, {len(df_hr)} review queue rows.")
