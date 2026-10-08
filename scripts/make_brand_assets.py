#!/usr/bin/env python3
"""Generate the site's brand assets: favicon set + Open Graph preview image.

Outputs (written to the repository root):
    favicon.svg            vector favicon (modern browsers)
    favicon.ico            16/32/48 px multi-size fallback
    apple-touch-icon.png   180x180 iOS home-screen icon
    og-image.png           1200x630 social preview (Open Graph / Twitter)

Requires Pillow (``pip install pillow``) - only for regenerating assets; the
site itself has no build-time dependency on it.

Fonts: pass a directory containing Manrope / Inter / JetBrains Mono TTFs via
``--fonts DIR`` (variable fonts from github.com/google/fonts work); otherwise
DejaVu Sans is used as a fallback.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

GREEN = (15, 138, 95)        # --green  (light)
GREEN_DARK = (34, 197, 139)  # --green  (dark)
CORAL = (255, 128, 100)
PAPER = (250, 250, 249)
INK = (28, 28, 30)
INK_SOFT = (199, 199, 203)
MUTED = (138, 138, 143)

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <title>Everyday AI, Done Right</title>
  <rect width="64" height="64" rx="15" fill="#0F8A5F"/>
  <circle cx="32" cy="32" r="12" fill="#FAFAF9"/>
</svg>
"""


def _font(fonts: Path | None, candidates: list[str], size: int, variation: str | None = None) -> ImageFont.FreeTypeFont:
    if fonts is not None:
        for name in candidates:
            p = fonts / name
            if p.is_file():
                f = ImageFont.truetype(str(p), size)
                if variation:
                    try:
                        f.set_variation_by_name(variation)
                    except Exception:
                        pass
                return f
    fallback = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if variation in ("ExtraBold", "Bold") else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(fallback, size)


def draw_mark(size: int) -> Image.Image:
    """Green rounded square with a paper-coloured dot (matches the topbar mark)."""
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radius = int(s * 15 / 64)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=radius, fill=GREEN + (255,))
    r = s * 12 / 64
    c = s / 2
    d.ellipse((c - r, c - r, c + r, c + r), fill=PAPER + (255,))
    return img.resize((size, size), Image.LANCZOS)


def make_favicons() -> None:
    (ROOT / "favicon.svg").write_text(FAVICON_SVG, encoding="utf-8")
    icons = [draw_mark(n) for n in (16, 32, 48)]
    icons[-1].save(ROOT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=icons[:-1])
    draw_mark(180).save(ROOT / "apple-touch-icon.png", optimize=True)


def make_og_image(fonts: Path | None) -> None:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # subtle green glow top-right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((760, -260, 1460, 440), fill=GREEN_DARK + (38,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"))
    d = ImageDraw.Draw(img)

    manrope = ["Manrope.ttf", "Manrope[wght].ttf", "Manrope-ExtraBold.ttf"]
    inter = ["Inter.ttf", "Inter[opsz,wght].ttf", "Inter-Regular.ttf"]
    mono = ["JetBrainsMono.ttf", "JetBrainsMono[wght].ttf", "JetBrainsMono-Medium.ttf"]

    f_brand = _font(fonts, manrope, 26, "ExtraBold")
    f_eyebrow = _font(fonts, mono, 20, "Medium")
    f_h1 = _font(fonts, manrope, 96, "ExtraBold")
    f_sub = _font(fonts, inter, 30, "Regular")
    f_small = _font(fonts, mono, 19, "Medium")
    f_price = _font(fonts, manrope, 44, "ExtraBold")

    x = 72
    # brand mark + name
    img.paste(draw_mark(40), (x, 64), draw_mark(40))
    d.text((x + 56, 70), "Everyday AI, Done Right", font=f_brand, fill=PAPER)

    # eyebrow pill
    label = "VERIFIED  ·  NO CREDIT CARD  ·  EVER"
    tw = d.textlength(label, font=f_eyebrow)
    px, py = x, 150
    d.rounded_rectangle((px, py, px + tw + 40, py + 44), radius=22, fill=(30, 60, 48))
    d.text((px + 20, py + 11), label, font=f_eyebrow, fill=GREEN_DARK)

    # headline
    d.text((x - 4, 220), "Real AI leverage.", font=f_h1, fill=PAPER)
    d.text((x - 4, 322), "Actually free.", font=f_h1, fill=GREEN_DARK)

    # subline
    d.text((x, 448), "100+ step-by-step guides using AI tools that cost genuinely nothing —", font=f_sub, fill=INK_SOFT)
    d.text((x, 488), "checked against real provider docs, not vibes.", font=f_sub, fill=INK_SOFT)

    # footer row
    d.line((x, 556, W - 72, 556), fill=(60, 60, 64), width=1)
    d.text((x, 576), "iggym.github.io/everyday-ai-done-right", font=f_small, fill=MUTED)

    # price flip, bottom-right
    old = "$29/mo"
    new = "$0"
    nw = d.textlength(new, font=f_price)
    ow = d.textlength(old, font=f_small)
    nx = W - 72 - nw
    d.text((nx, 560), new, font=f_price, fill=GREEN_DARK)
    ox = nx - ow - 22
    d.text((ox, 578), old, font=f_small, fill=MUTED)
    # strike-through in coral
    d.line((ox - 2, 590, ox + ow + 2, 590), fill=CORAL, width=3)

    img.save(ROOT / "og-image.png", optimize=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fonts", type=Path, default=None, help="directory with Manrope/Inter/JetBrains Mono TTFs")
    args = ap.parse_args()
    make_favicons()
    make_og_image(args.fonts)
    for name in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "og-image.png"):
        print(f"wrote {name} ({(ROOT / name).stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
