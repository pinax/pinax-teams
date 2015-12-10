from django.db.models import Q

from django.core.urlresolvers import reverse


MESSAGE_STRINGS = {
    "joined-team": "Joined team.",
    "left-team": "Left team.",
    "applied-to-join": "Applied to join team.",
    "accepted-application": "Accepted application.",
    "rejected-application": "Rejected application.",
    "slug-exists": "Team with this name already exists",
    "on-team-blacklist": "You can not create a team by this name",
    "user-member-exists": "User already on team.",
    "invitee-member-exists": "Invite already sent.",
}


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

    def get_message_strings(self):
        return MESSAGE_STRINGS


class HookProxy(object):

    def __getattr__(self, attr):
        from pinax.teams.conf import settings
        return getattr(settings.TEAMS_HOOKSET, attr)


hookset = HookProxy()
