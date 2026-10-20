#!/usr/bin/env python3
"""neofetch-style card that prints line by line."""
import os
from pathlib import Path

USER = "rushanadv"
ROWS = [
    ("Now",       "Student / Developer"),
    ("Prev",      "Add your previous role here"),
    ("Stack",     "Python &#183; JavaScript &#183; React"),
    ("Writing",   "yourblog.dev"),
    ("Highlight", "Something you shipped"),
    ("Reach",     "you@example.com"),
]

KEY, VAL, ACCENT, BORDER = "#39d353", "#c9d1d9", "#58a6ff", "#30363d"
W, LH, PAD = 490, 26, 22
STATIC = os.environ.get("STATIC") == "1"


def build():
    h = PAD * 2 + 46 + len(ROWS) * LH
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
           f'viewBox="0 0 {W} {h}" role="img">',
           f'<style>text{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px}}'
           f'.k{{fill:{KEY};font-weight:600}}.v{{fill:{VAL}}}.t{{fill:{ACCENT};font-size:14px;font-weight:700}}'
           + ("" if STATIC else
              f'.r{{opacity:0;animation:in .4s ease-out forwards}}'
              f'@keyframes in{{from{{opacity:0;transform:translateX(-10px)}}to{{opacity:1;transform:none}}}}')
           + '</style>',
           f'<rect x="1" y="1" width="{W-2}" height="{h-2}" rx="8" fill="#0d1117" stroke="{BORDER}"/>',
           f'<text class="t" x="{PAD}" y="{PAD+16}">{USER}@github</text>',
           f'<line x1="{PAD}" y1="{PAD+26}" x2="{W-PAD}" y2="{PAD+26}" stroke="{BORDER}"/>']

    cls = "" if STATIC else ' class="r"'
    for i, (k, v) in enumerate(ROWS):
        y = PAD + 50 + i * LH
        delay = "" if STATIC else f' style="animation-delay:{round(0.25 + i * 0.09, 2)}s"'
        out.append(f'<g{cls}{delay}><text class="k" x="{PAD}" y="{y}">{k}</text>'
                   f'<text class="v" x="{PAD + 92}" y="{y}">{v}</text></g>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    Path("info-card.svg").write_text(build())
    print("wrote info-card.svg")
