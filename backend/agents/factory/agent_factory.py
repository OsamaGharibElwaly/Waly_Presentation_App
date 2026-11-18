"""AgentFactory with auto-registration and crash-proof fallback."""
from typing import Dict, Type
from backend.agents.base.agent import BaseAgent, AgentContext

_REGISTRY: Dict[str, Type[BaseAgent]] = {}

class AgentFactory:
    @classmethod
    def register(cls, name: str):
        def decorator(subclass: Type[BaseAgent]):
            _REGISTRY[name] = subclass
            return subclass
        return decorator

    @classmethod
    def create(cls, name: str, ctx: AgentContext | None = None) -> BaseAgent:
        if name not in _REGISTRY:
            cls._auto_register()
        
        if name not in _REGISTRY:
            class SafeFallbackAgent(BaseAgent):
                def run(self, text: str):
                    from backend.agents.base.agent import SlideSpec
                    return [SlideSpec(title="Presentation Slide", bullets=[text[:120]], notes="Fallback generated.")]
            return SafeFallbackAgent(ctx)
            
        return _REGISTRY[name](ctx)

    @classmethod
    def _auto_register(cls) -> None:
        try:
            from backend.agents.markdown_manipulator import MarkdownManipulatorAgent
            _REGISTRY["markdown_manipulator"] = MarkdownManipulatorAgent
        except Exception:
            pass
