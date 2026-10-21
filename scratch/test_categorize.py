import json, os, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

rules_file = 'rulebook_collection/domains/advanced_imaging/rules/draft_rules.json'
with open(rules_file, 'r', encoding='utf-8') as f:
    rules = json.load(f)

print(f'Total rules: {len(rules)}')

# Categorize by modality and anatomy
categorized = defaultdict(lambda: defaultdict(list))

for r in rules:
    service = r.get('clinical_service_or_procedure', '')
    rule_id = r.get('rule_id', '')
    section = r.get('source_section', '')
    
    # Extract guideline code from rule_id: RULE-ADV-CG2008-001 -> CG2008
    m = re.search(r'RULE-ADV-([A-Z0-9]+)-', rule_id)
    cg = m.group(1) if m else 'OTHER'
    
    # Determine modality
    s_lower = (service + ' ' + section).lower()
    
    if 'preamble' in cg.lower() or 'preamble' in s_lower:
        modality = 'governance'
        anatomy = 'preamble'
    elif 'epos' in cg.lower() or 'place of service' in s_lower:
        modality = 'cross_cutting'
        anatomy = 'place_of_service'
    elif 'urgent' in s_lower or 'emergent' in s_lower or cg == 'CG2066':
        modality = 'cross_cutting'
        anatomy = 'urgent_emergent'
    elif 'cta' in s_lower or 'computed tomography angiography' in s_lower or cg in ['CG2002', 'CG2005', 'CG2006', 'CG2009', 'CG2020', 'CG2033', 'CG2040', 'CG2043', 'CG2063']:
        modality = 'cta'
        if any(w in s_lower for w in ['brain', 'head']):
            anatomy = 'head_brain'
        elif any(w in s_lower for w in ['neck', 'carotid']):
            anatomy = 'neck'
        elif any(w in s_lower for w in ['chest', 'pulmonary', 'aort']):
            anatomy = 'chest'
        elif any(w in s_lower for w in ['abdomen', 'aorta', 'runoff']):
            anatomy = 'abdomen_pelvis'
        elif any(w in s_lower for w in ['pelvis']):
            anatomy = 'abdomen_pelvis'
        elif any(w in s_lower for w in ['lower extremity', 'leg']):
            anatomy = 'extremities'
        elif any(w in s_lower for w in ['upper extremity', 'arm']):
            anatomy = 'extremities'
        else:
            anatomy = 'general'
    elif 'mra' in s_lower or 'magnetic resonance angiography' in s_lower or cg in ['CG2003', 'CG2011', 'CG2021', 'CG2034', 'CG2041', 'CG2044', 'CG2053', 'CG2064']:
        modality = 'mra'
        if any(w in s_lower for w in ['brain', 'head']):
            anatomy = 'head_brain'
        elif any(w in s_lower for w in ['neck']):
            anatomy = 'neck'
        elif any(w in s_lower for w in ['chest']):
            anatomy = 'chest'
        elif any(w in s_lower for w in ['spinal canal', 'spine']):
            anatomy = 'spine'
        elif any(w in s_lower for w in ['abdomen', 'pelvis']):
            anatomy = 'abdomen_pelvis'
        elif any(w in s_lower for w in ['extremity']):
            anatomy = 'extremities'
        else:
            anatomy = 'general'
    elif 'pet' in s_lower or 'spect' in s_lower or cg in ['CG2013', 'CG2046', 'CG2052', 'CG2058']:
        modality = 'pet_spect'
        if 'brain' in s_lower:
            anatomy = 'brain'
        else:
            anatomy = 'oncology_tumor_imaging'
    elif 'ct' in s_lower or cg in ['CG2000', 'CG2001', 'CG2008', 'CG2015', 'CG2016', 'CG2018', 'CG2022', 'CG2023', 'CG2024', 'CG2029', 'CG2030', 'CG2032', 'CG2036', 'CG2039', 'CG2042', 'CG2047', 'CG2054', 'CG2056', 'CG2062']:
        modality = 'ct'
        if any(w in s_lower for w in ['brain', 'head', 'cerebral', 'orbit', 'sella', 'ear', 'mastoid', 'sinus', 'maxillofacial']):
            anatomy = 'head_brain'
        elif 'neck' in s_lower:
            anatomy = 'neck'
        elif any(w in s_lower for w in ['chest', 'lung', 'thorax']):
            anatomy = 'chest'
        elif any(w in s_lower for w in ['cervical spine', 'thoracic spine', 'lumbar spine', 'spine']):
            anatomy = 'spine'
        elif any(w in s_lower for w in ['abdomen', 'pelvis', 'colonoscopy']):
            anatomy = 'abdomen_pelvis'
        elif any(w in s_lower for w in ['extremity', 'arm', 'leg', 'foot', 'hand']):
            anatomy = 'extremities'
        elif any(w in s_lower for w in ['bone density', 'qct']):
            anatomy = 'specialized'
        else:
            anatomy = 'general'
    elif 'mri' in s_lower or cg in ['CG2004', 'CG2007', 'CG2010', 'CG2012', 'CG2014', 'CG2017', 'CG2019', 'CG2027', 'CG2028', 'CG2031', 'CG2035', 'CG2037', 'CG2038', 'CG2045', 'CG2048', 'CG2055', 'CG2057', 'CG2065']:
        modality = 'mri'
        if any(w in s_lower for w in ['brain', 'spectroscopy', 'functional', 'tmj', 'internal auditory canal', 'iac']):
            anatomy = 'brain'
        elif any(w in s_lower for w in ['chest', 'breast']):
            anatomy = 'chest_breast'
        elif any(w in s_lower for w in ['cervical spine', 'thoracic spine', 'lumbar spine', 'spine']):
            anatomy = 'spine'
        elif any(w in s_lower for w in ['abdomen', 'mrcp', 'elastography', 'pelvis']):
            anatomy = 'abdomen_pelvis'
        elif any(w in s_lower for w in ['extremity', 'joint', 'knee', 'shoulder', 'hip']):
            anatomy = 'extremities'
        elif any(w in s_lower for w in ['bone marrow', 'fetal']):
            anatomy = 'specialized'
        else:
            anatomy = 'general'
    else:
        modality = 'specialized'
        anatomy = 'general'
        
    categorized[modality][anatomy].append(r)

for mod, anats in sorted(categorized.items()):
    total_mod = sum(len(v) for v in anats.values())
    print(f'Modality: {mod.upper()} ({total_mod} rules)')
    for anat, r_list in sorted(anats.items()):
        print(f'   ├── {anat}: {len(r_list)} rules')
