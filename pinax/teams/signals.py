import django.dispatch

added_member = django.dispatch.Signal()
invited_user = django.dispatch.Signal()
promoted_member = django.dispatch.Signal()
demoted_member = django.dispatch.Signal()
accepted_membership = django.dispatch.Signal()
rejected_membership = django.dispatch.Signal()
resent_invite = django.dispatch.Signal()
removed_membership = django.dispatch.Signal()
