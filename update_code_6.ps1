# ============================================================
# update_code_6.ps1 - 15 Design Systems + 15 Animation Sequences
# Run from project root: .\update_code_6.ps1
# ============================================================
[CmdletBinding()]
param([string]$ProjectRoot = $PSScriptRoot, [switch]$SkipCompileCheck)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path $ProjectRoot).Path
$Utf8 = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList $false
foreach ($Required in @('backend/pptx_engine/builder.py', 'frontend/ui/main_window.py', 'backend/pipeline/orchestrator.py')) {
    if (-not (Test-Path (Join-Path $Root $Required))) { throw "Project root check failed: missing $Required. Pass -ProjectRoot <project-folder>." }
}
function Write-ProjectFile([string]$RelativePath, [string]$Content) {
    $Path = Join-Path $Root $RelativePath
    $Parent = Split-Path $Path -Parent
    if (-not (Test-Path $Parent)) { New-Item -ItemType Directory -Path $Parent -Force | Out-Null }
    if (Test-Path $Path) { Copy-Item $Path ($Path + '.bak_code6') -Force; Write-Host "[backup] $RelativePath.bak_code6" -ForegroundColor DarkGray }
    [IO.File]::WriteAllText($Path, $Content, $Utf8)
    Write-Host "[updated] $RelativePath" -ForegroundColor Green
}
Write-Host "=== Offline AI Presentation Factory / Code Update 6 ===" -ForegroundColor Cyan
Write-Host "Root: $Root" -ForegroundColor DarkGray

$Designs = @'
{
 "design_systems":[
  {"id":"swiss_grid_editorial","name":"Swiss Grid Editorial","category":"Editorial","description":"Disciplined modular grid, whitespace, precise alignment and editorial typography.","best_for":["research","engineering reports","consulting","education"],"default_palette":"Minimalist Scandinavian","geometry":"Asymmetric grid-aligned columns, hairline rules, numbered sections and rectangular regions.","typography":"Editorial headings, restrained sans-serif body and compact metadata.","diagram_treatment":"Align charts and diagrams to a shared baseline and column grid.","prompt":"Use a disciplined modular grid, generous whitespace, precise alignment, restrained accents, thin dividers and editorial typography. Align charts and diagrams to the grid."},
  {"id":"executive_corporate","name":"Executive Corporate","category":"Business","description":"Decision-oriented layouts with KPI strips, consistent headers and concise evidence blocks.","best_for":["board decks","business cases","management reports","proposals"],"default_palette":"Cyber Slate & Neon Blue","geometry":"Consistent header/footer, KPI strips, metric cards and balanced columns.","typography":"Strong executive headlines and readable sans-serif body.","diagram_treatment":"Clean charts, KPI cards and evidence-to-action blocks.","prompt":"Use a clean corporate grid, consistent headers, restrained navy and neutrals, KPI cards and decision-oriented layouts. Prioritize credibility and readability."},
  {"id":"engineering_blueprint","name":"Engineering Blueprint","category":"Engineering","description":"Technical drawing language with dimension lines, leaders, callouts and precise diagram frames.","best_for":["mechanical","civil","electrical","industrial","systems engineering"],"default_palette":"Cyber Slate & Neon Blue","geometry":"Drawing frames, section markers, dimension arrows, coordinate axes and numbered callouts.","typography":"Technical sans-serif with monospaced metadata and legible labels.","diagram_treatment":"Diagram-first orthographic panels, exploded views and annotated figures.","prompt":"Use precise technical geometry, dimension lines, leaders, numbered callouts and consistent line weights. Preserve measurements and units exactly; never fabricate specifications."},
  {"id":"technical_dark_neon","name":"Technical Dark / Neon","category":"Technology","description":"High-contrast dark panels with restrained cyan, electric-blue or violet accents.","best_for":["AI","software architecture","robotics","electronics","cybersecurity"],"default_palette":"Cyber Slate & Neon Blue","geometry":"Dark cards, network nodes, data-flow connectors and thin borders.","typography":"High-contrast sans-serif headings and compact technical labels.","diagram_treatment":"Crisp node-link diagrams and directional flows; restrained effects.","prompt":"Use a deep charcoal canvas, crisp high-contrast panels, restrained neon accents, system diagrams, network nodes and precise labels. Keep effects subtle."},
  {"id":"bento_grid","name":"Bento Grid","category":"Product","description":"Modular cards with varied sizes and clear content grouping.","best_for":["product strategy","software features","dashboards","summaries"],"default_palette":"Minimalist Scandinavian","geometry":"Unequal modular cards, consistent gutters and generous padding.","typography":"Bold compact card titles and concise body text.","diagram_treatment":"Group related metrics, diagrams and explanations into independent modules.","prompt":"Use a modular bento grid with varied card sizes, consistent gutters, rounded containers and clear grouping. Give each card one message."},
  {"id":"minimalist_scandinavian","name":"Minimalist Scandinavian","category":"Minimal","description":"Light neutral canvas, restrained color, whitespace and simple geometry.","best_for":["education","portfolio","strategy","general business"],"default_palette":"Minimalist Scandinavian","geometry":"Open layouts, simple blocks, subtle separators and generous margins.","typography":"Clean sans-serif, restrained weights and comfortable line spacing.","diagram_treatment":"Simple flat diagrams with minimal decoration.","prompt":"Use a light neutral canvas, generous whitespace, restrained accents, simple geometry and clean typography. Remove decoration that does not aid comprehension."},
  {"id":"neo_brutalist","name":"Neo-Brutalist","category":"Bold","description":"Bold blocks, thick outlines, hard offset shadows and high-contrast typography.","best_for":["creative technology","workshops","bold concepts"],"default_palette":"Editorial Obsidian & Gold","geometry":"Rectangular blocks, thick borders, hard offset shadows and asymmetric compositions.","typography":"Heavy display headings and concise supporting text.","diagram_treatment":"Bold simple diagrams with strong outlines.","prompt":"Use bold rectangular blocks, thick dark outlines, hard offset shadows and strong typography. Keep diagrams simple and legible."},
  {"id":"architecture_materiality","name":"Architecture & Materiality","category":"Architecture","description":"Spatial composition inspired by concrete, timber, glass, plans and material samples.","best_for":["architecture","construction","urban design","materials"],"default_palette":"Warm Architectural Earth","geometry":"Large drawing zones, material swatches, section bands and calm asymmetry.","typography":"Elegant headings with clear technical captions.","diagram_treatment":"Plans, sections, elevations, material boards and spatial annotations.","prompt":"Use architectural editorial language, material-inspired neutrals, spatial balance, plan-like grids and clear section drawings."},
  {"id":"data_visualization","name":"Data Visualization / Analytical","category":"Analytics","description":"Evidence-led layouts prioritizing charts, scales, labels, comparisons and sources.","best_for":["analytics","operations","finance","research results"],"default_palette":"Minimalist Scandinavian","geometry":"Chart-first panels, aligned axes, compact legends and annotation zones.","typography":"Numerically clear labels, strong chart titles and compact source notes.","diagram_treatment":"Accurate charts and tables with units, axes, series and sources.","prompt":"Prioritize accurate data visualization. Preserve values and units, label axes and series, use restrained gridlines and clear legends. Never invent data."},
  {"id":"isometric_exploded_view","name":"Isometric / Exploded View","category":"Engineering","description":"Layered spatial component views with separation, numbered parts and assembly logic.","best_for":["mechanical assemblies","product systems","infrastructure","technical training"],"default_palette":"Cyber Slate & Neon Blue","geometry":"Isometric groupings, separated layers and component callouts.","typography":"Compact technical labels and readable descriptions.","diagram_treatment":"Exploded component relationships and assembly order.","prompt":"Use an isometric or exploded-view composition with separated components, numbered callouts and visible assembly relationships. Do not invent dimensions."},
  {"id":"process_flow_chevron","name":"Process Flow / Chevron","category":"Process","description":"Directional stages, transitions, inputs, outputs and decision points.","best_for":["workflows","manufacturing","operations","pipelines"],"default_palette":"Construction Safety & Steel","geometry":"Aligned process blocks, directional connectors, decision diamonds and stage bands.","typography":"Short action-led labels and concise descriptions.","diagram_treatment":"Make sequence direction, branches, inputs and outputs unmistakable.","prompt":"Use a clear left-to-right process flow with aligned stages, directional connectors, explicit decisions, inputs and outputs."},
  {"id":"timeline_roadmap","name":"Timeline / Roadmap","category":"Planning","description":"Chronological milestones, phases, dependencies and delivery checkpoints.","best_for":["project plans","engineering programs","product roadmaps"],"default_palette":"Cyber Slate & Neon Blue","geometry":"Timeline, milestone markers, phase bands and dependency lines.","typography":"Date-first labels and concise milestone descriptions.","diagram_treatment":"Preserve chronology and distinguish milestones, durations and dependencies.","prompt":"Use a structured timeline with clear milestones, phases, dates and dependencies. Preserve chronology; do not invent dates."},
  {"id":"comparison_matrix","name":"Comparison Matrix","category":"Decision","description":"Side-by-side evaluation with criteria, trade-offs and recommendation emphasis.","best_for":["design alternatives","vendor selection","technical decisions","risk reviews"],"default_palette":"Minimalist Scandinavian","geometry":"Aligned comparison columns, criterion rows and highlighted decision cells.","typography":"Clear row labels and compact cell text.","diagram_treatment":"Compare like-for-like criteria and distinguish facts from judgments.","prompt":"Use a precise comparison matrix with aligned criteria, balanced columns, readable labels and explicit trade-offs. Do not fabricate scores."},
  {"id":"scientific_research","name":"Scientific Research / Academic","category":"Research","description":"Evidence hierarchy with methods, results, figures, limitations and citations.","best_for":["papers","experiments","technical research","academic lectures"],"default_palette":"Minimalist Scandinavian","geometry":"Figure panels, method/result sections, caption zones and citation footer.","typography":"Formal readable hierarchy with compact captions and references.","diagram_treatment":"Separate method, observation, interpretation and limitation.","prompt":"Use scientific editorial style with methods, results, figures, captions, citations and limitations. Separate evidence from interpretation."},
  {"id":"futuristic_hud","name":"Futuristic HUD / Systems Interface","category":"Technology","description":"Instrument-panel framing, technical readouts, node maps and restrained interface detailing.","best_for":["control systems","AI platforms","network operations","advanced engineering"],"default_palette":"Quantum Deep Purple","geometry":"Framed panels, segmented headers, fine rules and structured readout zones.","typography":"Technical micro-labels paired with legible main text.","diagram_treatment":"System maps and readouts with consistent status semantics; no fake telemetry.","prompt":"Use a futuristic systems-interface aesthetic with framed panels, fine technical rules and restrained accents. Never invent telemetry or status."}
 ]
}
'@
$Animations = @'
{
 "animation_sequences":[
  {"id":"progressive_build","name":"Progressive Build","category":"General","description":"Reveal headline, structure, details and takeaway in stages.","steps":["title_and_context","main_structure","supporting_details","evidence_and_takeaway"],"default_intensity":"balanced"},
  {"id":"left_to_right_process","name":"Left-to-Right Process Flow","category":"Engineering","description":"Reveal process stages in directional order.","steps":["process_start","stage_one","stage_two","stage_three","process_output"],"default_intensity":"balanced"},
  {"id":"engineering_exploded_assembly","name":"Engineering Exploded Assembly","category":"Engineering","description":"Reveal components from base to final assembly.","steps":["base_component","primary_components","secondary_components","connectors_and_fasteners","assembled_result"],"default_intensity":"balanced"},
  {"id":"layered_system_architecture","name":"Layer-by-Layer System Architecture","category":"Engineering","description":"Reveal boundaries, layers, integrations and data flow.","steps":["system_boundary","input_layer","service_layer","data_layer","integrations_security","data_flow"],"default_intensity":"balanced"},
  {"id":"circuit_signal_propagation","name":"Circuit Signal Propagation","category":"Engineering","description":"Trace signal through components and outputs.","steps":["circuit_overview","input_source","processing_components","signal_path","output_response"],"default_intensity":"dynamic"},
  {"id":"data_pipeline_etl","name":"Data Pipeline / ETL Flow","category":"Engineering","description":"Reveal extraction, transformation, validation, storage and consumption.","steps":["source_systems","extraction","transformation","validation","storage","consumption"],"default_intensity":"balanced"},
  {"id":"timeline_milestone_reveal","name":"Timeline Milestone Reveal","category":"Planning","description":"Reveal milestones chronologically, then dependencies.","steps":["timeline_axis","milestone_one","milestone_two","milestone_three","dependencies"],"default_intensity":"subtle"},
  {"id":"before_after_transformation","name":"Before / After Transformation","category":"General","description":"Show baseline, intervention and comparison.","steps":["before_state","intervention","after_state","measured_comparison"],"default_intensity":"balanced"},
  {"id":"zoom_technical_detail","name":"Zoom Into Technical Detail","category":"Engineering","description":"Move from system overview to component-level detail.","steps":["system_overview","subsystem_focus","component_detail","technical_annotation"],"default_intensity":"subtle"},
  {"id":"branching_decision_tree","name":"Branching Decision Tree","category":"Engineering","description":"Reveal decision criteria, branches and outcomes.","steps":["decision_node","criteria","branch_a","branch_b","outcomes_and_selected_path"],"default_intensity":"balanced"},
  {"id":"network_node_activation","name":"Network Node Activation","category":"Engineering","description":"Reveal nodes, links, clusters and network flow.","steps":["network_topology","core_nodes","edge_nodes","connections","end_to_end_flow"],"default_intensity":"dynamic"},
  {"id":"chart_series_reveal","name":"Chart Series Reveal","category":"Data","description":"Introduce axes, baseline, series and annotations.","steps":["chart_frame_and_axes","baseline","series_one","additional_series","annotations_and_takeaway"],"default_intensity":"balanced"},
  {"id":"structural_assembly","name":"Construction / Structural Assembly","category":"Engineering","description":"Reveal foundation, supports, members and completed frame.","steps":["foundation","supports","primary_members","secondary_members","completed_structure"],"default_intensity":"balanced"},
  {"id":"formula_derivation","name":"Formula / Equation Derivation","category":"Engineering","description":"Build derivation from known terms to final expression.","steps":["known_variables","starting_equation","transformation_one","transformation_two","final_expression"],"default_intensity":"subtle"},
  {"id":"focus_spotlight","name":"Focus / Spotlight Emphasis","category":"General","description":"Progressively focus attention on key regions.","steps":["full_context","focus_area_one","focus_area_two","key_conclusion"],"default_intensity":"subtle"}
 ]
}
'@
Write-ProjectFile 'knowledge/catalog/design_systems.json' $Designs
Write-ProjectFile 'knowledge/catalog/animation_sequences.json' $Animations

$DesignRegistry = @'
"""Local registry for the 15 stable presentation design-system IDs."""
from pathlib import Path
import json
CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"
class DesignRegistry:
    def __init__(self, catalog_dir=None):
        self.path = (catalog_dir or CATALOG_DIR) / "design_systems.json"
        self.data = json.loads(self.path.read_text(encoding="utf-8-sig")) if self.path.exists() else {"design_systems": []}
    def all(self): return list(self.data.get("design_systems", []))
    def by_id(self, key):
        return next((x for x in self.all() if x.get("id") == key), self.all()[0] if self.all() else {})
'@
Write-ProjectFile 'frontend/theme_factory/design_registry.py' $DesignRegistry
$AnimationRegistry = @'
"""Local registry for the 15 presentation build-sequence definitions."""
from pathlib import Path
import json
CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"
class AnimationRegistry:
    def __init__(self, catalog_dir=None):
        self.path = (catalog_dir or CATALOG_DIR) / "animation_sequences.json"
        self.data = json.loads(self.path.read_text(encoding="utf-8-sig")) if self.path.exists() else {"animation_sequences": []}
    def all(self): return list(self.data.get("animation_sequences", []))
    def by_id(self, key):
        return next((x for x in self.all() if x.get("id") == key), {})
'@
Write-ProjectFile 'frontend/theme_factory/animation_registry.py' $AnimationRegistry
$PromptComposer = @'
"""Build deterministic style instructions for local LLM prompt workflows."""
from frontend.theme_factory.design_registry import DesignRegistry
from frontend.theme_factory.animation_registry import AnimationRegistry
def compose_style_prompt(design_id, animation_id, palette, intensity="balanced", animation_mode="off"):
    d = DesignRegistry().by_id(design_id)
    a = AnimationRegistry().by_id(animation_id or "")
    lines = ["You are a senior presentation designer and technical communication specialist.",
      "DESIGN SYSTEM: " + d.get("name", "Minimalist Scandinavian"),
      "VISUAL DIRECTION: " + d.get("prompt", ""), "GEOMETRY: " + d.get("geometry", ""),
      "TYPOGRAPHY: " + d.get("typography", ""), "DIAGRAMS: " + d.get("diagram_treatment", ""),
      "PALETTE: " + palette.get("name", "Default") + " | " + ", ".join(palette.get("colors", [])),
      "Preserve every supplied fact, figure, equation, unit, date and reference.",
      "Never invent dimensions, standards, citations, test results, telemetry or performance claims.",
      "Prefer accurate diagrams, charts and tables where they improve communication."]
    if a and animation_mode != "off":
        lines += ["ANIMATION SEQUENCE: " + a.get("name", ""), "STEPS: " + " -> ".join(a.get("steps", [])),
                  "INTENSITY: " + intensity, "Do not let animation alter the selected design system or palette."]
    else: lines.append("ANIMATION: None; use static slides.")
    return "\n".join(lines)
'@
Write-ProjectFile 'backend/pptx_engine/style_prompt.py' $PromptComposer

# PPTX renderer: distinct geometry families + click-through staged build output.
$Builder = @'
"""16:9 style-aware PowerPoint renderer. Build-sequence mode creates staged slides, not native object animations."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from backend.agents.base.agent import AgentContext
from frontend.theme_factory.design_registry import DesignRegistry
from frontend.theme_factory.animation_registry import AnimationRegistry
W, H = 13.333, 7.5
DEFAULTS = ["#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC"]
def rgb(c):
    c = str(c or "#1E293B").lstrip("#")
    if len(c) != 6: c = "1E293B"
    try: return RGBColor(int(c[:2],16), int(c[2:4],16), int(c[4:],16))
    except ValueError: return RGBColor(30,41,59)
class PptxBuilder:
    def __init__(self, ctx: AgentContext):
        self.ctx=ctx; self.colors=list(ctx.palette.get("colors") or DEFAULTS)
        while len(self.colors)<5: self.colors.append(DEFAULTS[len(self.colors)])
        self.bg,self.card_color,self.accent,self.highlight,self.fg=self.colors[:5]
        self.design=DesignRegistry().by_id(ctx.meta.get("design_id","minimalist_scandinavian"))
        self.sid=self.design.get("id","minimalist_scandinavian")
        self.animation=AnimationRegistry().by_id(ctx.meta.get("animation_id",""))
        self.mode=ctx.meta.get("animation_mode","off")
    def shape(self, slide, kind, x,y,w,h, fill=None, line=None, width=1):
        sh=slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill: sh.fill.solid(); sh.fill.fore_color.rgb=rgb(fill)
        else: sh.fill.background()
        if line: sh.line.color.rgb=rgb(line); sh.line.width=Pt(width)
        else: sh.line.fill.background()
        return sh
    def text(self, slide, value, x,y,w,h, size=18, color=None, bold=False, align=PP_ALIGN.LEFT):
        box=slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf=box.text_frame
        tf.clear(); tf.word_wrap=True; tf.margin_left=Inches(.04); tf.margin_right=Inches(.04)
        p=tf.paragraphs[0]; p.text=str(value); p.alignment=align; p.font.name="Aptos"; p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=rgb(color or self.fg)
        return box
    def background(self, slide): self.shape(slide,MSO_SHAPE.RECTANGLE,0,0,W,H,self.bg)
    def card(self, slide,x,y,w,h,square=False,heavy=False):
        return self.shape(slide,MSO_SHAPE.RECTANGLE if square else MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h,self.card_color,"#000000" if heavy else self.accent,3 if heavy else 1.2)
    def title_slide(self, prs):
        s=prs.slides.add_slide(prs.slide_layouts[6]); self.background(s)
        if self.sid=="neo_brutalist":
            self.card(s,1.35,1.45,10.5,4.3,True,True); self.card(s,1.1,1.2,10.5,4.3,True,True)
        elif self.sid in ("swiss_grid_editorial","scientific_research"):
            self.text(s,"01 / PRESENTATION",.9,.8,4,.3,10,self.accent,True); self.shape(s,MSO_SHAPE.RECTANGLE,.9,1.35,11.5,.04,self.accent)
        else: self.card(s,.9,1.2,11.5,4.8,self.sid in ("engineering_blueprint","data_visualization"))
        title=self.ctx.meta.get("deck_title") or self.ctx.theme.get("name","Presentation")
        self.text(s,title,1.35,2.0,10.4,1.3,36,self.fg,True)
        self.text(s,f"{self.ctx.theme.get('industry','General')}  |  {self.design.get('name','Design system')}",1.4,3.55,10,.5,17,self.accent,True)
        self.text(s,f"Palette: {self.ctx.palette.get('name','Default')}",1.4,4.25,8,.35,12,self.fg)
    def content_slide(self, prs, spec, bullets, stage=None):
        s=prs.slides.add_slide(prs.slide_layouts[6]); self.background(s); sid=self.sid
        if sid=="neo_brutalist":
            self.card(s,1.0,1.05,11.3,5.7,True,True); self.card(s,.8,.85,11.3,5.7,True,True); ty,by=1.25,2.15
        elif sid in ("swiss_grid_editorial","scientific_research"):
            self.shape(s,MSO_SHAPE.RECTANGLE,.85,1.55,11.6,.04,self.accent); self.card(s,.85,1.85,11.6,4.95,True); ty,by=2.1,2.9
        elif sid=="executive_corporate":
            self.shape(s,MSO_SHAPE.RECTANGLE,.8,.75,11.7,.16,self.accent); self.card(s,.8,1.1,11.7,5.7); ty,by=1.4,2.3
        elif sid=="bento_grid":
            self.card(s,.8,.8,11.7,1.25); self.card(s,.8,2.25,7.3,4.45); self.card(s,8.3,2.25,4.2,4.45); ty,by=1.0,2.6
        elif sid=="architecture_materiality":
            self.card(s,.8,.8,7.4,5.95,True); self.card(s,8.45,.8,4.05,5.95); ty,by=1.15,2.0
        elif sid in ("engineering_blueprint","isometric_exploded_view"):
            self.card(s,.75,.75,11.85,6.0,True)
            for x in (1.0,12.25): self.shape(s,MSO_SHAPE.RECTANGLE,x,1.0,.025,5.4,self.accent)
            ty,by=1.1,2.0
        elif sid=="futuristic_hud":
            self.card(s,.8,.8,11.7,5.95,True)
            for x in (1.0,9.8): self.shape(s,MSO_SHAPE.RECTANGLE,x,1.0,2.0,.04,self.accent)
            ty,by=1.2,2.1
        else:
            self.card(s,.8,.8,11.7,5.95,sid in ("data_visualization","process_flow_chevron","timeline_roadmap","comparison_matrix","minimalist_scandinavian")); ty,by=1.2,2.1
        self.text(s,spec.title,1.25,ty,10.6,.7,27,self.accent,True)
        if stage: self.text(s,stage.upper(),9.5,.35,3,.25,9,self.accent,True,PP_ALIGN.RIGHT)
        if sid in ("bento_grid","executive_corporate") and len(bullets)>1:
            cols=2 if len(bullets)<4 else 3; cw=10.5/cols-.12
            for i,b in enumerate(bullets):
                row,col=divmod(i,cols); x=1.2+col*(cw+.18); y=by+row*1.35
                self.card(s,x,y,cw,1.15); self.text(s,b,x+.12,y+.12,cw-.24,.9,14,self.fg)
        else:
            y=by
            for i,b in enumerate(bullets):
                if y>6.45: break
                self.text(s,f"{i+1:02d}   {b}",1.3,y,10.4,.72,17,self.fg); y+=.88
        if spec.notes:
            try: s.notes_slide.notes_text_frame.text=spec.notes
            except Exception: pass
        return s
    def stages(self,spec):
        steps=self.animation.get("steps",[])
        if self.mode!="build_sequence" or not steps or not spec.bullets: return [(list(spec.bullets),None)]
        n=min(len(steps),len(spec.bullets)); out=[]; seen=set()
        for i in range(n):
            k=max(1,round((i+1)*len(spec.bullets)/n)); visible=list(spec.bullets[:k]); key=tuple(visible)
            if key not in seen:
                seen.add(key); out.append((visible,f"Build {i+1}/{n} - {steps[i].replace('_',' ')}"))
        return out or [(list(spec.bullets),None)]
    def build(self, slides, target: Path):
        prs=Presentation(); prs.slide_width=Inches(W); prs.slide_height=Inches(H); self.title_slide(prs)
        for spec in slides:
            for bullets,label in self.stages(spec): self.content_slide(prs,spec,bullets,label)
        target.parent.mkdir(parents=True,exist_ok=True); prs.save(str(target))
'@
Write-ProjectFile 'backend/pptx_engine/builder.py' $Builder

# Patch current UI in-place: preserve existing tabs, themes, palettes and PDF export.
$Patch = @'
from pathlib import Path
p = Path("frontend/ui/main_window.py")
s = p.read_text(encoding="utf-8-sig")
if "DesignRegistry" not in s:
    s = s.replace("from backend.pipeline.orchestrator import Orchestrator", "from backend.pipeline.orchestrator import Orchestrator\nfrom frontend.theme_factory.design_registry import DesignRegistry\nfrom frontend.theme_factory.animation_registry import AnimationRegistry\nfrom backend.pptx_engine.style_prompt import compose_style_prompt")
if "self.design_combo" not in s:
    marker = "        v_insp.addWidget(self.palette_combo)\n"
    add = marker + """
        self.design_registry = DesignRegistry()
        self.animation_registry = AnimationRegistry()
        v_insp.addWidget(QLabel("Design System (15 styles):"))
        self.design_combo = QComboBox()
        for item in self.design_registry.all(): self.design_combo.addItem(item["name"], item["id"])
        idx = self.design_combo.findData("engineering_blueprint")
        if idx >= 0: self.design_combo.setCurrentIndex(idx)
        v_insp.addWidget(self.design_combo)
        v_insp.addWidget(QLabel("Animation Sequence (15 sequences):"))
        self.animation_combo = QComboBox()
        self.animation_combo.addItem("None / Static", "")
        for item in self.animation_registry.all(): self.animation_combo.addItem(item["name"], item["id"])
        v_insp.addWidget(self.animation_combo)
        v_insp.addWidget(QLabel("Animation Output:"))
        self.animation_mode_combo = QComboBox()
        self.animation_mode_combo.addItem("Off - static slides", "off")
        self.animation_mode_combo.addItem("Build sequence - advance slides to reveal", "build_sequence")
        v_insp.addWidget(self.animation_mode_combo)
        v_insp.addWidget(QLabel("Motion Intensity:"))
        self.animation_intensity_combo = QComboBox()
        for value in ("subtle", "balanced", "dynamic"): self.animation_intensity_combo.addItem(value.title(), value)
        self.animation_intensity_combo.setCurrentIndex(1)
        v_insp.addWidget(self.animation_intensity_combo)
"""
    if marker not in s: raise SystemExit("Palette selector anchor was not found; no UI changes applied.")
    s = s.replace(marker, add, 1)
old = '        orch = Orchestrator(theme=theme, palette=palette, meta={"deck_title": self.name_input.text().strip()})'
new = """        design_id = self.design_combo.currentData() or "minimalist_scandinavian"
        animation_id = self.animation_combo.currentData() or ""
        animation_mode = self.animation_mode_combo.currentData() or "off"
        intensity = self.animation_intensity_combo.currentData() or "balanced"
        if not animation_id: animation_mode = "off"
        style_prompt = compose_style_prompt(design_id, animation_id, palette, intensity, animation_mode)
        meta = {"deck_title": self.name_input.text().strip(), "design_id": design_id,
                "animation_id": animation_id, "animation_mode": animation_mode,
                "animation_intensity": intensity, "style_prompt": style_prompt}
        orch = Orchestrator(theme=theme, palette=palette, meta=meta)"""
if old in s: s = s.replace(old, new, 1)
elif '"design_id": design_id' not in s: raise SystemExit("Orchestrator export anchor was not found.")
s = s.replace("Generated 30-Archetype styled {kind.upper()} presentation at:", "Generated styled {kind.upper()} presentation at:")
p.write_text(s, encoding="utf-8")
'@
$PatchPath = Join-Path $Root '.update_code_6_patch.py'
[IO.File]::WriteAllText($PatchPath, $Patch, $Utf8)
try {
    Push-Location $Root
    python $PatchPath
    if ($LASTEXITCODE -ne 0) { throw 'UI patch failed.' }
} finally { Pop-Location; Remove-Item $PatchPath -ErrorAction SilentlyContinue }
Write-Host '[updated] frontend/ui/main_window.py' -ForegroundColor Green

if (-not $SkipCompileCheck) {
    Push-Location $Root
    try {
        python -c "import json,pathlib; a=json.loads(pathlib.Path('knowledge/catalog/design_systems.json').read_text(encoding='utf-8-sig')); b=json.loads(pathlib.Path('knowledge/catalog/animation_sequences.json').read_text(encoding='utf-8-sig')); assert len(a['design_systems'])==15 and len(b['animation_sequences'])==15; print('Validated: 15 design systems + 15 animation sequences')"
        if ($LASTEXITCODE -ne 0) { throw 'Catalog validation failed.' }
        python -m compileall -q backend frontend
        if ($LASTEXITCODE -ne 0) { throw 'Python compile check failed.' }
        Write-Host '[passed] JSON validation and Python compileall' -ForegroundColor Green
    } finally { Pop-Location }
}
Write-Host "`n=== Code Update 6 completed ===" -ForegroundColor Cyan
Write-Host 'Launch: python -m frontend.main' -ForegroundColor Yellow
Write-Host 'Build sequence uses staged slides for click-through reveal; it is not native PowerPoint object animation.' -ForegroundColor Magenta
