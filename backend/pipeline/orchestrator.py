"""Orchestrator coordinates agents and export builders."""
from pathlib import Path
from backend.agents.factory.agent_factory import AgentFactory
from backend.agents.base.agent import AgentContext
from backend.pptx_engine.builder import PptxBuilder
from backend.pdf_engine.builder import PdfBuilder

class Orchestrator:
    def __init__(self, theme: dict, palette: dict, meta: dict | None = None) -> None:
        self.ctx = AgentContext(theme=theme, palette=palette, meta=meta or {})
        self.md_agent = AgentFactory.create("markdown_manipulator", self.ctx)

    def run(self, markdown_text: str, target: Path) -> None:
        slides = self.md_agent.run(markdown_text)
        suffix = target.suffix.lower()
        if suffix == ".pptx":
            builder = PptxBuilder(self.ctx)
            builder.build(slides, target)
        elif suffix == ".pdf":
            builder = PdfBuilder(self.ctx)
            builder.build(slides, target)
        else:
            raise ValueError(f"Unsupported export format: {suffix}")
