from django.conf import settings  # noqa
from django.core.exceptions import ImproperlyConfigured
from django.utils import importlib

from appconf import AppConf


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    try:
        mod = importlib.import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured("Error importing {0}: '{1}'".format(module, e))
    try:
        attr = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured("Module '{0}' does not define a '{1}'".format(module, attr))
    return attr


class TeamAppConf(AppConf):

    PROFILE_MODEL = ""
    HOOKSET = "pinax.teams.hooks.TeamDefaultHookset"
    NAME_BLACKLIST = []
    MESSAGE_STRINGS = {
        "joined-team": "Joined team.",
        "left-team": "Left team.",
        "applied-to-join": "Applied to join team.",
        "accepted-application": "Accepted application.",
        "rejected-application": "Rejected application.",
        "slug-exists": "Team with this name already exists",
        "on-team-blacklist": "You can not create a team by this name",
        "user-member-exists": "User already on team.",
        "invitee-member-exists": "Invite already sent." 
    }

    def configure_profile_model(self, value):
        if value:
            return load_path_attr(value)

    def configure_hookset(self, value):
        return load_path_attr(value)()
