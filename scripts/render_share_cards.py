"""Render the three Open Graph cards with Chrome and the site's cropped portrait."""

import argparse
from base64 import b64encode
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory


SITE = Path(__file__).resolve().parents[1] / "site"
WIDTH, HEIGHT = 1200, 630

CARDS = (
    (
        "en", "en", "Academic homepage", "Li Lin", "林立",
        "Senior AI Engineer · CATL HKRI", "PhD, The University of Hong Kong",
        ("Agentic AI · Recursive Self-Improvement (RSI)",
         "AI for Science · AI for Healthcare · Computer Vision"),
    ),
    (
        "zh", "zh-CN", "学术主页", "林立", "Li Lin",
        "高级 AI 工程师 · 宁德时代香港研究院", "香港大学博士",
        ("智能体 AI · 递归自我改进（RSI）", "科学智能 · 医疗人工智能 · 计算机视觉"),
    ),
    (
        "zh-hant", "zh-Hant", "學術主頁", "林立", "Li Lin",
        "高級 AI 工程師 · 寧德時代香港研究院", "香港大學博士",
        ("智能體 AI · 遞歸自我改進（RSI）", "科學智能 · 醫療人工智能 · 計算機視覺"),
    ),
)

STYLE = """
    * { box-sizing: border-box; }
    html, body { width: 1200px; height: 630px; margin: 0; }
    body {
      font-family: 'Apple SD Gothic Neo', 'PingFang SC', 'PingFang TC',
        'Noto Sans CJK SC', sans-serif;
      color: #111827;
      background: #f9fafb;
    }
    :lang(zh-Hant) { font-family: 'PingFang TC', 'Noto Sans CJK TC', sans-serif; }
    main { position: relative; height: 100%; border-top: 8px solid #24558c; }
    section { position: absolute; left: 76px; top: 95px; width: 665px; }
    h1, p { margin: 0; }
    .kicker { font-size: 24px; font-weight: 700; letter-spacing: .14em; color: #315f8b; }
    :lang(en) .kicker { text-transform: uppercase; }
    header { display: flex; align-items: baseline; gap: 23px; margin: 11px 0 17px; }
    h1 { font-size: 94px; line-height: 1.11; font-weight: 750; }
    .alternate { font-size: 38px; font-weight: 600; color: #626d7f; white-space: nowrap; }
    .role { font-size: 31px; font-weight: 650; line-height: 1.4; }
    .degree { margin-top: 1px; font-size: 27px; color: #43536a; }
    .interests {
      padding-top: 23px; margin-top: 27px; border-top: 1px solid #d8e2ed;
      font-size: 25px; font-weight: 650; line-height: 1.55; color: #315f8b;
    }
    .portrait { position: absolute; left: 792px; top: 107px; }
    img { display: block; width: 330px; height: auto; border: 1px solid #d8e2ed; border-radius: 10px; }
    .address { position: absolute; bottom: 42px; left: 76px; font-size: 26px; color: #43536a; font-weight: 650; }
"""


def render_html(card, portrait):
    _, language, heading, name, alternate, role, degree, interests = card
    alternate_language = "zh-CN" if language == "en" else "en"
    return f"""<!doctype html>
<html lang="{language}">
<meta charset="utf-8">
<title>{name} · {heading}</title>
<style>{STYLE}</style>
<main>
  <section>
    <p class="kicker">{heading}</p>
    <header><h1>{name}</h1><p class="alternate" lang="{alternate_language}">{alternate}</p></header>
    <p class="role">{role}</p>
    <p class="degree">{degree}</p>
    <div class="interests">{"".join(f"<p>{line}</p>" for line in interests)}</div>
  </section>
  <div class="portrait"><img width="408" height="491" alt="{name}" src="data:image/webp;base64,{portrait}"></div>
  <p class="address">llmir.github.io</p>
</main>
</html>
"""


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    mac_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    chrome = str(mac_chrome) if mac_chrome.is_file() else shutil.which("chromium") or shutil.which("google-chrome")
    cli.add_argument("--chrome", default=chrome, help="Chrome or Chromium executable")
    args = cli.parse_args()
    if not args.chrome:
        cli.error("Specify a Chrome or Chromium executable with --chrome.")

    portrait = b64encode((SITE / "assets/li-lin.webp").read_bytes()).decode("ascii")
    destination = SITE / "assets/social"
    destination.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as workspace:
        source = Path(workspace) / "card.html"
        for card in CARDS:
            source.write_text(render_html(card, portrait), encoding="utf-8")
            output = destination / f"share-{card[0]}.png"
            subprocess.run([
                args.chrome, "--headless", "--hide-scrollbars", "--force-device-scale-factor=1",
                f"--window-size={WIDTH},{HEIGHT}", f"--user-data-dir={workspace}/browser",
                f"--screenshot={output}", source.as_uri(),
            ], check=True, capture_output=True)
            print(output.relative_to(SITE), output.stat().st_size)


if __name__ == "__main__":
    main()
