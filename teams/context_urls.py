# include these urls instead of urls.py if you are using the WSGI + Django middlewares
# to set request.team, manually hooking up List/Create views as well as the accept/reject

from django.conf.urls import patterns, url


urlpatterns = patterns(
    "teams.views",

    # team specific
    url(r"^detail/$", "team_detail", name="team_detail"),
    url(r"^join/$", "team_join", name="team_join"),
    url(r"^leave/$", "team_leave", name="team_leave"),
    url(r"^apply/$", "team_apply", name="team_apply"),
    url(r"^edit/$", "team_update", name="team_edit"),
    url(r"^manage/$", "team_manage", name="team_manage"),
    url(r"^ac/users-to-invite/$", "autocomplete_users", name="team_autocomplete_users"),  # noqa
    url(r"^invite-user/$", "team_invite", name="team_invite"),
)
