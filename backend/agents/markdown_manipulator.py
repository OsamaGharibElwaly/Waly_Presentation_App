"""Markdown Manipulator Agent - parses input text into semantic SlideSpecs."""
import re

from backend.agents.base.agent import BaseAgent, SlideSpec
from backend.agents.factory.agent_factory import AgentFactory

METRIC_RE = re.compile(r"(?:\d+(?:\.\d+)?\s*%|\$\s?\d|\b\d+x\b|\bKPI\b|\brevenue\b|\bcost\b)", re.I)
STEP_RE = re.compile(r"(?:^\s*\d+[.)]\s|\bphase\b|\bstage\b|\broadmap\b|\bmilestone\b|\bstep\b)", re.I)
COMPARE_RE = re.compile(r"\bvs\.?\b|\bversus\b|\bbefore\b|\bafter\b|\|", re.I)
TAKEAWAY_RE = re.compile(r"!important|key (?:takeaway|insight)|\bhighlight\b", re.I)
CUE_RE = re.compile(r"\b(?:Emphasize|Highlight|Point out|Walk through)\b", re.I)
BULLET_RE = re.compile(r"^(?:[-*]\s+|\d+[.)]\s+)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
NUMBERED_RE = re.compile(r"^\s*\d+[.)]\s")


def classify_intent(title: str, bullets: list[str], notes: str, bold: list[int]) -> str:
    text = " ".join([title, *bullets])
    if COMPARE_RE.search(text):
        return "comparison"
    if METRIC_RE.search(text):
        return "kpi"
    if STEP_RE.search(text) or any(NUMBERED_RE.match(item) for item in bullets):
        return "process"
    if bold or TAKEAWAY_RE.search(notes) or CUE_RE.search(notes):
        return "spotlight"
    return "bento"


def resolve_focal(bullets: list[str], notes: str, bold: list[int]) -> tuple[int | None, str]:
    cue_match = CUE_RE.search(notes)
    cue = cue_match.group(0) if cue_match else ""
    if bold:
        return bold[0], cue
    if cue:
        tail = notes[cue_match.end():]
        words = re.findall(r"[a-z0-9]+", tail.lower())
        for index, bullet in enumerate(bullets):
            tokens = re.findall(r"[a-z0-9]+", bullet.lower())
            if tokens and tokens[0] in words:
                return index, cue
    return (0 if bullets else None), cue


@AgentFactory.register("markdown_manipulator")
class MarkdownManipulatorAgent(BaseAgent):
    def run(self, text: str) -> list[SlideSpec]:
        slides: list[SlideSpec] = []
        current_title = "Overview"
        current_bullets: list[str] = []
        current_bold: list[int] = []
        current_notes = ""

        def commit() -> None:
            if not (current_bullets or current_title != "Overview"):
                return
            bold = list(current_bold)
            bullets = list(current_bullets)
            focal, cue = resolve_focal(bullets, current_notes, bold)
            slides.append(SlideSpec(
                title=current_title,
                bullets=bullets,
                notes=current_notes.strip(),
                layout_type=classify_intent(current_title, bullets, current_notes, bold),
                focal_index=focal,
                emphasis_cue=cue,
            ))

        for line in text.splitlines():
            line_s = line.strip()
            if line_s.startswith("# "):
                continue
            if line_s.startswith("## "):
                commit()
                current_title = line_s[3:].strip()
                current_bullets = []
                current_bold = []
                current_notes = ""
            elif line_s.startswith(">"):
                current_notes += line_s.lstrip("> ").strip() + " "
            elif BULLET_RE.match(line_s):
                bullet = BULLET_RE.sub("", line_s, count=1).strip()
                if BOLD_RE.search(bullet):
                    current_bold.append(len(current_bullets))
                current_bullets.append(BOLD_RE.sub(r"\1", bullet).strip(" |"))
            elif line_s.startswith("|") and not re.fullmatch(r"[|\-: ]+", line_s):
                bullet = " ".join(part.strip() for part in line_s.strip("|").split("|") if part.strip())
                if bullet:
                    current_bullets.append(bullet)
        commit()

        if slides:
            return slides
        return [SlideSpec(title="Presentation", bullets=[text[:100]], notes="",
                          layout_type="bento", focal_index=0)]
