"""MedRule Prior Authorization Requirements Discovery Module.

Defines the contract and models for discovering whether prior authorization
is mandatory for a specific service and retrieving required documentation checklists.
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
class AuthRequirementRequest:
    """Strongly typed input model for prior auth requirement discovery."""
    payer_id: str
    procedure_code: str
    clinical_domain: str
    plan_id: Optional[str] = None
    line_of_business: Optional[str] = None
    primary_diagnosis_code: Optional[str] = None
    place_of_service: Optional[str] = None


@dataclass(frozen=True)
class AuthRequirementResponse:
    """Strongly typed response model for prior auth requirements."""
    auth_required: bool
    requirement_status: str  # PRIOR_AUTH_MANDATORY, PRIOR_NOTIFICATION_ONLY, NO_AUTH_REQUIRED, STATUTORY_EXEMPTION_APPLIES, REQUIREMENT_UNRESOLVED
    documentation_checklist: List[str] = field(default_factory=list)
    standard_turnaround_calendar_days: int = 14
    urgent_turnaround_hours: int = 72
    submission_portal_id: Optional[str] = None
    regulatory_reference: Optional[str] = None
    provenance_metadata: Dict[str, Any] = field(default_factory=dict)


class AuthorizationRequirementsConnector(BaseConnector):
    """Abstract interface for prior authorization requirement discovery adapters."""

    def __init__(
        self,
        name: str = "PriorAuthRequirementsConnector",
        mode: ConnectorMode = ConnectorMode.DISABLED,
        timeout_ms: float = 3000.0,
        max_retries: int = 2
    ):
        super().__init__(
            name=name,
            category=ConnectorCategory.AUTHORIZATION_REQUIREMENTS,
            mode=mode,
            timeout_ms=timeout_ms,
            max_retries=max_retries,
            required_scope="connectors:auth_requirements:read"
        )

    def _validate_request(self, payload: Dict[str, Any]) -> None:
        """Enforce presence of mandatory requirement inquiry fields."""
        if not payload.get("payer_id"):
            raise ValueError("Auth requirement discovery requires non-empty 'payer_id'.")
        if not payload.get("procedure_code"):
            raise ValueError("Auth requirement discovery requires non-empty 'procedure_code'.")
        if not payload.get("clinical_domain"):
            raise ValueError("Auth requirement discovery requires non-empty 'clinical_domain'.")

    def check_requirements(
        self,
        request: AuthRequirementRequest,
        security_context: Optional[SecurityContext] = None
    ) -> AuthRequirementResponse:
        """Execute prior auth requirement discovery inquiry and return structured AuthRequirementResponse."""
        sec_ctx = security_context or SecurityContext(
            caller_id="INTAKE_ORCHESTRATOR",
            role="INTAKE_COORDINATOR",
            scopes={"connectors:auth_requirements:read"},
            is_authenticated=True
        )
        payload = {
            "payer_id": request.payer_id,
            "procedure_code": request.procedure_code,
            "clinical_domain": request.clinical_domain,
            "plan_id": request.plan_id,
            "line_of_business": request.line_of_business,
            "primary_diagnosis_code": request.primary_diagnosis_code,
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
                    res.error_message or f"Auth requirements check failed with code {res.status_code}",
                    raw_payload=res.data
                )

        data = res.data or {}
        if "auth_required" not in data or "requirement_status" not in data:
            from medrule_engine.integrations.base import InvalidConnectorResponseError
            raise InvalidConnectorResponseError(
                "Auth requirements response missing mandatory outcome fields ('auth_required', 'requirement_status')",
                raw_payload=data
            )

        metadata = dict(data.get("provenance_metadata", {}))
        metadata["latency_ms"] = res.latency_ms

        return AuthRequirementResponse(
            auth_required=bool(data.get("auth_required", True)),
            requirement_status=str(data.get("requirement_status", "PRIOR_AUTH_MANDATORY")),
            documentation_checklist=list(data.get("documentation_checklist", [])),
            standard_turnaround_calendar_days=int(data.get("standard_turnaround_calendar_days", 14)),
            urgent_turnaround_hours=int(data.get("urgent_turnaround_hours", 72)),
            submission_portal_id=data.get("submission_portal_id"),
            regulatory_reference=data.get("regulatory_reference"),
            provenance_metadata=metadata
        )

