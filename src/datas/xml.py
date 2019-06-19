import os
import json

from src.render import env
from src.customize.common import join, getModifyTime, writefile
from src.customize import cprint
from src.settings import BLOG_PATH, VERSION, WEBSITE


def update_rss():
    """生成rss"""
    cprint.normal("Updating feed.xml...", index=1)

    def get_article():
        for each in os.listdir(join(BLOG_PATH, "articles")):
            with open(join(BLOG_PATH, "articles", each, "index.json"), encoding="UTF-8") as file:
                yield json.load(file)

    rss = env.get_template("feed.xml").render({
        "VERSION": VERSION, 
        "WEBSITE": WEBSITE,
        "articles": get_article()
    })
    writefile(join(BLOG_PATH, "feed.xml"), rss, encoding="UTF-8")


def update_sitemap():
    """生成sitemap.xml"""
    cprint.normal('Updating sitemap.xml...', index=1)
    xml_0 = """<?xml version='1.0' encoding='UTF-8'?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n"""
    xml_1 = "</urlset>"
    xml = xml_0
    path = join(BLOG_PATH, "articles")
    for each in os.listdir(path):
        with open(join(path, each, "index.json"), encoding="UTF-8") as file:
            infos = json.load(file)
        if not infos.get("date"):
            continue
        blog_link = f"""    <url>
        <loc>{WEBSITE}/articles/{each}/</loc>
        <lastmod>{getModifyTime(join(path, each, "index.html"))}</lastmod>\n    </url>\n"""
        xml += blog_link
    xml += xml_1
    writefile(join(BLOG_PATH, "sitemap.xml"), xml, encoding="UTF-8")
