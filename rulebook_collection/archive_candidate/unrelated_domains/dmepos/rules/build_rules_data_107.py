"""Centene DMEPOS Clinical Policy CP.MP.107 Rule Definitions (Revision 08/26).

Contains 58 atomic, source-grounded rules extracted from CP.MP.107.
"""

from pathlib import Path

BASE_POLICY = {
    "domain": "centene_dme_orthotics_prosthetics",
    "document_type": "governing_policy",
    "policy_title": (
        "Clinical Policy CP.MP.107: Durable Medical Equipment and Orthotics"
        " and Prosthetics Guidelines (Rev. 08/26)"
    ),
    "policy_version": "Revision 08/26",
    "version_status": "current_2026_verified",
    "source_file": (
        "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.107"
        " (Revision 08-26).pdf"
    ),
    "source_url": (
        "https://www.centene.com/content/dam/centene/policies/clinical-policies/CP.MP.107.pdf"
    ),
}


def get_cp_mp_107_rules():
  rules = [
      # 1. General Necessity & Reasonableness
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 24"},
          "source_section": "Policy/Criteria - Section I.A.1 General Criteria",
          "source_quote": (
              "Equipment is necessary and reasonable for the treatment of an"
              " illness or injury or to improve the functioning of a physical"
              " deficit;*"
          ),
          "clinical_service_or_procedure": (
              "Durable Medical Equipment, Orthotics, and Prosthetics - General"
              " Medical Necessity and Reasonableness Standard"
          ),
          "rule_type": "clinical_prerequisite",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-001-A",
                      "description": (
                          "Equipment makes a meaningful contribution to"
                          " treatment of illness/injury or improvement of"
                          " malformed body member"
                      ),
                      "parameter": "medical_necessity_contribution",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-107-001-B",
                      "description": (
                          "Expense of item is not disproportionate to"
                          " therapeutic benefits and not substantially more"
                          " costly than feasible alternative"
                      ),
                      "parameter": "cost_reasonableness_evaluation",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Clinical documentation establishing medical necessity and"
              " reasonable contribution to care",
              "Comparative cost analysis if higher cost alternative is"
              " requested over standard item",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": [
              "CMS Medicare Claims Processing Manual Ch. 20 Section 10"
          ],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Preamble standard: if a lesser cost medically necessary item"
              " exists, higher cost item will be denied."
          ),
      },
      # 2. General Education & Trial
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-002",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 24"},
          "source_section": "Policy/Criteria - Section I.A.2 General Criteria",
          "source_quote": (
              "Both of the following have been provided to the member/enrollee"
              " and/or caregiver, as applicable: a. Education regarding use of"
              " the device, with demonstrated understanding; b. A trial of the"
              " requested device, with demonstrated ability to use it safely"
              " and effectively."
          ),
          "clinical_service_or_procedure": (
              "Durable Medical Equipment, Orthotics, and Prosthetics - Patient"
              " Education and Device Trial Requirement"
          ),
          "rule_type": "clinical_prerequisite",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-002-A",
                      "description": (
                          "Education regarding use of device provided with"
                          " demonstrated understanding"
                      ),
                      "parameter": "device_education_provided",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-002-B",
                      "description": (
                          "Trial of requested device completed with"
                          " demonstrated ability to use safely and effectively"
                      ),
                      "parameter": "device_trial_successful",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Caregiver or member education attestation",
              "Device trial documentation demonstrating safe and effective use",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Mandatory prerequisite for all DMEPOS items under Section I.A.2."
          ),
      },
      # 3. Deluxe / Aesthetic Features Exclusion
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-003",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 24"},
          "source_section": (
              "Policy/Criteria - Section I.A Note on Deluxe Features"
          ),
          "source_quote": (
              'Additional "deluxe" features or items that are rented or'
              " purchased for aesthetic reasons or added convenience, do not"
              " meet the reasonableness test."
          ),
          "clinical_service_or_procedure": (
              "Deluxe DME Features, Aesthetic Additions, and Convenience Items"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-003-A",
                      "description": (
                          "Requested item or component is for aesthetic reasons"
                      ),
                      "parameter": "aesthetic_purpose",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-003-B",
                      "description": (
                          "Requested item or component is for added convenience"
                      ),
                      "parameter": "convenience_purpose",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Deluxe/convenience features fail reasonableness test."
          ),
      },
      # 4. Member/Enrollee's Home Inpatient Exclusion
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-004",
          "source_page": {"physical_page": 13, "printed_page": "Page 13 of 24"},
          "source_section": "Background - Member/Enrollee’s Home",
          "source_quote": (
              "However, an institution may not be considered a"
              " member/enrollee’s home if the following are met: • Meets at"
              " least the basic requirement in the definition of a hospital,"
              " i.e., it is primarily engaged in providing by or under the"
              " supervision of physicians, inpatient, diagnostic and"
              " therapeutic services for medical diagnosis, treatment, and"
              " care of injured, disabled, and sick persons, or rehabilitation"
              " services for the rehabilitation of injured, disabled, or sick"
              " persons; or • Meets at least the basic requirement in the"
              " definition of a skilled nursing facility, i.e., it is primarily"
              " engaged in providing to inpatients skilled nursing care and"
              " related services for members/enrollees who require medical or"
              " nursing care, or rehabilitation services for the"
              " rehabilitation of injured, disabled, or sick persons."
          ),
          "clinical_service_or_procedure": (
              "DMEPOS Place of Service - Hospital or Skilled Nursing Facility"
              " Inpatient Exclusion"
          ),
          "rule_type": "place_of_service",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-004-A",
                      "description": (
                          "Member resides in hospital providing inpatient"
                          " diagnostic/therapeutic services"
                      ),
                      "parameter": "institution_type",
                      "comparator": "EQUALS",
                      "value": "HOSPITAL",
                  },
                  {
                      "condition_id": "COND-DME-107-004-B",
                      "description": (
                          "Member resides in skilled nursing facility providing"
                          " inpatient skilled nursing care (without permanent"
                          " address change)"
                      ),
                      "parameter": "institution_type",
                      "comparator": "EQUALS",
                      "value": "SNF_NON_PERMANENT",
                  },
              ],
          },
          "exclusion_conditions": [
              "Permanent admission to SNF or inpatient hospice where home"
              " address has been officially changed"
          ],
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["CMS SOM Appendix A"],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Exception applies if member permanently admitted to SNF/hospice"
              " and changed official home address."
          ),
      },
      # 5. Speech Generating Device Mobile Tech
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-005",
          "source_page": {"physical_page": 14, "printed_page": "Page 14 of 24"},
          "source_section": "Background - Medical Equipment",
          "source_quote": (
              "Personal computers or mobile technology such as iPads, smart"
              " phones, iPods, personal digital assistants, etc., may be"
              " considered as medical equipment when used for the purpose of"
              " speech generating equipment when other non-medical functions"
              " are limited or disabled and that device is used as the primary"
              " source of communication for those qualifying for a speech"
              " generating device."
          ),
          "clinical_service_or_procedure": (
              "Speech Generating Equipment Interfaces (Tablet, Computer, Mobile"
              " Device)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-005-A",
                      "description": (
                          "Member qualifies for a speech generating device"
                      ),
                      "parameter": "speech_generating_device_eligible",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-005-B",
                      "description": (
                          "Non-medical functions on personal computer or mobile"
                          " device are limited or disabled"
                      ),
                      "parameter": "non_medical_functions_locked",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-005-C",
                      "description": (
                          "Device is used as the primary source of"
                          " communication"
                      ),
                      "parameter": "primary_communication_source",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Speech-language pathologist comprehensive evaluation",
              (
                  "Device configuration report confirming dedicated/locked"
                  " communication state"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["CP.MP.48 Speech Generating Devices"],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Requires dedicated software configuration restricting device"
              " solely to communication function."
          ),
      },
      # 6. Burn Garments
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-006",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 24"},
          "source_section": "Policy/Criteria - BURN GARMENTS",
          "source_quote": (
              "Medically necessary with associated physical and/or occupational"
              " therapy when both of the following are met: A. At risk of a"
              " post-burn contracture; B. The garment and physical and/or"
              " occupational therapies are being used with the intent of"
              " preventing the need for skin grafting or contractures as a"
              " result of hypertrophic scarring."
          ),
          "clinical_service_or_procedure": (
              "Burn garments (HCPCS A6501, A6502, A6503, A6504, A6505, A6506,"
              " A6507, A6508, A6509, A6510, A6511, A6512, A6513)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-006-A",
                      "description": "Member is at risk of post-burn contracture",
                      "parameter": "post_burn_contracture_risk",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-006-B",
                      "description": (
                          "Garment and associated PT/OT are used to prevent"
                          " need for skin grafting or hypertrophic scarring"
                          " contractures"
                      ),
                      "parameter": (
                          "prevent_grafting_or_hypertrophic_scarring"
                      ),
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Burn surgeon or specialist clinical assessment",
              "Concurrent PT/OT treatment plan targeting contracture prevention",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": "Requires concurrent PT and/or OT therapy regimen.",
      },
      # 7. Non-wearable external defibrillator
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-007",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 24"},
          "source_section": "Policy/Criteria - CARDIAC EQUIPMENT",
          "source_quote": (
              "Not medically necessary, as it is primarily considered a safety"
              " device."
          ),
          "clinical_service_or_procedure": (
              "Non-wearable external defibrillator with integrated ECG analysis"
              " (HCPCS E0617)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-007-A",
                  "description": (
                      "Request is for non-wearable external defibrillator with"
                      " integrated ECG analysis"
                  ),
                  "parameter": "non_wearable_defibrillator_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Deemed a safety device without medical necessity standing."
          ),
      },
      # 8. Wearable Cardioverter-Defibrillator (WCD) Initial Request
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-008",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 24"},
          "source_section": "Policy/Criteria - CARDIAC EQUIPMENT",
          "source_quote": (
              "Initial requests for wearable cardioverter-defibrillators (WCD)"
              " are considered medically necessary for 30 days when meeting all"
              " of the following: A. Member/enrollee is ≥ 18 years of age with"
              " increased risk of sudden cardiac death; B. One of the"
              " following: 1. Awaiting cardiac transplant; 2. Previously"
              " implanted cardioverter-defibrillator (ICD) must be removed due"
              " to infection and awaiting re-implantation; 3. Newly indicated"
              " ICD delayed due to one of the following; a. Systemic infection;"
              " b. Left ventricular ejection fraction (LVEF) ≤ 35% and any of"
              " the following: i. Myocardial infarction (MI) within the past 40"
              " days;"
          ),
          "clinical_service_or_procedure": (
              "Wearable Cardioverter-Defibrillator (WCD) - Initial 30-Day"
              " Request (HCPCS K0606)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-008-A",
                      "description": (
                          "Member is ≥ 18 years of age with increased risk of"
                          " sudden cardiac death"
                      ),
                      "parameter": "age_and_scd_risk",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": "18",
                  },
                  {
                      "condition_id": "COND-DME-107-008-B",
                      "description": (
                          "Awaiting transplant, ICD explant due to infection,"
                          " systemic infection delay, or LVEF ≤ 35% post-MI/CABG"
                      ),
                      "parameter": "wcd_qualifying_cardiac_indication",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Cardiology clinical notes documenting SCD risk",
              "Echocardiogram documenting LVEF",
              "Transplant listing or ICD infection/explantation operative note",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": "Initial coverage is strictly limited to 30 days.",
      },
      # 9. Wearable Cardioverter-Defibrillator (WCD) Ongoing Request
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-009",
          "source_page": {"physical_page": 3, "printed_page": "Page 3 of 24"},
          "source_section": "Policy/Criteria - CARDIAC EQUIPMENT",
          "source_quote": (
              "Ongoing requests for WCDs are considered medically necessary and"
              " will be approved in 30-day increments (up to a total of 90"
              " days) when meeting all of the following: A. Initial request"
              " criteria continue to be met; B. Adherence is confirmed by"
              " device reports and attestation from the ordering provider; C."
              " Plan of care has been updated with progression towards a"
              " definitive treatment pathway."
          ),
          "clinical_service_or_procedure": (
              "Wearable Cardioverter-Defibrillator (WCD) - Ongoing Request"
              " (HCPCS K0606)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-009-A",
                      "description": "Initial request criteria continue to be met",
                      "parameter": "initial_criteria_continuing",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-009-B",
                      "description": (
                          "Adherence confirmed by device reports and"
                          " attestation from ordering provider"
                      ),
                      "parameter": "wcd_adherence_confirmed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-009-C",
                      "description": (
                          "Updated plan of care progressing toward definitive"
                          " treatment pathway"
                      ),
                      "parameter": "definitive_pathway_progression",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Device compliance/adherence download report",
              "Ordering provider attestation of adherence",
              "Updated cardiology plan of care for permanent ICD or recovery",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Approved in 30-day increments up to a total maximum of 90 days."
          ),
      },
      # 10. Non-pneumatic compression devices
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-010",
          "source_page": {"physical_page": 3, "printed_page": "Page 3 of 24"},
          "source_section": "Policy/Criteria - COMPRESSION THERAPY EQUIPMENT",
          "source_quote": (
              "Not medically necessary, as there is insufficient clinical"
              " evidence to support the safety and effectiveness of"
              " non-pneumatic compression devices over the use of standard"
              " pneumatic compression devices."
          ),
          "clinical_service_or_procedure": (
              "Non-pneumatic compression devices (HCPCS E0678, E0679, E0680,"
              " E0681)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-010-A",
                  "description": (
                      "Request is for non-pneumatic compression device"
                  ),
                  "parameter": "non_pneumatic_compression_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Investigational/unproven compared to standard pneumatic"
              " compression."
          ),
      },
      # 11. Blood glucose monitor with integrated voice synthesizer
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-011",
          "source_page": {"physical_page": 3, "printed_page": "Page 3 of 24"},
          "source_section": "Policy/Criteria - DIABETES CARE EQUIPMENT",
          "source_quote": (
              "Medically necessary for member/enrollees with diabetes who have"
              " a severe visual impairment (best corrected visual acuity of"
              " 20/200 or worse in both eyes)."
          ),
          "clinical_service_or_procedure": (
              "Blood glucose monitor with integrated voice synthesizer (HCPCS"
              " E2100)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-011-A",
                      "description": "Diagnosis of diabetes mellitus",
                      "parameter": "diabetes_mellitus_diagnosis",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-011-B",
                      "description": (
                          "Severe visual impairment with best corrected visual"
                          " acuity 20/200 or worse in both eyes"
                      ),
                      "parameter": "best_corrected_visual_acuity",
                      "comparator": "LESS_THAN_OR_EQUAL",
                      "value": "20/200",
                  },
              ],
          },
          "required_documentation": [
              "Endocrinology/PCP diabetes management notes",
              (
                  "Ophthalmology or optometry evaluation confirming visual"
                  " acuity ≤ 20/200 in both eyes"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Revision 08/26 updated language from legally blind to severe"
              " visual impairment (20/200 or worse in both eyes)."
          ),
      },
      # 12. Ultraviolet panel lights
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-012",
          "source_page": {"physical_page": 3, "printed_page": "Page 3 of 24"},
          "source_section": (
              "Policy/Criteria - HEAT, COLD & LIGHT THERAPY EQUIPMENT"
          ),
          "source_quote": (
              "Medically necessary when meeting both of the following: A."
              " Refractory psoriasis; B. Documentation supports treatment at"
              " home versus alternate sites (e.g. outpatient department at"
              " hospital)."
          ),
          "clinical_service_or_procedure": (
              "Ultraviolet panel lights (HCPCS E0691, E0692, E0693, E0694)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-012-A",
                      "description": "Diagnosis of refractory psoriasis",
                      "parameter": "refractory_psoriasis",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-012-B",
                      "description": (
                          "Clinical documentation supports home treatment"
                          " versus outpatient facility"
                      ),
                      "parameter": "home_treatment_justified",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Dermatology treatment history detailing failed prior therapies",
              (
                  "Documentation of home treatment necessity (travel/mobility"
                  " constraints)"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Cabinet-style reserved for extensive BSA; panel lights for"
              " discrete body areas."
          ),
      },
      # 13. Cold pad pump post-op exclusion
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-013",
          "source_page": {"physical_page": 4, "printed_page": "Page 4 of 24"},
          "source_section": (
              "Policy/Criteria - HEAT, COLD & LIGHT THERAPY EQUIPMENT"
          ),
          "source_quote": (
              "Not medically necessary for post-operative management, as"
              " research does not indicate improved outcomes in pain or edema"
              " management with the use of cold compression therapy over the"
              " use of other treatments to include conservative treatment, cold"
              " therapy alone, compression therapy alone, etc."
          ),
          "clinical_service_or_procedure": "Cold pad pump (HCPCS E0236)",
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-013-A",
                  "description": (
                      "Cold pad pump requested for post-operative management"
                  ),
                  "parameter": "post_operative_management_use",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": "Explicit non-coverage for post-operative management.",
      },
      # 14. Breast pumps
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-014",
          "source_page": {"physical_page": 4, "printed_page": "Page 4 of 24"},
          "source_section": "Policy/Criteria - NEWBORN CARE EQUIPMENT",
          "source_quote": (
              "Medically necessary when breast pumps are a covered benefit for"
              " the member/enrollee."
          ),
          "clinical_service_or_procedure": "Breast pumps (HCPCS E0604)",
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-014-A",
                  "description": "Breast pump is a covered plan benefit",
                  "parameter": "covered_plan_benefit",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "INDICATED",
          "missing_information_behavior": "CANNOT_DETERMINE",
          "dependencies": ["Member Benefit Schedule"],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Coverage is dependent upon individual plan benefit design."
          ),
      },
      # 15. Enclosed Beds Medical Necessity
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-015",
          "source_page": {"physical_page": 4, "printed_page": "Page 4 of 24"},
          "source_section": "Policy/Criteria - OTHER EQUIPMENT",
          "source_quote": (
              "Medically necessary when meeting all of the following: A."
              " Standard bed or standard hospital bed is unable to meet"
              " positioning needs due to disability; B. Less intensive"
              " alternatives to improve the member/enrollee’s safety have been"
              " tried and ruled out (to include documentation of why medical"
              " needs could not be met)."
          ),
          "clinical_service_or_procedure": (
              "Enclosed Beds (HCPCS E0316, E1399, E0328/E0329)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-015-A",
                      "description": (
                          "Standard bed/hospital bed unable to meet positioning"
                          " needs due to disability"
                      ),
                      "parameter": "standard_bed_inadequate",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-015-B",
                      "description": (
                          "Less intensive safety alternatives tried and ruled"
                          " out"
                      ),
                      "parameter": "less_intensive_safety_ruled_out",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-015-C",
                      "description": (
                          "Qualifying diagnosis (CP, developmental delay,"
                          " genetic/neuro disorder, seizure, severe behavior)"
                      ),
                      "parameter": "enclosed_bed_qualifying_diagnosis",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-107-015-D",
                      "description": (
                          "PT/OT home evaluation, functional status, and"
                          " caregiver education documented"
                      ),
                      "parameter": "therapist_home_eval_documented",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-015-E",
                      "description": (
                          "Itemized invoice and model specifications provided"
                      ),
                      "parameter": "bed_invoice_provided",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "PT/OT functional evaluation and home safety assessment",
              (
                  "Documentation ruling out rails, floor mattresses, alarms,"
                  " monitors, calming routines"
              ),
              "Caregiver training attestation",
              "Itemized bed invoice",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Requires mandatory secondary review by medical director and/or"
              " therapy advisor."
          ),
      },
      # 16. Enclosed Beds Mandatory Review
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-016",
          "source_page": {"physical_page": 5, "printed_page": "Page 5 of 24"},
          "source_section": "Policy/Criteria - OTHER EQUIPMENT",
          "source_quote": (
              "All requests for enclosed beds require mandatory secondary"
              " review by a medical director and/or therapy advisor."
          ),
          "clinical_service_or_procedure": (
              "Enclosed Beds - Secondary Review Requirement"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-016-A",
                  "description": (
                      "Medical director and/or therapy advisor secondary review"
                      " conducted"
                  ),
                  "parameter": "secondary_medical_review_completed",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "INDICATED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Mandatory peer-to-peer / medical director secondary review"
              " gateway."
          ),
      },
      # 17. Positioning seat
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-017",
          "source_page": {"physical_page": 5, "printed_page": "Page 5 of 24"},
          "source_section": "Policy/Criteria - OTHER EQUIPMENT",
          "source_quote": (
              "Medically necessary when all of the following are met: A."
              " Documentation of therapist evaluation and ongoing treatment"
              " plan; B. Commercial device must be unable to meet the"
              " positioning needs due to height, weight, or disability; C."
              " Other positioning devices in the home must be reviewed to"
              " ensure duplication of devices are not already in place."
          ),
          "clinical_service_or_procedure": (
              "Positioning seat (HCPCS T5001, E1399)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-017-A",
                      "description": (
                          "Therapist evaluation and ongoing treatment plan"
                          " documented"
                      ),
                      "parameter": "therapist_eval_and_plan",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-017-B",
                      "description": (
                          "Commercial device unable to meet positioning needs"
                          " due to height, weight, or disability"
                      ),
                      "parameter": "commercial_device_inadequate",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-017-C",
                      "description": (
                          "Home positioning devices reviewed to ensure no"
                          " duplication"
                      ),
                      "parameter": "no_device_duplication",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "PT/OT seating and positioning evaluation",
              "Inventory of existing seating/positioning devices in the home",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Requires mandatory secondary review by medical director or"
              " therapy advisor."
          ),
      },
      # 18. Specialized supply or miscellaneous equipment
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-018",
          "source_page": {"physical_page": 5, "printed_page": "Page 5 of 24"},
          "source_section": "Policy/Criteria - OTHER EQUIPMENT",
          "source_quote": (
              "Requests for not otherwise specified supplies or miscellaneous"
              " equipment codes require mandatory secondary review by a medical"
              " director and/or therapy advisor to determine medical necessity."
          ),
          "clinical_service_or_procedure": (
              "Specialized supply or miscellaneous equipment (HCPCS E0240,"
              " T2028, T2029, K0108, K0739, E1399)"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-018-A",
                  "description": (
                      "Secondary review completed by medical director or"
                      " therapy advisor"
                  ),
                  "parameter": "secondary_medical_review_completed",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "UNDETERMINED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "dependencies": ["CP.MP.99 Wheelchair Seating for seating requests"],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "All NOC/miscellaneous equipment codes require secondary medical"
              " director review."
          ),
      },
      # 19. ROMTech PortableConnect Device
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-019",
          "source_page": {"physical_page": 5, "printed_page": "Page 5 of 24"},
          "source_section": "Policy/Criteria - OTHER EQUIPMENT",
          "source_quote": (
              "Not medically necessary, as there is insufficient evidence in"
              " published peer-reviewed literature to support the use of this"
              " technology over currently available alternatives."
          ),
          "clinical_service_or_procedure": (
              "ROMTech® PortableConnect® Device (HCPCS E1399, A9900)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-019-A",
                  "description": (
                      "Request is for ROMTech PortableConnect Device"
                  ),
                  "parameter": "romtech_portableconnect_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Explicit non-coverage determination based on lack of evidence."
          ),
      },
      # 20. Cervical traction equipment
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-020",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Medically necessary when all of the following are met: A."
              " Musculoskeletal or neurologic impairment requiring traction"
              " equipment; B. One of the following: 1. Diagnosis of"
              " temporomandibular joint (TMJ) dysfunction and has received"
              " treatment for TMJ condition; 2. Distortion of the lower jaw and"
              " neck anatomy (e.g. radical neck dissection) such that a chin"
              " halter is unable to be utilized; 3. The treating physician"
              " orders and/or documents the medical necessity for greater than"
              " 20 pounds of cervical traction in the home setting."
          ),
          "clinical_service_or_procedure": (
              "Cervical traction equipment (HCPCS E0849)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-020-A",
                      "description": (
                          "Musculoskeletal or neurologic impairment requiring"
                          " traction"
                      ),
                      "parameter": "cervical_impairment_requiring_traction",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-020-B",
                      "description": (
                          "TMJ dysfunction treated, lower jaw/neck distortion"
                          " precluding chin halter, or >20 lbs home traction"
                          " ordered"
                      ),
                      "parameter": "cervical_traction_qualifying_feature",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Physician order documenting traction poundage",
              (
                  "Clinical records documenting TMJ treatment or anatomical"
                  " distortion"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "E0849 indicated when chin halter cannot be used or >20 lbs"
              " ordered."
          ),
      },
      # 21. Cervical collar, custom molded
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-021",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Requests for custom molded cervical collars require mandatory"
              " secondary review by a medical director and/or therapy advisor"
              " to determine medical necessity. Documentation accompanying the"
              " request must state the reason why a prefabricated collar is not"
              " adequate."
          ),
          "clinical_service_or_procedure": (
              "Cervical collar, custom molded (HCPCS L0170, L0190, L0200)"
          ),
          "rule_type": "clinical_prerequisite",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-021-A",
                      "description": (
                          "Documentation states why prefabricated collar is not"
                          " adequate"
                      ),
                      "parameter": "prefabricated_collar_inadequate_reason",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-107-021-B",
                      "description": (
                          "Mandatory secondary review completed by medical"
                          " director or therapy advisor"
                      ),
                      "parameter": "secondary_medical_review_completed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Physician/orthotist documentation stating why prefabricated"
                  " collar fails"
              ),
              "Anatomical measurements or structural deformity findings",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Mandatory secondary review requirement for custom molded"
              " cervical collars."
          ),
      },
      # 22. Spinal Orthotics
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-022",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Requests for spinal orthotics will be reviewed using relevant"
              " nationally recognized decision support tool criteria for"
              " similar codes."
          ),
          "clinical_service_or_procedure": (
              "Spinal Orthotics (HCPCS L0700, L0710, L0720, L0999, L1000,"
              " L1001, L1005, L1006)"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-022-A",
                  "description": (
                      "Evaluated against relevant nationally recognized"
                      " decision support tool criteria (InterQual)"
                  ),
                  "parameter": "decision_support_tool_criteria_met",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "UNDETERMINED",
          "missing_information_behavior": "CANNOT_DETERMINE",
          "dependencies": ["InterQual Spinal Orthotics Criteria"],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Defers to nationally recognized clinical decision support tools"
              " (InterQual)."
          ),
      },
      # 23. Hip orthotics - Surgical / Pediatric Indications
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-023",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Medically necessary when ordered by an orthopedic surgeon for"
              " treatment of, or postoperatively for any of the following: A."
              " Total hip arthroplasty; B. Hip labral tear; C. Hip disorders in"
              " children when used to stabilize the hip and/or to correct and"
              " maintain hip abduction."
          ),
          "clinical_service_or_procedure": (
              "Hip orthotics (HCPCS L1640, L1680, L1685, L1686, L1690)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-023-A",
                      "description": "Ordered by an orthopedic surgeon",
                      "parameter": "ordering_provider_specialty",
                      "comparator": "EQUALS",
                      "value": "ORTHOPEDIC_SURGEON",
                  },
                  {
                      "condition_id": "COND-DME-107-023-B",
                      "description": (
                          "Total hip arthroplasty, labral tear, or pediatric"
                          " hip disorder requiring abduction"
                      ),
                      "parameter": "hip_orthotic_indication",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Orthopedic surgeon operative report or clinic note",
              "Prescription specifying hip stabilization or abduction",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Lateral replacements due to growth are medically necessary in"
              " pediatrics."
          ),
      },
      # 24. Hip orthotics - Non-surgical Osteoarthritis Review
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-024",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Requests for hip orthotics for hip osteoarthritis in patients"
              " who are not surgical candidates will be reviewed on a"
              " case-by-case basis by a medical director and/or therapy"
              " advisor."
          ),
          "clinical_service_or_procedure": (
              "Hip orthotics for Non-Surgical Hip Osteoarthritis"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-024-A",
                      "description": (
                          "Patient has hip osteoarthritis and is not a surgical"
                          " candidate"
                      ),
                      "parameter": "hip_osteoarthritis_non_surgical",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-024-B",
                      "description": (
                          "Case-by-case review completed by medical director or"
                          " therapy advisor"
                      ),
                      "parameter": "medical_director_review_completed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "decision_effect": "UNDETERMINED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Individualized medical director evaluation required for"
              " non-surgical OA."
          ),
      },
      # 25. Legg Perthes orthotics
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-025",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Medically necessary when ordered by an orthopedic surgeon for"
              " use in the treatment for Legg-Calvé-Perthes disease in children."
          ),
          "clinical_service_or_procedure": (
              "Legg Perthes orthotics (HCPCS L1700, L1710, L1720, L1730, L1755)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-025-A",
                      "description": "Ordered by an orthopedic surgeon",
                      "parameter": "ordering_provider_specialty",
                      "comparator": "EQUALS",
                      "value": "ORTHOPEDIC_SURGEON",
                  },
                  {
                      "condition_id": "COND-DME-107-025-B",
                      "description": (
                          "Diagnosis of Legg-Calvé-Perthes disease in a child"
                      ),
                      "parameter": "legg_calve_perthes_disease",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Orthopedic surgeon order and clinical evaluation"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Established clinical indication for Legg-Calve-Perthes disease."
          ),
      },
      # 26. Hip-knee-ankle-foot orthotics (HKAFO)
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-026",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Requests for HKAFOs require mandatory secondary review by a"
              " medical director and/or therapy advisor to determine medical"
              " necessity."
          ),
          "clinical_service_or_procedure": (
              "Hip-knee-ankle-foot orthotics (HKAFO) (HCPCS L2050, L2060, L2090)"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-026-A",
                  "description": (
                      "Mandatory secondary review completed by medical"
                      " director or therapy advisor"
                  ),
                  "parameter": "secondary_medical_review_completed",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "UNDETERMINED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "All HKAFO requests require secondary clinical review."
          ),
      },
      # 27. Orthotic components
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-027",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Requests for orthotic components will be reviewed using relevant"
              " nationally recognized decision support tool criteria for"
              " similar codes."
          ),
          "clinical_service_or_procedure": (
              "Orthotic components (HCPCS L2570, L2580, L2627, L2628)"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-027-A",
                  "description": (
                      "Evaluated against relevant nationally recognized"
                      " decision support tool criteria (InterQual)"
                  ),
                  "parameter": "decision_support_tool_criteria_met",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "UNDETERMINED",
          "missing_information_behavior": "CANNOT_DETERMINE",
          "dependencies": ["InterQual Orthotic Components Criteria"],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Defers to nationally recognized clinical decision support tools"
              " (InterQual)."
          ),
      },
      # 28. Foot orthotics, custom
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-028",
          "source_page": {"physical_page": 7, "printed_page": "Page 7 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Medically necessary for arch, heel, or other foot pain when"
              " meeting both of the following: A. Foot condition, as indicated"
              " by one of the following: 1. Juvenile idiopathic arthritis; 2."
              " Pes cavus (high arch); 3. Rheumatoid arthritis; 4. Plantar"
              " fasciitis when symptoms have been present for at least one"
              " month; 5. Posterior tibial tendon dysfunction in adult, as"
              " indicated by one or more of the following: a. Stage I disease"
              " (tenosynovitis without deformity); b. Stage II disease"
              " (flexible and passively correctable deformity); B."
              " Documentation that adjustment of activities, anti-inflammatory"
              " medications, prefabricated orthotics, stretching of calf"
              " muscles and plantar surface have failed to improve symptoms."
          ),
          "clinical_service_or_procedure": (
              "Foot orthotics, custom (HCPCS L3000, L3001, L3002, L3003, L3010,"
              " L3020, L3030, L3031, L3070, L3080)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-028-A",
                      "description": (
                          "Qualifying foot condition (JIA, pes cavus, RA,"
                          " plantar fasciitis ≥1 month, or PTTD Stage I/II)"
                      ),
                      "parameter": "qualifying_foot_condition",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-107-028-B",
                      "description": (
                          "Failure of conservative care: activity adjustment,"
                          " NSAIDs, prefab orthotics, and stretching"
                      ),
                      "parameter": "conservative_care_failed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Clinical notes documenting foot condition and duration",
              (
                  "Documentation detailing failure of activity adjustment,"
                  " medications, prefab inserts, and stretching"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Plantar fasciitis requires ≥1 month duration. PTTD limited to"
              " Stage I or II."
          ),
      },
      # 29. Upper extremity orthotics (shoulder, elbow, wrist, hand, finger)
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-029",
          "source_page": {"physical_page": 7, "printed_page": "Page 7 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Medically necessary when ordered immediately post-operative for"
              " orthopedic surgeries such as rotator cuff repair, tendon"
              " repair, or ORIF. Replacement with the same or similar item due"
              " to normal wear and tear is considered medically necessary when"
              " the orthotic is still needed."
          ),
          "clinical_service_or_procedure": (
              "Shoulder, elbow, wrist, hand, finger orthotics (HCPCS L3904,"
              " L4000, L4010, L4020, L4030, L4205)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-029-A",
                      "description": (
                          "Ordered immediately post-operative for orthopedic"
                          " surgery (rotator cuff, tendon repair, ORIF)"
                      ),
                      "parameter": "post_operative_orthopedic_surgery",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-029-B",
                      "description": (
                          "Replacement due to normal wear and tear when"
                          " orthotic is still medically needed"
                      ),
                      "parameter": "replacement_wear_and_tear_needed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Operative report or surgical discharge plan",
              "Replacement order documenting ongoing medical need",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Covers immediate post-op period and normal wear/tear"
              " replacements."
          ),
      },
      # 30. Upper Extremity and Myoelectric Prosthetics Initial Request
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-030",
          "source_page": {"physical_page": 7, "printed_page": "Page 7 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Medically necessary when the request specific criteria in A. or"
              " B. are met: A. Initial request meets all of the following: 1."
              " Functional needs cannot be met with activity modification and"
              " compensatory techniques; 2. Requested prosthesis is anticipated"
              " to meet functional needs; 3. Clinical examination findings"
              " include all of the following:"
          ),
          "clinical_service_or_procedure": (
              "Upper Extremity and Myoelectric Prosthetics - Initial Request"
              " (HCPCS L6000-L7499)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-030-A",
                      "description": (
                          "Functional needs cannot be met with activity"
                          " modification or compensatory techniques"
                      ),
                      "parameter": "compensatory_techniques_inadequate",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-030-B",
                      "description": (
                          "Requested prosthesis anticipated to meet functional"
                          " needs"
                      ),
                      "parameter": "prosthesis_meets_functional_needs",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-030-C",
                      "description": (
                          "Clinical exam: appropriate residual limb length,"
                          " stable volume, skin integrity, strength/ROM,"
                          " cognitive function"
                      ),
                      "parameter": "residual_limb_clinical_exam_pass",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-030-D",
                      "description": (
                          "Comprehensive rehab plan: pre-prosthetic therapy,"
                          " control method discussed, task training, home"
                          " exercise"
                      ),
                      "parameter": "prosthetic_rehab_plan_complete",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Prosthetist detailed clinical evaluation and measurements",
              "Physiatry or orthopedic comprehensive limb exam",
              "Comprehensive prosthetic rehabilitation and training plan",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Requires mandatory secondary review by medical director or"
              " therapy advisor."
          ),
      },
      # 31. Upper Extremity and Myoelectric Prosthetics Replacement Request
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-031",
          "source_page": {"physical_page": 8, "printed_page": "Page 8 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Replacement request, all of the following: 1. Replacement is"
              " requested due to one of the following: a. Current prosthesis no"
              " longer functions properly or physiological or surgical changes"
              " to residual limb no longer accommodate current prosthesis; b."
              " Irreparable wear to prosthesis or prosthetic components; c."
              " Significant change in member/enrollee condition resulting in"
              " poor fit or function of prosthesis or prosthetic components; 2."
              " Irreparable damage to prosthesis or prosthetic components or"
              " repair cost > 60% of replacement cost;"
          ),
          "clinical_service_or_procedure": (
              "Upper Extremity and Myoelectric Prosthetics - Replacement"
              " Request (HCPCS L6000-L7499)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-031-A",
                      "description": (
                          "Loss of function, physiological/surgical limb change,"
                          " irreparable wear, or condition change"
                      ),
                      "parameter": "replacement_qualifying_reason",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-107-031-B",
                      "description": (
                          "Irreparable damage or repair cost exceeds 60% of"
                          " replacement cost"
                      ),
                      "parameter": "repair_cost_vs_replacement_threshold",
                      "comparator": "GREATER_THAN",
                      "value": "60%",
                  },
                  {
                      "condition_id": "COND-DME-107-031-C",
                      "description": (
                          "Prosthesis has been properly cared for following"
                          " manufacturer recommendations"
                      ),
                      "parameter": "proper_care_maintained",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-031-D",
                      "description": (
                          "Medical documentation supports continued use,"
                          " motivation, appropriate functional level, same/similar"
                          " components"
                      ),
                      "parameter": "continued_medical_need_supported",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Detailed repair estimate demonstrating repair cost >60% of"
                  " replacement"
              ),
              "Prosthetist clinical evaluation of limb changes and wear",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Mandatory 60% repair-cost threshold and secondary review by"
              " medical director."
          ),
      },
      # 32. Upper Extremity Prosthetics Secondary Review
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-032",
          "source_page": {"physical_page": 8, "printed_page": "Page 8 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "All requests for upper extremity and myoelectric prosthetics and"
              " additions require mandatory secondary review by a medical"
              " director and/or therapy advisor."
          ),
          "clinical_service_or_procedure": (
              "Upper Extremity and Myoelectric Prosthetics - Mandatory"
              " Secondary Review Requirement"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-032-A",
                  "description": (
                      "Secondary review completed by medical director or"
                      " therapy advisor"
                  ),
                  "parameter": "secondary_medical_review_completed",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "INDICATED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Mandatory clinical peer review for all upper extremity and"
              " myoelectric prosthetics."
          ),
      },
      # 33. Breast Prosthetics
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-033",
          "source_page": {"physical_page": 8, "printed_page": "Page 8 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Medically necessary post-mastectomy. If the request is for a"
              " custom prosthetic, accompanying documentation must state the"
              " reason why a prefabricated device is not adequate."
          ),
          "clinical_service_or_procedure": (
              "Breast Prosthetics (HCPCS L8030, L8035)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-033-A",
                      "description": "Post-mastectomy status",
                      "parameter": "post_mastectomy_status",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-033-B",
                      "description": (
                          "If custom prosthetic requested, documentation states"
                          " why prefabricated device is not adequate"
                      ),
                      "parameter": "custom_breast_prosthetic_justified",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Surgical notes documenting mastectomy",
              "If custom requested: clinical rationale why prefab is inadequate",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["Women's Health and Cancer Rights Act (WHCRA)"],
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "WHCRA-mandated post-mastectomy coverage. Custom requires"
              " pre-fab inadequacy justification."
          ),
      },
      # 34. External Lower Extremity Sensory Prosthetic Device (Walkasins)
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-034",
          "source_page": {"physical_page": 8, "printed_page": "Page 8 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Not medically necessary, as there is insufficient evidence in"
              " published peer-reviewed literature to support the effectiveness"
              " of this device."
          ),
          "clinical_service_or_procedure": (
              "External Lower Extremity Sensory Prosthetic Device (Walkasins®)"
              " (HCPCS L8720, L8721)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-034-A",
                  "description": "Request is for Walkasins device",
                  "parameter": "walkasins_device_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Added in Revision 08/26 as an explicit non-coverage exclusion."
          ),
      },
      # 35. Myoelectric Rehabilitation Systems
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-035",
          "source_page": {"physical_page": 8, "printed_page": "Page 8 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Not medically necessary, as there is insufficient evidence in"
              " published peer-reviewed literature to support the effectiveness"
              " of these devices."
          ),
          "clinical_service_or_procedure": (
              "Myoelectric Rehabilitation Systems (HCPCS E0738, E0739)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-035-A",
                  "description": (
                      "Request is for myoelectric rehabilitation system"
                      " (MyoPro)"
                  ),
                  "parameter": "myoelectric_rehab_system_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Updated in 07/25 to include HCPCS E0738 and E0739 as not"
              " medically necessary."
          ),
      },
      # 36. Facial Prosthetics
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-036",
          "source_page": {"physical_page": 8, "printed_page": "Page 8 of 24"},
          "source_section": "Policy/Criteria - PROSTHETICS AND ORTHOTICS",
          "source_quote": (
              "Requests for facial prosthetics are medically necessary when"
              " there is loss or absence of facial tissue due to disease,"
              " trauma, surgery, or a congenital defect."
          ),
          "clinical_service_or_procedure": (
              "Facial Prosthetics (HCPCS L8040, L8041, L8042, L8043, L8044,"
              " L8045, L8046, L8047, L8499)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-036-A",
                  "description": (
                      "Loss or absence of facial tissue due to disease, trauma,"
                      " surgery, or congenital defect"
                  ),
                  "parameter": "facial_tissue_loss_or_absence",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "required_documentation": [
              (
                  "Surgical or clinical notes detailing etiology of facial"
                  " tissue loss"
              ),
              "Anaplastology or prosthetics detailed fabrication plan",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Covers traumatic, surgical, oncology, or congenital facial tissue"
              " absence."
          ),
      },
      # 37. Ambulatory infusion pump
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-037",
          "source_page": {"physical_page": 9, "printed_page": "Page 9 of 24"},
          "source_section": "Policy/Criteria - PUMPS",
          "source_quote": (
              "Medically necessary when used for one of the following"
              " indications: A. Iron poisoning when used in the administration"
              " of deferoxamine for the treatment of acute iron poisoning and"
              " iron overload; B. Chemotherapy for liver cancer when used in"
              " the treatment of primary hepatocellular carcinoma or colorectal"
              " cancer where the disease is unresectable or where the patient"
              " refuses surgical excision of the tumor; C. With opioid drugs"
              " when used for intractable pain caused by cancer; D. To"
              " administer a drug considered reasonable and necessary by"
              " either: 1. Prolonged infusion of at least eight hours because"
              " of proven improved clinical efficacy (i.e., proven or generally"
              " accepted to have significant advantages over intermittent bolus"
              " administration regimens or infusions lasting less than eight"
              " hours); 2. Intermittent infusion, each episode of infusion"
              " lasting less than eight hours"
          ),
          "clinical_service_or_procedure": (
              "Ambulatory infusion pump (HCPCS E0780, E0781)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-037-A",
                  "description": (
                      "Deferoxamine for iron poisoning/overload, liver cancer"
                      " chemo, opioid for cancer pain, or qualifying prolonged/"
                      " intermittent infusion"
                  ),
                  "parameter": "ambulatory_pump_qualifying_indication",
                  "comparator": "IS_PRESENT",
              }],
          },
          "required_documentation": [
              "Prescription specifying drug, dosage, and infusion duration",
              (
                  "Oncology or clinical notes confirming cancer pain or"
                  " diagnosis"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "CMS NCD 280.14 aligned criteria for ambulatory infusion."
          ),
      },
      # 38. Gastric suction pump, home model
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-038",
          "source_page": {"physical_page": 9, "printed_page": "Page 9 of 24"},
          "source_section": "Policy/Criteria - PUMPS",
          "source_quote": (
              "Medically necessary for home use for gastric suction due to"
              " inability to empty gastric secretions through normal"
              " gastrointestinal functions."
          ),
          "clinical_service_or_procedure": (
              "Gastric suction pump, home model (HCPCS E2000)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-038-A",
                  "description": (
                      "Inability to empty gastric secretions through normal"
                      " gastrointestinal functions"
                  ),
                  "parameter": "gastric_emptying_failure",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "required_documentation": [
              "Gastroenterology or surgical notes documenting GI obstruction or"
              " dysmotility"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Home model suction pump indicated for severe dysmotility or"
              " obstruction."
          ),
      },
      # 39. Implantable infusion pumps
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-039",
          "source_page": {"physical_page": 9, "printed_page": "Page 9 of 24"},
          "source_section": "Policy/Criteria - PUMPS",
          "source_quote": (
              "Medically necessary when meeting both of the following: A. One"
              " of the following indications: 1. Chemotherapy for liver cancer:"
              " primary hepatocellular carcinoma or Duke’s Class D colorectal"
              " cancer, in which the metastases are limited to the liver and"
              " where either the disease is unresectable, or the patient"
              " refuses excision of the tumor; 2. Anti-spasmodic drugs for"
              " severe spasticity: administered intrathecally to treat chronic"
              " intractable spasticity in member/enrollee unresponsive to less"
              " invasive medical therapy including both of the following: a. A"
              " 6-week trial of noninvasive methods, such as oral"
              " anti- spasmodic drugs, that failed to adequately control the"
              " spasticity or produced intolerable side effects; b. Prior to"
              " pump implantation, there has been a favorable response to a"
              " trial of intrathecal dose of the anti-spasmodic drug; 3. Other"
              " uses when all of the following are met: a. The drug is"
              " reasonable and necessary for the treatment of the individual;"
              " b. It is medically necessary that the drug be administered by"
              " an implanted infusion pump. The infusion pump has been"
          ),
          "clinical_service_or_procedure": (
              "Implantable infusion pumps (HCPCS E0782, E0783, E0785, E0786)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-039-A",
                      "description": (
                          "Liver cancer chemo (Duke's Class D / unresectable),"
                          " severe spasticity with failed 6-wk oral trial and"
                          " successful intrathecal trial, or other FDA-approved"
                          " use"
                      ),
                      "parameter": "implantable_pump_indication_met",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-107-039-B",
                      "description": "None of the contraindications present",
                      "parameter": "contraindications_absent",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Oncology or physiatry notes confirming diagnosis",
              (
                  "Documentation of 6-week oral trial failure and successful"
                  " intrathecal trial (for spasticity)"
              ),
              "FDA approval status for drug and pump indication",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": [
              "CP.MP.173 for chronic intractable pain opioid pumps"
          ],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "For opioid pumps for intractable pain, refer to CP.MP.173."
          ),
      },
      # 40. Implantable infusion pumps contraindications
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-040",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - PUMPS",
          "source_quote": (
              "B. None of the following contraindications to implantation of an"
              " infusion pump: 1. Known allergy or hypersensitivity to the drug"
              " being used (e.g., oral baclofen, morphine, etc.); 2. Active"
              " infection; 3. Body size insufficient to support the weight and"
              " bulk of the device; 4. Presence of another implanted"
              " programmable device; 5. Heparin or insulin is the drug"
              " intended for administration."
          ),
          "clinical_service_or_procedure": (
              "Implantable infusion pumps - Contraindications"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-040-A",
                      "description": (
                          "Known allergy or hypersensitivity to drug being used"
                      ),
                      "parameter": "drug_hypersensitivity",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-040-B",
                      "description": "Active infection",
                      "parameter": "active_infection",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-040-C",
                      "description": (
                          "Body size insufficient to support weight and bulk of"
                          " device"
                      ),
                      "parameter": "insufficient_body_size",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-040-D",
                      "description": (
                          "Presence of another implanted programmable device"
                      ),
                      "parameter": "other_implanted_programmable_device",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-040-E",
                      "description": (
                          "Heparin or insulin is drug intended for"
                          " administration"
                      ),
                      "parameter": "heparin_or_insulin_administration",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Absolute contraindications including heparin/insulin pump"
              " administration."
          ),
      },
      # 41. Parenteral pump for medication administration
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-041",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - PUMPS",
          "source_quote": (
              "Medically necessary for uninterrupted parenteral administration"
              " of medication via pump."
          ),
          "clinical_service_or_procedure": (
              "Parenteral pump for medication administration (HCPCS K0455)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-041-A",
                  "description": (
                      "Requires uninterrupted parenteral administration of"
                      " medication"
                  ),
                  "parameter": "uninterrupted_parenteral_medication_required",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "required_documentation": [
              "Physician order detailing uninterrupted continuous IV infusion"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": "Established medical necessity for uninterrupted IV.",
      },
      # 42. Vacuum erection device
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-042",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - PUMPS",
          "source_quote": (
              "Medically necessary for the treatment of erectile dysfunction."
          ),
          "clinical_service_or_procedure": (
              "Vacuum erection device (HCPCS L7900, L7902)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-042-A",
                  "description": "Diagnosis of erectile dysfunction",
                  "parameter": "erectile_dysfunction_diagnosis",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "required_documentation": [
              "Urology or primary care clinical notes documenting ED"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["Benefit Plan Sexual Dysfunction Limitations"],
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": "Subject to plan-specific benefit limitations for ED.",
      },
      # 43. Nebulizer, ultrasonic
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-043",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - RESPIRATORY EQUIPMENT",
          "source_quote": (
              "Not medically necessary, as it provides no clinical advantage"
              " over use of a small-volume nebulizer (E0574) and compressor."
          ),
          "clinical_service_or_procedure": (
              "Nebulizer, ultrasonic (HCPCS E0575)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-043-A",
                  "description": "Request is for ultrasonic nebulizer",
                  "parameter": "ultrasonic_nebulizer_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Ultrasonic nebulizers provide no proven clinical advantage over"
              " E0574."
          ),
      },
      # 44. IPPB & supplies
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-044",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - RESPIRATORY EQUIPMENT",
          "source_quote": (
              "Medically necessary for member/enrollee with respiratory disease"
              " when an incentive spirometer is ineffective."
          ),
          "clinical_service_or_procedure": (
              "IPPB & supplies (HCPCS E0500, E0550)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-044-A",
                      "description": "Member has respiratory disease",
                      "parameter": "respiratory_disease_diagnosis",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-044-B",
                      "description": "Incentive spirometer is ineffective",
                      "parameter": "incentive_spirometer_ineffective",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Pulmonology or clinical records documenting respiratory disease",
              (
                  "Documentation showing incentive spirometry failed to"
                  " achieve adequate lung expansion"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Prerequisite: incentive spirometry ineffective or unable to be"
              " performed."
          ),
      },
      # 45. Oximeter Medically Necessary Indications
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-045",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - RESPIRATORY EQUIPMENT",
          "source_quote": (
              "Medically necessary when used as a monitoring and alarm device"
              " for any of the following: A. To monitor individuals on a home"
              " ventilator or with a tracheostomy B. To determine appropriate"
              " home oxygen requirements C. To wean an individual from home"
              " oxygen D. To monitor an unstable respiratory condition"
          ),
          "clinical_service_or_procedure": "Oximeter (HCPCS E0445)",
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-045-A",
                      "description": (
                          "Monitor individual on home ventilator or with"
                          " tracheostomy"
                      ),
                      "parameter": "ventilator_or_tracheostomy_monitoring",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-045-B",
                      "description": (
                          "Determine appropriate home oxygen requirements"
                      ),
                      "parameter": "oxygen_titration_determination",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-045-C",
                      "description": "Wean individual from home oxygen",
                      "parameter": "oxygen_weaning",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-045-D",
                      "description": "Monitor unstable respiratory condition",
                      "parameter": "unstable_respiratory_condition_monitoring",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Pulmonology clinical documentation of ventilator,"
                  " tracheostomy, oxygen weaning, or unstable condition"
              )
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Covered as a continuous monitoring/alarm device for qualifying"
              " indications."
          ),
      },
      # 46. Oximeter Exclusions
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-046",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - RESPIRATORY EQUIPMENT",
          "source_quote": (
              "Not medically necessary when used for any of the following: A."
              " Oximetry when used as a diagnostic procedure B. Monitoring of a"
              " stable respiratory condition C. Asthma management D. Other"
              " conditions not listed above"
          ),
          "clinical_service_or_procedure": "Oximeter (HCPCS E0445) - Exclusions",
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-046-A",
                      "description": "Diagnostic procedure use",
                      "parameter": "oximetry_diagnostic_procedure",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-046-B",
                      "description": "Monitoring of stable respiratory condition",
                      "parameter": "stable_respiratory_monitoring",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-046-C",
                      "description": "Asthma management",
                      "parameter": "asthma_management_use",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Explicitly non-covered for routine asthma, stable conditions, or"
              " diagnostic testing."
          ),
      },
      # 47. Intrapulmonary percussive ventilation devices (IPV)
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-047",
          "source_page": {"physical_page": 10, "printed_page": "Page 10 of 24"},
          "source_section": "Policy/Criteria - RESPIRATORY EQUIPMENT",
          "source_quote": (
              "Not medically necessary, as current evidence does not support"
              " the effectiveness of intrapulmonary percussive ventilation"
              " (IPV) devices."
          ),
          "clinical_service_or_procedure": (
              "Intrapulmonary percussive ventilation devices"
              " (Percussionaire-TRUE-IPV®) (HCPCS E1399)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-047-A",
                  "description": (
                      "Request is for intrapulmonary percussive ventilation"
                      " device"
                  ),
                  "parameter": "ipv_device_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Volara removed from this section in 08/26 and moved to OLE"
              " section."
          ),
      },
      # 48. Oscillation and Lung Expansion (OLE) Therapy Devices
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-048",
          "source_page": {"physical_page": 11, "printed_page": "Page 11 of 24"},
          "source_section": "Policy/Criteria - RESPIRATORY EQUIPMENT",
          "source_quote": (
              "Not medically necessary, as there is insufficient evidence to"
              " support the effectiveness of oscillation and lung expansion"
              " (OLE) therapy devices compared with conventional therapies."
          ),
          "clinical_service_or_procedure": (
              "Oscillation and Lung Expansion (OLE) Therapy Devices (Volara™,"
              " BiWaze Clear) (HCPCS E0469)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-048-A",
                  "description": (
                      "Request is for oscillation and lung expansion device"
                      " (Volara, BiWaze Clear)"
                  ),
                  "parameter": "ole_device_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Added in Revision 08/26 under new dedicated OLE section."
          ),
      },
      # 49. Walker, standard
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-049",
          "source_page": {"physical_page": 11, "printed_page": "Page 11 of 24"},
          "source_section": "Policy/Criteria - WALKERS",
          "source_quote": (
              "Requests for standard walkers are considered medically necessary"
              " when meeting all of the following: A. Mobility-related"
              " activities of daily living (MRADLs) in the home cannot be met"
              " due to mobility limitation; B. Walker can be safely used by"
              " member/enrollee; C. Functional mobility deficit will be"
              " sufficiently resolved with the use of a walker."
          ),
          "clinical_service_or_procedure": (
              "Walker, standard (HCPCS E0130, E0135, E0141, E0143)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-049-A",
                      "description": (
                          "MRADLs in home cannot be met due to mobility"
                          " limitation"
                      ),
                      "parameter": "mradls_impaired_by_mobility",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-049-B",
                      "description": (
                          "Walker can be safely used by member/enrollee"
                      ),
                      "parameter": "safe_walker_use_demonstrated",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-049-C",
                      "description": (
                          "Functional mobility deficit sufficiently resolved"
                          " with walker"
                      ),
                      "parameter": "deficit_resolved_by_walker",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Clinical mobility evaluation detailing in-home MRADL deficits",
              "Physical therapy or provider safe ambulation assessment",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["CMS LCD L33791 Walkers"],
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Standard walker criteria aligned with CMS LCD L33791."
          ),
      },
      # 50. Walker, heavy duty
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-050",
          "source_page": {"physical_page": 11, "printed_page": "Page 11 of 24"},
          "source_section": "Policy/Criteria - WALKERS",
          "source_quote": (
              "Requests for heavy duty walkers (E0148, E0149) are considered"
              " medically necessary when meeting the above standard walker"
              " criteria and the member/enrollee weighs more than 300 pounds."
              " Requests for heavy duty, multiple braking system, variable"
              " wheel resistance walkers (E0147) are considered medically"
              " necessary when meeting the above standard walker criteria and"
              " the member/enrollee is unable to use a standard walker due to a"
              " severe neurologic disorder or other condition causing the"
              " restricted use of one hand."
          ),
          "clinical_service_or_procedure": (
              "Walker, heavy duty (HCPCS E0147, E0148, E0149)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-050-A",
                      "description": "Standard walker criteria met",
                      "parameter": "standard_walker_criteria_met",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-050-B",
                      "description": (
                          "Weight > 300 lbs for E0148/E0149 OR severe"
                          " neurologic disorder/restricted single hand use for"
                          " E0147"
                      ),
                      "parameter": "heavy_duty_walker_qualifying_feature",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Member weight measurement > 300 lbs (for E0148/E0149)",
              (
                  "Neurologic assessment documenting single hand functional"
                  " restriction (for E0147)"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Weight > 300 lbs threshold for E0148/E0149; single-hand"
              " neurologic restriction for E0147."
          ),
      },
      # 51. Manual wheelchair initial request
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-051",
          "source_page": {"physical_page": 11, "printed_page": "Page 11 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "Initial requests for manual wheelchairs are medically necessary"
              " when meeting all of the following: A. Mobility limitation"
              " interferes with ability to participate in mobility-related"
              " activities of daily living, all of the following: 1. Mobility"
              " limitation cannot be met with a cane or walker; 2. Manual"
              " wheelchair will significantly improve member/enrollee’s ability"
              " to participate in mobility-related activities of daily living; 3."
              " Home provides adequate access and maneuvering space for"
              " requested manual wheelchair; 4. Willingness by member/enrollee"
              " or caregiver to use a manual wheelchair in the home; B. One of"
              " the following: 1. Caregiver is able to assist with wheelchair"
              " use; 2. Member/enrollee is able to safely and efficiently"
              " self-propel manual wheelchair."
          ),
          "clinical_service_or_procedure": (
              "Manual wheelchair - Initial Request (HCPCS E1050-E1295)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-051-A",
                      "description": (
                          "Mobility limitation cannot be met with cane or"
                          " walker"
                      ),
                      "parameter": "cane_or_walker_insufficient",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-051-B",
                      "description": (
                          "Manual wheelchair significantly improves in-home"
                          " MRADL participation"
                      ),
                      "parameter": "mradl_significantly_improved",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-051-C",
                      "description": (
                          "Home provides adequate access and maneuvering space"
                      ),
                      "parameter": "home_access_adequate",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-051-D",
                      "description": (
                          "Willingness to use manual wheelchair in the home"
                      ),
                      "parameter": "willingness_to_use_in_home",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-051-E",
                      "description": (
                          "Caregiver able to assist OR member safely/efficiently"
                          " self-propels"
                      ),
                      "parameter": "propulsion_or_caregiver_assistance_feasible",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "In-home MRADL mobility assessment",
              "Home environment evaluation confirming doorways and turns",
              "Self-propulsion or caregiver assistance demonstration",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["CMS LCD L33788 Manual Wheelchair Bases"],
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Covers 37 HCPCS codes for standard, lightweight, and custom"
              " manual wheelchair bases."
          ),
      },
      # 52. Manual wheelchair replacement request
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-052",
          "source_page": {"physical_page": 12, "printed_page": "Page 12 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "A. Replacement necessary due to loss, theft, or irreparable damage"
              " and both of the following: 1. Documentation supports continued"
              " medical necessity; 2. Replacement is with the same or similar"
              " equipment; B. All of the following: 1. Replacement is due to"
              " one of the following reasons: a. Replacement necessary after"
              " reasonable useful lifetime of five years or more; b. Change in"
              " member/enrollee status requiring different equipment than"
              " currently in use and growth features of current equipment have"
              " been maximized;"
          ),
          "clinical_service_or_procedure": (
              "Manual wheelchair - Replacement Request (HCPCS E1050-E1295)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-052-A",
                      "description": (
                          "Loss, theft, or irreparable damage with continued"
                          " necessity and same/similar replacement"
                      ),
                      "parameter": "loss_theft_or_irreparable_damage",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-052-B",
                      "description": (
                          "Useful lifetime ≥ 5 years OR condition change with"
                          " maximized growth features, plus all MRADL criteria"
                      ),
                      "parameter": "lifetime_or_condition_change_replacement",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Police report (theft), damage report, or proof of age ≥ 5"
                  " years"
              ),
              (
                  "Clinical records documenting growth feature maximization or"
                  " condition change"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["CMS 5-Year Reasonable Useful Lifetime (RUL) Rule"],
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "5-year reasonable useful lifetime rule explicitly applied to"
              " replacement wheelchairs."
          ),
      },
      # 53. Power seat elevator on power wheelchair
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-053",
          "source_page": {"physical_page": 12, "printed_page": "Page 12 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "Medically necessary as a component on a power wheelchair when"
              " all of the following are met: A. A licensed, certified medical"
              " professional (i.e. physical or occupational therapist) is"
              " involved with the assessment, prescription, trials and training"
              " of equipment; B. Adequate cognitive function to safely use the"
              " seat elevating feature; C. A clear functional need for the"
              " feature is indicated; D. Provision of the feature will improve"
              " functional independence with an activity, such as but not"
              " limited to facilitating reach for the completion of ADLs or"
              " IADLs or improving transfer biomechanics and safety."
          ),
          "clinical_service_or_procedure": (
              "Power seat elevator on power wheelchair (HCPCS E2298)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-053-A",
                      "description": (
                          "Licensed PT/OT involved in assessment, prescription,"
                          " trials, and training"
                      ),
                      "parameter": "licensed_therapist_involved",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-053-B",
                      "description": (
                          "Adequate cognitive function to safely use seat"
                          " elevation"
                      ),
                      "parameter": "cognitive_function_adequate_for_elevation",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-053-C",
                      "description": (
                          "Clear functional need indicated for the feature"
                      ),
                      "parameter": "functional_need_indicated",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-053-D",
                      "description": (
                          "Improves independence: facilitates reach for"
                          " ADLs/IADLs or improves transfer biomechanics/safety"
                      ),
                      "parameter": "reach_or_transfer_biomechanics_improved",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "PT/OT comprehensive seating evaluation including transfer"
                  " biomechanics"
              ),
              "Trial notes documenting safe cognitive operation of seat elevator",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": [
              "RESNA Position on the Application of Seat Elevation Devices"
              " (2019)"
          ],
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "RESNA Position Paper cited directly as supporting authority"
              " (Reference 42)."
          ),
      },
      # 54. Robotic Arm, Wheelchair-mounted (JACO)
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-054",
          "source_page": {"physical_page": 12, "printed_page": "Page 12 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "Not medically necessary, as there is insufficient clinical"
              " evidence to support safety and improved health outcomes of the"
              " JACO Assistive Robotic Arm (Kinova, Inc.) over other"
              " technologies."
          ),
          "clinical_service_or_procedure": (
              "Robotic Arm, Wheelchair-mounted (JACO) (HCPCS E1399)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-054-A",
                  "description": (
                      "Request is for JACO Assistive Robotic Arm on wheelchair"
                  ),
                  "parameter": "jaco_robotic_arm_requested",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Unproven robotic technology without established superiority over"
              " assistive alternatives."
          ),
      },
      # 55. Rollabout chair
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-055",
          "source_page": {"physical_page": 12, "printed_page": "Page 12 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "Medically necessary when used in lieu of a wheelchair for those"
              " who would qualify for a wheelchair (except for the ability to"
              " self- propel a manual wheelchair)."
          ),
          "clinical_service_or_procedure": "Rollabout chair (HCPCS E1031)",
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-055-A",
                      "description": (
                          "Member qualifies for a wheelchair except for the"
                          " ability to self- propel a manual wheelchair"
                      ),
                      "parameter": (
                          "wheelchair_eligible_except_self_propulsion"
                      ),
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-055-B",
                      "description": "Used in lieu of a standard wheelchair",
                      "parameter": "used_in_lieu_of_wheelchair",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Clinical mobility notes confirming inability to self-propel"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Specifically indicated for non-self-propelling individuals in"
              " lieu of wheelchair."
          ),
      },
      # 56. Wheelchair and other DME repairs
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-056",
          "source_page": {"physical_page": 12, "printed_page": "Page 12 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "Medically necessary when meeting all of the following: A. Less"
              " than 5 years old (as evident by the age/date of purchase"
              " information provided);"
          ),
          "clinical_service_or_procedure": (
              "Wheelchair and other DME repairs (HCPCS K0108, K0739, E1399)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-056-A",
                      "description": (
                          "Equipment is less than 5 years old based on purchase"
                          " date"
                      ),
                      "parameter": "equipment_age_years",
                      "comparator": "LESS_THAN",
                      "value": "5",
                  },
                  {
                      "condition_id": "COND-DME-107-056-B",
                      "description": (
                          "Cost of repairs is less than the cost of replacement"
                      ),
                      "parameter": "repair_cost_less_than_replacement",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-056-C",
                      "description": (
                          "Repairs required due to normal wear and tear, not"
                          " abuse/misuse or overutilization"
                      ),
                      "parameter": "normal_wear_and_tear_verified",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Original equipment purchase invoice / date of service",
              "Itemized repair cost estimate and parts invoice",
              "Equipment technician report on condition and wear-and-tear",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Repairs using K0108, K0739, or E1399 mandate secondary review."
          ),
      },
      # 57. Wheelchair rental during repair
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-057",
          "source_page": {"physical_page": 13, "printed_page": "Page 13 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "One month’s rental for a standard manual wheelchair is"
              " considered medically necessary if a member/enrollee owned"
              " wheelchair is 41 being repaired."
          ),
          "clinical_service_or_procedure": (
              "Standard manual wheelchair rental during repair"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-107-057-A",
                      "description": (
                          "Member-owned wheelchair is currently undergoing"
                          " authorized repair"
                      ),
                      "parameter": "wheelchair_undergoing_repair",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-107-057-B",
                      "description": (
                          "Rental is for standard manual wheelchair for up to"
                          " one month"
                      ),
                      "parameter": "rental_duration_months",
                      "comparator": "LESS_THAN_OR_EQUAL",
                      "value": "1",
                  },
              ],
          },
          "required_documentation": [
              "Proof of member-owned wheelchair repair in progress",
              "Rental agreement for loaner standard manual wheelchair",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "One month loaner wheelchair rental authorized while primary"
              " chair is repaired."
          ),
      },
      # 58. Wheelchair and DME repairs secondary review
      {
          **BASE_POLICY,
          "rule_id": "RULE-DME-107-058",
          "source_page": {"physical_page": 13, "printed_page": "Page 13 of 24"},
          "source_section": "Policy/Criteria - WHEELCHAIRS",
          "source_quote": (
              "Requests for wheelchair or other DME repairs specifically using"
              " codes K0108, K0739, or E1399 require mandatory secondary review"
              " by a medical director or therapy advisor."
          ),
          "clinical_service_or_procedure": (
              "Wheelchair and DME repairs (HCPCS K0108, K0739, E1399) -"
              " Secondary Review Requirement"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-107-058-A",
                  "description": (
                      "Mandatory secondary review completed by medical"
                      " director or therapy advisor"
                  ),
                  "parameter": "secondary_medical_review_completed",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "INDICATED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Mandatory clinical peer review for miscellaneous and"
              " non-specific repair codes."
          ),
      },
  ]
  return rules
