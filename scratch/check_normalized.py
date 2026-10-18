import fitz, sys, re
sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')

slices = {
    'RULE-ADV-CG2000-001': (8, 'It is an expectation that all patients receive care/services from a licensed clinician. All appropriate supporting documentation, including recent pertinent office visit notes, laboratory data, and results of any special testing must be provided. If applicable: All prior relevant imaging results and the reason that alternative imaging cannot be performed must be included in the documentation submitted.'),
    'RULE-ADV-CG2000-002': (9, 'For suspected inflammatory bowel disease after complete work up including physical exam, labs, and recent colonoscopy'),
    'RULE-ADV-CG2000-003': (9, 'Magnetic resonance imaging (MRI) should be considered in patients younger than 35 years of age to minimize radiation exposure'),
    'RULE-ADV-CG2000-004': (9, 'Suspected diverticulitis or acute appendicitis for initial imaging with at least ONE of the following (10): ○ WBC Elevated ○ Fever ○ Anorexia ○ Nausea and vomiting'),
    'RULE-ADV-CG2000-005': (9, 'When initial workup with x-ray and/or ultrasound is inconclusive, negative, or does not provide sufficient detail to guide management'),
    'RULE-ADV-CG2000-006': (10, 'Initial imaging for suspected acute pancreatitis due to epigastric pain with elevated amylase and/or lipase: ○ Mild presentation when symptom improvement is not seen after 72 hours of treatment and either: ■ Ultrasound has been performed and did not show an abnormality such as gallstones, dilated bile duct ■ Ultrasound suggests complications (such as fluid collection)'),
    'RULE-ADV-CG2000-007': (10, 'Severe presentation (such as fever, elevated WBC) ○ Decline in clinical status and/or suspected complication'),
    'RULE-ADV-CG2000-008': (11, 'Kidney Stone is NOT suspected AND ● Urinalysis is negative for infection or hematuria persists on urine microscopy following treatment of urinary tract infection AND ● At least one of the following: ○ Gross hematuria ○ > 25 RBC/hpf on urine microscopy'),
    'RULE-ADV-CG2000-009': (11, '3-25 RBC/hpf on urine microscopy AND ONE or more of the following: ■ >30 pack year smoking history ■ Male ≥ age 60 ■ Abnormal renal ultrasound ■ Negative renal ultrasound and repeat sample shows persistence of ≥ 3 RBC/hpf'),
    'RULE-ADV-CG2000-010': (13, 'Aneurysm size 5.0-5.4 cm, every 6 months'),
    'RULE-ADV-CG2000-011': (13, 'Known or suspected symptomatic AAA (30,31) ○ Symptoms may include: ■ Abrupt onset of severe sharp or stabbing pain in the chest, back or abdomen (could indicate possible aneurysm rupture) ■ Acute abdominal or back pain with a pulsatile or epigastric mass ■ Acute abdominal or back pain and at high risk for aortic aneurysm and/or aortic syndrome (risk factors include hypertension, atherosclerosis, prior cardiac or aortic surgery, underlying aneurysm, connective tissue disorder (Such as Marfan syndrome, vascular form of Ehlers-Danlos syndrome, Loeys-Dietz syndrome), and bicuspid aortic valve) (32)'),
    'RULE-ADV-CG2000-012': (19, 'When a cancer is not listed above, Abdomen and Pelvis CT is not routinely a part of surveillance for that cancer in an asymptomatic patient. There would need to be a sign or symptom of recurrence to consider Abdomen and Pelvis CT.'),
    'RULE-ADV-CG2012-001': (224, 'Known or suspected brain tumor (primary or metastatic) or cancer with a high risk of CNS metastases (such as lung, breast, melanoma, renal cell, and colorectal)'),
    'RULE-ADV-CG2012-002': (225, 'Persistent headache and any ONE of the following (8–10): ○ Immune deficiency ○ History of neoplasm ○ History of congenital heart disease ○ See Imaging in Known Genetic Conditions for additional indications ○ Coagulopathy ○ Occipital location ○ Age < 6 years'),
    'RULE-ADV-CG2017-001': (330, 'Failure of conservative treatment* for a minimum of six (6) weeks within the last six (6) months: NOTE - Failure of conservative treatment is defined as one of the following: ○ Lack of meaningful improvement after a full course of treatment; OR ○ Progression or worsening of symptoms during treatment; OR ○ Documentation of a medical reason the member is unable to participate in treatment'),
    'RULE-ADV-CG2017-002': (331, 'Evaluation of Suspected Myelopathy (11,12) ● Progressive symptoms including hand clumsiness, worsening handwriting, difficulty with grasping and holding objects, diffuse numbness in the hands, pins and needles sensation, increasing difficulty with balance and ambulation ● Any of the neurological deficits as noted above NOTE: Does NOT require conservative care')
}

all_matched = True
for rid, (p, text) in slices.items():
    page_text = doc[p - 1].get_text('text')
    clean_p = re.sub(r'\s+', ' ', page_text).strip()
    clean_q = re.sub(r'\s+', ' ', text).strip()
    if clean_q in clean_p:
        print(f'{rid} (page {p}): MATCH')
    else:
        print(f'{rid} (page {p}): FAIL')
        all_matched = False
print(f'ALL MATCHED: {all_matched}')
