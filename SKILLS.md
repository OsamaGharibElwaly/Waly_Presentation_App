# SKILLS.md — Offline AI Presentation Factory Agent Rules

## 1. PyQt6 UI Ergonomics & Scroller Standard
- **Scroll Area Wrapping:** Every main tab or content panel must be wrapped in a `QScrollArea` with `setWidgetResizable(True)` and styled scrollbars to support small displays and prevent widget clipping.
- **Dark Studio QSS Palette:** Use `#090D16` (background), `#111827` (cards/inputs), `#1F2937` (borders), and `#38BDF8` (primary highlights).
- **Live Swatch Binding:** Color swatches in the inspector must immediately trigger layout updates and propagate hexadecimal changes to the Orchestrator.

## 2. Intelligent Markdown Manipulator & Semantic Layout Routing
- **Anti-Monotony Rule:** Never apply the exact same shape layout or diagram template across consecutive slides. Track `previous_layout_type` in the slide builder and enforce structural rotation through the cycle `bento -> kpi -> process -> comparison -> spotlight`; when a slide's detected intent equals the previous layout, take the next cycle entry.
- **Classifier Contract:** `SlideSpec.layout_type` is one of `bento`, `kpi`, `process`, `comparison`, `spotlight`; `SlideSpec.focal_index` identifies the primary element; `SlideSpec.emphasis_cue` carries the presenter signal.
- **Content-Aware Shape & Diagram Selection:**
  - *Comparisons / Contrasts (`vs.`, tables, before/after):* Render split-screen dual-panel cards or styled native comparison matrices with contrasting accent headers.
  - *Sequential Steps / Roadmaps (`1., 2., 3.`, phases, stages):* Render connected horizontal process chevrons, stepped timeline nodes, or numbered milestone badges.
  - *Metrics / KPIs / Percentages (`$`, `%`, `85%`, `10x`):* Extract numeric callouts into oversized Hero Stat Cards (`36pt–48pt` bold display numbers) paired with subtle supporting captions.
  - *Core Takeaways / Speaker Emphasis (`**bold**`, `!important`, key insights):* Elevate high-priority points into spotlight callout banners, thick left-accented quote blocks, or elevated focal cards with accent borders.
  - *Multi-Pillar Concepts (3–4 distinct items):* Alternate between bento-box asymmetric grids, icon-header vertical columns, and radial/hub-and-spoke diagram primitives.

## 3. Presenter Attention & Visual Hierarchy Rules
- **Focal Point Dominance:** Every slide must have one clear visual anchor (a hero metric, a highlighted focal card, or a central diagram node) styled with the primary accent color (`#38BDF8` or active theme accent) while secondary cards remain muted.
- **Progressive Disclosure & Pacing:** Map focal emphasis to OpenXML `<p:timing>` entrance animations so the main point or hero stat animates in distinctly (`Zoom` ID `23` or `Wipe` ID `22`) while supporting bullets use subtle `Fade` (ID `10`). The focal shape is tagged `focal` and emitted before choreography effects.
- **Speaker Note Signal Parsing:** Parse presenter intent cues in `> Speaker note:` (e.g., *"Emphasize"*, *"Highlight"*, *"Point out"*, *"Walk through"*) to automatically boost visual weight (accent border, elevated card fill, or spotlight badge) on the corresponding slide element.

## 4. python-pptx Geometry & Shape Primitives
- **Canvas Dimensions:** Widescreen 16:9 (`13.333"` width × `7.5"` height | `12,192,000` × `6,858,000` EMUs).
- **Shape Safety:** Always verify shape coordinates and widths to avoid text frame overflows. Combine varied primitives (`ROUNDED_RECTANGLE`, `CHEVRON`, `OVAL` stat badges, thin `RECTANGLE` divider rules, and connector lines) based on slide archetype.
- **OpenXML Animation Injection:** Inject `<p:timing>` and `<p:transition>` nodes directly into `slide._element` using standard preset IDs (`10` = Fade, `2` = Fly In, `22` = Wipe, `23` = Zoom).