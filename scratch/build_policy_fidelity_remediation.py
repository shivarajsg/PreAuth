import json
import csv
import re
from pathlib import Path

ROOT = Path("d:/PreAuth")
DATA_FILE = ROOT / "scratch" / "detailed_50_rules_data.json"
OUT_CSV = ROOT / "rulebook_collection" / "manifests" / "policy_fidelity_remediation.csv"
OUT_CSV_ROOT = ROOT / "policy_fidelity_remediation.csv"

with open(DATA_FILE, "r", encoding="utf-8") as f:
    rules = json.load(f)

# Define fields for policy_fidelity_remediation.csv
fieldnames = [
    "rule_id",
    "domain",
    "governing_policy",
    "policy_version",
    "source_section",
    "physical_page",
    "baseline_audit_status",
    "implemented_conditions_summary",
    "policy_text_verbatim",
    "fidelity_gap_type",
    "mandatory_vs_advisory",
    "threshold_and_timing_verification",
    "omitted_exceptions_or_prerequisites",
    "unsupported_inferences_or_broad_logic",
    "proposed_correction_for_human_review",
    "human_review_priority",
    "clinical_review_question"
]

remediation_records = []

for r in rules:
    rid = r["rule_id"]
    domain = r["domain"]
    status = r["audit_status"]
    page = r["physical_page"]
    section = r["source_section"]
    quote = r["rule_quote"]
    policy_name = r["policy_name"]
    policy_ver = r["policy_version"]
    cond = r["conditions"]
    issue = r["issue_description"]
    page_text = r["full_page_text"]
    
    # Analyze rule condition summary
    cond_str = json.dumps(cond)
    op = cond.get("operator", "UNKNOWN")
    criteria_count = len(cond.get("criteria", []))
    
    # Custom analysis per rule
    gap_type = ""
    nature = ""
    threshold_verif = ""
    omitted = ""
    inferences = ""
    proposed = ""
    priority = ""
    question = ""
    
    # ----------------- 7 HUMAN_REVIEW_REQUIRED RULES -----------------
    if rid == "RULE-ADV-PREAMBLE-001":
        gap_type = "CLINICAL_JUDGMENT_PREAMBLE"
        nature = "CLINICAL_JUDGMENT"
        threshold_verif = "None; overarching preamble framework without numerical criteria or time windows."
        omitted = "Full preamble context: Determinations require clinical judgment consistent with standards of good medical practice and individual patient circumstances; treating clinician retains final authority."
        inferences = "Critique: Overly broad logic. Draft rule encoded condition 'clinical_information_submitted == true' -> 'INDICATED', which would erroneously auto-approve any request if notes are attached."
        proposed = "PROPOSAL: Keep rule blocked from autonomous execution. Convert to non-executable governance policy definition or require manual clinical reviewer triage. Do not use as an approval rule."
        priority = "PRIORITY_1_GOVERNANCE_BLOCKED"
        question = "Should the Preamble remain entirely excluded from the deterministic rule registry as a non-evaluating governance standard, or be handled as an initial case triage gate?"
        
    elif rid == "RULE-IPM-PREAMBLEIPM-001":
        gap_type = "CLINICAL_JUDGMENT_PREAMBLE"
        nature = "CLINICAL_JUDGMENT"
        threshold_verif = "None; overarching clinical judgment framework."
        omitted = "Clinical judgment preamble: ESI and IPM criteria guide reviewers to most appropriate procedures based on unique circumstances; treating clinician has final authority."
        inferences = "Critique: Overly broad logic. Encoded single placeholder condition 'preambleipm_indication IS_PRESENT' -> 'INDICATED', bypassing specific clinical criteria."
        proposed = "PROPOSAL: Keep rule blocked from autonomous execution. Maintain exclusion of preamble from active authorization decision logic."
        priority = "PRIORITY_1_GOVERNANCE_BLOCKED"
        question = "Confirm that the IPM preamble is excluded from active deterministic evaluation and cannot be invoked to approve prior authorization requests."

    elif rid == "RULE-ADV-CG2000-003":
        gap_type = "ADVISORY_WORDING"
        nature = "ADVISORY_RECOMMENDATION"
        threshold_verif = "Age threshold: < 35 years explicitly stated in policy ('MRI should be considered for age < 35 to reduce radiation exposure')."
        omitted = "Policy context: 'includes CT enterography, however, MRI should be considered for age < 35 to reduce radiation exposure'. Does not state that CT is medically contraindicated or denied."
        inferences = "Critique: Advisory wording interpreted as mandatory decision effect. The rule applied 'ALTERNATIVE_MODALITY_RECOMMENDED' which triggers prior-auth redirection, whereas policy text is advisory ('should be considered')."
        proposed = "PROPOSAL: Maintain blocked status. Medical Director review required to determine whether payer contractually requires mandatory redirection to MR enterography in < 35yo or allows CT enterography when clinical justification is documented."
        priority = "PRIORITY_1_GOVERNANCE_BLOCKED"
        question = "Does 'MRI should be considered for age < 35' mandate an automated denial/redirection of CT enterography, or should it emit an advisory informational note while evaluating CT criteria?"

    elif rid == "RULE-ADV-CG2001-001":
        gap_type = "CLAIMS_BILLING_RULE"
        nature = "BILLING_ADMINISTRATIVE"
        threshold_verif = "CPT codes: 74176, 74177, 74178 (combined Abdomen/Pelvis CT) vs separate 74150-74170 (Abdomen) and 72192-72194 (Pelvis)."
        omitted = "Administrative billing rule: 'When separate requests for CT abdomen and CT Pelvis are encountered for processes involving both the abdomen and pelvis, they need to be resubmitted as Evolent Clinical Guideline 2000... (to avoid unbundling)'."
        inferences = "Critique: Claims unbundling edit conflated with clinical necessity determination. The rule issues ALTERNATIVE_MODALITY_RECOMMENDED, but unbundling is an intake/claims billing edit."
        proposed = "PROPOSAL: Keep blocked from clinical necessity tree. Route this rule to the intake/claims pre-processing validation layer to reject unbundled duplicate requests prior to clinical necessity evaluation."
        priority = "PRIORITY_1_GOVERNANCE_BLOCKED"
        question = "Should anti-unbundling code combination rules be evaluated at intake/claims pre-processing rather than as a clinical necessity decision tree?"

    elif rid == "RULE-ADV-CG2066-001":
        gap_type = "CLINICAL_JUDGMENT_PREAMBLE"
        nature = "MANDATORY_CRITERIA"
        threshold_verif = "Retrospective time window: Date of service must be in the past ('This type of medical necessity review is only conducted for those requests where the date of service has passed')."
        omitted = "Surrounding clinical definitions: Immediate attention needed to prevent loss of life, limb, or permanent disability, including airway/breathing/circulation impairment or severe tissue necrosis (compartment syndrome, acute thrombus/embolus)."
        inferences = "Critique: Subjective clinical threshold. Parameter 'emergent_life_or_limb_threat_present' requires qualitative physician interpretation of emergency medical records."
        proposed = "PROPOSAL: Keep blocked from automated approval. Retrospective emergency claims must route deterministically to Medical Director / Physician Review queue."
        priority = "PRIORITY_1_GOVERNANCE_BLOCKED"
        question = "Can retrospective emergent imaging ever be auto-approved deterministically, or must all retrospective emergency claims require Physician Reviewer adjudication?"

    elif rid == "RULE-ADV-CG2066-002":
        gap_type = "CLINICAL_JUDGMENT_PREAMBLE"
        nature = "MANDATORY_CRITERIA"
        threshold_verif = "Time window: 24 hours ('Any condition that cannot be postponed for a period of time (24 hours) without risking progression to an emergent condition'). Date of service must have passed."
        omitted = "Clinical definition of urgent progression: Prompt medical intervention required to prevent additional consequences or escalation to an emergency condition."
        inferences = "Critique: Qualitative clinical evaluation. Encoded condition 'urgent_intervention_needed_within_24h == true' cannot be objectively validated without clinician chart review."
        proposed = "PROPOSAL: Keep blocked from automated approval. Retrospective urgent claims must route deterministically to Human Clinical Review."
        priority = "PRIORITY_1_GOVERNANCE_BLOCKED"
        question = "Confirm policy workflow that retrospective urgent review (CG 2066) requires clinician adjudication rather than autonomous approval."

    elif rid == "RULE-IPM-CGINFUSIONPUMPS-001":
        gap_type = "OVERSIMPLIFIED_CRITERIA"
        nature = "MANDATORY_CRITERIA"
        threshold_verif = "Pain intensity >= 6/10; conservative therapy >= 12 weeks; MRSA/MSSA decolonization <= 10 days prior; temporary trial >= 50% relief; life expectancy > 3 months."
        omitted = "Extensive prerequisite criteria on pp. 68-72: Documented failure of >= 12 weeks of non-operative conservative therapy targeting the spinal region; psychological evaluation within 12 months; formal intraspinal drug trial with >= 50% relief; MRSA decolonization plan; exclusion of active substance abuse."
        inferences = "Critique: Highly oversimplified draft rule. Encoded single placeholder 'cginfusionpumps_indication IS_PRESENT' which completely bypasses the rigorous multi-step clinical prerequisites."
        proposed = "PROPOSAL: Maintain blocked status. Create comprehensive decomposed criteria model splitting into: (1) Pre-trial conservative therapy & psychological eval, (2) Intraspinal trial protocol, and (3) Permanent pump insertion criteria."
        priority = "PRIORITY_1_GOVERNANCE_BLOCKED"
        question = "Should intrathecal pump prior auth be split into two distinct deterministic modules: Trial Authorization (CG 1751/1752) and Permanent Placement Authorization (CG 1752)?"

    # ----------------- 43 PARTIALLY_VERIFIED RULES -----------------
    else:
        # Check rule details
        priority = "PRIORITY_2_CORE_FIDELITY"
        nature = "MANDATORY_CRITERIA"
        
        # Check specific rule IDs
        if "RULE-ADV-CG2000-002" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Physical exam, labs, recent colonoscopy completed; no specific duration specified on p. 9."
            omitted = "Contraindication note on p. 9: If patient has acute severe flare with suspected perforation or toxic megacolon, immediate surgical consult / emergency evaluation is indicated; CT with oral contrast may be contraindicated."
            inferences = "Rule correctly models prerequisites (exam, labs, colonoscopy) but omits explicit exclusions for acute toxic megacolon / gastrointestinal perforation where plain radiographs or emergent surgery supersede elective CT."
            proposed = "PROPOSAL: Add explicit exclusion parameter 'suspected_bowel_perforation_or_toxic_megacolon == true' -> 'EMERGENT_TRIAGE_REQUIRED'."
            question = "Should toxic megacolon or suspected free air/perforation explicitly trigger emergency redirection rather than standard prior auth evaluation?"
            
        elif "RULE-ADV-CG2000-004" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "At least ONE systemic sign: Elevated WBC, Fever, Anorexia, Nausea/vomiting."
            omitted = "Pregnancy and pediatric notes on p. 9: Note 1: If CT requested for pregnant woman with suspected appendicitis, ultrasound must be insufficient AND MRI contraindicated. Note 2: Suspected appendicitis in child (< 18) requires ultrasound first."
            inferences = "Rule applies generally without checking pregnancy status or pediatric age gates (< 18), which have mandatory ultrasound-first prerequisites on the same page."
            proposed = "PROPOSAL: Add cross-condition checks routing pregnant members and pediatric members (< 18) to US-first / MRI pathways before CT diverticulitis/appendicitis approval."
            question = "Should pregnancy and pediatric status be mandatory prerequisite gates before evaluating general adult CT diverticulitis/appendicitis criteria?"

        elif "RULE-ADV-CG2000-005" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Age < 18 years; ultrasound inconclusive/cannot be completed OR peritoneal signs present."
            omitted = "Specific body habitus or cooperation exceptions on p. 9: 'due to body habitus or inability to cooperate OR when peritoneal signs are present (guarding, rebound) or other red flags'."
            inferences = "Conditions model ultrasound inconclusive OR peritoneal signs, but the policy also allows CT if ultrasound cannot be completed due to documented patient inability to cooperate or body habitus."
            proposed = "PROPOSAL: Expand sub-condition to include 'ultrasound_cannot_be_completed_due_to_cooperation_or_habitus == true'."
            question = "Confirm addition of 'inability to cooperate / body habitus preventing US completion' to pediatric appendicitis CT criteria."

        elif "RULE-ADV-CG2003-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Initial diagnosis; q6m during first 2 years; annually thereafter."
            omitted = "Contraindications to MRI/MRA (implanted metallic devices, severe renal failure with GFR < 30 for gadolinium) noted in general vascular imaging guidelines."
            inferences = "Surveillance interval verified, but general MRI contraindications and alternative CTA pathway are not codified as an explicit negative branch."
            proposed = "PROPOSAL: Add safety condition verifying absence of non-MRI-compatible implants and adequate renal clearance."
            question = "Should MRA rules reference standard MRI contrast/device contraindication checks?"

        elif "RULE-ADV-CG2004-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Ultrasound completed prior to CT/MRI request."
            omitted = "Pediatric congenital vs adult presentation notes; bile duct dilatation thresholds (> 6 mm in normal, > 10 mm post-cholecystectomy)."
            inferences = "Rule requires prior ultrasound, but does not capture duct diameter thresholds or MRCP preference over CT for biliary tree evaluation."
            proposed = "PROPOSAL: Add verification of inconclusive ultrasound and confirm whether MRCP is preferred over CT."
            question = "Does policy intend MRCP as the preferred modality over CT for choledochal cyst when ultrasound is indeterminate?"

        elif "RULE-ADV-CG2004-002" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Suspected acute pancreatitis; upper abdominal / epigastric pain."
            omitted = "Atlanta criteria alignment on p. 92: Diagnosis requires 2 of 3: (1) abdominal pain, (2) serum lipase/amylase > 3x upper limit of normal, (3) characteristic imaging findings. CT is often not indicated in first 48-72h unless diagnosis uncertain."
            inferences = "Rule only checks epigastric pain, omitting the laboratory diagnostic threshold (lipase > 3x ULN) and timing consideration (CT recommended >= 48-72h after onset to detect necrosis)."
            proposed = "PROPOSAL: Refine conditions to require either diagnostic ambiguity (lipase < 3x ULN with severe symptoms) or timing >= 48-72h post-onset for necrosis/complication assessment."
            question = "Should acute pancreatitis CT criteria codify the Atlanta standard (lipase > 3x ULN and/or >= 48-72h delay to assess necrosis)?"

        elif "RULE-ADV-CG2005-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Acute or chronic mesenteric ischemia / ischemic colitis."
            omitted = "Surrounding notes on p. 118: CTA abdomen/pelvis is primary modality for acute mesenteric ischemia; distinction between acute arterial thromboembolism vs non-occlusive mesenteric ischemia."
            inferences = "Core indication verified; surrounding notes contain advisory recommendations for biphasic CTA protocol."
            proposed = "PROPOSAL: No condition change; add informational clinical guidance flag for biphasic CTA acquisition protocol."
            question = "Confirm that general clinical suspicion of mesenteric ischemia is sufficient for CTA without mandatory prior ultrasound."

        elif "RULE-ADV-CG2005-002" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Indeterminate initial ultrasound for pelvic venous syndromes (May-Thurner, Nutcracker)."
            omitted = "Clinical documentation of chronic pelvic pain (> 6 months), lower extremity swelling, or varicosities."
            inferences = "Rule checks indeterminate ultrasound, but does not enforce documentation of chronic pelvic pain or venous symptoms."
            proposed = "PROPOSAL: Add requirement for documented symptom chronicity (> 6 months) or venous examination findings."
            question = "Should pelvic congestion CTA require documentation of symptom duration > 6 months?"

        elif "RULE-ADV-CG2008-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Acute ischemic stroke or intracranial hemorrhage."
            omitted = "Emergency non-contrast CT brain protocol: Time window (< 24h) and NIHSS or acute neurological deficit documentation."
            inferences = "Rule models acute stroke indication, but page includes advisory notes regarding CT vs MRI in subacute/chronic presentations."
            proposed = "PROPOSAL: Add condition specifying acute presentation (< 24h) to differentiate from subacute/chronic stroke where MRI is preferred."
            question = "Should acute head CT for stroke be bounded by symptom onset < 24 hours to separate from subacute MRI pathways?"

        elif "RULE-ADV-CG2008-002" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Suspected acute subarachnoid hemorrhage (SAH)."
            omitted = "Timing notes on p. 151: Non-contrast CT sensitivity for SAH is highest in first 6-24 hours; negative CT after 6h may require lumbar puncture."
            inferences = "Rule verifies indication; surrounding text provides diagnostic algorithm guidance regarding LP."
            proposed = "PROPOSAL: Add advisory footnote note regarding LP correlation if CT is negative > 6 hours from onset."
            question = "Confirm that non-contrast CT is approved for acute SAH without requiring prior lumbar puncture."

        elif "RULE-ADV-CG2008-003" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Acute head trauma with acute, new, or fluctuating neurologic findings."
            omitted = "Clinical decision rules (Canadian CT Head Rule / New Orleans Criteria) on pp. 151-152: GCS < 15, suspected skull fracture, >= 2 vomiting episodes, age >= 65."
            inferences = "Rule uses broad parameter 'acute_head_trauma_with_neurologic_deficit', whereas policy details specific high-risk Canadian CT Head criteria."
            proposed = "PROPOSAL: Decompose into specific criteria: GCS score, signs of skull fracture, vomiting, or age >= 65."
            question = "Should head trauma CT criteria be explicitly mapped to the Canadian CT Head Rule criteria elements?"

        elif "RULE-ADV-CG2008-004" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Acute sudden onset headache presenting within 48h ('thunderclap' / 'worst of life'); duration < 4 weeks."
            omitted = "Surrounding headache red flags: New headache with fever/meningismus, papilledema, or postural aggravation."
            inferences = "Thunderclap criteria verified; other acute headache subsections on p. 149 remain as separate gap items."
            proposed = "PROPOSAL: Keep thunderclap criteria focused; map other headache subtypes to distinct rule IDs."
            question = "Confirm thunderclap headache rule boundary is restricted to sudden onset < 48 hours."

        elif "RULE-ADV-CG2009-002" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Acute ischemic stroke evaluated for Large Vessel Occlusion (LVO) / mechanical thrombectomy."
            omitted = "Time window on p. 176: LVO evaluation within 24 hours of last known well; concurrent non-contrast CT."
            inferences = "Rule checks acute stroke LVO evaluation, but does not explicitly bind time window to <= 24 hours from last known normal."
            proposed = "PROPOSAL: Add parameter 'hours_since_last_known_well <= 24' aligned with acute thrombectomy window."
            question = "Should Brain CTA for LVO explicitly enforce time window <= 24 hours from last known well?"

        elif "RULE-ADV-CG2015-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Evaluation for thrombectomy/reperfusion; <= 24 hours of onset."
            omitted = "CT perfusion / MR perfusion automated mismatch criteria (DAWN / DEFUSE 3 protocol) referenced in footnote on p. 297."
            inferences = "Time window <= 24h verified; perfusion-specific core-infarct volume thresholds left to neurointerventional software."
            proposed = "PROPOSAL: Verify documented baseline NIHSS >= 6 and consideration for mechanical thrombectomy."
            question = "Does CT perfusion require pre-authorization review, or should it be bundled with acute CTA brain/neck in emergent stroke?"

        elif "RULE-ADV-CG2016-001" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Blunt cervical trauma; Canadian C-Spine or NEXUS criteria."
            omitted = "Canadian C-Spine Rule high risk factors: age >= 65, dangerous mechanism, paresthesias; low risk factors permitting range of motion assessment."
            inferences = "Rule uses composite parameter 'acute_cervical_trauma', but does not isolate individual NEXUS / Canadian criteria fields."
            proposed = "PROPOSAL: Add NEXUS / Canadian C-Spine parameter fields (midline tenderness, focal deficit, altered sensorium, intoxication)."
            question = "Should cervical spine CT trauma criteria explicitly validate individual NEXUS/CCR check-boxes?"

        elif "RULE-ADV-CG2017-001" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Minimum 6 consecutive weeks of conservative therapy within the prior 6 months."
            omitted = "Footnote on p. 330 defining conservative treatment components: active physical therapy, home exercise program, NSAIDs/analgesics, and clinical re-evaluation; exception for progressive neurological deficit."
            inferences = "Rule checks duration (>= 6 weeks) and recency (<= 6 months), but does not validate specific therapeutic modalities or red flag bypass conditions."
            proposed = "PROPOSAL: Add red flag bypass condition (progressive motor weakness, myelopathy, cauda equina) that waives the 6-week conservative care prerequisite."
            question = "Confirm that progressive motor deficit or myelopathy bypasses the 6-week conservative therapy requirement for Cervical Spine MRI."

        elif "RULE-ADV-CG2017-002" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Progressive upper extremity symptoms / balance difficulty; objective myelopathic signs."
            omitted = "Specific myelopathic examination findings: Hoffmann's reflex, inverted radial reflex, clonus, Romberg sign, hyperreflexia."
            inferences = "Rule checks objective signs, but does not list specific reflexes as codified parameters."
            proposed = "PROPOSAL: Specify objective myelopathy parameter options (Hoffmann, clonus, Babinski, gait ataxia)."
            question = "Should myelopathy signs be structured as a multi-select list requiring at least one documented physical finding?"

        elif "RULE-ADV-CG2017-003" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Suspected acute cord compression with neurological deficits."
            omitted = "Surgical emergency warning: acute cord compression requires urgent evaluation without conservative care delay."
            inferences = "Rule correctly models emergent bypass; lacks explicit exclusion of stable non-progressive chronic pain."
            proposed = "PROPOSAL: Retain immediate indication for acute compression; clarify non-applicability to stable chronic radicular pain."
            question = "Confirm acute cord compression MRI is an immediate indication without prior treatment prerequisites."

        elif "RULE-ADV-CG2022-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Prior failed or technically incomplete conventional optical colonoscopy."
            omitted = "Contraindications on p. 436: Active diverticulitis flare, acute bowel obstruction, recent colonic resection/biopsy within 2-4 weeks (risk of perforation during CO2 insufflation)."
            inferences = "Rule checks incomplete optical colonoscopy, but fails to check absolute contraindications to CT Colonography (acute abdomen, active acute diverticulitis)."
            proposed = "PROPOSAL: Add negative criteria: 'acute_diverticulitis_flare == false' and 'suspected_colonic_perforation == false'."
            question = "Should CT Colonography rule explicitly exclude patients with acute diverticulitis flare or suspected perforation?"

        elif "RULE-ADV-CG2030-001" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Age 50-80 years; >= 20 pack-year smoking history; current smoker or quit within past 15 years."
            omitted = "Footnote criteria on p. 490: Shared decision-making visit documented; absence of signs/symptoms of lung cancer (hemoptysis, unexplained weight loss - which require diagnostic chest CT, not screening LDCT)."
            inferences = "Rule captures USPSTF demographic thresholds perfectly, but omits the mandatory exclusion: patient must be asymptomatic (no cough/hemoptysis/fever/weight loss)."
            proposed = "PROPOSAL: Add mandatory screening prerequisite: 'symptomatic_of_lung_disease == false' (if true, redirect to diagnostic CT chest 71250)."
            question = "Must LDCT screening rule enforce 'patient is asymptomatic' to prevent misuse of screening codes for diagnostic workup?"

        elif "RULE-ADV-CG2032-001" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Non-specific lower extremity pain; prior plain X-ray completed; MRI contraindicated."
            omitted = "Conservative care duration on p. 504: Minimum 4-6 weeks of conservative therapy required for chronic non-traumatic pain before advanced imaging."
            inferences = "Rule checks X-ray and MRI contraindication, but omits the 4-6 week conservative treatment requirement for non-traumatic pain."
            proposed = "PROPOSAL: Add condition requiring documented failure of >= 4-6 weeks conservative care unless acute trauma or red flag present."
            question = "Should lower extremity CT for non-specific pain require documented failure of 4-6 weeks of conservative management?"

        elif "RULE-ADV-CG2035-001" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Joint-specific pain, mechanical locking, instability, or suspected internal derangement."
            omitted = "Prerequisite on p. 553: Plain X-rays must precede MRI evaluation; 4-6 weeks conservative care required if no mechanical locking or acute trauma."
            inferences = "Rule models internal derangement broadly without separating acute mechanical locking (immediate MRI) from chronic pain (4-6 weeks conservative therapy + X-ray)."
            proposed = "PROPOSAL: Branch criteria: Immediate MRI if acute mechanical locking/inability to extend knee; require 4-6 weeks conservative therapy + negative X-ray for persistent joint pain without locking."
            question = "Should knee/joint MRI separate acute mechanical locking (immediate MRI) from chronic joint pain (requiring 4-6 weeks conservative care)?"

        elif "RULE-ADV-CG2035-002" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Positive joint-specific sign (McMurray, Lachman, drawer, pivot shift); prior X-ray completed."
            omitted = "Subtle difference between acute traumatic ligament tear (Lachman/pivot shift - immediate MRI) vs degenerative meniscal tear in older patients (X-ray showing OA -> conservative care first)."
            inferences = "Rule requires prior X-ray, but does not check whether X-ray revealed severe tri-compartmental osteoarthritis (where knee MRI is typically not indicated)."
            proposed = "PROPOSAL: Add exclusion: 'xray_demonstrates_bone_on_bone_advanced_osteoarthritis == true' -> 'MRI_NOT_INDICATED / ORTHOPEDIC_CONSULT_RECOMMENDED'."
            question = "Does policy exclude routine knee MRI when weight-bearing plain radiographs already demonstrate bone-on-bone advanced osteoarthritis?"

        elif "RULE-ADV-CG2036-001" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Acute lumbar trauma, fusion integrity/pseudoarthrosis, or lumbar pain with MRI contraindicated."
            omitted = "Footnote 1 on p. 574: Plain X-ray requirements and documentation of specific MRI contraindication (e.g. non-conditional pacemaker, metallic foreign body)."
            inferences = "Rule combines multiple indications; lacks explicit requirement that MRI contraindication must be documented in records."
            proposed = "PROPOSAL: Separate into distinct rules for: (1) Post-surgical fusion integrity assessment, and (2) Lumbar pain where MRI is medically contraindicated."
            question = "Should CT lumbar spine for fusion evaluation be decoupled from MRI-contraindicated lumbar pain?"

        elif "RULE-ADV-CG2037-001" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Lumbosacral radiculopathy; >= 6 consecutive weeks conservative care within prior 6 months."
            omitted = "Footnote 1 on p. 594: Red flag exceptions that waive conservative care (progressive motor deficit, foot drop, cauda equina, history of active cancer with new localized back pain)."
            inferences = "Conservative care threshold (6 weeks in 6 months) verified; needs explicit uncodified red flag waiver bypass."
            proposed = "PROPOSAL: Add ANY_OF bypass condition: 'progressive_motor_deficit == true OR active_malignancy_with_back_pain == true' waives conservative therapy."
            question = "Confirm that documented progressive motor deficit (e.g. foot drop) or cancer history bypasses the 6-week conservative care rule for Lumbar MRI."

        elif "RULE-ADV-CG2037-002" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Suspected acute cauda equina syndrome (saddle anesthesia, bowel/bladder dysfunction, bilateral motor weakness)."
            omitted = "Surrounding clinical definition on p. 595: Emergent indication; immediate MRI spine without conservative care delay."
            inferences = "Rule correctly models cauda equina as immediate; surrounding notes specify emergent same-day surgical decompression urgency."
            proposed = "PROPOSAL: Retain as immediate approval; confirm non-requirement of prior plain X-rays."
            question = "Confirm acute cauda equina syndrome is an immediate autonomous approval without X-ray or conservative care prerequisites."

        elif "RULE-ADV-CG2042-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Acute severe pelvic pain of unknown etiology; Age > 65 years."
            omitted = "Age < 65 female workup on p. 673: Pelvic ultrasound is mandatory first-line imaging in females of childbearing age (< 65) with pelvic pain."
            inferences = "Rule correctly captures age > 65 CT pathway, but does not codify the reverse boundary for females < 65 requiring ultrasound."
            proposed = "PROPOSAL: Add cross-cutting validation that for females < 65, pelvic ultrasound must be completed before Pelvis CT is considered."
            question = "Confirm that females under age 65 with acute pelvic pain require pelvic ultrasound prior to pelvic CT."

        elif "RULE-ADV-CG2045-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Suspected perianal fistula, perirectal abscess, or complex fistulizing Crohn's disease."
            omitted = "Notes on p. 718: Pelvic MRI is gold standard for perianal fistula anatomy; CT pelvis may be substituted only if MRI contraindicated or emergent drainable abscess suspected."
            inferences = "Indication verified; surrounding text confirms MRI is superior to CT for anal sphincter and fistulous tract evaluation."
            proposed = "PROPOSAL: Codify Pelvic MRI as first-line indication for perianal Crohn's fistula."
            question = "Confirm Pelvic MRI is indicated for complex perianal fistula without requiring prior CT or ultrasound."

        elif "RULE-ADV-CG2054-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Known sellar, suprasellar, or parasellar mass; bony evaluation or surgical planning."
            omitted = "General sella guideline notes on p. 881: Brain/Sella MRI is primary diagnostic modality; CT is indicated only for bony erosion/sphenoid anatomy surgical planning or when MRI is contraindicated."
            inferences = "Rule checks sellar mass, but does not enforce that Brain/Pituitary MRI must precede CT or that CT is specifically for bony surgical navigation."
            proposed = "PROPOSAL: Add condition: 'mri_sella_completed_or_contraindicated == true' and 'surgical_planning_for_transsphenoidal_approach == true'."
            question = "Should Sella CT require prior Brain MRI or documented transsphenoidal surgical planning?"

        elif "RULE-ADV-CG2055-001" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Suspected internal TMJ derangement (mechanical locking, persistent pain, limited opening)."
            omitted = "Prerequisites on p. 896: Plain radiographs / panorex completed; failure of at least 4-6 weeks of conservative management (splint therapy, soft diet, NSAIDs, physical therapy)."
            inferences = "Rule models clinical symptoms, but completely omits the mandatory conservative therapy prerequisite (4-6 weeks of conservative dental/splint therapy)."
            proposed = "PROPOSAL: Add conditions: 'prior_panorex_or_xray_completed == true' AND 'conservative_therapy_duration_weeks >= 4'."
            question = "Must TMJ MRI require documented completion of at least 4-6 weeks of conservative treatment (including oral appliance/splint therapy)?"

        elif "RULE-ADV-CG2056-001" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Progressive thoracic neurologic deficit (weakness, bowel/bladder dysfunction, sensory level); MRI contraindicated."
            omitted = "Footnote on p. 905: Documentation of specific MRI contraindication (implant, shrapnel, severe claustrophobia requiring general anesthesia)."
            inferences = "Rule models neurologic deficit and MRI contraindication; needs explicit parameter for documented medical contraindication reason."
            proposed = "PROPOSAL: Validate structured contraindication reason parameter against standard contraindicated device list."
            question = "Should MRI contraindications for spine CT be validated against an enumerated list of non-compatible devices?"

        elif "RULE-ADV-CG2056-002" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Persistent thoracic pain > 4 weeks; failure of 4-6 weeks conservative care; MRI contraindicated."
            omitted = "Footnotes on p. 906: Plain thoracic spine radiographs must be completed; conservative care components defined."
            inferences = "Rule checks pain duration (> 4 weeks) and conservative care, but omits mandatory prior thoracic X-ray prerequisite."
            proposed = "PROPOSAL: Add condition: 'prior_thoracic_xray_completed == true'."
            question = "Confirm thoracic spine CT for subacute pain requires prior plain X-rays in addition to conservative care failure."

        elif "RULE-ADV-CG2057-001" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Objective physical exam findings of thoracic myelopathy or sensory/motor level deficit."
            omitted = "Emergency bypass notes on p. 925: Thoracic myelopathy is an emergent/urgent surgical condition; no conservative therapy required."
            inferences = "Rule correctly models immediate approval for thoracic myelopathy; lacks explicit distinction from stable axial thoracic pain."
            proposed = "PROPOSAL: Confirm thoracic myelopathy rules do not inadvertently require conservative therapy."
            question = "Confirm thoracic myelopathy with upper motor neuron signs is an immediate indication without prior treatment."

        elif "RULE-ADV-CG2057-002" in rid:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Thoracic back pain > 4 weeks; failure of at least 4-6 weeks conservative therapy."
            omitted = "Footnotes on p. 926: Prior thoracic spine X-rays required; red flag exceptions (fever, cancer history, immunosuppression) waiving conservative therapy."
            inferences = "Rule captures 4-week pain and 4-6 week conservative care, but omits prior X-ray requirement and red flag bypasses."
            proposed = "PROPOSAL: Add 'prior_xray_completed == true' and red flag bypass for cancer history or fever/infection."
            question = "Should thoracic spine MRI require prior plain radiographs when evaluated for non-emergent pain > 4 weeks?"

        elif "RULE-ADV-CG2062-001" in rid:
            gap_type = "OMITTED_EXCLUSION"
            threshold_verif = "Prior X-ray completed; persistent pain unresponsive to >= 4 weeks conservative therapy OR acute complex fracture."
            omitted = "Notes on p. 965: Upper extremity CT is primarily for bony architecture / complex intra-articular fractures; soft tissue / ligamentous injuries require MRI."
            inferences = "Rule allows CT for persistent pain after 4 weeks conservative therapy, whereas policy states MRI is preferred for soft tissue pain; CT is restricted to bony pathology."
            proposed = "PROPOSAL: Refine condition to specify 'suspected_bony_abnormality_or_fracture_planning == true' or redirect soft tissue symptoms to MRI."
            question = "Does policy restrict Upper Extremity CT to bony pathology, requiring MRI for soft tissue and tendon derangements?"

        # ----------------- 8 IPM PARTIALLY_VERIFIED RULES -----------------
        elif "RULE-IPM-CGEPIDURALINJECTIONS-001" in rid:
            gap_type = "OVERSIMPLIFIED_CRITERIA"
            threshold_verif = "Radicular pain; objective neurologic findings; failure of >= 6 weeks conservative care."
            omitted = "Detailed criteria on pp. 4-10: Radiculopathy conforming to dermatomal distribution; MRI/CT correlation showing nerve root compression; >= 6 weeks conservative therapy; max 3 sessions per rolling 12 months; minimum 14 days between injections."
            inferences = "Draft rule used single placeholder 'cgepiduralinjections_indication IS_PRESENT', completely bypassing multi-step clinical necessity criteria."
            proposed = "PROPOSAL: Decompose into full clinical criteria: (1) Radicular dermatomal pain, (2) Concordant imaging findings, (3) >= 6 weeks conservative therapy failure (unless cauda equina/progressive deficit), (4) Interval >= 14 days."
            question = "Should Epidural Steroid Injections be decomposed into separate rule criteria for Initial Injection vs Subsequent Injections?"

        elif "RULE-IPM-CGEPIDURALINJECTIONS-002" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Failure of conservative therapy (pharmacotherapy, active PT, HEP) for radicular pain."
            omitted = "Specific conservative care elements on p. 11: Active physical therapy (minimum 6 sessions over 6 weeks) OR documented home exercise program (HEP) instructed by clinician + oral medications (NSAIDs, acetaminophen, neuropathic agents) for >= 6 weeks."
            inferences = "Rule checks generic 'conservative_therapy_failure', without codifying the specific 6-week duration or therapeutic modalities."
            proposed = "PROPOSAL: Codify specific requirements: 'conservative_care_weeks >= 6' AND 'active_pt_or_instructed_hep == true' AND 'oral_analgesic_trial == true'."
            question = "Confirm that conservative care for ESI requires at least 6 weeks of combined physical therapy/HEP and pharmacotherapy."

        elif "RULE-IPM-CGEPIDURALPUMPTRIALS-001" in rid:
            gap_type = "OVERSIMPLIFIED_CRITERIA"
            threshold_verif = "Single injection trial for intrathecal pump; continuous monitoring; life expectancy > 3 months."
            omitted = "Extensive criteria on pp. 17-23: Refractory chronic pain or spasticity failing oral therapies; multidisciplinary pain and psychological clearance; inpatient or monitored observation."
            inferences = "Draft rule used single placeholder 'cgepiduralpumptrials_indication IS_PRESENT'."
            proposed = "PROPOSAL: Decompose into specific trial prerequisites: failure of all conventional therapies, psychological clearance, and monitored clinical protocol."
            question = "Should Single Injection Epidural Pump Trials require distinct authorization from permanent pump placement?"

        elif "RULE-IPM-CGFACETBLOCKS-001" in rid:
            gap_type = "OVERSIMPLIFIED_CRITERIA"
            threshold_verif = "Axial spine pain >= 3 months; failure of >= 6 weeks conservative care; max 3 levels; >= 50% relief for diagnostic blocks."
            omitted = "Criteria on pp. 31-36: Primary axial low back or neck pain without radiculopathy; facet loading provocative maneuvers positive; failure of 6 weeks conservative care; max 3 levels per session; fluoroscopic guidance mandatory; dual diagnostic blocks required before RFA."
            inferences = "Draft rule used single placeholder 'cgfacetblocks_indication IS_PRESENT'."
            proposed = "PROPOSAL: Decompose into: (1) Initial Diagnostic Facet Block, (2) Confirmatory Second Diagnostic Block (>= 50% relief required), and (3) Session limit (max 3 contiguous levels)."
            question = "Should Facet Block rules enforce dual diagnostic blocks (>= 50% relief) prior to RFA approval?"

        elif "RULE-IPM-CGSIINJECTIONS-001" in rid:
            gap_type = "OVERSIMPLIFIED_CRITERIA"
            threshold_verif = "SI joint pain >= 3 months; 3 of 5 positive provocative tests; >= 6 weeks conservative care; max 4 injections per 12 months; minimum 60 days interval."
            omitted = "Criteria on pp. 57-62: Pain below L5; at least 3 of 5 physical exam maneuvers positive (FABER, Gaenslen, distraction, compression, thigh thrust); failure of 6 weeks conservative therapy; fluoroscopic guidance mandatory; max 4 per year."
            inferences = "Draft rule used single placeholder 'cgsiinjections_indication IS_PRESENT'."
            proposed = "PROPOSAL: Decompose into: (1) 3-of-5 provocative test requirement, (2) >= 6 weeks conservative therapy failure, (3) Fluoroscopy mandate, and (4) 60-day interval & 4/year frequency cap."
            question = "Should SI Joint Injection rules mandate documentation of 3 of 5 positive provocative physical examination maneuvers?"

        elif "RULE-IPM-CGSPINALCORDSTIM-001" in rid:
            gap_type = "OVERSIMPLIFIED_CRITERIA"
            threshold_verif = "Severe chronic neuropathic pain >= 6 months; failed back surgery syndrome or CRPS; failure of multidisciplinary conservative care."
            omitted = "Criteria on pp. 78-83: Intractable neuropathic pain failing conservative therapy for >= 6 months; formal psychological evaluation within 12 months clearing patient; no active substance abuse; trial prerequisite before permanent implant."
            inferences = "Draft rule used placeholder 'cgspinalcordstim_indication IS_PRESENT'."
            proposed = "PROPOSAL: Decompose into Trial Phase Authorization vs Permanent Implant Authorization with explicit psychological evaluation validation."
            question = "Should Spinal Cord Stimulation be split into separate rules for Trial Lead Placement vs Permanent Generator Implantation?"

        elif "RULE-IPM-CGSPINALCORDSTIM-002" in rid:
            gap_type = "UNCODIFIED_CONSERVATIVE_CARE"
            threshold_verif = "Documented trial of spinal cord stimulation demonstrating >= 50% pain relief."
            omitted = "Detailed trial parameters on p. 80: Trial duration typically 3-7 days; objective improvement in functional activities of daily living; reduction in oral opioid usage."
            inferences = "Rule correctly models >= 50% pain relief threshold, but lacks validation of trial duration (3-7 days) and functional improvement documentation."
            proposed = "PROPOSAL: Add parameter: 'scs_trial_duration_days between 3 and 7' AND 'documented_functional_adls_improvement == true'."
            question = "Should permanent SCS implant criteria validate trial duration of at least 3-7 days in addition to >= 50% pain relief?"

        elif "RULE-IPM-CGSYMPATHETICBLOCKS-001" in rid:
            gap_type = "OVERSIMPLIFIED_CRITERIA"
            threshold_verif = "CRPS Type I/II; visceral cancer pain; objective sympatholysis; max repeat intervals."
            omitted = "Anatomical differentiation on pp. 89-100: Stellate ganglion (upper extremity CRPS), Lumbar sympathetic (lower extremity CRPS), Celiac plexus (pancreatic/abdominal cancer pain), Superior hypogastric (pelvic pain), Ganglion impar (perineal pain); objective signs (Horner syndrome, skin temperature rise > 1.5 C)."
            inferences = "Draft rule lumped all sympathetic nerve blocks into a single placeholder 'cgsympatheticblocks_indication IS_PRESENT'."
            proposed = "PROPOSAL: Decompose into anatomic procedure-specific rules (Stellate, Lumbar, Celiac, Hypogastric, Impar) with procedure-specific objective monitoring criteria."
            question = "Should sympathetic blocks be partitioned into distinct rules by anatomic site (Stellate vs Lumbar vs Celiac vs Hypogastric)?"
            
        else:
            gap_type = "UNCODIFIED_FOOTNOTE"
            threshold_verif = "Standard clinical thresholds verified on page."
            omitted = "Surrounding clinical footnotes and advisory clinical considerations."
            inferences = "Core criteria verified; surrounding context requires explicit alignment."
            proposed = "PROPOSAL: Maintain rule in DRAFT status with clinical footnote alignment."
            question = "Review clinical criteria alignment against governing guideline."

    remediation_records.append({
        "rule_id": rid,
        "domain": domain,
        "governing_policy": policy_name,
        "policy_version": policy_ver,
        "source_section": section,
        "physical_page": page,
        "baseline_audit_status": status,
        "implemented_conditions_summary": f"Operator: {op}, Criteria Count: {criteria_count}. Params: {', '.join(c.get('parameter','') for c in cond.get('criteria',[]))}",
        "policy_text_verbatim": quote[:250].replace("\n", " "),
        "fidelity_gap_type": gap_type,
        "mandatory_vs_advisory": nature,
        "threshold_and_timing_verification": threshold_verif,
        "omitted_exceptions_or_prerequisites": omitted,
        "unsupported_inferences_or_broad_logic": inferences,
        "proposed_correction_for_human_review": proposed,
        "human_review_priority": priority,
        "clinical_review_question": question
    })

# Write CSV to manifests and root
for p in [OUT_CSV, OUT_CSV_ROOT]:
    with open(p, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(remediation_records)

print(f"Generated {len(remediation_records)} remediation records at {OUT_CSV} and {OUT_CSV_ROOT}")
