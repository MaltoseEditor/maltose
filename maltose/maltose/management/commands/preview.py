import os

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "启动模拟Github Page的预览服务器"

    def handle(self, *args, **options):
        os.chdir(settings.BLOG_REPOSITORIES)
        if os.name == "posix":
            os.system("python3 -m http.server")
        else:
            os.system("python -m http.server")
