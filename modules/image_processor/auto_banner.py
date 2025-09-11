#!/usr/bin/env python3
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Tuple


PALETTE = {
    "news": (24, 84, 199),
    "chips-compute": (16, 95, 82),
    "robotics": (120, 53, 15),
    "consumer-electronics": (88, 28, 135),
    "policy": (29, 78, 216),
    "default": (15, 23, 42)
}


def _text_wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> str:
    words = text.split()
    lines = []
    cur = []
    for w in words:
        test = " ".join(cur + [w])
        if draw.textlength(test, font=font) <= max_width:
            cur.append(w)
        else:
            lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return "\n".join(lines[:3])


def generate_banner(title: str, category: str, out_dir: str = "static/images/news") -> Tuple[str, str]:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    w, h = 1200, 630
    bg = Image.new("RGB", (w, h), (245, 247, 250))
    draw = ImageDraw.Draw(bg)
    color = PALETTE.get(category, PALETTE["default"])

    # gradient bar
    for i in range(h):
        ratio = i / h
        r = int(color[0] * (1 - ratio) + 255 * ratio)
        g = int(color[1] * (1 - ratio) + 255 * ratio)
        b = int(color[2] * (1 - ratio) + 255 * ratio)
        draw.line([(0, i), (w, i)], fill=(r, g, b))

    # translucent overlay
    overlay = Image.new("RGBA", (w, h), (255, 255, 255, 140))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(bg)

    # fonts
    try:
        font_bold = ImageFont.truetype("arial.ttf", 64)
    except Exception:
        font_bold = ImageFont.load_default()

    title_wrapped = _text_wrap(draw, title, font_bold, int(w * 0.8))
    tw, th = draw.multiline_textsize(title_wrapped, font=font_bold, spacing=8)
    x = (w - tw) // 2
    y = (h - th) // 2
    draw.multiline_text((x, y), title_wrapped, fill=(20, 30, 46), font=font_bold, spacing=8, align="center")

    # save
    safe = "-".join(title.lower().split())[:60]
    fname = f"news-banner-{safe}.jpg"
    out_path = str(Path(out_dir) / fname)
    bg.convert("RGB").save(out_path, format="JPEG", quality=85)
    alt = f"{title} — {category.replace('-', ' ').title()} news banner"
    return out_path, alt

