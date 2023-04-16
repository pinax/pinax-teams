import importlib

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):

    name = "pinax.teams"
    label = "pinax_teams"
    verbose_name = _("Pinax Teams")

    def ready(self):
        importlib.import_module("pinax.teams.receivers")
