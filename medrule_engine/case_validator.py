"""MedRule Case Intake Validation Module.

Validates structured prior authorization case intake payloads against canonical
case_schema.json. Enforces strict type consistency, absence preservation,
and explicit error reporting without silent type coercion.
"""

from dataclasses import dataclass, field
import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import jsonschema

SCHEMA_PATH = Path(__file__).parent / "case_schema.json"


@dataclass(frozen=True)
class CaseIntake:
    """Strongly-typed wrapper for validated case intake payload."""
    case_id: str
    clinical_domain: str
    procedure_code: str
    procedure_name: str
    requested_date_of_service: str
    line_of_business: str
    payer_id: str
    clinical_evidence: Dict[str, Any]
    member_id: Optional[str] = None
    patient_age_years: Optional[float] = None
    patient_gender: Optional[str] = None
    modality: Optional[str] = None
    place_of_service: Optional[str] = None
    primary_diagnosis_code: Optional[str] = None
    secondary_diagnosis_codes: List[str] = field(default_factory=list)
    diagnosis_description: Optional[str] = None
    plan_id: Optional[str] = None
    jurisdiction: Optional[str] = None
    request_date: Optional[str] = None
    supporting_documentation_provided: List[str] = field(default_factory=list)
    ordering_provider: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    evidence_provenance: Dict[str, Any] = field(default_factory=dict)
    raw_payload: Dict[str, Any] = field(default_factory=dict, repr=False)

    def get_evidence(self, parameter: str) -> Tuple[bool, Any]:
        """Look up a clinical evidence parameter.
        
        Returns:
            Tuple[bool, Any]: (is_present, value)
            If the parameter is absent, returns (False, None).
            If present (even if value is False or None), returns (True, value).
        """
        # First check explicit clinical_evidence dictionary
        if parameter in self.clinical_evidence:
            return True, self.clinical_evidence[parameter]
        
        # Check standard top-level fields that rules frequently evaluate
        if parameter == "patient_age_years" and self.patient_age_years is not None:
            return True, self.patient_age_years
        if parameter == "patient_gender" and self.patient_gender is not None:
            return True, self.patient_gender
        if parameter == "place_of_service" and self.place_of_service is not None:
            return True, self.place_of_service
        if parameter == "primary_diagnosis_code" and self.primary_diagnosis_code is not None:
            return True, self.primary_diagnosis_code
        if parameter == "ordering_provider_license" and self.ordering_provider:
            return True, self.ordering_provider.get("is_licensed")
            
        return False, None


class CaseValidator:
    """Validates case data dictionaries against the JSON schema."""

    def __init__(self, schema_file: Optional[Path] = None):
        schema_to_load = schema_file or SCHEMA_PATH
        with open(schema_to_load, "r", encoding="utf-8") as f:
            self.schema = json.load(f)
        self.validator = jsonschema.Draft7Validator(self.schema)

    def validate(self, case_dict: Dict[str, Any]) -> Tuple[bool, List[str], Optional[CaseIntake]]:
        """Validate a case payload.

        Returns:
            Tuple: (is_valid, list_of_error_messages, CaseIntake_object_if_valid)
        """
        if not isinstance(case_dict, dict):
            return False, ["Case payload must be a JSON object (dictionary)"], None

        errors: List[str] = []
        for err in self.validator.iter_errors(case_dict):
            path_str = ".".join(str(p) for p in err.path) or "root"
            errors.append(f"[{path_str}] {err.message}")

        if errors:
            return False, sorted(errors), None

        # Additional semantic date checks
        dos_str = case_dict.get("requested_date_of_service")
        if dos_str:
            try:
                datetime.date.fromisoformat(dos_str)
            except ValueError:
                errors.append(f"Invalid requested_date_of_service format '{dos_str}', must be YYYY-MM-DD")

        req_date_str = case_dict.get("request_date")
        if req_date_str:
            try:
                datetime.date.fromisoformat(req_date_str)
            except ValueError:
                errors.append(f"Invalid request_date format '{req_date_str}', must be YYYY-MM-DD")

        if errors:
            return False, sorted(errors), None

        # Build typed CaseIntake object
        # NOTE: Do NOT default missing clinical evidence fields to false or zero!
        case_obj = CaseIntake(
            case_id=case_dict["case_id"],
            clinical_domain=case_dict["clinical_domain"],
            procedure_code=case_dict["procedure_code"],
            procedure_name=case_dict["procedure_name"],
            requested_date_of_service=case_dict["requested_date_of_service"],
            line_of_business=case_dict["line_of_business"],
            payer_id=case_dict["payer_id"],
            clinical_evidence=dict(case_dict.get("clinical_evidence", {})),
            member_id=case_dict.get("member_id"),
            patient_age_years=case_dict.get("patient_age_years"),
            patient_gender=case_dict.get("patient_gender"),
            modality=case_dict.get("modality"),
            place_of_service=case_dict.get("place_of_service"),
            primary_diagnosis_code=case_dict.get("primary_diagnosis_code"),
            secondary_diagnosis_codes=list(case_dict.get("secondary_diagnosis_codes", [])),
            diagnosis_description=case_dict.get("diagnosis_description"),
            plan_id=case_dict.get("plan_id"),
            jurisdiction=case_dict.get("jurisdiction"),
            request_date=case_dict.get("request_date"),
            supporting_documentation_provided=list(case_dict.get("supporting_documentation_provided", [])),
            ordering_provider=case_dict.get("ordering_provider"),
            notes=case_dict.get("notes"),
            evidence_provenance=dict(case_dict.get("evidence_provenance", {})),
            raw_payload=case_dict
        )

        return True, [], case_obj


def validate_case(case_dict: Dict[str, Any]) -> Tuple[bool, List[str], Optional[CaseIntake]]:
    """Convenience functional wrapper for CaseValidator."""
    validator = CaseValidator()
    return validator.validate(case_dict)
