import os
import shutil
from urllib import parse

from django.db.models import Count
from django.db.models.functions.datetime import TruncMonth
from django.test import Client
from django.conf import settings
from django.urls import reverse

from .models import *

__all__ = [
    'create',
    'delete',
]


def fetch(path) -> str:
    return Client().get(path).content.decode("UTF-8")


def create(path):
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


def delete(path):
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
    create(path)


def update_home():
    update_o('home')


def update_sitemap():
    update_o('sitemap')


def update_feed():
    update_o('feed')


def update_article(article: Article):
    path = reverse('article:get_article', kwargs={"slug": article.slug})
    if not article.is_draft:
        create(path)


def update_tag(tag: Tag):
    path = reverse('article:get_tag', kwargs={"name": tag.name})
    create(path)


def update_corpus(corpus: Corpus):
    path = reverse('article:get_corpus', kwargs={"name": corpus.name})
    create(path)


def update_time(year, month):
    path = reverse('article:get_time', kwargs={"year": year, 'month': month})
    create(path)


def update_all():
    shutil.rmtree(os.path.join(settings.BLOG_REPOSITORIES, 'articles'), True)
    shutil.rmtree(os.path.join(settings.BLOG_REPOSITORIES, 'corpus'), True)
    shutil.rmtree(os.path.join(settings.BLOG_REPOSITORIES, 'tags'), True)
    shutil.rmtree(os.path.join(settings.BLOG_REPOSITORIES, 'time'), True)

    for corpus in Corpus.objects.annotate(count=Count('article')).filter(count__gte=0):
        update_corpus(corpus)

    for tag in Tag.objects.annotate(count=Count('article')).filter(count__gte=0):
        update_tag(tag)

    for time in Article.visible().dates('create_time', 'month', order='DESC'):
        update_time(time.year, time.strftime('%m'))

    for article in Article.visible():
        update_article(article)

    update_home()
    update_feed()
    update_sitemap()
