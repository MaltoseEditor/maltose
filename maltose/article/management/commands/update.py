import os
from django.core.management.base import BaseCommand, CommandError

from maltose.article.models import Article
from maltose.article.build import update_all, update_o


class Command(BaseCommand):
    help = "更新或创建对应文章"

    def add_arguments(self, parser):
        os.environ["DJANGO_DEBUG"] = "False"
        parser.add_argument("--all", action="store_true", dest="update-all")
        parser.add_argument("-o", type=str, dest="view")

    def handle(self, *args, **options):
        if options["update-all"]:
            update_all()
            return
        if options.get("view") is not None:
            update_o(options["view"])
            return
