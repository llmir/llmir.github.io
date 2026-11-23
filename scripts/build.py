"""Build both languages and the full chronological publication index."""
from pathlib import Path
from html import escape
from itertools import groupby
import argparse,json,re

import academic_cv
import homepage
from localize import LANGUAGES, localize
from refresh_scholar_stats import SCHEDULED_REFRESH_TIMES

ROOT=Path(__file__).resolve().parents[1]
CONTENT,SITE=ROOT/'content',ROOT/'site'
cli=argparse.ArgumentParser()
cli.add_argument('--preview',action='store_true',help='write local noindex preview; keep analytics off')
cli.add_argument('--visitor-stats',type=Path,default=CONTENT/'visitor-stats.json',help='read a MapMyVisitors aggregate snapshot')
args=cli.parse_args()

def load(name):
    return json.loads((CONTENT/(name+'.json')).read_text(encoding='utf8'))

p,s,papers=(load(n) for n in ('profile','scholar','publications'))
figures={d['id']:d for d in load('figures')}
publication_dates=load('publication-dates')
representatives=set(load('selected-publications'))
if not representatives <= {paper['id'] for paper in papers}:
    raise ValueError('Selected publications must be present in the publication catalog')

def publication_date(paper):
    date = publication_dates.get(paper['id'], {}).get('date', [paper['year']])
    return tuple((date + [0, 0])[:3])

papers.sort(key=publication_date, reverse=True)

def visitor_links():
    config = p.get('visitors')
    if args.preview or config is None:
        return None
    key, stats_id = config.get('key', ''), config.get('statsId', '')
    if not (re.fullmatch(r'[a-zA-Z0-9_-]{15,120}', key)
            and re.fullmatch(r'[a-zA-Z0-9]{3,24}', stats_id)):
        raise ValueError('Supply your MapMyVisitors widget key and statistics ID.')
    return (f'https://mapmyvisitors.com/map.png?d={key}&cl=ffffff',
            f'https://mapmyvisitors.com/web/{stats_id}')

visitors = visitor_links()
visitor_totals = {}
if visitors and args.visitor_stats.is_file():
    snapshot = json.loads(args.visitor_stats.read_text(encoding='utf8'))
    if snapshot.get('statsId') == p['visitors']['statsId']:
        visitor_totals = snapshot
visitor_privacy = 'https://mapmyvisitors.com/b/policy'
date=s['asOf']
year=int(date[:4])
dblp='https://dblp.org/pid/38/4000-6.html'
catl='https://www.catl.com/en/news/6308.html'
catl_zh='https://www.catl.com/news/8099.html'
thesis='https://hub.hku.hk/handle/10722/370810'
review_venues=load('review-venues')
venue_metrics=load('venue-metrics')

def e(x):
    return escape(str(x),quote=True)

def a(u,label='',cls=''):
    return f'<a href="{e(u)}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{e(label or u)}</a>'

def venue_metric(name):
    metric = venue_metrics.get(name)
    if not metric:
        return ''
    label, metric_year, url, *notes = metric
    title = notes[0] if notes else f'{label} · {metric_year}'
    return f' <a class="venue-metric" href="{e(url)}" title="{e(title)}">({e(label)})</a>'

def author_line(paper, zh):
    people=[]
    authors = paper.get('authorsZh', paper['authors']) if zh else paper['authors']
    for name in authors.replace('，',',').split(','):
        name=name.strip()
        person=name.rstrip(' *†')
        owner=person in {'Li Lin','L Lin','林立'}
        joint=person in paper.get('equalAuthors',[]) or '*' in name or owner and paper.get('role')=='Joint first author'
        correspond=person in paper.get('correspondingAuthors',[]) or '†' in name or owner and paper.get('correspondence')
        marks=[]
        if joint:
            label='共同第一作者' if zh else 'Co-first author'
            marks.append(f'<sup class="author-mark joint" aria-label="{label}">*</sup>')
        if correspond:
            label='通讯作者' if zh else 'Corresponding author'
            marks.append(f'<sup class="author-mark correspondence" aria-label="{label}">†</sup>')
        text=f'<strong>{e(person)}</strong>' if owner else e(person)
        people.append(f'<span class="author-name">{text}{"".join(marks)}</span>')
    return ', '.join(people)

def author_credit(paper, zh):
    role=paper.get('roleZh' if zh else 'role')
    correspondence=paper.get('correspondenceZh' if zh else 'correspondence')
    if role == 'Joint first author':
        role = 'Co-first author'
    role_style = {'First author':'first','First student author':'student-first'}.get(paper.get('role'),'joint')
    labels=[(role_style,role),('correspondence',correspondence)]
    return ''.join(f' <span class="contrib {css}">{e(label)}</span>' for css,label in labels if label)

def sharing_metadata(language, canonical, description):
    card_locales = {'en': ('en_US', 'en'), 'zh-CN': ('zh_CN', 'zh'), 'zh-Hant': ('zh_HK', 'zh-hant')}
    locale, suffix = card_locales[language]
    name = p['name'] if language == 'en' else '林立'
    title = f"{name} · {'Academic Homepage' if language == 'en' else '学术主页'}"
    image = f'{p["site"]}assets/social/share-{suffix}.png'
    alt = ('Li Lin’s portrait, CATL HKRI role, University of Hong Kong PhD, and AI research areas.'
           if language == 'en' else '林立的肖像、宁德时代香港研究院职务、香港大学博士学历及人工智能研究方向。')
    open_graph = {
        'type': 'website', 'title': title, 'description': description, 'url': canonical,
        'site_name': name, 'image': image, 'image:width': 1200, 'image:height': 630,
        'image:alt': alt, 'locale': locale,
    }
    twitter = {
        'card': 'summary_large_image', 'title': title, 'description': description,
        'image': image, 'image:alt': alt,
    }
    tags = [f'<meta property="og:{key}" content="{e(value)}">' for key, value in open_graph.items()]
    tags.extend(f'<meta property="og:locale:alternate" content="{other_locale}">'
                for other_locale, _ in card_locales.values() if other_locale != locale)
    tags.extend(f'<meta name="twitter:{key}" content="{e(value)}">' for key, value in twitter.items())
    return '\n'.join(tags)

def header(language,page='home'):
    zh = language != 'en'
    L=lambda x,y:y if zh else x
    _, home, _, cv = LANGUAGES[language]
    column = {'home':1,'archive':2,'cv':3}[page]
    page_urls = {code: routes[column] for code, routes in LANGUAGES.items()}
    canonical = p['site'] + page_urls[language].removeprefix('index.html')
    alternate = '\n'.join(
        f'<link rel="alternate" hreflang="{code}" href="{e(p["site"] + file.removeprefix("index.html"))}">'
        for code, file in page_urls.items()
    )
    language_links = []
    for code, (name, *_) in LANGUAGES.items():
        selected = ' aria-current="true"' if code == language else ''
        language_links.append(f'<li><a data-language-option href="{page_urls[code]}" hreflang="{code}" lang="{code}"{selected}>{name}</a></li>')
    language_menu = '\n'.join(language_links)
    index='' if page=='home' else home
    ttl=L('Li Lin','林立 Li Lin')+{'home':'','archive':' · '+L('Publications','论文目录'),'cv':' · '+L('Academic CV','学术简历')}[page]
    description = L(
        'Li Lin — AI for Science, Agentic AI, and AI for Healthcare. Research and publications in medical image analysis, data-efficient learning, and federated learning.',
        '林立的学术主页：AI for Science、Agentic AI 与 AI for Healthcare；医学影像分析、数据与标注高效学习、泛化与联邦学习。',
    )
    sharing = '\n' + sharing_metadata(language, canonical, description) if page == 'home' else ''
    style_version = {'home': '?v=scholar-timing', 'cv': '?v=cv-resources'}.get(page, '')
    return f'''<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(description)}">
<meta name="referrer" content="strict-origin-when-cross-origin">
{'<meta name="robots" content="noindex,nofollow">' if args.preview else ''}
<link rel="canonical" href="{e(canonical)}">
{alternate}
<title>{ttl}</title>{sharing}
<link rel="stylesheet" href="assets/style.css{style_version}">
<link rel="stylesheet" href="assets/publication-design.css">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<script src="assets/site.js?v=scholar-refresh" defer></script>
</head>
<body id="Home"{' class="cv-document"' if page=='cv' else ''}>
<a class="skip" href="#main">{L('Skip to content','跳到正文')}</a>
<header class="site-header"><div class="container header-inner">
{a(home,L('Li Lin','林立'))}
<nav aria-label="{L('Primary navigation','主导航')}">
{a(index+'#Biography',L('Biography','个人简介'))}
{a(index+'#News',L('News','动态'))}
{a(index+'#Experience',L('Experience','经历'))}
{a(index+'#Publications',L('Publications','论文'))}
{a(index+'#Service',L('Service','学术服务'))}
<a href="{cv}"{(' aria-current="page"') if page=='cv' else ''}>{L('CV','简历')}</a>
</nav>
<details class="language-switcher">
<summary aria-label="{L('Switch language','切换语言')}">
<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>
{L('Language','语言')}<span class="language-chevron" aria-hidden="true"></span>
</summary>
<ul aria-label="{L('Available languages','可用语言')}">
{language_menu}
</ul></details></div></header>'''

def footer(zh, track_visit=False):
    L=lambda x,y:y if zh else x
    source = f' · {a(p["sourceCode"], L("Site source", "网站源码"))}' if p.get('sourceCode') else ''
    pixel = ''
    if visitors and track_visit:
        pixel = (f'<img src="{e(visitors[0])}" alt="" width="1" height="1"'
                 ' loading="eager" fetchpriority="low" hidden>')
        privacy = a(visitor_privacy, L('Visitor privacy','访客隐私'))
        pixel += f'<p>{privacy}</p>'
    return f'''<footer class="container footer">
<p>© {year} {L('Li Lin','林立')} · <a href="#Home">{L('Back to top','回到顶部')} ↑</a>{source}</p>
{pixel}
</footer>
<dialog id="figure" aria-labelledby="fig-title">
<div class="dialog-bar"><h2 id="fig-title"></h2><button type="button" data-close autofocus>{L('Close','关闭')} <span aria-hidden="true">×</span></button></div>
<div class="fig-scroll"><img alt=""></div>
<div class="dialog-meta"><p data-fig-desc></p><a data-fig-source href="{e(p['scholar'])}">{L('Open figure source','打开原图出处')} ↗</a></div>
</dialog></body></html>'''

def paper_figure(figure, zh):
    L=lambda en,cn:cn if zh else en
    parts=[figure, *figure.get('additionalFigures', [])]
    if figure.get('results'):
        parts.append(figure['results'])
    orientation = figure.get('pairAxis', 'rows') if len(parts) > 1 else None
    layout = f' paired paired-{orientation}' if orientation else ''
    split = f' style="--pair-first:{int(figure["pairSplit"])}%"' if figure.get('pairSplit') else ''
    anchors=[]
    sources=[]
    for i,f in enumerate(parts):
        number=f['figure']
        edition=L(f['edition'],{
            'Publisher Early Access':'出版方在线优先版',
            'Official CVF proceedings copy':'CVF 官方论文集开放版',
            'Official IEEE conference proceedings copy':'IEEE 官方论文集版',
            'Published version':'正式发表版',
            'arXiv preprint':'arXiv 预印本',
            'Research Square preprint':'Research Square 预印本',
        }[f['edition']])
        desc=L(f'Fig. {number}',f'图 {number}')
        if f.get('page'):
            desc+=' · '+L(f"PDF p. {f['page']}",f"PDF 第 {f['page']} 页")
        desc+=' · '+edition
        if len(parts)>1:
            default_role = L('Method','方法') if i == 0 else L('Results','结果')
            role = f.get(L('panelType', 'panelTypeZh'), default_role)
            desc+=' · '+role
            img=f['pairThumb']
            w,h=f.get('pairSize', [960,270])
        else:
            img,w,h=f['thumb'],f['thumbWidth'],f['thumbHeight']
        label=e(f.get(L('label','labelZh'), f['label']))
        marker = (f'<span class="figure-number" aria-hidden="true">{number}</span>' if orientation == 'grid'
                  else '<span class="zoom" aria-hidden="true">+</span>')
        anchors.append(f'''<a class="pub-figure-link" data-figure href="{e(f['file'])}" data-source="{e(f['source'])}"
data-desc="{e(desc)}" data-caption="{label}" aria-label="{L('Enlarge figure','放大论文图')} {number} · {label}">
<img src="{e(img)}" alt="{label}" width="{w}" height="{h}" loading="lazy" decoding="async">{marker}</a>''')
        link_text=L(f'Fig. {number}',f'图 {number}') if len(parts)>1 else L('Source','原文出处')
        sources.append(a(f['source'],link_text))
    if len(parts)==1:
        sources.insert(0,L(f"Fig. {figure['figure']}",f"图 {figure['figure']}"))
    if figure.get('licenseUrl'):
        sources.append(a(figure['licenseUrl'],figure['license']))
    return f'''<figure class="pub-figure"><div class="pub-figure-area{layout}"{split}>{''.join(anchors)}</div>
<figcaption>{' · '.join(sources)}</figcaption></figure>'''

def row(paper,zh,selected=None):
    L=lambda x,y:y if zh else x
    f=figures.get(paper['id'])
    figure=paper_figure(f,zh) if f else ''
    status=paper['status']
    label=L('Paper','论文')
    keywords=' · '.join(paper[L('keywords','keywordsZh')])
    title=paper[L('title','titleZh')]
    source_title=f' data-original-title="{e(paper["title"])}"' if zh and title != paper['title'] else ''
    if paper['linkType']=='scholar':
        label=L('Scholar record','Scholar 记录')
    if paper['linkType']=='preprint':
        label=paper.get('preprintLabel','arXiv')
    tag=(f'<span class="status">{L("Preprint","预印本")}</span>' if status=='preprint' else
         f'<span class="status">{L("Venue unconfirmed","发表信息待核")}</span>' if status=='unconfirmed' else '')
    reading=' '.join(a(paper[k],L(x,y),'pub-link') for k,x,y in [('preprint','arXiv','arXiv'),('code','Code','代码'),('data','Data','数据')] if paper.get(k))
    dv=paper.get('zh' if zh else 'desc')
    venue=e(paper.get(L('venue','venueZh'), paper['venue']))
    has_year=re.search(r'\b(?:19|20)\d{2}\b', venue)
    yr='' if not venue or paper['linkType']=='scholar' or has_year else f' {paper["year"]}'
    award=paper.get(L('award','awardZh'))
    award_tag=f'<span class="status">{e(award)}</span>' if award else ''
    selection = '' if selected is None else (' data-representative' if selected else ' hidden')
    return f'''<article class="pub-row{" with-figure" if f else ""}" id="{paper['id']}" data-year="{paper['year']}" data-status="{status}"{source_title}{selection}>
{figure}<div class="pub-text">
<p class="pub-keywords">{e(keywords)}</p>
<h3>{a(paper['url'],title)}</h3>
<p class="pub-authors">{author_line(paper,zh)}{author_credit(paper,zh)}</p>
{f'<p class="pub-desc">{e(dv)}</p>' if dv else ''}
<div class="pub-meta"><span class="pub-venue">{venue}{yr}{venue_metric(paper['venue'])}</span>{tag}{award_tag}{a(paper['url'],label,'pub-link')}{reading}</div>
</div></article>'''

def rows(records,zh,selection=None):
    sections = []
    for year, group in groupby(records, key=lambda paper: paper['year']):
        members = list(group)
        hidden = ' hidden' if selection is not None and all(paper['id'] not in selection for paper in members) else ''
        cards = ''.join(row(paper, zh, None if selection is None else paper['id'] in selection) for paper in members)
        sections.append(f'<section class="pub-group" aria-label="{year}"{hidden}><h3 class="pub-year">{year}</h3>{cards}</section>')
    return ''.join(sections)

def stats(zh):
    L=lambda x,y:y if zh else x
    basemap=f'<img src="assets/visitor-world.svg" width="804" height="367" alt="{L("World map","世界地图")}">'
    fallback=f'<div class="visitor-off" data-visitor-fallback{" hidden" if visitors else ""}>{basemap}</div>'
    totals = visitor_totals if visitors else {}
    view_metrics = (
        ('total', L('Total views', '累计浏览量')),
        ('today', L('Today', '今日浏览量')),
        ('last7', L('Prior 7 days', '前 7 天')),
    )
    metric_date = totals.get('asOf', '')
    updated_label = L('Updated from MapMyVisitors', '更新自 MapMyVisitors')
    as_of = f' title="{e(updated_label + " · " + metric_date)}"' if metric_date else ''
    stats_data = (
        f' data-visitor-stats="{e(p["visitors"]["statsId"])}" data-visitor-as-of="{e(metric_date)}"'
        f' data-visitor-updated-label="{e(updated_label)}"' if visitors else ''
    )
    metrics = f'<dl class="visitor-metrics"{as_of}{stats_data}>' + ''.join(
        f'<div><dt>{label}</dt><dd><strong data-visitor-value="{key}">'
        f'{f"{totals[key]:,}" if key in totals else "—"}</strong></dd></div>'
        for key, label in view_metrics
    ) + '</dl>'
    if visitors:
        map_url,detail=visitors
        mapbody=f'''<a class="visitor-image" data-visitor-widget href="{detail}" aria-label="{L('Open visitor statistics on MapMyVisitors','在 MapMyVisitors 查看访客统计')}"><img src="{e(map_url + '&w=420')}" width="420" height="229" loading="eager" fetchpriority="low" alt="{L('Red-dot visitor world map and pageview count','红点访客世界地图及页面浏览量')}"></a>
{fallback}<p class="map-status" data-visitor-unavailable hidden>{L('Visitor map unavailable','访客地图暂不可用')}</p>
{metrics}'''
    else:
        mapbody=f'{fallback}{metrics}'
    entries=s['yearly']; xmax=max(100,100*((max(v for _,v in entries)+99)//100))
    bar=''.join(f'<div><span>{v}</span><div class="chart-well"><i class="{"partial" if y==s["partialYear"] else ""}" style="height:{100*v/xmax:.2f}%"></i></div><span>{y}</span></div>' for y,v in entries)
    accessible=', '.join(f'{y}: {v}' for y,v in entries)
    statrow=''.join(f'<div><strong data-scholar-value="{key}">{s[key]}</strong><span>{label}</span></div>' for key,label in [('hIndex',L('h-index','h 指数')),('i10Index',L('i10-index','i10 指数')),('indexedRecords',L('Scholar records','收录条目'))])
    collected = s.get('collectedAt') or date
    collected_label = collected[:16].replace('T', ' ')
    refresh_times = ' / '.join(at.strftime('%H:%M') for at in SCHEDULED_REFRESH_TIMES)
    schedule_label = L('Scheduled daily (UTC+8)', '每日计划刷新（北京时间）')
    collected_caption = L('Last collected', '最近采集')
    return f'''<aside class="stats-section" id="Contact" aria-label="{L('Citation and visitor statistics','引用与访客统计')}">
<div class="footer-widgets">
<section class="scholar-card" aria-labelledby="sch-title" data-scholar-profile="{e(s['profileId'])}">
<div class="scholar-top"><span id="sch-title">{a(p['scholar'],'Google Scholar')}</span></div>
<div class="scholar-timing">
<div>{schedule_label} <span>{refresh_times}</span></div>
<div>{collected_caption} <time datetime="{e(collected)}">{e(collected_label)}</time></div>
</div>
<div class="scholar-total"><strong data-scholar-value="citations">{s['citations']:,}</strong><span>{L('TOTAL CITATIONS','总被引次数')}</span></div>
<div class="scholar-metrics">{statrow}</div>
<div class="scholar-chart"><p>{L('Citations by year','年度引用')}</p><div class="chart-bars" role="img" aria-label="{e(accessible)}">{bar}</div></div>
</section>
<section class="visitor-card visitors" aria-label="{L('Visitor Map','访客地图')}">{mapbody}</section>
</div></aside>'''

def home(language):
    zh = language != 'en'
    L=lambda x,y:y if zh else x
    _, _, idx, cv_url = LANGUAGES[language]
    institution=catl_zh if zh else catl
    return header(language)+f'''<main id="main">
{homepage.intro(zh,p,cv_url)}
{homepage.biography(zh,thesis,p,stats(zh))}
{homepage.news(zh,institution,thesis,cv_url,papers)}
{homepage.experience(zh,cv_url)}
<section class="container section publications" aria-labelledby="Publications">
<div class="section-title"><h2 id="Publications">{L('Publications','学术论文')}</h2>
<div class="publication-controls">
<div class="publication-view" data-publication-view role="group" aria-label="{L('Publication view','论文展示方式')}" hidden>
<button type="button" data-publication-mode="selected" aria-pressed="true">{L('Selected','代表作')} <span class="view-count">{len(representatives)}</span></button>
<button type="button" data-publication-mode="all" aria-pressed="false">{L('All','全部论文')} <span class="view-count">{len(papers)}</span></button>
</div>
{a(idx+'#filters',L('Search publications','检索论文'),'publication-search')}
</div></div>
{rows(papers,zh,representatives)}</section>
{homepage.peer_review(zh,review_venues,venue_metric,venue_metrics)}
</main>{homepage.wechat_dialog(zh,p)}{footer(zh)}'''

def archive(language):
    zh = language != 'en'
    L=lambda x,y:y if zh else x
    return header(language,'archive')+f'''<main id="main" class="container archive">
<div class="section-title"><h1>{L('Publication Index','完整论文目录')}</h1><div>{a(p['scholar'],'Google Scholar')} <span>·</span> {a(dblp,'DBLP')}</div></div>
<p class="section-note">{L('Journal articles, conference papers and preprints, organized by year. Venue metrics link to their sources.','按年份收录期刊论文、会议论文和预印本。期刊影响因子和会议评级均链接至数据来源。')}</p>
<div id="filters" class="filters" hidden>
<label>{L('Search','搜索')}<input type="search" id="find" placeholder="{L('Title, author, venue','题名、作者、期刊或会议')}"></label>
<label>{L('Year','年份')}<select id="year"><option value="">{L('All years','全部年份')}</option>{''.join(f'<option>{y}</option>' for y in sorted({a["year"] for a in papers},reverse=True))}</select></label>
</div>
<p id="count" class="section-note" aria-live="polite" data-template="{L('{n} records','{n} 条记录')}">{len(papers)} {L('records','条记录')}</p>
<div id="pub-index">{rows(papers,zh)}</div>
<p id="empty" hidden>{L('No publications match your search.','没有符合条件的论文。')}</p>
</main>{footer(zh, track_visit=True)}'''

def cv(language):
    return academic_cv.render(language != 'en', p, papers, load('patents'), thesis,
                              header(language, 'cv'), footer, a, e,
                              author_line, author_credit, venue_metric, LANGUAGES[language][2])

if __name__=='__main__':
    for language, (_, *pages) in LANGUAGES.items():
        for name, render in zip(pages, (home, archive, cv), strict=True):
            html = render(language)
            if language == 'zh-Hant':
                html = localize(html)
            (SITE/name).write_text(html+'\n',encoding='utf8')
    (SITE/'scholar.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    visitor_output = SITE/'visitor-stats.json'
    if visitors:
        visitor_output.write_text(json.dumps(visitor_totals, indent=2)+'\n', encoding='utf8')
    else:
        visitor_output.unlink(missing_ok=True)
