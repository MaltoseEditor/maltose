from django.conf import settings
import markdown

default_app_config = 'article.apps.ArticleConfig'


def render(source):
    """
    对source进行markdown渲染处理

    :param source: markdown原始数据
    :return: markdown渲染后的结果
    """
    return markdown.markdown(source, **settings.MARKDOWN)
