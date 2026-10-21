# Interventional Pain Management (IPM) Domain (Core Project Scope)

## Overview
The Interventional Pain Management (IPM) domain governs interventional pain procedures in the MedRule clinical decision support system.

## Folder Organization
- `policies/current/`: Authoritative 2026 governing guideline (102 pages) and EPOS 1755 Place of Service policy.
- `policies/historical/`: Historical 2025 guideline edition (75 pages) preserved for audit provenance.
- `supporting_documents/`:
  - `checklists/`: Mandatory documentation submission checklists.
  - `forms/`: Conservative treatment history forms (Rev 08/07/2025) documenting PT/OT, medications, and duration.
  - `tip_sheets/`: Injection intervals and diagnostic block relief thresholds.
- `rules/`: 14 deterministic clinical rules strictly validated against canonical schema.
  - `epidural_injections/`: Cervical, thoracic, and lumbar interlaminar/transforaminal ESIs.
  - `facet_interventions/`: Diagnostic medial branch blocks and radiofrequency facet neurotomy.
  - `sacroiliac_joint/`: Diagnostic and therapeutic SI joint injections.
  - `neuromodulation_pumps/`: Spinal cord stimulation trial/implantation and intrathecal drug delivery systems.
  - `sympathetic_blocks/`: Stellate ganglion, lumbar sympathetic, and celiac plexus blocks.
  - `cross_cutting/`: General conservative therapy requirements and place of service EPOS 1755.
- `manifests/`: Traceability matrix, guideline coverage inventory, and human review queue.

## Governance Invariant
Zero rules are approved. All 14 rules are maintained in `DRAFT` or `NEEDS_HUMAN_REVIEW` status.
