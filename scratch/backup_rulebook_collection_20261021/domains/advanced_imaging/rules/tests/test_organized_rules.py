"""Automated test suite verifying the clean rule structure directly under rules/.
Ensures every partition file conforms strictly to schema.json, all 114 rules are preserved without loss,
and no regressions occur.
"""
import json
import unittest
from pathlib import Path
import jsonschema

BASE_DIR = Path(__file__).resolve().parents[5]
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
SCHEMA_PATH = RULES_DIR / "schema.json"
DRAFT_RULES_PATH = RULES_DIR / "draft_rules.json"

class TestCleanOrganizedRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)
        with open(DRAFT_RULES_PATH, "r", encoding="utf-8") as f:
            cls.draft_rules = json.load(f)

    def test_01_all_files_valid_schema_and_counts(self):
        """Verify each partitioned file validates against schema.json and count matches exactly 114."""
        total_rules = 0
        rule_ids = set()
        
        target_dirs = [
            RULES_DIR / "ct",
            RULES_DIR / "mri",
            RULES_DIR / "cta",
            RULES_DIR / "mra",
            RULES_DIR / "pet_spect",
            RULES_DIR / "cross_cutting"
        ]
        
        partition_files = []
        for td in target_dirs:
            self.assertTrue(td.exists(), f"Directory must exist: {td}")
            partition_files.extend(list(td.rglob("*.json")))

        self.assertGreater(len(partition_files), 25, "Expected at least 25 organized partition files")

        for file_path in partition_files:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.assertIn("section_title", data, f"Missing section_title in {file_path}")
            self.assertIn("rules", data, f"Missing rules array in {file_path}")
            self.assertIn("procedure_codes", data, f"Missing procedure_codes in {file_path}")
            
            rules = data["rules"]
            self.assertEqual(data["rule_count"], len(rules), f"Rule count mismatch in {file_path}")
            
            for rule in rules:
                # Validate against official MedRule schema
                jsonschema.validate(instance=rule, schema=self.schema)
                rid = rule["rule_id"]
                self.assertNotIn(rid, rule_ids, f"Duplicate rule ID found across partitions: {rid}")
                rule_ids.add(rid)
                total_rules += 1

        self.assertEqual(total_rules, 114, f"Expected 114 total rules across partitions, got {total_rules}")
        self.assertEqual(len(rule_ids), len(self.draft_rules), "Partitioned rule IDs must match draft_rules exactly")

    def test_02_clean_modality_directories_exist(self):
        """Ensure all required modality directories exist directly under rules/ without wrapper folders."""
        expected_dirs = [
            RULES_DIR / "ct" / "head_brain",
            RULES_DIR / "ct" / "chest",
            RULES_DIR / "ct" / "spine",
            RULES_DIR / "ct" / "abdomen_pelvis",
            RULES_DIR / "ct" / "extremities",
            RULES_DIR / "mri" / "brain",
            RULES_DIR / "mri" / "chest",
            RULES_DIR / "mri" / "spine",
            RULES_DIR / "mri" / "abdomen_pelvis",
            RULES_DIR / "mri" / "extremities",
            RULES_DIR / "cta",
            RULES_DIR / "mra",
            RULES_DIR / "pet_spect",
            RULES_DIR / "cross_cutting"
        ]
        for ed in expected_dirs:
            self.assertTrue(ed.exists(), f"Expected directory does not exist: {ed}")
            
        # Verify old organized_by_modality directory is removed
        old_dir = RULES_DIR / "organized_by_modality"
        self.assertFalse(old_dir.exists(), "Old organized_by_modality directory must not exist")

if __name__ == "__main__":
    unittest.main()
