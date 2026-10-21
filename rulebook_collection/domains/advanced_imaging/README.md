# Advanced Imaging Domain (Core Project Scope)

## Overview
The Advanced Imaging domain governs diagnostic CT, MRI, CTA, MRA, and PET/SPECT procedures in the MedRule clinical decision support system.

## Folder Organization
- `policies/current/`: Authoritative 2026 governing guidelines (1,041-page v2 guideline and EPOS 2067 Place of Service policy).
- `policies/historical/`: Historical 2025 guideline edition (1,074 pages) preserved for audit provenance.
- `supporting_documents/`:
  - `checklists/`: Documentation checklists for general prior authorization and Low Dose CT lung screening.
  - `forms/`: Conservative treatment history forms documenting physical therapy and medication trials.
  - `tip_sheets/`: Expedited review tip sheets and modality selection guidance.
- `rules/`: 114 deterministic clinical rules strictly validated against canonical schema.
  - `ct/`: CT Head/Brain, Chest, Spine, Abdomen/Pelvis, Extremities, Sinus/Maxillofacial, Temporal Bone.
  - `mri/`: MRI Brain, Spine, Extremities, TMJ, Orbit/Face/Neck.
  - `cta/`: CT Angiography Head, Neck, Chest, Abdomen, Pelvis, Extremity.
  - `mra/`: MR Angiography Head, Neck, Chest, Abdomen, Spinal Canal.
  - `pet_spect/`: PET/CT Oncologic, Brain, Myocardial, and SPECT.
  - `cross_cutting/`: Preamble, contrast safety, and place of service EPOS 2067.
- `manifests/`: Traceability matrix, guideline coverage inventory, completeness audits, and human review queue.

## Governance Invariant
Zero rules are approved. All 114 rules are maintained in `DRAFT` or `NEEDS_HUMAN_REVIEW` status.
