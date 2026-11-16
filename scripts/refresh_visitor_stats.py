"""Read aggregate pageview counts from the site's MapMyVisitors dashboard."""

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import re
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://mapmyvisitors.com"


def fetch(url):
    request = Request(url, headers={"User-Agent": "AcademicHomepageStats/1.0"})
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
    html = fetch(f"{ORIGIN}/web/{stats_id}")
    dashboard_id = field(r'''/ajax/orange_dots['"],?\s*\{\s*['"]id['"]\s*:\s*['"]?(\d+)''', html)
    cursor = field(r"var last_hit_id\s*=\s*(\d+)", html)
    recent_visits = field(r"var max_visit_count\s*=\s*(\d+)", html)
    query = urlencode({
        "id": dashboard_id, "last_hit_id": cursor, "max_hit_id": cursor,
        "max_visit_count": recent_visits,
    })
    view_counts = json.loads(fetch(f"{ORIGIN}/ajax/orange_dots?{query}"))
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


def validate(totals, stats_id):
    collected = datetime.fromisoformat(totals["asOf"])
    counts = [totals[key] for key in ("total", "today", "last7")]
    if (totals["statsId"] != stats_id or collected.tzinfo is None
            or collected > datetime.now(UTC)
            or any(type(count) is not int or count < 0 for count in counts)):
        raise ValueError("Invalid visitor snapshot")
    return collected


def refresh(output, stats_id, published_url):
    try:
        totals = snapshot(stats_id)
        validate(totals, stats_id)
        source = "MapMyVisitors"
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"Visitor refresh unavailable ({type(error).__name__})")
        try:
            totals = json.loads(fetch(published_url))
            published_at = validate(totals, stats_id)
        except (OSError, KeyError, TypeError, ValueError):
            raise SystemExit("Using the checked-in visitor snapshot") from None
        try:
            checked_in = json.loads(output.read_text(encoding="utf-8"))
            checked_in_at = validate(checked_in, stats_id)
        except (OSError, KeyError, TypeError, ValueError):
            checked_in_at = None
        if checked_in_at and checked_in_at >= published_at:
            print(f"Using checked-in visitor snapshot from {checked_in['asOf']}")
            return
        source = "the last published snapshot"
    output.write_text(json.dumps(totals, indent=2) + "\n", encoding="utf-8")
    print(f"Using visitor counts from {source} ({totals['asOf']})")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    profile = json.loads((ROOT / "content/profile.json").read_text(encoding="utf8"))
    if visitors := profile.get("visitors"):
        refresh(args.output, visitors["statsId"], urljoin(profile["site"], "visitor-stats.json"))
