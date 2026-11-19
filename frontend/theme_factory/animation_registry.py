"""Local registry for the 15 presentation build-sequence definitions."""
from pathlib import Path
from functools import lru_cache
import json
CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"

@lru_cache(maxsize=None)
def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}

class AnimationRegistry:
    def __init__(self, catalog_dir=None):
        self.path = (catalog_dir or CATALOG_DIR) / "animation_sequences.json"
        self.data = _load(self.path)
    def all(self): return list(self.data.get("animation_sequences", []))
    def by_id(self, key):
        return next((x for x in self.all() if x.get("id") == key), {})