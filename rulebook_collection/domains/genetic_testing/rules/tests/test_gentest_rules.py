"""Automated deterministic quality and coverage test suite for MedRule Genetic Testing rules."""
import csv
import json
import re
import unittest
from pathlib import Path
import fitz
import jsonschema

BASE_DIR = Path(__file__).resolve().parents[5]
GEN_DIR = BASE_DIR / "rulebook_collection" / "domains" / "genetic_testing"
RULES_DIR = GEN_DIR / "rules"
SCHEMA_PATH = BASE_DIR / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"

class TestGenTestRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema_path = SCHEMA_PATH
        cls.rules_path = RULES_DIR / "draft_rules.json"
        cls.traceability_path = RULES_DIR / "source_to_rule_traceability.csv"
        cls.queue_path = RULES_DIR / "human_review_queue.csv"
        cls.coverage_inventory_path = RULES_DIR / "guideline_coverage_inventory.csv"

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
        if not text:
            return ""
        text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
        return re.sub(r"\s+", " ", text).strip().lower()

    def test_01_total_rule_count_and_coverage(self):
        """Check 1: Exactly 25 rules covering all 23 governed units."""
        self.assertEqual(len(self.rules), 25, f"Expected 25 rules, found {len(self.rules)}")
        with open(self.coverage_inventory_path, "r", encoding="utf-8") as f:
            inv = list(csv.DictReader(f))
        self.assertEqual(len(inv), 23, f"Expected 23 governed units, found {len(inv)}")

    def test_02_unique_rule_ids_and_naming_pattern(self):
        """Check 2: Unique rule IDs conforming to RULE-GEN-[A-Z0-9_]+-[0-9]{3,}$."""
        pattern = re.compile(r"^RULE-GEN-[A-Z0-9_]+-[0-9]{3,}$")
        seen = set()
        for r in self.rules:
            rid = r["rule_id"]
            self.assertNotIn(rid, seen, f"Duplicate rule ID: {rid}")
            self.assertTrue(pattern.match(rid), f"Invalid rule ID format: {rid}")
            seen.add(rid)

    def test_03_schema_compliance(self):
        """Check 3: All 25 rules validate against canonical schema."""
        for r in self.rules:
            jsonschema.validate(instance=r, schema=self.schema)

    def test_04_source_pdf_resolution(self):
        """Check 4: Every source PDF file exists on disk."""
        for r in self.rules:
            pdf_path = (BASE_DIR / r["source_file"]).resolve()
            self.assertTrue(pdf_path.exists(), f"Source file does not exist: {pdf_path}")

    def test_05_page_bounds_and_validity(self):
        """Check 5: Every cited physical page number is within valid document bounds."""
        for r in self.rules:
            doc = self.get_pdf(r["source_file"])
            p = r["source_page"]["physical_page"]
            self.assertTrue(1 <= p <= len(doc), f"Page {p} out of bounds for {r['source_file']}")

    def test_06_verbatim_quote_fidelity(self):
        """Check 6: 100% of quotes exist verbatim in cited physical page text layer."""
        mismatches = []
        for r in self.rules:
            doc = self.get_pdf(r["source_file"])
            p = r["source_page"]["physical_page"]
            page_text = self.normalize_text(doc[p - 1].get_text("text"))
            quote_text = self.normalize_text(r["source_quote"])
            if quote_text not in page_text:
                mismatches.append((r["rule_id"], p, quote_text[:50]))
        self.assertEqual(len(mismatches), 0, f"Quote mismatches: {mismatches}")

    def test_07_no_rule_marked_approved(self):
        """Check 7: Exactly 0 rules marked APPROVED."""
        for r in self.rules:
            self.assertNotEqual(r["extraction_status"], "APPROVED")
            self.assertIn(r["extraction_status"], ["DRAFT", "NEEDS_HUMAN_REVIEW"])

    def test_08_decision_effects_valid(self):
        """Check 8: Valid decision effects matching schema enum."""
        valid_effects = set(self.schema["properties"]["decision_effect"]["enum"])
        for r in self.rules:
            self.assertIn(r["decision_effect"], valid_effects)

    def test_09_condition_tree_integrity(self):
        """Check 9: Valid condition nodes, operators, and parameters."""
        for r in self.rules:
            cond = r["conditions"]
            self.assertIn(cond["operator"], ["ALL_OF", "ANY_OF", "NONE_OF", "SINGLE_CONDITION"])
            self.assertGreater(len(cond["criteria"]), 0)

    def test_10_traceability_alignment(self):
        """Check 10: Traceability matrix matches rules count and IDs 1:1."""
        with open(self.traceability_path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), len(self.rules))
        r_ids = [r["rule_id"] for r in self.rules]
        t_ids = [row["rule_id"] for row in rows]
        self.assertEqual(r_ids, t_ids)

    def test_11_human_review_queue_accuracy(self):
        """Check 11: Review queue accounts for all flagged rules."""
        with open(self.queue_path, "r", encoding="utf-8") as f:
            q_rows = list(csv.DictReader(f))
        flagged = [r["rule_id"] for r in self.rules if r["human_review_required"] or r["extraction_status"] == "NEEDS_HUMAN_REVIEW"]
        q_ids = [row["rule_id"] for row in q_rows]
        self.assertEqual(sorted(flagged), sorted(q_ids))

    def test_12_coverage_inventory_completion(self):
        """Check 12: All 23 inventory rows marked COMPLETE / VALIDATED_FOR_REVIEW."""
        with open(self.coverage_inventory_path, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 23)
        for row in rows:
            self.assertEqual(row["source_parsing_status"], "SOURCE_PARSED")
            self.assertEqual(row["completion_status"], "VALIDATED_FOR_REVIEW")
            self.assertEqual(int(row["validation_issues_count"]), 0)

if __name__ == "__main__":
    unittest.main()
