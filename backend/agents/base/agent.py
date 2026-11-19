"""Base agent definitions and data structures."""
from dataclasses import dataclass, field

@dataclass
class AgentContext:
    theme: dict = field(default_factory=dict)
    palette: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

@dataclass
class TextBlock:
    kind: str
    text: str


@dataclass
class VisualSpec:
    mode: str = "geometric_composition"
    prompt: str = ""
    placement: str = "split_right"
    typography_scale: str = "headline"


@dataclass
class SlideSpec:
    title: str
    bullets: list[str]
    notes: str = ""
    layout_type: str = ""
    focal_index: int | None = None
    emphasis_cue: str = ""
    visual_hint: str = ""
    image_spec: str = ""
    visual_spec: VisualSpec | None = None
    pacing: str = ""
    image_path: str = ""
    image_placement: str = ""
    blocks: list[TextBlock] = field(default_factory=list)

class BaseAgent:
    def __init__(self, ctx: AgentContext | None = None) -> None:
        self.ctx = ctx or AgentContext()

    def run(self, content: str):
        raise NotImplementedError
