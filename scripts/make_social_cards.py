#!/usr/bin/env python3
"""Generate one 1200x630 social card per published guide (backlog 5.3+).

Output: ``og/<slug>.png``.  ``scripts/build.py`` points each guide's og:image and
twitter:image at its card when the file exists, and falls back to the site-wide
``og-image.png`` otherwise.

Usage:
    python3 scripts/make_social_cards.py              # (re)generate every card
    python3 scripts/make_social_cards.py --only SLUG  # one guide
    python3 scripts/make_social_cards.py --prune      # delete cards for unknown slugs

Requires Pillow (``pip install pillow``); it is only needed when cards are
regenerated, never by the site itself.  Fonts: pass ``--fonts DIR`` with
Manrope / Inter / JetBrains Mono TTFs, otherwise DejaVu Sans is used.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / "metadata.json"
OUT = ROOT / "og"

W, H = 1200, 630
PAPER = (250, 250, 249)
INK = (28, 28, 30)
INK_SOFT = (84, 84, 90)
MUTED = (110, 110, 115)
GREEN = (15, 138, 95)
GREEN_DARK = (13, 125, 86)
LINE = (224, 224, 222)
CHIP = (230, 244, 238)
STALE = (194, 65, 12)

DEJAVU = "/usr/share/fonts/truetype/dejavu/"


def font(fonts: Path | None, names: list[str], size: int, fallback: str) -> ImageFont.FreeTypeFont:
    if fonts is not None:
        for name in names:
            p = fonts / name
            if p.is_file():
                return ImageFont.truetype(str(p), size)
    return ImageFont.truetype(DEJAVU + fallback, size)


def wrap_to_width(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, max_w: int, max_lines: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
            continue
        if cur:
            lines.append(cur)
        cur = w
        if len(lines) == max_lines:
            break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and " ".join(words) != " ".join(lines):
        # ran out of room: add an ellipsis to the last line
        last = lines[-1]
        while last and draw.textlength(last + "…", font=f) > max_w:
            last = last[:-1].rstrip()
        lines[-1] = last + "…"
    return lines


def draw_card(a: dict, site: dict, cats: dict, fonts: Path | None) -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    f_brand = font(fonts, ["Manrope-ExtraBold.ttf", "Manrope[wght].ttf", "Manrope.ttf"], 26, "DejaVuSans-Bold.ttf")
    f_mono = font(fonts, ["JetBrainsMono-Medium.ttf", "JetBrainsMono[wght].ttf"], 22, "DejaVuSans.ttf")
    f_title = font(fonts, ["Manrope-ExtraBold.ttf", "Manrope[wght].ttf", "Manrope.ttf"], 60, "DejaVuSans-Bold.ttf")
    f_hook = font(fonts, ["Inter-Regular.ttf", "Inter[opsz,wght].ttf", "Inter.ttf"], 27, "DejaVuSans.ttf")
    f_small = font(fonts, ["JetBrainsMono-Medium.ttf", "JetBrainsMono[wght].ttf"], 20, "DejaVuSans.ttf")

    # left rail + brand mark
    d.rectangle([0, 0, 18, H], fill=GREEN)
    d.ellipse([64, 62, 84, 82], fill=GREEN)
    d.text((98, 58), site["title"], font=f_brand, fill=INK)

    # category chip
    cat = cats.get(a["category"], {})
    label = cat.get("label", a["category"].replace("-", " ").title()).upper()
    tw = d.textlength(label, font=f_mono)
    d.rounded_rectangle([64, 128, 64 + int(tw) + 34, 128 + 44], radius=22, fill=CHIP)
    d.text((81, 137), label, font=f_mono, fill=GREEN_DARK)

    # title + hook
    y = 200
    for line in wrap_to_width(d, a["title"], f_title, W - 128, 3):
        d.text((64, y), line, font=f_title, fill=INK)
        y += 72
    y += 14
    for line in wrap_to_width(d, a["hook"], f_hook, W - 128, 2):
        d.text((64, y), line, font=f_hook, fill=INK_SOFT)
        y += 38

    # footer: tool + verified date + reading time
    d.line([64, 548, W - 64, 548], fill=LINE, width=2)
    tool = wrap_to_width(d, a["tool"], f_small, 760, 1)[0]
    d.text((64, 572), tool, font=f_small, fill=MUTED)
    verified = dt.date.fromisoformat(a["verified"])
    stale = (dt.date.today() - verified).days > 365
    vtxt = ("⚠ " if stale else "✓ ") + "verified " + verified.strftime("%b %-d, %Y")
    vw = d.textlength(vtxt, font=f_small)
    d.text((W - 64 - vw, 572), vtxt, font=f_small, fill=STALE if stale else GREEN_DARK)
    d.text((64, 604), site["base_url"].replace("https://", "").rstrip("/"), font=f_small, fill=MUTED)
    return img


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fonts", type=Path, default=None, help="directory with Manrope / Inter / JetBrains Mono TTFs")
    ap.add_argument("--only", help="generate only this slug")
    ap.add_argument("--prune", action="store_true", help="delete cards whose slug is no longer published")
    args = ap.parse_args()

    data = json.loads(METADATA.read_text(encoding="utf-8"))
    site = data["site"]
    cats = site.get("categories", {})
    published = [a for a in data["articles"] if a["status"] == "published"]
    if args.only:
        published = [a for a in published if a["slug"] == args.only]
        if not published:
            raise SystemExit(f"no published guide with slug {args.only!r}")

    OUT.mkdir(exist_ok=True)
    for a in published:
        draw_card(a, site, cats, args.fonts).save(OUT / f"{a['slug']}.png", optimize=True)

    if args.prune and not args.only:
        keep = {a["slug"] for a in data["articles"] if a["status"] == "published"}
        for p in OUT.glob("*.png"):
            if p.stem not in keep:
                p.unlink()
    print(f"wrote {len(published)} social card(s) to {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
