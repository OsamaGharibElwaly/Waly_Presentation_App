"""Local registry for the 15 stable presentation design-system IDs."""
from pathlib import Path
from functools import lru_cache
import json
CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"

@lru_cache(maxsize=None)
def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}

class DesignRegistry:
    def __init__(self, catalog_dir=None):
        self.path = (catalog_dir or CATALOG_DIR) / "design_systems.json"
        self.data = _load(self.path)
    def all(self): return list(self.data.get("design_systems", []))
    def by_id(self, key):
        return next((x for x in self.all() if x.get("id") == key), self.all()[0] if self.all() else {})