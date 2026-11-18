"""Main window: Fully synchronized studio inspector, color swatches, archetypes, and animation choreography."""
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
        self.setWindowTitle("Offline AI Presentation Factory â€” Pareto 30-Archetype Studio")
        self.resize(1420, 920)
        self.setStyleSheet(DARK_STUDIO_QSS)
        
        self.theme_registry = ThemeRegistry()
        self._selected_theme = {"industry": "Architecture", "name": "Minimalist Glass", "accent": "#0284C7", "style": "glassmorphism_card", "animation": "progressive_bullet_reveal"}
        self._build_ui()
        self._update_color_swatches()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        top_bar = QHBoxLayout()
        lbl_proj = QLabel("Presentation Title:")
        lbl_proj.setStyleSheet("font-size: 16px; color: #38BDF8;")
        top_bar.addWidget(lbl_proj)
        self.name_input = QLineEdit("Enterprise_AI_Transformation_Deck")
        self.name_input.setStyleSheet("font-size: 15px; font-weight: bold;")
        top_bar.addWidget(self.name_input, 1)
        root.addLayout(top_bar)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        # --- TAB 1: Industry & Style Studio ---
        tab_studio = QWidget()
        studio_layout = QHBoxLayout(tab_studio)

        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("Collapsing Industry Categories & Design Archetypes:"))
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

        right_panel = QVBoxLayout()
        
        inspector_frame = QFrame()
        inspector_frame.setStyleSheet("background-color: #111827; border-radius: 12px; padding: 18px; border: 1px solid #1F2937;")
        v_insp = QVBoxLayout(inspector_frame)
        
        v_insp.addWidget(QLabel("ACTIVE INDUSTRY & ARCHETYPE INSPECTOR:"))
        self.theme_display_lbl = QLabel("[Architecture] Minimalist Glass (glassmorphism_card)")
        self.theme_display_lbl.setStyleSheet("color: #38BDF8; font-size: 18px; font-weight: bold;")
        v_insp.addWidget(self.theme_display_lbl)

        self.anim_display_lbl = QLabel("Animation Choreography: progressive_bullet_reveal")
        self.anim_display_lbl.setStyleSheet("color: #34D399; font-size: 14px; font-weight: bold;")
        v_insp.addWidget(self.anim_display_lbl)

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
        
        v_insp.addWidget(QLabel("Live Color Palette Swatches (Click swatch to sync):"))
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
        self.anim_display_lbl.setText(f"Animation Choreography: {theme.get('animation', 'progressive_bullet_reveal')}")
        
        ind_data = INDUSTRIES.get(industry, {})
        self.industry_desc_lbl.setText(ind_data.get("description", ""))
        self.status_lbl.setText(f"Synced active theme & choreography: {disp}")

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
            QMessageBox.information(self, "Export Successful", f"Generated 30-Archetype styled {kind.upper()} presentation with OpenXML animations at:\n{target.resolve()}")
        except Exception as exc:
            QMessageBox.critical(self, "Export Error", str(exc))
            self.status_lbl.setText("Export failed.")
