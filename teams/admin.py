from django.contrib import admin

import reversion

from .models import Team, Membership


def members_count(obj):
    return obj.memberships.count()
members_count.short_description = "Members Count"


admin.site.register(
    Team,
    list_display=["name", "member_access", "manager_access", members_count, "creator"],
    fields=[
        "name",
        "slug",
        "avatar",
        "description",
        "member_access",
        "manager_access",
        "creator"
    ],
    prepopulated_fields={"slug": ("name",)},
    raw_id_fields=["creator"]
)


class MembershipAdmin(reversion.VersionAdmin):
    raw_id_fields = ["user"]
    list_display = ["team", "user", "state", "role"]
    list_filter = ["team"]
    search_fields = ["user__username"]


admin.site.register(Membership, MembershipAdmin)
