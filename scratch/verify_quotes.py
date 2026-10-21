import json, os, re, fitz

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip().lower()

with open('rulebook_collection/domains/advanced_imaging/rules/draft_rules.json', encoding='utf-8') as f:
    adv = json.load(f)
with open('rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json', encoding='utf-8') as f:
    ipm = json.load(f)

all_rules = adv + ipm
pdf_docs = {}

def get_doc(sfile):
    cand_paths = [
        sfile,
        os.path.join('rulebook_collection', sfile),
        os.path.join('rulebook_collection/domains/advanced_imaging/policy_pdfs/current_2026', os.path.basename(sfile)),
        os.path.join('rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026', os.path.basename(sfile)),
        os.path.join('rulebook_collection/domains/interventional_pain_management/policy_pdfs/current_2026', 'EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf')
    ]
    for cp in cand_paths:
        if os.path.exists(cp):
            if cp not in pdf_docs:
                pdf_docs[cp] = fitz.open(cp)
            return pdf_docs[cp]
    return None

exact_matches = 0
fuzzy_matches = 0
not_found = []

for r in all_rules:
    rid = r['rule_id']
    sfile = r['source_file']
    spage = r['source_page']
    quote = r.get('source_quote', '')
    
    doc = get_doc(sfile)
    if not doc:
        not_found.append((rid, "Doc not found", sfile))
        continue
        
    phys_p = spage.get('physical_page') if isinstance(spage, dict) else spage
    if not isinstance(phys_p, int):
        phys_p = int(phys_p)
        
    page = doc[phys_p - 1]
    page_text = page.get_text()
    
    norm_page = normalize_text(page_text)
    norm_quote = normalize_text(quote)
    
    # Check first 50 chars of quote
    first_snippet = norm_quote[:60].strip()
    if norm_quote in norm_page:
        exact_matches += 1
    elif first_snippet and first_snippet in norm_page:
        fuzzy_matches += 1
    else:
        # Check if words appear
        words = [w for w in norm_quote.split() if len(w) > 4][:5]
        found_words = sum(1 for w in words if w in norm_page)
        if words and found_words >= len(words) - 1:
            fuzzy_matches += 1
        else:
            not_found.append((rid, phys_p, quote[:60]))

print(f"Total rules: {len(all_rules)}")
print(f"Exact quote matches: {exact_matches}")
print(f"Fuzzy / snippet matches: {fuzzy_matches}")
print(f"Quotes not matched directly: {len(not_found)}")
if not_found:
    print("Sample unmatched quotes:")
    for item in not_found[:5]:
        print(" ", item)
