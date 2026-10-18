"""MedRule Prior Authorization Submission Integration Adapter (Disabled Stub).

Designed for future production authorization submission, but strictly DISABLED
during Phase 3E. Prevents accidental or automated outbound transmission of
binding authorization requests.
"""

from typing import Any, Dict, List, Optional, Tuple

from medrule_engine.integrations.base import (
    BaseConnector,
    ConnectorCategory,
    ConnectorDisabledError,
    ConnectorMode,
    ConnectorResult,
    SecurityContext,
)


class SubmissionDisabledError(ConnectorDisabledError):
    """Explicit exception indicating authorization submission is prohibited in this phase."""
    def __init__(self):
        super().__init__("AuthorizationSubmissionAdapter")


class AuthorizationSubmissionAdapter(BaseConnector):
    """Stub adapter for outbound authorization requests, strictly disabled in Phase 3E."""

    def __init__(
        self,
        name: str = "PayerAuthorizationSubmissionAdapter",
        mode: ConnectorMode = ConnectorMode.DISABLED
    ):
        # Mode is unconditionally forced to DISABLED in Phase 3E
        super().__init__(
            name=name,
            category=ConnectorCategory.SUBMISSION,
            mode=ConnectorMode.DISABLED,
            required_scope="connectors:submission:execute"
        )

    def set_mode(self, new_mode: ConnectorMode, security_context: SecurityContext) -> None:
        """Reject any attempt to activate submission mode in Phase 3E."""
        raise SubmissionDisabledError()

    def _validate_request(self, payload: Dict[str, Any]) -> None:
        pass

    def _do_execute(
        self,
        payload: Dict[str, Any],
        security_context: SecurityContext
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        raise SubmissionDisabledError()

    def submit_authorization(
        self,
        case_id: str,
        evaluation_result: Dict[str, Any],
        security_context: SecurityContext
    ) -> ConnectorResult:
        """Always returns non-binding disabled outcome."""
        return ConnectorResult(
            is_success=False,
            status_code="SUBMISSION_DISABLED",
            error_code="SUBMISSION_DISABLED_IN_PHASE_3E",
            error_message="Phase 3E strictly prohibits outbound authorization submissions. System operates in non-binding support mode.",
            execution_mode=ConnectorMode.DISABLED,
            provenance_metadata={
                "is_binding": False,
                "phase": "Phase 3E",
                "policy": "Safe local integration architecture testing only"
            }
        )

    def submit_prior_authorization(self, *args, **kwargs) -> Any:
        """Explicitly block any attempt to submit prior authorizations."""
        raise SubmissionDisabledError()

    def is_disabled(self) -> bool:
        """Verify that the adapter is strictly disabled."""
        return self.mode == ConnectorMode.DISABLED
