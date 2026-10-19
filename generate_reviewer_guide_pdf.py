"""Generate an executive-grade, beautifully formatted Reviewer Guide PDF for MedRule."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.pdfgen import canvas

PDF_PATH = r"c:\Users\KumarShiva\Downloads\PreAuth\MedRule_Reviewer_Walkthrough_Guide.pdf"


class NumberedCanvas(canvas.Canvas):
    """Custom canvas that adds headers, footers, and page numbers across all pages."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        # Top Header (pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 750, "MedRule Prior-Authorization Decision Support — Reviewer Walkthrough")
            self.drawRightString(558, 750, "Deterministic CDS Prototype")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Bottom Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 558, 42)

        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 30, "CLINICAL DECISION SUPPORT PROTOTYPE • NON-BINDING (is_binding: false) • ZERO GENERATIVE AI")

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(558, 30, page_str)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0284C7"),
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
    )

    step_title_style = ParagraphStyle(
        "StepTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
    )

    step_url_style = ParagraphStyle(
        "StepUrl",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0284C7"),
    )

    bullet_style = ParagraphStyle(
        "BulletItem",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12.8,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=2.5,
    )

    subbullet_style = ParagraphStyle(
        "SubBulletItem",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#475569"),
        leftIndent=24,
        firstLineIndent=-10,
        spaceAfter=2,
    )

    elements = []

    # Title & Subtitle
    elements.append(Paragraph("MedRule Prior-Authorization Decision Support", title_style))
    elements.append(Spacer(1, 3))
    elements.append(Paragraph("Interactive Clinical Evaluation & Reviewer Walkthrough Guide", subtitle_style))
    elements.append(Spacer(1, 8))

    # Executive Summary Table
    meta_data = [
        [
            Paragraph("<b>Live Cloud URL:</b> <font color='#0284C7'><a href='https://medrule-preauth.onrender.com'><u>https://medrule-preauth.onrender.com</u></a></font>", body_style),
            Paragraph("<b>Architecture:</b> 100% Deterministic (Zero Generative AI)", body_style),
        ],
        [
            Paragraph("<b>GitHub Repository:</b> <font color='#0284C7'><a href='https://github.com/shivarajsg/PreAuth'><u>github.com/shivarajsg/PreAuth</u></a></font>", body_style),
            Paragraph("<b>Knowledge Base:</b> 372 Policy Rules (9 Specialties)", body_style),
        ],
        [
            Paragraph("<b>Health Status:</b> <font color='#059669'><b>OPERATIONAL & HEALTHY (200 OK)</b></font>", body_style),
            Paragraph("<b>Safety Invariant:</b> Exactly 0 Approved Rules (Strictly Enforced)", body_style),
        ],
    ]
    t_meta = Table(meta_data, colWidths=[264, 240])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 6))

    # Wake-up Notice Box
    notice_text = (
        "<b>Cloud Container Notice:</b> Hosted on a containerized cloud runtime. "
        "If idle, the initial page load may require 15–25 seconds while the instance spins up. "
        "All subsequent interactions, rule searches, and case evaluations will execute immediately."
    )
    notice_table = Table([[Paragraph(notice_text, callout_style)]], colWidths=[504])
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#BFDBFE")),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(notice_table)
    elements.append(Spacer(1, 8))

    # Steps Definitions
    steps = [
        {
            "num": "1",
            "title": "System Dashboard & Governance Invariants",
            "url": "https://medrule-preauth.onrender.com/dashboard",
            "bullets": [
                ("Rule Knowledge Base Audit:", "Inspect live breakdown of 372 rules across 9 clinical specialties (322 in Draft, 50 in Needs Human Review, 0 in Approved)."),
                ("Zero-Approved Safety Invariant:", "Enforces that no rule can be auto-approved or executed in binding mode without formal multi-clinician sign-off."),
                ("Persona Switcher (Top Right):", "Switch personas to test Role-Based Access Control (RBAC):"),
            ],
            "subbullets": [
                "<b>Dr. Sarah Chen, MD:</b> Clinical SME Reviewer (Imaging & Diagnostics).",
                "<b>Dr. Eleanor Vance, MD:</b> Medical Director (Authorized Sign-Off & Approvals).",
                "<b>Quality Auditor:</b> Read-Only Compliance & Invariant Monitoring.",
            ]
        },
        {
            "num": "2",
            "title": "Rule Explorer & Clinical Policy Workbench",
            "url": "https://medrule-preauth.onrender.com/rules",
            "bullets": [
                ("Domain Filtering:", "Filter rules across Cardiology, Radiology, Oncology, Musculoskeletal, DME, and 4 other specialties."),
                ("CPT/HCPCS Search:", "Search for specific codes or clinical conditions (e.g., CPT 70450 for CT Head or CPT 93306 for Echocardiography)."),
                ("Interactive Workbench:", "Click any rule (e.g., <code>RULE-RAD-001</code>) to inspect:"),
            ],
            "subbullets": [
                "<b>Structured Logic:</b> Deterministic boolean logic trees (AND/OR condition groups and numerical thresholds).",
                "<b>Source Provenance:</b> Exact verbatim quotation from governing payer policies with physical page citations.",
            ]
        },
        {
            "num": "3",
            "title": "Human Review Queue & Governance Workflow",
            "url": "https://medrule-preauth.onrender.com/queue",
            "bullets": [
                ("Triage Ambiguous Criteria:", "Inspect the 50 rules requiring clinical human clarification due to conflicting guidelines or edge cases."),
                ("Propose Criteria Corrections:", "Submit clinical correction diffs with documented rationale and supporting medical literature citations."),
                ("Enforced Approval Prerequisites:", "Validates the 8 mandatory prerequisites (dual clinician sign-off, citation verification, audit hashing) before any promotion."),
            ],
            "subbullets": []
        },
        {
            "num": "4",
            "title": "Case Intake & Live Deterministic Evaluation",
            "url": "https://medrule-preauth.onrender.com/intake",
            "bullets": [
                ("One-Click Sample Case:", "Click <b>'Load Sample Case'</b> to populate a realistic synthetic prior-authorization request (or choose a clinical preset)."),
                ("Execute Evaluation:", "Click <b>'Run Intake & Evaluate'</b> to execute the 10-stage deterministic pipeline:"),
            ],
            "subbullets": [
                "1. Member eligibility & benefit verification (simulated connector).",
                "2. Prior-authorization requirement determination.",
                "3. Policy routing to the exact clinical guideline.",
                "4. Deterministic condition evaluation (<code>MET</code>, <code>NOT_MET</code>, or <code>UNKNOWN</code>).",
                "5. Comprehensive audit generation with full citation trace and non-binding CDS disclaimer.",
            ]
        },
        {
            "num": "5",
            "title": "Pilot Adjudication & Concordance Tracking",
            "url": "https://medrule-preauth.onrender.com/pilot",
            "bullets": [
                ("Synthetic Cohort Benchmark:", "Compare automated decision-support outputs against benchmark human adjudication across 36 pilot cases."),
                ("Discrepancy Root-Cause Analysis:", "Inspect discrepancy categories: documentation ambiguity, threshold mismatch, or missing clinical notes."),
            ],
            "subbullets": []
        },
        {
            "num": "6",
            "title": "System Health & Safety Invariant Telemetry",
            "url": "https://medrule-preauth.onrender.com/api/health",
            "bullets": [
                ("Live JSON Health Status:", "Direct machine-readable verification endpoint reporting:"),
            ],
            "subbullets": [
                "<b>database:</b> CONNECTED (SQLite with cryptographic hash-chain audit logging).",
                "<b>zero_approved_invariant:</b> true (strict enforcement active).",
                "<b>is_binding:</b> false (all evaluations remain strictly non-binding CDS).",
                "<b>submission_adapter:</b> DISABLED (external payer networks permanently locked).",
            ]
        },
    ]

    for step in steps:
        step_elements = []

        # Step Header Row: [Badge] [Title] on left, clean URL on next line
        header_table = Table(
            [
                [
                    Paragraph(f"<b>STEP {step['num']}</b>", ParagraphStyle(
                        "StepBadge", fontName="Helvetica-Bold", fontSize=8, textColor=colors.white, alignment=1
                    )),
                    Paragraph(f"<b>{step['title']}</b>", step_title_style),
                ],
                [
                    "",
                    Paragraph(f"<b>Direct URL:</b> <font color='#0284C7'><a href='{step['url']}'><u>{step['url']}</u></a></font>", step_url_style),
                ]
            ],
            colWidths=[48, 456]
        )
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#0284C7")),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        step_elements.append(header_table)
        step_elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=2, spaceAfter=3))

        # Bullets
        for lead, text in step["bullets"]:
            bullet_text = f"&bull; <b>{lead}</b> {text}"
            step_elements.append(Paragraph(bullet_text, bullet_style))

        # Sub-bullets
        for sub in step["subbullets"]:
            step_elements.append(Paragraph(f"&ndash; {sub}", subbullet_style))

        step_elements.append(Spacer(1, 4))
        elements.append(KeepTogether(step_elements))

    # Reviewer Verification Checklist (Fits cleanly on Page 2)
    elements.append(Spacer(1, 4))
    checklist_title = Paragraph("<b>Reviewer Verification Checklist</b>", ParagraphStyle(
        "ChecklistTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10, textColor=colors.HexColor("#0F172A"), spaceAfter=3
    ))
    elements.append(checklist_title)

    checklist_data = [
        [Paragraph("<b>Verification Item</b>", body_style), Paragraph("<b>Expected Behavior & Invariant</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [
            Paragraph("Zero Generative AI Invariant", body_style),
            Paragraph("100% deterministic boolean logic trees; zero hallucinated thresholds or probabilistic weights.", body_style),
            Paragraph("<font color='#059669'><b>ENFORCED</b></font>", body_style)
        ],
        [
            Paragraph("Non-Binding Evaluation", body_style),
            Paragraph("Every intake evaluation asserts <code>is_binding: false</code> with complete audit trail.", body_style),
            Paragraph("<font color='#059669'><b>ENFORCED</b></font>", body_style)
        ],
        [
            Paragraph("Zero Approved Rules", body_style),
            Paragraph("Exactly 0/372 rules in APPROVED status (322 Draft, 50 Needs Human Review).", body_style),
            Paragraph("<font color='#059669'><b>ENFORCED</b></font>", body_style)
        ],
        [
            Paragraph("Outbound Submission Locking", body_style),
            Paragraph("External submission adapter locked (DISABLED); eligibility & benefits run in mock mode.", body_style),
            Paragraph("<font color='#059669'><b>LOCKED</b></font>", body_style)
        ],
    ]
    t_checklist = Table(checklist_data, colWidths=[140, 290, 74])
    t_checklist.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_checklist)

    # Build Document
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"Successfully generated refined PDF at: {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
