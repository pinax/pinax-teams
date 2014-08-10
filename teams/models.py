import os
import uuid

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

import reversion

from kaleo.models import JoinInvitation
from slugify import slugify


def avatar_upload(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("avatars", filename)


def create_slug(name):
    return slugify(name)[:50]


class Team(models.Model):

    MEMBER_ACCESS_OPEN = "open"
    MEMBER_ACCESS_APPLICATION = "application"
    MEMBER_ACCESS_INVITATION = "invitation"

    MANAGER_ACCESS_ADD = "add someone"
    MANAGER_ACCESS_INVITE = "invite someone"

    MEMBER_ACCESS_CHOICES = [
        (MEMBER_ACCESS_OPEN, "open"),
        (MEMBER_ACCESS_APPLICATION, "by application"),
        (MEMBER_ACCESS_INVITATION, "by invitation")
    ]

    MANAGER_ACCESS_CHOICES = [
        (MANAGER_ACCESS_ADD, "add someone"),
        (MANAGER_ACCESS_INVITE, "invite someone")
    ]

    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to=avatar_upload, blank=True)
    description = models.TextField(blank=True)
    member_access = models.CharField(max_length=20, choices=MEMBER_ACCESS_CHOICES)
    manager_access = models.CharField(max_length=20, choices=MANAGER_ACCESS_CHOICES)
    creator = models.ForeignKey(User, related_name="teams_created")
    created = models.DateTimeField(default=timezone.now, editable=False)

    def get_absolute_url(self):
        return reverse("team_detail", args=[self.slug])

    def __str__(self):
        return self.name

    def __unicode__(self):
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

    def is_manager(self, user):
        return self.managers.filter(user=user).exists()

    def is_on_team(self, user):
        return self.acceptances.filter(user=user).exists()

    def add_user(self, user, role):
        state = Membership.STATE_AUTO_JOINED
        if self.manager_access == Team.MANAGER_ACCESS_INVITE:
            state = Membership.STATE_INVITED
        membership, _ = self.memberships.get_or_create(
            user=user,
            defaults={"role": role, "state": state}
        )
        return membership

    def invite_user(self, from_user, to_email, role):
        invite = JoinInvitation.invite(from_user, to_email)
        membership, _ = self.memberships.get_or_create(
            invite=invite,
            defaults={"role": role, "state": Membership.STATE_INVITED}
        )
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
        membership = self.for_user(user)
        if membership:
            return membership.role

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = create_slug(self.name)
        self.full_clean()
        super(Team, self).save(*args, **kwargs)


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
        (STATE_APPLIED, "applied"),
        (STATE_INVITED, "invited"),
        (STATE_DECLINED, "declined"),
        (STATE_REJECTED, "rejected"),
        (STATE_ACCEPTED, "accepted"),
        (STATE_AUTO_JOINED, "auto joined")
    ]

    ROLE_CHOICES = [
        (ROLE_MEMBER, "member"),
        (ROLE_MANAGER, "manager"),
        (ROLE_OWNER, "owner")
    ]

    team = models.ForeignKey(Team, related_name="memberships")
    user = models.ForeignKey(User, related_name="memberships", null=True)
    invite = models.ForeignKey(JoinInvitation, related_name="memberships", null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    created = models.DateTimeField(default=timezone.now)

    def promote(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.role == Membership.ROLE_MEMBER:
                self.role = Membership.ROLE_MANAGER
                self.save()
                return True
        return False

    def demote(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.role == Membership.ROLE_MANAGER:
                self.role = Membership.ROLE_MEMBER
                self.save()
                return True
        return False

    def accept(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.state == Membership.STATE_APPLIED:
                self.state = Membership.STATE_ACCEPTED
                self.save()
                return True
        return False

    def reject(self, by):
        role = self.team.role_for(by)
        if role in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
            if self.state == Membership.STATE_APPLIED:
                self.state = Membership.STATE_REJECTED
                self.save()
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

    @property
    def invitee(self):
        return self.user or self.invite.to_user_email

    def __str__(self):
        return "{0} in {1}".format(self.user, self.team)

    def __unicode__(self):
        return u"{0} in {1}".format(self.user, self.team)

    class Meta:
        unique_together = [("team", "user", "invite")]


reversion.register(Membership)
