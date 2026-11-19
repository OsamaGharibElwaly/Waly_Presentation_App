"""16:9 PowerPoint renderer for the 30-item Pareto design/animation specification.

Every archetype is drawn with native PowerPoint shapes (no images), so the result
stays editable in Microsoft Office. Text colour is chosen from the palette but
automatically corrected when contrast is too low, so it is never black-on-black.

Animation modes:
  off              - static slides
  build_sequence   - several slides per source slide that reveal bullets step by step
  native           - native OpenXML <p:timing> entrance effects + slide transitions
"""
from __future__ import annotations

import math
import re
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

from backend.agents.base.agent import AgentContext
from frontend.theme_factory.animation_registry import AnimationRegistry
from frontend.theme_factory.design_registry import DesignRegistry

W, H = 13.333, 7.5
V4_PLACEMENTS = ("split_right", "split_left", "giant_stat_split", "hero_banner", "full_bleed_glass")
DEFAULTS = ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]
BODY_FONT = "Aptos"
MONO_FONT = "Consolas"

# Legacy design-system IDs from the earlier catalog remain usable and are mapped
# onto the closest Pareto archetype so old projects still export with a design.
LEGACY_TO_ARCHETYPE = {
    "minimalist_scandinavian": "glassmorphism_card",
    "swiss_grid_editorial": "swiss_grid_editorial",
    "scientific_research": "swiss_grid_editorial",
    "executive_corporate": "executive_kpi_strip",
    "engineering_blueprint": "blueprint_cad_grid",
    "technical_dark_neon": "cyberpunk_hud_frame",
    "futuristic_hud": "cyberpunk_hud_frame",
    "bento_grid": "bento_grid_dashboard",
    "neo_brutalist": "neo_brutalist_pop",
    "architecture_materiality": "swiss_grid_editorial",
    "data_visualization": "bento_grid_dashboard",
    "isometric_exploded_view": "isometric_layer_stack",
    "process_flow_chevron": "chevron_process_flow",
    "timeline_roadmap": "minimalist_timeline_bar",
    "comparison_matrix": "dual_comparison_matrix",
}

MORPH_TRANSITION = (
    '<mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">'
    '<mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">'
    '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
    '<p159:morph option="byObject"/></p:transition></mc:Choice>'
    '<mc:Fallback><p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
    '<p:fade/></p:transition></mc:Fallback></mc:AlternateContent>'
)
FADE_TRANSITION = (
    '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
    '<p:fade/></p:transition>'
)


def rgb(value: object) -> RGBColor:
    text = str(value or "#1E293B").lstrip("#")
    if len(text) != 6:
        text = "1E293B"
    try:
        return RGBColor(int(text[:2], 16), int(text[2:4], 16), int(text[4:], 16))
    except ValueError:
        return RGBColor(30, 41, 59)


def _channels(value: object) -> tuple[int, int, int]:
    text = str(value or "#1E293B").lstrip("#")
    if len(text) != 6:
        return (30, 41, 59)
    try:
        return (int(text[:2], 16), int(text[2:4], 16), int(text[4:], 16))
    except ValueError:
        return (30, 41, 59)


def _luminance(value: object) -> float:
    r, g, b = (c / 255 for c in _channels(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def readable_text(background: str, preferred: str | None = None) -> str:
    """Return the palette text colour when legible, otherwise black or white."""
    bg_lum = _luminance(background)
    if preferred:
        fg_lum = _luminance(preferred)
        light, dark = max(fg_lum, bg_lum), min(fg_lum, bg_lum)
        if (light + 0.05) / (dark + 0.05) >= 4.2:
            return preferred
    return "#FFFFFF" if bg_lum < 0.55 else "#0B1220"


class PptxBuilder:
    def __init__(self, ctx: AgentContext) -> None:
        self.ctx = ctx
        self.colors = [str(c) for c in (ctx.palette.get("colors") or DEFAULTS)]
        while len(self.colors) < 5:
            self.colors.append(DEFAULTS[len(self.colors)])
        self.bg, self.card_color, self.accent, self.highlight, self.fg = self.colors[:5]

        # Legibility first: never emit black text on a dark card (or white on light).
        self.fg = readable_text(self.card_color, self.fg)
        self.accent_fg = readable_text(self.accent, "#FFFFFF")
        self.highlight_fg = readable_text(self.highlight, "#FFFFFF")

        self.design = DesignRegistry().by_id(ctx.meta.get("design_id", ""))
        self.animation = AnimationRegistry().by_id(ctx.meta.get("animation_id", ""))
        self.mode = ctx.meta.get("animation_mode", "off") or "off"
        self.intensity = ctx.meta.get("animation_intensity", "balanced") or "balanced"
        self.sid = self._resolve_style()

        self._groups: dict[str, list[int]] = {}
        self._slide_no = 0
        self._total_slides = 0

    # ------------------------------------------------------------------ setup
    def _resolve_style(self) -> str:
        candidates = [
            self.ctx.meta.get("design_id", ""),
            self.ctx.theme.get("style", ""),
            self.design.get("id", ""),
        ]
        aliases = {}
        for item in DesignRegistry().all():
            for alias in item.get("aliases", []):
                aliases[alias] = item["id"]
        for raw in candidates:
            if not raw:
                continue
            if raw in aliases:
                return aliases[raw]
            if raw in LEGACY_TO_ARCHETYPE:
                return LEGACY_TO_ARCHETYPE[raw]
            if any(item.get("id") == raw for item in DesignRegistry().all()):
                return raw
        return "glassmorphism_card"

    # --------------------------------------------------------------- primitives
    def shape(
        self,
        slide,
        kind,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str | None = None,
        line: str | None = None,
        width: float = 1.0,
        group: str | None = None,
    ):
        shp = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill:
            shp.fill.solid()
            shp.fill.fore_color.rgb = rgb(fill)
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(width)
        else:
            shp.line.fill.background()
        if group:
            self.tag(group, shp)
        return shp

    def text(
        self,
        slide,
        value: object,
        x: float,
        y: float,
        w: float,
        h: float,
        size: float = 17,
        color: str | None = None,
        bold: bool = False,
        align=PP_ALIGN.LEFT,
        font: str = BODY_FONT,
        group: str | None = None,
        anchor=MSO_ANCHOR.TOP,
        line_spacing: float | None = None,
    ):
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        frame = box.text_frame
        frame.clear()
        frame.word_wrap = True
        frame.margin_left = frame.margin_right = Inches(0.04)
        frame.margin_top = frame.margin_bottom = Inches(0.02)
        frame.vertical_anchor = anchor
        para = frame.paragraphs[0]
        para.text = str(value)
        para.alignment = align
        para.font.name = font
        para.font.size = Pt(size)
        para.font.bold = bold
        para.font.color.rgb = rgb(color or self.fg)
        if line_spacing:
            para.line_spacing = line_spacing
        for run in para.runs:  # explicit run formatting survives Office round-trips
            run.font.name = font
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = rgb(color or self.fg)
        if group:
            self.tag(group, box)
        return box

    def tag(self, group: str, shape) -> None:
        self._groups.setdefault(group, []).append(shape.shape_id)

    def background(self, slide):
        self.shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, W, H, self.bg, group="background")

    def rule(self, slide, x, y, w, h=0.025, color=None, group=None):
        return self.shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, color or self.accent, group=group)

    @staticmethod
    def clip(value: object, limit: int = 110) -> str:
        text = " ".join(str(value).split())
        return text if len(text) <= limit else text[: limit - 1].rstrip() + "\u2026"

    # -------------------------------------------------------------- animation
    def _effects(self):
        """Yield (spid, preset, subtype, trigger, duration, delay, filter)."""
        choreography = (self.animation or {}).get("choreography") or {}
        intensity_scale = {"subtle": 0.7, "balanced": 1.0, "dynamic": 1.3}.get(self.intensity, 1.0)
        focal_ids = self._groups.get("focal", [])
        if focal_ids:
            yield (focal_ids[0], 23, 16, "withEffect", int(350 * intensity_scale), 0, "fade")
        for effect in choreography.get("effects", []):
            spids = self._groups.get(effect.get("group"), [])
            if not spids:
                continue
            duration = int(round(float(effect.get("duration", 300)) * intensity_scale))
            stagger = int(round(float(effect.get("stagger", 0)) * intensity_scale))
            trigger = effect.get("trigger", "withEffect")
            alternatives = effect.get("alternating_subtypes") or []
            for index, spid in enumerate(spids):
                subtype = effect.get("subtype", 0)
                if alternatives:
                    subtype = alternatives[index % len(alternatives)]
                if trigger == "clickEffect":
                    delay = int(effect.get("delay", 0))
                else:
                    delay = int(effect.get("delay", 0)) + index * stagger
                yield (spid, int(effect.get("preset", 10)), int(subtype), trigger, duration, delay,
                       effect.get("filter", "fade"))

    def _apply_transition(self, slide) -> None:
        choreography = (self.animation or {}).get("choreography") or {}
        xml = MORPH_TRANSITION if choreography.get("transition") == "morph" else FADE_TRANSITION
        try:
            slide._element.append(parse_xml(xml))
        except Exception:
            pass  # a transition is decoration; never block an export

    def _apply_native_animation(self, slide) -> None:
        effects = list(self._effects())
        if not effects:
            return
        try:
            timing = self._build_timing(effects)
            slide._element.append(timing)
        except Exception:
            pass  # keep the deck valid even if a PowerPoint version rejects an effect

    @staticmethod
    def _build_timing(effects):
        def node(tag: str, **attrs):
            element = etree.Element(qn("p:" + tag))
            for key, value in attrs.items():
                element.set(str(key), str(value))
            return element

        timing = node("timing")
        tn_list = node("tnLst")
        timing.append(tn_list)
        root_par = node("par")
        tn_list.append(root_par)
        root = node("cTn", id=1, dur="indefinite", restart="never", nodeType="tmRoot")
        root_par.append(root)
        root_children = node("childTnLst")
        root.append(root_children)

        seq = node("seq", concurrent=1, nextAc="seek")
        root_children.append(seq)
        main = node("cTn", id=2, dur="indefinite", nodeType="mainSeq")
        seq.append(main)
        main_children = node("childTnLst")
        main.append(main_children)

        next_id = 3
        for spid, preset, subtype, trigger, duration, delay, filter_name in effects:
            click_par = node("par")
            main_children.append(click_par)
            click_ctn = node("cTn", id=next_id, fill="hold")
            next_id += 1
            click_par.append(click_ctn)
            click_conds = node("stCondLst")
            click_conds.append(node("cond", delay="indefinite" if trigger == "clickEffect" else "0"))
            click_ctn.append(click_conds)
            click_children = node("childTnLst")
            click_ctn.append(click_children)

            wrapper_par = node("par")
            click_children.append(wrapper_par)
            wrapper = node("cTn", id=next_id, fill="hold")
            next_id += 1
            wrapper_par.append(wrapper)
            wrapper.append(node("stCondLst"))
            wrapper_children = node("childTnLst")
            wrapper.append(wrapper_children)

            behavior_par = node("par")
            wrapper_children.append(behavior_par)
            behavior = node(
                "cTn",
                id=next_id,
                presetID=preset,
                presetClass="entr",
                presetSubtype=subtype,
                fill="hold",
                nodeType=trigger,
            )
            next_id += 1
            behavior_par.append(behavior)
            behavior_conds = node("stCondLst")
            behavior_conds.append(node("cond", delay=max(0, delay)))
            behavior.append(behavior_conds)
            behavior_children = node("childTnLst")
            behavior.append(behavior_children)

            set_effect = node("set")
            behavior_children.append(set_effect)
            set_behavior = node("cBhvr")
            set_effect.append(set_behavior)
            set_behavior.append(node("cTn", id=next_id, dur=1, fill="hold"))
            next_id += 1
            target = node("tgtEl")
            target.append(node("spTgt", spid=spid))
            set_behavior.append(target)
            attrs = node("attrNameLst")
            attrs.append(node("attrName"))
            attrs[0].text = "style.visibility"
            set_behavior.append(attrs)
            to = node("to")
            to.append(node("strVal", val="visible"))
            set_effect.append(to)

            if filter_name != "appear" and duration > 0:
                anim = node("animEffect", transition="in", filter=filter_name)
                behavior_children.append(anim)
                anim_behavior = node("cBhvr")
                anim.append(anim_behavior)
                anim_behavior.append(node("cTn", id=next_id, dur=duration))
                next_id += 1
                target = node("tgtEl")
                target.append(node("spTgt", spid=spid))
                anim_behavior.append(target)

        for event, tag in (("onPrev", "prevCondLst"), ("onNext", "nextCondLst")):
            cond_list = node(tag)
            cond = node("cond", evt=event, delay=0)
            target = node("tgtEl")
            target.append(node("sldTgt"))
            cond.append(target)
            cond_list.append(cond)
            seq.append(cond_list)
        return timing

    # ------------------------------------------------------------ slide chrome
    def title_slide(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        self._groups = {}
        self.background(slide)
        sid = self.sid

        if sid == "blueprint_cad_grid":
            self.rule(slide, 0.45, 0.45, 12.43, 0.015, self.accent, "accent")
            self.rule(slide, 0.45, 7.03, 12.43, 0.015, self.accent, "accent")
            for x in (0.45, 12.86):
                self.rule(slide, x, 0.45, 0.015, 6.58, self.accent, "accent")
            self.text(slide, "DWG-01 / GENERAL ARRANGEMENT", 0.85, 0.9, 6, 0.3, 11,
                      self.accent, True, font=MONO_FONT, group="stamp")
        elif sid == "cyberpunk_hud_frame":
            self.shape(slide, MSO_SHAPE.OCTAGON, 0.55, 0.55, 12.23, 6.4, None,
                       self.highlight, 1.25, "frame")
            for i in range(3):
                self.shape(slide, MSO_SHAPE.PARALLELOGRAM, 11.2, 0.55 + i * 0.32, 0.55, 0.16,
                           self.highlight, group="accent")
        elif sid == "radial_sunburst_hub":
            for diameter in (2.0, 3.4, 4.8):
                offset = (6.4 - diameter) / 2
                self.shape(slide, MSO_SHAPE.OVAL, 10.6 + offset, 1.35 + offset,
                           diameter, diameter, None, self.accent, 0.75, "accent")
        elif sid == "oversized_watermark":
            self.text(slide, "01", 8.2, 0.55, 4.4, 4.0, 150, self.highlight, True,
                      PP_ALIGN.RIGHT, group="background")
        elif sid == "neo_brutalist_pop":
            self.shape(slide, MSO_SHAPE.RECTANGLE, 1.35, 1.55, 10.6, 4.5, "#000000",
                       group="accent")
        else:
            self.rule(slide, 0.85, 1.35, 11.6, 0.05, self.accent, "accent")

        card = self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.9, 1.55, 10.4, 4.35,
                          self.card_color, self.accent, 2.0, "frame")
        if sid == "neo_brutalist_pop":
            card.line.color.rgb = rgb("#000000")
            card.line.width = Pt(3.5)
        elif sid == "blueprint_cad_grid":
            card.fill.background()
            card.line.width = Pt(1.5)

        title = self.ctx.meta.get("deck_title") or self.ctx.theme.get("name", "Presentation")
        title_size = 30 if len(str(title)) > 45 else 38
        self.text(slide, self.clip(title, 120), 1.35, 2.15, 9.5, 1.35, title_size,
                  self.fg, True, group="header")
        self.text(slide, f"{self.ctx.theme.get('industry', 'General')}  |  {self._style_name()}",
                  1.4, 3.65, 9.4, 0.45, 16, self.accent, True, group="header")
        self.text(slide, f"Palette: {self.ctx.palette.get('name', 'Default')}   •   16:9   •   100% OFFLINE",
                  1.4, 4.35, 9.4, 0.35, 12, self.fg)
        if sid in ("blueprint_cad_grid", "minimalist_timeline_bar"):
            self.text(slide, "APPROVED FOR CONSTRUCTION / ISSUE FOR REVIEW", 8.6, 6.25, 4.0, 0.3,
                      9, self.highlight, True, PP_ALIGN.RIGHT, MONO_FONT, "stamp")
        self._decorate(slide)
        self._apply_transition(slide)
        self._apply_native_animation(slide)

    def _style_name(self) -> str:
        for item in DesignRegistry().all():
            if item.get("id") == self.sid:
                return str(item.get("name", self.sid))
        return self.sid.replace("_", " ").title()

    def _decorate(self, slide) -> None:
        self.rule(slide, 0.45, 7.16, 12.43, 0.018, self.highlight, "footer")
        self.text(slide, self.clip(self.ctx.meta.get("deck_title", "Presentation"), 42),
                  0.55, 7.18, 8.5, 0.22, 8, self.fg)
        self.text(slide, f"{self._slide_no:02d}", 11.9, 7.18, 0.85, 0.22, 8,
                  self.accent, True, PP_ALIGN.RIGHT)

    # ------------------------------------------------------------ content flow
    def stages(self, spec):
        if self.mode != "build_sequence":
            return [(list(spec.bullets), None)]
        steps = (self.animation or {}).get("steps", [])
        if not steps or not spec.bullets:
            return [(list(spec.bullets), None)]
        count = min(len(steps), len(spec.bullets))
        result, seen = [], set()
        for index in range(count):
            keep = max(1, round((index + 1) * len(spec.bullets) / count))
            visible = list(spec.bullets[:keep])
            key = tuple(visible)
            if key not in seen:
                seen.add(key)
                result.append((visible, f"Build {index + 1}/{count} - {steps[index].replace('_', ' ')}"))
        return result or [(list(spec.bullets), None)]

    def build(self, slides, target: Path) -> None:
        prs = Presentation()
        prs.slide_width = Inches(W)
        prs.slide_height = Inches(H)
        self._total_slides = 1 + sum(len(self.stages(spec)) for spec in slides)
        self._slide_no = 1
        self.title_slide(prs)
        for spec in slides:
            for bullets, stage in self.stages(spec):
                self._slide_no += 1
                slide = prs.slides.add_slide(prs.slide_layouts[6])
                self._groups = {}
                self.background(slide)
                visual = getattr(spec, "visual_spec", None)
                if visual and visual.placement in V4_PLACEMENTS:
                    self._render_v4(slide, spec, bullets, stage)
                else:
                    self._render(slide, spec, bullets, stage)
                if spec.notes:
                    try:
                        slide.notes_slide.notes_text_frame.text = spec.notes
                    except Exception:
                        pass
                self._decorate(slide)
                self._apply_transition(slide)
                if self.mode == "native":
                    self._apply_native_animation(slide)
        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))

    def _render(self, slide, spec, bullets, stage) -> None:
        layout = getattr(spec, "layout_type", "")
        renderer = getattr(self, "render_semantic_" + layout, None) if layout else None
        if renderer is None:
            renderer_id = "swiss_grid_editorial" if self.sid == "swiss_grid_editorial_archetype" else self.sid
            renderer = getattr(self, "render_" + renderer_id, None) or self.render_glassmorphism_card
        renderer(slide, spec, list(bullets), stage)
        if stage:
            self.text(slide, stage.upper(), 9.25, 0.30, 3.6, 0.28, 9,
                      self.accent, True, PP_ALIGN.RIGHT, MONO_FONT, "stamp")

    @staticmethod
    def _text_height(value: str, width: float, size: float) -> float:
        per_line = max(8, int((width * 72) / (size * 0.52)))
        lines = sum(max(1, math.ceil(len(part) / per_line)) for part in str(value).split("\n"))
        return lines * size * 1.25 / 72 + 0.08

    def _place_image(self, slide, path, x, y, width, height) -> None:
        try:
            if path and Path(path).exists():
                slide.shapes.add_picture(str(path), Inches(x), Inches(y),
                                         width=Inches(width), height=Inches(height))
                return
        except (OSError, ValueError):
            pass
        self.shape(slide, MSO_SHAPE.RECTANGLE, x, y, width, height, self.card_color, self.accent, 1.5)
        for index in range(1, 5):
            self.rule(slide, x + 0.3, y + height * index / 5, width - 0.6, 0.02, self.highlight)

    def _v4_text(self, slide, spec, bullets, x, y, width, title_size, bullet_size, limit,
                 focal_group: bool = True):
        title = self.clip(spec.title, 120)
        title_h = self._text_height(title, width, title_size)
        self.text(slide, title, x, y, width, title_h, title_size, self.fg, True,
                  group="focal" if focal_group else None)
        top = y + title_h + 0.18
        focal = getattr(spec, "focal_index", None)
        for index, bullet in enumerate(list(bullets)[:limit]):
            text = self.clip(bullet, 160)
            height = self._text_height(text, width, bullet_size)
            color = self.highlight if focal == index else self.fg
            self.text(slide, text, x, top, width, height, bullet_size, color, focal == index)
            top += height + 0.14
        return top

    def _render_v4(self, slide, spec, bullets, stage) -> None:
        placement = spec.visual_spec.placement
        path = getattr(spec, "image_path", "")
        if placement == "hero_banner":
            self._place_image(slide, path, 0, 0, W, 4.35)
            self.shape(slide, MSO_SHAPE.RECTANGLE, 0, 4.35, W, 3.15, self.card_color)
            self._v4_text(slide, spec, bullets, 0.7, 4.62, 11.9, 36, 17, 3)
        elif placement == "full_bleed_glass":
            self._place_image(slide, path, 0, 0, W, H)
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.85, 0.95, 7.9, 5.5,
                       self.card_color, self.highlight, 1.5)
            self._v4_text(slide, spec, bullets, 1.25, 1.35, 7.1, 44, 19, 4)
        elif placement == "giant_stat_split":
            self._place_image(slide, path, 7.33, 0, 6.0, H)
            self.shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, 7.33, H, self.card_color)
            hero = self._metric(next(iter(bullets), "")) or self.clip(spec.title, 10)
            hero_h = self._text_height(hero, 6.1, 76)
            self.text(slide, hero, 0.6, 0.75, 6.1, hero_h, 76, self.highlight, True, group="focal")
            subtitle = self.clip(spec.title, 80)
            subtitle_h = self._text_height(subtitle, 6.0, 20)
            self.text(slide, subtitle, 0.65, 0.75 + hero_h + 0.1,
                      6.0, subtitle_h, 20, self.fg, True)
            self._v4_text(slide, spec, bullets, 0.65, 0.85 + hero_h + subtitle_h + 0.3,
                          6.0, 20, 17, 3, focal_group=False)
        else:
            right = placement == "split_right"
            image_x = 6.667 if right else 0
            text_x = 0.65 if right else 7.32
            self._place_image(slide, path, image_x, 0, 6.666, H)
            self.shape(slide, MSO_SHAPE.RECTANGLE, 0 if right else 6.667, 0, 6.667, H,
                       self.card_color)
            self._v4_text(slide, spec, bullets, text_x, 0.95, 5.4, 40, 18, 4)
        if stage:
            self.text(slide, stage.upper(), 9.25, 6.82, 3.6, 0.22, 9,
                      self.accent, True, PP_ALIGN.RIGHT, MONO_FONT, "stamp")

    def _is_focal(self, spec, index: int) -> bool:
        focal = getattr(spec, "focal_index", None)
        return focal == index or (focal is None and index == 0)

    @staticmethod
    def _metric(bullet: str) -> str:
        match = re.search(r"[$€£]?\s?\d+(?:\.\d+)?\s?(?:%|x\b|days\b|hours\b|points\b|slides\b)?", bullet, re.I)
        return match.group(0).strip() if match else ""

    def render_semantic_bento(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 68), 0.8, 0.4, 11.7, 0.7, 26, self.accent, True,
                  group="header")
        tiles = ((0.8, 1.3, 5.6, 5.45), (6.65, 1.3, 5.88, 2.6), (6.65, 4.2, 5.88, 2.55))
        groups = ([0], [1, 2], [3, 4])
        labels = ("CORE ARCHITECTURE", "PERFORMANCE METRICS", "EDGE CONSTRAINTS")
        for (x, y, w, h), indices, label in zip(tiles, groups, labels):
            focal_here = any(self._is_focal(spec, i) for i in indices if i < len(bullets))
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, self.card_color,
                       self.accent if focal_here else self.highlight, 3.0 if focal_here else 1.0,
                       "focal" if focal_here else "items")
            self.text(slide, label, x + 0.25, y + 0.2, w - 0.5, 0.35, 13,
                      self.accent if focal_here else self.highlight, True, group="header")
            yy = y + 0.72
            for i in indices:
                if i < len(bullets):
                    self.text(slide, self.clip(bullets[i], 105 if w > 5.7 else 72),
                              x + 0.25, yy, w - 0.55, 1.15, 15 if w > 5.7 else 13.5,
                              self.fg, group="items")
                    yy += 1.25

    def render_semantic_kpi(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 68), 0.8, 0.4, 11.7, 0.7, 26, self.accent, True,
                  group="header")
        for index, x in enumerate((0.8, 4.816, 8.833)):
            focal = self._is_focal(spec, index)
            fill = self.accent if focal else self.card_color
            foreground = self.accent_fg if focal else self.fg
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.3, 3.7, 2.55, fill,
                       self.accent if focal else self.highlight, 3.0 if focal else 1.0,
                       "focal" if focal else "items")
            bullet = bullets[index] if index < len(bullets) else ""
            value = self._metric(bullet) or self.clip(bullet, 12) or "\u2014"
            self.text(slide, value, x + 0.2, 1.7, 3.3, 0.9, 38, self.accent_fg if focal else self.accent,
                      True, PP_ALIGN.CENTER, group="items")
            self.text(slide, self.clip(bullet, 72), x + 0.2, 2.85, 3.3, 0.75, 13, foreground,
                      align=PP_ALIGN.CENTER, group="items")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.8, 4.15, 11.73, 2.55,
                   self.card_color, self.highlight, 1.0, "items")
        self.text(slide, "SYNTHESIS", 1.1, 4.35, 10.8, 0.35, 14, self.highlight, True, group="header")
        yy = 4.85
        for item in (bullets[3:6] or bullets[:3]):
            self.text(slide, f"\u25aa {self.clip(item, 108)}", 1.15, yy, 10.9, 0.52, 15,
                      self.fg, group="items")
            yy += 0.58

    def render_semantic_process(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 70), 0.85, 0.4, 11.6, 0.7, 26, self.accent, True,
                  group="header")
        phases = bullets[:4] or ["Define phase"]
        for index in range(4):
            x = 0.8 + index * 2.95
            focal = self._is_focal(spec, index)
            fill = self.accent if focal else (self.highlight if index % 2 else self.card_color)
            chevron = self.shape(slide, MSO_SHAPE.CHEVRON, x, 1.4, 2.85, 1.15, fill,
                                 self.accent if focal else None, 3.0 if focal else 1.0,
                                 "focal" if focal else "items")
            label = self.clip(phases[index], 22) if index < len(phases) else f"PHASE {index + 1:02d}"
            self.text(slide, label, x + 0.3, 1.7, 2.2, 0.55, 14, readable_text(fill), True,
                      PP_ALIGN.CENTER, group="items")
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, 2.95, 2.75, 3.75,
                       self.card_color, self.accent if focal else self.highlight,
                       3.0 if focal else 1.0, "items")
            detail = self.clip(phases[index], 100) if index < len(phases) else "Gate criterion pending."
            self.text(slide, detail, x + 0.2, 3.25, 2.4, 3.1, 13.5, self.fg, group="items")

    def render_semantic_comparison(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 70), 0.85, 0.4, 11.6, 0.7, 26, self.accent, True,
                  PP_ALIGN.CENTER, group="header")
        middle = (len(bullets) + 1) // 2
        left, right = bullets[:middle], bullets[middle:]
        left_focal = any(self._is_focal(spec, i) for i in range(len(left)))
        for x, items, focal, label in ((0.8, left, left_focal, "BASELINE / CURRENT"),
                                       (6.983, right, not left_focal, "TARGET / PROPOSED")):
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.35, 5.55, 5.4,
                       self.card_color, self.accent if focal else self.highlight,
                       3.0 if focal else 1.0, "focal" if focal else "items")
            self.text(slide, label, x + 0.3, 1.6, 5.0, 0.4, 18,
                      self.accent if focal else self.highlight, True, group="header")
            yy = 2.35
            for item in items[:5]:
                self.text(slide, f"\u25aa {self.clip(item, 62)}", x + 0.3, yy, 4.95, 0.68,
                          15, self.fg, group="items")
                yy += 0.88
        self.shape(slide, MSO_SHAPE.OVAL, 6.266, 3.8, 0.8, 0.8, self.accent, group="accent")
        self.text(slide, "VS", 6.266, 3.96, 0.8, 0.4, 17, self.accent_fg, True,
                  PP_ALIGN.CENTER, group="accent")

    def render_semantic_spotlight(self, slide, spec, bullets, stage):
        focal_index = getattr(spec, "focal_index", 0) or 0
        focal_text = bullets[focal_index] if focal_index < len(bullets) else (bullets[0] if bullets else "")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.8, 1.3, 6.4, 5.45, self.accent,
                   self.accent, 3.0, "focal")
        self.text(slide, "KEY TAKEAWAY", 1.15, 1.6, 5.6, 0.4, 14, self.accent_fg, True,
                  group="header")
        self.text(slide, self.clip(focal_text, 150), 1.15, 2.25, 5.7, 2.0, 22,
                  self.accent_fg, True, group="items")
        rest = [item for index, item in enumerate(bullets) if index != focal_index]
        for index, item in enumerate(rest[:4]):
            y = 1.3 + index * 1.38
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 7.45, y, 5.08, 1.16,
                       self.card_color, self.highlight, 1.0, "items")
            self.text(slide, self.clip(item, 88), 7.7, y + 0.18, 4.6, 0.85, 14,
                      self.fg, group="items")

    # ------------------------------------------------------------- archetypes
    def render_blueprint_cad_grid(self, slide, spec, bullets, stage):
        self.shape(slide, MSO_SHAPE.RECTANGLE, 0.4, 0.4, 12.533, 6.7, None,
                   self.accent, 1.5, "frame")
        for i in range(1, 5):
            self.rule(slide, 0.4 + i * 2.506, 0.4, 0.015, 6.7, self.card_color, "accent")
        for i in range(1, 3):
            self.rule(slide, 0.4, 0.4 + i * 2.233, 12.533, 0.015, self.card_color, "accent")
        self.text(slide, self.clip(spec.title.upper(), 70), 0.85, 0.8, 10.0, 0.65, 24,
                  self.accent, True, font=MONO_FONT, group="header")
        self.rule(slide, 0.85, 1.55, 10.0, 0.03, self.accent, "accent")
        y = 1.85
        for index, bullet in enumerate(bullets[:5]):
            tag = ("[LOAD]", "[TOL]", "[SPEC]", "[CHK]", "[NOTE]")[index % 5]
            self.text(slide, f"{tag} {self.clip(bullet, 105)}", 0.95, y, 10.1, 0.65, 15,
                      self.fg, font=MONO_FONT, group="items")
            y += 0.82
        self.shape(slide, MSO_SHAPE.RECTANGLE, 8.8, 6.1, 4.13, 0.82, self.card_color,
                   self.accent, 1, "stamp")
        self.text(slide, "ENGINEERING TITLE BLOCK / REV A / SCALE 1:100", 8.95, 6.25, 3.9, 0.5,
                  9, self.fg, True, font=MONO_FONT, group="stamp")

    def render_cyberpunk_hud_frame(self, slide, spec, bullets, stage):
        self.shape(slide, MSO_SHAPE.OCTAGON, 0.7, 0.7, 11.93, 6.1, self.card_color,
                   self.accent, 2.25, "frame")
        self.shape(slide, MSO_SHAPE.HEXAGON, 1.0, 0.45, 5.75, 0.72, self.accent,
                   group="header")
        self.text(slide, self.clip(spec.title.upper(), 48), 1.28, 0.58, 5.1, 0.45, 18,
                  self.accent_fg, True, group="header")
        for i in range(3):
            self.shape(slide, MSO_SHAPE.PARALLELOGRAM, 11.05, 0.55 + i * 0.3, 0.42, 0.16,
                       self.highlight, group="accent")
        y = 1.75
        for bullet in bullets[:5]:
            self.text(slide, f"\u25b8 {self.clip(bullet, 104)}", 1.35, y, 10.45, 0.68, 16,
                      self.fg, group="items")
            self.rule(slide, 1.35, y + 0.72, 10.2, 0.012, self.highlight, "accent")
            y += 0.92
        self.text(slide, "SYS.ONLINE  //  TELEMETRY NOMINAL", 1.4, 6.28, 7.5, 0.25, 9,
                  self.highlight, True, PP_ALIGN.LEFT, MONO_FONT, "stamp")

    def render_executive_kpi_strip(self, slide, spec, bullets, stage):
        self.shape(slide, MSO_SHAPE.RECTANGLE, 0.8, 0.5, 11.73, 0.8, self.card_color, group="frame")
        self.rule(slide, 0.8, 1.3, 11.73, 0.05, self.accent, "accent")
        self.text(slide, self.clip(spec.title, 68), 1.05, 0.68, 10.8, 0.5, 22,
                  self.fg, True, group="header")
        metrics = bullets[:3]
        positions = (0.8, 4.816, 8.833)
        for i, x in enumerate(positions):
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, 1.55, 3.7, 2.1,
                       self.card_color, self.accent, 1.2, "items")
            self.rule(slide, x, 1.55, 3.7, 0.14, self.highlight if i == 1 else self.accent, "accent")
            value = self.clip(metrics[i], 26) if i < len(metrics) else "\u2014"
            self.text(slide, value, x + 0.22, 1.95, 3.26, 0.85, 26, self.accent, True,
                      PP_ALIGN.CENTER, group="items")
            self.text(slide, f"METRIC {i + 1:02d}", x + 0.22, 3.05, 3.26, 0.3, 10,
                      self.fg, False, PP_ALIGN.CENTER, MONO_FONT, "items")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.8, 3.9, 11.73, 2.85,
                   self.card_color, self.highlight, 1, "frame")
        self.text(slide, "SYNTHESIS & RECOMMENDATION", 1.1, 4.15, 10.8, 0.4, 16,
                  self.highlight, True, group="header")
        y = 4.75
        for bullet in bullets[3:6] or bullets[:3]:
            self.text(slide, f"\u25aa {self.clip(bullet, 110)}", 1.15, y, 10.8, 0.6, 15,
                      self.fg, group="items")
            y += 0.62

    def render_chevron_process_flow(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 72), 0.85, 0.55, 11.6, 0.6, 25,
                  self.accent, True, group="header")
        phases = bullets[:4] or ["Phase 01"]
        for i in range(4):
            x = 0.8 + i * 2.95
            fill = self.accent if i % 2 == 0 else self.highlight
            self.shape(slide, MSO_SHAPE.CHEVRON, x, 1.55, 2.85, 1.1, fill, group="items")
            label = self.clip(phases[i], 22) if i < len(phases) else f"PHASE {i + 1:02d}"
            self.text(slide, label, x + 0.28, 1.8, 2.25, 0.6, 14, readable_text(fill),
                      True, PP_ALIGN.CENTER, group="items")
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, 3.0, 2.75, 3.45,
                       self.card_color, self.accent, 1, "frame")
            detail = self.clip(phases[i], 120) if i < len(phases) else "Gate criterion pending."
            self.text(slide, detail, x + 0.18, 3.25, 2.4, 2.95, 13.5, self.fg, group="items")
            if i < 3:
                self.rule(slide, x + 2.8, 2.05, 0.15, 0.1, self.highlight, "accent")

    def render_dual_comparison_matrix(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 72), 0.85, 0.6, 11.6, 0.6, 25,
                  self.accent, True, PP_ALIGN.CENTER, group="header")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.8, 1.6, 5.55, 5.2,
                   self.card_color, self.highlight, 1.5, "frame")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.983, 1.6, 5.55, 5.2,
                   self.card_color, self.accent, 2.5, "frame")
        self.text(slide, "BASELINE / CURRENT STATE", 1.1, 1.85, 5.0, 0.45, 18,
                  self.highlight, True, group="header")
        self.text(slide, "TARGET / PROPOSED ARCHITECTURE", 7.25, 1.85, 5.0, 0.45, 18,
                  self.accent, True, group="header")
        middle = (len(bullets) + 1) // 2
        for y, bullet in zip((2.55, 3.35, 4.15, 4.95, 5.75), bullets[:middle]):
            self.text(slide, f"\u25aa {self.clip(bullet, 62)}", 1.1, y, 4.95, 0.68, 15,
                      self.fg, group="items")
        for y, bullet in zip((2.55, 3.35, 4.15, 4.95, 5.75), bullets[middle:]):
            self.text(slide, f"\u25aa {self.clip(bullet, 62)}", 7.25, y, 4.95, 0.68, 15,
                      self.fg, group="items")
        self.shape(slide, MSO_SHAPE.OVAL, 6.266, 3.8, 0.8, 0.8, self.accent, group="accent")
        self.text(slide, "VS", 6.266, 3.96, 0.8, 0.4, 17, self.accent_fg, True,
                  PP_ALIGN.CENTER, group="accent")

    def render_swiss_grid_editorial(self, slide, spec, bullets, stage):
        self.rule(slide, 0.8, 0.7, 11.733, 0.035, self.accent, "accent")
        self.rule(slide, 4.6, 0.7, 0.035, 6.1, self.highlight, "accent")
        self.text(slide, self.clip(spec.title, 60), 0.85, 1.35, 3.5, 2.6, 29,
                  self.accent, True, group="header")
        self.text(slide, f"{self.ctx.theme.get('industry', 'GENERAL').upper()} / ANALYSIS",
                  0.85, 5.95, 3.4, 0.4, 10, self.fg, True, PP_ALIGN.LEFT, MONO_FONT, "stamp")
        self.shape(slide, MSO_SHAPE.RECTANGLE, 4.9, 1.0, 7.633, 5.8, self.card_color,
                   group="frame")
        y = 1.45
        for bullet in bullets[:6]:
            self.text(slide, self.clip(bullet, 108), 5.25, y, 6.95, 0.82, 16,
                      self.fg, line_spacing=1.25, group="items")
            y += 0.94

    def render_neo_brutalist_pop(self, slide, spec, bullets, stage):
        self.shape(slide, MSO_SHAPE.RECTANGLE, 1.05, 1.65, 11.6, 5.1, "#000000",
                   group="accent")
        self.shape(slide, MSO_SHAPE.RECTANGLE, 0.85, 1.45, 11.6, 5.1, self.card_color,
                   "#000000", 3.5, "frame")
        self.shape(slide, MSO_SHAPE.RECTANGLE, 0.85, 0.65, 7.5, 0.65, self.accent,
                   "#000000", 3, "header")
        self.text(slide, self.clip(spec.title.upper(), 48), 1.05, 0.78, 7.1, 0.45, 20,
                  self.accent_fg, True, group="header")
        y = 1.9
        for bullet in bullets[:5]:
            self.text(slide, f"\u25a0 {self.clip(bullet, 100)}", 1.3, y, 10.6, 0.75, 17,
                      self.fg, True, group="items")
            y += 0.98

    def render_glassmorphism_card(self, slide, spec, bullets, stage):
        for x, y in ((10.4, 0.7), (0.75, 4.55)):
            self.shape(slide, MSO_SHAPE.OVAL, x, y, 2.6, 2.6, self.highlight, group="accent")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.9, 0.85, 11.533, 5.8,
                   self.card_color, self.accent, 1.75, "frame")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 1.25, 1.25, 0.14, 0.65,
                   self.accent, group="accent")
        self.text(slide, self.clip(spec.title, 72), 1.65, 1.15, 10.1, 0.7, 26,
                  self.fg, True, group="header")
        y = 2.05
        for bullet in bullets[:4]:
            self.text(slide, f"\u25c6 {self.clip(bullet, 110)}", 1.6, y, 10.1, 0.85, 17,
                      self.fg, group="items")
            y += 1.08

    def render_bento_grid_dashboard(self, slide, spec, bullets, stage):
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 0.8, 1.5, 5.6, 5.3,
                   self.card_color, self.accent, 1.5, "frame")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.65, 1.5, 5.883, 2.5,
                   self.card_color, self.highlight, 1.5, "frame")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.65, 4.3, 5.883, 2.5,
                   self.card_color, self.highlight, 1.5, "frame")
        self.text(slide, self.clip(spec.title, 46), 1.1, 1.75, 5.0, 0.8, 21,
                  self.accent, True, group="header")
        self.text(slide, "CORE ARCHITECTURE", 6.95, 1.75, 5.2, 0.4, 14,
                  self.highlight, True, group="header")
        self.text(slide, "PERFORMANCE / CONSTRAINTS", 6.95, 4.55, 5.2, 0.4, 14,
                  self.highlight, True, group="header")
        for y, bullet in zip((2.75, 3.6, 4.45, 5.3), bullets[:4]):
            self.text(slide, f"\u25aa {self.clip(bullet, 52)}", 1.1, y, 5.0, 0.75, 15,
                      self.fg, group="items")
        for y, bullet in zip((2.35, 3.15), bullets[4:6]):
            self.text(slide, self.clip(bullet, 78), 6.95, y, 5.2, 0.72, 14, self.fg, group="items")
        for y, bullet in zip((5.2, 6.0), bullets[6:8]):
            self.text(slide, self.clip(bullet, 78), 6.95, y, 5.2, 0.72, 14, self.fg, group="items")

    def render_isometric_layer_stack(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 64), 5.8, 0.55, 6.7, 0.6, 24,
                  self.accent, True, group="header")
        palette = (self.accent, self.highlight, self.card_color)
        for index, y in enumerate((1.7, 3.1, 4.5)):
            fill = palette[index % 3]
            self.shape(slide, MSO_SHAPE.DIAMOND, 1.1, y, 3.6, 1.6, fill, self.accent,
                       1.5, "items")
            label = self.clip(bullets[index], 18) if index < len(bullets) else f"LAYER {index + 1}"
            self.text(slide, label, 1.65, y + 0.58, 2.5, 0.5, 14, readable_text(fill),
                      True, PP_ALIGN.CENTER, group="items")
            self.rule(slide, 4.7, y + 0.78, 1.1, 0.03, self.accent, "accent")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 5.8, 1.5, 6.733, 5.3,
                   self.card_color, self.accent, 1.5, "frame")
        y = 1.95
        for bullet in bullets[:5]:
            self.text(slide, f"\u2192 {self.clip(bullet, 88)}", 6.15, y, 6.0, 0.82, 15,
                      self.fg, group="items")
            y += 0.94

    def render_oversized_watermark(self, slide, spec, bullets, stage):
        self.text(slide, "01", 0.6, 0.8, 5.0, 5.8, 180, self.highlight, True,
                  group="background")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 3.2, 1.6, 9.333, 5.0,
                   self.card_color, self.accent, 2, "frame")
        self.text(slide, self.clip(spec.title, 60), 3.65, 1.95, 8.4, 0.8, 27,
                  self.accent, True, group="header")
        y = 3.0
        for bullet in bullets[:4]:
            self.text(slide, f"\u2014 {self.clip(bullet, 92)}", 3.7, y, 8.3, 0.72, 16,
                      self.fg, group="items")
            y += 0.85

    def render_minimalist_timeline_bar(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 68), 0.9, 0.55, 11.5, 0.6, 25,
                  self.accent, True, group="header")
        self.rule(slide, 1.0, 4.15, 11.333, 0.08, self.accent, "frame")
        for index, x in enumerate((1.8, 4.8, 7.8, 10.8)):
            self.shape(slide, MSO_SHAPE.OVAL, x - 0.225, 3.955, 0.45, 0.45,
                       self.bg, self.accent, 3, "items")
            above = index % 2 == 0
            y = 1.7 if above else 4.85
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x - 1.35, y, 2.7, 1.9,
                       self.card_color, self.highlight, 1, "frame")
            label = self.clip(bullets[index], 78) if index < len(bullets) else f"MILESTONE {index + 1}"
            self.text(slide, label, x - 1.18, y + 0.22, 2.35, 1.45, 13.5,
                      self.fg, True, group="items")
            if above:
                self.rule(slide, x - 0.01, y + 1.9, 0.02, 2.2, self.highlight, "accent")
            else:
                self.rule(slide, x - 0.01, 4.4, 0.02, 0.45, self.highlight, "accent")

    def render_concentric_circle_target(self, slide, spec, bullets, stage):
        self.text(slide, self.clip(spec.title, 64), 6.4, 0.55, 6.1, 0.6, 24,
                  self.accent, True, group="header")
        rings = (
            (1.0, 1.7, 4.8, self.card_color, self.highlight, "OUTER"),
            (1.75, 2.45, 3.3, self.highlight, self.accent, "MID-TIER"),
            (2.5, 3.2, 1.8, self.accent, self.fg, "CORE"),
        )
        for index, (x, y, size, fill, line, label) in enumerate(rings):
            self.shape(slide, MSO_SHAPE.OVAL, x, y, size, size, fill, line, 1.75, "items")
            self.text(slide, label, x, y + size / 2 - 0.18, size, 0.36, 13,
                      readable_text(fill), True, PP_ALIGN.CENTER, group="items")
        zones = ("INNER CORE", "OPERATIONAL PERIMETER", "OUTER BOUNDARY")
        for index, y in enumerate((1.7, 3.4, 5.1)):
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 6.4, y, 6.133, 1.4,
                       self.card_color, self.accent if index == 0 else self.highlight,
                       1.25, "frame")
            self.text(slide, zones[index], 6.7, y + 0.16, 5.6, 0.4, 17,
                      self.accent if index == 0 else self.highlight, True, group="header")
            detail = self.clip(bullets[index], 85) if index < len(bullets) else "Define scope boundary."
            self.text(slide, detail, 6.7, y + 0.66, 5.6, 0.6, 14, self.fg, group="items")

    def render_frosted_sidebar_nav(self, slide, spec, bullets, stage):
        rail = self.shape(slide, MSO_SHAPE.RECTANGLE, 0, 0, 3.8, 7.5,
                          self.card_color, group="frame")
        rail.line.fill.background()
        self.rule(slide, 3.78, 0, 0.03, 7.5, self.accent, "accent")
        self.rule(slide, 0, 1.4, 0.16, 1.2, self.accent, "accent")
        self.text(slide, self.clip(spec.title, 42), 0.45, 1.45, 3.0, 1.2, 23,
                  self.accent, True, group="header")
        self.text(slide, f"SECTION / {self.ctx.theme.get('industry', 'GENERAL').upper()}",
                  0.45, 0.65, 3.0, 0.35, 9, self.fg, True, PP_ALIGN.LEFT, MONO_FONT, "stamp")
        self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, 4.3, 0.8, 8.233, 5.9,
                   self.card_color, self.highlight, 1, "frame")
        y = 1.3
        for index, bullet in enumerate(bullets[:6]):
            self.text(slide, f"{index + 1:02d}", 4.65, y, 0.55, 0.5, 14,
                      self.accent, True, PP_ALIGN.LEFT, MONO_FONT, "accent")
            self.text(slide, self.clip(bullet, 92), 5.3, y, 6.9, 0.75, 16,
                      self.fg, group="items")
            y += 0.92

    def render_radial_sunburst_hub(self, slide, spec, bullets, stage):
        self.shape(slide, MSO_SHAPE.OVAL, 5.566, 3.15, 2.2, 2.2, self.accent,
                   self.fg, 3, "header")
        self.text(slide, self.clip(spec.title, 20), 5.75, 3.85, 2.0, 0.8, 15,
                  self.accent_fg, True, PP_ALIGN.CENTER, group="header")
        cards = ((0.8, 1.4), (8.433, 1.4), (0.8, 4.8), (8.433, 4.8))
        for index, (x, y) in enumerate(cards):
            self.shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, 4.1, 2.1,
                       self.card_color, self.highlight, 1.5, "items")
            heading = f"NODE {index + 1:02d}"
            self.text(slide, heading, x + 0.25, y + 0.2, 3.6, 0.4, 14,
                      self.accent, True, group="items")
            detail = self.clip(bullets[index], 88) if index < len(bullets) else "Interface specification."
            self.text(slide, detail, x + 0.25, y + 0.75, 3.6, 1.1, 13.5,
                      self.fg, group="items")
            sx = x + 4.1 if x < 5 else x - 0.6
            sy = y + 1.4
            self.rule(slide, min(sx, 6.66), sy, abs(6.66 - sx) + 0.4, 0.035,
                      self.highlight, "accent")
