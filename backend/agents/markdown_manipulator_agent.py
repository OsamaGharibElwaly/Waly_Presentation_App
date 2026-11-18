"""Markdown Manipulator Agent - parses input text into structured SlideSpecs."""
from backend.agents.base.agent import BaseAgent, SlideSpec
from backend.agents.factory.agent_factory import AgentFactory

@AgentFactory.register("markdown_manipulator")
class MarkdownManipulatorAgent(BaseAgent):
    def run(self, text: str) -> list[SlideSpec]:
        slides = []
        current_title = "Overview"
        current_bullets = []
        current_notes = ""

        lines = text.splitlines()
        for line in lines:
            line_s = line.strip()
            if line_s.startswith("# "):
                continue  # Main presentation title
            elif line_s.startswith("## "):
                if current_bullets or current_title != "Overview":
                    slides.append(SlideSpec(title=current_title, bullets=current_bullets, notes=current_notes.strip()))
                current_title = line_s[3:].strip()
                current_bullets = []
                current_notes = ""
            elif line_s.startswith("- ") or line_s.startswith("* "):
                current_bullets.append(line_s[2:].strip())
            elif line_s.startswith(">"):
                current_notes += line_s.lstrip("> ").strip() + " "

        if current_bullets or current_title:
            slides.append(SlideSpec(title=current_title, bullets=current_bullets, notes=current_notes.strip()))

        return slides if slides else [SlideSpec(title="Presentation", bullets=[text[:100]], notes="")]