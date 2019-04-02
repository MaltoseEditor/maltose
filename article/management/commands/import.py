import os
import re
from django.core.management.base import BaseCommand
import markdown

from article.models import Article, Tag, Corpus

# TODO 导入文章
'''
class Command(BaseCommand):
    help = '从指定目录中导入博文'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def get_info(md: str) -> (dict, str):
        datas = re.match(r'---(?P<datas>[\S\s]+?)---', md).group('datas')

        info = dict()
        # XML风格
        if "<title>" in datas:
            for each in re.findall(r'<(?P<name>\S+?)>([\S\s]*?)</\1>', datas):
                info[each[0]] = each[1].strip()

            if not info.get("tags"):
                info["tags"] = []
            else:
                info["tags"] = info["tags"].split(",")

        # YAML风格
        else:
            _md = markdown.Markdown(extensions=['markdown.extensions.meta'])
            _md.convert(md)
            info = _md.Meta
            for key, value in info.items():
                if key == "tags":
                    continue
                info[key] = value[0]

            if info.get("tags") is None or info["tags"][0] == "":
                info["tags"] = []

        md = re.sub(r"^---[\s\S]+?---", "", md)
        return info, md

    def handle(self, *args, **options):
        path = options["path"]
        for eachfile in os.listdir(path):
            if not eachfile.endswith('md'):
                continue
            with open(os.path.join(path, eachfile)) as file:
                data = file.read()
            info, md = self.get_info(data)
'''
