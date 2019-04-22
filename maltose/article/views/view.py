from django.conf import settings
from django.db.models.functions.datetime import TruncYear, TruncMonth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, HttpResponse, Http404
from django.contrib.syndication.views import Feed as _Feed
from django.contrib.sitemaps import Sitemap as _Sitemap

from maltose.maltose.common import create_dict
from maltose.article.models import Article, Tag, Corpus

__all__ = [
    'home',
    'about',
    'donation',
    'feedback',
    'Sitemap',
    'Feed',
    'get_article',
    'get_tag',
    'get_corpus',
    'get_time',
    'page_not_found',
]


class PaginatorView:
    """
    分页, 可以直接使用 /page/1/ 这种形式的url
    """
    template = None

    def __call__(self, *args, **kwargs):
        context = self.get_context(*args, **kwargs)
        context.update(self.get_paginator(context["articles"], kwargs.get('page') if kwargs.get('page') else 1))
        return render(args[0], self.template, context)

    def get_context(self, *args, **kwargs):
        return {'articles': []}

    @staticmethod
    def get_paginator(articles, page):
        paginator = Paginator(articles, settings.PAGE_MAX_NUM)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        empty_list = ['' for _ in range(settings.PAGE_MAX_NUM - articles.object_list.count())]
        return create_dict(locals(), ['articles', 'empty_list'])


class Sitemap(_Sitemap):
    protocol = 'https'

    def items(self):
        return Article.all()

    def lastmod(self, obj: Article):
        return obj.update_time


class Feed(_Feed):
    # 显示在聚合阅读器上的标题
    title = "AberSheeran's BLOG"

    # 通过聚合阅读器跳转到网站的地址
    link = settings.HOMEPAGE

    # 显示在聚合阅读器上的描述信息
    description = "I know nothing except the fact of my ignorance."

    def items(self):
        """
        需要显示的内容条目
        """
        return Article.all()

    def item_title(self, item):
        """
        聚合器中显示的内容条目的标题
        """
        return item.title

    def item_description(self, item):
        """
        聚合器中显示的内容条目的描述
        """
        return item.body

    def item_link(self, item):
        """
        聚合器中显示的内容条目的链接
        """
        return item.get_absolute_url()


def home(request):
    articles = Article.all()
    return render(request, 'article/home.html', context=locals())


def get_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'article/article.html', context=locals())


def get_tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    articles = Article.all().filter(tags=tag)
    return render(request, 'article/tag.html', context=locals())


def get_corpus(request, name):
    corpus = get_object_or_404(Corpus, name=name)
    articles = Article.all().filter(corpus=corpus)
    return render(request, 'article/corpus.html', context=locals())


def get_time(request, year, month):
    articles = Article.all().filter(create_time__year=year, create_time__month=month)
    if articles.count() == 0:
        raise Http404("当前日期无任何文章")
    return render(request, 'article/time.html', context=locals())


def about(request):
    return render(request, 'article/about.html')


def donation(request):
    return render(request, 'article/donation.html')


def feedback(request):
    return render(request, 'article/feedback.html')


def page_not_found(request):
    return render(request, 'article/404.html')
