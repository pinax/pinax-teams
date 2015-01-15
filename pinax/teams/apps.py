from django.apps import AppConfig as BaseAppConfig
from django.utils.importlib import import_module


class AppConfig(BaseAppConfig):

    name = "pinax.teams"
    verbose_name = "Pinax Teams"

    def ready(self):
        import_module("pinax.teams.receivers")
