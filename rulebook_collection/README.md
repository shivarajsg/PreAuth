# MedRule Rulebook Collection

The authoritative, deterministic clinical knowledge base for pre-authorization decision support.

## Project Scope
The MedRule active rulebook collection focuses strictly on two core clinical domains:
1. **Advanced Imaging** (Diagnostic CT, MRI, CTA, MRA, PET/SPECT)
2. **Interventional Pain Management (IPM)** (ESIs, Facet Interventions, SI Joint, SCS, Intrathecal Pumps, Sympathetic Blocks)

## Structure
- `source_pdfs/`: Authoritative project seed document (`PreauthorizationMRI.pdf`) defining scope boundaries.
- `domains/`:
  - `advanced_imaging/`: 114 active clinical rules, 2026 governing policies, and supporting documents.
  - `interventional_pain_management/`: 14 active clinical rules, 2026 governing policies, and supporting documents.
- `shared_references/`: Shared regulatory authorities (CMS claims manuals, state ops, quality standards).
- `manifests/`:
  - `scope_cleanup_proposal.csv`: Master proposal manifest.
  - `scope_completeness_report.md`: Initial audit and completeness report.
  - `file_inventory.csv`: Pre-cleanup inventory of all 101 physical PDFs.
  - `file_hashes.csv`: SHA-256 cryptographic verification hashes.
  - `relocation_log.csv`: Reversible audit log of every file relocation.
  - `duplicate_report.csv`: Cryptographic duplicate tracking report.
  - `source_to_rule_traceability.csv`: Consolidated 128-rule source traceability.
  - `cleanup_validation_report.md`: Final post-cleanup execution and verification report.
- `archive_candidate/`:
  - `unrelated_domains/`: Relocated guidelines from 7 non-core domains (Cardiology, DMEPOS, Genetics, MSK, PhysMed, RadOnc, Sleep).
  - `duplicate_quarantine/`: Redundant identical PDF copies (raw Phase 1 downloads and duplicate seed).
- `tests/`: Scope boundary, citation validity, and integrity test suites.
