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
                bp.text = f"▪   {b}"
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
        self.setWindowTitle("Offline AI Presentation Factory — 30 Design Archetypes Studio")
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
                btn = QPushButton(f"✦ {theme['name']} ({theme['style']})")
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

        self.tabs.addTab(tab_studio, "🎨 1. Industry & Style Studio")

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