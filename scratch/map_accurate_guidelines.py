import csv, fitz, re, json, sys

sys.stdout.reconfigure(encoding='utf-8')

inv_path = 'rulebook_collection/domains/advanced_imaging/rules/guideline_coverage_inventory.csv'
pdf_path = 'rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf'

doc = fitz.open(pdf_path)

entries = []
with open(inv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        entries.append(row)

results = []
for entry in entries:
    gid = entry['guideline_id']
    gtitle = entry['guideline_title']
    try:
        start_p = int(entry['physical_start_page'])
        end_p = int(entry['physical_end_page'])
    except:
        continue
    
    codes = set()
    found_coding_section = False
    
    for p in range(start_p - 1, min(end_p, len(doc))):
        text = doc[p].get_text('text')
        if 'CODING AND STANDARDS' in text:
            found_coding_section = True
            idx = text.find('CODING AND STANDARDS')
            after = text[idx:idx+600]
            m = re.search(r'Codes\s*\n([^\n]+)', after)
            if m:
                code_line = m.group(1).strip()
                cpts = re.findall(r'[+]?[0-9]{4,5}[A-Z]?', code_line)
                codes.update(cpts)
            direct = re.findall(r'\b(7\d{4}|0\d{3}T)\b', after)
            codes.update(direct)
            
    results.append({
        'guideline_id': gid,
        'title': gtitle,
        'start_page': start_p,
        'end_page': end_p,
        'page_count': end_p - start_p + 1,
        'codes': sorted(list(codes))
    })

with open('scratch/accurate_guidelines_map.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

for r in results:
    code_str = ', '.join(r['codes']) if r['codes'] else 'None'
    print(f"{r['guideline_id']} | {r['title']} | pp.{r['start_page']}-{r['end_page']} | Codes: {code_str}")
