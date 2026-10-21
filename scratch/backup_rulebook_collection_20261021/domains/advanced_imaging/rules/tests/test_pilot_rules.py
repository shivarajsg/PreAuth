"""Automated deterministic quality test suite for MedRule Phase 2A Advanced Imaging Pilot Rules.
Verifies all 10 deterministic quality check requirements specified in Section 9.
"""
import re
import csv
import json
import unittest
from pathlib import Path
import fitz
import jsonschema

BASE_DIR = Path(__file__).resolve().parents[5]
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
MANIFESTS_DIR = BASE_DIR / "rulebook_collection" / "manifests"

@unittest.skip("Historical Phase 2A test suite superseded by test_phase2b_rules.py")
class TestPilotRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema_path = RULES_DIR / "schema.json"
        cls.rules_path = RULES_DIR / "draft_rules.json"
        cls.traceability_path = RULES_DIR / "source_to_rule_traceability.csv"
        cls.queue_path = RULES_DIR / "human_review_queue.csv"
        cls.master_inventory_path = MANIFESTS_DIR / "master_pdf_inventory.csv"

        with open(cls.schema_path, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)

        with open(cls.rules_path, "r", encoding="utf-8") as f:
            cls.rules = json.load(f)

        cls.pdf_cache = {}

    @classmethod
    def tearDownClass(cls):
        for doc in cls.pdf_cache.values():
            doc.close()

    def get_pdf(self, path_str):
        full_path = (BASE_DIR / path_str).resolve()
        if str(full_path) not in self.pdf_cache:
            self.assertTrue(full_path.exists(), f"PDF not found: {full_path}")
            self.pdf_cache[str(full_path)] = fitz.open(str(full_path))
        return self.pdf_cache[str(full_path)]

    def normalize_text(self, text):
        """Normalize whitespace, non-breaking spaces, and quotes for deterministic matching."""
        if not text:
            return ""
        text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
        return re.sub(r"\s+", " ", text).strip().lower()

    def test_01_unique_rule_ids_and_format(self):
        """Check 1: Every rule has a unique rule_id conforming to the naming pattern."""
        rule_ids = set()
        pattern = re.compile(r"^RULE-[A-Z0-9]+-[A-Z0-9_]+-[0-9]{3,}$")
        for r in self.rules:
            rid = r.get("rule_id", "")
            self.assertTrue(rid, "Rule missing rule_id")
            self.assertNotIn(rid, rule_ids, f"Duplicate rule_id found: {rid}")
            self.assertTrue(pattern.match(rid), f"rule_id {rid} does not match naming pattern")
            rule_ids.add(rid)
        self.assertEqual(len(self.rules), 16, "Expected exactly 16 pilot rules")

    def test_02_schema_validation(self):
        """Check 2: Every rule validates against schema.json."""
        for r in self.rules:
            try:
                jsonschema.validate(instance=r, schema=self.schema)
            except jsonschema.ValidationError as e:
                self.fail(f"Rule {r.get('rule_id')} failed schema validation: {e.message}")

    def test_03_cited_pdf_files_exist(self):
        """Check 3: Every cited source PDF file exists at the specified path."""
        for r in self.rules:
            src = r.get("source_file", "")
            self.assertTrue(src, f"Rule {r.get('rule_id')} missing source_file")
            pdf_path = (BASE_DIR / src).resolve()
            self.assertTrue(pdf_path.exists(), f"Source file does not exist: {pdf_path}")

    def test_04_cited_page_numbers_within_bounds(self):
        """Check 4: Every cited page number is within the valid page range of that PDF."""
        for r in self.rules:
            src = r["source_file"]
            doc = self.get_pdf(src)
            max_pages = len(doc)
            page_info = r.get("source_page", {})
            phys_page = page_info.get("physical_page") if isinstance(page_info, dict) else page_info
            self.assertIsInstance(phys_page, int, f"Physical page must be int in {r.get('rule_id')}")
            self.assertTrue(
                1 <= phys_page <= max_pages,
                f"Page {phys_page} out of bounds for {src} (1-{max_pages}) in {r.get('rule_id')}"
            )

    def test_05_verbatim_quote_presence_on_cited_page(self):
        """Check 5: Every source_quote exists verbatim in the extracted text of the cited page (allowing whitespace normalization)."""
        mismatches = []
        for r in self.rules:
            rid = r["rule_id"]
            src = r["source_file"]
            page_info = r.get("source_page", {})
            phys_page = page_info.get("physical_page") if isinstance(page_info, dict) else page_info
            doc = self.get_pdf(src)
            page_text = doc[phys_page - 1].get_text("text")

            norm_page = self.normalize_text(page_text)
            norm_quote = self.normalize_text(r.get("source_quote", ""))

            if norm_quote not in norm_page:
                mismatches.append((rid, phys_page, norm_quote[:60]))

        self.assertEqual(len(mismatches), 0, f"Source quote mismatches: {mismatches}")

    def test_06_policy_version_and_document_type_match_inventory(self):
        """Check 6: Every policy_version and document_type matches the master PDF inventory."""
        with open(self.master_inventory_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            inventory = {Path(row["local_relative_path"]).name: row for row in reader if row.get("local_relative_path")}

        for r in self.rules:
            src = r["source_file"]
            fname = Path(src).name
            self.assertIn(fname, inventory, f"File {fname} not found in master_pdf_inventory.csv")
            inv_row = inventory[fname]
            self.assertEqual(
                r.get("document_type"),
                inv_row["document_type"],
                f"Document type mismatch for {fname} in {r.get('rule_id')}"
            )
            self.assertEqual(
                r.get("policy_version"),
                inv_row["edition_or_version"],
                f"Policy version mismatch for {fname} in {r.get('rule_id')}"
            )

    def test_07_no_rule_is_approved(self):
        """Check 7: No rule has extraction_status: 'APPROVED'."""
        for r in self.rules:
            rid = r.get("rule_id")
            status = r.get("extraction_status")
            self.assertNotEqual(status, "APPROVED", f"Rule {rid} must not be marked APPROVED before clinical review")
            self.assertIn(status, ["DRAFT", "NEEDS_HUMAN_REVIEW"], f"Invalid extraction status {status} in {rid}")

    def test_08_condition_group_non_empty(self):
        """Check 8: Every condition group has at least one condition."""
        def check_conditions(cond_group, rid):
            criteria = cond_group.get("criteria", [])
            sub_conds = cond_group.get("sub_conditions", [])
            total_elements = len(criteria) + (len(sub_conds) if isinstance(sub_conds, list) else 1 if sub_conds else 0)
            self.assertGreater(total_elements, 0, f"Condition group in {rid} is empty")
            if isinstance(sub_conds, list):
                for sub in sub_conds:
                    check_conditions(sub, rid)
            elif isinstance(sub_conds, dict):
                check_conditions(sub_conds, rid)

        for r in self.rules:
            rid = r.get("rule_id")
            conds = r.get("conditions", {})
            check_conditions(conds, rid)

    def test_09_nested_condition_tree_validity(self):
        """Check 9: Every nested condition tree has valid logic operators and terminating conditions."""
        valid_ops = {"ALL_OF", "ANY_OF", "NONE_OF", "SINGLE_CONDITION"}
        valid_comparators = {
            "EQUALS", "NOT_EQUALS", "GREATER_THAN", "GREATER_THAN_OR_EQUAL",
            "LESS_THAN", "LESS_THAN_OR_EQUAL", "BETWEEN", "CONTAINS",
            "NOT_CONTAINS", "IS_PRESENT", "IS_ABSENT", "DOCUMENTED_FAILURE",
            "CONTRAINDICATED"
        }

        def validate_node(node, rid):
            op = node.get("operator")
            self.assertIn(op, valid_ops, f"Invalid operator {op} in {rid}")
            for crit in node.get("criteria", []):
                self.assertIn("condition_id", crit, f"Missing condition_id in {rid}")
                self.assertIn("description", crit, f"Missing description in {rid}")
                if "comparator" in crit:
                    comp = crit["comparator"]
                    self.assertIn(comp, valid_comparators, f"Invalid comparator {comp} in {rid}")
                if "sub_conditions" in crit and crit["sub_conditions"]:
                    validate_node(crit["sub_conditions"], rid)

            sub_conditions = node.get("sub_conditions")
            if isinstance(sub_conditions, list):
                for sub in sub_conditions:
                    validate_node(sub, rid)
            elif isinstance(sub_conditions, dict):
                validate_node(sub_conditions, rid)

        for r in self.rules:
            rid = r.get("rule_id")
            validate_node(r.get("conditions", {}), rid)

    def test_10_inventory_count_consistency(self):
        """Check 10: Count of extracted rules matches traceability rows and pilot target (10-20)."""
        self.assertTrue(10 <= len(self.rules) <= 20, f"Rule count {len(self.rules)} outside 10-20 target")
        with open(self.traceability_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            t_rows = list(reader)
        self.assertEqual(len(self.rules), len(t_rows), "Rules count does not match traceability rows count")
        with open(self.queue_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            q_rows = list(reader)
        self.assertGreaterEqual(len(q_rows), 1, "Review queue must contain flagged rules")


if __name__ == "__main__":
    unittest.main()
