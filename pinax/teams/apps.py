from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _

try:
    import importlib
except ImportError:
    from django.utils import importlib


class AppConfig(BaseAppConfig):

    name = "pinax.teams"
    label = "pinax_teams"
    verbose_name = _("Pinax Teams")

    def ready(self):
        importlib.import_module("pinax.teams.receivers")
