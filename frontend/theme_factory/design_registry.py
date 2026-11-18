"""Local registry for the 15 stable presentation design-system IDs."""
from pathlib import Path
import json
CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"
class DesignRegistry:
    def __init__(self, catalog_dir=None):
        self.path = (catalog_dir or CATALOG_DIR) / "design_systems.json"
        self.data = json.loads(self.path.read_text(encoding="utf-8-sig")) if self.path.exists() else {"design_systems": []}
    def all(self): return list(self.data.get("design_systems", []))
    def by_id(self, key):
        return next((x for x in self.all() if x.get("id") == key), self.all()[0] if self.all() else {})