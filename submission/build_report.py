"""Build the editable Markdown report as a polished two-page PDF."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "hangman_development_report.md"
OUTPUT = ROOT / "hangman_development_report.pdf"

INK = colors.HexColor("#17201d")
GREEN = colors.HexColor("#1c7258")
MUTED = colors.HexColor("#66706d")
PALE = colors.HexColor("#e2f2eb")
CORAL = colors.HexColor("#d96045")


def draw_page(canvas, document):
    width, height = letter
    canvas.saveState()
    canvas.setFillColor(GREEN)
    canvas.rect(0, height - 0.16 * inch, width, 0.16 * inch, fill=1, stroke=0)
    canvas.setStrokeColor(colors.HexColor("#dcd7cc"))
    canvas.line(0.58 * inch, 0.48 * inch, width - 0.58 * inch, 0.48 * inch)
    canvas.setFont("Helvetica", 7.4)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.58 * inch, 0.28 * inch, "CSE 4095 - Web-Based Hangman Development Report")
    canvas.drawRightString(width - 0.58 * inch, 0.28 * inch, f"Page {document.page}")
    canvas.restoreState()


def make_document():
    document = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.58 * inch,
        rightMargin=0.58 * inch,
        topMargin=0.48 * inch,
        bottomMargin=0.58 * inch,
        title="Building a Web-Based Hangman Game with Codex",
        author="CSE 4095 Student",
    )
    frame = Frame(
        document.leftMargin,
        document.bottomMargin,
        document.width,
        document.height,
        id="report-frame",
    )
    document.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=draw_page)])
    return document


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=23,
            leading=25,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=GREEN,
            alignment=TA_CENTER,
            spaceAfter=10,
        ),
        "heading": ParagraphStyle(
            "Heading",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.2,
            leading=13,
            textColor=GREEN,
            spaceBefore=6,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.35,
            leading=10.7,
            textColor=INK,
            spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.15,
            leading=10.2,
            leftIndent=12,
            firstLineIndent=-7,
            bulletIndent=0,
            textColor=INK,
            spaceAfter=2.2,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=7.85,
            leading=10,
            leftIndent=12,
            rightIndent=8,
            borderColor=GREEN,
            borderWidth=0,
            borderPadding=(4, 7, 4, 8),
            backColor=PALE,
            textColor=INK,
            spaceBefore=2,
            spaceAfter=4,
        ),
    }


def inline_markup(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    while "`" in text:
        start = text.find("`")
        end = text.find("`", start + 1)
        if end == -1:
            break
        code = text[start + 1 : end]
        text = text[:start] + f'<font name="Courier" size="7.5">{code}</font>' + text[end + 1 :]
    while "**" in text:
        start = text.find("**")
        end = text.find("**", start + 2)
        if end == -1:
            break
        bold = text[start + 2 : end]
        text = text[:start] + f"<b>{bold}</b>" + text[end + 2 :]
    return text


def build_story(markdown):
    report_styles = styles()
    story = []
    paragraph_lines = []

    def flush_paragraph():
        if paragraph_lines:
            text = " ".join(paragraph_lines).strip()
            story.append(Paragraph(inline_markup(text), report_styles["body"]))
            paragraph_lines.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line == "\\pagebreak":
            flush_paragraph()
            story.append(PageBreak())
        elif line.startswith("# "):
            flush_paragraph()
            story.append(Spacer(1, 4))
            story.append(Paragraph(inline_markup(line[2:]), report_styles["title"]))
        elif line.startswith("## "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[3:]), report_styles["heading"]))
        elif line.startswith("**") and line.endswith("**"):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line), report_styles["subtitle"]))
        elif line.startswith("- "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:]), report_styles["bullet"], bulletText="•"))
        elif line.startswith("> "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:]), report_styles["quote"]))
        elif not line:
            flush_paragraph()
        else:
            paragraph_lines.append(line)
    flush_paragraph()
    return story


if __name__ == "__main__":
    source_text = SOURCE.read_text(encoding="utf-8")
    document = make_document()
    document.build(build_story(source_text))
    print(OUTPUT)
