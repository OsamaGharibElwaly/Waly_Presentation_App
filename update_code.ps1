# ============================================================
# update_code.ps1 - Complete code update for backend & frontend
# Run from PowerShell: .\update_code.ps1
# ============================================================
$ErrorActionPreference = "Stop"
$Root = "H:\devH\offlinepresentationapp\OfflineAIPresentationFactory"

function New-File($p, $content) {
    $dir = Split-Path $p -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    Set-Content -Path $p -Value $content -Encoding UTF8
    Write-Host "  [file created/updated] $p" -ForegroundColor Green
}

Write-Host "`n=== Overhauling Project Files (Backend & Frontend) ===" -ForegroundColor Cyan

# 1. backend/agents/base/agent.py
New-File "$Root/backend/agents/base/agent.py" @'
"""Base agent definitions and data structures."""
from dataclasses import dataclass, field

@dataclass
class AgentContext:
    theme: dict = field(default_factory=dict)
    palette: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

@dataclass
class SlideSpec:
    title: str
    bullets: list[str]
    notes: str = ""

class BaseAgent:
    def __init__(self, ctx: AgentContext | None = None) -> None:
        self.ctx = ctx or AgentContext()

    def run(self, content: str):
        raise NotImplementedError
'@

# 2. backend/agents/factory/agent_factory.py
New-File "$Root/backend/agents/factory/agent_factory.py" @'
"""AgentFactory with auto-registration and crash-proof fallback."""
from typing import Dict, Type
from backend.agents.base.agent import BaseAgent, AgentContext

_REGISTRY: Dict[str, Type[BaseAgent]] = {}

class AgentFactory:
    @classmethod
    def register(cls, name: str):
        def decorator(subclass: Type[BaseAgent]):
            _REGISTRY[name] = subclass
            return subclass
        return decorator

    @classmethod
    def create(cls, name: str, ctx: AgentContext | None = None) -> BaseAgent:
        if name not in _REGISTRY:
            cls._auto_register()
        
        if name not in _REGISTRY:
            class SafeFallbackAgent(BaseAgent):
                def run(self, text: str):
                    from backend.agents.base.agent import SlideSpec
                    return [SlideSpec(title="Presentation Slide", bullets=[text[:120]], notes="Fallback generated.")]
            return SafeFallbackAgent(ctx)
            
        return _REGISTRY[name](ctx)

    @classmethod
    def _auto_register(cls) -> None:
        try:
            from backend.agents.markdown_manipulator import MarkdownManipulatorAgent
            _REGISTRY["markdown_manipulator"] = MarkdownManipulatorAgent
        except Exception:
            pass
'@

# 3. backend/agents/markdown_manipulator.py
New-File "$Root/backend/agents/markdown_manipulator.py" @'
"""Markdown Manipulator Agent - parses input text into structured SlideSpecs."""
from backend.agents.base.agent import BaseAgent, SlideSpec
from backend.agents.factory.agent_factory import AgentFactory

@AgentFactory.register("markdown_manipulator")
class MarkdownManipulatorAgent(BaseAgent):
    def run(self, text: str) -> list[SlideSpec]:
        slides = []
        current_title = "Overview"
        current_bullets = []
        current_notes = ""

        for line in text.splitlines():
            line_s = line.strip()
            if line_s.startswith("# "):
                continue
            elif line_s.startswith("## "):
                if current_bullets or current_title != "Overview":
                    slides.append(SlideSpec(title=current_title, bullets=current_bullets, notes=current_notes.strip()))
                current_title = line_s[3:].strip()
                current_bullets = []
                current_notes = ""
            elif line_s.startswith("- ") or line_s.startswith("* "):
                current_bullets.append(line_s[2:].strip())
            elif line_s.startswith(">"):
                current_notes += line_s.lstrip("> ").strip() + " "

        if current_bullets or current_title:
            slides.append(SlideSpec(title=current_title, bullets=current_bullets, notes=current_notes.strip()))

        return slides if slides else [SlideSpec(title="Presentation", bullets=[text[:100]], notes="")]
'@

# 4. backend/pptx_engine/builder.py
New-File "$Root/backend/pptx_engine/builder.py" @'
"""python-pptx presentation generation engine."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from backend.agents.base.agent import AgentContext

def _hex(c: str) -> RGBColor:
    c = c.lstrip("#")
    return RGBColor(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

class PptxBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self.colors = ctx.palette.get("colors") or ["#FFFFFF", "#1E293B", "#38BDF8"]

    def build(self, slides, target: Path) -> None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        # Title Slide
        title_slide = prs.slides.add_slide(prs.slide_layouts[0])
        deck_title = self.ctx.meta.get("deck_title", self.ctx.theme.get("name", "Presentation"))
        title_slide.shapes.title.text = deck_title
        title_slide.placeholders[1].text = (
            f"Industry Theme: {self.ctx.theme.get('industry', 'General')} — {self.ctx.theme.get('name', '')}\n"
            "Generated via Offline Agentic AI Factory"
        )

        # Content Slides
        for spec in slides:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = spec.title
            title_p = slide.shapes.title.text_frame.paragraphs[0]
            title_p.font.size = Pt(30)
            title_p.font.color.rgb = _hex(self.colors[1] if len(self.colors) > 1 else "#1E293B")

            body = slide.placeholders[1].text_frame
            if spec.bullets:
                body.text = spec.bullets[0]
                for b in spec.bullets[1:]:
                    p = body.add_paragraph()
                    p.text = b
                    p.font.size = Pt(18)

            if spec.notes:
                slide.notes_slide.notes_text_frame.text = spec.notes

        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))
'@

# 5. backend/pdf_engine/builder.py
New-File "$Root/backend/pdf_engine/builder.py" @'
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
                c.drawString(1.0 * inch, y, f"• {b[:100]}")
                y -= 0.45 * inch
                if y < 1.0 * inch:
                    break
            c.showPage()
        c.save()
'@

# 6. backend/pipeline/orchestrator.py
New-File "$Root/backend/pipeline/orchestrator.py" @'
"""Orchestrator coordinates agents and export builders."""
from pathlib import Path
from backend.agents.factory.agent_factory import AgentFactory
from backend.agents.base.agent import AgentContext
from backend.pptx_engine.builder import PptxBuilder
from backend.pdf_engine.builder import PdfBuilder

class Orchestrator:
    def __init__(self, theme: dict, palette: dict, meta: dict | None = None) -> None:
        self.ctx = AgentContext(theme=theme, palette=palette, meta=meta or {})
        self.md_agent = AgentFactory.create("markdown_manipulator", self.ctx)

    def run(self, markdown_text: str, target: Path) -> None:
        slides = self.md_agent.run(markdown_text)
        suffix = target.suffix.lower()
        if suffix == ".pptx":
            builder = PptxBuilder(self.ctx)
            builder.build(slides, target)
        elif suffix == ".pdf":
            builder = PdfBuilder(self.ctx)
            builder.build(slides, target)
        else:
            raise ValueError(f"Unsupported export format: {suffix}")
'@

# 7. frontend/theme_factory/registry.py
New-File "$Root/frontend/theme_factory/registry.py" @'
"""ThemeRegistry - loads palettes + industries from JSON catalogs using utf-8-sig."""
import json
from pathlib import Path

CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"

class ThemeRegistry:
    def __init__(self, catalog_dir: Path | None = None) -> None:
        self.dir = catalog_dir or CATALOG_DIR
        self._palettes = self._load("palettes.json")
        self._industries = self._load("industries.json")

    def _load(self, name: str) -> dict:
        path = self.dir / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8-sig"))
        return {}

    def palettes(self) -> list[dict]:
        return self._palettes.get("palettes", [])

    def palette_by_name(self, name: str) -> dict:
        for p in self.palettes():
            if p["name"] == name:
                return p
        return self.palettes()[0] if self.palettes() else {"name": "Default", "colors": []}
'@

# 8. frontend/theme_factory/catalog.py
New-File "$Root/frontend/theme_factory/catalog.py" @'
"""Static fallback for industries with utf-8-sig BOM support."""
from pathlib import Path
import json

_HERE = Path(__file__).resolve().parents[2]
_PATH = _HERE / "knowledge" / "catalog" / "industries.json"

INDUSTRIES = json.loads(_PATH.read_text(encoding="utf-8-sig")) if _PATH.exists() else {}
'@

Write-Host "`n=== All Files Updated Successfully! ===" -ForegroundColor Cyan
Write-Host "Run your application with: python -m frontend.main" -ForegroundColor Yellow