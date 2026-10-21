import json
import re
from pathlib import Path

with open("scratch/batch1_first10_audit.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

for r in rules:
    page_norm = re.sub(r"\s+", " ", r["page_text"])
    quote_clean = re.sub(r"[●○■\s]+", " ", r["source_quote"]).strip()
    match = quote_clean[:50].lower() in page_norm.lower()
    print(f"Rule: {r['rule_id']} | Page: {r['physical_page']} | Match: {match}")
    print(f"   Quote clean: {quote_clean[:80]}...")
    if not match:
        print(f"   Page excerpt: {page_norm[:150]}...")
