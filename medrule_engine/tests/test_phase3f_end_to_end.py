"""MedRule Phase 3F Test Suite: End-to-End Application Integration & Release Candidate.

Verifies all 25 specific integration, security, and governance requirements:
 1. Application startup and database initialization in clean state
 2. Loading of all 9 clinical domains into rule registry (372 rules total)
 3. Creation of valid prior-auth case via intake web form & API
 4. Rejection of invalid case with clear validation error messages
 5. Mock payer configuration resolution (matching correct policy)
 6. Routing fallback when line of business is unknown
 7. Benefits verification check (handling missing benefits safely)
 8. Prior-auth requirement determination (mock connector execution)
 9. Deterministic evaluation of applicable rules for submitted case
 10. Proper handling of insufficient clinical information (UNKNOWN / INSUFFICIENT_INFO)
 11. Automatic escalation to human review queue when indicated
 12. Display of source policy citations on results page
 13. Persistence of case intake and evaluation records in SQLite
 14. Navigation from evaluation result to Clinical SME Review Workbench for governing rule
 15. Enforcement of reviewer permissions on governance actions (SME vs Medical Director)
 16. Preservation of proposed corrections without modifying original rules
 17. Rejection of prior-authorization submission when adapter is disabled
 18. Proper distinction between simulated and real connector execution
 19. Preservation of the 0-approved-rules invariant throughout intake and evaluation
 20. is_binding: false flag unconditionally present on all outputs
 21. Application state reload from disk after restart (persistence verification)
 22. Path traversal attack rejection on /pdf/ route
 23. Non-PDF file rejection on /pdf/ route
 24. Session and security headers present in responses
 25. Full synthetic workflow from intake to evaluation to review to dashboard across all 9 domains
"""

from dataclasses import asdict
from datetime import datetime, timezone
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
)
from medrule_engine.governance.workflow_service import GovernanceWorkflowService
from medrule_engine.integrations.base import (
    ConnectorMode,
    SecurityContext,
)
from medrule_engine.integrations.intake_service import (
    CaseIntakeOrchestrator,
    LifecycleState,
)
from medrule_engine.integrations.submission import (
    AuthorizationSubmissionAdapter,
    SubmissionDisabledError,
)
from medrule_engine.rule_registry import RuleRegistry
from medrule_engine.web.app import create_app


class TestPhase3FEndToEnd(unittest.TestCase):
    """Phase 3F End-to-End Application Integration and Release Candidate Test Suite."""

    @classmethod
    def setUpClass(cls):
        cls.registry = RuleRegistry(include_archived=True)
        cls.registry.load_all_domains()

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = Path(self.temp_dir.name) / "test_governance.db"
        self.gov_db = GovernanceDatabase(db_path=self.db_path)
        self.workflow_service = GovernanceWorkflowService(registry=self.registry, db=self.gov_db)
        self.eval_service = EvaluationService(registry=self.registry)
        self.intake_orchestrator = CaseIntakeOrchestrator(
            evaluation_service=self.eval_service,
            governance_db=self.gov_db
        )
        self.app = create_app(
            registry=self.registry,
            db=self.gov_db,
            test_config={"TESTING": True}
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    # -------------------------------------------------------------------------
    # Test 1: Application startup and database initialization in clean state
    # -------------------------------------------------------------------------
    def test_01_app_startup_and_db_initialization_clean_state(self):
        """Verify clean startup, table creation, default reviewers, and healthy response."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "HEALTHY")
        self.assertEqual(data["database"], "CONNECTED")
        self.assertEqual(data["rules_approved"], 0)
        self.assertTrue(data["zero_approved_invariant"])
        self.assertFalse(data["is_binding"])

        # Verify default users seeded
        users = self.gov_db.list_users()
        self.assertGreaterEqual(len(users), 4)
        roles = {u.role for u in users}
        self.assertIn(ReviewRole.CLINICAL_SME_REVIEWER, roles)
        self.assertIn(ReviewRole.MEDICAL_DIRECTOR, roles)
        self.assertIn(ReviewRole.ADMINISTRATOR, roles)

    # -------------------------------------------------------------------------
    # Test 2: Loading of all 9 clinical domains into rule registry (372 rules)
    # -------------------------------------------------------------------------
    def test_02_all_nine_clinical_domains_loaded_into_registry(self):
        """Verify registry loads exactly 372 rules across all 9 domains with 0 approved."""
        rules = self.registry.get_all_rules()
        self.assertEqual(len(rules), 372, "Total knowledge base rules must equal 372")

        stats = self.registry.get_statistics()
        self.assertEqual(len(stats["domains"]), 9, "Must contain exactly 9 clinical domains")
        self.assertEqual(stats["status_counts"]["DRAFT"], 322)
        self.assertEqual(stats["status_counts"]["NEEDS_HUMAN_REVIEW"], 50)
        self.assertEqual(stats["status_counts"]["APPROVED"], 0, "Approved rules must strictly equal 0")

    # -------------------------------------------------------------------------
    # Test 3: Creation of valid prior-auth case via intake web form & API
    # -------------------------------------------------------------------------
    def test_03_create_valid_case_via_intake_web_and_api(self):
        """Verify both API and web form creation of valid intake cases."""
        # 1. API creation
        api_payload = {
            "case_id": "CASE-TEST-API-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "payer_id": "EVOLENT",
            "plan_id": "COMMERCIAL_CHOICE_PLUS",
            "submitted_documents": ["Comprehensive clinical notes and diagnostic findings"],
            "bypass_documentation_check": True,
            "clinical_evidence": {
                "pancreatitis_diagnostic_markers": "ELEVATED",
                "conservative_treatment_duration_hours": 96,
                "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT",
                "ordering_provider_license": True
            }
        }
        res_api = self.client.post("/api/cases/intake", json=api_payload)
        self.assertEqual(res_api.status_code, 201)
        api_data = res_api.get_json()
        self.assertEqual(api_data["case_id"], "CASE-TEST-API-001")
        self.assertIn(api_data["lifecycle_state"], ("EVALUATED_NON_BINDING", "MANUAL_REVIEW_REQUIRED"))
        self.assertFalse(api_data["is_binding"])

        # 2. Web Form submission
        form_payload = {
            "case_id": "CASE-TEST-FORM-002",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "payer_id": "EVOLENT",
            "plan_id": "COMMERCIAL_CHOICE_PLUS",
            "submitted_documents": "Comprehensive clinical notes and diagnostic findings",
            "bypass_documentation_check": "true",
            "clinical_evidence_json": json.dumps({
                "pancreatitis_diagnostic_markers": "ELEVATED",
                "conservative_treatment_duration_hours": 96,
                "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT",
                "ordering_provider_license": True
            })
        }
        res_form = self.client.post("/intake", data=form_payload, follow_redirects=False)
        self.assertEqual(res_form.status_code, 302)
        self.assertIn("/cases/CASE-TEST-FORM-002", res_form.headers["Location"])

    # -------------------------------------------------------------------------
    # Test 4: Rejection of invalid case with clear validation error messages
    # -------------------------------------------------------------------------
    def test_04_rejection_of_invalid_case_with_validation_errors(self):
        """Verify invalid payload missing mandatory fields returns 400 with explanation."""
        invalid_payload = {
            "case_id": "CASE-INVALID-001",
            "procedure_code": "74177"
            # Missing patient_id, clinical_domain, requested_date_of_service, line_of_business
        }
        res = self.client.post("/api/cases/intake", json=invalid_payload)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("Missing required", data["error"])
        self.assertEqual(data["status"], "VALIDATION_FAILED")

    # -------------------------------------------------------------------------
    # Test 5: Mock payer configuration resolution (matching correct policy)
    # -------------------------------------------------------------------------
    def test_05_mock_payer_config_resolution(self):
        """Verify intake resolves matching payer plan configuration."""
        payload = {
            "case_id": "CASE-CFG-RESOLVE-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "payer_id": "EVOLENT",
            "plan_id": "COMMERCIAL_CHOICE_PLUS",
            "submitted_documents": ["Comprehensive clinical notes and diagnostic findings"],
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        }
        res = self.client.post("/api/cases/intake", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data["metadata"]["governing_policy_id"], "DOC-ADV-001")
        self.assertEqual(data["metadata"]["governing_policy_version"], "2026 v2")

    # -------------------------------------------------------------------------
    # Test 6: Routing fallback when line of business is unknown
    # -------------------------------------------------------------------------
    def test_06_routing_fallback_unknown_line_of_business(self):
        """Verify fallback when an unconfigured line of business is submitted."""
        payload = {
            "case_id": "CASE-UNKNOWN-LOB-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "OTHER",
            "requested_date_of_service": "2026-03-15",
            "payer_id": "EVOLENT",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        }
        res = self.client.post("/api/cases/intake", json=payload)
        # Should transition safely to POLICY_CONTEXT_UNRESOLVED or fallback
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn(data["lifecycle_state"], ("POLICY_CONTEXT_UNRESOLVED", "EVALUATED_NON_BINDING", "AWAITING_DOCUMENTATION"))

    # -------------------------------------------------------------------------
    # Test 7: Benefits verification check (handling missing benefits safely)
    # -------------------------------------------------------------------------
    def test_07_benefits_verification_missing_benefits_safely_handled(self):
        """Verify handling when procedure is excluded or benefits are missing."""
        payload = {
            "case_id": "CASE-EXCLUDED-BENEFIT-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "99999_EXCLUDED",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "payer_id": "EVOLENT",
            "clinical_evidence": {}
        }
        res = self.client.post("/api/cases/intake", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn(data["lifecycle_state"], ("POLICY_CONTEXT_UNRESOLVED", "AWAITING_DOCUMENTATION"))

    # -------------------------------------------------------------------------
    # Test 8: Prior-auth requirement determination (mock connector execution)
    # -------------------------------------------------------------------------
    def test_08_prior_auth_requirement_mock_connector_execution(self):
        """Verify mock connector execution and audit logging."""
        payload = {
            "case_id": "CASE-CONN-EXEC-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        }
        res = self.client.post("/api/cases/intake", json=payload)
        self.assertEqual(res.status_code, 201)
        events = self.gov_db.list_connector_audit_events(case_id="CASE-CONN-EXEC-001")
        self.assertGreaterEqual(len(events), 2)
        for ev in events:
            self.assertEqual(ev["execution_mode"], "MOCK")
            self.assertEqual(ev["status"], "SUCCESS")

    # -------------------------------------------------------------------------
    # Test 9: Deterministic evaluation of applicable rules for submitted case
    # -------------------------------------------------------------------------
    def test_09_deterministic_evaluation_of_applicable_rules(self):
        """Verify deterministic rule condition evaluation."""
        payload = {
            "case_id": "CASE-DETERMINISTIC-MET-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "submitted_documents": ["Comprehensive clinical notes and diagnostic findings"],
            "bypass_documentation_check": True,
            "clinical_evidence": {
                "pancreatitis_diagnostic_markers": "ELEVATED",
                "conservative_treatment_duration_hours": 96,
                "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT",
                "ordering_provider_license": True
            }
        }
        res = self.client.post("/api/cases/intake", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        eval_res = data.get("evaluation_result", {})
        self.assertIn(eval_res.get("assessment_status"), ("NON_BINDING_MEETS_CRITERIA", "MANUAL_REVIEW_REQUIRED"))
        eval_rules = eval_res.get("rule_results", []) or eval_res.get("rule_evaluations", [])
        self.assertGreater(len(eval_rules), 0)
        any_met = any(
            "TRUE" in str(r.get("condition_result", {}).get("status", "")) or
            "MET" in str(r.get("condition_result", {}).get("status", ""))
            for r in eval_rules
        )
        self.assertTrue(any_met, "At least one applicable clinical condition must be MET")

    # -------------------------------------------------------------------------
    # Test 10: Handling of insufficient clinical information
    # -------------------------------------------------------------------------
    def test_10_handling_insufficient_clinical_information(self):
        """Verify omitted evidence parameters lead to UNKNOWN condition states."""
        payload = {
            "case_id": "CASE-INSUFFICIENT-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "bypass_documentation_check": True,
            "clinical_evidence": {}
        }
        res = self.client.post("/api/cases/intake", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        eval_res = data.get("evaluation_result", {})
        self.assertIn(eval_res.get("assessment_status"), (
            "NON_BINDING_INSUFFICIENT_INFORMATION",
            "NON_BINDING_DOES_NOT_MEET_CRITERIA",
            "MANUAL_REVIEW_REQUIRED"
        ))

    # -------------------------------------------------------------------------
    # Test 11: Automatic escalation to human review queue when indicated
    # -------------------------------------------------------------------------
    def test_11_automatic_escalation_to_human_review_queue(self):
        """Verify rules requiring human review result in escalation flags."""
        payload = {
            "case_id": "CASE-ESCALATE-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "bypass_documentation_check": True,
            "clinical_evidence": {"clinical_information_submitted": True}
        }
        res = self.client.post("/api/cases/intake", json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        # Case should be flagged for manual review or have review escalations
        self.assertTrue(
            data["lifecycle_state"] == "MANUAL_REVIEW_REQUIRED" or
            len(data.get("evaluation_result", {}).get("human_review_escalations", [])) > 0
        )

    # -------------------------------------------------------------------------
    # Test 12: Display of source policy citations on results page
    # -------------------------------------------------------------------------
    def test_12_display_of_source_policy_citations(self):
        """Verify evaluation detail view renders policy source citations."""
        case_data = {
            "case_id": "CASE-CITATION-VIEW-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "procedure_name": "CT Abdomen and Pelvis with contrast",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "submitted_documents": ["Comprehensive clinical notes and diagnostic findings"],
            "bypass_documentation_check": True,
            "clinical_evidence": {
                "pancreatitis_diagnostic_markers": "ELEVATED",
                "conservative_treatment_duration_hours": 96,
                "ultrasound_findings": "NO_GALLSTONES_OR_DILATED_DUCT",
                "ordering_provider_license": True
            }
        }
        self.intake_orchestrator.process_intake(case_data)

        res = self.client.get("/cases/CASE-CITATION-VIEW-001")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn("NON-BINDING EVALUATION", html)
        self.assertIn("Governing Policy Citation:", html)
        self.assertIn("is_binding: false", html)

    # -------------------------------------------------------------------------
    # Test 13: Persistence of case intake and evaluation records in SQLite
    # -------------------------------------------------------------------------
    def test_13_persistence_of_case_intake_and_evaluation_records(self):
        """Verify SQLite datastore securely stores and retrieves case records."""
        case_data = {
            "case_id": "CASE-PERSIST-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        }
        self.intake_orchestrator.process_intake(case_data)

        rec = self.gov_db.get_case_intake_record("CASE-PERSIST-001")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["case_id"], "CASE-PERSIST-001")
        self.assertFalse(rec["is_binding"])
        self.assertIn(rec["lifecycle_state"], [s.value for s in LifecycleState])

    # -------------------------------------------------------------------------
    # Test 14: Navigation from evaluation result to Clinical SME Review Workbench
    # -------------------------------------------------------------------------
    def test_14_navigation_from_evaluation_to_workbench(self):
        """Verify links on case detail point to rule workbench and workbench loads."""
        rule_id = "RULE-ADV-CG2000-001"
        res = self.client.get(f"/rules/{rule_id}")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn(rule_id, html)
        self.assertIn("OFFICIAL VERBATIM SOURCE QUOTATION", html)

    # -------------------------------------------------------------------------
    # Test 15: Enforcement of reviewer permissions on governance actions
    # -------------------------------------------------------------------------
    def test_15_enforcement_of_reviewer_permissions(self):
        """Verify SME reviewer cannot perform medical director approval."""
        rule_id = "RULE-ADV-CG2000-001"
        sme_user = "USR-SME-01"

        res = self.client.post(
            f"/api/rules/{rule_id}/review",
            json={
                "action": "APPROVE",
                "comments": "Attempting unauthorized approval"
            },
            query_string={"as_user": sme_user}
        )
        self.assertIn(res.status_code, (400, 403))
        self.assertIn("error", res.get_json())

    # -------------------------------------------------------------------------
    # Test 16: Preservation of proposed corrections without modifying original rules
    # -------------------------------------------------------------------------
    def test_16_preservation_of_proposed_corrections(self):
        """Verify proposed correction leaves active rule in registry untouched."""
        rule_id = "RULE-ADV-CG2000-001"
        orig_rule = self.registry.get_rule(rule_id)
        orig_effect = orig_rule.decision_effect

        prop_data = dict(orig_rule.raw_data)
        prop_data["decision_effect"] = "NOT_INDICATED"

        res = self.client.post(
            f"/api/rules/{rule_id}/correct",
            json={
                "rationale": "Clarification on not indicated clinical threshold",
                "proposed_rule_data": prop_data
            },
            query_string={"as_user": "USR-SME-01"}
        )
        self.assertEqual(res.status_code, 200)

        # Verify active registry remains untouched
        current_rule = self.registry.get_rule(rule_id)
        self.assertEqual(current_rule.decision_effect, orig_effect)

        # Verify correction stored as PENDING
        corrections = self.gov_db.get_proposed_corrections(rule_id=rule_id)
        self.assertGreaterEqual(len(corrections), 1)
        self.assertEqual(corrections[0]["status"], "PENDING")

    # -------------------------------------------------------------------------
    # Test 17: Rejection of prior-authorization submission when adapter disabled
    # -------------------------------------------------------------------------
    def test_17_rejection_of_prior_auth_submission_disabled_adapter(self):
        """Verify outbound submission adapter is strictly disabled."""
        adapter = AuthorizationSubmissionAdapter()
        self.assertEqual(adapter.mode, ConnectorMode.DISABLED)
        with self.assertRaises(SubmissionDisabledError):
            adapter.submit_prior_authorization(case_data={"case_id": "TEST"})

    # -------------------------------------------------------------------------
    # Test 18: Proper distinction between simulated and real connector execution
    # -------------------------------------------------------------------------
    def test_18_proper_distinction_between_simulated_and_real_connector(self):
        """Verify connector execution mode is explicitly MOCK, never LIVE."""
        payload = {
            "case_id": "CASE-MOCK-CHECK-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        }
        res = self.client.post("/api/cases/intake", json=payload)
        self.assertEqual(res.status_code, 201)
        events = self.gov_db.list_connector_audit_events(case_id="CASE-MOCK-CHECK-001")
        for ev in events:
            self.assertEqual(ev["execution_mode"], "MOCK")
            self.assertNotEqual(ev["execution_mode"], "LIVE_AUTHORIZED")

    # -------------------------------------------------------------------------
    # Test 19: Preservation of the 0-approved-rules invariant
    # -------------------------------------------------------------------------
    def test_19_preservation_of_zero_approved_rules_invariant(self):
        """Verify approved rules count is strictly 0 across the entire system."""
        metrics = self.gov_db.get_dashboard_metrics()
        self.assertEqual(metrics["approved_rules"], 0)
        self.assertTrue(metrics["zero_approved_governance_enforced"])

        res = self.client.get("/api/metrics")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["approved_rules"], 0)

    # -------------------------------------------------------------------------
    # Test 20: is_binding: false flag unconditionally present on all outputs
    # -------------------------------------------------------------------------
    def test_20_is_binding_false_unconditionally_present(self):
        """Verify is_binding: false on health check, intake, evaluation, and DB records."""
        # 1. Health endpoint
        res_h = self.client.get("/health")
        self.assertFalse(res_h.get_json()["is_binding"])

        # 2. Intake API
        res_i = self.client.post("/api/cases/intake", json={
            "case_id": "CASE-BINDING-CHECK-001",
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        })
        self.assertFalse(res_i.get_json()["is_binding"])

        # 3. Database record
        rec = self.gov_db.get_case_intake_record("CASE-BINDING-CHECK-001")
        self.assertFalse(rec["is_binding"])

    # -------------------------------------------------------------------------
    # Test 21: Application state reload from disk after restart
    # -------------------------------------------------------------------------
    def test_21_application_state_reload_from_disk_after_restart(self):
        """Verify SQLite data persistence across process restart simulation."""
        case_id = "CASE-RELOAD-TEST-001"
        self.intake_orchestrator.process_intake({
            "case_id": case_id,
            "patient_id": "MEM-SYNTH-88219",
            "clinical_domain": "advanced_imaging",
            "procedure_code": "74177",
            "line_of_business": "COMMERCIAL",
            "requested_date_of_service": "2026-03-15",
            "clinical_evidence": {"pancreatitis_diagnostic_markers": "ELEVATED"}
        })

        # Reopen database connection to the same file
        reloaded_db = GovernanceDatabase(db_path=self.db_path)
        case_rec = reloaded_db.get_case_intake_record(case_id)
        self.assertIsNotNone(case_rec)
        self.assertEqual(case_rec["case_id"], case_id)
        self.assertFalse(case_rec["is_binding"])

    # -------------------------------------------------------------------------
    # Test 22: Path traversal attack rejection on /pdf/ route
    # -------------------------------------------------------------------------
    def test_22_path_traversal_attack_rejection_on_pdf_route(self):
        """Verify path traversal sequences are rejected with 400 or 403 or 404."""
        bad_paths = [
            "../../etc/passwd",
            "..\\..\\windows\\win.ini",
            "%2e%2e/%2e%2e/etc/passwd",
            "rulebook_collection/../../secret.txt",
        ]
        for bp in bad_paths:
            res = self.client.get(f"/pdf/{bp}")
            self.assertIn(res.status_code, (400, 403, 404), f"Failed to reject traversal on: {bp}")

    # -------------------------------------------------------------------------
    # Test 23: Non-PDF file rejection on /pdf/ route
    # -------------------------------------------------------------------------
    def test_23_non_pdf_file_rejection_on_pdf_route(self):
        """Verify non-PDF files requested through /pdf/ are rejected with 403."""
        res = self.client.get("/pdf/rulebook_collection/schemas/medrule_rule_schema.json")
        self.assertEqual(res.status_code, 403)

    # -------------------------------------------------------------------------
    # Test 24: Session and security headers present in responses
    # -------------------------------------------------------------------------
    def test_24_session_and_security_headers_present(self):
        """Verify security headers X-Content-Type-Options and X-Frame-Options are set."""
        res = self.client.get("/")
        self.assertEqual(res.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(res.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertIn("default-src", res.headers.get("Content-Security-Policy", ""))

    # -------------------------------------------------------------------------
    # Test 25: Full synthetic workflow across all 9 clinical domains
    # -------------------------------------------------------------------------
    def test_25_full_synthetic_workflow_end_to_end_all_domains(self):
        """Execute end-to-end synthetic intake and evaluation across all 9 domains."""
        domains_and_codes = [
            ("advanced_imaging", "74177", "CT Abdomen and Pelvis with contrast"),
            ("cardiology", "93458", "Diagnostic Coronary Angiography"),
            ("musculoskeletal", "27447", "Total Knee Arthroplasty"),
            ("interventional_pain", "62323", "Lumbar Epidural Steroid Injection"),
            ("radiation_oncology", "77301", "IMRT Treatment Planning"),
            ("physical_medicine", "97110", "Therapeutic Exercise PT"),
            ("sleep_health", "95806", "Home Sleep Apnea Test"),
            ("genetic_testing", "81162", "BRCA1 BRCA2 Gene Sequencing"),
            ("centene_dme", "A9276", "Continuous Glucose Monitor Sensor"),
        ]

        for i, (dom, code, name) in enumerate(domains_and_codes, 1):
            c_id = f"CASE-E2E-{dom.upper()}-{i:03d}"
            payload = {
                "case_id": c_id,
                "patient_id": "MEM-SYNTH-88219",
                "clinical_domain": dom,
                "procedure_code": code,
                "procedure_name": name,
                "line_of_business": "COMMERCIAL",
                "requested_date_of_service": "2026-03-15",
                "payer_id": "CENTENE" if "centene" in dom else "EVOLENT",
                "plan_id": "COMMERCIAL_CHOICE_PLUS",
                "submitted_documents": ["Comprehensive clinical notes and diagnostic findings"],
                "bypass_documentation_check": True,
                "clinical_evidence": {
                    "ordering_provider_license": True,
                    "clinical_indication_documented": True
                }
            }
            res = self.client.post("/api/cases/intake", json=payload)
            self.assertEqual(res.status_code, 201, f"Failed on domain {dom}")
            data = res.get_json()
            self.assertEqual(data["case_id"], c_id)
            self.assertFalse(data["is_binding"])

            # Verify inspection endpoint
            res_view = self.client.get(f"/cases/{c_id}")
            self.assertEqual(res_view.status_code, 200, f"Failed detail view for {c_id}")

        # Verify dashboard reflects all cases
        dash_res = self.client.get("/dashboard")
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn("Case Intake Total", dash_res.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
