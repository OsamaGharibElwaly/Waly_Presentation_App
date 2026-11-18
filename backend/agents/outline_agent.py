"""Outline Refinement Agent ensuring presentation flow and length constraints."""
from backend.agents.base.agent import BaseAgent, AgentContext
from backend.agents.factory.agent_factory import register


@register("outline")
class OutlineAgent(BaseAgent):
    name = "outline"

    def run(self, slides, ctx: AgentContext):
        for s in slides:
            if not s.title:
                s.title = "Overview"
            s.title = s.title[:75]
            s.bullets = [b[:160] for b in s.bullets[:6]]
        return slides
