# SKILLS.md — Phase 4 Senior Visual Studio & Synthetic Art Engine

## 1. Objective & Architectural Upgrade
Upgrade `OfflineAIPresentationFactory` Phase 4 from small icon-level graphics to **senior-designer, agency-grade visual compositions** across **any Markdown input** (both explicit `::visual` directives and plain headings/bullets/tables/steps).

- **Zero Cloud / Zero Cost:** 100% offline execution using `Pillow` (`PIL`), `NumPy`, `NetworkX`, `python-pptx`, and `reportlab`.
- **Every Slide Gets Visual Craft:** Even plain Markdown without `::visual` tags automatically triggers `PlannerAgent` + `Image_Factory_Agent` so no deck falls back to plain bullet walls.
- **Full-Scale Eye-Candy Layouts (Not Small Icons):** Render high-resolution (`2x` supersampled `LANCZOS`) editorial artwork sized for **50/50 half-slide split panels, full-bleed hero backdrops, and giant-typography spotlight spreads**.

---

## 2. Verified Module Map & Contracts
- `backend/agents/base/agent.py` — Typed `SlideSpec`, `VisualSpec`, `AgentContext`, and fixed `@register` agent factory alias resolution.
- `backend/agents/markdown_manipulator.py` — Parses `#`, `##`, `-`/`*`, `>`, `::visual`, `![alt](spec)`, pipe tables, numbered steps, and inline `**bold**` / `` `code` ``.
- `backend/agents/planner_agent.py` — Assigns senior presentation direction: layout archetype, `visual_placement`, `typography_scale`, `focal_index`, `emphasis_cue`, and `VisualSpec` with anti-repetition pacing.
- `backend/agents/image_factory_agent.py` — Synthesizes high-DPI (`2x` `LANCZOS`) eye-candy PNGs cached by `(content_hash, theme_hash, placement, aspect_ratio)` under `out/.cache/images/`.
- `backend/pipeline/orchestrator.py` — Enforces stage order: `Parse -> Optimize -> Plan -> Synthesize -> Build`.
- `backend/builders/pptx_builder.py` & `pdf_builder.py` — Renders giant display typography paired with half-slide, full-bleed, and split visual placements.
- `frontend/ui/export_worker.py` & `main_window.py` — Non-blocking `QThread` export worker with progress, cancellation, error signals, and in-memory catalog caching.

---

## 3. Senior Presentation Layouts & Placement Contracts (`VisualSpec`)
`PlannerAgent` and `Image_Factory_Agent` must coordinate **layout geometry** and **image aspect ratio** so images fill their designated canvas cleanly without distortion or tiny icon framing:

| Placement ID | Slide Composition (16:9 `13.333" × 7.5"`) | Target Image Aspect (`2x` Render) | Typography & Eye-Candy Treatment |
| :--- | :--- | :--- | :--- |
| `split_right` | **50/50 Split:** Left 50% giant display title (`36–48pt`) + concise bullets; Right 50% edge-to-edge synthetic artwork (`6.67" × 7.5"`) | `1600 × 1800` (`8:9`) | Full-height right canvas with layered glass cards, gradient mesh, and focal art |
| `split_left` | **50/50 Split (Inverted):** Left 50% edge-to-edge artwork (`6.67" × 7.5"`); Right 50% oversized headline + key takeaways | `1600 × 1800` (`8:9`) | Alternates visual weight across consecutive slides for magazine-style pacing |
| `giant_stat_split` | **Giant Typography Hero:** Left 55% monumental callout number/phrase (`64–96pt`) + subtitle; Right 45% high-contrast visual | `1440 × 1800` (`4:5`) | Hero metric or bold thesis statement paired with custom spark/glow geometry |
| `hero_banner` | **Top/Bottom Split:** Top 58% panoramic synthetic banner (`13.333" × 4.35"`); Bottom 42% clean horizontal summary strip | `2560 × 840` (`3:1`) | Ideal for section openers, roadmaps, and `node_flow_diagram` pipelines |
| `full_bleed_glass` | **Full-Bleed Backdrop + Frosted Panel:** Full-slide `16:9` atmospheric art (`13.333" × 7.5"`) behind a translucent high-contrast content card | `2560 × 1440` (`16:9`) | Used for title/closing slides and spotlight theses with vignette & film grain |

### Anti-Icon & Pacing Rules
1. **Minimum Visual Footprint:** Never render standalone decorative graphics smaller than `40%` of slide area unless inside a multi-card bento grid.
2. **Automatic Synthesis for Plain Markdown:** When a slide has no explicit `::visual` tag, `PlannerAgent` infers the best visual mode and placement from slide structure:
   - Title / Opening / Closing slide $\rightarrow$ `full_bleed_glass` + `split_illustration`
   - Numbered steps (`1. 2. 3.`) or architecture keywords $\rightarrow$ `hero_banner` or `split_right` + `node_flow_diagram`
   - Numbers, percentages, or KPIs (`$`, `%`, `x`, benchmarks) $\rightarrow$ `giant_stat_split` + `metric_visual`
   - Pipe tables or comparisons $\rightarrow$ `split_left` + `geometric_composition`
   - Standard bullet slides $\rightarrow$ Alternate `split_right` and `split_left` with `split_illustration` / `geometric_composition`
3. **Zero Consecutive Repeats:** Adjacent slides must never share the same `(placement, visual_mode)` pair.

---

## 4. `Image_Factory_Agent` Senior Artist Rendering Standards (`PIL` + `NumPy` + `NetworkX`)
Every generated PNG must look like an intentional editorial illustration rather than flat primitive shapes:

1. **Multi-Layer Depth Stack (Bottom to Top):**
   - **Layer 1 — Atmospheric Base:** Smooth diagonal/radial `NumPy` color field blending palette `bg` and `surface`, plus subtle organic grain/noise (`σ = 3–6`) to eliminate flat digital banding.
   - **Layer 2 — Architectural Framing:** Subtle perspective grid lines, concentric arcs, or golden-ratio framing guides at low alpha (`12–28`).
   - **Layer 3 — Hero Focal Composition:** Mode-specific centerpiece (`geometric_composition`, `node_flow_diagram`, `metric_visual`, or `split_illustration`) rendered with soft drop shadows, glowing accent halos (`GaussianBlur`), and multi-stop highlights using palette `accent` and `highlight`.
   - **Layer 4 — Glassmorphic Overlay Accents:** Frosted translucent pills/cards (`RGBA` blur + `1px` crisp rim highlight) displaying structured node labels, metric bars, or visual badges derived from slide keywords.
2. **Typography & Contrast Safety:**
   - Ensure text-bearing slides (`full_bleed_glass`, `split_right`, `split_left`, `giant_stat_split`) maintain high contrast against the active palette's `text` slot.
   - Supersample at `2x` target dimensions and downsample via `Image.Resampling.LANCZOS`.
3. **Cache Key Integrity:**
   - Include `renderer_version` (e.g., `v4_senior_artist`) in the `out/.cache/images/` hash key so upgrading the visual renderer automatically invalidates old small-icon PNGs without manual cache clearing.

---

## 5. Builder Integration (`PptxBuilder` & `PdfBuilder`)
- **Edge-to-Edge Placement:** Place `split_right` (`x=6.667", y=0", w=6.667", h=7.5"`) and `split_left` (`x=0", y=0", w=6.667", h=7.5"`) flush to slide edges, with generous inner padding (`0.65"`) on the typography half.
- **Giant Typography Hierarchy:**
  - `giant_stat_split`: Render extracted hero number/headline at `64–88pt` bold with a tight `16–20pt` supporting caption underneath.
  - `split_right` / `split_left`: Render slide title at `34–44pt` bold, max 3–4 crisp bullets (`16–20pt`) with highlighted lead-in phrases (`**bold**`).
- **Deterministic Fallback:** If an image file fails to load or generate, fall back gracefully to styled vector shapes without aborting export.

---

## 6. Verification Checklist
- [ ] Plain Markdown (without any `::visual` directives) produces full-bleed / 50-50 split eye-candy slides on every slide.
- [ ] `out/.cache/images/` generates high-DPI (`1600×1800`, `2560×1440`, `2560×840`) PNGs and invalidates legacy icon caches via `renderer_version`.
- [ ] `PptxBuilder` and `PdfBuilder` align half-slide images flush to edges with giant, legible, non-overlapping typography.
- [ ] All `@register` agents resolve via the agent factory regression test, and `pytest` passes cleanly.
- [ ] `.venv\Scripts\python.exe frontend\main.py` exports asynchronously via `ExportWorker` with responsive progress and cancellation.