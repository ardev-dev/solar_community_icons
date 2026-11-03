"""Builds the custom icons that are not part of the Solar Vol.2 community set.

Each icon is drawn from simple geometry on the Solar grid (24x24, 1.5px
stroke, round caps and joins), then flattened to filled outlines so that
`icon_generator` can turn it into a font glyph like the rest of the set.

Usage (needs `pip install skia-pathops picosvg`):

    python scripts/custom_icons/build_custom_icons.py

Writes assets/icons/linear/<name>.svg and assets/icons/bold/<name>.svg.
"""

from __future__ import annotations

import math
import pathlib
import re

import pathops
from picosvg.svg_pathops import skia_path, svg_commands
from picosvg.svg_transform import Affine2D
from picosvg.svg_types import SVGCircle, SVGEllipse, SVGPath

STROKE = 1.5
ROOT = pathlib.Path(__file__).resolve().parents[2]


# --- geometry helpers -------------------------------------------------------


def _sk(svg_path: SVGPath) -> pathops.Path:
    p = skia_path(svg_path.as_cmd_seq(), "nonzero")
    p.convertConicsToQuads()
    return p


def path(d: str, transform: str | None = None) -> pathops.Path:
    p = SVGPath(d=d)
    if transform:
        p = p.apply_transform(Affine2D.fromstring(transform))
    return _sk(p)


def circle(cx: float, cy: float, r: float) -> pathops.Path:
    return _sk(SVGCircle(cx=cx, cy=cy, r=r).as_path())


def ellipse(cx, cy, rx, ry, rotate: float = 0) -> pathops.Path:
    p = SVGEllipse(cx=cx, cy=cy, rx=rx, ry=ry).as_path()
    if rotate:
        p = p.apply_transform(Affine2D.fromstring(f"rotate({rotate} {cx} {cy})"))
    return _sk(p)


def rect(x, y, w, h) -> pathops.Path:
    return path(f"M{x} {y} H{x + w} V{y + h} H{x} Z")


def stroke(p: pathops.Path, width: float = STROKE) -> pathops.Path:
    out = pathops.Path(p)
    out.stroke(width, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
    out.convertConicsToQuads()
    return out


def union(*paths: pathops.Path) -> pathops.Path:
    out = pathops.Path()
    for p in paths:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def diff(a: pathops.Path, *b: pathops.Path) -> pathops.Path:
    return pathops.op(a, union(*b), pathops.PathOp.DIFFERENCE)


def inter(a: pathops.Path, b: pathops.Path) -> pathops.Path:
    return pathops.op(a, b, pathops.PathOp.INTERSECTION)


def polygon(points) -> pathops.Path:
    head, *rest = points
    d = f"M{head[0]:.3f} {head[1]:.3f} " + " ".join(f"L{x:.3f} {y:.3f}" for x, y in rest)
    return path(d + " Z")


# --- icons ------------------------------------------------------------------


def car():
    body = (
        "M5 17.25 H4 C3.31 17.25 2.75 16.69 2.75 16 V13.62 C2.75 12.67 3.42 11.85 4.35 11.66"
        " L6.5 11.2 L8.36 7.98 C8.81 7.22 9.62 6.75 10.5 6.75 H13.82 C14.66 6.75 15.44 7.18"
        " 15.89 7.89 L17.9 11.1 L19.6 11.43 C20.56 11.62 21.25 12.46 21.25 13.43 V16"
        " C21.25 16.69 20.69 17.25 20 17.25 H19"
    )
    linear = union(
        stroke(path(body)),
        stroke(path("M9 17.25 H15")),
        stroke(path("M6.5 11.2 H17.9")),
        stroke(path("M12.25 6.75 V11.2")),
        stroke(circle(7, 17.25, 2)),
        stroke(circle(17, 17.25, 2)),
    )
    shell = path(
        "M4 17.25 C3.31 17.25 2.75 16.69 2.75 16 V13.62 C2.75 12.67 3.42 11.85 4.35 11.66"
        " L6.5 11.2 L8.36 7.98 C8.81 7.22 9.62 6.75 10.5 6.75 H13.82 C14.66 6.75 15.44 7.18"
        " 15.89 7.89 L17.9 11.1 L19.6 11.43 C20.56 11.62 21.25 12.46 21.25 13.43 V16"
        " C21.25 16.69 20.69 17.25 20 17.25 Z"
    )
    shell = union(shell, stroke(shell))
    windows = union(
        path("M8.2 10.45 L9.5 8.6 C9.7 8.35 9.95 8.25 10.3 8.25 H11.5 V10.45 Z"),
        path("M13 8.25 H13.75 C14.1 8.25 14.4 8.4 14.6 8.7 L15.75 10.45 H13 Z"),
    )
    bold = union(
        diff(shell, windows, circle(7, 17.25, 3.5), circle(17, 17.25, 3.5)),
        circle(7, 17.25, 2.5),
        circle(17, 17.25, 2.5),
    )
    return linear, bold


def _saw_teeth(cx=12, cy=12, teeth=8, r_tip=9.75, r_valley=6.25, rise=0.82):
    """Hooked teeth: a slow rise to the tip, then a sharp drop to the next valley."""
    step = 2 * math.pi / teeth
    points = []
    for i in range(teeth):
        a = i * step - math.pi / 2
        points.append((cx + r_valley * math.cos(a), cy + r_valley * math.sin(a)))
        b = a + step * rise
        points.append((cx + r_tip * math.cos(b), cy + r_tip * math.sin(b)))
    return polygon(points)


def saw():
    teeth = _saw_teeth()
    linear = union(stroke(teeth), stroke(circle(12, 12, 2.25)))
    disc = union(teeth, stroke(teeth))
    bold = diff(disc, circle(12, 12, 2.25))
    return linear, bold


def concrete_mixer():
    """A mixer truck: cab, tilted ribbed drum and two wheels."""
    drum_t = "translate(8.75 10.75) rotate(22)"
    drum = path(
        "M-5.75 -1.6 L-0.75 -3.9 C2.6 -3.9 5.25 -2.25 5.25 0"
        " C5.25 2.25 2.6 3.9 -0.75 3.9 L-5.75 1.6 Z",
        drum_t,
    )
    stripes = path("M-3.25 -4 V4 M0.25 -4.5 V4.5", drum_t)
    cab = path(
        "M15.25 17.25 V10.75 C15.25 10.2 15.7 9.75 16.25 9.75 H18.4 C18.9 9.75 19.35 10.05"
        " 19.55 10.5 L21.05 13.75 C21.18 14.05 21.25 14.35 21.25 14.65 V16.25"
        " C21.25 16.8 20.8 17.25 20.25 17.25"
    )
    chassis = path("M8.75 17.25 H15.25 M10.5 14.75 V17.25")
    wheels = union(circle(6.25, 17.75, 1.75), circle(17.75, 17.75, 1.75))
    linear = union(
        stroke(drum),
        inter(stroke(stripes), drum),
        stroke(cab),
        stroke(chassis),
        stroke(wheels),
    )
    cab_fill = path(
        "M15.25 17.25 V10.75 C15.25 10.2 15.7 9.75 16.25 9.75 H18.4 C18.9 9.75 19.35 10.05"
        " 19.55 10.5 L21.05 13.75 C21.18 14.05 21.25 14.35 21.25 14.65 V16.25"
        " C21.25 16.8 20.8 17.25 20.25 17.25 Z"
    )
    cab_fill = union(cab_fill, stroke(cab_fill))
    window = path("M16.75 11.25 H18.25 L19.4 13.75 H16.75 Z")
    drum_fill = union(drum, stroke(drum))
    clearance = union(circle(6.25, 17.75, 3), circle(17.75, 17.75, 3))
    bold = union(
        diff(drum_fill, inter(stroke(stripes, 1.25), drum)),
        diff(union(cab_fill, stroke(chassis)), window, clearance),
        union(circle(6.25, 17.75, 2.25), circle(17.75, 17.75, 2.25)),
    )
    return linear, bold


def bee():
    head = circle(12, 5, 1.75)
    body = ellipse(12, 14.25, 4, 5.25)
    stripes = path("M7 12.75 H17 M7 15.75 H17")
    clearance = ellipse(12, 14.25, 5.5, 6.75)
    wings = union(ellipse(6.4, 9.6, 3.25, 2, 25), ellipse(17.6, 9.6, 3.25, 2, -25))
    feelers = union(
        stroke(path("M11 3.6 L9.9 2")),
        stroke(path("M13 3.6 L14.1 2")),
        stroke(path("M12 19.5 V21")),
    )
    linear = union(
        stroke(head),
        stroke(body),
        inter(stroke(stripes), body),
        diff(stroke(wings), clearance),
        feelers,
    )
    body_fill = union(body, stroke(body))
    wings_fill = union(wings, stroke(wings))
    bold = union(
        union(head, stroke(head)),
        diff(body_fill, inter(stroke(stripes, 1.25), body)),
        diff(wings_fill, clearance),
        feelers,
    )
    return linear, bold


def _existing_icon(style: str, name: str) -> pathops.Path:
    """The outline of an icon already in the set, exactly as it ships."""
    source = (ROOT / "assets/icons" / style / f"{name}.svg").read_text()
    d = re.search(r' d="([^"]+)"', source).group(1)
    p = skia_path(SVGPath(d=d).as_cmd_seq(), "evenodd")
    p.convertConicsToQuads()
    return p


def _with_slash(icon: pathops.Path) -> pathops.Path:
    """Adds a 45-degree slash, cleared on its upper right so it reads at small sizes."""
    gap = 1.2
    offset = gap / 2 / math.sqrt(2)
    clearance = stroke(
        path(f"M{4 + offset} {4 - offset} L{20 + offset} {20 - offset}"),
        STROKE + gap,
    )
    return union(diff(icon, clearance), stroke(path("M4 4 L20 20")))


def microphone_muted():
    """The set's `microphone` icon with a mute slash, so the two swap in place."""
    return (
        _with_slash(_existing_icon("linear", "microphone")),
        _with_slash(_existing_icon("bold", "microphone")),
    )


ICONS = {
    "car": car,
    "saw": saw,
    "concrete_mixer": concrete_mixer,
    "bee": bee,
    "microphone_muted": microphone_muted,
}


# --- output -----------------------------------------------------------------


def to_d(p: pathops.Path) -> str:
    simplified = pathops.simplify(p, clockwise=True)
    return SVGPath.from_commands(svg_commands(simplified)).round_floats(3).d


def svg(d: str, fill: str) -> str:
    return (
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg"><path d="{d}" stroke="none" '
        f'fill-rule="evenodd" fill="{fill}"></path></svg>'
    )


def main() -> None:
    for name, build in ICONS.items():
        linear, bold = build()
        (ROOT / "assets/icons/linear" / f"{name}.svg").write_text(svg(to_d(linear), "black"))
        (ROOT / "assets/icons/bold" / f"{name}.svg").write_text(svg(to_d(bold), "#1C274C"))
        print(f"✓ {name}")


if __name__ == "__main__":
    main()
