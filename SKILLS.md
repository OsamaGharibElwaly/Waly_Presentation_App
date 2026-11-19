# SKILLS.md — Phase 5 Zero-Overlap Typography, `/images-factory` Pool & Right Inspector Studio

## 1. Phase 5 Objectives
Upgrade `OfflineAIPresentationFactory` for **Phase 5** with three concrete improvements:
1. **Zero Text Collisions (`Conflict-Free Layout & Typography Guard`):** Eliminate overlapping titles, headings, bullets, tables, notes, and image zones across both `PptxBuilder` and `PdfBuilder`.
2. **Pre-Built Append-Only `/images-factory` Pool (No Runtime Image Generation Overhead):** Decouple image creation from deck export runtime. Generate/curate images via a dedicated `/images-factory` workflow that **appends** new assets to the pool on each run, while export/build time only selects and embeds matching pre-built assets (with safe local fallback if the pool is empty).
3. **Right Inspector Panel & Guided Settings in Frontend (`frontend/`):** Add a right-hand dock/panel in `MainWindow` featuring a **live layout/text-box & animation sequence preview** (plus an optional pop-out preview window) and a **guided settings walkthrough** before running export.

---

## 2. Zero Text-Overlap & Typography Invariants
Text conflicts happen when fixed coordinates meet variable text length, tables, numbered steps, or split-panel images. Enforce these deterministic rules before placing any text element:

- **Non-Overlapping Zone Allocation (`16:9` `13.333" × 7.5"`):**
  - Partition every slide into **disjoint bounding boxes** (`[x, y, w, h]`)—never let a text box overlap an image zone or footer/header band.
  - Reserve explicit margins (`≥ 0.55"` outer margin, `≥ 0.30"` gutter between columns/panels, `≥ 0.25"` vertical gap between title block, body block, and footer).
- **Dynamic Font Scaling & Line Budgeting:**
  - Compute max character/line capacity per bounding box from box width, font size, and line height.
  - Step down font size deterministically (within a safe floor, e.g., `13pt` body / `28pt` title) or clamp/paginate overflowing bullets/rows *before* rendering so text never clips or collides with adjacent elements.
- **Structured Block Isolation (Tables, Steps, Callouts):**
  - Render pipe tables (`| ... |`) and numbered steps (`1. ...`) inside dedicated non-overlapping containers with explicit cell/row padding and capped column/row counts per slide.
  - Keep speaker notes (`>`) strictly in notes/metadata—never overlaid onto slide canvas text.
- **Automated Overlap Assertion:**
  - Include a geometry overlap helper (`rects_intersect(a, b)`) in tests and builder validation so intersecting text/image boxes fail tests deterministically.

---

## 3. Append-Only `/images-factory` Workflow (Zero Runtime Generation Overhead)
Move synthetic image creation out of the export hot path into a dedicated `/images-factory` command/workflow:

- **Directory & Manifest Layout:**
  - Maintain a persistent `/images-factory` asset pool (e.g., `images-factory/` or `/images-factory` at project root, plus an `images-factory/manifest.json` index) containing pre-rendered high-DPI images tagged by `id`, `mode`, `aspect_ratio`, `palette_tag`/`mood`, `dimensions`, and `created_at`.
- **Append-Only Generation Behavior:**
  - Each run of `/images-factory` **appends** newly generated images to the pool and updates `manifest.json` without deleting or overwriting existing pool assets (unless explicitly requested).
  - Support a count/batch parameter (e.g., generate `N` new images per run) so each `/images-factory` run grows the library incrementally.
- **Runtime Export Behavior (`Orchestrator` + `Image_Factory_Agent` + Builders):**
  - During normal deck generation and PPTX/PDF export, **do not synthesize heavy new images on the fly**.
  - `Image_Factory_Agent` queries the pre-built `/images-factory` pool (matching placement orientation/aspect ratio and avoiding duplicate picks within the same deck) and embeds those ready files.
  - If `/images-factory` has no matching or available images yet, fall back cleanly to a lightweight, deterministic placeholder/shape without blocking or timing out export.

---

## 4. Frontend Right Panel: Animation/Layout Preview & Guided Settings
Enhance `frontend/main_window.py` and `frontend/ui/` while preserving strict boundary isolation (`frontend/` talks to backend contracts/workers, never embedding heavy builder logic in UI event handlers):

- **Right Inspector Panel (`RightInspectorPanel`):**
  - Docked on the right side of `MainWindow` with two clear tabs:
    1. **`Preview & Animation` Tab:**
       - **Slide & Zone Wireframe Preview:** Shows the active slide's layout zones, text/table/step blocks, and selected `/images-factory` visual slot with visual overlap warnings if text is dense.
       - **Animation & Transition Preview:** Lets the user pick a slide/transition/animation preset, preview a smooth UI motion/stagger simulation (`QTimer` / `QPropertyAnimation`) with Play/Replay/Step controls, and see the exact PowerPoint transition & animation settings that will be exported.
       - **Pop-Out Preview Button:** Opens a larger resizable preview dialog (`QDialog`) for inspecting slides and motion before exporting.
    2. **`Guided Settings` Tab:**
       - Step-by-step guided workflow for first-time or fast users:
         - **Step 1 — Deck & Text Safety:** Markdown source, layout/pacing mode, and text-fit/anti-overlap status.
         - **Step 2 — Visual Pool & Motion:** Selected `/images-factory` assets, palette/theme, and slide transition/animation preset (plus a hint/action if `/images-factory` needs more appended images).
         - **Step 3 — Export Target:** Output format (`.pptx`, `.pdf`), target path, and one-click export via `ExportWorker` (`QThread`).
- **In-Memory Caching & Non-Blocking Execution:**
  - Keep theme/palette/layout catalogs and `/images-factory` manifest reads cached in memory with refresh triggers, and keep all export operations on `ExportWorker` (`QThread`) with progress, cancel, and error handling.

---

## 5. Verification Checklist
- [ ] **No Text Collisions:** Unit/integration tests verify zero bounding-box overlaps across titles, bullets, tables, steps, and image frames on `16:9` PPTX and PDF outputs.
- [ ] **Append-Only `/images-factory`:** Running `/images-factory` multiple times appends new assets and updates the manifest without erasing prior pool images, and normal export does not run heavy image generation at runtime.
- [ ] **Right Inspector & Guided UI:** Launching `.venv\Scripts\python.exe frontend\main.py` shows the right-hand preview/animation & guided settings panel, pop-out preview window, and non-blocking `ExportWorker` export flow.
- [ ] **Test Suite:** `pytest` passes cleanly with zero regressions on `@register` agent resolution and pipeline stages.