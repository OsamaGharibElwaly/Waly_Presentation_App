"""ReportLab PDF export engine."""
import re
import textwrap
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from backend.agents.base.agent import AgentContext

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

    def _write(self, c, value, x, y, width, size, color, bold=False, leading=1.25):
        c.setFillColor(HexColor(color))
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        lines = textwrap.wrap(str(value), width=max(8, int(width / (size * 0.52)))) or [""]
        for line in lines:
            c.drawString(x, y, line[:120])
            y -= size * leading
        return y - 6

    def _legacy_page(self, c, spec, w, h, card, accent, highlight, fg) -> None:
        self._image(c, getattr(spec, "image_path", ""), w - 2.2 * inch,
                    h - 1.2 * inch, 1.8 * inch, 1.01 * inch, card, accent)
        self._write(c, spec.title, 0.75 * inch, h - 1.2 * inch, 9.5 * inch, 26, fg, True)
        y = h - 2.0 * inch
        for bullet in spec.bullets[:6]:
            y = self._write(c, bullet, 1.0 * inch, y, 9.5 * inch, 15, fg)
            if y < 0.9 * inch:
                break

    def _v4_page(self, c, spec, w, h, placement, path, card, accent, highlight, fg) -> None:
        bullets = list(spec.bullets)[:4]
        if placement == "hero_banner":
            self._image(c, path, 0, h * 0.42, w, h * 0.58, card, accent)
            self._panel(c, 0, 0, w, h * 0.42, card, accent)
            y = self._write(c, spec.title, 0.7 * inch, h * 0.42 - 0.45 * inch,
                            w - 1.4 * inch, 36, fg, True)
        elif placement == "full_bleed_glass":
            self._image(c, path, 0, 0, w, h, card, accent)
            self._panel(c, 0.85 * inch, 0.85 * inch, w * 0.62, h * 0.78, card, accent)
            y = self._write(c, spec.title, 1.2 * inch, h * 0.78, w * 0.55, 44, fg, True)
        elif placement == "giant_stat_split":
            self._image(c, path, w * 0.55, 0, w * 0.45, h, card, accent)
            self._panel(c, 0, 0, w * 0.55, h, card, accent)
            match = METRIC_RE.search(" ".join(bullets) or spec.title)
            hero = match.group(0).strip() if match else spec.title[:10]
            y = self._write(c, hero, 0.6 * inch, h - 1.0 * inch, w * 0.48, 76, highlight, True)
            y = self._write(c, spec.title, 0.65 * inch, y, w * 0.48, 20, fg, True)
            bullets = bullets[:3]
        else:
            right = placement == "split_right"
            self._image(c, path, w * 0.5 if right else 0, 0, w * 0.5, h, card, accent)
            self._panel(c, 0 if right else w * 0.5, 0, w * 0.5, h, card, accent)
            x = 0.65 * inch if right else w * 0.5 + 0.65 * inch
            y = self._write(c, spec.title, x, h - 0.95 * inch, w * 0.4, 40, fg, True)
        for bullet in bullets:
            y = self._write(c, bullet, x if placement in ("split_right", "split_left")
                            else (0.65 * inch if placement == "giant_stat_split" else 0.7 * inch),
                            y, w * 0.42 if placement.startswith("split") else w * 0.85,
                            18 if placement.startswith("split") else 17, fg)
            if y < 0.8 * inch:
                break
