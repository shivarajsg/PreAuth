# MedRule — Phase 8B.3A: Governance Invariant Reconciliation Report

**Document ID:** `MEDRULE-REPORT-PHASE-08B3A-RECONCILIATION`  
**Date:** 2026-10-22  
**Investigation Type:** Diagnostic & Governance Audit (Read-Only Investigation)  
**Governing Documents & Code:**  
- `medrule_engine/decision_tree.py` (`GOVERNANCE_BLOCKED_RULE_IDS`)  
- `rulebook_collection/domains/advanced_imaging/rules/draft_rules.json`  
- `rulebook_collection/domains/interventional_pain_management/rules/draft_rules.json`  
- `medrule_engine/governance/data/governance.db` (`rule_governance_state`)  
- `medrule_engine/tests/test_decision_tree.py`  
- `medrule_engine/tests/test_phase8b3_tier1_rules.py`  
- `reports/phase_08b3_tier1_implementation.md`  
- `reports/phase_08b1_citation_corrections.md`  
- `reports/phase_08a_remediation_register.json`  
- `reports/phase_07_policy_fidelity_audit.md`  
- `reports/phase_03_governance_reconciliation.md`  

---

## 1. Executive Summary & Core Findings

This investigation was initiated to resolve a discrepancy between the governance-blocked rule IDs reported across earlier phases (Phase 3 through Phase 8B.1) and an alternative set of seven rule IDs listed in Section 5 of the Phase 8B.3 completion report.

### Key Audit Findings:

1. **`GOVERNANCE_BLOCKED_RULE_IDS` Never Changed in Code:**  
   The authoritative hardcoded set of blocked rule IDs in `medrule_engine/decision_tree.py` (lines 30–39) has **never been altered** since repository inception (Git commit `0b99dc89e4b884a7158edf8e03fdbea2b30064b0`). The canonical set consists strictly of:
   - `RULE-ADV-PREAMBLE-001`
   - `RULE-ADV-CG2000-003`
   - `RULE-ADV-CG2001-001`
   - `RULE-ADV-CG2066-001`
   - `RULE-ADV-CG2066-002`
   - `RULE-IPM-PREAMBLEIPM-001`
   - `RULE-IPM-CGINFUSIONPUMPS-001`

2. **The Active Rule Registry Is 100% Consistent with the Code:**  
   In `RuleRegistry(include_archived=False)`, exactly the same 7 rules have `extraction_status: "NEEDS_HUMAN_REVIEW"` and `human_review_required: true` (5 in Advanced Imaging, 2 in IPM). The remaining 121 active rules have status `DRAFT`. Exactly 0 rules have status `APPROVED`.

3. **The Phase 8B.3 Report Text Contained a Narrative Transcription Error:**  
   The text in Section 5 of `reports/phase_08b3_tier1_implementation.md` listed an erroneous set of 7 rule IDs. This was purely a **documentation/clerical error in the Markdown text** of that report. The actual Python code, rulebook files, database records, and automated test fixtures were never modified to use that erroneous list.

4. **All Canonical Blocked Rules Remain Unconditionally Protected:**  
   Every one of the 7 canonical blocked rules evaluates strictly to `DecisionOutcome.NEEDS_HUMAN_REVIEW` in `DecisionTreeEngine.evaluate()`. None can autonomously approve or deny a request.

5. **No Rule Has Been Approved & Scope Invariants Are Preserved:**  
   The active registry contains exactly 128 rules across 2 active domains (114 Advanced Imaging, 14 IPM). Zero rules are approved in the registry (`APPROVED: 0`) and zero rules are approved in `governance.db` (`is_approved == 0` for all 372 records).

---

## 2. Authoritative Governance State Audit

### A. Decision Tree Engine (`medrule_engine/decision_tree.py`)

Lines 30–39 of `medrule_engine/decision_tree.py` define the engine-level safety gate:

```python
# The 7 rules strictly blocked from autonomous decision execution by governance
GOVERNANCE_BLOCKED_RULE_IDS: Set[str] = {
    "RULE-ADV-PREAMBLE-001",
    "RULE-ADV-CG2000-003",
    "RULE-ADV-CG2001-001",
    "RULE-ADV-CG2066-001",
    "RULE-ADV-CG2066-002",
    "RULE-IPM-PREAMBLEIPM-001",
    "RULE-IPM-CGINFUSIONPUMPS-001",
}
```

A Git blame/log check on these exact lines confirms:
- **Commit:** `0b99dc89e4b884a7158edf8e03fdbea2b30064b0`
- **Author:** Shrinidhi Bijapur
- **Date:** 2026-10-21 09:30:15 +0530
- **Modifications since creation:** **0 modifications (completely untouched)**.

### B. Active Rulebook Registry (`draft_rules.json`)

Querying `RuleRegistry(include_archived=False).all_rules` yields:

| Domain | Rule ID | Governance Status | `human_review_required` | Blocking Rationale in Policy |
| :--- | :--- | :--- | :--- | :--- |
| `advanced_imaging` | `RULE-ADV-PREAMBLE-001` | `NEEDS_HUMAN_REVIEW` | `True` | Overly broad pseudo-rule; clinical judgment preamble |
| `advanced_imaging` | `RULE-ADV-CG2000-003` | `NEEDS_HUMAN_REVIEW` | `True` | Advisory language ("MRI should be considered < 35") |
| `advanced_imaging` | `RULE-ADV-CG2001-001` | `NEEDS_HUMAN_REVIEW` | `True` | Claims billing unbundling edit (74176 vs 74150+72192) |
| `advanced_imaging` | `RULE-ADV-CG2066-001` | `NEEDS_HUMAN_REVIEW` | `True` | Retrospective emergent review requires physician judgment |
| `advanced_imaging` | `RULE-ADV-CG2066-002` | `NEEDS_HUMAN_REVIEW` | `True` | Retrospective urgent review requires physician judgment |
| `interventional_pain_management` | `RULE-IPM-PREAMBLEIPM-001` | `NEEDS_HUMAN_REVIEW` | `True` | Non-executable clinical preamble |
| `interventional_pain_management` | `RULE-IPM-CGINFUSIONPUMPS-001` | `NEEDS_HUMAN_REVIEW` | `True` | Multi-step permanent pump criteria (12w care, psych, trial) |

**Set Equality Verification:**
$$\text{set}(\text{rules with NEEDS\_HUMAN\_REVIEW}) \equiv \text{GOVERNANCE\_BLOCKED\_RULE\_IDS} \quad (\text{True})$$

### C. Governance Database (`medrule_engine/governance/data/governance.db`)

Direct query against `rule_governance_state`:
```sql
SELECT extraction_status, is_approved, count(*) 
FROM rule_governance_state 
GROUP BY extraction_status, is_approved;
```
**Results:**
- `('DRAFT', 0, 322)`
- `('NEEDS_HUMAN_REVIEW', 0, 50)`
- Total tracked rules: 372 (128 active + 244 archived domains)
- Total `is_approved == 1`: **0**
- Total `extraction_status == 'APPROVED'`: **0**

---

## 3. Root Cause Analysis of the Discrepancy

In Section 5 of `reports/phase_08b3_tier1_implementation.md`, the following erroneous text block appeared:

```markdown
Blocked Governance Gates (GOVERNANCE_BLOCKED_RULE_IDS):
  1. RULE-ADV-CG2000-001 (General Preamble Criteria)
  2. RULE-ADV-CG2012-001 (Adult Brain MRI Inconclusive Imaging)
  3. RULE-ADV-CG2012-003 (Brain MRI Multiple Sclerosis)
  4. RULE-ADV-CG2035-003 (Knee MRI Revision / Post-Op)
  5. RULE-IPM-CGFACETINJECTIONS-001 (Facet Joint Injections Initial Diagnostic)
  6. RULE-IPM-CGTRIGGERPOINT-001 (Trigger Point Injections Initial Series)
  7. RULE-IPM-EPOS1755-001 (Place of Service Inpatient Exception)
```

### Detailed Breakdown of the Erroneous List:

| Erroneously Listed Rule ID | Actual Status in Active Registry | Actual Role in Decision Tree | Why It Appeared in the Erroneous List |
| :--- | :--- | :--- | :--- |
| `RULE-ADV-CG2000-001` | `DRAFT` (`human_review_required: False`) | Runnable active rule | Tested in `test_decision_tree.py` line 228 (`test_06_boolean_all_of_and_any_of_logic_paths`) |
| `RULE-ADV-CG2012-001` | `DRAFT` (`human_review_required: False`) | Runnable active rule | Tested in `test_decision_tree.py` line 295 (`test_08_prior_treatment_prerequisites`) |
| `RULE-ADV-CG2012-003` | `DRAFT` (`human_review_required: False`) | Runnable active rule | Tested in `test_decision_tree.py` line 170 (`test_04_dual_track_separation`) |
| `RULE-ADV-CG2035-003` | `DRAFT` (`human_review_required: False`) | Runnable active rule | Tested in `test_phase3b_integration.py` line 526 (`test_knee_mri_routes_knee_rules`) |
| `RULE-IPM-CGFACETINJECTIONS-001` | **DOES NOT EXIST** | N/A | Hallucinated ID; actual rule is `RULE-IPM-CGFACETBLOCKS-001` (`DRAFT`) |
| `RULE-IPM-CGTRIGGERPOINT-001` | **DOES NOT EXIST** | N/A | Hallucinated ID; Trigger Point Injections are uncodified in active 14 IPM rules |
| `RULE-IPM-EPOS1755-001` | `DRAFT` (`human_review_required: False`) | Runnable active rule | Tested in `test_decision_tree.py` line 130 (`test_04_dual_track_separation`) |

### Cause of the Defect:
During the composition of the completion report `reports/phase_08b3_tier1_implementation.md`, the Markdown section was manually drafted rather than programmatically rendered from `medrule_engine.decision_tree.GOVERNANCE_BLOCKED_RULE_IDS`. The author conflated test fixture rule IDs frequently referenced in `test_decision_tree.py` with the blocked governance gate list.

Crucially, **the automated test `test_governance_invariants_preserved` in `test_phase8b3_tier1_rules.py` executed against the true code object `GOVERNANCE_BLOCKED_RULE_IDS`**, which is why the test suite passed with 100% green assertions:

```python
    def test_governance_invariants_preserved(self):
        approved_rules = [r for r in self.registry.all_rules if r.extraction_status == "APPROVED"]
        self.assertEqual(len(approved_rules), 0)

        blocked_rules = [r for r in self.registry.all_rules if r.extraction_status == "NEEDS_HUMAN_REVIEW"]
        self.assertEqual(len(blocked_rules), 7)

        blocked_ids = {r.rule_id for r in blocked_rules}
        self.assertEqual(blocked_ids, set(GOVERNANCE_BLOCKED_RULE_IDS)) # Evaluated True against canonical set!
```

---

## 4. Protection Verification of Canonical Blocked Rules

To guarantee that none of the seven canonical blocked rules can generate an autonomous authorization decision, each rule was evaluated through `DecisionTreeEngine.evaluate()` with synthetic clinical evidence designed to satisfy all condition parameters:

```python
Testing evaluation of all 7 GOVERNANCE_BLOCKED_RULE_IDS:
  RULE-ADV-CG2000-003: outcome=NEEDS_HUMAN_REVIEW, reasons=["RULE-ADV-CG2000-003: Rule RULE-ADV-CG2000-003 is flagged 'NEEDS_HUMAN_REVIEW': Advisory wording ('MRI should be considered'). Flagged for medical director determination..."]
  RULE-ADV-CG2001-001: outcome=NEEDS_HUMAN_REVIEW, reasons=["RULE-ADV-CG2001-001: Rule RULE-ADV-CG2001-001 is flagged 'NEEDS_HUMAN_REVIEW': Anti-unbundling coding rule mandating combined CT Abdomen/Pelvis codes (74176-74178)..."]
  RULE-ADV-CG2066-001: outcome=NEEDS_HUMAN_REVIEW, reasons=["RULE-ADV-CG2066-001: Rule RULE-ADV-CG2066-001 is flagged 'NEEDS_HUMAN_REVIEW': Emergent retrospective review requires physician clinical determination of life/limb threat."]
  RULE-ADV-CG2066-002: outcome=NEEDS_HUMAN_REVIEW, reasons=["RULE-ADV-CG2066-002: Rule RULE-ADV-CG2066-002 is flagged 'NEEDS_HUMAN_REVIEW': Urgent retrospective review requires physician clinical evaluation of 24-hour urgency."]
  RULE-ADV-PREAMBLE-001: outcome=NEEDS_HUMAN_REVIEW, reasons=["RULE-ADV-PREAMBLE-001: Rule RULE-ADV-PREAMBLE-001 is flagged 'NEEDS_HUMAN_REVIEW': Clinical preamble establishing that determinations are made based on both guidelines and clinical judgment..."]
  RULE-IPM-CGINFUSIONPUMPS-001: outcome=NEEDS_HUMAN_REVIEW, reasons=["RULE-IPM-CGINFUSIONPUMPS-001: Rule RULE-IPM-CGINFUSIONPUMPS-001 is flagged 'NEEDS_HUMAN_REVIEW': Flagged for human clinical review"]
  RULE-IPM-PREAMBLEIPM-001: outcome=NEEDS_HUMAN_REVIEW, reasons=["RULE-IPM-PREAMBLEIPM-001: Rule RULE-IPM-PREAMBLEIPM-001 is flagged 'NEEDS_HUMAN_REVIEW': Flagged for human clinical review"]
```

**Result:** Every single blocked rule unconditionally intercepts evaluation before decision execution and escalates to `NEEDS_HUMAN_REVIEW`. Autonomous approval is strictly impossible.

---

## 5. Scope and Invariant Summary

| Invariant Dimension | Verified Current Value | Expected Invariant | Status |
| :--- | :--- | :--- | :--- |
| **Total Active Rules** | 128 | 128 | **CONFIRMED** |
| **Advanced Imaging Rules** | 114 | 114 | **CONFIRMED** |
| **IPM Rules** | 14 | 14 | **CONFIRMED** |
| **Active APPROVED Rules** | 0 | 0 | **CONFIRMED** |
| **Active DRAFT Rules** | 121 | 121 | **CONFIRMED** |
| **Active NEEDS_HUMAN_REVIEW Rules** | 7 | 7 | **CONFIRMED** |
| **Database APPROVED Rules (`is_approved == 1`)** | 0 | 0 | **CONFIRMED** |
| **Engine Blocked Gates (`GOVERNANCE_BLOCKED_RULE_IDS`)** | 7 canonical rules | 7 canonical rules | **CONFIRMED** |
| **Archived Domains (`CP.MP.107` DMEPOS)** | Completely isolated | Completely isolated | **CONFIRMED** |

---

## 6. Corrective Action

1. **No Code, Configuration, or Database Changes Needed:**  
   The system implementation is completely intact, uncorrupted, and mathematically aligned with all previous governance audits and safety gates.
2. **Report Remediation (Completed in Phase 8B.3B):**  
   In [reports/phase_08b3_tier1_implementation.md](file:///d:/PreAuth/reports/phase_08b3_tier1_implementation.md), Section 5 has been administratively corrected to display the true canonical list of seven blocked rule IDs:
   - `RULE-ADV-PREAMBLE-001`
   - `RULE-ADV-CG2000-003`
   - `RULE-ADV-CG2001-001`
   - `RULE-ADV-CG2066-001`
   - `RULE-ADV-CG2066-002`
   - `RULE-IPM-PREAMBLEIPM-001`
   - `RULE-IPM-CGINFUSIONPUMPS-001`
3. **Investigation & Correction Boundary:**  
   In accordance with instructions, zero production code, rule definitions, databases, statuses, or tests were modified during this diagnostic and administrative correction phase.

---

## 7. Stage Sign-Off

Phase 8B.3A diagnostic reconciliation is complete. The system's governance invariants remain 100% solid and uncompromised. Execution has halted. Awaiting authorization before proceeding to Tier 2 remediation.
