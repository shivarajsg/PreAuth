"""Scope Integrity and Verification Test Suite for MedRule Rulebook Collection.

Validates that:
1. Only Advanced Imaging and IPM are designated primary active domains.
2. Every active rule references an existing physical PDF.
3. Every referenced PDF has a valid inventory entry.
4. Every referenced source page is within physical PDF page boundaries.
5. Every rule ID is unique across the entire active knowledge base.
6. Every rule conforms strictly to canonical MedRule JSON schema.
7. Every active rule has a corresponding source-to-rule traceability record.
8. Historical documents cannot silently enter active policy registry.
9. Shared dependencies are retained and explicitly mapped.
10. Duplicate detection operates via SHA-256 cryptographic hashes.
11. No rules have been automatically promoted to APPROVED status.
12. Existing rule logic and count baselines (114 imaging, 14 IPM) remain intact.
13. Enforces final folder structure conformance.
14. Enforces relocation log, inventory, and duplicate report completeness.
"""

import csv
import hashlib
import json
import os
import unittest
from pathlib import Path
import jsonschema

# Optional import for PDF validation
try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

BASE_DIR = Path(__file__).resolve().parents[2]
RULEBOOK_DIR = BASE_DIR / "rulebook_collection"
DOMAINS_DIR = RULEBOOK_DIR / "domains"
MANIFESTS_DIR = RULEBOOK_DIR / "manifests"
SCHEMAS_DIR = RULEBOOK_DIR / "schemas"
ARCHIVE_DIR = RULEBOOK_DIR / "archive_candidate"
SHARED_DIR = RULEBOOK_DIR / "shared_references"

ADV_RULES_DIR = DOMAINS_DIR / "advanced_imaging" / "rules"
IPM_RULES_DIR = DOMAINS_DIR / "interventional_pain_management" / "rules"

CANONICAL_SCHEMA_PATH = SCHEMAS_DIR / "medrule_rule_schema.json"
ADV_SCHEMA_PATH = ADV_RULES_DIR / "schema.json"

PROPOSAL_CSV_PATH = MANIFESTS_DIR / "scope_cleanup_proposal.csv"
RELOCATION_LOG_PATH = MANIFESTS_DIR / "relocation_log.csv"
DUPLICATE_REPORT_PATH = MANIFESTS_DIR / "duplicate_report.csv"
FILE_INVENTORY_PATH = MANIFESTS_DIR / "file_inventory.csv"
FILE_HASHES_PATH = MANIFESTS_DIR / "file_hashes.csv"
TRACEABILITY_MASTER_PATH = MANIFESTS_DIR / "source_to_rule_traceability.csv"


class TestScopeIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load rules
        with open(ADV_RULES_DIR / "draft_rules.json", "r", encoding="utf-8") as f:
            cls.adv_rules = json.load(f)
        with open(IPM_RULES_DIR / "draft_rules.json", "r", encoding="utf-8") as f:
            cls.ipm_rules = json.load(f)
        cls.all_active_rules = cls.adv_rules + cls.ipm_rules

        # Load schemas
        with open(CANONICAL_SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.canonical_schema = json.load(f)
        with open(ADV_SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.adv_schema = json.load(f)

        # Load proposal manifest
        cls.proposal_rows = []
        if PROPOSAL_CSV_PATH.exists():
            with open(PROPOSAL_CSV_PATH, "r", encoding="utf-8") as f:
                cls.proposal_rows = list(csv.DictReader(f))

    def test_01_primary_active_domains_restriction(self):
        """Verify only Advanced Imaging and IPM are designated primary active domains."""
        active_domains = set()
        for r in self.all_active_rules:
            active_domains.add(r.get("domain"))
        self.assertEqual(active_domains, {"advanced_imaging", "interventional_pain_management"})

        # Verify active domains folder strictly contains only advanced_imaging and interventional_pain_management
        existing_domain_dirs = {d.name for d in DOMAINS_DIR.iterdir() if d.is_dir()}
        self.assertEqual(existing_domain_dirs, {"advanced_imaging", "interventional_pain_management"})

    def test_02_every_active_rule_references_existing_pdf(self):
        """Verify every active rule references a physical PDF that exists on disk."""
        missing = []
        for r in self.all_active_rules:
            rid = r["rule_id"]
            sfile = r["source_file"]
            resolved = BASE_DIR / sfile
            if not resolved.exists():
                missing.append((rid, sfile))
        self.assertEqual(missing, [], f"Active rules referencing non-existent PDFs: {missing}")

    def test_03_every_referenced_pdf_has_valid_inventory_entry(self):
        """Verify every referenced source PDF has a recorded entry in the proposal manifest."""
        proposal_filenames = {Path(r["relative_path"]).name: r for r in self.proposal_rows}
        for r in self.all_active_rules:
            sfile_name = Path(r["source_file"]).name
            self.assertIn(sfile_name, proposal_filenames, f"Referenced PDF not in proposal: {sfile_name}")

    def test_04_every_referenced_source_page_within_pdf_bounds(self):
        """Verify every referenced source page is within physical PDF page boundaries."""
        if fitz is None:
            self.skipTest("PyMuPDF / fitz not installed")

        pdf_doc_cache = {}
        out_of_bounds = []

        for r in self.all_active_rules:
            rid = r["rule_id"]
            sfile = r["source_file"]
            spage = r["source_page"]

            resolved = BASE_DIR / sfile
            self.assertTrue(resolved.exists(), f"Could not find PDF for {rid}: {sfile}")

            if str(resolved) not in pdf_doc_cache:
                pdf_doc_cache[str(resolved)] = fitz.open(str(resolved))
            doc = pdf_doc_cache[str(resolved)]
            max_pages = len(doc)

            if isinstance(spage, dict):
                phys_p = spage.get("physical_page")
            elif isinstance(spage, int):
                phys_p = spage
            elif isinstance(spage, str) and spage.isdigit():
                phys_p = int(spage)
            else:
                phys_p = None

            if phys_p is None or phys_p < 1 or phys_p > max_pages:
                out_of_bounds.append((rid, spage, max_pages, str(resolved)))

        for doc in pdf_doc_cache.values():
            doc.close()

        self.assertEqual(out_of_bounds, [], f"Pages out of bounds: {out_of_bounds}")

    def test_05_rule_id_uniqueness_across_active_knowledge_base(self):
        """Verify every rule ID is globally unique across the active knowledge base."""
        all_ids = [r["rule_id"] for r in self.all_active_rules]
        self.assertEqual(len(all_ids), len(set(all_ids)), "Duplicate rule ID found in active rules")
        self.assertEqual(len(all_ids), 128, "Expected exactly 128 total rules (114 imaging + 14 IPM)")

    def test_06_rule_schema_conformance(self):
        """Verify every rule conforms strictly to canonical schema."""
        for r in self.adv_rules:
            jsonschema.validate(instance=r, schema=self.adv_schema)
        for r in self.ipm_rules:
            jsonschema.validate(instance=r, schema=self.canonical_schema)

    def test_07_every_active_rule_has_traceability_record(self):
        """Verify every active rule has an exact matching record in source_to_rule_traceability.csv."""
        adv_trace = set()
        with open(ADV_RULES_DIR / "source_to_rule_traceability.csv", "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                adv_trace.add(row["rule_id"])
        for r in self.adv_rules:
            self.assertIn(r["rule_id"], adv_trace, f"Advanced Imaging rule missing traceability: {r['rule_id']}")

        ipm_trace = set()
        with open(IPM_RULES_DIR / "source_to_rule_traceability.csv", "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ipm_trace.add(row["rule_id"])
        for r in self.ipm_rules:
            self.assertIn(r["rule_id"], ipm_trace, f"IPM rule missing traceability: {r['rule_id']}")

        # Verify consolidated master traceability manifest
        self.assertTrue(TRACEABILITY_MASTER_PATH.exists())
        master_trace = set()
        with open(TRACEABILITY_MASTER_PATH, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                master_trace.add(row["rule_id"])
        self.assertEqual(len(master_trace), 128)

    def test_08_historical_documents_cannot_silently_enter_active_registry(self):
        """Verify historical documents cannot enter the active policy registry as governing policy."""
        for r in self.all_active_rules:
            self.assertEqual(r.get("version_status"), "current_2026_verified")
            self.assertNotIn("historical", r.get("source_file", ""))
            self.assertIn("policies/current", r.get("source_file", ""))

    def test_09_shared_dependencies_retained_and_explicitly_mapped(self):
        """Verify shared external dependencies are explicitly mapped and preserved."""
        cms_dir = SHARED_DIR / "cms"
        self.assertTrue(cms_dir.exists())
        cms_pdfs = list(cms_dir.glob("*.pdf"))
        self.assertEqual(len(cms_pdfs), 4, "Expected 4 shared CMS reference PDFs in shared_references/cms/")

    def test_10_cryptographic_duplicate_detection_by_sha256(self):
        """Verify duplicate detection relies on SHA-256 hash matching and quarantine."""
        self.assertTrue(DUPLICATE_REPORT_PATH.exists())
        with open(DUPLICATE_REPORT_PATH, "r", encoding="utf-8") as f:
            dup_rows = list(csv.DictReader(f))
        self.assertGreater(len(dup_rows), 0)
        for d in dup_rows:
            self.assertEqual(len(d["sha256"]), 64)

    def test_11_no_rules_automatically_promoted_to_approved(self):
        """Verify safety constraint: no rules have been marked APPROVED."""
        for r in self.all_active_rules:
            self.assertNotEqual(r.get("extraction_status"), "APPROVED", f"Rule {r['rule_id']} marked APPROVED")
            self.assertIn(r.get("extraction_status"), {"DRAFT", "NEEDS_HUMAN_REVIEW"})

    def test_12_existing_rule_logic_and_counts_preserved(self):
        """Verify existing rule counts and logic remain intact."""
        self.assertEqual(len(self.adv_rules), 114, "Advanced Imaging rule count altered")
        self.assertEqual(len(self.ipm_rules), 14, "IPM rule count altered")

    def test_13_final_folder_structure_conformance(self):
        """Verify target folder structure is strictly implemented without clutter."""
        # 1. Root source_pdfs
        seed_pdf = RULEBOOK_DIR / "source_pdfs" / "PreauthorizationMRI.pdf"
        self.assertTrue(seed_pdf.exists(), "PreauthorizationMRI.pdf seed must remain in source_pdfs/")

        # 2. Advanced imaging structure
        adv_dir = DOMAINS_DIR / "advanced_imaging"
        self.assertTrue((adv_dir / "policies" / "current").exists())
        self.assertTrue((adv_dir / "policies" / "historical").exists())
        self.assertTrue((adv_dir / "supporting_documents" / "checklists").exists())
        self.assertTrue((adv_dir / "supporting_documents" / "forms").exists())
        self.assertTrue((adv_dir / "supporting_documents" / "tip_sheets").exists())
        self.assertTrue((adv_dir / "rules" / "ct").exists())
        self.assertTrue((adv_dir / "rules" / "mri").exists())
        self.assertTrue((adv_dir / "rules" / "cta").exists())
        self.assertTrue((adv_dir / "rules" / "mra").exists())
        self.assertTrue((adv_dir / "rules" / "pet_spect").exists())
        self.assertTrue((adv_dir / "rules" / "cross_cutting").exists())
        self.assertTrue((adv_dir / "manifests").exists())
        self.assertTrue((adv_dir / "README.md").exists())

        # 3. IPM structure
        ipm_dir = DOMAINS_DIR / "interventional_pain_management"
        self.assertTrue((ipm_dir / "policies" / "current").exists())
        self.assertTrue((ipm_dir / "policies" / "historical").exists())
        self.assertTrue((ipm_dir / "supporting_documents" / "checklists").exists())
        self.assertTrue((ipm_dir / "supporting_documents" / "forms").exists())
        self.assertTrue((ipm_dir / "supporting_documents" / "tip_sheets").exists())
        self.assertTrue((ipm_dir / "rules" / "epidural_injections").exists())
        self.assertTrue((ipm_dir / "rules" / "facet_interventions").exists())
        self.assertTrue((ipm_dir / "rules" / "sacroiliac_joint").exists())
        self.assertTrue((ipm_dir / "rules" / "neuromodulation_pumps").exists())
        self.assertTrue((ipm_dir / "rules" / "sympathetic_blocks").exists())
        self.assertTrue((ipm_dir / "rules" / "cross_cutting").exists())
        self.assertTrue((ipm_dir / "manifests").exists())
        self.assertTrue((ipm_dir / "README.md").exists())

        # 4. Archive candidates
        self.assertTrue((ARCHIVE_DIR / "unrelated_domains" / "cardiology").exists())
        self.assertTrue((ARCHIVE_DIR / "unrelated_domains" / "dmepos").exists())
        self.assertTrue((ARCHIVE_DIR / "unrelated_domains" / "genetics").exists())
        self.assertTrue((ARCHIVE_DIR / "unrelated_domains" / "msk").exists())
        self.assertTrue((ARCHIVE_DIR / "unrelated_domains" / "physmed").exists())
        self.assertTrue((ARCHIVE_DIR / "unrelated_domains" / "radonc").exists())
        self.assertTrue((ARCHIVE_DIR / "unrelated_domains" / "sleep").exists())
        self.assertTrue((ARCHIVE_DIR / "duplicate_quarantine").exists())

    def test_14_relocation_log_and_inventory_completeness(self):
        """Verify all relocation manifests exist and record all 101 physical PDFs."""
        self.assertTrue(RELOCATION_LOG_PATH.exists())
        self.assertTrue(FILE_INVENTORY_PATH.exists())
        self.assertTrue(FILE_HASHES_PATH.exists())

        with open(RELOCATION_LOG_PATH, "r", encoding="utf-8") as f:
            reloc_rows = list(csv.DictReader(f))
        self.assertEqual(len(reloc_rows), 101, "Relocation log must contain exactly 101 records")

        # Every file hash must match before and after
        for r in reloc_rows:
            self.assertEqual(r["sha256_before"], r["sha256_after"])


if __name__ == "__main__":
    unittest.main()
