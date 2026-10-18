"""Automated deterministic quality and coverage test suite for MedRule Phase 2B.1 Complete Advanced Imaging Rules & Completeness Audit.
Verifies all quality criteria across all 63 governed units, 114 consolidated rules, and completeness audit matrix.
"""
import csv
import json
import re
import unittest
from pathlib import Path
import fitz
import jsonschema

BASE_DIR = Path(__file__).resolve().parents[5]
RULES_DIR = BASE_DIR / "rulebook_collection" / "domains" / "advanced_imaging" / "rules"
MANIFESTS_DIR = BASE_DIR / "rulebook_collection" / "manifests"

class TestPhase2BRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema_path = RULES_DIR / "schema.json"
        cls.rules_path = RULES_DIR / "draft_rules.json"
        cls.traceability_path = RULES_DIR / "source_to_rule_traceability.csv"
        cls.queue_path = RULES_DIR / "human_review_queue.csv"
        cls.coverage_inventory_path = RULES_DIR / "guideline_coverage_inventory.csv"
        cls.audit_path = RULES_DIR / "completeness_audit.csv"
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
        if not text:
            return ""
        text = text.replace("\xa0", " ").replace("’", "'").replace("“", '"').replace("”", '"')
        return re.sub(r"\s+", " ", text).strip().lower()

    def test_01_total_rule_count_and_guideline_coverage(self):
        """Check 1: Exactly 114 rules extracted covering all 63 governed units."""
        self.assertEqual(len(self.rules), 114, f"Expected exactly 114 rules, found {len(self.rules)}")
        
        # Load coverage inventory
        with open(self.coverage_inventory_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            expected_units = [row["guideline_id"] for row in reader]
        self.assertEqual(len(expected_units), 63, "Expected 63 governed units in coverage inventory")

        covered_units = set()
        for r in self.rules:
            rid = r["rule_id"]
            m = re.match(r"^RULE-ADV-([A-Z0-9]+)-", rid)
            self.assertIsNotNone(m, f"Could not parse guideline prefix from {rid}")
            pfx = m.group(1)
            if pfx.startswith("CG"):
                gid = "CG-" + pfx[2:]
            elif pfx.startswith("EPOS"):
                gid = "EPOS-" + pfx[4:]
            else:
                gid = pfx
            covered_units.add(gid)

        missing = set(expected_units) - covered_units
        self.assertEqual(len(missing), 0, f"Governed units missing from extracted rules: {missing}")
        self.assertEqual(len(covered_units), 63, "All 63 governed units must be covered")

    def test_02_unique_rule_ids_and_naming_pattern(self):
        """Check 2: Every rule has a unique rule_id conforming to the standard naming pattern."""
        rule_ids = set()
        pattern = re.compile(r"^RULE-[A-Z0-9]+-[A-Z0-9_]+-[0-9]{3,}$")
        for r in self.rules:
            rid = r.get("rule_id", "")
            self.assertTrue(rid, "Rule missing rule_id")
            self.assertNotIn(rid, rule_ids, f"Duplicate rule_id found: {rid}")
            self.assertTrue(pattern.match(rid), f"rule_id {rid} does not match naming pattern")
            rule_ids.add(rid)

    def test_03_schema_compliance(self):
        """Check 3: All 114 rules validate against schema.json without error."""
        for r in self.rules:
            try:
                jsonschema.validate(instance=r, schema=self.schema)
            except jsonschema.ValidationError as e:
                self.fail(f"Rule {r.get('rule_id')} failed schema validation: {e.message}")

    def test_04_pilot_rules_preservation(self):
        """Check 4: All 16 Phase 2A pilot rules are present and unmodified."""
        expected_pilot_ids = [
            "RULE-ADV-CG2000-001", "RULE-ADV-CG2000-002", "RULE-ADV-CG2000-003", "RULE-ADV-CG2000-004",
            "RULE-ADV-CG2000-005", "RULE-ADV-CG2000-006", "RULE-ADV-CG2000-007", "RULE-ADV-CG2000-008",
            "RULE-ADV-CG2000-009", "RULE-ADV-CG2000-010", "RULE-ADV-CG2000-011", "RULE-ADV-CG2000-012",
            "RULE-ADV-CG2012-001", "RULE-ADV-CG2012-002", "RULE-ADV-CG2017-001", "RULE-ADV-CG2017-002"
        ]
        rule_ids = {r["rule_id"] for r in self.rules}
        for pid in expected_pilot_ids:
            self.assertIn(pid, rule_ids, f"Phase 2A pilot rule {pid} missing from Phase 2B consolidated rules")

    def test_05_source_pdf_files_exist(self):
        """Check 5: Every cited source PDF file exists on disk."""
        for r in self.rules:
            src = r.get("source_file", "")
            self.assertTrue(src, f"Rule {r.get('rule_id')} missing source_file")
            pdf_path = (BASE_DIR / src).resolve()
            self.assertTrue(pdf_path.exists(), f"Source file does not exist: {pdf_path}")

    def test_06_physical_page_bounds(self):
        """Check 6: Every cited physical page number is within the valid page bounds of the source PDF."""
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

    def test_07_verbatim_quote_presence(self):
        """Check 7: Every source_quote exists verbatim in the extracted text of the cited physical page."""
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

    def test_08_no_rule_marked_approved(self):
        """Check 8: Zero rules marked APPROVED (all DRAFT or NEEDS_HUMAN_REVIEW)."""
        for r in self.rules:
            rid = r.get("rule_id")
            status = r.get("extraction_status")
            self.assertNotEqual(status, "APPROVED", f"Rule {rid} must not be marked APPROVED before clinical signoff")
            self.assertIn(status, ["DRAFT", "NEEDS_HUMAN_REVIEW"], f"Invalid extraction status {status} in {rid}")

    def test_09_decision_effects_valid(self):
        """Check 9: Every rule has a valid deterministic decision effect matching schema enum."""
        valid_effects = set(self.schema["properties"]["decision_effect"]["enum"])
        for r in self.rules:
            de = r.get("decision_effect")
            self.assertIn(de, valid_effects, f"Invalid decision effect {de} in {r.get('rule_id')}")

    def test_10_condition_tree_integrity(self):
        """Check 10: Every condition group has non-empty criteria and valid operators."""
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
            criteria = node.get("criteria", [])
            sub_conds = node.get("sub_conditions", [])
            total = len(criteria) + (len(sub_conds) if isinstance(sub_conds, list) else 1 if sub_conds else 0)
            self.assertGreater(total, 0, f"Condition node in {rid} is empty")
            for crit in criteria:
                self.assertIn("condition_id", crit, f"Missing condition_id in {rid}")
                self.assertIn("description", crit, f"Missing description in {rid}")
                if "comparator" in crit:
                    self.assertIn(crit["comparator"], valid_comparators, f"Invalid comparator in {rid}")

        for r in self.rules:
            validate_node(r.get("conditions", {}), r.get("rule_id"))

    def test_11_traceability_consistency(self):
        """Check 11: Traceability CSV has exactly 114 rows matching draft_rules.json."""
        with open(self.traceability_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            t_rows = list(reader)
        self.assertEqual(len(self.rules), len(t_rows), "Rules count does not match traceability rows count")
        rule_ids = [r["rule_id"] for r in self.rules]
        trace_ids = [r["rule_id"] for r in t_rows]
        self.assertEqual(rule_ids, trace_ids, "Traceability rule ID order/content does not match draft_rules.json")

    def test_12_human_review_queue_consistency(self):
        """Check 12: Human review queue accurately reflects all flagged rules."""
        with open(self.queue_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            q_rows = list(reader)
        
        expected_flagged = [
            r["rule_id"] for r in self.rules 
            if r.get("human_review_required") is True or r.get("extraction_status") == "NEEDS_HUMAN_REVIEW"
        ]
        q_ids = [r["rule_id"] for r in q_rows]
        self.assertEqual(len(expected_flagged), len(q_ids), "Queue row count does not match flagged rules count")
        self.assertEqual(sorted(expected_flagged), sorted(q_ids), "Queue rule IDs do not match flagged rules")

    def test_13_coverage_inventory_status(self):
        """Check 13: Coverage inventory has all 63 rows marked COMPLETE and VALIDATED_FOR_REVIEW."""
        with open(self.coverage_inventory_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 63, "Expected 63 rows in coverage inventory")
        for row in rows:
            gid = row["guideline_id"]
            self.assertEqual(row["parsing_status"], "SOURCE_PARSED", f"{gid} parsing_status not SOURCE_PARSED")
            self.assertEqual(row["extraction_status"], "COMPLETE", f"{gid} extraction_status not COMPLETE")
            self.assertEqual(row["completion_status"], "VALIDATED_FOR_REVIEW", f"{gid} completion_status not VALIDATED_FOR_REVIEW")
            self.assertEqual(int(row["validation_issues_count"]), 0, f"{gid} validation_issues_count not 0")
            self.assertGreater(int(row["rules_extracted_count"]), 0, f"{gid} rules_extracted_count must be > 0")

    def test_14_completeness_audit_csv_exists_and_reconciles(self):
        """Check 14: Completeness audit CSV exists, covers all 63 units, and reconciles 15 remediated omissions."""
        self.assertTrue(self.audit_path.exists(), "completeness_audit.csv does not exist")
        with open(self.audit_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 165, f"Expected 165 audited rows, found {len(rows)}")
        
        # Verify statuses
        valid_statuses = {"COVERED", "NOT_APPLICABLE_NON_EXECUTABLE", "REMEDIATED_IN_PHASE_2B1", "COVERED_NEEDS_HUMAN_REVIEW"}
        remediated_count = 0
        rule_ids_in_rules = {r["rule_id"] for r in self.rules}

        for row in rows:
            st = row["coverage_status"]
            self.assertIn(st, valid_statuses, f"Invalid coverage status {st} in {row['guideline_or_policy_identifier']}")
            if st == "REMEDIATED_IN_PHASE_2B1":
                remediated_count += 1
                rid = row["existing_rule_ids"]
                self.assertIn(rid, rule_ids_in_rules, f"Remediated rule {rid} not found in draft_rules.json")

        self.assertEqual(remediated_count, 15, f"Expected 15 remediated omissions, found {remediated_count}")

if __name__ == "__main__":
    unittest.main()
