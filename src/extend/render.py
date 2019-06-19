import re

from src.settings import AUTHOR
from src.customize import cprint


def insert_element(page: str, element: str, extend: str, head: bool = False, inside: bool = True) -> str:
    """在element插入一段字符串, 默认为元素内尾部

    head 决定头部或尾部

    inside 决定元素内还是外
    """
    if inside:
        if not head:
            page = re.sub(f"</{element}>", f'{extend}\n</{element}>', page)
        else:
            page = re.sub(f"<{element}>", f'<{element}>\n{extend}', page)
    else:
        if not head:
            page = re.sub(f"</{element}>", f'</{element}>\n{extend}', page)
        else:
            page = re.sub(f"<{element}>", f'{extend}\n<{element}>', page)
    return page


def render_extends(page: str, info: dict) -> str:
    """改变最终渲染结果"""
    # 增加最后修改时间,作者信息等
    cprint.green("标题下额外信息", index=2)
    last_mod = f'<div id="detail">\
        <span>\
            <a href="/">首页</a>\
        </span>\
        &#124; \
        <span>最后更新时间: {info["update"]}</span>\
        &#124; \
        <span>作者: <a href="/about/">{AUTHOR}</a></span>\
        &#124; \
        <span><a href="/about/donation.html" target="_blank">捐助</a></span>\
    </div>'
    page = insert_element(page, "h1", last_mod, inside=False)
    # 查找是否有参考链接，如果有，则调换其与标签等的位置
    if '<div class="reference-link">' in page:
        cprint.green("调转参考链接与文集等位置", index=2)
        page = re.sub(r'(<div class="reference-link">[\s\S]*?</div>)([\s\S]*?)(<div id="extend">[\s\S]*?</div>)(\s*?</main>)',
                      r'\g<3>\g<2>\g<1>\g<4>',
                      page
                      )
    return page
