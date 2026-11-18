# `PPTX_STYLES.md` — The 30-Item Pareto Presentation Design & Animation Specification

**Target Architecture:** `OfflineAIPresentationFactory` (`backend/pptx_engine/builder.py` & `knowledge/catalog/`)  
**Canvas Standard:** Widescreen `16:9` (`13.333"` × `7.5"` | `12,192,000` × `6,858,000` EMUs)  
**Domain Focus:** Engineering, Architecture, Heavy Construction, Systems Design, & Technical Literature  

---

## 1. System Architecture & Palette Slot Mapping

To ensure seamless integration with `AgentContext` and `PptxBuilder`, every style and animation sequence in this catalog maps directly to the 5-slot hex array defined in `knowledge/catalog/palettes.json`:

| Slot Index | Semantic Role | Usage in `python-pptx` Geometry |
| :--- | :--- | :--- |
| `colors[0]` | **Canvas Background** | Full-bleed base slide fill (`0, 0, 13.333", 7.5"`) |
| `colors[1]` | **Surface / Container** | Primary card fill, HUD panels, matrix cells |
| `colors[2]` | **Primary Accent** | Headers, active nodes, glowing borders, kinetic bars |
| `colors[3]` | **Secondary Highlight** | Sub-headers, secondary connectors, chart/KPI indicators |
| `colors[4]` | **Primary Typography** | High-contrast body text and technical specifications |

---

## Part I: Top 15 Engineering & Technical Design Archetypes (Shapes, Geometry & Layouts)

These 15 structural blueprints cover the 80% Pareto distribution of high-impact technical, architectural, and executive presentations using native `MSO_SHAPE` primitives.

---

### 1. Blueprint CAD Grid (`blueprint_cad_grid`)
* **Domain Fit:** Civil Engineering, Structural Mechanics, Architecture
* **Visual Composition:** Deep technical drafting canvas overlaid with orthogonal hairlines, corner registration crosshairs, and a bottom-right engineering title block stamp.
* **Shape & Geometry (`python-pptx`):**
  * **Canvas:** `MSO_SHAPE.RECTANGLE` (`0, 0, 13.333", 7.5"`) filled with `colors[0]`.
  * **Drafting Border:** Hollow `MSO_SHAPE.RECTANGLE` (`0.4", 0.4", 12.533", 6.7"`), `1.5pt` solid border in `colors[2]`.
  * **Grid Hairlines:** 4 vertical and 2 horizontal `MSO_SHAPE.RECTANGLE` dividers (`0.015"` thickness) in `colors[1]`.
  * **Title Stamp Box:** `MSO_SHAPE.RECTANGLE` (`8.8", 6.1", 4.133", 1.0"`) in bottom-right corner with `1pt` border (`colors[2]`) housing slide metadata.
* **Typography & Hierarchy:** Monospace/Geometric Sans (`Consolas` or `Segoe UI`), `24pt` Bold ALL-CAPS header in `colors[2]`, `15pt` technical bullets in `colors[4]`.
* **LLM Prompt Injection Snippet:**
  > *"Format slides as technical CAD schematics: concise, specification-driven bullet points prefixed with parameter tags (e.g., `[LOAD]`, `[TOLERANCE]`, `[SPEC]`). Keep bullets under 12 words."*

---

### 2. Cyberpunk HUD Telemetry Frame (`cyberpunk_hud_frame`)
* **Domain Fit:** Robotics, Quantum Computing, Aerospace, Defense Systems
* **Visual Composition:** Chamfered octagonal tactical display with corner targeting brackets and high-contrast neon edge illumination.
* **Shape & Geometry (`python-pptx`):**
  * **Main HUD Container:** `MSO_SHAPE.OCTAGON` or `MSO_SHAPE.SNIP_2_DIAG_RECTANGLE` (`0.7", 0.7", 11.933", 6.1"`), fill `colors[1]`, border `2.25pt` in `colors[2]`.
  * **Header Pill:** `MSO_SHAPE.HEXAGON` (`1.0", 0.45", 5.5", 0.55"`) overlapping top-left edge, fill `colors[2]`, text in `colors[0]`.
  * **Telemetry Accent Bars:** Three small `MSO_SHAPE.PARALLELOGRAM` (`11.2", 0.55", 0.3", 0.2"`) in `colors[3]` at top right.
* **Typography & Hierarchy:** `22pt` Bold header inside the top-left hexagon; `16pt` crisp sans-serif bullets inside the chamfered frame (`colors[4]`).
* **LLM Prompt Injection Snippet:**
  > *"Adopt a mission-control telemetry tone. Structure each slide with a system subsystem header and 3–5 high-signal operational metrics or architectural states."*

---

### 3. Executive KPI Strip (`executive_kpi_strip`)
* **Domain Fit:** Construction Management, Project Controls, Enterprise Strategy
* **Visual Composition:** Three equal-width vertical metric cards anchored across the upper canvas, topped with thick status accent bars, above a unified synthesis container.
* **Shape & Geometry (`python-pptx`):**
  * **Header Banner:** `MSO_SHAPE.RECTANGLE` (`0.8", 0.5", 11.733", 0.8"`), fill `colors[0]`, bottom underline `0.05"` in `colors[2]`.
  * **3 KPI Cards:** Three `MSO_SHAPE.ROUNDED_RECTANGLE` blocks (`width: 3.7"`, `height: 2.1"`, `y: 1.55"`, `x: [0.8", 4.816", 8.833"]`), fill `colors[1]`.
  * **Top Accent Caps:** Three `MSO_SHAPE.RECTANGLE` strips (`width: 3.7"`, `height: 0.14"`, `y: 1.55"`) in `colors[2]`.
  * **Bottom Analysis Panel:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`0.8", 3.9", 11.733", 3.0"`), fill `colors[1]`, border `1pt` in `colors[3]`.
* **Typography & Hierarchy:** `32pt` Bold metric callout in `colors[2]` inside each top card; `16pt` body insights (`colors[4]`) in the lower panel.
* **LLM Prompt Injection Snippet:**
  > *"Lead every slide with 3 quantifiable KPIs or structural benchmarks (e.g., `99.98% Uptime | -42% Latency | 14ms Cycle`) followed by 3 concise analytical takeaways."*

---

### 4. Chevron Process Flow (`chevron_process_flow`)
* **Domain Fit:** Manufacturing Pipelines, Site Logistics, CI/CD & Data Engineering
* **Visual Composition:** Horizontal sequence of interlocking chevron arrows illustrating sequential phases, paired with aligned vertical detail columns below each stage.
* **Shape & Geometry (`python-pptx`):**
  * **Stage Chevrons (4 Phases):** `MSO_SHAPE.CHEVRON` (`width: 2.85"`, `height: 1.1"`, `y: 1.7"`, `x: [0.8", 3.75", 6.7", 9.65"]`), fill stepping between `colors[2]` and `colors[3]`.
  * **Detail Columns:** Four `MSO_SHAPE.ROUNDED_RECTANGLE` (`width: 2.75"`, `height: 3.9"`, `y: 3.0"`), fill `colors[1]`, border `1pt` in `colors[2]`.
* **Typography & Hierarchy:** `16pt` Bold centered phase titles inside chevrons; `14pt` left-aligned phase deliverables inside columns.
* **LLM Prompt Injection Snippet:**
  > *"Organize the slide into 3 to 4 sequential engineering phases. Format each bullet as `Phase Name: Actionable deliverable or gate criterion`."*

---

### 5. Dual Comparison Matrix (`dual_comparison_matrix`)
* **Domain Fit:** Trade-off Studies, Legacy vs. Modern Architecture, Material Selection
* **Visual Composition:** Symmetrical split-screen layout with a central circular `VS` badge separating two contrasting technical states.
* **Shape & Geometry (`python-pptx`):**
  * **Left Panel (Baseline/Problem):** `MSO_SHAPE.ROUNDED_RECTANGLE` (`0.8", 1.6", 5.55", 5.2"`), fill `colors[1]`, border `1.5pt` in `colors[3]`.
  * **Right Panel (Target/Solution):** `MSO_SHAPE.ROUNDED_RECTANGLE` (`6.983", 1.6", 5.55", 5.2"`), fill `colors[1]`, border `2.5pt` in `colors[2]`.
  * **Center Bridge Badge:** `MSO_SHAPE.OVAL` (`6.266", 3.8", 0.8", 0.8"`), fill `colors[2]`, bold label `"VS"` in `colors[0]`.
* **Typography & Hierarchy:** `20pt` Bold column headers; `16pt` paired comparison bullets (`colors[4]`).
* **LLM Prompt Injection Snippet:**
  > *"Structure content as a direct binary comparison (e.g., Current State vs. Proposed Architecture). Provide balanced, parallel bullet points for both sides."*

---

### 6. Swiss Grid Editorial (`swiss_grid_editorial`)
* **Domain Fit:** Architecture Theory, Urban Planning, Academic Research, Literature
* **Visual Composition:** Asymmetric 1/3 to 2/3 layout separated by razor-thin structural rules, emphasizing generous negative space and typographic rigor.
* **Shape & Geometry (`python-pptx`):**
  * **Top Rule:** `MSO_SHAPE.RECTANGLE` (`0.8", 0.7", 11.733", 0.03"`), fill `colors[2]`.
  * **Vertical Spine Divider:** `MSO_SHAPE.RECTANGLE` (`4.6", 0.7", 0.03"`, `6.1"`), fill `colors[3]`.
  * **Left Title Zone:** Borderless text frame (`0.8", 1.0", 3.5", 5.5"`).
  * **Right Content Zone:** `MSO_SHAPE.RECTANGLE` (`4.9", 1.0", 7.633", 5.8"`), fill `colors[1]` (subtle tint), no border.
* **Typography & Hierarchy:** `30pt` Bold title in the left column (`colors[2]`); `17pt` generous line-spaced prose bullets (`1.3x` spacing) in the right column.
* **LLM Prompt Injection Snippet:**
  > *"Write in an authoritative, editorial research tone. Use complete, well-crafted analytical statements rather than fragmented shorthand."*

---

### 7. Neo-Brutalist Structural Pop (`neo_brutalist_pop`)
* **Domain Fit:** Industrial Design, Brutalist Architecture, High-Impact Pitch Decks
* **Visual Composition:** Sharp-edged rectangular cards with thick solid borders and hard-offset solid drop shadows creating tactile architectural depth.
* **Shape & Geometry (`python-pptx`):**
  * **Offset Shadow:** `MSO_SHAPE.RECTANGLE` (`1.05", 1.65", 11.6", 5.1"`), fill `#000000` (or `colors[3]`), no border.
  * **Foreground Card:** `MSO_SHAPE.RECTANGLE` (`0.85", 1.45", 11.6", 5.1"`), fill `colors[1]`, border `3.5pt` solid `#000000` (or `colors[2]`).
  * **Header Tag:** `MSO_SHAPE.RECTANGLE` (`0.85", 0.65", 7.5", 0.65"`), fill `colors[2]`, border `3pt` solid `#000000`.
* **Typography & Hierarchy:** `24pt` Heavy Bold header; `17pt` high-contrast bullets with `24pt` paragraph spacing.
* **LLM Prompt Injection Snippet:**
  > *"Use punchy, high-conviction engineering statements. Eliminate filler words; focus on bold structural claims and decisive outcomes."*

---

### 8. Glassmorphism Layered Card (`glassmorphism_card`)
* **Domain Fit:** Cloud Infrastructure, AI Software Architecture, Smart Cities
* **Visual Composition:** Floating rounded translucent card framed by a crisp luminescent border, anchored by a vertical accent pill on the left edge.
* **Shape & Geometry (`python-pptx`):**
  * **Ambient Backdrop Accents:** Two `MSO_SHAPE.OVAL` (`width: 3.5", height: 3.5"`) at top-right and bottom-left in `colors[3]` (subtle decorative depth).
  * **Primary Glass Container:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`0.9", 0.85", 11.533", 5.8"`), fill `colors[1]`, border `1.75pt` in `colors[2]`.
  * **Left Indicator Pill:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`1.25", 1.25", 0.14", 0.65"`), fill `colors[2]`.
* **Typography & Hierarchy:** `26pt` Bold title aligned beside the indicator pill; `17pt` clean sans-serif bullets (`colors[4]`).
* **LLM Prompt Injection Snippet:**
  > *"Present clean, modular system concepts. Limit to 4 bullets per slide, each focusing on a distinct architectural layer or capability."*

---

### 9. Bento Grid Dashboard (`bento_grid_dashboard`)
* **Domain Fit:** IoT Telemetry, Multi-Module Software Suites, Building Management Systems
* **Visual Composition:** Asymmetric modular tile grid (one tall hero tile on the left, two stacked horizontal tiles on the right) maximizing information density without clutter.
* **Shape & Geometry (`python-pptx`):**
  * **Left Hero Tile:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`0.8", 1.5", 5.6", 5.3"`), fill `colors[1]`, border `1.5pt` in `colors[2]`.
  * **Top-Right Tile:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`6.65", 1.5", 5.883", 2.5"`), fill `colors[1]`, border `1.5pt` in `colors[3]`.
  * **Bottom-Right Tile:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`6.65", 4.3", 5.883", 2.5"`), fill `colors[1]`, border `1.5pt` in `colors[3]`.
* **Typography & Hierarchy:** `20pt` Bold tile headers in `colors[2]`; `15pt` concise bullets distributed across the three modular compartments.
* **LLM Prompt Injection Snippet:**
  > *"Group slide content into 3 distinct functional clusters: Core Architecture (primary), Performance Metrics (secondary), and Edge Constraints (tertiary)."*

---

### 10. Isometric Layer Stack (`isometric_layer_stack`)
* **Domain Fit:** Full-Stack Engineering, Geological Strata, Composite Material Design
* **Visual Composition:** Vertically stacked isometric diamond planes on the left representing system layers, linked via horizontal callout lines to right-hand technical descriptions.
* **Shape & Geometry (`python-pptx`):**
  * **3 Stacked Diamonds (Left):** `MSO_SHAPE.DIAMOND` (`width: 3.6", height: 1.6"`, `x: 1.1"`, `y: [1.7", 3.1", 4.5"]`), alternating fills `colors[2]`, `colors[3]`, `colors[1]` with `1.5pt` borders.
  * **Connector Lines:** Three `MSO_SHAPE.RECTANGLE` (`x: 4.7", width: 1.1", height: 0.03"`) linking diamond vertices to the right panel.
  * **Right Specification Card:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`5.8", 1.5", 6.733", 5.3"`), fill `colors[1]`, border `1.5pt` in `colors[2]`.
* **Typography & Hierarchy:** `15pt` Bold layer labels centered in diamonds; `16pt` detailed layer specifications on the right.
* **LLM Prompt Injection Snippet:**
  > *"Structure the slide as a 3-tier vertical stack (e.g., Hardware Layer, Middleware Layer, Application Layer) with corresponding specifications for each tier."*

---

### 11. Oversized Number Watermark (`oversized_watermark`)
* **Domain Fit:** Milestones, Engineering Principles, Sequential Case Studies
* **Visual Composition:** Massive architectural index numeral (`01`, `02`, `03`) anchored in the background behind a crisp foreground specification card.
* **Shape & Geometry (`python-pptx`):**
  * **Watermark Text Box:** Borderless frame (`0.6", 0.8", 5.0", 5.8"`), containing `180pt` Bold slide index (`01`) in `colors[1]` (or muted `colors[3]`).
  * **Foreground Content Card:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`3.2", 1.6", 9.333", 5.0"`), fill `colors[1]`, border `2pt` in `colors[2]`.
* **Typography & Hierarchy:** `180pt` Bold background numeral; `28pt` Bold title and `17pt` bullets in the foreground frame.
* **LLM Prompt Injection Snippet:**
  > *"Frame this slide around a single core engineering pillar or numbered milestone. Provide a clear thesis statement followed by 3 supporting proofs."*

---

### 12. Minimalist Timeline Milestone Bar (`minimalist_timeline_bar`)
* **Domain Fit:** Construction Schedules, R&D Roadmaps, Critical Path Method (CPM)
* **Visual Composition:** Horizontal central axis bar pierced by circular milestone nodes, with alternating callout boxes positioned above and below the axis.
* **Shape & Geometry (`python-pptx`):**
  * **Horizontal Axis Spine:** `MSO_SHAPE.RECTANGLE` (`1.0", 4.15", 11.333", 0.08"`), fill `colors[2]`.
  * **4 Milestone Nodes:** `MSO_SHAPE.OVAL` (`width: 0.45", height: 0.45"`, `y: 3.96"`, `x: [1.8", 4.8", 7.8", 10.8"]`), fill `colors[0]`, border `3pt` in `colors[2]`.
  * **Alternating Callout Cards:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`width: 2.7", height: 1.9"`), placed above (`y: 1.7"`) for odd nodes and below (`y: 4.7"`) for even nodes, fill `colors[1]`.
* **Typography & Hierarchy:** `15pt` Bold date/phase headers in `colors[2]`; `13.5pt` milestone deliverables inside each node box.
* **LLM Prompt Injection Snippet:**
  > *"Provide 4 chronological milestones or project gates. Format each bullet with a time marker and concrete engineering deliverable."*

---

### 13. Concentric Circle Target / Reach (`concentric_circle_target`)
* **Domain Fit:** Blast/Acoustic Radius Analysis, Market/System Scope, Defense Perimeters
* **Visual Composition:** Three nested concentric circles on the left illustrating core-to-periphery architecture, paired with structured legend cards on the right.
* **Shape & Geometry (`python-pptx`):**
  * **Outer Ring:** `MSO_SHAPE.OVAL` (`1.0", 1.7", 4.8", 4.8"`), fill `colors[1]`, border `2pt` in `colors[3]`.
  * **Middle Ring:** `MSO_SHAPE.OVAL` (`1.75", 2.45", 3.3", 3.3"`), fill `colors[3]`, border `1.5pt` in `colors[2]`.
  * **Core Circle:** `MSO_SHAPE.OVAL` (`2.5", 3.2", 1.8", 1.8"`), fill `colors[2]`, bold label `"CORE"` in `colors[0]`.
  * **Right Legend Stack:** Three `MSO_SHAPE.ROUNDED_RECTANGLE` (`6.4", y: [1.7", 3.4", 5.1"], width: 6.133", height: 1.4"`), fill `colors[1]`.
* **Typography & Hierarchy:** `18pt` Bold zone titles (`Core`, `Mid-Tier`, `Edge`); `14.5pt` technical scope descriptions (`colors[4]`).
* **LLM Prompt Injection Snippet:**
  > *"Categorize the system into 3 concentric zones of influence or containment: Inner Core, Operational Perimeter, and Outer Boundary."*

---

### 14. Frosted Sidebar Navigation (`frosted_sidebar_nav`)
* **Domain Fit:** Multi-Chapter Technical Manuals, Compliance Audits, Standard Operating Procedures
* **Visual Composition:** Full-height vertical navigation rail on the left housing the section title and structural metadata, paired with a spacious right-hand working canvas.
* **Shape & Geometry (`python-pptx`):**
  * **Left Sidebar Rail:** `MSO_SHAPE.RECTANGLE` (`0, 0, 3.8", 7.5"`), fill `colors[1]`, right border `2pt` in `colors[2]`.
  * **Active Section Indicator:** `MSO_SHAPE.RECTANGLE` (`0, 1.4", 0.16", 1.2"`), fill `colors[2]`.
  * **Right Content Container:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`4.3", 0.8", 8.233", 5.9"`), fill `colors[1]`, border `1pt` in `colors[3]`.
* **Typography & Hierarchy:** `24pt` Bold title inside the left rail (`colors[2]`); `17pt` structured operational checklist (`colors[4]`) on the right.
* **LLM Prompt Injection Snippet:**
  > *"Format as a structured technical SOP or compliance audit slide with a clear section title and 4–5 verifiable engineering criteria."*

---

### 15. Radial Sunburst Hub (`radial_sunburst_hub`)
* **Domain Fit:** Microservices Topology, Power Grid Distribution, Central BIM Hub
* **Visual Composition:** Central octagonal or circular hub connected via radiating spoke bars to four corner satellite node cards.
* **Shape & Geometry (`python-pptx`):**
  * **Central Hub:** `MSO_SHAPE.OVAL` (`5.566", 3.15", 2.2", 2.2"`), fill `colors[2]`, border `3pt` in `colors[4]`.
  * **4 Corner Satellite Cards:** `MSO_SHAPE.ROUNDED_RECTANGLE` (`width: 4.1", height: 2.1"`) at top-left (`0.8", 1.4"`), top-right (`8.433", 1.4"`), bottom-left (`0.8", 4.8"`), and bottom-right (`8.433", 4.8"`), fill `colors[1]`, border `1.5pt` in `colors[3]`.
  * **Connector Bars:** Four thin `MSO_SHAPE.RECTANGLE` bridges linking satellite inner corners to the central hub.
* **Typography & Hierarchy:** `18pt` Bold hub title in `colors[0]`; `15pt` node headers (`colors[2]`) and `13.5pt` node specs (`colors[4]`).
* **LLM Prompt Injection Snippet:**
  > *"Define a central system orchestrator/hub and 4 peripheral subsystems or interfaces that exchange data or energy with the core."*

---

## Part II: Top 15 Engineering & Technical Animation Sequences (OpenXML `<p:timing>` Choreography)

`python-pptx` does not expose a high-level `.animations` API out of the box, so `PptxBuilder` injects standard ECMA-376 PresentationML `<p:timing>` XML directly into `slide._element` and `<p:transition>` for slide transitions. Below are the 15 essential Pareto choreography sequences tailored for technical presentations.

### Master OpenXML Helper Reference for `backend/pptx_engine/builder.py`
* **Namespace Map:** `p="http://schemas.openxmlformats.org/presentationml/2006/main"`, `a="http://schemas.openxmlformats.org/drawingml/2006/main"`
* **Trigger Types:** `indefinite` (On Click), `afterEffect` (After Previous), `withEffect` (With Previous)
* **Preset Filter IDs (`presetID`):**
  * `10` = Fade (`fade`)
  * `2` = Fly In (`fly`)
  * `22` = Wipe (`wipe`)
  * `23` = Zoom (`zoom`)
  * `16` = Split (`split`)
  * `1` = Appear (`appear`)
  * `4` = Blinds (`blinds`)
  * `14` = Random Bars / Shutter (`bars`)

---

### 1. Progressive Bullet Reveal (`progressive_bullet_reveal`)
* **Target Archetypes:** `swiss_grid_editorial`, `glassmorphism_card`, `frosted_sidebar_nav`
* **Choreography Behavior:** Header banner and card container appear immediately (`withEffect`, `0ms`), while each bullet paragraph (`<p:txEl><p:pRg st="idx" end="idx"/>`) fades in sequentially on click (`indefinite`, `300ms` duration).
* **OpenXML Implementation Spec:**
  * Slide Transition: `<p:fade spd="med"/>`
  * `<p:par>` click group per paragraph index `i` targeting `spid` of the content container with `presetID="10"` (`presetClass="entr"`), `dur="300"`.
* **Engineering Rationale:** Prevents cognitive overload during dense technical walkthroughs by pacing presenter explanation line-by-line.

---

### 2. Left-to-Right Pipeline Wipe (`left_to_right_pipeline_wipe`)
* **Target Archetypes:** `chevron_process_flow`, `minimalist_timeline_bar`
* **Choreography Behavior:** Sequential horizontal wipe (`fromLeft`, `presetSubtype="8"`) across process chevrons and timeline connectors, automatically chaining stage `N` to stage `N+1` (`afterEffect`, `150ms` delay).
* **OpenXML Implementation Spec:**
  * `<p:cTn presetID="22" presetClass="entr" presetSubtype="8">` (Wipe from Left), `dur="400"`, `nodeType="afterEffect"`, `delay="150"`.
* **Engineering Rationale:** Visually mimics signal propagation, fluid flow, or manufacturing assembly lines moving left-to-right.

---

### 3. CAD Blueprint Grid Assembly (`cad_blueprint_assembly`)
* **Target Archetypes:** `blueprint_cad_grid`, `neo_brutalist_pop`
* **Choreography Behavior:** Outer drafting border splits open from center (`split`, `presetID="16"`), grid hairlines wipe across (`250ms`), and the bottom-right title stamp snaps into place (`appear`, `presetID="1"`).
* **OpenXML Implementation Spec:**
  * Border: `presetID="16"`, `presetSubtype="16"` (Vertical Out), `dur="350"`.
  * Grid lines: `presetID="22"`, `dur="250"`, `nodeType="withEffect"`, `delay="200"`.
  * Stamp & Text: `presetID="10"`, `dur="250"`, `nodeType="afterEffect"`.
* **Engineering Rationale:** Evokes CAD viewport initialization and engineering drawing plot generation.

---

### 4. HUD Telemetry Lock-On (`hud_telemetry_lock_on`)
* **Target Archetypes:** `cyberpunk_hud_frame`
* **Choreography Behavior:** Octagonal HUD frame zooms in rapidly (`zoom`, `presetID="23"`, `250ms`), followed by rapid sequential staccato fade-ins (`120ms` stagger) of the top-right telemetry parallelograms and header hexagon.
* **OpenXML Implementation Spec:**
  * Frame: `presetID="23"`, `presetSubtype="16"` (Object Center), `dur="250"`.
  * Telemetry Bars (1–3): `presetID="1"`, `nodeType="afterEffect"`, `delay="100"`.
  * Body Readout: `presetID="10"`, `dur="200"`, `nodeType="afterEffect"`.
* **Engineering Rationale:** Simulates heads-up display avionics initialization and sensor lock.

---

### 5. KPI Counter Stagger (`kpi_counter_stagger`)
* **Target Archetypes:** `executive_kpi_strip`
* **Choreography Behavior:** The three top KPI cards rise upward (`fly` from bottom, `presetID="2"`, `presetSubtype="4"`) in a `150ms` cascade, followed on click by the bottom synthesis panel fading in.
* **OpenXML Implementation Spec:**
  * KPI Cards 1, 2, 3: `presetID="2"`, `presetSubtype="4"` (From Bottom), `dur="350"`, `delay="0 / 150 / 300"`, `nodeType="withEffect"`.
  * Synthesis Card: `presetID="10"`, `dur="350"`, `nodeType="clickEffect"`.
* **Engineering Rationale:** Draws executive eyes immediately to headline metrics before revealing root-cause analysis.

---

### 6. Dual Matrix Opposing Slide (`dual_matrix_opposing_slide`)
* **Target Archetypes:** `dual_comparison_matrix`
* **Choreography Behavior:** Left panel enters from left (`presetSubtype="8"`), right panel enters from right (`presetSubtype="2"`), and the central `VS` badge pops in at the center (`zoom`, `presetID="23"`).
* **OpenXML Implementation Spec:**
  * Left Card: `presetID="2"`, `presetSubtype="8"`, `dur="400"`, `nodeType="withEffect"`.
  * Right Card: `presetID="2"`, `presetSubtype="2"`, `dur="400"`, `nodeType="withEffect"`.
  * Center Oval (`VS`): `presetID="23"`, `dur="250"`, `nodeType="afterEffect"`.
* **Engineering Rationale:** Physically reinforces architectural tension and trade-off comparison between two competing designs.

---

### 7. Isometric Layer Stack Rise (`isometric_layer_rise`)
* **Target Archetypes:** `isometric_layer_stack`
* **Choreography Behavior:** Bottom diamond plane enters first, followed upward by middle and top planes (`fly` from bottom, `200ms` stagger), then horizontal connector bars wipe right to reveal the specification card.
* **OpenXML Implementation Spec:**
  * Diamonds (Bottom → Top): `presetID="2"`, `presetSubtype="4"`, `dur="350"`, `nodeType="afterEffect"`, `delay="100"`.
  * Connectors: `presetID="22"`, `presetSubtype="8"`, `dur="250"`, `nodeType="afterEffect"`.
* **Engineering Rationale:** Mirrors bottom-up system construction (foundation → structure → envelope, or hardware → kernel → application).

---

### 8. Radial Hub-and-Spoke Expansion (`radial_hub_expansion`)
* **Target Archetypes:** `radial_sunburst_hub`
* **Choreography Behavior:** Central hub zooms out from center (`presetID="23"`), four spoke bridges wipe outward (`presetID="22"`), and corner satellite cards fade in simultaneously (`presetID="10"`).
* **OpenXML Implementation Spec:**
  * Center Oval: `presetID="23"`, `dur="350"`, `nodeType="withEffect"`.
  * Spokes (1–4): `presetID="22"`, `dur="250"`, `nodeType="afterEffect"`.
  * Corner Cards (1–4): `presetID="10"`, `dur="300"`, `nodeType="afterEffect"`.
* **Engineering Rationale:** Demonstrates distributed network topology, power distribution, or microservices fan-out from a central orchestrator.

---

### 9. Concentric Ring Pulse (`concentric_ring_pulse`)
* **Target Archetypes:** `concentric_circle_target`
* **Choreography Behavior:** Inner `CORE` circle zooms in first, followed outward by the middle ring and outer boundary ring (`zoom` from object center, `200ms` stagger), syncing with right-hand legend cards.
* **OpenXML Implementation Spec:**
  * Core → Mid → Outer Ovals: `presetID="23"`, `presetSubtype="16"`, `dur="350"`, `nodeType="afterEffect"`, `delay="150"`.
* **Engineering Rationale:** Ideal for demonstrating blast radius propagation, RF signal attenuation, or defense-in-depth security layers.

---

### 10. Bento Grid Modular Cascade (`bento_grid_cascade`)
* **Target Archetypes:** `bento_grid_dashboard`
* **Choreography Behavior:** Left hero tile fades in first (`0ms`), top-right tile slides down (`150ms`), and bottom-right tile slides up (`300ms`), locking into a unified grid.
* **OpenXML Implementation Spec:**
  * Hero Tile: `presetID="10"`, `dur="350"`, `nodeType="withEffect"`.
  * Top-Right Tile: `presetID="2"`, `presetSubtype="1"` (From Top), `dur="350"`, `delay="150"`, `nodeType="withEffect"`.
  * Bottom-Right Tile: `presetID="2"`, `presetSubtype="4"` (From Bottom), `dur="350"`, `delay="300"`, `nodeType="withEffect"`.
* **Engineering Rationale:** Creates a crisp, modern software dashboard assembly effect.

---

### 11. Neo-Brutalist Shadow Snap (`neo_brutalist_shadow_snap`)
* **Target Archetypes:** `neo_brutalist_pop`
* **Choreography Behavior:** Foreground card appears instantaneously (`appear`, `presetID="1"`), followed `120ms` later by the hard offset black shadow snapping diagonally into place behind it.
* **OpenXML Implementation Spec:**
  * Foreground Card: `presetID="1"`, `nodeType="withEffect"`.
  * Shadow Shape: `presetID="2"`, `presetSubtype="12"` (From Top-Left), `dur="150"`, `delay="120"`, `nodeType="withEffect"`.
* **Engineering Rationale:** Gives flat geometric shapes sudden physical mass and mechanical punch.

---

### 12. Watermark Parallax Drift (`watermark_parallax_drift`)
* **Target Archetypes:** `oversized_watermark`
* **Choreography Behavior:** Giant background numeral (`01`) fades in slowly (`600ms`) while drifting slightly (`fly` from left, `presetSubtype="8"`), while the foreground specification card enters faster (`300ms`) from the right (`presetSubtype="2"`).
* **OpenXML Implementation Spec:**
  * Watermark Textbox: `presetID="2"`, `presetSubtype="8"`, `dur="600"`, `nodeType="withEffect"`.
  * Foreground Card: `presetID="2"`, `presetSubtype="2"`, `dur="350"`, `nodeType="withEffect"`.
* **Engineering Rationale:** Differential velocities create a high-end 2.5D parallax depth illusion natively inside PowerPoint.

---

### 13. Timeline Node-by-Node Step (`timeline_node_step`)
* **Target Archetypes:** `minimalist_timeline_bar`
* **Choreography Behavior:** Horizontal axis spine wipes full width on slide load; each milestone circle + paired callout card advances on individual presenter clicks (`clickEffect`).
* **OpenXML Implementation Spec:**
  * Axis Spine: `presetID="22"`, `presetSubtype="8"`, `dur="450"`, `nodeType="withEffect"`.
  * Per Milestone `k`: Group `nodeType="clickEffect"` containing Node `k` (`presetID="23"`, `dur="200"`) + Card `k` (`presetID="10"`, `dur="250"`, `nodeType="withEffect"`).
* **Engineering Rationale:** Gives project managers granular click-by-click control over schedule reviews and critical path gates.

---

### 14. Swiss Editorial Rule Draw (`swiss_editorial_rule_draw`)
* **Target Archetypes:** `swiss_grid_editorial`
* **Choreography Behavior:** Top horizontal rule wipes right (`300ms`), vertical spine divider wipes downward (`300ms`), and left/right typography fades in cleanly (`400ms`).
* **OpenXML Implementation Spec:**
  * Top Rule: `presetID="22"`, `presetSubtype="8"`, `dur="300"`, `nodeType="withEffect"`.
  * Vertical Spine: `presetID="22"`, `presetSubtype="4"` (From Top), `dur="300"`, `nodeType="afterEffect"`.
  * Text Frames: `presetID="10"`, `dur="400"`, `nodeType="afterEffect"`.
* **Engineering Rationale:** Architectural drafting precision without flashy bounce or overshoot.

---

### 15. Smooth Morph / Cross-Fade Transition (`smooth_morph_crossfade`)
* **Target Archetypes:** Universal / All 15 Styles (Slide-Level Transition)
* **Choreography Behavior:** Applies PowerPoint's native `<mc:AlternateContent>` Morph transition (`p159:morph` with `option="byObject"`) with a `<p:fade/>` fallback for older viewers, smoothly interpolating shared shape positions and colors across consecutive slides.
* **OpenXML Implementation Spec:**
  * Inject inside `<p:sld>` after `<p:cSld>`:
    ```xml
    <mc:AlternateContent xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
      <mc:Choice xmlns:p159="http://schemas.microsoft.com/office/powerpoint/2015/09/main" Requires="p159">
        <p:transition spd="med"><p159:morph option="byObject"/></p:transition>
      </mc:Choice>
      <mc:Fallback>
        <p:transition spd="med"><p:fade/></p:transition>
      </mc:Fallback>
    </mc:AlternateContent>
    ```
* **Engineering Rationale:** Provides seamless cinematic continuity when transitioning between structural diagrams or evolving architectural states.

---

## 3. Recommended Integration Matrix (`knowledge/catalog/industries.json`)

Map each industry theme in your PyQt6 Studio (`frontend/ui/main_window.py`) to a paired `(style_id, animation_id)` tuple so `Orchestrator` passes both to `PptxBuilder`:

| Industry Domain | Theme Preset | Design Archetype (`style_id`) | Default Animation (`animation_id`) |
| :--- | :--- | :--- | :--- |
| **Architecture** | Brutalist Concrete | `neo_brutalist_pop` | `neo_brutalist_shadow_snap` |
| **Architecture** | Biophilic & Timber | `swiss_grid_editorial` | `swiss_editorial_rule_draw` |
| **Architecture** | Minimalist Glass | `glassmorphism_card` | `progressive_bullet_reveal` |
| **Construction** | Structural Steel & Safety | `executive_kpi_strip` | `kpi_counter_stagger` |
| **Construction** | Smart Site Logistics | `chevron_process_flow` | `left_to_right_pipeline_wipe` |
| **Construction** | Geotechnical Foundation | `isometric_layer_stack` | `isometric_layer_rise` |
| **Engineering** | Quantum & Neon | `cyberpunk_hud_frame` | `hud_telemetry_lock_on` |
| **Engineering** | Systems Thermodynamics | `radial_sunburst_hub` | `radial_hub_expansion` |
| **Engineering** | Precision Robotics | `blueprint_cad_grid` | `cad_blueprint_assembly` |
| **Literature** | Classic Parchment | `oversized_watermark` | `watermark_parallax_drift` |
| **Literature** | Modern Typography | `frosted_sidebar_nav` | `progressive_bullet_reveal` |
| **Literature** | Corpus Linguistics | `dual_comparison_matrix` | `dual_matrix_opposing_slide` |