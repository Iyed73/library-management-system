from django.apps import AppConfig
from django.core.signals import request_finished


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"

    def ready(self):
        import catalog.signals
