"""MedRule Evidence Verification Module.

Separates checking clinical criteria from checking whether sufficient evidence
was supplied to evaluate them. Analyzes required parameters, provided evidence,
missing fields, and clinical documentation completeness for every evaluated rule.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from medrule_engine.case_validator import CaseIntake
from medrule_engine.rule_registry import RuleRecord


@dataclass
class EvidenceVerificationReport:
    """Detailed evidence sufficiency accounting for a single rule."""
    rule_id: str
    required_parameters: List[str]
    provided_parameters: Dict[str, Any]
    missing_parameters: List[str]
    type_errors: List[str]
    is_sufficient: bool
    required_documentation: List[str] = field(default_factory=list)
    provided_documentation: List[str] = field(default_factory=list)
    missing_documentation: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


class EvidenceValidator:
    """Audits clinical case evidence against rule requirements."""

    def verify_rule_evidence(self, rule: RuleRecord, case: CaseIntake) -> EvidenceVerificationReport:
        """Inspect evidence completeness for a rule before or alongside evaluation."""
        required_params: List[str] = []
        self._extract_params_from_conditions(rule.conditions, required_params)

        provided: Dict[str, Any] = {}
        missing: List[str] = []
        type_errors: List[str] = []

        for p in required_params:
            is_present, val = case.get_evidence(p)
            if is_present and val is not None:
                provided[p] = val
            else:
                missing.append(p)

        # Check documentation prerequisites
        req_docs = list(rule.raw_data.get("required_documentation", []))
        prov_docs = list(case.supporting_documentation_provided)
        missing_docs = [d for d in req_docs if not any(d.lower() in pd.lower() or pd.lower() in d.lower() for pd in prov_docs)]

        is_sufficient = (len(missing) == 0 and len(type_errors) == 0)

        notes = []
        if missing:
            notes.append(f"{len(missing)} required clinical evidence parameter(s) missing: {missing}")
        if missing_docs:
            notes.append(f"{len(missing_docs)} required documentation item(s) missing: {missing_docs}")

        return EvidenceVerificationReport(
            rule_id=rule.rule_id,
            required_parameters=required_params,
            provided_parameters=provided,
            missing_parameters=missing,
            type_errors=type_errors,
            is_sufficient=is_sufficient,
            required_documentation=req_docs,
            provided_documentation=prov_docs,
            missing_documentation=missing_docs,
            notes=notes
        )

    def _extract_params_from_conditions(self, cond_obj: Dict[str, Any], params_out: List[str]):
        """Recursively gather all parameter names from a condition tree."""
        if not isinstance(cond_obj, dict):
            return

        for crit in cond_obj.get("criteria", []):
            param = crit.get("parameter")
            if param and param not in params_out:
                params_out.append(param)
            sub_conds = crit.get("sub_conditions")
            if sub_conds:
                self._extract_params_from_conditions(sub_conds, params_out)
