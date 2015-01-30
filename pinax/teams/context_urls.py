# include these urls instead of urls.py if you are using the WSGI + Django middlewares
# to set request.team, manually hooking up List/Create views as well as the accept/reject

from django.conf.urls import patterns, url


urlpatterns = patterns(
    "pinax.teams.views",

    # team specific
    url(r"^detail/$", "team_detail", name="team_detail"),
    url(r"^join/$", "team_join", name="team_join"),
    url(r"^leave/$", "team_leave", name="team_leave"),
    url(r"^apply/$", "team_apply", name="team_apply"),
    url(r"^edit/$", "team_update", name="team_edit"),
    url(r"^manage/$", "team_manage", name="team_manage"),
    url(r"^ac/users-to-invite/$", "autocomplete_users", name="team_autocomplete_users"),  # noqa
    url(r"^invite-user/$", "team_invite", name="team_invite"),
    url(r"^members/(?P<pk>\d+)/revoke-invite/$", "team_member_revoke_invite", name="team_member_revoke_invite"),  # noqa
    url(r"^members/(?P<pk>\d+)/resend-invite/$", "team_member_resend_invite", name="team_member_resend_invite"),  # noqa
    url(r"^members/(?P<pk>\d+)/promote/$", "team_member_promote", name="team_member_promote"),  # noqa
    url(r"^members/(?P<pk>\d+)/demote/$", "team_member_demote", name="team_member_demote"),  # noqa
    url(r"^members/(?P<pk>\d+)/remove/$", "team_member_remove", name="team_member_remove"),  # noqa

)
