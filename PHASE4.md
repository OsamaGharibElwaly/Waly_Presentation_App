# Phase 4 - Markdown Extensions, Planner, Offline Visuals & Non-Blocking Export

## Added
- `MarkdownManipulatorAgent`: `::visual <hint>`, `![alt](spec)`, pipe tables, numbered steps, `**bold**` and `` `code` `` without changing `#`/`##`/`-`/`*` or `>` handling.
- `VisualSpec` and `SlideSpec` fields: `visual_hint`, `image_spec`, `visual_spec`, `pacing`, `image_path`, `image_placement`.
- `PlannerAgent` between outline refinement and `route_layouts()`: pacing, layout intent, focal emphasis and typed visual contracts with no consecutive layout/visual/placement repeats.
- `ImageFactoryAgent`: offline Pillow synthesis (`geometric_composition`, `node_flow_diagram`, `metric_visual`, `split_illustration`) with active 5-color palette, deterministic NumPy/NetworkX geometry, 2x LANCZOS downsampling, and disk cache at `out/.cache/images/` keyed by content + palette.
- PPTX/PDF builders embed generated images in 16:9 geometry.
- Cached catalog loads in `ThemeRegistry`, `DesignRegistry` and `AnimationRegistry`.
- `ExportWorker(QThread)` with progress, cancellation and error signals; UI adds progress bar, cancel button and no longer blocks on export.

## Verification
- `pytest`: 47 passed.
- CLI deck: `out/Enterprise_AI_Transformation_Semantic.pptx` - 11 slides, 10 embedded images, 10 native timing nodes, progress `10/30/50/70/85/100`.
- `python -m frontend.main` (offscreen smoke): clean launch.

## v4 Senior Artist Upgrade
- `VisualSpec` placements: `split_right`, `split_left`, `giant_stat_split`, `hero_banner`, `full_bleed_glass`; output sizes `1600x1800`, `1440x1800`, `2560x840`, `2560x1440` rendered at 2x and downsampled with LANCZOS.
- `renderer_version = "v4_senior_artist"` in the cache key; multi-layer NumPy atmosphere/grain, Gaussian glow, NetworkX flow graphs and glass accents replace small icons.
- Planner infers placements/modes from layout intent with zero consecutive `(placement, visual_mode)` repeats; plain Markdown without `::visual` gets full visual coverage.
- PPTX/PDF builders place artwork flush to slide edges with display typography (up to 76-88pt) and vector-shape fallbacks.

## v4 Verification
- `pytest`: 49 passed.
- CLI deck: 11 slides, 10 embedded images, progress `10/30/50/70/85/100`, cache sizes `1600x1800`, `1440x1800`, `2560x840`, `2560x1440`.
- Offscreen `python -m frontend.main`: clean launch.
