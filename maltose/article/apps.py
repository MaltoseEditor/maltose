from django.apps import AppConfig


class ArticleConfig(AppConfig):
    name = 'maltose.article'

    def ready(self):
        import maltose.article.signals
