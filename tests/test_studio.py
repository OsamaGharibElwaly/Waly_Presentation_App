"""Regression tests for the Pareto exporter and the white-on-dark studio."""
import math
from pathlib import Path

import pytest
from lxml import etree
from pptx import Presentation
from pptx.util import Inches

from backend.agents.base.agent import AgentContext
from backend.agents.markdown_manipulator import MarkdownManipulatorAgent, classify_intent
from backend.pipeline.orchestrator import Orchestrator
from backend.pptx_engine.builder import PptxBuilder, readable_text
from backend.pptx_engine.layout_router import CYCLE, route_layouts
from frontend.theme_factory.animation_registry import AnimationRegistry
from frontend.theme_factory.design_registry import DesignRegistry

PALETTE = {
    "name": "Cyber Slate & Neon Blue",
    "colors": ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"],
}
SPEC = type("Slide", (), {
    "title": "Systems engineering review",
    "bullets": [f"Engineering point number {i} with a measurable outcome" for i in range(1, 6)],
    "notes": "Speaker note",
})()


def archetypes():
    return [item["id"] for item in DesignRegistry().all() if item.get("archetype")]


def native_animations():
    return [item["id"] for item in AnimationRegistry().all() if item.get("native")]


def test_catalogs_contain_all_pareto_items():
    assert len(archetypes()) == 15
    assert len(native_animations()) == 15


def test_text_is_always_legible():
    assert readable_text("#0F172A", "#F8FAFC") == "#F8FAFC"
    assert readable_text("#F8FAFC", "#F8FAFC") == "#0B1220"
    assert readable_text("#1E293B", "#000000") == "#FFFFFF"


@pytest.mark.parametrize("style_id", archetypes())
def test_every_archetype_exports_editable_pptx(style_id, tmp_path):
    ctx = AgentContext(
        theme={"industry": "Engineering", "name": "Review", "style": style_id},
        palette=PALETTE,
        meta={
            "deck_title": "Verification Deck", "design_id": style_id,
            "animation_id": "progressive_bullet_reveal",
            "animation_mode": "native", "animation_intensity": "balanced",
        },
    )
    target = tmp_path / f"{style_id}.pptx"
    PptxBuilder(ctx).build([SPEC], target)

    prs = Presentation(target)
    assert len(prs.slides) == 2
    slide_xml = prs.slides[1]._element.xml
    assert "<p:timing>" in slide_xml
    assert "<p:transition" in slide_xml
    etree.fromstring(slide_xml.encode("utf-8"))
    # Native PowerPoint shapes, not flattened pictures.
    assert len(prs.slides[1].shapes) > 8
    assert not any(shape.shape_type == 13 for shape in prs.slides[1].shapes)
    if style_id == "swiss_grid_editorial_archetype":
        assert any("ANALYSIS" in shape.text for shape in prs.slides[1].shapes if shape.has_text_frame)
    W, H = Inches(13.333), Inches(7.5)
    for shape in prs.slides[1].shapes:
        assert shape.left >= 0 and shape.top >= 0
        assert shape.left + shape.width <= W
        assert shape.top + shape.height <= H


@pytest.mark.parametrize("animation_id", native_animations())
def test_every_native_choreography_is_valid(animation_id, tmp_path):
    ctx = AgentContext(
        theme={"industry": "Engineering", "name": "Review", "style": "blueprint_cad_grid"},
        palette=PALETTE,
        meta={
            "deck_title": "Animation Check", "design_id": "blueprint_cad_grid",
            "animation_id": animation_id, "animation_mode": "native",
            "animation_intensity": "dynamic",
        },
    )
    target = tmp_path / f"{animation_id}.pptx"
    PptxBuilder(ctx).build([SPEC], target)
    slide_xml = Presentation(target).slides[1]._element.xml
    etree.fromstring(slide_xml.encode("utf-8"))
    assert "<p:timing>" in slide_xml


def test_legacy_design_ids_still_render(tmp_path):
    ctx = AgentContext(
        theme={"industry": "Business", "name": "Legacy", "style": "minimalist_scandinavian"},
        palette=PALETTE,
        meta={"deck_title": "Legacy", "design_id": "minimalist_scandinavian"},
    )
    target = tmp_path / "legacy.pptx"
    PptxBuilder(ctx).build([SPEC], target)
    assert len(Presentation(target).slides) == 2


def test_frontend_uses_white_text(tmp_path, monkeypatch):
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    qt = pytest.importorskip("PyQt6.QtWidgets")
    app = qt.QApplication.instance() or qt.QApplication([])
    from frontend.ui.main_window import MainWindow

    window = MainWindow()
    assert "QWidget {" in window.styleSheet()
    assert "color: #F8FAFC;" in window.styleSheet()
    assert "#FFFFFF" in window.styleSheet()
    assert window.design_combo.count() == 30
    assert window.animation_combo.count() == 31
    window.close()
    app.processEvents()


def test_tabs_wrapped_in_resizable_scroll_areas(monkeypatch):
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    qt = pytest.importorskip("PyQt6.QtWidgets")
    app = qt.QApplication.instance() or qt.QApplication([])
    from frontend.ui.main_window import MainWindow

    window = MainWindow()
    for index in range(window.tabs.count()):
        page = window.tabs.widget(index)
        assert isinstance(page, qt.QScrollArea)
        assert page.widgetResizable()
    window.close()
    app.processEvents()


def test_swatch_accent_reaches_orchestrator(monkeypatch):
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    qt = pytest.importorskip("PyQt6.QtWidgets")
    app = qt.QApplication.instance() or qt.QApplication([])
    from frontend.ui import main_window as mw

    captured = {}

    class FakeOrchestrator:
        def __init__(self, theme, palette, meta=None):
            captured["palette"] = palette

        def run(self, text, target):
            return None

    monkeypatch.setattr(mw, "Orchestrator", FakeOrchestrator)
    monkeypatch.setattr(mw.QMessageBox, "information", staticmethod(lambda *a, **k: None))
    window = mw.MainWindow()
    original = window.theme_registry.palette_by_name(window.palette_combo.currentText())["colors"][2]
    window._on_swatch_clicked("#D4AF37")
    window._export("pptx")
    assert captured["palette"]["colors"][2] == "#D4AF37"
    assert window.theme_registry.palette_by_name(window.palette_combo.currentText())["colors"][2] == original
    window.close()
    app.processEvents()


FIXTURE = Path(__file__).parent / "fixtures" / "enterprise_ai_transformation.md"


def test_semantic_classifier_detects_intents_and_focus():
    specs = MarkdownManipulatorAgent(AgentContext()).run(FIXTURE.read_text(encoding="utf-8"))
    assert len(specs) == 10
    assert [spec.layout_type for spec in specs[:5]] == [
        "kpi", "bento", "process", "comparison", "spotlight",
    ]
    assert specs[4].focal_index == 0
    assert specs[4].emphasis_cue == "Highlight"
    assert specs[9].emphasis_cue == "Point out"


def test_layout_rotation_never_repeats_consecutive_slides():
    routed = route_layouts(["bento", "bento", "kpi", "kpi", "process", "process",
                            "comparison", "comparison", "spotlight", "spotlight"])
    assert all(first != second for first, second in zip(routed, routed[1:]))
    assert set(routed) == set(CYCLE)
    assert route_layouts([]) == []


def assert_no_text_overflow(slide) -> None:
    for shape in slide.shapes:
        if not shape.has_text_frame or not shape.text.strip():
            continue
        sizes = [run.font.size.pt for para in shape.text_frame.paragraphs
                 for run in para.runs if run.font.size]
        size = max(sizes, default=18)
        per_line = max(1, int((shape.width / 12700) / (size * 0.52)))
        lines = sum(max(1, math.ceil(len(part) / per_line)) for part in shape.text.split("\n"))
        assert lines * size * 1.25 <= (shape.height / 12700) + 5, (
            shape.text[:40], lines, size, shape.height / 12700,
        )


def test_ten_slide_deck_has_varied_hierarchy_focal_zoom_and_no_overflow(tmp_path):
    meta = {
        "deck_title": "Enterprise AI Transformation",
        "design_id": "executive_kpi_strip",
        "animation_id": "progressive_bullet_reveal",
        "animation_mode": "native",
        "animation_intensity": "balanced",
    }
    theme = {"industry": "Business", "name": "Test", "style": "executive_kpi_strip"}
    target = tmp_path / "enterprise_ai.pptx"
    Orchestrator(theme=theme, palette=PALETTE, meta=meta).run(
        FIXTURE.read_text(encoding="utf-8"), target,
    )

    prs = Presentation(target)
    assert len(prs.slides) == 11
    signatures = []
    for slide in list(prs.slides)[1:]:
        xml = slide._element.xml
        assert "<p:timing>" in xml
        assert 'presetID="23"' in xml
        etree.fromstring(xml.encode("utf-8"))
        assert_no_text_overflow(slide)
        signatures.append(tuple((int(shape.shape_type), shape.left, shape.top,
                                 shape.width, shape.height) for shape in slide.shapes))
    assert all(first != second for first, second in zip(signatures, signatures[1:]))
    assert len(set(signatures)) >= 5
