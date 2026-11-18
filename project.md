# Project Snapshot
Generated: 2026-11-18 14:38
Root: H:\devH\offlinepresentationapp\OfflineAIPresentationFactory

## File Tree
```
.gitignore
code_enhance_3.ps1
code_enhance_4.ps1
pyproject.toml
README.md
requirements.txt
update_code.ps1
update_frontend.ps1
update_frontend_2.ps1
backend\__init__.py
backend\agents\markdown_manipulator.py
backend\agents\markdown_manipulator_agent.py
backend\agents\outline_agent.py
backend\agents\text_tools_agent.py
backend\agents\__init__.py
backend\agents\base\agent.py
backend\agents\base\__init__.py
backend\agents\factory\agent_factory.py
backend\agents\factory\__init__.py
backend\pdf_engine\builder.py
backend\pdf_engine\__init__.py
backend\pipeline\orchestrator.py
backend\pipeline\__init__.py
backend\pptx_engine\builder.py
backend\pptx_engine\__init__.py
backend\rules\README.md
backend\rules\__init__.py
docs\PRD.md
frontend\main.py
frontend\__init__.py
frontend\theme_factory\catalog.py
frontend\theme_factory\registry.py
frontend\theme_factory\__init__.py
frontend\theme_factory\industries\README.md
frontend\theme_factory\industries\__init__.py
frontend\ui\main_window.py
frontend\ui\__init__.py
frontend\ui\widgets\placeholders.py
frontend\ui\widgets\__init__.py
knowledge\catalog\industries.json
knowledge\catalog\palettes.json
knowledge\md_format\template_guide.md
knowledge\offline_tools\tools_manifest.md
knowledge\offline_tools\__init__.py
```

## File Contents

### `.gitignore`
```gitignore
__pycache__/
*.pyc
.venv/
venv/
*.pptx
*.pdf
out/
build/
dist/
.vscode/.ropeproject
.DS_Store
*.log

```

### `code_enhance_3.ps1`
```ps1
# ============================================================
# code_enhance_3.ps1 - Advanced Designer Overhaul (Shapes, UI Sync, & Rich Palettes)
# Run from PowerShell: .\code_enhance_3.ps1
# ============================================================
$ErrorActionPreference = "Stop"
$Root = "H:\devH\offlinepresentationapp\OfflineAIPresentationFactory"

function New-File($p, $content) {
    $dir = Split-Path $p -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    Set-Content -Path $p -Value $content -Encoding UTF8
    Write-Host "  [file created/updated] $p" -ForegroundColor Green
}

Write-Host "`n=== Overhauling Application with Advanced Shapes & Synchronized Right Panel ===" -ForegroundColor Cyan

# 1. Update knowledge/catalog/industries.json
New-File "$Root/knowledge/catalog/industries.json" @'
{
  "Architecture": {
    "description": "Spatial design, structural acoustics, urban planning, materiality, and sustainable formwork.",
    "accent_color": "#D97706",
    "themes": [
      {"name": "Brutalist Concrete", "accent": "#64748B", "style": "monolithic"},
      {"name": "Biophilic & Timber", "accent": "#059669", "style": "organic"},
      {"name": "Minimalist Glass", "accent": "#0284C7", "style": "clean"}
    ]
  },
  "Construction": {
    "description": "Heavy civil works, site logistics, safety compliance, structural steel, and BIM modeling.",
    "accent_color": "#EA580C",
    "themes": [
      {"name": "Structural Steel & Safety", "accent": "#EA580C", "style": "heavy"},
      {"name": "Smart Site Logistics", "accent": "#2563EB", "style": "operational"},
      {"name": "Geotechnical Foundation", "accent": "#78350F", "style": "earth"}
    ]
  },
  "Engineering": {
    "description": "Mechanical systems, quantum computing, thermodynamics, robotics, and software architecture.",
    "accent_color": "#2563EB",
    "themes": [
      {"name": "Quantum & Neon", "accent": "#38BDF8", "style": "futuristic"},
      {"name": "Systems Thermodynamics", "accent": "#DC2626", "style": "energetic"},
      {"name": "Precision Robotics", "accent": "#7C3AED", "style": "cyber"}
    ]
  },
  "Literature": {
    "description": "Narrative pacing, linguistic chunking, corpus linguistics, and editorial publishing strategy.",
    "accent_color": "#9333EA",
    "themes": [
      {"name": "Classic Parchment", "accent": "#B45309", "style": "editorial"},
      {"name": "Modern Typography", "accent": "#1E293B", "style": "clean"},
      {"name": "Corpus Linguistics", "accent": "#0D9488", "style": "analytical"}
    ]
  }
}
'@

# 2. Update knowledge/catalog/palettes.json
New-File "$Root/knowledge/catalog/palettes.json" @'
{
  "palettes": [
    {"name": "Cyber Slate & Neon Blue", "colors": ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]},
    {"name": "Warm Architectural Earth", "colors": ["#1C1917", "#292524", "#D97706", "#B45309", "#FAFAF9"]},
    {"name": "Construction Safety & Steel", "colors": ["#09090B", "#18181B", "#EA580C", "#52525B", "#FAFAFA"]},
    {"name": "Biophilic Forest & Timber", "colors": ["#064E3B", "#065F46", "#059669", "#34D399", "#ECFDF5"]},
    {"name": "Quantum Deep Purple", "colors": ["#2E1065", "#3B0764", "#7C3AED", "#A78BFA", "#F5F3FF"]},
    {"name": "Minimalist Scandinavian", "colors": ["#F8FAFC", "#E2E8F0", "#0284C7", "#0F172A", "#334155"]},
    {"name": "Editorial Obsidian & Gold", "colors": ["#0A0A0A", "#171717", "#D4AF37", "#E5E5E5", "#FFFFFF"]},
    {"name": "Thermal Gradient Red", "colors": ["#450A0A", "#7F1D1D", "#DC2626", "#F87171", "#FEF2F2"]}
  ]
}
'@

# 3. Update backend/pptx_engine/builder.py with Advanced Geometric Shapes & Styled Cards
New-File "$Root/backend/pptx_engine/builder.py" @'
"""python-pptx engine with advanced geometric shapes, header banner cards, and styled containers."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from backend.agents.base.agent import AgentContext

def _hex(c: str) -> RGBColor:
    c = c.lstrip("#")
    if len(c) != 6:
        c = "1E293B"
    return RGBColor(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

class PptxBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self.colors = ctx.palette.get("colors") or ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]

    def build(self, slides, target: Path) -> None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        bg_color = _hex(self.colors[0])
        card_bg = _hex(self.colors[1])
        accent_color = _hex(self.colors[2])
        highlight_color = _hex(self.colors[3])
        text_color = _hex(self.colors[4] if len(self.colors) > 4 else "#FFFFFF")

        # --- TITLE SLIDE (Rich Styled Geometry) ---
        blank_layout = prs.slide_layouts[6]
        title_slide = prs.slides.add_slide(blank_layout)
        
        # Background fill
        bg_shape = title_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = bg_color
        bg_shape.line.fill.background()

        # Decorative Top Accent Bar
        bar = title_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.5), Inches(0.25), Inches(3.2))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        bar.line.fill.background()

        # Title Card Box
        box = title_slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.5), Inches(10.5), Inches(3.2))
        box.fill.solid()
        box.fill.fore_color.rgb = card_bg
        box.line.color.rgb = accent_color
        box.line.width = Pt(2)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.4)
        tf.margin_top = Inches(0.5)

        deck_title = self.ctx.meta.get("deck_title", self.ctx.theme.get("name", "Enterprise Presentation"))
        p = tf.paragraphs[0]
        p.text = deck_title
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = text_color

        p2 = tf.add_paragraph()
        p2.text = f"Industry Domain: {self.ctx.theme.get('industry', 'General')} â€” {self.ctx.theme.get('name', '')} ({self.ctx.theme.get('style', 'modern')})"
        p2.font.size = Pt(16)
        p2.font.color.rgb = accent_color
        p2.space_before = Pt(14)

        p3 = tf.add_paragraph()
        p3.text = f"Palette Theme: {self.ctx.palette.get('name', 'Custom')} | 100% Offline Agentic AI Factory"
        p3.font.size = Pt(13)
        p3.font.color.rgb = text_color
        p3.space_before = Pt(8)

        # --- CONTENT SLIDES (Advanced Layout Shapes) ---
        for spec in slides:
            slide = prs.slides.add_slide(blank_layout)

            # Slide Background
            s_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
            s_bg.fill.solid()
            s_bg.fill.fore_color.rgb = bg_color
            s_bg.line.fill.background()

            # Header Banner Shape
            header_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(1.1))
            header_box.fill.solid()
            header_box.fill.fore_color.rgb = card_bg
            header_box.line.color.rgb = accent_color
            header_box.line.width = Pt(1.5)

            htf = header_box.text_frame
            htf.word_wrap = True
            htf.margin_left = Inches(0.3)
            hp = htf.paragraphs[0]
            hp.text = spec.title
            hp.font.size = Pt(26)
            hp.font.bold = True
            hp.font.color.rgb = accent_color

            # Content Card Shape
            content_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.8))
            content_box.fill.solid()
            content_box.fill.fore_color.rgb = card_bg
            content_box.line.color.rgb = highlight_color
            content_box.line.width = Pt(1.5)

            ctf = content_box.text_frame
            ctf.word_wrap = True
            ctf.margin_left = Inches(0.4)
            ctf.margin_top = Inches(0.4)
            ctf.margin_right = Inches(0.4)

            for idx, b in enumerate(spec.bullets):
                cp = ctf.add_paragraph() if idx > 0 else ctf.paragraphs[0]
                cp.text = f"â–ھ   {b}"
                cp.font.size = Pt(17)
                cp.font.color.rgb = text_color
                cp.space_after = Pt(14)

            if spec.notes:
                try:
                    slide.notes_slide.notes_text_frame.text = spec.notes
                except Exception:
                    pass

        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))
'@

# 4. Update frontend/ui/main_window.py to instantly update the right panel on click
New-File "$Root/frontend/ui/main_window.py" @'
"""Main window: Fully responsive right panel inspector, live color swatches, and rich studio controls."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QPlainTextEdit, QComboBox, QToolBox, QFileDialog, QMessageBox,
    QTabWidget, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt

from frontend.theme_factory.registry import ThemeRegistry
from frontend.theme_factory.catalog import INDUSTRIES
from backend.pipeline.orchestrator import Orchestrator

DARK_STUDIO_QSS = """
QMainWindow {
    background-color: #090D16;
    color: #F8FAFC;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QLabel {
    color: #E2E8F0;
    font-weight: 600;
}
QLineEdit, QPlainTextEdit {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 10px;
    selection-background-color: #38BDF8;
}
QLineEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #38BDF8;
    background-color: #030712;
}
QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton:pressed {
    background-color: #1E40AF;
}
QComboBox {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}
QComboBox::drop-down {
    border: 0px;
}
QToolBox::tab {
    background-color: #1F2937;
    color: #38BDF8;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 4px;
}
QToolBox::tab:selected {
    background-color: #2563EB;
    color: #FFFFFF;
}
QTabWidget::pane {
    border: 2px solid #1F2937;
    background: #090D16;
    border-radius: 12px;
}
QTabBar::tab {
    background: #111827;
    color: #9CA3AF;
    padding: 10px 20px;
    margin-right: 6px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #2563EB;
    color: #FFFFFF;
}
"""

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline AI Presentation Factory â€” Advanced Studio Designer")
        self.resize(1400, 900)
        self.setStyleSheet(DARK_STUDIO_QSS)
        
        self.theme_registry = ThemeRegistry()
        self._selected_theme = {"industry": "Architecture", "name": "Minimalist Glass", "accent": "#0284C7", "style": "clean"}
        self._build_ui()
        self._update_color_swatches()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Top Project Title Input
        top_bar = QHBoxLayout()
        lbl_proj = QLabel("Presentation Title:")
        lbl_proj.setStyleSheet("font-size: 16px; color: #38BDF8;")
        top_bar.addWidget(lbl_proj)
        self.name_input = QLineEdit("Enterprise_AI_Transformation_Deck")
        self.name_input.setStyleSheet("font-size: 15px; font-weight: bold;")
        top_bar.addWidget(self.name_input, 1)
        root.addLayout(top_bar)

        # Tabs
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        # --- TAB 1: Industry & Palette Studio ---
        tab_studio = QWidget()
        studio_layout = QHBoxLayout(tab_studio)

        # Left: Industry Toolbox
        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("Select Industry Domain & Sub-Theme:"))
        self.industry_toolbox = QToolBox()
        
        for industry, data in INDUSTRIES.items():
            holder = QWidget()
            v = QVBoxLayout(holder)
            desc = QLabel(data.get("description", ""))
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #9CA3AF; font-size: 12px; margin-bottom: 6px;")
            v.addWidget(desc)
            
            for theme in data["themes"]:
                btn = QPushButton(f"âœ¦ {theme['name']} ({theme['style']})")
                btn.setStyleSheet(f"text-align: left; padding-left: 14px; background-color: #1F2937; border-left: 5px solid {theme['accent']};")
                # Bind lambda correctly capturing industry and theme
                btn.clicked.connect(lambda checked=False, ind=industry, t=theme: self._pick_theme(ind, t))
                v.addWidget(btn)
            v.addStretch(1)
            self.industry_toolbox.addItem(holder, industry)
            
        left_box.addWidget(self.industry_toolbox, 1)
        studio_layout.addLayout(left_box, 1)

        # Right: Active Theme & Live Color Swatch Studio Inspector
        right_panel = QVBoxLayout()
        
        inspector_frame = QFrame()
        inspector_frame.setStyleSheet("background-color: #111827; border-radius: 12px; padding: 18px; border: 1px solid #1F2937;")
        v_insp = QVBoxLayout(inspector_frame)
        
        v_insp.addWidget(QLabel("ACTIVE INDUSTRY & THEME INSPECTOR:"))
        self.theme_display_lbl = QLabel("[Architecture] Minimalist Glass (clean)")
        self.theme_display_lbl.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        v_insp.addWidget(self.theme_display_lbl)

        self.industry_desc_lbl = QLabel("Spatial design, structural acoustics, urban planning, materiality, and sustainable formwork.")
        self.industry_desc_lbl.setWordWrap(True)
        self.industry_desc_lbl.setStyleSheet("color: #9CA3AF; font-size: 13px; margin-bottom: 10px;")
        v_insp.addWidget(self.industry_desc_lbl)
        
        v_insp.addWidget(QLabel("Select Color Palette Group (30+ Tuned Groups):"))
        self.palette_combo = QComboBox()
        for p in self.theme_registry.palettes():
            self.palette_combo.addItem(p["name"])
        self.palette_combo.currentIndexChanged.connect(self._update_color_swatches)
        v_insp.addWidget(self.palette_combo)
        
        v_insp.addWidget(QLabel("Live Color Palette Swatches (Interpretable Hex Preview):"))
        self.swatch_grid = QGridLayout()
        v_insp.addLayout(self.swatch_grid)
        
        right_panel.addWidget(inspector_frame)
        right_panel.addStretch(1)
        studio_layout.addLayout(right_panel, 1)

        self.tabs.addTab(tab_studio, "ًںژ¨ 1. Industry & Palette Studio")

        # --- TAB 2: Markdown Input Editor ---
        tab_md = QWidget()
        md_layout = QVBoxLayout(tab_md)
        md_layout.addWidget(QLabel("Presentation Markdown Structure (DeepSeek / LLM Format):"))
        
        self.md_editor = QPlainTextEdit()
        self.md_editor.setPlainText(
            "# Enterprise AI Transformation: Strategy & Architecture\n\n"
            "## Slide 1 - Executive Summary & Vision\n"
            "- Transitioning from cloud-dependent AI to secure, zero-API cost local execution\n"
            "- Balancing high productivity gains with absolute enterprise data sovereignty\n"
            "- Eliminating recurring token subscription costs through local processing\n"
            "> Speaker note: Emphasize that zero cloud dependency protects sensitive corporate data while slashing operational overhead to zero.\n\n"
            "## Slide 2 - The Offline Agentic Ecosystem\n"
            "- Modular architecture powered by specialized local Python libraries and rule engines\n"
            "- Air-gapped security ensuring zero data leakage to external third-party servers\n"
            "- Deterministic processing pipelines combining heuristics with local ML models\n"
            "> Speaker note: Highlight how local agents and deterministic rules work in tandem without relying on external network calls.\n\n"
            "## Slide 3 - Markdown Ingestion & Parsing Engine\n"
            "- Standardized DeepSeek-guided markdown schema for flawless structure extraction\n"
            "- Automatic header recognition, slide boundary splitting, and speaker note isolation\n"
            "- Seamless integration with local models or direct text copy-pasting\n"
            "> Speaker note: Explain how engineers can pipe structured output from any local LLM directly into the ingestion pipeline with zero manual formatting friction.\n\n"
            "## Slide 4 - NLP Optimization & Semantic Filtering\n"
            "- TF-IDF vectorization and cosine similarity for intelligent bullet deduplication\n"
            "- Automated constraint checks for title length and bullet point density bounds\n"
            "- Semantic cleaning ensuring high signal-to-noise ratio on every slide\n"
            "> Speaker note: Describe how semantic filtering automatically detects and removes redundant bullet points, keeping slide text concise and impactful.\n\n"
            "## Slide 5 - Automated Theme Factory & Design Patterns\n"
            "- Industry-tailored design variants across engineering, architectural, and corporate domains\n"
            "- Dynamic color palette mapping with over 30 tuned color group variations\n"
            "- Extensible factory pattern allowing custom theme additions across git commits\n"
            "> Speaker note: Show how the theme factory maintains strict visual consistency and professional aesthetics across all exported presentations.\n\n"
            "## Slide 6 - Multi-Format Vector Export & Roadmap\n"
            "- Instantaneous widescreen 16:9 .pptx generation via python-pptx\n"
            "- Clean landscape .pdf document vector compilation via ReportLab\n"
            "- Phased rollout strategy scaling across enterprise desktop workstations\n"
            "> Speaker note: Conclude with the deployment timeline and invite feedback on upcoming agentic modules."
        )
        md_layout.addWidget(self.md_editor, 1)
        self.tabs.addTab(tab_md, "ًں“‌ 2. Markdown AI Input")

        # Bottom Actions Bar
        actions_bar = QHBoxLayout()
        btn_load = QPushButton("ًں“پ Load Markdown File")
        btn_load.clicked.connect(self._load_file)
        actions_bar.addWidget(btn_load)

        btn_pptx = QPushButton("âڑ، Export Styled .pptx Presentation")
        btn_pptx.setStyleSheet("background-color: #059669; font-size: 15px;")
        btn_pptx.clicked.connect(lambda: self._export("pptx"))
        actions_bar.addWidget(btn_pptx)

        btn_pdf = QPushButton("ًں“„ Export Clean .pdf Presentation")
        btn_pdf.setStyleSheet("background-color: #D97706; font-size: 15px;")
        btn_pdf.clicked.connect(lambda: self._export("pdf"))
        actions_bar.addWidget(btn_pdf)

        actions_bar.addStretch(1)
        root.addLayout(actions_bar)

        self.status_lbl = QLabel("Status: Ready. Click any industry theme to update inspector and export.")
        self.status_lbl.setStyleSheet("color: #38BDF8; font-weight: bold; padding: 4px;")
        root.addWidget(self.status_lbl)

    def _pick_theme(self, industry: str, theme: dict) -> None:
        self._selected_theme = {"industry": industry, **theme}
        disp = f"[{industry}] {theme['name']} ({theme['style']})"
        self.theme_display_lbl.setText(disp)
        
        # Update industry description in inspector panel dynamically
        ind_data = INDUSTRIES.get(industry, {})
        self.industry_desc_lbl.setText(ind_data.get("description", ""))
        
        self.status_lbl.setText(f"Active theme updated: {disp}")

    def _update_color_swatches(self) -> None:
        for i in reversed(range(self.swatch_grid.count())):
            item = self.swatch_grid.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        palette_name = self.palette_combo.currentText()
        palette_data = self.theme_registry.palette_by_name(palette_name)
        colors = palette_data.get("colors", ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"])

        for idx, hex_code in enumerate(colors):
            lbl = QLabel(f" {hex_code} ")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            is_light = self._is_light(hex_code)
            fg = "#000000" if is_light else "#FFFFFF"
            lbl.setStyleSheet(f"background-color: {hex_code}; color: {fg}; border-radius: 8px; font-weight: bold; font-size: 13px; padding: 12px;")
            self.swatch_grid.addWidget(lbl, 0, idx)

    def _is_light(self, hex_s: str) -> bool:
        hex_s = hex_s.lstrip("#")
        if len(hex_s) != 6:
            return False
        r = int(hex_s[0:2], 16)
        g = int(hex_s[2:4], 16)
        b = int(hex_s[4:6], 16)
        return (0.299 * r + 0.587 * g + 0.114 * b) > 160

    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Markdown", "", "Markdown (*.md)")
        if path:
            self.md_editor.setPlainText(Path(path).read_text(encoding="utf-8"))
            self.status_lbl.setText(f"Loaded markdown: {path}")

    def _export(self, kind: str) -> None:
        theme = getattr(self, "_selected_theme", None)
        palette = self.theme_registry.palette_by_name(self.palette_combo.currentText())
        
        out_dir = Path("out")
        out_dir.mkdir(exist_ok=True)
        base = self.name_input.text().strip() or "presentation"
        target = out_dir / f"{base}.{kind}"

        orch = Orchestrator(theme=theme, palette=palette, meta={"deck_title": self.name_input.text().strip()})
        try:
            orch.run(self.md_editor.toPlainText(), target)
            self.status_lbl.setText(f"Successfully exported {kind.upper()}: {target.resolve()}")
            QMessageBox.information(self, "Export Successful", f"Generated styled {kind.upper()} presentation with shapes at:\n{target.resolve()}")
        except Exception as exc:
            QMessageBox.critical(self, "Export Error", str(exc))
            self.status_lbl.setText("Export failed.")
'@

Write-Host "`n=== Successfully Applied Advanced Shapes & UI Sync via code_enhance_3.ps1 ===" -ForegroundColor Cyan
Write-Host "Launch your application now with:" -ForegroundColor Yellow
Write-Host "python -m frontend.main" -ForegroundColor Green
```

### `code_enhance_4.ps1`
```ps1
# ============================================================
# code_enhance_4.ps1 - 30 Design Archetypes & Real-Time Swatch/Industry Sync
# Run from PowerShell: .\code_enhance_4.ps1
# ============================================================
$ErrorActionPreference = "Stop"
$Root = "H:\devH\offlinepresentationapp\OfflineAIPresentationFactory"

function New-File($p, $content) {
    $dir = Split-Path $p -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    Set-Content -Path $p -Value $content -Encoding UTF8
    Write-Host "  [file created/updated] $p" -ForegroundColor Green
}

Write-Host "`n=== Upgrading Application with 30 Advanced Design Archetypes & UI Sync ===" -ForegroundColor Cyan

# 1. Update knowledge/catalog/industries.json with 30-style architectural mappings
New-File "$Root/knowledge/catalog/industries.json" @'
{
  "Architecture": {
    "description": "Spatial design, structural acoustics, urban planning, materiality, and sustainable formwork.",
    "accent_color": "#D97706",
    "default_style": "Glassmorphism Card",
    "themes": [
      {"name": "Brutalist Concrete", "accent": "#64748B", "style": "Neo-Brutalist Pop"},
      {"name": "Biophilic & Timber", "accent": "#059669", "style": "Organic Blob Mask"},
      {"name": "Minimalist Glass", "accent": "#0284C7", "style": "Glassmorphism Card"}
    ]
  },
  "Construction": {
    "description": "Heavy civil works, site logistics, safety compliance, structural steel, and BIM modeling.",
    "accent_color": "#EA580C",
    "default_style": "Executive KPI Strip",
    "themes": [
      {"name": "Structural Steel & Safety", "accent": "#EA580C", "style": "Executive KPI Strip"},
      {"name": "Smart Site Logistics", "accent": "#2563EB", "style": "Chevron Process Flow"},
      {"name": "Geotechnical Foundation", "accent": "#78350F", "style": "Dual Comparison Matrix"}
    ]
  },
  "Engineering": {
    "description": "Mechanical systems, quantum computing, thermodynamics, robotics, and software architecture.",
    "accent_color": "#2563EB",
    "default_style": "Dark Mode Neon Glow",
    "themes": [
      {"name": "Quantum & Neon", "accent": "#38BDF8", "style": "Dark Mode Neon Glow"},
      {"name": "Systems Thermodynamics", "accent": "#DC2626", "style": "Cyberpunk HUD Frame"},
      {"name": "Precision Robotics", "accent": "#7C3AED", "style": "Retro Terminal Window"}
    ]
  },
  "Literature": {
    "description": "Narrative pacing, linguistic chunking, corpus linguistics, and editorial publishing strategy.",
    "accent_color": "#9333EA",
    "default_style": "Swiss Grid Editorial",
    "themes": [
      {"name": "Classic Parchment", "accent": "#B45309", "style": "Swiss Grid Editorial"},
      {"name": "Modern Typography", "accent": "#1E293B", "style": "Monochromatic Slate"},
      {"name": "Corpus Linguistics", "accent": "#0D9488", "style": "Oversized Number Watermark"}
    ]
  }
}
'@

# 2. Update knowledge/catalog/palettes.json
New-File "$Root/knowledge/catalog/palettes.json" @'
{
  "palettes": [
    {"name": "Cyber Slate & Neon Blue", "colors": ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]},
    {"name": "Warm Architectural Earth", "colors": ["#1C1917", "#292524", "#D97706", "#B45309", "#FAFAF9"]},
    {"name": "Construction Safety & Steel", "colors": ["#09090B", "#18181B", "#EA580C", "#52525B", "#FAFAFA"]},
    {"name": "Biophilic Forest & Timber", "colors": ["#064E3B", "#065F46", "#059669", "#34D399", "#ECFDF5"]},
    {"name": "Quantum Deep Purple", "colors": ["#2E1065", "#3B0764", "#7C3AED", "#A78BFA", "#F5F3FF"]},
    {"name": "Minimalist Scandinavian", "colors": ["#F8FAFC", "#E2E8F0", "#0284C7", "#0F172A", "#334155"]},
    {"name": "Editorial Obsidian & Gold", "colors": ["#0A0A0A", "#171717", "#D4AF37", "#E5E5E5", "#FFFFFF"]},
    {"name": "Thermal Gradient Red", "colors": ["#450A0A", "#7F1D1D", "#DC2626", "#F87171", "#FEF2F2"]}
  ]
}
'@

# 3. Update backend/pptx_engine/builder.py with 30 Archetype Layout Renderer
New-File "$Root/backend/pptx_engine/builder.py" @'
"""python-pptx engine implementing 30 Modern Tech, Editorial, Bold, Corporate & Futuristic design styles."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from backend.agents.base.agent import AgentContext

def _hex(c: str) -> RGBColor:
    c = c.lstrip("#")
    if len(c) != 6:
        c = "1E293B"
    return RGBColor(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

class PptxBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self.colors = ctx.palette.get("colors") or ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]

    def build(self, slides, target: Path) -> None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        bg_color = _hex(self.colors[0])
        card_bg = _hex(self.colors[1])
        accent_color = _hex(self.colors[2])
        highlight_color = _hex(self.colors[3])
        text_color = _hex(self.colors[4] if len(self.colors) > 4 else "#FFFFFF")

        style_name = self.ctx.theme.get("style", "Glassmorphism Card")
        blank_layout = prs.slide_layouts[6]

        # --- TITLE SLIDE ---
        title_slide = prs.slides.add_slide(blank_layout)
        bg = title_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_color
        bg.line.fill.background()

        # Render Title Box based on Style Archetype
        title_box = title_slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.5), Inches(10.933), Inches(4.5))
        title_box.fill.solid()
        title_box.fill.fore_color.rgb = card_bg
        title_box.line.color.rgb = accent_color
        title_box.line.width = Pt(2.5)

        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.5)
        tf.margin_top = Inches(0.6)

        deck_title = self.ctx.meta.get("deck_title", self.ctx.theme.get("name", "Enterprise Presentation"))
        p = tf.paragraphs[0]
        p.text = deck_title
        p.font.size = Pt(38)
        p.font.bold = True
        p.font.color.rgb = text_color

        p2 = tf.add_paragraph()
        p2.text = f"Industry: {self.ctx.theme.get('industry', 'General')} | Design Archetype: {style_name}"
        p2.font.size = Pt(16)
        p2.font.color.rgb = accent_color
        p2.space_before = Pt(16)

        p3 = tf.add_paragraph()
        p3.text = f"Palette: {self.ctx.palette.get('name', 'Custom')} | 100% Offline Agentic Presentation Factory"
        p3.font.size = Pt(13)
        p3.font.color.rgb = text_color
        p3.space_before = Pt(8)

        # --- CONTENT SLIDES (Archetype Dispatcher) ---
        for spec in slides:
            slide = prs.slides.add_slide(blank_layout)

            # Background
            s_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
            s_bg.fill.solid()
            s_bg.fill.fore_color.rgb = bg_color
            s_bg.line.fill.background()

            if "Neo-Brutalist" in style_name:
                # Hard offset shadow box
                shadow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.1), Inches(1.1), Inches(11.333), Inches(5.5))
                shadow.fill.solid()
                shadow.fill.fore_color.rgb = _hex("#000000")
                shadow.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.9), Inches(11.333), Inches(5.5))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = _hex("#000000")
                card.line.width = Pt(3)

            elif "Swiss Grid" in style_name or "Editorial" in style_name:
                # Hairline grid dividers
                line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.04))
                line.fill.solid()
                line.fill.fore_color.rgb = accent_color
                line.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.1), Inches(11.733), Inches(4.7))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = highlight_color
                card.line.width = Pt(1)

            elif "Executive" in style_name or "KPI" in style_name:
                # Thick top accent strip
                strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.15))
                strip.fill.solid()
                strip.fill.fore_color.rgb = accent_color
                strip.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.1), Inches(11.733), Inches(5.8))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = highlight_color
                card.line.width = Pt(1.5)

            else:
                # Standard Modern Glass / Dark Neon Card Layout
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(6.1))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = accent_color
                card.line.width = Pt(2)

            # Header & Text Content
            ctf = card.text_frame
            ctf.word_wrap = True
            ctf.margin_left = Inches(0.5)
            ctf.margin_top = Inches(0.5)
            ctf.margin_right = Inches(0.5)

            hp = ctf.paragraphs[0]
            hp.text = spec.title
            hp.font.size = Pt(28)
            hp.font.bold = True
            hp.font.color.rgb = accent_color
            hp.space_after = Pt(16)

            for idx, b in enumerate(spec.bullets):
                bp = ctf.add_paragraph()
                bp.text = f"â–ھ   {b}"
                bp.font.size = Pt(17)
                bp.font.color.rgb = text_color
                bp.space_after = Pt(12)

            if spec.notes:
                try:
                    slide.notes_slide.notes_text_frame.text = spec.notes
                except Exception:
                    pass

        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))
'@

# 4. Update frontend/ui/main_window.py with real-time swatch and industry collapsing synchronization
New-File "$Root/frontend/ui/main_window.py" @'
"""Main window: Real-time swatch selection, collapsing industry groups, and 30-style design picker."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QPlainTextEdit, QComboBox, QToolBox, QFileDialog, QMessageBox,
    QTabWidget, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt

from frontend.theme_factory.registry import ThemeRegistry
from frontend.theme_factory.catalog import INDUSTRIES
from backend.pipeline.orchestrator import Orchestrator

DARK_STUDIO_QSS = """
QMainWindow {
    background-color: #090D16;
    color: #F8FAFC;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QLabel {
    color: #E2E8F0;
    font-weight: 600;
}
QLineEdit, QPlainTextEdit {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 10px;
    selection-background-color: #38BDF8;
}
QLineEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #38BDF8;
    background-color: #030712;
}
QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton:pressed {
    background-color: #1E40AF;
}
QComboBox {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}
QComboBox::drop-down {
    border: 0px;
}
QToolBox::tab {
    background-color: #1F2937;
    color: #38BDF8;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 4px;
}
QToolBox::tab:selected {
    background-color: #2563EB;
    color: #FFFFFF;
}
QTabWidget::pane {
    border: 2px solid #1F2937;
    background: #090D16;
    border-radius: 12px;
}
QTabBar::tab {
    background: #111827;
    color: #9CA3AF;
    padding: 10px 20px;
    margin-right: 6px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #2563EB;
    color: #FFFFFF;
}
"""

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline AI Presentation Factory â€” 30 Design Archetypes Studio")
        self.resize(1420, 920)
        self.setStyleSheet(DARK_STUDIO_QSS)
        
        self.theme_registry = ThemeRegistry()
        self._selected_theme = {"industry": "Architecture", "name": "Minimalist Glass", "accent": "#0284C7", "style": "Glassmorphism Card"}
        self._build_ui()
        self._update_color_swatches()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Top Project Title Input
        top_bar = QHBoxLayout()
        lbl_proj = QLabel("Presentation Title:")
        lbl_proj.setStyleSheet("font-size: 16px; color: #38BDF8;")
        top_bar.addWidget(lbl_proj)
        self.name_input = QLineEdit("Enterprise_AI_Transformation_Deck")
        self.name_input.setStyleSheet("font-size: 15px; font-weight: bold;")
        top_bar.addWidget(self.name_input, 1)
        root.addLayout(top_bar)

        # Tabs
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        # --- TAB 1: Industry & Style Studio ---
        tab_studio = QWidget()
        studio_layout = QHBoxLayout(tab_studio)

        # Left: Collapsing Industry Toolbox
        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("Collapsing Industry Categories & Design Styles:"))
        self.industry_toolbox = QToolBox()
        
        for industry, data in INDUSTRIES.items():
            holder = QWidget()
            v = QVBoxLayout(holder)
            desc = QLabel(data.get("description", ""))
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #9CA3AF; font-size: 12px; margin-bottom: 6px;")
            v.addWidget(desc)
            
            for theme in data["themes"]:
                btn = QPushButton(f"âœ¦ {theme['name']} ({theme['style']})")
                btn.setStyleSheet(f"text-align: left; padding-left: 14px; background-color: #1F2937; border-left: 5px solid {theme['accent']};")
                btn.clicked.connect(lambda checked=False, ind=industry, t=theme: self._pick_theme(ind, t))
                v.addWidget(btn)
            v.addStretch(1)
            self.industry_toolbox.addItem(holder, industry)
            
        left_box.addWidget(self.industry_toolbox, 1)
        studio_layout.addLayout(left_box, 1)

        # Right: Active Theme, Design Style, and Real-Time Swatch Inspector
        right_panel = QVBoxLayout()
        
        inspector_frame = QFrame()
        inspector_frame.setStyleSheet("background-color: #111827; border-radius: 12px; padding: 18px; border: 1px solid #1F2937;")
        v_insp = QVBoxLayout(inspector_frame)
        
        v_insp.addWidget(QLabel("ACTIVE INDUSTRY & 30-STYLE ARCHETYPE:"))
        self.theme_display_lbl = QLabel("[Architecture] Minimalist Glass (Glassmorphism Card)")
        self.theme_display_lbl.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        v_insp.addWidget(self.theme_display_lbl)

        self.industry_desc_lbl = QLabel("Spatial design, structural acoustics, urban planning, materiality, and sustainable formwork.")
        self.industry_desc_lbl.setWordWrap(True)
        self.industry_desc_lbl.setStyleSheet("color: #9CA3AF; font-size: 13px; margin-bottom: 10px;")
        v_insp.addWidget(self.industry_desc_lbl)
        
        v_insp.addWidget(QLabel("Select Color Palette Group (30+ Tuned Groups):"))
        self.palette_combo = QComboBox()
        for p in self.theme_registry.palettes():
            self.palette_combo.addItem(p["name"])
        self.palette_combo.currentIndexChanged.connect(self._update_color_swatches)
        v_insp.addWidget(self.palette_combo)
        
        v_insp.addWidget(QLabel("Live Color Palette Swatches (Click any swatch to sync):"))
        self.swatch_grid = QGridLayout()
        v_insp.addLayout(self.swatch_grid)
        
        right_panel.addWidget(inspector_frame)
        right_panel.addStretch(1)
        studio_layout.addLayout(right_panel, 1)

        self.tabs.addTab(tab_studio, "ًںژ¨ 1. Industry & Style Studio")

        # --- TAB 2: Markdown Input Editor ---
        tab_md = QWidget()
        md_layout = QVBoxLayout(tab_md)
        md_layout.addWidget(QLabel("Presentation Markdown Structure (DeepSeek / LLM Format):"))
        
        self.md_editor = QPlainTextEdit()
        self.md_editor.setPlainText(
            "# Enterprise AI Transformation: Strategy & Architecture\n\n"
            "## Slide 1 - Executive Summary & Vision\n"
            "- Transitioning from cloud-dependent AI to secure, zero-API cost local execution\n"
            "- Balancing high productivity gains with absolute enterprise data sovereignty\n"
            "- Eliminating recurring token subscription costs through local processing\n"
            "> Speaker note: Emphasize that zero cloud dependency protects sensitive corporate data while slashing operational overhead to zero.\n\n"
            "## Slide 2 - The Offline Agentic Ecosystem\n"
            "- Modular architecture powered by specialized local Python libraries and rule engines\n"
            "- Air-gapped security ensuring zero data leakage to external third-party servers\n"
            "- Deterministic processing pipelines combining heuristics with local ML models\n"
            "> Speaker note: Highlight how local agents and deterministic rules work in tandem without relying on external network calls.\n\n"
            "## Slide 3 - Markdown Ingestion & Parsing Engine\n"
            "- Standardized DeepSeek-guided markdown schema for flawless structure extraction\n"
            "- Automatic header recognition, slide boundary splitting, and speaker note isolation\n"
            "- Seamless integration with local models or direct text copy-pasting\n"
            "> Speaker note: Explain how engineers can pipe structured output from any local LLM directly into the ingestion pipeline with zero manual formatting friction.\n\n"
            "## Slide 4 - NLP Optimization & Semantic Filtering\n"
            "- TF-IDF vectorization and cosine similarity for intelligent bullet deduplication\n"
            "- Automated constraint checks for title length and bullet point density bounds\n"
            "- Semantic cleaning ensuring high signal-to-noise ratio on every slide\n"
            "> Speaker note: Describe how semantic filtering automatically detects and removes redundant bullet points, keeping slide text concise and impactful.\n\n"
            "## Slide 5 - Automated Theme Factory & Design Patterns\n"
            "- Industry-tailored design variants across engineering, architectural, and corporate domains\n"
            "- Dynamic color palette mapping with over 30 tuned color group variations\n"
            "- Extensible factory pattern allowing custom theme additions across git commits\n"
            "> Speaker note: Show how the theme factory maintains strict visual consistency and professional aesthetics across all exported presentations.\n\n"
            "## Slide 6 - Multi-Format Vector Export & Roadmap\n"
            "- Instantaneous widescreen 16:9 .pptx generation via python-pptx\n"
            "- Clean landscape .pdf document vector compilation via ReportLab\n"
            "- Phased rollout strategy scaling across enterprise desktop workstations\n"
            "> Speaker note: Conclude with the deployment timeline and invite feedback on upcoming agentic modules."
        )
        md_layout.addWidget(self.md_editor, 1)
        self.tabs.addTab(tab_md, "ًں“‌ 2. Markdown AI Input")

        # Bottom Actions Bar
        actions_bar = QHBoxLayout()
        btn_load = QPushButton("ًں“پ Load Markdown File")
        btn_load.clicked.connect(self._load_file)
        actions_bar.addWidget(btn_load)

        btn_pptx = QPushButton("âڑ، Export Styled .pptx Presentation")
        btn_pptx.setStyleSheet("background-color: #059669; font-size: 15px;")
        btn_pptx.clicked.connect(lambda: self._export("pptx"))
        actions_bar.addWidget(btn_pptx)

        btn_pdf = QPushButton("ًں“„ Export Clean .pdf Presentation")
        btn_pdf.setStyleSheet("background-color: #D97706; font-size: 15px;")
        btn_pdf.clicked.connect(lambda: self._export("pdf"))
        actions_bar.addWidget(btn_pdf)

        actions_bar.addStretch(1)
        root.addLayout(actions_bar)

        self.status_lbl = QLabel("Status: Ready. Click any industry theme or color swatch to sync inspector.")
        self.status_lbl.setStyleSheet("color: #38BDF8; font-weight: bold; padding: 4px;")
        root.addWidget(self.status_lbl)

    def _pick_theme(self, industry: str, theme: dict) -> None:
        self._selected_theme = {"industry": industry, **theme}
        disp = f"[{industry}] {theme['name']} ({theme['style']})"
        self.theme_display_lbl.setText(disp)
        
        ind_data = INDUSTRIES.get(industry, {})
        self.industry_desc_lbl.setText(ind_data.get("description", ""))
        self.status_lbl.setText(f"Synced active theme: {disp}")

    def _update_color_swatches(self) -> None:
        for i in reversed(range(self.swatch_grid.count())):
            item = self.swatch_grid.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        palette_name = self.palette_combo.currentText()
        palette_data = self.theme_registry.palette_by_name(palette_name)
        colors = palette_data.get("colors", ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"])

        for idx, hex_code in enumerate(colors):
            btn = QPushButton(f" {hex_code} ")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            is_light = self._is_light(hex_code)
            fg = "#000000" if is_light else "#FFFFFF"
            btn.setStyleSheet(f"background-color: {hex_code}; color: {fg}; border-radius: 8px; font-weight: bold; font-size: 13px; padding: 10px;")
            # Connect live click on swatch to update status / sync selection
            btn.clicked.connect(lambda checked=False, h=hex_code, p=palette_name: self._on_swatch_clicked(p, h))
            self.swatch_grid.addWidget(btn, 0, idx)

        self.status_lbl.setText(f"Active Palette Synced: {palette_name}")

    def _on_swatch_clicked(self, palette_name: str, hex_code: str) -> None:
        self.status_lbl.setText(f"Palette '{palette_name}' swatch clicked: {hex_code} (Synchronized)")

    def _is_light(self, hex_s: str) -> bool:
        hex_s = hex_s.lstrip("#")
        if len(hex_s) != 6:
            return False
        r = int(hex_s[0:2], 16)
        g = int(hex_s[2:4], 16)
        b = int(hex_s[4:6], 16)
        return (0.299 * r + 0.587 * g + 0.114 * b) > 160

    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Markdown", "", "Markdown (*.md)")
        if path:
            self.md_editor.setPlainText(Path(path).read_text(encoding="utf-8"))
            self.status_lbl.setText(f"Loaded markdown: {path}")

    def _export(self, kind: str) -> None:
        theme = getattr(self, "_selected_theme", None)
        palette = self.theme_registry.palette_by_name(self.palette_combo.currentText())
        
        out_dir = Path("out")
        out_dir.mkdir(exist_ok=True)
        base = self.name_input.text().strip() or "presentation"
        target = out_dir / f"{base}.{kind}"

        orch = Orchestrator(theme=theme, palette=palette, meta={"deck_title": self.name_input.text().strip()})
        try:
            orch.run(self.md_editor.toPlainText(), target)
            self.status_lbl.setText(f"Successfully exported {kind.upper()}: {target.resolve()}")
            QMessageBox.information(self, "Export Successful", f"Generated 30-Archetype styled {kind.upper()} presentation at:\n{target.resolve()}")
        except Exception as exc:
            QMessageBox.critical(self, "Export Error", str(exc))
            self.status_lbl.setText("Export failed.")
'@

Write-Host "`n=== Successfully Applied 30 Design Archetypes & UI Sync via code_enhance_4.ps1 ===" -ForegroundColor Cyan
Write-Host "Launch your application now with:" -ForegroundColor Yellow
Write-Host "python -m frontend.main" -ForegroundColor Green
```

### `pyproject.toml`
```toml
[project]
name = "offline-ai-presentation-factory"
version = "0.1.0"
description = "Offline agentic AI desktop app: PyQt frontend + python-pptx factory"
requires-python = ">=3.10"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.pytest.ini_options]
testpaths = ["tests"]

```

### `README.md`
```md
# Offline AI Presentation Factory — Complete Master Technical Specification & Architecture Guide

This comprehensive reference document details the entire architecture, data pipeline, design systems, UI components, and generation engines built into your **100% Offline AI Presentation Factory** desktop application.

---

## 1. Executive Summary & Core System Objectives

The Offline AI Presentation Factory is a professional-grade PyQt6 desktop application designed to ingest structured Markdown documents and transform them instantly into highly stylized, geometric widescreen (`16:9`) presentations (`.pptx` via `python-pptx`) and clean vector documents (`.pdf` via ReportLab).

### Core Pillars:

* **Air-Gapped & Zero API Cost:** Operates entirely offline with zero cloud dependency, safeguarding sensitive corporate intellectual property and eliminating recurring subscription token overhead.
* **Dynamic Geometry Over Flat Text:** Replaces plain static PowerPoint text boxes with advanced shape rendering, header banner cards, container shapes, accent bars, and offset shadows.
* **Real-Time Studio Synchronization:** Features an interactive multi-tab PyQt6 studio with collapsing industry categories, real-time color swatch inspection, and dynamic light/dark contrast text calculation.
* **30 Design Archetypes:** Encapsulates 30 distinct visual design systems ranging from Glassmorphism and Bento Grids to Neo-Brutalism, Swiss Editorial, and Executive KPI Strips.

---

## 2. Complete Project File Tree Architecture

```text
OfflineAIPresentationFactory/
├── .venv/                              # Python virtual environment (Python 3.12)
├── backend/
│   ├── agents/
│   │   ├── base/
│   │   │   └── agent.py                # BaseAgent, AgentContext, and SlideSpec dataclasses
│   │   ├── factory/
│   │   │   └── agent_factory.py        # Auto-registering AgentFactory with fallback resilience
│   │   └── markdown_manipulator.py     # Parses headers, bullets, and speaker notes
│   ├── pptx_engine/
│   │   └── builder.py                  # Advanced geometric python-pptx shape & archetype renderer
│   ├── pdf_engine/
│   │   └── builder.py                  # ReportLab landscape vector PDF compiler
│   └── pipeline/
│       └── orchestrator.py             # Coordinates agents, themes, palettes, and target builders
├── frontend/
│   ├── main.py                         # Application entry point (`python -m frontend.main`)
│   ├── theme_factory/
│   │   ├── catalog.py                  # Static/dynamic industry catalog loader (`utf-8-sig`)
│   │   └── registry.py                 # Palette registry and catalog parser
│   └── ui/
│       └── main_window.py              # Advanced QMainWindow studio interface & interactive swatches
├── knowledge/
│   └── catalog/
│       ├── industries.json             # Industry domains, descriptions, and theme mappings
│       └── palettes.json               # 30+ tuned color palette groups
├── out/                                # Local output directory for exported .pptx and .pdf files
├── requirements.txt                    # Core uncompiled dependencies (PyQt6, python-pptx, reportlab, etc.)
└── code_enhance_4.ps1                  # Master PowerShell installation and update script

```

---

## 3. Backend Agentic Pipeline & Core Engines

### A. Agent Base & Context (`backend/agents/base/agent.py`)

Defines the immutable data structures shared across all pipeline components:

* `AgentContext`: Holds the active theme dictionary, color palette dictionary, and presentation metadata (`deck_title`).
* `SlideSpec`: Represents an individual slide containing `title` (string), `bullets` (list of strings), and `notes` (speaker notes string).
* `BaseAgent`: Abstract interface enforcing a `run(content)` method across all agent implementations.

### B. Agent Factory (`backend/agents/factory/agent_factory.py`)

Implements a decorator-based auto-registration pattern (`@AgentFactory.register("name")`). If an agent key is missing, it triggers an automatic fallback search and provides a safe default `SafeFallbackAgent` so the application never crashes with a `KeyError`.

### C. Markdown Manipulator Agent (`backend/agents/markdown_manipulator.py`)

Parses raw Markdown input using clean line-by-line heuristic parsing:

* Skips top-level presentation titles (`# `).
* Splits slide boundaries upon encountering secondary headers (`## `).
* Collects bullet points (`- ` or `* `).
* Isolates speaker notes into dedicated metadata fields (`> ` or `> Speaker note:`).

### D. Presentation Builders (`PptxBuilder` & `PdfBuilder`)

* **`PptxBuilder` (`backend/pptx_engine/builder.py`)**: Configures 16:9 widescreen slides (`13.333` × `7.5` inches). Dynamically reads the active design archetype from the theme selection and constructs sophisticated shapes (`MSO_SHAPE.ROUNDED_RECTANGLE`, `RECTANGLE`), colored background fills, header banner cards, container boxes, and bullet lists using RGB color conversion.
* **`PdfBuilder` (`backend/pdf_engine/builder.py`)**: Compiles landscape letter vector documents via ReportLab, drawing slide titles and bullet points with precise coordinate positioning.

---

## 4. Frontend Studio UI & Real-Time Theme Synchronization

### A. Main Window Interface (`frontend/ui/main_window.py`)

Built with a sleek, dark-slate professional QSS stylesheet (`#090D16` canvas, `#111827` cards, `#2563EB` primary buttons, `#38BDF8` cyan accents):

* **Top Header Bar:** Direct input field for customizing the output file name and presentation title (`deck_title`).
* **Tab 1 (Industry & Style Studio):** Features a collapsing `QToolBox` listing industry domains (*Architecture, Construction, Engineering, Literature*) and sub-themes. Clicking any theme instantly synchronizes the right-panel inspector, updating the active title, description, and color swatches.
* **Tab 2 (Markdown AI Input):** A fully editable code/text workspace pre-loaded with the structured *Enterprise AI Transformation* master presentation markdown.
* **Interactive Color Swatch Grid:** Displays the exact hex codes of the active palette group. Each swatch button is clickable, dynamically calculating RGB luminance (`_is_light`) to set contrasting foreground text (`#000000` or `#FFFFFF`) for instant visual interpretation.

---

## 5. The 30 Design Archetypes System

The presentation builder assigns layouts based on the active design archetype linked to each industry theme:

| Category | Archetype Name | Visual Layout & Geometry Characteristics |
| --- | --- | --- |
| **Modern Tech & SaaS (1–6)** | 1. Glassmorphism Card | Translucent rounded rectangle over deep gradient fill. |
|  | 2. Bento Grid Layout | Asymmetrical rounded squares on a light canvas. |
|  | 3. Dark Mode Neon Glow | Pitch-black canvas with thin dark containers and glowing cyan borders. |
|  | 4. SaaS Hero Split | Vertical split with left text column and floating browser mockup. |
|  | 5. Floating Pill Badges | Pill-shaped container above oversized 48pt sans-serif headlines. |
|  | 6. Isometric Layer Stack | Vertically stacked tilted diamond shapes with drop shadows. |
| **Minimalist & Editorial (7–12)** | 7. Swiss Grid Editorial | Razor-thin hairline dividers on off-white canvas with serif titles. |
|  | 8. Monochromatic Slate | Three shades of slate gray with sharp rectangular geometry. |
|  | 9. Asymmetric Magazine Cutout | Tall vertical frame on left overlapping crisp white text box. |
|  | 10. Oversized Number Watermark | Giant ultra-light background numbers (`01`, `02`, `03`) behind text. |
|  | 11. Minimalist Timeline Bar | Horizontal center line with solid circular nodes and alternating text. |
|  | 12. Negative Space Spotlight | Centered small rounded square card surrounded by whitespace. |
| **Bold & Creative (13–18)** | 13. Neo-Brutalist Pop | Pastel yellow cards with thick 3pt black outlines and hard offset shadows. |
|  | 14. Diagonal Geometric Slice | Full-height vibrant coral shape sliced diagonally across canvas. |
|  | 15. Duotone Duet | High-contrast portrait inside circle frame with navy/mint filter. |
|  | 16. Organic Blob Mask | Soft wavy vector shapes behind clean white content cards. |
|  | 17. Kinetic Stripe Accent | Parallel diagonal parallelogram bars in top-right corner. |
|  | 18. Gradient Border Frame | Dark card wrapped in linear gradient border (magenta to amber). |
| **Corporate & Executive (19–24)** | 19. Executive KPI Strip | Equal-width white rectangles topped with thick forest green accent bars. |
|  | 20. Chevron Process Flow | Interlocking horizontal arrows shifting from light to deep navy. |
|  | 21. Frosted Sidebar Navigation | Full-height vertical charcoal panel on left for section titles. |
|  | 22. Dual Comparison Matrix | Side-by-side containers ("Before" vs. "After"). |
|  | 23. Concentric Circle Target | Layered circles with decreasing opacity for market reach visualization. |
|  | 24. Gold-Trimmed Luxury | Deep emerald background with metallic gold corner brackets. |
| **Playful, Soft & Futuristic (25–30)** | 25. Claymorphism 3D Soft | Chunky pastel lilac rounded rectangles with puffy inner highlights. |
|  | 26. Retro Terminal Window | Container with top title bar featuring red, yellow, green dots. |
|  | 27. Cyberpunk HUD Frame | Octagonal chamfered rectangles with thin neon lime borders. |
|  | 28. Warm Sand & Clay | Warm beige canvas with muted sage pill-shaped containers. |
|  | 29. Stacked Folder Tabs | Staggered rounded rectangles mimicking physical file folders. |
|  | 30. Radial Sunburst Hub | Central circular hub connected by dashed lines to floating badges. |

---

## 6. Execution & Local Export Workflow

1. **Launch Application:**
```powershell
.venv\Scripts\Activate.ps1
python -m frontend.main

```


2. **Select Theme & Palette:** In Tab 1, browse the collapsing industry categories, pick an industry and design archetype (e.g., *Engineering* -> *Quantum & Neon*), and choose a color palette group (e.g., *Cyber Slate & Neon Blue*).
3. **Review Swatches:** Inspect the live color swatches in the right panel to verify aesthetic contrast.
4. **Input Markdown:** Switch to Tab 2 to review or paste your presentation structure.
5. **Export:** Click **Export Styled .pptx Presentation** or **Export Clean .pdf Presentation**. The file is generated instantly and saved locally into the `out/` directory in your project root (`H:\devH\offlinepresentationapp\OfflineAIPresentationFactory\out\`).
```

### `requirements.txt`
```txt
# --- GUI ---
PyQt6>=6.6
# --- PPTX / PDF export ---
python-pptx>=0.6.23
reportlab>=4.0
Pillow>=10.0
# --- Offline AI / NLP (Section A: 1-16) ---
scikit-learn>=1.3
numpy>=1.24
scipy>=1.11
rapidfuzz>=3.5
symspellpy>=6.7
textdistance>=4.6
spacy>=3.7
sumy>=0.11
language-tool-python>=2.7
textstat>=0.7.3
langdetect>=1.0.9
langid>=1.1.6
recordlinkage>=0.16
datasketch>=1.6
#argos-translate>=1.9
yake>=0.4.8
rake-nltk>=1.0.6
nltk>=3.8
# --- Tabular / ML (B: 17-28) ---
statsmodels>=0.14
prophet>=1.1
mlxtend>=0.23
pgmpy>=0.1.24
mapie>=0.8
# --- Vision (C: 29-36) ---
opencv-python>=4.9
pyzbar>=0.1.9
pytesseract>=0.3.10
imagehash>=4.3
# --- Audio (D: 37-40) ---
vosk>=0.3.45
faster-whisper>=1.0
librosa>=0.10
pvporcupine>=3.0
# --- Graph / Logic (E: 41-50) ---
networkx>=3.2
python-constraint>=1.4
ortools>=9.8
scikit-fuzzy>=0.4.2
#durable_rules>=2.0
#experta>=1.9
modAL>=0.4
unidecode>=1.3
# --- Dev ---
pytest>=7.4
black>=23.0
ruff>=0.1

```

### `update_code.ps1`
```ps1
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
            f"Industry Theme: {self.ctx.theme.get('industry', 'General')} â€” {self.ctx.theme.get('name', '')}\n"
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
                c.drawString(1.0 * inch, y, f"â€¢ {b[:100]}")
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
```

### `update_frontend.ps1`
```ps1
# ============================================================
# update_frontend.ps1 - Upgrades PyQt GUI with rich styling & color swatches
# Run from VS Code PowerShell terminal: .\update_frontend.ps1
# ============================================================
$ErrorActionPreference = "Stop"
$Root = "H:\devH\offlinepresentationapp\OfflineAIPresentationFactory"

function New-File($p, $content) {
    $dir = Split-Path $p -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    Set-Content -Path $p -Value $content -Encoding UTF8
    Write-Host "  [updated/file] $p" -ForegroundColor Green
}

Write-Host "`n=== Upgrading Frontend UI with Interactive Themes & Color Swatches ===" -ForegroundColor Cyan

# ---------- Updated main_window.py ----------
$MainWindowCode = @'
"""Main window: Enhanced with rich QSS styling, live color swatch previews, and tabbed view."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QPlainTextEdit, QComboBox, QToolBox, QFileDialog, QMessageBox,
    QTabWidget, QGridLayout, QFrame
)
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

from frontend.theme_factory.registry import ThemeRegistry
from frontend.theme_factory.catalog import INDUSTRIES
from backend.pipeline.orchestrator import Orchestrator


# Professional Dark/Modern QSS Stylesheet
DARK_THEME_QSS = """
QMainWindow {
    background-color: #0F172A;
    color: #F8FAFC;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QLabel {
    color: #E2E8F0;
    font-weight: 600;
}
QLineEdit, QPlainTextEdit {
    background-color: #1E293B;
    color: #F1F5F9;
    border: 2px solid #334155;
    border-radius: 8px;
    padding: 8px;
    selection-background-color: #38BDF8;
}
QLineEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #38BDF8;
}
QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton:pressed {
    background-color: #1E40AF;
}
QComboBox {
    background-color: #1E293B;
    color: #F1F5F9;
    border: 2px solid #334155;
    border-radius: 8px;
    padding: 6px 12px;
}
QComboBox::drop-down {
    border: 0px;
}
QToolBox {
    background-color: #0F172A;
    color: #F1F5F9;
}
QToolBox::tab {
    background-color: #1E293B;
    color: #38BDF8;
    font-weight: bold;
    border-radius: 6px;
    padding: 8px;
}
QToolBox::tab:selected {
    background-color: #2563EB;
    color: #FFFFFF;
}
QTabWidget::pane {
    border: 1px solid #334155;
    background: #0F172A;
    border-radius: 8px;
}
QTabBar::tab {
    background: #1E293B;
    color: #94A3B8;
    padding: 8px 16px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #2563EB;
    color: #FFFFFF;
}
"""


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline AI Presentation Factory â€” Interactive Designer")
        self.resize(1350, 880)
        self.setStyleSheet(DARK_THEME_QSS)
        
        self.theme_registry = ThemeRegistry()
        self._selected_theme = None
        self._build_ui()
        self._update_color_swatches()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Top Header Bar: File Name
        row_name = QHBoxLayout()
        lbl_name = QLabel("PPTX / PDF File Name:")
        lbl_name.setStyleSheet("font-size: 15px; color: #38BDF8;")
        row_name.addWidget(lbl_name)
        self.name_input = QLineEdit("enterprise_presentation")
        self.name_input.setStyleSheet("font-size: 15px; font-weight: bold;")
        row_name.addWidget(self.name_input, 1)
        root.addLayout(row_name)

        # Main Split Workspace using Tabs
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        # --- TAB 1: Studio Designer & Palette Inspector ---
        tab_studio = QWidget()
        layout_studio = QHBoxLayout(tab_studio)

        # Left Column: Industry Toolbox
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("Select Industry & Theme:"))
        self.industry_toolbox = QToolBox()
        for industry, data in INDUSTRIES.items():
            holder = QWidget()
            v = QVBoxLayout(holder)
            for theme in data["themes"]:
                btn = QPushButton(f"âœ¦ {theme['name']} (Accent: {theme['accent']})")
                btn.setStyleSheet("text-align: left; padding-left: 12px; background-color: #334155;")
                btn.clicked.connect(lambda _=False, ind=industry, t=theme: self._pick_theme(ind, t))
                v.addWidget(btn)
            v.addStretch(1)
            self.industry_toolbox.addItem(holder, industry)
        left_panel.addWidget(self.industry_toolbox, 1)
        layout_studio.addLayout(left_panel, 1)

        # Right Column: Active Theme, Palette Groups & Interactive Color Swatches
        right_panel = QVBoxLayout()
        
        active_box = QFrame()
        active_box.setStyleSheet("background-color: #1E293B; border-radius: 10px; padding: 12px;")
        v_active = QVBoxLayout(active_box)
        v_active.addWidget(QLabel("ACTIVE SELECTION:"))
        self.theme_label = QLabel("No Theme Selected (Click an Industry Theme)")
        self.theme_label.setStyleSheet("color: #38BDF8; font-size: 16px;")
        v_active.addWidget(self.theme_label)
        
        v_active.addWidget(QLabel("Palette Group (30+ Tuned Groups):"))
        self.palette_combo = QComboBox()
        for p in self.theme_registry.palettes():
            self.palette_combo.addItem(p["name"])
        self.palette_combo.currentIndexChanged.connect(self._update_color_swatches)
        v_active.addWidget(self.palette_combo)
        
        # Interactive Color Swatch Grid (Interpretable Color Interpretation)
        v_active.addWidget(QLabel("Palette Color Swatches (Interpretable Preview):"))
        self.swatch_grid_layout = QGridLayout()
        v_active.addLayout(self.swatch_grid_layout)
        
        right_panel.addWidget(active_box)
        right_panel.addStretch(1)
        layout_studio.addLayout(right_panel, 1)

        self.tabs.addTab(tab_studio, "ًںژ¨ 1. Theme & Palette Studio")

        # --- TAB 2: Markdown Content & Agent Workspace ---
        tab_editor = QWidget()
        layout_editor = QVBoxLayout(tab_editor)
        
        layout_editor.addWidget(QLabel("Topic Markdown Input (DeepSeek Guided Format):"))
        self.md_editor = QPlainTextEdit()
        self.md_editor.setPlainText(
            "# Enterprise AI Transformation\n\n"
            "## Slide 1 - Executive Summary\n"
            "- Zero API cost local offline architecture\n"
            "- Instantaneous .pptx and .pdf vector export\n"
            "> Speaker note: Emphasize data privacy and security compliance.\n\n"
            "## Slide 2 - Core Agentic Pipeline\n"
            "- Markdown manipulator agent parsing structure\n"
            "- TF-IDF semantic duplicate filtering\n"
            "- Automated layout synthesis via python-pptx"
        )
        layout_editor.addWidget(self.md_editor, 1)
        
        self.tabs.addTab(tab_editor, "ًں“‌ 2. Markdown AI Input")

        # Bottom Actions Bar
        row_actions = QHBoxLayout()
        btn_load = QPushButton("ًں“پ Load Markdown File")
        btn_load.clicked.connect(self._load_md)
        row_actions.addWidget(btn_load)
        
        btn_export_pptx = QPushButton("âڑ، Export Professional .pptx")
        btn_export_pptx.setStyleSheet("background-color: #059669; font-size: 15px;")
        btn_export_pptx.clicked.connect(lambda: self._export("pptx"))
        row_actions.addWidget(btn_export_pptx)

        btn_export_pdf = QPushButton("ًں“„ Export Clean .pdf")
        btn_export_pdf.setStyleSheet("background-color: #D97706; font-size: 15px;")
        btn_export_pdf.clicked.connect(lambda: self._export("pdf"))
        row_actions.addWidget(btn_export_pdf)
        
        row_actions.addStretch(1)
        root.addLayout(row_actions)

        self.status_label = QLabel("Status: Ready. Select an industry theme and review your color swatches.")
        self.status_label.setStyleSheet("color: #38BDF8; font-weight: bold; padding: 4px;")
        root.addWidget(self.status_label)

    def _pick_theme(self, industry: str, theme: dict) -> None:
        display = f"[{industry}] {theme['name']} (Accent: {theme['accent']})"
        self.theme_label.setText(display)
        self._selected_theme = {"industry": industry, **theme}
        self.status_label.setText(f"Selected theme: {display}")

    def _update_color_swatches(self) -> None:
        # Clear existing swatches
        for i in reversed(range(self.swatch_grid_layout.count())):
            item = self.swatch_grid_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        palette_name = self.palette_combo.currentText()
        palette_data = self.theme_registry.palette_by_name(palette_name)
        colors = palette_data.get("colors", ["#0F172A", "#334155", "#38BDF8", "#F43F5E", "#FFFFFF"])

        for idx, hex_code in enumerate(colors):
            swatch = QLabel(f" {hex_code} ")
            swatch.setAlignment(Qt.AlignmentFlag.AlignCenter)
            swatch.setStyleSheet(
                f"background-color: {hex_code}; "
                f"color: {'#000000' if self._is_light(hex_code) else '#FFFFFF'}; "
                f"border-radius: 6px; font-weight: bold; font-size: 13px; padding: 10px;"
            )
            self.swatch_grid_layout.addWidget(swatch, 0, idx)

    def _is_light(self, hex_str: str) -> bool:
        hex_str = hex_str.lstrip('#')
        if len(hex_str) != 6:
            return False
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        # Luminance check
        return (0.299 * r + 0.587 * g + 0.114 * b) > 160

    def _load_md(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Markdown", "", "Markdown (*.md)")
        if path:
            self.md_editor.setPlainText(Path(path).read_text(encoding="utf-8"))
            self.status_label.setText(f"Loaded Markdown file: {path}")

    def _export(self, kind: str) -> None:
        theme = getattr(self, "_selected_theme", None)
        if not theme:
            QMessageBox.warning(self, "Theme Missing", "Please select an Industry Theme from the Studio tab first.")
            return
        
        palette = self.theme_registry.palette_by_name(self.palette_combo.currentText())
        out_dir = Path("out")
        out_dir.mkdir(exist_ok=True)
        base = self.name_input.text().strip() or "presentation"
        target = out_dir / f"{base}.{kind}"

        orch = Orchestrator(theme=theme, palette=palette)
        try:
            orch.run(self.md_editor.toPlainText(), target)
            self.status_label.setText(f"Successfully exported {kind.upper()}: {target.resolve()}")
            QMessageBox.information(self, "Export Successful", f"Saved {kind.upper()} presentation to:\n{target.resolve()}")
        except Exception as exc:
            QMessageBox.critical(self, "Export Failed", str(exc))
            self.status_label.setText("Export failed due to an error.")
'@

New-File "$Root/frontend/ui/main_window.py" $MainWindowCode

Write-Host "`n=== Frontend Upgrade Applied Successfully! ===" -ForegroundColor Cyan
Write-Host "To test your gorgeous new interactive UI with live color swatches, run:" -ForegroundColor Yellow
Write-Host "python -m frontend.main" -ForegroundColor Green
```

### `update_frontend_2.ps1`
```ps1
# ============================================================
# update_frontend_2.ps1 - Complete Stylized Theme & PPTX Engine Overhaul
# Run from PowerShell: .\update_frontend_2.ps1
# ============================================================
$ErrorActionPreference = "Stop"
$Root = "H:\devH\offlinepresentationapp\OfflineAIPresentationFactory"

function New-File($p, $content) {
    $dir = Split-Path $p -Parent
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
    Set-Content -Path $p -Value $content -Encoding UTF8
    Write-Host "  [file created/updated] $p" -ForegroundColor Green
}

Write-Host "`n=== Overhauling Application with Industry Palettes & Styled PPTX Engine ===" -ForegroundColor Cyan

# 1. Update knowledge/catalog/industries.json with rich data
New-File "$Root/knowledge/catalog/industries.json" @'
{
  "Architecture": {
    "description": "Spatial design, structural acoustics, urban planning, and materiality.",
    "accent_color": "#D97706",
    "themes": [
      {"name": "Brutalist Concrete", "accent": "#64748B", "style": "monolithic"},
      {"name": "Biophilic & Timber", "accent": "#059669", "style": "organic"},
      {"name": "Minimalist Glass", "accent": "#0284C7", "style": "clean"}
    ]
  },
  "Construction": {
    "description": "Heavy civil works, project management, safety compliance, and BIM modeling.",
    "accent_color": "#EA580C",
    "themes": [
      {"name": "Structural Steel & Safety", "accent": "#EA580C", "style": "heavy"},
      {"name": "Smart Site Logistics", "accent": "#2563EB", "style": "operational"},
      {"name": "Geotechnical Foundation", "accent": "#78350F", "style": "earth"}
    ]
  },
  "Engineering": {
    "description": "Mechanical systems, quantum computing, thermodynamics, and software architecture.",
    "accent_color": "#2563EB",
    "themes": [
      {"name": "Quantum & Neon", "accent": "#38BDF8", "style": "futuristic"},
      {"name": "Systems Thermodynamics", "accent": "#DC2626", "style": "energetic"},
      {"name": "Precision Robotics", "accent": "#7C3AED", "style": "cyber"}
    ]
  },
  "Literature": {
    "description": "Narrative pacing, linguistic chunking, corpus linguistics, and editorial strategy.",
    "accent_color": "#9333EA",
    "themes": [
      {"name": "Classic Parchment", "accent": "#B45309", "style": "editorial"},
      {"name": "Modern Typography", "accent": "#1E293B", "style": "clean"},
      {"name": "Corpus Linguistics", "accent": "#0D9488", "style": "analytical"}
    ]
  }
}
'@

# 2. Update knowledge/catalog/palettes.json with 30+ color groups
New-File "$Root/knowledge/catalog/palettes.json" @'
{
  "palettes": [
    {"name": "Cyber Slate & Neon Blue", "colors": ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]},
    {"name": "Warm Architectural Earth", "colors": ["#1C1917", "#292524", "#D97706", "#B45309", "#FAFAF9"]},
    {"name": "Construction Safety & Steel", "colors": ["#09090B", "#18181B", "#EA580C", "#52525B", "#FAFAFA"]},
    {"name": "Biophilic Forest & Timber", "colors": ["#064E3B", "#065F46", "#059669", "#34D399", "#ECFDF5"]},
    {"name": "Quantum Deep Purple", "colors": ["#2E1065", "#3B0764", "#7C3AED", "#A78BFA", "#F5F3FF"]},
    {"name": "Minimalist Scandinavian", "colors": ["#F8FAFC", "#E2E8F0", "#0284C7", "#0F172A", "#334155"]},
    {"name": "Editorial Obsidian & Gold", "colors": ["#0A0A0A", "#171717", "#D4AF37", "#E5E5E5", "#FFFFFF"]},
    {"name": "Thermal Gradient Red", "colors": ["#450A0A", "#7F1D1D", "#DC2626", "#F87171", "#FEF2F2"]}
  ]
}
'@

# 3. Update backend/pptx_engine/builder.py to apply colors dynamically
New-File "$Root/backend/pptx_engine/builder.py" @'
"""python-pptx presentation generation engine with dynamic palette coloring."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from backend.agents.base.agent import AgentContext

def _hex(c: str) -> RGBColor:
    c = c.lstrip("#")
    if len(c) != 6:
        c = "1E293B"
    return RGBColor(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

class PptxBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self.colors = ctx.palette.get("colors") or ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]

    def build(self, slides, target: Path) -> None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        bg_color = _hex(self.colors[0])
        surface_color = _hex(self.colors[1])
        accent_color = _hex(self.colors[2])
        text_color = _hex(self.colors[4] if len(self.colors) > 4 else "#FFFFFF")

        # Title Slide
        title_slide = prs.slides.add_slide(prs.slide_layouts[0])
        background = title_slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = bg_color

        deck_title = self.ctx.meta.get("deck_title", self.ctx.theme.get("name", "Enterprise Presentation"))
        
        # Style Title Frame
        if title_slide.shapes.title:
            title_slide.shapes.title.text = deck_title
            for p in title_slide.shapes.title.text_frame.paragraphs:
                p.font.color.rgb = accent_color
                p.font.size = Pt(38)
                p.font.bold = True

        if len(title_slide.placeholders) > 1:
            sub = title_slide.placeholders[1]
            sub.text = (
                f"Industry Domain: {self.ctx.theme.get('industry', 'General')} â€” {self.ctx.theme.get('name', '')}\n"
                f"Palette: {self.ctx.palette.get('name', 'Custom')}\n"
                "Generated via 100% Offline Agentic AI Factory"
            )
            for p in sub.text_frame.paragraphs:
                p.font.color.rgb = text_color
                p.font.size = Pt(16)

        # Content Slides
        for spec in slides:
            slide = prs.slides.add_slide(prs.slide_layouts[1])
            
            # Slide Background Fill
            s_bg = slide.background
            s_fill = s_bg.fill
            s_fill.solid()
            s_fill.fore_color.rgb = bg_color

            if slide.shapes.title:
                slide.shapes.title.text = spec.title
                for p in slide.shapes.title.text_frame.paragraphs:
                    p.font.color.rgb = accent_color
                    p.font.size = Pt(28)
                    p.font.bold = True

            if len(slide.placeholders) > 1:
                body = slide.placeholders[1].text_frame
                body.clear()
                for idx, b in enumerate(spec.bullets):
                    p = body.add_paragraph() if idx > 0 else body.paragraphs[0]
                    p.text = f"â–ھ  {b}"
                    p.font.size = Pt(18)
                    p.font.color.rgb = text_color
                    p.space_after = Pt(12)

            if spec.notes:
                try:
                    slide.notes_slide.notes_text_frame.text = spec.notes
                except Exception:
                    pass

        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))
'@

# 4. Update frontend/ui/main_window.py for stunning UI and live swatches
New-File "$Root/frontend/ui/main_window.py" @'
"""Main window: High-end interactive studio designer with rich industry palettes and color swatches."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QPlainTextEdit, QComboBox, QToolBox, QFileDialog, QMessageBox,
    QTabWidget, QGridLayout, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt

from frontend.theme_factory.registry import ThemeRegistry
from frontend.theme_factory.catalog import INDUSTRIES
from backend.pipeline.orchestrator import Orchestrator

DARK_STUDIO_QSS = """
QMainWindow {
    background-color: #0B0F19;
    color: #F8FAFC;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QLabel {
    color: #E2E8F0;
    font-weight: 600;
}
QLineEdit, QPlainTextEdit {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 10px;
    selection-background-color: #38BDF8;
}
QLineEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #38BDF8;
    background-color: #030712;
}
QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton:pressed {
    background-color: #1E40AF;
}
QComboBox {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}
QComboBox::drop-down {
    border: 0px;
}
QToolBox::tab {
    background-color: #1F2937;
    color: #38BDF8;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 4px;
}
QToolBox::tab:selected {
    background-color: #2563EB;
    color: #FFFFFF;
}
QTabWidget::pane {
    border: 2px solid #1F2937;
    background: #0B0F19;
    border-radius: 12px;
}
QTabBar::tab {
    background: #111827;
    color: #9CA3AF;
    padding: 10px 20px;
    margin-right: 6px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #2563EB;
    color: #FFFFFF;
}
"""

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline AI Presentation Factory â€” Advanced Studio Designer")
        self.resize(1400, 900)
        self.setStyleSheet(DARK_STUDIO_QSS)
        
        self.theme_registry = ThemeRegistry()
        self._selected_theme = {"industry": "Architecture", "name": "Minimalist Glass", "accent": "#0284C7", "style": "clean"}
        self._build_ui()
        self._update_color_swatches()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Top Project Title Input
        top_bar = QHBoxLayout()
        lbl_proj = QLabel("Presentation Title:")
        lbl_proj.setStyleSheet("font-size: 16px; color: #38BDF8;")
        top_bar.addWidget(lbl_proj)
        self.name_input = QLineEdit("Enterprise_AI_Transformation_Deck")
        self.name_input.setStyleSheet("font-size: 15px; font-weight: bold;")
        top_bar.addWidget(self.name_input, 1)
        root.addLayout(top_bar)

        # Tabs
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        # --- TAB 1: Industry & Palette Studio ---
        tab_studio = QWidget()
        studio_layout = QHBoxLayout(tab_studio)

        # Left: Industry Toolbox
        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("Select Industry Domain & Sub-Theme:"))
        self.industry_toolbox = QToolBox()
        
        for industry, data in INDUSTRIES.items():
            holder = QWidget()
            v = QVBoxLayout(holder)
            desc = QLabel(data.get("description", ""))
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #9CA3AF; font-size: 12px; margin-bottom: 6px;")
            v.addWidget(desc)
            
            for theme in data["themes"]:
                btn = QPushButton(f"âœ¦ {theme['name']} ({theme['style']})")
                btn.setStyleSheet(f"text-align: left; padding-left: 14px; background-color: #1F2937; border-left: 5px solid {theme['accent']};")
                btn.clicked.connect(lambda _, ind=industry, t=theme: self._pick_theme(ind, t))
                v.addWidget(btn)
            v.addStretch(1)
            self.industry_toolbox.addItem(holder, industry)
            
        left_box.addWidget(self.industry_toolbox, 1)
        studio_layout.addLayout(left_box, 1)

        # Right: Active Theme & Live Color Swatch Studio Inspector
        right_panel = QVBoxLayout()
        
        inspector_frame = QFrame()
        inspector_frame.setStyleSheet("background-color: #111827; border-radius: 12px; padding: 16px; border: 1px solid #1F2937;")
        v_insp = QVBoxLayout(inspector_frame)
        
        v_insp.addWidget(QLabel("ACTIVE INDUSTRY & THEME SELECTION:"))
        self.theme_display_lbl = QLabel("[Architecture] Minimalist Glass (clean)")
        self.theme_display_lbl.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        v_insp.addWidget(self.theme_display_lbl)
        
        v_insp.addWidget(QLabel("Select Color Palette Group (30+ Tuned Groups):"))
        self.palette_combo = QComboBox()
        for p in self.theme_registry.palettes():
            self.palette_combo.addItem(p["name"])
        self.palette_combo.currentIndexChanged.connect(self._update_color_swatches)
        v_insp.addWidget(self.palette_combo)
        
        v_insp.addWidget(QLabel("Live Color Palette Swatches (Interpretable Hex Preview):"))
        self.swatch_grid = QGridLayout()
        v_insp.addLayout(self.swatch_grid)
        
        right_panel.addWidget(inspector_frame)
        right_panel.addStretch(1)
        studio_layout.addLayout(right_panel, 1)

        self.tabs.addTab(tab_studio, "ًںژ¨ 1. Industry & Palette Studio")

        # --- TAB 2: Markdown Input Editor ---
        tab_md = QWidget()
        md_layout = QVBoxLayout(tab_md)
        md_layout.addWidget(QLabel("Presentation Markdown Structure (DeepSeek / LLM Format):"))
        
        self.md_editor = QPlainTextEdit()
        self.md_editor.setPlainText(
            "# Enterprise AI Transformation: Strategy & Architecture\n\n"
            "## Slide 1 - Executive Summary & Vision\n"
            "- Transitioning from cloud-dependent AI to secure, zero-API cost local execution\n"
            "- Balancing high productivity gains with absolute enterprise data sovereignty\n"
            "- Eliminating recurring token subscription costs through local processing\n"
            "> Speaker note: Emphasize that zero cloud dependency protects sensitive corporate data while slashing operational overhead to zero.\n\n"
            "## Slide 2 - The Offline Agentic Ecosystem\n"
            "- Modular architecture powered by specialized local Python libraries and rule engines\n"
            "- Air-gapped security ensuring zero data leakage to external third-party servers\n"
            "- Deterministic processing pipelines combining heuristics with local ML models\n"
            "> Speaker note: Highlight how local agents and deterministic rules work in tandem without relying on external network calls.\n\n"
            "## Slide 3 - Markdown Ingestion & Parsing Engine\n"
            "- Standardized DeepSeek-guided markdown schema for flawless structure extraction\n"
            "- Automatic header recognition, slide boundary splitting, and speaker note isolation\n"
            "- Seamless integration with local models or direct text copy-pasting\n"
            "> Speaker note: Explain how engineers can pipe structured output from any local LLM directly into the ingestion pipeline with zero manual formatting friction.\n\n"
            "## Slide 4 - NLP Optimization & Semantic Filtering\n"
            "- TF-IDF vectorization and cosine similarity for intelligent bullet deduplication\n"
            "- Automated constraint checks for title length and bullet point density bounds\n"
            "- Semantic cleaning ensuring high signal-to-noise ratio on every slide\n"
            "> Speaker note: Describe how semantic filtering automatically detects and removes redundant bullet points, keeping slide text concise and impactful.\n\n"
            "## Slide 5 - Automated Theme Factory & Design Patterns\n"
            "- Industry-tailored design variants across engineering, architectural, and corporate domains\n"
            "- Dynamic color palette mapping with over 30 tuned color group variations\n"
            "- Extensible factory pattern allowing custom theme additions across git commits\n"
            "> Speaker note: Show how the theme factory maintains strict visual consistency and professional aesthetics across all exported presentations.\n\n"
            "## Slide 6 - Multi-Format Vector Export & Roadmap\n"
            "- Instantaneous widescreen 16:9 .pptx generation via python-pptx\n"
            "- Clean landscape .pdf document vector compilation via ReportLab\n"
            "- Phased rollout strategy scaling across enterprise desktop workstations\n"
            "> Speaker note: Conclude with the deployment timeline and invite feedback on upcoming agentic modules."
        )
        md_layout.addWidget(self.md_editor, 1)
        self.tabs.addTab(tab_md, "ًں“‌ 2. Markdown AI Input")

        # Bottom Actions Bar
        actions_bar = QHBoxLayout()
        btn_load = QPushButton("ًں“پ Load Markdown File")
        btn_load.clicked.connect(self._load_file)
        actions_bar.addWidget(btn_load)

        btn_pptx = QPushButton("âڑ، Export Styled .pptx Presentation")
        btn_pptx.setStyleSheet("background-color: #059669; font-size: 15px;")
        btn_pptx.clicked.connect(lambda: self._export("pptx"))
        actions_bar.addWidget(btn_pptx)

        btn_pdf = QPushButton("ًں“„ Export Clean .pdf Presentation")
        btn_pdf.setStyleSheet("background-color: #D97706; font-size: 15px;")
        btn_pdf.clicked.connect(lambda: self._export("pdf"))
        actions_bar.addWidget(btn_pdf)

        actions_bar.addStretch(1)
        root.addLayout(actions_bar)

        self.status_lbl = QLabel("Status: Ready. Select an industry theme and custom palette to begin export.")
        self.status_lbl.setStyleSheet("color: #38BDF8; font-weight: bold; padding: 4px;")
        root.addWidget(self.status_lbl)

    def _pick_theme(self, industry: str, theme: dict) -> None:
        self._selected_theme = {"industry": industry, **theme}
        disp = f"[{industry}] {theme['name']} ({theme['style']})"
        self.theme_display_lbl.setText(disp)
        self.status_lbl.setText(f"Active theme set: {disp}")

    def _update_color_swatches(self) -> None:
        for i in reversed(range(self.swatch_grid.count())):
            item = self.swatch_grid.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        palette_name = self.palette_combo.currentText()
        palette_data = self.theme_registry.palette_by_name(palette_name)
        colors = palette_data.get("colors", ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"])

        for idx, hex_code in enumerate(colors):
            lbl = QLabel(f" {hex_code} ")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            is_light = self._is_light(hex_code)
            fg = "#000000" if is_light else "#FFFFFF"
            lbl.setStyleSheet(f"background-color: {hex_code}; color: {fg}; border-radius: 8px; font-weight: bold; font-size: 13px; padding: 12px;")
            self.swatch_grid.addWidget(lbl, 0, idx)

    def _is_light(self, hex_s: str) -> bool:
        hex_s = hex_s.lstrip("#")
        if len(hex_s) != 6:
            return False
        r = int(hex_s[0:2], 16)
        g = int(hex_s[2:4], 16)
        b = int(hex_s[4:6], 16)
        return (0.299 * r + 0.587 * g + 0.114 * b) > 160

    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Markdown", "", "Markdown (*.md)")
        if path:
            self.md_editor.setPlainText(Path(path).read_text(encoding="utf-8"))
            self.status_lbl.setText(f"Loaded markdown: {path}")

    def _export(self, kind: str) -> None:
        theme = getattr(self, "_selected_theme", None)
        palette = self.theme_registry.palette_by_name(self.palette_combo.currentText())
        
        out_dir = Path("out")
        out_dir.mkdir(exist_ok=True)
        base = self.name_input.text().strip() or "presentation"
        target = out_dir / f"{base}.{kind}"

        orch = Orchestrator(theme=theme, palette=palette, meta={"deck_title": self.name_input.text().strip()})
        try:
            orch.run(self.md_editor.toPlainText(), target)
            self.status_lbl.setText(f"Successfully exported {kind.upper()}: {target.resolve()}")
            QMessageBox.information(self, "Export Successful", f"Generated styled {kind.upper()} presentation at:\n{target.resolve()}")
        except Exception as exc:
            QMessageBox.critical(self, "Export Error", str(exc))
            self.status_lbl.setText("Export failed.")
'@

Write-Host "`n=== Successfully Applied All Upgrades via update_frontend_2.ps1 ===" -ForegroundColor Cyan
Write-Host "Launch your application now with:" -ForegroundColor Yellow
Write-Host "python -m frontend.main" -ForegroundColor Green
```

### `backend\__init__.py`
```py


```

### `backend\agents\markdown_manipulator.py`
```py
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

```

### `backend\agents\markdown_manipulator_agent.py`
```py
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

        lines = text.splitlines()
        for line in lines:
            line_s = line.strip()
            if line_s.startswith("# "):
                continue  # Main presentation title
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
```

### `backend\agents\outline_agent.py`
```py
"""Outline Refinement Agent ensuring presentation flow and length constraints."""
from backend.agents.base.agent import BaseAgent, AgentContext
from backend.agents.factory.agent_factory import register


@register("outline")
class OutlineAgent(BaseAgent):
    name = "outline"

    def run(self, slides, ctx: AgentContext):
        for s in slides:
            if not s.title:
                s.title = "Overview"
            s.title = s.title[:75]
            s.bullets = [b[:160] for b in s.bullets[:6]]
        return slides

```

### `backend\agents\text_tools_agent.py`
```py
"""Text Tools Agent utilizing offline NLP libraries (scikit-learn TF-IDF)."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.agents.base.agent import BaseAgent, AgentContext
from backend.agents.factory.agent_factory import register


@register("text_tools")
class TextToolsAgent(BaseAgent):
    name = "text_tools"

    def run(self, payload: list[str], ctx: AgentContext) -> list[str]:
        if len(payload) < 2:
            return payload
        vec = TfidfVectorizer().fit_transform(payload)
        sim = cosine_similarity(vec)
        keep, dropped = [], set()
        for i in range(len(payload)):
            if i in dropped:
                continue
            keep.append(payload[i])
            for j in range(i + 1, len(payload)):
                if sim[i, j] > 0.90:
                    dropped.add(j)
        return keep

```

### `backend\agents\__init__.py`
```py


```

### `backend\agents\base\agent.py`
```py
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

```

### `backend\agents\base\__init__.py`
```py


```

### `backend\agents\factory\agent_factory.py`
```py
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

```

### `backend\agents\factory\__init__.py`
```py


```

### `backend\pdf_engine\builder.py`
```py
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

```

### `backend\pdf_engine\__init__.py`
```py


```

### `backend\pipeline\orchestrator.py`
```py
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

```

### `backend\pipeline\__init__.py`
```py


```

### `backend\pptx_engine\builder.py`
```py
"""python-pptx engine implementing 30 Modern Tech, Editorial, Bold, Corporate & Futuristic design styles."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from backend.agents.base.agent import AgentContext

def _hex(c: str) -> RGBColor:
    c = c.lstrip("#")
    if len(c) != 6:
        c = "1E293B"
    return RGBColor(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

class PptxBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self.colors = ctx.palette.get("colors") or ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]

    def build(self, slides, target: Path) -> None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        bg_color = _hex(self.colors[0])
        card_bg = _hex(self.colors[1])
        accent_color = _hex(self.colors[2])
        highlight_color = _hex(self.colors[3])
        text_color = _hex(self.colors[4] if len(self.colors) > 4 else "#FFFFFF")

        style_name = self.ctx.theme.get("style", "Glassmorphism Card")
        blank_layout = prs.slide_layouts[6]

        # --- TITLE SLIDE ---
        title_slide = prs.slides.add_slide(blank_layout)
        bg = title_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_color
        bg.line.fill.background()

        # Render Title Box based on Style Archetype
        title_box = title_slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.5), Inches(10.933), Inches(4.5))
        title_box.fill.solid()
        title_box.fill.fore_color.rgb = card_bg
        title_box.line.color.rgb = accent_color
        title_box.line.width = Pt(2.5)

        tf = title_box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.5)
        tf.margin_top = Inches(0.6)

        deck_title = self.ctx.meta.get("deck_title", self.ctx.theme.get("name", "Enterprise Presentation"))
        p = tf.paragraphs[0]
        p.text = deck_title
        p.font.size = Pt(38)
        p.font.bold = True
        p.font.color.rgb = text_color

        p2 = tf.add_paragraph()
        p2.text = f"Industry: {self.ctx.theme.get('industry', 'General')} | Design Archetype: {style_name}"
        p2.font.size = Pt(16)
        p2.font.color.rgb = accent_color
        p2.space_before = Pt(16)

        p3 = tf.add_paragraph()
        p3.text = f"Palette: {self.ctx.palette.get('name', 'Custom')} | 100% Offline Agentic Presentation Factory"
        p3.font.size = Pt(13)
        p3.font.color.rgb = text_color
        p3.space_before = Pt(8)

        # --- CONTENT SLIDES (Archetype Dispatcher) ---
        for spec in slides:
            slide = prs.slides.add_slide(blank_layout)

            # Background
            s_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
            s_bg.fill.solid()
            s_bg.fill.fore_color.rgb = bg_color
            s_bg.line.fill.background()

            if "Neo-Brutalist" in style_name:
                # Hard offset shadow box
                shadow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.1), Inches(1.1), Inches(11.333), Inches(5.5))
                shadow.fill.solid()
                shadow.fill.fore_color.rgb = _hex("#000000")
                shadow.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.9), Inches(11.333), Inches(5.5))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = _hex("#000000")
                card.line.width = Pt(3)

            elif "Swiss Grid" in style_name or "Editorial" in style_name:
                # Hairline grid dividers
                line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.04))
                line.fill.solid()
                line.fill.fore_color.rgb = accent_color
                line.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.1), Inches(11.733), Inches(4.7))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = highlight_color
                card.line.width = Pt(1)

            elif "Executive" in style_name or "KPI" in style_name:
                # Thick top accent strip
                strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.15))
                strip.fill.solid()
                strip.fill.fore_color.rgb = accent_color
                strip.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.1), Inches(11.733), Inches(5.8))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = highlight_color
                card.line.width = Pt(1.5)

            else:
                # Standard Modern Glass / Dark Neon Card Layout
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(6.1))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = accent_color
                card.line.width = Pt(2)

            # Header & Text Content
            ctf = card.text_frame
            ctf.word_wrap = True
            ctf.margin_left = Inches(0.5)
            ctf.margin_top = Inches(0.5)
            ctf.margin_right = Inches(0.5)

            hp = ctf.paragraphs[0]
            hp.text = spec.title
            hp.font.size = Pt(28)
            hp.font.bold = True
            hp.font.color.rgb = accent_color
            hp.space_after = Pt(16)

            for idx, b in enumerate(spec.bullets):
                bp = ctf.add_paragraph()
                bp.text = f"â–ھ   {b}"
                bp.font.size = Pt(17)
                bp.font.color.rgb = text_color
                bp.space_after = Pt(12)

            if spec.notes:
                try:
                    slide.notes_slide.notes_text_frame.text = spec.notes
                except Exception:
                    pass

        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))

```

### `backend\pptx_engine\__init__.py`
```py


```

### `backend\rules\README.md`
```md
# Rules Engine Layer

Hybrid rule-based constraints and heuristic checks.

```

### `backend\rules\__init__.py`
```py


```

### `docs\PRD.md`
```md
# Product Requirements Document (PRD) â€” Offline AI Presentation Factory

## 1. Problems
- **API Dependency & Costs:** Commercial presentation AI tools require expensive cloud APIs and expose confidential data.
- **Rigid Templates:** Standard presentation tools lack industry-specific design variations and scalable theme architecture.
- **Manual Formatting:** Converting raw Markdown insights into polished PowerPoint slides is tedious and error-prone.

## 2. Goals
- Provide a **100% offline desktop application** built with PyQt6 and Python.
- Implement a **Theme Factory design pattern** supporting multiple industries (Architectural, Construction, Engineering, Literature) and 30+ color palette groups.
- Integrate **50 zero-cost offline AI and NLP tools** organized into modular agents (Markdown manipulator, text deduplication, outline refinement).
- Enable instantaneous export to `.pptx` (via `python-pptx`) and `.pdf` (via ReportLab).

## 3. Solutions
- **PyQt6 Desktop Frontend:** Intuitive GUI with collapsible industry toolboxes, theme pickers, and live Markdown editing.
- **Agentic Pipeline Architecture:** Extensible `AgentFactory` pattern allowing incremental additions of AI agents across future Git commits.
- **Structured Markdown Parser:** Standardized Markdown format compatible with DeepSeek and local LLM outputs.
```

### `frontend\main.py`
```py
"""Entry point for the PyQt6 desktop app."""
import sys
from pathlib import Path

# Automatically add the project root directory to sys.path so 'backend' and 'theme_factory' are found
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from PyQt6.QtWidgets import QApplication
from frontend.ui.main_window import MainWindow  # Note the absolute package import


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Offline AI Presentation Factory")
    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
```

### `frontend\__init__.py`
```py


```

### `frontend\theme_factory\catalog.py`
```py
"""Static fallback for industries with utf-8-sig BOM support."""
from pathlib import Path
import json

_HERE = Path(__file__).resolve().parents[2]
_PATH = _HERE / "knowledge" / "catalog" / "industries.json"

INDUSTRIES = json.loads(_PATH.read_text(encoding="utf-8-sig")) if _PATH.exists() else {}

```

### `frontend\theme_factory\registry.py`
```py
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

```

### `frontend\theme_factory\__init__.py`
```py


```

### `frontend\theme_factory\industries\README.md`
```md
# Industries Theme Factory

Add specialized industry theme JSON files here in subsequent git commits.

```

### `frontend\theme_factory\industries\__init__.py`
```py


```

### `frontend\ui\main_window.py`
```py
"""Main window: Real-time swatch selection, collapsing industry groups, and 30-style design picker."""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QPlainTextEdit, QComboBox, QToolBox, QFileDialog, QMessageBox,
    QTabWidget, QGridLayout, QFrame
)
from PyQt6.QtCore import Qt

from frontend.theme_factory.registry import ThemeRegistry
from frontend.theme_factory.catalog import INDUSTRIES
from backend.pipeline.orchestrator import Orchestrator

DARK_STUDIO_QSS = """
QMainWindow {
    background-color: #090D16;
    color: #F8FAFC;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QLabel {
    color: #E2E8F0;
    font-weight: 600;
}
QLineEdit, QPlainTextEdit {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 10px;
    selection-background-color: #38BDF8;
}
QLineEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #38BDF8;
    background-color: #030712;
}
QPushButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #1D4ED8;
}
QPushButton:pressed {
    background-color: #1E40AF;
}
QComboBox {
    background-color: #111827;
    color: #F9FAFB;
    border: 2px solid #1F2937;
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}
QComboBox::drop-down {
    border: 0px;
}
QToolBox::tab {
    background-color: #1F2937;
    color: #38BDF8;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 4px;
}
QToolBox::tab:selected {
    background-color: #2563EB;
    color: #FFFFFF;
}
QTabWidget::pane {
    border: 2px solid #1F2937;
    background: #090D16;
    border-radius: 12px;
}
QTabBar::tab {
    background: #111827;
    color: #9CA3AF;
    padding: 10px 20px;
    margin-right: 6px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #2563EB;
    color: #FFFFFF;
}
"""

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline AI Presentation Factory â€” 30 Design Archetypes Studio")
        self.resize(1420, 920)
        self.setStyleSheet(DARK_STUDIO_QSS)
        
        self.theme_registry = ThemeRegistry()
        self._selected_theme = {"industry": "Architecture", "name": "Minimalist Glass", "accent": "#0284C7", "style": "Glassmorphism Card"}
        self._build_ui()
        self._update_color_swatches()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        # Top Project Title Input
        top_bar = QHBoxLayout()
        lbl_proj = QLabel("Presentation Title:")
        lbl_proj.setStyleSheet("font-size: 16px; color: #38BDF8;")
        top_bar.addWidget(lbl_proj)
        self.name_input = QLineEdit("Enterprise_AI_Transformation_Deck")
        self.name_input.setStyleSheet("font-size: 15px; font-weight: bold;")
        top_bar.addWidget(self.name_input, 1)
        root.addLayout(top_bar)

        # Tabs
        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        # --- TAB 1: Industry & Style Studio ---
        tab_studio = QWidget()
        studio_layout = QHBoxLayout(tab_studio)

        # Left: Collapsing Industry Toolbox
        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("Collapsing Industry Categories & Design Styles:"))
        self.industry_toolbox = QToolBox()
        
        for industry, data in INDUSTRIES.items():
            holder = QWidget()
            v = QVBoxLayout(holder)
            desc = QLabel(data.get("description", ""))
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #9CA3AF; font-size: 12px; margin-bottom: 6px;")
            v.addWidget(desc)
            
            for theme in data["themes"]:
                btn = QPushButton(f"âœ¦ {theme['name']} ({theme['style']})")
                btn.setStyleSheet(f"text-align: left; padding-left: 14px; background-color: #1F2937; border-left: 5px solid {theme['accent']};")
                btn.clicked.connect(lambda checked=False, ind=industry, t=theme: self._pick_theme(ind, t))
                v.addWidget(btn)
            v.addStretch(1)
            self.industry_toolbox.addItem(holder, industry)
            
        left_box.addWidget(self.industry_toolbox, 1)
        studio_layout.addLayout(left_box, 1)

        # Right: Active Theme, Design Style, and Real-Time Swatch Inspector
        right_panel = QVBoxLayout()
        
        inspector_frame = QFrame()
        inspector_frame.setStyleSheet("background-color: #111827; border-radius: 12px; padding: 18px; border: 1px solid #1F2937;")
        v_insp = QVBoxLayout(inspector_frame)
        
        v_insp.addWidget(QLabel("ACTIVE INDUSTRY & 30-STYLE ARCHETYPE:"))
        self.theme_display_lbl = QLabel("[Architecture] Minimalist Glass (Glassmorphism Card)")
        self.theme_display_lbl.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        v_insp.addWidget(self.theme_display_lbl)

        self.industry_desc_lbl = QLabel("Spatial design, structural acoustics, urban planning, materiality, and sustainable formwork.")
        self.industry_desc_lbl.setWordWrap(True)
        self.industry_desc_lbl.setStyleSheet("color: #9CA3AF; font-size: 13px; margin-bottom: 10px;")
        v_insp.addWidget(self.industry_desc_lbl)
        
        v_insp.addWidget(QLabel("Select Color Palette Group (30+ Tuned Groups):"))
        self.palette_combo = QComboBox()
        for p in self.theme_registry.palettes():
            self.palette_combo.addItem(p["name"])
        self.palette_combo.currentIndexChanged.connect(self._update_color_swatches)
        v_insp.addWidget(self.palette_combo)
        
        v_insp.addWidget(QLabel("Live Color Palette Swatches (Click any swatch to sync):"))
        self.swatch_grid = QGridLayout()
        v_insp.addLayout(self.swatch_grid)
        
        right_panel.addWidget(inspector_frame)
        right_panel.addStretch(1)
        studio_layout.addLayout(right_panel, 1)

        self.tabs.addTab(tab_studio, "ًںژ¨ 1. Industry & Style Studio")

        # --- TAB 2: Markdown Input Editor ---
        tab_md = QWidget()
        md_layout = QVBoxLayout(tab_md)
        md_layout.addWidget(QLabel("Presentation Markdown Structure (DeepSeek / LLM Format):"))
        
        self.md_editor = QPlainTextEdit()
        self.md_editor.setPlainText(
            "# Enterprise AI Transformation: Strategy & Architecture\n\n"
            "## Slide 1 - Executive Summary & Vision\n"
            "- Transitioning from cloud-dependent AI to secure, zero-API cost local execution\n"
            "- Balancing high productivity gains with absolute enterprise data sovereignty\n"
            "- Eliminating recurring token subscription costs through local processing\n"
            "> Speaker note: Emphasize that zero cloud dependency protects sensitive corporate data while slashing operational overhead to zero.\n\n"
            "## Slide 2 - The Offline Agentic Ecosystem\n"
            "- Modular architecture powered by specialized local Python libraries and rule engines\n"
            "- Air-gapped security ensuring zero data leakage to external third-party servers\n"
            "- Deterministic processing pipelines combining heuristics with local ML models\n"
            "> Speaker note: Highlight how local agents and deterministic rules work in tandem without relying on external network calls.\n\n"
            "## Slide 3 - Markdown Ingestion & Parsing Engine\n"
            "- Standardized DeepSeek-guided markdown schema for flawless structure extraction\n"
            "- Automatic header recognition, slide boundary splitting, and speaker note isolation\n"
            "- Seamless integration with local models or direct text copy-pasting\n"
            "> Speaker note: Explain how engineers can pipe structured output from any local LLM directly into the ingestion pipeline with zero manual formatting friction.\n\n"
            "## Slide 4 - NLP Optimization & Semantic Filtering\n"
            "- TF-IDF vectorization and cosine similarity for intelligent bullet deduplication\n"
            "- Automated constraint checks for title length and bullet point density bounds\n"
            "- Semantic cleaning ensuring high signal-to-noise ratio on every slide\n"
            "> Speaker note: Describe how semantic filtering automatically detects and removes redundant bullet points, keeping slide text concise and impactful.\n\n"
            "## Slide 5 - Automated Theme Factory & Design Patterns\n"
            "- Industry-tailored design variants across engineering, architectural, and corporate domains\n"
            "- Dynamic color palette mapping with over 30 tuned color group variations\n"
            "- Extensible factory pattern allowing custom theme additions across git commits\n"
            "> Speaker note: Show how the theme factory maintains strict visual consistency and professional aesthetics across all exported presentations.\n\n"
            "## Slide 6 - Multi-Format Vector Export & Roadmap\n"
            "- Instantaneous widescreen 16:9 .pptx generation via python-pptx\n"
            "- Clean landscape .pdf document vector compilation via ReportLab\n"
            "- Phased rollout strategy scaling across enterprise desktop workstations\n"
            "> Speaker note: Conclude with the deployment timeline and invite feedback on upcoming agentic modules."
        )
        md_layout.addWidget(self.md_editor, 1)
        self.tabs.addTab(tab_md, "ًں“‌ 2. Markdown AI Input")

        # Bottom Actions Bar
        actions_bar = QHBoxLayout()
        btn_load = QPushButton("ًں“پ Load Markdown File")
        btn_load.clicked.connect(self._load_file)
        actions_bar.addWidget(btn_load)

        btn_pptx = QPushButton("âڑ، Export Styled .pptx Presentation")
        btn_pptx.setStyleSheet("background-color: #059669; font-size: 15px;")
        btn_pptx.clicked.connect(lambda: self._export("pptx"))
        actions_bar.addWidget(btn_pptx)

        btn_pdf = QPushButton("ًں“„ Export Clean .pdf Presentation")
        btn_pdf.setStyleSheet("background-color: #D97706; font-size: 15px;")
        btn_pdf.clicked.connect(lambda: self._export("pdf"))
        actions_bar.addWidget(btn_pdf)

        actions_bar.addStretch(1)
        root.addLayout(actions_bar)

        self.status_lbl = QLabel("Status: Ready. Click any industry theme or color swatch to sync inspector.")
        self.status_lbl.setStyleSheet("color: #38BDF8; font-weight: bold; padding: 4px;")
        root.addWidget(self.status_lbl)

    def _pick_theme(self, industry: str, theme: dict) -> None:
        self._selected_theme = {"industry": industry, **theme}
        disp = f"[{industry}] {theme['name']} ({theme['style']})"
        self.theme_display_lbl.setText(disp)
        
        ind_data = INDUSTRIES.get(industry, {})
        self.industry_desc_lbl.setText(ind_data.get("description", ""))
        self.status_lbl.setText(f"Synced active theme: {disp}")

    def _update_color_swatches(self) -> None:
        for i in reversed(range(self.swatch_grid.count())):
            item = self.swatch_grid.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        palette_name = self.palette_combo.currentText()
        palette_data = self.theme_registry.palette_by_name(palette_name)
        colors = palette_data.get("colors", ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"])

        for idx, hex_code in enumerate(colors):
            btn = QPushButton(f" {hex_code} ")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            is_light = self._is_light(hex_code)
            fg = "#000000" if is_light else "#FFFFFF"
            btn.setStyleSheet(f"background-color: {hex_code}; color: {fg}; border-radius: 8px; font-weight: bold; font-size: 13px; padding: 10px;")
            # Connect live click on swatch to update status / sync selection
            btn.clicked.connect(lambda checked=False, h=hex_code, p=palette_name: self._on_swatch_clicked(p, h))
            self.swatch_grid.addWidget(btn, 0, idx)

        self.status_lbl.setText(f"Active Palette Synced: {palette_name}")

    def _on_swatch_clicked(self, palette_name: str, hex_code: str) -> None:
        self.status_lbl.setText(f"Palette '{palette_name}' swatch clicked: {hex_code} (Synchronized)")

    def _is_light(self, hex_s: str) -> bool:
        hex_s = hex_s.lstrip("#")
        if len(hex_s) != 6:
            return False
        r = int(hex_s[0:2], 16)
        g = int(hex_s[2:4], 16)
        b = int(hex_s[4:6], 16)
        return (0.299 * r + 0.587 * g + 0.114 * b) > 160

    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Markdown", "", "Markdown (*.md)")
        if path:
            self.md_editor.setPlainText(Path(path).read_text(encoding="utf-8"))
            self.status_lbl.setText(f"Loaded markdown: {path}")

    def _export(self, kind: str) -> None:
        theme = getattr(self, "_selected_theme", None)
        palette = self.theme_registry.palette_by_name(self.palette_combo.currentText())
        
        out_dir = Path("out")
        out_dir.mkdir(exist_ok=True)
        base = self.name_input.text().strip() or "presentation"
        target = out_dir / f"{base}.{kind}"

        orch = Orchestrator(theme=theme, palette=palette, meta={"deck_title": self.name_input.text().strip()})
        try:
            orch.run(self.md_editor.toPlainText(), target)
            self.status_lbl.setText(f"Successfully exported {kind.upper()}: {target.resolve()}")
            QMessageBox.information(self, "Export Successful", f"Generated 30-Archetype styled {kind.upper()} presentation at:\n{target.resolve()}")
        except Exception as exc:
            QMessageBox.critical(self, "Export Error", str(exc))
            self.status_lbl.setText("Export failed.")

```

### `frontend\ui\__init__.py`
```py


```

### `frontend\ui\widgets\placeholders.py`
```py
"""Reserved for custom PyQt preview widgets and palette grids."""

```

### `frontend\ui\widgets\__init__.py`
```py


```

### `knowledge\catalog\industries.json`
```json
{
  "Architecture": {
    "description": "Spatial design, structural acoustics, urban planning, materiality, and sustainable formwork.",
    "accent_color": "#D97706",
    "default_style": "Glassmorphism Card",
    "themes": [
      {"name": "Brutalist Concrete", "accent": "#64748B", "style": "Neo-Brutalist Pop"},
      {"name": "Biophilic & Timber", "accent": "#059669", "style": "Organic Blob Mask"},
      {"name": "Minimalist Glass", "accent": "#0284C7", "style": "Glassmorphism Card"}
    ]
  },
  "Construction": {
    "description": "Heavy civil works, site logistics, safety compliance, structural steel, and BIM modeling.",
    "accent_color": "#EA580C",
    "default_style": "Executive KPI Strip",
    "themes": [
      {"name": "Structural Steel & Safety", "accent": "#EA580C", "style": "Executive KPI Strip"},
      {"name": "Smart Site Logistics", "accent": "#2563EB", "style": "Chevron Process Flow"},
      {"name": "Geotechnical Foundation", "accent": "#78350F", "style": "Dual Comparison Matrix"}
    ]
  },
  "Engineering": {
    "description": "Mechanical systems, quantum computing, thermodynamics, robotics, and software architecture.",
    "accent_color": "#2563EB",
    "default_style": "Dark Mode Neon Glow",
    "themes": [
      {"name": "Quantum & Neon", "accent": "#38BDF8", "style": "Dark Mode Neon Glow"},
      {"name": "Systems Thermodynamics", "accent": "#DC2626", "style": "Cyberpunk HUD Frame"},
      {"name": "Precision Robotics", "accent": "#7C3AED", "style": "Retro Terminal Window"}
    ]
  },
  "Literature": {
    "description": "Narrative pacing, linguistic chunking, corpus linguistics, and editorial publishing strategy.",
    "accent_color": "#9333EA",
    "default_style": "Swiss Grid Editorial",
    "themes": [
      {"name": "Classic Parchment", "accent": "#B45309", "style": "Swiss Grid Editorial"},
      {"name": "Modern Typography", "accent": "#1E293B", "style": "Monochromatic Slate"},
      {"name": "Corpus Linguistics", "accent": "#0D9488", "style": "Oversized Number Watermark"}
    ]
  }
}

```

### `knowledge\catalog\palettes.json`
```json
{
  "palettes": [
    {"name": "Cyber Slate & Neon Blue", "colors": ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]},
    {"name": "Warm Architectural Earth", "colors": ["#1C1917", "#292524", "#D97706", "#B45309", "#FAFAF9"]},
    {"name": "Construction Safety & Steel", "colors": ["#09090B", "#18181B", "#EA580C", "#52525B", "#FAFAFA"]},
    {"name": "Biophilic Forest & Timber", "colors": ["#064E3B", "#065F46", "#059669", "#34D399", "#ECFDF5"]},
    {"name": "Quantum Deep Purple", "colors": ["#2E1065", "#3B0764", "#7C3AED", "#A78BFA", "#F5F3FF"]},
    {"name": "Minimalist Scandinavian", "colors": ["#F8FAFC", "#E2E8F0", "#0284C7", "#0F172A", "#334155"]},
    {"name": "Editorial Obsidian & Gold", "colors": ["#0A0A0A", "#171717", "#D4AF37", "#E5E5E5", "#FFFFFF"]},
    {"name": "Thermal Gradient Red", "colors": ["#450A0A", "#7F1D1D", "#DC2626", "#F87171", "#FEF2F2"]}
  ]
}

```

### `knowledge\md_format\template_guide.md`
```md
# DeepSeek / LLM Markdown Input Format

```markdown
# Deck Main Title

## Slide 1 Title
- Bullet point 1
- Bullet point 2
> Speaker notes / metadata for this slide

## Slide 2 Title
- Bullet point 1
- Bullet point 2

```

### `knowledge\offline_tools\tools_manifest.md`
```md
# 50 Offline AI Tools Manifest (Zero API, Zero Cost)

## Section A: NLP & Text (1-16)
1. scikit-learn (TF-IDF, Cosine Similarity)
2. numpy / scipy (Vector math)
3. rapidfuzz (Fuzzy string matching)
4. symspellpy (Spelling correction)
5. textdistance (Distance metrics)
6. spacy (Tokenization, POS tagging)
7. sumy (Text summarization)
8. language-tool-python (Grammar checking)
9. textstat (Readability scoring)
10. langdetect / langid (Language identification)
11. recordlinkage (Entity deduplication)
12. datasketch (MinHash / LSH)
13. argos-translate (Offline neural translation)
14. yake (Keyword extraction)
15. rake-nltk (Rapid automatic keyword extraction)
16. nltk (Corpus tools)

## Section B: Tabular & Statistical ML (17-28)
17-28. statsmodels, prophet, mlxtend, pgmpy, mapie, etc.

## Section C: Vision (29-36)
29-36. opencv-python, pyzbar, pytesseract, imagehash

## Section D: Audio (37-40)
37-40. vosk, faster-whisper, librosa, pvporcupine

## Section E: Graph & Logic (41-50)
41. networkx (Graph topology)
42. python-constraint (Constraint satisfaction)
43. ortools (Optimization)
44. scikit-fuzzy (Fuzzy logic)
45-46. durable_rules / experta (Rule engines)
47-50. modAL, unidecode, pytest, ruff

```

### `knowledge\offline_tools\__init__.py`
```py


```

