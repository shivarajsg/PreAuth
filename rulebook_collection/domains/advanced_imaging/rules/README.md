# Advanced Imaging — Rule Schema Specification & Extraction Foundation

This directory houses the foundational extraction artifacts for MedRule Phase 2A, including the reusable rule schema ([`schema.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/advanced_imaging/rules/schema.json)), the representative draft rules pilot ([`draft_rules.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/advanced_imaging/rules/draft_rules.json)), and complete traceability and audit records.

---

## 1. Schema Architecture Overview

The MedRule rule schema is a versioned, deterministic data contract designed to capture clinical prior-authorization guidelines across all nine domains without loss of semantic fidelity, logical nuances, or clinical uncertainty.

The formal schema definition is located in [`schema.json`](file:///c:/Users/KumarShiva/Downloads/PreAuth/rulebook_collection/domains/advanced_imaging/rules/schema.json).

### Core Schema Fields

| Field Name | Type | Description | Required | Controlled Values |
| :--- | :---: | :--- | :---: | :--- |
| `rule_id` | String | Stable, globally unique rule identifier | Yes | Pattern: `^RULE-[A-Z0-9]+-[A-Z0-9_]+-[0-9]{3,}$` |
| `domain` | String | Clinical specialty domain | Yes | `advanced_imaging`, `cardiology`, `musculoskeletal_surgery`, `interventional_pain_management`, `radiation_oncology`, `physical_medicine`, `sleep_health`, `genetic_testing`, `centene_dme_orthotics_prosthetics`, `cross_domain_references` |
| `document_type` | String | Role of source document | Yes | `governing_policy`, `supplementary_policy`, `coding_grid`, `checklist`, `form`, `tip_sheet`, `external_reference`, `other` |
| `policy_title` | String | Official title of source policy | Yes | Unrestricted string matching manifest |
| `policy_version` | String | Published edition / revision date | Yes | Unrestricted string matching manifest |
| `version_status` | String | Temporal and governance state | Yes | `current_2026_verified`, `historical`, `superseded`, `future_preview`, `unverified` |
| `source_file` | String | Relative path to source PDF | Yes | Verified path relative to workspace root |
| `source_url` | String | Official publisher URL | No | Valid URI |
| `source_page` | Object | Physical & printed page location | Yes | `physical_page` (int >= 1), `printed_page` (string) |
| `source_section` | String | Heading / subsection title | Yes | Section title |
| `source_quote` | String | Verbatim supporting excerpt | Yes | Unaltered text extracted from cited page |
| `clinical_service_or_procedure` | String | Imaging study or test governed | Yes | e.g. "Abdomen and Pelvis CT", "Brain MRI" |
| `rule_type` | String | Structural criterion pattern | Yes | `clinical_prerequisite`, `clinical_indication`, `documentation_requirement`, `exclusion_criterion`, `temporal_threshold`, `conditional_modality_selection`, `administrative_prerequisite`, `coding_rule`, `other` |
| `conditions` | Object | Structured boolean / relational tree | Yes | `operator` (`ALL_OF`, `ANY_OF`, `NONE_OF`, `SINGLE_CONDITION`), `criteria` array |
| `required_documentation` | Array | Required clinical notes / reports | No | Array of documentation strings |
| `exclusion_conditions` | Array | Disqualifiers / contraindications | No | Array of exclusion strings |
| `decision_effect` | String | Explicit policy effect | Yes | `INDICATED`, `NOT_INDICATED`, `ALTERNATIVE_MODALITY_RECOMMENDED`, `DOCUMENTATION_DEFICIENT`, `PAYS_AS_CLAIM_EDIT`, `CONTINGENT_ON_APPEAL`, `UNDETERMINED` |
| `missing_information_behavior` | String | Engine behavior when data absent | Yes | `PEND_FOR_DOCUMENTATION`, `CANNOT_DETERMINE`, `FAIL_CONDITION`, `ASSUME_ABSENT`, `ESCALATE_TO_PEER_REVIEW` |
| `dependencies` | Array | Cross-referenced policies / grids | No | Array of policy references |
| `human_review_required` | Boolean | Clinical discretion / ambiguity flag | Yes | `true` or `false` |
| `extraction_status` | String | Governance review state | Yes | `DRAFT`, `NEEDS_HUMAN_REVIEW`, `APPROVED` |
| `review_notes` | String | Clinical reviewer notes | No | Detailed commentary explaining caveats |

---

## 2. Condition Logic & Boolean Modeling

The `conditions` object represents complex clinical logic as an explicit, nested Boolean tree without distorting medical intent:

### Logical Operators
- `ALL_OF`: All listed criteria must be satisfied simultaneously (Logical AND).
- `ANY_OF`: At least one listed criterion must be satisfied (Logical OR).
- `NONE_OF`: None of the listed criteria may be satisfied (Logical NOT / Exclusion).
- `SINGLE_CONDITION`: Exactly one atomic condition is evaluated.

### Relational Comparators
Individual criteria within the `criteria` array use controlled comparators:
- `EQUALS`, `NOT_EQUALS`
- `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`
- `LESS_THAN`, `LESS_THAN_OR_EQUAL`
- `BETWEEN` (inclusive numerical interval)
- `CONTAINS`, `NOT_CONTAINS`
- `IS_PRESENT`, `IS_ABSENT`
- `DOCUMENTED_FAILURE` (e.g. failure of conservative therapy trial)
- `CONTRAINDICATED` (e.g. MRI contraindicated in patient with non-conditional pacemaker)

### Recursive Sub-conditions
When a criterion contains nested logic (e.g., "Condition A AND (Condition B OR Condition C)"), the atomic criterion incorporates a `sub_conditions` block, allowing arbitrary tree depth while maintaining readability.

---

## 3. Human Review & Governance Lifecycle

To preserve safety and auditability, MedRule enforces a strict state machine for `extraction_status`:
1. `DRAFT`: Criterion has been extracted from the source PDF and validated against `schema.json`. It has not yet undergone medical review.
2. `NEEDS_HUMAN_REVIEW`: Criterion involves clinical judgment, ambiguous phrasing, conflicting guidance, or an unresolved dependency. It is enqueued in `human_review_queue.csv`.
3. `APPROVED`: Criterion has been manually reviewed and accepted by a credentialed clinician or authorized reviewer.

> [!IMPORTANT]
> **No automated script, validation test, or parser is permitted to set `extraction_status` to `APPROVED`.** All newly extracted criteria must be initialized as `DRAFT` or `NEEDS_HUMAN_REVIEW`.

---

## 4. Policy Semantics & Uncertainty Principles

1. **Information Absence $\neq$ Failure:** Missing clinical documentation results in `PEND_FOR_DOCUMENTATION`, not an automatic adverse medical necessity determination.
2. **Hierarchy of Sources:** Checklists and tip sheets do not override governing clinical guidelines.
3. **No Cross-Version Contamination:** Superseded historical editions (e.g., 2025 guidelines) are preserved for version diffing but never contribute active rules to the 2026 rule set.
4. **Unresolved Dependencies:** When an external dependency (such as a state Medicaid custom fee schedule or private health plan waiver grid) is inaccessible, it is recorded as an unresolved dependency, not assumed.
5. **Faithful Quotations:** Every rule includes a verbatim `source_quote` matching the exact text on the cited physical page.
