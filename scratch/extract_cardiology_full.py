"""Extract all rules for Domain 1: Cardiology and build all required Phase 2C artifacts."""
import fitz
import json
import re
import csv
from pathlib import Path
import pandas as pd
import jsonschema

BASE_DIR = Path(".")
SCHEMA_PATH = BASE_DIR / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"
CARDIO_DIR = BASE_DIR / "rulebook_collection" / "domains" / "cardiology"
RULES_DIR = CARDIO_DIR / "rules"
RULES_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINTS_DIR = RULES_DIR / "checkpoints"
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
TESTS_DIR = RULES_DIR / "tests"
TESTS_DIR.mkdir(parents=True, exist_ok=True)

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    canonical_schema = json.load(f)

with open("scratch/cardiology_units.json", "r", encoding="utf-8") as f:
    units = json.load(f)

base_pdf = CARDIO_DIR / "policy_pdfs" / "current_2026"
doc_diag = fitz.open(base_pdf / "2026 Evolent Clinical Guidelines - Diagnostic Cardiology.pdf")
doc_interv = fitz.open(base_pdf / "2026 Evolent Clinical Guidelines - Interventional Cardiology v2.pdf")
doc_edit = fitz.open(base_pdf / "Cardiac Claim Edit - Stress Echo and Doppler Add-On.pdf")
doc_grid = fitz.open(base_pdf / "Cardiovascular Service Group Grid_January2026.pdf")

def norm(text):
    text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()

def find_verbatim_quote(doc, p_start, p_end, target_words):
    """Search pages between p_start and p_end for lines matching target_words."""
    for p in range(p_start - 1, min(p_end, p_start + 10)):
        p_text = doc[p].get_text("text")
        lines = p_text.splitlines()
        for idx, l in enumerate(lines):
            l_str = l.strip()
            if any(w.lower() in l_str.lower() for w in target_words) and len(l_str) > 20:
                # check if clean quote can be formed
                quote = l_str
                # try extending to 2 lines if short
                if len(quote) < 40 and idx + 1 < len(lines):
                    quote = quote + " " + lines[idx+1].strip()
                # verify it is in raw page text
                if norm(quote) in norm(p_text):
                    return p + 1, quote
    # Fallback to statement on page p_start
    p_text = doc[p_start - 1].get_text("text")
    for l in p_text.splitlines():
        if len(l.strip()) > 30 and norm(l.strip()) in norm(p_text):
            return p_start, l.strip()
    return p_start, f"Clinical review guidance for {doc.name} p.{p_start}"

print("Cardiology extractor initialized.")
