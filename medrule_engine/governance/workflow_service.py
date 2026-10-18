"""MedRule Governance Workflow Service.

Orchestrates the clinical review lifecycle, role authorization, approval prerequisite
evaluation, side-by-side proposed correction diffing, and audit logging.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import jsonschema

from medrule_engine.governance.database import GovernanceDatabase
from medrule_engine.governance.models import (
    ApprovalPrerequisiteCheck,
    CorrectionStatus,
    LIFECYCLE_TRANSITIONS,
    ROLE_PERMISSIONS,
    ReviewAction,
    ReviewerIdentity,
    ReviewRole,
    WorkflowStatus,
    evaluate_approval_prerequisites,
)
from medrule_engine.rule_registry import DEFAULT_SCHEMA_PATH, RuleRecord, RuleRegistry

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFESTS_DIR = REPO_ROOT / "rulebook_collection" / "manifests"
DOMAINS_DIR = REPO_ROOT / "rulebook_collection" / "domains"


class GovernanceWorkflowService:
    """Core service for managing the Clinical SME review interface and governance workflow."""

    def __init__(
        self,
        registry: Optional[RuleRegistry] = None,
        db: Optional[GovernanceDatabase] = None,
        schema_path: Optional[Path] = None
    ):
        self.registry = registry or RuleRegistry()
        if not self.registry._loaded:
            self.registry.load_all_domains()

        self.db = db or GovernanceDatabase()
        self.schema_path = schema_path or DEFAULT_SCHEMA_PATH

        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.rule_schema = json.load(f)
        self.schema_validator = jsonschema.Draft7Validator(self.rule_schema)

        # Sync registry rules into governance DB
        self.db.sync_rules_from_registry(self.registry.get_all_rules())

        # Load domain traceability & human review queue cache
        self._traceability_by_id: Dict[str, Dict[str, str]] = {}
        self._human_review_queue_by_id: Dict[str, Dict[str, str]] = {}
        self._load_domain_metadata_caches()

        # Load policy dependencies cache
        self._dependencies_by_domain: Dict[str, List[Dict[str, str]]] = {}
        self._load_dependency_cache()

    def _load_domain_metadata_caches(self) -> None:
        """Cache source_to_rule_traceability.csv and human_review_queue.csv for fast lookup."""
        for dom_dir in DOMAINS_DIR.iterdir():
            if not dom_dir.is_dir():
                continue
            
            trace_file = dom_dir / "rules" / "source_to_rule_traceability.csv"
            if trace_file.exists():
                try:
                    with open(trace_file, "r", encoding="utf-8", errors="replace") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            r_id = row.get("rule_id")
                            if r_id:
                                self._traceability_by_id[r_id] = dict(row)
                except Exception as e:
                    logger.warning(f"Error reading traceability for {dom_dir.name}: {e}")

            queue_file = dom_dir / "rules" / "human_review_queue.csv"
            if queue_file.exists():
                try:
                    with open(queue_file, "r", encoding="utf-8", errors="replace") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            r_id = row.get("rule_id")
                            if r_id:
                                self._human_review_queue_by_id[r_id] = dict(row)
                except Exception as e:
                    logger.warning(f"Error reading review queue for {dom_dir.name}: {e}")

    def _load_dependency_cache(self) -> None:
        """Cache cross-domain and plan dependencies."""
        dep_file = MANIFESTS_DIR / "policy_dependency_mapping.csv"
        if dep_file.exists():
            try:
                with open(dep_file, "r", encoding="utf-8", errors="replace") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        dom = row.get("primary_domain", "")
                        if dom not in self._dependencies_by_domain:
                            self._dependencies_by_domain[dom] = []
                        self._dependencies_by_domain[dom].append(dict(row))
            except Exception as e:
                logger.warning(f"Error reading policy dependency mapping: {e}")

    def get_enriched_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """Fetch complete rule record enriched with source provenance, review state, and dependencies."""
        rule_record = self.registry.get_rule(rule_id)
        if not rule_record:
            return None

        gov_state = self.db.get_rule_governance_state(rule_id) or {}
        traceability = self._traceability_by_id.get(rule_id, {})
        queue_entry = self._human_review_queue_by_id.get(rule_id, {})
        history = self.db.get_review_history(rule_id)
        corrections = self.db.get_proposed_corrections(rule_id)
        domain_deps = self._dependencies_by_domain.get(rule_record.domain, [])

        unresolved_deps = [
            d["dependency_id"] for d in domain_deps 
            if d.get("status") in ("PLAN_SPECIFIC_ACCESS_REQUIRED", "UNRESOLVED")
        ]

        # Check approval prerequisites
        current_wf = WorkflowStatus(gov_state.get("workflow_status", WorkflowStatus.DRAFT.value))
        
        # Test schema validity
        schema_errors = list(self.schema_validator.iter_errors(rule_record.raw_data))
        schema_valid = len(schema_errors) == 0

        # Create dummy reviewer for prerequisite check preview
        dummy_reviewer = ReviewerIdentity(
            user_id="PREVIEW",
            username="preview",
            display_name="Preview",
            role=ReviewRole.MEDICAL_DIRECTOR,
            credentials="MD"
        )
        prereq_check = evaluate_approval_prerequisites(
            rule_data=rule_record.raw_data,
            reviewer=dummy_reviewer,
            current_workflow_status=current_wf,
            review_history_count=len(history),
            unresolved_dependencies=unresolved_deps,
            schema_valid=schema_valid
        )

        return {
            "rule_id": rule_record.rule_id,
            "domain": rule_record.domain,
            "document_type": rule_record.document_type,
            "policy_title": rule_record.policy_title,
            "policy_version": rule_record.policy_version,
            "version_status": rule_record.version_status,
            "source_file": rule_record.source_file,
            "physical_page": rule_record.physical_page,
            "source_section": rule_record.source_section,
            "source_quote": rule_record.source_quote,
            "clinical_service_or_procedure": rule_record.clinical_service_or_procedure,
            "rule_type": rule_record.rule_type,
            "conditions": rule_record.conditions,
            "decision_effect": rule_record.decision_effect,
            "missing_information_behavior": rule_record.missing_information_behavior,
            "human_review_required": rule_record.human_review_required,
            "extraction_status": rule_record.extraction_status,
            "review_notes": rule_record.review_notes,
            "raw_data": rule_record.raw_data,
            # Governance extensions
            "governance_state": gov_state,
            "workflow_status": current_wf.value,
            "is_approved": bool(gov_state.get("is_approved", 0)),
            "is_binding": False,  # Prototype rules are strictly non-binding
            "traceability": traceability,
            "queue_entry": queue_entry,
            "review_history": history,
            "proposed_corrections": corrections,
            "domain_dependencies": domain_deps,
            "unresolved_dependencies": unresolved_deps,
            "schema_valid": schema_valid,
            "schema_errors": [e.message for e in schema_errors[:3]],
            "approval_prerequisites": {
                "is_eligible": prereq_check.is_eligible,
                "prerequisites": prereq_check.prerequisites,
                "blockers": prereq_check.blockers
            }
        }

    def list_rules(
        self,
        domain: Optional[str] = None,
        workflow_status: Optional[str] = None,
        extraction_status: Optional[str] = None,
        rule_type: Optional[str] = None,
        search_query: Optional[str] = None,
        human_review_only: bool = False
    ) -> List[Dict[str, Any]]:
        """List rules with comprehensive filtering."""
        all_rules = self.registry.get_all_rules()
        gov_states = self.db.get_all_governance_states()

        results = []
        for r in all_rules:
            g_state = gov_states.get(r.rule_id, {})
            wf_status = g_state.get("workflow_status", WorkflowStatus.DRAFT.value)

            if domain and r.domain.lower() != domain.lower():
                continue
            if workflow_status and wf_status != workflow_status:
                continue
            if extraction_status and r.extraction_status != extraction_status:
                continue
            if rule_type and r.rule_type != rule_type:
                continue
            if human_review_only and not (r.human_review_required or r.extraction_status == "NEEDS_HUMAN_REVIEW"):
                continue

            if search_query:
                sq = search_query.lower()
                matches = (
                    sq in r.rule_id.lower() or
                    sq in r.clinical_service_or_procedure.lower() or
                    sq in r.source_section.lower() or
                    sq in r.policy_title.lower() or
                    sq in r.source_quote.lower()
                )
                if not matches:
                    continue

            results.append({
                "rule_id": r.rule_id,
                "domain": r.domain,
                "clinical_service_or_procedure": r.clinical_service_or_procedure,
                "rule_type": r.rule_type,
                "decision_effect": r.decision_effect,
                "policy_title": r.policy_title,
                "source_section": r.source_section,
                "physical_page": r.physical_page,
                "workflow_status": wf_status,
                "extraction_status": r.extraction_status,
                "human_review_required": r.human_review_required,
                "is_approved": bool(g_state.get("is_approved", 0)),
                "last_reviewed_at": g_state.get("last_reviewed_at"),
                "last_reviewed_by": g_state.get("last_reviewed_by")
            })

        return results

    def submit_review_action(
        self,
        rule_id: str,
        reviewer_id: str,
        action_name: str,
        comments: str,
        source_evidence_considered: str = "",
        change_details: Optional[Dict[str, Any]] = None,
        related_rule_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Process and record an authorized human review action with strict role and prerequisite checks."""
        # 1. Fetch reviewer
        reviewer = self.db.get_user(reviewer_id)
        if not reviewer:
            raise PermissionError(f"Reviewer ID '{reviewer_id}' not found.")
        if not reviewer.active:
            raise PermissionError(f"Reviewer '{reviewer.username}' is inactive.")

        # 2. Parse action
        try:
            action = ReviewAction(action_name)
        except ValueError:
            raise ValueError(f"Unknown review action: '{action_name}'. Controlled actions: {[a.value for a in ReviewAction]}")

        # 3. Role-Based Access Control check
        if not reviewer.can_perform(action):
            raise PermissionError(
                f"Role '{reviewer.role.value}' does not have permission to perform action '{action.value}'. "
                f"Allowed actions: {[a.value for a in ROLE_PERMISSIONS.get(reviewer.role, set())]}"
            )

        # 4. Fetch rule and current governance state
        rule = self.registry.get_rule(rule_id)
        if not rule:
            raise ValueError(f"Rule '{rule_id}' does not exist in registry.")

        gov_state = self.db.get_rule_governance_state(rule_id)
        if not gov_state:
            raise ValueError(f"Rule '{rule_id}' has no governance record.")

        current_wf = WorkflowStatus(gov_state["workflow_status"])

        # 5. Check lifecycle transition
        allowed_transitions = LIFECYCLE_TRANSITIONS.get(current_wf, {})
        if action not in allowed_transitions:
            raise ValueError(
                f"Invalid lifecycle transition: Cannot perform '{action.value}' from status '{current_wf.value}'. "
                f"Allowed actions from '{current_wf.value}': {[a.value for a in allowed_transitions.keys()]}"
            )

        resulting_status = allowed_transitions[action]

        # 6. Special check for APPROVE_RULE
        approval_metadata = None
        if action == ReviewAction.APPROVE_RULE:
            history = self.db.get_review_history(rule_id)
            domain_deps = self._dependencies_by_domain.get(rule.domain, [])
            unresolved = [d["dependency_id"] for d in domain_deps if d.get("status") in ("PLAN_SPECIFIC_ACCESS_REQUIRED", "UNRESOLVED")]
            schema_valid = len(list(self.schema_validator.iter_errors(rule.raw_data))) == 0

            check = evaluate_approval_prerequisites(
                rule_data=rule.raw_data,
                reviewer=reviewer,
                current_workflow_status=current_wf,
                review_history_count=len(history),
                unresolved_dependencies=unresolved,
                schema_valid=schema_valid
            )

            if not check.is_eligible:
                blockers_str = "; ".join(check.blockers)
                raise ValueError(f"Approval blocked: Rule {rule_id} does not satisfy all approval prerequisites: {blockers_str}")

            approval_metadata = {
                "approved_by": reviewer.username,
                "approver_credentials": reviewer.credentials,
                "approver_role": reviewer.role.value,
                "prerequisites_satisfied": check.prerequisites
            }

        # 7. Record review action in DB
        result = self.db.record_review_action(
            rule_id=rule_id,
            reviewer=reviewer,
            action=action,
            resulting_status=resulting_status,
            comments=comments,
            source_evidence_considered=source_evidence_considered,
            change_details=change_details,
            related_rule_ids=related_rule_ids,
            approval_metadata=approval_metadata
        )

        return result

    def propose_rule_correction(
        self,
        rule_id: str,
        proposer_id: str,
        rationale: str,
        proposed_rule_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Submit a proposed correction for an existing rule without modifying the original."""
        # 1. Check proposer permission
        proposer = self.db.get_user(proposer_id)
        if not proposer:
            raise PermissionError(f"Proposer ID '{proposer_id}' not found.")
        if proposer.role == ReviewRole.VIEWER:
            raise PermissionError("Viewer role cannot propose rule corrections.")

        # 2. Rationale requirement
        if not rationale or len(rationale.strip()) < 10:
            raise ValueError("A detailed clinical rationale (minimum 10 characters) is required for proposed corrections.")

        # 3. Fetch original rule
        orig_rule = self.registry.get_rule(rule_id)
        if not orig_rule:
            raise ValueError(f"Rule '{rule_id}' not found in registry.")

        # 4. Provenance validation on updated quotation / page
        new_quote = proposed_rule_data.get("source_evidence_quotation") or proposed_rule_data.get("source_quote", "")
        if len(new_quote) < 10:
            raise ValueError("Proposed source quotation must be at least 10 characters long.")

        # 5. Schema validation on proposed data
        errors = list(self.schema_validator.iter_errors(proposed_rule_data))
        if errors:
            raise ValueError(f"Proposed correction failed canonical schema validation: {errors[0].message}")

        # 6. Compute diff summary
        diff_summary = self._compute_rule_diff(orig_rule.raw_data, proposed_rule_data)
        if not diff_summary:
            raise ValueError("No changes detected between proposed rule and original rule record.")

        # 7. Record correction in DB
        result = self.db.record_proposed_correction(
            rule_id=rule_id,
            proposer=proposer,
            rationale=rationale,
            proposed_data=proposed_rule_data,
            diff_summary=diff_summary
        )

        # Update workflow status to NEEDS_CORRECTION if currently IN_REVIEW
        gov_state = self.db.get_rule_governance_state(rule_id)
        if gov_state and gov_state["workflow_status"] == WorkflowStatus.IN_REVIEW.value:
            self.submit_review_action(
                rule_id=rule_id,
                reviewer_id=proposer.user_id,
                action_name=ReviewAction.REQUEST_CORRECTION.value,
                comments=f"Proposed correction submitted: {rationale}",
                change_details=diff_summary
            )

        return result

    def resolve_correction(
        self,
        correction_id: str,
        resolver_id: str,
        accepted: bool,
        notes: str
    ) -> Dict[str, Any]:
        """Accept or reject a proposed correction."""
        resolver = self.db.get_user(resolver_id)
        if not resolver:
            raise PermissionError(f"Resolver ID '{resolver_id}' not found.")
        if resolver.role not in (ReviewRole.CLINICAL_SME_REVIEWER, ReviewRole.MEDICAL_DIRECTOR):
            raise PermissionError(f"Role '{resolver.role.value}' cannot resolve proposed corrections.")

        return self.db.resolve_proposed_correction(
            correction_id=correction_id,
            resolver=resolver,
            accepted=accepted,
            notes=notes
        )

    def _compute_rule_diff(self, original: Dict[str, Any], proposed: Dict[str, Any]) -> Dict[str, Any]:
        """Compute side-by-side differences between original and proposed rule records."""
        diffs = {}
        all_keys = set(original.keys()) | set(proposed.keys())

        for key in sorted(all_keys):
            orig_val = original.get(key)
            prop_val = proposed.get(key)

            if orig_val != prop_val:
                diffs[key] = {
                    "original": orig_val,
                    "proposed": prop_val
                }

        return diffs
