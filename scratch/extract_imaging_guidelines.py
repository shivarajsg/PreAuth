import fitz, re, sys, json

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf'
doc = fitz.open(pdf_path)
toc = doc.get_toc()

guidelines = []
for i in range(len(toc)):
    level, title, start_page = toc[i]
    if 'Clinical Guideline' in title or 'Preamble' in title:
        end_page = toc[i+1][2] - 1 if i+1 < len(toc) else len(doc)
        guidelines.append((title, start_page, end_page))

print(f'Total clinical guidelines found: {len(guidelines)}')

extracted_data = []

for title, start_p, end_p in guidelines:
    clean_title = ' '.join(title.split())
    codes = set()
    indications = []
    
    # scan pages
    for p in range(start_p - 1, min(end_p, len(doc))):
        text = doc[p].get_text('text')
        if 'CODING AND STANDARDS' in text:
            idx = text.find('CODING AND STANDARDS')
            after = text[idx:idx+600]
            m = re.search(r'Codes\s*\n([^\n]+)', after)
            if m:
                code_line = m.group(1).strip()
                # parse codes
                cpts = re.findall(r'[+]?[0-9]{4,5}[A-Z]?', code_line)
                codes.update(cpts)
            # also look for direct CPTs
            direct_cpts = re.findall(r'\b(7\d{4}|0\d{3}T)\b', after)
            codes.update(direct_cpts)
            
    extracted_data.append({
        'title': clean_title,
        'start_page': start_p,
        'end_page': end_p,
        'codes': sorted(list(codes))
    })

with open('scratch/imaging_guidelines_index.json', 'w', encoding='utf-8') as f:
    json.dump(extracted_data, f, indent=2)

for item in extracted_data:
    print(f"{item['title']} (pp. {item['start_page']}-{item['end_page']}): {', '.join(item['codes'])}")
