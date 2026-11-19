"""Offline senior-artist visual synthesizer with deterministic cached output."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from backend.agents.base.agent import AgentContext, BaseAgent
from backend.agents.factory.agent_factory import register

POOL_DIR = Path("images-factory")
MANIFEST_PATH = POOL_DIR / "manifest.json"
RENDERER_VERSION = "v4_senior_artist"
_manifest_cache: list[dict] | None = None
SCALE = 2
SIZES = {
    "split_right": (1600, 1800),
    "split_left": (1600, 1800),
    "giant_stat_split": (1440, 1800),
    "hero_banner": (2560, 840),
    "full_bleed_glass": (2560, 1440),
}
CACHE_DIR = Path("out/.cache/images")
DEFAULTS = ("#0F172A", "#1E293B", "#38BDF8", "#2563EB", "#F8FAFC")


def palette_colors(ctx) -> list[str]:
    colors = list(ctx.palette.get("colors") or [])
    return [colors[index] if index < len(colors) else DEFAULTS[index] for index in range(5)]


def channels(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    if len(text) == 3:
        text = "".join(char * 2 for char in text)
    return tuple(int(text[index:index + 2], 16) for index in (0, 2, 4))


def numbers(text: str) -> list[float]:
    values: list[float] = []
    for match in re.finditer(r"\$?\s?\d+(?:\.\d+)?\s?[%x]?", text):
        token = re.sub(r"[^0-9.]", "", match.group(0))
        if token:
            values.append(float(token))
    return values[:6] or [1.0, 2.0, 3.0]


def load_manifest(refresh: bool = False) -> list[dict]:
    global _manifest_cache
    if _manifest_cache is None or refresh:
        try:
            data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            data = []
        _manifest_cache = data if isinstance(data, list) else []
    return list(_manifest_cache)


@register("image_factory")
class ImageFactoryAgent(BaseAgent):
    def run(self, slides):
        manifest = load_manifest()
        used: set[str] = set()
        for slide in slides:
            spec = slide.visual_spec
            if spec is None:
                continue
            candidates = [entry for entry in manifest
                          if entry.get("placement") == spec.placement and entry.get("path") not in used]
            if not candidates:
                candidates = [entry for entry in manifest if entry.get("path") not in used]
            if candidates:
                index = int(hashlib.sha256(spec.prompt.encode("utf-8")).hexdigest()[:8], 16) % len(candidates)
                entry = candidates[index]
                path = Path(entry["path"])
                slide.image_path = str(path) if path.exists() else ""
                used.add(entry["path"])
            else:
                slide.image_path = ""
            slide.image_placement = spec.placement
        return slides

    def _synthesize(self, mode: str, placement: str, prompt: str, palette: list[str]) -> Image.Image:
        width, height = SIZES.get(placement, SIZES["split_right"])
        canvas_w, canvas_h = width * SCALE, height * SCALE
        seed = int(hashlib.sha256((mode + prompt).encode("utf-8")).hexdigest()[:8], 16)
        image = self._atmosphere(canvas_w, canvas_h, palette, seed).convert("RGBA")
        draw = ImageDraw.Draw(image, "RGBA")
        self._glow(image, palette, seed, canvas_w, canvas_h)
        draw = ImageDraw.Draw(image, "RGBA")
        self._framing(draw, palette, canvas_w, canvas_h)
        try:
            if mode == "metric_visual":
                self._metric(draw, prompt, palette, canvas_w, canvas_h)
            elif mode == "node_flow_diagram":
                self._flow(draw, prompt, palette, canvas_w, canvas_h, seed)
            elif mode == "split_illustration":
                self._split(draw, palette, canvas_w, canvas_h)
            else:
                self._geometric(draw, prompt, palette, canvas_w, canvas_h, seed)
        except Exception:
            draw.rectangle((0, 0, canvas_w, canvas_h), fill=(*channels(palette[0]), 255))
            draw.rectangle(self._box(0.06, 0.1, 0.88, 0.8, canvas_w, canvas_h),
                           outline=(*channels(palette[2]), 180), width=4 * SCALE)
        self._glass(draw, palette, prompt, canvas_w, canvas_h)
        return image.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)

    @staticmethod
    def _box(x: float, y: float, w: float, h: float, canvas_w: int, canvas_h: int):
        return (int(x * canvas_w), int(y * canvas_h),
                int((x + w) * canvas_w), int((y + h) * canvas_h))

    def _atmosphere(self, width: int, height: int, palette: list[str], seed: int) -> Image.Image:
        small_w, small_h = max(8, width // 8), max(8, height // 8)
        yy, xx = np.mgrid[0:small_h, 0:small_w]
        tx = xx / small_w
        ty = yy / small_h
        gradient = 0.65 * tx + 0.35 * ty
        base = np.array(channels(palette[0]), dtype=np.float32)
        surface = np.array(channels(palette[1]), dtype=np.float32)
        accent = np.array(channels(palette[3]), dtype=np.float32)
        field = base[None, None, :] * (1 - gradient[..., None]) + surface[None, None, :] * gradient[..., None]
        radius = np.sqrt(((tx - 0.72) * 1.3) ** 2 + ((ty - 0.3) * 1.6) ** 2)
        halo = np.exp(-radius * radius * 5)[..., None] * 0.5
        field = field * (1 - halo) + accent[None, None, :] * halo
        grain = np.random.default_rng(seed).normal(0, 4.0, size=(small_h, small_w, 1))
        field = np.clip(field + grain, 0, 255).astype(np.uint8)
        return Image.fromarray(field, "RGB").resize((width, height), Image.Resampling.BICUBIC)

    def _glow(self, image: Image.Image, palette: list[str], seed: int,
              width: int, height: int) -> None:
        layer = Image.new("RGBA", (max(8, width // 4), max(8, height // 4)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer, "RGBA")
        rng = np.random.default_rng(seed ^ 0x9E3779B9)
        color = channels(palette[2])
        for _ in range(4):
            cx = int(rng.uniform(0.15, 0.9) * layer.width)
            cy = int(rng.uniform(0.15, 0.85) * layer.height)
            radius = int(rng.uniform(0.05, 0.14) * min(layer.size))
            draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(*color, 130))
        blurred = layer.filter(ImageFilter.GaussianBlur(radius=12))
        image.alpha_composite(blurred.resize((width, height), Image.Resampling.BICUBIC))

    def _framing(self, draw, palette: list[str], width: int, height: int) -> None:
        accent = channels(palette[2])
        for index in range(1, 9):
            x = int(width * index / 9)
            draw.line((x, 0, x - int(width * 0.12), height), fill=(*accent, 20), width=2)
        for index in range(1, 7):
            y = int(height * index / 7)
            draw.line((0, y, width, y + int(height * 0.03)), fill=(*accent, 16), width=2)
        for index in range(4):
            size = min(width, height) * (0.22 + index * 0.14)
            box = (width * 0.68 - size / 2, height * 0.38 - size / 2,
                   width * 0.68 + size / 2, height * 0.38 + size / 2)
            draw.arc(tuple(int(value) for value in box), 0, 360, fill=(*accent, 34), width=3)

    def _glass(self, draw, palette: list[str], prompt: str, width: int, height: int) -> None:
        highlight = channels(palette[4])
        accent = channels(palette[2])
        for index, fraction in enumerate((0.16, 0.34)):
            box = self._box(0.07, fraction, 0.3, 0.1, width, height)
            draw.rounded_rectangle(box, radius=14 * SCALE, fill=(*highlight, 32),
                                   outline=(*highlight, 110), width=2 * SCALE)
            draw.rounded_rectangle((box[0] + 10 * SCALE, box[1] + 8 * SCALE,
                                    box[0] + 70 * SCALE, box[1] + 11 * SCALE),
                                   radius=3 * SCALE, fill=(*accent, 170))
        badge = self._box(0.78, 0.82, 0.16, 0.08, width, height)
        draw.rounded_rectangle(badge, radius=20 * SCALE, fill=(*accent, 60),
                               outline=(*highlight, 150), width=2 * SCALE)

    def _geometric(self, draw, prompt: str, palette: list[str],
                   width: int, height: int, seed: int) -> None:
        rng = np.random.default_rng(seed)
        for index in range(14):
            x = float(rng.uniform(0.1, 0.78))
            y = float(rng.uniform(0.08, 0.78))
            size = float(rng.uniform(0.08, 0.18))
            color = channels(palette[1 + index % 3])
            shadow = self._box(x + 0.012, y + 0.018, size, size * 0.5, width, height)
            draw.rounded_rectangle(shadow, radius=12 * SCALE, fill=(0, 0, 0, 90))
            box = self._box(x, y, size, size * 0.5, width, height)
            draw.rounded_rectangle(box, radius=12 * SCALE, fill=(*color, 230),
                                   outline=(*channels(palette[4]), 90), width=2 * SCALE)
            draw.line((box[0] + 6, box[1] + 6, box[2] - 6, box[1] + 6),
                      fill=(*channels(palette[4]), 150), width=2 * SCALE)

    def _flow(self, draw, prompt: str, palette: list[str],
              width: int, height: int, seed: int) -> None:
        graph = nx.path_graph(6)
        positions = {node: (0.1 + node * 0.16, 0.32 + (node % 2) * 0.28) for node in graph.nodes}
        for start, end in graph.edges:
            first = tuple(int(value) for value in (positions[start][0] * width, positions[start][1] * height))
            second = tuple(int(value) for value in (positions[end][0] * width, positions[end][1] * height))
            draw.line((first, second), fill=(*channels(palette[3]), 70), width=16 * SCALE)
            draw.line((first, second), fill=(*channels(palette[2]), 220), width=5 * SCALE)
        for node, (fx, fy) in positions.items():
            radius = 0.075 if node in (0, 5) else 0.05
            box = self._box(fx - radius, fy - radius, radius * 2, radius * 2, width, height)
            color = channels(palette[2] if node in (0, 5) else palette[1])
            draw.ellipse(box, fill=(*color, 245), outline=(*channels(palette[4]), 200), width=3 * SCALE)

    def _metric(self, draw, prompt: str, palette: list[str], width: int, height: int) -> None:
        values = numbers(prompt)
        peak = max(values) or 1.0
        for index, value in enumerate(values[:5]):
            x = 0.1 + index * 0.17
            bar_height = 0.55 * value / peak
            box = self._box(x, 0.8 - bar_height, 0.12, bar_height, width, height)
            color = channels(palette[2 + index % 3])
            draw.rounded_rectangle(box, radius=10 * SCALE, fill=(*color, 235),
                                   outline=(*channels(palette[4]), 100), width=2 * SCALE)
            draw.line((box[0] + 8, box[1] + 8, box[2] - 8, box[1] + 8),
                      fill=(*channels(palette[4]), 170), width=3 * SCALE)
        draw.line(self._box(0.06, 0.81, 0.88, 0.006, width, height),
                  fill=(*channels(palette[4]), 170), width=2 * SCALE)

    def _split(self, draw, palette: list[str], width: int, height: int) -> None:
        draw.polygon([(0, 0), (int(width * 0.62), 0), (int(width * 0.38), height), (0, height)],
                     fill=(*channels(palette[1]), 230))
        draw.polygon([(int(width * 0.62), 0), (width, 0), (width, height), (int(width * 0.38), height)],
                     fill=(*channels(palette[3]), 210))
        draw.line((int(width * 0.62), 0, int(width * 0.38), height),
                  fill=(*channels(palette[4]), 190), width=4 * SCALE)
        for index in range(3):
            y = 0.24 + index * 0.2
            box = self._box(0.14, y, 0.28, 0.09, width, height)
            draw.rounded_rectangle(box, radius=12 * SCALE, fill=(*channels(palette[4]), 55),
                                   outline=(*channels(palette[4]), 170), width=2 * SCALE)


def build_pool(count: int = 4, palette: dict | None = None) -> list[dict]:
    global _manifest_cache
    POOL_DIR.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(refresh=True)
    ctx = AgentContext(palette=palette or {"colors": list(DEFAULTS)})
    agent = ImageFactoryAgent(ctx)
    colors = palette_colors(ctx)
    placements = tuple(SIZES)
    modes = ("geometric_composition", "node_flow_diagram", "metric_visual", "split_illustration")
    created: list[dict] = []
    for index in range(max(0, count)):
        identifier = f"asset_{len(manifest) + len(created) + 1:04d}"
        mode = modes[index % len(modes)]
        placement = placements[index % len(placements)]
        path = POOL_DIR / f"{identifier}_{mode}.png"
        if path.exists():
            continue
        agent._synthesize(mode, placement, f"{identifier} editorial {mode}", colors).save(path)
        created.append({
            "id": identifier,
            "mode": mode,
            "placement": placement,
            "aspect_ratio": f"{SIZES[placement][0]}:{SIZES[placement][1]}",
            "palette_tag": str((palette or {}).get("name", "default")),
            "dimensions": list(SIZES[placement]),
            "path": str(path),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "renderer_version": RENDERER_VERSION,
        })
    if created:
        manifest.extend(created)
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        _manifest_cache = manifest
    return created


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append assets to the offline images-factory pool.")
    parser.add_argument("--count", type=int, default=4)
    print(json.dumps(build_pool(parser.parse_args().count), indent=2))
