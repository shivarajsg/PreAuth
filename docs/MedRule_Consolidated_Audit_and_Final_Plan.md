# MedRule — Consolidated Audit and Final Plan

**Purpose:** One shared plan to stabilize MedRule, verify what works, fix confirmed defects, and prepare for a safe UI.

**Evidence note:** This plan is based on reports shared in chat. Their claims are not independently verified here. Treat them as reported until reproduced from actual files and command output.

## 1. Product goal

MedRule is intended to be a deterministic, policy-based prior-authorization decision-support prototype. It should take a doctor's note or structured case, extract documented facts without inventing information, select the applicable policy, evaluate source-grounded criteria, explain `MET`, `NOT_MET`, `INSUFFICIENT_DATA`, and `NOT_APPLICABLE`, and provide traceable evidence and citations.

The intended active scope is **Advanced Imaging** and **Interventional Pain Management (IPM)** only. It is not a binding authorization system.

## 2. Intended policy sources

Verify filenames, locations, content, version, and applicability in the repository.

**Advanced Imaging**
- `2026 Evolent Clinical Guidelines - Advanced Imaging v2.pdf`
- `EPOS 2067 for Place of Service - Radiology 2026_final.pdf`

**IPM**
- `2026 Evolent Interventional Pain Management Guidelines.pdf`
- `EPOS 1755 for Place of Service - Interventional Pain Management 2026_final.pdf`

`CP.MP.107` (DMEPOS) must remain excluded from active decision logic. Do not restore other clinical domains just to satisfy legacy tests unless the owner explicitly expands scope.

## 3. Audit findings reported so far (not independently verified)

- Repository: `C:\Users\KumarShiva\Downloads\PreAuth`; branch `main`; commit `086d286`.
- 128 active rule definitions reportedly exist: 114 Advanced Imaging and 14 IPM.
- Rule files reportedly contain 121 `DRAFT`, 7 `NEEDS_HUMAN_REVIEW`, and 0 `APPROVED`.
- Governance database reportedly contains 372 rule-state records: 322 `DRAFT`, 50 `NEEDS_HUMAN_REVIEW`, 0 `APPROVED`. The discrepancy with the 128 active rules needs investigation.
- Seven additional domain rulebooks are reportedly absent. These may be intentionally out of scope; do not restore them automatically.
- Test collection reportedly fails with 10 import errors: 8 for `jsonschema`, 2 for `pymupdf`; zero tests ran in that attempt.
- The documentation claim of 252 passing tests is unverified.
- The project reportedly contains a Python/Flask engine, router, rule registry, PDF extractor, SQLite governance store, CLI, UI/templates, mock connectors, and pilot benchmark.
- OCR for image-only PDFs is reportedly missing.
- CPT-to-rule matching reportedly relies partly on keyword matching.
- Reviewer identity may be spoofable via a parameter such as `?as_user=USR-MD-01`; CSRF protection is reportedly absent.
- UI behavior has not been verified end-to-end in a browser.
- Manual extraction checks reportedly found provider-name, negation, treatment-modality aggregation, symptom-duration, and examination-finding defects.
- Earlier policy audits reportedly covered 43 partially verified rules and 204 gap records. Gap records do not necessarily equal distinct missing rules.
- The “45% complete” estimate is subjective and must not be used as an acceptance metric.

## 4. Non-negotiable safeguards

1. No automatic rule approval; keep the seven governance-blocked rules blocked.
2. All outputs remain non-binding; submission and live integrations stay disabled.
3. Never fabricate clinical facts or policy criteria.
4. Missing documentation is not proof of a negative finding.
5. Preserve explicit negative, missing, ambiguous, and conflicting evidence separately.
6. Do not select policies based only on keyword similarity.
7. Keep Clinical Necessity and Place of Service separate.
8. Do not use historical policies as silent fallbacks.
9. Keep CP.MP.107 excluded.
10. Do not weaken tests just to make them pass.
11. Back up and inspect before destructive file or database changes.
12. Use synthetic/de-identified test data only.

## 5. Final phased plan

Execute one phase at a time. Each phase must produce a short report, actual test evidence where relevant, and stop for review.

### Phase 0 — Read-only baseline
- Confirm repository root, branch, commit, and `git status`.
- List staged, modified, untracked, and relevant ignored files.
- Verify presence of the two active rulebooks and four policy PDFs.
- Identify Python versions, virtual environments, dependency manifests, test configuration, reports, databases, and `.gitignore` behavior.
- Do not install, edit, reset, clean, stash, or delete anything.

**Deliverable:** `reports/phase_00_baseline.md`

### Phase 1 — Reproducible environment
- Inspect dependency files and documented Python compatibility.
- Use a project-local virtual environment and install dependencies there only after confirming the right Python version.
- Record exact commands and package versions; verify required imports.
- Do not alter clinical logic.

**Deliverable:** `reports/phase_01_environment.md`

### Phase 2 — Reproduce test failures
- Run collection and the full suite.
- Capture exact tracebacks and categorize environment errors, genuine regressions, stale fixtures, obsolete domain expectations, database-state dependencies, or unresolved failures.
- Do not claim failures are pre-existing without baseline evidence or weaken assertions.

**Deliverable:** `reports/phase_02_test_baseline.md`

### Phase 3 — Reconcile rules and governance database
- Verify rule IDs and statuses from active JSON files.
- Inspect DB schema, history, foreign keys, migrations, and timestamps.
- Explain the 128-rule versus 372-record discrepancy and identify the runtime source of truth.
- Preserve historical audit records unless a reviewed migration plan says otherwise.
- Determine whether missing domain files are intentionally out of scope.

**Deliverable:** `reports/phase_03_rulebook_database_reconciliation.md`

### Phase 4 — Correct obsolete tests and documentation
- Update only tests that conflict with the intended two-domain scope, preserving meaningful safety assertions.
- Correct health endpoints and documentation to reflect actual active domains/rule counts.
- Do not restore out-of-scope domains just to satisfy old benchmark counts.

**Deliverable:** `reports/phase_04_scope_and_test_fixes.md`

### Phase 5 — Fix extraction defects
Investigate the reported provider-name, negation-scope, modality aggregation, symptom-duration, structured examination, and red-flag uncertainty issues against actual source text and code. Fix only reproducible defects; avoid document-specific hardcoding. Add synthetic tests for positive, explicit negative, missing, ambiguous, conflicting, durations, units, and multiple findings. If OCR is absent, report scanned documents as unreadable/OCR-required rather than implying successful extraction.

**Deliverables:** `reports/phase_05_extraction_findings.md`, `reports/phase_05_extraction_validation.md`

### Phase 6 — Validate policy routing and procedure matching
Verify routing by domain, procedure/CPT, line of business, date of service, policy version, and POS. Test supported and unsupported procedures, malformed codes, missing LOB, and old service dates. Do not send unsupported procedures to a merely similar rule.

**Deliverable:** `reports/phase_06_routing_validation.md`

### Phase 7 — Validate logic, citations, and aggregation
Test `ALL_OF`, `ANY_OF`, `NONE_OF`, comparators, TRUE/FALSE/UNKNOWN, all criterion states, contradictions, and the effect of unresolved mandatory red-flag checks. Verify citations point to the relevant policy text. Reconcile the 43 audited rules and 204 gap records, separating duplicates, advisory items, shared criteria, real omissions, and ambiguous language. Do not automatically implement or approve clinical criteria.

**Deliverables:** `reports/phase_07_policy_logic_validation.md`, `reports/phase_07_human_review_queue.md`

### Phase 8 — Secure the web application
Before privileged review workflows are exposed, verify server-side authentication and RBAC. Remove trust in client-controlled `as_user` parameters. Add CSRF protection for state-changing routes, verify session security, and test unauthenticated access and role escalation. Audit identity must come from the authenticated server-side session.

**Deliverable:** `reports/phase_08_security_review.md`

### Phase 9 — Decide document/OCR support
Decide whether scanned PDFs are in the initial scope. If OCR is needed, evaluate local options, privacy, dependencies, accuracy, and failure modes before implementation. Preserve page provenance and mark uncertain OCR output for review. Otherwise clearly document and safely reject unsupported scans.

**Deliverable:** `reports/phase_09_document_support_decision.md`

### Phase 10 — UI readiness
Only after relevant backend, routing, extraction, provenance, and security checks pass, design a UI for upload, extracted-fact review, criterion-by-criterion outcomes, citations, separate Clinical Necessity/POS results, unresolved items, and a non-binding disclaimer.

**Deliverable:** `reports/phase_10_ui_readiness_and_design.md`; implementation requires a separate go-ahead.

## 6. Additional items to track

- Policy PDFs and synthetic fixtures: verify whether tracked, external, or ignored; do not commit sensitive or unrelated files just to pass tests.
- Health endpoint and documentation must report actual supported domains and counts.
- Database migrations must preserve audit history.
- Verify append-only audit behavior and hash-chain checks without overstating tamper-proof guarantees.
- Distinguish invalid input, unreadable document, unsupported procedure, missing policy, insufficient evidence, and internal errors.
- Keep policy effective dates explicit and prevent silent historical fallback.
- Record exact commands, environment, pass/fail counts, files changed, and report paths for each phase.
- Human clinical/policy review is required for unresolved interpretation and criteria; tests alone do not establish clinical correctness, policy completeness, regulatory compliance, or production readiness.

## 7. Global acceptance criteria

For a controlled, non-binding demonstration:
- The app runs in a documented environment.
- The intended test suite executes and failures are resolved or explicitly isolated.
- Only the two intended domains are active.
- Rule counts and statuses agree with the documented source of truth.
- Seven blocked rules remain blocked; no automatic approvals occur.
- Missing facts remain insufficient rather than silently false.
- Extraction preserves source meaning and flags uncertainty.
- Routing, selected rule IDs, and policy citations are validated.
- Clinical Necessity and POS are separately evaluated.
- Authentication and authorization protect privileged review functions.
- Submission/live integrations remain disabled.
- Unresolved policy gaps are disclosed and queued for human review.

## 8. Working protocol

For each phase: inspect first; report findings; get approval before destructive, clinical, governance, database, or security-sensitive changes; make the smallest reversible change; run focused tests then relevant regression tests; report actual output and files changed; stop for review before the next phase. Do not bundle multiple phases into one task.

## 9. Immediate next action — Phase 0 only

Create `reports/phase_00_baseline.md` with the actual repository path, branch, commit, Git status, changed/untracked files, presence of the two rulebooks and four PDFs, Python/venv/dependency/test setup, existing reports/databases, and discrepancies from this plan.

**Read-only only:** do not install packages, edit files, clean the tree, reset Git, delete DB records, restore domains, modify rules, or approve anything. Stop after the report and review it before Phase 1.
