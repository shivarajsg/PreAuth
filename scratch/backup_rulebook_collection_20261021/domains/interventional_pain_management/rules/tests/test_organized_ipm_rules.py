"""Automated test suite verifying the clean organized IPM rule structure.
Ensures every procedure file conforms strictly to the schema, all 14 rules are preserved without loss,
and no regressions occur.
"""
import json
import unittest
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parents[5]
IPM_RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "interventional_pain_management" / "rules"
SCHEMA_PATH = BASE_DIR / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"
DRAFT_RULES_PATH = IPM_RULES_DIR / "draft_rules.json"

class TestCleanOrganizedIPMRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)
        with open(DRAFT_RULES_PATH, "r", encoding="utf-8") as f:
            cls.draft_rules = json.load(f)

    def test_01_all_ipm_files_valid_schema_and_counts(self):
        """Verify each partitioned IPM file validates against schema.json and count matches exactly 14."""
        total_rules = 0
        rule_ids = set()
        
        target_dirs = [
            IPM_RULES_DIR / "epidural_injections",
            IPM_RULES_DIR / "facet_interventions",
            IPM_RULES_DIR / "sacroiliac_joint",
            IPM_RULES_DIR / "neuromodulation_pumps",
            IPM_RULES_DIR / "sympathetic_blocks",
            IPM_RULES_DIR / "cross_cutting"
        ]
        
        partition_files = []
        for td in target_dirs:
            self.assertTrue(td.exists(), f"Directory must exist: {td}")
            partition_files.extend(list(td.glob("*.json")))

        self.assertEqual(len(partition_files), 10, "Expected exactly 10 organized IPM procedure files")

        for file_path in partition_files:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.assertIn("section_title", data, f"Missing section_title in {file_path}")
            self.assertIn("rules", data, f"Missing rules array in {file_path}")
            self.assertIn("procedure_codes", data, f"Missing procedure_codes in {file_path}")
            
            rules = data["rules"]
            self.assertEqual(data["rule_count"], len(rules), f"Rule count mismatch in {file_path}")
            
            for rule in rules:
                jsonschema.validate(instance=rule, schema=self.schema)
                rid = rule["rule_id"]
                self.assertNotIn(rid, rule_ids, f"Duplicate rule ID found across partitions: {rid}")
                rule_ids.add(rid)
                total_rules += 1

        self.assertEqual(total_rules, 14, f"Expected 14 total rules across partitions, got {total_rules}")
        self.assertEqual(len(rule_ids), len(self.draft_rules), "Partitioned rule IDs must match draft_rules exactly")

if __name__ == "__main__":
    unittest.main()
