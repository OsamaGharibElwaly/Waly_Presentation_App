"""Orchestrator coordinates agents and export builders."""
from pathlib import Path
from backend.agents.factory.agent_factory import AgentFactory
from backend.agents.base.agent import AgentContext
from backend.agents.outline_agent import OutlineAgent
from backend.agents.planner_agent import PlannerAgent
from backend.agents.image_factory_agent import ImageFactoryAgent
from backend.pptx_engine.builder import PptxBuilder
from backend.pdf_engine.builder import PdfBuilder
from backend.pptx_engine.layout_router import route_layouts

class Orchestrator:
    def __init__(self, theme: dict, palette: dict, meta: dict | None = None) -> None:
        self.ctx = AgentContext(theme=theme, palette=palette, meta=meta or {})
        self.md_agent = AgentFactory.create("markdown_manipulator", self.ctx)

    def run(self, markdown_text: str, target: Path, progress=None) -> None:
        report = progress or (lambda value, message: None)
        report(10, "Parsing markdown")
        slides = self.md_agent.run(markdown_text)
        report(30, "Refining outline")
        slides = OutlineAgent(self.ctx).run(slides, self.ctx)
        report(50, "Planning layout")
        slides = PlannerAgent(self.ctx).run(slides)
        for slide, layout in zip(slides, route_layouts([item.layout_type for item in slides])):
            slide.layout_type = layout
        report(70, "Synthesizing visuals")
        slides = ImageFactoryAgent(self.ctx).run(slides)
        report(85, "Rendering")
        suffix = target.suffix.lower()
        if suffix == ".pptx":
            builder = PptxBuilder(self.ctx)
            builder.build(slides, target)
        elif suffix == ".pdf":
            builder = PdfBuilder(self.ctx)
            builder.build(slides, target)
        else:
            raise ValueError(f"Unsupported export format: {suffix}")
        report(100, "Complete")
