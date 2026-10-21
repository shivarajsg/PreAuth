import json
import csv
from pathlib import Path
import pymupdf
import re

def audit_ipm():
    doc26 = pymupdf.open('rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf')
    doc25 = pymupdf.open('rulebook_collection/domains/interventional_pain_management/policies/historical/2025 Evolent Interventional Pain Management Guidelines.pdf')
    epos = pymupdf.open('rulebook_collection/domains/interventional_pain_management/policies/current/EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf')

    with open('rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json', 'r', encoding='utf-8') as f:
        existing_rules = json.load(f)

    # Let's inspect sections in doc26
    guidelines = [
        {"id": "PREAMBLE-IPM", "title": "Preamble and Guideline Development Process", "start": 1, "end": 3},
        {"id": "CG-1750", "title": "Epidural Spine Injections", "start": 4, "end": 16},
        {"id": "CG-1751", "title": "Epidural Spine Injections and Single Injection Trials for Intrathecal Pumps", "start": 17, "end": 30},
        {"id": "CG-1753", "title": "Paravertebral Facet Joint Injections or Blocks", "start": 31, "end": 44},
        {"id": "CG-1754", "title": "Paravertebral Facet Joint Denervation (Radiofrequency Neurolysis)", "start": 45, "end": 56},
        {"id": "CG-1756", "title": "Sacroiliac Joint Injections", "start": 57, "end": 66},
        {"id": "CG-1752", "title": "Implantable Infusion Pump Insertion", "start": 67, "end": 76},
        {"id": "CG-1757", "title": "Spinal Cord Stimulation", "start": 77, "end": 88},
        {"id": "CG-1758", "title": "Sympathetic Nerve Blocks", "start": 89, "end": 102},
    ]

    print("=== Extracting sections from IPM 2026 ===")
    all_sections = []
    for g in guidelines:
        g_sections = []
        for p in range(g['start'], g['end'] + 1):
            text = doc26[p-1].get_text('text')
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            for l in lines:
                # Header detector: all caps or starts with standard header terms
                if len(l) > 3 and l.isupper() and not l.startswith("PAGE") and not l.startswith("EVOLENT"):
                    g_sections.append((p, l))
        print(f"Guideline {g['id']} ({g['title']}): {len(g_sections)} uppercase lines found")
        # Let's sample key sections
        unique_secs = []
        for p, s in g_sections:
            if s not in [us[1] for us in unique_secs] and len(s) > 5:
                unique_secs.append((p, s))
        for p, s in unique_secs[:10]:
            print(f"    p{p}: {s}")

if __name__ == '__main__':
    audit_ipm()
