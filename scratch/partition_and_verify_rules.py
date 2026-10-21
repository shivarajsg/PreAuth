from collections import defaultdict
import json, os, re, sys
from pathlib import Path
import jsonschema
import fitz

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path('rulebook_collection/domains/advanced_imaging/rules')
ORGANIZED_DIR = BASE_DIR / 'organized_by_modality'
SCHEMA_PATH = BASE_DIR / 'schema.json'
RULES_PATH = BASE_DIR / 'draft_rules.json'
PDF_PATH = Path('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf')
EPOS_PATH = Path('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/EPOS 2067 for Place of Service - Radiology 2026_final.pdf')

with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
    schema = json.load(f)

with open(RULES_PATH, 'r', encoding='utf-8') as f:
    rules = json.load(f)

print(f"Loaded {len(rules)} rules to organize and verify.")

# Map each rule to target folder and file
# Structure:
# organized_by_modality/
# ├── ct/
# │   ├── head_brain/
# │   ├── chest/
# │   ├── spine/
# │   ├── abdomen_pelvis/
# │   ├── extremities/
# │   └── specialized/
# ├── mri/
# │   ├── brain/
# │   ├── chest_breast/
# │   ├── spine/
# │   ├── abdomen_pelvis/
# │   ├── extremities/
# │   └── specialized/
# ├── cta/
# ├── mra/
# ├── pet_spect/
# └── cross_cutting/

def get_target_location(r):
    rid = r['rule_id']
    service = r.get('clinical_service_or_procedure', '')
    section = r.get('source_section', '')
    s_lower = (service + ' ' + section).lower()
    
    m = re.search(r'RULE-ADV-([A-Z0-9]+)-', rid)
    cg = m.group(1) if m else 'OTHER'
    
    if cg == 'PREAMBLE':
        return 'cross_cutting/governance', 'clinical_review_preamble.json', 'Clinical Review Preamble'
    elif 'epos' in cg.lower() or 'place of service' in s_lower:
        return 'cross_cutting/place_of_service', 'epos_2067_site_of_care.json', 'Place of Service Policy EPOS-2067'
    elif 'urgent' in s_lower or 'emergent' in s_lower or cg == 'CG2066':
        return 'cross_cutting/urgent_emergent', 'cg_2066_urgent_emergent_exceptions.json', 'Urgent / Emergent Exceptions CG-2066'
    elif cg in ['CG2002', 'CG2005', 'CG2006', 'CG2009', 'CG2020', 'CG2033', 'CG2040', 'CG2043', 'CG2063']:
        # CTA
        if cg == 'CG2009':
            return 'cta/head_brain', 'cta_brain_70496.json', 'Brain CTA (CPT 70496)'
        elif cg == 'CG2040':
            return 'cta/neck', 'cta_neck_70498.json', 'Neck CTA (CPT 70498)'
        elif cg == 'CG2020':
            return 'cta/chest', 'cta_chest_pe_71275.json', 'Chest CTA (CPT 71275)'
        elif cg == 'CG2002':
            return 'cta/abdomen_pelvis', 'cta_abdomen_74175.json', 'Abdomen CTA (CPT 74175)'
        elif cg == 'CG2005':
            return 'cta/abdomen_pelvis', 'cta_abdomen_pelvis_74174.json', 'Abdomen and Pelvis CTA (CPT 74174)'
        elif cg == 'CG2006':
            return 'cta/abdomen_pelvis', 'cta_aorta_runoff_75635.json', 'Abdominal Aorta CTA with Runoff (CPT 75635)'
        elif cg == 'CG2043':
            return 'cta/abdomen_pelvis', 'cta_pelvis_72191.json', 'Pelvis CTA (CPT 72191)'
        elif cg == 'CG2063':
            return 'cta/extremities', 'cta_upper_extremity_73206.json', 'Upper Extremity CTA (CPT 73206)'
        elif cg == 'CG2033':
            return 'cta/extremities', 'cta_lower_extremity_73706.json', 'Lower Extremity CTA (CPT 73706)'
        else:
            return 'cta/other', f'{cg.lower()}_cta.json', service
    elif cg in ['CG2003', 'CG2011', 'CG2021', 'CG2034', 'CG2041', 'CG2044', 'CG2053', 'CG2064']:
        # MRA
        if cg == 'CG2011':
            return 'mra/head_brain', 'mra_brain_70544_70546.json', 'Brain MRA (CPT 70544-70546)'
        elif cg == 'CG2041':
            return 'mra/neck', 'mra_neck_70547_70549.json', 'Neck MRA (CPT 70547-70549)'
        elif cg == 'CG2021':
            return 'mra/chest', 'mra_chest_71555.json', 'Chest MRA (CPT 71555)'
        elif cg == 'CG2053':
            return 'mra/spine', 'mra_spinal_canal_72159.json', 'Spinal Canal MRA (CPT 72159)'
        elif cg == 'CG2003':
            return 'mra/abdomen_pelvis', 'mra_abdomen_74185.json', 'Abdomen MRA (CPT 74185)'
        elif cg == 'CG2044':
            return 'mra/abdomen_pelvis', 'mra_pelvis_72198.json', 'Pelvis MRA (CPT 72198)'
        elif cg == 'CG2064':
            return 'mra/extremities', 'mra_upper_extremity_73225.json', 'Upper Extremity MRA (CPT 73225)'
        elif cg == 'CG2034':
            return 'mra/extremities', 'mra_lower_extremity_73725.json', 'Lower Extremity MRA (CPT 73725)'
        else:
            return 'mra/other', f'{cg.lower()}_mra.json', service
    elif cg in ['CG2013', 'CG2046', 'CG2052', 'CG2058']:
        # PET / SPECT
        if cg == 'CG2013':
            return 'pet_spect/brain', 'pet_brain_78608_78609.json', 'Brain PET (CPT 78608-78609)'
        elif cg in ['CG2046', 'CG2058']:
            return 'pet_spect/oncology_tumor', 'pet_ct_tumor_imaging_78811_78816.json', 'PET/CT Tumor Imaging (CPT 78811-78816)'
        elif cg == 'CG2052':
            return 'pet_spect/oncology_tumor', 'spect_tumor_localization_78830_78835.json', 'SPECT Tumor Localization (CPT 78830-78835)'
        else:
            return 'pet_spect/other', f'{cg.lower()}_pet.json', service
    elif cg in ['CG2000', 'CG2001', 'CG2008', 'CG2015', 'CG2016', 'CG2018', 'CG2022', 'CG2023', 'CG2024', 'CG2026', 'CG2029', 'CG2030', 'CG2032', 'CG2036', 'CG2039', 'CG2042', 'CG2047', 'CG2054', 'CG2056', 'CG2061', 'CG2062']:
        # CT
        if cg == 'CG2008':
            return 'ct/head_brain', 'ct_head_brain_70450_70470.json', 'CT Head/Brain (CPT 70450, 70460, 70470)'
        elif cg == 'CG2015':
            return 'ct/head_brain', 'ct_cerebral_perfusion_70473.json', 'CT Cerebral Perfusion (CPT 70473)'
        elif cg == 'CG2054':
            return 'ct/head_brain', 'ct_temporal_bone_orbit_sella_70480_70482.json', 'CT Orbit / Sella / Temporal Bone (CPT 70480-70482)'
        elif cg == 'CG2047':
            return 'ct/head_brain', 'ct_sinus_maxillofacial_70486_70488.json', 'CT Maxillofacial / Sinus (CPT 70486-70488)'
        elif cg == 'CG2039':
            return 'ct/neck', 'ct_neck_soft_tissue_70490_70492.json', 'CT Neck Soft Tissue (CPT 70490-70492)'
        elif cg == 'CG2018':
            return 'ct/chest', 'ct_chest_diagnostic_71250_71270.json', 'CT Chest Diagnostic (CPT 71250, 71260, 71270)'
        elif cg == 'CG2030':
            return 'ct/chest', 'ct_lung_cancer_screening_71271.json', 'Low-Dose CT Lung Cancer Screening (CPT 71271)'
        elif cg == 'CG2016':
            return 'ct/spine', 'ct_cervical_spine_72125_72127.json', 'CT Cervical Spine (CPT 72125-72127)'
        elif cg == 'CG2056':
            return 'ct/spine', 'ct_thoracic_spine_72128_72130.json', 'CT Thoracic Spine (CPT 72128-72130)'
        elif cg == 'CG2036':
            return 'ct/spine', 'ct_lumbar_spine_72131_72133.json', 'CT Lumbar Spine (CPT 72131-72133)'
        elif cg == 'CG2001':
            return 'ct/abdomen_pelvis', 'ct_abdomen_only_74150_74170.json', 'CT Abdomen Only (CPT 74150-74170)'
        elif cg == 'CG2042':
            return 'ct/abdomen_pelvis', 'ct_pelvis_only_72192_72194.json', 'CT Pelvis Only (CPT 72192-72194)'
        elif cg == 'CG2000':
            return 'ct/abdomen_pelvis', 'ct_abdomen_pelvis_combined_74176_74178.json', 'CT Abdomen and Pelvis (CPT 74176-74178)'
        elif cg in ['CG2022', 'CG2023']:
            return 'ct/abdomen_pelvis', 'ct_colonography_virtual_colonoscopy_74261_74263.json', 'CT Virtual Colonoscopy (CPT 74261-74263)'
        elif cg == 'CG2062':
            return 'ct/extremities', 'ct_upper_extremity_73200_73202.json', 'CT Upper Extremity (CPT 73200-73202)'
        elif cg == 'CG2032':
            return 'ct/extremities', 'ct_lower_extremity_73700_73702.json', 'CT Lower Extremity (CPT 73700-73702)'
        elif cg == 'CG2024':
            return 'ct/specialized', 'ct_bone_density_qct_77078.json', 'QCT Bone Density Study (CPT 77078)'
        elif cg == 'CG2026':
            return 'ct/specialized', 'ct_needle_guidance_77011_77013.json', 'CT Needle Guidance (CPT 77011-77013)'
        elif cg in ['CG2029', 'CG2061']:
            return 'ct/specialized', f'{cg.lower()}_ct.json', service
        else:
            return 'ct/other', f'{cg.lower()}_ct.json', service
    elif cg in ['CG2004', 'CG2007', 'CG2010', 'CG2012', 'CG2014', 'CG2017', 'CG2019', 'CG2027', 'CG2028', 'CG2031', 'CG2035', 'CG2037', 'CG2038', 'CG2045', 'CG2048', 'CG2055', 'CG2057', 'CG2065']:
        # MRI
        if cg == 'CG2012':
            return 'mri/brain', 'mri_brain_70551_70553.json', 'MRI Brain (CPT 70551, 70552, 70553)'
        elif cg == 'CG2028':
            return 'mri/brain', 'mri_functional_brain_70554_70555.json', 'Functional MRI Brain (CPT 70554, 70555)'
        elif cg == 'CG2010':
            return 'mri/brain', 'mr_spectroscopy_76390.json', 'Magnetic Resonance Spectroscopy MRS (CPT 76390)'
        elif cg == 'CG2048':
            return 'mri/brain', 'mri_sinus_face_neck_iac_70540_70543.json', 'MRI Face / Neck / Orbit / IAC (CPT 70540-70543)'
        elif cg == 'CG2055':
            return 'mri/brain', 'mri_tmj_70336.json', 'MRI Temporomandibular Joint TMJ (CPT 70336)'
        elif cg == 'CG2019':
            return 'mri/chest_breast', 'mri_chest_71550_71552.json', 'MRI Chest (CPT 71550-71552)'
        elif cg == 'CG2014':
            return 'mri/chest_breast', 'mri_breast_77046_77049.json', 'MRI Breast (CPT 77046-77049)'
        elif cg == 'CG2017':
            return 'mri/spine', 'mri_cervical_spine_72141_72156.json', 'MRI Cervical Spine (CPT 72141, 72142, 72156)'
        elif cg == 'CG2057':
            return 'mri/spine', 'mri_thoracic_spine_72146_72157.json', 'MRI Thoracic Spine (CPT 72146, 72147, 72157)'
        elif cg == 'CG2037':
            return 'mri/spine', 'mri_lumbar_spine_72148_72158.json', 'MRI Lumbar Spine (CPT 72148, 72149, 72158)'
        elif cg == 'CG2004':
            return 'mri/abdomen_pelvis', 'mri_abdomen_mrcp_74181_74183.json', 'MRI Abdomen / MRCP (CPT 74181-74183)'
        elif cg == 'CG2038':
            return 'mri/abdomen_pelvis', 'mr_elastography_76391.json', 'Magnetic Resonance Elastography MRE (CPT 76391)'
        elif cg == 'CG2045':
            return 'mri/abdomen_pelvis', 'mri_pelvis_72195_72197.json', 'MRI Pelvis (CPT 72195-72197)'
        elif cg == 'CG2065':
            return 'mri/extremities', 'mri_upper_extremity_73218_73223.json', 'MRI Upper Extremity (CPT 73218-73223)'
        elif cg == 'CG2035':
            return 'mri/extremities', 'mri_lower_extremity_73718_73723.json', 'MRI Lower Extremity (CPT 73718-73723)'
        elif cg == 'CG2007':
            return 'mri/specialized', 'mri_bone_marrow_77084.json', 'MRI Bone Marrow (CPT 77084)'
        elif cg == 'CG2027':
            return 'mri/specialized', 'mri_fetal_74712_74713.json', 'Fetal MRI (CPT 74712-74713)'
        elif cg in ['CG2031']:
            return 'mri/specialized', 'mri_low_field.json', 'Low Field MRI'
        else:
            return 'mri/other', f'{cg.lower()}_mri.json', service
    else:
        return 'specialized/other', f'{cg.lower()}.json', service

groups = defaultdict(lambda: defaultdict(list))
titles_map = {}

for r in rules:
    folder_rel, filename, section_title = get_target_location(r)
    groups[folder_rel][filename].append(r)
    titles_map[(folder_rel, filename)] = section_title

print(f"Divided into {len(groups)} directory paths across modalities.")

# Now verify and write each file
total_written = 0
ORGANIZED_DIR.mkdir(parents=True, exist_ok=True)

for folder_rel, file_dict in sorted(groups.items()):
    dir_path = ORGANIZED_DIR / folder_rel
    dir_path.mkdir(parents=True, exist_ok=True)
    
    for filename, r_list in sorted(file_dict.items()):
        file_path = dir_path / filename
        title = titles_map[(folder_rel, filename)]
        
        # Verify every rule in r_list against schema
        for r in r_list:
            jsonschema.validate(instance=r, schema=schema)
            
        data = {
            "section_title": title,
            "folder_classification": folder_rel,
            "file_name": filename,
            "rule_count": len(r_list),
            "procedure_codes": sorted(list(set(re.findall(r'\b(7\d{4}|0\d{3}T)\b', json.dumps(r_list))))),
            "rules": r_list
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        total_written += len(r_list)

print(f"Successfully wrote {total_written} verified rules into organized_by_modality.")
assert total_written == len(rules), f"Mismatch: wrote {total_written} vs original {len(rules)}"
