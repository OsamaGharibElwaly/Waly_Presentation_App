"""Base agent definitions and data structures."""
from dataclasses import dataclass, field

@dataclass
class AgentContext:
    theme: dict = field(default_factory=dict)
    palette: dict = field(default_factory=dict)
    meta: dict = field(default_factory=dict)

@dataclass
class SlideSpec:
    title: str
    bullets: list[str]
    notes: str = ""

class BaseAgent:
    def __init__(self, ctx: AgentContext | None = None) -> None:
        self.ctx = ctx or AgentContext()

    def run(self, content: str):
        raise NotImplementedError
