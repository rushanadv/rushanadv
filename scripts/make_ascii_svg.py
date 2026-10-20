#!/usr/bin/env python3
"""photo -> self-typing monochrome ASCII SVG.  usage: make_ascii_svg.py photo.jpg"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

COLS = 100
RAMP = " .`:-=+*cs#%@"
CHAR_W, LINE_H = 7.8, 13.0
FG, CURSOR = "#c9d1d9", "#39d353"
OUT = Path("ascii-portrait.svg")


def prep(path):
    img = Image.open(path).convert("RGB")

    try:
        from rembg import remove
        cut = remove(img)
        flat = Image.new("RGB", cut.size, (255, 255, 255))
        flat.paste(cut, mask=cut.split()[-1])
        img = flat
    except (Exception, SystemExit):
        # rembg calls sys.exit(1) when no onnxruntime backend is present.
        print("rembg unavailable - using the raw image")

    try:
        import cv2
        lab = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(l)
        img = Image.fromarray(cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2RGB))
    except ImportError:
        img = ImageOps.autocontrast(img, cutoff=2)

    return ImageOps.grayscale(img)


def to_rows(gray, contrast=1.4):
    rows = max(1, round(COLS * gray.height / gray.width * 0.5))
    arr = np.asarray(gray.resize((COLS, rows), Image.LANCZOS), np.float32) / 255.0
    arr = np.clip((arr - 0.5) * contrast + 0.5, 0, 1)
    idx = ((1 - arr) * (len(RAMP) - 1)).round().astype(int)
    return ["".join(RAMP[i] for i in row).rstrip() for row in idx]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(rows):
    w, h = COLS * CHAR_W, len(rows) * LINE_H + 8
    defs, body = [], []
    for i, line in enumerate(rows):
        top, delay = i * LINE_H, round(i * 0.042, 3)
        cid = f"w{i}"
        defs.append(
            f'<clipPath id="{cid}"><rect x="0" y="{top}" width="0" height="{LINE_H + 2}">'
            f'<animate attributeName="width" from="0" to="{w}" begin="{delay}s" '
            f'dur="0.3s" fill="freeze"/></rect></clipPath>'
        )
        body.append(f'<text x="0" y="{top + LINE_H}" clip-path="url(#{cid})" '
                    f'xml:space="preserve">{esc(line)}</text>')
        body.append(
            f'<rect x="0" y="{top + 2}" width="{CHAR_W}" height="{LINE_H - 3}" '
            f'fill="{CURSOR}" opacity="0">'
            f'<animate attributeName="x" from="0" to="{w}" begin="{delay}s" dur="0.3s" fill="freeze"/>'
            f'<set attributeName="opacity" to=".85" begin="{delay}s"/>'
            f'<set attributeName="opacity" to="0" begin="{round(delay + 0.3, 3)}s"/></rect>'
        )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">'
            f'<style>text{{font-family:ui-monospace,Menlo,Consolas,monospace;'
            f'font-size:11px;fill:{FG};white-space:pre}}</style>'
            f'<defs>{"".join(defs)}</defs>{"".join(body)}</svg>')


if __name__ == "__main__":
    OUT.write_text(build(to_rows(prep(sys.argv[1]))))
    print(f"wrote {OUT}")
