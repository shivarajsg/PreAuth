"""Centene Referenced Clinical Policies Rule Definitions.

Covers 41 atomic, source-grounded rules across:
- CP.MP.48: Neuromuscular and Peroneal Nerve Electrical Stimulation (3 rules)
- CP.MP.99: Wheelchair Seating (7 rules)
- CP.MP.173: Implantable Intrathecal or Epidural Pain Pump (6 rules)
- CP.MP.184: Home Ventilators (7 rules)
- CP.MP.185: Skin and Soft Tissue Substitutes (9 rules)
- CP.MP.203: Diaphragmatic/Phrenic Nerve Stimulation (3 rules)
- CP.MP.243: Implantable Loop Recorder (6 rules)
"""

URL_PREFIX = (
    "https://www.centene.com/content/dam/centene/policies/clinical-policies/"
)


def get_referenced_rules():
  rules = [
      # =========================================================================
      # CP.MP.48: Neuromuscular and Peroneal Nerve Electrical Stimulation (NMES)
      # =========================================================================
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.48: Neuromuscular and Peroneal Nerve"
              " Electrical Stimulation (NMES)"
          ),
          "policy_version": "Revision 04/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.48.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.48.pdf",
          "rule_id": "RULE-DME-048-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 7"},
          "source_section": "Policy/Criteria - Section I NMES for Disuse Atrophy",
          "source_quote": (
              "neuromuscular electrical stimulation (NMES) is medically"
              " necessary when used as one component of a comprehensive rehab"
              " program for the treatment of disuse atrophy when the nerve"
              " supply to the atrophied muscle is intact and has any of the"
              " following atrophy indications: A. Contractures due to scarring"
              " of soft tissue (e.g., burn lesions); B. Previous casting or"
              " splinting of a limb; C. Major knee surgery with failure to"
              " respond to physical therapy; D. Recent hip replacement and NMES"
              " will be used until physical therapy begins."
          ),
          "clinical_service_or_procedure": (
              "Neuromuscular Electrical Stimulation (NMES) for Disuse Atrophy"
              " (HCPCS E0745)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-048-001-A",
                      "description": (
                          "Part of a comprehensive rehabilitation program"
                      ),
                      "parameter": "comprehensive_rehab_program",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-048-001-B",
                      "description": (
                          "Nerve supply to the atrophied muscle is intact"
                      ),
                      "parameter": "nerve_supply_intact",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-048-001-C",
                      "description": (
                          "Atrophy indication: soft tissue contractures/burn,"
                          " previous cast/splint, major knee surgery failed PT,"
                          " or recent hip replacement"
                      ),
                      "parameter": "disuse_atrophy_qualifying_indication",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Physical therapy comprehensive rehabilitation plan",
              "Neurologic exam confirming intact peripheral nerve supply",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Indicated as one component of comprehensive rehab for qualifying"
              " disuse atrophy."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.48: Neuromuscular and Peroneal Nerve"
              " Electrical Stimulation (NMES)"
          ),
          "policy_version": "Revision 04/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.48.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.48.pdf",
          "rule_id": "RULE-DME-048-002",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 7"},
          "source_section": "Policy/Criteria - Section II FES for Spinal Cord Injury",
          "source_quote": (
              "functional electrical stimulation (FES) is medically necessary"
              " for spinal cord injury (SCI) when all of the following criteria"
              " are met: A. The member/enrollee has brisk muscle contraction to"
              " stimulation and sensory perception of electrical stimulation"
              " sufficient for muscle contraction; B. At least six months have"
              " passed since recovery from spinal cord injury and restorative"
              " surgery; C. Member/enrollee is highly motivated, committed, and"
              " has the cognitive ability to use FES devices for walking; D."
              " Successful completion of a training program consisting of at"
              " least 32 physical therapy sessions with the device over a"
              " three-month period; E. Member/enrollee demonstrates a"
              " willingness to use the device long-term;"
          ),
          "clinical_service_or_procedure": (
              "Functional Electrical Stimulation (FES) for Spinal Cord Injury"
              " (HCPCS E0764, E0770)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-048-002-A",
                      "description": (
                          "Brisk muscle contraction and sensory perception to"
                          " stimulation"
                      ),
                      "parameter": "brisk_muscle_contraction",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-048-002-B",
                      "description": (
                          "≥ 6 months post-recovery from SCI and restorative"
                          " surgery"
                      ),
                      "parameter": "post_sci_duration_months",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 6,
                      "unit": "months",
                  },
                  {
                      "condition_id": "COND-DME-048-002-C",
                      "description": (
                          "Completed training program of at least 32 PT"
                          " sessions over 3 months"
                      ),
                      "parameter": "pt_training_sessions_completed",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 32,
                      "unit": "sessions",
                  },
                  {
                      "condition_id": "COND-DME-048-002-D",
                      "description": (
                          "No contraindications: pacemaker, severe"
                          " scoliosis/osteoporosis, skin disease/cancer,"
                          " contracture, dysreflexia"
                      ),
                      "parameter": "fes_contraindications_present",
                      "comparator": "EQUALS",
                      "value": "FALSE",
                  },
              ],
          },
          "required_documentation": [
              "Neurologic exam documenting brisk contraction",
              "Physical therapy log verifying ≥32 training sessions",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Mandatory 32-session training prerequisite and 6-month post-SCI"
              " stability."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.48: Neuromuscular and Peroneal Nerve"
              " Electrical Stimulation (NMES)"
          ),
          "policy_version": "Revision 04/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.48.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.48.pdf",
          "rule_id": "RULE-DME-048-003",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 7"},
          "source_section": "Policy/Criteria - Section IV Peroneal Nerve Non-Covered",
          "source_quote": (
              "peroneal nerve stimulators (e.g., NESS L300, NESS L300 Plus, L300"
              " Go System, WalkAide, Odstock [ODFS®] Dropped Foot Stimulator)"
              " have not been proven safe and effective for any indication"
              " other than incomplete spinal cord injury, including, but not"
              " limited to: foot drop in cerebral palsy, multiple sclerosis,"
              " traumatic brain injury, or stroke."
          ),
          "clinical_service_or_procedure": (
              "Peroneal nerve stimulators (WalkAide, NESS L300) for"
              " Non-SCI Indications"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-048-003-A",
                      "description": "Foot drop due to cerebral palsy",
                      "parameter": "cerebral_palsy_foot_drop",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-048-003-B",
                      "description": "Foot drop due to multiple sclerosis",
                      "parameter": "multiple_sclerosis_foot_drop",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-048-003-C",
                      "description": (
                          "Foot drop due to traumatic brain injury or stroke"
                      ),
                      "parameter": "tbi_or_stroke_foot_drop",
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
              "Peroneal nerve stimulators are unproven for non-incomplete SCI"
              " indications."
          ),
      },
      # =========================================================================
      # CP.MP.99: Wheelchair Seating
      # =========================================================================
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.99: Wheelchair Seating",
          "policy_version": "Revision 01/24",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.99.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.99.pdf",
          "rule_id": "RULE-DME-099-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 49"},
          "source_section": "Policy/Criteria - Section I.A General Use Cushions",
          "source_quote": (
              "A general use seat cushion (E2601, E2602) and a general use"
              " wheelchair back cushion (E2611, E2612) for an approved manual"
              " wheelchair or power wheelchair with a sling or solid seat or"
              " back."
          ),
          "clinical_service_or_procedure": (
              "General use wheelchair seat and back cushions (HCPCS E2601,"
              " E2602, E2611, E2612)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-099-001-A",
                  "description": (
                      "Approved manual or power wheelchair with sling or solid"
                      " seat/back"
                  ),
                  "parameter": "approved_wheelchair_with_sling_solid_seat",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "General use cushions covered with an approved manual or power"
              " chair."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.99: Wheelchair Seating",
          "policy_version": "Revision 01/24",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.99.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.99.pdf",
          "rule_id": "RULE-DME-099-002",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 49"},
          "source_section": "Policy/Criteria - Section I.B Skin Protection Cushions",
          "source_quote": (
              "A skin-protection seat cushion (E2603, E2604, E2622, E2623) with"
              " an approved manual wheelchair or power wheelchair, with a"
              " sling/solid seat/back; and either of the following: 1. Current"
              " pressure ulcer or past history of a pressure ulcer"
          ),
          "clinical_service_or_procedure": (
              "Skin-protection wheelchair seat cushion (HCPCS E2603, E2604,"
              " E2622, E2623)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-099-002-A",
                      "description": (
                          "Approved manual or power wheelchair with sling/solid"
                          " seat/back"
                      ),
                      "parameter": "approved_wheelchair_present",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-099-002-B",
                      "description": (
                          "Current pressure ulcer or history of pressure ulcer"
                          " at seating contact area OR absent/impaired sensation"
                          " / inability to weight shift from qualifying neuro"
                          " disease"
                      ),
                      "parameter": "skin_protection_qualifying_condition",
                      "comparator": "IS_PRESENT",
                  },
              ],
          },
          "required_documentation": [
              "Wound care or clinical notes documenting pressure ulcer history",
              (
                  "Neurologic assessment documenting sensory loss or inability"
                  " to perform weight shift"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Indicated for pressure ulcer history or qualifying neurological"
              " sensory loss."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.99: Wheelchair Seating",
          "policy_version": "Revision 01/24",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.99.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.99.pdf",
          "rule_id": "RULE-DME-099-003",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 49"},
          "source_section": "Policy/Criteria - Section I.C Positioning Cushions",
          "source_quote": (
              "A positioning seat cushion (E2605, E2606), positioning back"
              " cushion (E2613, E2614, E2615, E2616, E2620, E2621), and"
              " positioning accessory (E0953, E0955, E0956, E0957, E0960) with"
              " both of the following: 1. An approved manual wheelchair or"
              " power wheelchair with a sling/solid seat/back; and 2."
              " Significant postural asymmetries"
          ),
          "clinical_service_or_procedure": (
              "Positioning seat and back cushions and accessories (HCPCS E2605,"
              " E2606, E2613-E2616, E2620, E2621, E0953, E0955, E0956, E0957,"
              " E0960)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-099-003-A",
                      "description": (
                          "Approved wheelchair with sling/solid seat/back"
                      ),
                      "parameter": "approved_wheelchair_present",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-099-003-B",
                      "description": (
                          "Significant postural asymmetries due to qualifying"
                          " neurological or musculoskeletal diagnosis"
                      ),
                      "parameter": "significant_postural_asymmetries",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "PT/OT seating evaluation detailing postural asymmetries"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Requires documentation of significant postural asymmetries from"
              " qualifying conditions."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.99: Wheelchair Seating",
          "policy_version": "Revision 01/24",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.99.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.99.pdf",
          "rule_id": "RULE-DME-099-004",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 49"},
          "source_section": "Policy/Criteria - Section I.D Wheelchair Headrest",
          "source_quote": (
              "A headrest (E0955) when the member/enrollee has an approved"
              " manual tilt-in-space, manual semi or fully reclining back on a"
              " manual wheelchair, a manual fully reclining back on a power"
              " wheelchair, or power tilt and/or recline power seating system."
          ),
          "clinical_service_or_procedure": (
              "Wheelchair headrest (HCPCS E0955)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-099-004-A",
                  "description": (
                      "Approved manual tilt-in-space, reclining back, or power"
                      " tilt/recline seating system"
                  ),
                  "parameter": "tilt_or_recline_seating_system_present",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Headrest indicated when wheelchair has tilt-in-space or recline"
              " feature."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.99: Wheelchair Seating",
          "policy_version": "Revision 01/24",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.99.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.99.pdf",
          "rule_id": "RULE-DME-099-005",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 49"},
          "source_section": "Policy/Criteria - Section I.E Combination Cushions",
          "source_quote": (
              "A combination skin-protection and positioning seat cushion"
              " (E2607, E2608, E2624, E2625) if the criteria for both a"
              " skin-protection seat cushion and a positioning seat cushion are"
              " met."
          ),
          "clinical_service_or_procedure": (
              "Combination skin-protection and positioning wheelchair seat"
              " cushion (HCPCS E2607, E2608, E2624, E2625)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-099-005-A",
                      "description": "Criteria for skin-protection cushion met",
                      "parameter": "skin_protection_criteria_met",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-099-005-B",
                      "description": "Criteria for positioning cushion met",
                      "parameter": "positioning_cushion_criteria_met",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Clinical records documenting both pressure ulcer/sensory"
                  " deficit AND postural asymmetry"
              )
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Dual qualification: must meet skin-protection and positioning"
              " criteria simultaneously."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.99: Wheelchair Seating",
          "policy_version": "Revision 01/24",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.99.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.99.pdf",
          "rule_id": "RULE-DME-099-006",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 49"},
          "source_section": "Policy/Criteria - Section I.F Custom Fabricated Cushions",
          "source_quote": (
              "A custom fabricated seat cushion (E2609) if criteria (1) and (3)"
              " below are met. A custom fabricated back cushion (E2617) if"
              " criteria (2) and (3) below are met: 1. The member/enrollee"
              " meets all of the criteria for a prefabricated skin-protection"
              " seat cushion or positioning seat cushion; 2. The"
              " member/enrollee meets all of the criteria for a prefabricated"
              " positioning back cushion; 3. There is a comprehensive, written"
              " evaluation by a licensed/certified medical professional, such"
              " as a physical therapist (PT) or occupational therapist (OT),"
              " which clearly explains why a prefabricated seating system is"
              " not sufficient to meet seating and positioning needs. The PT or"
              " OT must have no financial relationship with the supplier."
          ),
          "clinical_service_or_procedure": (
              "Custom fabricated wheelchair seat or back cushion (HCPCS E2609,"
              " E2617)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-099-006-A",
                      "description": (
                          "Prefabricated cushion criteria met (skin protection"
                          " or positioning)"
                      ),
                      "parameter": "prefab_cushion_criteria_met",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-099-006-B",
                      "description": (
                          "Comprehensive evaluation by independent PT/OT"
                          " explaining why prefab system is insufficient"
                      ),
                      "parameter": "independent_therapist_eval_prefab_insufficient",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Independent PT/OT written evaluation",
              (
                  "Supplier conflict-of-interest attestation confirming no"
                  " financial relationship"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Requires independent PT/OT evaluation explaining why prefab"
              " system fails."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.99: Wheelchair Seating",
          "policy_version": "Revision 01/24",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.99.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.99.pdf",
          "rule_id": "RULE-DME-099-007",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 49"},
          "source_section": "Policy/Criteria - Section II Seating Non-Covered",
          "source_quote": (
              "special wheelchair cushions and accessories are not medically"
              " necessary for the following indications: A. A general use seat"
              " cushion (E2601, E2602) if the member/enrollee has a"
              " power-operated vehicle (POV) or a power wheelchair with a"
              " captain's chair seat."
          ),
          "clinical_service_or_procedure": (
              "Wheelchair cushions and accessories on POV or Captain's Chair"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-099-007-A",
                      "description": (
                          "Cushion requested for POV or power wheelchair with"
                          " captain's chair seat"
                      ),
                      "parameter": "captain_chair_or_pov_seating",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-099-007-B",
                      "description": (
                          "Cushion provided for use with transport chair (E1037,"
                          " E1038)"
                      ),
                      "parameter": "transport_chair_seating",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-099-007-C",
                      "description": (
                          "Powered seat cushion (E2610) for any indication"
                      ),
                      "parameter": "powered_seat_cushion_requested",
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
              "Excluded on captain's chair, transport chair, or powered seat"
              " cushion (E2610)."
          ),
      },
      # =========================================================================
      # CP.MP.173: Implantable Intrathecal or Epidural Pain Pump
      # =========================================================================
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.173: Implantable Intrathecal or Epidural"
              " Pain Pump"
          ),
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.173.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.173.pdf",
          "rule_id": "RULE-DME-173-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 10"},
          "source_section": "Policy/Criteria - Section I.A.1 Malignant Pain Trial",
          "source_quote": (
              "Chronic intractable pain of malignant origin when all of the"
              " following criteria is met: a. Inadequate response to, or"
              " intolerable side effects from, noninvasive methods of pain"
              " control such as systemic opioids; b. Life expectancy > three"
              " months; c. No evidence of epidural metastatic lesion(s) or"
              " tumor encroachment of the thecal sac by imaging;"
          ),
          "clinical_service_or_procedure": (
              "Preliminary trial of epidural or intrathecal opioid - Malignant"
              " Pain"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-173-001-A",
                      "description": (
                          "Inadequate response or intolerable side effects from"
                          " systemic opioids"
                      ),
                      "parameter": "systemic_opioids_inadequate",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-173-001-B",
                      "description": "Life expectancy > 3 months",
                      "parameter": "life_expectancy_months",
                      "comparator": "GREATER_THAN",
                      "value": 3,
                      "unit": "months",
                  },
                  {
                      "condition_id": "COND-DME-173-001-C",
                      "description": (
                          "No evidence of epidural metastasis or thecal sac"
                          " encroachment on imaging"
                      ),
                      "parameter": "thecal_sac_encroachment_absent",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Oncology records documenting life expectancy > 3 months",
              "Spine MRI/CT ruling out epidural metastases or cord compression",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Preliminary trial prerequisite for cancer-related intractable"
              " pain."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.173: Implantable Intrathecal or Epidural"
              " Pain Pump"
          ),
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.173.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.173.pdf",
          "rule_id": "RULE-DME-173-002",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 10"},
          "source_section": "Policy/Criteria - Section I.A.2 Non-Malignant Pain Trial",
          "source_quote": (
              "Chronic intractable pain of nonmalignant origin (e.g. failed"
              " back surgery syndrome, complex regional pain syndrome) when all"
              " the following criteria are met: a. Pathology for the pain has"
              " been identified; b. Life expectancy is > three months; c."
              " Failure or inability to tolerate other conservative treatment"
              " methods"
          ),
          "clinical_service_or_procedure": (
              "Preliminary trial of epidural or intrathecal opioid -"
              " Non-Malignant Pain"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-173-002-A",
                      "description": (
                          "Identified pain pathology (e.g. FBSS, CRPS)"
                      ),
                      "parameter": "identifiable_pain_pathology",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-173-002-B",
                      "description": "Life expectancy > 3 months",
                      "parameter": "life_expectancy_months",
                      "comparator": "GREATER_THAN",
                      "value": 3,
                      "unit": "months",
                  },
                  {
                      "condition_id": "COND-DME-173-002-C",
                      "description": (
                          "Failure of conservative methods, psychological"
                          " clearance, weaned opioids by ≥50%"
                      ),
                      "parameter": "conservative_care_and_weaning_met",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Psychological evaluation ruling out major mental health cause",
              "Opioid weaning records confirming ≥50% reduction prior to trial",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Requires 50% systemic opioid weaning and psychological"
              " evaluation."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.173: Implantable Intrathecal or Epidural"
              " Pain Pump"
          ),
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.173.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.173.pdf",
          "rule_id": "RULE-DME-173-003",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 10"},
          "source_section": "Policy/Criteria - Section I.B Trial Contraindications",
          "source_quote": (
              "None of the following contraindications: 1. Known allergies to"
              " materials in the implant; 2. Active alcohol or drug abuse,"
              " including but not limited to opioid addiction and intravenous"
              " drug abuse;"
          ),
          "clinical_service_or_procedure": (
              "Pain pump preliminary trial - Contraindications"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-173-003-A",
                      "description": (
                          "Active alcohol or drug abuse / untreated addiction"
                      ),
                      "parameter": "active_substance_abuse",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-173-003-B",
                      "description": (
                          "Diagnosis of dementia, psychosis, or active infection"
                      ),
                      "parameter": "dementia_psychosis_or_infection",
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
              "Contraindicated in active addiction, psychosis, or infection."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.173: Implantable Intrathecal or Epidural"
              " Pain Pump"
          ),
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.173.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.173.pdf",
          "rule_id": "RULE-DME-173-004",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 10"},
          "source_section": "Policy/Criteria - Section II.A.1 Permanent Malignant",
          "source_quote": (
              "Chronic intractable pain of malignant origin when the above"
              " criteria for the preliminary trial are met, and all of the"
              " following: a. The trial provided ≥ 50% reduction in pain with"
              " minimal side effects;* b. Body size is sufficient to support"
              " the weight and bulk of the device;"
          ),
          "clinical_service_or_procedure": (
              "Permanent implantable intrathecal pain pump - Malignant Pain"
              " (HCPCS E0782, E0783)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-173-004-A",
                      "description": "Preliminary trial criteria met",
                      "parameter": "trial_criteria_met",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-173-004-B",
                      "description": (
                          "Trial provided ≥ 50% reduction in pain with minimal"
                          " side effects"
                      ),
                      "parameter": "pain_reduction_percentage",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": "50%",
                  },
                  {
                      "condition_id": "COND-DME-173-004-C",
                      "description": (
                          "Body size sufficient to support weight and bulk of"
                          " device"
                      ),
                      "parameter": "body_size_sufficient",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Trial log documenting ≥50% pain reduction",
              "Surgical notes regarding device pocket feasibility",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Trial requirement may be reviewed by medical director for"
              " advanced terminal disease."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.173: Implantable Intrathecal or Epidural"
              " Pain Pump"
          ),
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.173.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.173.pdf",
          "rule_id": "RULE-DME-173-005",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 10"},
          "source_section": "Policy/Criteria - Section II.A.2 Permanent Non-Malignant",
          "source_quote": (
              "Severe chronic pain of non-malignant origin when the above"
              " criteria for the preliminary trial is met and all of the"
              " following: a. Preliminary trial provided ≥ 50% reduction in"
              " pain and increase in function with minimal side effects; b."
              " There is a plan in place to continue to wean systemic opioids;"
          ),
          "clinical_service_or_procedure": (
              "Permanent implantable intrathecal pain pump - Non-Malignant"
              " Pain (HCPCS E0782, E0783)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-173-005-A",
                      "description": (
                          "Trial provided ≥ 50% reduction in pain AND increase"
                          " in function"
                      ),
                      "parameter": "pain_reduction_and_functional_gain",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": "50%",
                  },
                  {
                      "condition_id": "COND-DME-173-005-B",
                      "description": (
                          "Plan in place to continue to wean systemic opioids"
                      ),
                      "parameter": "ongoing_opioid_weaning_plan",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-173-005-C",
                      "description": (
                          "No active coagulopathy, normal ICP, no anatomical"
                          " spine barrier"
                      ),
                      "parameter": "surgical_safety_cleared",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Trial log confirming ≥50% pain relief and functional improvement",
              "Systemic opioid weaning taper schedule",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Requires documented functional gain and ongoing opioid weaning"
              " protocol."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.173: Implantable Intrathecal or Epidural"
              " Pain Pump"
          ),
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.173.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.173.pdf",
          "rule_id": "RULE-DME-173-006",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 10"},
          "source_section": (
              "Policy/Criteria - Section II.B Permanent Contraindications"
          ),
          "source_quote": (
              "B. None of the following contraindications: 1. Known allergies"
              " to materials in the implant; 2. Active alcohol or drug abuse,"
              " including but not limited to opioid addiction and intravenous"
              " drug abuse; 3. Diagnosis of dementia or psychosis; 4. Active"
              " systemic infection; 5. Active infection at the site of"
              " implantation."
          ),
          "clinical_service_or_procedure": (
              "Permanent pain pump implantation - Contraindications"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-173-006-A",
                      "description": (
                          "Active infection (systemic or at implant site)"
                      ),
                      "parameter": "active_infection_present",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-173-006-B",
                      "description": "Active substance abuse or addiction",
                      "parameter": "active_substance_abuse",
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
              "Absolute exclusion for infection, active abuse, dementia, or"
              " implant allergy."
          ),
      },
      # =========================================================================
      # CP.MP.184: Home Ventilators
      # =========================================================================
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.184: Home Ventilators",
          "policy_version": "Revision 03/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.184.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.184.pdf",
          "rule_id": "RULE-DME-184-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
          "source_section": "Policy/Criteria - Section I.A Restrictive Thoracic",
          "source_quote": (
              "Initial request for the first three months of noninvasive home"
              " ventilator use for restrictive thoracic disorders, all of the"
              " following:4,5,9 1. Documentation of a neuromuscular disease"
              " (ex. amyotrophic lateral sclerosis) or a severe thoracic cage"
              " abnormality (ex. post-thoracoplasty for tuberculosis or severe"
              " kyphoscoliosis)"
          ),
          "clinical_service_or_procedure": (
              "Noninvasive Home Ventilator - Restrictive Thoracic Disorders"
              " (HCPCS E0466)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-184-001-A",
                      "description": (
                          "Neuromuscular disease (ALS) or severe thoracic cage"
                          " abnormality"
                      ),
                      "parameter": "restrictive_thoracic_diagnosis",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-184-001-B",
                      "description": (
                          "Awake PaCO2 ≥ 45 mm Hg, sleep O2 sat ≤ 88% for ≥5"
                          " min, MIP < 60 cm H2O, or FVC < 50%"
                      ),
                      "parameter": "respiratory_insufficiency_threshold_met",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-184-001-C",
                      "description": (
                          "Cannot be treated with RAD; ventilator will provide"
                          " AVAPS not CPAP"
                      ),
                      "parameter": "rad_inadequate_and_avaps_provided",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "ABG report documenting PaCO2 ≥ 45 mm Hg or sleep oximetry",
              "Pulmonary function tests (MIP / FVC)",
              "Documentation explaining why RAD is inadequate",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Initial authorization strictly limited to first 3 months."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.184: Home Ventilators",
          "policy_version": "Revision 03/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.184.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.184.pdf",
          "rule_id": "RULE-DME-184-002",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
          "source_section": "Policy/Criteria - Section I.B Severe COPD",
          "source_quote": (
              "Initial request for the first three months of noninvasive home"
              " ventilator use for severe COPD, all of the following: 1. An"
              " arterial blood gas PaCO2 measurement was done while awake and"
              " breathing at baseline and prescribed FIO2 is ≥ 52 mm Hg;4"
          ),
          "clinical_service_or_procedure": (
              "Noninvasive Home Ventilator - Severe COPD (HCPCS E0466)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-184-002-A",
                      "description": "Severe COPD with baseline PaCO2 ≥ 52 mm Hg",
                      "parameter": "awake_paco2_level",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 52,
                      "unit": "mm Hg",
                  },
                  {
                      "condition_id": "COND-DME-184-002-B",
                      "description": (
                          "Sleep apnea considered and ruled out prior to therapy"
                      ),
                      "parameter": "sleep_apnea_ruled_out",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-184-002-C",
                      "description": (
                          "Cannot be treated with RAD; ventilator will provide"
                          " AVAPS"
                      ),
                      "parameter": "rad_inadequate_and_avaps_provided",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Baseline ABG documenting PaCO2 ≥ 52 mm Hg",
              "Documentation ruling out sleep apnea as predominant cause",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Severe COPD threshold PaCO2 ≥ 52 mm Hg awake on prescribed FIO2."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.184: Home Ventilators",
          "policy_version": "Revision 03/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.184.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.184.pdf",
          "rule_id": "RULE-DME-184-003",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 8"},
          "source_section": "Policy/Criteria - Section I.C Obesity Hypoventilation",
          "source_quote": (
              "Initial request for the first three months of noninvasive home"
              " ventilator use for obesity hypoventilation syndrome (OHS) (also"
              " known as Pickwickian syndrome), all of the following: 1. BMI ≥"
              " 30;13,14 2. An initial arterial blood gas PaCO2, done while"
              " awake and breathing at baseline and the prescribed FIO2 is ≥ 45"
              " mm Hg;13,14"
          ),
          "clinical_service_or_procedure": (
              "Noninvasive Home Ventilator - Obesity Hypoventilation Syndrome"
              " (OHS) (HCPCS E0466)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-184-003-A",
                      "description": "BMI ≥ 30",
                      "parameter": "body_mass_index",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 30,
                      "unit": "kg/m2",
                  },
                  {
                      "condition_id": "COND-DME-184-003-B",
                      "description": "Baseline awake PaCO2 ≥ 45 mm Hg",
                      "parameter": "awake_paco2_level",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 45,
                      "unit": "mm Hg",
                  },
                  {
                      "condition_id": "COND-DME-184-003-C",
                      "description": (
                          "PSG confirms sleep-disordered hypoventilation without"
                          " other primary cause"
                      ),
                      "parameter": "psg_confirmed_ohs",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "BMI calculation and height/weight",
              "Awake ABG showing PaCO2 ≥ 45 mm Hg",
              "Polysomnography report documenting hypoventilation",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "OHS requires BMI ≥ 30, awake PaCO2 ≥ 45 mm Hg, and PSG."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.184: Home Ventilators",
          "policy_version": "Revision 03/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.184.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.184.pdf",
          "rule_id": "RULE-DME-184-004",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 8"},
          "source_section": "Policy/Criteria - Section II Continuation Criteria",
          "source_quote": (
              "continued use of noninvasive home ventilators after the initial"
              " three-month certification period is medically necessary when"
              " meeting the following: A. The device is used for at least an"
              " average of four hours per 24-hour period;5 B. Documentation"
              " supports both of the following: 1. Ongoing benefits from use"
              " of the device;5,10 2. The noninvasive home ventilator is not"
              " being used provide RAD or CPAP therapy"
          ),
          "clinical_service_or_procedure": (
              "Noninvasive Home Ventilator - Continued Use (HCPCS E0466)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-184-004-A",
                      "description": (
                          "Device used for at least average of 4 hours per"
                          " 24-hour period"
                      ),
                      "parameter": "average_daily_usage_hours",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 4,
                      "unit": "hours",
                  },
                  {
                      "condition_id": "COND-DME-184-004-B",
                      "description": (
                          "Documented ongoing clinical benefit from use"
                      ),
                      "parameter": "ongoing_clinical_benefit",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-184-004-C",
                      "description": "Not being used to provide RAD/CPAP therapy",
                      "parameter": "not_rad_or_cpap_therapy",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Device compliance download confirming ≥4 hours/24hr usage",
              "Pulmonologist clinical follow-up documenting ongoing benefit",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Continuation requires adherence ≥ 4 hours/day and clinical"
              " benefit."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.184: Home Ventilators",
          "policy_version": "Revision 03/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.184.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.184.pdf",
          "rule_id": "RULE-DME-184-005",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 8"},
          "source_section": "Policy/Criteria - Section III Overlap Syndromes",
          "source_quote": (
              "noninvasive home ventilators for overlap syndromes (presence of"
              " more than one condition, such as COPD and sleep apnea) require"
              " secondary review by a medical director.4,10"
          ),
          "clinical_service_or_procedure": (
              "Noninvasive Home Ventilator - Overlap Syndromes (COPD + Sleep"
              " Apnea)"
          ),
          "rule_type": "administrative_prerequisite",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-184-005-A",
                      "description": (
                          "Presence of overlap syndrome (COPD + sleep apnea)"
                      ),
                      "parameter": "overlap_syndrome_present",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-184-005-B",
                      "description": (
                          "Secondary review completed by medical director"
                      ),
                      "parameter": "secondary_medical_review_completed",
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
              "Mandatory secondary review by medical director for overlap"
              " syndromes."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.184: Home Ventilators",
          "policy_version": "Revision 03/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.184.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.184.pdf",
          "rule_id": "RULE-DME-184-006",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 8"},
          "source_section": "Policy/Criteria - Section IV Invasive Ventilator",
          "source_quote": (
              "initial and ongoing use of an invasive ventilator is medically"
              " necessary for a long-term/chronic condition or disease"
              " affecting the ability to effectively maintain an adequate"
              " respiratory"
          ),
          "clinical_service_or_procedure": (
              "Invasive Home Mechanical Ventilator (HCPCS E0465)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-184-006-A",
                  "description": (
                      "Long-term/chronic respiratory condition requiring"
                      " invasive tracheostomy ventilation"
                  ),
                  "parameter": "chronic_invasive_ventilation_needed",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "required_documentation": [
              "Pulmonology records confirming tracheostomy and ventilator"
              " dependence"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Invasive ventilation via tracheostomy indicated for chronic"
              " respiratory failure."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.184: Home Ventilators",
          "policy_version": "Revision 03/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.184.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.184.pdf",
          "rule_id": "RULE-DME-184-007",
          "source_page": {"physical_page": 3, "printed_page": "Page 3 of 8"},
          "source_section": "Policy/Criteria - Section V Second / Back-up Ventilator",
          "source_quote": (
              "a second or back up noninvasive or invasive ventilator is"
              " considered medically necessary for the following indications:"
              " A. A second ventilator to serve a different purpose from the"
              " first ventilator, based on medical needs."
          ),
          "clinical_service_or_procedure": (
              "Second or Back-up Ventilator (HCPCS E0465, E0466)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-184-007-A",
                      "description": (
                          "Serves a different purpose based on medical needs"
                          " (e.g. negative pressure vs positive pressure)"
                      ),
                      "parameter": "different_ventilator_purpose",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-184-007-B",
                      "description": (
                          "Wheelchair-mounted during day and bed-mounted at"
                          " night"
                      ),
                      "parameter": "wheelchair_vs_bed_mounted_need",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-184-007-C",
                      "description": "Residence in remote area with poor emergency access",
                      "parameter": "remote_area_residence",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Physician clinical documentation justifying second ventilator"
                  " purpose, wheelchair mount, or remote area"
              )
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Back-up ventilator requires distinct functional justification or"
              " geographic isolation."
          ),
      },
      # =========================================================================
      # CP.MP.185: Skin and Soft Tissue Substitutes
      # =========================================================================
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 31"},
          "source_section": "Policy/Criteria - Section I Initial 4 Applications",
          "source_quote": (
              "up to four initial applications of skin and soft tissue"
              " substitutes/cellular and tissue-based products (CTPs) are"
              " medically necessary for diabetic foot ulcers (DFU) or venous"
              " leg ulcers (VLU) when all the following criteria are met,"
              " specific to the wound for which the skin substitute/CTP is"
              " being requested:"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes / CTPs - Initial 4 Applications"
              " for DFU or VLU"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-001-A",
                      "description": "Wound is > 1 square centimeter",
                      "parameter": "wound_surface_area_sq_cm",
                      "comparator": "GREATER_THAN",
                      "value": 1,
                      "unit": "cm2",
                  },
                  {
                      "condition_id": "COND-DME-185-001-B",
                      "description": (
                          "Failed ≥ 50% ulcer area reduction after ≥ 4 weeks of"
                          " standard of care (SOC) wound treatment"
                      ),
                      "parameter": "failed_soc_wound_care_duration_weeks",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 4,
                      "unit": "weeks",
                  },
                  {
                      "condition_id": "COND-DME-185-001-C",
                      "description": (
                          "Requested product is one of the preferred products"
                          " (Apligraf, Dermagraft, Epifix, Grafix, Integra,"
                          " Kerecis, Oasis, etc.)"
                      ),
                      "parameter": "preferred_product_selected",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-001-D",
                      "description": "Only one CTP in place per wound episode",
                      "parameter": "single_ctp_per_episode",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Photographic documentation with visible ruler at baseline"
                  " and follow-up"
              ),
              "Complete description of product, size, and NDC",
              "Wound treatment notes verifying 4 weeks failed SOC",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Initial authorization strictly limited to up to 4 applications."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-002",
          "source_page": {"physical_page": 3, "printed_page": "Page 3 of 31"},
          "source_section": "Policy/Criteria - Section II Continued Treatment",
          "source_quote": (
              "continued treatment beyond the initial four applications and up"
              " to a total of eight applications with skin and soft tissue"
              " substitutes/cellular and tissue-based products (CTPs) is"
              " medically necessary for diabetic foot ulcers (DFU) or venous"
              " leg ulcers (VLU) when all of the following criteria are met,"
              " specific to the wound for which the skin substitute/CTP is"
              " being requested:"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes / CTPs - Continued Treatment"
              " (Applications 5 to 8)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-002-A",
                      "description": (
                          "Initial 4 applications resulted in wound healing and"
                          " expectation of continued healing"
                      ),
                      "parameter": "initial_applications_demonstrated_healing",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-002-B",
                      "description": (
                          "Total cumulative applications will not exceed 8 per"
                          " wound per 12-week episode"
                      ),
                      "parameter": "cumulative_applications_limit",
                      "comparator": "LESS_THAN_OR_EQUAL",
                      "value": 8,
                      "unit": "applications",
                  },
                  {
                      "condition_id": "COND-DME-185-002-C",
                      "description": (
                          "Modifiable risk factors (diabetes, venous"
                          " insufficiency) adequately addressed"
                      ),
                      "parameter": "modifiable_risk_factors_managed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Sequential photos with visible ruler demonstrating wound"
                  " size reduction"
              ),
              (
                  "Treatment notes explaining medical necessity of extended"
                  " applications"
              ),
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Strict cap of 8 total applications per 12-week episode."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-003",
          "source_page": {"physical_page": 5, "printed_page": "Page 5 of 31"},
          "source_section": "Policy/Criteria - Section III DFU/VLU Non-Covered",
          "source_quote": (
              "skin and soft tissue substitutes/CTPs for diabetic foot ulcers (DFU)"
              " and venous leg ulcers (VLU) are not medically necessary for the"
              " following indications or scenarios: A. Any usage not listed in"
              " section I. or II. of the policy; B. Greater than eight"
              " applications of a skin and soft tissue substitute/CTP within an"
              " episode of care"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes / CTPs - DFU/VLU Exclusions"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-003-A",
                      "description": (
                          "Greater than 8 applications within 12-week episode"
                          " of care"
                      ),
                      "parameter": "applications_count",
                      "comparator": "GREATER_THAN",
                      "value": 8,
                      "unit": "applications",
                  },
                  {
                      "condition_id": "COND-DME-185-003-B",
                      "description": (
                          "Repeat application when previous application was"
                          " unsuccessful"
                      ),
                      "parameter": "previous_application_unsuccessful",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-003-C",
                      "description": (
                          "Active infection, necrosis, active Charcot"
                          " arthropathy, or ischemia"
                      ),
                      "parameter": "wound_infection_or_ischemia_present",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-003-D",
                      "description": "Liquid or gel CTP formulation for ulcer care",
                      "parameter": "liquid_or_gel_ctp_formulation",
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
              "Explicit frequency limit of 8 applications and clinical"
              " contraindications."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-004",
          "source_page": {"physical_page": 5, "printed_page": "Page 5 of 31"},
          "source_section": "Policy/Criteria - Section IV Burn Treatment",
          "source_quote": (
              "burn treatment with skin and soft tissue substitutes/CTPs"
              " (including the procedure, product, service) is considered"
              " medically necessary when meeting all the following, specific to"
              " the wound for which the skin substitute/CTP is being requested:"
              " A. Request indicates the specific wound to which the skin and"
              " soft tissue substitute/CTP will be applied; B. Request is for"
              " four weeks of treatment at a time; C. The wound is > 1 square"
              " centimeter; D. Sufficient autograft is not available"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes / CTPs - Burn Treatment"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-004-A",
                      "description": (
                          "Burn is deep partial-thickness or full-thickness"
                      ),
                      "parameter": "burn_thickness_depth",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-185-004-B",
                      "description": (
                          "Sufficient autograft is not available or feasible"
                      ),
                      "parameter": "autograft_unavailable_or_infeasible",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-004-C",
                      "description": "No evidence of burn wound infection",
                      "parameter": "burn_infection_absent",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-004-D",
                      "description": (
                          "Treatment with approved allograft, xenograft, or"
                          " tissue-engineered CTP (Biobrane, Epicel, etc.)"
                      ),
                      "parameter": "approved_burn_substitute",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Burn center clinical notes documenting depth and TBSA",
              "Documentation explaining autograft unavailability",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Approved for 4 weeks of treatment at a time for deep partial or"
              " full thickness burns."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-005",
          "source_page": {"physical_page": 6, "printed_page": "Page 6 of 31"},
          "source_section": "Policy/Criteria - Section V Breast Reconstruction",
          "source_quote": (
              "treatment with skin and soft tissue substitutes/CTPs for breast"
              " reconstruction are considered medically necessary when meeting"
              " all of the following, specific to the wound for which the skin"
              " substitute/CTP is being requested: A. Request indicates the"
              " specific wound to which the skin and soft tissue substitute/CTP"
              " will be applied; B. Request is for up to four weeks of"
              " treatment at a time; C. The wound is > 1 square centimeter; D."
              " Post-mastectomy breast reconstruction;"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes - Post-Mastectomy Breast"
              " Reconstruction"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-005-A",
                      "description": "Post-mastectomy breast reconstruction",
                      "parameter": "post_mastectomy_reconstruction",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-005-B",
                      "description": "No evidence of wound infection",
                      "parameter": "wound_infection_absent",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-005-C",
                      "description": (
                          "Approved product: AlloDerm, Cortiva, DermaCell, or"
                          " FlexHD/AllopatchHD"
                      ),
                      "parameter": "approved_breast_reconstruction_product",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Surgical operative report detailing reconstruction",
              "Product label and package size documentation",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "dependencies": ["WHCRA Post-Mastectomy Coverage"],
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Specifically covers acellular dermal matrices for"
              " post-mastectomy reconstruction."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-006",
          "source_page": {"physical_page": 7, "printed_page": "Page 7 of 31"},
          "source_section": "Policy/Criteria - Section VI Mitten Hand OrCel",
          "source_quote": (
              "OrCel™ is medically necessary for up to four weeks of treatment"
              " for mitten hand deformities due to dystrophic epidermolysis"
              " bullosa when meeting all the following, specific to the wound"
              " for which the skin substitute/CTP is being requested:"
          ),
          "clinical_service_or_procedure": (
              "OrCel™ for Mitten Hand Deformities in Dystrophic Epidermolysis"
              " Bullosa"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-006-A",
                      "description": (
                          "Mitten hand deformities due to dystrophic"
                          " epidermolysis bullosa"
                      ),
                      "parameter": "dystrophic_epidermolysis_bullosa",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-006-B",
                      "description": "Used according to FDA HDE specifications",
                      "parameter": "fda_hde_compliant",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-006-C",
                      "description": "No evidence of wound infection",
                      "parameter": "wound_infection_absent",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Genetic/dermatology confirmation of dystrophic EB",
              "Surgical notes for mitten hand release",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "FDA Humanitarian Device Exemption (HDE) protocol compliance"
              " required."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-007",
          "source_page": {"physical_page": 8, "printed_page": "Page 8 of 31"},
          "source_section": "Policy/Criteria - Section VII Abdominal Wall",
          "source_quote": (
              "skin and soft tissue substitutes/CTPs for post-reconstruction surgery"
              " of abdominal wall wounds are considered medically necessary"
              " when meeting all the following, specific to the wound for which"
              " the skin substitute/CTP is being requested: A. Request"
              " indicates the specific wound to which the skin and soft tissue"
              " substitute/CTP will be applied; B. Request is for up to four"
              " weeks of treatment at a time; C. The wound is > 1 square"
              " centimeter; D. Repair of hernias or for surgical repair of"
              " complex abdominal wall wounds;"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes - Complex Abdominal Wall"
              " Reconstruction"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-007-A",
                      "description": (
                          "Repair of hernias or complex abdominal wall wounds"
                      ),
                      "parameter": "complex_abdominal_wall_repair",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-007-B",
                      "description": (
                          "Approved product: Alloderm, Phasix ST, or Strattice"
                      ),
                      "parameter": "approved_abdominal_wall_product",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-007-C",
                      "description": "No evidence of wound infection",
                      "parameter": "wound_infection_absent",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Surgical operative report detailing complex hernia/wall defect",
              "Product label and size used with minimal wastage",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Indicated for complex abdominal wall hernia repair with Alloderm,"
              " Phasix ST, Strattice."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-008",
          "source_page": {"physical_page": 9, "printed_page": "Page 9 of 31"},
          "source_section": "Policy/Criteria - Section VIII General Limitations",
          "source_quote": (
              "skin and soft tissue substitutes/CTPs for any indication listed in"
              " sections IV to VII above are considered not medically necessary"
              " for any of the following: A. Treatment longer than twelve"
              " weeks; B. Repeat applications when initial treatment was"
              " unsuccessful for a period of four weeks past the start of"
              " therapy"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes - General Limitations and"
              " Duration Exclusions"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "ANY_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-185-008-A",
                      "description": "Treatment duration longer than 12 weeks",
                      "parameter": "treatment_duration_weeks",
                      "comparator": "GREATER_THAN",
                      "value": 12,
                      "unit": "weeks",
                  },
                  {
                      "condition_id": "COND-DME-185-008-B",
                      "description": (
                          "Repeat application after 4 weeks of unsuccessful"
                          " therapy"
                      ),
                      "parameter": "unsuccessful_at_4_weeks",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-185-008-C",
                      "description": (
                          "Retreatment of healed wounds (>75% reduction and"
                          " <0.5 sq cm)"
                      ),
                      "parameter": "healed_wound_retreatment",
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
              "Hard cap of 12 weeks maximum and prohibition against"
              " re-treating healed wounds."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.185: Skin and Soft Tissue Substitutes"
          ),
          "policy_version": "Revision 09/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.185.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.185.pdf",
          "rule_id": "RULE-DME-185-009",
          "source_page": {"physical_page": 9, "printed_page": "Page 9 of 31"},
          "source_section": "Policy/Criteria - Section IX Outpatient Exclusions",
          "source_quote": (
              "current evidence does not support the use of skin and soft"
              " tissue substitutes/cellular and tissue-based products (CTPs) in"
              " the outpatient setting for either of the following: A."
              " Indications other than those listed as medically necessary"
              " above, including but not limited to, pressure ulcers;"
          ),
          "clinical_service_or_procedure": (
              "Skin and Soft Tissue Substitutes - Outpatient Unproven"
              " Indications (e.g. Pressure Ulcers)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-185-009-A",
                  "description": (
                      "Requested in outpatient setting for pressure ulcers or"
                      " unlisted indication"
                  ),
                  "parameter": "pressure_ulcer_or_unlisted_ctp_indication",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Unproven in outpatient setting for pressure ulcers or other"
              " non-listed indications."
          ),
      },
      # =========================================================================
      # CP.MP.203: Diaphragmatic/Phrenic Nerve Stimulation
      # =========================================================================
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.203: Diaphragmatic/Phrenic Nerve"
              " Stimulation"
          ),
          "policy_version": "Revision 07/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.203.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.203.pdf",
          "rule_id": "RULE-DME-203-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 7"},
          "source_section": "Policy/Criteria - Section I Avery Mark IV / Spirit",
          "source_quote": (
              "diaphragmatic/phrenic nerve stimulation with the Mark IV™"
              " Breathing Pacemaker System or the Spirit Diaphragm Pacing"
              " Transmitter is medically necessary when all of the following"
              " are met: A. Stimulation is used as an alternative to mechanical"
              " ventilation for an individual with severe, chronic respiratory"
              " failure due to one of the following: 1. Upper cervical spinal"
              " cord injury (at or above the C3 vertebral level); 2. Central"
              " alveolar hypoventilation disorder;"
          ),
          "clinical_service_or_procedure": (
              "Diaphragmatic/Phrenic Nerve Stimulation - Avery Mark IV / Spirit"
              " System (CPT 64575, 64585, 64590)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-203-001-A",
                      "description": (
                          "Severe chronic respiratory failure due to upper"
                          " cervical SCI (≥C3) or central alveolar"
                          " hypoventilation"
                      ),
                      "parameter": "avery_qualifying_respiratory_failure",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-203-001-B",
                      "description": (
                          "Diaphragm movement visible under fluoroscopy"
                      ),
                      "parameter": "fluoroscopy_diaphragm_movement_confirmed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-203-001-C",
                      "description": (
                          "Intact phrenic nerve, lung, and diaphragm function"
                      ),
                      "parameter": "intact_phrenic_and_lung_function",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-203-001-D",
                      "description": (
                          "Normal chest anatomy and consciousness to"
                          " participate in rehabilitation"
                      ),
                      "parameter": "chest_anatomy_and_cognition_adequate",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Fluoroscopy report demonstrating diaphragm excursion",
              "Phrenic nerve conduction study confirming viability",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Indicated as alternative to mechanical ventilation for upper"
              " cervical SCI (≥C3)."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.203: Diaphragmatic/Phrenic Nerve"
              " Stimulation"
          ),
          "policy_version": "Revision 07/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.203.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.203.pdf",
          "rule_id": "RULE-DME-203-002",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 7"},
          "source_section": "Policy/Criteria - Section II NeuRx RA/4 System",
          "source_quote": (
              "diaphragmatic/phrenic nerve stimulation with the NeuRx RA/4"
              " Diaphragm Pacing System® is medically necessary when provided"
              " in accordance with the Humanitarian Device Exemption (HDE)"
              " specifications of the U.S Food and Drug Administration when"
              " all of the following are met: A. Stimulation is used as an"
              " alternative to mechanical ventilation for an individual with"
              " severe, chronic respiratory failure due to one of the"
              " following: 1. Amyotrophic lateral sclerosis (ALS);"
          ),
          "clinical_service_or_procedure": (
              "NeuRx RA/4 Diaphragm Pacing System® under HDE (CPT 64575, 64585)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-203-002-A",
                      "description": (
                          "Alternative to mechanical ventilation for ALS (age"
                          " ≥21, FVC ≥45%) OR upper cervical SCI (age ≥18)"
                      ),
                      "parameter": "neurx_qualifying_diagnosis",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-203-002-B",
                      "description": (
                          "Diaphragm movement visible under fluoroscopy or"
                          " ultrasound"
                      ),
                      "parameter": "imaging_diaphragm_movement_confirmed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-203-002-C",
                      "description": (
                          "Allows breathing without mechanical ventilator for"
                          " at least 4 continuous hours/day"
                      ),
                      "parameter": "ventilator_free_hours_achievable",
                      "comparator": "GREATER_THAN_OR_EQUAL",
                      "value": 4,
                      "unit": "hours",
                  },
              ],
          },
          "required_documentation": [
              "ALS diagnosis and spirometry (FVC ≥ 45% predicted)",
              "Fluoroscopy/ultrasound report",
              "FDA HDE protocol adherence documentation",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "FDA HDE protocol requirement: ALS requires age ≥21 and FVC ≥45%."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": (
              "Clinical Policy CP.MP.203: Diaphragmatic/Phrenic Nerve"
              " Stimulation"
          ),
          "policy_version": "Revision 07/26",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.203.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.203.pdf",
          "rule_id": "RULE-DME-203-003",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 7"},
          "source_section": "Policy/Criteria - Section III Central Sleep Apnea",
          "source_quote": (
              "there is insufficient evidence to support the safety and"
              " efficacy of diaphragmatic/phrenic nerve stimulation for any"
              " other conditions, including but not limited to, central sleep"
              " apnea."
          ),
          "clinical_service_or_procedure": (
              "Phrenic Nerve Stimulation for Central Sleep Apnea (Remedé"
              " System)"
          ),
          "rule_type": "exclusion_criterion",
          "conditions": {
              "operator": "SINGLE_CONDITION",
              "criteria": [{
                  "condition_id": "COND-DME-203-003-A",
                  "description": (
                      "Stimulation requested for central sleep apnea (Remedé"
                      " System) or unlisted condition"
                  ),
                  "parameter": "central_sleep_apnea_phrenic_stimulation",
                  "comparator": "EQUALS",
                  "value": "TRUE",
              }],
          },
          "decision_effect": "NOT_INDICATED",
          "missing_information_behavior": "FAIL_CONDITION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Remedé System for CSA is explicitly considered investigational/"
              " unproven."
          ),
      },
      # =========================================================================
      # CP.MP.243: Implantable Loop Recorder
      # =========================================================================
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.243: Implantable Loop Recorder",
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.243.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.243.pdf",
          "rule_id": "RULE-DME-243-001",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
          "source_section": "Policy/Criteria - Section I.A Cryptogenic Stroke",
          "source_quote": (
              "Suspected silent atrial fibrillation (AF) in the setting of"
              " cryptogenic stroke, when 30-day external ambulatory monitoring"
              " is inconclusive or contraindicated;"
          ),
          "clinical_service_or_procedure": (
              "Implantable Loop Recorder (ILR / ICM) - Cryptogenic Stroke (CPT"
              " 33285)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-243-001-A",
                      "description": (
                          "Suspected silent atrial fibrillation post-cryptogenic"
                          " stroke"
                      ),
                      "parameter": "cryptogenic_stroke_silent_af_suspected",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-001-B",
                      "description": (
                          "30-day external ambulatory monitoring inconclusive"
                          " or contraindicated"
                      ),
                      "parameter": "external_monitoring_inconclusive",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Neurology/cardiology notes documenting cryptogenic stroke workup",
              "30-day external event monitor report showing inconclusive rhythm",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Prerequisite: 30-day external monitoring must precede ILR."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.243: Implantable Loop Recorder",
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.243.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.243.pdf",
          "rule_id": "RULE-DME-243-002",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
          "source_section": "Policy/Criteria - Section I.B Ventricular Arrhythmia",
          "source_quote": (
              "Suspected or known ventricular arrhythmia when 30-day external"
              " ambulatory monitoring is inconclusive or contraindicated;"
          ),
          "clinical_service_or_procedure": (
              "Implantable Loop Recorder - Ventricular Arrhythmia (CPT 33285)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-243-002-A",
                      "description": (
                          "Suspected or known ventricular arrhythmia"
                      ),
                      "parameter": "ventricular_arrhythmia_suspected",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-002-B",
                      "description": (
                          "30-day external monitoring inconclusive or"
                          " contraindicated"
                      ),
                      "parameter": "external_monitoring_inconclusive",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Cardiology clinical notes and 30-day external telemetry log"
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Prerequisite: 30-day external monitoring inconclusive."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.243: Implantable Loop Recorder",
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.243.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.243.pdf",
          "rule_id": "RULE-DME-243-003",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
          "source_section": "Policy/Criteria - Section I.C Structural Heart Disease",
          "source_quote": (
              "History of structural or infiltrative heart disease (e.g.,"
              " valvular aortic stenosis, hypertrophic cardiomyopathy, cardiac"
              " sarcoidosis, congenital heart disease) and both of the"
              " following: 1. High risk for arrhythmias (e.g., family history,"
              " symptoms, anatomy of structural heart disease); 2. 30-day"
              " external ambulatory monitoring (e.g., external loop recorder)"
              " is inconclusive or contraindicated;"
          ),
          "clinical_service_or_procedure": (
              "Implantable Loop Recorder - Structural/Infiltrative Heart Disease"
              " (CPT 33285)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-243-003-A",
                      "description": (
                          "Structural or infiltrative heart disease (AS, HCM,"
                          " sarcoidosis, CHD)"
                      ),
                      "parameter": "structural_heart_disease_present",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-003-B",
                      "description": "High risk for arrhythmias",
                      "parameter": "high_arrhythmia_risk",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-003-C",
                      "description": "30-day external monitoring inconclusive",
                      "parameter": "external_monitoring_inconclusive",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Echocardiogram or cardiac MRI confirming structural disease",
              "30-day ambulatory telemetry report",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Covers structural heart disease with high arrhythmia risk."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.243: Implantable Loop Recorder",
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.243.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.243.pdf",
          "rule_id": "RULE-DME-243-004",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
          "source_section": "Policy/Criteria - Section I.D Unexplained Syncope",
          "source_quote": (
              "Recurrent, unexplained syncope or presyncope and both of the"
              " following: 1. Cardiac arrhythmia is suspected and external"
              " ambulatory monitoring (e.g., 30-day external loop recorder) is"
              " inconclusive or contraindicated; 2. Symptoms are infrequent"
              " (e.g., less than once per month)."
          ),
          "clinical_service_or_procedure": (
              "Implantable Loop Recorder - Infrequent Unexplained Syncope (CPT"
              " 33285)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-243-004-A",
                      "description": (
                          "Recurrent, unexplained syncope or presyncope"
                      ),
                      "parameter": "unexplained_syncope_recurrent",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-004-B",
                      "description": "30-day external monitoring inconclusive",
                      "parameter": "external_monitoring_inconclusive",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-004-C",
                      "description": "Symptoms infrequent (< 1 time per month)",
                      "parameter": "symptom_frequency_monthly",
                      "comparator": "LESS_THAN",
                      "value": 1,
                      "unit": "events_per_month",
                  },
              ],
          },
          "required_documentation": [
              "Syncope clinical history documenting frequency < 1/month",
              "Inconclusive 30-day external loop recorder report",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Requires infrequent symptoms (< 1 per month) and non-diagnostic"
              " 30-day monitor."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.243: Implantable Loop Recorder",
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.243.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.243.pdf",
          "rule_id": "RULE-DME-243-005",
          "source_page": {"physical_page": 1, "printed_page": "Page 1 of 8"},
          "source_section": "Policy/Criteria - Section II Secondary Review Indications",
          "source_quote": (
              "an implantable loop recorder/implantable cardiac monitor may be"
              " considered medically necessary following mandatory secondary"
              " medical director review when meeting all of the following: A."
              " Presenting condition meets one of the following: 1. Single,"
              " abrupt episode of unexplained syncope without prodrome (e.g.,"
              " sense of warmth, dizziness, pallor, diaphoresis, abdominal"
              " pain, changes in vision, or nausea) resulting in injury/trauma;"
              " 2. Significant, recurrent and unexplained palpitations;"
          ),
          "clinical_service_or_procedure": (
              "Implantable Loop Recorder - Abrupt Syncope with Trauma or"
              " Palpitations"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-243-005-A",
                      "description": (
                          "Single abrupt syncope with trauma OR significant"
                          " recurrent palpitations"
                      ),
                      "parameter": "abrupt_syncope_or_palpitations",
                      "comparator": "IS_PRESENT",
                  },
                  {
                      "condition_id": "COND-DME-243-005-B",
                      "description": "Serious cardiac arrhythmia is suspected",
                      "parameter": "serious_arrhythmia_suspected",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-005-C",
                      "description": (
                          "Mandatory secondary review completed by medical"
                          " director"
                      ),
                      "parameter": "secondary_medical_review_completed",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              "Trauma/ED notes detailing abrupt syncope without prodrome",
              "Cardiology clinical assessment",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "ESCALATE_TO_PEER_REVIEW",
          "human_review_required": True,
          "extraction_status": "NEEDS_HUMAN_REVIEW",
          "review_notes": (
              "Mandatory secondary review by medical director required."
          ),
      },
      {
          "domain": "centene_dme_orthotics_prosthetics",
          "document_type": "governing_policy",
          "policy_title": "Clinical Policy CP.MP.243: Implantable Loop Recorder",
          "policy_version": "Revision 11/25",
          "version_status": "current_2026_verified",
          "source_file": (
              "rulebook_collection/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.243.pdf"
          ),
          "source_url": f"{URL_PREFIX}CP.MP.243.pdf",
          "rule_id": "RULE-DME-243-006",
          "source_page": {"physical_page": 2, "printed_page": "Page 2 of 8"},
          "source_section": "Policy/Criteria - Section III Replacement",
          "source_quote": (
              "the replacement of an implantable loop recorder/implantable"
              " cardiac monitor may be considered medically necessary when"
              " meeting all of the above criteria and the existing monitor is"
              " no longer functioning and is outside its warranty (e.g., device"
              " is nearing the end of its battery life)."
          ),
          "clinical_service_or_procedure": (
              "Replacement of Implantable Loop Recorder (CPT 33285)"
          ),
          "rule_type": "clinical_indication",
          "conditions": {
              "operator": "ALL_OF",
              "criteria": [
                  {
                      "condition_id": "COND-DME-243-006-A",
                      "description": "Initial request criteria continue to be met",
                      "parameter": "initial_criteria_continuing",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
                  {
                      "condition_id": "COND-DME-243-006-B",
                      "description": (
                          "Existing device no longer functioning and outside"
                          " warranty (battery depletion)"
                      ),
                      "parameter": "device_depleted_and_outside_warranty",
                      "comparator": "EQUALS",
                      "value": "TRUE",
                  },
              ],
          },
          "required_documentation": [
              (
                  "Device interrogation report showing end-of-service / battery"
                  " depletion"
              ),
              "Proof device is outside manufacturer warranty",
          ],
          "decision_effect": "INDICATED",
          "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
          "human_review_required": False,
          "extraction_status": "DRAFT",
          "review_notes": (
              "Requires interrogation report showing battery depletion and"
              " expired warranty."
          ),
      },
  ]
  return rules
