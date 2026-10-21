import json
import re
from pathlib import Path
import pymupdf

ROOT = Path(".")
# 1. Check RULE-ADV-CG2009-002 page citation
doc = pymupdf.open("rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf")
print("=== CARRY-FORWARD 1: RULE-ADV-CG2009-002 Page Check ===")
for p in [174, 175, 176]:
    txt = doc[p-1].get_text()
    has_lvo = "large vessel occlusion" in txt.lower() or "thrombectomy" in txt.lower()
    has_aneurysm = "aneurysm" in txt.lower()
    print(f"Physical Page {p}: has_lvo={has_lvo}, has_aneurysm={has_aneurysm}")
    for l in txt.split("\n"):
        if "large vessel occlusion" in l.lower() or "mechanical thrombectomy" in l.lower() or "evaluation of known intracranial" in l.lower():
            print(f"  Page {p} line:", l.strip())

# 2. Check RULE-ADV-CG2030-001 asymptomatic enforcement
print("\n=== CARRY-FORWARD 2: RULE-ADV-CG2030-001 Asymptomatic Check ===")
# Search across medrule_engine for 71271, CG2030, asymptomatic
engine_files = list(Path("medrule_engine").glob("**/*.py")) + list(Path("medrule_engine").glob("**/*.json"))
for f in engine_files:
    content = f.read_text(encoding="utf-8", errors="ignore")
    if "71271" in content or "CG2030" in content or "asymptomatic" in content:
        print(f"Found reference in {f.name}:")
        for line in content.split("\n"):
            if "71271" in line or "CG2030" in line or "asymptomatic" in line:
                print("   ", line.strip()[:100])
