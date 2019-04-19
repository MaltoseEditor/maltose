from django.apps import AppConfig


class SundriesConfig(AppConfig):
    name = 'maltose.sundries'

    def ready(self):
        import maltose.sundries.signals
