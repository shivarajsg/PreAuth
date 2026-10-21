import json, os, re, sys
from pathlib import Path
import jsonschema

sys.stdout.reconfigure(encoding='utf-8')

IPM_RULES_DIR = Path('rulebook_collection/domains/interventional_pain_management/rules')
SCHEMA_PATH = Path('rulebook_collection/schemas/medrule_rule_schema.json')
DRAFT_RULES_PATH = IPM_RULES_DIR / 'draft_rules.json'

with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
    schema = json.load(f)

with open(DRAFT_RULES_PATH, 'r', encoding='utf-8') as f:
    rules = json.load(f)

print(f"Loaded {len(rules)} IPM rules.")

# Map rules to clean procedure folders
# Structure directly under IPM_RULES_DIR:
# ├── epidural_injections/
# ├── facet_interventions/
# ├── sacroiliac_joint/
# ├── neuromodulation_pumps/
# ├── sympathetic_blocks/
# └── cross_cutting/

def map_ipm_rule(r):
    rid = r['rule_id']
    service = r.get('clinical_service_or_procedure', '')
    section = r.get('source_section', '')
    
    if 'PREAMBLE' in rid:
        return 'cross_cutting', 'ipm_clinical_review_preamble.json', 'IPM Clinical Review Preamble', ['General']
    elif 'EPOS1755' in rid:
        return 'cross_cutting', 'epos_1755_site_of_care.json', 'Evolent Place of Service Policy 1755 for IPM', ['Site of Care']
    elif 'EPIDURALINJECTIONS' in rid:
        return 'epidural_injections', 'epidural_spine_injections_62321_62323.json', 'Epidural Spine Injections (ESI)', ['62320', '62321', '62322', '62323', '64479', '64480', '64483', '64484']
    elif 'EPIDURALPUMPTRIALS' in rid:
        return 'epidural_injections', 'epidural_pump_trials_62321.json', 'Epidural Injections Single Injection Trials for Intrathecal Pumps', ['62320', '62321', '62322', '62323', '64479', '64483']
    elif 'FACETBLOCKS' in rid:
        return 'facet_interventions', 'facet_joint_blocks_64490_64493.json', 'Paravertebral Facet Joint Injections or Blocks', ['64490', '64491', '64492', '64493', '64494', '64495', '0213T', '0214T', '0215T', '0216T', '0217T', '0218T']
    elif 'FACETDENERVATION' in rid:
        return 'facet_interventions', 'facet_radiofrequency_neurotomy_64633_64635.json', 'Paravertebral Facet Joint Denervation (Radiofrequency Neurotomy)', ['64633', '64634', '64635', '64636']
    elif 'SIINJECTIONS' in rid:
        return 'sacroiliac_joint', 'sacroiliac_joint_injections_27096.json', 'Sacroiliac (SI) Joint Injections', ['27096', 'G0260']
    elif 'SPINALCORDSTIM' in rid:
        return 'neuromodulation_pumps', 'spinal_cord_stimulation_63650_63685.json', 'Spinal Cord Stimulation (SCS Trial & Permanent Implant)', ['63650', '63655', '63685', '63688']
    elif 'INFUSIONPUMPS' in rid:
        return 'neuromodulation_pumps', 'implantable_infusion_pumps_62350_62362.json', 'Implantable Infusion Pump Insertion', ['62350', '62351', '62360', '62361', '62362']
    elif 'SYMPATHETICBLOCKS' in rid:
        return 'sympathetic_blocks', 'sympathetic_nerve_blocks_64510_64530.json', 'Sympathetic Nerve Blocks (Stellate, Celiac, Lumbar)', ['64510', '64517', '64520', '64530']
    else:
        return 'other', f"{rid.lower()}.json", service, []

from collections import defaultdict
groups = defaultdict(lambda: defaultdict(list))
titles_map = {}
codes_map = {}

for r in rules:
    folder, fname, title, cpts = map_ipm_rule(r)
    groups[folder][fname].append(r)
    titles_map[(folder, fname)] = title
    codes_map[(folder, fname)] = cpts

total_written = 0
for folder, file_dict in sorted(groups.items()):
    dir_path = IPM_RULES_DIR / folder
    dir_path.mkdir(parents=True, exist_ok=True)
    
    for fname, r_list in sorted(file_dict.items()):
        file_path = dir_path / fname
        title = titles_map[(folder, fname)]
        cpts = codes_map[(folder, fname)]
        
        for r in r_list:
            jsonschema.validate(instance=r, schema=schema)
            
        payload = {
            "section_title": title,
            "folder_classification": folder,
            "file_name": fname,
            "rule_count": len(r_list),
            "procedure_codes": cpts,
            "rules": r_list
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2)
            
        total_written += len(r_list)

print(f"Successfully organized and wrote {total_written} IPM rules across {len(groups)} clean directories.")
assert total_written == len(rules)
