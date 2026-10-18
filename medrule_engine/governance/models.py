"""MedRule Governance Models and Role-Based Access Control Specifications.

Defines roles, review actions, workflow lifecycle states, permission matrices,
and approval prerequisites for the clinical SME review interface.
"""

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any, Dict, List, Optional, Set, Tuple


class ReviewRole(str, Enum):
    """User roles for clinical governance and review workflow."""
    VIEWER = "VIEWER"
    CLINICAL_SME_REVIEWER = "CLINICAL_SME_REVIEWER"
    MEDICAL_DIRECTOR = "MEDICAL_DIRECTOR"
    ADMINISTRATOR = "ADMINISTRATOR"


class WorkflowStatus(str, Enum):
    """Rule review lifecycle status.
    
    Distinct from extraction_status (DRAFT, NEEDS_HUMAN_REVIEW, APPROVED)
    and validation_status (VALID, INVALID).
    """
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    NEEDS_CORRECTION = "NEEDS_CORRECTION"
    READY_FOR_MEDICAL_DIRECTOR = "READY_FOR_MEDICAL_DIRECTOR"
    APPROVED = "APPROVED"
    FLAGGED_CONFLICT = "FLAGGED_CONFLICT"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ReviewAction(str, Enum):
    """Controlled review actions that authorized reviewers can perform."""
    START_REVIEW = "START_REVIEW"
    CONFIRM_INTERPRETATION = "CONFIRM_INTERPRETATION"
    REQUEST_CORRECTION = "REQUEST_CORRECTION"
    NEEDS_ADDITIONAL_EVIDENCE = "NEEDS_ADDITIONAL_EVIDENCE"
    ESCALATE_TO_MEDICAL_DIRECTOR = "ESCALATE_TO_MEDICAL_DIRECTOR"
    FLAG_POLICY_CONFLICT = "FLAG_POLICY_CONFLICT"
    MARK_NOT_APPLICABLE_WITH_RATIONALE = "MARK_NOT_APPLICABLE_WITH_RATIONALE"
    RETURN_TO_DRAFT = "RETURN_TO_DRAFT"
    APPROVE_RULE = "APPROVE_RULE"


class CorrectionStatus(str, Enum):
    """Status of a proposed rule correction."""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


# Role-Based Permission Matrix: maps role to allowed ReviewActions
ROLE_PERMISSIONS: Dict[ReviewRole, Set[ReviewAction]] = {
    ReviewRole.VIEWER: set(),  # Read-only
    ReviewRole.CLINICAL_SME_REVIEWER: {
        ReviewAction.START_REVIEW,
        ReviewAction.CONFIRM_INTERPRETATION,
        ReviewAction.REQUEST_CORRECTION,
        ReviewAction.NEEDS_ADDITIONAL_EVIDENCE,
        ReviewAction.ESCALATE_TO_MEDICAL_DIRECTOR,
        ReviewAction.FLAG_POLICY_CONFLICT,
        ReviewAction.MARK_NOT_APPLICABLE_WITH_RATIONALE,
        ReviewAction.RETURN_TO_DRAFT,
    },
    ReviewRole.MEDICAL_DIRECTOR: {
        ReviewAction.START_REVIEW,
        ReviewAction.CONFIRM_INTERPRETATION,
        ReviewAction.REQUEST_CORRECTION,
        ReviewAction.NEEDS_ADDITIONAL_EVIDENCE,
        ReviewAction.ESCALATE_TO_MEDICAL_DIRECTOR,
        ReviewAction.FLAG_POLICY_CONFLICT,
        ReviewAction.MARK_NOT_APPLICABLE_WITH_RATIONALE,
        ReviewAction.RETURN_TO_DRAFT,
        ReviewAction.APPROVE_RULE,  # Exclusive privilege
    },
    ReviewRole.ADMINISTRATOR: {
        ReviewAction.RETURN_TO_DRAFT,  # Can reset workflow if needed
    }
}


# Valid Lifecycle Transitions
# current_status -> {allowed_action: resulting_status}
LIFECYCLE_TRANSITIONS: Dict[WorkflowStatus, Dict[ReviewAction, WorkflowStatus]] = {
    WorkflowStatus.DRAFT: {
        ReviewAction.START_REVIEW: WorkflowStatus.IN_REVIEW,
        ReviewAction.FLAG_POLICY_CONFLICT: WorkflowStatus.FLAGGED_CONFLICT,
        ReviewAction.MARK_NOT_APPLICABLE_WITH_RATIONALE: WorkflowStatus.NOT_APPLICABLE,
    },
    WorkflowStatus.IN_REVIEW: {
        ReviewAction.CONFIRM_INTERPRETATION: WorkflowStatus.READY_FOR_MEDICAL_DIRECTOR,
        ReviewAction.REQUEST_CORRECTION: WorkflowStatus.NEEDS_CORRECTION,
        ReviewAction.NEEDS_ADDITIONAL_EVIDENCE: WorkflowStatus.IN_REVIEW,
        ReviewAction.ESCALATE_TO_MEDICAL_DIRECTOR: WorkflowStatus.READY_FOR_MEDICAL_DIRECTOR,
        ReviewAction.FLAG_POLICY_CONFLICT: WorkflowStatus.FLAGGED_CONFLICT,
        ReviewAction.MARK_NOT_APPLICABLE_WITH_RATIONALE: WorkflowStatus.NOT_APPLICABLE,
        ReviewAction.RETURN_TO_DRAFT: WorkflowStatus.DRAFT,
    },
    WorkflowStatus.NEEDS_CORRECTION: {
        ReviewAction.START_REVIEW: WorkflowStatus.IN_REVIEW,
        ReviewAction.RETURN_TO_DRAFT: WorkflowStatus.DRAFT,
        ReviewAction.FLAG_POLICY_CONFLICT: WorkflowStatus.FLAGGED_CONFLICT,
    },
    WorkflowStatus.READY_FOR_MEDICAL_DIRECTOR: {
        ReviewAction.APPROVE_RULE: WorkflowStatus.APPROVED,
        ReviewAction.REQUEST_CORRECTION: WorkflowStatus.NEEDS_CORRECTION,
        ReviewAction.RETURN_TO_DRAFT: WorkflowStatus.DRAFT,
        ReviewAction.FLAG_POLICY_CONFLICT: WorkflowStatus.FLAGGED_CONFLICT,
    },
    WorkflowStatus.FLAGGED_CONFLICT: {
        ReviewAction.START_REVIEW: WorkflowStatus.IN_REVIEW,
        ReviewAction.RETURN_TO_DRAFT: WorkflowStatus.DRAFT,
    },
    WorkflowStatus.NOT_APPLICABLE: {
        ReviewAction.RETURN_TO_DRAFT: WorkflowStatus.DRAFT,
    },
    WorkflowStatus.APPROVED: {
        # Approved rules cannot be altered through normal review; must be formally returned to draft
        ReviewAction.RETURN_TO_DRAFT: WorkflowStatus.DRAFT,
    }
}


@dataclass
class ReviewerIdentity:
    """Authenticated human reviewer context."""
    user_id: str
    username: str
    display_name: str
    role: ReviewRole
    credentials: str  # e.g. "MD, FACC" or "RN, BSN, SME"
    email: str = ""
    active: bool = True

    def can_perform(self, action: ReviewAction) -> bool:
        """Check if reviewer role has permission for action."""
        if not self.active:
            return False
        return action in ROLE_PERMISSIONS.get(self.role, set())


@dataclass
class ApprovalPrerequisiteCheck:
    """Rigorous evaluation of the 8 mandatory approval prerequisites."""
    rule_id: str
    prerequisites: Dict[str, bool] = field(default_factory=dict)
    blockers: List[str] = field(default_factory=list)

    @property
    def is_eligible(self) -> bool:
        """Rule is eligible for approval if and only if ALL prerequisites are satisfied."""
        return len(self.blockers) == 0 and all(self.prerequisites.values())


def evaluate_approval_prerequisites(
    rule_data: Dict[str, Any],
    reviewer: ReviewerIdentity,
    current_workflow_status: WorkflowStatus,
    review_history_count: int,
    unresolved_dependencies: List[str],
    schema_valid: bool
) -> ApprovalPrerequisiteCheck:
    """Verify all 8 mandatory prerequisites before a rule can be approved.
    
    Prerequisites:
    1. Source and active policy version verified.
    2. Structured conditions reviewed.
    3. Interpretation and exceptions resolved (workflow status is READY_FOR_MEDICAL_DIRECTOR).
    4. Required source dependencies addressed (no unresolved blockers).
    5. Automated structural and traceability validation passes.
    6. Required clinical review and sign-off recorded.
    7. Approver has required authority (MEDICAL_DIRECTOR).
    8. Final approval action explicitly confirmed (verified reviewer identity).
    """
    check = ApprovalPrerequisiteCheck(rule_id=rule_data.get("rule_id", "UNKNOWN"))

    # 1. Source and active policy version
    v_status = rule_data.get("version_status", "")
    p1 = v_status == "current_2026_verified"
    check.prerequisites["1_source_version_verified"] = p1
    if not p1:
        check.blockers.append(f"Policy version status '{v_status}' is not current_2026_verified")

    # 2. Structured conditions exist and non-empty
    conditions = rule_data.get("conditions", {})
    criteria = conditions.get("criteria", [])
    p2 = bool(criteria and len(criteria) > 0)
    check.prerequisites["2_structured_conditions_present"] = p2
    if not p2:
        check.blockers.append("No structured conditions found in rule record")

    # 3. Interpretation and exceptions resolved (must be in READY_FOR_MEDICAL_DIRECTOR)
    p3 = current_workflow_status == WorkflowStatus.READY_FOR_MEDICAL_DIRECTOR
    check.prerequisites["3_interpretation_resolved_ready_for_director"] = p3
    if not p3:
        check.blockers.append(f"Current workflow status '{current_workflow_status.value}' is not READY_FOR_MEDICAL_DIRECTOR")

    # 4. Required dependencies addressed
    p4 = len(unresolved_dependencies) == 0
    check.prerequisites["4_no_unresolved_dependencies"] = p4
    if not p4:
        check.blockers.append(f"Unresolved policy dependencies exist: {', '.join(unresolved_dependencies)}")

    # 5. Schema validation passes
    p5 = schema_valid
    check.prerequisites["5_schema_validation_passed"] = p5
    if not p5:
        check.blockers.append("Canonical Draft-07 schema validation failed")

    # 6. Prior clinical SME review recorded
    p6 = review_history_count > 0
    check.prerequisites["6_prior_clinical_sme_review_recorded"] = p6
    if not p6:
        check.blockers.append("No prior clinical SME review record found; SME review sign-off is required before approval")

    # 7. Approver has MEDICAL_DIRECTOR authority
    p7 = reviewer.role == ReviewRole.MEDICAL_DIRECTOR
    check.prerequisites["7_approver_is_medical_director"] = p7
    if not p7:
        check.blockers.append(f"Reviewer role '{reviewer.role.value}' does not have Medical Director approval authority")

    # 8. Authenticated human identity with credentials
    p8 = bool(reviewer.user_id and reviewer.credentials and reviewer.active)
    check.prerequisites["8_authenticated_clinical_credentials"] = p8
    if not p8:
        check.blockers.append("Approver must be an active user with verified clinical credentials")

    return check
