from django.contrib import admin

import reversion

from .models import Team, Membership


admin.site.register(
    Team,
    list_display=["name", "member_access", "manager_access", "creator"],
    prepopulated_fields={"slug": ("name",)},
)


class MembershipAdmin(reversion.VersionAdmin):
    list_display = ["team", "user", "state", "role"]
    list_filter = ["team"]
    search_fields = ["user__username"]


admin.site.register(Membership, MembershipAdmin)
