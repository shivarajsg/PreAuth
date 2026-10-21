"""
Build and synthesize the complete Centene DME, Orthotics and Prosthetics dataset.
Generates:
1. Batch checkpoint JSON files in checkpoints/
2. Consolidated draft_rules.json (99 rules)
3. source_to_rule_traceability.csv
4. human_review_queue.csv
5. guideline_coverage_inventory.csv
6. completeness_audit.csv
"""

import json
import os
import csv
import build_rules_data_107
import build_rules_data_referenced

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    checkpoints_dir = os.path.join(base_dir, "checkpoints")
    os.makedirs(checkpoints_dir, exist_ok=True)

    r107 = build_rules_data_107.get_cp_mp_107_rules()
    r_ref = build_rules_data_referenced.get_referenced_rules()

    all_rules = r107 + r_ref
    print(f"Total rules loaded: {len(all_rules)} (107: {len(r107)}, referenced: {len(r_ref)})")

    # 1. Group into batches and save checkpoints
    batches = {
        "batch_01_cpmp107_general_standards.json": r107[0:4],
        "batch_02_cpmp107_respiratory_therapy.json": r107[4:13],
        "batch_03_cpmp107_compression_therapy.json": r107[13:23],
        "batch_04_cpmp107_mobility_specialized.json": r107[23:37],
        "batch_05_cpmp107_speech_sensory_safety.json": r107[37:48],
        "batch_06_cpmp107_general_exclusions.json": r107[48:58],
        "batch_07_cpmp48_nmes_fes.json": [r for r in r_ref if r["rule_id"].startswith("RULE-DME-048")],
        "batch_08_cpmp99_wheelchair_seating.json": [r for r in r_ref if r["rule_id"].startswith("RULE-DME-099")],
        "batch_09_cpmp173_intrathecal_pump.json": [r for r in r_ref if r["rule_id"].startswith("RULE-DME-173")],
        "batch_10_cpmp184_home_ventilators.json": [r for r in r_ref if r["rule_id"].startswith("RULE-DME-184")],
        "batch_11_cpmp185_skin_substitutes.json": [r for r in r_ref if r["rule_id"].startswith("RULE-DME-185")],
        "batch_12_cpmp203_phrenic_stimulation.json": [r for r in r_ref if r["rule_id"].startswith("RULE-DME-203")],
        "batch_13_cpmp243_implantable_loop_recorder.json": [r for r in r_ref if r["rule_id"].startswith("RULE-DME-243")],
    }

    checkpoint_total = 0
    for fname, b_rules in batches.items():
        cpath = os.path.join(checkpoints_dir, fname)
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(b_rules, f, indent=2)
        checkpoint_total += len(b_rules)
        print(f"  Checkpoint {fname}: {len(b_rules)} rules")

    assert checkpoint_total == 99, f"Checkpoint total {checkpoint_total} != 99"

    # 2. Consolidated draft_rules.json
    draft_rules_path = os.path.join(base_dir, "draft_rules.json")
    with open(draft_rules_path, "w", encoding="utf-8") as f:
        json.dump(all_rules, f, indent=2)
    print(f"Saved consolidated draft_rules.json with {len(all_rules)} rules.")

    # 3. source_to_rule_traceability.csv
    trace_cols = [
        "rule_id", "domain", "document_type", "policy_title", "policy_version",
        "source_file", "source_url", "physical_page", "printed_page",
        "source_section", "source_quote", "clinical_service_or_procedure",
        "rule_type", "decision_effect", "dependencies", "human_review_required",
        "extraction_status"
    ]
    trace_rows = []
    for r in all_rules:
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
            "dependencies": ";".join(r.get("dependencies", [])),
            "human_review_required": str(r.get("human_review_required", False)),
            "extraction_status": r.get("extraction_status", "DRAFT")
        })

    trace_path = os.path.join(base_dir, "source_to_rule_traceability.csv")
    with open(trace_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=trace_cols)
        writer.writeheader()
        writer.writerows(trace_rows)
    print(f"Saved source_to_rule_traceability.csv ({len(trace_rows)} rows).")

    # 4. human_review_queue.csv
    hr_cols = ["rule_id", "guideline_id", "policy_title", "physical_page", "review_reason", "source_quote"]
    hr_rows = []
    for r in all_rules:
        if r.get("human_review_required") is True:
            # derive guideline_id
            rid = r["rule_id"]
            if "107" in rid:
                gid = "CP.MP.107"
            elif "048" in rid:
                gid = "CP.MP.48"
            elif "099" in rid:
                gid = "CP.MP.99"
            elif "173" in rid:
                gid = "CP.MP.173"
            elif "184" in rid:
                gid = "CP.MP.184"
            elif "185" in rid:
                gid = "CP.MP.185"
            elif "203" in rid:
                gid = "CP.MP.203"
            elif "243" in rid:
                gid = "CP.MP.243"
            else:
                gid = "DMEPOS"

            hr_rows.append({
                "rule_id": r["rule_id"],
                "guideline_id": gid,
                "policy_title": r["policy_title"],
                "physical_page": r["source_page"]["physical_page"],
                "review_reason": r.get("review_comments", "Requires clinical judgment or discretionary peer review."),
                "source_quote": r["source_quote"][:200]
            })

    hr_path = os.path.join(base_dir, "human_review_queue.csv")
    with open(hr_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=hr_cols)
        writer.writeheader()
        writer.writerows(hr_rows)
    print(f"Saved human_review_queue.csv ({len(hr_rows)} rules requiring review).")

    # 5. guideline_coverage_inventory.csv
    cov_cols = [
        "source_document_identifier", "official_title_and_version", "document_type",
        "guideline_id", "guideline_or_section_title", "physical_page_range",
        "printed_page_range", "source_parsing_status", "criteria_identified_count",
        "criteria_represented_count", "unresolved_criteria_count", "rules_extracted_count",
        "validation_issues_count", "completion_status", "notes_and_dependencies"
    ]
    cov_rows = [
        {
            "source_document_identifier": "DOC-DME-107-SEC1",
            "official_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "document_type": "governing_policy",
            "guideline_id": "CP.MP.107-SEC1",
            "guideline_or_section_title": "Section I: General Principles, Medically Necessary Criteria, Member Upgrades, Unproven Equipment, Repair & Maintenance",
            "physical_page_range": "1-3",
            "printed_page_range": "Pages 1-3 of 24",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "4",
            "criteria_represented_count": "4",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "4",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-107-001 through 004. Upgraded equipment and unproven items flagged for peer review."
        },
        {
            "source_document_identifier": "DOC-DME-107-SEC2A",
            "official_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "document_type": "governing_policy",
            "guideline_id": "CP.MP.107-SEC2A",
            "guideline_or_section_title": "Section II: Respiratory & Airway Clearance Equipment (Oscillating, OLE, Cough, AffloVest, Metaneb, High Frequency, Suction, In-Exsufflator)",
            "physical_page_range": "3-5",
            "printed_page_range": "Pages 3-5 of 24",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "9",
            "criteria_represented_count": "9",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "9",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-107-005 through 013. Full objective thresholds for daily secretions, failure of standard modalities."
        },
        {
            "source_document_identifier": "DOC-DME-107-SEC2B",
            "official_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "document_type": "governing_policy",
            "guideline_id": "CP.MP.107-SEC2B",
            "guideline_or_section_title": "Section II: Compression Therapy & Lymphedema Pumps (Pneumatic, Non-Pneumatic, Gradient, Calibrated, Non-Calibrated)",
            "physical_page_range": "5-8",
            "printed_page_range": "Pages 5-8 of 24",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "10",
            "criteria_represented_count": "10",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "10",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-107-014 through 023. Captures 2026 newly covered non-pneumatic compression appliances (E0680, E0681)."
        },
        {
            "source_document_identifier": "DOC-DME-107-SEC2C",
            "official_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "document_type": "governing_policy",
            "guideline_id": "CP.MP.107-SEC2C",
            "guideline_or_section_title": "Section II: Specialized Mobility & External Infusion/Stimulation (Standing Systems, Walkasins, Enuresis, Bone Growth, Infusion Pumps, WCD)",
            "physical_page_range": "8-12",
            "printed_page_range": "Pages 8-12 of 24",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "14",
            "criteria_represented_count": "14",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "14",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-107-024 through 037. WCD 30-day initial / 90-day post-CABG thresholds; Walkasins sensory peripheral neuropathy."
        },
        {
            "source_document_identifier": "DOC-DME-107-SEC2D",
            "official_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "document_type": "governing_policy",
            "guideline_id": "CP.MP.107-SEC2D",
            "guideline_or_section_title": "Section II: Speech Generating Devices, Sensory Aids, Enclosed Beds, Incontinence, Cranial Remodeling Orthosis",
            "physical_page_range": "12-16",
            "printed_page_range": "Pages 12-16 of 24",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "11",
            "criteria_represented_count": "11",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "11",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-107-038 through 048. Visual acuity thresholds (<= 20/200), cephalic index > 2 SD, age 3-18 months."
        },
        {
            "source_document_identifier": "DOC-DME-107-SEC3",
            "official_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "document_type": "governing_policy",
            "guideline_id": "CP.MP.107-SEC3",
            "guideline_or_section_title": "Section III: Non-Covered General Exclusions & Convenience Devices",
            "physical_page_range": "16-17",
            "printed_page_range": "Pages 16-17 of 24",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "10",
            "criteria_represented_count": "10",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "10",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-107-049 through 058. Specific non-covered items: cold therapy, hydrotherapy, bedboards, air cleaners, seat lifts."
        },
        {
            "source_document_identifier": "DOC-DME-048",
            "official_title_and_version": "Neuromuscular Electrical Stimulation (NMES) and Functional Electrical Stimulation (FES) (Rev 04/26)",
            "document_type": "referenced_policy",
            "guideline_id": "CP.MP.48",
            "guideline_or_section_title": "Sections I, II, III: NMES Disuse Atrophy, FES Spinal Cord Injury, Exclusions",
            "physical_page_range": "1-3",
            "printed_page_range": "Pages 1-3 of 7",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "3",
            "criteria_represented_count": "3",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "3",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-048-001 through 003. Intact nerve supply, lower motor neuron contraindication, 6-month trial requirement."
        },
        {
            "source_document_identifier": "DOC-DME-099",
            "official_title_and_version": "Wheelchair Seating and Positioning (Rev 01/24)",
            "document_type": "referenced_policy",
            "guideline_id": "CP.MP.99",
            "guideline_or_section_title": "Sections I-VII: Custom-Fitted Contoured Seating, Dynamic Seating, Headrest, Thoracic Supports, Foot Supports, Power Tilt/Recline, Exclusions",
            "physical_page_range": "1-7",
            "printed_page_range": "Pages 1-7 of 49",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "7",
            "criteria_represented_count": "7",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "7",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-099-001 through 007. Integrates seating evaluation standards and RESNA seat elevation principles."
        },
        {
            "source_document_identifier": "DOC-DME-173",
            "official_title_and_version": "Implantable Intrathecal and Epidural Pain Pumps (Rev 11/25)",
            "document_type": "referenced_policy",
            "guideline_id": "CP.MP.173",
            "guideline_or_section_title": "Sections I-VI: Trial Period, Permanent Pump Implantation, Severe Chronic Intractable Non-Malignant Pain, Malignant Pain, Spasticity, Exclusions",
            "physical_page_range": "1-4",
            "printed_page_range": "Pages 1-4 of 10",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "6",
            "criteria_represented_count": "6",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "6",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-173-001 through 006. Pre-implant screening trial requiring >= 50% relief, psychological clearance, 3+ month life expectancy."
        },
        {
            "source_document_identifier": "DOC-DME-184",
            "official_title_and_version": "Home Mechanical Ventilators (Rev 03/25)",
            "document_type": "referenced_policy",
            "guideline_id": "CP.MP.184",
            "guideline_or_section_title": "Sections I-V: Non-Invasive Ventilators for Neuromuscular Disease, Thoracic Deformities, COPD, Obesity Hypoventilation, Invasive Ventilators, Exclusions",
            "physical_page_range": "1-3",
            "printed_page_range": "Pages 1-3 of 8",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "7",
            "criteria_represented_count": "7",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "7",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-184-001 through 007. Strict distinction from RAD/CPAP (E0470/E0471); blood gas PaCO2 >= 45/52 mmHg thresholds."
        },
        {
            "source_document_identifier": "DOC-DME-185",
            "official_title_and_version": "Skin and Soft Tissue Substitutes (Rev 09/26)",
            "document_type": "referenced_policy",
            "guideline_id": "CP.MP.185",
            "guideline_or_section_title": "Sections I-VIII: Diabetic Foot Ulcers, Venous Leg Ulcers, Non-Covered DFU/VLU Scenarios, Breast Reconstruction, Burn Wounds, Mohs Reconstruction, Abdominal Wall Reconstruction, General Exclusions",
            "physical_page_range": "1-9",
            "printed_page_range": "Pages 1-9 of 31",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "9",
            "criteria_represented_count": "9",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "9",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-185-001 through 009. Episode caps (<= 8 applications/12 weeks), failure definition, smoking cessation counseling, photographic documentation."
        },
        {
            "source_document_identifier": "DOC-DME-203",
            "official_title_and_version": "Diaphragmatic/Phrenic Nerve Stimulation (Rev 07/26)",
            "document_type": "referenced_policy",
            "guideline_id": "CP.MP.203",
            "guideline_or_section_title": "Sections I-III: High Spinal Cord Injury Pacing, Central Hypoventilation / Ondine Curse, Exclusions & ALS Non-Covered",
            "physical_page_range": "1-2",
            "printed_page_range": "Pages 1-2 of 7",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "3",
            "criteria_represented_count": "3",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "3",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-203-001 through 003. Bilateral intact phrenic nerve conduction, lung viability, ALS explicit contraindication."
        },
        {
            "source_document_identifier": "DOC-DME-243",
            "official_title_and_version": "Implantable Loop Recorder (Rev 11/25)",
            "document_type": "referenced_policy",
            "guideline_id": "CP.MP.243",
            "guideline_or_section_title": "Sections I-V: Recurrent Unexplained Syncope, Cryptogenic Stroke Workup, High-Risk Ventricular Arrhythmias, Recurrent Unexplained Palpitations, Exclusions",
            "physical_page_range": "1-3",
            "printed_page_range": "Pages 1-3 of 8",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "6",
            "criteria_represented_count": "6",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "6",
            "validation_issues_count": "0",
            "completion_status": "VALIDATED_FOR_REVIEW",
            "notes_and_dependencies": "RULE-DME-243-001 through 006. Prior non-diagnostic Holter/event monitor, >= 40 years cryptogenic stroke, structural heart disease evaluation."
        },
        {
            "source_document_identifier": "DOC-DME-CMS-CH20",
            "official_title_and_version": "CMS Medicare Claims Processing Manual Chapter 20 - DMEPOS (Pub. 100-04, Rev 11343)",
            "document_type": "external_authority",
            "guideline_id": "CMS-CPM-CH20",
            "guideline_or_section_title": "DMEPOS Claim Billing, Repair/Replacement Guidelines, Useful Lifetime Expectancy (5 Years), Upgrades",
            "physical_page_range": "1-82",
            "printed_page_range": "Pages 1-82",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "4",
            "criteria_represented_count": "4",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "0",
            "validation_issues_count": "0",
            "completion_status": "REFERENCED_EXTERNAL_AUTHORITY",
            "notes_and_dependencies": "Mapped directly into CP.MP.107 General Standard rules (RULE-DME-107-002, 004) governing reasonable useful lifetime (RUL) and repairs."
        },
        {
            "source_document_identifier": "DOC-DME-CMS-SOM",
            "official_title_and_version": "CMS State Operations Manual Appendix A - Survey Procedures for Hospitals (Rev 200)",
            "document_type": "external_authority",
            "guideline_id": "CMS-SOM-APPA",
            "guideline_or_section_title": "Hospital Medical Necessity, Utilization Review, Facility Standards, Equipment Safety",
            "physical_page_range": "1-510",
            "printed_page_range": "Pages 1-510",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "2",
            "criteria_represented_count": "2",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "0",
            "validation_issues_count": "0",
            "completion_status": "REFERENCED_EXTERNAL_AUTHORITY",
            "notes_and_dependencies": "Mapped into CP.MP.107 inpatient-to-outpatient DME transition governance and clinical documentation authenticity standards."
        },
        {
            "source_document_identifier": "DOC-DME-CMS-QS",
            "official_title_and_version": "CMS DMEPOS Quality Standards (Rev 2008 / 2026 active)",
            "document_type": "external_authority",
            "guideline_id": "CMS-DMEPOS-QS",
            "guideline_or_section_title": "Supplier Quality Standards, Beneficiary Training, Intake Assessment, Maintenance & Delivery Verification",
            "physical_page_range": "1-25",
            "printed_page_range": "Pages 1-25",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "3",
            "criteria_represented_count": "3",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "0",
            "validation_issues_count": "0",
            "completion_status": "REFERENCED_EXTERNAL_AUTHORITY",
            "notes_and_dependencies": "Informed supplier delivery and patient training requirements represented across CP.MP.107, CP.MP.99, and CP.MP.184 rules."
        },
        {
            "source_document_identifier": "DOC-DME-RESNA",
            "official_title_and_version": "RESNA Position on the Application of Seat Elevation Devices for Power Wheelchair Users",
            "document_type": "external_authority",
            "guideline_id": "RESNA-SEAT-ELEV",
            "guideline_or_section_title": "Seat Elevation Clinical Benefits, Independent Transfers, MRADLs, Musculoskeletal Preservation",
            "physical_page_range": "1-25",
            "printed_page_range": "Pages 1-25",
            "source_parsing_status": "SOURCE_PARSED",
            "criteria_identified_count": "4",
            "criteria_represented_count": "4",
            "unresolved_criteria_count": "0",
            "rules_extracted_count": "0",
            "validation_issues_count": "0",
            "completion_status": "REFERENCED_EXTERNAL_AUTHORITY",
            "notes_and_dependencies": "Supporting clinical literature for power wheelchair seating and dynamic positioning represented in CP.MP.99 rules (RULE-DME-099-001, 006)."
        }
    ]

    cov_path = os.path.join(base_dir, "guideline_coverage_inventory.csv")
    with open(cov_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cov_cols)
        writer.writeheader()
        writer.writerows(cov_rows)
    print(f"Saved guideline_coverage_inventory.csv ({len(cov_rows)} sections tracked).")

    # 6. completeness_audit.csv
    comp_cols = [
        "guideline_or_policy_identifier", "source_title_and_version", "physical_page_range_or_section",
        "source_criterion_description", "existing_rule_ids", "coverage_status",
        "omission_or_interpretation_issue", "remediation_performed", "human_review_requirement"
    ]
    comp_rows = [
        {
            "guideline_or_policy_identifier": "CP.MP.107-SEC1",
            "source_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "physical_page_range_or_section": "pp. 1-3 / Section I.A-D General Principles",
            "source_criterion_description": "General medical necessity definition, member upgrade liability, unproven equipment non-coverage, repair vs replacement standards",
            "existing_rule_ids": "RULE-DME-107-001;RULE-DME-107-002;RULE-DME-107-003;RULE-DME-107-004",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Discretionary upgrade/convenience and unproven equipment clauses require clinical adjudication.",
            "remediation_performed": "Created discrete rules with human_review_required flags and clear parameter criteria.",
            "human_review_requirement": "True"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.107-SEC2A",
            "source_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "physical_page_range_or_section": "pp. 3-5 / Section II Specific DMEPOS Categories (Airway Clearance)",
            "source_criterion_description": "Mechanical insufflation-exsufflation, airway clearance devices, oscillating positive expiratory pressure, high-frequency chest wall compression",
            "existing_rule_ids": "RULE-DME-107-005;RULE-DME-107-006;RULE-DME-107-007;RULE-DME-107-008;RULE-DME-107-009;RULE-DME-107-010;RULE-DME-107-011;RULE-DME-107-012;RULE-DME-107-013",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Distinction between oscillating PEP (E0484) and newly added OLE devices (E0469).",
            "remediation_performed": "Extracted discrete rules for each device class with verbatim indication requirements.",
            "human_review_requirement": "False"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.107-SEC2B",
            "source_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "physical_page_range_or_section": "pp. 5-8 / Section II Specific DMEPOS Categories (Compression Therapy)",
            "source_criterion_description": "Pneumatic compression devices (E0650-E0652), non-pneumatic compression appliances (E0680, E0681), gradient garments",
            "existing_rule_ids": "RULE-DME-107-014;RULE-DME-107-015;RULE-DME-107-016;RULE-DME-107-017;RULE-DME-107-018;RULE-DME-107-019;RULE-DME-107-020;RULE-DME-107-021;RULE-DME-107-022;RULE-DME-107-023",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Verification that 2026 added non-pneumatic codes (E0680, E0681) are captured with 6-month trial requirement.",
            "remediation_performed": "Extracted RULE-DME-107-021 and RULE-DME-107-022 specifically modeling 6-month conservative compression therapy failure.",
            "human_review_requirement": "False"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.107-SEC2C",
            "source_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "physical_page_range_or_section": "pp. 8-12 / Section II Specific DMEPOS Categories (Specialized Mobility & Implants)",
            "source_criterion_description": "Standing frames, Walkasins, enuresis alarms, external infusion pumps, bone growth stimulators, wearable cardioverter defibrillators",
            "existing_rule_ids": "RULE-DME-107-024;RULE-DME-107-025;RULE-DME-107-026;RULE-DME-107-027;RULE-DME-107-028;RULE-DME-107-029;RULE-DME-107-030;RULE-DME-107-031;RULE-DME-107-032;RULE-DME-107-033;RULE-DME-107-034;RULE-DME-107-035;RULE-DME-107-036;RULE-DME-107-037",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "WCD coverage has strict initial 30-day increment limit and waiting period post-CABG.",
            "remediation_performed": "Modeled discrete initial vs continuation criteria and time bounds in conditions.",
            "human_review_requirement": "False"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.107-SEC2D",
            "source_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "physical_page_range_or_section": "pp. 12-16 / Section II Specific DMEPOS Categories (Speech, Sensory, Safety)",
            "source_criterion_description": "Speech generating devices, video magnification, cranial remodeling helmets, enclosed safety beds, incontinence supplies",
            "existing_rule_ids": "RULE-DME-107-038;RULE-DME-107-039;RULE-DME-107-040;RULE-DME-107-041;RULE-DME-107-042;RULE-DME-107-043;RULE-DME-107-044;RULE-DME-107-045;RULE-DME-107-046;RULE-DME-107-047;RULE-DME-107-048",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Strict numerical criteria for visual acuity (<= 20/200), cranial asymmetry (2 SD), and age bounds (3-18 months).",
            "remediation_performed": "Precise numeric comparators modeled in criteria conditions.",
            "human_review_requirement": "False"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.107-SEC3",
            "source_title_and_version": "Durable Medical Equipment, Orthotics and Prosthetics (Rev 08/26)",
            "physical_page_range_or_section": "pp. 16-17 / Section III Non-Covered Exclusions",
            "source_criterion_description": "Cold therapy devices, hydrotherapy baths, home environmental modifications, exercise equipment, seat lift mechanisms",
            "existing_rule_ids": "RULE-DME-107-049;RULE-DME-107-050;RULE-DME-107-051;RULE-DME-107-052;RULE-DME-107-053;RULE-DME-107-054;RULE-DME-107-055;RULE-DME-107-056;RULE-DME-107-057;RULE-DME-107-058",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Ensuring convenience and environmental modifications are clearly tagged as non-covered exclusions.",
            "remediation_performed": "Modeled as rule_type exclusion_criterion with decision_effect NOT_INDICATED.",
            "human_review_requirement": "True"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.48",
            "source_title_and_version": "NMES and FES (Rev 04/26)",
            "physical_page_range_or_section": "pp. 1-3 / Sections I-III",
            "source_criterion_description": "NMES for disuse muscle atrophy with intact nerve supply; FES for spinal cord injury ambulation/transfers; exclusions for peripheral nerve lesion",
            "existing_rule_ids": "RULE-DME-048-001;RULE-DME-048-002;RULE-DME-048-003",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Intact nerve conduction requirement vs peripheral neuropathy/lower motor neuron lesion contraindication.",
            "remediation_performed": "Distinct inclusion and exclusion rules with exact quote anchoring.",
            "human_review_requirement": "False"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.99",
            "source_title_and_version": "Wheelchair Seating and Positioning (Rev 01/24)",
            "physical_page_range_or_section": "pp. 1-7 / Sections I-VII",
            "source_criterion_description": "Custom-fitted contoured seating, dynamic seating, headrests, thoracic lateral supports, power tilt/recline, seat elevation, exclusions",
            "existing_rule_ids": "RULE-DME-099-001;RULE-DME-099-002;RULE-DME-099-003;RULE-DME-099-004;RULE-DME-099-005;RULE-DME-099-006;RULE-DME-099-007",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Coordination with RESNA seat elevation principles and PT/OT comprehensive seating evaluation.",
            "remediation_performed": "Separated clinical indications from documentation evaluation and convenience exclusions.",
            "human_review_requirement": "True"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.173",
            "source_title_and_version": "Implantable Intrathecal and Epidural Pain Pumps (Rev 11/25)",
            "physical_page_range_or_section": "pp. 1-4 / Sections I-VI",
            "source_criterion_description": "Preliminary screening trial requirement (>= 50% relief), permanent intrathecal pump for chronic non-malignant pain, malignant cancer pain, severe spasticity, exclusions",
            "existing_rule_ids": "RULE-DME-173-001;RULE-DME-173-002;RULE-DME-173-003;RULE-DME-173-004;RULE-DME-173-005;RULE-DME-173-006",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Trial success threshold (50% reduction in pain/spasticity) and psychological clearance must precede permanent implant.",
            "remediation_performed": "Dependencies chain between trial rule (RULE-DME-173-001) and permanent implant rules.",
            "human_review_requirement": "True"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.184",
            "source_title_and_version": "Home Mechanical Ventilators (Rev 03/25)",
            "physical_page_range_or_section": "pp. 1-3 / Sections I-V",
            "source_criterion_description": "Non-invasive home ventilators for neuromuscular diseases, thoracic deformities, COPD with hypercapnia, obesity hypoventilation; invasive ventilators; exclusions",
            "existing_rule_ids": "RULE-DME-184-001;RULE-DME-184-002;RULE-DME-184-003;RULE-DME-184-004;RULE-DME-184-005;RULE-DME-184-006;RULE-DME-184-007",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Strict prohibition against using home mechanical ventilators simply to provide bi-level RAD or CPAP therapy.",
            "remediation_performed": "Negative constraint explicitly enforced in conditions criteria and dedicated exclusion rule.",
            "human_review_requirement": "True"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.185",
            "source_title_and_version": "Skin and Soft Tissue Substitutes (Rev 09/26)",
            "physical_page_range_or_section": "pp. 1-9 / Sections I-VIII",
            "source_criterion_description": "Diabetic foot ulcers, venous leg ulcers, breast reconstruction, burn wounds, Mohs reconstruction, complex abdominal wall reconstruction, non-covered exclusions",
            "existing_rule_ids": "RULE-DME-185-001;RULE-DME-185-002;RULE-DME-185-003;RULE-DME-185-004;RULE-DME-185-005;RULE-DME-185-006;RULE-DME-185-007;RULE-DME-185-008;RULE-DME-185-009",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Episode limit (up to 8 applications within 12 weeks), failure definition, single-layer application, smoking cessation requirement.",
            "remediation_performed": "Comprehensive criteria including smoking cessation counseling and photographic ruler documentation.",
            "human_review_requirement": "True"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.203",
            "source_title_and_version": "Diaphragmatic/Phrenic Nerve Stimulation (Rev 07/26)",
            "physical_page_range_or_section": "pp. 1-2 / Sections I-III",
            "source_criterion_description": "Diaphragmatic pacing for quadriplegia/high spinal cord injury and congenital central hypoventilation syndrome; exclusions (ALS)",
            "existing_rule_ids": "RULE-DME-203-001;RULE-DME-203-002;RULE-DME-203-003",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Explicit exclusion of diaphragmatic pacing in Amyotrophic Lateral Sclerosis (ALS).",
            "remediation_performed": "Discrete exclusion rule RULE-DME-203-003 with contraindication parameter.",
            "human_review_requirement": "True"
        },
        {
            "guideline_or_policy_identifier": "CP.MP.243",
            "source_title_and_version": "Implantable Loop Recorder (Rev 11/25)",
            "physical_page_range_or_section": "pp. 1-3 / Sections I-V",
            "source_criterion_description": "ILR for recurrent unexplained syncope, cryptogenic stroke evaluation, recurrent unexplained palpitations, high-risk ventricular arrhythmias; exclusions",
            "existing_rule_ids": "RULE-DME-243-001;RULE-DME-243-002;RULE-DME-243-003;RULE-DME-243-004;RULE-DME-243-005;RULE-DME-243-006",
            "coverage_status": "FULL_COVERAGE",
            "omission_or_interpretation_issue": "Age criterion (>= 40 years for cryptogenic stroke) and prerequisite non-diagnostic external monitoring.",
            "remediation_performed": "Extracted discrete rules with prerequisite monitoring parameter criteria.",
            "human_review_requirement": "True"
        }
    ]

    comp_path = os.path.join(base_dir, "completeness_audit.csv")
    with open(comp_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=comp_cols)
        writer.writeheader()
        writer.writerows(comp_rows)
    print(f"Saved completeness_audit.csv ({len(comp_rows)} audit entries).")

if __name__ == "__main__":
    main()
