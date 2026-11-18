"""Main window: white-on-dark studio with live design preview and 30-item Pareto controls."""
from __future__ import annotations

import copy
import re
from pathlib import Path

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QKeySequence, QPainter, QAction
from PyQt6.QtWidgets import (
    QComboBox, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPlainTextEdit, QPushButton, QScrollArea, QTabWidget, QToolBox,
    QVBoxLayout, QWidget,
)

from backend.pipeline.orchestrator import Orchestrator
from backend.pptx_engine.style_prompt import compose_style_prompt
from frontend.theme_factory.animation_registry import AnimationRegistry
from frontend.theme_factory.catalog import INDUSTRIES
from frontend.theme_factory.design_registry import DesignRegistry
from frontend.theme_factory.registry import ThemeRegistry

DARK_STUDIO_QSS = """
QWidget {
    color: #F8FAFC;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}
QMainWindow, QMessageBox {
    background-color: #090D16;
    color: #F8FAFC;
}
QLabel { color: #E2E8F0; }
QLabel[role="muted"] { color: #94A3B8; }
QLineEdit, QPlainTextEdit, QTextEdit {
    background-color: #0B1220;
    color: #FFFFFF;
    border: 1px solid #273449;
    border-radius: 8px;
    padding: 8px 10px;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
}
QLineEdit:focus, QPlainTextEdit:focus { border: 1px solid #38BDF8; }
QComboBox {
    background-color: #0B1220;
    color: #FFFFFF;
    border: 1px solid #273449;
    border-radius: 8px;
    padding: 7px 10px;
    min-height: 20px;
}
QComboBox:hover { border: 1px solid #38BDF8; }
QComboBox QAbstractItemView, QListView, QTreeView, QTableView {
    background-color: #0B1220;
    color: #FFFFFF;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
    border: 1px solid #273449;
}
QPushButton {
    background-color: #1E293B;
    color: #FFFFFF;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
}
QPushButton:hover { background-color: #334155; border-color: #38BDF8; }
QPushButton:pressed { background-color: #2563EB; }
QPushButton:disabled { color: #64748B; background-color: #111827; border-color: #1F2937; }
QToolBox::tab {
    background-color: #162134;
    color: #E2E8F0;
    font-weight: 600;
    border-radius: 6px;
    padding: 8px;
}
QToolBox::tab:selected { background-color: #2563EB; color: #FFFFFF; }
QTabWidget::pane {
    border: 1px solid #273449;
    border-radius: 10px;
    background-color: #0C1322;
    margin-top: 4px;
}
QTabBar::tab {
    background-color: #111C2E;
    color: #CBD5E1;
    padding: 9px 18px;
    margin-right: 4px;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    font-weight: 600;
}
QTabBar::tab:selected { background-color: #2563EB; color: #FFFFFF; }
QFrame#Inspector { background-color: #111827; border: 1px solid #273449; border-radius: 10px; }
QFrame#PreviewFrame { background-color: #0B1220; border: 1px solid #273449; border-radius: 10px; }
QScrollBar:vertical, QScrollBar:horizontal { background: #0B1220; border: none; width: 10px; height: 10px; }
QScrollBar::handle { background: #334155; border-radius: 5px; }
QScrollBar::handle:hover { background: #475569; }
QToolTip { background-color: #1E293B; color: #FFFFFF; border: 1px solid #475569; padding: 4px; }
QStatusBar { color: #94A3B8; }
"""

ALIAS_DESIGN = {"swiss_grid_editorial": "swiss_grid_editorial_archetype"}

SLIDE_TEMPLATE = """## Slide {n} - New Section Heading
- First concise, evidence-led engineering statement
- Second measurable outcome or design constraint
> Speaker note: Explain the intent and the evidence behind this slide.
"""


def readable_text(background: str) -> str:
    value = str(background or "").lstrip("#")
    if len(value) != 6:
        return "#FFFFFF"
    try:
        r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return "#FFFFFF"
    return "#0B1220" if 0.2126 * r + 0.7152 * g + 0.0722 * b > 140 else "#FFFFFF"


class DesignPreview(QFrame):
    """Paints a miniature of the selected archetype using the live palette."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("PreviewFrame")
        self.setMinimumSize(320, 240)
        self.design_id = "glassmorphism_card"
        self.label = "Glassmorphism Layered Card"
        self.palette = {
            "name": "Cyber Slate & Neon Blue",
            "colors": ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"],
        }

    def set_selection(self, design_id: str, label: str, palette: dict) -> None:
        self.design_id = design_id
        self.label = label
        self.palette = palette
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        colors = self.palette.get("colors") or ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]
        colors = (colors + ["#FFFFFF"] * 5)[:5]
        bg, surface, accent, highlight, preferred = (QColor(c) for c in colors)
        fg = QColor(readable_text(colors[1]))
        accent_text = QColor(readable_text(colors[2]))

        available_w, available_h = self.width() - 16, self.height() - 16
        w = min(available_w, available_h * 16 / 9)
        h = w * 9 / 16
        x0, y0 = (self.width() - w) / 2, (self.height() - h) / 2
        painter.fillRect(self.rect(), QColor("#0B1220"))
        painter.fillRect(QRectF(x0, y0, w, h), bg)
        painter.setPen(Qt.PenStyle.NoPen)
        s = w / 13.333
        sy = h / 7.5

        def rect(x, y, rw, rh, color, rounded=False):
            r = QRectF(x0 + x * s, y0 + y * sy, rw * s, rh * sy)
            if rounded:
                painter.drawRoundedRect(r, 5, 5)
            else:
                painter.drawRect(r)
            return r

        def solid(color):
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)

        def outline(color, width=1.4):
            painter.setBrush(Qt.BrushStyle.NoBrush)
            pen = painter.pen()
            pen.setColor(color)
            pen.setWidthF(width)
            painter.setPen(pen)

        def caption(text, x, y, rw, color, size=9, bold=True):
            pen = painter.pen()
            font = QFont("Segoe UI", size)
            font.setBold(bold)
            painter.setFont(font)
            painter.setPen(color)
            painter.drawText(QRectF(x0 + x * s, y0 + y * sy, rw * s, 0.36 * sy),
                             Qt.AlignmentFlag.AlignVCenter, text)
            painter.setPen(pen)

        did = self.design_id
        if did == "blueprint_cad_grid":
            outline(accent, 1.0)
            rect(0.4, 0.4, 12.53, 6.7, accent)
            for i in range(1, 5):
                solid(surface)
                rect(0.4 + i * 2.5, 0.4, 0.02, 6.7, surface)
            solid(surface)
            rect(8.8, 6.1, 4.13, 0.85, surface)
            caption("[SPEC] STRUCTURAL REVIEW", 0.85, 0.8, 6.0, accent, 9)
        elif did == "cyberpunk_hud_frame":
            solid(surface)
            outline(accent, 2.0)
            rect(0.7, 0.7, 11.93, 6.1, surface, True)
            solid(accent)
            rect(1.0, 0.45, 5.75, 0.72, accent)
            caption("SYSTEM TELEMETRY", 1.25, 0.55, 5.0, accent_text, 9)
            for i in range(3):
                solid(highlight)
                rect(11.05, 0.55 + i * 0.3, 0.42, 0.16, highlight)
        elif did == "executive_kpi_strip":
            solid(accent)
            rect(0.8, 0.5, 11.73, 0.12, accent)
            for x in (0.8, 4.82, 8.83):
                solid(surface)
                rect(x, 1.55, 3.7, 2.1, surface, True)
                solid(highlight)
                rect(x, 1.55, 3.7, 0.14, highlight)
                caption("99.98%", x + 0.25, 2.1, 2.0, accent, 13)
            solid(surface)
            rect(0.8, 3.9, 11.73, 2.85, surface, True)
        elif did == "chevron_process_flow":
            for i in range(4):
                solid(accent if i % 2 == 0 else highlight)
                rect(0.8 + i * 2.95, 1.55, 2.85, 1.1, accent if i % 2 == 0 else highlight)
                solid(surface)
                rect(0.8 + i * 2.95, 3.0, 2.75, 3.45, surface, True)
                caption(f"PHASE {i + 1:02d}", 1.05 + i * 2.95, 1.85, 2.2, accent_text, 8)
        elif did == "dual_comparison_matrix":
            solid(surface)
            rect(0.8, 1.6, 5.55, 5.2, surface, True)
            rect(6.98, 1.6, 5.55, 5.2, surface, True)
            solid(accent)
            rect(6.27, 3.8, 0.8, 0.8, accent)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            pen = painter.pen()
            pen.setColor(accent_text)
            painter.setPen(pen)
            painter.drawEllipse(QRectF(x0 + 6.27 * s, y0 + 3.8 * sy, 0.8 * s, 0.8 * sy))
        elif did == "bento_grid_dashboard":
            solid(surface)
            rect(0.8, 1.5, 5.6, 5.3, surface, True)
            rect(6.65, 1.5, 5.88, 2.5, surface, True)
            rect(6.65, 4.3, 5.88, 2.5, surface, True)
            solid(accent)
            rect(0.8, 1.5, 0.14, 5.3, accent)
        elif did == "radial_sunburst_hub":
            for x, y in ((0.8, 1.4), (8.43, 1.4), (0.8, 4.8), (8.43, 4.8)):
                solid(surface)
                rect(x, y, 4.1, 2.1, surface, True)
            solid(accent)
            painter.setBrush(accent)
            painter.drawEllipse(QRectF(x0 + 5.56 * s, y0 + 3.15 * sy, 2.2 * s, 2.2 * sy))
        elif did == "concentric_circle_target":
            for diameter, color in ((4.8, surface), (3.3, highlight), (1.8, accent)):
                off = (5.8 - diameter) / 2
                painter.setBrush(color)
                painter.drawEllipse(QRectF(x0 + (1.0 + off) * s, y0 + (2.0 + off) * sy,
                                           diameter * s, diameter * sy))
            for y in (1.7, 3.4, 5.1):
                solid(surface)
                rect(6.4, y, 6.13, 1.4, surface, True)
        elif did == "minimalist_timeline_bar":
            solid(accent)
            rect(1.0, 4.15, 11.33, 0.08, accent)
            for i, x in enumerate((1.8, 4.8, 7.8, 10.8)):
                painter.setBrush(accent)
                painter.drawEllipse(QRectF(x0 + (x - 0.22) * s, y0 + 3.95 * sy, 0.44 * s, 0.44 * sy))
                solid(surface)
                rect(x - 1.35, 1.7 if i % 2 == 0 else 4.85, 2.7, 1.9, surface, True)
        elif did == "isometric_layer_stack":
            for i, y in enumerate((1.7, 3.1, 4.5)):
                solid((accent, highlight, surface)[i])
                rect(1.1, y, 3.6, 1.6, (accent, highlight, surface)[i])
                solid(surface)
                rect(5.8, 1.5, 6.73, 5.3, surface, True)
        elif did == "oversized_watermark":
            caption("01", 0.7, 1.1, 4.5, highlight, 70, True)
            solid(surface)
            rect(3.2, 1.6, 9.33, 5.0, surface, True)
        elif did == "frosted_sidebar_nav":
            solid(surface)
            rect(0, 0, 3.8, 7.5, surface)
            solid(accent)
            rect(3.78, 0, 0.03, 7.5, accent)
            rect(0, 1.4, 0.16, 1.2, accent)
            rect(4.3, 0.8, 8.23, 5.9, surface, True)
        elif did in ("swiss_grid_editorial", "swiss_grid_editorial_archetype"):
            solid(accent)
            rect(0.8, 0.7, 11.73, 0.04, accent)
            solid(highlight)
            rect(4.6, 0.7, 0.03, 6.1, highlight)
            solid(surface)
            rect(4.9, 1.0, 7.63, 5.8, surface)
        elif did == "neo_brutalist_pop":
            solid(QColor("#000000"))
            rect(1.05, 1.65, 11.6, 5.1, QColor("#000000"))
            solid(surface)
            outline(QColor("#000000"), 3.0)
            rect(0.85, 1.45, 11.6, 5.1, surface)
            solid(accent)
            rect(0.85, 0.65, 7.5, 0.65, accent)
        else:
            solid(surface)
            outline(accent, 1.8)
            rect(0.9, 0.85, 11.53, 5.8, surface, True)
            solid(accent)
            rect(1.25, 1.25, 0.14, 0.65, accent)

        caption(self.label.upper(), 1.3, 0.28, 10.8, fg, 9)
        painter.end()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Offline AI Presentation Factory - 30-Item Pareto Studio")
        self.resize(1460, 940)
        self.setStyleSheet(DARK_STUDIO_QSS)

        self.theme_registry = ThemeRegistry()
        self.design_registry = DesignRegistry()
        self.animation_registry = AnimationRegistry()
        self._accent_override: str | None = None
        self._selected_theme = {
            "industry": "Architecture", "name": "Minimalist Glass", "accent": "#0284C7",
            "style": "glassmorphism_card", "animation": "progressive_bullet_reveal",
        }
        self._build_ui()
        self._update_color_swatches()
        self._update_stats()

    # ------------------------------------------------------------------- UI
    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 14, 16, 12)
        root.setSpacing(10)

        top = QHBoxLayout()
        title_label = QLabel("Presentation title")
        title_label.setStyleSheet("font-size: 15px; font-weight: 600; color: #38BDF8;")
        top.addWidget(title_label)
        self.name_input = QLineEdit("Enterprise_AI_Transformation_Deck")
        self.name_input.setStyleSheet("font-size: 14px; font-weight: 600; color: #FFFFFF;")
        top.addWidget(self.name_input, 1)
        root.addLayout(top)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)
        self.tabs.addTab(self._build_studio_tab(), "1. Industry & Design Studio")
        self.tabs.addTab(self._build_markdown_tab(), "2. Markdown AI Input")

        actions = QHBoxLayout()
        load_btn = QPushButton("Load Markdown")
        load_btn.setToolTip("Open a .md file into the editor")
        load_btn.clicked.connect(self._load_file)
        actions.addWidget(load_btn)

        save_btn = QPushButton("Save Markdown")
        save_btn.clicked.connect(self._save_file)
        actions.addWidget(save_btn)

        pptx_btn = QPushButton("Export styled .pptx")
        pptx_btn.setStyleSheet("background-color: #047857; color: #FFFFFF; font-size: 14px;")
        pptx_btn.clicked.connect(lambda _checked=False: self._export("pptx"))
        actions.addWidget(pptx_btn)

        pdf_btn = QPushButton("Export clean .pdf")
        pdf_btn.setStyleSheet("background-color: #B45309; color: #FFFFFF; font-size: 14px;")
        pdf_btn.clicked.connect(lambda _checked=False: self._export("pdf"))
        actions.addWidget(pdf_btn)

        self.open_btn = QPushButton("Open output folder")
        self.open_btn.setEnabled(False)
        self.open_btn.clicked.connect(self._open_output)
        actions.addWidget(self.open_btn)
        actions.addStretch(1)
        root.addLayout(actions)

        self.status_lbl = QLabel("Ready. Select an industry theme, then export when the preview looks right.")
        self.status_lbl.setStyleSheet("color: #7DD3FC; font-weight: 600; padding: 4px 0;")
        root.addWidget(self.status_lbl)

        export_action = QAction(self)
        export_action.setShortcut(QKeySequence("Ctrl+Return"))
        export_action.triggered.connect(lambda _checked=False: self._export("pptx"))
        self.addAction(export_action)

    def _build_studio_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        left = QVBoxLayout()
        hint = QLabel("Industry categories and Pareto archetypes (click to apply)")
        hint.setProperty("role", "muted")
        hint.setWordWrap(True)
        left.addWidget(hint)
        toolbox = QToolBox()
        for industry, data in INDUSTRIES.items():
            holder = QWidget()
            inner = QVBoxLayout(holder)
            desc = QLabel(data.get("description", ""))
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #94A3B8; font-size: 12px; margin-bottom: 4px;")
            inner.addWidget(desc)
            for theme in data["themes"]:
                label = f"{theme['name']}   [{theme['style']}]"
                button = QPushButton(label)
                button.setToolTip(f"Animation: {theme.get('animation', 'none')}")
                button.setStyleSheet(
                    "color: #FFFFFF; text-align: left; padding-left: 12px; "
                    f"background-color: #1F2937; border-left: 4px solid {theme['accent']};"
                )
                button.clicked.connect(
                    lambda _checked=False, ind=industry, item=theme: self._pick_theme(ind, item)
                )
                inner.addWidget(button)
            inner.addStretch(1)
            toolbox.addItem(holder, industry)
        left.addWidget(toolbox, 1)
        layout.addLayout(left, 1)

        right = QVBoxLayout()
        inspector = QFrame()
        inspector.setObjectName("Inspector")
        form = QVBoxLayout(inspector)
        form.setSpacing(8)

        form.addWidget(QLabel("ACTIVE INDUSTRY / ARCHETYPE"))
        self.theme_display_lbl = QLabel("[Architecture] Minimalist Glass (glassmorphism_card)")
        self.theme_display_lbl.setStyleSheet("color: #38BDF8; font-size: 16px; font-weight: 700;")
        self.theme_display_lbl.setWordWrap(True)
        form.addWidget(self.theme_display_lbl)

        self.industry_desc_lbl = QLabel("Spatial design, structural acoustics, urban planning.")
        self.industry_desc_lbl.setWordWrap(True)
        self.industry_desc_lbl.setStyleSheet("color: #94A3B8; font-size: 12px;")
        form.addWidget(self.industry_desc_lbl)

        self.preview = DesignPreview()
        form.addWidget(self.preview)

        form.addWidget(QLabel("Colour palette"))
        self.palette_combo = QComboBox()
        for palette in self.theme_registry.palettes():
            self.palette_combo.addItem(palette["name"], palette["name"])
        self.palette_combo.currentIndexChanged.connect(self._on_palette_changed)
        form.addWidget(self.palette_combo)

        swatch_head = QHBoxLayout()
        swatch_head.addWidget(QLabel("Live palette (click a colour to override the accent)"))
        reset_btn = QPushButton("Reset")
        reset_btn.setStyleSheet("padding: 3px 10px; font-size: 11px; color: #FFFFFF;")
        reset_btn.clicked.connect(self._reset_accent)
        swatch_head.addWidget(reset_btn)
        form.addLayout(swatch_head)
        self.swatch_grid = QGridLayout()
        form.addLayout(self.swatch_grid)

        form.addWidget(QLabel("Design system (15 legacy + 15 Pareto archetypes)"))
        self.design_combo = QComboBox()
        for item in self.design_registry.all():
            prefix = "Pareto | " if item.get("archetype") else "Classic | "
            self.design_combo.addItem(prefix + item["name"], item["id"])
        self.design_combo.currentIndexChanged.connect(self._on_controls_changed)
        form.addWidget(self.design_combo)

        form.addWidget(QLabel("Animation choreography"))
        self.animation_combo = QComboBox()
        self.animation_combo.addItem("None / static slides", "")
        for item in self.animation_registry.all():
            prefix = "Native | " if item.get("native") else "Build | "
            self.animation_combo.addItem(prefix + item["name"], item["id"])
        self.animation_combo.currentIndexChanged.connect(self._on_controls_changed)
        form.addWidget(self.animation_combo)

        form.addWidget(QLabel("Animation output"))
        self.animation_mode_combo = QComboBox()
        self.animation_mode_combo.addItem("Off - static slides", "off")
        self.animation_mode_combo.addItem("Native PowerPoint animation (OpenXML)", "native")
        self.animation_mode_combo.addItem("Build sequence - extra reveal slides", "build_sequence")
        self.animation_mode_combo.currentIndexChanged.connect(self._on_controls_changed)
        form.addWidget(self.animation_mode_combo)

        form.addWidget(QLabel("Motion intensity"))
        self.animation_intensity_combo = QComboBox()
        for value in ("subtle", "balanced", "dynamic"):
            self.animation_intensity_combo.addItem(value.title(), value)
        self.animation_intensity_combo.setCurrentIndex(1)
        form.addWidget(self.animation_intensity_combo)

        inspector_scroll = QScrollArea()
        inspector_scroll.setWidget(inspector)
        inspector_scroll.setWidgetResizable(True)
        inspector_scroll.setFrameShape(QFrame.Shape.NoFrame)
        inspector_scroll.setStyleSheet("QScrollArea { background: transparent; color: #F8FAFC; }")
        right.addWidget(inspector_scroll, 1)
        layout.addLayout(right, 1)

        self._set_combo_data(self.design_combo, "glassmorphism_card")
        self._set_combo_data(self.animation_combo, "progressive_bullet_reveal")
        return tab

    def _build_markdown_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        toolbar = QHBoxLayout()
        note = QLabel("Markdown: '# deck', '## Slide N - title', '- bullet', '> speaker note'")
        note.setProperty("role", "muted")
        toolbar.addWidget(note)
        toolbar.addStretch(1)
        insert_btn = QPushButton("Insert slide template")
        insert_btn.clicked.connect(self._insert_slide_template)
        toolbar.addWidget(insert_btn)
        bullet_btn = QPushButton("Insert bullet")
        bullet_btn.clicked.connect(self._insert_bullet)
        toolbar.addWidget(bullet_btn)
        layout.addLayout(toolbar)

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
            "## Slide 3 - Automated Theme Factory & Design Patterns\n"
            "- Industry-tailored design variants across engineering, architectural, and corporate domains\n"
            "- Dynamic colour palette mapping with 30 tuned archetype/color combinations\n"
            "- Native OpenXML choreography for cinematic, fully editable PowerPoint output\n"
            "> Speaker note: Show how the theme factory maintains strict visual consistency across every exported presentation."
        )
        self.md_editor.textChanged.connect(self._update_stats)
        layout.addWidget(self.md_editor, 1)

        self.stats_lbl = QLabel("")
        self.stats_lbl.setStyleSheet("color: #94A3B8; font-size: 12px;")
        layout.addWidget(self.stats_lbl)
        return tab

    # --------------------------------------------------------------- helpers
    @staticmethod
    def _set_combo_data(combo: QComboBox, value: str) -> None:
        index = combo.findData(value)
        if index >= 0:
            combo.setCurrentIndex(index)

    def _current_palette(self) -> dict:
        palette = copy.deepcopy(
            self.theme_registry.palette_by_name(self.palette_combo.currentText())
        )
        if self._accent_override and len(palette.get("colors", [])) >= 3:
            palette["colors"][2] = self._accent_override
        return palette

    def _refresh_preview(self) -> None:
        design_id = self.design_combo.currentData() or "glassmorphism_card"
        index = self.design_combo.currentIndex()
        name = self.design_combo.itemText(index).split("| ", 1)[-1]
        self.preview.set_selection(design_id, name, self._current_palette())

    def _pick_theme(self, industry: str, theme: dict) -> None:
        self._selected_theme = {"industry": industry, **theme}
        self.theme_display_lbl.setText(
            f"[{industry}] {theme['name']} ({theme['style']})"
        )
        self.industry_desc_lbl.setText(INDUSTRIES.get(industry, {}).get("description", ""))
        self._set_combo_data(self.design_combo, ALIAS_DESIGN.get(theme["style"], theme["style"]))
        self._set_combo_data(self.animation_combo, theme.get("animation", ""))
        self._refresh_preview()
        self.status_lbl.setText(
            f"Applied [{industry}] {theme['name']} - design and animation synced."
        )

    def _on_controls_changed(self, *_args) -> None:
        # Signals fire while the combos are still being populated during build.
        if (not hasattr(self, "animation_combo") or not hasattr(self, "animation_mode_combo")
                or not hasattr(self, "status_lbl")):
            return
        design_id = self.design_combo.currentData()
        if design_id:
            self._selected_theme["style"] = design_id
        animation_id = self.animation_combo.currentData()
        if animation_id:
            self._selected_theme["animation"] = animation_id
        else:
            self._selected_theme.pop("animation", None)
        if self.animation_mode_combo.currentData() == "off":
            self.animation_combo.setEnabled(True)
        self._refresh_preview()
        self.status_lbl.setText(
            f"Preview: {self.design_combo.currentText()} | "
            f"{self.animation_combo.currentText()} | {self.animation_mode_combo.currentText()}"
        )

    def _on_palette_changed(self, *_args) -> None:
        self._accent_override = None
        self._update_color_swatches(status=False)
        self._refresh_preview()
        self.status_lbl.setText(f"Palette changed: {self.palette_combo.currentText()}")

    def _update_color_swatches(self, status: bool = True, *_args) -> None:
        for i in reversed(range(self.swatch_grid.count())):
            item = self.swatch_grid.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
        palette = self.theme_registry.palette_by_name(self.palette_combo.currentText())
        for index, hex_code in enumerate(palette.get("colors", [])):
            button = QPushButton(hex_code)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setToolTip("Click to use this colour as the export accent")
            fg = "#000000" if self._is_light(hex_code) else "#FFFFFF"
            border = "2px solid #FFFFFF" if hex_code == self._accent_override else "1px solid #334155"
            button.setStyleSheet(
                f"background-color: {hex_code}; color: {fg}; border: {border}; "
                "border-radius: 7px; font-weight: 700; font-size: 11px; padding: 9px 4px;"
            )
            button.clicked.connect(
                lambda _checked=False, h=hex_code: self._on_swatch_clicked(h)
            )
            self.swatch_grid.addWidget(button, 0, index)
        if status:
            self.status_lbl.setText(f"Palette synced: {palette.get('name', 'Default')}")

    def _on_swatch_clicked(self, hex_code: str) -> None:
        self._accent_override = hex_code
        self._update_color_swatches(status=False)
        self._refresh_preview()
        self.status_lbl.setText(f"Accent override set to {hex_code} for the next export.")

    def _reset_accent(self) -> None:
        self._accent_override = None
        self._update_color_swatches(status=False)
        self._refresh_preview()
        self.status_lbl.setText("Accent reset to the selected palette.")

    @staticmethod
    def _is_light(hex_s: str) -> bool:
        value = hex_s.lstrip("#")
        if len(value) != 6:
            return False
        try:
            r, g, b = (int(value[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return False
        return 0.299 * r + 0.587 * g + 0.114 * b > 160

    def _update_stats(self) -> None:
        text = self.md_editor.toPlainText() if hasattr(self, "md_editor") else ""
        slides = len(re.findall(r"^##\s+", text, flags=re.MULTILINE))
        bullets = len(re.findall(r"^\s*[-*]\s+", text, flags=re.MULTILINE))
        words = len(text.split())
        self.stats_lbl.setText(f"{slides} slides  |  {bullets} bullets  |  {words} words")

    def _insert_slide_template(self) -> None:
        text = self.md_editor.toPlainText()
        count = len(re.findall(r"^##\s+", text, flags=re.MULTILINE)) + 1
        cursor = self.md_editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        block = "\n\n" + SLIDE_TEMPLATE.format(n=count)
        cursor.insertText(block)
        self.md_editor.setTextCursor(cursor)
        self.md_editor.setFocus()

    def _insert_bullet(self) -> None:
        cursor = self.md_editor.textCursor()
        cursor.insertText("- Concise engineering statement\n")
        self.md_editor.setFocus()

    # ----------------------------------------------------------- file / export
    def _load_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open Markdown", "", "Markdown (*.md *.txt)")
        if path:
            try:
                self.md_editor.setPlainText(Path(path).read_text(encoding="utf-8"))
                self.status_lbl.setText(f"Loaded markdown: {path}")
            except OSError as exc:
                QMessageBox.warning(self, "Load failed", str(exc))

    def _save_file(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save Markdown", "presentation.md", "Markdown (*.md)")
        if path:
            try:
                Path(path).write_text(self.md_editor.toPlainText(), encoding="utf-8")
                self.status_lbl.setText(f"Saved markdown: {path}")
            except OSError as exc:
                QMessageBox.warning(self, "Save failed", str(exc))

    def _export(self, kind: str) -> None:
        palette = self._current_palette()
        design_id = self.design_combo.currentData() or "glassmorphism_card"
        animation_id = self.animation_combo.currentData() or ""
        mode = self.animation_mode_combo.currentData() or "off"
        intensity = self.animation_intensity_combo.currentData() or "balanced"
        if not animation_id:
            mode = "off"

        style_prompt = compose_style_prompt(design_id, animation_id, palette, intensity, mode)
        meta = {
            "deck_title": self.name_input.text().strip() or "presentation",
            "design_id": design_id,
            "animation_id": animation_id,
            "animation_mode": mode,
            "animation_intensity": intensity,
            "style_prompt": style_prompt,
        }
        out_dir = Path("out")
        out_dir.mkdir(exist_ok=True)
        target = out_dir / f"{meta['deck_title']}.{kind}"

        try:
            Orchestrator(theme=self._selected_theme, palette=palette, meta=meta).run(
                self.md_editor.toPlainText(), target
            )
        except Exception as exc:
            QMessageBox.critical(self, "Export failed", str(exc))
            self.status_lbl.setText("Export failed - see the error dialog.")
            return

        self.open_btn.setEnabled(True)
        self.status_lbl.setText(f"Exported {kind.upper()}: {target.resolve()}")
        QMessageBox.information(
            self, "Export successful",
            f"Created {target.resolve()}\n\n"
            f"Design: {self.design_combo.currentText()}\n"
            f"Palette: {palette.get('name', 'Default')}\n"
            f"Animation: {self.animation_combo.currentText()} ({mode})",
        )

    def _open_output(self) -> None:
        import os
        import subprocess

        out_dir = Path("out").resolve()
        try:
            if os.name == "nt":
                subprocess.Popen(["explorer", str(out_dir)])
            else:
                subprocess.Popen(["xdg-open", str(out_dir)])
        except OSError as exc:
            QMessageBox.warning(self, "Could not open folder", str(exc))
