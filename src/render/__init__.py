import re
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.settings import DEFAULT_CORPUS, TEMPLATE_PATH
from src.extend import render_extends
from .plugins import All
from .SafeHtml import SafeHTML


def render_info(md: str) -> (dict, str):
    datas = re.match(r'---(?P<datas>[\S\s]+?)---', md).group('datas')

    info = dict()
    # XML风格
    if "<title>" in datas:
        for each in re.findall(r'<(?P<name>\S+?)>([\S\s]*?)</\1>', datas):
            info[each[0]] = each[1].strip()

        if not info.get("tags"):
            info["tags"] = []
        else:
            info["tags"] = info["tags"].split(",")

        if info.get("corpus") is None or info["corpus"] == "":
            if info.get("date"):
                info["corpus"] = DEFAULT_CORPUS
    # YAML风格
    else:
        _md = markdown.Markdown(extensions=['markdown.extensions.meta'])
        _md.convert(md)
        info = _md.Meta
        for key, value in info.items():
            if key == "tags":
                continue
            info[key] = value[0]

        if info.get("tags") is None or info["tags"][0] == "":
            info["tags"] = []

        if info.get("corpus") is None or info["corpus"] == "":
            if info.get("date"):
                info["corpus"] = DEFAULT_CORPUS

    if info.get("recommend") is None:
        info["recommend"] = 'false'

    md = re.sub(r"^---[\s\S]+?---", "", md)
    return info, md


env = Environment(
    loader=FileSystemLoader(TEMPLATE_PATH),
    autoescape=select_autoescape(['html', 'xml'])
)


def render_article(md: str, info: dict) -> str:
    extend_source = []

    for each in All.enable():
        md = each(md, info, extend_source)

    blog = markdown.markdown(md, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.tables',
        'markdown.extensions.codehilite',
        'markdown.extensions.nl2br',
    ], extension_configs={
        "markdown.extensions.codehilite": {
            "linenums": False,
        }
    })

    blog = SafeHTML(blog)

    html = env.get_template("article.html").render(**locals())
    return html
