import django.dispatch


added_member = django.dispatch.Signal(providing_args=["membership"])
invited_user = django.dispatch.Signal(providing_args=["membership"])
promoted_member = django.dispatch.Signal(providing_args=["membership"])
demoted_member = django.dispatch.Signal(providing_args=["membership"])
accepted_membership = django.dispatch.Signal(providing_args=["membership"])
rejected_membership = django.dispatch.Signal(providing_args=["membership"])
resent_invite = django.dispatch.Signal(providing_args=["membership"])
removed_membership = django.dispatch.Signal(providing_args=["team", "user"])
