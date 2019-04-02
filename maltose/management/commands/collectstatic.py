import os
import shutil

from django.contrib.staticfiles.management.commands.collectstatic import Command as _Command
from django.conf import settings


class Command(_Command):

    def handle(self, **options):
        super().handle(**options)
        with open(os.path.join(settings.STATIC_ROOT, '.gitignore'), 'w+') as file:
            file.write('admin/')
