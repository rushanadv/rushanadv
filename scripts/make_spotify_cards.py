#!/usr/bin/env python3
"""Generate sleek Spotify embed cards (SVG) for GitHub README."""
import base64
from pathlib import Path
import urllib.request

TRACKS = [
    {
        "id": "1",
        "title": "Call Out My Name",
        "artist": "The Weeknd",
        "album_art_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e021f6a2a40bb692936879db730",
        "duration": "3:48",
        "progress_ratio": 0.55,
        "out_file": Path("spotify-track-1.svg"),
        "url": "https://open.spotify.com/track/09mEdoA6zrmBPgTEN5qXmN",
    },
    {
        "id": "2",
        "title": "Feel It (From “Invincible”)",
        "artist": "d4vd",
        "album_art_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e02a9da992c2ef398245027d654",
        "duration": "2:38",
        "progress_ratio": 0.42,
        "out_file": Path("spotify-track-2.svg"),
        "url": "https://open.spotify.com/track/3SAga35lAPYdjj3qyfEsCF",
    },
]

SPOTIFY_ICON_PATH = (
    "M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm3.669 11.538a.498.498 0 0 "
    "1-.686.165c-1.879-1.147-4.243-1.407-7.028-.77a.499.499 0 0 "
    "1-.222-.973c3.049-.696 5.662-.397 7.77.892a.5.5 0 0 1 .166.686zm.979-2.178a.624.624 "
    "0 0 1-.857.205c-2.15-1.321-5.428-1.704-7.972-.932a.625.625 0 0 "
    "1-.362-1.196c2.904-.882 6.516-.454 8.986 1.066a.624.624 0 0 1 .205.857zm.084-2.269C10.158 "
    "5.55 5.864 5.409 3.415 6.153a.749.749 0 1 1-.434-1.435c2.812-.852 7.553-.69 10.427 "
    "1.018a.749.749 0 1 1-.776 1.282z"
)


def render_card(track):
    # Fetch artwork
    req = urllib.request.Request(
        track["album_art_url"],
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as resp:
        b64_art = base64.b64encode(resp.read()).decode("ascii")

    prog_w = int(140 * track["progress_ratio"])
    knob_x = 158 + prog_w

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="420" height="120" viewBox="0 0 420 120" role="img" aria-label="{track['title']} - {track['artist']}">
  <defs>
    <linearGradient id="bg-{track['id']}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#181818" />
      <stop offset="100%" stop-color="#101010" />
    </linearGradient>
    <clipPath id="art-clip-{track['id']}">
      <rect x="12" y="12" width="96" height="96" rx="8" />
    </clipPath>
  </defs>

  <style>
    .card {{ cursor: pointer; }}
    .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 14.5px; font-weight: 700; fill: #ffffff; }}
    .artist {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 12.5px; font-weight: 500; fill: #b3b3b3; }}
    .badge {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 10px; font-weight: 700; fill: #1DB954; letter-spacing: 0.8px; }}
    .dur {{ font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 10.5px; fill: #727272; }}
    @keyframes pulse {{
      0%, 100% {{ height: 4px; y: 92px; }}
      50% {{ height: 12px; y: 84px; }}
    }}
    .eq-bar-1 {{ animation: pulse 1.2s ease-in-out infinite; }}
    .eq-bar-2 {{ animation: pulse 0.9s ease-in-out infinite 0.2s; }}
    .eq-bar-3 {{ animation: pulse 1.4s ease-in-out infinite 0.4s; }}
    .eq-bar-4 {{ animation: pulse 1.0s ease-in-out infinite 0.1s; }}
  </style>

  <!-- Card Background -->
  <rect x="1" y="1" width="418" height="118" rx="12" fill="url(#bg-{track['id']})" stroke="#282828" stroke-width="1.2" />

  <!-- Album Artwork -->
  <image href="data:image/jpeg;base64,{b64_art}" x="12" y="12" width="96" height="96" clip-path="url(#art-clip-{track['id']})" />

  <!-- Spotify Header -->
  <g transform="translate(122, 14)">
    <path d="{SPOTIFY_ICON_PATH}" fill="#1DB954" transform="scale(0.85)" />
    <text x="17" y="11" class="badge">SPOTIFY &#183; SUGGESTED TRACK</text>
  </g>

  <!-- Track Title -->
  <text x="122" y="52" class="title">{track['title']}</text>

  <!-- Artist -->
  <text x="122" y="71" class="artist">{track['artist']}</text>

  <!-- Player Controls -->
  <!-- Play Button -->
  <g transform="translate(122, 83)">
    <circle cx="11" cy="11" r="11" fill="#1DB954" />
    <polygon points="9,7 16,11 9,15" fill="#000000" />
  </g>

  <!-- Equalizer / Visualizer -->
  <g fill="#1DB954">
    <rect class="eq-bar-1" x="150" y="88" width="2.5" height="8" rx="1.2" />
    <rect class="eq-bar-2" x="154.5" y="86" width="2.5" height="10" rx="1.2" />
    <rect class="eq-bar-3" x="159" y="85" width="2.5" height="11" rx="1.2" />
    <rect class="eq-bar-4" x="163.5" y="87" width="2.5" height="9" rx="1.2" />
  </g>

  <!-- Progress Track -->
  <g transform="translate(174, 91)">
    <rect x="0" y="2" width="160" height="3" rx="1.5" fill="#3e3e3e" />
    <rect x="0" y="2" width="{prog_w}" height="3" rx="1.5" fill="#1DB954" />
    <circle cx="{prog_w}" cy="3.5" r="3.5" fill="#ffffff" />
  </g>

  <!-- Duration -->
  <text x="344" y="97" class="dur">{track['duration']}</text>
</svg>
"""
    track["out_file"].write_text(svg, encoding="utf-8")
    print(f"Wrote {track['out_file']}")


if __name__ == "__main__":
    for t in TRACKS:
        render_card(t)

