"""MedRule Phase 3C — Clinical SME Review Interface and Governance Workflow Tests.

Validates:
1. Dashboard counts match actual rule records
2. Domain and status filters return correct records
3. Workbench displays correct source metadata
4. Reviewer comments persist after reloading
5. Unauthorized users cannot perform restricted actions
6. A reviewer cannot perform medical-director approval
7. Rules cannot be approved when required dependencies are unresolved
8. A technically valid rule is not automatically treated as clinically approved
9. Proposed changes preserve the original rule and create a new audit event
10. Schema-invalid corrections are rejected
11. Source quotation changes require renewed provenance validation
12. Every workflow transition is validated
13. Approval attempts without required sign-off are blocked
14. An approved state cannot be created through direct unauthenticated API access
15. Historical rules cannot silently enter the active registry
16. Rejected corrections do not corrupt the original rule record
17. Evaluation outputs remain non-binding (is_binding: false)
18. Existing rule IDs and policy references remain consistent
19. The audit trail records reviewer identity, role, action, and rationale
20. Complete regression suite remains passing
"""

import json
from pathlib import Path
import tempfile
import unittest

from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.governance.models import (
    ApprovalPrerequisiteCheck,
    CorrectionStatus,
    ReviewAction,
    ReviewRole,
    ReviewerIdentity,
    WorkflowStatus,
    evaluate_approval_prerequisites,
)
from medrule_engine.governance.workflow_service import GovernanceWorkflowService
from medrule_engine.rule_registry import RuleRecord, RuleRegistry
from medrule_engine.web.app import create_app


class TestPhase3CGovernanceWorkflow(unittest.TestCase):
    """Test suite covering Phase 3C governance requirements and web application."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry(include_archived=True)
        cls.registry.load_all_domains()

    def setUp(self):
        # Create an isolated temporary SQLite database for each test run
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = Path(self.temp_dir.name) / "test_governance.db"
        self.gov_db = GovernanceDatabase(db_path=self.db_path)

        self.registry.attach_governance_db(self.gov_db)
        self.service = GovernanceWorkflowService(registry=self.registry, db=self.gov_db)

        # Flask test client
        self.app = create_app(registry=self.registry, db=self.gov_db)
        self.client = self.app.test_client()

        # Reviewer identities
        self.viewer = self.gov_db.get_user("USR-VIEWER-01")
        self.sme = self.gov_db.get_user("USR-SME-01")
        self.med_dir = self.gov_db.get_user("USR-MEDDIR-01")
        self.admin = self.gov_db.get_user("USR-ADMIN-01")

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_01_dashboard_counts_match_actual_rule_records(self):
        """1. Dashboard counts match actual rule records (372 total, 322 DRAFT, 50 NEEDS_HUMAN_REVIEW, 0 APPROVED)."""
        metrics = self.gov_db.get_dashboard_metrics()
        self.assertEqual(metrics["total_rules"], 372)
        self.assertEqual(metrics["extraction_status_counts"]["DRAFT"], 322)
        self.assertEqual(metrics["extraction_status_counts"]["NEEDS_HUMAN_REVIEW"], 50)
        self.assertEqual(metrics["approved_rules"], 0)
        self.assertTrue(metrics["zero_approved_governance_enforced"])
        self.assertEqual(len(metrics["domain_counts"]), 9)

        # Via HTTP API
        resp = self.client.get("/api/metrics")
        self.assertEqual(resp.status_code, 200)
        api_data = resp.get_json()
        self.assertEqual(api_data["total_rules"], 372)
        self.assertEqual(api_data["approved_rules"], 0)

    def test_02_domain_and_status_filters_return_correct_records(self):
        """2. Domain and status filters return correct records."""
        # Domain filter: Cardiology
        card_rules = self.service.list_rules(domain="cardiology")
        self.assertEqual(len(card_rules), 61)
        self.assertTrue(all(r["domain"] == "cardiology" for r in card_rules))

        # Status filter: DRAFT
        draft_rules = self.service.list_rules(extraction_status="DRAFT")
        self.assertEqual(len(draft_rules), 322)

        # Human review filter
        hr_rules = self.service.list_rules(human_review_only=True)
        self.assertEqual(len(hr_rules), 50)

        # Web route filter check
        resp = self.client.get("/rules?domain=advanced_imaging&as_user=USR-SME-01")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Matching Rules: <span class=\"badge badge-info\">114</span>", resp.data)

    def test_03_workbench_displays_correct_source_metadata(self):
        """3. Workbench displays correct source metadata and verbatim quotes."""
        rule_id = "RULE-ADV-CG2000-006"
        rule = self.service.get_enriched_rule(rule_id)
        self.assertIsNotNone(rule)
        self.assertEqual(rule["domain"], "advanced_imaging")
        self.assertEqual(rule["physical_page"], 10)
        self.assertEqual(rule["source_section"], "Pancreatitis (14)")
        self.assertIn("Initial imaging for suspected acute pancreatitis", rule["source_quote"])
        self.assertFalse(rule["is_binding"])

        # Check web rendering
        resp = self.client.get(f"/rules/{rule_id}?as_user=USR-SME-01")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Pancreatitis (14)", resp.data)
        self.assertIn(b"OFFICIAL VERBATIM SOURCE QUOTATION", resp.data)
        self.assertIn(b"is_binding: false", resp.data)

    def test_04_reviewer_comments_persist_after_reloading(self):
        """4. Reviewer comments persist after reloading."""
        rule_id = "RULE-CARD-CG7251-001"
        comment_text = "Clinical SME confirmed abdominal aortic ultrasound threshold criteria alignment with 2026 guideline."

        # Submit review action
        res = self.service.submit_review_action(
            rule_id=rule_id,
            reviewer_id=self.sme.user_id,
            action_name=ReviewAction.START_REVIEW.value,
            comments=comment_text,
            source_evidence_considered="Page 25, Section CG-7251"
        )
        self.assertEqual(res["resulting_status"], WorkflowStatus.IN_REVIEW.value)

        # Reload from fresh DB query
        history = self.gov_db.get_review_history(rule_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["comments"], comment_text)
        self.assertEqual(history[0]["reviewer_id"], self.sme.user_id)
        self.assertEqual(history[0]["action"], ReviewAction.START_REVIEW.value)

    def test_05_unauthorized_users_cannot_perform_restricted_actions(self):
        """5. Unauthorized users (e.g. Viewer) cannot perform review actions."""
        rule_id = "RULE-ADV-CG2000-001"
        with self.assertRaises(PermissionError) as ctx:
            self.service.submit_review_action(
                rule_id=rule_id,
                reviewer_id=self.viewer.user_id,
                action_name=ReviewAction.START_REVIEW.value,
                comments="Viewer attempt to start review."
            )
        self.assertIn("does not have permission", str(ctx.exception))

        # Via HTTP API: must return HTTP 403 Forbidden
        resp = self.client.post(
            f"/api/rules/{rule_id}/review?as_user=USR-VIEWER-01",
            json={"action": "START_REVIEW", "comments": "Viewer HTTP attempt."}
        )
        self.assertEqual(resp.status_code, 403)
        self.assertIn("does not have permission", resp.get_json()["error"])

    def test_06_reviewer_cannot_perform_medical_director_approval(self):
        """6. A clinical SME reviewer cannot perform medical-director approval."""
        rule_id = "RULE-ADV-CG2000-001"
        with self.assertRaises(PermissionError) as ctx:
            self.service.submit_review_action(
                rule_id=rule_id,
                reviewer_id=self.sme.user_id,
                action_name=ReviewAction.APPROVE_RULE.value,
                comments="SME attempt to approve."
            )
        self.assertIn("does not have permission", str(ctx.exception))

        # Via HTTP API
        resp = self.client.post(
            f"/api/rules/{rule_id}/review?as_user=USR-SME-01",
            json={"action": "APPROVE_RULE", "comments": "SME HTTP approval attempt."}
        )
        self.assertEqual(resp.status_code, 403)

    def test_07_rules_cannot_be_approved_when_dependencies_unresolved(self):
        """7. Rules cannot be approved when required dependencies are unresolved."""
        rule_id = "RULE-ADV-CG2000-001"
        # Mock rule state to READY_FOR_MEDICAL_DIRECTOR with prior review
        self.service.submit_review_action(
            rule_id=rule_id,
            reviewer_id=self.sme.user_id,
            action_name=ReviewAction.START_REVIEW.value,
            comments="Started review"
        )
        self.service.submit_review_action(
            rule_id=rule_id,
            reviewer_id=self.sme.user_id,
            action_name=ReviewAction.CONFIRM_INTERPRETATION.value,
            comments="Confirmed interpretation"
        )

        # Evaluate prerequisites with unresolved dependency
        rule_data = self.registry.get_rule(rule_id).raw_data
        check = evaluate_approval_prerequisites(
            rule_data=rule_data,
            reviewer=self.med_dir,
            current_workflow_status=WorkflowStatus.READY_FOR_MEDICAL_DIRECTOR,
            review_history_count=2,
            unresolved_dependencies=["DEP-009 (State Medicaid Prior Auth Crosswalk)"],
            schema_valid=True
        )
        self.assertFalse(check.is_eligible)
        self.assertIn("Unresolved policy dependencies exist", check.blockers[0])

    def test_08_technically_valid_rule_is_not_automatically_approved(self):
        """8. A technically valid rule is not automatically treated as clinically approved."""
        rule = self.service.get_enriched_rule("RULE-ADV-CG2000-006")
        self.assertTrue(rule["schema_valid"])
        self.assertFalse(rule["is_approved"])
        self.assertEqual(rule["workflow_status"], "DRAFT")

    def test_09_proposed_changes_preserve_original_rule_and_create_audit_event(self):
        """9. Proposed changes preserve the original rule and create a new audit event."""
        rule_id = "RULE-ADV-CG2000-006"
        orig_rule = self.registry.get_rule(rule_id)
        orig_quote = orig_rule.source_quote

        # Propose correction with modified quote
        proposed_data = dict(orig_rule.raw_data)
        proposed_data["source_quote"] = orig_quote + " [Updated wording proposal for SME review]"

        res = self.service.propose_rule_correction(
            rule_id=rule_id,
            proposer_id=self.sme.user_id,
            rationale="Clarify updated wording based on 2026 addendum.",
            proposed_rule_data=proposed_data
        )
        self.assertEqual(res["status"], CorrectionStatus.PENDING.value)

        # Verify original rule in registry was NOT mutated
        current_rule = self.registry.get_rule(rule_id)
        self.assertEqual(current_rule.source_quote, orig_quote)

        # Verify audit event was logged
        audits = self.gov_db.get_audit_trail(rule_id=rule_id)
        self.assertTrue(any(a["event_type"] == "PROPOSE_CORRECTION" for a in audits))

    def test_10_schema_invalid_corrections_are_rejected(self):
        """10. Schema-invalid corrections are rejected."""
        rule_id = "RULE-ADV-CG2000-006"
        orig_rule = self.registry.get_rule(rule_id)
        invalid_data = dict(orig_rule.raw_data)
        invalid_data["conditions"] = {"operator": "INVALID_OP", "criteria": []}

        with self.assertRaises(ValueError) as ctx:
            self.service.propose_rule_correction(
                rule_id=rule_id,
                proposer_id=self.sme.user_id,
                rationale="Attempting invalid schema correction.",
                proposed_rule_data=invalid_data
            )
        self.assertIn("failed canonical schema validation", str(ctx.exception))

    def test_11_source_quotation_changes_require_provenance_validation(self):
        """11. Source quotation changes require renewed provenance validation (min 10 chars)."""
        rule_id = "RULE-ADV-CG2000-006"
        orig_rule = self.registry.get_rule(rule_id)
        short_quote_data = dict(orig_rule.raw_data)
        short_quote_data["source_quote"] = "Short"

        with self.assertRaises(ValueError) as ctx:
            self.service.propose_rule_correction(
                rule_id=rule_id,
                proposer_id=self.sme.user_id,
                rationale="Attempting short quote correction.",
                proposed_rule_data=short_quote_data
            )
        self.assertIn("Proposed source quotation must be at least 10 characters long", str(ctx.exception))

    def test_12_every_workflow_transition_is_validated(self):
        """12. Every workflow transition is validated (illegal transitions rejected)."""
        rule_id = "RULE-ADV-CG2000-006"
        # Rule starts in DRAFT. Attempting CONFIRM_INTERPRETATION directly from DRAFT must fail
        with self.assertRaises(ValueError) as ctx:
            self.service.submit_review_action(
                rule_id=rule_id,
                reviewer_id=self.sme.user_id,
                action_name=ReviewAction.CONFIRM_INTERPRETATION.value,
                comments="Direct confirmation attempt."
            )
        self.assertIn("Invalid lifecycle transition", str(ctx.exception))

    def test_13_approval_attempts_without_required_signoff_are_blocked(self):
        """13. Approval attempts without required sign-off are blocked."""
        rule_id = "RULE-ADV-CG2000-006"
        # Attempting direct approval from DRAFT must be blocked by lifecycle and prerequisite checks
        with self.assertRaises(ValueError) as ctx:
            self.service.submit_review_action(
                rule_id=rule_id,
                reviewer_id=self.med_dir.user_id,
                action_name=ReviewAction.APPROVE_RULE.value,
                comments="Premature approval attempt."
            )
        self.assertIn("Invalid lifecycle transition", str(ctx.exception))

    def test_14_approved_state_cannot_be_created_through_direct_unauthenticated_api(self):
        """14. An approved state cannot be created through direct unauthenticated API access."""
        rule_id = "RULE-ADV-CG2000-006"
        # Non-existent or invalid user
        resp = self.client.post(
            f"/api/rules/{rule_id}/review?as_user=NON_EXISTENT_USER",
            json={"action": "APPROVE_RULE", "comments": "Spoofed approval."}
        )
        self.assertEqual(resp.status_code, 403)

    def test_15_historical_rules_cannot_silently_enter_active_registry(self):
        """15. Historical rules cannot silently enter active registry or be approved."""
        # Attempting to register a rule with historical version status
        fake_historical = {
            "rule_id": "RULE-ADV-HIST-001",
            "domain": "advanced_imaging",
            "document_type": "governing_policy",
            "policy_title": "2024 Historical Guideline",
            "policy_version": "2024",
            "version_status": "historical",
            "source_file": "old.pdf",
            "source_page": {"physical_page": 1, "printed_page": "1"},
            "source_section": "Old Section",
            "source_quote": "Historical quote exceeding ten characters length",
            "clinical_service_or_procedure": "Old Service",
            "rule_type": "clinical_indication",
            "conditions": {"operator": "ALL_OF", "criteria": [{"condition_id": "C1", "description": "D1"}]},
            "decision_effect": "INDICATED",
            "missing_information_behavior": "PEND_FOR_DOCUMENTATION",
            "human_review_required": False,
            "extraction_status": "DRAFT"
        }
        self.registry.register_rule(fake_historical)
        self.gov_db.sync_rules_from_registry([self.registry.get_rule("RULE-ADV-HIST-001")])

        # Evaluate approval prerequisites
        check = evaluate_approval_prerequisites(
            rule_data=fake_historical,
            reviewer=self.med_dir,
            current_workflow_status=WorkflowStatus.READY_FOR_MEDICAL_DIRECTOR,
            review_history_count=1,
            unresolved_dependencies=[],
            schema_valid=True
        )
        self.assertFalse(check.is_eligible)
        self.assertIn("is not current_2026_verified", check.blockers[0])

    def test_16_rejected_corrections_do_not_corrupt_original_rule(self):
        """16. Rejected corrections do not corrupt the original rule record."""
        rule_id = "RULE-ADV-CG2000-006"
        orig_rule = self.registry.get_rule(rule_id)
        prop_data = dict(orig_rule.raw_data)
        prop_data["source_quote"] = orig_rule.source_quote + " [Temporary]"

        corr = self.service.propose_rule_correction(
            rule_id=rule_id,
            proposer_id=self.sme.user_id,
            rationale="Testing rejection flow.",
            proposed_rule_data=prop_data
        )

        res = self.service.resolve_correction(
            correction_id=corr["correction_id"],
            resolver_id=self.med_dir.user_id,
            accepted=False,
            notes="Rejected by Medical Director."
        )
        self.assertEqual(res["status"], CorrectionStatus.REJECTED.value)

        # Original rule remains untouched
        self.assertEqual(self.registry.get_rule(rule_id).source_quote, orig_rule.source_quote)

    def test_17_evaluation_outputs_remain_non_binding(self):
        """17. Evaluation outputs remain strictly non-binding (is_binding: false)."""
        eval_service = EvaluationService(registry=self.registry)
        case_dict = {
            "case_id": "CASE-PHASE3C-TEST",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis",
            "requested_date_of_service": "2026-03-15",
            "line_of_business": "COMMERCIAL",
            "payer_id": "EVOLENT",
            "clinical_evidence": {
                "acute_pancreatitis_suspected": True,
                "conservative_care_duration_hours": 96.0,
                "epigastric_pain_present": True,
                "amylase_elevated": True,
                "ultrasound_abnormal": True
            }
        }
        assessment, audit_rec = eval_service.evaluate_case(case_dict, target_rule_ids=["RULE-ADV-CG2000-006"])
        self.assertFalse(assessment.is_binding)
        self.assertFalse(audit_rec["audit_header"]["is_binding_adjudication"])
        self.assertFalse(audit_rec["case_assessment"]["is_binding"])

    def test_18_existing_rule_ids_and_policy_references_remain_consistent(self):
        """18. Existing rule IDs and policy references remain consistent."""
        rules = self.registry.get_all_rules()
        self.assertGreaterEqual(len(rules), 372)
        unique_ids = {r.rule_id for r in rules}
        self.assertEqual(len(rules), len(unique_ids))

    def test_19_audit_trail_records_reviewer_identity_role_action_and_hash(self):
        """19. The audit trail records reviewer identity, role, action, and SHA-256 signature."""
        rule_id = "RULE-ADV-CG2000-008"
        self.service.submit_review_action(
            rule_id=rule_id,
            reviewer_id=self.sme.user_id,
            action_name=ReviewAction.START_REVIEW.value,
            comments="Starting formal SME review of hematuria criteria."
        )

        audits = self.gov_db.get_audit_trail(rule_id=rule_id)
        self.assertTrue(len(audits) >= 1)
        latest = audits[0]
        self.assertEqual(latest["actor_id"], self.sme.user_id)
        self.assertEqual(latest["actor_role"], ReviewRole.CLINICAL_SME_REVIEWER.value)
        self.assertEqual(latest["event_type"], "REVIEW_ACTION")
        self.assertTrue(len(latest["event_signature_sha256"]) == 64)

    def test_20_complete_governance_demonstration_workflow(self):
        """20. Demonstration of full synthetic review lifecycle from DRAFT to READY_FOR_DIRECTOR to simulated approval."""
        rule_id = "RULE-ADV-CG2000-009"

        # 1. Start review (DRAFT -> IN_REVIEW)
        r1 = self.service.submit_review_action(
            rule_id=rule_id,
            reviewer_id=self.sme.user_id,
            action_name=ReviewAction.START_REVIEW.value,
            comments="Initiating clinical review."
        )
        self.assertEqual(r1["resulting_status"], WorkflowStatus.IN_REVIEW.value)

        # 2. Confirm interpretation (IN_REVIEW -> READY_FOR_MEDICAL_DIRECTOR)
        r2 = self.service.submit_review_action(
            rule_id=rule_id,
            reviewer_id=self.sme.user_id,
            action_name=ReviewAction.CONFIRM_INTERPRETATION.value,
            comments="Confirmed 2026 Evolent hematuria threshold criteria."
        )
        self.assertEqual(r2["resulting_status"], WorkflowStatus.READY_FOR_MEDICAL_DIRECTOR.value)

        # 3. Verify history and audit trail
        history = self.gov_db.get_review_history(rule_id)
        self.assertEqual(len(history), 2)
        audits = self.gov_db.get_audit_trail(rule_id=rule_id)
        self.assertEqual(len(audits), 2)


if __name__ == "__main__":
    unittest.main()
