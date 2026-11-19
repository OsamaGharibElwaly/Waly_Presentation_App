"""Regression tests for the Pareto exporter and the white-on-dark studio."""
import math
from pathlib import Path

import pytest
from lxml import etree
from pptx import Presentation
from pptx.util import Inches

from backend.agents.base.agent import AgentContext, SlideSpec, VisualSpec
from backend.agents.image_factory_agent import ImageFactoryAgent
from backend.agents.markdown_manipulator import MarkdownManipulatorAgent, classify_intent
from backend.agents.planner_agent import PlannerAgent
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

        def run(self, text, target, progress=None):
            if progress:
                for value in (25, 50, 75, 100):
                    progress(value, "step")
            return None

    from frontend.ui import export_worker
    from PyQt6.QtCore import QEventLoop, QTimer

    monkeypatch.setattr(export_worker, "Orchestrator", FakeOrchestrator)
    monkeypatch.setattr(mw.QMessageBox, "information", staticmethod(lambda *a, **k: None))
    window = mw.MainWindow()
    original = window.theme_registry.palette_by_name(window.palette_combo.currentText())["colors"][2]
    window._on_swatch_clicked("#D4AF37")
    window._export("pptx")
    loop = QEventLoop()
    QTimer.singleShot(5000, loop.quit)
    window._worker.finished.connect(loop.quit)
    loop.exec()
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


MARKDOWN_EXT = """# Deck

## Extended syntax slide
::visual luminous geometric grid for planning
![cost chart](metric://68/42/71)
| Metric | Value |
| --- | --- |
| Cost | 68% |
1. First deterministic step
- **Bold takeaway** with `inline code`
> Speaker note: Walk through the bold point
"""


def test_markdown_extensions_parse_into_slide_spec():
    specs = MarkdownManipulatorAgent(AgentContext()).run(MARKDOWN_EXT)
    assert len(specs) == 1
    spec = specs[0]
    assert spec.visual_hint == "luminous geometric grid for planning"
    assert spec.image_spec == "metric://68/42/71"
    assert any("Cost 68%" in bullet for bullet in spec.bullets)
    assert any("First deterministic step" in bullet for bullet in spec.bullets)
    assert any("Bold takeaway with inline code" in bullet for bullet in spec.bullets)
    assert spec.focal_index == 3
    assert spec.emphasis_cue == "Walk through"


def test_planner_assigns_contracts_without_repeats():
    specs = [SlideSpec(title=f"Slide {i}", bullets=[f"point {i}"]) for i in range(9)]
    planned = PlannerAgent(AgentContext()).run(specs)
    assert [item.pacing for item in planned[:4]] == ["open", "build", "evidence", "close"]
    assert all(first.layout_type != second.layout_type for first, second in zip(planned, planned[1:]))
    assert all(first.visual_spec.mode != second.visual_spec.mode for first, second in zip(planned, planned[1:]))
    assert all(first.image_placement != second.image_placement for first, second in zip(planned, planned[1:]))
    pairs = [(item.image_placement, item.visual_spec.mode) for item in planned]
    assert all(first != second for first, second in zip(pairs, pairs[1:]))
    from backend.agents import planner_agent as planner
    assert set(item.image_placement for item in planned) <= set(planner.PLACEMENTS)
    assert all(isinstance(item.visual_spec, VisualSpec) and item.focal_index == 0 for item in planned)


def test_image_factory_is_deterministic_and_cached(tmp_path, monkeypatch):
    from PIL import Image
    from backend.agents import image_factory_agent as factory

    monkeypatch.setattr(factory, "CACHE_DIR", tmp_path / "images")
    assert factory.SCALE == 2
    prompt = "42% cost, 68% revenue, 71% uptime"

    def make_spec():
        return SlideSpec(title="Metrics", bullets=[], visual_spec=VisualSpec(
            mode="metric_visual", prompt=prompt, placement="giant_stat_split"))

    first = make_spec()
    ImageFactoryAgent(AgentContext(palette=PALETTE)).run([first])
    path = Path(first.image_path)
    assert path.exists()
    with Image.open(path) as image:
        assert image.size == factory.SIZES["giant_stat_split"]
        pixels = image.tobytes()
    raw = path.read_bytes()

    second = make_spec()
    ImageFactoryAgent(AgentContext(palette=PALETTE)).run([second])
    assert second.image_path == first.image_path
    assert Path(second.image_path).read_bytes() == raw
    with Image.open(second.image_path) as image:
        assert image.tobytes() == pixels

    monkeypatch.setattr(factory, "RENDERER_VERSION", "v4_senior_artist_next")
    upgraded = make_spec()
    ImageFactoryAgent(AgentContext(palette=PALETTE)).run([upgraded])
    assert upgraded.image_path != first.image_path
    with Image.open(upgraded.image_path) as image:
        assert image.size == factory.SIZES["giant_stat_split"]


def test_image_factory_supports_all_four_modes(tmp_path, monkeypatch):
    from backend.agents import image_factory_agent as factory

    monkeypatch.setattr(factory, "CACHE_DIR", tmp_path)
    modes = ("geometric_composition", "node_flow_diagram", "metric_visual", "split_illustration")
    specs = [SlideSpec(title=mode, bullets=[], visual_spec=VisualSpec(mode=mode, prompt="42% growth"))
             for mode in modes]
    ImageFactoryAgent(AgentContext(palette=PALETTE)).run(specs)
    assert len({spec.image_path for spec in specs}) == len(modes)
    assert all(Path(spec.image_path).exists() for spec in specs)


def test_plain_markdown_gets_v4_visuals_without_repeats():
    from backend.agents import image_factory_agent as factory

    markdown = FIXTURE.read_text(encoding="utf-8")
    assert "::visual" not in markdown
    parsed = MarkdownManipulatorAgent(AgentContext()).run(markdown)
    planned = PlannerAgent(AgentContext()).run(parsed)
    assert all(spec.visual_spec and spec.visual_spec.placement in factory.SIZES for spec in planned)
    pairs = [(spec.visual_spec.placement, spec.visual_spec.mode) for spec in planned]
    assert all(first != second for first, second in zip(pairs, pairs[1:]))
    assert all(spec.focal_index is not None for spec in planned)
    assert any(spec.visual_spec.typography_scale == "display" for spec in planned)


def test_builder_places_v4_images_flush_to_edges(tmp_path):
    from PIL import Image

    image = tmp_path / "art.png"
    Image.new("RGB", (16, 16), "#0F172A").save(image)
    expected = {
        "split_right": (6.667, 0, 6.666, 7.5),
        "split_left": (0, 0, 6.667, 7.5),
        "giant_stat_split": (7.33, 0, 6.0, 7.5),
        "hero_banner": (0, 0, 13.333, 4.35),
        "full_bleed_glass": (0, 0, 13.333, 7.5),
    }
    for placement, box in expected.items():
        spec = SlideSpec(title="Flush placement", bullets=["68% faster delivery"],
                         focal_index=0, visual_spec=VisualSpec(placement=placement),
                         image_path=str(image), image_placement=placement)
        ctx = AgentContext(theme={"industry": "Business", "name": "Test", "style": "glassmorphism_card"},
                           palette=PALETTE, meta={"deck_title": "Placement"})
        target = tmp_path / f"{placement}.pptx"
        PptxBuilder(ctx).build([spec], target)
        pictures = [shape for shape in Presentation(target).slides[1].shapes if shape.shape_type == 13]
        assert len(pictures) == 1
        actual = (pictures[0].left / 914400, pictures[0].top / 914400,
                  pictures[0].width / 914400, pictures[0].height / 914400)
        assert all(abs(first - second) < 0.02 for first, second in zip(actual, box))


def test_builders_render_generated_images(tmp_path):
    meta = {
        "deck_title": "Visual Deck", "design_id": "executive_kpi_strip",
        "animation_id": "progressive_bullet_reveal", "animation_mode": "native",
        "animation_intensity": "balanced",
    }
    theme = {"industry": "Business", "name": "Test", "style": "executive_kpi_strip"}
    markdown = "## Visual deck\n::visual node flow\n- **Key** point with 42% lift\n"
    for suffix in ("pptx", "pdf"):
        target = tmp_path / f"visual.{suffix}"
        Orchestrator(theme, PALETTE, meta).run(markdown, target)
        assert target.exists() and target.stat().st_size > 0
    prs = Presentation(tmp_path / "visual.pptx")
    assert any(shape.shape_type == 13 for shape in prs.slides[1].shapes)


def test_export_worker_reports_progress(monkeypatch):
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")
    qt = pytest.importorskip("PyQt6.QtWidgets")
    from PyQt6.QtCore import QEventLoop, QTimer
    from frontend.ui import export_worker

    app = qt.QApplication.instance() or qt.QApplication([])
    seen = []

    class FakeOrchestrator:
        def __init__(self, theme, palette, meta=None):
            pass

        def run(self, text, target, progress=None):
            for value in (10, 50, 100):
                progress(value, "phase")

    monkeypatch.setattr(export_worker, "Orchestrator", FakeOrchestrator)
    worker = export_worker.ExportWorker({}, PALETTE, {}, "text", Path("out/x.pptx"))
    worker.progress.connect(lambda value, message: seen.append(value))
    loop = QEventLoop()
    QTimer.singleShot(5000, loop.quit)
    worker.finished.connect(loop.quit)
    worker.start()
    loop.exec()
    assert seen[:3] == [10, 50, 100]
    app.processEvents()


def test_agent_factory_resolves_all_pipeline_agents():
    from backend.agents.factory.agent_factory import AgentFactory
    from backend.agents.image_factory_agent import ImageFactoryAgent
    from backend.agents.markdown_manipulator import MarkdownManipulatorAgent
    from backend.agents.outline_agent import OutlineAgent
    from backend.agents.planner_agent import PlannerAgent

    for name, expected in (
        ("markdown_manipulator", MarkdownManipulatorAgent),
        ("outline", OutlineAgent),
        ("planner", PlannerAgent),
        ("image_factory", ImageFactoryAgent),
    ):
        assert isinstance(AgentFactory.create(name, AgentContext(palette=PALETTE)), expected)


def test_catalogs_are_cached_in_memory():
    from frontend.theme_factory.design_registry import DesignRegistry
    from frontend.theme_factory.animation_registry import AnimationRegistry
    from frontend.theme_factory.registry import ThemeRegistry

    assert DesignRegistry().data is DesignRegistry().data
    assert AnimationRegistry().data is AnimationRegistry().data
    assert ThemeRegistry().palettes() is ThemeRegistry().palettes()
