import os
import shutil
from urllib import parse

from django.test import Client
from django.conf import settings
from django.urls import reverse

from .models import *

__all__ = [
    'update',
    'delete',
]


def fetch(path) -> str:
    return Client().get(path).content.decode("UTF-8")


def _create(path):
    """
    请求对应的 url 并将结果写入对应文件中
    :param path: 请求的相对路径
    :return: None
    """
    file_path = os.path.join(settings.BLOG_REPOSITORIES, parse.unquote(path).lstrip('/'))
    if path[-1] == "/" or path == "":
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_path += 'index.html'
    else:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

    with open(file_path, 'w+', encoding="UTF-8") as file:
        file.write(fetch(path))


def _delete(path):
    """
    删除对应 url 的对应的目录/文件
    :param path: 请求的相对路径
    :return: None
    """
    file_path = os.path.join(settings.BLOG_REPOSITORIES, parse.unquote(path).lstrip('/'))
    if file_path[-1] == "/":
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
    else:
        os.remove(file_path)


def update_o(name):
    path = reverse(f'article:get_{name}')
    _create(path)


def _update_home():
    update_o('home')


def _update_sitemap():
    update_o('sitemap')


def _update_feed():
    update_o('feed')


def _update_article(article: Article, delete=False):
    path = reverse('article:get_article', kwargs={"slug": article.slug})
    if delete:
        _delete(path)
    else:
        _create(path)


def _update_tag(tag: Tag, delete=False):
    path = reverse('article:get_tag', kwargs={"name": tag.name})
    if delete:
        _delete(path)
    else:
        _create(path)


def _update_corpus(corpus: Corpus, delete=False):
    path = reverse('article:get_corpus', kwargs={"name": corpus.name})
    if delete:
        _delete(path)
    else:
        _create(path)


def _update_time(article: Article, delete=False):
    path = reverse('article:get_time', kwargs={
        "year": article.create_time.strftime("%Y"),
        'month': article.create_time.strftime("%m")
    })
    if delete:
        _delete(path)
    else:
        _create(path)


def update(article: Article):
    _update_article(article)
    if article.corpus is not None:
        _update_corpus(article.corpus)
    for tag in article.tags.all():
        _update_tag(tag)
    _update_time(article)
    _update_sitemap()
    _update_feed()
    _update_home()


def update_all():
    for article in Article.all():
        _update_article(article)
        if article.corpus is not None:
            _update_corpus(article.corpus)
        for tag in article.tags.all():
            _update_tag(tag)
        _update_time(article)
    _update_sitemap()
    _update_feed()
    _update_home()


def delete(article: Article):
    _update_article(article, delete=True)
    if article.corpus is not None:
        _update_corpus(article.corpus)
    for tag in article.tags.all():
        _update_tag(tag)
    _update_time(article)
    _update_sitemap()
    _update_feed()
    _update_home()
