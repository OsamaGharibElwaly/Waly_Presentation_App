"""Local registry for the 15 presentation build-sequence definitions."""
from pathlib import Path
import json
CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"
class AnimationRegistry:
    def __init__(self, catalog_dir=None):
        self.path = (catalog_dir or CATALOG_DIR) / "animation_sequences.json"
        self.data = json.loads(self.path.read_text(encoding="utf-8-sig")) if self.path.exists() else {"animation_sequences": []}
    def all(self): return list(self.data.get("animation_sequences", []))
    def by_id(self, key):
        return next((x for x in self.all() if x.get("id") == key), {})