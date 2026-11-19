"""Pure 16:9 geometry contracts shared by builders and the inspector."""
import math

W, H = 13.333, 7.5
MARGIN = 0.55
GUTTER = 0.30
FOOTER = (MARGIN, 7.16, W - 2 * MARGIN, 0.22)

ZONES = {
    "split_right": {
        "image": (6.667, 0, 6.666, H),
        "content": (0.65, 0.95, 5.4, 5.9),
    },
    "split_left": {
        "image": (0, 0, 6.667, H),
        "content": (7.32, 0.95, 5.4, 5.9),
    },
    "giant_stat_split": {
        "image": (7.33, 0, 6.0, H),
        "content": (0.65, 0.75, 6.0, 6.1),
    },
    "hero_banner": {
        "image": (0, 0, W, 4.35),
        "content": (0.7, 4.62, 11.9, 2.3),
    },
    "full_bleed_glass": {
        "image": (0, 0, W, H),
        "content": (1.25, 1.35, 7.1, 5.0),
    },
}


def layout_zones(placement: str) -> dict[str, tuple[float, float, float, float]]:
    zones = dict(ZONES.get(placement, ZONES["split_right"]))
    zones["footer"] = FOOTER
    return zones


def rects_intersect(a, b, gap: float = 0.0) -> bool:
    return (a[0] < b[0] + b[2] + gap and b[0] < a[0] + a[2] + gap
            and a[1] < b[1] + b[3] + gap and b[1] < a[1] + a[3] + gap)


def text_lines(value: str, width: float, size: float) -> list[str]:
    per_line = max(8, int((width * 72) / (size * 0.52)))
    lines: list[str] = []
    for part in str(value).split("\n"):
        for start in range(0, max(1, len(part)), per_line):
            lines.append(part[start:start + per_line])
    return lines


def fit_size(value: str, width: float, height: float, size: float,
             minimum: float = 13.0) -> tuple[float, list[str]]:
    current = size
    while current > minimum:
        lines = text_lines(value, width, current)
        if len(lines) * current * 1.25 / 72 <= height:
            return current, lines
        current -= 1
    return minimum, text_lines(value, width, minimum)
