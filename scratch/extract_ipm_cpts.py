import fitz, re, sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = 'rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026/2026 Evolent Interventional Pain Management Guidelines.pdf'
doc = fitz.open(pdf_path)

toc = doc.get_toc()
sections = []
for i in range(len(toc)):
    level, title, page = toc[i]
    if level == 3 or 'Preamble' in title:
        end_p = toc[i+1][2] - 1 if i+1 < len(toc) else len(doc)
        sections.append((title, page, end_p))

for title, start_p, end_p in sections:
    codes = set()
    for p in range(start_p - 1, min(end_p, len(doc))):
        text = doc[p].get_text('text')
        # look for CPTs
        cpts = re.findall(r'\b(6\d{4}|27096|0\d{3}T)\b', text)
        if 'CODING' in text:
            idx = text.find('CODING')
            after = text[idx:idx+400]
            section_cpts = re.findall(r'\b(6\d{4}|27096|0\d{3}T)\b', after)
            codes.update(section_cpts)
        codes.update(cpts)
    print(f"{title} (pp. {start_p}-{end_p}): {sorted(list(codes))}")
