"""Static fallback for industries with utf-8-sig BOM support."""
from pathlib import Path
import json

_HERE = Path(__file__).resolve().parents[2]
_PATH = _HERE / "knowledge" / "catalog" / "industries.json"

INDUSTRIES = json.loads(_PATH.read_text(encoding="utf-8-sig")) if _PATH.exists() else {}
