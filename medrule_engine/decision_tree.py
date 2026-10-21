"""MedRule Deterministic Decision-Tree Module.

Compiles and executes deterministic decision trees for MedRule clinical rules.
Maintains strict separation between Clinical Necessity and Place of Service,
enforces the 7 NEEDS_HUMAN_REVIEW governance blockage gates, handles three-valued logic
(TRUE, FALSE, UNKNOWN), executes quantitative and temporal boundary checks,
tracks criterion-level provenance, and prevents unsupported approvals or denials.
"""

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import logging
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from medrule_engine.case_validator import CaseIntake, CaseValidator
from medrule_engine.condition_evaluator import (
    ConditionEvaluator,
    ConditionGroupEvaluation,
    CriterionEvaluation,
    EvaluationState,
)
from medrule_engine.evidence_validator import EvidenceValidator
from medrule_engine.policy_router import PolicyRouter, RoutingResult
from medrule_engine.rule_registry import RuleRecord, RuleRegistry

logger = logging.getLogger(__name__)

# The 7 rules strictly blocked from autonomous decision execution by governance
GOVERNANCE_BLOCKED_RULE_IDS: Set[str] = {
    "RULE-ADV-PREAMBLE-001",
    "RULE-ADV-CG2000-003",
    "RULE-ADV-CG2001-001",
    "RULE-ADV-CG2066-001",
    "RULE-ADV-CG2066-002",
    "RULE-IPM-PREAMBLEIPM-001",
    "RULE-IPM-CGINFUSIONPUMPS-001",
}


class DecisionOutcome(str, Enum):
    """Deterministic decision tree evaluation outcomes."""
    CRITERIA_MET = "CRITERIA_MET"
    CRITERIA_NOT_MET = "CRITERIA_NOT_MET"
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFORMATION"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"
    POLICY_NOT_APPLICABLE = "POLICY_NOT_APPLICABLE"
    POLICY_VERSION_UNRESOLVED = "POLICY_VERSION_UNRESOLVED"
    EVALUATION_ERROR = "EVALUATION_ERROR"

    def __repr__(self) -> str:
        return self.value


class DecisionTrack(str, Enum):
    """Categorical separation between clinical necessity and place of service."""
    CLINICAL_NECESSITY = "CLINICAL_NECESSITY"
    PLACE_OF_SERVICE = "PLACE_OF_SERVICE"

    def __repr__(self) -> str:
        return self.value


@dataclass
class CriterionExecutionTrace:
    """Detailed provenance and execution trace for a single clinical criterion."""
    condition_id: str
    description: str
    parameter: Optional[str]
    comparator: Optional[str]
    expected_value: Any
    actual_value: Any
    status: EvaluationState
    reason: str
    is_optional: bool
    evidence_missing: bool
    source_file: str
    physical_page: int
    source_section: str
    source_quote: str
    rule_id: str
    criterion_state: str = "INSUFFICIENT_DATA"
    evidence_state: str = "MISSING"
    evidence_snippet: Optional[str] = None


@dataclass
class RuleTreeExecution:
    """Execution outcome of a single rule in the decision tree."""
    rule_id: str
    rule_name: str
    domain: str
    track: DecisionTrack
    governance_status: str
    is_blocked_by_governance: bool
    outcome: DecisionOutcome
    decision_effect: str
    traces: List[CriterionExecutionTrace] = field(default_factory=list)
    missing_parameters: List[str] = field(default_factory=list)
    explanation: str = ""
    provenance: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionTreeAssessment:
    """Consolidated deterministic assessment across Clinical Necessity and Place of Service."""
    case_id: str
    clinical_necessity_outcome: DecisionOutcome
    clinical_necessity_explanation: str
    clinical_necessity_rules: List[RuleTreeExecution]
    place_of_service_outcome: Optional[DecisionOutcome]
    place_of_service_explanation: Optional[str]
    place_of_service_rules: List[RuleTreeExecution]
    overall_outcome: DecisionOutcome
    overall_summary: str
    human_review_reasons: List[str] = field(default_factory=list)
    missing_evidence_fields: List[str] = field(default_factory=list)
    uncovered_gaps_encountered: List[str] = field(default_factory=list)
    criteria_met: List[str] = field(default_factory=list)
    criteria_not_met: List[str] = field(default_factory=list)
    criteria_insufficient_data: List[str] = field(default_factory=list)
    criteria_not_applicable: List[str] = field(default_factory=list)
    is_binding: bool = False
    reproducibility_hash: str = ""
    disclaimer: str = (
        "NON-BINDING PROTOTYPE EVALUATION: THIS EVALUATION IS A DETERMINISTIC RESEARCH PROTOTYPE FOR TESTING PURPOSES ONLY. "
        "NO REAL-WORLD AUTHORIZATION APPROVAL OR DENIAL IS EXECUTED. "
        "RULES ARE IN DRAFT/TESTING STATUS AWAITING CLINICAL SME REVIEW."
    )


class DecisionTreeEngine:
    """Deterministic Decision Tree Engine enforcing strict scope, three-valued logic, and dual tracks."""

    def __init__(
        self,
        registry: Optional[RuleRegistry] = None,
        validator: Optional[CaseValidator] = None,
        router: Optional[PolicyRouter] = None,
        evaluator: Optional[ConditionEvaluator] = None,
        evidence_auditor: Optional[EvidenceValidator] = None,
    ):
        self.registry = registry or RuleRegistry(include_archived=False)
        # Ensure rules are loaded
        if not self.registry.all_rules:
            self.registry.load_all_domains()
            
        self.validator = validator or CaseValidator()
        self.router = router or PolicyRouter(self.registry)
        self.evaluator = evaluator or ConditionEvaluator()
        self.evidence_auditor = evidence_auditor or EvidenceValidator()

    def evaluate(
        self,
        case_data: Union[Dict[str, Any], CaseIntake],
        target_rule_ids: Optional[List[str]] = None,
        policy_context: Optional[Dict[str, Any]] = None,
    ) -> DecisionTreeAssessment:
        """Evaluate a case deterministically against the decision tree.

        Args:
            case_data: CaseIntake instance or raw dictionary.
            target_rule_ids: Optional list of explicit rule IDs to evaluate.
            policy_context: Optional context for overrides or dependencies.

        Returns:
            DecisionTreeAssessment
        """
        # 1. Normalize and validate case intake
        if isinstance(case_data, CaseIntake):
            case = case_data
        else:
            is_valid, errs, case_obj = self.validator.validate(case_data)
            if not is_valid or not case_obj:
                cid = case_data.get("case_id", "INVALID_CASE") if isinstance(case_data, dict) else "INVALID_CASE"
                return DecisionTreeAssessment(
                    case_id=cid,
                    clinical_necessity_outcome=DecisionOutcome.EVALUATION_ERROR,
                    clinical_necessity_explanation=f"Case validation rejected: {'; '.join(errs)}",
                    clinical_necessity_rules=[],
                    place_of_service_outcome=None,
                    place_of_service_explanation=None,
                    place_of_service_rules=[],
                    overall_outcome=DecisionOutcome.EVALUATION_ERROR,
                    overall_summary=f"Case validation failed: {'; '.join(errs)}",
                    missing_evidence_fields=errs,
                    is_binding=False,
                    reproducibility_hash=""
                )
            case = case_obj

        # 2. Check clinical domain isolation: only advanced_imaging and interventional_pain_management
        active_domains = {"advanced_imaging", "interventional_pain_management"}
        if case.clinical_domain not in active_domains:
            # Allow evaluation only if explicit historical/archived context is granted
            if not (policy_context and policy_context.get("allow_archived_domains")):
                return DecisionTreeAssessment(
                    case_id=case.case_id,
                    clinical_necessity_outcome=DecisionOutcome.POLICY_NOT_APPLICABLE,
                    clinical_necessity_explanation=f"Clinical domain '{case.clinical_domain}' is not in active MedRule scope (Advanced Imaging & IPM only).",
                    clinical_necessity_rules=[],
                    place_of_service_outcome=None,
                    place_of_service_explanation=None,
                    place_of_service_rules=[],
                    overall_outcome=DecisionOutcome.POLICY_NOT_APPLICABLE,
                    overall_summary=f"Domain '{case.clinical_domain}' is outside active scope.",
                    is_binding=False,
                    reproducibility_hash=""
                )

        # 3. Route case to candidate rules
        routing = self.router.route_case(
            case,
            target_rule_ids=target_rule_ids,
            policy_context=policy_context
        )

        if routing.status != "ROUTED":
            outcome_map = {
                "POLICY_NOT_APPLICABLE": DecisionOutcome.POLICY_NOT_APPLICABLE,
                "POLICY_VERSION_UNRESOLVED": DecisionOutcome.POLICY_VERSION_UNRESOLVED,
                "MANUAL_REVIEW_REQUIRED": DecisionOutcome.NEEDS_HUMAN_REVIEW,
                "EVALUATION_ERROR": DecisionOutcome.EVALUATION_ERROR,
            }
            mapped_outcome = outcome_map.get(routing.status, DecisionOutcome.POLICY_NOT_APPLICABLE)
            summary_msg = "; ".join(routing.routing_notes) or f"Routing returned {routing.status}"
            return DecisionTreeAssessment(
                case_id=case.case_id,
                clinical_necessity_outcome=mapped_outcome,
                clinical_necessity_explanation=summary_msg,
                clinical_necessity_rules=[],
                place_of_service_outcome=None,
                place_of_service_explanation=None,
                place_of_service_rules=[],
                overall_outcome=mapped_outcome,
                overall_summary=summary_msg,
                human_review_reasons=routing.unresolved_dependencies if mapped_outcome == DecisionOutcome.NEEDS_HUMAN_REVIEW else [],
                is_binding=False,
                reproducibility_hash=""
            )

        # 4. Separate applicable rules into Clinical Necessity and Place of Service tracks
        clin_rules: List[RuleRecord] = []
        pos_rules: List[RuleRecord] = []

        for r_rec in routing.applicable_rules:
            is_pos = (
                r_rec.rule_type == "place_of_service" or
                "EPOS 2067" in r_rec.policy_title or
                "EPOS 1755" in r_rec.policy_title or
                "EPOS" in r_rec.rule_id
            )
            if is_pos:
                pos_rules.append(r_rec)
            else:
                clin_rules.append(r_rec)

        # 5. Evaluate Clinical Necessity Track
        clin_executions = [self._evaluate_rule_node(case, r) for r in clin_rules]

        # 6. Evaluate Place of Service Track
        pos_executions = [self._evaluate_rule_node(case, r) for r in pos_rules]

        # 7. Detect known clinical coverage gaps
        gaps_encountered = self._detect_coverage_gaps(case, routing)

        # 8. Synthesize outcomes for each track
        clin_outcome, clin_expl, clin_hr, clin_missing = self._synthesize_track(clin_executions, DecisionTrack.CLINICAL_NECESSITY)
        
        pos_outcome = None
        pos_expl = None
        pos_hr: List[str] = []
        pos_missing: List[str] = []
        if pos_executions:
            pos_outcome, pos_expl, pos_hr, pos_missing = self._synthesize_track(pos_executions, DecisionTrack.PLACE_OF_SERVICE)

        # 9. Aggregate overall assessment
        all_hr = list(clin_hr + pos_hr)
        all_missing = list(dict.fromkeys(clin_missing + pos_missing))

        if gaps_encountered:
            for gap in gaps_encountered:
                all_hr.append(f"Uncovered Policy Criterion: {gap}")

        # Deterministic precedence:
        # A. If any human review escalation exists (governance blocked rule, gap, advisory) -> NEEDS_HUMAN_REVIEW
        # B. If clinical necessity is CRITERIA_NOT_MET -> CRITERIA_NOT_MET
        # C. If clinical necessity is INSUFFICIENT_INFORMATION -> INSUFFICIENT_INFORMATION
        # D. If clinical necessity is CRITERIA_MET:
        #    - If POS is evaluated and CRITERIA_NOT_MET -> CRITERIA_MET (for clinical necessity) with POS site redirection note
        #    - If POS is evaluated and INSUFFICIENT_INFORMATION -> INSUFFICIENT_INFORMATION
        #    - Else -> CRITERIA_MET
        if all_hr:
            overall_outcome = DecisionOutcome.NEEDS_HUMAN_REVIEW
            overall_summary = (
                f"Evaluation escalated to clinical review: {len(all_hr)} issue(s) require clinical review. "
                f"Issues: {'; '.join(all_hr[:3])}"
            )
        elif not clin_executions and pos_executions:
            # Pure Place of Service evaluation (e.g. targeted testing of EPOS rules)
            overall_outcome = pos_outcome
            overall_summary = f"Place of Service evaluation: {pos_expl}"
        elif clin_outcome == DecisionOutcome.CRITERIA_NOT_MET:
            overall_outcome = DecisionOutcome.CRITERIA_NOT_MET
            overall_summary = f"Clinical necessity criteria not met: {clin_expl}"
        elif clin_outcome == DecisionOutcome.INSUFFICIENT_INFORMATION:
            overall_outcome = DecisionOutcome.INSUFFICIENT_INFORMATION
            overall_summary = f"Insufficient clinical evidence to determine necessity: {clin_expl}"
        elif clin_outcome == DecisionOutcome.CRITERIA_MET:
            if pos_outcome == DecisionOutcome.CRITERIA_NOT_MET:
                # Dual track nuance: clinical necessity met, but requested place of service not authorized
                overall_outcome = DecisionOutcome.CRITERIA_NOT_MET
                overall_summary = (
                    f"Clinical necessity criteria MET for procedure, but requested Place of Service "
                    f"({case.place_of_service or 'Hospital Outpatient'}) is NOT MET under governing policy: {pos_expl}. "
                    "Redirection to ambulatory/freestanding facility required."
                )
            elif pos_outcome == DecisionOutcome.INSUFFICIENT_INFORMATION:
                overall_outcome = DecisionOutcome.INSUFFICIENT_INFORMATION
                overall_summary = (
                    f"Clinical necessity criteria MET for procedure, but Place of Service documentation is insufficient: {pos_expl}"
                )
            else:
                overall_outcome = DecisionOutcome.CRITERIA_MET
                pos_note = f" (Place of Service: {pos_expl})" if pos_expl else ""
                overall_summary = f"All applicable clinical criteria met: {clin_expl}{pos_note}"
        else:
            overall_outcome = clin_outcome
            overall_summary = clin_expl

        # 10. Collect criteria lists for explainability
        crit_met: List[str] = []
        crit_not_met: List[str] = []
        crit_insufficient: List[str] = []
        crit_na: List[str] = []

        for ex in clin_executions + pos_executions:
            for t in ex.traces:
                desc_str = f"[{t.rule_id} / {t.condition_id}] {t.description or t.parameter or 'Criterion'}"
                if t.criterion_state == "MET":
                    if desc_str not in crit_met:
                        crit_met.append(desc_str)
                elif t.criterion_state == "NOT_MET":
                    if desc_str not in crit_not_met:
                        crit_not_met.append(desc_str)
                elif t.criterion_state == "NOT_APPLICABLE":
                    if desc_str not in crit_na:
                        crit_na.append(desc_str)
                else:  # INSUFFICIENT_DATA
                    if desc_str not in crit_insufficient:
                        crit_insufficient.append(desc_str)

        # 11. Generate reproducibility hash
        rep_hash = self._compute_reproducibility_hash(case, clin_executions + pos_executions, overall_outcome)

        return DecisionTreeAssessment(
            case_id=case.case_id,
            clinical_necessity_outcome=clin_outcome,
            clinical_necessity_explanation=clin_expl,
            clinical_necessity_rules=clin_executions,
            place_of_service_outcome=pos_outcome,
            place_of_service_explanation=pos_expl,
            place_of_service_rules=pos_executions,
            overall_outcome=overall_outcome,
            overall_summary=overall_summary,
            human_review_reasons=all_hr,
            missing_evidence_fields=all_missing,
            uncovered_gaps_encountered=gaps_encountered,
            criteria_met=crit_met,
            criteria_not_met=crit_not_met,
            criteria_insufficient_data=crit_insufficient,
            criteria_not_applicable=crit_na,
            is_binding=False,
            reproducibility_hash=rep_hash
        )

    def _evaluate_rule_node(self, case: CaseIntake, rule: RuleRecord) -> RuleTreeExecution:
        """Evaluate a single rule node in the decision tree."""
        rid = rule.rule_id
        is_pos = (
            rule.rule_type == "place_of_service" or
            "EPOS 2067" in rule.policy_title or
            "EPOS 1755" in rule.policy_title or
            "EPOS" in rule.rule_id
        )
        track = DecisionTrack.PLACE_OF_SERVICE if is_pos else DecisionTrack.CLINICAL_NECESSITY

        provenance = {
            "rule_id": rid,
            "policy_title": rule.policy_title,
            "policy_version": rule.policy_version,
            "source_file": rule.source_file,
            "physical_page": rule.physical_page,
            "source_section": rule.source_section,
            "source_quote": rule.source_quote,
            "decision_effect": rule.decision_effect,
            "extraction_status": rule.extraction_status,
        }

        # 1. STRICT GOVERNANCE GATE: Block the 7 rules marked NEEDS_HUMAN_REVIEW
        is_blocked = (
            rid in GOVERNANCE_BLOCKED_RULE_IDS or
            rule.extraction_status == "NEEDS_HUMAN_REVIEW" or
            rule.human_review_required is True
        )

        if is_blocked:
            reason_msg = (
                f"Rule {rid} is flagged '{rule.extraction_status}': "
                f"{rule.review_notes or 'Requires clinical medical director sign-off before logic execution.'}"
            )
            return RuleTreeExecution(
                rule_id=rid,
                rule_name=rule.clinical_service_or_procedure,
                domain=rule.domain,
                track=track,
                governance_status=rule.extraction_status,
                is_blocked_by_governance=True,
                outcome=DecisionOutcome.NEEDS_HUMAN_REVIEW,
                decision_effect=rule.decision_effect,
                traces=[],
                missing_parameters=[],
                explanation=reason_msg,
                provenance=provenance
            )

        # 2. Evaluate condition tree deterministically
        group_eval = self.evaluator.evaluate(rule.conditions, case)

        # 3. Flatten criteria results into execution traces with exact source provenance
        traces: List[CriterionExecutionTrace] = []
        missing_params: List[str] = []
        self._collect_traces(group_eval, rule, traces, missing_params)

        # 4. Map condition evaluation state to DecisionOutcome
        if group_eval.status == EvaluationState.TRUE:
            if rule.decision_effect == "NOT_INDICATED":
                outcome = DecisionOutcome.CRITERIA_NOT_MET
                expl = f"Disqualifying exclusion criterion met: {group_eval.explanation}"
            else:
                outcome = DecisionOutcome.CRITERIA_MET
                expl = group_eval.explanation
        elif group_eval.status == EvaluationState.FALSE:
            if rule.decision_effect == "NOT_INDICATED":
                # Exclusion condition was FALSE -> exclusion not present
                outcome = DecisionOutcome.CRITERIA_MET
                expl = f"Exclusion condition not present: {group_eval.explanation}"
            else:
                outcome = DecisionOutcome.CRITERIA_NOT_MET
                expl = group_eval.explanation
        else:  # UNKNOWN
            outcome = DecisionOutcome.INSUFFICIENT_INFORMATION
            expl = f"Missing clinical data for rule: {group_eval.explanation}"

        return RuleTreeExecution(
            rule_id=rid,
            rule_name=rule.clinical_service_or_procedure,
            domain=rule.domain,
            track=track,
            governance_status=rule.extraction_status,
            is_blocked_by_governance=False,
            outcome=outcome,
            decision_effect=rule.decision_effect,
            traces=traces,
            missing_parameters=missing_params,
            explanation=expl,
            provenance=provenance
        )

    def _collect_traces(
        self,
        group_eval: ConditionGroupEvaluation,
        rule: RuleRecord,
        traces: List[CriterionExecutionTrace],
        missing_params: List[str]
    ) -> None:
        """Recursively collect criterion execution traces."""
        for c in group_eval.criteria_results:
            c_state = getattr(c, "criterion_state", "INSUFFICIENT_DATA")
            c_state_str = c_state.value if hasattr(c_state, "value") else str(c_state)
            e_state = getattr(c, "evidence_state", "MISSING")
            e_state_str = e_state.value if hasattr(e_state, "value") else str(e_state)
            c_snippet = getattr(c, "evidence_snippet", None)

            trace = CriterionExecutionTrace(
                condition_id=c.condition_id,
                description=c.description,
                parameter=c.parameter,
                comparator=c.comparator,
                expected_value=c.expected_value,
                actual_value=c.actual_value,
                status=c.status,
                reason=c.reason,
                is_optional=c.is_optional,
                evidence_missing=c.evidence_missing,
                source_file=rule.source_file,
                physical_page=rule.physical_page,
                source_section=rule.source_section,
                source_quote=rule.source_quote,
                rule_id=rule.rule_id,
                criterion_state=c_state_str,
                evidence_state=e_state_str,
                evidence_snippet=c_snippet
            )
            traces.append(trace)
            if c.evidence_missing and c.parameter and c.parameter not in missing_params:
                missing_params.append(c.parameter)

            # Recurse into sub-evaluations
            for sc in c.sub_evaluations:
                sc_state = getattr(sc, "criterion_state", "INSUFFICIENT_DATA")
                sc_state_str = sc_state.value if hasattr(sc_state, "value") else str(sc_state)
                sc_e_state = getattr(sc, "evidence_state", "MISSING")
                sc_e_state_str = sc_e_state.value if hasattr(sc_e_state, "value") else str(sc_e_state)
                sc_snippet = getattr(sc, "evidence_snippet", None)

                sub_trace = CriterionExecutionTrace(
                    condition_id=sc.condition_id,
                    description=sc.description,
                    parameter=sc.parameter,
                    comparator=sc.comparator,
                    expected_value=sc.expected_value,
                    actual_value=sc.actual_value,
                    status=sc.status,
                    reason=sc.reason,
                    is_optional=sc.is_optional,
                    evidence_missing=sc.evidence_missing,
                    source_file=rule.source_file,
                    physical_page=rule.physical_page,
                    source_section=rule.source_section,
                    source_quote=rule.source_quote,
                    rule_id=rule.rule_id,
                    criterion_state=sc_state_str,
                    evidence_state=sc_e_state_str,
                    evidence_snippet=sc_snippet
                )
                traces.append(sub_trace)
                if sc.evidence_missing and sc.parameter and sc.parameter not in missing_params:
                    missing_params.append(sc.parameter)

    def _synthesize_track(
        self,
        executions: List[RuleTreeExecution],
        track_type: DecisionTrack
    ) -> Tuple[DecisionOutcome, str, List[str], List[str]]:
        """Synthesize multiple rule execution outcomes within a track."""
        if not executions:
            return (
                DecisionOutcome.POLICY_NOT_APPLICABLE,
                f"No candidate {track_type.value} rules evaluated.",
                [],
                []
            )

        hr_reasons: List[str] = []
        missing_fields: List[str] = []
        has_met = False
        has_not_met = False
        has_unknown = False
        met_rules: List[str] = []
        not_met_rules: List[str] = []
        unknown_rules: List[str] = []

        for ex in executions:
            for p in ex.missing_parameters:
                if p not in missing_fields:
                    missing_fields.append(p)

            if ex.is_blocked_by_governance or ex.outcome == DecisionOutcome.NEEDS_HUMAN_REVIEW:
                hr_reasons.append(f"{ex.rule_id}: {ex.explanation}")
            elif ex.outcome == DecisionOutcome.CRITERIA_MET:
                has_met = True
                met_rules.append(ex.rule_id)
            elif ex.outcome == DecisionOutcome.CRITERIA_NOT_MET:
                has_not_met = True
                not_met_rules.append(ex.rule_id)
            elif ex.outcome == DecisionOutcome.INSUFFICIENT_INFORMATION:
                has_unknown = True
                unknown_rules.append(ex.rule_id)

        # Track precedence:
        # 1. Human review blocked rules
        if hr_reasons:
            return (
                DecisionOutcome.NEEDS_HUMAN_REVIEW,
                f"Track {track_type.value} escalated to clinical review: {'; '.join(hr_reasons[:2])}",
                hr_reasons,
                missing_fields
            )

        # 2. Check if any evaluated exclusion rule resulted in CRITERIA_NOT_MET (disqualifying condition was met)
        exclusion_fails = [
            ex for ex in executions
            if ex.outcome == DecisionOutcome.CRITERIA_NOT_MET and ex.decision_effect == "NOT_INDICATED"
        ]
        if exclusion_fails:
            exclusion_ids = [ex.rule_id for ex in exclusion_fails]
            return (
                DecisionOutcome.CRITERIA_NOT_MET,
                f"Disqualifying exclusion criterion met under rule(s): {', '.join(exclusion_ids)}",
                [],
                missing_fields
            )

        # 3. If any standard indication rule was not met and no indication rule was met
        if has_not_met and not has_met:
            return (
                DecisionOutcome.CRITERIA_NOT_MET,
                f"Clinical criteria not met for evaluated rules: {', '.join(not_met_rules)}",
                [],
                missing_fields
            )

        if has_met:
            return (
                DecisionOutcome.CRITERIA_MET,
                f"Criteria satisfied under rule(s): {', '.join(met_rules)}",
                [],
                missing_fields
            )

        if has_unknown:
            return (
                DecisionOutcome.INSUFFICIENT_INFORMATION,
                f"Missing clinical evidence required for rule(s): {', '.join(unknown_rules)}",
                [],
                missing_fields
            )

        return (
            DecisionOutcome.CRITERIA_NOT_MET,
            "Criteria not satisfied across evaluated rules.",
            [],
            missing_fields
        )

    def _detect_coverage_gaps(self, case: CaseIntake, routing: RoutingResult) -> List[str]:
        """Detect known clinical coverage gaps where governing policy is incomplete or ambiguous."""
        gaps: List[str] = []
        ev = case.clinical_evidence

        # Gap 1: Spinal Stenosis without Radiculopathy in IPM (CG 1750)
        # Policy requires distinct claudication distance and canal diameter thresholds not yet codified
        if case.clinical_domain == "interventional_pain_management":
            proc_code = case.procedure_code or ""
            proc_name = (case.procedure_name or "").lower()
            if "epidural" in proc_name or proc_code in ("62321", "62322", "62323"):
                is_stenosis = ev.get("spinal_stenosis_present") is True
                is_radicular = ev.get("radicular_pain_confirmed") is True
                if is_stenosis and not is_radicular:
                    gaps.append(
                        "IPM CG 1750 Gap: Epidural injection requested for isolated spinal stenosis / neurogenic claudication "
                        "without radiculopathy. Specific stenosis imaging severity criteria and walking distance thresholds "
                        "remain uncodified in active rulebook."
                    )

        # Gap 2: Dorsal Root Ganglion (DRG) stimulation non-lower-extremity (CG 1757)
        if case.clinical_domain == "interventional_pain_management":
            if "drg" in (case.procedure_name or "").lower() or ev.get("requested_stimulation_type") == "DRG":
                location = str(ev.get("crps_anatomical_location", "")).lower()
                if location and "lower" not in location:
                    gaps.append(
                        "IPM CG 1757 Gap: DRG neuromodulation is restricted by 2026 governing policy exclusively to "
                        "CRPS Type I/II of the lower extremities. Requested location is non-lower-extremity."
                    )

        # Gap 3: Repeat epidural injection with interval < 14 days (CG 1750 2026 policy limit)
        if case.clinical_domain == "interventional_pain_management":
            interval = ev.get("subsequent_injection_interval_days")
            if interval is not None and isinstance(interval, (int, float)) and interval < 14:
                gaps.append(
                    f"IPM CG 1750 Policy Violation: Subsequent epidural injection interval ({interval} days) "
                    "violates mandatory 2026 policy minimum interval of 14 days."
                )

        # Gap 4: Annual session limits exceeded
        if case.clinical_domain == "interventional_pain_management":
            sessions = ev.get("annual_session_count_past_12mo")
            if sessions is not None and isinstance(sessions, (int, float)) and sessions >= 3:
                gaps.append(
                    f"IPM CG 1750 Policy Limit: Annual epidural session count ({sessions}) meets or exceeds "
                    "the maximum annual limit of 3 sessions per rolling 12-month period."
                )

        # Gap 5: Advisory language in CG 2000 (IBD patient age < 35)
        if case.clinical_domain == "advanced_imaging":
            if case.patient_age_years is not None and case.patient_age_years < 35:
                diag = (case.diagnosis_description or "").lower()
                if "crohn" in diag or "ibd" in diag or "inflammatory bowel" in diag:
                    gaps.append(
                        "Advanced Imaging CG 2000 Advisory Gap: Policy recommends MRI enterography over CT for patients < 35 "
                        "years old to reduce cumulative ionizing radiation ('MRI should be considered'). Advisory guidance "
                        "requires physician clinical reviewer discretion."
                    )

        return gaps

    def _compute_reproducibility_hash(
        self,
        case: CaseIntake,
        executions: List[RuleTreeExecution],
        outcome: DecisionOutcome
    ) -> str:
        """Compute cryptographic SHA-256 reproducibility hash over normalized inputs and outputs."""
        hasher = hashlib.sha256()
        canonical_input = {
            "case_id": case.case_id,
            "clinical_domain": case.clinical_domain,
            "procedure_code": case.procedure_code,
            "procedure_name": case.procedure_name,
            "dos": case.requested_date_of_service,
            "lob": case.line_of_business,
            "evidence": {k: case.clinical_evidence[k] for k in sorted(case.clinical_evidence.keys())}
        }
        hasher.update(json.dumps(canonical_input, sort_keys=True).encode("utf-8"))

        canonical_eval = {
            "outcome": outcome.value,
            "rule_outcomes": [
                {
                    "rule_id": ex.rule_id,
                    "outcome": ex.outcome.value,
                    "traces": [
                        {
                            "cid": t.condition_id,
                            "param": t.parameter,
                            "status": t.status.value,
                        }
                        for t in ex.traces
                    ]
                }
                for ex in sorted(executions, key=lambda x: x.rule_id)
            ]
        }
        hasher.update(json.dumps(canonical_eval, sort_keys=True).encode("utf-8"))
        return hasher.hexdigest()
