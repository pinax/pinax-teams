from django.apps import AppConfig as BaseAppConfig


try:
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

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
