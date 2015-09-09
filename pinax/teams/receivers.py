from django.dispatch import receiver
from django.db.models.signals import post_save

from pinax.invitations.signals import invite_accepted, joined_independently

from .models import Team, Membership


@receiver(post_save, sender=Team)
def handle_team_save(sender, **kwargs):
    created = kwargs.pop("created")
    team = kwargs.pop("instance")
    if created:
        team.memberships.get_or_create(
            user=team.creator,
            defaults={
                "role": Membership.ROLE_OWNER,
                "state": Membership.STATE_AUTO_JOINED
            }
        )


@receiver([invite_accepted, joined_independently])
def handle_invite_used(sender, invitation, **kwargs):
    for membership in invitation.memberships.all():
        membership.joined()
