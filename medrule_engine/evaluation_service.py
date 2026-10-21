"""MedRule Evaluation Service Module.

Primary programmatic interface for deterministic case and rule evaluation.
Coordinates intake validation, policy routing, condition tree evaluation,
evidence auditing, decision aggregation, and audit logging.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from medrule_engine.audit_logger import AuditLogger
from medrule_engine.case_validator import CaseIntake, CaseValidator
from medrule_engine.condition_evaluator import ConditionEvaluator, EvaluationState
from medrule_engine.decision_aggregator import CaseAssessment, CaseAssessmentStatus, DecisionAggregator, RuleEvaluationResult
from medrule_engine.decision_tree import DecisionTreeAssessment, DecisionTreeEngine
from medrule_engine.evidence_validator import EvidenceValidator
from medrule_engine.policy_router import PolicyRouter, RoutingResult
from medrule_engine.rule_registry import RuleRecord, RuleRegistry

logger = logging.getLogger(__name__)


class EvaluationService:
    """Service orchestrating deterministic prior authorization evaluation."""

    def __init__(
        self,
        registry: Optional[RuleRegistry] = None,
        validator: Optional[CaseValidator] = None,
        router: Optional[PolicyRouter] = None,
        evaluator: Optional[ConditionEvaluator] = None,
        evidence_auditor: Optional[EvidenceValidator] = None,
        aggregator: Optional[DecisionAggregator] = None,
        logger_: Optional[AuditLogger] = None
    ):
        self.registry = registry or RuleRegistry()
        self.validator = validator or CaseValidator()
        self.router = router or PolicyRouter(self.registry)
        self.evaluator = evaluator or ConditionEvaluator()
        self.evidence_auditor = evidence_auditor or EvidenceValidator()
        self.aggregator = aggregator or DecisionAggregator()
        self.audit_logger = logger_ or AuditLogger()
        self.tree_engine = DecisionTreeEngine(
            registry=self.registry,
            validator=self.validator,
            router=self.router,
            evaluator=self.evaluator,
            evidence_auditor=self.evidence_auditor
        )

    def evaluate_rule(
        self,
        case_data: Union[Dict[str, Any], CaseIntake],
        rule: Union[Dict[str, Any], RuleRecord],
        policy_context: Optional[Dict[str, Any]] = None
    ) -> RuleEvaluationResult:
        """Evaluate a single rule against a case.

        Args:
            case_data: Raw dictionary or validated CaseIntake.
            rule: Raw dictionary or RuleRecord.
            policy_context: Optional contextual parameters.

        Returns:
            RuleEvaluationResult
        """
        # 1. Normalize case
        if isinstance(case_data, CaseIntake):
            case = case_data
        else:
            is_valid, errs, case_obj = self.validator.validate(case_data)
            if not is_valid or not case_obj:
                raise ValueError(f"Invalid case data for rule evaluation: {'; '.join(errs)}")
            case = case_obj

        # 2. Normalize rule
        if isinstance(rule, RuleRecord):
            rule_rec = rule
        else:
            # Look up or build transient record
            rid = rule.get("rule_id", "TRANSIENT_RULE")
            existing = self.registry.get_rule(rid)
            if existing:
                rule_rec = existing
            else:
                rule_rec = RuleRecord(
                    rule_id=rid,
                    domain=rule.get("domain", case.clinical_domain),
                    document_type=rule.get("document_type", "transient"),
                    policy_title=rule.get("policy_title", "Custom/Test Policy"),
                    policy_version=rule.get("policy_version", "1.0"),
                    version_status=rule.get("version_status", "current_2026_verified"),
                    source_file=rule.get("source_file", ""),
                    physical_page=1,
                    source_section=rule.get("source_section", ""),
                    source_quote=rule.get("source_quote", ""),
                    clinical_service_or_procedure=rule.get("clinical_service_or_procedure", case.procedure_name),
                    rule_type=rule.get("rule_type", "clinical_indication"),
                    conditions=rule.get("conditions", {}),
                    decision_effect=rule.get("decision_effect", "INDICATED"),
                    missing_information_behavior=rule.get("missing_information_behavior", "CANNOT_DETERMINE"),
                    human_review_required=bool(rule.get("human_review_required", False) or rule.get("extraction_status") == "NEEDS_HUMAN_REVIEW"),
                    extraction_status=rule.get("extraction_status", "DRAFT"),
                    review_notes=rule.get("review_notes"),
                    raw_data=rule
                )

        # 3. Evidence verification
        ev_report = self.evidence_auditor.verify_rule_evidence(rule_rec, case)

        # 4. Condition evaluation
        cond_eval = self.evaluator.evaluate(rule_rec.conditions, case)

        # Check governance status from registry
        gov_status = self.registry.get_governance_status(rule_rec.rule_id)
        requires_hr = bool(
            rule_rec.human_review_required or
            gov_status in ("IN_REVIEW", "NEEDS_CORRECTION", "READY_FOR_MEDICAL_DIRECTOR", "FLAGGED_CONFLICT")
        )

        return RuleEvaluationResult(
            rule=rule_rec,
            condition_result=cond_eval,
            evidence_report=ev_report,
            requires_human_review=requires_hr,
            is_applicable=True,
            notes=[]
        )

    def evaluate_case(
        self,
        case_data: Union[Dict[str, Any], CaseIntake],
        applicable_rules: Optional[List[Union[Dict[str, Any], RuleRecord]]] = None,
        policy_context: Optional[Dict[str, Any]] = None,
        target_rule_ids: Optional[List[str]] = None
    ) -> Tuple[CaseAssessment, Dict[str, Any]]:
        """Evaluate a case against applicable policy rules.

        Returns:
            Tuple[CaseAssessment, Dict[str, Any]]: (strongly_typed_assessment, structured_audit_record)
        """
        # 1. Validate case
        if isinstance(case_data, CaseIntake):
            case = case_data
        else:
            is_valid, errs, case_obj = self.validator.validate(case_data)
            if not is_valid or not case_obj:
                # Return evaluation error assessment
                assessment = CaseAssessment(
                    assessment_status=CaseAssessmentStatus.EVALUATION_ERROR,
                    is_binding=False,
                    summary_explanation=f"Case validation rejected: {'; '.join(errs)}",
                    rule_results=[],
                    human_review_escalations=[],
                    missing_evidence_summary=[],
                    conflicts_or_unresolved_dependencies=errs
                )
                dummy_case = CaseIntake(
                    case_id=case_data.get("case_id", "MALFORMED_CASE"),
                    clinical_domain=case_data.get("clinical_domain", "UNKNOWN"),
                    procedure_code=case_data.get("procedure_code", "UNKNOWN"),
                    procedure_name=case_data.get("procedure_name", "UNKNOWN"),
                    requested_date_of_service=case_data.get("requested_date_of_service", "2026-01-01"),
                    line_of_business=case_data.get("line_of_business", "UNKNOWN"),
                    payer_id=case_data.get("payer_id", "UNKNOWN"),
                    clinical_evidence={}
                )
                routing = RoutingResult(status="EVALUATION_ERROR", routing_notes=errs)
                audit = self.audit_logger.build_audit_record(dummy_case, routing, assessment)
                return assessment, audit
            case = case_obj

        # 2. Determine routing and candidate rules
        if applicable_rules is not None:
            if len(applicable_rules) == 0:
                routing = RoutingResult(
                    status="POLICY_NOT_APPLICABLE",
                    routing_notes=["Empty or unavailable applicable rule set provided."]
                )
            else:
                rule_records: List[RuleRecord] = []
                for r in applicable_rules:
                    if isinstance(r, RuleRecord):
                        rule_records.append(r)
                    else:
                        rule_res = self.evaluate_rule(case, r).rule
                        rule_records.append(rule_res)
                routing = RoutingResult(
                    status="ROUTED",
                    applicable_rules=rule_records,
                    routing_notes=["Applicable rules explicitly supplied by caller."]
                )
        else:
            routing = self.router.route_case(case, target_rule_ids=target_rule_ids, policy_context=policy_context)

        if routing.status != "ROUTED":
            assessment = self.aggregator.aggregate(
                [],
                router_status=routing.status,
                router_notes=routing.routing_notes,
                unresolved_dependencies=routing.unresolved_dependencies
            )
            audit = self.audit_logger.build_audit_record(case, routing, assessment)
            return assessment, audit

        # 3. Evaluate each applicable rule
        rule_results: List[RuleEvaluationResult] = []
        for r_rec in routing.applicable_rules:
            r_eval = self.evaluate_rule(case, r_rec, policy_context)
            rule_results.append(r_eval)

        # 4. Aggregate results
        assessment = self.aggregator.aggregate(
            rule_results,
            router_status=routing.status,
            router_notes=routing.routing_notes,
            unresolved_dependencies=routing.unresolved_dependencies
        )

        # 5. Build auditable output
        audit = self.audit_logger.build_audit_record(case, routing, assessment)

        return assessment, audit

    def evaluate_batch(
        self,
        cases: List[Union[Dict[str, Any], CaseIntake]],
        policy_context: Optional[Dict[str, Any]] = None,
        target_rule_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Evaluate a batch of cases independently with per-case error isolation.

        Returns:
            Dict containing batch statistics and per-case results.
        """
        case_results: List[Dict[str, Any]] = []
        status_dist: Dict[str, int] = {}
        validation_failures = 0
        successful = 0
        escalations = 0

        for idx, c in enumerate(cases):
            case_id = c.get("case_id", f"BATCH_CASE_{idx+1}") if isinstance(c, dict) else c.case_id
            try:
                assessment, audit = self.evaluate_case(
                    c,
                    policy_context=policy_context,
                    target_rule_ids=target_rule_ids
                )
                st_val = assessment.assessment_status.value
                status_dist[st_val] = status_dist.get(st_val, 0) + 1
                if st_val == CaseAssessmentStatus.EVALUATION_ERROR.value:
                    validation_failures += 1
                else:
                    successful += 1

                if assessment.human_review_escalations:
                    escalations += 1

                case_results.append({
                    "case_id": case_id,
                    "assessment_status": st_val,
                    "is_binding": assessment.is_binding,
                    "summary_explanation": assessment.summary_explanation,
                    "human_review_escalations": assessment.human_review_escalations,
                    "missing_evidence_summary": assessment.missing_evidence_summary,
                    "reproducibility_hash_sha256": audit.get("reproducibility_hash_sha256"),
                    "audit_record": audit,
                    "error": None
                })
            except Exception as ex:
                logger.exception(f"Unhandled exception in batch processing for case {case_id}")
                validation_failures += 1
                status_dist["EVALUATION_ERROR"] = status_dist.get("EVALUATION_ERROR", 0) + 1
                case_results.append({
                    "case_id": case_id,
                    "assessment_status": "EVALUATION_ERROR",
                    "is_binding": False,
                    "summary_explanation": f"Unhandled execution error: {str(ex)}",
                    "human_review_escalations": [],
                    "missing_evidence_summary": [],
                    "reproducibility_hash_sha256": None,
                    "audit_record": None,
                    "error": str(ex)
                })

        return {
            "total_cases": len(cases),
            "successful_evaluations": successful,
            "validation_failures": validation_failures,
            "escalations_count": escalations,
            "status_distribution": status_dist,
            "case_results": case_results
        }


    def evaluate_decision_tree(
        self,
        case_data: Union[Dict[str, Any], CaseIntake],
        target_rule_ids: Optional[List[str]] = None,
        policy_context: Optional[Dict[str, Any]] = None
    ) -> DecisionTreeAssessment:
        """Evaluate a case deterministically using the compiled decision tree."""
        return self.tree_engine.evaluate(case_data, target_rule_ids=target_rule_ids, policy_context=policy_context)


# Global instance for quick functional imports
_DEFAULT_SERVICE = EvaluationService()


def evaluate_rule(
    case_data: Union[Dict[str, Any], CaseIntake],
    rule: Union[Dict[str, Any], RuleRecord],
    policy_context: Optional[Dict[str, Any]] = None
) -> RuleEvaluationResult:
    """Functional interface for single-rule evaluation."""
    return _DEFAULT_SERVICE.evaluate_rule(case_data, rule, policy_context)


def evaluate_case(
    case_data: Union[Dict[str, Any], CaseIntake],
    applicable_rules: Optional[List[Union[Dict[str, Any], RuleRecord]]] = None,
    policy_context: Optional[Dict[str, Any]] = None,
    target_rule_ids: Optional[List[str]] = None
) -> Tuple[CaseAssessment, Dict[str, Any]]:
    """Functional interface for complete case evaluation."""
    return _DEFAULT_SERVICE.evaluate_case(case_data, applicable_rules, policy_context, target_rule_ids)


def evaluate_batch(
    cases: List[Union[Dict[str, Any], CaseIntake]],
    policy_context: Optional[Dict[str, Any]] = None,
    target_rule_ids: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Functional interface for batch evaluation."""
    return _DEFAULT_SERVICE.evaluate_batch(cases, policy_context, target_rule_ids)


def evaluate_decision_tree(
    case_data: Union[Dict[str, Any], CaseIntake],
    target_rule_ids: Optional[List[str]] = None,
    policy_context: Optional[Dict[str, Any]] = None
) -> DecisionTreeAssessment:
    """Functional interface for deterministic decision-tree evaluation."""
    return _DEFAULT_SERVICE.evaluate_decision_tree(case_data, target_rule_ids, policy_context)

