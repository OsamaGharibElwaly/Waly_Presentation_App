"""ThemeRegistry - loads palettes + industries from JSON catalogs using utf-8-sig."""
import json
from functools import lru_cache
from pathlib import Path

CATALOG_DIR = Path(__file__).resolve().parents[2] / "knowledge" / "catalog"

@lru_cache(maxsize=None)
def _load_catalog(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}

class ThemeRegistry:
    def __init__(self, catalog_dir: Path | None = None) -> None:
        self.dir = catalog_dir or CATALOG_DIR
        self._palettes = self._load("palettes.json")
        self._industries = self._load("industries.json")

    def _load(self, name: str) -> dict:
        path = self.dir / name
        return _load_catalog(path)

    def palettes(self) -> list[dict]:
        return self._palettes.get("palettes", [])

    def palette_by_name(self, name: str) -> dict:
        for p in self.palettes():
            if p["name"] == name:
                return p
        return self.palettes()[0] if self.palettes() else {"name": "Default", "colors": []}
