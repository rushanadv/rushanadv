#!/usr/bin/env python3
"""contributions.json -> contrib-heatmap.svg (diagonal reveal, plays once)."""
import json
from datetime import date
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")

CELL, GAP, R = 12, 3, 2.5
PAD_L, PAD_T = 30, 22
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
TEXT, MUTED = "#c9d1d9", "#7d8590"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def level_of(day):
    if day["level"] >= 4 and day["count"] >= 25:
        return 5
    return day["level"]


def build(doc):
    days, st = doc["days"], doc["stats"]
    step = CELL + GAP

    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7
    cols = (offset + len(days) + 6) // 7

    w = PAD_L + cols * step + 20
    h = PAD_T + 7 * step + 58

    cells, labels, seen = [], [], set()
    for i, d in enumerate(days):
        idx = offset + i
        col, row = idx // 7, idx % 7
        x, y = PAD_L + col * step, PAD_T + row * step
        delay = round((col + row) * 0.011, 3)
        cells.append(
            f'<rect class="d" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{R}" '
            f'fill="{PALETTE[level_of(d)]}" style="animation-delay:{delay}s">'
            f'<title>{d["count"]} on {d["date"]}</title></rect>'
        )
        month = d["date"][:7]
        if row == 0 and month not in seen and col < cols - 1:
            seen.add(month)
            labels.append(f'<text class="m" x="{x}" y="{PAD_T - 7}">'
                          f'{MONTHS[int(d["date"][5:7]) - 1]}</text>')

    for r_i, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        labels.append(f'<text class="m" x="0" y="{PAD_T + r_i * step + 10}">{name}</text>')

    legend_x = w - 150
    legend_y = PAD_T + 7 * step + 18
    legend = [f'<text class="m" x="{legend_x}" y="{legend_y + 10}">Less</text>']
    for i, c in enumerate(PALETTE[:5]):
        legend.append(f'<rect x="{legend_x + 32 + i * 16}" y="{legend_y}" width="{CELL}" '
                      f'height="{CELL}" rx="{R}" fill="{c}"/>')
    legend.append(f'<text class="m" x="{legend_x + 118}" y="{legend_y + 10}">More</text>')

    footer = (f'<text class="f" x="{PAD_L}" y="{legend_y + 10}">'
              f'{st["total"]:,} contributions in the last year  &#183;  '
              f'{st["current_streak"]}d current  &#183;  {st["longest_streak"]}d longest  &#183;  '
              f'best {st["best_day"]["count"]} on {st["best_day"]["date"]}</text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<style>
  text {{ font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; }}
  .m {{ font-size: 9px; fill: {MUTED}; }}
  .f {{ font-size: 11px; fill: {TEXT}; }}
  .d {{ opacity: 0; transform-box: fill-box; transform-origin: center;
        animation: pop .42s cubic-bezier(.2,.8,.3,1) forwards; }}
  @keyframes pop {{
    from {{ opacity: 0; transform: translateY(-7px) scale(.55); }}
    to   {{ opacity: 1; transform: none; }}
  }}
</style>
{"".join(labels)}
{"".join(cells)}
{"".join(legend)}
{footer}
</svg>'''


if __name__ == "__main__":
    OUT.write_text(build(json.loads(DATA.read_text())))
    print(f"wrote {OUT}")
