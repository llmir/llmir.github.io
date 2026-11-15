"""Refresh the homepage's Google Scholar snapshot once per day."""

from datetime import date, datetime
import json
import os
from pathlib import Path
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
PAGE_SIZE = 100
METRICS = {"citations": "citations", "hIndex": "h_index", "i10Index": "i10_index"}


def fetch_json(url):
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=15) as response:
        return json.load(response)


def validate(snapshot, profile_id, today):
    acquired = date.fromisoformat(snapshot["asOf"])
    if snapshot["profileId"] != profile_id or acquired > today:
        raise ValueError("Invalid profile or snapshot date")
    counts = [snapshot[field] for field in (*METRICS, "indexedRecords")]
    if any(type(count) is not int or count < 0 for count in counts):
        raise ValueError("Invalid Scholar count")
    if snapshot["i10Index"] > snapshot["indexedRecords"] or snapshot["hIndex"] > snapshot["indexedRecords"]:
        raise ValueError("Incomplete Scholar record count")
    yearly = snapshot["yearly"]
    years = [year for year, _ in yearly]
    if not yearly or years != sorted(set(years)):
        raise ValueError("Invalid Scholar citation years")
    if any(type(year) is not int or not 1900 <= year <= today.year
           or type(count) is not int or count < 0 for year, count in yearly):
        raise ValueError("Invalid yearly citation count")
    if snapshot["partialYear"] != acquired.year:
        raise ValueError("Invalid current year")
    return acquired


def author_page(profile_id, api_key, start):
    query = urlencode({
        "engine": "google_scholar_author",
        "author_id": profile_id,
        "hl": "en",
        "num": PAGE_SIZE,
        "cstart": start,
        "no_cache": "true",
        "api_key": api_key,
    })
    reply = fetch_json(f"https://serpapi.com/search.json?{query}")
    if reply["search_metadata"]["status"] != "Success" or reply["search_parameters"]["author_id"] != profile_id:
        raise ValueError("Scholar author query did not succeed")
    return reply


def collect(profile_id, api_key, today):
    reply = author_page(profile_id, api_key, 0)
    statistics = reply["cited_by"]
    all_time = {key: stat["all"] for row in statistics["table"] for key, stat in row.items()}
    yearly = sorted([row["year"], row["citations"]] for row in statistics["graph"])
    records = set()
    start = 0
    while True:
        articles = reply["articles"]
        page_ids = {article["citation_id"] for article in articles}
        if len(page_ids) != len(articles) or page_ids & records:
            raise ValueError("Repeated Scholar records")
        records.update(page_ids)
        if not reply.get("serpapi_pagination", {}).get("next"):
            break
        if len(articles) != PAGE_SIZE:
            raise ValueError("Incomplete Scholar page")
        start += PAGE_SIZE
        reply = author_page(profile_id, api_key, start)
    return {
        "asOf": today.isoformat(),
        "profileId": profile_id,
        **{field: all_time[key] for field, key in METRICS.items()},
        "yearly": yearly,
        "partialYear": today.year,
        "indexedRecords": len(records),
    }


def refresh(snapshot_file, published_url, api_key, today):
    checked_in = json.loads(snapshot_file.read_text(encoding="utf-8"))
    profile_id = checked_in["profileId"]
    best = checked_in
    best_date = validate(best, profile_id, today)
    try:
        published = fetch_json(published_url)
        published_date = validate(published, profile_id, today)
        if published_date > best_date:
            best, best_date = published, published_date
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"Published Scholar snapshot unavailable ({type(error).__name__})")

    if api_key and best_date < today:
        try:
            updated = collect(profile_id, api_key, today)
            validate(updated, profile_id, today)
            best = updated
        except (OSError, KeyError, TypeError, ValueError) as error:
            print(f"Scholar refresh unavailable ({type(error).__name__})")

    if best != checked_in:
        snapshot_file.write_text(json.dumps(best, indent=2) + "\n", encoding="utf-8")
    print(f"Using Scholar snapshot from {best['asOf']}")


if __name__ == "__main__":
    site = json.loads((ROOT / "content/profile.json").read_text(encoding="utf-8"))["site"]
    today = datetime.now(ZoneInfo("Asia/Hong_Kong")).date()
    refresh(ROOT / "content/scholar.json", urljoin(site, "scholar.json"),
            os.environ.get("SERPAPI_KEY"), today)
