from pathlib import Path

ROOT = Path(".")
summary_file = ROOT / "reports" / "batch_02_summary.md"

content = """# MedRule — Batch 2 Policy Fidelity Audit Summary

- **Audited Rules (10):** `RULE-ADV-CG2008-003`, `RULE-ADV-CG2008-004`, `RULE-ADV-CG2009-002`, `RULE-ADV-CG2015-001`, `RULE-ADV-CG2016-001`, `RULE-ADV-CG2017-001`, `RULE-ADV-CG2017-002`, `RULE-ADV-CG2017-003`, `RULE-ADV-CG2022-001`, `RULE-ADV-CG2030-001` (all Advanced Imaging; IPM remains segregated).
- **Files Inspected:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (pp. 149, 151, 175–176, 297, 308, 330–331, 436, 490), `advanced_imaging/rules/draft_rules.json`, `test_decision_tree.py`, `test_scope_integrity.py`.
- **Category A (Explicit Policy Omissions):** All 10 rules omit explicit sub-criteria: 003 (8 distinct trauma signs); 004 (< 48h onset); 002 (<= 24h LVO window); 001 (prior CT prerequisite); 001 (individual NEXUS criteria); 001 (specific PT modalities); 002 (reflex findings); 003 (neurological deficits clause); 001 (symptomatic gate & diverticulitis exclusion); 001 (mandatory asymptomatic screening gate).
- **Category B (Shared/Routing Handled):** Sibling rules handle red flag bypasses (CG2017-002/003); routing handles MRI contraindication waivers (CG2008-004) and CPT/LOB validations (CG2015-001, CG2030-001).
- **Category C (Advisory Context):** Background references for NEXUS/CCR, stroke penumbra software, and smoking cessation counseling.
- **Category D (Ambiguity/Discrepancy):** `RULE-ADV-CG2009-002` cites p. 176 (aneurysm section), but LVO policy is on p. 175; `RULE-ADV-CG2030-001` footnote * allows curative candidates > 80yo.
- **Category E (Unconfirmed Claims):** None (all clinical concepts confirmed in source text).
- **Significant Evidence Excerpts:**
  1. *CG2009 p. 175:* "candidates for mechanical thrombectomy within 24 hours of symptom onset or last known well" (omitted in 002).
  2. *CG2017 p. 330:* "with any neurological deficits as listed above" (omitted in 003, which only checks cord compression).
  3. *CG2030 p. 490:* "medically necessary ONLY when used to screen... asymptomatic individuals" (omitted in 001).
- **Unresolved Questions:** (1) Should `RULE-ADV-CG2009-002` citation be updated from p. 176 to p. 175? (2) Must LDCT rule enforce `asymptomatic == true`?
- **Validation & Invariants:** 29 of 29 regression tests passed (`.venv\\Scripts\\pytest medrule_engine/tests/test_decision_tree.py rulebook_collection/tests/test_scope_integrity.py`). All 7 blocked rules remain blocked; 0 approved rules; historical fallbacks blocked; CP.MP.107 100% excluded.
"""

lines = content.strip().split("\n")
print(f"Total lines: {len(lines)}")
assert len(lines) <= 25, f"Line count {len(lines)} exceeds 25 lines!"

with open(summary_file, "w", encoding="utf-8") as f:
    f.write(content.strip() + "\n")

print(f"Written {summary_file} successfully ({len(lines)} lines).")
