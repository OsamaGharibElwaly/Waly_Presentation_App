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
        self.setWindowTitle("Offline AI Presentation Factory — Interactive Designer")
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
                btn = QPushButton(f"✦ {theme['name']} (Accent: {theme['accent']})")
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

        self.tabs.addTab(tab_studio, "🎨 1. Theme & Palette Studio")

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
        
        self.tabs.addTab(tab_editor, "📝 2. Markdown AI Input")

        # Bottom Actions Bar
        row_actions = QHBoxLayout()
        btn_load = QPushButton("📁 Load Markdown File")
        btn_load.clicked.connect(self._load_md)
        row_actions.addWidget(btn_load)
        
        btn_export_pptx = QPushButton("⚡ Export Professional .pptx")
        btn_export_pptx.setStyleSheet("background-color: #059669; font-size: 15px;")
        btn_export_pptx.clicked.connect(lambda: self._export("pptx"))
        row_actions.addWidget(btn_export_pptx)

        btn_export_pdf = QPushButton("📄 Export Clean .pdf")
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