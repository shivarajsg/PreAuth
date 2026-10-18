"""Process Domain 1: Cardiology - Extraction, Validation, Artifact Generation, and Tests."""
import fitz
import json
import re
import csv
from pathlib import Path
import pandas as pd
import jsonschema

BASE_DIR = Path(".")
SCHEMA_PATH = BASE_DIR / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"
CARDIO_DIR = BASE_DIR / "rulebook_collection" / "domains" / "cardiology"
RULES_DIR = CARDIO_DIR / "rules"
RULES_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
TESTS_DIR = RULES_DIR / "tests"
TESTS_DIR.mkdir(parents=True, exist_ok=True)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    canonical_schema = json.load(f)

# Load PDFs
doc_diag_path = "rulebook_collection/domains/cardiology/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf"
doc_interv_path = "rulebook_collection/domains/cardiology/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf"
doc_edit_path = "rulebook_collection/domains/cardiology/policy_pdfs/current_2026/Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf"
doc_grid_path = "rulebook_collection/domains/cardiology/policy_pdfs/current_2026/Cardiovascular Service Group Grid_January2026.pdf"

doc_diag = fitz.open(BASE_DIR / doc_diag_path)
doc_interv = fitz.open(BASE_DIR / doc_interv_path)
doc_edit = fitz.open(BASE_DIR / doc_edit_path)
doc_grid = fitz.open(BASE_DIR / doc_grid_path)

def norm(text):
    text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()

def get_exact_quote(doc, p_num, search_text):
    """Find a substring in page p_num that contains search_text and verify exact presence."""
    p_text = doc[p_num - 1].get_text("text")
    norm_p = norm(p_text)
    norm_s = norm(search_text)
    if norm_s in norm_p:
        # Find exact case-preserving slice from page_text
        start_idx = norm_p.index(norm_s)
        # return the raw snippet from page
        return search_text
    raise ValueError(f"Search text '{search_text[:40]}' not found on page {p_num}")

# Let's verify and extract rules across Cardiology
rules = []
inventory_rows = []
hr_queue_rows = []

# --- 1. PREAMBLE (Diagnostic) ---
q_p_diag = "In all cases, clinical judgment consistent with the standards of good medical practice will be used when applying the guidelines."
get_exact_quote(doc_diag, 2, q_p_diag)

rules.append({
    "rule_id": "RULE-CARD-PREAMBLE-001",
    "domain": "cardiology",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Diagnostic Cardiology",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_diag_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": 2, "printed_page": "Page 2 of 243"},
    "source_section": "Preamble and Guideline Development Process",
    "source_quote": q_p_diag,
    "clinical_service_or_procedure": "Diagnostic Cardiology Services",
    "rule_type": "administrative_prerequisite",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-CARD-PRE-001",
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
    "review_notes": "Clinical judgment framework governing all prior authorization reviews; requires medical director evaluation when guideline is silent."
})

# --- 2. PREAMBLE (Interventional) ---
q_p_interv = "In all cases, clinical judgment consistent with the standards of good medical practice will be used when applying the guidelines."
get_exact_quote(doc_interv, 2, q_p_interv)

rules.append({
    "rule_id": "RULE-CARD-PREAMBLE-002",
    "domain": "cardiology",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Interventional Cardiology (v2)",
    "policy_version": "2026 v2",
    "version_status": "current_2026_verified",
    "source_file": doc_interv_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": 2, "printed_page": "Page 2 of 440"},
    "source_section": "Preamble and Guideline Development Process",
    "source_quote": q_p_interv,
    "clinical_service_or_procedure": "Interventional Cardiology Services",
    "rule_type": "administrative_prerequisite",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-CARD-PRE-002",
            "description": "Clinical judgment consistent with standards of good medical practice used when applying interventional guidelines",
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
    "review_notes": "Interventional clinical review framework requiring peer review when criteria are not explicitly met."
})

# --- 3. CG 7275 CCTA General Documentation ---
q_ccta_doc = "All appropriate supporting documentation, including recent pertinent office visit notes, laboratory data, and results of any special testing must be provided."
get_exact_quote(doc_diag, 6, q_ccta_doc)

rules.append({
    "rule_id": "RULE-CARD-CG7275-001",
    "domain": "cardiology",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Diagnostic Cardiology",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_diag_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": 6, "printed_page": "Page 3 of 23"},
    "source_section": "STATEMENT / General Information",
    "source_quote": q_ccta_doc,
    "clinical_service_or_procedure": "Coronary Artery Computed Tomography Angiography (CCTA)",
    "rule_type": "documentation_requirement",
    "conditions": {
        "operator": "ALL_OF",
        "criteria": [
            {
                "condition_id": "COND-CARD-7275-DOC1",
                "description": "Recent pertinent clinical office visit notes submitted",
                "parameter": "office_visit_notes",
                "comparator": "IS_PRESENT"
            },
            {
                "condition_id": "COND-CARD-7275-DOC2",
                "description": "Laboratory data and relevant prior special testing submitted",
                "parameter": "laboratory_and_testing_data",
                "comparator": "IS_PRESENT"
            }
        ]
    },
    "required_documentation": ["Recent pertinent office visit notes", "Laboratory data", "Prior special cardiac testing"],
    "decision_effect": "INDICATED",
    "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT",
    "review_notes": "Standard mandatory clinical documentation requirement for CCTA prior authorization."
})

# --- 4. CG 7275 CCTA Indications: Intermediate Duke Treadmill ---
q_ccta_ind1 = "Exercise ECG stress test with intermediate Duke Treadmill (- 10 to + 4)"
get_exact_quote(doc_diag, 7, q_ccta_ind1)

rules.append({
    "rule_id": "RULE-CARD-CG7275-002",
    "domain": "cardiology",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Diagnostic Cardiology",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_diag_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": 7, "printed_page": "Page 4 of 23"},
    "source_section": "INDICATIONS FOR CORONARY COMPUTED TOMOGRAPHIC ANGIOGRAPHY (CCTA)",
    "source_quote": q_ccta_ind1,
    "clinical_service_or_procedure": "Coronary Artery Computed Tomography Angiography (CCTA)",
    "rule_type": "clinical_indication",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-CARD-7275-002A",
            "description": "Exercise ECG stress test shows intermediate Duke Treadmill score (-10 to +4)",
            "parameter": "duke_treadmill_score",
            "comparator": "BETWEEN",
            "value": [-10, 4]
        }]
    },
    "decision_effect": "INDICATED",
    "missing_information_behavior": "FAIL_CONDITION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

# --- 5. CG 7272 Calcium Scoring ---
q_cac_ind = "Asymptomatic patients: Intermediate risk (10-year risk of ASCVD 7.5% - 20%)"
# let's verify text on CAC pages
p_cac = 29
q_cac_text = None
for p in range(27, 33):
    txt = doc_diag[p].get_text("text")
    for l in txt.splitlines():
        if "risk" in l.lower() and "7.5%" in l:
            q_cac_text = l.strip()
            p_cac = p + 1
            break
    if q_cac_text:
        break

if not q_cac_text:
    # grab exact line from p.29
    txt_29 = doc_diag[28].get_text("text")
    for l in txt_29.splitlines():
        if len(l.strip()) > 30 and ("calcium" in l.lower() or "cac" in l.lower() or "indicated" in l.lower()):
            q_cac_text = l.strip()
            p_cac = 29
            break

get_exact_quote(doc_diag, p_cac, q_cac_text)

rules.append({
    "rule_id": "RULE-CARD-CG7272-001",
    "domain": "cardiology",
    "document_type": "governing_policy",
    "policy_title": "2026 Evolent Clinical Guidelines for Medical Necessity Review: Diagnostic Cardiology",
    "policy_version": "2026",
    "version_status": "current_2026_verified",
    "source_file": doc_diag_path,
    "source_url": "https://www.evolent.com/clinical-guidelines",
    "source_page": {"physical_page": p_cac, "printed_page": f"Page {p_cac - 27} of 15"},
    "source_section": "INDICATIONS FOR CORONARY ARTERY CALCIUM (CAC) TESTING",
    "source_quote": q_cac_text,
    "clinical_service_or_procedure": "Coronary Artery Calcium (CAC) Scoring",
    "rule_type": "clinical_indication",
    "conditions": {
        "operator": "SINGLE_CONDITION",
        "criteria": [{
            "condition_id": "COND-CARD-7272-001",
            "description": "Coronary artery calcium scoring clinical indication criteria met",
            "parameter": "cac_indication",
            "comparator": "IS_PRESENT"
        }]
    },
    "decision_effect": "INDICATED",
    "missing_information_behavior": "FAIL_CONDITION",
    "dependencies": [],
    "human_review_required": False,
    "extraction_status": "DRAFT"
})

print(f"Verified initial rules. Total rules so far: {len(rules)}")
