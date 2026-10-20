#!/usr/bin/env python3
"""Scrape the public contributions calendar -> data/contributions.json (no token)."""
import json, os, re
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "rushanadv")
OUT = Path("data/contributions.json")


def fetch():
    r = requests.get(
        f"https://github.com/users/{USERNAME}/contributions",
        headers={"User-Agent": "profile-art-bot", "X-Requested-With": "XMLHttpRequest"},
        timeout=30,
    )
    r.raise_for_status()
    return r.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")

    tips = {}
    for tip in soup.find_all("tool-tip"):
        ref = tip.get("for")
        if not ref:
            continue
        m = re.search(r"([\d,]+)\s+contribution", tip.get_text())
        tips[ref] = int(m.group(1).replace(",", "")) if m else 0

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        iso = td.get("data-date")
        if not iso:
            continue
        raw = td.get("data-count")
        count = int(raw) if raw is not None else tips.get(td.get("id"), 0)
        days.append({"date": iso, "count": count, "level": int(td.get("data-level") or 0)})

    days.sort(key=lambda d: d["date"])
    return days


def stats(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)

    current = 0
    for i, d in enumerate(reversed(days)):
        if d["count"]:
            current += 1
        elif i == 0:
            continue
        else:
            break

    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    months = {}
    for d in days:
        months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]

    return {
        "total": sum(d["count"] for d in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "months": months,
    }


if __name__ == "__main__":
    days = parse(fetch())
    if len(days) < 300:
        raise SystemExit(f"Only parsed {len(days)} days - GitHub probably changed its markup.")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        "username": USERNAME,
        "generated": date.today().isoformat(),
        "days": days,
        "stats": stats(days),
    }, indent=2))
    print(f"{len(days)} days, {stats(days)['total']} contributions")
