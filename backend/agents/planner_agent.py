"""Planner agent assigns senior-artist pacing, focus and visual contracts."""
import re

from backend.agents.base.agent import BaseAgent, VisualSpec
from backend.agents.factory.agent_factory import register
from backend.pptx_engine.layout_router import CYCLE

PLACEMENTS = ("split_right", "split_left", "giant_stat_split", "hero_banner", "full_bleed_glass")
MODES = ("geometric_composition", "split_illustration", "node_flow_diagram", "metric_visual")
PLACEMENT_BY_LAYOUT = {
    "kpi": "giant_stat_split",
    "process": "hero_banner",
    "comparison": "split_left",
    "spotlight": "full_bleed_glass",
    "bento": "split_right",
}
MODE_BY_LAYOUT = {
    "kpi": "metric_visual",
    "process": "node_flow_diagram",
    "comparison": "geometric_composition",
    "spotlight": "split_illustration",
    "bento": "geometric_composition",
}
SCALE_BY_PLACEMENT = {
    "giant_stat_split": "display",
    "full_bleed_glass": "display",
}
PACE = ("open", "build", "evidence", "close")
CUE_RE = re.compile(r"\b(?:Emphasize|Highlight|Point out|Walk through)\b", re.I)


def _next(options: tuple[str, ...], current: str) -> str:
    return options[(options.index(current) + 1) % len(options)] if current in options else options[0]


@register("planner")
class PlannerAgent(BaseAgent):
    def run(self, slides):
        previous_pair = ("", "")
        previous_layout = ""
        for index, slide in enumerate(slides):
            slide.pacing = PACE[min(index, len(PACE) - 1)]
            layout = slide.layout_type if slide.layout_type in CYCLE else CYCLE[index % len(CYCLE)]
            if layout == previous_layout:
                layout = _next(CYCLE, layout)
            slide.layout_type = layout
            if slide.focal_index is None:
                slide.focal_index = 0 if slide.bullets else None
            if not slide.emphasis_cue:
                match = CUE_RE.search(slide.notes)
                if match:
                    slide.emphasis_cue = match.group(0)

            placement = PLACEMENT_BY_LAYOUT[layout]
            mode = "geometric_composition" if slide.image_spec else MODE_BY_LAYOUT[layout]
            if placement == previous_pair[0]:
                placement = _next(PLACEMENTS, placement)
            if (placement, mode) == previous_pair or mode == previous_pair[1]:
                mode = _next(MODES, mode)
            if (placement, mode) == previous_pair:
                placement = _next(PLACEMENTS, placement)

            slide.visual_spec = VisualSpec(
                mode=mode,
                prompt=slide.visual_hint or slide.image_spec or slide.title,
                placement=placement,
                typography_scale=SCALE_BY_PLACEMENT.get(placement, "headline"),
            )
            slide.image_placement = placement
            previous_pair = (placement, mode)
            previous_layout = layout
        return slides
