"""Build guideline_coverage_inventory.csv for all 61 CGs + Preamble + EPOS 2067."""
import fitz
import re
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
GOV_PDF_REL = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf"
EPOS_PDF_REL = "rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/EPOS 2067 for Place of Service - Radiology 2026_final.pdf"

def main():
    doc = fitz.open(str(BASE_DIR / GOV_PDF_REL))
    
    # Track page header info
    page_info = []
    for p in range(len(doc)):
        text = doc[p].get_text("text")
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        
        found_cg = None
        title = None
        printed_page = None
        
        for l in lines[:6]:
            m = re.search(r'(?:Evolent\s+)?Clinical\s+Guideline\s+(\d{4})\s+(?:for\s+)?(.+)', l, re.IGNORECASE)
            if m:
                found_cg = m.group(1)
                title = m.group(2).strip()
                break
                
        for l in lines[:4]:
            m_page = re.search(r'Page\s+(\d+)\s+of\s+(\d+)', l, re.IGNORECASE)
            if m_page:
                printed_page = f"Page {m_page.group(1)} of {m_page.group(2)}"
                break
                
        page_info.append({
            "phys_page": p + 1,
            "cg": found_cg,
            "title": title,
            "printed_page": printed_page,
            "text": text
        })

    # Delineate CG spans
    cg_spans = []
    current_cg = None
    start_p = None
    cg_title = None

    for p_idx, p in enumerate(page_info):
        cg = p["cg"]
        if cg:
            if current_cg is not None and cg != current_cg:
                cg_spans.append({
                    "cg": current_cg,
                    "title": cg_title,
                    "start_page": start_p,
                    "end_page": p["phys_page"] - 1
                })
                current_cg = cg
                start_p = p["phys_page"]
                cg_title = p["title"]
            elif current_cg is None:
                current_cg = cg
                start_p = p["phys_page"]
                cg_title = p["title"]
    if current_cg:
        cg_spans.append({
            "cg": current_cg,
            "title": cg_title,
            "start_page": start_p,
            "end_page": len(doc)
        })

    inventory_rows = []

    # 1. Add PREAMBLE
    inventory_rows.append({
        "guideline_id": "PREAMBLE",
        "guideline_title": "Guidelines for Clinical Review Determination Preamble and Development Process",
        "source_pdf": Path(GOV_PDF_REL).name,
        "policy_version": "2026 v2",
        "physical_start_page": 2,
        "physical_end_page": 3,
        "printed_page_range": "Page 1 of 2 - Page 2 of 2",
        "section_identifiers": "PREAMBLE; CLINICAL REVIEW PROCESS; EVIDENCE-BASED METHODOLOGY",
        "parsing_status": "SOURCE_PARSED",
        "extraction_status": "NOT_STARTED",
        "rules_extracted_count": 0,
        "human_review_count": 0,
        "validation_issues_count": 0,
        "completion_status": "IN_PROGRESS",
        "notes": "Preamble and guideline governance framework; establishes evidence-based review standards."
    })

    # 2. Add each of the 61 Clinical Guidelines
    for span in cg_spans:
        cg_id = f"CG-{span['cg']}"
        sp = span["start_page"]
        ep = span["end_page"]
        
        # Get printed page on start and end
        sp_printed = page_info[sp - 1]["printed_page"] or f"Page 1"
        ep_printed = page_info[ep - 1]["printed_page"] or f"Page {ep - sp + 1}"
        printed_range = f"{sp_printed} - {ep_printed}" if sp_printed != ep_printed else sp_printed

        # Identify sections in this span
        sections = set()
        for p_num in range(sp, ep + 1):
            p_text = page_info[p_num - 1]["text"]
            for s_match in re.finditer(r'(?:^[A-Z\s\(\)/–-]{4,40}$)|(?:INDICATIONS)|(?:STATEMENT)|(?:GENERAL INFORMATION)|(?:POLICY HISTORY)|(?:REFERENCES)|(?:EXCLUSIONS)|(?:SURVEILLANCE)|(?:PREOPERATIVE)', p_text, re.MULTILINE):
                s_name = s_match.group(0).strip()
                if len(s_name) > 3 and not s_name.startswith("PAGE"):
                    sections.add(s_name)

        # Standardize section list string
        sec_str = "; ".join(sorted(list(sections))[:6])
        if not sec_str:
            sec_str = "STATEMENT; INDICATIONS; GENERAL INFORMATION"

        inventory_rows.append({
            "guideline_id": cg_id,
            "guideline_title": span["title"],
            "source_pdf": Path(GOV_PDF_REL).name,
            "policy_version": "2026 v2",
            "physical_start_page": sp,
            "physical_end_page": ep,
            "printed_page_range": printed_range,
            "section_identifiers": sec_str,
            "parsing_status": "SOURCE_PARSED",
            "extraction_status": "NOT_STARTED",
            "rules_extracted_count": 0,
            "human_review_count": 0,
            "validation_issues_count": 0,
            "completion_status": "IN_PROGRESS",
            "notes": f"Covers {ep - sp + 1} physical pages ({printed_range})."
        })

    # 3. Add EPOS 2067 (Place of Service Policy)
    inventory_rows.append({
        "guideline_id": "EPOS-2067",
        "guideline_title": "Evolent Place of Service Policy 2067 for Radiology (2026 Final)",
        "source_pdf": Path(EPOS_PDF_REL).name,
        "policy_version": "2026 Final",
        "physical_start_page": 1,
        "physical_end_page": 11,
        "printed_page_range": "Page 1 of 11 - Page 11 of 11",
        "section_identifiers": "STATEMENT; LEVEL OF CARE; PLACE OF SERVICE; POLICY AND PROCEDURE; CODING AND STANDARDS",
        "parsing_status": "SOURCE_PARSED",
        "extraction_status": "NOT_STARTED",
        "rules_extracted_count": 0,
        "human_review_count": 0,
        "validation_issues_count": 0,
        "completion_status": "IN_PROGRESS",
        "notes": "Supplementary Place of Service policy establishing hospital outpatient vs freestanding clinical criteria."
    })

    # Write CSV
    out_csv = RULES_DIR / "guideline_coverage_inventory.csv"
    fields = [
        "guideline_id",
        "guideline_title",
        "source_pdf",
        "policy_version",
        "physical_start_page",
        "physical_end_page",
        "printed_page_range",
        "section_identifiers",
        "parsing_status",
        "extraction_status",
        "rules_extracted_count",
        "human_review_count",
        "validation_issues_count",
        "completion_status",
        "notes"
    ]

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(inventory_rows)

    print(f"Generated {out_csv} with {len(inventory_rows)} inventory entries.")

if __name__ == "__main__":
    main()
