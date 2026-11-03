"""Appends a custom icon to both fonts and Dart classes without touching the rest.

`icon_generator` rebuilds a font from scratch and reassigns code points, which
would change the glyph behind every icon an app has already compiled. This adds
one glyph after the last code point instead.

Usage (needs `pip install fonttools`):

    python scripts/custom_icons/append_to_fonts.py microphone_muted microphoneMuted
"""

from __future__ import annotations

import pathlib
import re
import sys

from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCALE = 512 / 24  # 24x24 SVG grid to the fonts' 512 units per em.
ASCENT = 272
STYLES = {
    "linear": ("Linear", "solar_linear_icons"),
    "bold": ("Bold", "solar_bold_icons"),
}


def glyph_from_svg(svg_path: pathlib.Path):
    d = re.search(r' d="([^"]+)"', svg_path.read_text()).group(1)
    pen = TTGlyphPen(None)
    quadratic = Cu2QuPen(pen, 0.5, reverse_direction=False)
    parse_path(d, TransformPen(quadratic, (SCALE, 0, 0, -SCALE, 0, ASCENT)))
    return pen.glyph()


def append(style: str, file_name: str, dart_name: str) -> int:
    label, stem = STYLES[style]
    # recalcBBoxes must stay off: the existing glyphs carry xMin 0 with a left side
    # bearing of 0, and recalculating would shift every icon sideways.
    font_path = ROOT / "assets/fonts" / f"{stem}.ttf"
    font = TTFont(font_path, recalcBBoxes=False, recalcTimestamp=False)
    if file_name in font.getGlyphOrder():
        raise SystemExit(f"{file_name} is already in {font_path.name}")

    code_point = max(font.getBestCmap()) + 1
    glyph = glyph_from_svg(ROOT / "assets/icons" / style / f"{file_name}.svg")
    glyph.recalcBounds(font["glyf"])

    order = font.getGlyphOrder() + [file_name]
    font["glyf"][file_name] = glyph
    font["hmtx"][file_name] = (512, glyph.xMin)
    font.setGlyphOrder(order)
    font["glyf"].glyphOrder = order
    maxp = font["maxp"]
    maxp.numGlyphs = len(order)
    coordinates, _, _ = glyph.getCoordinates(font["glyf"])
    maxp.maxPoints = max(maxp.maxPoints, len(coordinates))
    maxp.maxContours = max(maxp.maxContours, glyph.numberOfContours)
    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap[code_point] = file_name
    font.save(font_path)

    dart_path = ROOT / "lib" / f"{stem}.dart"
    source = dart_path.read_text().rstrip()
    if not source.endswith("}"):
        raise SystemExit(f"Unexpected end of {dart_path.name}")
    entry = (
        f"  /// {label} icon: {dart_name}.\n"
        f"  static const IconData {dart_name} = IconData(0x{code_point:x}, "
        f"fontFamily: 'SolarCommunity{label}Icons', "
        "fontPackage: 'solar_community_icons');\n"
    )
    dart_path.write_text(source[:-1] + entry + "}\n")
    return code_point


def main() -> None:
    file_name, dart_name = sys.argv[1:3]
    for style in STYLES:
        print(f"✓ {style}: 0x{append(style, file_name, dart_name):x}")


if __name__ == "__main__":
    main()
