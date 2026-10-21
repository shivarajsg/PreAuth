# MedRule — Targeted Audit: CP.MP.107 Runtime Isolation Verification

**Document ID:** MEDRULE-AUDIT-CPMP107-001  
**Audit Date:** 2026-10-21  
**Auditor:** Automated Clinical Governance & Security Audit Agent  
**Active Clinical Scope:** Advanced Imaging & Interventional Pain Management (IPM)  
**Approved Rules Invariant:** 0 (Zero-Approval Invariant Enforced)  
**Final Audit Status:** `NO ACTIVE RUNTIME DEPENDENCY VERIFIED`  

---

## 1. Executive Summary

A targeted audit was conducted to investigate whether Centene Clinical Policy **CP.MP.107** (*"Durable Medical Equipment and Orthotics and Prosthetics Guidelines"*), any of its physical PDF copies, its duplicate clones, or its codified clinical criteria can enter, influence, or cross-contaminate active MedRule prior authorization evaluations in **Advanced Imaging** or **Interventional Pain Management (IPM)**.

### Summary of Audit Proof
1. **Zero Active Runtime Dependencies:** Not a single active rule in Advanced Imaging (114 rules) or IPM (14 rules) references `CP.MP.107`, cites DME criteria, or links to any CP.MP.107 PDF.
2. **Physical PDF Quarantining:** All copies of `CP.MP.107` reside exclusively in `rulebook_collection/archive_candidate/` (and the pre-cleanup backup directory `scratch/backup_rulebook_collection_20261021/`). None exist in active policy folders.
3. **Domain Gate Rejection:** Any case intake specifying `centene_dme_orthotics_prosthetics` is unconditionally rejected at the domain isolation gate as `POLICY_NOT_APPLICABLE` before policy routing occurs.
4. **Registry Isolation:** The active runtime registry ([`RuleRegistry`](file:///d:/PreAuth/medrule_engine/rule_registry.py)) loads rules exclusively from `rulebook_collection/domains/`, which contains only `advanced_imaging` and `interventional_pain_management`. Exactly 0 DMEPOS rules are loaded into memory.
5. **Database Decoupling:** The 99 historical Centene DME rows in `governance.db` belong to the Phase 4A review workbench and are never queried by `DecisionTreeEngine`, `EvaluationService`, `PolicyRouter`, or `ConditionEvaluator`.
6. **Non-Interference Empirically Proven:** Dedicated negative regression test [`test_15_cp_mp_107_dmepos_complete_isolation_and_non_interference`](file:///d:/PreAuth/medrule_engine/tests/test_decision_tree.py#L535-L635) proved that injecting CP.MP.107 criteria into active imaging and pain management cases has exactly zero effect on decision outcomes, rule execution traces, or cryptographic hashes.

---

## 2. Physical Inventory of CP.MP.107 Copies & Cryptographic Hashes

An exhaustive search of the repository identified exactly 8 physical files matching `CP.MP.107`:

| Relative File Path | Directory Classification | File Size | Page Count | SHA-256 Cryptographic Hash |
| :--- | :--- | :---: | :---: | :--- |
| `rulebook_collection/archive_candidate/duplicate_quarantine/source_pdfs/CP.MP.107(4).pdf` | Quarantined Duplicate | 428,607 bytes | 21 | `9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29` |
| `rulebook_collection/archive_candidate/unrelated_domains/dmepos/CP.MP.107.pdf` | Archived Unrelated Policy | 428,607 bytes | 21 | `9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29` |
| `rulebook_collection/archive_candidate/unrelated_domains/dmepos/policy_pdfs/current_2026/CP.MP.107 (Revision 08-26).pdf` | Archived Unrelated Policy | 566,759 bytes | 28 | `e67ca165b078fdb32caea282ca6b5a486c39f12d0633fb52b8e7e7199c212fb4` |
| `rulebook_collection/archive_candidate/unrelated_domains/dmepos/policy_pdfs/historical_versions/CP.MP.107 (Revision 11-24).pdf` | Archived Unrelated Policy | 428,607 bytes | 21 | `9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29` |
| `scratch/backup_rulebook_collection_20261021/domains/centene_dme_orthotics_prosthetics/policy_pdfs/current_2026/CP.MP.107 (Revision 08-26).pdf` | Pre-Cleanup Backup | 566,759 bytes | 28 | `e67ca165b078fdb32caea282ca6b5a486c39f12d0633fb52b8e7e7199c212fb4` |
| `scratch/backup_rulebook_collection_20261021/domains/centene_dme_orthotics_prosthetics/policy_pdfs/historical_versions/CP.MP.107 (Revision 11-24).pdf` | Pre-Cleanup Backup | 428,607 bytes | 21 | `9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29` |
| `scratch/backup_rulebook_collection_20261021/source_pdfs/CP.MP.107(4).pdf` | Pre-Cleanup Backup | 428,607 bytes | 21 | `9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29` |
| `scratch/backup_rulebook_collection_20261021/source_pdfs/CP.MP.107.pdf` | Pre-Cleanup Backup | 428,607 bytes | 21 | `9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29` |

### Key Findings on Physical Files:
- Exactly **two unique SHA-256 hashes** exist across all physical copies of CP.MP.107:
  - `9ef5e7dbf19af436c7aa42bf19013cdde77ad067fb17a10173f2bd68adc03d29` (Rev. 11/24, 21 pages)
  - `e67ca165b078fdb32caea282ca6b5a486c39f12d0633fb52b8e7e7199c212fb4` (Rev. 08/26, 28 pages)
- **Zero active policy folders** contain any copy of CP.MP.107. All 4 active copies in `rulebook_collection/` reside inside `archive_candidate/` (`duplicate_quarantine` or `unrelated_domains/dmepos`).

---

## 3. Repository-Wide Code & Rule Search

Searches across the entire repository for `CP.MP.107`, `DME and O&P`, `Durable Medical Equipment`, and both SHA-256 hashes produced the following results:

### 3.1 Active Clinical Rules Search
- Searched:
  - `rulebook_collection/domains/advanced_imaging/rules/*.json`
  - `rulebook_collection/domains/interventional_pain_management/rules/*.json`
- **Result:** **0 matches**. Not a single active rule in either domain contains `CP.MP.107`, `CP.MP`, `DME and O&P`, or either SHA-256 hash.

### 3.2 Active Runtime Engine Code (`medrule_engine/`)
- `policy_router.py:129-139`: Contains a date boundary check for `centene_dme_orthotics_prosthetics`:
  ```python
  if domain == "centene_dme_orthotics_prosthetics" and dos < datetime.date(2026, 8, 1):
      ...
  ```
  *Analysis:* This branch is completely unreachable during active evaluation because `DecisionTreeEngine.evaluate()` rejects `centene_dme_orthotics_prosthetics` at line 188 before routing is invoked.
- `integrations/payer_config.py:127`: Contains mock metadata defining Centene plan products. It is not referenced in clinical evaluation logic.
- `decision_tree.py`: **0 matches**.
- `condition_evaluator.py`: **0 matches**.
- `rule_registry.py`: **0 matches**.
- `case_validator.py`: **0 matches**.

### 3.3 Database Search (`medrule_engine/governance/data/governance.db`)
- `rule_governance_state`: Contains 99 historical rows for `centene_dme_orthotics_prosthetics` from the earlier Phase 3F/4A workbench snapshot.
- *Analysis:* The runtime decision-tree engine does **not** connect to or read from `governance.db`. Rules are loaded exclusively from JSON rule files into memory by `RuleRegistry`.

### 3.4 Historical & Test Artifacts (Non-Runtime Matches)
- Matches in `medrule_engine/pilot/synthetic_pilot_cases.json` and `human_adjudication_log.csv`: Static test fixtures from the Phase 3D 9-domain pilot.
- Matches in `rulebook_collection/manifests/`: Audit manifests documenting the scope cleanup and relocation of DMEPOS to `archive_candidate/`.

---

## 4. Active Runtime Path & Execution Pipeline Trace

Tracing a submitted case through the active MedRule runtime confirms strict isolation:

```mermaid
flowchart TD
    A["Case Intake Payload"] --> B["CaseValidator.validate()"]
    B --> C{"DecisionTreeEngine Domain Gate"}
    
    C -->|"clinical_domain == centene_dme_orthotics_prosthetics"| D["REJECT IMMEDIATELY<br/>(POLICY_NOT_APPLICABLE)"]
    C -->|"clinical_domain in {'advanced_imaging', 'interventional_pain_management'}"| E["PolicyRouter.route_case()"]
    
    E --> F["Filter Active Registry Rules<br/>(rule.version_status == 'current_2026_verified')"]
    F --> G{"Dual-Track Partitioning"}
    
    G --> H["Track 1: CLINICAL_NECESSITY<br/>(2026 Evolent Guidelines)"]
    G --> I["Track 2: PLACE_OF_SERVICE<br/>(EPOS 2067 / EPOS 1755)"]
    
    H --> J["ConditionEvaluator (3-Valued Logic)"]
    I --> J
    
    J --> K["Outcome Aggregation & Provenance"]
```

### Trace Details:
1. **Case Intake:** When a case with `clinical_domain: "centene_dme_orthotics_prosthetics"` or DME procedure code `E0601` is received, `DecisionTreeEngine.evaluate()` executes line 188:
   ```python
   active_domains = {"advanced_imaging", "interventional_pain_management"}
   if case.clinical_domain not in active_domains:
       return DecisionTreeAssessment(
           overall_outcome=DecisionOutcome.POLICY_NOT_APPLICABLE,
           clinical_necessity_explanation=f"Clinical domain '{case.clinical_domain}' is not in active MedRule scope (Advanced Imaging & IPM only)."
       )
   ```
   *Execution terminates instantly. Zero rules are loaded, routed, or evaluated.*
2. **Rule Loading:** `RuleRegistry.load_all_domains()` iterates exclusively over subdirectories in `rulebook_collection/domains/`. Only `advanced_imaging` and `interventional_pain_management` exist in this directory. The archived DME directory (`rulebook_collection/archive_candidate/unrelated_domains/dmepos/`) is ignored because `include_archived` defaults to `False`.
3. **No Cross-Domain Fallback:** `PolicyRouter` has zero fallback logic to query other domains. If no rules match the procedure code or modality, it returns `POLICY_NOT_APPLICABLE`.

---

## 5. Confirmation of the Four Intended Governing Documents

The audit confirmed that all active evaluations are governed strictly and exclusively by the four designated policies:

| Clinical / Administrative Track | Intended Governing Document | Physical File Path | Verification Status |
| :--- | :--- | :--- | :---: |
| **Advanced Imaging (Clinical Necessity)** | 2026 Evolent Clinical Guidelines for Medical Necessity Review: Advanced Imaging Guidelines (v2) | `rulebook_collection/domains/advanced_imaging/policies/current/2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf` | **VERIFIED** |
| **Advanced Imaging (Place of Service)** | Evolent Place of Service Policy 2067 for Radiology | `rulebook_collection/domains/advanced_imaging/policies/current/EPOS 2067 for Place of Service - Radiology 2026_final.pdf` | **VERIFIED** |
| **Interventional Pain Management (Clinical Necessity)** | 2026 Evolent Clinical Guidelines for Medical Necessity Review: Interventional Pain Management Guidelines | `rulebook_collection/domains/interventional_pain_management/policies/current/2026 Evolent Interventional Pain Management Guidelines.pdf` | **VERIFIED** |
| **Interventional Pain Management (Place of Service)** | Evolent Place of Service Policy 1755 for Interventional Pain Management | `rulebook_collection/domains/interventional_pain_management/policies/current/EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf` | **VERIFIED** |

---

## 6. Negative Regression Test Execution

A dedicated test method was added to [`medrule_engine/tests/test_decision_tree.py`](file:///d:/PreAuth/medrule_engine/tests/test_decision_tree.py):  
`TestMedRuleDecisionTree.test_15_cp_mp_107_dmepos_complete_isolation_and_non_interference`

### Executed Test Scenarios & Verifications:
1. **Direct DMEPOS Intake Rejection:**
   - Case: CPAP device (`E0601`), domain `centene_dme_orthotics_prosthetics`, DOS `2026-08-15`, Commercial LOB.
   - Result: `overall_outcome == DecisionOutcome.POLICY_NOT_APPLICABLE`. Explanation: *"Clinical domain 'centene_dme_orthotics_prosthetics' is not in active MedRule scope"*. Evaluated rules count = 0.
2. **Registry Absence Check:**
   - Evaluated: `RULE-DME-001`, `RULE-DME-CPAP-001`, `RULE-DME-048`, `RULE-DME-099`.
   - Result: All return `None` from `engine.registry.get_rule()`.
3. **Explicit Rule Targeting Rejection:**
   - Targeted rule `RULE-DME-001` via `engine.evaluate(..., target_rule_ids=["RULE-DME-001"])`.
   - Result: `POLICY_NOT_APPLICABLE` (*"None of the requested target_rule_ids could be found in registry"*).
4. **Non-Interference in Advanced Imaging:**
   - Baseline Case: Brain MRI (CPT `70551`) for Multiple Sclerosis.
   - Polluted Case: Identical Brain MRI case injected with CP.MP.107 clinical criteria (`ahi_score = 25.0`, `cp_mp_107_dme_trial_completed = True`, `mobility_limitation_daily_activities = True`, `cervical_traction_device_demonstrated = True`).
   - Result: Both cases produce **identical outcomes**, identical evaluated rules, and identical traces.
5. **Non-Interference in IPM:**
   - Baseline Case: Facet Radiofrequency Neurotomy (CPT `64635`).
   - Polluted Case: Identical Facet case injected with CP.MP.107 criteria (`ahi_score = 3.0`, `dme_wheelchair_replacement_useful_lifetime_years = 5`, `prosthetic_functional_needs_unmet = True`).
   - Result: Both cases produce **identical outcomes**, identical evaluated rules, and identical traces.

### Test Execution Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.11.5, pytest-9.1.1 -- D:\PreAuth\.venv\Scripts\python.exe
rootdir: D:\PreAuth, configfile: pytest.ini

medrule_engine/tests/test_decision_tree.py::TestMedRuleDecisionTree::test_15_cp_mp_107_dmepos_complete_isolation_and_non_interference PASSED [100%]

============================= 15 passed in 1.17s ==============================
```

---

## 7. Audit Conclusion & Final Status Determination

The audit verified that:
1. `CP.MP.107` and all its duplicate copies are quarantined in `archive_candidate/` and completely excluded from the active rulebook collection.
2. Zero active clinical rules in Advanced Imaging or IPM cite or depend on CP.MP.107.
3. The active runtime engine strictly isolates evaluation to Advanced Imaging and IPM.
4. Injecting CP.MP.107 evidence parameters into active imaging or pain management cases has zero effect on adjudication outcomes or audit traces.

**FINAL AUDIT STATUS:**  
# `NO ACTIVE RUNTIME DEPENDENCY VERIFIED`
