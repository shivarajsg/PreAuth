"""MedRule Integration and Payer Connectivity Module.

Provides modular, secure connector abstractions and orchestration for member eligibility,
health plan benefits, prior-authorization requirements discovery, clinical data minimization,
and case lifecycle governance.
"""

from medrule_engine.integrations.base import (
    AuthenticationError,
    BaseConnector,
    ConnectorCategory,
    ConnectorDisabledError,
    ConnectorMode,
    ConnectorResult,
    IntegrationError,
    InvalidConnectorResponseError,
    SecurityContext,
    ServiceUnavailableError,
    TimeoutExhaustedError,
    UnauthorizedActivationError,
)
from medrule_engine.integrations.eligibility import (
    EligibilityConnector,
    EligibilityRequest,
    EligibilityResponse,
)
from medrule_engine.integrations.benefits import (
    BenefitConnector,
    BenefitRequest,
    BenefitResponse,
)
from medrule_engine.integrations.authorization_requirements import (
    AuthorizationRequirementsConnector,
    AuthRequirementRequest,
    AuthRequirementResponse,
)
from medrule_engine.integrations.clinical_data import ClinicalDataIntakeAdapter
from medrule_engine.integrations.submission import (
    AuthorizationSubmissionAdapter,
    SubmissionDisabledError,
)
from medrule_engine.integrations.payer_config import (
    PayerPlanConfig,
    PayerPlanConfigManager,
)
from medrule_engine.integrations.intake_service import (
    CaseIntakeOrchestrator,
    CaseLifecycleManager,
    IllegalLifecycleTransitionError,
    LifecycleState,
    PriorAuthIntakeOrchestrator,
)
from medrule_engine.integrations.mock_connectors import (
    MockAuthorizationRequirementsConnector,
    MockBenefitConnector,
    MockClinicalDataAdapter,
    MockEligibilityConnector,
    MockSubmissionAdapter,
)

__all__ = [
    # Base and Security
    "BaseConnector",
    "ConnectorCategory",
    "ConnectorMode",
    "ConnectorResult",
    "IntegrationError",
    "ConnectorDisabledError",
    "AuthenticationError",
    "ServiceUnavailableError",
    "TimeoutExhaustedError",
    "InvalidConnectorResponseError",
    "UnauthorizedActivationError",
    "SecurityContext",
    # Connectors
    "EligibilityConnector",
    "EligibilityRequest",
    "EligibilityResponse",
    "BenefitConnector",
    "BenefitRequest",
    "BenefitResponse",
    "AuthorizationRequirementsConnector",
    "AuthRequirementRequest",
    "AuthRequirementResponse",
    "ClinicalDataIntakeAdapter",
    "AuthorizationSubmissionAdapter",
    "SubmissionDisabledError",
    # Payer Configuration
    "PayerPlanConfig",
    "PayerPlanConfigManager",
    # Lifecycle and Orchestration
    "LifecycleState",
    "CaseLifecycleManager",
    "IllegalLifecycleTransitionError",
    "PriorAuthIntakeOrchestrator",
    "CaseIntakeOrchestrator",
    # Mock implementations
    "MockEligibilityConnector",
    "MockBenefitConnector",
    "MockAuthorizationRequirementsConnector",
    "MockClinicalDataAdapter",
    "MockSubmissionAdapter",
]
