"""MedRule Audit Logger Module.

Formats structured, reproducible JSON audit trails for every case evaluation.
Captures exact policy and rule versions, condition logic trees, verbatim quotes,
evidence parameters, human-review escalations, and deterministic result hashes.
"""

from dataclasses import asdict
import datetime
import hashlib
import json
from typing import Any, Dict, List, Optional

from medrule_engine.case_validator import CaseIntake
from medrule_engine.decision_aggregator import CaseAssessment, RuleEvaluationResult
from medrule_engine.policy_router import RoutingResult

EVALUATOR_VERSION = "3A.1.0"
INPUT_SCHEMA_VERSION = "1.0.0"
RULESET_VERSION = "2026.1-AUDITED"


class AuditLogger:
    """Produces structured, auditable evaluation records."""

    def build_audit_record(
        self,
        case: CaseIntake,
        routing_result: RoutingResult,
        assessment: CaseAssessment,
        evaluation_timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """Construct deterministic audit dictionary."""
        timestamp = evaluation_timestamp or datetime.datetime.now(datetime.timezone.utc).isoformat()

        rule_evals: List[Dict[str, Any]] = []
        for rr in assessment.rule_results:
            rule = rr.rule
            cond_res = rr.condition_result
            ev_rep = rr.evidence_report

            criteria_details = []
            for cr in cond_res.criteria_results:
                crit_dict = {
                    "condition_id": cr.condition_id,
                    "description": cr.description,
                    "parameter": cr.parameter,
                    "comparator": cr.comparator,
                    "expected_value": cr.expected_value,
                    "actual_value": cr.actual_value,
                    "status": cr.status.value,
                    "criterion_state": cr.criterion_state.value if hasattr(cr, "criterion_state") and cr.criterion_state else None,
                    "evidence_state": cr.evidence_state.value if hasattr(cr, "evidence_state") and cr.evidence_state else None,
                    "evidence_snippet": getattr(cr, "evidence_snippet", None),
                    "reason": cr.reason,
                    "is_optional": cr.is_optional,
                    "evidence_missing": cr.evidence_missing,
                    "type_error": cr.type_error
                }
                if cr.sub_evaluations:
                    crit_dict["sub_evaluations"] = [
                        {
                            "condition_id": sub.condition_id,
                            "description": sub.description,
                            "parameter": sub.parameter,
                            "comparator": sub.comparator,
                            "status": sub.status.value,
                            "criterion_state": sub.criterion_state.value if hasattr(sub, "criterion_state") and sub.criterion_state else None,
                            "evidence_state": sub.evidence_state.value if hasattr(sub, "evidence_state") and sub.evidence_state else None,
                            "evidence_snippet": getattr(sub, "evidence_snippet", None),
                            "reason": sub.reason
                        }
                        for sub in cr.sub_evaluations
                    ]
                criteria_details.append(crit_dict)

            rule_evals.append({
                "rule_id": rule.rule_id,
                "domain": rule.domain,
                "extraction_status": rule.extraction_status,
                "decision_effect": rule.decision_effect,
                "policy_provenance": {
                    "policy_title": rule.policy_title,
                    "policy_version": rule.policy_version,
                    "version_status": rule.version_status,
                    "source_file": rule.source_file,
                    "physical_page": rule.physical_page,
                    "source_section": rule.source_section,
                    "source_quote": rule.source_quote
                },
                "condition_evaluation": {
                    "operator": cond_res.operator,
                    "status": cond_res.status.value,
                    "short_circuited": cond_res.short_circuited,
                    "explanation": cond_res.explanation,
                    "criteria": criteria_details
                },
                "evidence_verification": {
                    "required_parameters": ev_rep.required_parameters,
                    "provided_parameters": ev_rep.provided_parameters,
                    "missing_parameters": ev_rep.missing_parameters,
                    "type_errors": ev_rep.type_errors,
                    "is_sufficient": ev_rep.is_sufficient,
                    "missing_documentation": ev_rep.missing_documentation
                },
                "requires_human_review": rr.requires_human_review,
                "is_binding": rule.is_binding
            })

        record: Dict[str, Any] = {
            "audit_header": {
                "evaluator_name": "MedRule Deterministic Decision Engine",
                "evaluator_version": EVALUATOR_VERSION,
                "input_schema_version": INPUT_SCHEMA_VERSION,
                "ruleset_version": RULESET_VERSION,
                "evaluation_timestamp": timestamp,
                "is_binding_adjudication": False,
                "disclaimer": assessment.disclaimer
            },
            "case_metadata": {
                "case_id": case.case_id,
                "clinical_domain": case.clinical_domain,
                "procedure_code": case.procedure_code,
                "procedure_name": case.procedure_name,
                "modality": case.modality,
                "place_of_service": case.place_of_service,
                "primary_diagnosis_code": case.primary_diagnosis_code,
                "line_of_business": case.line_of_business,
                "payer_id": case.payer_id,
                "plan_id": case.plan_id,
                "jurisdiction": case.jurisdiction,
                "requested_date_of_service": case.requested_date_of_service
            },
            "routing_summary": {
                "routing_status": routing_result.status,
                "selected_policies": routing_result.selected_policies,
                "applicable_rule_ids": [r.rule_id for r in routing_result.applicable_rules],
                "excluded_rules": [
                    {"rule_id": rid, "reason": rsn} for rid, rsn in routing_result.excluded_rules
                ],
                "routing_notes": routing_result.routing_notes
            },
            "case_assessment": {
                "assessment_status": assessment.assessment_status.value,
                "is_binding": assessment.is_binding,
                "summary_explanation": assessment.summary_explanation,
                "human_review_escalations": assessment.human_review_escalations,
                "missing_evidence_summary": assessment.missing_evidence_summary,
                "conflicts_or_unresolved_dependencies": assessment.conflicts_or_unresolved_dependencies
            },
            "rule_evaluations": rule_evals
        }

        # Calculate reproducible SHA-256 hash of the normalized record (excluding timestamp for repeatable hash check)
        hashable_content = dict(record)
        hashable_meta = dict(hashable_content["audit_header"])
        hashable_meta["evaluation_timestamp"] = "NORMALIZED_FOR_REPRODUCIBILITY"
        hashable_content["audit_header"] = hashable_meta
        
        canon_json = json.dumps(hashable_content, sort_keys=True)
        record["reproducibility_hash_sha256"] = hashlib.sha256(canon_json.encode("utf-8")).hexdigest()

        return record
