#!/usr/bin/env python3
"""Generate 3D Isometric Contributions Calendar SVG for GitHub profile."""
import json
from datetime import date
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-iso.svg")

# Pre-shaded faces for 100% native SVG / GitHub Camo compatibility
LEVEL_COLORS = {
    0: {"top": "#ebedf0", "left": "#c7c9cc", "right": "#a4a5a8", "stroke": "rgba(27,31,35,0.06)"},
    1: {"top": "#9be9a8", "left": "#72ae7d", "right": "#4d7a54", "stroke": "rgba(27,31,35,0.10)"},
    2: {"top": "#40c463", "left": "#2f9349", "right": "#206632", "stroke": "rgba(27,31,35,0.12)"},
    3: {"top": "#30a14e", "left": "#237739", "right": "#175126", "stroke": "rgba(27,31,35,0.14)"},
    4: {"top": "#216e39", "left": "#174f28", "right": "#0f351b", "stroke": "rgba(27,31,35,0.15)"},
}

CALENDAR_ICON = (
    "M4.75 0a.75.75 0 01.75.75V2h5V.75a.75.75 0 011.5 0V2h1.25c.966 0 1.75.784 "
    "1.75 1.75v10.5A1.75 1.75 0 0113.25 16H2.75A1.75 1.75 0 011 14.25V3.75C1 "
    "2.784 1.784 2 2.75 2H4V.75A.75.75 0 014.75 0zm0 3.5h8.5a.25.25 0 "
    "01.25.25V6h-11V3.75a.25.25 0 01.25-.25h2zm-2.25 4v6.75c0 .138.112.25.25.25h10.5a.25.25 "
    "0 00.25-.25V7.5h-11z"
)

FLAME_ICON = (
    "M8 0c-.22 0-.43.09-.59.25L3.82 3.84C2.69 4.97 2 6.51 2 8.16 2 11.47 4.69 "
    "14.16 8 14.16s6-2.69 6-6c0-1.65-.69-3.19-1.82-4.32L8.59.25A.83.83 0 0 0 8 0zm0 "
    "2.05l2.76 2.76c.86.86 1.39 2.04 1.39 3.35 0 2.29-1.86 4.15-4.15 4.15S3.85 "
    "10.45 3.85 8.16c0-1.31.53-2.49 1.39-3.35L8 2.05z"
)

TREND_ICON = (
    "M1.5 13a.75.75 0 01-.75-.75V2a.75.75 0 011.5 0v9.5h11a.75.75 0 "
    "010 1.5H1.5zm3.22-4.72a.75.75 0 011.06 0L8 10.44l3.72-3.72a.75.75 0 "
    "111.06 1.06l-4.25 4.25a.75.75 0 01-1.06 0L5.72 9.34l-1.44 1.44a.75.75 "
    "0 01-1.06-1.06l2-2a.75.75 0 01.5-.22z"
)


def build_svg():
    with open(DATA) as f:
        doc = json.load(f)

    days = doc["days"]
    stats = doc["stats"]

    # Filter to last 26 weeks (182 days) aligned to Sunday
    num_days = 182
    subset = days[-num_days:]
    first_date = date.fromisoformat(subset[0]["date"])
    sun_offset = (first_date.weekday() + 1) % 7
    start_idx = len(days) - num_days - sun_offset
    if start_idx < 0:
        start_idx = 0
    aligned = days[start_idx:]

    weeks = []
    for k in range(0, len(aligned), 7):
        chunk = aligned[k : k + 7]
        if len(chunk) == 7:
            weeks.append(chunk)

    ref = max([d["count"] for d in aligned] + [1])
    active_commits = sum(d["count"] for d in aligned)
    avg_per_day = round(active_commits / len(aligned), 2)
    streak = stats.get("current_streak", 0)

    size = 6
    cubes_svg = []

    for i, w in enumerate(weeks):
        week_cubes = []
        for j, d in enumerate(w):
            cnt = d["count"]
            lvl = d["level"]
            ratio = round(cnt / ref, 3) if ref > 0 else 0
            c = LEVEL_COLORS[lvl]
            y_rise = round((1 - ratio) * size, 3) if cnt > 0 else size
            h_left = round(2 + ratio * size, 3) if cnt > 0 else 2
            h_right = round(1 + ratio * size, 3) if cnt > 0 else 1

            trans_x = round(j * -1.7, 2)
            trans_y = round(j + y_rise, 2)

            top_poly = 'M1.7,2 0,1 1.7,0 3.4,1 z'
            left_poly = f'M0,1 1.7,2 1.7,{h_left} 0,{round(h_left - 1, 3)} z'
            right_poly = f'M1.7,2 3.4,1 3.4,{h_right} 1.7,{round(h_right + 1, 3)} z'

            cube = (
                f'<g transform="translate({trans_x}, {trans_y})">'
                f'<path fill="{c["top"]}" stroke="{c["stroke"]}" stroke-width="0.08" d="{top_poly}" />'
                f'<path fill="{c["left"]}" stroke="{c["stroke"]}" stroke-width="0.08" d="{left_poly}" />'
                f'<path fill="{c["right"]}" stroke="{c["stroke"]}" stroke-width="0.08" d="{right_poly}" />'
                f'</g>'
            )
            week_cubes.append(cube)

        w_trans_x = round(i * 1.7, 2)
        w_trans_y = i
        cubes_svg.append(f'<g transform="translate({w_trans_x}, {w_trans_y})">' + "".join(week_cubes) + "</g>")

    grid_content = "".join(cubes_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="270" viewBox="0 0 860 270" role="img" aria-label="Contributions calendar">
  <style>
    .header-title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 15px; font-weight: 600; fill: #58a6ff; }}
    .stat-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13px; font-weight: 500; fill: #c9d1d9; }}
  </style>

  <!-- Container Box -->
  <rect x="1" y="1" width="858" height="268" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.2" />

  <!-- Header: Contributions calendar -->
  <g transform="translate(24, 22)">
    <path d="{CALENDAR_ICON}" fill="#58a6ff" />
    <text x="26" y="13" class="header-title">Contributions calendar</text>
  </g>

  <!-- Top Right Stats -->
  <g transform="translate(390, 22)">
    <!-- Streak -->
    <g transform="translate(0, 0)">
      <path d="{FLAME_ICON}" fill="#f0883e" />
      <text x="22" y="12" class="stat-text">Current streak <tspan font-weight="700" fill="#f0883e">{streak} days</tspan></text>
    </g>

    <!-- Commits per day -->
    <g transform="translate(185, 0)">
      <path d="{TREND_ICON}" fill="#3fb950" />
      <text x="22" y="12" class="stat-text">~{avg_per_day} commits per day</text>
    </g>
  </g>

  <!-- Centered Isometric Projection Grid -->
  <g transform="translate(325, 48) scale(5.1)">
    {grid_content}
  </g>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build_svg()
