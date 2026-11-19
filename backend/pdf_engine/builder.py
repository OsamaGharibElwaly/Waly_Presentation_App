"""ReportLab PDF export engine."""
import re
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from backend.agents.base.agent import AgentContext
from backend.layout.geometry import fit_size, layout_zones

V4_PLACEMENTS = ("split_right", "split_left", "giant_stat_split", "hero_banner", "full_bleed_glass")
DEFAULTS = ("#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC")
METRIC_RE = re.compile(r"[$€£]?\s?\d+(?:\.\d+)?\s?(?:%|x\b|days\b|hours\b|points\b|slides\b)?", re.I)


def _luminance(value: str) -> float:
    text = value.lstrip("#")
    if len(text) == 3:
        text = "".join(char * 2 for char in text)
    channels = [int(text[index:index + 2], 16) / 255 for index in (0, 2, 4)]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def _readable(background: str, preferred: str) -> str:
    if abs(_luminance(background) - _luminance(preferred)) >= 0.35:
        return preferred
    return "#FFFFFF" if _luminance(background) < 0.5 else "#0B1220"


class PdfBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx

    def build(self, slides, target: Path) -> None:
        target.parent.mkdir(parents=True, exist_ok=True)
        c = Canvas(str(target), pagesize=landscape(letter))
        w, h = landscape(letter)
        colors = [str(color) for color in (self.ctx.palette.get("colors") or DEFAULTS)]
        while len(colors) < 5:
            colors.append(DEFAULTS[len(colors)])
        bg, card, accent, highlight, fg = colors[:5]
        fg = _readable(card, fg)
        for spec in slides:
            c.setFillColor(HexColor(bg))
            c.rect(0, 0, w, h, fill=1, stroke=0)
            visual = getattr(spec, "visual_spec", None)
            placement = visual.placement if visual else ""
            if placement in V4_PLACEMENTS:
                self._v4_page(c, spec, w, h, placement, getattr(spec, "image_path", ""),
                              card, accent, highlight, fg)
            else:
                self._legacy_page(c, spec, w, h, card, accent, highlight, fg)
            c.showPage()
        c.save()

    def _image(self, c, path, x, y_bottom, width, height, card, accent) -> None:
        try:
            if path and Path(path).exists():
                c.drawImage(str(path), x, y_bottom, width, height)
                return
        except (OSError, ValueError):
            pass
        c.setFillColor(HexColor(card))
        c.setStrokeColor(HexColor(accent))
        c.rect(x, y_bottom, width, height, fill=1, stroke=1)

    def _panel(self, c, x, y_bottom, width, height, card, accent) -> None:
        c.setFillColor(HexColor(card))
        c.setStrokeColor(HexColor(accent))
        c.rect(x, y_bottom, width, height, fill=1, stroke=1)

    def _write(self, c, value, x, y_top, width, height, size, color, bold=False, minimum=13):
        fitted, lines = fit_size(str(value), width / inch, height / inch, size, minimum)
        c.setFillColor(HexColor(color))
        c.setFont("Helvetica-Bold" if bold else "Helvetica", fitted)
        cursor = y_top
        for line in lines:
            c.drawString(x, cursor, line[:120])
            cursor -= fitted * 1.25
        return cursor

    def _legacy_page(self, c, spec, w, h, card, accent, highlight, fg) -> None:
        self._image(c, getattr(spec, "image_path", ""), w - 2.2 * inch,
                    h - 1.2 * inch, 1.8 * inch, 1.01 * inch, card, accent)
        y = self._write(c, spec.title, 0.75 * inch, h - 1.2 * inch, 9.5 * inch,
                        0.6 * inch, 26, fg, True)
        for bullet in spec.bullets[:6]:
            y = self._write(c, bullet, 1.0 * inch, y, 9.5 * inch, 0.45 * inch, 15, fg)
            if y < 0.9 * inch:
                break

    def _v4_page(self, c, spec, w, h, placement, path, card, accent, highlight, fg) -> None:
        zones = layout_zones(placement)
        image, content, footer = zones["image"], zones["content"], zones["footer"]
        self._image(c, path, image[0] * inch, h - (image[1] + image[3]) * inch,
                    image[2] * inch, image[3] * inch, card, accent)
        if placement == "hero_banner":
            self._panel(c, 0, 0, w, h * 0.42, card, accent)
        elif placement == "full_bleed_glass":
            self._panel(c, 0.85 * inch, 0.85 * inch, w * 0.62, h * 0.78, card, accent)
        elif placement == "giant_stat_split":
            self._panel(c, 0, 0, image[0] * inch, h, card, accent)
        else:
            panel_x = 0 if placement == "split_right" else image[0] * inch
            self._panel(c, panel_x, 0, image[2] * inch, h, card, accent)

        structured = [block for block in getattr(spec, "blocks", [])
                      if block.kind in ("table", "steps")]
        reserved = 1.05 if structured else 0.0
        bottom_in = footer[1] - 0.15 - reserved
        x = content[0] * inch
        width = content[2] * inch
        top = h - content[1] * inch
        title_size = 76 if placement == "giant_stat_split" else (44 if placement == "full_bleed_glass" else 38)
        title = spec.title
        if placement == "giant_stat_split":
            match = METRIC_RE.search(" ".join(spec.bullets) or spec.title)
            title = match.group(0).strip() if match else spec.title[:10]
        y = self._write(c, title, x, top, width, min(1.6 * inch, (bottom_in - content[1]) * inch),
                        title_size, highlight if placement == "giant_stat_split" else fg, True,
                        minimum=28 if placement == "giant_stat_split" else 26)
        if placement == "giant_stat_split":
            y = self._write(c, spec.title, x, y, width, 0.7 * inch, 20, fg, True)
        bullets = list(spec.bullets)[:3 if placement == "giant_stat_split" else 4]
        for bullet in bullets:
            capacity_in = max(0.25, bottom_in - (h - y) / inch)
            y = self._write(c, bullet, x, y, width, min(0.55 * inch, capacity_in * inch),
                            17, fg)
            if y < footer[1] * inch:
                break
        if structured:
            block_top = (footer[1] - reserved) * inch
            for block in structured[:2]:
                height = 0.4 * inch
                self._panel(c, x, block_top - height, width, height, card,
                            accent if block.kind == "table" else highlight)
                self._write(c, block.text, x + 0.1 * inch, block_top - 0.04 * inch,
                            width - 0.2 * inch, height - 0.08 * inch, 13, fg, minimum=11)
                block_top -= height + 0.08 * inch
