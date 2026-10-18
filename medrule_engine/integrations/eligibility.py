"""MedRule Member Eligibility Integration Module.

Defines the contract and strongly typed models for verifying synthetic member
enrollment status and active coverage period boundaries across health plans.
"""

from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List, Optional, Tuple

from medrule_engine.integrations.base import (
    BaseConnector,
    ConnectorCategory,
    ConnectorMode,
    InvalidConnectorResponseError,
    SecurityContext,
)


@dataclass(frozen=True)
class EligibilityRequest:
    """Strongly typed input model for member eligibility inquiry."""
    member_id: str
    date_of_service: str
    payer_id: str
    plan_id: Optional[str] = None
    line_of_business: Optional[str] = None
    patient_dob: Optional[str] = None
    subscriber_id: Optional[str] = None


@dataclass(frozen=True)
class EligibilityResponse:
    """Strongly typed verification outcome for member eligibility."""
    is_eligible: bool
    member_id: str
    payer_id: str
    eligibility_status: str  # ACTIVE_COVERAGE, INELIGIBLE_MEMBER_NOT_FOUND, COVERAGE_TERMINATED, DATE_OUTSIDE_COVERAGE_PERIOD, PLAN_ID_MISMATCH
    coverage_start: Optional[str] = None
    coverage_end: Optional[str] = None
    plan_id: Optional[str] = None
    line_of_business: Optional[str] = None
    ineligibility_reason: Optional[str] = None
    verification_reference: Optional[str] = None
    provenance_metadata: Dict[str, Any] = field(default_factory=dict)


class EligibilityConnector(BaseConnector):
    """Abstract interface for payer member eligibility adapters."""

    def __init__(
        self,
        name: str = "PayerEligibilityConnector",
        mode: ConnectorMode = ConnectorMode.DISABLED,
        timeout_ms: float = 3000.0,
        max_retries: int = 2
    ):
        super().__init__(
            name=name,
            category=ConnectorCategory.ELIGIBILITY,
            mode=mode,
            timeout_ms=timeout_ms,
            max_retries=max_retries,
            required_scope="connectors:eligibility:read"
        )

    def _validate_request(self, payload: Dict[str, Any]) -> None:
        """Enforce presence of mandatory fields."""
        if not payload.get("member_id"):
            raise ValueError("Eligibility inquiry requires non-empty 'member_id'.")
        if not payload.get("date_of_service"):
            raise ValueError("Eligibility inquiry requires non-empty 'date_of_service'.")
        if not payload.get("payer_id"):
            raise ValueError("Eligibility inquiry requires non-empty 'payer_id'.")
        # Validate date format
        try:
            datetime.date.fromisoformat(payload["date_of_service"])
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date_of_service format: '{payload.get('date_of_service')}'. Expected YYYY-MM-DD.")

    def check_eligibility(
        self,
        request: EligibilityRequest,
        security_context: Optional[SecurityContext] = None
    ) -> EligibilityResponse:
        """Execute eligibility verification inquiry and return structured EligibilityResponse."""
        sec_ctx = security_context or SecurityContext(
            caller_id="INTAKE_ORCHESTRATOR",
            role="INTAKE_COORDINATOR",
            scopes={"connectors:eligibility:read"},
            is_authenticated=True
        )
        payload = {
            "member_id": request.member_id,
            "date_of_service": request.date_of_service,
            "payer_id": request.payer_id,
            "plan_id": request.plan_id,
            "line_of_business": request.line_of_business,
            "patient_dob": request.patient_dob,
            "subscriber_id": request.subscriber_id
        }
        res = self.execute(payload, sec_ctx)
        if not res.is_success:
            if res.error_code == "SERVICE_UNAVAILABLE":
                from medrule_engine.integrations.base import ServiceUnavailableError
                raise ServiceUnavailableError(self.name)
            elif res.error_code == "TIMEOUT_EXHAUSTED":
                from medrule_engine.integrations.base import TimeoutExhaustedError
                raise TimeoutExhaustedError(self.name, self.max_retries, self.timeout_ms)
            elif res.error_code == "AUTHENTICATION_FAILED":
                from medrule_engine.integrations.base import AuthenticationError
                raise AuthenticationError(res.error_message or "Authentication failed")
            else:
                raise InvalidConnectorResponseError(
                    res.error_message or f"Eligibility check failed with code {res.status_code}",
                    raw_payload=res.data
                )

        data = res.data or {}
        if "is_eligible" not in data or "eligibility_status" not in data:
            raise InvalidConnectorResponseError(
                "Eligibility response missing mandatory outcome fields ('is_eligible', 'eligibility_status')",
                raw_payload=data
            )

        metadata = dict(data.get("provenance_metadata", {}))
        metadata["latency_ms"] = res.latency_ms

        return EligibilityResponse(
            is_eligible=bool(data.get("is_eligible", False)),
            member_id=str(data.get("member_id", request.member_id)),
            payer_id=str(data.get("payer_id", request.payer_id)),
            eligibility_status=str(data.get("eligibility_status", "UNKNOWN")),
            coverage_start=data.get("coverage_start"),
            coverage_end=data.get("coverage_end"),
            plan_id=data.get("plan_id"),
            line_of_business=data.get("line_of_business"),
            ineligibility_reason=data.get("ineligibility_reason"),
            verification_reference=data.get("verification_reference"),
            provenance_metadata=metadata
        )
