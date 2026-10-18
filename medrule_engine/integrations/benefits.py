"""MedRule Benefit Configuration and Limitation Module.

Defines the contract and models for retrieving verified benefit limitations,
annual accumulator counts, place of service restrictions, and tiering protocols.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from medrule_engine.integrations.base import (
    BaseConnector,
    ConnectorCategory,
    ConnectorMode,
    SecurityContext,
)


@dataclass(frozen=True)
class BenefitRequest:
    """Strongly typed input model for benefit coverage query."""
    member_id: str
    plan_id: str
    procedure_code: str
    clinical_domain: str
    date_of_service: str
    payer_id: Optional[str] = None
    line_of_business: Optional[str] = None
    place_of_service: Optional[str] = None


@dataclass(frozen=True)
class BenefitResponse:
    """Strongly typed response model for benefit parameters and accumulators."""
    is_covered_benefit: bool
    benefit_status: str  # COVERED_BENEFIT, NON_COVERED_EXCLUSION, BENEFIT_MAXIMUM_EXHAUSTED, TIERING_STEP_THERAPY_REQUIRED, BENEFIT_CONFIG_UNAVAILABLE
    preauth_mandatory: bool
    annual_visit_cap: Optional[int] = None
    visits_used_to_date: Optional[int] = None
    remaining_visits: Optional[int] = None
    place_of_service_allowed: bool = True
    step_therapy_protocol_id: Optional[str] = None
    non_coverage_reason: Optional[str] = None
    benefit_notes: str = ""
    provenance_metadata: Dict[str, Any] = field(default_factory=dict)


class BenefitConnector(BaseConnector):
    """Abstract interface for health plan benefit configuration and accumulator adapters."""

    def __init__(
        self,
        name: str = "HealthPlanBenefitConnector",
        mode: ConnectorMode = ConnectorMode.DISABLED,
        timeout_ms: float = 3000.0,
        max_retries: int = 2
    ):
        super().__init__(
            name=name,
            category=ConnectorCategory.BENEFITS,
            mode=mode,
            timeout_ms=timeout_ms,
            max_retries=max_retries,
            required_scope="connectors:benefits:read"
        )

    def _validate_request(self, payload: Dict[str, Any]) -> None:
        """Enforce presence of mandatory benefit inquiry fields."""
        if not payload.get("member_id"):
            raise ValueError("Benefit inquiry requires non-empty 'member_id'.")
        if not payload.get("plan_id"):
            raise ValueError("Benefit inquiry requires non-empty 'plan_id'.")
        if not payload.get("procedure_code"):
            raise ValueError("Benefit inquiry requires non-empty 'procedure_code'.")
        if not payload.get("clinical_domain"):
            raise ValueError("Benefit inquiry requires non-empty 'clinical_domain'.")

    def check_benefits(
        self,
        request: BenefitRequest,
        security_context: Optional[SecurityContext] = None
    ) -> BenefitResponse:
        """Execute benefit coverage and limitation inquiry and return structured BenefitResponse."""
        sec_ctx = security_context or SecurityContext(
            caller_id="INTAKE_ORCHESTRATOR",
            role="INTAKE_COORDINATOR",
            scopes={"connectors:benefits:read"},
            is_authenticated=True
        )
        payload = {
            "member_id": request.member_id,
            "plan_id": request.plan_id,
            "procedure_code": request.procedure_code,
            "clinical_domain": request.clinical_domain,
            "date_of_service": request.date_of_service,
            "payer_id": request.payer_id,
            "line_of_business": request.line_of_business,
            "place_of_service": request.place_of_service
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
                from medrule_engine.integrations.base import InvalidConnectorResponseError
                raise InvalidConnectorResponseError(
                    res.error_message or f"Benefit check failed with code {res.status_code}",
                    raw_payload=res.data
                )

        data = res.data or {}
        if "is_covered_benefit" not in data or "benefit_status" not in data:
            from medrule_engine.integrations.base import InvalidConnectorResponseError
            raise InvalidConnectorResponseError(
                "Benefit response missing mandatory outcome fields ('is_covered_benefit', 'benefit_status')",
                raw_payload=data
            )

        metadata = dict(data.get("provenance_metadata", {}))
        metadata["latency_ms"] = res.latency_ms

        return BenefitResponse(
            is_covered_benefit=bool(data.get("is_covered_benefit", False)),
            benefit_status=str(data.get("benefit_status", "UNKNOWN")),
            preauth_mandatory=bool(data.get("preauth_mandatory", True)),
            annual_visit_cap=data.get("annual_visit_cap"),
            visits_used_to_date=data.get("visits_used_to_date"),
            remaining_visits=data.get("remaining_visits"),
            place_of_service_allowed=bool(data.get("place_of_service_allowed", True)),
            step_therapy_protocol_id=data.get("step_therapy_protocol_id"),
            non_coverage_reason=data.get("non_coverage_reason"),
            benefit_notes=str(data.get("benefit_notes", "")),
            provenance_metadata=metadata
        )

