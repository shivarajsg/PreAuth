"""MedRule Policy Router Module.

Deterministic policy applicability and routing component. Selects governing clinical
policies and candidate rules based on case domain, procedure code, modality,
line of business, jurisdiction, and date of service boundaries without heuristic guessing.
"""

from dataclasses import dataclass, field
import datetime
import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from medrule_engine.case_validator import CaseIntake
from medrule_engine.rule_registry import RuleRecord, RuleRegistry

logger = logging.getLogger(__name__)


@dataclass
class RoutingResult:
    """Outcome of deterministic policy routing."""
    status: str  # ROUTED, POLICY_NOT_APPLICABLE, POLICY_VERSION_UNRESOLVED, MANUAL_REVIEW_REQUIRED
    applicable_rules: List[RuleRecord] = field(default_factory=list)
    excluded_rules: List[Tuple[str, str]] = field(default_factory=list)  # (rule_id, reason)
    selected_policies: List[Dict[str, str]] = field(default_factory=list)
    routing_notes: List[str] = field(default_factory=list)
    unresolved_dependencies: List[str] = field(default_factory=list)


class PolicyRouter:
    """Routes structured cases to applicable policy rule sets."""

    def __init__(self, registry: RuleRegistry):
        self.registry = registry

    def route_case(
        self,
        case: CaseIntake,
        target_rule_ids: Optional[List[str]] = None,
        policy_context: Optional[Dict[str, Any]] = None
    ) -> RoutingResult:
        """Deterministically determine which rules apply to a case.

        Args:
            case: Validated CaseIntake object.
            target_rule_ids: Optional explicit rule ID list (for targeted testing).
            policy_context: Optional context dictionary for plan dependencies or version overrides.

        Returns:
            RoutingResult
        """
        # 1. Check plan-specific or external policy section dependencies from context first
        if policy_context:
            if policy_context.get("unresolved_plan_dependency"):
                dep_msg = str(policy_context.get("unresolved_plan_dependency"))
                return RoutingResult(
                    status="MANUAL_REVIEW_REQUIRED",
                    unresolved_dependencies=[dep_msg],
                    routing_notes=[f"Unresolved plan-specific dependency: {dep_msg}. Requires clinical manual review."]
                )
            if policy_context.get("unresolved_policy_section_dependency"):
                sec_dep = str(policy_context.get("unresolved_policy_section_dependency"))
                return RoutingResult(
                    status="POLICY_VERSION_UNRESOLVED",
                    unresolved_dependencies=[sec_dep],
                    routing_notes=[f"Unresolved governing policy section dependency: {sec_dep}. Evaluation cannot proceed."]
                )

        # 2. If explicit rule IDs are requested (e.g. for unit testing or targeted evaluation)
        if target_rule_ids is not None:
            if len(target_rule_ids) == 0:
                return RoutingResult(
                    status="POLICY_NOT_APPLICABLE",
                    routing_notes=["Empty candidate rule set requested."]
                )
            applicable = []
            excluded = []
            for rid in target_rule_ids:
                rule = self.registry.get_rule(rid)
                if rule:
                    applicable.append(rule)
                else:
                    excluded.append((rid, "Rule ID not found in registry"))

            if not applicable:
                return RoutingResult(
                    status="POLICY_NOT_APPLICABLE",
                    excluded_rules=excluded,
                    routing_notes=["None of the requested target_rule_ids could be found in registry."]
                )
            return RoutingResult(
                status="ROUTED",
                applicable_rules=applicable,
                excluded_rules=excluded,
                routing_notes=[f"Routed to {len(applicable)} explicitly requested rules."]
            )

        # 3. Check clinical domain
        domain = case.clinical_domain
        domain_rules = self.registry.get_rules_by_domain(domain)
        if not domain_rules:
            return RoutingResult(
                status="POLICY_NOT_APPLICABLE",
                routing_notes=[f"No active rules configured for clinical domain '{domain}'."]
            )

        # 4. Check Date of Service (DOS) validity and policy version boundaries
        try:
            dos = datetime.date.fromisoformat(case.requested_date_of_service)
        except (ValueError, TypeError):
            return RoutingResult(
                status="POLICY_VERSION_UNRESOLVED",
                routing_notes=[f"Invalid or missing requested_date_of_service: '{case.requested_date_of_service}'."]
            )

        # MedRule 2026 Guidelines effective boundary: 2026-01-01 onwards
        # For historical dates of service (e.g. < 2026-01-01), historical evaluation mode must be explicit.
        if dos < datetime.date(2026, 1, 1):
            if not (policy_context and policy_context.get("allow_historical_evaluation")):
                return RoutingResult(
                    status="POLICY_VERSION_UNRESOLVED",
                    routing_notes=[
                        f"Requested date of service ({dos.isoformat()}) precedes the effective date "
                        "of the 2026 governing guidelines (effective 2026-01-01). "
                        "Historical policy retrieval required."
                    ]
                )

        # Centene-specific revision date boundary (CP.MP.107 Rev. 08/26 effective 2026-08-01)
        if domain == "centene_dme_orthotics_prosthetics" and dos < datetime.date(2026, 8, 1):
            if not (policy_context and policy_context.get("allow_historical_evaluation")):
                return RoutingResult(
                    status="POLICY_VERSION_UNRESOLVED",
                    routing_notes=[
                        f"Date of service {dos.isoformat()} precedes effective date 2026-08-01 of active Centene CP.MP.107 Rev. 08/26. "
                        "Requires interim policy version evaluation."
                    ]
                )

        # 5. Check Line of Business (LOB)
        lob = (case.line_of_business or "").upper().strip()
        valid_lobs = {"COMMERCIAL", "MEDICARE_ADVANTAGE", "MEDICAID"}
        if not lob or lob == "OTHER" or lob not in valid_lobs:
            return RoutingResult(
                status="MANUAL_REVIEW_REQUIRED",
                routing_notes=[
                    f"Unrecognized, empty, or unverified line_of_business '{case.line_of_business}'. "
                    "MedRule does not assume commercial applicability without verification. Requires clinical manual review."
                ]
            )

        # 6. Check for malformed or cross-domain incompatible procedure code
        proc_code = (case.procedure_code or "").upper().strip()
        if proc_code and (proc_code.startswith("INVALID") or not proc_code.replace("-", "").isalnum()):
            return RoutingResult(
                status="POLICY_NOT_APPLICABLE",
                routing_notes=[f"Procedure code '{case.procedure_code}' is malformed or invalid."]
            )

        # Cross-domain scope guard: Diagnostic radiology codes (70000-76999, 78000-79999) do not belong in IPM
        if proc_code and proc_code.isdigit():
            code_num = int(proc_code)
            if domain == "interventional_pain_management" and (70000 <= code_num <= 79999):
                return RoutingResult(
                    status="POLICY_NOT_APPLICABLE",
                    routing_notes=[f"Diagnostic radiology procedure code '{case.procedure_code}' is outside interventional_pain_management clinical scope."]
                )

        applicable_rules: List[RuleRecord] = []
        excluded_rules: List[Tuple[str, str]] = []
        selected_policies: Dict[str, Dict[str, str]] = {}

        # 6. Filter rules by modality / procedure code / service scope
        # If modality or procedure_name is supplied, match relevant rules in domain
        case_modality = (case.modality or "").upper()
        proc_code = (case.procedure_code or "").upper()
        proc_name = (case.procedure_name or "").lower()

        for rule in domain_rules:
            # Policy version status check: current_2026_verified only for active evaluation
            if rule.version_status != "current_2026_verified":
                excluded_rules.append((rule.rule_id, f"Quarantined/non-active version status '{rule.version_status}'"))
                continue

            # Record selected policy metadata
            pol_key = f"{rule.policy_title}::{rule.policy_version}"
            if pol_key not in selected_policies:
                selected_policies[pol_key] = {
                    "policy_title": rule.policy_title,
                    "policy_version": rule.policy_version,
                    "version_status": rule.version_status,
                    "domain": rule.domain
                }

            # Procedure / Modality scope filtering
            rule_service = rule.clinical_service_or_procedure.lower()
            
            # If rule is a domain-wide general prerequisite or general medical necessity standard
            is_general_rule = any(kw in rule_service for kw in [
                "general", "all advanced", "preamble", "place of service", "durable medical equipment"
            ])
            
            # Modality match check
            modality_matches = True
            if case_modality:
                if case_modality in ("MRI", "MRA") and "ct" in rule_service and "mri" not in rule_service:
                    modality_matches = False
                elif case_modality in ("CT", "CTA") and "mri" in rule_service and "ct" not in rule_service:
                    modality_matches = False

            if is_general_rule or modality_matches:
                applicable_rules.append(rule)
            else:
                excluded_rules.append((rule.rule_id, f"Modality '{case_modality}' not applicable to rule service '{rule.clinical_service_or_procedure}'"))

        if not applicable_rules:
            return RoutingResult(
                status="POLICY_NOT_APPLICABLE",
                excluded_rules=excluded_rules,
                selected_policies=list(selected_policies.values()),
                routing_notes=[f"No applicable rules found for procedure '{case.procedure_code}' / modality '{case.modality}' in domain '{domain}'."]
            )

        return RoutingResult(
            status="ROUTED",
            applicable_rules=applicable_rules,
            excluded_rules=excluded_rules,
            selected_policies=list(selected_policies.values()),
            routing_notes=[f"Successfully routed to {len(applicable_rules)} candidate rules across {len(selected_policies)} policies."]
        )
