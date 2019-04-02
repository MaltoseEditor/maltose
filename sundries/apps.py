from django.apps import AppConfig


class SundriesConfig(AppConfig):
    name = 'sundries'

    def ready(self):
        import sundries.signals
