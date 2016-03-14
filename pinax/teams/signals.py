import django.dispatch


added_member = django.dispatch.Signal(providing_args=["membership", "by"])
invited_user = django.dispatch.Signal(providing_args=["membership", "by"])
promoted_member = django.dispatch.Signal(providing_args=["membership", "by"])
demoted_member = django.dispatch.Signal(providing_args=["membership", "by"])
accepted_membership = django.dispatch.Signal(providing_args=["membership"])
rejected_membership = django.dispatch.Signal(providing_args=["membership"])
resent_invite = django.dispatch.Signal(providing_args=["membership", "by"])
removed_membership = django.dispatch.Signal(providing_args=["team", "user", "invitee", "by"])
