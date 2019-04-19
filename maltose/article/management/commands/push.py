from django.core.management.base import BaseCommand

from maltose.maltose.common import push


class Command(BaseCommand):
    help = '推送生成的静态文件到远程仓库'

    def handle(self, *args, **options):
        process = push()
        process.wait()
