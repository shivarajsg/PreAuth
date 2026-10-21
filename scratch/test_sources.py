import json, os, fitz

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', encoding='utf-8') as f:
    adv = json.load(f)
with open('rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json', encoding='utf-8') as f:
    ipm = json.load(f)

all_rules = adv + ipm
print('Total rules across both domains:', len(all_rules))

all_ids = set()
for r in all_rules:
    rid = r['rule_id']
    if rid in all_ids:
        print('DUPLICATE ID:', rid)
    all_ids.add(rid)

print('Unique rule IDs:', len(all_ids))

pdf_pages = {}
out_of_bounds = []
missing_files = []

for r in all_rules:
    sfile = r['source_file']
    spage = r['source_page']
    rid = r['rule_id']
    
    cand_paths = [
        sfile,
        os.path.join('rulebook_collection', sfile),
        os.path.join('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026', os.path.basename(sfile)),
        os.path.join('rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026', os.path.basename(sfile)),
        os.path.join('rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026', 'EPOS 1755 for Place of Service - Interventional Pain Management 2026.pdf')
    ]
    found = None
    for cp in cand_paths:
        if os.path.exists(cp):
            found = cp
            break
    if not found:
        missing_files.append((rid, sfile))
        continue
        
    if found not in pdf_pages:
        doc = fitz.open(found)
        pdf_pages[found] = len(doc)
        doc.close()
    max_p = pdf_pages[found]
    
    if isinstance(spage, dict):
        phys_p = spage.get('physical_page')
    elif isinstance(spage, int):
        phys_p = spage
    elif isinstance(spage, str) and spage.isdigit():
        phys_p = int(spage)
    else:
        phys_p = None
        
    if phys_p is None or phys_p < 1 or phys_p > max_p:
        out_of_bounds.append((rid, spage, max_p, found))

print(f"Missing source files: {len(missing_files)}")
print(f"Out of bounds pages: {len(out_of_bounds)}")
if out_of_bounds:
    for item in out_of_bounds:
        print("  ", item)
if missing_files:
    for item in missing_files:
        print("  ", item)

print(f"Resolved PDFs and page counts:")
for k, v in pdf_pages.items():
    print(f"  {k}: {v} pages")
