"""Deterministic semantic layout rotation for consecutive slides."""

CYCLE = ("bento", "kpi", "process", "comparison", "spotlight")


def route_layouts(layouts: list[str]) -> list[str]:
    routed: list[str] = []
    previous = ""
    for layout in layouts:
        chosen = layout if layout in CYCLE else "bento"
        if chosen == previous:
            chosen = CYCLE[(CYCLE.index(chosen) + 1) % len(CYCLE)]
        routed.append(chosen)
        previous = chosen
    return routed
