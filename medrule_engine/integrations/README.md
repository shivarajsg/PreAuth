# MedRule Phase 3E — Production Intake Architecture & Payer Connectivity

## 1. Executive Summary

MedRule's Phase 3E establishes a modular, secure intake architecture and payer-connectivity framework. It enables the deterministic prior-authorization decision engine to interface cleanly with external eligibility, benefit configuration, authorization requirements, and clinical data sources.

**Strict Phase 3E Safety Invariant:**
- **Zero Live Outbound Transmission:** All connectors operate by default in `ConnectorMode.DISABLED` or in local deterministic `ConnectorMode.MOCK`.
- **Zero Automated Rule Approvals:** Exactly 372 rules remain active (322 `DRAFT`, 50 `NEEDS_HUMAN_REVIEW`, zero `APPROVED`).
- **Strictly Non-Binding:** Every machine assessment unconditionally enforces `is_binding: false`.
- **Zero Generative AI / Probabilistic Inference:** Built solely on deterministic logic trees and official policy criteria.

---

## 2. Component Architecture

```
                    +------------------------------------+
                    |  External EHR / Intake API Client  |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |    PriorAuthIntakeOrchestrator     |
                    +------------------------------------+
                                      |
        +-----------------------------+-----------------------------+
        |                             |                             |
        v                             v                             v
+------------------+         +------------------+         +--------------------+
|   Eligibility    |         |  Benefit & Plan  |         | Authorization Req. |
|    Connector     |         |    Connector     |         |     Connector      |
| (MOCK / DISABLED)|         | (MOCK / DISABLED)|         |  (MOCK / DISABLED) |
+------------------+         +------------------+         +--------------------+
        |                             |                             |
        +-----------------------------+-----------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |    ClinicalDataIntakeAdapter       |
                    | (Data Minimization & PHI Stripping)|
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |      PayerPlanConfigManager        |
                    | (22 Grounded Plan Configurations)  |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |      Core EvaluationService        |
                    |   (Non-Binding Deterministic Tree) |
                    +------------------------------------+
                                      |
                                      v
                    +------------------------------------+
                    |  AuthorizationSubmissionAdapter    |
                    |       (STRICTLY DISABLED)          |
                    +------------------------------------+
```

---

## 3. Ten-Stage Intake Workflow

1. **Intake Validation**: Evaluates incoming payload schema, mandatory identifiers, and procedural details. Invalid cases immediately transition to `VALIDATION_FAILED`.
2. **Member Eligibility Verification**: Checks active member coverage and effective date alignment via `EligibilityConnector`. Terminated or mismatched coverage transitions to `MANUAL_REVIEW_REQUIRED`.
3. **Benefit & Coverage Determination**: Evaluates procedure coverage, annual visit accumulators (e.g., DEP-013 visit caps), step-therapy tiering prerequisites (DEP-010), and non-covered exclusions (DEP-015) via `BenefitConnector`.
4. **Prior Authorization Requirement Determination**: Verifies whether prior auth is mandatory or notification-only via `AuthorizationRequirementsConnector`, returning the required evidence checklist.
5. **Payer & Plan Policy Context Resolution**: Matches payer ID, plan product, line of business, and date of service against `PayerPlanConfigManager`. Unresolved policies transition to `POLICY_CONTEXT_UNRESOLVED`.
6. **Clinical Data Intake & Minimization**: Sanitizes raw intake records via `ClinicalDataIntakeAdapter`, removing direct identifiers (SSN, phone, address, MRN) while preserving clinical variables.
7. **Evidence Completeness & Documentation Check**: Compares submitted attachments against policy documentation checklists. Incomplete records transition to `AWAITING_DOCUMENTATION`.
8. **Non-Binding Deterministic Evaluation Handoff**: Formulates normalized `CaseIntake` payload and passes it to `EvaluationService`.
9. **Non-Binding Result Recording & Lifecycle Transition**: Aggregates rule condition evaluations, transitions to `EVALUATED_NON_BINDING` (or `MANUAL_REVIEW_REQUIRED`), unconditionally asserting `is_binding: false`.
10. **Outbound Adapter Guard**: Asserts that `AuthorizationSubmissionAdapter` is disabled, ensuring no binding outbound transmissions occur.

---

## 4. Connector Execution Modes & Security Boundaries

Each connector inherits from `BaseConnector` and implements standard execution modes:

- `ConnectorMode.DISABLED`: Default mode for all connectors. Returns `CONNECTOR_DISABLED` without initiating I/O.
- `ConnectorMode.MOCK`: Local deterministic execution using synthetic fixtures. Used for comprehensive testing and verification.
- `ConnectorMode.LIVE_AUTHORIZED`: Reserved for future production integrations. Strictly blocked with `UnauthorizedActivationError` in Phase 3E.

### Security Context
Every invocation requires an authenticated `SecurityContext` specifying:
- `caller_id`: Unique identifier of the calling service or persona.
- `role`: Role of the caller (`INTAKE_COORDINATOR`, `CLINICAL_SME`, `SYSTEM_ADMIN`).
- `scopes`: Specific authorization scopes (e.g. `connectors:eligibility:read`, `connectors:benefits:read`).

---

## 5. Future External Integration Boundaries

MedRule's connector interfaces map directly to standard healthcare interoperability protocols:

### HL7(R) FHIR(R) Da Vinci Standards
- **Coverage Requirements Discovery (CRD / Da Vinci CRD)**:
  - Maps to `AuthorizationRequirementsConnector`.
  - Interfaces with payer CRD CDS Hooks (`order-select`, `order-sign`) to discover documentation templates and coverage rules.
- **Documentation Templates and Rules (DTR / Da Vinci DTR)**:
  - Maps to `ClinicalDataIntakeAdapter`.
  - Retrieves CQL-based Questionnaires and prepopulates structured clinical evidence from provider EHRs.
- **Prior Authorization Support (PAS / Da Vinci PAS)**:
  - Maps to `AuthorizationSubmissionAdapter`.
  - Translates FHIR Claim and ClaimResponse resources to and from ASC X12 278 transactions for electronic authorization requests.

### ASC X12 EDI Transactions
- **X12 270/271**:
  - Maps to `EligibilityConnector`.
  - 270 Health Care Eligibility Benefit Inquiry / 271 Eligibility Response.
- **X12 278**:
  - Maps to `AuthorizationSubmissionAdapter`.
  - 278 Health Care Services Review - Request and Response (Notification and Prior Authorization).

---

## 6. Audit & Traceability

Every connector execution automatically computes SHA-256 hashes of input requests and response payloads and logs immutable events to `connector_audit_events` in the SQLite governance database:
- `event_id`: Unique audit identifier (`EVT-...`).
- `case_id`: Case context identifier.
- `connector_type`: `ELIGIBILITY`, `BENEFITS`, `AUTH_REQUIREMENTS`, `CLINICAL_DATA`.
- `execution_mode`: `MOCK` or `DISABLED`.
- `latency_ms`: Duration of execution in milliseconds.
- `request_hash_sha256` & `response_hash_sha256`: Cryptographic integrity hashes.
