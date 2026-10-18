"""MedRule Clinical Data Intake and Normalization Adapter.

Maps and normalizes incoming clinical records (e.g. synthetic EHR extracts,
progress notes, diagnostic labs, imaging findings) into the canonical
MedRule CaseIntake schema while enforcing strict data minimization.
"""

from dataclasses import dataclass, field
import datetime
import logging
from typing import Any, Dict, List, Optional, Tuple

from medrule_engine.case_validator import CaseIntake, CaseValidator
from medrule_engine.integrations.base import (
    BaseConnector,
    ConnectorCategory,
    ConnectorMode,
    InvalidConnectorResponseError,
    SecurityContext,
)

logger = logging.getLogger(__name__)


class ClinicalDataIntakeAdapter(BaseConnector):
    """Adapter normalizing raw clinical intake records into validated CaseIntake payloads."""

    def __init__(
        self,
        name: str = "ClinicalDataIntakeAdapter",
        mode: ConnectorMode = ConnectorMode.DISABLED,
        validator: Optional[CaseValidator] = None
    ):
        super().__init__(
            name=name,
            category=ConnectorCategory.CLINICAL_DATA,
            mode=mode,
            timeout_ms=2000.0,
            max_retries=1,
            required_scope="connectors:clinical_data:ingest"
        )
        self.validator = validator or CaseValidator()

    def _validate_request(self, payload: Dict[str, Any]) -> None:
        """Verify minimum raw payload requirements."""
        if not isinstance(payload, dict):
            raise ValueError("Clinical intake payload must be a JSON dictionary.")
        if not payload.get("case_id"):
            raise ValueError("Clinical intake payload requires 'case_id'.")
        if not payload.get("clinical_domain"):
            raise ValueError("Clinical intake payload requires 'clinical_domain'.")

    def _do_execute(
        self,
        payload: Dict[str, Any],
        security_context: SecurityContext
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        """Normalize raw payload, strip unneeded identifiers, and validate against case schema."""
        # Data minimization: strip unnecessary demographic/identifying attributes
        minimized = dict(payload)
        for sensitive_key in ("ssn", "social_security_number", "phone", "email", "address", "patient_address", "mrn_raw"):
            minimized.pop(sensitive_key, None)

        # Standardize date formats if present
        for date_key in ("requested_date_of_service", "request_date"):
            if date_key in minimized and minimized[date_key]:
                val = str(minimized[date_key]).split("T")[0]
                minimized[date_key] = val

        # Validate against canonical case schema
        is_valid, errs, case_obj = self.validator.validate(minimized)
        if not is_valid or not case_obj:
            raise InvalidConnectorResponseError(
                f"Clinical data normalization failed case validation: {'; '.join(errs)}",
                raw_payload=errs
            )

        provenance = {
            "adapter": self.name,
            "minimized_fields_scrubbed": True,
            "schema_version": "1.0.0",
            "ingested_by": security_context.caller_id
        }

        return minimized, "NORMALIZED_SUCCESS", provenance

    def normalize(self, raw_payload: Dict[str, Any], security_context: SecurityContext) -> Tuple[bool, Optional[Dict[str, Any]], List[str]]:
        """Convenience functional wrapper returning (is_valid, normalized_payload, errors)."""
        result = self.execute(raw_payload, security_context)
        if not result.is_success:
            return False, None, [result.error_message or "Normalization failed"]
        return True, result.data, []

    def minimize_and_extract(
        self,
        clinical_evidence: Dict[str, Any],
        clinical_domain: str
    ) -> Tuple[Dict[str, Any], List[str]]:
        """Extract relevant clinical evidence and scrub all direct identifiers (PHI).
        
        Returns:
            Tuple[Dict[str, Any], List[str]]: (minimized_evidence, removed_fields)
        """
        if not isinstance(clinical_evidence, dict):
            return {}, []

        minimized = dict(clinical_evidence)
        removed: List[str] = []

        sensitive_fields = (
            "ssn", "social_security_number", "phone", "email",
            "address", "patient_address", "mrn_raw", "patient_name",
            "full_name", "date_of_birth", "dob"
        )
        for sf in sensitive_fields:
            if sf in minimized:
                minimized.pop(sf)
                removed.append(sf)

        return minimized, removed

