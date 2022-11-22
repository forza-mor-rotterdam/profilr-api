from django.apps import AppConfig


class StatusConfig(AppConfig):
    name = "apps.status"
    verbose_name = "Status"

    def ready(self):
        import apps.status.signals  # noqa
