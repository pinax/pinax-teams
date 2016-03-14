from django.conf.urls import url

from . import views


urlpatterns = [
    # overall
    url(r"^$", views.TeamListView.as_view(), name="team_list"),
    url(r"^:create/$", views.TeamCreateView.as_view(), name="team_create"),

    # team specific
    url(r"^(?P<slug>[\w\-]+)/$", views.team_detail, name="team_detail"),
    url(r"^(?P<slug>[\w\-]+)/join/$", views.team_join, name="team_join"),
    url(r"^(?P<slug>[\w\-]+)/leave/$", views.team_leave, name="team_leave"),
    url(r"^(?P<slug>[\w\-]+)/apply/$", views.team_apply, name="team_apply"),
    url(r"^(?P<slug>[\w\-]+)/edit/$", views.team_update, name="team_edit"),
    url(r"^(?P<slug>[\w\-]+)/manage/$", views.TeamManageView.as_view(), name="team_manage"),

    # membership specific
    url(r"^(?P<slug>[\w\-]+)/ac/users-to-invite/$", views.autocomplete_users, name="team_autocomplete_users"),  # noqa
    url(r"^(?P<slug>[\w\-]+)/invite-user/$", views.TeamInviteView.as_view(), name="team_invite"),
    url(r"^(?P<slug>[\w\-]+)/members/(?P<pk>\d+)/revoke-invite/$", views.team_member_revoke_invite, name="team_member_revoke_invite"),  # noqa
    url(r"^(?P<slug>[\w\-]+)/members/(?P<pk>\d+)/resend-invite/$", views.team_member_resend_invite, name="team_member_resend_invite"),  # noqa
    url(r"^(?P<slug>[\w\-]+)/members/(?P<pk>\d+)/promote/$", views.team_member_promote, name="team_member_promote"),  # noqa
    url(r"^(?P<slug>[\w\-]+)/members/(?P<pk>\d+)/demote/$", views.team_member_demote, name="team_member_demote"),  # noqa
    url(r"^(?P<slug>[\w\-]+)/members/(?P<pk>\d+)/remove/$", views.team_member_remove, name="team_member_remove"),  # noqa

    url(r"^accept/(?P<pk>\d+)/$", views.team_accept, name="team_accept"),
    url(r"^reject/(?P<pk>\d+)/$", views.team_reject, name="team_reject"),
]
