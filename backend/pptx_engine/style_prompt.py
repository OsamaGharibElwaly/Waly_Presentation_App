"""Build deterministic style instructions for local LLM prompt workflows."""
from frontend.theme_factory.design_registry import DesignRegistry
from frontend.theme_factory.animation_registry import AnimationRegistry
def compose_style_prompt(design_id, animation_id, palette, intensity="balanced", animation_mode="off"):
    d = DesignRegistry().by_id(design_id)
    a = AnimationRegistry().by_id(animation_id or "")
    lines = ["You are a senior presentation designer and technical communication specialist.",
      "DESIGN SYSTEM: " + d.get("name", "Minimalist Scandinavian"),
      "VISUAL DIRECTION: " + d.get("prompt", ""), "GEOMETRY: " + d.get("geometry", ""),
      "TYPOGRAPHY: " + d.get("typography", ""), "DIAGRAMS: " + d.get("diagram_treatment", ""),
      "PALETTE: " + palette.get("name", "Default") + " | " + ", ".join(palette.get("colors", [])),
      "Preserve every supplied fact, figure, equation, unit, date and reference.",
      "Never invent dimensions, standards, citations, test results, telemetry or performance claims.",
      "Prefer accurate diagrams, charts and tables where they improve communication."]
    if a and animation_mode != "off":
        lines += ["ANIMATION SEQUENCE: " + a.get("name", ""), "STEPS: " + " -> ".join(a.get("steps", [])),
                  "INTENSITY: " + intensity, "Do not let animation alter the selected design system or palette."]
    else: lines.append("ANIMATION: None; use static slides.")
    return "\n".join(lines)