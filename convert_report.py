#!/usr/bin/env python3
"""Convert the most recent ai-hedge-fund JSON output (outputs/run_*.json) into a
polished PDF report with a cover page, saved to reports/latest/.

This is a standalone convenience script - it does not modify any project source.
"""

import json
import os
import platform
import subprocess
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports" / "latest"

AUTHOR = "Kevin Cheng"
POWERED_BY = "Powered by ai-hedge-fund"
TITLE = "Investment Research Report"


def find_latest_report():
    try:
        if not OUTPUTS_DIR.exists():
            print(f"[convert_report] No outputs directory found at {OUTPUTS_DIR}")
            return None
        candidates = sorted(
            OUTPUTS_DIR.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        return candidates[0] if candidates else None
    except Exception as exc:
        print(f"[convert_report] Failed to scan outputs directory: {exc}")
        return None


def load_report(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        print(f"[convert_report] Failed to read report {path}: {exc}")
        return None


def build_filename(data):
    try:
        decisions = data.get("decisions", {}) if isinstance(data, dict) else {}
        tickers = list(decisions.keys())
        if not tickers:
            ticker_part = "REPORT"
        elif len(tickers) <= 3:
            ticker_part = "-".join(tickers)
        else:
            ticker_part = f"{tickers[0]}-PLUS-{len(tickers) - 1}"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"{ticker_part}_{timestamp}.pdf"
    except Exception as exc:
        print(f"[convert_report] Failed to build filename, using fallback: {exc}")
        return f"REPORT_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"


def unique_path(path):
    """Never overwrite an existing file - append a counter suffix if needed."""
    if not path.exists():
        return path
    stem, suffix, parent = path.stem, path.suffix, path.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def render_pdf(data, source_path, output_path):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import LETTER
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
    cover_title_style = ParagraphStyle("CoverTitle", parent=styles["Title"], fontSize=28, alignment=1, spaceAfter=24)
    cover_sub_style = ParagraphStyle("CoverSub", parent=styles["Normal"], fontSize=14, alignment=1, spaceAfter=8)
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # Cover page
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph(TITLE, cover_title_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(AUTHOR, cover_sub_style))
    story.append(Paragraph(POWERED_BY, cover_sub_style))
    story.append(Paragraph(datetime.now().strftime("%B %d, %Y %H:%M"), cover_sub_style))
    story.append(Paragraph(f"Source: {source_path.name}", cover_sub_style))
    story.append(PageBreak())

    decisions = data.get("decisions", {}) if isinstance(data, dict) else {}
    analyst_signals = data.get("analyst_signals", {}) if isinstance(data, dict) else {}

    # Decisions summary
    story.append(Paragraph("Trading Decisions", heading_style))
    if decisions:
        table_data = [["Ticker", "Action", "Quantity", "Confidence"]]
        for ticker, decision in decisions.items():
            if not isinstance(decision, dict):
                continue
            table_data.append([
                ticker,
                str(decision.get("action", "")).upper(),
                str(decision.get("quantity", "")),
                f"{decision.get('confidence', '')}%",
            ])
        table = Table(table_data, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

        for ticker, decision in decisions.items():
            if not isinstance(decision, dict):
                continue
            reasoning = decision.get("reasoning", "")
            if reasoning:
                story.append(Paragraph(f"<b>{ticker} reasoning:</b>", body_style))
                story.append(Paragraph(str(reasoning).replace("\n", "<br/>"), body_style))
                story.append(Spacer(1, 0.15 * inch))
    else:
        story.append(Paragraph("No trading decisions found in this report.", body_style))

    # Analyst signals
    if analyst_signals:
        story.append(PageBreak())
        story.append(Paragraph("Analyst Signals", heading_style))
        for agent, signals in analyst_signals.items():
            if not isinstance(signals, dict):
                continue
            story.append(Paragraph(f"<b>{agent}</b>", body_style))
            for ticker, signal in signals.items():
                if not isinstance(signal, dict):
                    continue
                story.append(Paragraph(f"{ticker}: {signal.get('signal', '')} ({signal.get('confidence', '')}%)", body_style))
                reasoning = signal.get("reasoning", "")
                if reasoning:
                    story.append(Paragraph(str(reasoning).replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 0.15 * inch))

    doc = SimpleDocTemplate(str(output_path), pagesize=LETTER, topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    doc.build(story)


def open_with_browser(path):
    try:
        system = platform.system()
        if system == "Windows":
            edge_candidates = [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            ]
            for edge in edge_candidates:
                if os.path.exists(edge):
                    subprocess.Popen([edge, str(path)])
                    return
            os.startfile(str(path))  # fall back to the OS default handler
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", "Microsoft Edge", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except Exception as exc:
        print(f"[convert_report] Could not auto-open the PDF ({exc}). Open it manually: {path}")


def main():
    try:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        print(f"[convert_report] Could not create reports directory: {exc}")
        return

    latest = find_latest_report()
    if latest is None:
        print("[convert_report] No saved report found in outputs/. Run an analysis and save it first.")
        return

    data = load_report(latest)
    if data is None:
        return

    try:
        import reportlab  # noqa: F401
    except ImportError:
        print("[convert_report] reportlab is not installed. Run: pip install reportlab")
        return

    output_path = unique_path(REPORTS_DIR / build_filename(data))

    try:
        render_pdf(data, latest, output_path)
        print(f"[convert_report] Saved PDF report to {output_path}")
    except Exception as exc:
        print(f"[convert_report] Failed to generate PDF: {exc}")
        return

    open_with_browser(output_path)


if __name__ == "__main__":
    main()
