import datetime
import os
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from pinax.invitations.models import JoinInvitation
from reversion import revisions as reversion
from slugify import slugify

from . import signals
from .hooks import hookset


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)


def create_slug(name):
    return slugify(name)[:50]


@python_2_unicode_compatible
class Team(models.Model):

    MEMBER_ACCESS_OPEN = "open"
    MEMBER_ACCESS_APPLICATION = "application"
    MEMBER_ACCESS_INVITATION = "invitation"

    MANAGER_ACCESS_ADD = "add someone"
    MANAGER_ACCESS_INVITE = "invite someone"

    MEMBER_ACCESS_CHOICES = [
        (MEMBER_ACCESS_OPEN, _("open")),
        (MEMBER_ACCESS_APPLICATION, _("by application")),
        (MEMBER_ACCESS_INVITATION, _("by invitation"))
    ]

    MANAGER_ACCESS_CHOICES = [
        (MANAGER_ACCESS_ADD, _("add someone")),
        (MANAGER_ACCESS_INVITE, _("invite someone"))
    ]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100, verbose_name=_("name"))
    avatar = models.ImageField(upload_to=avatar_upload, blank=True, verbose_name=_("avatar"))
    description = models.TextField(blank=True, verbose_name=_("description"))
    member_access = models.CharField(max_length=20, choices=MEMBER_ACCESS_CHOICES, verbose_name=_("member access"))
    manager_access = models.CharField(max_length=20, choices=MANAGER_ACCESS_CHOICES, verbose_name=_("manager access"))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="teams_created", verbose_name=_("creator"))
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name=_("created"))

    def get_absolute_url(self):
        return reverse("team_detail", args=[self.slug])

    def __str__(self):
        return self.name

    def can_join(self, user):
        state = self.state_for(user)
        if self.member_access == Team.MEMBER_ACCESS_OPEN and state is None:
            return True
        elif state == Membership.STATE_INVITED:
            return True
        else:
            return False

    def can_leave(self, user):
        # managers can't leave at the moment
        role = self.role_for(user)
        return role == Membership.ROLE_MEMBER

    def can_apply(self, user):
        state = self.state_for(user)
        return self.member_access == Team.MEMBER_ACCESS_APPLICATION and state is None

    @property
    def applicants(self):
        return self.memberships.filter(state=Membership.STATE_APPLIED)

    @property
    def invitees(self):
        return self.memberships.filter(state=Membership.STATE_INVITED)

    @property
    def declines(self):
        return self.memberships.filter(state=Membership.STATE_DECLINED)

    @property
    def rejections(self):
        return self.memberships.filter(state=Membership.STATE_REJECTED)

    @property
    def acceptances(self):
        return self.memberships.filter(state__in=[
            Membership.STATE_ACCEPTED,
            Membership.STATE_AUTO_JOINED]
        )

    @property
    def members(self):
        return self.acceptances.filter(role=Membership.ROLE_MEMBER)

    @property
    def managers(self):
        return self.acceptances.filter(role=Membership.ROLE_MANAGER)

    @property
    def owners(self):
        return self.acceptances.filter(role=Membership.ROLE_OWNER)

    def is_owner_or_manager(self, user):
        return self.acceptances.filter(
            role__in=[
                Membership.ROLE_OWNER,
                Membership.ROLE_MANAGER
            ],
            user=user
        ).exists()

    def is_member(self, user):
        return self.members.filter(user=user).exists()

    def is_manager(self, user):
        return self.managers.filter(user=user).exists()

    def is_owner(self, user):
        return self.owners.filter(user=user).exists()

    def is_on_team(self, user):
        return self.acceptances.filter(user=user).exists()

    def add_member(self, user, role=None, state=None, by=None):
        # we do this, rather than put the Membership constants in declaration
        # because Membership is not yet defined
        if role is None:
            role = Membership.ROLE_MEMBER
        if state is None:
            state = Membership.STATE_AUTO_JOINED

        membership, created = Membership.objects.get_or_create(
            team=self,
            user=user,
            defaults={"role": role, "state": state},
        )
        signals.added_member.send(sender=self, membership=membership, by=by)
        return membership

    def add_user(self, user, role, by=None):
        state = Membership.STATE_AUTO_JOINED
        if self.manager_access == Team.MANAGER_ACCESS_INVITE:
            state = Membership.STATE_INVITED
        membership, _ = self.memberships.get_or_create(
            user=user,
            defaults={"role": role, "state": state}
        )
        signals.added_member.send(sender=self, membership=membership, by=by)
        return membership

    def invite_user(self, from_user, to_email, role, message=None):
        if not JoinInvitation.objects.filter(signup_code__email=to_email).exists():
            invite = JoinInvitation.invite(from_user, to_email, message, send=False)
            membership, _ = self.memberships.get_or_create(
                invite=invite,
                defaults={"role": role, "state": Membership.STATE_INVITED}
            )
            invite.send_invite()
            signals.invited_user.send(sender=self, membership=membership, by=from_user)
            return membership

    def for_user(self, user):
        try:
            return self.memberships.get(user=user)
        except Membership.DoesNotExist:
            pass

    def state_for(self, user):
        membership = self.for_user(user=user)
        if membership:
            return membership.state

    def role_for(self, user):
        if hookset.user_is_staff(user):
            return Membership.ROLE_MANAGER

        membership = self.for_user(user)
        if membership:
            return membership.role

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = create_slug(self.name)
        self.full_clean()
        super(Team, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")


@python_2_unicode_compatible
class Membership(models.Model):

    STATE_APPLIED = "applied"
    STATE_INVITED = "invited"
    STATE_DECLINED = "declined"
    STATE_REJECTED = "rejected"
    STATE_ACCEPTED = "accepted"
    STATE_AUTO_JOINED = "auto-joined"

    ROLE_MEMBER = "member"
    ROLE_MANAGER = "manager"
    ROLE_OWNER = "owner"

    STATE_CHOICES = [
        (STATE_APPLIED, _("applied")),
        (STATE_INVITED, _("invited")),
        (STATE_DECLINED, _("declined")),
        (STATE_REJECTED, _("rejected")),
        (STATE_ACCEPTED, _("accepted")),
        (STATE_AUTO_JOINED, _("auto joined"))
    ]

    ROLE_CHOICES = [
        (ROLE_MEMBER, _("member")),
        (ROLE_MANAGER, _("manager")),
        (ROLE_OWNER, _("owner"))
    ]

    team = models.ForeignKey(Team, related_name="memberships", verbose_name=_("team"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="memberships", null=True, blank=True, verbose_name=_("user"))
    invite = models.ForeignKey(JoinInvitation, related_name="memberships", null=True, blank=True, verbose_name=_("invite"))
    state = models.CharField(max_length=20, choices=STATE_CHOICES, verbose_name=_("state"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER, verbose_name=_("role"))
    created = models.DateTimeField(default=timezone.now, verbose_name=_("created"))

    def is_owner(self):
        return self.role == Membership.ROLE_OWNER

    def is_manager(self):
        return self.role == Membership.ROLE_MANAGER

    def is_member(self):
        return self.role == Membership.ROLE_MEMBER

    def promote(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.role == Membership.ROLE_MEMBER:
                self.role = Membership.ROLE_MANAGER
                self.save()
                signals.promoted_member.send(sender=self, membership=self, by=by)
                return True
        return False

    def demote(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.role == Membership.ROLE_MANAGER:
                self.role = Membership.ROLE_MEMBER
                self.save()
                signals.demoted_member.send(sender=self, membership=self, by=by)
                return True
        return False

    def accept(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.state == Membership.STATE_APPLIED:
                self.state = Membership.STATE_ACCEPTED
                self.save()
                signals.accepted_membership.send(sender=self, membership=self)
                return True
        return False

    def reject(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.state == Membership.STATE_APPLIED:
                self.state = Membership.STATE_REJECTED
                self.save()
                signals.rejected_membership.send(sender=self, membership=self)
                return True
        return False

    def joined(self):
        self.user = self.invite.to_user
        if self.team.manager_access == Team.MANAGER_ACCESS_ADD:
            self.state = Membership.STATE_AUTO_JOINED
        else:
            self.state = Membership.STATE_INVITED
        self.save()

    def status(self):
        if self.user:
            return self.get_state_display()
        if self.invite:
            return self.invite.get_status_display()
        return "Unknown"

    def resend_invite(self, by=None):
        if self.invite is not None:
            code = self.invite.signup_code
            code.expiry = timezone.now() + datetime.timedelta(days=5)
            code.save()
            code.send()
            signals.resent_invite.send(sender=self, membership=self, by=by)

    def remove(self, by=None):
        if self.invite is not None:
            self.invite.signup_code.delete()
            self.invite.delete()
        self.delete()
        signals.removed_membership.send(sender=Membership, team=self.team, user=self.user, invitee=self.invitee, by=by)

    @property
    def invitee(self):
        return self.user or self.invite.to_user_email()

    def __str__(self):
        return "{0} in {1}".format(self.user, self.team)

    class Meta:
        unique_together = [("team", "user", "invite")]
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")


reversion.register(Membership)
