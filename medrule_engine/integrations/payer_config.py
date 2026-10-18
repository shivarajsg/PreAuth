"""MedRule Payer and Health Plan Configuration Manager.

Provides a strongly-typed, schema-validated, versioned model for payer-specific
coverage parameters, governing policy bindings, place of service restrictions,
contractual benefit limitations, and external dependencies.
Grounded directly in phase_3d_policy_applicability_matrix.csv and policy_dependency_mapping.csv.
"""

import csv
from dataclasses import asdict, dataclass, field
import datetime
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import jsonschema

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
APPLICABILITY_MATRIX_PATH = REPO_ROOT / "rulebook_collection" / "manifests" / "phase_3d_policy_applicability_matrix.csv"
DEPENDENCY_MAPPING_PATH = REPO_ROOT / "rulebook_collection" / "manifests" / "policy_dependency_mapping.csv"
SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "payer_plan_config_schema.json"


@dataclass(frozen=True)
class PayerPlanConfig:
    """Strongly-typed, immutable representation of a verified payer and plan configuration."""
    config_id: str
    payer_id: str
    plan_id: str
    line_of_business: str
    jurisdiction: str
    clinical_domain: str
    procedure_code: str
    effective_date_start: str
    effective_date_end: str
    governing_policy_id: str
    governing_policy_version: str
    provenance_source: str
    verification_status: str  # VERIFIED_ACTIVE, PLAN_SPECIFIC_ACCESS_REQUIRED, STATUTORY_OVERRIDE, PENDING_VERIFICATION, UNRESOLVED
    config_version: str = "1.0.0"
    product_id: Optional[str] = None
    procedure_name: Optional[str] = None
    governing_policy_title: Optional[str] = None
    place_of_service_rules: Dict[str, Any] = field(default_factory=dict)
    benefit_limitations: Dict[str, Any] = field(default_factory=dict)
    required_dependencies: List[str] = field(default_factory=list)
    reviewed_by: Optional[str] = None
    review_date: Optional[str] = None

    def is_effective_for_date(self, dos_str: str) -> bool:
        """Check whether date of service falls inside effective start and end dates."""
        try:
            dos = datetime.date.fromisoformat(dos_str)
            start = datetime.date.fromisoformat(self.effective_date_start)
            end = datetime.date.fromisoformat(self.effective_date_end)
            return start <= dos <= end
        except (ValueError, TypeError):
            return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)


class PayerPlanConfigManager:
    """Manages loading, schema validation, indexing, and lookup of payer & plan configurations."""

    def __init__(self, schema_file: Optional[Path] = None):
        self.schema_file = schema_file or SCHEMA_PATH
        with open(self.schema_file, "r", encoding="utf-8") as f:
            self.schema = json.load(f)
        self.validator = jsonschema.Draft7Validator(self.schema)
        self._configs: Dict[str, PayerPlanConfig] = {}
        self._index_by_key: Dict[Tuple[str, str, str], List[PayerPlanConfig]] = {}  # (domain, procedure, lob) -> configs

    def load_from_matrix(
        self,
        matrix_path: Optional[Path] = None,
        dep_path: Optional[Path] = None
    ) -> int:
        """Load and index configurations from verified Phase 3D applicability matrix."""
        mat_file = matrix_path or APPLICABILITY_MATRIX_PATH
        if not mat_file.exists():
            logger.warning("Policy applicability matrix not found at %s", mat_file)
            return 0

        self._configs.clear()
        self._index_by_key.clear()

        # Load dependencies map first
        dep_map: Dict[str, Dict[str, str]] = {}
        dep_file = dep_path or DEPENDENCY_MAPPING_PATH
        if dep_file.exists():
            with open(dep_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    dep_map[r["dependency_id"]] = dict(r)

        loaded_count = 0
        with open(mat_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                cid = f"CFG-{r['matrix_id']}"
                dom = r["clinical_domain"].strip()
                code = r["procedure_code"].strip()
                lob = r["line_of_business"].strip()

                # Extract dependencies
                dep_raw = r.get("contract_or_benefit_dependency", "")
                deps: List[str] = []
                for token in dep_raw.split(";"):
                    token = token.strip()
                    if "DEP-" in token:
                        for part in token.split():
                            if part.startswith("DEP-"):
                                clean_dep = part.rstrip(":").rstrip(",")
                                deps.append(clean_dep)

                # Parse place of service
                pos_text = r.get("place_of_service_requirement", "")
                pos_rules = {
                    "text_requirement": pos_text,
                    "requires_clinical_exception": "clinical exception" in pos_text.lower(),
                    "exception_policy_ref": "EPOS 2067" if "EPOS 2067" in pos_text else None
                }

                # Benefit limitations
                benefit_limits = {
                    "text": dep_raw,
                    "requires_tiering_step_therapy": "tiering" in dep_raw.lower(),
                    "tiering_protocol_id": "DEP-010" if "DEP-010" in deps else None,
                    "is_excluded_benefit": "exclusion" in dep_raw.lower() or "non-covered" in dep_raw.lower(),
                    "exclusion_schedule_ref": "DEP-015" if "DEP-015" in deps else None
                }

                config = PayerPlanConfig(
                    config_id=cid,
                    payer_id=r["payer_id"].strip(),
                    plan_id=r["plan_or_product"].strip(),
                    line_of_business=lob,
                    jurisdiction=r["jurisdiction"].strip(),
                    clinical_domain=dom,
                    procedure_code=code,
                    procedure_name=r.get("procedure_name", "").strip(),
                    effective_date_start=r["effective_date_start"].strip(),
                    effective_date_end=r["effective_date_end"].strip(),
                    governing_policy_id=r["governing_policy_id"].strip(),
                    governing_policy_title=r.get("governing_policy_title", "").strip(),
                    governing_policy_version=r["governing_policy_version"].strip(),
                    place_of_service_rules=pos_rules,
                    benefit_limitations=benefit_limits,
                    required_dependencies=deps,
                    provenance_source=r["source_evidence_citation"].strip(),
                    verification_status=r["applicability_status"].strip(),
                    config_version="1.0.0",
                    reviewed_by="Clinical SME Review Board",
                    review_date=r.get("verification_timestamp", "2026-10-18T17:00:00Z").split("T")[0]
                )

                # Validate against schema
                raw_dict = config.to_dict()
                errs = list(self.validator.iter_errors(raw_dict))
                if errs:
                    err_msg = "; ".join(e.message for e in errs[:3])
                    raise ValueError(f"Config {cid} failed schema validation: {err_msg}")

                self._configs[cid] = config
                idx_key = (dom, code, lob)
                self._index_by_key.setdefault(idx_key, []).append(config)
                loaded_count += 1

        return loaded_count

    def lookup_config(
        self,
        clinical_domain: str,
        procedure_code: str,
        line_of_business: str,
        date_of_service: str,
        payer_id: Optional[str] = None,
        plan_id: Optional[str] = None
    ) -> Tuple[Optional[PayerPlanConfig], List[str]]:
        """Look up verified payer configuration matching case criteria.
        
        Returns:
            Tuple: (matched_config, notes)
        """
        notes: List[str] = []
        idx_key = (clinical_domain, procedure_code, line_of_business)
        candidates = self._index_by_key.get(idx_key, [])

        if not candidates:
            # Check without LOB match to report specific mismatch
            domain_procs = [c for c in self._configs.values() if c.clinical_domain == clinical_domain and c.procedure_code == procedure_code]
            if domain_procs:
                available_lobs = list(set(c.line_of_business for c in domain_procs))
                notes.append(f"No configuration found for LOB '{line_of_business}'. Available LOBs: {available_lobs}")
            else:
                notes.append(f"No configuration found for domain '{clinical_domain}' and procedure '{procedure_code}'.")
            return None, notes

        # Filter by effective date
        date_matched = [c for c in candidates if c.is_effective_for_date(date_of_service)]
        if not date_matched:
            notes.append(f"Date of service '{date_of_service}' is outside effective windows for candidate configurations.")
            return None, notes

        # Filter by payer_id if provided
        if payer_id:
            payer_matched = [c for c in date_matched if c.payer_id.upper() == payer_id.upper()]
            if payer_matched:
                date_matched = payer_matched
            else:
                notes.append(f"Payer ID '{payer_id}' did not match candidate configurations; falling back to general candidates.")

        # Match exact plan_id if provided
        if plan_id:
            plan_matched = [c for c in date_matched if c.plan_id.upper() == plan_id.upper() or plan_id.upper() in c.plan_id.upper()]
            if plan_matched:
                return plan_matched[0], notes

        return date_matched[0], notes

    def get_config(self, config_id: str) -> Optional[PayerPlanConfig]:
        """Get configuration by its configuration ID (e.g., 'CFG-PAM-ADV-001' or 'PAM-ADV-001')."""
        if config_id in self._configs:
            return self._configs[config_id]
        alt_id = f"CFG-{config_id}" if not config_id.startswith("CFG-") else config_id.replace("CFG-", "")
        return self._configs.get(alt_id)

    def list_configs(self, domain: Optional[str] = None) -> List[PayerPlanConfig]:
        """List all indexed configurations, optionally filtered by domain."""
        if domain:
            return [c for c in self._configs.values() if c.clinical_domain == domain]
        return list(self._configs.values())

