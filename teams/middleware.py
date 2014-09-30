import re

from django.http import Http404

from account.utils import handle_redirect_to_login

from .conf import settings
from .models import Team, Membership


def check_team_allowed(request):
    allowed = [
        r"^/teams/[\w-]+/account/login/$",
        r"^/teams/[\w-]+/account/signup/",
        r"^/teams/[\w-]+/ajax/username-validation/",
        r"^/teams/[\w-]+/account/password/reset/",
    ]
    for allow_re in allowed:
        if re.search(allow_re, request.path):
            return None
    return handle_redirect_to_login(request, redirect_field_name="next")


class TeamMiddleware(object):

    def process_request(self, request):
        team_slug = request.environ.get("pinax.team")
        if team_slug is not None:
            try:
                team = Team.objects.get(slug=team_slug)
            except Team.DoesNotExist:
                if request.user.is_authenticated():
                    request.user.teams = None
                    raise Http404()
                else:
                    return check_team_allowed(request)
            else:
                request.team = team
        else:
            request.team = None
        if request.user.is_authenticated() and settings.TEAMS_PROFILE_MODEL:
            if re.search(r"^/teams/[\w-]+/account/signup/", request.path):
                return None
            profiles = settings.TEAMS_PROFILE_MODEL.objects.filter(
                user=request.user
            )
            request.user.teams = profiles.filter(
                team__isnull=False,
                team__memberships__state__in=[
                    Membership.STATE_ACCEPTED,
                    Membership.STATE_AUTO_JOINED
                ]
            ).distinct()
            try:
                request.profile = profiles.get(team=request.team)
            except settings.TEAMS_PROFILE_MODEL.DoesNotExist:
                raise Http404()
        else:
            if team_slug is not None:
                return check_team_allowed(request)


class WSGITeamMiddleware(object):

    def __init__(self, application):
        self.app = application

    def __call__(self, environ, start_repsonse):
        m = re.match(r"(/teams/([\w-]+))(.*)", environ["PATH_INFO"])
        if m:
            environ["SCRIPT_NAME"] = m.group(1)
            environ["PATH_INFO"] = m.group(3)
            environ["pinax.team"] = m.group(2)
        return self.app(environ, start_repsonse)
