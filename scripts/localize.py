"""Traditional Chinese localization for the generated HTML."""

from html.parser import HTMLParser
import re

from opencc import OpenCC


LANGUAGES = {
    "en": ("English", "index.html", "publications.html", "cv.html"),
    "zh-CN": ("简体中文", "zh.html", "publications-zh.html", "cv-zh.html"),
    "zh-Hant": ("繁體中文", "zh-hant.html", "publications-zh-hant.html", "cv-zh-hant.html"),
}

converter = OpenCC("s2hk.json")
translated_attributes = re.compile(
    r'\b(alt|aria-label|title|placeholder|data-caption|data-desc|data-template|content)="([^"]*)"'
)
wording = {
    "搜索": "搜尋",
    "學術簡歷": "學術履歷",
    "跳到正文": "跳至正文",
    "郵件聯繫我": "電郵聯絡我",
    "給我發郵件": "電郵聯絡我",
    "回到頂部": "返回頁首",
    "打開原圖出處": "查看原圖出處",
}


def traditional(text):
    text = converter.convert(text)
    for source, target in wording.items():
        text = text.replace(source, target)
    return text


class TraditionalHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts = []
        self.language_label = False

    def handle_starttag(self, tag, attrs):
        if tag == "a" and "data-language-option" in dict(attrs):
            self.language_label = True
        self.parts.append(translated_attributes.sub(
            lambda match: f'{match[1]}="{traditional(match[2])}"', self.get_starttag_text()
        ))

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag == "a":
            self.language_label = False
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data if self.language_label else traditional(data))

    def handle_entityref(self, name):
        self.parts.append(f"&{name};")

    def handle_charref(self, name):
        self.parts.append(f"&#{name};")

    def handle_decl(self, decl):
        self.parts.append(f"<!{decl}>")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")


def localize(html):
    parser = TraditionalHTML()
    parser.feed(html)
    parser.close()
    return "".join(parser.parts)
