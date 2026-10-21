# MedRule — Batch 1 Policy Audit Summary

- **Audit Target:** First 10 partially verified rules (`RULE-ADV-CG2000-002` through `RULE-ADV-CG2008-002`), all within Advanced Imaging.
- **Governing Policy Inspected:** `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` (1,041 physical pages).
- **Domain Separation:** Advanced Imaging (rules 1–35 of 43 PV) and Interventional Pain Management (rules 36–43) remain strictly isolated.
- **Baseline Rule Inventory:** 128 unique rule IDs (114 Advanced Imaging, 14 IPM); 121 DRAFT, 7 NEEDS_HUMAN_REVIEW, 0 APPROVED.
- **Coverage-Gap Baseline:** 204 records verified (170 Advanced Imaging, 34 IPM).
- **Citations & Provenance Verification:** 10 of 10 cited physical pages (pp. 9, 75, 92, 118, 119, 150, 151) and sections resolve exactly.
- **Unverified Files or Citations:** **NONE** (0 unverified citations; all 10 source quotations located and cross-referenced in active PDF).
- **Audit Findings:** All 10 rules confirmed **PARTIALLY_VERIFIED**:
  1. `RULE-ADV-CG2000-002` (p. 9): Core prerequisites match; lacks uncodified toxic megacolon/perforation emergency exclusion.
  2. `RULE-ADV-CG2000-004` (p. 9): Systemic criteria match; lacks uncodified pregnancy ultrasound-first gate.
  3. `RULE-ADV-CG2000-005` (p. 9): Pediatric criteria match; lacks uncodified body habitus/cooperation ultrasound exception.
  4. `RULE-ADV-CG2003-001` (p. 75): Surveillance intervals match verbatim; relies on external cross-cutting MRI contraindication rules.
  5. `RULE-ADV-CG2004-001` (p. 92): Prior ultrasound requirement matches; needs clarification on MRCP CPT code specificity.
  6. `RULE-ADV-CG2004-002` (p. 92): Pain criterion matches; omits objective lipase/amylase > 3x ULN laboratory criterion.
  7. `RULE-ADV-CG2005-001` (p. 118): Mesenteric ischemia matches; surrounding text details biphasic CTA acquisition protocol.
  8. `RULE-ADV-CG2005-002` (p. 119): Indication matches; lacks explicit CT contraindication check to trigger MR angiography fallback.
  9. `RULE-ADV-CG2008-001` (p. 150): Acute stroke indication matches; focal deficits compressed into composite boolean.
  10. `RULE-ADV-CG2008-002` (p. 151): Acute SAH indication matches; lumbar puncture correlation is advisory guidance.
- **Safety Checks:** 29 of 29 regression tests passed (`test_decision_tree.py` [15], `test_scope_integrity.py` [14]).
- **Governance Invariants:** 0 rules approved; all 7 blocked rules remain blocked; CP.MP.107 DME policy remains 100% isolated.
