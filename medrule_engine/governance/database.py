"""MedRule Persistent Governance Datastore.

Manages SQLite storage for reviewer identities, rule governance states,
review records, proposed corrections, and the append-only audit event trail.
Supports ACID transactions, cryptographic SHA-256 state chaining, and data migrations.
"""

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import logging
from pathlib import Path
import sqlite3
from typing import Any, Dict, List, Optional, Tuple, Union
import uuid

from medrule_engine.governance.models import (
    CorrectionStatus,
    ReviewAction,
    ReviewerIdentity,
    ReviewRole,
    WorkflowStatus,
)

logger = logging.getLogger(__name__)

DEFAULT_DB_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_DB_PATH = DEFAULT_DB_DIR / "governance.db"


class GovernanceDatabase:
    """Persistent SQLite database manager for MedRule governance workflow."""

    def __init__(self, db_path: Optional[Union[Path, str]] = None):
        if db_path is not None:
            self.db_path = Path(db_path) if str(db_path) != ":memory:" else db_path
        else:
            self.db_path = DEFAULT_DB_PATH
        if isinstance(self.db_path, Path) and str(self.db_path) != ":memory:":
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Create and configure a SQLite connection with foreign keys enabled, ensuring clean closure."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Initialize database tables, indexes, and initial schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Users Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                display_name TEXT NOT NULL,
                role TEXT NOT NULL,
                credentials TEXT NOT NULL,
                email TEXT,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
            """)

            # 2. Rule Governance State Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS rule_governance_state (
                rule_id TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                workflow_status TEXT NOT NULL DEFAULT 'DRAFT',
                extraction_status TEXT NOT NULL DEFAULT 'DRAFT',
                human_review_required INTEGER NOT NULL DEFAULT 0,
                is_approved INTEGER NOT NULL DEFAULT 0,
                last_action TEXT,
                last_reviewed_at TEXT,
                last_reviewed_by TEXT,
                approval_metadata_json TEXT,
                updated_at TEXT NOT NULL
            );
            """)

            # 3. Review Records Table (Immutable History)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_records (
                review_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                reviewer_id TEXT NOT NULL,
                reviewer_role TEXT NOT NULL,
                action TEXT NOT NULL,
                previous_status TEXT NOT NULL,
                resulting_status TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                comments TEXT NOT NULL,
                source_evidence_considered TEXT,
                change_details_json TEXT,
                related_rule_ids_json TEXT,
                FOREIGN KEY (rule_id) REFERENCES rule_governance_state(rule_id),
                FOREIGN KEY (reviewer_id) REFERENCES review_users(user_id)
            );
            """)

            # 4. Proposed Corrections Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS proposed_corrections (
                correction_id TEXT PRIMARY KEY,
                rule_id TEXT NOT NULL,
                proposer_id TEXT NOT NULL,
                rationale TEXT NOT NULL,
                proposed_data_json TEXT NOT NULL,
                diff_summary_json TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                created_at TEXT NOT NULL,
                resolved_at TEXT,
                resolved_by TEXT,
                resolution_notes TEXT,
                FOREIGN KEY (rule_id) REFERENCES rule_governance_state(rule_id),
                FOREIGN KEY (proposer_id) REFERENCES review_users(user_id)
            );
            """)

            # 5. Append-Only Audit Events Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                actor_role TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                details_json TEXT NOT NULL,
                prev_state_hash TEXT NOT NULL,
                new_state_hash TEXT NOT NULL,
                event_signature_sha256 TEXT NOT NULL
            );
            """)

            # 6. Pilot Evaluations Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pilot_evaluations (
                case_id TEXT PRIMARY KEY,
                clinical_domain TEXT NOT NULL,
                procedure_code TEXT NOT NULL,
                procedure_name TEXT NOT NULL,
                line_of_business TEXT NOT NULL,
                requested_date_of_service TEXT NOT NULL,
                engine_status TEXT NOT NULL,
                expected_status TEXT NOT NULL,
                status_match INTEGER NOT NULL,
                human_adjudication_decision TEXT,
                human_comparison_status TEXT,
                discrepancy_id TEXT,
                is_binding INTEGER NOT NULL DEFAULT 0,
                reproducibility_hash_sha256 TEXT NOT NULL,
                evaluation_metadata_json TEXT NOT NULL,
                evaluated_at TEXT NOT NULL
            );
            """)

            # 7. Human Clinical Adjudications Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS human_adjudications (
                adjudication_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                reviewer_id TEXT NOT NULL,
                reviewer_name TEXT NOT NULL,
                reviewer_role TEXT NOT NULL,
                clinical_domain TEXT NOT NULL,
                procedure_code TEXT NOT NULL,
                human_adjudication_decision TEXT NOT NULL,
                human_adjudication_rationale TEXT NOT NULL,
                source_evidence_considered TEXT,
                comparison_status_with_engine TEXT NOT NULL,
                discrepancy_id TEXT,
                adjudication_timestamp TEXT NOT NULL
            );
            """)

            # 8. Pilot Discrepancies Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pilot_discrepancies (
                discrepancy_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                clinical_domain TEXT NOT NULL,
                procedure_code TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                policy_version TEXT NOT NULL,
                source_section TEXT,
                engine_assessment TEXT NOT NULL,
                human_assessment TEXT NOT NULL,
                discrepancy_category TEXT NOT NULL,
                root_cause_analysis TEXT NOT NULL,
                remediation_proposal TEXT NOT NULL,
                assigned_reviewer TEXT NOT NULL,
                remediation_status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """)

            # 9. Case Intake Records Table (Phase 3E)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS case_intake_records (
                case_id TEXT PRIMARY KEY,
                lifecycle_state TEXT NOT NULL,
                received_at TEXT NOT NULL,
                last_updated_at TEXT NOT NULL,
                is_binding INTEGER NOT NULL DEFAULT 0 CHECK(is_binding = 0),
                payer_id TEXT,
                plan_id TEXT,
                line_of_business TEXT,
                clinical_domain TEXT,
                procedure_code TEXT,
                state_history_json TEXT NOT NULL,
                unresolved_dependencies_json TEXT,
                missing_documentation_json TEXT,
                connector_events_json TEXT,
                evaluation_result_json TEXT,
                metadata_json TEXT
            );
            """)

            # 10. Connector Audit Events Table (Phase 3E)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS connector_audit_events (
                event_id TEXT PRIMARY KEY,
                case_id TEXT,
                connector_type TEXT NOT NULL,
                execution_mode TEXT NOT NULL,
                status TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                latency_ms REAL NOT NULL,
                reference_id TEXT,
                request_hash_sha256 TEXT NOT NULL,
                response_hash_sha256 TEXT NOT NULL,
                error_details TEXT,
                metadata_json TEXT
            );
            """)

            # 11. Payer Plan Configurations Table (Phase 3E)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS payer_plan_configurations (
                config_id TEXT PRIMARY KEY,
                payer_id TEXT NOT NULL,
                plan_id TEXT NOT NULL,
                line_of_business TEXT NOT NULL,
                clinical_domain TEXT NOT NULL,
                procedure_code TEXT NOT NULL,
                procedure_name TEXT,
                effective_date_start TEXT NOT NULL,
                effective_date_end TEXT NOT NULL,
                governing_policy_id TEXT NOT NULL,
                governing_policy_title TEXT,
                governing_policy_version TEXT,
                verification_status TEXT NOT NULL,
                config_version TEXT NOT NULL,
                config_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """)

            # Indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_rule_gov_domain ON rule_governance_state(domain);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_rule_gov_status ON rule_governance_state(workflow_status);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_review_rule_id ON review_records(rule_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_corrections_rule_id ON proposed_corrections(rule_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_rule_id ON audit_events(rule_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pilot_eval_domain ON pilot_evaluations(clinical_domain);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_human_adj_case ON human_adjudications(case_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_discrepancies_case ON pilot_discrepancies(case_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_case_intake_state ON case_intake_records(lifecycle_state);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_connector_events_case ON connector_audit_events(case_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_payer_cfg_key ON payer_plan_configurations(clinical_domain, procedure_code, line_of_business);")

            conn.commit()

        # Seed default realistic review personas for development
        self.seed_default_users()

    def seed_default_users(self) -> None:
        """Seed realistic clinical personas for development testing."""
        default_users = [
            ReviewerIdentity(
                user_id="USR-VIEWER-01",
                username="auditor_viewer",
                display_name="Quality Auditor (Viewer)",
                role=ReviewRole.VIEWER,
                credentials="BS, RHIA, Health Information Specialist",
                email="auditor@medrule.org"
            ),
            ReviewerIdentity(
                user_id="USR-SME-01",
                username="dr_sarah_chen",
                display_name="Dr. Sarah Chen, MD",
                role=ReviewRole.CLINICAL_SME_REVIEWER,
                credentials="MD, Board Certified Radiologist & Imaging SME",
                email="schen@medrule.org"
            ),
            ReviewerIdentity(
                user_id="USR-SME-02",
                username="dr_james_wilson",
                display_name="Dr. James Wilson, MD",
                role=ReviewRole.CLINICAL_SME_REVIEWER,
                credentials="MD, FACC, Cardiologist & Vascular Specialist",
                email="jwilson@medrule.org"
            ),
            ReviewerIdentity(
                user_id="USR-MEDDIR-01",
                username="dr_eleanor_vance",
                display_name="Dr. Eleanor Vance, MD",
                role=ReviewRole.MEDICAL_DIRECTOR,
                credentials="MD, MBA, Chief Medical Officer & Authorized Approver",
                email="evance@medrule.org"
            ),
            ReviewerIdentity(
                user_id="USR-ADMIN-01",
                username="admin_governance",
                display_name="Governance Administrator",
                role=ReviewRole.ADMINISTRATOR,
                credentials="MS, Certified Healthcare Compliance (CHC)",
                email="admin@medrule.org"
            ),
        ]

        now = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for u in default_users:
                cursor.execute("""
                INSERT OR IGNORE INTO review_users 
                (user_id, username, display_name, role, credentials, email, active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 1, ?)
                """, (u.user_id, u.username, u.display_name, u.role.value, u.credentials, u.email, now))
            conn.commit()

    def get_user(self, user_id: str) -> Optional[ReviewerIdentity]:
        """Fetch user by ID."""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM review_users WHERE user_id = ?", (user_id,)).fetchone()
            if not row:
                return None
            return ReviewerIdentity(
                user_id=row["user_id"],
                username=row["username"],
                display_name=row["display_name"],
                role=ReviewRole(row["role"]),
                credentials=row["credentials"],
                email=row["email"] or "",
                active=bool(row["active"])
            )

    def get_user_by_username(self, username: str) -> Optional[ReviewerIdentity]:
        """Fetch user by username."""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM review_users WHERE username = ?", (username,)).fetchone()
            if not row:
                return None
            return ReviewerIdentity(
                user_id=row["user_id"],
                username=row["username"],
                display_name=row["display_name"],
                role=ReviewRole(row["role"]),
                credentials=row["credentials"],
                email=row["email"] or "",
                active=bool(row["active"])
            )

    def list_users(self) -> List[ReviewerIdentity]:
        """List all active reviewer identities."""
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM review_users WHERE active = 1 ORDER BY display_name").fetchall()
            return [
                ReviewerIdentity(
                    user_id=r["user_id"],
                    username=r["username"],
                    display_name=r["display_name"],
                    role=ReviewRole(r["role"]),
                    credentials=r["credentials"],
                    email=r["email"] or "",
                    active=bool(r["active"])
                ) for r in rows
            ]

    def sync_rules_from_registry(self, rule_records: List[Any]) -> int:
        """Sync loaded rules from RuleRegistry into rule_governance_state table.
        
        Preserves existing review states if already populated.
        """
        now = datetime.now(timezone.utc).isoformat()
        synced_count = 0
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for r in rule_records:
                rule_id = r.rule_id
                dom = r.domain
                ext_status = r.extraction_status
                hr_req = 1 if r.human_review_required else 0
                
                # Default workflow status:
                # If rule is already flagged as NEEDS_HUMAN_REVIEW, workflow status is IN_REVIEW or DRAFT
                default_wf = WorkflowStatus.DRAFT.value

                cursor.execute("""
                INSERT OR IGNORE INTO rule_governance_state
                (rule_id, domain, workflow_status, extraction_status, human_review_required, is_approved, updated_at)
                VALUES (?, ?, ?, ?, ?, 0, ?)
                """, (rule_id, dom, default_wf, ext_status, hr_req, now))
                synced_count += 1
            conn.commit()
        return synced_count

    def get_rule_governance_state(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """Fetch current governance state for a rule."""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM rule_governance_state WHERE rule_id = ?", (rule_id,)).fetchone()
            if not row:
                return None
            return dict(row)

    def get_all_governance_states(self) -> Dict[str, Dict[str, Any]]:
        """Fetch governance state for all rules indexed by rule_id."""
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM rule_governance_state").fetchall()
            return {r["rule_id"]: dict(r) for r in rows}

    def record_review_action(
        self,
        rule_id: str,
        reviewer: ReviewerIdentity,
        action: ReviewAction,
        resulting_status: WorkflowStatus,
        comments: str,
        source_evidence_considered: str = "",
        change_details: Optional[Dict[str, Any]] = None,
        related_rule_ids: Optional[List[str]] = None,
        approval_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Record a validated review action with transaction and append-only audit event."""
        now = datetime.now(timezone.utc).isoformat()
        review_id = f"REV-{uuid.uuid4().hex[:12].upper()}"

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Fetch previous state
            prev_row = cursor.execute("SELECT * FROM rule_governance_state WHERE rule_id = ?", (rule_id,)).fetchone()
            if not prev_row:
                raise ValueError(f"Rule {rule_id} does not exist in governance database.")
            
            prev_status = prev_row["workflow_status"]
            prev_state_str = json.dumps(dict(prev_row), sort_keys=True)
            prev_hash = hashlib.sha256(prev_state_str.encode("utf-8")).hexdigest()

            is_app = 1 if resulting_status == WorkflowStatus.APPROVED else 0
            app_meta_json = json.dumps(approval_metadata) if approval_metadata else None

            # 2. Update rule_governance_state
            cursor.execute("""
            UPDATE rule_governance_state
            SET workflow_status = ?,
                is_approved = ?,
                last_action = ?,
                last_reviewed_at = ?,
                last_reviewed_by = ?,
                approval_metadata_json = COALESCE(?, approval_metadata_json),
                updated_at = ?
            WHERE rule_id = ?
            """, (resulting_status.value, is_app, action.value, now, reviewer.username, app_meta_json, now, rule_id))

            # 3. Insert review_record
            cursor.execute("""
            INSERT INTO review_records
            (review_id, rule_id, reviewer_id, reviewer_role, action, previous_status, resulting_status,
             timestamp, comments, source_evidence_considered, change_details_json, related_rule_ids_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                review_id,
                rule_id,
                reviewer.user_id,
                reviewer.role.value,
                action.value,
                prev_status,
                resulting_status.value,
                now,
                comments,
                source_evidence_considered,
                json.dumps(change_details or {}),
                json.dumps(related_rule_ids or [])
            ))

            # 4. Fetch new state and compute hash
            new_row = cursor.execute("SELECT * FROM rule_governance_state WHERE rule_id = ?", (rule_id,)).fetchone()
            new_state_str = json.dumps(dict(new_row), sort_keys=True)
            new_hash = hashlib.sha256(new_state_str.encode("utf-8")).hexdigest()

            # 5. Append-only audit event
            event_id = f"EVT-{uuid.uuid4().hex[:12].upper()}"
            event_details = {
                "review_id": review_id,
                "action": action.value,
                "from_status": prev_status,
                "to_status": resulting_status.value,
                "comments": comments,
                "reviewer": {
                    "user_id": reviewer.user_id,
                    "username": reviewer.username,
                    "role": reviewer.role.value,
                    "credentials": reviewer.credentials
                }
            }
            details_json = json.dumps(event_details, sort_keys=True)
            sig_payload = f"{event_id}|{rule_id}|{reviewer.user_id}|{now}|{prev_hash}|{new_hash}|{details_json}"
            event_sig = hashlib.sha256(sig_payload.encode("utf-8")).hexdigest()

            cursor.execute("""
            INSERT INTO audit_events
            (event_id, event_type, rule_id, actor_id, actor_role, timestamp, details_json,
             prev_state_hash, new_state_hash, event_signature_sha256)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id,
                "REVIEW_ACTION",
                rule_id,
                reviewer.user_id,
                reviewer.role.value,
                now,
                details_json,
                prev_hash,
                new_hash,
                event_sig
            ))

            conn.commit()

        return {
            "review_id": review_id,
            "rule_id": rule_id,
            "action": action.value,
            "previous_status": prev_status,
            "resulting_status": resulting_status.value,
            "timestamp": now,
            "audit_event_id": event_id,
            "audit_signature": event_sig
        }

    def record_proposed_correction(
        self,
        rule_id: str,
        proposer: ReviewerIdentity,
        rationale: str,
        proposed_data: Dict[str, Any],
        diff_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Record a proposed correction without modifying the original rule."""
        now = datetime.now(timezone.utc).isoformat()
        correction_id = f"CORR-{uuid.uuid4().hex[:12].upper()}"

        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO proposed_corrections
            (correction_id, rule_id, proposer_id, rationale, proposed_data_json, diff_summary_json, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                correction_id,
                rule_id,
                proposer.user_id,
                rationale,
                json.dumps(proposed_data),
                json.dumps(diff_summary),
                CorrectionStatus.PENDING.value,
                now
            ))

            # Audit event
            event_id = f"EVT-{uuid.uuid4().hex[:12].upper()}"
            details = {
                "correction_id": correction_id,
                "rationale": rationale,
                "diff_summary": diff_summary,
                "proposer": proposer.username
            }
            details_json = json.dumps(details, sort_keys=True)
            sig = hashlib.sha256(f"{event_id}|{rule_id}|{proposer.user_id}|{now}|{details_json}".encode("utf-8")).hexdigest()

            cursor.execute("""
            INSERT INTO audit_events
            (event_id, event_type, rule_id, actor_id, actor_role, timestamp, details_json,
             prev_state_hash, new_state_hash, event_signature_sha256)
            VALUES (?, ?, ?, ?, ?, ?, ?, '', '', ?)
            """, (event_id, "PROPOSE_CORRECTION", rule_id, proposer.user_id, proposer.role.value, now, details_json, sig))

            conn.commit()

        return {
            "correction_id": correction_id,
            "rule_id": rule_id,
            "status": CorrectionStatus.PENDING.value,
            "created_at": now
        }

    def resolve_proposed_correction(
        self,
        correction_id: str,
        resolver: ReviewerIdentity,
        accepted: bool,
        notes: str
    ) -> Dict[str, Any]:
        """Accept or reject a proposed correction with audit logging."""
        now = datetime.now(timezone.utc).isoformat()
        new_status = CorrectionStatus.ACCEPTED if accepted else CorrectionStatus.REJECTED

        with self.get_connection() as conn:
            cursor = conn.cursor()
            corr = cursor.execute("SELECT * FROM proposed_corrections WHERE correction_id = ?", (correction_id,)).fetchone()
            if not corr:
                raise ValueError(f"Correction {correction_id} not found.")

            cursor.execute("""
            UPDATE proposed_corrections
            SET status = ?, resolved_at = ?, resolved_by = ?, resolution_notes = ?
            WHERE correction_id = ?
            """, (new_status.value, now, resolver.username, notes, correction_id))

            # Audit event
            event_id = f"EVT-{uuid.uuid4().hex[:12].upper()}"
            details = {
                "correction_id": correction_id,
                "resolution": new_status.value,
                "resolver": resolver.username,
                "notes": notes
            }
            details_json = json.dumps(details, sort_keys=True)
            sig = hashlib.sha256(f"{event_id}|{corr['rule_id']}|{resolver.user_id}|{now}|{details_json}".encode("utf-8")).hexdigest()

            cursor.execute("""
            INSERT INTO audit_events
            (event_id, event_type, rule_id, actor_id, actor_role, timestamp, details_json,
             prev_state_hash, new_state_hash, event_signature_sha256)
            VALUES (?, ?, ?, ?, ?, ?, ?, '', '', ?)
            """, (event_id, "RESOLVE_CORRECTION", corr["rule_id"], resolver.user_id, resolver.role.value, now, details_json, sig))

            conn.commit()

        return {
            "correction_id": correction_id,
            "status": new_status.value,
            "resolved_at": now,
            "resolved_by": resolver.username
        }

    def get_review_history(self, rule_id: str) -> List[Dict[str, Any]]:
        """Fetch chronologically ordered review records for a rule."""
        with self.get_connection() as conn:
            rows = conn.execute("""
            SELECT r.*, u.display_name, u.credentials
            FROM review_records r
            LEFT JOIN review_users u ON r.reviewer_id = u.user_id
            WHERE r.rule_id = ?
            ORDER BY r.timestamp ASC
            """, (rule_id,)).fetchall()
            return [dict(r) for r in rows]

    def get_proposed_corrections(self, rule_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch proposed corrections (optionally filtered by rule_id)."""
        with self.get_connection() as conn:
            if rule_id:
                rows = conn.execute("""
                SELECT c.*, u.display_name, u.role as proposer_role
                FROM proposed_corrections c
                LEFT JOIN review_users u ON c.proposer_id = u.user_id
                WHERE c.rule_id = ?
                ORDER BY c.created_at DESC
                """, (rule_id,)).fetchall()
            else:
                rows = conn.execute("""
                SELECT c.*, u.display_name, u.role as proposer_role
                FROM proposed_corrections c
                LEFT JOIN review_users u ON c.proposer_id = u.user_id
                ORDER BY c.created_at DESC
                """).fetchall()
            return [dict(r) for r in rows]

    def get_audit_trail(self, rule_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch append-only audit events."""
        with self.get_connection() as conn:
            if rule_id:
                rows = conn.execute("""
                SELECT a.*, u.display_name
                FROM audit_events a
                LEFT JOIN review_users u ON a.actor_id = u.user_id
                WHERE a.rule_id = ?
                ORDER BY a.timestamp DESC
                LIMIT ?
                """, (rule_id, limit)).fetchall()
            else:
                rows = conn.execute("""
                SELECT a.*, u.display_name
                FROM audit_events a
                LEFT JOIN review_users u ON a.actor_id = u.user_id
                ORDER BY a.timestamp DESC
                LIMIT ?
                """, (limit,)).fetchall()
            return [dict(r) for r in rows]

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Compute live governance metrics from actual database records."""
        with self.get_connection() as conn:
            total_rules = conn.execute("SELECT COUNT(*) FROM rule_governance_state").fetchone()[0]
            
            # Workflow statuses
            wf_counts = {}
            for r in conn.execute("SELECT workflow_status, COUNT(*) as c FROM rule_governance_state GROUP BY workflow_status"):
                wf_counts[r["workflow_status"]] = r["c"]

            # Extraction statuses
            ext_counts = {}
            for r in conn.execute("SELECT extraction_status, COUNT(*) as c FROM rule_governance_state GROUP BY extraction_status"):
                ext_counts[r["extraction_status"]] = r["c"]

            # Domains
            dom_counts = {}
            for r in conn.execute("SELECT domain, COUNT(*) as c FROM rule_governance_state GROUP BY domain"):
                dom_counts[r["domain"]] = r["c"]

            # Awaiting review: rules where human_review_required = 1 or workflow_status in ('DRAFT', 'IN_REVIEW', 'NEEDS_CORRECTION')
            awaiting_review = conn.execute("""
            SELECT COUNT(*) FROM rule_governance_state 
            WHERE human_review_required = 1 OR workflow_status IN ('IN_REVIEW', 'NEEDS_CORRECTION', 'READY_FOR_MEDICAL_DIRECTOR')
            """).fetchone()[0]

            approved_count = conn.execute("SELECT COUNT(*) FROM rule_governance_state WHERE is_approved = 1").fetchone()[0]
            pending_corrections = conn.execute("SELECT COUNT(*) FROM proposed_corrections WHERE status = 'PENDING'").fetchone()[0]
            total_reviews = conn.execute("SELECT COUNT(*) FROM review_records").fetchone()[0]
            total_audits = conn.execute("SELECT COUNT(*) FROM audit_events").fetchone()[0]

            # Pilot adjudication metrics
            total_pilot_cases = conn.execute("SELECT COUNT(*) FROM pilot_evaluations").fetchone()[0]
            pilot_matches = conn.execute("SELECT COUNT(*) FROM pilot_evaluations WHERE status_match = 1").fetchone()[0]
            pilot_discrepancies = conn.execute("SELECT COUNT(*) FROM pilot_discrepancies").fetchone()[0]
            pilot_match_rate = round((pilot_matches / total_pilot_cases * 100), 1) if total_pilot_cases > 0 else 0.0

            # Intake records metrics (Phase 3E/3F)
            total_intake_cases = conn.execute("SELECT COUNT(*) FROM case_intake_records").fetchone()[0]
            intake_state_counts = {}
            for r in conn.execute("SELECT lifecycle_state, COUNT(*) as c FROM case_intake_records GROUP BY lifecycle_state"):
                intake_state_counts[r["lifecycle_state"]] = r["c"]

            # Connector metrics (Phase 3E/3F)
            total_connector_events = conn.execute("SELECT COUNT(*) FROM connector_audit_events").fetchone()[0]
            connector_mode_counts = {}
            for r in conn.execute("SELECT execution_mode, COUNT(*) as c FROM connector_audit_events GROUP BY execution_mode"):
                connector_mode_counts[r["execution_mode"]] = r["c"]

            total_payer_configs = conn.execute("SELECT COUNT(*) FROM payer_plan_configurations").fetchone()[0]

            return {
                "total_rules": total_rules,
                "workflow_status_counts": wf_counts,
                "extraction_status_counts": ext_counts,
                "domain_counts": dom_counts,
                "awaiting_human_review": awaiting_review,
                "approved_rules": approved_count,
                "pending_corrections": pending_corrections,
                "total_review_records": total_reviews,
                "total_audit_events": total_audits,
                "zero_approved_governance_enforced": approved_count == 0,
                "total_pilot_cases": total_pilot_cases,
                "pilot_matches": pilot_matches,
                "pilot_discrepancies": pilot_discrepancies,
                "pilot_match_rate": pilot_match_rate,
                "total_intake_cases": total_intake_cases,
                "intake_state_counts": intake_state_counts,
                "total_connector_events": total_connector_events,
                "connector_mode_counts": connector_mode_counts,
                "total_payer_configs": total_payer_configs,
                "outbound_submission_disabled": True,
                "non_binding_enforced": True
            }

    # =========================================================
    # Phase 3D Pilot Adjudication Methods
    # =========================================================

    def save_pilot_evaluation(self, eval_data: Dict[str, Any]) -> None:
        """Save or update a pilot case evaluation record."""
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO pilot_evaluations (
                case_id, clinical_domain, procedure_code, procedure_name,
                line_of_business, requested_date_of_service, engine_status,
                expected_status, status_match, human_adjudication_decision,
                human_comparison_status, discrepancy_id, is_binding,
                reproducibility_hash_sha256, evaluation_metadata_json, evaluated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                eval_data["case_id"],
                eval_data["clinical_domain"],
                eval_data["procedure_code"],
                eval_data.get("procedure_name", ""),
                eval_data.get("line_of_business", "COMMERCIAL"),
                eval_data.get("date_of_service", "2026-01-01"),
                eval_data["engine_status"],
                eval_data.get("expected_status", ""),
                1 if eval_data.get("status_match") else 0,
                eval_data.get("human_adjudication_decision"),
                eval_data.get("human_comparison_status"),
                eval_data.get("discrepancy_id"),
                1 if eval_data.get("is_binding") else 0,
                eval_data.get("reproducibility_hash_sha256", ""),
                json.dumps(eval_data),
                datetime.now(timezone.utc).isoformat()
            ))
            conn.commit()

    def get_pilot_evaluations(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve pilot evaluations with optional domain filter."""
        with self.get_connection() as conn:
            if domain:
                rows = conn.execute(
                    "SELECT * FROM pilot_evaluations WHERE clinical_domain = ? ORDER BY case_id ASC",
                    (domain,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM pilot_evaluations ORDER BY case_id ASC"
                ).fetchall()
            return [dict(r) for r in rows]

    def get_pilot_evaluation(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific pilot case evaluation."""
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM pilot_evaluations WHERE case_id = ?",
                (case_id,)
            ).fetchone()
            return dict(row) if row else None

    def save_human_adjudication(self, adj_data: Dict[str, Any]) -> None:
        """Save or update a human clinical SME adjudication record."""
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO human_adjudications (
                adjudication_id, case_id, reviewer_id, reviewer_name,
                reviewer_role, clinical_domain, procedure_code,
                human_adjudication_decision, human_adjudication_rationale,
                source_evidence_considered, comparison_status_with_engine,
                discrepancy_id, adjudication_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                adj_data["adjudication_id"],
                adj_data["case_id"],
                adj_data["reviewer_id"],
                adj_data["reviewer_name"],
                adj_data["reviewer_role"],
                adj_data["clinical_domain"],
                adj_data["procedure_code"],
                adj_data["human_adjudication_decision"],
                adj_data["human_adjudication_rationale"],
                adj_data.get("source_evidence_considered", ""),
                adj_data.get("comparison_status_with_engine", "AGREEMENT"),
                adj_data.get("discrepancy_id"),
                adj_data.get("adjudication_timestamp", datetime.now(timezone.utc).isoformat())
            ))
            conn.commit()

    def get_human_adjudications(self) -> List[Dict[str, Any]]:
        """Retrieve all human adjudications."""
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM human_adjudications ORDER BY case_id ASC").fetchall()
            return [dict(r) for r in rows]

    def save_pilot_discrepancy(self, disc_data: Dict[str, Any]) -> None:
        """Save or update a pilot discrepancy record."""
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO pilot_discrepancies (
                discrepancy_id, case_id, clinical_domain, procedure_code,
                rule_id, policy_version, source_section, engine_assessment,
                human_assessment, discrepancy_category, root_cause_analysis,
                remediation_proposal, assigned_reviewer, remediation_status,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                disc_data["discrepancy_id"],
                disc_data["case_id"],
                disc_data["clinical_domain"],
                disc_data["procedure_code"],
                disc_data["rule_id"],
                disc_data.get("policy_version", ""),
                disc_data.get("source_section", ""),
                disc_data["engine_assessment"],
                disc_data["human_assessment"],
                disc_data["discrepancy_category"],
                disc_data["root_cause_analysis"],
                disc_data["remediation_proposal"],
                disc_data["assigned_reviewer"],
                disc_data.get("remediation_status", "OPEN"),
                disc_data.get("created_at", datetime.now(timezone.utc).isoformat()),
                disc_data.get("updated_at", datetime.now(timezone.utc).isoformat())
            ))
            conn.commit()

    def get_pilot_discrepancies(self) -> List[Dict[str, Any]]:
        """Retrieve all tracked pilot discrepancies."""
        with self.get_connection() as conn:
            rows = conn.execute("SELECT * FROM pilot_discrepancies ORDER BY discrepancy_id ASC").fetchall()
            return [dict(r) for r in rows]

    def sync_pilot_results(self, pilot_run_results_file: Path) -> int:
        """Sync evaluated pilot cases from pilot_run_results.json into database."""
        if not pilot_run_results_file.exists():
            return 0
        with open(pilot_run_results_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        evals = data.get("case_evaluations", [])
        for ev in evals:
            self.save_pilot_evaluation(ev)
        return len(evals)

    def sync_pilot_all(self, pilot_dir: Path) -> Dict[str, int]:
        """Sync pilot evaluations, human adjudications, and discrepancies into SQLite."""
        counts = {"evaluations": 0, "adjudications": 0, "discrepancies": 0}
        
        eval_file = pilot_dir / "pilot_run_results.json"
        counts["evaluations"] = self.sync_pilot_results(eval_file)
        
        adj_file = pilot_dir / "human_adjudication_log.csv"
        if adj_file.exists():
            import csv
            with open(adj_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self.save_human_adjudication(dict(r))
                    counts["adjudications"] += 1

        disc_file = pilot_dir / "pilot_discrepancies.csv"
        if disc_file.exists():
            import csv
            with open(disc_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self.save_pilot_discrepancy(dict(r))
                    counts["discrepancies"] += 1

        return counts

    # =========================================================================
    # Phase 3E: Intake Records, Connector Audits & Payer Plan Configurations
    # =========================================================================

    def save_case_intake_record(self, intake_data: Dict[str, Any]) -> None:
        """Save or update a case intake lifecycle record."""
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO case_intake_records (
                case_id, lifecycle_state, received_at, last_updated_at,
                is_binding, payer_id, plan_id, line_of_business,
                clinical_domain, procedure_code, state_history_json,
                unresolved_dependencies_json, missing_documentation_json,
                connector_events_json, evaluation_result_json, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                intake_data["case_id"],
                intake_data["lifecycle_state"],
                intake_data.get("received_at", datetime.now(timezone.utc).isoformat()),
                intake_data.get("last_updated_at", datetime.now(timezone.utc).isoformat()),
                0,  # is_binding unconditionally 0
                intake_data.get("payer_id"),
                intake_data.get("plan_id"),
                intake_data.get("line_of_business"),
                intake_data.get("clinical_domain"),
                intake_data.get("procedure_code"),
                json.dumps(intake_data.get("state_history", [])),
                json.dumps(intake_data.get("unresolved_dependencies", [])),
                json.dumps(intake_data.get("missing_documentation", [])),
                json.dumps(intake_data.get("connector_events", [])),
                json.dumps(intake_data.get("evaluation_result", {})) if intake_data.get("evaluation_result") else None,
                json.dumps(intake_data.get("metadata", {}))
            ))
            conn.commit()

    def get_case_intake_record(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve case intake record by case_id."""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM case_intake_records WHERE case_id = ?", (case_id,)).fetchone()
            if not row:
                return None
            res = dict(row)
            res["is_binding"] = False
            res["state_history"] = json.loads(res.get("state_history_json") or "[]")
            res["unresolved_dependencies"] = json.loads(res.get("unresolved_dependencies_json") or "[]")
            res["missing_documentation"] = json.loads(res.get("missing_documentation_json") or "[]")
            res["connector_events"] = json.loads(res.get("connector_events_json") or "[]")
            res["evaluation_result"] = json.loads(res.get("evaluation_result_json") or "{}") if res.get("evaluation_result_json") else None
            res["metadata"] = json.loads(res.get("metadata_json") or "{}")
            return res

    def list_case_intake_records(self, lifecycle_state: Optional[str] = None) -> List[Dict[str, Any]]:
        """List case intake records, optionally filtered by state."""
        with self.get_connection() as conn:
            if lifecycle_state:
                rows = conn.execute("SELECT * FROM case_intake_records WHERE lifecycle_state = ? ORDER BY last_updated_at DESC", (lifecycle_state,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM case_intake_records ORDER BY last_updated_at DESC").fetchall()
            
            result: List[Dict[str, Any]] = []
            for r in rows:
                item = dict(r)
                item["is_binding"] = False
                item["state_history"] = json.loads(item.get("state_history_json") or "[]")
                item["unresolved_dependencies"] = json.loads(item.get("unresolved_dependencies_json") or "[]")
                item["missing_documentation"] = json.loads(item.get("missing_documentation_json") or "[]")
                item["connector_events"] = json.loads(item.get("connector_events_json") or "[]")
                item["evaluation_result"] = json.loads(item.get("evaluation_result_json") or "{}") if item.get("evaluation_result_json") else None
                item["metadata"] = json.loads(item.get("metadata_json") or "{}")
                result.append(item)
            return result

    def save_connector_audit_event(self, event_data: Dict[str, Any]) -> None:
        """Save a connector execution audit event."""
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO connector_audit_events (
                event_id, case_id, connector_type, execution_mode,
                status, timestamp, latency_ms, reference_id,
                request_hash_sha256, response_hash_sha256,
                error_details, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_data.get("event_id", f"EVT-{uuid.uuid4().hex[:12].upper()}"),
                event_data.get("case_id"),
                event_data["connector_type"],
                event_data["execution_mode"],
                event_data["status"],
                event_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
                event_data.get("latency_ms", 0.0),
                event_data.get("reference_id"),
                event_data.get("request_hash_sha256", ""),
                event_data.get("response_hash_sha256", ""),
                event_data.get("error_details"),
                json.dumps(event_data.get("metadata", {}))
            ))
            conn.commit()

    def list_connector_audit_events(self, case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """List connector audit events, optionally filtered by case_id."""
        with self.get_connection() as conn:
            if case_id:
                rows = conn.execute("SELECT * FROM connector_audit_events WHERE case_id = ? ORDER BY timestamp ASC", (case_id,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM connector_audit_events ORDER BY timestamp DESC").fetchall()
            
            result: List[Dict[str, Any]] = []
            for r in rows:
                item = dict(r)
                item["metadata"] = json.loads(item.get("metadata_json") or "{}")
                result.append(item)
            return result

    def save_payer_plan_config(self, config_data: Dict[str, Any]) -> None:
        """Save or update a payer plan configuration."""
        with self.get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO payer_plan_configurations (
                config_id, payer_id, plan_id, line_of_business,
                clinical_domain, procedure_code, procedure_name,
                effective_date_start, effective_date_end,
                governing_policy_id, governing_policy_title,
                governing_policy_version, verification_status,
                config_version, config_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                config_data["config_id"],
                config_data["payer_id"],
                config_data["plan_id"],
                config_data["line_of_business"],
                config_data["clinical_domain"],
                config_data["procedure_code"],
                config_data.get("procedure_name"),
                config_data["effective_date_start"],
                config_data["effective_date_end"],
                config_data["governing_policy_id"],
                config_data.get("governing_policy_title"),
                config_data.get("governing_policy_version"),
                config_data.get("verification_status", "DRAFT"),
                config_data.get("config_version", "1.0.0"),
                json.dumps(config_data),
                datetime.now(timezone.utc).isoformat()
            ))
            conn.commit()

    def get_payer_plan_config(self, config_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve payer plan configuration by config_id."""
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM payer_plan_configurations WHERE config_id = ?", (config_id,)).fetchone()
            if not row:
                return None
            res = dict(row)
            res["config"] = json.loads(res.get("config_json") or "{}")
            return res

    def list_payer_plan_configs(self, clinical_domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all payer plan configurations, optionally filtered by domain."""
        with self.get_connection() as conn:
            if clinical_domain:
                rows = conn.execute("SELECT * FROM payer_plan_configurations WHERE clinical_domain = ? ORDER BY config_id ASC", (clinical_domain,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM payer_plan_configurations ORDER BY config_id ASC").fetchall()
            
            result: List[Dict[str, Any]] = []
            for r in rows:
                item = dict(r)
                item["config"] = json.loads(item.get("config_json") or "{}")
                result.append(item)
            return result


