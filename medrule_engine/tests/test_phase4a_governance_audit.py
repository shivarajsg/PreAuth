"""MedRule Phase 4A Automated Test Suite: Clinical Validation & Governance Audit.

Verifies:
1. Clinical Review Inventory completeness (372 rules, 0 approved, valid explicit review states).
2. Adjudication Provenance Audit integrity (36 pilot adjudications verified as synthetic fixtures).
3. Payer Readiness Matrix coverage (22 grounded configurations categorized, mock modes declared).
4. Production Readiness Matrix coverage (10 dimensions, blockers identified, accountable reviewers).
5. Core Safety Invariants (zero approved rules, is_binding: false, submission disabled).
6. Security and Clinical Review Plan documentation artifacts presence and completeness.
"""

import csv
import json
from pathlib import Path
import unittest

from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.integrations.submission import AuthorizationSubmissionAdapter, SubmissionDisabledError
from medrule_engine.rule_registry import RuleRegistry


class TestPhase4AGovernanceAudit(unittest.TestCase):
    """Automated test cases for Phase 4A audit artifacts and safety invariants."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parents[2]
        cls.manifests_dir = cls.repo_root / "rulebook_collection" / "manifests"
        cls.registry = RuleRegistry()
        cls.registry.load_all_domains()

    # -------------------------------------------------------------------------
    # Test 1: Clinical Review Inventory Completeness
    # -------------------------------------------------------------------------
    def test_01_clinical_review_inventory_completeness(self):
        """Verify phase_4a_clinical_review_inventory.csv contains all 372 rules with 0 approved."""
        inv_path = self.manifests_dir / "phase_4a_clinical_review_inventory.csv"
        self.assertTrue(inv_path.exists(), f"Missing clinical review inventory: {inv_path}")

        with open(inv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 372, f"Expected 372 rules in inventory, found {len(rows)}")

        allowed_clinical_statuses = {
            "NOT_REVIEWED",
            "IN_REVIEW",
            "NEEDS_CORRECTION",
            "AWAITING_DEPENDENCY_RESOLUTION",
            "READY_FOR_CLINICAL_SIGNOFF",
            "CLINICALLY_APPROVED",
            "REJECTED",
            "DEFERRED",
        }

        registry_ids = {r.rule_id for r in self.registry.get_all_rules()}
        approved_count = 0

        for r in rows:
            rule_id = r["rule_id"]
            self.assertIn(rule_id, registry_ids, f"Inventory contains unknown rule ID: {rule_id}")
            self.assertIn(r["clinical_review_status"], allowed_clinical_statuses)
            self.assertEqual(r["reviewer_identity_and_role"], "NONE_VERIFIED")
            self.assertEqual(r["schema_validation_status"], "SCHEMA_VALID_DRAFT_07")
            self.assertEqual(r["source_quotation_verification_status"], "VERIFIED_IN_SOURCE_PDF")

            if r["clinical_review_status"] == "CLINICALLY_APPROVED":
                approved_count += 1

        self.assertEqual(approved_count, 0, "Approved rules in clinical review inventory must strictly equal 0")

    # -------------------------------------------------------------------------
    # Test 2: Adjudication Provenance Audit Integrity
    # -------------------------------------------------------------------------
    def test_02_adjudication_provenance_audit_integrity(self):
        """Verify phase_4a_adjudication_provenance_audit.csv correctly classifies 36 pilot records."""
        audit_path = self.manifests_dir / "phase_4a_adjudication_provenance_audit.csv"
        self.assertTrue(audit_path.exists(), f"Missing adjudication provenance audit: {audit_path}")

        with open(audit_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 36, f"Expected 36 pilot adjudication records, found {len(rows)}")

        for r in rows:
            self.assertEqual(r["provenance_classification"], "SYNTHETIC_BENCHMARK_FIXTURE")
            self.assertEqual(r["authenticity_finding"], "UNVERIFIED_REVIEW_PROVENANCE")
            self.assertEqual(r["clinical_credentials_verified"], "FALSE")
            self.assertIn("BLOCKS_PRODUCTION_DEPLOYMENT", r["impact_on_production_readiness"])
            self.assertTrue(len(r["supporting_evidence"]) > 20)

    # -------------------------------------------------------------------------
    # Test 3: Payer Readiness Matrix Coverage & Classification
    # -------------------------------------------------------------------------
    def test_03_payer_readiness_matrix_coverage(self):
        """Verify phase_4a_payer_readiness_matrix.csv contains all 22 configurations and appropriate blockers."""
        matrix_path = self.manifests_dir / "phase_4a_payer_readiness_matrix.csv"
        self.assertTrue(matrix_path.exists(), f"Missing payer readiness matrix: {matrix_path}")

        with open(matrix_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 22, f"Expected 22 payer configurations, found {len(rows)}")

        allowed_classifications = {
            "VERIFIED_PUBLIC_POLICY",
            "VERIFIED_CONTRACT_CONFIGURATION",
            "MOCK_ONLY",
            "PLAN_SPECIFIC_ACCESS_REQUIRED",
            "UNRESOLVED",
            "NOT_IN_SCOPE",
        }

        prod_blocker_count = 0
        for r in rows:
            self.assertIn(r["readiness_classification"], allowed_classifications)
            self.assertEqual(r["connector_execution_mode"], "SIMULATED_MOCK_ONLY")
            if "YES" in r["blocks_production_deployment"]:
                prod_blocker_count += 1

        self.assertGreaterEqual(prod_blocker_count, 6, "Expected at least 6 configurations blocking production")

    # -------------------------------------------------------------------------
    # Test 4: Production Readiness Matrix Dimensions
    # -------------------------------------------------------------------------
    def test_04_production_readiness_matrix_dimensions(self):
        """Verify phase_4a_production_readiness_matrix.csv evaluates all 10 mandated readiness dimensions."""
        matrix_path = self.manifests_dir / "phase_4a_production_readiness_matrix.csv"
        self.assertTrue(matrix_path.exists(), f"Missing production readiness matrix: {matrix_path}")

        with open(matrix_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 10, f"Expected exactly 10 readiness dimensions, found {len(rows)}")

        dimension_names = {r["readiness_dimension"] for r in rows}
        expected_dimensions = {
            "Rule Extraction and Clinical Validation",
            "Payer and Plan Applicability Configuration",
            "Human Identity and Clinical Credential Verification",
            "Technical Application Security",
            "Audit Retention and Integrity",
            "Privacy and Data Governance",
            "External Integration Authorization and Testing",
            "Clinical and Operational Validation",
            "Incident Handling and Rollback",
            "Regulatory and Legal Review",
        }
        self.assertEqual(dimension_names, expected_dimensions)

        for r in rows:
            self.assertTrue(len(r["evidence"]) > 10)
            self.assertTrue(len(r["outstanding_gaps"]) > 10)
            self.assertTrue(len(r["accountable_reviewer"]) > 5)
            self.assertEqual(r["blocks_production_deployment"], "YES", "All dimensions currently block production")

    # -------------------------------------------------------------------------
    # Test 5: Core Safety Invariants Enforced
    # -------------------------------------------------------------------------
    def test_05_core_safety_invariants(self):
        """Verify 0 approved rules in registry and DB, non-binding evaluations, and disabled submissions."""
        # Invariant 1: Zero approved rules in registry
        stats = self.registry.get_statistics()
        self.assertEqual(stats["status_counts"]["APPROVED"], 0)
        self.assertEqual(stats["status_counts"]["DRAFT"], 322)
        self.assertEqual(stats["status_counts"]["NEEDS_HUMAN_REVIEW"], 50)

        # Invariant 2: Database has 0 approved rules and 0 authentic review records
        db = GovernanceDatabase()
        with db.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM rule_governance_state WHERE workflow_status = 'APPROVED'")
            self.assertEqual(c.fetchone()[0], 0)
            c.execute("SELECT COUNT(*) FROM review_records")
            self.assertEqual(c.fetchone()[0], 0, "review_records in default database must be 0")

        # Invariant 3: Evaluation Service unconditionally produces is_binding: false
        eval_svc = EvaluationService(registry=self.registry)
        sample_case = {
            "case_id": "TEST-INVARIANT-CASE-01",
            "patient": {"id": "P01", "first_name": "Test", "last_name": "Patient", "dob": "1980-01-01", "gender": "male"},
            "payer": {"payer_id": "CENTENE", "plan_id": "MEDICARE_ADV_FL", "line_of_business": "medicare_advantage"},
            "provider": {"npi": "1234567890", "name": "Dr. Specialist", "taxonomy": "207L00000X"},
            "clinical_context": {
                "domain": "cardiology",
                "requested_procedure": {"cpt_code": "93306", "description": "TTE"},
                "diagnoses": [{"icd10_code": "I42.0", "description": "Dilated cardiomyopathy"}],
                "date_of_service": "2026-05-10",
                "clinical_notes": "Dilated cardiomyopathy assessment",
                "structured_evidence": {"dyspnea_nyha_class": 3}
            }
        }
        assessment, audit_record = eval_svc.evaluate_case(sample_case)
        self.assertFalse(assessment.is_binding, "Evaluations must unconditionally enforce is_binding: false")

        # Invariant 4: Outbound submission adapter raises SubmissionDisabledError
        adapter = AuthorizationSubmissionAdapter()
        with self.assertRaises(SubmissionDisabledError):
            adapter.submit_prior_authorization({"case_id": "TEST-CASE"})

    # -------------------------------------------------------------------------
    # Test 6: Markdown Documentation Artifacts Present
    # -------------------------------------------------------------------------
    def test_06_markdown_artifacts_present(self):
        """Verify Phase 4A markdown audit and planning artifacts exist and are comprehensive."""
        plan_path = self.manifests_dir / "phase_4a_clinical_review_plan.md"
        sec_path = self.manifests_dir / "phase_4a_security_gap_assessment.md"
        rep_path = self.manifests_dir / "phase_4a_completion_report.md"

        self.assertTrue(plan_path.exists(), f"Missing review plan: {plan_path}")
        self.assertTrue(sec_path.exists(), f"Missing security assessment: {sec_path}")
        self.assertTrue(rep_path.exists(), f"Missing completion report: {rep_path}")

        self.assertGreater(plan_path.stat().st_size, 2000, "Review plan markdown must be substantive")
        self.assertGreater(sec_path.stat().st_size, 3000, "Security assessment markdown must be substantive")
        self.assertGreater(rep_path.stat().st_size, 3000, "Completion report markdown must be substantive")


if __name__ == "__main__":
    unittest.main()
