from django.core.urlresolvers import reverse

from teams.conf import settings


class TeamDefaultHookset(object):

    def build_team_url(self, url_name, team_slug):
        return reverse(url_name, args=[team_slug])

    def get_autocomplete_result(self, user):
        return {"pk": user.pk, "email": user.email, "name": user.get_full_name()}


class HookProxy(object):

    def __getattr__(self, attr):
        return getattr(settings.TEAMS_HOOKSET, attr)


hookset = HookProxy()
