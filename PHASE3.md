# Phase 3 - Semantic Layout Routing & Presenter Emphasis

## Added
- `SlideSpec` intent fields: `layout_type`, `focal_index`, `emphasis_cue`.
- Markdown classifier: metrics/KPIs, numbered steps/roadmaps, comparisons, bolded takeaways, speaker-note cues.
- `route_layouts()` from `backend/pptx_engine/layout_router.py`: deterministic cycle `bento -> kpi -> process -> comparison -> spotlight`, zero consecutive repeats.
- Five semantic renderers with high-contrast focal cards and native `<p:timing>` Zoom (ID 23) on the primary emphasis.
- `SKILLS.md` Sections 2 and 3 updated with the routing and emphasis standards.
- Fixture + tests: `tests/fixtures/enterprise_ai_transformation.md`, `tests/test_studio.py`.

## Verification
- `pytest`: 39 passed.
- Deck: `out/Enterprise_AI_Transformation_Semantic.pptx` - 11 slides, 0 consecutive repeats, 10/10 focal Zoom presets, 0 text overflows.
- `python -m frontend.main`: clean launch.
