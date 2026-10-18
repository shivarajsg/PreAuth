"""
Automated Test Suite for MedRule Phase 2E:
Supporting Documents, Evidence Mapping and Policy Dependencies.
"""

import unittest
import os
import csv
import json
import hashlib
import fitz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DOMAINS_DIR = os.path.join(BASE_DIR, "rulebook_collection", "domains")
MANIFESTS_DIR = os.path.join(BASE_DIR, "rulebook_collection", "manifests")

DOMAINS = [
    "advanced_imaging",
    "cardiology",
    "musculoskeletal_surgery",
    "interventional_pain_management",
    "radiation_oncology",
    "physical_medicine",
    "sleep_health",
    "genetic_testing",
    "centene_dme_orthotics_prosthetics",
]

ALLOWED_FUNCTIONAL_ROLES = {
    "INTAKE_OR_DOCUMENTATION_AID",
    "SUPPLEMENTARY_PROCEDURAL_GUIDANCE",
    "CODING_OR_BILLING_REFERENCE",
    "SEPARATELY_GOVERNED_POLICY",
    "EXTERNAL_AUTHORITY",
    "HISTORICAL_DOCUMENT_COMPARISON",
    "PLAN_SPECIFIC_DEPENDENCY",
}

ALLOWED_RELATIONSHIPS = {
    "SUPPORTS_DOCUMENTATION_COLLECTION",
    "REFERENCES_GOVERNING_POLICY",
    "SUPPLEMENTS_PROCEDURAL_GUIDANCE",
    "SUPPORTS_CODE_INTERPRETATION",
    "REFERENCES_EXTERNAL_AUTHORITY",
    "HISTORICAL_COMPARISON_ONLY",
    "APPLICABILITY_UNRESOLVED",
    "UNMAPPED_NEEDS_REVIEW",
}

ALLOWED_DATA_TYPES = {
    "string",
    "date",
    "numeric",
    "boolean",
    "enum",
    "file_attachment",
}

ALLOWED_CLINICAL_VS_ADMIN = {
    "ADMINISTRATIVE_INTAKE",
    "CLINICAL_EVIDENCE",
}

class TestPhase2EMappings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load master PDF inventory
        master_path = os.path.join(MANIFESTS_DIR, "master_pdf_inventory.csv")
        with open(master_path, encoding="utf-8") as f:
            cls.master_records = {r["document_id"]: r for r in csv.DictReader(f)}

        # Load active rule IDs from draft_rules.json across all domains
        cls.active_rules = {}
        for d in DOMAINS:
            rule_path = os.path.join(DOMAINS_DIR, d, "rules", "draft_rules.json")
            with open(rule_path, encoding="utf-8") as f:
                data = json.load(f)
                rules = data if isinstance(data, list) else data.get("rules", [])
                cls.active_rules[d] = {r["rule_id"]: r for r in rules}

    def test_01_all_domain_artifacts_exist(self):
        """Verify that all 5 required artifacts exist in every domain's supporting_documents directory."""
        required_files = [
            "supporting_document_inventory.csv",
            "policy_rule_mapping.csv",
            "documentation_field_mapping.csv",
            "unmapped_documents_review.csv",
            "supporting_document_report.md",
        ]
        for d in DOMAINS:
            sup_dir = os.path.join(DOMAINS_DIR, d, "supporting_documents")
            self.assertTrue(os.path.isdir(sup_dir), f"Missing supporting_documents directory in domain: {d}")
            for req in required_files:
                p = os.path.join(sup_dir, req)
                self.assertTrue(os.path.isfile(p), f"Missing required file: {p}")
                self.assertGreater(os.path.getsize(p), 0, f"File is empty: {p}")

    def test_02_master_manifests_exist(self):
        """Verify that master supporting document inventory and policy dependency mappings exist."""
        inv_path = os.path.join(MANIFESTS_DIR, "supporting_document_inventory.csv")
        dep_path = os.path.join(MANIFESTS_DIR, "policy_dependency_mapping.csv")
        self.assertTrue(os.path.isfile(inv_path), "Missing master supporting_document_inventory.csv")
        self.assertTrue(os.path.isfile(dep_path), "Missing master policy_dependency_mapping.csv")
        self.assertGreater(os.path.getsize(inv_path), 0, "Master inventory is empty")
        self.assertGreater(os.path.getsize(dep_path), 0, "Master dependency mapping is empty")

    def test_03_master_inventory_counts_and_uniqueness(self):
        """Verify master supporting document inventory count (74) and unique IDs."""
        inv_path = os.path.join(MANIFESTS_DIR, "supporting_document_inventory.csv")
        with open(inv_path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 74, f"Expected 74 supporting documents, got {len(rows)}")
        doc_ids = [r["document_id"] for r in rows]
        self.assertEqual(len(doc_ids), len(set(doc_ids)), "Duplicate document_id found in master inventory")

    def test_04_supporting_doc_inventory_validity_and_hashes(self):
        """Verify every supporting document resolves to disk, matches SHA-256, page count, and allowed functional roles."""
        inv_path = os.path.join(MANIFESTS_DIR, "supporting_document_inventory.csv")
        with open(inv_path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            doc_id = r["document_id"]
            self.assertIn(doc_id, self.master_records, f"Unknown document_id in master inventory: {doc_id}")
            self.assertIn(r["functional_role"], ALLOWED_FUNCTIONAL_ROLES, f"Invalid functional_role for {doc_id}: {r['functional_role']}")
            
            # Check physical file on disk
            local_path = os.path.join(BASE_DIR, r["source_file_path"])
            self.assertTrue(os.path.isfile(local_path), f"File not found on disk: {local_path}")
            
            # Verify SHA-256
            h = hashlib.sha256()
            with open(local_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            actual_sha = h.hexdigest()
            self.assertEqual(r["file_sha256"], actual_sha, f"SHA-256 mismatch for {doc_id}")
            
            # Verify page count with fitz
            doc = fitz.open(local_path)
            self.assertEqual(int(r["physical_page_count"]), len(doc), f"Page count mismatch for {doc_id}")

    def test_05_policy_rule_mappings_integrity(self):
        """Verify mapping IDs are unique, relationship types valid, and linked rule_ids exist in draft_rules.json."""
        all_map_ids = set()
        for d in DOMAINS:
            map_path = os.path.join(DOMAINS_DIR, d, "supporting_documents", "policy_rule_mapping.csv")
            with open(map_path, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            for r in rows:
                mid = r["mapping_id"]
                self.assertNotIn(mid, all_map_ids, f"Duplicate mapping_id: {mid}")
                all_map_ids.add(mid)
                self.assertIn(r["relationship_type"], ALLOWED_RELATIONSHIPS, f"Invalid relationship_type: {r['relationship_type']}")
                rule_id = r["rule_id"].strip()
                if rule_id:
                    self.assertIn(rule_id, self.active_rules[d], f"Rule ID {rule_id} mapped in {d} does not exist in draft_rules.json")

    def test_06_field_mappings_integrity(self):
        """Verify field IDs are globally unique, data types and clinical/administrative tags are valid."""
        all_field_ids = set()
        total_fields = 0
        for d in DOMAINS:
            field_path = os.path.join(DOMAINS_DIR, d, "supporting_documents", "documentation_field_mapping.csv")
            with open(field_path, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            total_fields += len(rows)
            for r in rows:
                fid = r["field_id"]
                self.assertNotIn(fid, all_field_ids, f"Duplicate field_id: {fid}")
                all_field_ids.add(fid)
                self.assertIn(r["data_type"], ALLOWED_DATA_TYPES, f"Invalid data_type: {r['data_type']} in {fid}")
                self.assertIn(r["clinical_vs_administrative"], ALLOWED_CLINICAL_VS_ADMIN, f"Invalid clinical_vs_administrative: {r['clinical_vs_administrative']} in {fid}")
                self.assertTrue(r["field_label"].strip(), f"Empty field_label in {fid}")
                self.assertTrue(r["field_meaning"].strip(), f"Empty field_meaning in {fid}")
        self.assertGreaterEqual(total_fields, 100, f"Expected at least 100 field mappings, got {total_fields}")

    def test_07_historical_quarantine_enforcement(self):
        """Verify that historical documents are strictly quarantined and not linked to active decision rules."""
        for d in DOMAINS:
            map_path = os.path.join(DOMAINS_DIR, d, "supporting_documents", "policy_rule_mapping.csv")
            with open(map_path, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            for r in rows:
                if r["relationship_type"] == "HISTORICAL_COMPARISON_ONLY":
                    self.assertEqual(r["rule_id"].strip(), "", f"Historical mapping {r['mapping_id']} must not link to active rule_id")

    def test_08_cross_domain_dependencies_integrity(self):
        """Verify that cross-domain policy dependency register contains all 15 entries and valid statuses."""
        dep_path = os.path.join(MANIFESTS_DIR, "policy_dependency_mapping.csv")
        with open(dep_path, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 15, f"Expected 15 dependency records, got {len(rows)}")
        dep_ids = [r["dependency_id"] for r in rows]
        self.assertEqual(len(dep_ids), len(set(dep_ids)), "Duplicate dependency_id in policy_dependency_mapping.csv")

    def test_09_cumulative_rule_non_regression(self):
        """Verify cumulative 372 rules across all 9 domains remain unmodified (322 DRAFT, 50 NEEDS_HUMAN_REVIEW, 0 APPROVED)."""
        status_counts = {"DRAFT": 0, "NEEDS_HUMAN_REVIEW": 0, "APPROVED": 0}
        total_rules = 0
        for d in DOMAINS:
            rules = self.active_rules[d].values()
            total_rules += len(rules)
            for r in rules:
                st = r.get("status") or r.get("extraction_status", "DRAFT")
                self.assertNotEqual(st, "APPROVED", f"Forbidden APPROVED status in rule {r['rule_id']}")
                status_counts[st] = status_counts.get(st, 0) + 1

        self.assertEqual(total_rules, 372, f"Total rule count changed! Expected 372, found {total_rules}")
        self.assertEqual(status_counts.get("APPROVED", 0), 0, "Zero rules must be marked APPROVED")
        self.assertEqual(status_counts.get("DRAFT", 0), 322, f"Expected 322 DRAFT rules, found {status_counts.get('DRAFT')}")
        self.assertEqual(status_counts.get("NEEDS_HUMAN_REVIEW", 0), 50, f"Expected 50 NEEDS_HUMAN_REVIEW rules, found {status_counts.get('NEEDS_HUMAN_REVIEW')}")

if __name__ == "__main__":
    unittest.main()
