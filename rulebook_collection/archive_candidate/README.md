# MedRule Archive Candidate Repository

This directory contains documents and domain artifacts segregated from the active MedRule collection during the Two-Domain Scope Realignment (October 2026).

## Contents
1. `unrelated_domains/`:
   Clinical policies and rule files from domains outside the narrowed scope (Advanced Imaging & IPM only):
   - `cardiology/`
   - `dmepos/` (Centene DMEPOS)
   - `genetics/` (Genetic Testing)
   - `msk/` (Musculoskeletal Surgery)
   - `physmed/` (Physical Medicine)
   - `radonc/` (Radiation Oncology)
   - `sleep/` (Sleep Health)
2. `duplicate_quarantine/`:
   Cryptographic duplicates segregated to eliminate redundancy while preserving original file hashes:
   - `downloaded_pdfs/`: 13 raw Phase 1 download replicas.
   - `source_pdfs/`: Redundant seed replica `CP.MP.107(4).pdf`.
3. `superseded_or_unresolved/`:
   Files with pending review or superseded status.

All relocations are recorded in `rulebook_collection/manifests/relocation_log.csv` and can be reversed if required.
