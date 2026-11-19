# Phase 5 - Zero-Overlap Layout, Append-Only Visual Pool & Right Inspector

## Added
- `TextBlock` contract + `SlideSpec.blocks`; manipulator tags `table`, `steps`, `bullets` and `notes` blocks.
- `backend/layout/geometry.py`: `rects_intersect`, `layout_zones`, `fit_size` shared by builders and inspector.
- Pptx/PDF builders allocate disjoint image/content/footer zones, clamp font size, and render table/step blocks in dedicated containers.
- `images-factory/` append-only pool with `manifest.json`; `python -m backend.agents.image_factory_agent --count N` grows the pool, runtime agent only selects existing assets and falls back to vector shapes when empty.
- `RightInspectorPanel` right dock: zone wireframe with overlap warning, QPropertyAnimation/QTimer motion controls, pop-out dialog, and three-step guided settings wired to `ExportWorker`.

## Verification
- `pytest`: 52 passed.
- Append-only pool: repeated runs preserve prior asset ids and paths; runtime synthesis count is zero.
- Overlap: content/footer/text/block zones are disjoint on all five placements.
- Offscreen `python -m frontend.main`: clean launch with right inspector dock.
