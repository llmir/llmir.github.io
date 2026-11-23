# Li Lin Academic Homepage

A three-language academic homepage and chronological publication index for GitHub Pages.

- Homepages: `site/index.html`, `site/zh.html` (简体), and `site/zh-hant.html` (繁體).
- The publication index and public academic CV use the same language choices. The CV includes the research timeline, doctoral methods, patents, publication years, and open research.
- 论文目录按年份归档，支持搜索；近期论文和完整目录使用同一份数据。
- 正式论文的缩略图来自出版方或官方会议论文集。预印本使用相应版本的原文图。图号、版次、来源和许可信息见 `content/figures.json`。待配图的条目保留简介和原文链接。

## Source and reuse

The original site generator, layout code, CSS, JavaScript, and deployment workflows are available under the [MIT License](LICENSE). Publication figures follow the terms of the sources in [`content/figures.json`](content/figures.json). The [font license](site/assets/fonts/OFL-Noto-Sans-KR.txt) and the basemap attribution are listed separately. Use your own photograph, contact details, QR code, and scholarly records when adapting the site.

For a new site, use the [Academic Homepage Template](https://github.com/llmir/academic-homepage-template) and edit the sample records in `content/`. The homepage, publication index, and CV build in all three languages from those records.

Institutional marks are sourced from [CATL](https://www.catl.com/en/), [HKU](https://www.hku.hk/en/about-hku/university-identity/basic-specifications), [SUSTech](https://www.sustech.edu.cn/zh/school_logo.html), [Sun Yat-sen University](https://www.sysu.edu.cn/xxg/zdjj1.htm), and [South China Normal University](https://www.scnu.edu.cn/a/20150906/2.html).

## Preview

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build.py --preview
python3 scripts/check.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8000/`. The preview build disables visitor tracking.

## Publish on GitHub Pages

1. Check the reuse terms for figures before public deployment. The review bundle includes publisher figure assets and their attribution in `content/figures.json`.
2. Put the source in the root of your Pages repository and use its `main` branch. A personal site on GitHub Pages uses the repository name `<username>.github.io`.
3. In the repository, select **Settings → Pages → Source → GitHub Actions**. Then run **Deploy academic homepage** on the Actions tab or push an update to `main`. Only the `site/` directory is published.

See [GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Visitor map and traffic

[MapMyVisitors](https://mapmyvisitors.com/add) provides the flat red-dot world map and a pageview count. Create your own widget for the actual public GitHub Pages URL, then fill in `content/profile.json`:

```json
"visitors": {
  "key": "<value of d in your own widget embed URL>",
  "statsId": "<your identifier in the mapmyvisitors.com/web/… URL>"
}
```

Use the two public identifiers from the widget embed. Each page requests the widget once. On the homepages, the map links to MapMyVisitors and the three counts show the total, today, and the previous seven complete days. GitHub Actions schedules a refresh every 15 minutes and publishes the latest valid counts in `visitor-stats.json`. An open homepage checks for a newer snapshot every five minutes while visible and when the tab becomes active. The map updates separately through the live widget. [MapMyVisitors HTML setup](https://mapmyvisitors.com/learn/tools/add-visitor-map-html/).

After deployment, open the site on its public hostname and check the statistics page for a test visit. If the image fails to load, the homepage shows the basemap and keeps the statistics link available. The provider estimates locations from visitor IP addresses and describes its data handling in its [privacy policy](https://mapmyvisitors.com/b/policy).

When `visitors` is `null` or the site is built with `--preview`, the homepage shows a static world map sourced from [Natural Earth](https://www.naturalearthdata.com/about/terms-of-use/).

## Maintain content

- `content/profile.json`: contact and academic profile links.
- `content/publications.json`: citation metadata for 65 published papers and 4 preprints. The duplicate MEFN preprint is linked from the published entry. `content/publication-dates.json` records publication dates with sources. `content/selected-publications.json` lists the papers in the homepage's default view.
- `content/scholar.json` stores Google Scholar metrics and annual citations. With the repository Actions secret `SERPAPI_KEY` configured, collection is scheduled at 08:18 and 18:18 Shanghai time. Builds reuse the newest valid snapshot and skip another API call if the current scheduled interval already has a SerpApi result. The card shows the schedule date and time for the latest published snapshot and checks for newer snapshots while the page is open. To refresh manually from a network that can reach the author profile, install `beautifulsoup4==4.15.0` and `Protego==0.7.0` and run `python scripts/refresh_scholar_stats.py --public-profile`. The manual route checks Google's crawl rules and reads a complete first page. The Scholar record count includes duplicate versions, while the website lists its reconciled bibliography. [Google Scholar crawl rules](https://scholar.google.com/robots.txt) · [SerpApi author API](https://serpapi.com/google-scholar-author-api).
- `content/patents.json`: co-inventor entries indexed once per application or patent family, with grant numbers for verified granted records. Titles describe the technical subject. The records give the official legal titles.
- `content/figures.json` records the source, edition, figure number, image hashes, and available licensing information. Cards have a common 16:9 frame. When a method diagram is unusually narrow or wide, a nearby result panel can share the frame. Each panel opens its full source image.
- `content/venue-metrics.json` records the metric, data year, and source for each displayed JIF and conference grade.
- `assets/fonts/OFL-Noto-Sans-KR.txt` in the site directory gives the license of the Latin fallback font. Apple SD Gothic Neo is used on systems that have it installed.
