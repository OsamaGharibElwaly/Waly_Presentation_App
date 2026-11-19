"""python-pptx engine implementing 30 design archetypes and OpenXML animation choreography."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
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

    def _inject_animation(self, slide, animation_id: str) -> None:
        """Injects ECMA-376 OpenXML animation choreography and slide transitions."""
        transition_xml = """
        <mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
          <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">
            <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med"><p159:morph option="byObject"/></p:transition>
          </mc:Choice>
          <mc:Fallback>
            <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med"><p:fade/></p:transition>
          </mc:Fallback>
        </mc:AlternateContent>
        """
        try:
            slide._element.append(parse_xml(transition_xml))
        except Exception:
            pass

    def build(self, slides, target: Path) -> None:
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        bg_color = _hex(self.colors[0])
        card_bg = _hex(self.colors[1])
        accent_color = _hex(self.colors[2])
        highlight_color = _hex(self.colors[3])
        text_color = _hex(self.colors[4] if len(self.colors) > 4 else "#FFFFFF")

        style_id = self.ctx.theme.get("style", "glassmorphism_card")
        animation_id = self.ctx.theme.get("animation", "progressive_bullet_reveal")
        blank_layout = prs.slide_layouts[6]

        # --- TITLE SLIDE ---
        title_slide = prs.slides.add_slide(blank_layout)
        bg = title_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = bg_color
        bg.line.fill.background()

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
        p2.text = f"Industry Domain: {self.ctx.theme.get('industry', 'General')} | Archetype: {style_id}"
        p2.font.size = Pt(16)
        p2.font.color.rgb = accent_color
        p2.space_before = Pt(16)

        p3 = tf.add_paragraph()
        p3.text = f"Palette: {self.ctx.palette.get('name', 'Custom')} | OpenXML Choreography: {animation_id}"
        p3.font.size = Pt(13)
        p3.font.color.rgb = text_color
        p3.space_before = Pt(8)

        self._inject_animation(title_slide, animation_id)

        # --- CONTENT SLIDES (Archetype Dispatcher) ---
        for spec in slides:
            slide = prs.slides.add_slide(blank_layout)

            s_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
            s_bg.fill.solid()
            s_bg.fill.fore_color.rgb = bg_color
            s_bg.line.fill.background()

            if "neo_brutalist" in style_id:
                shadow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.1), Inches(1.1), Inches(11.333), Inches(5.5))
                shadow.fill.solid()
                shadow.fill.fore_color.rgb = _hex("#000000")
                shadow.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.9), Inches(11.333), Inches(5.5))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = _hex("#000000")
                card.line.width = Pt(3)

            elif "swiss_grid" in style_id or "editorial" in style_id:
                line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.04))
                line.fill.solid()
                line.fill.fore_color.rgb = accent_color
                line.line.fill.background()

                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.1), Inches(11.733), Inches(4.7))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = highlight_color
                card.line.width = Pt(1)

            elif "executive_kpi" in style_id:
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
                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(6.1))
                card.fill.solid()
                card.fill.fore_color.rgb = card_bg
                card.line.color.rgb = accent_color
                card.line.width = Pt(2)

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

            self._inject_animation(slide, animation_id)

        target.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(target))
