"""MedRule Deterministic Mock Connectors Module.

Implements high-fidelity local mock adapters for Member Eligibility,
Health Plan Benefit Limitations, Prior Auth Requirements Discovery,
Clinical Data Normalization, and strictly disabled Submission.

All responses are explicitly marked as MOCK/SYNTHETIC and involve ZERO
external network transmission.
"""

from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from medrule_engine.integrations.authorization_requirements import (
    AuthRequirementRequest,
    AuthRequirementResponse,
    AuthorizationRequirementsConnector,
)
from medrule_engine.integrations.base import (
    ConnectorCategory,
    ConnectorMode,
    InvalidConnectorResponseError,
    SecurityContext,
    ServiceUnavailableError,
    TimeoutExhaustedError,
)
from medrule_engine.integrations.benefits import (
    BenefitConnector,
    BenefitRequest,
    BenefitResponse,
)
from medrule_engine.integrations.clinical_data import ClinicalDataIntakeAdapter
from medrule_engine.integrations.eligibility import (
    EligibilityConnector,
    EligibilityRequest,
    EligibilityResponse,
)
from medrule_engine.integrations.submission import (
    AuthorizationSubmissionAdapter,
    SubmissionDisabledError,
)

logger = logging.getLogger(__name__)

FIXTURES_FILE = Path(__file__).resolve().parent / "fixtures" / "synthetic_connector_fixtures.json"


def _load_fixtures() -> Dict[str, Any]:
    """Load mock response fixtures safely."""
    if not FIXTURES_FILE.exists():
        return {}
    with open(FIXTURES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ==============================================================================
# 1. Mock Eligibility Connector
# ==============================================================================

class MockEligibilityConnector(EligibilityConnector):
    """Deterministic local mock connector for member eligibility verification."""

    def __init__(
        self,
        name: str = "MockEligibilityConnector",
        mode: ConnectorMode = ConnectorMode.MOCK,
        fixtures_override: Optional[Dict[str, Any]] = None
    ):
        super().__init__(name=name, mode=mode)
        self.fixtures = fixtures_override or _load_fixtures().get("eligibility_fixtures", {})

    def _do_execute(
        self,
        payload: Dict[str, Any],
        security_context: SecurityContext
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        member_id = payload["member_id"]
        dos_str = payload["date_of_service"]

        fixture = self.fixtures.get(member_id)

        # Simulation triggers
        if fixture and fixture.get("simulate_outage"):
            raise ServiceUnavailableError("SimulatedPayerEligibilityGateway")
        if fixture and fixture.get("simulate_timeout"):
            raise TimeoutExhaustedError(self.name, self.max_retries, self.timeout_ms)
        if fixture and fixture.get("simulate_malformed"):
            return {"malformed_garbage": True}, "UNKNOWN_FORMAT", {}

        provenance = {
            "source": "MedRule_Deterministic_Mock_Eligibility_Service",
            "execution_mode": "MOCK",
            "fixture_matched": bool(fixture),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "synthetic_disclaimer": "SYNTHETIC TEST RECORD — NOT A REAL PAYER ELIGIBILITY RESPONSE"
        }

        # Known fixture match
        if fixture:
            # Check coverage dates
            c_start = fixture.get("coverage_start")
            c_end = fixture.get("coverage_end")
            status = fixture.get("eligibility_status", "ACTIVE_COVERAGE")
            is_eligible = fixture.get("is_eligible", False)

            if is_eligible and c_start and c_end:
                if dos_str < c_start or dos_str > c_end:
                    is_eligible = False
                    status = "DATE_OUTSIDE_COVERAGE_PERIOD"

            response_data = {
                "is_eligible": is_eligible,
                "member_id": member_id,
                "payer_id": fixture.get("payer_id", payload.get("payer_id", "EVOLENT")),
                "plan_id": fixture.get("plan_id", payload.get("plan_id")),
                "line_of_business": fixture.get("line_of_business", payload.get("line_of_business", "COMMERCIAL")),
                "eligibility_status": status,
                "coverage_start": c_start,
                "coverage_end": c_end,
                "ineligibility_reason": fixture.get("ineligibility_reason"),
                "verification_reference": fixture.get("verification_reference", f"MOCK-VERIF-{member_id[:8]}"),
                "provenance_metadata": provenance
            }
            return response_data, status, provenance

        # Dynamic default behavior for unlisted patient/member records:
        # Unless explicitly indicated as ineligible or terminated, treat patient as having active coverage
        # so clinical guidelines and medical necessity can be evaluated smoothly without synthetic blockers.
        is_negative_case = any(tag in member_id.upper() for tag in ["INELIGIBLE", "INVALID", "TERMINATED"])
        if not is_negative_case:
            response_data = {
                "is_eligible": True,
                "member_id": member_id,
                "payer_id": payload.get("payer_id", "EVOLENT"),
                "plan_id": payload.get("plan_id", "COMMERCIAL_CHOICE_PLUS"),
                "line_of_business": payload.get("line_of_business", "COMMERCIAL"),
                "eligibility_status": "ACTIVE_COVERAGE",
                "coverage_start": "2026-01-01",
                "coverage_end": "2026-12-31",
                "verification_reference": f"VERIF-{member_id[:12].replace('-', '')}",
                "provenance_metadata": provenance
            }
            return response_data, "ACTIVE_COVERAGE", provenance

        # Explicitly unverified or invalid member
        response_data = {
            "is_eligible": False,
            "member_id": member_id,
            "payer_id": payload.get("payer_id", "UNKNOWN"),
            "eligibility_status": "INELIGIBLE_MEMBER_NOT_FOUND",
            "coverage_start": None,
            "coverage_end": None,
            "ineligibility_reason": f"Patient / Member ID '{member_id}' not found in active plan enrollment roster.",
            "provenance_metadata": provenance
        }
        return response_data, "INELIGIBLE_MEMBER_NOT_FOUND", provenance


# ==============================================================================
# 2. Mock Benefit Connector
# ==============================================================================

class MockBenefitConnector(BenefitConnector):
    """Deterministic local mock connector for plan benefits, limitations, and visit accumulators."""

    def __init__(
        self,
        name: str = "MockBenefitConnector",
        mode: ConnectorMode = ConnectorMode.MOCK,
        fixtures_override: Optional[Dict[str, Any]] = None
    ):
        super().__init__(name=name, mode=mode)
        self.fixtures = fixtures_override or _load_fixtures().get("benefit_fixtures", {})

    def _do_execute(
        self,
        payload: Dict[str, Any],
        security_context: SecurityContext
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        plan_id = payload["plan_id"]
        proc_code = payload["procedure_code"]
        dom = payload["clinical_domain"]

        # Check exact fixture keys
        match_key = None
        for k in (f"{plan_id}:{proc_code}:CAPPED", f"{plan_id}:{proc_code}", f"{plan_id}:{proc_code}:AVAILABLE"):
            if k in self.fixtures:
                match_key = k
                break

        # Check special case for therapy caps (case 24 in pilot, DEP-013)
        if proc_code == "97110" and payload.get("visits_used_to_date", 0) >= 30:
            match_key = "COMMERCIAL_CHOICE_PLUS:97110:CAPPED"

        provenance = {
            "source": "MedRule_Deterministic_Mock_Benefit_Service",
            "execution_mode": "MOCK",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "synthetic_disclaimer": "SYNTHETIC TEST RECORD — NOT REAL PAYER BENEFIT SCHEDULE"
        }

        if match_key and match_key in self.fixtures:
            f = self.fixtures[match_key]
            res = dict(f)
            res["provenance_metadata"] = provenance
            return res, f.get("benefit_status", "COVERED_BENEFIT"), provenance

        # Dynamic fallback: Standard covered benefit subject to medical necessity
        res = {
            "is_covered_benefit": True,
            "benefit_status": "COVERED_BENEFIT",
            "preauth_mandatory": True,
            "annual_visit_cap": None,
            "visits_used_to_date": None,
            "remaining_visits": None,
            "place_of_service_allowed": True,
            "benefit_notes": f"Standard coverage applies for procedure {proc_code} under {plan_id}.",
            "provenance_metadata": provenance
        }
        return res, "COVERED_BENEFIT", provenance


# ==============================================================================
# 3. Mock Prior Authorization Requirements Connector
# ==============================================================================

class MockAuthorizationRequirementsConnector(AuthorizationRequirementsConnector):
    """Deterministic local mock connector for PA requirement discovery."""

    def __init__(
        self,
        name: str = "MockPriorAuthRequirementsConnector",
        mode: ConnectorMode = ConnectorMode.MOCK,
        fixtures_override: Optional[Dict[str, Any]] = None
    ):
        super().__init__(name=name, mode=mode)
        self.fixtures = fixtures_override or _load_fixtures().get("auth_requirement_fixtures", {})

    def _do_execute(
        self,
        payload: Dict[str, Any],
        security_context: SecurityContext
    ) -> Tuple[Dict[str, Any], str, Dict[str, Any]]:
        payer = payload["payer_id"]
        proc = payload["procedure_code"]

        key = f"{payer}:{proc}"
        f = self.fixtures.get(key)

        provenance = {
            "source": "MedRule_Deterministic_Mock_Requirements_Service",
            "execution_mode": "MOCK",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "synthetic_disclaimer": "SYNTHETIC TEST RECORD — NOT A REAL PAYER AUTH REQUIREMENT"
        }

        if f:
            res = dict(f)
            res["provenance_metadata"] = provenance
            return res, f.get("requirement_status", "PRIOR_AUTH_MANDATORY"), provenance

        # Default for MedRule clinical scope procedures: PA mandatory with standard checklist
        res = {
            "auth_required": True,
            "requirement_status": "PRIOR_AUTH_MANDATORY",
            "documentation_checklist": [
                "CLINICAL_OFFICE_NOTES",
                "OBJECTIVE_DIAGNOSTIC_FINDINGS",
                "PHYSICIAN_ORDERS"
            ],
            "standard_turnaround_calendar_days": 14,
            "urgent_turnaround_hours": 72,
            "submission_portal_id": f"{payer}_SECURE_PORTAL",
            "regulatory_reference": "State Prior Authorization Standard Guidelines 2026",
            "provenance_metadata": provenance
        }
        return res, "PRIOR_AUTH_MANDATORY", provenance


# ==============================================================================
# 4. Mock Clinical Data Adapter & Mock Submission Adapter
# ==============================================================================

class MockClinicalDataAdapter(ClinicalDataIntakeAdapter):
    """Mock clinical data intake adapter operating in local MOCK mode."""
    def __init__(self, name: str = "MockClinicalDataAdapter"):
        super().__init__(name=name, mode=ConnectorMode.MOCK)


class MockSubmissionAdapter(AuthorizationSubmissionAdapter):
    """Mock submission adapter explicitly locked in DISABLED mode."""
    def __init__(self, name: str = "MockSubmissionAdapter"):
        super().__init__(name=name, mode=ConnectorMode.DISABLED)
