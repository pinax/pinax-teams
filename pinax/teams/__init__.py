import pkg_resources


__version__ = pkg_resources.get_distribution("pinax-teams").version

default_app_config = "pinax.teams.apps.AppConfig"
