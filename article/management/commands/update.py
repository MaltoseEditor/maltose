import os
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings

from article.models import Article
from article.build import update, update_all, update_o


class Command(BaseCommand):
    help = '更新或创建对应文章'

    def add_arguments(self, parser):
        os.environ['DJANGO_DEBUG'] = 'False'
        parser.add_argument('-a', type=str, dest="article_title", required=False)
        parser.add_argument('--all', action='store_true', dest="update-all", default=False)
        parser.add_argument('-o', type=str, dest="view", required=False)

    def handle(self, *args, **options):
        if options['update-all']:
            update_all()
            return
        if options.get('view') is not None:
            update_o(options['view'])
            return
        try:
            article = Article.objects.get(title=options.get('article_title'))
        except Article.DoesNotExist:
            raise CommandError('文章不存在, 请检查标题是否正确')
        update(article)
