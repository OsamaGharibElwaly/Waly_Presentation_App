"""Regression tests for the Pareto exporter and the white-on-dark studio."""
from pathlib import Path

import pytest
from lxml import etree
from pptx import Presentation

from backend.agents.base.agent import AgentContext
from backend.pptx_engine.builder import PptxBuilder, readable_text
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
