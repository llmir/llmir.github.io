from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse, json
from hashlib import sha256
from localize import LANGUAGES

root = Path(__file__).resolve().parents[1]
site = root / "site"
cli = argparse.ArgumentParser()
cli.add_argument("--production", action="store_true")
prod = cli.parse_args().production
pages = {path: language for language, (_, *paths) in LANGUAGES.items() for path in paths}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.urls = set(), []
        self.duplicates = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            if d["id"] in self.ids:
                self.duplicates.append(d["id"])
            self.ids.add(d["id"])
        self.urls.extend((d[k], tag) for k in ("src", "href", "data-source") if d.get(k))
    handle_startendtag = handle_starttag

parsers = {}
for name, language in pages.items():
    t = (site / name).read_text()
    assert f'<html lang="{language}">' in t, name
    assert t.count('data-language-option') == len(LANGUAGES), name
    l = Links()
    l.feed(t)
    assert not l.duplicates, (name, l.duplicates)
    assert "rsi-research" not in t
    assert not any(w in t for w in ("0.9384", "linlimir@gmail.com", "Active AutoResearch application filed"))
    assert "MOST CITED PAPER" not in t and "引用最高的论文" not in t
    assert "Selected Publications" not in t
    if prod:
        assert 'name="robots" content="noindex' not in t
    parsers[name] = l

for name, p in parsers.items():
    for url, tag in p.urls:
        dest = urlsplit(url)
        if dest.scheme:
            assert dest.scheme in ("https", "mailto"), (name, url)
            continue
        assert not dest.netloc, (name, url)
        path = unquote(dest.path) or name
        f = (site / path).resolve()
        assert site in (f, *f.parents), (name, url)
        assert f.is_file(), (name, url, tag)
        if dest.fragment and f.name in parsers:
            assert unquote(dest.fragment) in parsers[f.name].ids, (name, url)

data = json.loads((root / "content/publications.json").read_text())
figs = json.loads((root / "content/figures.json").read_text())
patents = json.loads((root / "content/patents.json").read_text())
assert len({r["id"] for r in data}) == len(data)
assert len({r["id"] for r in figs}) == len(figs)
assert set(r["id"] for r in figs) <= set(r["id"] for r in data)
for row in data:
    first = row["authors"].replace("，", ",").split(",", 1)[0].strip(" *†")
    assert (first in {"Li Lin", "L Lin", "林立"}) == (row.get("role") == "First author"), row["id"]
    assert bool(row.get("correspondence")) == bool(row.get("correspondenceZh")), row["id"]
    assert row.get("desc") and row.get("zh"), row["id"]
assert len({p["number"][:-1] for p in patents}) == len(patents)
assert all(p["number"].endswith("B" if p["kind"] == "grant" else "A") for p in patents)
editions = {"Published version", "Publisher Early Access", "Official CVF proceedings copy", "Official IEEE conference proceedings copy", "arXiv preprint", "Research Square preprint"}
preprint_editions = {"arXiv preprint", "Research Square preprint"}
assert {r['id'] for r in data if r['status']=='preprint'} == {r['id'] for r in figs if r['edition'] in preprint_editions}
for f in figs:
    assert f["edition"] in editions
    assert (site / f["file"]).is_file()
    assert f["source"].startswith("https://")
    assert f.get("thumbWidth") == 960 and f.get("thumbHeight") == 540
    assert sha256((site / f["file"]).read_bytes()).hexdigest() == f["fileSha256"]
    assert sha256((site / f["thumb"]).read_bytes()).hexdigest() == f["thumbSha256"]
flagged = {f[k] for f in figs for k in ("file","thumb")}
for f in figs:
    if extra := f.get("results"):
        assert extra["id"] == f["id"] and extra["figure"] != f["figure"]
        assert extra["edition"] in editions
        assert extra["source"].startswith("https://")
        assert sha256((site / extra["file"]).read_bytes()).hexdigest() == extra["fileSha256"]
        flagged.add(extra["file"])
        for part in (f, extra):
            assert sha256((site / part["pairThumb"]).read_bytes()).hexdigest() == part["pairThumbSha256"]
            flagged.add(part["pairThumb"])
        first_size, second_size = [part.get("pairSize", [960, 270]) for part in (f, extra)]
        if f.get("pairAxis") == "columns":
            assert first_size[0] + second_size[0] == 960 and first_size[1] == second_size[1] == 540
        else:
            assert first_size[1] + second_size[1] == 540 and first_size[0] == second_size[0] == 960
assert set(p.relative_to(site).as_posix() for p in (site / "assets/papers").iterdir()) == flagged
print(f"Checked {len(parsers)} pages, {len(data)} publication records and {len(figs)} sourced illustrations.")
