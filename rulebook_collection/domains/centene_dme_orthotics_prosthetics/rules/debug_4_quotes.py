import fitz
from build_rules_data_107 import get_cp_mp_107_rules

doc = fitz.open(r"c:\Users\KumarShiva\Downloads\PreAuth\rulebook_collection\domains\centene_dme_orthotics_prosthetics\policy_pdfs\current_2026\CP.MP.107 (Revision 08-26).pdf")
rules = {r["rule_id"]: r for r in get_cp_mp_107_rules()}

for rid in ["RULE-DME-107-039", "RULE-DME-107-052", "RULE-DME-107-055", "RULE-DME-107-056"]:
    r = rules[rid]
    p_num = r["source_page"]["physical_page"]
    p_text = " ".join(doc[p_num - 1].get_text().split())
    q = " ".join(r["source_quote"].split())
    print(f"=== {rid} (Page {p_num}) ===")
    print("Wanted quote:", q[:80])
    # check where it diverges
    words = q.split()
    matched_len = 0
    for i in range(1, len(words) + 1):
        sub = " ".join(words[:i])
        if sub in p_text:
            matched_len = i
        else:
            break
    print(f"Matched up to {matched_len}/{len(words)} words: {' '.join(words[:matched_len])}")
    if matched_len < len(words):
        print("Diverged at word:", words[matched_len:matched_len+5])
        # Find where the last matched words are in p_text
        last_sub = " ".join(words[max(0, matched_len-5):matched_len])
        idx = p_text.find(last_sub)
        if idx != -1:
            print("Text in PDF around here:", p_text[idx:idx+150])
