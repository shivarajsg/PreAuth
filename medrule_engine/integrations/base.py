"""MedRule Integrations Base Module.

Provides abstract connector interfaces, execution modes, security contexts,
strongly typed result structures, and standardized error hierarchies.
All external integrations are strictly disabled by default.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
import time
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class ConnectorMode(str, Enum):
    """Execution modes for integration connectors."""
    DISABLED = "DISABLED"
    MOCK = "MOCK"
    LIVE_AUTHORIZED = "LIVE_AUTHORIZED"


class ConnectorCategory(str, Enum):
    """Categories of prior authorization integration connectors."""
    ELIGIBILITY = "ELIGIBILITY"
    BENEFITS = "BENEFITS"
    AUTHORIZATION_REQUIREMENTS = "AUTHORIZATION_REQUIREMENTS"
    CLINICAL_DATA = "CLINICAL_DATA"
    SUBMISSION = "SUBMISSION"


# ==============================================================================
# Standardized Integration Exceptions
# ==============================================================================

class IntegrationError(Exception):
    """Base exception for all integration failures."""
    def __init__(self, message: str, error_code: str = "INTEGRATION_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}


class ConnectorDisabledError(IntegrationError):
    """Raised when an execution is attempted on a disabled connector."""
    def __init__(self, connector_name: str):
        super().__init__(
            f"Connector '{connector_name}' is DISABLED. External connectivity must be explicitly authorized.",
            error_code="CONNECTOR_DISABLED"
        )


class AuthenticationError(IntegrationError):
    """Raised on security token, credential, or scope authorization failure."""
    def __init__(self, message: str = "Connector authentication failed"):
        super().__init__(message, error_code="AUTHENTICATION_FAILED")


class TimeoutExhaustedError(IntegrationError):
    """Raised when connector timeouts and all configured retry attempts are exhausted."""
    def __init__(self, connector_name: str, retries: int, timeout_ms: float):
        super().__init__(
            f"Connector '{connector_name}' timed out after {retries} retries ({timeout_ms}ms timeout).",
            error_code="TIMEOUT_EXHAUSTED"
        )


class InvalidConnectorResponseError(IntegrationError):
    """Raised when a connector returns a malformed or non-conforming payload."""
    def __init__(self, message: str, raw_payload: Optional[Any] = None):
        super().__init__(message, error_code="MALFORMED_RESPONSE", details={"raw": str(raw_payload)})


class ServiceUnavailableError(IntegrationError):
    """Raised when an external payer service endpoint reports 503 or network failure."""
    def __init__(self, service_name: str):
        super().__init__(f"Payer service '{service_name}' is currently unavailable.", error_code="SERVICE_UNAVAILABLE")


class UnauthorizedActivationError(IntegrationError):
    """Raised when an unauthorized actor attempts to activate a connector."""
    def __init__(self, actor_id: str, action: str):
        super().__init__(
            f"Actor '{actor_id}' is not authorized to perform '{action}'. Administrative approval required.",
            error_code="UNAUTHORIZED_ACTIVATION"
        )


# ==============================================================================
# Security & Result Contexts
# ==============================================================================

@dataclass(frozen=True)
class SecurityContext:
    """Security credentials and authorization boundaries for connector execution."""
    caller_id: str
    role: str
    scopes: Set[str] = field(default_factory=set)
    is_authenticated: bool = False
    is_admin: bool = False
    environment: str = "LOCAL_DEVELOPMENT"
    client_certificate_thumbprint: Optional[str] = None
    token_fingerprint: Optional[str] = None

    def has_scope(self, required_scope: str) -> bool:
        """Verify whether caller holds specific authorization scope."""
        return self.is_admin or (required_scope in self.scopes)


@dataclass
class ConnectorResult:
    """Standardized outcome envelope for any connector execution."""
    is_success: bool
    status_code: str
    data: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    execution_mode: ConnectorMode = ConnectorMode.DISABLED
    latency_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    provenance_metadata: Dict[str, Any] = field(default_factory=dict)
    audit_hash: str = ""

    def __post_init__(self):
        if not self.audit_hash:
            canonical = json.dumps({
                "is_success": self.is_success,
                "status_code": self.status_code,
                "data": self.data,
                "error_code": self.error_code,
                "execution_mode": self.execution_mode.value,
                "timestamp": self.timestamp
            }, sort_keys=True, default=str)
            self.audit_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ==============================================================================
# Abstract Base Connector
# ==============================================================================

class BaseConnector(ABC):
    """Abstract base class for all MedRule integration connectors."""

    def __init__(
        self,
        name: str,
        category: ConnectorCategory,
        mode: ConnectorMode = ConnectorMode.DISABLED,
        timeout_ms: float = 3000.0,
        max_retries: int = 2,
        required_scope: Optional[str] = None
    ):
        self.name = name
        self.category = category
        self.mode = mode
        self.timeout_ms = timeout_ms
        self.max_retries = max_retries
        self.required_scope = required_scope or f"connectors:{category.value.lower()}:read"

    def set_mode(self, new_mode: ConnectorMode, security_context: SecurityContext) -> None:
        """Change connector execution mode with strict administrative access control."""
        if not security_context.is_admin and not security_context.has_scope("connectors:admin:configure"):
            raise UnauthorizedActivationError(security_context.caller_id, f"set_mode({new_mode.value})")
        if new_mode == ConnectorMode.LIVE_AUTHORIZED:
            raise UnauthorizedActivationError(
                security_context.caller_id,
                "Phase 3E forbids activation of LIVE_AUTHORIZED mode. Local MOCK mode only."
            )
        self.mode = new_mode
        logger.info("Connector '%s' execution mode updated to %s by %s", self.name, new_mode.value, security_context.caller_id)

    def execute(self, request_payload: Dict[str, Any], security_context: SecurityContext) -> ConnectorResult:
        """Template execution method enforcing security checks, mode guards, and metrics."""
        start_time = time.perf_counter()

        # 1. Mode guard: disabled by default
        if self.mode == ConnectorMode.DISABLED:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ConnectorResult(
                is_success=False,
                status_code="CONNECTOR_DISABLED",
                error_code="CONNECTOR_DISABLED",
                error_message=f"Connector '{self.name}' is DISABLED.",
                execution_mode=self.mode,
                latency_ms=round(elapsed_ms, 2),
                provenance_metadata={"connector": self.name, "category": self.category.value}
            )

        # 2. Authentication and scope validation
        if not security_context.is_authenticated:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ConnectorResult(
                is_success=False,
                status_code="UNAUTHENTICATED",
                error_code="AUTHENTICATION_FAILED",
                error_message=f"Caller '{security_context.caller_id}' is not authenticated.",
                execution_mode=self.mode,
                latency_ms=round(elapsed_ms, 2)
            )

        if not security_context.has_scope(self.required_scope):
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ConnectorResult(
                is_success=False,
                status_code="FORBIDDEN_SCOPE",
                error_code="FORBIDDEN",
                error_message=f"Caller lacks required scope '{self.required_scope}'.",
                execution_mode=self.mode,
                latency_ms=round(elapsed_ms, 2)
            )

        # 3. Input payload validation
        try:
            self._validate_request(request_payload)
        except Exception as ve:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ConnectorResult(
                is_success=False,
                status_code="INVALID_REQUEST",
                error_code="VALIDATION_FAILED",
                error_message=f"Request payload validation error: {str(ve)}",
                execution_mode=self.mode,
                latency_ms=round(elapsed_ms, 2)
            )

        # 4. Delegate to subclass execution with retry logic
        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                res_data, status_code, provenance = self._do_execute(request_payload, security_context)
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                return ConnectorResult(
                    is_success=True,
                    status_code=status_code,
                    data=res_data,
                    execution_mode=self.mode,
                    latency_ms=round(elapsed_ms, 2),
                    provenance_metadata=provenance
                )
            except ServiceUnavailableError as sue:
                last_error = sue
                logger.warning("Attempt %d failed on connector '%s': %s", attempt + 1, self.name, str(sue))
            except TimeoutExhaustedError as te:
                last_error = te
                break
            except Exception as ex:
                last_error = ex
                break

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        err_msg = str(last_error) if last_error else "Unknown execution error"
        err_code = getattr(last_error, "error_code", "EXECUTION_FAILED")
        return ConnectorResult(
            is_success=False,
            status_code="FAILED",
            error_code=err_code,
            error_message=err_msg,
            execution_mode=self.mode,
            latency_ms=round(elapsed_ms, 2),
            provenance_metadata={"connector": self.name, "category": self.category.value, "retries_attempted": self.max_retries}
        )

    @abstractmethod
    def _validate_request(self, payload: Dict[str, Any]) -> None:
        """Validate input payload against connector schema."""
        pass

    @abstractmethod
    def _do_execute(
        self,
        payload: Dict[str, Any],
        security_context: SecurityContext
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        """Subclass execution implementation. Returns (response_data, status_code, provenance_metadata)."""
        pass
