from django.apps import AppConfig as BaseAppConfig

try:
    import importlib
except ImportError:
    from django.utils import importlib


class AppConfig(BaseAppConfig):

    name = "pinax.teams"
    verbose_name = "Pinax Teams"

    def ready(self):
        importlib.import_module("pinax.teams.receivers")
