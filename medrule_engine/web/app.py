"""MedRule Clinical SME Review Interface Web Application.

A lightweight, local Flask web application providing:
- Real-time governance dashboard
- Searchable rule explorer with comprehensive filtering
- Rule review workbench with exact source quotation vs structured interpretation
- Source PDF viewer/launcher
- Side-by-side proposed correction diffs
- Append-only audit history
- Role-based access control and approval prerequisite enforcement
"""

from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.governance.models import (
    CorrectionStatus,
    ReviewAction,
    ReviewRole,
    ReviewerIdentity,
    WorkflowStatus,
)
from medrule_engine.governance.workflow_service import GovernanceWorkflowService
from medrule_engine.integrations.intake_service import CaseIntakeOrchestrator
from medrule_engine.rule_registry import RuleRegistry

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app(
    registry: Optional[RuleRegistry] = None,
    db: Optional[GovernanceDatabase] = None,
    test_config: Optional[Dict[str, Any]] = None
) -> Flask:
    """Create and configure the Flask web application."""
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR)
    )

    if test_config:
        app.config.update(test_config)

    app.jinja_env.filters["from_json"] = lambda s: json.loads(s) if (s and isinstance(s, str)) else (s or {})

    # Instantiate services
    rule_reg = registry or RuleRegistry()
    gov_db = db or GovernanceDatabase()
    service = GovernanceWorkflowService(registry=rule_reg, db=gov_db)
    eval_service = EvaluationService(registry=rule_reg)
    intake_orchestrator = CaseIntakeOrchestrator(
        evaluation_service=eval_service,
        governance_db=gov_db
    )

    @app.after_request
    def set_security_headers(response):
        """Inject strict security headers for all responses."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' https:; "
            "img-src 'self' data:; "
            "object-src 'self'"
        )
        return response

    # Helper to get current reviewer from request (cookie or query param or default SME)
    def get_current_reviewer() -> ReviewerIdentity:
        user_id = request.args.get("as_user") or request.cookies.get("active_user_id") or "USR-SME-01"
        user = gov_db.get_user(user_id)
        if not user:
            user = gov_db.get_user("USR-SME-01") or ReviewerIdentity(
                user_id="USR-DEFAULT",
                username="default_sme",
                display_name="Dr. Default SME",
                role=ReviewRole.CLINICAL_SME_REVIEWER,
                credentials="MD"
            )
        return user

    @app.context_processor
    def inject_global_context():
        reviewer = get_current_reviewer()
        all_users = gov_db.list_users()
        return {
            "current_user": reviewer,
            "all_users": all_users,
            "roles": [r.value for r in ReviewRole],
            "workflow_statuses": [s.value for s in WorkflowStatus],
            "review_actions": [a.value for a in ReviewAction]
        }

    # ---------------------------------------------------------
    # Web UI Routes
    # ---------------------------------------------------------

    @app.route("/")
    @app.route("/dashboard")
    def dashboard():
        """Render the governance and review metrics dashboard."""
        metrics = gov_db.get_dashboard_metrics()
        recent_audits = gov_db.get_audit_trail(limit=8)
        recent_corrections = gov_db.get_proposed_corrections()[:5]

        # Load policy versions
        policy_versions = []
        p_file = REPO_ROOT / "rulebook_collection" / "manifests" / "policy_versions.csv"
        if p_file.exists():
            import csv
            with open(p_file, "r", encoding="utf-8", errors="replace") as f:
                policy_versions = list(csv.DictReader(f))

        return render_template(
            "dashboard.html",
            metrics=metrics,
            recent_audits=recent_audits,
            recent_corrections=recent_corrections,
            policy_versions=policy_versions
        )

    @app.route("/rules")
    def rule_list():
        """Filterable rule catalog."""
        domain = request.args.get("domain") or None
        wf_status = request.args.get("status") or None
        ext_status = request.args.get("extraction_status") or None
        rule_type = request.args.get("rule_type") or None
        search = request.args.get("search") or None
        hr_only = request.args.get("human_review_only") == "1"

        rules = service.list_rules(
            domain=domain,
            workflow_status=wf_status,
            extraction_status=ext_status,
            rule_type=rule_type,
            search_query=search,
            human_review_only=hr_only
        )

        all_domains = sorted(list(service.registry._rules_by_domain.keys()))

        return render_template(
            "rule_list.html",
            rules=rules,
            total_matches=len(rules),
            domains=all_domains,
            selected_domain=domain,
            selected_status=wf_status,
            selected_extraction_status=ext_status,
            selected_rule_type=rule_type,
            search_query=search or "",
            human_review_only=hr_only
        )

    @app.route("/rules/<rule_id>")
    def rule_workbench(rule_id: str):
        """Dedicated review workbench for an individual rule."""
        rule = service.get_enriched_rule(rule_id)
        if not rule:
            abort(404, description=f"Rule {rule_id} not found.")

        # Determine relative path to PDF if available
        pdf_rel_path = rule.get("source_file", "")
        pdf_exists = False
        if pdf_rel_path:
            full_pdf_path = REPO_ROOT / pdf_rel_path
            pdf_exists = full_pdf_path.exists()

        return render_template(
            "rule_workbench.html",
            rule=rule,
            pdf_rel_path=pdf_rel_path,
            pdf_exists=pdf_exists
        )

    @app.route("/queue")
    def human_review_queue():
        """Priority queue for rules awaiting human clinical review."""
        rules = service.list_rules(human_review_only=True)
        return render_template(
            "human_review_queue.html",
            rules=rules,
            total_queue_count=len(rules)
        )

    @app.route("/corrections")
    def proposed_corrections():
        """Review queue of all proposed rule corrections."""
        corrections = gov_db.get_proposed_corrections()
        return render_template(
            "corrections.html",
            corrections=corrections
        )

    # ---------------------------------------------------------
    # Phase 3D Pilot Adjudication UI & Routes
    # ---------------------------------------------------------

    @app.route("/pilot")
    def pilot_dashboard():
        """Phase 3D Clinical Pilot Evaluation and Adjudication Dashboard."""
        selected_domain = request.args.get("domain", "").strip() or None
        comparison_filter = request.args.get("comparison", "").strip() or None

        # Auto-sync if table is empty
        evals = gov_db.get_pilot_evaluations(domain=selected_domain)
        if not evals:
            pilot_dir = REPO_ROOT / "medrule_engine" / "pilot"
            gov_db.sync_pilot_all(pilot_dir)
            evals = gov_db.get_pilot_evaluations(domain=selected_domain)

        # Apply comparison filter in memory if provided
        if comparison_filter:
            evals = [e for e in evals if e.get("human_comparison_status") == comparison_filter]

        discrepancies = gov_db.get_pilot_discrepancies()
        all_evals = gov_db.get_pilot_evaluations()

        total_cases = len(all_evals)
        passed_cases = sum(1 for e in all_evals if e.get("status_match"))
        pass_rate = round((passed_cases / total_cases * 100.0), 1) if total_cases > 0 else 0
        agree_cases = sum(1 for e in all_evals if e.get("human_comparison_status") == "AGREEMENT")
        agreement_rate = round((agree_cases / total_cases * 100.0), 1) if total_cases > 0 else 0

        # Unique domains for filter dropdown
        domains = sorted(list(set(e["clinical_domain"] for e in all_evals)))

        return render_template(
            "pilot_dashboard.html",
            evaluations=evals,
            discrepancies=discrepancies,
            total_cases=total_cases,
            passed_cases=passed_cases,
            pass_rate=pass_rate,
            agree_cases=agree_cases,
            agreement_rate=agreement_rate,
            discrepancy_count=len(discrepancies),
            domains=domains,
            selected_domain=selected_domain,
            comparison_filter=comparison_filter
        )

    @app.route("/pilot/<case_id>")
    def pilot_case_detail(case_id: str):
        """View specific pilot case side-by-side machine vs human adjudication."""
        evaluation = gov_db.get_pilot_evaluation(case_id)
        if not evaluation:
            abort(404, f"Pilot case {case_id} not found.")

        # Load raw case intake payload
        raw_case = {}
        cases_file = REPO_ROOT / "medrule_engine" / "pilot" / "synthetic_pilot_cases.json"
        if cases_file.exists():
            with open(cases_file, "r", encoding="utf-8") as f:
                c_list = json.load(f)
                for c in c_list:
                    if c.get("case_id") == case_id:
                        raw_case = c
                        break

        # Load discrepancy details if present
        discrepancy = None
        disc_id = evaluation.get("discrepancy_id")
        if disc_id:
            for d in gov_db.get_pilot_discrepancies():
                if d["discrepancy_id"] == disc_id:
                    discrepancy = d
                    break

        if request.args.get("format") == "json":
            return jsonify({
                "evaluation": evaluation,
                "raw_case": raw_case,
                "discrepancy": discrepancy
            })

        return render_template(
            "pilot_case_detail.html",
            case_id=case_id,
            evaluation=evaluation,
            raw_case=raw_case,
            discrepancy=discrepancy
        )

    # ---------------------------------------------------------
    # Case Intake & Prior Authorization Case Management Routes
    # ---------------------------------------------------------

    @app.route("/intake", methods=["GET", "POST"])
    def case_intake_view():
        """Render intake submission form and process intake executions."""
        if request.method == "GET":
            timestamp_now = int(datetime.now().timestamp())
            return render_template("intake.html", timestamp_now=timestamp_now, error=None)

        # POST submission
        if request.is_json:
            data = request.get_json() or {}
        else:
            form = request.form
            evidence_raw = form.get("clinical_evidence_json", "{}")
            try:
                evidence = json.loads(evidence_raw)
            except Exception:
                evidence = {}

            docs_raw = form.get("submitted_documents", "")
            submitted_docs = [d.strip() for d in docs_raw.split(",") if d.strip()]

            data = {
                "case_id": form.get("case_id") or f"CASE-SYNTH-{int(datetime.now().timestamp())}",
                "patient_id": form.get("patient_id"),
                "clinical_domain": form.get("clinical_domain"),
                "procedure_code": form.get("procedure_code"),
                "procedure_name": form.get("procedure_name"),
                "line_of_business": form.get("line_of_business"),
                "requested_date_of_service": form.get("requested_date_of_service"),
                "payer_id": form.get("payer_id") or "EVOLENT",
                "plan_id": form.get("plan_id") or "COMMERCIAL_CHOICE_PLUS",
                "submitted_documents": submitted_docs,
                "clinical_evidence": evidence,
                "bypass_documentation_check": form.get("bypass_documentation_check") == "true"
            }

        # Validate mandatory intake fields
        req_fields = ["patient_id", "clinical_domain", "procedure_code", "requested_date_of_service", "line_of_business"]
        missing = [f for f in req_fields if not data.get(f)]
        if missing:
            err = f"Missing required intake fields: {', '.join(missing)}"
            if request.is_json:
                return jsonify({"error": err, "status": "VALIDATION_FAILED"}), 400
            return render_template("intake.html", timestamp_now=int(datetime.now().timestamp()), error=err), 400

        try:
            result = intake_orchestrator.process_intake(data)
            if request.is_json:
                return jsonify(result), 201
            return redirect(url_for("case_detail_view", case_id=result["case_id"]))
        except Exception as e:
            logger.exception("Case intake processing failure:")
            if request.is_json:
                return jsonify({"error": str(e), "status": "INTEGRATION_ERROR"}), 500
            return render_template("intake.html", timestamp_now=int(datetime.now().timestamp()), error=str(e)), 500

    @app.route("/cases")
    def case_history_view():
        """Render searchable, filterable case history table."""
        state_filter = request.args.get("state")
        domain_filter = request.args.get("domain")
        search_query = (request.args.get("search") or "").strip().lower()

        all_cases = gov_db.list_case_intake_records()
        available_states = sorted(list({c.get("lifecycle_state") for c in all_cases if c.get("lifecycle_state")}))
        available_domains = sorted(list({c.get("clinical_domain") for c in all_cases if c.get("clinical_domain")}))

        filtered = all_cases
        if state_filter:
            filtered = [c for c in filtered if c.get("lifecycle_state") == state_filter]
        if domain_filter:
            filtered = [c for c in filtered if c.get("clinical_domain") == domain_filter]
        if search_query:
            filtered = [
                c for c in filtered
                if search_query in c.get("case_id", "").lower()
                or search_query in (c.get("procedure_code") or "").lower()
                or search_query in (c.get("clinical_domain") or "").lower()
                or search_query in (c.get("metadata", {}).get("patient_id") or "").lower()
            ]

        return render_template(
            "cases.html",
            cases=filtered,
            available_states=available_states,
            available_domains=available_domains,
            selected_state=state_filter,
            selected_domain=domain_filter,
            search_query=search_query
        )

    @app.route("/cases/<case_id>")
    def case_detail_view(case_id: str):
        """Render unified evaluation results page for a specific case."""
        case = gov_db.get_case_intake_record(case_id)
        if not case:
            abort(404, f"Case {case_id} not found.")

        events = gov_db.list_connector_audit_events(case_id=case_id)
        if request.args.get("format") == "json":
            return jsonify({"case": case, "connector_events": events})

        return render_template("case_detail.html", case=case, connector_events=events)

    @app.route("/api/cases/intake", methods=["POST"])
    def api_case_intake():
        """Programmatic case intake endpoint accepting structured JSON."""
        data = request.get_json() or {}
        req_fields = ["patient_id", "clinical_domain", "procedure_code", "requested_date_of_service", "line_of_business"]
        missing = [f for f in req_fields if not data.get(f)]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}", "status": "VALIDATION_FAILED"}), 400

        try:
            result = intake_orchestrator.process_intake(data)
            return jsonify(result), 201
        except Exception as e:
            logger.exception("API intake error:")
            return jsonify({"error": str(e), "status": "ERROR"}), 500

    @app.route("/api/cases")
    def api_list_cases():
        """List case intake records as JSON."""
        state_filter = request.args.get("state")
        cases = gov_db.list_case_intake_records(lifecycle_state=state_filter)
        return jsonify(cases)

    @app.route("/api/cases/<case_id>")
    def api_get_case(case_id: str):
        """Fetch individual case record with connector events as JSON."""
        case = gov_db.get_case_intake_record(case_id)
        if not case:
            return jsonify({"error": f"Case {case_id} not found."}), 404
        events = gov_db.list_connector_audit_events(case_id=case_id)
        return jsonify({"case": case, "connector_events": events})

    @app.route("/health")
    @app.route("/api/health")
    def health_check():
        """System health and safety invariant verification endpoint."""
        metrics = gov_db.get_dashboard_metrics()
        approved = metrics.get("approved_rules", 0)
        return jsonify({
            "status": "HEALTHY",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rules_total": metrics.get("total_rules", 372),
            "rules_approved": approved,
            "zero_approved_invariant": approved == 0,
            "is_binding": False,
            "submission_adapter": "DISABLED",
            "connectors": {
                "eligibility": "MOCK",
                "benefits": "MOCK",
                "auth_requirements": "MOCK",
                "submission": "DISABLED"
            },
            "clinical_domains": len(rule_reg.get_statistics().get("domains", {}) or {}),
            "database": "CONNECTED"
        })

    # ---------------------------------------------------------
    # PDF Viewer & Download Route
    # ---------------------------------------------------------

    @app.route("/pdf/<path:pdf_path>")
    def serve_policy_pdf(pdf_path: str):
        """Safely serve or stream local policy PDF for source verification."""
        # 1. Null byte and traversal sequence detection
        if "\x00" in pdf_path or "%00" in pdf_path:
            abort(400, "Invalid file path.")

        # Check for directory traversal sequences
        normalized_path = pdf_path.replace("\\", "/")
        parts = normalized_path.split("/")
        if any(part in ("..", "%2e%2e", "%2E%2E") for part in parts) or ".." in normalized_path:
            abort(400, "Directory traversal sequences forbidden.")

        safe_path = (REPO_ROOT / normalized_path).resolve()

        # 2. Path verification: must reside inside REPO_ROOT
        try:
            safe_path.relative_to(REPO_ROOT.resolve())
        except ValueError:
            abort(403, "Access to external file path forbidden.")

        # 3. Extension check: must be a .pdf file
        if safe_path.suffix.lower() != ".pdf":
            abort(403, "Only PDF files may be served.")

        # 4. Existence check
        if not safe_path.exists() or not safe_path.is_file():
            abort(404, f"Policy PDF file not found at: {pdf_path}")

        return send_file(safe_path, mimetype="application/pdf")

    # ---------------------------------------------------------
    # Review & Governance Actions API Endpoints
    # ---------------------------------------------------------

    @app.route("/api/rules/<rule_id>/review", methods=["POST"])
    def api_submit_review(rule_id: str):
        """Submit a clinical review action."""
        data = request.get_json() or request.form
        reviewer = get_current_reviewer()

        action = data.get("action")
        comments = data.get("comments", "").strip()
        evidence = data.get("source_evidence_considered", "").strip()

        if not action:
            return jsonify({"error": "Missing required field 'action'."}), 400
        if not comments:
            return jsonify({"error": "A review comment or clinical rationale is required."}), 400

        try:
            result = service.submit_review_action(
                rule_id=rule_id,
                reviewer_id=reviewer.user_id,
                action_name=action,
                comments=comments,
                source_evidence_considered=evidence
            )
            if request.is_json:
                return jsonify({"status": "success", "result": result})
            return redirect(url_for("rule_workbench", rule_id=rule_id, as_user=reviewer.user_id))
        except PermissionError as pe:
            return jsonify({"error": str(pe)}), 403
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            logger.exception("Unexpected error during review action:")
            return jsonify({"error": f"Internal evaluation error: {str(e)}"}), 500

    @app.route("/api/rules/<rule_id>/propose-correction", methods=["POST"])
    @app.route("/api/rules/<rule_id>/correct", methods=["POST"])
    def api_propose_correction(rule_id: str):
        """Submit a proposed correction for an existing rule."""
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON payload required."}), 400

        reviewer = get_current_reviewer()
        rationale = data.get("rationale", "").strip()
        proposed_rule_data = data.get("proposed_rule_data")

        if not rationale:
            return jsonify({"error": "A clinical rationale is required."}), 400
        if not proposed_rule_data:
            return jsonify({"error": "Missing 'proposed_rule_data'."}), 400

        try:
            result = service.propose_rule_correction(
                rule_id=rule_id,
                proposer_id=reviewer.user_id,
                rationale=rationale,
                proposed_rule_data=proposed_rule_data
            )
            return jsonify({"status": "success", "result": result})
        except PermissionError as pe:
            return jsonify({"error": str(pe)}), 403
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/corrections/<correction_id>/resolve", methods=["POST"])
    def api_resolve_correction(correction_id: str):
        """Accept or reject a proposed correction."""
        data = request.get_json() or {}
        reviewer = get_current_reviewer()
        accepted = bool(data.get("accepted", False))
        notes = data.get("notes", "").strip()

        try:
            result = service.resolve_correction(
                correction_id=correction_id,
                resolver_id=reviewer.user_id,
                accepted=accepted,
                notes=notes
            )
            return jsonify({"status": "success", "result": result})
        except PermissionError as pe:
            return jsonify({"error": str(pe)}), 403
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

    @app.route("/api/rules/<rule_id>")
    def api_get_rule(rule_id: str):
        """Fetch complete enriched rule record as JSON."""
        rule = service.get_enriched_rule(rule_id)
        if not rule:
            return jsonify({"error": f"Rule {rule_id} not found."}), 404
        return jsonify(rule)

    @app.route("/api/metrics")
    def api_get_metrics():
        """Fetch dashboard metrics as JSON."""
        return jsonify(gov_db.get_dashboard_metrics())

    @app.route("/api/pilot/run", methods=["POST"])
    def api_run_pilot():
        """Trigger execution of full Phase 3D pilot evaluation runner."""
        try:
            from medrule_engine.pilot.run_pilot import run_pilot
            summary = run_pilot()
            return jsonify({"status": "success", "summary": summary})
        except Exception as e:
            logger.exception("Error executing pilot run:")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/pilot/evaluations")
    def api_get_pilot_evaluations():
        """Fetch pilot evaluations with optional domain filter as JSON."""
        dom = request.args.get("domain")
        return jsonify(gov_db.get_pilot_evaluations(domain=dom))

    return app


if __name__ == "__main__":
    app = create_app()
    print("=" * 70)
    print("MEDRULE CLINICAL SME REVIEW WORKFLOW INTERFACE RUNNING AT:")
    print("http://127.0.0.1:5000")
    print("=" * 70)
    app.run(host="127.0.0.1", port=5000, debug=True)
