"""Automated deterministic quality and coverage test suite for MedRule Centene DME rules."""
import csv
import json
import re
import unittest
from pathlib import Path
import fitz
import jsonschema

BASE_DIR = Path(__file__).resolve().parents[5]
DME_DIR = BASE_DIR / "rulebook_collection" / "domains" / "centene_dme_orthotics_prosthetics"
RULES_DIR = DME_DIR / "rules"
SCHEMA_PATH = BASE_DIR / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"

class TestCenteneDMERules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema_path = SCHEMA_PATH
        cls.rules_path = RULES_DIR / "draft_rules.json"
        cls.traceability_path = RULES_DIR / "source_to_rule_traceability.csv"
        cls.queue_path = RULES_DIR / "human_review_queue.csv"
        cls.coverage_inventory_path = RULES_DIR / "guideline_coverage_inventory.csv"
        cls.completeness_audit_path = RULES_DIR / "completeness_audit.csv"

        with open(cls.schema_path, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)

        with open(cls.rules_path, "r", encoding="utf-8") as f:
            cls.rules = json.load(f)

        cls.validator = jsonschema.Draft7Validator(cls.schema)
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
        if not text:
            return ""
        text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
        return re.sub(r"\s+", " ", text).strip().lower()

    def test_01_total_rule_count_and_composition(self):
        """Verify exactly 99 rules extracted: 58 from CP.MP.107 and 41 from referenced policies."""
        self.assertEqual(len(self.rules), 99, f"Expected 99 rules, got {len(self.rules)}")
        r107 = [r for r in self.rules if "RULE-DME-107" in r["rule_id"]]
        r048 = [r for r in self.rules if "RULE-DME-048" in r["rule_id"]]
        r099 = [r for r in self.rules if "RULE-DME-099" in r["rule_id"]]
        r173 = [r for r in self.rules if "RULE-DME-173" in r["rule_id"]]
        r184 = [r for r in self.rules if "RULE-DME-184" in r["rule_id"]]
        r185 = [r for r in self.rules if "RULE-DME-185" in r["rule_id"]]
        r203 = [r for r in self.rules if "RULE-DME-203" in r["rule_id"]]
        r243 = [r for r in self.rules if "RULE-DME-243" in r["rule_id"]]

        self.assertEqual(len(r107), 58, f"Expected 58 CP.MP.107 rules, got {len(r107)}")
        self.assertEqual(len(r048), 3, f"Expected 3 CP.MP.48 rules, got {len(r048)}")
        self.assertEqual(len(r099), 7, f"Expected 7 CP.MP.99 rules, got {len(r099)}")
        self.assertEqual(len(r173), 6, f"Expected 6 CP.MP.173 rules, got {len(r173)}")
        self.assertEqual(len(r184), 7, f"Expected 7 CP.MP.184 rules, got {len(r184)}")
        self.assertEqual(len(r185), 9, f"Expected 9 CP.MP.185 rules, got {len(r185)}")
        self.assertEqual(len(r203), 3, f"Expected 3 CP.MP.203 rules, got {len(r203)}")
        self.assertEqual(len(r243), 6, f"Expected 6 CP.MP.243 rules, got {len(r243)}")

    def test_02_unique_rule_ids_and_naming_pattern(self):
        """Verify all rule IDs are unique and strictly adhere to RULE-DME-XXX-YYY pattern."""
        rule_ids = [r["rule_id"] for r in self.rules]
        self.assertEqual(len(rule_ids), len(set(rule_ids)), "Duplicate rule IDs detected")
        pattern = re.compile(r"^RULE-DME-\d{3}-\d{3}$")
        for rid in rule_ids:
            self.assertRegex(rid, pattern, f"Rule ID '{rid}' does not match pattern RULE-DME-XXX-YYY")

    def test_03_schema_compliance(self):
        """Validate every rule against canonical medrule_rule_schema.json."""
        for r in self.rules:
            errors = list(self.validator.iter_errors(r))
            self.assertEqual(len(errors), 0, f"Rule {r.get('rule_id')} failed schema: {[e.message for e in errors]}")

    def test_04_source_pdf_resolution(self):
        """Verify each rule points to an existing source PDF."""
        for r in self.rules:
            pdf_path = BASE_DIR / r["source_file"]
            self.assertTrue(pdf_path.exists(), f"Source file does not exist: {r['source_file']}")

    def test_05_page_bounds_and_validity(self):
        """Verify physical page is within valid page count of the source PDF."""
        for r in self.rules:
            doc = self.get_pdf(r["source_file"])
            page_num = r["source_page"]["physical_page"]
            self.assertGreaterEqual(page_num, 1, f"Invalid page {page_num} in {r['rule_id']}")
            self.assertLessEqual(page_num, len(doc), f"Page {page_num} exceeds max {len(doc)} in {r['rule_id']}")

    def test_06_verbatim_quote_fidelity(self):
        """Verify source quote exists verbatim on the specified physical page."""
        mismatches = []
        for r in self.rules:
            doc = self.get_pdf(r["source_file"])
            page_idx = r["source_page"]["physical_page"] - 1
            page_text = self.normalize_text(doc[page_idx].get_text())
            quote = self.normalize_text(r["source_quote"])
            if quote not in page_text:
                mismatches.append((r["rule_id"], r["source_file"], r["source_page"]["physical_page"], quote[:80]))
        self.assertEqual(len(mismatches), 0, f"Quote mismatches ({len(mismatches)}): {mismatches}")

    def test_07_no_rule_marked_approved(self):
        """Mandatory constraint: Zero rules marked APPROVED (only DRAFT or NEEDS_HUMAN_REVIEW)."""
        for r in self.rules:
            status = r.get("extraction_status", "")
            self.assertIn(status, ["DRAFT", "NEEDS_HUMAN_REVIEW"], f"Rule {r['rule_id']} has unauthorized status '{status}'")
            self.assertNotEqual(status, "APPROVED", f"Rule {r['rule_id']} cannot be marked APPROVED")

    def test_08_decision_effects_valid(self):
        """Verify decision effects conform to schema enum."""
        valid_effects = set(self.schema["properties"]["decision_effect"]["enum"])
        for r in self.rules:
            self.assertIn(r["decision_effect"], valid_effects, f"Invalid decision effect in {r['rule_id']}")

    def test_09_condition_tree_integrity(self):
        """Verify logical operators and non-empty criteria list."""
        valid_ops = {"ALL_OF", "ANY_OF", "NONE_OF", "SINGLE_CONDITION"}
        for r in self.rules:
            conds = r.get("conditions", {})
            self.assertIn(conds.get("operator"), valid_ops, f"Invalid operator in {r['rule_id']}")
            criteria = conds.get("criteria", [])
            self.assertGreaterEqual(len(criteria), 1, f"Empty criteria in {r['rule_id']}")
            for crit in criteria:
                self.assertTrue("condition_id" in crit, f"Missing condition_id in {r['rule_id']}")
                self.assertTrue("description" in crit, f"Missing description in {r['rule_id']}")

    def test_10_traceability_alignment(self):
        """Verify source_to_rule_traceability.csv aligns exactly with draft_rules.json."""
        self.assertTrue(self.traceability_path.exists(), "Traceability CSV does not exist")
        with open(self.traceability_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            csv_rules = list(reader)
        self.assertEqual(len(csv_rules), len(self.rules), "Traceability row count mismatch")
        json_ids = [r["rule_id"] for r in self.rules]
        csv_ids = [row["rule_id"] for row in csv_rules]
        self.assertEqual(json_ids, csv_ids, "Rule ID sequence mismatch between JSON and CSV")

    def test_11_human_review_queue_accuracy(self):
        """Verify all rules flagged for human review are present in human_review_queue.csv."""
        self.assertTrue(self.queue_path.exists(), "Human review queue CSV does not exist")
        with open(self.queue_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            queue_rows = list(reader)
        queue_ids = set(row["rule_id"] for row in queue_rows)
        flagged_ids = set(r["rule_id"] for r in self.rules if r.get("human_review_required") is True)
        self.assertEqual(queue_ids, flagged_ids, f"Mismatch in human review queue: {queue_ids ^ flagged_ids}")
        self.assertGreater(len(queue_ids), 0, "Human review queue should contain discretionary/clinical judgment rules")

    def test_12_coverage_inventory_completion(self):
        """Verify guideline_coverage_inventory.csv contains all sections and authorities."""
        self.assertTrue(self.coverage_inventory_path.exists(), "Coverage inventory CSV does not exist")
        with open(self.coverage_inventory_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 17, f"Expected 17 sections in inventory, found {len(rows)}")
        g_ids = [row["guideline_id"] for row in rows]
        for expected in ["CP.MP.107-SEC1", "CP.MP.48", "CP.MP.99", "CP.MP.173", "CP.MP.184", "CP.MP.185", "CP.MP.203", "CP.MP.243", "CMS-CPM-CH20"]:
            self.assertIn(expected, g_ids, f"Missing guideline_id {expected} in inventory")

    def test_13_current_vs_historical_isolation(self):
        """Verify strict isolation: all rules reference current verified versions, none reference historical."""
        for r in self.rules:
            self.assertEqual(r["version_status"], "current_2026_verified", f"Non-current version_status in {r['rule_id']}")
            self.assertNotIn("11-24", r["source_file"], f"Historical file referenced in {r['rule_id']}")
            self.assertNotIn("11/24", r["policy_version"], f"Historical policy version referenced in {r['rule_id']}")

    def test_14_cross_domain_regression_and_cumulative_totals(self):
        """Regression test verifying all 273 existing Evolent rules across 8 domains remain intact, bringing cumulative total to 372."""
        domain_dirs = {
            "advanced_imaging": 114,
            "cardiology": 61,
            "musculoskeletal_surgery": 19,
            "interventional_pain_management": 14,
            "radiation_oncology": 15,
            "physical_medicine": 17,
            "sleep_health": 8,
            "genetic_testing": 25,
        }
        total_evolent_rules = 0
        for dname, expected_count in domain_dirs.items():
            dpath = BASE_DIR / "rulebook_collection" / "domains" / dname / "rules" / "draft_rules.json"
            self.assertTrue(dpath.exists(), f"Domain rules file missing: {dpath}")
            with open(dpath, "r", encoding="utf-8") as f:
                drules = json.load(f)
            self.assertEqual(len(drules), expected_count, f"Domain {dname} count changed: expected {expected_count}, got {len(drules)}")
            total_evolent_rules += len(drules)

        self.assertEqual(total_evolent_rules, 273, f"Expected 273 Evolent rules, found {total_evolent_rules}")
        cumulative_medrule_total = total_evolent_rules + len(self.rules)
        self.assertEqual(cumulative_medrule_total, 372, f"Expected cumulative total 372, got {cumulative_medrule_total}")


if __name__ == "__main__":
    unittest.main()
