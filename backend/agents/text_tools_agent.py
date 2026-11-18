"""Text Tools Agent utilizing offline NLP libraries (scikit-learn TF-IDF)."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.agents.base.agent import BaseAgent, AgentContext
from backend.agents.factory.agent_factory import register


@register("text_tools")
class TextToolsAgent(BaseAgent):
    name = "text_tools"

    def run(self, payload: list[str], ctx: AgentContext) -> list[str]:
        if len(payload) < 2:
            return payload
        vec = TfidfVectorizer().fit_transform(payload)
        sim = cosine_similarity(vec)
        keep, dropped = [], set()
        for i in range(len(payload)):
            if i in dropped:
                continue
            keep.append(payload[i])
            for j in range(i + 1, len(payload)):
                if sim[i, j] > 0.90:
                    dropped.add(j)
        return keep
