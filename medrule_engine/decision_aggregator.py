"""MedRule Decision Aggregation Module.

Combines rule-level three-valued condition outcomes, evidence verification reports,
and governance constraints into a case-level assessment. Enforces non-binding
prototype status, escalation of human-review rules, and preservation of uncertainty.
"""

from dataclasses import dataclass, field
from enum import Enum
import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from medrule_engine.condition_evaluator import ConditionGroupEvaluation, EvaluationState
from medrule_engine.evidence_validator import EvidenceVerificationReport
from medrule_engine.rule_registry import RuleRecord

logger = logging.getLogger(__name__)


class CaseAssessmentStatus(str, Enum):
    """Case-level deterministic assessment statuses (non-binding software assessments)."""
    CRITERIA_MET = "CRITERIA_MET"
    CRITERIA_NOT_MET = "CRITERIA_NOT_MET"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    POLICY_NOT_APPLICABLE = "POLICY_NOT_APPLICABLE"
    POLICY_VERSION_UNRESOLVED = "POLICY_VERSION_UNRESOLVED"
    EVALUATION_ERROR = "EVALUATION_ERROR"

    def __repr__(self) -> str:
        return self.value


@dataclass
class RuleEvaluationResult:
    """Consolidated outcome for an individual evaluated rule."""
    rule: RuleRecord
    condition_result: ConditionGroupEvaluation
    evidence_report: EvidenceVerificationReport
    requires_human_review: bool
    is_applicable: bool
    notes: List[str] = field(default_factory=list)


@dataclass
class CaseAssessment:
    """Final aggregated deterministic case assessment."""
    assessment_status: CaseAssessmentStatus
    is_binding: bool
    summary_explanation: str
    rule_results: List[RuleEvaluationResult]
    human_review_escalations: List[str]
    missing_evidence_summary: List[str]
    conflicts_or_unresolved_dependencies: List[str]
    disclaimer: str = (
        "NON-BINDING PROTOTYPE EVALUATION: THIS EVALUATION IS A DETERMINISTIC RESEARCH PROTOTYPE FOR TESTING PURPOSES ONLY. "
        "NO REAL-WORLD AUTHORIZATION APPROVAL OR DENIAL IS EXECUTED. "
        "RULES ARE IN DRAFT/TESTING STATUS AWAITING CLINICAL SME REVIEW."
    )


class DecisionAggregator:
    """Aggregates rule-level evaluation outcomes into case-level determination."""

    def aggregate(
        self,
        rule_results: List[RuleEvaluationResult],
        router_status: Optional[str] = None,
        router_notes: Optional[List[str]] = None,
        unresolved_dependencies: Optional[List[str]] = None
    ) -> CaseAssessment:
        """Deterministically aggregate rule results."""
        human_review_escalations: List[str] = []
        missing_evidence: List[str] = []
        unresolved_deps: List[str] = list(unresolved_dependencies or [])

        # 1. Check router-level issues
        if router_status == "POLICY_NOT_APPLICABLE":
            return CaseAssessment(
                assessment_status=CaseAssessmentStatus.POLICY_NOT_APPLICABLE,
                is_binding=False,
                summary_explanation="No governing policy or applicable clinical rules matched the requested procedure/modality.",
                rule_results=rule_results,
                human_review_escalations=[],
                missing_evidence_summary=[],
                conflicts_or_unresolved_dependencies=router_notes or []
            )

        if router_status == "POLICY_VERSION_UNRESOLVED":
            return CaseAssessment(
                assessment_status=CaseAssessmentStatus.POLICY_VERSION_UNRESOLVED,
                is_binding=False,
                summary_explanation="The requested date of service does not align with active policy version effective boundaries.",
                rule_results=rule_results,
                human_review_escalations=[],
                missing_evidence_summary=[],
                conflicts_or_unresolved_dependencies=router_notes or []
            )

        if router_status == "MANUAL_REVIEW_REQUIRED":
            return CaseAssessment(
                assessment_status=CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED,
                is_binding=False,
                summary_explanation="Routing encountered unresolvable line of business or regulatory prerequisites requiring clinical review.",
                rule_results=rule_results,
                human_review_escalations=["Policy routing triggered manual review."],
                missing_evidence_summary=[],
                conflicts_or_unresolved_dependencies=router_notes or []
            )

        if not rule_results:
            return CaseAssessment(
                assessment_status=CaseAssessmentStatus.POLICY_NOT_APPLICABLE,
                is_binding=False,
                summary_explanation="No candidate rules evaluated for this case.",
                rule_results=[],
                human_review_escalations=[],
                missing_evidence_summary=[],
                conflicts_or_unresolved_dependencies=[]
            )

        # 2. Inspect rule outcomes
        has_false = False
        has_unknown = False
        all_true = True
        false_reasons: List[str] = []
        unknown_reasons: List[str] = []

        for rr in rule_results:
            rule_id = rr.rule.rule_id
            st = rr.condition_result.status

            # Collect missing evidence
            if rr.evidence_report.missing_parameters:
                for p in rr.evidence_report.missing_parameters:
                    item = f"Rule {rule_id}: Parameter '{p}' is missing"
                    if item not in missing_evidence:
                        missing_evidence.append(item)

            if rr.evidence_report.missing_documentation:
                for d in rr.evidence_report.missing_documentation:
                    item = f"Rule {rule_id}: Documentation '{d}' is missing"
                    if item not in missing_evidence:
                        missing_evidence.append(item)

            # Check human review requirement
            if rr.requires_human_review:
                human_review_escalations.append(
                    f"Rule {rule_id} is flagged '{rr.rule.extraction_status}': "
                    f"{rr.rule.review_notes or 'Requires clinical medical director discretion.'}"
                )

            # Evaluate state
            if st == EvaluationState.FALSE:
                has_false = True
                all_true = False
                false_reasons.append(f"Rule {rule_id} ({rr.rule.clinical_service_or_procedure}) not satisfied: {rr.condition_result.explanation}")
            elif st == EvaluationState.UNKNOWN:
                has_unknown = True
                all_true = False
                unknown_reasons.append(f"Rule {rule_id} ({rr.rule.clinical_service_or_procedure}) inconclusive: {rr.condition_result.explanation}")

        # 3. Determine aggregated status
        # Order of precedence:
        # A. If mandatory human review rule is triggered -> MANUAL_REVIEW_REQUIRED
        # B. If a condition is definitively FALSE -> CRITERIA_NOT_MET
        # C. If any condition is UNKNOWN -> INSUFFICIENT_INFORMATION
        # D. If all conditions are TRUE -> CRITERIA_MET
        if human_review_escalations:
            status = CaseAssessmentStatus.MANUAL_REVIEW_REQUIRED
            explanation = (
                f"Case escalated to clinical manual review: {len(human_review_escalations)} applicable rule(s) "
                "require clinical discretion, interpretation of ambiguous criteria, or plan carve-out review."
            )
        elif has_false:
            status = CaseAssessmentStatus.CRITERIA_NOT_MET
            explanation = f"Clinical criteria not satisfied: {'; '.join(false_reasons[:3])}"
        elif has_unknown:
            status = CaseAssessmentStatus.INSUFFICIENT_INFORMATION
            explanation = (
                f"Insufficient clinical information to determine criteria fulfillment: "
                f"{len(missing_evidence)} evidence/documentation item(s) missing. ({'; '.join(unknown_reasons[:2])})"
            )
        elif all_true:
            status = CaseAssessmentStatus.CRITERIA_MET
            explanation = (
                f"All {len(rule_results)} applicable deterministic rule condition(s) satisfied by provided evidence. "
                "(Note: Testing evaluation only; non-binding authorization assessment)."
            )
        else:
            status = CaseAssessmentStatus.EVALUATION_ERROR
            explanation = "Unexpected logical state during decision aggregation."

        return CaseAssessment(
            assessment_status=status,
            is_binding=False,
            summary_explanation=explanation,
            rule_results=rule_results,
            human_review_escalations=human_review_escalations,
            missing_evidence_summary=missing_evidence,
            conflicts_or_unresolved_dependencies=unresolved_deps
        )
