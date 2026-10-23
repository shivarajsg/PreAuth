"""MedRule Policy Router Module.

Deterministic policy applicability and routing component. Selects governing clinical
policies and candidate rules based on case domain, procedure code, modality,
line of business, jurisdiction, and date of service boundaries without heuristic guessing.
"""

from dataclasses import dataclass, field
import datetime
import logging
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from medrule_engine.case_validator import CaseIntake
from medrule_engine.rule_registry import RuleRecord, RuleRegistry

logger = logging.getLogger(__name__)

# Strict CPT / HCPCS 5-character alphanumeric syntax pattern
CPT_SYNTAX_PATTERN = re.compile(r"^[0-9]{4}[0-9A-Z]$|^[A-Z][0-9]{4}$")

# =============================================================================
# Authoritative CPT-to-Rule Mapping Inventories (Phase 6B Verified)
# Validated against reports/phase_06b_mapping_validation.md & authoritative policy sources.
# =============================================================================

ACTIVE_IPM_CPT_RULE_MAP: Dict[str, List[str]] = {
    "0213T": ["RULE-IPM-CGFACETBLOCKS-001"],
    "0214T": ["RULE-IPM-CGFACETBLOCKS-001"],
    "0215T": ["RULE-IPM-CGFACETBLOCKS-001"],
    "0216T": ["RULE-IPM-CGFACETBLOCKS-001"],
    "0217T": ["RULE-IPM-CGFACETBLOCKS-001"],
    "0218T": ["RULE-IPM-CGFACETBLOCKS-001"],
    "27096": ["RULE-IPM-CGSIINJECTIONS-001"],
    "62320": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "62321": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "62322": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "62323": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "62350": ["RULE-IPM-CGINFUSIONPUMPS-001"],
    "62351": ["RULE-IPM-CGINFUSIONPUMPS-001"],
    "62355": ["RULE-IPM-CGINFUSIONPUMPS-001"],
    "62360": ["RULE-IPM-CGINFUSIONPUMPS-001"],
    "62361": ["RULE-IPM-CGINFUSIONPUMPS-001"],
    "62362": ["RULE-IPM-CGINFUSIONPUMPS-001"],
    "63650": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "63655": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "63661": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "63662": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "63663": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "63664": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "63685": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "63688": ["RULE-IPM-CGSPINALCORDSTIM-001", "RULE-IPM-CGSPINALCORDSTIM-002"],
    "64479": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "64480": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "64483": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "64484": ["RULE-IPM-CGEPIDURALINJECTIONS-001", "RULE-IPM-CGEPIDURALINJECTIONS-002", "RULE-IPM-CGEPIDURALPUMPTRIALS-001"],
    "64490": ["RULE-IPM-CGFACETBLOCKS-001"],
    "64491": ["RULE-IPM-CGFACETBLOCKS-001"],
    "64492": ["RULE-IPM-CGFACETBLOCKS-001"],
    "64493": ["RULE-IPM-CGFACETBLOCKS-001"],
    "64494": ["RULE-IPM-CGFACETBLOCKS-001"],
    "64495": ["RULE-IPM-CGFACETBLOCKS-001"],
    "64510": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"],
    "64517": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"],
    "64520": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"],
    "64530": ["RULE-IPM-CGSYMPATHETICBLOCKS-001"],
    "64633": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
    "64634": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
    "64635": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
    "64636": ["RULE-IPM-CGFACETDENERVATION-001", "RULE-IPM-CGFACETDENERVATION-002"],
    "G0260": ["RULE-IPM-CGSIINJECTIONS-001"],
}

ACTIVE_AI_CPT_RULE_MAP: Dict[str, List[str]] = {
    "0042T": ["RULE-ADV-CG2015-001"],
    "70336": ["RULE-ADV-CG2055-001"],
    "70450": ["RULE-ADV-CG2008-001", "RULE-ADV-CG2008-002", "RULE-ADV-CG2008-003", "RULE-ADV-CG2008-004"],
    "70460": ["RULE-ADV-CG2008-001", "RULE-ADV-CG2008-003"],
    "70470": ["RULE-ADV-CG2008-003"],
    "70480": ["RULE-ADV-CG2054-001"],
    "70486": ["RULE-ADV-CG2047-001", "RULE-ADV-CG2047-002"],
    "70490": ["RULE-ADV-CG2039-001"],
    "70491": ["RULE-ADV-CG2039-001"],
    "70496": ["RULE-ADV-CG2009-001", "RULE-ADV-CG2009-002"],
    "70498": ["RULE-ADV-CG2040-001"],
    "70540": ["RULE-ADV-CG2048-001"],
    "70543": ["RULE-ADV-CG2048-001"],
    "70544": ["RULE-ADV-CG2011-001"],
    "70546": ["RULE-ADV-CG2011-001"],
    "70547": ["RULE-ADV-CG2041-001"],
    "70549": ["RULE-ADV-CG2041-001"],
    "70551": ["RULE-ADV-CG2012-001", "RULE-ADV-CG2012-002", "RULE-ADV-CG2012-004"],
    "70553": ["RULE-ADV-CG2012-001", "RULE-ADV-CG2012-002", "RULE-ADV-CG2012-003", "RULE-ADV-CG2012-004"],
    "70554": ["RULE-ADV-CG2028-001"],
    "70555": ["RULE-ADV-CG2028-001"],
    "71250": ["RULE-ADV-CG2018-001", "RULE-ADV-CG2018-003"],
    "71260": ["RULE-ADV-CG2018-001", "RULE-ADV-CG2018-002", "RULE-ADV-CG2018-003"],
    "71271": ["RULE-ADV-CG2030-001"],
    "71275": ["RULE-ADV-CG2020-001", "RULE-ADV-CG2020-002"],
    "71550": ["RULE-ADV-CG2019-001"],
    "71552": ["RULE-ADV-CG2019-001"],
    "71555": ["RULE-ADV-CG2021-001"],
    "72125": ["RULE-ADV-CG2016-001"],
    "72128": ["RULE-ADV-CG2056-001", "RULE-ADV-CG2056-002"],
    "72129": ["RULE-ADV-CG2056-001", "RULE-ADV-CG2056-002"],
    "72130": ["RULE-ADV-CG2056-001", "RULE-ADV-CG2056-002"],
    "72131": ["RULE-ADV-CG2036-001"],
    "72141": ["RULE-ADV-CG2017-001", "RULE-ADV-CG2017-002", "RULE-ADV-CG2017-003"],
    "72142": ["RULE-ADV-CG2017-001", "RULE-ADV-CG2017-002", "RULE-ADV-CG2017-003"],
    "72146": ["RULE-ADV-CG2057-001", "RULE-ADV-CG2057-002"],
    "72147": ["RULE-ADV-CG2057-001", "RULE-ADV-CG2057-002"],
    "72148": ["RULE-ADV-CG2037-001", "RULE-ADV-CG2037-002"],
    "72157": ["RULE-ADV-CG2057-001", "RULE-ADV-CG2057-002"],
    "72158": ["RULE-ADV-CG2037-001", "RULE-ADV-CG2037-003"],
    "72159": ["RULE-ADV-CG2053-001"],
    "72191": ["RULE-ADV-CG2043-001"],
    "72192": ["RULE-ADV-CG2042-001"],
    "72193": ["RULE-ADV-CG2042-001"],
    "72195": ["RULE-ADV-CG2045-001"],
    "72197": ["RULE-ADV-CG2045-001"],
    "72198": ["RULE-ADV-CG2044-001"],
    "73200": ["RULE-ADV-CG2062-001"],
    "73201": ["RULE-ADV-CG2062-001"],
    "73202": ["RULE-ADV-CG2062-001"],
    "73206": ["RULE-ADV-CG2063-001"],
    "73221": ["RULE-ADV-CG2065-001", "RULE-ADV-CG2065-002"],
    "73222": ["RULE-ADV-CG2065-001", "RULE-ADV-CG2065-002"],
    "73223": ["RULE-ADV-CG2065-001", "RULE-ADV-CG2065-002"],
    "73225": ["RULE-ADV-CG2064-001"],
    "73700": ["RULE-ADV-CG2032-001", "RULE-ADV-CG2032-002"],
    "73701": ["RULE-ADV-CG2032-001", "RULE-ADV-CG2032-002"],
    "73702": ["RULE-ADV-CG2032-002"],
    "73706": ["RULE-ADV-CG2033-001"],
    "73721": ["RULE-ADV-CG2035-001", "RULE-ADV-CG2035-002", "RULE-ADV-CG2035-003"],
    "73722": ["RULE-ADV-CG2035-001", "RULE-ADV-CG2035-002"],
    "73723": ["RULE-ADV-CG2035-001", "RULE-ADV-CG2035-002"],
    "73725": ["RULE-ADV-CG2034-001"],
    "74150": ["RULE-ADV-CG2001-001"],
    "74160": ["RULE-ADV-CG2001-001", "RULE-ADV-CG2001-002", "RULE-ADV-CG2001-003", "RULE-ADV-CG2001-004", "RULE-ADV-CG2001-005"],
    "74170": ["RULE-ADV-CG2001-001", "RULE-ADV-CG2001-002", "RULE-ADV-CG2001-003", "RULE-ADV-CG2001-004", "RULE-ADV-CG2001-005"],
    "74174": ["RULE-ADV-CG2005-001", "RULE-ADV-CG2005-002"],
    "74175": ["RULE-ADV-CG2000-010", "RULE-ADV-CG2000-011", "RULE-ADV-CG2002-001", "RULE-ADV-CG2002-002", "RULE-ADV-CG2005-001"],
    "74176": ["RULE-ADV-CG2000-002", "RULE-ADV-CG2000-004", "RULE-ADV-CG2000-005", "RULE-ADV-CG2000-010", "RULE-ADV-CG2000-012", "RULE-ADV-CG2000-013"],
    "74177": ["RULE-ADV-CG2000-002", "RULE-ADV-CG2000-003", "RULE-ADV-CG2000-004", "RULE-ADV-CG2000-005", "RULE-ADV-CG2000-006", "RULE-ADV-CG2000-007", "RULE-ADV-CG2000-008", "RULE-ADV-CG2000-009", "RULE-ADV-CG2000-011", "RULE-ADV-CG2000-012", "RULE-ADV-CG2000-013"],
    "74178": ["RULE-ADV-CG2000-002", "RULE-ADV-CG2000-006", "RULE-ADV-CG2000-008", "RULE-ADV-CG2000-009", "RULE-ADV-CG2000-012"],
    "74181": ["RULE-ADV-CG2004-001"],
    "74183": ["RULE-ADV-CG2000-003", "RULE-ADV-CG2004-001", "RULE-ADV-CG2004-002"],
    "74185": ["RULE-ADV-CG2003-001", "RULE-ADV-CG2003-002"],
    "74261": ["RULE-ADV-CG2022-001"],
    "74262": ["RULE-ADV-CG2022-001"],
    "74263": ["RULE-ADV-CG2023-001"],
    "74712": ["RULE-ADV-CG2027-001"],
    "74713": ["RULE-ADV-CG2027-001"],
    "75635": ["RULE-ADV-CG2006-001"],
    "76380": ["RULE-ADV-CG2029-001"],
    "76390": ["RULE-ADV-CG2010-001"],
    "76391": ["RULE-ADV-CG2038-001"],
    "76497": ["RULE-ADV-CG2061-002"],
    "76498": ["RULE-ADV-CG2061-001"],
    "77012": ["RULE-ADV-CG2026-001"],
    "77021": ["RULE-ADV-CG2026-001"],
    "77047": ["RULE-ADV-CG2014-002"],
    "77048": ["RULE-ADV-CG2014-001"],
    "77049": ["RULE-ADV-CG2014-001"],
    "77078": ["RULE-ADV-CG2024-001"],
    "77084": ["RULE-ADV-CG2007-001"],
    "78803": ["RULE-ADV-CG2052-001"],
    "78811": ["RULE-ADV-CG2013-001"],
    "78815": ["RULE-ADV-CG2013-001", "RULE-ADV-CG2046-001", "RULE-ADV-CG2046-002", "RULE-ADV-CG2046-003", "RULE-ADV-CG2046-004"],
    "78816": ["RULE-ADV-CG2046-001", "RULE-ADV-CG2046-003", "RULE-ADV-CG2046-004"],
    "78830": ["RULE-ADV-CG2052-001"],
    "G0219": ["RULE-ADV-CG2058-001"],
    "G0235": ["RULE-ADV-CG2058-001"],
    "G0252": ["RULE-ADV-CG2058-001"],
    "S8042": ["RULE-ADV-CG2031-001"],
}

ACTIVE_AI_SHARED_RULES: Dict[str, List[str]] = {
    "preamble": [
        "RULE-ADV-PREAMBLE-001",
        "RULE-ADV-CG2000-001"
    ],
    "place_of_service": [
        "RULE-ADV-EPOS2067-001",
        "RULE-ADV-EPOS2067-002",
        "RULE-ADV-EPOS2067-003",
        "RULE-ADV-EPOS2067-004",
        "RULE-ADV-EPOS2067-005"
    ],
    "retrospective_review": [
        "RULE-ADV-CG2066-001",
        "RULE-ADV-CG2066-002"
    ]
}

ACTIVE_IPM_SHARED_RULES: Dict[str, List[str]] = {
    "preamble": [
        "RULE-IPM-PREAMBLEIPM-001"
    ],
    "place_of_service": [
        "RULE-IPM-EPOS1755-001",
        "RULE-IPM-EPOS1755-002"
    ],
    "retrospective_review": []
}


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

        # 6. Strict procedure code syntax validation & whitespace normalization
        raw_code = case.procedure_code or ""
        proc_code = raw_code.strip().upper()
        if not proc_code:
            return RoutingResult(
                status="POLICY_NOT_APPLICABLE",
                routing_notes=["Procedure code is missing or empty."]
            )

        if not CPT_SYNTAX_PATTERN.match(proc_code):
            return RoutingResult(
                status="POLICY_NOT_APPLICABLE",
                routing_notes=[f"Procedure code '{raw_code}' is malformed or invalid syntax."]
            )

        # 7. Domain mapping lookup & primary procedure-specific routing authority
        if domain == "advanced_imaging":
            cpt_map = ACTIVE_AI_CPT_RULE_MAP
            shared_spec = ACTIVE_AI_SHARED_RULES
        elif domain == "interventional_pain_management":
            cpt_map = ACTIVE_IPM_CPT_RULE_MAP
            shared_spec = ACTIVE_IPM_SHARED_RULES
        else:
            cpt_map = {}
            shared_spec = {}

        # Primary authority: check if code is directly mapped in active domain
        if proc_code not in cpt_map:
            # Secondary symmetric cross-domain guards & explicit unsupported rejection
            if domain == "advanced_imaging":
                if proc_code in ACTIVE_IPM_CPT_RULE_MAP or (proc_code.isdigit() and (60000 <= int(proc_code) <= 69999 or int(proc_code) == 27096)):
                    return RoutingResult(
                        status="POLICY_NOT_APPLICABLE",
                        routing_notes=[f"Interventional pain procedure code '{proc_code}' is outside advanced_imaging clinical scope."]
                    )
                if proc_code.isdigit() and 93000 <= int(proc_code) <= 93999:
                    return RoutingResult(
                        status="POLICY_NOT_APPLICABLE",
                        routing_notes=[f"Cardiology procedure code '{proc_code}' is outside advanced_imaging clinical scope."]
                    )
                if proc_code.isdigit() and 10000 <= int(proc_code) <= 59999:
                    return RoutingResult(
                        status="POLICY_NOT_APPLICABLE",
                        routing_notes=[f"Surgical procedure code '{proc_code}' is outside advanced_imaging clinical scope."]
                    )
                return RoutingResult(
                    status="POLICY_NOT_APPLICABLE",
                    routing_notes=[f"Procedure code '{proc_code}' is not supported under active advanced_imaging clinical policies."]
                )

            elif domain == "interventional_pain_management":
                if proc_code in ACTIVE_AI_CPT_RULE_MAP or (proc_code.isdigit() and 70000 <= int(proc_code) <= 79999):
                    return RoutingResult(
                        status="POLICY_NOT_APPLICABLE",
                        routing_notes=[f"Diagnostic radiology procedure code '{proc_code}' is outside interventional_pain_management clinical scope."]
                    )
                if proc_code.isdigit() and 93000 <= int(proc_code) <= 93999:
                    return RoutingResult(
                        status="POLICY_NOT_APPLICABLE",
                        routing_notes=[f"Cardiology procedure code '{proc_code}' is outside interventional_pain_management clinical scope."]
                    )
                if proc_code.isdigit() and 10000 <= int(proc_code) <= 59999 and proc_code != "27096":
                    return RoutingResult(
                        status="POLICY_NOT_APPLICABLE",
                        routing_notes=[f"Non-pain surgical procedure code '{proc_code}' is outside interventional_pain_management clinical scope."]
                    )
                return RoutingResult(
                    status="POLICY_NOT_APPLICABLE",
                    routing_notes=[f"Procedure code '{proc_code}' is not supported under active interventional_pain_management clinical policies."]
                )

            return RoutingResult(
                status="POLICY_NOT_APPLICABLE",
                routing_notes=[f"Clinical domain '{domain}' has no active CPT procedure mapping."]
            )

        # 8. Assemble procedure-specific and conditionally applicable shared rules
        target_rule_ids = set(cpt_map[proc_code])

        # Shared general preamble rules (applicable only when procedure matches)
        for p_rid in shared_spec.get("preamble", []):
            target_rule_ids.add(p_rid)

        # Place of Service rules (only when outpatient POS applicability condition is met)
        pos_val = (case.place_of_service or "").strip().upper()
        outpatient_pos = {
            "OUTPATIENT_HOSPITAL", "AMBULATORY_SURGICAL_CENTER", "OFFICE",
            "POS_11", "POS_19", "POS_21", "POS_22", "POS_24",
            "POS 11", "POS 19", "POS 21", "POS 22", "POS 24"
        }
        if pos_val in outpatient_pos:
            for pos_rid in shared_spec.get("place_of_service", []):
                target_rule_ids.add(pos_rid)

        # Retrospective review rules (only when retrospective review context is indicated)
        is_retro = bool(
            policy_context and (
                policy_context.get("is_retrospective") or
                policy_context.get("review_type") == "RETROSPECTIVE"
            )
        )
        if is_retro:
            for retro_rid in shared_spec.get("retrospective_review", []):
                target_rule_ids.add(retro_rid)

        # 9. Filter and select active rules
        applicable_rules: List[RuleRecord] = []
        excluded_rules: List[Tuple[str, str]] = []
        selected_policies: Dict[str, Dict[str, str]] = {}
        case_modality = (case.modality or "").upper().strip()

        for rule in domain_rules:
            if rule.rule_id not in target_rule_ids:
                excluded_rules.append((rule.rule_id, f"Not applicable to procedure '{proc_code}'"))
                continue

            # Policy version status check: current_2026_verified only for active evaluation
            if rule.version_status != "current_2026_verified":
                excluded_rules.append((rule.rule_id, f"Quarantined/non-active version status '{rule.version_status}'"))
                continue

            # Modality check if case modality is specified
            rule_service = rule.clinical_service_or_procedure.lower()
            if case_modality:
                if case_modality in ("MRI", "MRA") and "ct" in rule_service and "mri" not in rule_service:
                    excluded_rules.append((rule.rule_id, f"Modality '{case_modality}' not applicable to rule service '{rule.clinical_service_or_procedure}'"))
                    continue
                elif case_modality in ("CT", "CTA") and "mri" in rule_service and "ct" not in rule_service:
                    excluded_rules.append((rule.rule_id, f"Modality '{case_modality}' not applicable to rule service '{rule.clinical_service_or_procedure}'"))
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

            applicable_rules.append(rule)

        if not applicable_rules:
            return RoutingResult(
                status="POLICY_NOT_APPLICABLE",
                excluded_rules=excluded_rules,
                selected_policies=list(selected_policies.values()),
                routing_notes=[f"No applicable rules found for procedure '{proc_code}' in domain '{domain}'."]
            )

        return RoutingResult(
            status="ROUTED",
            applicable_rules=applicable_rules,
            excluded_rules=excluded_rules,
            selected_policies=list(selected_policies.values()),
            routing_notes=[f"Successfully routed procedure '{proc_code}' to {len(applicable_rules)} candidate rules across {len(selected_policies)} policies."]
        )
