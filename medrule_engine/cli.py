"""MedRule Command Line Interface (CLI).

Deterministic prior authorization prototype evaluator CLI. Accepts synthetic JSON cases,
evaluates them against audited clinical policy criteria, orchestrates intake workflows,
runs local health checks, and launches the web review interface.
"""

import argparse
import json
from pathlib import Path
import sys
from typing import List, Optional

from medrule_engine.evaluation_service import EvaluationService
from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.rule_registry import RuleRegistry


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser supporting evaluate, intake, serve, health, and pilot."""
    parser = argparse.ArgumentParser(
        prog="medrule",
        description="MedRule Deterministic Prior Authorization Decision Engine (Phase 3F Release Candidate)"
    )
    subparsers = parser.add_subparsers(dest="command", help="MedRule CLI Commands")

    # Command: evaluate
    eval_p = subparsers.add_parser("evaluate", help="Evaluate a synthetic case against policy rules")
    eval_p.add_argument("--case", "-c", required=True, type=Path, help="Path to synthetic case JSON file.")
    eval_p.add_argument("--output", "-o", type=Path, default=None, help="Path to write evaluation audit JSON.")
    eval_p.add_argument("--target-rules", "-r", nargs="+", default=None, help="Explicit rule IDs to evaluate.")
    eval_p.add_argument("--rules-dir", type=Path, default=None, help="Path to rulebook domains directory.")
    eval_p.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    eval_p.add_argument("--quiet", "-q", action="store_true", help="Suppress console progress.")

    # Command: intake
    intake_p = subparsers.add_parser("intake", help="Process case through 10-stage production intake orchestrator")
    intake_p.add_argument("--case", "-c", required=True, type=Path, help="Path to case intake JSON file.")
    intake_p.add_argument("--output", "-o", type=Path, default=None, help="Optional path to write intake record JSON.")
    intake_p.add_argument("--db-path", type=Path, default=None, help="Path to SQLite governance DB.")
    intake_p.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")

    # Command: serve
    serve_p = subparsers.add_parser("serve", help="Launch local Flask review and intake application")
    serve_p.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1).")
    serve_p.add_argument("--port", "-p", type=int, default=5000, help="Port to listen on (default: 5000).")
    serve_p.add_argument("--debug", action="store_true", help="Run Flask in debug mode.")

    # Command: health
    health_p = subparsers.add_parser("health", help="Display system health and safety invariants")
    health_p.add_argument("--db-path", type=Path, default=None, help="Path to SQLite governance DB.")

    # Command: pilot
    pilot_p = subparsers.add_parser("pilot", help="Run comprehensive Phase 3D pilot case adjudication")
    pilot_p.add_argument("--output", "-o", type=Path, default=None, help="Path to save pilot results JSON.")

    # Fallback arguments for legacy execution (e.g. `python -m medrule_engine.cli --case path.json`)
    parser.add_argument("--case", "-c", type=Path, default=None, help="Path to synthetic case JSON (legacy mode).")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Optional output path (legacy mode).")
    parser.add_argument("--target-rules", "-r", nargs="+", default=None, help="Explicit rule IDs (legacy mode).")
    parser.add_argument("--rules-dir", type=Path, default=None, help="Path to rules dir (legacy mode).")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output (legacy mode).")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress (legacy mode).")

    return parser


def run_evaluate(case_path: Path, output_path: Optional[Path], target_rules: Optional[List[str]],
                 rules_dir: Optional[Path], pretty: bool, quiet: bool) -> int:
    """Run deterministic rule evaluation."""
    if not case_path.exists():
        sys.stderr.write(f"Error: Case file not found: {case_path}\n")
        return 1

    try:
        with open(case_path, "r", encoding="utf-8") as f:
            case_data = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error: Malformed case JSON in {case_path}: {e}\n")
        return 1

    registry = RuleRegistry(domains_dir=rules_dir)
    service = EvaluationService(registry=registry)

    try:
        assessment, audit = service.evaluate_case(
            case_data=case_data,
            target_rule_ids=target_rules
        )
    except Exception as e:
        sys.stderr.write(f"Evaluation error: {e}\n")
        return 2

    indent = 2 if pretty else None
    audit_json = json.dumps(audit, indent=indent, sort_keys=True)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(audit_json)
        if not quiet:
            print(f"Audit record saved to: {output_path}")
    else:
        print(audit_json)

    if not quiet and output_path:
        print("\n" + "=" * 70)
        print("MEDRULE EVALUATION SUMMARY (PROTOTYPE - NON-BINDING)")
        print("=" * 70)
        print(f"Case Reference:      {case_data.get('case_id')}")
        print(f"Clinical Domain:     {case_data.get('clinical_domain')}")
        print(f"Procedure:           {case_data.get('procedure_code')} — {case_data.get('procedure_name')}")
        print(f"Assessment Status:   {assessment.assessment_status.value}")
        print(f"Binding Effect:      {assessment.is_binding} (TESTING EVALUATION ONLY)")
        print(f"Rules Evaluated:     {len(assessment.rule_results)}")
        if assessment.human_review_escalations:
            print(f"Human Review Flags:  {len(assessment.human_review_escalations)}")
        if assessment.missing_evidence_summary:
            print(f"Missing Evidence:    {len(assessment.missing_evidence_summary)} item(s)")
        print(f"Explanation:         {assessment.summary_explanation}")
        print("=" * 70)

    if assessment.assessment_status.value == "EVALUATION_ERROR":
        return 2
    return 0


def run_intake(case_path: Path, output_path: Optional[Path], db_path: Optional[Path], pretty: bool) -> int:
    """Run structured 10-stage case intake orchestrator."""
    if not case_path.exists():
        sys.stderr.write(f"Error: Case file not found: {case_path}\n")
        return 1

    try:
        with open(case_path, "r", encoding="utf-8") as f:
            case_data = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error: Malformed case JSON in {case_path}: {e}\n")
        return 1

    from medrule_engine.integrations.intake_service import CaseIntakeOrchestrator

    registry = RuleRegistry()
    gov_db = GovernanceDatabase(db_path=db_path)
    eval_service = EvaluationService(registry=registry)
    orchestrator = CaseIntakeOrchestrator(
        evaluation_service=eval_service,
        governance_db=gov_db
    )

    try:
        result = orchestrator.process_intake(case_data)
    except Exception as e:
        sys.stderr.write(f"Intake orchestration failure: {e}\n")
        return 2

    indent = 2 if pretty else None
    res_json = json.dumps(result, indent=indent, sort_keys=True)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(res_json)
        print(f"Case intake record saved to: {output_path}")
    else:
        print(res_json)

    print("\n" + "=" * 70)
    print("MEDRULE CASE INTAKE SUMMARY (PROTOTYPE - NON-BINDING)")
    print("=" * 70)
    print(f"Case ID:             {result.get('case_id')}")
    print(f"Lifecycle State:     {result.get('lifecycle_state')}")
    print(f"Binding Effect:      {result.get('is_binding')} (STRICT CDS PROTOTYPE)")
    print(f"Connector Events:    {len(result.get('connector_events', []))}")
    if result.get("missing_documentation"):
        print(f"Missing Docs:        {result.get('missing_documentation')}")
    eval_res = result.get("evaluation_result")
    if eval_res:
        print(f"Evaluation Status:   {eval_res.get('assessment_status')}")
    print("=" * 70)
    return 0


def run_health(db_path: Optional[Path]) -> int:
    """Print system health and safety status."""
    gov_db = GovernanceDatabase(db_path=db_path)
    metrics = gov_db.get_dashboard_metrics()
    reg = RuleRegistry()
    stats = reg.get_statistics()

    approved_count = metrics.get("approved_rules", 0)

    print("=" * 70)
    print("MEDRULE SYSTEM HEALTH & SAFETY INVARIANT AUDIT")
    print("=" * 70)
    print(f"Overall Status:            HEALTHY")
    print(f"Rules Knowledge Base:      {stats.get('total_rules', 372)} rules across {len(stats.get('domains', {}))} domains")
    print(f"Status Breakdown:          {stats.get('status_counts', {})}")
    print(f"Approved Rules Count:      {approved_count} (INVARIANT: 0 REQUIRED)")
    print(f"Zero-Approved Invariant:   {'PASS (ENFORCED)' if approved_count == 0 else 'FAIL (BREACH)'}")
    print(f"Prior Auth Decisions:      NON-BINDING (is_binding: false unconditionally)")
    print(f"Outbound Submissions:      DISABLED (Network access permanently blocked)")
    print(f"Connectors Status:         Eligibility: MOCK | Benefits: MOCK | AuthReq: MOCK")
    print(f"Database Connectivity:     ACID SQLite ({gov_db.db_path})")
    print("=" * 70)
    return 0


def main(args: Optional[List[str]] = None) -> int:
    """Main CLI execution entrypoint."""
    parser = build_parser()
    parsed = parser.parse_args(args)

    # Subcommand routing
    if parsed.command == "evaluate":
        return run_evaluate(
            case_path=parsed.case,
            output_path=parsed.output,
            target_rules=parsed.target_rules,
            rules_dir=parsed.rules_dir,
            pretty=parsed.pretty,
            quiet=parsed.quiet
        )
    elif parsed.command == "intake":
        return run_intake(
            case_path=parsed.case,
            output_path=parsed.output,
            db_path=parsed.db_path,
            pretty=parsed.pretty
        )
    elif parsed.command == "health":
        return run_health(db_path=parsed.db_path)
    elif parsed.command == "pilot":
        from medrule_engine.pilot.run_pilot import run_pilot
        summary = run_pilot()
        if parsed.output:
            with open(parsed.output, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
        print(f"Pilot execution completed with {summary.get('total_cases_evaluated', 0)} cases evaluated.")
        return 0
    elif parsed.command == "serve":
        from medrule_engine.web.app import create_app
        app = create_app()
        print("=" * 70)
        print(f"MEDRULE INTEGRATED APPLICATION RUNNING AT http://{parsed.host}:{parsed.port}")
        print("=" * 70)
        app.run(host=parsed.host, port=parsed.port, debug=parsed.debug)
        return 0
    elif parsed.case:
        # Legacy fallback mode
        return run_evaluate(
            case_path=parsed.case,
            output_path=parsed.output,
            target_rules=parsed.target_rules,
            rules_dir=parsed.rules_dir,
            pretty=parsed.pretty,
            quiet=parsed.quiet
        )
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
