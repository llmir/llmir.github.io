"""Read aggregate pageview counts from the site's MapMyVisitors dashboard."""

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import re
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://mapmyvisitors.com"


def fetch(path):
    request = Request(ORIGIN + path, headers={"User-Agent": "AcademicHomepageStats/1.0"})
    with urlopen(request, timeout=10) as response:
        return response.read().decode("utf-8")


def field(pattern, html):
    match = re.search(pattern, html, re.S)
    if match is None:
        raise ValueError("MapMyVisitors aggregate fields are unavailable")
    return match[1]


def integer(value):
    result = int(str(value).replace(",", "").strip())
    if result < 0:
        raise ValueError("Negative pageview count")
    return result


def snapshot(stats_id):
    if not re.fullmatch(r"[a-zA-Z0-9]{3,24}", stats_id):
        raise ValueError("Invalid MapMyVisitors statistics ID")
    html = fetch(f"/web/{stats_id}")
    dashboard_id = field(r'''/ajax/orange_dots['"],?\s*\{\s*['"]id['"]\s*:\s*['"]?(\d+)''', html)
    cursor = field(r"var last_hit_id\s*=\s*(\d+)", html)
    recent_visits = field(r"var max_visit_count\s*=\s*(\d+)", html)
    query = urlencode({
        "id": dashboard_id, "last_hit_id": cursor, "max_hit_id": cursor,
        "max_visit_count": recent_visits,
    })
    view_counts = json.loads(fetch(f"/ajax/orange_dots?{query}"))
    prior_week = field(
        r'Last 7 days\s*</div>\s*<div class="pvTV">\s*([\d,]+)\s*</div>', html
    )
    return {
        "asOf": datetime.now(UTC).isoformat(timespec="seconds"),
        "statsId": stats_id,
        "total": integer(view_counts["total_hits"]),
        "today": integer(view_counts["today_hits"]),
        "last7": integer(prior_week),
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    profile = json.loads((ROOT / "content/profile.json").read_text(encoding="utf8"))
    try:
        totals = snapshot(profile["visitors"]["statsId"])
    except (OSError, KeyError, ValueError) as exc:
        raise SystemExit(f"Aggregate visitor metrics unavailable: {type(exc).__name__}") from None
    args.output.write_text(json.dumps(totals, indent=2) + "\n", encoding="utf8")
