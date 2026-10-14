"""Renders an audit report PDF summarizing the analysis for download."""
from __future__ import annotations

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

styles = getSampleStyleSheet()
TITLE_STYLE = ParagraphStyle("TitleX", parent=styles["Title"], fontSize=20)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], spaceBefore=14, spaceAfter=6)
BODY = styles["BodyText"]
SMALL = ParagraphStyle("Small", parent=styles["BodyText"], fontSize=8, leading=10)


def _summary_table(summary: dict) -> Table:
    rows = [["Metric", "Value"]]
    for k, v in summary.items():
        rows.append([k, str(v)])
    t = Table(rows, colWidths=[3 * inch, 3 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
            ]
        )
    )
    return t


def _benford_table(benford: dict) -> Table:
    rows = [["Digit", "Observed %", "Expected %", "Diff"]]
    for d in benford.get("per_digit", []):
        rows.append([str(d["digit"]), f"{d['observed_pct']}%", f"{d['expected_pct']}%", f"{d['diff_pct']:+.2f}"])
    t = Table(rows, colWidths=[1 * inch, 1.5 * inch, 1.5 * inch, 1 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
            ]
        )
    )
    return t


def _flagged_table(flagged: list[dict]) -> Table:
    rows = [["Risk", "Amount", "Date", "Description", "Reasons"]]
    for f in flagged[:50]:
        reasons = "; ".join(f.get("reasons", []))[:180]
        rows.append(
            [
                f"{f['risk_score']:.0f}",
                f"{f['amount']:.2f}",
                f.get("date", "-") or "-",
                (f.get("description", "-") or "-")[:30],
                Paragraph(reasons, SMALL),
            ]
        )
    t = Table(rows, colWidths=[0.5 * inch, 0.8 * inch, 0.8 * inch, 1.4 * inch, 2.8 * inch])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7f1d1d")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fef2f2")]),
            ]
        )
    )
    return t


def generate_pdf_report(
    filename: str,
    summary: dict,
    benford: dict,
    flagged: list[dict],
) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=0.6 * inch, bottomMargin=0.6 * inch)
    story = []

    story.append(Paragraph("AuditTrace AI — Financial Statement Anomaly Report", TITLE_STYLE))
    story.append(Paragraph(f"Source file: {filename}", BODY))
    story.append(Paragraph(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", BODY))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Summary", H2))
    story.append(_summary_table(summary))

    story.append(Paragraph("Benford's Law Analysis", H2))
    if benford.get("applicable"):
        story.append(Paragraph(benford["summary"], BODY))
        story.append(Spacer(1, 0.1 * inch))
        story.append(_benford_table(benford))
    else:
        story.append(Paragraph(benford.get("reason", "Not applicable."), BODY))

    story.append(PageBreak())
    story.append(Paragraph(f"Flagged Transactions (top {min(len(flagged), 50)} by risk score)", H2))
    if flagged:
        story.append(_flagged_table(flagged))
    else:
        story.append(Paragraph("No transactions were flagged.", BODY))

    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph(
            "Methodology: anomaly risk scores come from an unsupervised Isolation Forest model over "
            "engineered transaction features; per-transaction reasons are derived from a SHAP-explained "
            "surrogate classifier trained on the isolation forest's flags, combined with Benford's Law, "
            "duplicate-posting, and round-number heuristics. This report is a screening tool, not a "
            "conclusive fraud determination — findings should be reviewed by a qualified professional.",
            SMALL,
        )
    )

    doc.build(story)
    return buf.getvalue()
