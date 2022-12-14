from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    name = "apps.incidents"
    verbose_name = "Incidents"

    def ready(self):
        import apps.incidents.signals  # noqa
