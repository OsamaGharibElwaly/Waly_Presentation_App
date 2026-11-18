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
        p2.text = f"Industry Domain: {self.ctx.theme.get('industry', 'General')} — {self.ctx.theme.get('name', '')} ({self.ctx.theme.get('style', 'modern')})"
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
                cp.text = f"▪   {b}"
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
        self.setWindowTitle("Offline AI Presentation Factory — Advanced Studio Designer")
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
                btn = QPushButton(f"✦ {theme['name']} ({theme['style']})")
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

        self.tabs.addTab(tab_studio, "🎨 1. Industry & Palette Studio")

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
        self.tabs.addTab(tab_md, "📝 2. Markdown AI Input")

        # Bottom Actions Bar
        actions_bar = QHBoxLayout()
        btn_load = QPushButton("📁 Load Markdown File")
        btn_load.clicked.connect(self._load_file)
        actions_bar.addWidget(btn_load)

        btn_pptx = QPushButton("⚡ Export Styled .pptx Presentation")
        btn_pptx.setStyleSheet("background-color: #059669; font-size: 15px;")
        btn_pptx.clicked.connect(lambda: self._export("pptx"))
        actions_bar.addWidget(btn_pptx)

        btn_pdf = QPushButton("📄 Export Clean .pdf Presentation")
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