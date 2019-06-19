import re

from src.settings import PLUGINS
from .SafeHtml import SafeHTML


class All:
    @staticmethod
    def enable() -> list:
        if PLUGINS is None:
            for method in filter(lambda x: True if not x.startswith("__") and x not in ("enable",) else False, dir(All)):
                yield getattr(All, method)
        else:
            for method in PLUGINS:
                yield getattr(All, method)

    @staticmethod
    def mermaid(md: str, info: dict, extend_source: list) -> str:
        if "```mermaid" in md:
            extend_source.append(
                SafeHTML('<link rel="stylesheet" href="/STATIC/style/mermaid.7.0.0.min.css">'))
            extend_source.append(
                SafeHTML('<script type="text/javascript" src="/STATIC/script/mermaid.7.0.0.min.js"></script>'))
            result = re.sub(r"```mermaid([\s\S]+?)```",
                            r'<div class="mermaid">\g<1></div>', md)
            return result
        return md

    @staticmethod
    def web_preview(md: str, info: dict, extend_source: list) -> str:
        result = re.sub(r"<web-preview>([\s\S]*?)</web-preview>", r"""\g<1>
```html
\g<1>
```""", md)
        return result

    @staticmethod
    def reference_link(md: str, info: dict, extend_source: list) -> str:
        """
        渲染参考链接。

        考虑到参考链接一般不分先后，所以任意列表都会渲染成无序列表
        """
        try:
            refs = re.search(
                r"<reference-link>([\s\S]*?)</reference-link>", md).group(0)
        except AttributeError:
            return md
        refs_link_html = ""
        for link in re.findall(r"(\d+\.|\-|\*) \[([\s\S]+?)\]\(([\s\S]+?)\)", refs):
            refs_link_html += f'    <li><a href="{link[2]}">{link[1]}</a></li>\r\n'
        refs_link_html = f"""<div class="reference-link">
    <p>参考链接</p>
    <ul>
    {refs_link_html}  </ul>
    </div>"""
        result = re.sub(
            r"<reference-link>([\s\S]*?)</reference-link>", refs_link_html, md)
        return result
