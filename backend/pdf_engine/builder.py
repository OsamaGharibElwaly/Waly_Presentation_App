"""ReportLab PDF export engine."""
from pathlib import Path
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from backend.agents.base.agent import AgentContext

class PdfBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx

    def build(self, slides, target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        c = Canvas(str(target), pagesize=landscape(letter))
        w, h = landscape(letter)

        for spec in slides:
            c.setFont("Helvetica-Bold", 26)
            c.drawString(0.75 * inch, h - 1.2 * inch, spec.title[:75])
            c.setFont("Helvetica", 15)
            y = h - 2.0 * inch
            for b in spec.bullets:
                c.drawString(1.0 * inch, y, f"â€¢ {b[:100]}")
                y -= 0.45 * inch
                if y < 1.0 * inch:
                    break
            c.showPage()
        c.save()
