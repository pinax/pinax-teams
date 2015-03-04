from django.db.models import Q

from django.core.urlresolvers import reverse


class TeamDefaultHookset(object):

    def build_team_url(self, url_name, team_slug):
        return reverse(url_name, args=[team_slug])

    def get_autocomplete_result(self, user):
        return {"pk": user.pk, "email": user.email, "name": user.get_full_name()}

    def search_queryset(self, query, users):
        return users.filter(
            Q(email__icontains=query) |
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )


class HookProxy(object):

    def __getattr__(self, attr):
        from pinax.teams.conf import settings
        return getattr(settings.TEAMS_HOOKSET, attr)


hookset = HookProxy()
