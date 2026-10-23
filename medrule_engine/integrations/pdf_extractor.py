"""Clinical PDF and Physician Notes Information Extraction Module.

Extracts structured prior-authorization intake parameters from clinical PDF documents,
such as EHR clinical progress notes, physician orders, diagnostic reports, and consult notes.
"""

from datetime import datetime
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

import pymupdf as fitz

logger = logging.getLogger(__name__)

# Canonical procedure knowledge mapping
PROCEDURE_CATALOG = {
    "74177": {
        "code": "74177",
        "name": "CT Abdomen and Pelvis with contrast",
        "domain": "advanced_imaging",
        "keywords": ["ct abdomen", "ct pelvis", "ct abdomen/pelvis", "pancreatitis", "abdominal pain", "diverticulitis"]
    },
    "74176": {
        "code": "74176",
        "name": "CT Abdomen and Pelvis without contrast",
        "domain": "advanced_imaging",
        "keywords": ["ct abdomen", "without contrast", "renal calculus", "kidney stone"]
    },
    "74178": {
        "code": "74178",
        "name": "CT Abdomen and Pelvis with and without contrast",
        "domain": "advanced_imaging",
        "keywords": ["ct abdomen", "with & without", "with and without", "biphasic ct"]
    },
    "70553": {
        "code": "70553",
        "name": "MRI Brain with and without contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri brain", "brain mri", "headache", "neuropathy", "acoustic neuroma", "seizure"]
    },
    "70552": {
        "code": "70552",
        "name": "MRI Brain with contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri brain with", "brain mri with contrast"]
    },
    "70551": {
        "code": "70551",
        "name": "MRI Brain without contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri brain without", "dementia", "stroke", "infarct"]
    },
    "70450": {
        "code": "70450",
        "name": "CT Head / Brain without contrast",
        "domain": "advanced_imaging",
        "keywords": ["ct head", "ct brain", "head ct without contrast", "head trauma", "hemorrhage"]
    },
    "71250": {
        "code": "71250",
        "name": "CT Thorax / Chest without contrast",
        "domain": "advanced_imaging",
        "keywords": ["ct chest", "ct thorax", "pulmonary nodule", "ldct", "lung cancer screen"]
    },
    "71260": {
        "code": "71260",
        "name": "CT Thorax / Chest with contrast",
        "domain": "advanced_imaging",
        "keywords": ["ct chest with contrast", "ct thorax with contrast", "mediastinal adenopathy"]
    },
    "72148": {
        "code": "72148",
        "name": "MRI Lumbar Spine without contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri lumbar", "lumbar spine", "back pain", "herniated disc", "radiculopathy"]
    },
    "72149": {
        "code": "72149",
        "name": "MRI Lumbar Spine with contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri lumbar with", "lumbar spine with contrast"]
    },
    "72158": {
        "code": "72158",
        "name": "MRI Lumbar Spine with and without contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri lumbar with and without", "lumbar spine with & without"]
    },
    "73721": {
        "code": "73721",
        "name": "MRI Lower Extremity Joint (Knee) without contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri knee", "knee mri", "meniscus", "meniscal tear", "cruciate ligament", "acl"]
    },
    "73722": {
        "code": "73722",
        "name": "MRI Lower Extremity Joint (Knee) with contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri knee with contrast", "knee mri with contrast"]
    },
    "73723": {
        "code": "73723",
        "name": "MRI Lower Extremity Joint (Knee) with and without contrast",
        "domain": "advanced_imaging",
        "keywords": ["mri knee with and without", "knee mri with & without"]
    },
    "78815": {
        "code": "78815",
        "name": "PET/CT Skull to Mid-Thigh",
        "domain": "advanced_imaging",
        "keywords": ["pet/ct", "pet scan", "positron emission", "metabolic tumor", "staging"]
    },
    "93458": {
        "code": "93458",
        "name": "Left Heart Catheterization with Coronary Angiogram",
        "domain": "cardiology",
        "keywords": ["coronary angiogram", "heart cath", "cardiac catheterization", "ischemia", "cad", "angina"]
    },
    "93459": {
        "code": "93459",
        "name": "Left Heart Catheterization with Bypass Graft Angiogram",
        "domain": "cardiology",
        "keywords": ["cabg angiogram", "bypass graft", "left heart catheterization with bypass"]
    },
    "93306": {
        "code": "93306",
        "name": "Transthoracic Echocardiography (TTE) Complete",
        "domain": "cardiology",
        "keywords": ["echocardiogram", "tte", "ejection fraction", "valvular", "heart failure"]
    },
    "93350": {
        "code": "93350",
        "name": "Stress Echocardiography",
        "domain": "cardiology",
        "keywords": ["stress echo", "stress echocardiography", "exercise stress", "dobutamine"]
    },
    "27447": {
        "code": "27447",
        "name": "Total Knee Arthroplasty (TKA)",
        "domain": "musculoskeletal_surgery",
        "keywords": ["total knee", "knee arthroplasty", "tka", "osteoarthritis", "tricompartmental"]
    },
    "27130": {
        "code": "27130",
        "name": "Total Hip Arthroplasty (THA)",
        "domain": "musculoskeletal_surgery",
        "keywords": ["total hip", "hip arthroplasty", "tha", "avascular necrosis", "hip osteoarthritis"]
    },
    "22612": {
        "code": "22612",
        "name": "Lumbar Spine Fusion (Arthrodesis)",
        "domain": "musculoskeletal_surgery",
        "keywords": ["spine fusion", "lumbar fusion", "spondylolisthesis", "arthrodesis"]
    },
    "62322": {
        "code": "62322",
        "name": "Lumbar/Sacral Epidural Steroid Injection without imaging",
        "domain": "interventional_pain_management",
        "keywords": ["epidural steroid without", "lesi without imaging", "esi non-guided"]
    },
    "62323": {
        "code": "62323",
        "name": "Lumbar Epidural Steroid Injection with imaging",
        "domain": "interventional_pain_management",
        "keywords": ["epidural steroid", "lesi", "esi", "lumbar epidural", "nerve root injection", "fluoroscopic epidural"]
    },
    "64483": {
        "code": "64483",
        "name": "Lumbar or Sacral Transforaminal Epidural Steroid Injection",
        "domain": "interventional_pain_management",
        "keywords": ["transforaminal", "tfesi", "epidural injection", "nerve root block"]
    },
    "64484": {
        "code": "64484",
        "name": "Lumbar or Sacral Transforaminal Epidural Steroid Injection, add'l level",
        "domain": "interventional_pain_management",
        "keywords": ["transforaminal additional", "tfesi add'l level"]
    },
    "64490": {
        "code": "64490",
        "name": "Facet Joint Injection / Medial Branch Block (Lumbar)",
        "domain": "interventional_pain_management",
        "keywords": ["facet joint", "medial branch block", "facet injection", "lumbar facet"]
    },
    "64493": {
        "code": "64493",
        "name": "Facet Joint Injection / Medial Branch Block, add'l level",
        "domain": "interventional_pain_management",
        "keywords": ["facet joint additional", "medial branch block add'l"]
    },
    "63650": {
        "code": "63650",
        "name": "Percutaneous Spinal Cord Stimulator Lead Trial",
        "domain": "interventional_pain_management",
        "keywords": ["spinal cord stimulator", "scs trial", "neurostimulator", "failed back surgery"]
    },
    "77301": {
        "code": "77301",
        "name": "Intensity Modulated Radiation Therapy (IMRT) Plan",
        "domain": "radiation_oncology",
        "keywords": ["imrt", "intensity modulated", "radiation plan", "prostate cancer", "sparing"]
    },
    "77385": {
        "code": "77385",
        "name": "Intensity Modulated Radiation Therapy Delivery",
        "domain": "radiation_oncology",
        "keywords": ["radiation delivery", "imrt delivery", "fractionation"]
    },
    "97110": {
        "code": "97110",
        "name": "Therapeutic Exercises, Outpatient Physical Therapy",
        "domain": "physical_medicine",
        "keywords": ["physical therapy", "therapeutic exercise", "pt evaluation", "rehabilitation"]
    },
    "97140": {
        "code": "97140",
        "name": "Manual Therapy Techniques",
        "domain": "physical_medicine",
        "keywords": ["manual therapy", "joint mobilization", "myofascial release"]
    },
    "95806": {
        "code": "95806",
        "name": "Unattended Sleep Study / Home Sleep Apnea Test",
        "domain": "sleep_health",
        "keywords": ["sleep study", "hsat", "home sleep", "apnea test", "epworth", "snoring"]
    },
    "95810": {
        "code": "95810",
        "name": "Polysomnography Diagnostic",
        "domain": "sleep_health",
        "keywords": ["polysomnography", "psg", "in-lab sleep study", "sleep apnea diagnostic"]
    },
    "81162": {
        "code": "81162",
        "name": "BRCA1, BRCA2 Gene Analysis Full Sequence & Duplication/Deletion",
        "domain": "genetic_testing",
        "keywords": ["brca", "brca1", "brca2", "genetic test", "hereditary breast", "gene analysis"]
    },
    "81432": {
        "code": "81432",
        "name": "Hereditary Breast Cancer-Related Multi-Gene Panel",
        "domain": "genetic_testing",
        "keywords": ["multi-gene panel", "hereditary cancer panel", "breast ovarian panel"]
    },
    "A9276": {
        "code": "A9276",
        "name": "Sensor; invasive, disposable, for use with CGM system",
        "domain": "centene_dme_orthotics_prosthetics",
        "keywords": ["cgm", "continuous glucose", "sensor", "dexcom", "freestyle", "type 1 diabetes"]
    },
    "E0601": {
        "code": "E0601",
        "name": "Continuous Positive Airway Pressure (CPAP) Device",
        "domain": "centene_dme_orthotics_prosthetics",
        "keywords": ["cpap device", "cpap machine", "airway pressure", "resmed"]
    },
    "K0823": {
        "code": "K0823",
        "name": "Power Wheelchair Group 2 Standard",
        "domain": "centene_dme_orthotics_prosthetics",
        "keywords": ["power wheelchair", "mobility device", "electric wheelchair", "wheelchair"]
    },
    "E0260": {
        "code": "E0260",
        "name": "Hospital Bed, Semi-Electric with Mattress",
        "domain": "centene_dme_orthotics_prosthetics",
        "keywords": ["hospital bed", "semi-electric", "mattress", "head adjustment", "elevation"]
    }
}


def _extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Tuple[str, int]:
    """Read full text and page count from in-memory PDF bytes."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        num_pages = len(doc)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n".join(text_parts), num_pages
    except Exception as exc:
        logger.warning("Failed to extract text from PDF stream: %s", exc)
        return "", 0


def _detect_patient_id(text: str) -> str:
    """Find patient/member identifier or clean medical record number."""
    # Check for direct MEM- pattern if present in clinical header
    m = re.search(r"\b(MEM-[A-Z0-9\-]+)\b", text, re.IGNORECASE)
    if m:
        return m.group(1).upper()

    # Check for Member ID / Subscriber ID / Insurance ID
    patterns = [
        r"(?:Member|Subscriber|Policy|Insurance)\s*(?:ID|#|Number|No\.?)?\s*[:#]?\s*([A-Z0-9\-]{5,20})",
        r"\bMRN\s*[:#]?\s*([A-Z0-9\-]{4,16})",
        r"\b(?:Patient\s*ID|Chart\s*#|Acct\s*#)\s*[:#]?\s*([A-Z0-9\-]{4,16})"
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip()
            if val.lower() not in ["number", "patient", "clinical", "hospital", "evaluation", "examination"]:
                return f"PT-{val.upper()}"

    # Check for Patient Name to generate a clean clinical reference
    pat_name_match = re.search(r"(?:Patient|Patient\s*Name|Name)\s*[:#]?\s*([A-Z][a-z]+)\s+([A-Z][a-z]+)", text)
    if pat_name_match:
        last = pat_name_match.group(2).upper()
        first = pat_name_match.group(1).upper()
        return f"PT-{last}-{first[:3]}"

    timestamp = int(datetime.now().timestamp()) % 100000
    return f"PT-{timestamp}"


def _detect_procedure_and_domain(text: str) -> Tuple[str, str, str]:
    """Identify procedure code, procedure name, and clinical domain from notes."""
    text_lower = text.lower()

    # 1. Look for explicit CPT / HCPCS code declaration (e.g., CPT 72148, Procedure Code: 99999)
    explicit_cpt = re.search(r"\b(?:CPT|HCPCS|Procedure\s*Code|Code)\s*[:#]?\s*([0-9]{5}|[A-Z][0-9]{4})\b", text, re.IGNORECASE)
    if explicit_cpt:
        code_found = explicit_cpt.group(1).upper()
        if code_found in PROCEDURE_CATALOG:
            info = PROCEDURE_CATALOG[code_found]
            return info["code"], info["name"], info["domain"]
        domain = _detect_domain_from_keywords(text_lower)
        name_match = re.search(rf"(?:Requested Procedure|Procedure|CPT|Code)?\s*[:#]?\s*([A-Za-z0-9\s,\(\)/]{{4,60}}?)\s*\(?CPT\s*{re.escape(code_found)}", text, re.IGNORECASE)
        proc_name = name_match.group(1).strip() if name_match else f"Requested Procedure ({code_found})"
        return code_found, proc_name, domain

    # 2. Look for exact known CPT / HCPCS codes standalone in text
    for code, info in PROCEDURE_CATALOG.items():
        if re.search(rf"\b{re.escape(code)}\b", text):
            return info["code"], info["name"], info["domain"]

    # 3. Look for keywords matching specific procedures
    best_match = None
    max_score = 0
    for code, info in PROCEDURE_CATALOG.items():
        score = sum(1 for kw in info["keywords"] if kw in text_lower)
        if score > max_score:
            max_score = score
            best_match = info

    if best_match and max_score >= 1:
        return best_match["code"], best_match["name"], best_match["domain"]

    # 4. Default fallback to advanced imaging
    domain = _detect_domain_from_keywords(text_lower)
    return "74177", "CT Abdomen and Pelvis with contrast", domain


def _detect_domain_from_keywords(text_lower: str) -> str:
    """Infer clinical domain based on keyword frequency."""
    domain_weights = {
        "cardiology": ["cardio", "angio", "catheter", "heart", "ischemia", "angina", "troponin", "stemi", "nstemi", "coronary"],
        "advanced_imaging": ["ct scan", "mri", "ultrasound", "pet scan", "radiology", "contrast", "abdomen", "pelvis", "tomography"],
        "musculoskeletal_surgery": ["arthroplasty", "knee", "hip", "orthopedic", "osteoarthritis", "meniscal", "joint replacement", "spine fusion"],
        "interventional_pain_management": ["epidural", "facet", "steroid injection", "nerve block", "radiculopathy", "pain management", "scs"],
        "radiation_oncology": ["radiation", "imrt", "sbrt", "oncology", "brachytherapy", "carcinoma", "tumor", "gleason", "prostate"],
        "physical_medicine": ["physical therapy", "occupational therapy", "therapeutic exercise", "rehabilitation", "functional deficit", "gait"],
        "sleep_health": ["sleep apnea", "polysomnography", "hsat", "snoring", "epworth", "cpap", "ahi", "respiratory disturbance"],
        "genetic_testing": ["brca", "gene", "mutation", "sequencing", "genetic counseling", "hereditary", "pedigree", "dna"],
        "centene_dme_orthotics_prosthetics": ["wheelchair", "dme", "prosthetic", "orthotic", "continuous glucose", "cgm", "insulin", "glucometer", "sensor", "hospital bed"]
    }

    scores = {}
    for dom, kws in domain_weights.items():
        scores[dom] = sum(1 for kw in kws if kw in text_lower)

    best_domain = max(scores.items(), key=lambda x: x[1])
    if best_domain[1] > 0:
        return best_domain[0]
    return "advanced_imaging"


def _detect_line_of_business(text: str) -> str:
    """Extract line of business from text."""
    text_lower = text.lower()
    if "medicare advantage" in text_lower or "part c" in text_lower or "medicare" in text_lower:
        return "MEDICARE_ADVANTAGE"
    if "medicaid" in text_lower or "managed medicaid" in text_lower or "chip" in text_lower:
        return "MEDICAID"
    return "COMMERCIAL"


def _detect_date_of_service(text: str) -> str:
    """Extract requested date of service from clinical note; preserve documented year.

    Does NOT clamp prior-year encounter dates (e.g. 2025-02-26) to the current year.
    The encounter date recorded in the clinical note is authoritative.
    """
    patterns = [
        r"(?:Date of Service|DOS|Requested Date|Encounter Date|Service Date)\s*[:#]?\s*([0-9]{4}[\-/][0-9]{1,2}[\-/][0-9]{1,2})",
        r"(?:Date of Service|DOS|Requested Date|Encounter Date|Service Date)\s*[:#]?\s*([0-9]{1,2}[\-/][0-9]{1,2}[\-/][0-9]{2,4})",
        r"\b(DOS)\s*[:#]?\s*([0-9]{1,2}[\-/][0-9]{1,2}[\-/][0-9]{2,4})\b",
        r"\b([0-9]{4}-[0-9]{2}-[0-9]{2})\b"
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if not m:
            continue
        # Pattern with a two-group DOS label uses group(2); others use group(1)
        raw_date = (m.group(2) if m.lastindex and m.lastindex >= 2 and m.group(2) else m.group(1)).replace("/", "-")
        parts = raw_date.split("-")
        try:
            if len(parts) == 3:
                if len(parts[0]) == 4:  # YYYY-MM-DD
                    y, mm, d = int(parts[0]), int(parts[1]), int(parts[2])
                else:  # MM-DD-YYYY
                    mm, d, y = int(parts[0]), int(parts[1]), int(parts[2])
                    if y < 100:
                        y += 2000
                # Validate the date; reject implausible years (pre-2000 or far future)
                if 2000 <= y <= 2099 and 1 <= mm <= 12 and 1 <= d <= 31:
                    return f"{y:04d}-{mm:02d}-{d:02d}"
        except Exception:
            pass
    return datetime.now().strftime("%Y-%m-%d")


def _detect_payer_and_plan(text: str, lob: str) -> Tuple[str, str]:
    """Infer payer identifier and plan name."""
    text_lower = text.lower()
    if "centene" in text_lower or "superior" in text_lower or "sunshine" in text_lower or "ambetter" in text_lower:
        payer = "CENTENE"
    else:
        payer = "EVOLENT"

    if lob == "MEDICARE_ADVANTAGE":
        plan = "MEDICARE_ADVANTAGE_PREMIER"
    elif lob == "MEDICAID":
        plan = "MEDICAID_COMMUNITY_CHOICE"
    else:
        plan = "COMMERCIAL_CHOICE_PLUS"

    return payer, plan


def _split_into_sentences(text: str) -> List[str]:
    """Split text into individual sentences for contextual analysis, handling soft PDF linebreaks and honorifics."""
    # Reconnect lines wrapped across soft linebreaks in PDFs (non-terminal punctuation followed by lowercase or continuation)
    normalized = re.sub(r'([^\.\:\;\?\!\|\n])\n+([a-z0-9])', r'\1 \2', text)
    safe = re.sub(r'\b(Dr|Doctor|Mr|Mrs|Ms|vs|e\.g|i\.e)\.', r'\1_DOT_', normalized)
    raw = re.split(r'(?:\.\s+|\n+|;\s+|•\s+|\|\s+)', safe)
    return [s.replace('_DOT_', '.').strip() for s in raw if s.strip()]


def _is_negated_in_sentence(sentence: str, target: str) -> bool:
    """Check if target keyword is explicitly negated in sentence."""
    s_lower = sentence.lower()
    t_lower = target.lower()
    if t_lower not in s_lower:
        return False

    neg_cues = [
        r"\bno\b", r"\bnot\b", r"\bdenies\b", r"\bdenied\b", r"\bwithout\b",
        r"\babsence of\b", r"\bnegative for\b", r"\brules out\b", r"\bruled out\b",
        r"\bnone\b", r"\bno evidence of\b", r"\bunremarkable\b", r"\bintact\b"
    ]
    for cue in neg_cues:
        pattern1 = rf"{cue}\s+(?:[\w\-,\/]+\s+){{0,10}}{re.escape(t_lower)}"
        pattern2 = rf"{re.escape(t_lower)}\s+(?:is|are|was|were)?\s*(?:ruled out|negative|denied|absent|none|unremarkable|intact)"
        if re.search(pattern1, s_lower) or re.search(pattern2, s_lower):
            return True
    return False


def _detect_laterality_and_anatomy(text: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract laterality and anatomical region from text."""
    t_lower = text.lower()
    laterality = None
    if re.search(r"\b(?:bilateral|both)\b", t_lower):
        laterality = "BILATERAL"
    elif re.search(r"\b(?:right|rt)\b", t_lower):
        laterality = "RIGHT"
    elif re.search(r"\b(?:left|lt)\b", t_lower):
        laterality = "LEFT"

    anatomy = None
    if any(k in t_lower for k in ("lumbar", "l1", "l2", "l3", "l4", "l5", "s1")):
        anatomy = "LUMBAR_SPINE"
    elif any(k in t_lower for k in ("cervical", "c-spine")):
        anatomy = "CERVICAL_SPINE"
    elif any(k in t_lower for k in ("thoracic", "t-spine")):
        anatomy = "THORACIC_SPINE"
    elif "knee" in t_lower:
        anatomy = "KNEE"
    elif "hip" in t_lower:
        anatomy = "HIP"
    elif any(k in t_lower for k in ("brain", "head", "cranial")):
        anatomy = "BRAIN"
    elif any(k in t_lower for k in ("abdomen", "pelvis")):
        anatomy = "ABDOMEN_PELVIS"
    elif any(k in t_lower for k in ("chest", "thorax", "lung")):
        anatomy = "CHEST"

    return laterality, anatomy


def _detect_place_of_service(text: str) -> Tuple[str, str]:
    """Extract requested place of service from text. Returns (pos_enum, pos_code)."""
    t_lower = text.lower()
    if re.search(r"\b(?:hospital\s*outpatient|outpatient\s*hospital|hopd|hospital\s*department)\b", t_lower):
        return "OUTPATIENT_HOSPITAL", "POS_22"
    elif re.search(r"\b(?:ambulatory\s*(?:surgical|surgery)\s*center|asc|freestanding)\b", t_lower):
        return "AMBULATORY_SURGICAL_CENTER", "POS_24"
    elif re.search(r"\b(?:inpatient|hospital\s*admission|admitted)\b", t_lower):
        return "INPATIENT_HOSPITAL", "POS_21"
    else:
        return "OFFICE", "POS_11"


def _normalise_name_whitespace(raw: str) -> str:
    """Collapse non-breaking spaces, tabs, newlines within a captured name token.

    PDF text extraction often uses \xa0 (NBSP) instead of regular spaces and
    may include a newline followed by a continuation label (e.g. '\\nDate').  Both
    must be cleaned before storing the provider name.
    """
    # Replace NBSP and other Unicode spacing with a regular space
    name = re.sub(r'[\xa0\u2009\u200b]+', ' ', raw)
    # Truncate at first newline (labels like '\nDate:' are not part of the name)
    name = name.split('\n')[0].split('\r')[0]
    # Collapse multiple consecutive spaces
    name = re.sub(r' {2,}', ' ', name)
    return name.strip()


def _detect_provider_name_and_provenance(text: str) -> Tuple[Optional[str], str]:
    """Robustly extract ordering provider name and snippet from clinical note headers, labels, and signatures."""
    blacklist = {
        "physician", "provider", "attending", "doctor", "specialist", "clinician",
        "md", "do", "mbbs", "phd", "facility", "practice", "clinic", "hospital",
        "spine", "orthopedic", "orthopedics", "department", "center", "order", "note",
        "progress", "consultation", "medical", "patient", "clinical",
        "date", "dos", "acc", "dob", "phone", "fax", "npi", "tel"
    }

    # 1. Explicit labeled field with delimiter (: or - or #)
    label_pattern = re.compile(
        r"(?:Attending\s+Physician|Ordering\s+Physician|Ordering\s+Provider|Attending\s+Doctor|Ordering\s+Clinician|Attending|Provider|Physician|Doctor)\s*[:#\-]\s*"
        r"(?:(?:Dr\.|Doctor)\s+)?"
        r"([A-Z][a-zA-Z\.\'\-]+(?:[^\S\r\n]+[A-Z][a-zA-Z\.\'\-]+){0,3})"
        r"(\s*,\s*(?:MD|DO|MBBS|PhD|NP|PA-C|PA|DC|DPM|FACS)(?:\s*,\s*[A-Za-z0-9\-]+)*)?",
        re.IGNORECASE
    )
    for m in label_pattern.finditer(text):
        name = m.group(1).strip()
        creds = m.group(2).strip() if m.group(2) else ""
        first_token = name.split()[0].lower()
        if first_token not in blacklist and len(name) >= 2:
            full = f"Dr. {name}{creds}" if not name.lower().startswith("dr.") and creds else f"{name}{creds}"
            return full, m.group(0).strip()

    # 2. Signature line e.g. "Dr. Yu, MD - Attending Spine & Orthopedic Specialist"
    sig_pattern = re.compile(
        r"(?:(?:Dr\.|Doctor)\s+)?([A-Z][a-zA-Z\.\'\-]+(?:[^\S\r\n]+[A-Z][a-zA-Z\.\'\-]+){0,3})\s*,\s*(MD|DO|MBBS)\s*-\s*(?:Attending|Treating|Ordering|Staff|Consulting)",
        re.IGNORECASE
    )
    m_sig = sig_pattern.search(text)
    if m_sig:
        name = m_sig.group(1).strip()
        cred = m_sig.group(2).strip().upper()
        if name.split()[0].lower() not in blacklist and len(name) >= 2:
            full = f"Dr. {name}, {cred}" if not name.lower().startswith("dr.") else f"{name}, {cred}"
            return full, m_sig.group(0).strip()

    # 3. Electronic signature e.g. "Electronically signed by KEWEI YU, MD on 05/19/2025"
    e_sig_pattern = re.compile(
        r"Electronically\s+signed\s+by\s+(?:(?:Dr\.|Doctor)\s+)?([A-Z][a-zA-Z\.\'\-]+(?:[^\S\r\n]+[A-Z][a-zA-Z\.\'\-]+){0,3})"
        r"(\s*,\s*(?:MD|DO|MBBS|PhD|NP|PA-C|PA|DC|DPM|FACS)(?:\s*,\s*[A-Za-z0-9\-]+)*)?",
        re.IGNORECASE
    )
    m_esig = e_sig_pattern.search(text)
    if m_esig:
        name = m_esig.group(1).strip()
        creds = m_esig.group(2).strip() if m_esig.group(2) else ""
        first_token = name.split()[0].lower()
        if first_token not in blacklist and len(name) >= 2:
            full = f"Dr. {name}{creds}" if not name.lower().startswith("dr.") and creds else f"{name}{creds}"
            return full, m_esig.group(0).strip()

    # 4. Standalone "Dr. <FirstName> <LastName>, <Credentials>"
    dr_pattern = re.compile(
        r"\b(?:Dr\.|Doctor)\s+([A-Z][a-zA-Z\.\'\-]+(?:[^\S\r\n]+[A-Z][a-zA-Z\.\'\-]+){0,3})"
        r"(\s*,\s*(?:MD|DO|MBBS|PhD|NP|PA|DC|DPM))?",
        re.IGNORECASE
    )
    for m in dr_pattern.finditer(text):
        name = m.group(1).strip()
        creds = m.group(2).strip() if m.group(2) else ""
        first_token = name.split()[0].lower()
        if first_token not in blacklist and len(name) >= 2:
            return f"Dr. {name}{creds}", m.group(0).strip()

    return None, ""


def _detect_provider_license_evidence(text: str) -> Tuple[Optional[str], Optional[str], bool, str]:
    """Extract provider credentials, license number, and verified licensure status.

    Returns:
        Tuple[Optional[str], Optional[str], bool, str]:
            (credentials, license_number, is_verified, snippet)
    """
    # 1. Credentials
    cred_match = re.search(r"\b(MD|DO|MBBS|PhD|NP|PA-C|PA|DC|DPM)\b", text)
    creds = cred_match.group(1).upper() if cred_match else None

    # 2. License number
    license_num = None
    lic_snippet = ""
    for lic_match in re.finditer(
        r"\b(?:State\s+Medical\s+License|Medical\s+License|State\s*Lic(?:ense)?|Lic(?:ense)?\s*(?:#|no\.?|num(?:ber)?)|License)\s*[:#]?\s*([A-Za-z0-9\-]+)",
        text,
        re.IGNORECASE
    ):
        cand = lic_match.group(1).strip()
        if cand.lower() not in ("number", "active", "verified", "pending", "none", "not", "is", "required", "requested", "status"):
            license_num = cand
            lic_snippet = lic_match.group(0).strip()
            break

    if not license_num:
        # Check electronic signature identifier e.g. KEWEI YU, MD, GAA-NP000612
        sig_id_match = re.search(
            r"Electronically\s+signed\s+by[^\.\n]+?,\s*(?:MD|DO|NP|PA|MBBS)\s*,\s*([A-Z]{2,4}-[A-Z0-9]{5,12}|[A-Z0-9]{6,12})",
            text,
            re.IGNORECASE
        )
        if sig_id_match:
            license_num = sig_id_match.group(1).strip()
            lic_snippet = sig_id_match.group(0).strip()

    # 3. Verified licensure status
    # Must have explicit evidence of active verified licensure in the record
    is_verified = False
    verif_match = re.search(
        r"\b(?:active\s+verified|state\s+medical\s+license\s*:\s*active\s+verified|physician\s+license\s*:\s*active\s+verified|verified\s+license|license\s+status\s*:\s*active|license\s+verified)\b",
        text,
        re.IGNORECASE
    )
    if verif_match:
        is_verified = True
        lic_snippet = verif_match.group(0).strip()

    return creds, license_num, is_verified, lic_snippet


def _is_qualifying_office_visit_note(text: str) -> Tuple[bool, str]:
    """Determine whether the uploaded document content is a qualifying clinical office visit note.

    Requirements:
      1. Clinical encounter document header/type.
      2. Encounter date or date of service.
      3. Clinical encounter content: at least 2 of (History/HPI, Physical Exam/Vitals, Assessment/Plan).
      4. Documented provider identification.

    Returns:
        Tuple[bool, str]: (is_qualifying, snippet)
    """
    text_low = text.lower()

    # Check for pure non-qualifying administrative/billing/denial documents
    is_pure_denial = bool(re.search(r"\b(?:notice\s+of\s+denial|denial\s+of\s+coverage|adverse\s+benefit\s+determination|claim\s+denial)\b", text_low))
    is_pure_billing = bool(re.search(r"\b(?:billing\s+invoice|statement\s+of\s+charges|payment\s+receipt|balance\s+due)\b", text_low))

    # 1. Header / Note type
    header_match = re.search(
        r"\b(?:consultation\s+notes?|office\s+visit\s+notes?|clinical\s+progress\s+notes?|progress\s+notes?|clinic\s+encounter|outpatient\s+clinic\s+notes?|soap\s+notes?|physician\s+clinical\s+notes?|consultation\s+notes\s+for|clinical\s+notes?\s*&?\s*order)\b",
        text_low
    )

    # 2. Encounter Date / DOS
    dos_match = re.search(
        r"\b(?:DOS|Date\s+of\s+Service|Encounter\s+Date|Visit\s+Date|Date)\s*[:#]?\s*(?:[0-9]{4}[/\-\.][0-9]{1,2}[/\-\.][0-9]{1,2}|[0-9]{1,2}[/\-\.][0-9]{1,2}[/\-\.][0-9]{2,4})",
        text,
        re.IGNORECASE
    )

    # 3. Clinical substance (at least 2 of History, Exam/Vitals, Assessment/Plan)
    has_history = bool(re.search(r"\b(?:history\s+of\s+present\s+illness|hpi|chief\s+complaint|subjective\s+symptoms|patient\s+presents?\b|patient\s+presented\b|clinical\s+history|history\s*:)", text_low))
    has_exam = bool(re.search(r"\b(?:general\s+examination|physical\s+examination|vital\s+signs|exam\b|objective\b|examination\s*:)", text_low))
    has_plan = bool(re.search(r"\b(?:assessments?\b|impression\b|treatment\s+plan|assessment\s+and\s+plan|treatment\s*:|plan\s*:|treatment\b)", text_low))
    substance_count = sum([has_history, has_exam, has_plan])

    # 4. Provider identification
    has_provider = bool(re.search(r"\b(?:provider|physician|attending|doctor|electronically\s+signed\s+by|signed\s+by)\b", text_low))

    if (is_pure_denial or is_pure_billing) and substance_count < 2:
        return False, ""

    if (header_match or substance_count >= 2) and dos_match and substance_count >= 2 and has_provider:
        matched_snip = header_match.group(0).strip() if header_match else "Clinical Encounter Documentation"
        if dos_match:
            matched_snip = f"{matched_snip} ({dos_match.group(0).strip()})"
        return True, matched_snip

    return False, ""


def _extract_clinical_evidence(text: str, domain: str, procedure_code: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Extract structured evidence key-value parameters and source provenance from doctor's narrative."""
    sentences = _split_into_sentences(text)
    evidence: Dict[str, Any] = {}
    provenance: Dict[str, Any] = {}

    def record_fact(param: str, val: Any, sentence: str):
        if param in evidence:
            existing_val = evidence[param]
            if existing_val != val:
                # Guard: if the existing value is already a CONFLICTING dict, add this value rather
                # than creating a nested CONFLICTING-within-CONFLICTING structure.
                if isinstance(existing_val, dict) and existing_val.get("status") == "CONFLICTING":
                    if val not in existing_val["values"]:
                        existing_val["values"].append(val)
                        prev_snip = provenance.get(param, {}).get("snippet", "")
                        provenance[param]["snippet"] = f"{prev_snip} | {sentence.strip()}"
                    return
                evidence[param] = {
                    "status": "CONFLICTING",
                    "details": f"Contradictory documented statements for '{param}'",
                    "values": [existing_val, val]
                }
                provenance[param] = {
                    "status": "CONFLICTING",
                    "snippet": f"1: {provenance.get(param, {}).get('snippet', '')} | 2: {sentence.strip()}",
                    "value": [existing_val, val]
                }
                return
        evidence[param] = val
        provenance[param] = {"snippet": sentence.strip(), "value": val}

    # Ordering provider
    prov_name, prov_snippet = _detect_provider_name_and_provenance(text)
    if prov_name:
        record_fact("ordering_provider_name", prov_name, prov_snippet)

    # Provider licensure evidence: credentials, license number, and verified licensure status are distinct
    creds, lic_num, is_verified, lic_snippet = _detect_provider_license_evidence(text)
    if creds:
        record_fact("ordering_provider_credentials", creds, f"Clinician credentials: {creds}")
    if lic_num:
        record_fact("ordering_provider_license_number", lic_num, f"Documented license/registration number: {lic_num}")
    if is_verified:
        # ONLY set ordering_provider_license = True when explicit active verified license evidence is present
        record_fact("ordering_provider_license", True, lic_snippet)
        record_fact("ordering_provider_license_verified", True, lic_snippet)

    # ICD-10 — capture only the first / primary code; the full list is in `all_diagnosis_codes`
    icd_match = re.search(r"\b([A-TV-Z][0-9][0-9A-Z](?:\.[0-9A-Z]{1,4})?)\b", text)
    if icd_match:
        record_fact("diagnosis_icd10", icd_match.group(1), icd_match.group(0))

    # Laterality & Anatomy
    lat, anat = _detect_laterality_and_anatomy(text)
    if lat:
        record_fact("laterality", lat, f"Laterality documented: {lat}")
    if anat:
        record_fact("anatomical_region", anat, f"Anatomical region documented: {anat}")
        record_fact("anatomy_region", anat, f"Anatomical region documented: {anat}")

    # Qualifying clinical office notes / consultation note evaluation
    is_qualifying_note, note_snippet = _is_qualifying_office_visit_note(text)
    if is_qualifying_note:
        record_fact("clinical_office_notes", True, note_snippet)
        record_fact("clinical_indication_documented", True, note_snippet)
        record_fact("clinical_information_submitted", True, note_snippet)

    # Place of Service code
    pos_enum, pos_code = _detect_place_of_service(text)
    record_fact("place_of_service_code", pos_code, f"Place of Service: {pos_enum} ({pos_code})")

    # Domain & Procedure Specific Logic
    for s in sentences:
        s_low = s.lower()

        # 1. Lumbar Spine & IPM
        if any(kw in s_low for kw in ("radiculopathy", "radiating pain", "radicular")):
            if _is_negated_in_sentence(s, "radiculopathy") or _is_negated_in_sentence(s, "radiating pain") or _is_negated_in_sentence(s, "radicular"):
                record_fact("lumbar_radiculopathy_present", False, s)
                record_fact("radicular_pain_confirmed", False, s)
            else:
                record_fact("lumbar_radiculopathy_present", True, s)
                record_fact("radicular_pain_confirmed", True, s)

        # Cauda equina and emergency red flags
        cauda_kws = ["cauda equina", "bowel incontinence", "bladder incontinence", "incontinence", "saddle anesthesia", "saddle numbness"]
        matched_cauda = [kw for kw in cauda_kws if kw in s_low]
        if matched_cauda:
            # Check for ambiguity
            if any(amb in s_low for amb in ("equivocal", "indeterminate", "cannot rule out", "possible cauda")):
                record_fact("suspected_cauda_equina_syndrome", {
                    "status": "AMBIGUOUS",
                    "details": "Documented equivocal or indeterminate cauda equina syndrome findings"
                }, s)
            elif any(_is_negated_in_sentence(s, kw) for kw in matched_cauda) or _is_negated_in_sentence(s, "saddle") or _is_negated_in_sentence(s, "incontinence"):
                record_fact("suspected_cauda_equina_syndrome", False, s)
            else:
                record_fact("suspected_cauda_equina_syndrome", True, s)

        # Conservative therapy & modalities
        # NOTE ON NEGATION SCOPE: Sentences like "patient did not get relief WITH conservative management"
        # are NOT evidence of absent conservative care — the 'not' negates 'relief', not 'conservative
        # management'. We must distinguish:
        #   (a) Explicitly denied care:  "no physical therapy", "denies physical therapy", "without PT"
        #   (b) Failed / insufficient care: "did not improve with PT", "failed conservative management"
        #   (c) Intolerance (care attempted but stopped): "cannot tolerate further physical therapy"
        # Only case (a) means no conservative care was performed.
        if any(kw in s_low for kw in ("conservative", "physical therapy", "pt", "nsaid", "therapy")):
            # Detect patterns that explicitly deny any conservative care has occurred
            # Avoid false negatives from "did not get relief WITH therapy" constructs
            explicitly_no_care = (
                bool(re.search(r'\b(?:no|without|denies?|denied|absence\s+of|zero)\s+(?:prior\s+|completing\s+|participating\s+in\s+)?(?:conservative|physical\s+therapy|pt)\b', s_low))
                and not re.search(r'\bdid not\s+(?:get|have|achieve|obtain|find)\s+\w+\s+(?:with|from)\s+(?:conservative|physical\s+therapy|pt)', s_low)
            )
            if explicitly_no_care:
                record_fact("conservative_therapy_duration_weeks", 0, s)
                record_fact("conservative_care_weeks", 0, s)
                record_fact("conservative_care_completed", False, s)
            else:
                # Intolerance sentences describe attempted care, not absent care
                is_intolerance = bool(re.search(r'\bcannot tolerate\b|\bunable to tolerate\b|\btoo painful\b', s_low))

                # Extract weeks or months
                m_wk = re.search(r'(\d+)\s*(?:weeks?|wks?)\b', s_low)
                m_mo = re.search(r'(\d+)\s*(?:months?|mos?)\b', s_low)

                # "at least N weeks" phrasing — the physician explicitly states duration >= N
                at_least_wk = re.search(r'\bat\s+least\s+(\d+)\s*(?:weeks?|wks?)\b', s_low)

                if at_least_wk:
                    wks = int(at_least_wk.group(1))
                    record_fact("conservative_therapy_duration_weeks", wks, s)
                    record_fact("conservative_care_weeks", wks, s)
                    if wks >= 6:
                        record_fact("conservative_care_completed", True, s)
                elif m_wk and not is_intolerance:
                    wks = int(m_wk.group(1))
                    record_fact("conservative_therapy_duration_weeks", wks, s)
                    record_fact("conservative_care_weeks", wks, s)
                    if wks >= 6:
                        record_fact("conservative_care_completed", True, s)
                elif m_mo:
                    mos = int(m_mo.group(1))
                    record_fact("conservative_therapy_duration_weeks", mos * 4, s)
                    record_fact("conservative_care_weeks", mos * 4, s)
                    record_fact("conservative_therapy_duration_months", mos, s)
                    if mos * 4 >= 6:
                        record_fact("conservative_care_completed", True, s)

                # Collect documented treatment modalities
                mods = []
                if "physical therapy" in s_low:
                    mods.append("Physical Therapy")
                if "home exercise" in s_low or "home exercise program" in s_low:
                    mods.append("Home Exercise Program")
                if "nsaid" in s_low:
                    mods.append("Oral NSAIDs")
                if ("pain medication" in s_low or "muscle relaxant" in s_low or "magnesium" in s_low or ("meloxicam" in s_low and "nsaid" not in s_low)):
                    mods.append("Analgesics / Muscle Relaxants")
                if "activity modification" in s_low:
                    mods.append("Activity Modification")
                if "chiropractic" in s_low:
                    mods.append("Chiropractic Care")
                if mods:
                    if "prior_conservative_care_modalities" in evidence:
                        existing_mods = evidence["prior_conservative_care_modalities"]
                        if isinstance(existing_mods, list):
                            for mod in mods:
                                if mod not in existing_mods:
                                    existing_mods.append(mod)
                            prev_snip = provenance.get("prior_conservative_care_modalities", {}).get("snippet", "")
                            if s.strip() not in prev_snip:
                                provenance["prior_conservative_care_modalities"]["snippet"] = f"{prev_snip} | {s.strip()}"
                        elif isinstance(existing_mods, dict) and existing_mods.get("status") == "CONFLICTING":
                            pass
                    else:
                        evidence["prior_conservative_care_modalities"] = list(mods)
                        provenance["prior_conservative_care_modalities"] = {
                            "snippet": s.strip(),
                            "value": evidence["prior_conservative_care_modalities"]
                        }

        # Symptom duration (distinct from conservative care duration)
        symp_dur_match = re.search(
            r"(?:pain|symptoms?|radiculopathy|sciatica|presents?\s+with[^\.\n]*?)\s*(?:lasting|persisting|for|duration\s*(?:of)?)\s*(\d+)\s*(?:consecutive\s*)?(weeks?|wks?|months?|mos?|days?)",
            s,
            re.IGNORECASE
        )
        if symp_dur_match:
            dur_val = int(symp_dur_match.group(1))
            unit = symp_dur_match.group(2).lower()
            if "month" in unit or "mo" in unit:
                record_fact("symptom_duration_weeks", dur_val * 4, s)
                record_fact("symptom_duration_months", dur_val, s)
            elif "week" in unit or "wk" in unit:
                record_fact("symptom_duration_weeks", dur_val, s)
            elif "day" in unit:
                record_fact("symptom_duration_days", dur_val, s)
                record_fact("symptom_duration_weeks", max(1, dur_val // 7), s)
            record_fact("symptom_duration_documented", True, s)

        # Straight leg raise (SLR) test
        if any(kw in s_low for kw in ("straight leg raise", "slr test", "slr")):
            if _is_negated_in_sentence(s, "straight leg raise") or _is_negated_in_sentence(s, "slr") or "negative" in s_low:
                record_fact("straight_leg_raise_positive", False, s)
                record_fact("straight_leg_raise_test_positive", False, s)
            else:
                record_fact("straight_leg_raise_positive", True, s)
                record_fact("straight_leg_raise_test_positive", True, s)

            deg_match = re.search(r"(?:straight\s*leg\s*raise|slr)[^\.\n]*?(?:at\s+)?(\d{1,2})\s*(?:degrees|deg|°)", s, re.IGNORECASE)
            if deg_match:
                record_fact("straight_leg_raise_angle_degrees", int(deg_match.group(1)), s)

            side_match = re.search(r"(?:straight\s*leg\s*raise|slr)[^\.\n]*?\b(right|left|bilateral)\b", s, re.IGNORECASE)
            if side_match:
                record_fact("straight_leg_raise_side", side_match.group(1).upper(), s)

        # Radiculopathy dermatome
        derm_match = re.search(r"\b(L[1-5]|S1)(?:\s*[-/]\s*(?:L[1-5]|S1))?\s*(?:dermatome|distribution|nerve\s*root)\b", s, re.IGNORECASE)
        if derm_match:
            record_fact("radiculopathy_dermatome", derm_match.group(1).upper(), s)

        # Neurological sensory deficit
        if any(kw in s_low for kw in ("diminished sensory", "decreased sensation", "loss of sensation", "sensory perception", "sensory deficit", "hypoesthesia")):
            if _is_negated_in_sentence(s, "sensory") or _is_negated_in_sentence(s, "sensation") or _is_negated_in_sentence(s, "deficit"):
                record_fact("sensory_deficit_documented", False, s)
            else:
                record_fact("sensory_deficit_documented", True, s)
                record_fact("sensory_deficit_present", True, s)

        # Functional limitation
        if re.search(r"\bfunctional\s+limitations?\b|\bimpairment\s+in\s+daily\b|\bactivities\s+of\s+daily\s+living\b", s, re.IGNORECASE):
            if not _is_negated_in_sentence(s, "functional"):
                record_fact("functional_limitation_documented", True, s)

        # Nerve root compression
        if "nerve root compression" in s_low or "mri shows" in s_low or "disc herniation" in s_low:
            if _is_negated_in_sentence(s, "compression") or _is_negated_in_sentence(s, "herniation"):
                record_fact("lumbar_mri_nerve_root_compression", False, s)
            else:
                record_fact("lumbar_mri_nerve_root_compression", True, s)

        # 2. Pancreatitis & Abdominal Imaging
        if any(kw in s_low for kw in ("pancreatitis", "amylase", "lipase")):
            if "elevated" in s_low or "high" in s_low or "positive" in s_low:
                record_fact("pancreatitis_diagnostic_markers", "ELEVATED", s)
            elif "normal" in s_low or "unremarkable" in s_low or _is_negated_in_sentence(s, "elevated"):
                record_fact("pancreatitis_diagnostic_markers", "NORMAL", s)

        if "abdominal pain" in s_low or "epigastric" in s_low:
            if _is_negated_in_sentence(s, "pain") or _is_negated_in_sentence(s, "abdominal"):
                record_fact("abdominal_pain_documented", False, s)
            else:
                record_fact("abdominal_pain_documented", True, s)

        if "fluid resuscitation" in s_low or "conservative therapy continued" in s_low or "treatment duration" in s_low or "hours" in s_low:
            m_hr = re.search(r'(\d+)\s*(?:hours?|hrs?)\b', s_low)
            if m_hr:
                record_fact("conservative_treatment_duration_hours", int(m_hr.group(1)), s)

        if "ultrasound" in s_low or "ruq" in s_low:
            if "no gallstones" in s_low or "no gallstones or dilated" in s_low or _is_negated_in_sentence(s, "gallstones"):
                record_fact("ultrasound_findings", "NO_GALLSTONES_OR_DILATED_DUCT", s)
            elif "gallstones" in s_low or "cholelithiasis" in s_low:
                record_fact("ultrasound_findings", "GALLSTONES_PRESENT", s)

        if "diverticulitis" in s_low:
            if _is_negated_in_sentence(s, "diverticulitis"):
                record_fact("diverticulitis_diagnosis_suspected", False, s)
            else:
                record_fact("diverticulitis_diagnosis_suspected", True, s)

        # 3. Brain MRI / Neurology
        if "headache" in s_low:
            if _is_negated_in_sentence(s, "headache"):
                record_fact("headache_documented", False, s)
            else:
                record_fact("headache_documented", True, s)

        if any(kw in s_low for kw in ("focal neurological", "neurological deficit", "focal deficit")):
            if _is_negated_in_sentence(s, "deficit") or _is_negated_in_sentence(s, "neurological"):
                record_fact("focal_neurological_deficit_present", False, s)
                record_fact("focal_neurological_deficit", False, s)
                record_fact("neurological_deficit_present", False, s)
            else:
                record_fact("focal_neurological_deficit_present", True, s)
                record_fact("focal_neurological_deficit", True, s)
                record_fact("neurological_deficit_present", True, s)

        if "multiple sclerosis" in s_low or bool(re.search(r"\bms\b", s_low)):
            if _is_negated_in_sentence(s, "multiple sclerosis"):
                record_fact("suspected_or_established_multiple_sclerosis", False, s)
            else:
                record_fact("suspected_or_established_multiple_sclerosis", True, s)

        if any(kw in s_low for kw in ("red flag", "thunderclap", "sudden onset severe")):
            if _is_negated_in_sentence(s, "red flag"):
                record_fact("red_flag_symptoms_documented", False, s)
            else:
                record_fact("red_flag_symptoms_documented", True, s)

        if "seizure" in s_low:
            if _is_negated_in_sentence(s, "seizure"):
                record_fact("seizure_activity_documented", False, s)
                record_fact("seizures_documented", False, s)
            else:
                record_fact("seizure_activity_documented", True, s)
                record_fact("seizures_documented", True, s)

        # 4. Knee MRI / Orthopedics
        if any(kw in s_low for kw in ("meniscus", "meniscal", "cruciate", "acl")):
            if _is_negated_in_sentence(s, "tear") or _is_negated_in_sentence(s, "meniscus") or _is_negated_in_sentence(s, "acl"):
                record_fact("knee_meniscal_or_ligamentous_injury_suspected", False, s)
                record_fact("meniscal_tear_suspected", False, s)
            else:
                record_fact("knee_meniscal_or_ligamentous_injury_suspected", True, s)
                record_fact("meniscal_tear_suspected", True, s)

        if "effusion" in s_low:
            if _is_negated_in_sentence(s, "effusion"):
                record_fact("joint_effusion_present", False, s)
            else:
                record_fact("joint_effusion_present", True, s)

        if any(kw in s_low for kw in ("mcmurray", "joint line tenderness", "lachman", "drawer", "pivot shift", "internal derangement")):
            if _is_negated_in_sentence(s, "mcmurray") or _is_negated_in_sentence(s, "tenderness") or _is_negated_in_sentence(s, "lachman"):
                record_fact("positive_knee_orthopedic_sign", False, s)
                record_fact("joint_specific_injury_or_pain", False, s)
            else:
                record_fact("positive_knee_orthopedic_sign", True, s)
                record_fact("joint_specific_injury_or_pain", True, s)

        if any(kw in s_low for kw in ("radiographs", "x-ray", "xray")):
            if _is_negated_in_sentence(s, "radiographs") or _is_negated_in_sentence(s, "x-ray") or _is_negated_in_sentence(s, "xray"):
                record_fact("weight_bearing_radiographs_completed", False, s)
                record_fact("prior_xray_completed", False, s)
            else:
                record_fact("weight_bearing_radiographs_completed", True, s)
                record_fact("prior_xray_completed", True, s)

        if any(kw in s_low for kw in ("osteoarthritis", "joint degeneration")):
            if "grade iv" in s_low or "advanced" in s_low or "severe" in s_low:
                record_fact("osteoarthritis_severity", "GRADE_IV_ADVANCED", s)
            elif "mild" in s_low or "grade i" in s_low:
                record_fact("osteoarthritis_severity", "GRADE_I_MILD", s)

        if "functional impairment" in s_low or "activities of daily living" in s_low or "adl" in s_low:
            if _is_negated_in_sentence(s, "impairment"):
                record_fact("functional_impairment_daily_living", False, s)
            else:
                record_fact("functional_impairment_daily_living", True, s)

        # 5. Cardiology
        if "ischemia" in s_low or "stress test" in s_low:
            if "high risk" in s_low:
                record_fact("stress_test_findings", "HIGH_RISK_ISCHEMIA", s)
            elif _is_negated_in_sentence(s, "ischemia"):
                record_fact("stress_test_findings", "NEGATIVE_FOR_ISCHEMIA", s)

        if "angina" in s_low or "chest pressure" in s_low or "chest pain" in s_low:
            if "class iii" in s_low or "class iv" in s_low:
                record_fact("angina_symptoms", "CANADIAN_CLASS_III_IV", s)
            elif _is_negated_in_sentence(s, "angina") or _is_negated_in_sentence(s, "pain"):
                record_fact("angina_symptoms", "NONE", s)

        # 6. Place of Service Exception Attributes (EPOS)
        if "claustrophobia" in s_low or "open mri" in s_low:
            if _is_negated_in_sentence(s, "claustrophobia"):
                record_fact("severe_claustrophobia_open_mri_needed", False, s)
            else:
                record_fact("severe_claustrophobia_open_mri_needed", True, s)

        if "bariatric" in s_low or "weight exceeds" in s_low:
            if _is_negated_in_sentence(s, "bariatric") or _is_negated_in_sentence(s, "exceeds"):
                record_fact("bariatric_weight_exceeds_freestanding_scanner", False, s)
            else:
                record_fact("bariatric_weight_exceeds_freestanding_scanner", True, s)

        if "specialized protocol" in s_low or "complex protocol" in s_low:
            if _is_negated_in_sentence(s, "protocol"):
                record_fact("complex_specialized_protocol_needed", False, s)
            else:
                record_fact("complex_specialized_protocol_needed", True, s)

    return evidence, provenance


def _detect_patient_demographics(text: str) -> Dict[str, str]:
    """Extract patient demographics such as DOB, age, and gender if present."""
    demo: Dict[str, str] = {}
    dob_match = re.search(r"(?:DOB|Date of Birth|Birth Date)\s*[:#]?\s*([0-9]{1,2}[\-/][0-9]{1,2}[\-/][0-9]{2,4})", text, re.IGNORECASE)
    if dob_match:
        demo["dob"] = dob_match.group(1).strip()
    age_match = re.search(r"\b([0-9]{1,2})\s*(?:yo|y\.o\.|year old|years old)\b", text, re.IGNORECASE)
    if age_match:
        demo["age"] = f"{age_match.group(1)} years"
    gender_match = re.search(r"\b(Male|Female)\b", text, re.IGNORECASE)
    if gender_match:
        demo["gender"] = gender_match.group(1).capitalize()
    elif re.search(r"\b(?:Gender|Sex)\s*[:#]?\s*(M|F)\b", text, re.IGNORECASE):
        m = re.search(r"\b(?:Gender|Sex)\s*[:#]?\s*(M|F)\b", text, re.IGNORECASE)
        demo["gender"] = "Male" if m.group(1).upper() == "M" else "Female"
    return demo


def _detect_provider_details(text: str, evidence_name: Optional[str] = None) -> Dict[str, Any]:
    """Extract ordering provider name, credentials, specialty, facility, and licensure metadata."""
    detected_name, _ = _detect_provider_name_and_provenance(text)
    creds, lic_num, is_verified, _ = _detect_provider_license_evidence(text)
    final_name = evidence_name or detected_name or ""
    res: Dict[str, Any] = {
        "provider_name": final_name,
        "credentials": creds or "",
        "license_number": lic_num or "",
        "is_licensed": True if is_verified else None,
        "specialty": "",
        "facility": ""
    }
    spec_match = re.search(r"(?:Specialty|Department|Practice)\s*[:#]?\s*([A-Za-z\s&]{3,35})", text, re.IGNORECASE)
    if spec_match:
        res["specialty"] = spec_match.group(1).strip()
    fac_match = re.search(r"(?:Facility|Clinic|Hospital|Center|Practice Name)\s*[:#]?\s*([A-Za-z0-9\s,\.]{4,45})", text, re.IGNORECASE)
    if fac_match:
        res["facility"] = fac_match.group(1).strip()
    return res


def _format_narrative_excerpt(text: str, max_chars: int = 2800) -> str:
    """Format verbatim clinical narrative excerpt preserving readability and paragraphs."""
    lines = [line.strip() for line in text.strip().split("\n")]
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if not line:
            if not prev_empty:
                cleaned_lines.append("")
                prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False
    cleaned_text = "\n".join(cleaned_lines)
    if len(cleaned_text) > max_chars:
        return cleaned_text[:max_chars].rstrip() + "\n... [Additional chart narrative documented in patient record]"
    return cleaned_text


def extract_case_from_pdf(pdf_bytes: bytes, filename: str = "doctor_notes.pdf") -> Dict[str, Any]:
    """Parse clinical PDF bytes and return structured case intake data dictionary."""
    clean_filename = filename.replace("\\", "/").split("/")[-1]
    text, num_pages = _extract_text_from_pdf_bytes(pdf_bytes)
    
    timestamp_suffix = int(datetime.now().timestamp())
    case_id = f"CASE-PDF-{timestamp_suffix}"

    # Handle unreadable, blank, or scanned PDFs gracefully
    if not text or not text.strip():
        return {
            "status": "UNREADABLE_OR_SCANNED_DOCUMENT",
            "error": "Uploaded document contains no extractable text (it may be a raster scan or image-only PDF). Requires OCR preprocessing or manual clinical review.",
            "filename": clean_filename,
            "pages_analyzed": num_pages,
            "diagnostics": {
                "extracted_characters": len(text) if text else 0,
                "pages_analyzed": num_pages,
                "is_raster_scan_likely": True
            },
            "extracted_fields": {
                "case_id": case_id,
                "patient_id": "PT-UNRESOLVED",
                "clinical_domain": "UNKNOWN",
                "procedure_code": "UNKNOWN",
                "procedure_name": "Unspecified Procedure",
                "line_of_business": "COMMERCIAL",
                "requested_date_of_service": datetime.now().strftime("%Y-%m-%d"),
                "payer_id": "EVOLENT",
                "plan_id": "COMMERCIAL_CHOICE_PLUS",
                "place_of_service": "OFFICE",
                "submitted_documents": f"Uploaded Physician PDF ({clean_filename})",
                "evidence": {},
                "evidence_provenance": {}
            },
            "details": {
                "patient_id": "PT-UNRESOLVED",
                "procedure_code": "UNKNOWN",
                "procedure_name": "Unspecified Procedure",
                "clinical_domain": "UNKNOWN",
                "clinical_domain_label": "Unknown / Unresolved",
                "key_findings": ["Unreadable or scanned document: No machine-readable text found."],
                "evidence_count": 0,
                "pages_analyzed": num_pages,
                "character_count": 0,
                "narrative_excerpt": ""
            },
            "text_snippet": "",
            "summary": f"Document {clean_filename} is an image-only scan or unreadable PDF with 0 extractable characters."
        }

    patient_id = _detect_patient_id(text)
    procedure_code, procedure_name, clinical_domain = _detect_procedure_and_domain(text)
    line_of_business = _detect_line_of_business(text)
    date_of_service = _detect_date_of_service(text)
    payer_id, plan_id = _detect_payer_and_plan(text, line_of_business)
    pos_enum, pos_code = _detect_place_of_service(text)
    evidence, provenance = _extract_clinical_evidence(text, clinical_domain, procedure_code)
    demographics = _detect_patient_demographics(text)
    provider_info = _detect_provider_details(text, evidence.get("ordering_provider_name"))

    submitted_docs = f"Comprehensive clinical notes and diagnostic findings, Uploaded Physician PDF ({clean_filename}), Clinical Notes & Order Documentation"
    formatted_narrative = _format_narrative_excerpt(text)
    snippet = " ".join(text[:450].split())

    key_findings: List[str] = []
    ordering_provider = provider_info["provider_name"]
    diag_code = evidence.get("diagnosis_icd10", "Documented")
    
    icd_descriptions = {
        # M62.838 = Other specified disorders of muscle, unspecified site (ICD-10-CM)
        # This code denotes muscle spasm.  It does NOT imply lumbar radicular syndrome.
        # Lumbar radicular syndrome is captured separately in the narrative findings.
        "M62.838": "Muscle spasm (other specified disorder of muscle)",
        "M54.5": "Low back pain, unspecified",
        "M54.50": "Low back pain, unspecified",
        "M54.16": "Radiculopathy, lumbar region",
        "M54.17": "Radiculopathy, lumbosacral region",
        "M51.16": "Intervertebral disc disorders with radiculopathy, lumbar region",
        "M51.26": "Other intervertebral disc displacement, lumbar region",
        "M47.816": "Spondylosis without myelopathy or radiculopathy, lumbar region",
        "K85.9": "Acute pancreatitis, unspecified",
        "K85.90": "Acute pancreatitis without necrosis or infection",
        "K57.90": "Diverticulitis of intestine, unspecified",
        "M17.11": "Primary osteoarthritis, right knee",
        "M17.12": "Primary osteoarthritis, left knee",
        "M17.0": "Bilateral primary osteoarthritis of knee",
        "M16.11": "Primary osteoarthritis, right hip",
        "M16.12": "Primary osteoarthritis, left hip",
        "G47.33": "Obstructive sleep apnea (adult)",
        "E10.9": "Type 1 diabetes mellitus without complications",
        "E11.9": "Type 2 diabetes mellitus without complications",
        "C61": "Malignant neoplasm of prostate",
        "C50.919": "Malignant neoplasm of unspecified breast",
        "I25.10": "Atherosclerotic heart disease of native coronary artery",
        "R07.9": "Chest pain, unspecified"
    }
    diag_desc = icd_descriptions.get(diag_code, f"Clinical Diagnosis ({diag_code})")

    key_findings.append(f"Diagnosis: {diag_desc} (ICD-10 {diag_code})")
    key_findings.append(f"Ordering Physician: {ordering_provider}")
    key_findings.append(f"Requested Procedure: {procedure_name} (CPT {procedure_code})")
    key_findings.append(f"Place of Service: {pos_enum} ({pos_code})")
    
    if "lumbar_radiculopathy_present" in evidence:
        val = evidence["lumbar_radiculopathy_present"]
        if val is True:
            key_findings.append("Documented lumbar radiculopathy / radiating pain")
        elif val is False:
            key_findings.append("Lumbar radiculopathy explicitly denied / absent")
    if "symptom_duration_weeks" in evidence:
        dur = evidence["symptom_duration_weeks"]
        if isinstance(dur, (int, float)):
            key_findings.append(f"Symptom duration documented ({dur} weeks)")
    if "conservative_therapy_duration_weeks" in evidence:
        dur = evidence['conservative_therapy_duration_weeks']
        if isinstance(dur, (int, float)):
            key_findings.append(f"Prior conservative therapy documented ({dur} weeks)")
    if "prior_conservative_care_modalities" in evidence:
        mods = evidence["prior_conservative_care_modalities"]
        if isinstance(mods, list):
            key_findings.append(f"Conservative modalities: {', '.join(mods)}")
    if "straight_leg_raise_positive" in evidence:
        if evidence["straight_leg_raise_positive"] is True:
            side = evidence.get("straight_leg_raise_side", "")
            ang = evidence.get("straight_leg_raise_angle_degrees")
            extra = f" on {side}" if side else ""
            extra += f" at {ang} degrees" if ang else ""
            key_findings.append(f"Physical exam: Positive straight leg raise{extra}")
        elif evidence["straight_leg_raise_positive"] is False:
            key_findings.append("Physical exam: Straight leg raise negative")
    if "radiculopathy_dermatome" in evidence:
        key_findings.append(f"Radiculopathy nerve distribution: {evidence['radiculopathy_dermatome']} dermatome")
    if "sensory_deficit_documented" in evidence and evidence["sensory_deficit_documented"] is True:
        key_findings.append("Documented neurological sensory perception deficit")
    if "suspected_cauda_equina_syndrome" in evidence:
        if evidence["suspected_cauda_equina_syndrome"] is False:
            key_findings.append("Cauda equina syndrome evaluated: Negative (No bowel/bladder incontinence)")
        elif evidence["suspected_cauda_equina_syndrome"] is True:
            key_findings.append("Red flag alert: Suspected cauda equina syndrome")
    if "pancreatitis_diagnostic_markers" in evidence:
        key_findings.append(f"Diagnostic amylase/lipase markers: {evidence['pancreatitis_diagnostic_markers']}")
    if "osteoarthritis_severity" in evidence:
        key_findings.append(f"Joint degeneration: {evidence['osteoarthritis_severity']}")

    domain_labels = {
        "advanced_imaging": "Advanced Imaging",
        "cardiology": "Cardiology",
        "musculoskeletal_surgery": "Musculoskeletal Surgery",
        "interventional_pain_management": "Interventional Pain Management",
        "radiation_oncology": "Radiation Oncology",
        "physical_medicine": "Physical Medicine",
        "sleep_health": "Sleep Health",
        "genetic_testing": "Genetic Testing",
        "centene_dme_orthotics_prosthetics": "Centene DME / Orthotics / Prosthetics"
    }

    details = {
        "patient_id": patient_id,
        "patient_dob": demographics.get("dob", "Documented in chart"),
        "patient_age": demographics.get("age", "Adult"),
        "patient_gender": demographics.get("gender", "Documented"),
        "ordering_provider": ordering_provider,
        "provider_specialty": provider_info["specialty"],
        "facility_name": provider_info["facility"],
        "procedure_code": procedure_code,
        "procedure_name": procedure_name,
        "clinical_domain": clinical_domain,
        "clinical_domain_label": domain_labels.get(clinical_domain, clinical_domain.replace("_", " ").title()),
        "diagnosis_icd10": diag_code,
        "diagnosis_description": diag_desc,
        "date_of_service": date_of_service,
        "line_of_business": line_of_business,
        "payer_id": payer_id,
        "plan_id": plan_id,
        "place_of_service": pos_enum,
        "place_of_service_code": pos_code,
        "key_findings": key_findings,
        "evidence_count": len(evidence),
        "pages_analyzed": num_pages,
        "character_count": len(text),
        "narrative_excerpt": formatted_narrative
    }

    return {
        "status": "SUCCESS",
        "filename": clean_filename,
        "pages_analyzed": num_pages,
        "extracted_fields": {
            "case_id": case_id,
            "patient_id": patient_id,
            "clinical_domain": clinical_domain,
            "procedure_code": procedure_code,
            "procedure_name": procedure_name,
            "line_of_business": line_of_business,
            "requested_date_of_service": date_of_service,
            "payer_id": payer_id,
            "plan_id": plan_id,
            "place_of_service": pos_enum,
            "submitted_documents": submitted_docs,
            "ordering_provider": provider_info,
            "evidence": evidence,
            "evidence_provenance": provenance
        },
        "details": details,
        "text_snippet": snippet,
        "summary": f"Extracted {len(evidence) + 8} clinical & administrative fields from {clean_filename} ({num_pages} pages, {len(text)} characters)."
    }


def extract_clinical_facts_from_text(text: str) -> Dict[str, Any]:
    """Extract clinical facts, procedure, domain, line of business, and evidence directly from clinical note text."""
    patient_id = _detect_patient_id(text)
    procedure_code, procedure_name, clinical_domain = _detect_procedure_and_domain(text)
    line_of_business = _detect_line_of_business(text)
    date_of_service = _detect_date_of_service(text)
    payer_id, plan_id = _detect_payer_and_plan(text, line_of_business)
    pos_enum, pos_code = _detect_place_of_service(text)
    evidence, provenance = _extract_clinical_evidence(text, clinical_domain, procedure_code)
    
    return {
        "patient_id": patient_id,
        "clinical_domain": clinical_domain,
        "procedure_code": procedure_code,
        "procedure_name": procedure_name,
        "line_of_business": line_of_business,
        "requested_date_of_service": date_of_service,
        "payer_id": payer_id,
        "plan_id": plan_id,
        "place_of_service": pos_enum,
        "evidence": evidence,
        "evidence_provenance": provenance
    }

