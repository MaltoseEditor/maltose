import os
import shutil
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = '清除项目路径下所有migrations下的文件'

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            path = os.path.join(os.path.join(settings.BASE_DIR, app.replace(".", "/")), "migrations")
            if os.path.exists(path):
                shutil.rmtree(path)
                os.makedirs(path)
                with open(os.path.join(path, "__init__.py"), "w+") as file:
                    pass
                self.stdout.write(self.style.SUCCESS(f"Clear {path}"))
        self.stdout.write(self.style.SUCCESS('Successfully cleared!'))
