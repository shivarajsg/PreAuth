"""MedRule Rule Registry Module.

Read-only, schema-validated repository of deterministic policy rules loaded from
all nine clinical domains. Enforces zero-approved governance, indexes rules for
efficient deterministic lookup, and prevents draft criteria from generating
binding authorization decisions.
"""

from dataclasses import dataclass
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import jsonschema

logger = logging.getLogger(__name__)

DEFAULT_DOMAINS_DIR = Path(__file__).resolve().parents[1] / "rulebook_collection" / "domains"
DEFAULT_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "rulebook_collection" / "schemas" / "medrule_rule_schema.json"


@dataclass(frozen=True)
class RuleRecord:
    """Immutable representation of an audited rule record."""
    rule_id: str
    domain: str
    document_type: str
    policy_title: str
    policy_version: str
    version_status: str
    source_file: str
    physical_page: int
    source_section: str
    source_quote: str
    clinical_service_or_procedure: str
    rule_type: str
    conditions: Dict[str, Any]
    decision_effect: str
    missing_information_behavior: str
    human_review_required: bool
    extraction_status: str
    review_notes: Optional[str]
    raw_data: Dict[str, Any]

    @property
    def is_approved(self) -> bool:
        """Strict governance flag: true ONLY if clinically vetted and approved."""
        return self.extraction_status == "APPROVED"

    @property
    def is_binding(self) -> bool:
        """Prior authorization decision support binding flag.
        Prototype and draft rules are ALWAYS non-binding.
        """
        return False


class RuleRegistry:
    """In-memory, read-only registry of validated MedRule policy rules."""

    def __init__(self, domains_dir: Optional[Path] = None, schema_path: Optional[Path] = None):
        self.domains_dir = domains_dir or DEFAULT_DOMAINS_DIR
        self.schema_path = schema_path or DEFAULT_SCHEMA_PATH
        
        self._rules_by_id: Dict[str, RuleRecord] = {}
        self._rules_by_domain: Dict[str, List[RuleRecord]] = {}
        self._loaded = False
        
        # Load canonical schema
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)
        self.validator = jsonschema.Draft7Validator(self.schema)

    def load_all_domains(self) -> int:
        """Load and validate draft_rules.json from all clinical domains.
        
        Returns:
            int: Total count of validated rules loaded into registry.
        """
        self._rules_by_id.clear()
        self._rules_by_domain.clear()

        domain_dirs = [d for d in self.domains_dir.iterdir() if d.is_dir()]
        total_loaded = 0

        for dom_dir in sorted(domain_dirs):
            rules_file = dom_dir / "rules" / "draft_rules.json"
            if not rules_file.exists():
                continue

            with open(rules_file, "r", encoding="utf-8") as f:
                raw_rules = json.load(f)

            domain_rules: List[RuleRecord] = []
            for r in raw_rules:
                rule_id = r.get("rule_id", "UNKNOWN")
                
                # Schema validation
                errors = list(self.validator.iter_errors(r))
                if errors:
                    err_msg = "; ".join(e.message for e in errors[:3])
                    raise ValueError(f"Rule {rule_id} failed canonical schema validation: {err_msg}")

                if rule_id in self._rules_by_id:
                    raise ValueError(f"Duplicate global rule ID detected: {rule_id}")

                # Strict governance check
                status = r.get("extraction_status")
                if status == "APPROVED":
                    raise ValueError(
                        f"Rule {rule_id} has extraction_status 'APPROVED'. "
                        "Phase 3 governance strictly forbids automated approval prior to formal clinical SME review."
                    )

                page_info = r.get("source_page", {})
                phys_page = page_info.get("physical_page") if isinstance(page_info, dict) else int(page_info)

                record = RuleRecord(
                    rule_id=rule_id,
                    domain=r.get("domain", dom_dir.name),
                    document_type=r.get("document_type", ""),
                    policy_title=r.get("policy_title", ""),
                    policy_version=r.get("policy_version", ""),
                    version_status=r.get("version_status", "current_2026_verified"),
                    source_file=r.get("source_file", ""),
                    physical_page=phys_page,
                    source_section=r.get("source_section", ""),
                    source_quote=r.get("source_quote", ""),
                    clinical_service_or_procedure=r.get("clinical_service_or_procedure", ""),
                    rule_type=r.get("rule_type", ""),
                    conditions=r.get("conditions", {}),
                    decision_effect=r.get("decision_effect", "UNDETERMINED"),
                    missing_information_behavior=r.get("missing_information_behavior", "CANNOT_DETERMINE"),
                    human_review_required=bool(r.get("human_review_required", False) or status == "NEEDS_HUMAN_REVIEW"),
                    extraction_status=status,
                    review_notes=r.get("review_notes"),
                    raw_data=r
                )

                self._rules_by_id[rule_id] = record
                domain_rules.append(record)
                total_loaded += 1

            self._rules_by_domain[dom_dir.name] = domain_rules

        self._loaded = True
        return total_loaded

    def get_rule(self, rule_id: str) -> Optional[RuleRecord]:
        """Fetch rule by unique ID."""
        if not self._loaded:
            self.load_all_domains()
        return self._rules_by_id.get(rule_id)

    def get_rules_by_domain(self, domain: str) -> List[RuleRecord]:
        """Fetch all rules belonging to a clinical domain."""
        if not self._loaded:
            self.load_all_domains()
        return list(self._rules_by_domain.get(domain, []))

    def get_all_rules(self) -> List[RuleRecord]:
        """Fetch all loaded rules."""
        if not self._loaded:
            self.load_all_domains()
        return list(self._rules_by_id.values())

    def get_statistics(self) -> Dict[str, Any]:
        """Return counts by domain, status, and governance."""
        if not self._loaded:
            self.load_all_domains()

        stats: Dict[str, Any] = {
            "total_rules": len(self._rules_by_id),
            "domains": {},
            "status_counts": {
                "DRAFT": 0,
                "NEEDS_HUMAN_REVIEW": 0,
                "APPROVED": 0
            },
            "governance_zero_approved_enforced": True
        }

        for dom, r_list in self._rules_by_domain.items():
            d_cnt = sum(1 for r in r_list if r.extraction_status == "DRAFT")
            h_cnt = sum(1 for r in r_list if r.extraction_status == "NEEDS_HUMAN_REVIEW")
            a_cnt = sum(1 for r in r_list if r.extraction_status == "APPROVED")
            stats["domains"][dom] = {
                "total": len(r_list),
                "DRAFT": d_cnt,
                "NEEDS_HUMAN_REVIEW": h_cnt,
                "APPROVED": a_cnt
            }
            stats["status_counts"]["DRAFT"] += d_cnt
            stats["status_counts"]["NEEDS_HUMAN_REVIEW"] += h_cnt
        return stats

    def register_rule(self, rule_data: Dict[str, Any]) -> RuleRecord:
        """Register an individual rule with schema validation and duplicate ID enforcement."""
        if not self._loaded:
            self.load_all_domains()

        rule_id = rule_data.get("rule_id", "UNKNOWN")
        if rule_id in self._rules_by_id:
            raise ValueError(f"Duplicate global rule ID detected: {rule_id}")

        errors = list(self.validator.iter_errors(rule_data))
        if errors:
            raise ValueError(f"Rule {rule_id} failed schema validation: {errors[0].message}")

        status = rule_data.get("extraction_status")
        if status == "APPROVED":
            raise ValueError(f"Rule {rule_id} cannot be registered with status 'APPROVED' before clinical review.")

        page_info = rule_data.get("source_page", {})
        phys_page = page_info.get("physical_page") if isinstance(page_info, dict) else int(page_info)

        record = RuleRecord(
            rule_id=rule_id,
            domain=rule_data.get("domain", "custom"),
            document_type=rule_data.get("document_type", ""),
            policy_title=rule_data.get("policy_title", ""),
            policy_version=rule_data.get("policy_version", ""),
            version_status=rule_data.get("version_status", "current_2026_verified"),
            source_file=rule_data.get("source_file", ""),
            physical_page=phys_page,
            source_section=rule_data.get("source_section", ""),
            source_quote=rule_data.get("source_quote", ""),
            clinical_service_or_procedure=rule_data.get("clinical_service_or_procedure", ""),
            rule_type=rule_data.get("rule_type", ""),
            conditions=rule_data.get("conditions", {}),
            decision_effect=rule_data.get("decision_effect", "UNDETERMINED"),
            missing_information_behavior=rule_data.get("missing_information_behavior", "CANNOT_DETERMINE"),
            human_review_required=bool(rule_data.get("human_review_required", False) or status == "NEEDS_HUMAN_REVIEW"),
            extraction_status=status,
            review_notes=rule_data.get("review_notes"),
            raw_data=rule_data
        )

        self._rules_by_id[rule_id] = record
        dom = record.domain
        if dom not in self._rules_by_domain:
            self._rules_by_domain[dom] = []
        self._rules_by_domain[dom].append(record)
        return record

    def attach_governance_db(self, db: Any) -> None:
        """Attach a persistent governance database instance."""
        self._governance_db = db

    def get_governance_status(self, rule_id: str) -> str:
        """Fetch the workflow governance status for a rule (e.g. DRAFT, IN_REVIEW, APPROVED)."""
        if hasattr(self, "_governance_db") and self._governance_db:
            state = self._governance_db.get_rule_governance_state(rule_id)
            if state:
                return state.get("workflow_status", "DRAFT")
        rule = self.get_rule(rule_id)
        if rule:
            return rule.extraction_status
        return "UNKNOWN"

