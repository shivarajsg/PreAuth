"""MedRule Deterministic Condition Evaluator Module.

Implements recursive three-valued Boolean condition evaluation (TRUE, FALSE, UNKNOWN)
for MedRule condition trees (ALL_OF, ANY_OF, NONE_OF, SINGLE_CONDITION) and
relational comparators without heuristic inference, approximations, or silent defaulting.
"""

from dataclasses import dataclass, field
from enum import Enum
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from medrule_engine.case_validator import CaseIntake

logger = logging.getLogger(__name__)

MAX_RECURSION_DEPTH = 10


class EvaluationState(str, Enum):
    """Three-valued logic evaluation states."""
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"

    def __repr__(self) -> str:
        return self.value


class CriterionState(str, Enum):
    """Normalized four-state representation for clinical policy criteria."""
    MET = "MET"
    NOT_MET = "NOT_MET"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_APPLICABLE = "NOT_APPLICABLE"

    def __repr__(self) -> str:
        return self.value


class EvidenceState(str, Enum):
    """Evidence presence and certainty classification."""
    EXPLICIT_POSITIVE = "EXPLICIT_POSITIVE"
    EXPLICIT_NEGATIVE = "EXPLICIT_NEGATIVE"
    MISSING = "MISSING"
    AMBIGUOUS = "AMBIGUOUS"
    CONFLICTING = "CONFLICTING"

    def __repr__(self) -> str:
        return self.value


@dataclass
class CriterionEvaluation:
    """Detailed result of evaluating a single atomic or sub-condition criterion."""
    condition_id: str
    description: str
    parameter: Optional[str]
    comparator: Optional[str]
    expected_value: Any
    actual_value: Any
    status: EvaluationState
    reason: str
    is_optional: bool = False
    evidence_missing: bool = False
    type_error: Optional[str] = None
    sub_evaluations: List["CriterionEvaluation"] = field(default_factory=list)
    criterion_state: CriterionState = CriterionState.INSUFFICIENT_DATA
    evidence_state: EvidenceState = EvidenceState.MISSING
    evidence_snippet: Optional[str] = None


@dataclass
class ConditionGroupEvaluation:
    """Detailed result of evaluating a condition group node (operator + child criteria)."""
    operator: str
    status: EvaluationState
    criteria_results: List[CriterionEvaluation] = field(default_factory=list)
    short_circuited: bool = False
    explanation: str = ""


class ConditionEvaluator:
    """Deterministic, recursive evaluator for policy condition trees."""

    def __init__(self, max_depth: int = MAX_RECURSION_DEPTH):
        self.max_depth = max_depth

    def evaluate(self, condition_group: Dict[str, Any], case: CaseIntake) -> ConditionGroupEvaluation:
        """Top-level entry point to evaluate a condition tree against a case."""
        return self._evaluate_group(condition_group, case, depth=0)

    def _evaluate_group(self, group: Dict[str, Any], case: CaseIntake, depth: int) -> ConditionGroupEvaluation:
        if depth > self.max_depth:
            return ConditionGroupEvaluation(
                operator=group.get("operator", "UNKNOWN"),
                status=EvaluationState.UNKNOWN,
                explanation=f"Exceeded maximum recursion depth ({self.max_depth}). Probable condition cycle."
            )

        operator = group.get("operator", "ALL_OF")
        raw_criteria = group.get("criteria", [])
        if not raw_criteria:
            return ConditionGroupEvaluation(
                operator=operator,
                status=EvaluationState.UNKNOWN,
                explanation="Condition group contains no child criteria."
            )

        eval_results: List[CriterionEvaluation] = []

        if operator == "SINGLE_CONDITION":
            crit = raw_criteria[0]
            c_res = self._evaluate_criterion(crit, case, depth)
            eval_results.append(c_res)
            return ConditionGroupEvaluation(
                operator=operator,
                status=c_res.status,
                criteria_results=eval_results,
                explanation=f"SINGLE_CONDITION: {c_res.description} -> {c_res.status.value} ({c_res.reason})"
            )

        elif operator == "ALL_OF":
            # Semantics:
            # - If ANY mandatory child is FALSE -> group is FALSE (short-circuit).
            # - Else if ANY mandatory child is UNKNOWN -> group is UNKNOWN.
            # - Else (all mandatory children are TRUE) -> group is TRUE.
            has_unknown = False
            is_false = False
            short_circuit_reason = ""

            for crit in raw_criteria:
                c_res = self._evaluate_criterion(crit, case, depth)
                eval_results.append(c_res)

                if crit.get("is_optional", False):
                    continue

                if c_res.status == EvaluationState.FALSE:
                    is_false = True
                    short_circuit_reason = f"Mandatory criterion {c_res.condition_id} is FALSE: {c_res.reason}"
                    break  # Safe short-circuit for ALL_OF
                elif c_res.status == EvaluationState.UNKNOWN:
                    has_unknown = True

            if is_false:
                # Mark remaining unevaluated criteria as NOT_APPLICABLE due to short-circuit
                if len(eval_results) < len(raw_criteria):
                    for remaining_crit in raw_criteria[len(eval_results):]:
                        eval_results.append(CriterionEvaluation(
                            condition_id=remaining_crit.get("condition_id", "UNKNOWN"),
                            description=remaining_crit.get("description", ""),
                            parameter=remaining_crit.get("parameter"),
                            comparator=remaining_crit.get("comparator"),
                            expected_value=remaining_crit.get("value"),
                            actual_value=None,
                            status=EvaluationState.UNKNOWN,
                            reason="Bypassed by ALL_OF short-circuit (prior mandatory criterion is FALSE).",
                            is_optional=bool(remaining_crit.get("is_optional", False)),
                            criterion_state=CriterionState.NOT_APPLICABLE,
                            evidence_state=EvidenceState.MISSING
                        ))
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.FALSE,
                    criteria_results=eval_results,
                    short_circuited=True,
                    explanation=f"ALL_OF evaluated to FALSE ({short_circuit_reason})"
                )
            elif has_unknown:
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.UNKNOWN,
                    criteria_results=eval_results,
                    short_circuited=False,
                    explanation="ALL_OF evaluated to UNKNOWN: one or more mandatory criteria have insufficient evidence."
                )
            else:
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.TRUE,
                    criteria_results=eval_results,
                    short_circuited=False,
                    explanation="ALL_OF evaluated to TRUE: all mandatory criteria fully satisfied."
                )

        elif operator == "ANY_OF":
            # Semantics:
            # - If ANY child is TRUE -> group is TRUE (short-circuit).
            # - Else if ALL children are FALSE -> group is FALSE.
            # - Else (no TRUE, and at least one UNKNOWN) -> group is UNKNOWN.
            has_true = False
            has_unknown = False
            short_circuit_reason = ""

            for crit in raw_criteria:
                c_res = self._evaluate_criterion(crit, case, depth)
                eval_results.append(c_res)

                if c_res.status == EvaluationState.TRUE:
                    has_true = True
                    c_res.criterion_state = CriterionState.MET
                    short_circuit_reason = f"Alternative criterion {c_res.condition_id} is TRUE: {c_res.reason}"
                    break  # Safe short-circuit for ANY_OF
                elif c_res.status == EvaluationState.UNKNOWN:
                    has_unknown = True

            if has_true:
                # Mark remaining unevaluated alternative criteria as NOT_APPLICABLE
                if len(eval_results) < len(raw_criteria):
                    for remaining_crit in raw_criteria[len(eval_results):]:
                        eval_results.append(CriterionEvaluation(
                            condition_id=remaining_crit.get("condition_id", "UNKNOWN"),
                            description=remaining_crit.get("description", ""),
                            parameter=remaining_crit.get("parameter"),
                            comparator=remaining_crit.get("comparator"),
                            expected_value=remaining_crit.get("value"),
                            actual_value=None,
                            status=EvaluationState.UNKNOWN,
                            reason="Alternative criterion satisfied; this alternative was not required.",
                            is_optional=bool(remaining_crit.get("is_optional", False)),
                            criterion_state=CriterionState.NOT_APPLICABLE,
                            evidence_state=EvidenceState.MISSING
                        ))
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.TRUE,
                    criteria_results=eval_results,
                    short_circuited=True,
                    explanation=f"ANY_OF evaluated to TRUE ({short_circuit_reason})"
                )
            elif has_unknown:
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.UNKNOWN,
                    criteria_results=eval_results,
                    short_circuited=False,
                    explanation="ANY_OF evaluated to UNKNOWN: no alternative satisfied, but one or more have missing evidence."
                )
            else:
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.FALSE,
                    criteria_results=eval_results,
                    short_circuited=False,
                    explanation="ANY_OF evaluated to FALSE: all evaluated alternatives are FALSE."
                )

        elif operator == "NONE_OF":
            # Semantics:
            # - If ANY child is TRUE -> group is FALSE (short-circuit: a forbidden condition holds).
            # - Else if ANY child is UNKNOWN -> group is UNKNOWN (cannot confirm none hold).
            # - Else (all children are FALSE) -> group is TRUE (none hold).
            has_true = False
            has_unknown = False
            short_circuit_reason = ""

            for crit in raw_criteria:
                c_res = self._evaluate_criterion(crit, case, depth)
                eval_results.append(c_res)

                if c_res.status == EvaluationState.TRUE:
                    has_true = True
                    short_circuit_reason = f"Disqualifying criterion {c_res.condition_id} is TRUE: {c_res.reason}"
                    break
                elif c_res.status == EvaluationState.UNKNOWN:
                    has_unknown = True

            if has_true:
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.FALSE,
                    criteria_results=eval_results,
                    short_circuited=True,
                    explanation=f"NONE_OF evaluated to FALSE ({short_circuit_reason})"
                )
            elif has_unknown:
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.UNKNOWN,
                    criteria_results=eval_results,
                    short_circuited=False,
                    explanation="NONE_OF evaluated to UNKNOWN: cannot verify exclusion because child condition evidence is missing."
                )
            else:
                return ConditionGroupEvaluation(
                    operator=operator,
                    status=EvaluationState.TRUE,
                    criteria_results=eval_results,
                    short_circuited=False,
                    explanation="NONE_OF evaluated to TRUE: none of the specified disqualifying conditions are present."
                )

        else:
            return ConditionGroupEvaluation(
                operator=operator,
                status=EvaluationState.UNKNOWN,
                criteria_results=eval_results,
                explanation=f"Unsupported operator '{operator}' encountered in condition group."
            )

    def _evaluate_criterion(self, crit: Dict[str, Any], case: CaseIntake, depth: int) -> CriterionEvaluation:
        cid = crit.get("condition_id", "UNKNOWN")
        desc = crit.get("description", "")
        param = crit.get("parameter")
        comparator = crit.get("comparator")
        expected_val = crit.get("value")
        is_optional = bool(crit.get("is_optional", False))
        sub_conds = crit.get("sub_conditions")

        # 1. If criterion has sub_conditions (nested tree)
        if sub_conds and isinstance(sub_conds, dict) and "criteria" in sub_conds:
            sub_res = self._evaluate_group(sub_conds, case, depth + 1)
            crit_state = (
                CriterionState.MET if sub_res.status == EvaluationState.TRUE
                else (CriterionState.NOT_MET if sub_res.status == EvaluationState.FALSE else CriterionState.INSUFFICIENT_DATA)
            )
            return CriterionEvaluation(
                condition_id=cid,
                description=desc,
                parameter=param,
                comparator=comparator,
                expected_value=expected_val,
                actual_value=None,
                status=sub_res.status,
                reason=f"Nested [{sub_res.operator}]: {sub_res.explanation}",
                is_optional=is_optional,
                sub_evaluations=sub_res.criteria_results,
                criterion_state=crit_state,
                evidence_state=EvidenceState.EXPLICIT_POSITIVE if crit_state == CriterionState.MET else EvidenceState.MISSING
            )

        # 2. Atomic criterion evaluation
        if not param:
            # Parameterless criteria represent policy declarations or high-level clinical milestones
            return CriterionEvaluation(
                condition_id=cid,
                description=desc,
                parameter=None,
                comparator=None,
                expected_value=expected_val,
                actual_value=None,
                status=EvaluationState.UNKNOWN,
                reason="Criterion defines clinical narrative without explicit parameter identifier.",
                is_optional=is_optional,
                evidence_missing=True,
                criterion_state=CriterionState.INSUFFICIENT_DATA,
                evidence_state=EvidenceState.MISSING
            )

        is_present, actual_val = case.get_evidence(param)

        # 1. Parameter does not exist in case record
        if not is_present:
            return CriterionEvaluation(
                condition_id=cid,
                description=desc,
                parameter=param,
                comparator=comparator,
                expected_value=expected_val,
                actual_value=None,
                status=EvaluationState.UNKNOWN,
                reason=f"Evidence parameter '{param}' is missing from case record.",
                is_optional=is_optional,
                evidence_missing=True,
                criterion_state=CriterionState.INSUFFICIENT_DATA,
                evidence_state=EvidenceState.MISSING
            )

        # 2. Parameter exists with explicit null/None
        if actual_val is None:
            return CriterionEvaluation(
                condition_id=cid,
                description=desc,
                parameter=param,
                comparator=comparator,
                expected_value=expected_val,
                actual_value=None,
                status=EvaluationState.UNKNOWN,
                reason=f"Evidence parameter '{param}' was provided as null (unrecorded/missing).",
                is_optional=is_optional,
                evidence_missing=True,
                criterion_state=CriterionState.INSUFFICIENT_DATA,
                evidence_state=EvidenceState.MISSING
            )

        # Check for explicitly marked conflicting or ambiguous evidence
        if isinstance(actual_val, dict) and actual_val.get("status") in ("CONFLICTING", "AMBIGUOUS"):
            ev_state = EvidenceState.CONFLICTING if actual_val["status"] == "CONFLICTING" else EvidenceState.AMBIGUOUS
            details = actual_val.get("details", "")
            return CriterionEvaluation(
                condition_id=cid,
                description=desc,
                parameter=param,
                comparator=comparator,
                expected_value=expected_val,
                actual_value=actual_val,
                status=EvaluationState.UNKNOWN,
                reason=f"Evidence for parameter '{param}' is {ev_state.value.lower()}: {details}",
                is_optional=is_optional,
                evidence_missing=True,
                criterion_state=CriterionState.INSUFFICIENT_DATA,
                evidence_state=ev_state,
                evidence_snippet=actual_val.get("snippet")
            )
        if isinstance(actual_val, str) and actual_val.upper() in ("CONFLICTING", "AMBIGUOUS"):
            ev_state = EvidenceState.CONFLICTING if actual_val.upper() == "CONFLICTING" else EvidenceState.AMBIGUOUS
            return CriterionEvaluation(
                condition_id=cid,
                description=desc,
                parameter=param,
                comparator=comparator,
                expected_value=expected_val,
                actual_value=actual_val,
                status=EvaluationState.UNKNOWN,
                reason=f"Evidence for parameter '{param}' is documented as {ev_state.value.lower()}.",
                is_optional=is_optional,
                evidence_missing=True,
                criterion_state=CriterionState.INSUFFICIENT_DATA,
                evidence_state=ev_state
            )

        # 3. Handle IS_ABSENT comparator where explicit absence of finding is required
        if comparator == "IS_ABSENT":
            # Explicit boolean false -> confirmed absent
            if actual_val is False:
                return CriterionEvaluation(
                    condition_id=cid,
                    description=desc,
                    parameter=param,
                    comparator=comparator,
                    expected_value=False,
                    actual_value=actual_val,
                    status=EvaluationState.TRUE,
                    reason=f"Parameter '{param}' is confirmed absent (explicit False).",
                    is_optional=is_optional,
                    evidence_missing=False,
                    criterion_state=CriterionState.MET,
                    evidence_state=EvidenceState.EXPLICIT_NEGATIVE
                )
            # Empty collection or empty string -> confirmed empty/absent
            if isinstance(actual_val, (list, tuple, set, str, dict)) and len(actual_val) == 0:
                return CriterionEvaluation(
                    condition_id=cid,
                    description=desc,
                    parameter=param,
                    comparator=comparator,
                    expected_value=False,
                    actual_value=actual_val,
                    status=EvaluationState.TRUE,
                    reason=f"Parameter '{param}' is empty ({type(actual_val).__name__}), confirming absence.",
                    is_optional=is_optional,
                    evidence_missing=False,
                    criterion_state=CriterionState.MET,
                    evidence_state=EvidenceState.EXPLICIT_NEGATIVE
                )
            # Boolean True or positive presence -> absence requirement violated
            if actual_val is True:
                return CriterionEvaluation(
                    condition_id=cid,
                    description=desc,
                    parameter=param,
                    comparator=comparator,
                    expected_value=False,
                    actual_value=actual_val,
                    status=EvaluationState.FALSE,
                    reason=f"Parameter '{param}' is present (True) when absence was required.",
                    is_optional=is_optional,
                    evidence_missing=False,
                    criterion_state=CriterionState.NOT_MET,
                    evidence_state=EvidenceState.EXPLICIT_POSITIVE
                )
            # Numerical zero or other number -> numerical value is present, not absent
            if isinstance(actual_val, (int, float)):
                return CriterionEvaluation(
                    condition_id=cid,
                    description=desc,
                    parameter=param,
                    comparator=comparator,
                    expected_value=False,
                    actual_value=actual_val,
                    status=EvaluationState.FALSE,
                    reason=f"Parameter '{param}' has recorded numerical measurement ({actual_val}) when absence was required.",
                    is_optional=is_optional,
                    evidence_missing=False,
                    criterion_state=CriterionState.NOT_MET,
                    evidence_state=EvidenceState.EXPLICIT_POSITIVE
                )
            # Non-empty collection/string
            return CriterionEvaluation(
                condition_id=cid,
                description=desc,
                parameter=param,
                comparator=comparator,
                expected_value=False,
                actual_value=actual_val,
                status=EvaluationState.FALSE,
                reason=f"Parameter '{param}' is present ({actual_val}) when absence was required.",
                is_optional=is_optional,
                evidence_missing=False,
                criterion_state=CriterionState.NOT_MET,
                evidence_state=EvidenceState.EXPLICIT_POSITIVE
            )

        # 4. Evaluate atomic comparators
        status, reason, type_err = self._apply_comparator(comparator, actual_val, expected_val, crit.get("unit"), param)
        crit_state = (
            CriterionState.MET if status == EvaluationState.TRUE
            else (CriterionState.NOT_MET if status == EvaluationState.FALSE else CriterionState.INSUFFICIENT_DATA)
        )
        if actual_val is False or (isinstance(actual_val, str) and actual_val.upper() in ("FALSE", "DENIED", "ABSENT", "NO")):
            ev_state = EvidenceState.EXPLICIT_NEGATIVE
        else:
            ev_state = EvidenceState.EXPLICIT_POSITIVE

        # Check if case raw payload or evidence snippet exists
        snippet = None
        if hasattr(case, "raw_payload") and isinstance(case.raw_payload, dict):
            prov = case.raw_payload.get("evidence_provenance", {})
            if isinstance(prov, dict) and param in prov:
                snippet = prov[param].get("snippet") if isinstance(prov[param], dict) else str(prov[param])

        return CriterionEvaluation(
            condition_id=cid,
            description=desc,
            parameter=param,
            comparator=comparator,
            expected_value=expected_val,
            actual_value=actual_val,
            status=status,
            reason=reason,
            is_optional=is_optional,
            evidence_missing=False,
            type_error=type_err,
            criterion_state=crit_state,
            evidence_state=ev_state,
            evidence_snippet=snippet
        )

    def _apply_comparator(
        self,
        comparator: Optional[str],
        actual: Any,
        expected: Any,
        unit: Optional[str],
        param_name: Optional[str] = None
    ) -> Tuple[EvaluationState, str, Optional[str]]:
        """Apply deterministic relational operator with strict type safety."""
        param_str = f"'{param_name}' " if param_name else ""

        # Default presence check when comparator is omitted or IS_PRESENT
        if not comparator or comparator == "IS_PRESENT":
            # Boolean explicit False
            if actual is False:
                return EvaluationState.FALSE, f"Parameter {param_str}is negative (False).", None
            # Boolean explicit True
            if actual is True:
                return EvaluationState.TRUE, f"Parameter {param_str}is positive (True).", None
            # Numerical zero or any valid number is present
            if isinstance(actual, (int, float)) and not isinstance(actual, bool):
                return EvaluationState.TRUE, f"Parameter {param_str}is present with numeric value: {actual}", None
            # Empty collection or empty string
            if isinstance(actual, (list, tuple, set, str, dict)):
                if len(actual) > 0:
                    return EvaluationState.TRUE, f"Parameter {param_str}is present with non-empty content: {actual}", None
                return EvaluationState.FALSE, f"Parameter {param_str}is empty ({type(actual).__name__}).", None
            # Any other non-None object
            return EvaluationState.TRUE, f"Parameter {param_str}is present: {actual}", None

        # EQUALS
        if comparator == "EQUALS":
            # Normalize string booleans (e.g. True matches 'TRUE' or 'true' extracted from policy JSON)
            b_actual = actual if isinstance(actual, bool) else (True if isinstance(actual, str) and actual.strip().upper() in ("TRUE", "YES") else (False if isinstance(actual, str) and actual.strip().upper() in ("FALSE", "NO") else None))
            b_expected = expected if isinstance(expected, bool) else (True if isinstance(expected, str) and expected.strip().upper() in ("TRUE", "YES") else (False if isinstance(expected, str) and expected.strip().upper() in ("FALSE", "NO") else None))

            if b_actual is not None and b_expected is not None:
                eq = (b_actual is b_expected)
                return (EvaluationState.TRUE if eq else EvaluationState.FALSE), f"Boolean {actual} {'==' if eq else '!='} {expected}", None

            # Strict Boolean type checking: booleans never equal numbers in MedRule
            if isinstance(actual, bool) or isinstance(expected, bool):
                return EvaluationState.FALSE, f"Type mismatch between Boolean and non-Boolean in EQUALS: actual={actual} ({type(actual).__name__}), expected={expected} ({type(expected).__name__})", None

            # Handle string case-insensitivity
            if isinstance(actual, str) and isinstance(expected, str):
                eq = actual.strip().lower() == expected.strip().lower()
                return (EvaluationState.TRUE if eq else EvaluationState.FALSE), f"'{actual}' {'==' if eq else '!='} '{expected}'", None

            # Handle numeric equality (excluding booleans)
            try:
                if isinstance(expected, (int, float)) and isinstance(actual, (int, float, str)):
                    eq = float(actual) == float(expected)
                    return (EvaluationState.TRUE if eq else EvaluationState.FALSE), f"{actual} {'==' if eq else '!='} {expected}", None
            except (ValueError, TypeError):
                pass

            eq = (actual == expected)
            return (EvaluationState.TRUE if eq else EvaluationState.FALSE), f"{actual} {'==' if eq else '!='} {expected}", None

        # NOT_EQUALS
        if comparator == "NOT_EQUALS":
            st, rsn, err = self._apply_comparator("EQUALS", actual, expected, unit, param_name)
            if st == EvaluationState.TRUE:
                return EvaluationState.FALSE, f"Value matches expected: {actual}", err
            elif st == EvaluationState.FALSE:
                return EvaluationState.TRUE, f"Value does not match expected: {actual}", err
            return EvaluationState.UNKNOWN, rsn, err

        # Numeric comparators: GREATER_THAN, GREATER_THAN_OR_EQUAL, LESS_THAN, LESS_THAN_OR_EQUAL
        if comparator in ("GREATER_THAN", "GREATER_THAN_OR_EQUAL", "LESS_THAN", "LESS_THAN_OR_EQUAL"):
            # Strict guard against boolean type coercion (in Python True==1, False==0)
            if isinstance(actual, bool) or isinstance(expected, bool):
                return EvaluationState.UNKNOWN, f"Cannot perform numeric comparison '{comparator}' on Boolean value: actual={actual}, expected={expected}", "Type mismatch: Boolean provided for numeric comparator"

            try:
                num_actual = float(actual)
                num_expected = float(expected)
            except (ValueError, TypeError):
                return EvaluationState.UNKNOWN, f"Cannot perform numeric comparison '{comparator}' on non-numeric value: actual={actual}, expected={expected}", "Type mismatch for numeric comparison"

            u_suffix = f" {unit}" if unit else ""
            if comparator == "GREATER_THAN":
                sat = num_actual > num_expected
                op_str = ">"
            elif comparator == "GREATER_THAN_OR_EQUAL":
                sat = num_actual >= num_expected
                op_str = ">="
            elif comparator == "LESS_THAN":
                sat = num_actual < num_expected
                op_str = "<"
            else:  # LESS_THAN_OR_EQUAL
                sat = num_actual <= num_expected
                op_str = "<="

            return (EvaluationState.TRUE if sat else EvaluationState.FALSE), f"{num_actual}{u_suffix} {op_str} {num_expected}{u_suffix} is {sat}", None

        # Range comparator: BETWEEN
        if comparator == "BETWEEN":
            # Strict guard against boolean type coercion
            if isinstance(actual, bool):
                return EvaluationState.UNKNOWN, f"Cannot perform range comparison BETWEEN on Boolean value: actual={actual}", "Type mismatch: Boolean provided for range"

            if not isinstance(expected, (list, tuple)) or len(expected) != 2:
                return EvaluationState.UNKNOWN, f"Comparator BETWEEN requires [min, max] list, got {expected}", "Malformed threshold array"

            if isinstance(expected[0], bool) or isinstance(expected[1], bool):
                return EvaluationState.UNKNOWN, f"Cannot perform range comparison BETWEEN with Boolean boundary in {expected}", "Type mismatch: Boolean boundary in range"

            try:
                num_actual = float(actual)
                min_val = float(expected[0])
                max_val = float(expected[1])
            except (ValueError, TypeError):
                return EvaluationState.UNKNOWN, f"Non-numeric values in BETWEEN comparison: actual={actual}, range={expected}", "Type mismatch in range"

            sat = min_val <= num_actual <= max_val
            u_suffix = f" {unit}" if unit else ""
            return (EvaluationState.TRUE if sat else EvaluationState.FALSE), f"{num_actual}{u_suffix} in [{min_val}, {max_val}]{u_suffix} is {sat}", None

        # Membership: CONTAINS, NOT_CONTAINS
        if comparator in ("CONTAINS", "NOT_CONTAINS"):
            sat = False
            if isinstance(actual, (list, tuple, set)):
                if isinstance(expected, (list, tuple, set)):
                    # Overlap / intersection
                    sat = bool(set(str(x).strip().lower() for x in actual) & set(str(y).strip().lower() for y in expected))
                else:
                    sat = any(str(expected).strip().lower() == str(item).strip().lower() for item in actual)
            elif isinstance(expected, (list, tuple, set)):
                # Patient finding is scalar, target is list of acceptable criteria
                sat = any(str(actual).strip().lower() == str(item).strip().lower() for item in expected)
            elif isinstance(actual, str) and isinstance(expected, str):
                sat = (expected.strip().lower() in actual.strip().lower()) or (actual.strip().lower() in expected.strip().lower())
            else:
                return EvaluationState.UNKNOWN, f"Cannot evaluate {comparator} between actual ({type(actual).__name__}) and expected ({type(expected).__name__})", "Incompatible collection type"

            if comparator == "NOT_CONTAINS":
                sat = not sat

            return (EvaluationState.TRUE if sat else EvaluationState.FALSE), f"Comparison '{comparator}' between '{actual}' and '{expected}' is {sat}", None

        # Clinical status: DOCUMENTED_FAILURE, CONTRAINDICATED
        if comparator in ("DOCUMENTED_FAILURE", "CONTRAINDICATED"):
            # Check boolean True or string matching
            if actual is True:
                return EvaluationState.TRUE, f"Condition status '{comparator}' documented as TRUE.", None
            if expected is not None and isinstance(actual, str) and actual.strip().upper() == str(expected).strip().upper():
                return EvaluationState.TRUE, f"Condition status '{comparator}' matches required therapy '{expected}'.", None
            if isinstance(actual, str) and actual.strip().upper() in (comparator, "TRUE", "YES", "CONFIRMED", "DOCUMENTED"):
                return EvaluationState.TRUE, f"Condition status '{comparator}' confirmed by '{actual}'.", None
            if actual is False or (isinstance(actual, str) and actual.strip().upper() in ("FALSE", "NO", "NONE")):
                return EvaluationState.FALSE, f"Condition status '{comparator}' is negative ({actual}).", None
            return EvaluationState.UNKNOWN, f"Ambiguous or incompatible value for {comparator}: '{actual}' ({type(actual).__name__})", "Ambiguous clinical status flag"

        return EvaluationState.UNKNOWN, f"Unrecognized comparator '{comparator}'", f"Unsupported comparator {comparator}"
