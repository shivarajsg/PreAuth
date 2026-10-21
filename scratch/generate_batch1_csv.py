import csv
from pathlib import Path

ROOT = Path(".")
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

csv_file = REPORTS_DIR / "batch_01_policy_audit.csv"

fieldnames = [
    "rule_id",
    "domain",
    "source_pdf",
    "pdf_physical_page",
    "policy_section",
    "exact_quotation",
    "reflects_source",
    "missing_context_or_exceptions",
    "audit_status",
    "explanation_and_recommendation"
]

rows = [
    {
        "rule_id": "RULE-ADV-CG2000-002",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 9,
        "policy_section": "Inflammatory Bowel Disease (3-5)",
        "exact_quotation": "For suspected inflammatory bowel disease after complete work up including physical exam, labs, and recent colonoscopy",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Omits acute surgical contraindications (toxic megacolon, free air/bowel perforation requiring emergency triage) and radiation-sparing MRI consideration for < 35yo.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Prerequisites of exam, labs, and recent colonoscopy match text. Recommend Clinical SME review to add an emergency exclusion gate for suspected perforation."
    },
    {
        "rule_id": "RULE-ADV-CG2000-004",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 9,
        "policy_section": "Diverticulitis or Acute Appendicitis (8,9)",
        "exact_quotation": "Suspected diverticulitis or acute appendicitis for initial imaging with at least ONE of the following (10): WBC Elevated; Fever; Anorexia; Nausea and vomiting",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Omits mandatory pregnancy note on page 9 (pregnant patients require insufficient ultrasound AND MRI contraindication before CT appendicitis evaluation).",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Adult systemic sign criteria match verbatim. Recommend Clinical SME review to add pregnancy status verification routing to US/MRI before CT."
    },
    {
        "rule_id": "RULE-ADV-CG2000-005",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 9,
        "policy_section": "Diverticulitis or Acute Appendicitis (8,9)",
        "exact_quotation": "Suspected appendicitis in a child (< age 18) (12) when ultrasound is inconclusive or cannot be completed (due to body habitus or inability to cooperate) OR when peritoneal signs are present (guarding, rebound) or other red flags",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Omits documented exception allowing CT when ultrasound cannot be completed due to documented patient lack of cooperation or body habitus.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Pediatric criteria (< 18) match source. Recommend Clinical SME review to add uncooperative/habitus parameter as valid ultrasound exception."
    },
    {
        "rule_id": "RULE-ADV-CG2003-001",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 75,
        "policy_section": "Other Vascular Abnormalities of the Abdomen / Takayasu's Arteritis (15)",
        "exact_quotation": "Takayasu's Arteritis (15): At initial diagnosis; Every 6 months for the first 2 years while on therapy; Annually after the first 2 years",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Cross-cutting MRI contraindications (non-conditional implants, GFR < 30 for gadolinium) are in general guidelines but not explicitly linked in rule.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Indication and frequency intervals match verbatim. Recommend Clinical SME review to confirm reliance on global contrast/implant safety rules."
    },
    {
        "rule_id": "RULE-ADV-CG2004-001",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 92,
        "policy_section": "INDICATIONS / Biliary / Choledochal cyst",
        "exact_quotation": "Suspected choledochal cyst after ultrasound has been done",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Guideline title specifies 'with or without MRCP'. Rule does not specify whether MRCP CPT codes are required over standard Abdomen MRI.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Prior ultrasound requirement matches source text. Recommend Clinical SME review to clarify MRCP CPT coding specificity."
    },
    {
        "rule_id": "RULE-ADV-CG2004-002",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 92,
        "policy_section": "INDICATIONS / Pancreas",
        "exact_quotation": "Suspected new onset acute pancreatitis and ALL of the following: Epigastric or upper abdominal pain",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Policy 'ALL of the following' clause includes laboratory diagnostic thresholds (lipase/amylase > 3x ULN) and timing consideration (>= 48-72h post-onset).",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Rule only codified the epigastric pain component. Recommend Clinical SME review to add objective lipase/amylase > 3x ULN criterion."
    },
    {
        "rule_id": "RULE-ADV-CG2005-001",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 118,
        "policy_section": "Ischemia or Hemorrhage",
        "exact_quotation": "Evaluation of known or suspected mesenteric ischemia/ischemic colitis (5)",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Surrounding text details biphasic CTA protocol and distinction between acute occlusive thromboembolism vs non-occlusive ischemia.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Indication verified against source. Recommend Clinical SME review to confirm whether documented acute symptom duration is required."
    },
    {
        "rule_id": "RULE-ADV-CG2005-002",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 119,
        "policy_section": "Venous Disease",
        "exact_quotation": "Suspected pelvic congestive syndrome (including May-Thurner and nutcracker syndromes) when ultrasound is indeterminant with no contraindications to CT (17)",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Omits explicit check for 'no contraindications to CT' (routing to MRA if contraindicated) and documentation of chronic pelvic pain duration (> 6m).",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Core indication and ultrasound failure match source. Recommend Clinical SME review to link CT contraindication checks to MRA fallback."
    },
    {
        "rule_id": "RULE-ADV-CG2008-001",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 150,
        "policy_section": "Stroke and Vascular Disease / Evaluation of Known or Suspected Stroke (11,12)",
        "exact_quotation": "Suspected stroke with any acute, new, or fluctuating symptoms or deficits such as sensory deficits, limb weakness, speech difficulties, visual loss, lack of coordination, or mental status changes",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Rule compresses specific focal deficits into a single generic boolean without validating at least one documented qualifying deficit.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Intent matches source. Recommend Clinical SME review to decompose generic parameter into multi-select focal neurological findings."
    },
    {
        "rule_id": "RULE-ADV-CG2008-002",
        "domain": "advanced_imaging",
        "source_pdf": "2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf",
        "pdf_physical_page": 151,
        "policy_section": "Evaluation of Known or Suspected Vascular Disease (13)",
        "exact_quotation": "Evaluation of suspected acute subarachnoid hemorrhage (SAH)",
        "reflects_source": "PARTIAL",
        "missing_context_or_exceptions": "Clinical timing notes on page 151 indicate non-contrast CT sensitivity peaks within 6-24 hours; negative CT > 6h requires lumbar puncture correlation.",
        "audit_status": "PARTIALLY_VERIFIED",
        "explanation_and_recommendation": "Indication verified against source. Recommend Clinical SME review to confirm non-contrast CT is approved without prerequisite lumbar puncture."
    }
]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Generated {len(rows)} audit rows in {csv_file}")
