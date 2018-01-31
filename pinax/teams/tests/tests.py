from __future__ import unicode_literals

import json

from django.contrib.auth.models import User

from pinax.teams.models import Membership, Team, avatar_upload
from test_plus.test import TestCase


class BaseTeamTests(TestCase):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_OPEN

    def _create_team(self):
        return Team.objects.create(
            name="Eldarion",
            creator=self.user,
            manager_access=self.MANAGER_ACCESS,
            member_access=self.MEMBER_ACCESS
        )

    def setUp(self):
        self.user = self.make_user("jtauber")


class AvatarUploadTests(TestCase):

    def test_avatar_upload_filename(self):
        path = avatar_upload(None, "MyHeadshot.png")
        self.assertTrue(path.startswith("avatars"))
        self.assertTrue(path.endswith(".png"))


class TeamTests(BaseTeamTests):

    def test_team_creation(self):
        team = self._create_team()
        self.assertEquals(team.name, "Eldarion")
        self.assertEquals(team.slug, "eldarion")
        self.assertEquals(team.creator, self.user)

    def test_team_absolute_url(self):
        team = self._create_team()
        self.assertTrue(team.slug in team.get_absolute_url())

    def test_team_str(self):
        team = self._create_team()
        self.assertEquals(str(team), "Eldarion")

    def test_team_creation_owner_is_member(self):
        team = self._create_team()
        team_user = team.memberships.all()[0]
        self.assertEquals(str(team_user), "jtauber in Eldarion")

    def test_team_role_for(self):
        team = self._create_team()
        self.assertEquals(team.role_for(self.user), Membership.ROLE_OWNER)

    def test_unknown_user(self):
        team = self._create_team()
        other_user = self.make_user("paltman")
        self.assertIsNone(team.for_user(other_user))
        self.assertIsNone(team.role_for(other_user))

    def test_user_is_member(self):
        team = self._create_team()
        other_user = self.make_user("paltman")
        team.add_user(other_user, Membership.ROLE_MEMBER)
        self.assertTrue(team.is_on_team(other_user))

    def test_member_can_leave(self):
        team = self._create_team()
        other_user = self.make_user("paltman")
        team.add_user(other_user, Membership.ROLE_MEMBER)
        self.assertTrue(team.can_leave(other_user))

    def test_manager_cannot_leave(self):
        team = self._create_team()
        self.assertFalse(team.can_leave(self.user))

    def test_owner_is_member(self):
        team = self._create_team()
        self.assertTrue(team.is_on_team(self.user))


class ManagerAddMemberOpenTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_OPEN

    def test_cannot_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.ROLE_MEMBER)
        self.assertFalse(team.can_apply(paltman))

    def test_can_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_apply(paltman))

    def test_can_join_non_member(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertTrue(team.can_join(paltman))

    def test_can_join_invited(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_INVITED
        membership.save()
        self.assertTrue(team.can_join(User.objects.get(username="paltman")))

    def test_can_join_declined(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.STATE_DECLINED)
        self.assertFalse(team.can_join(paltman))


class ManagerAddMemberApplicationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_APPLICATION

    def test_cannot_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.ROLE_MEMBER)
        self.assertFalse(team.can_apply(paltman))

    def test_can_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertTrue(team.can_apply(paltman))

    def test_can_join_non_member(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_join(paltman))

    def test_can_join_invited(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_INVITED
        membership.save()
        self.assertTrue(team.can_join(User.objects.get(username="paltman")))

    def test_can_join_declined(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.STATE_DECLINED)
        self.assertFalse(team.can_join(paltman))


class ManagerAddMemberInvitationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_ADD
    MEMBER_ACCESS = Team.MEMBER_ACCESS_INVITATION

    def test_cannot_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.ROLE_MEMBER)
        self.assertFalse(team.can_apply(paltman))

    def test_can_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_apply(paltman))

    def test_can_join_non_member(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_join(paltman))

    def test_can_join_invited(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_INVITED
        membership.save()
        self.assertTrue(team.can_join(User.objects.get(username="paltman")))

    def test_can_join_declined(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.STATE_DECLINED)
        self.assertFalse(team.can_join(paltman))


class ManagerInviteMemberOpenTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_INVITE
    MEMBER_ACCESS = Team.MEMBER_ACCESS_OPEN

    def test_cannot_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.ROLE_MEMBER)
        self.assertFalse(team.can_apply(paltman))

    def test_can_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_apply(paltman))

    def test_can_join_non_member(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertTrue(team.can_join(paltman))

    def test_can_join_invited(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_INVITED
        membership.save()
        self.assertTrue(team.can_join(User.objects.get(username="paltman")))

    def test_can_join_declined(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_DECLINED
        membership.save()
        self.assertFalse(team.can_join(paltman))


class ManagerInviteMemberApplicationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_INVITE
    MEMBER_ACCESS = Team.MEMBER_ACCESS_APPLICATION

    def test_cannot_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.ROLE_MEMBER)
        self.assertFalse(team.can_apply(paltman))

    def test_can_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertTrue(team.can_apply(paltman))

    def test_can_join_non_member(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_join(paltman))

    def test_can_join_invited(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_INVITED
        membership.save()
        self.assertTrue(team.can_join(User.objects.get(username="paltman")))

    def test_can_join_declined(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_DECLINED
        membership.save()
        self.assertFalse(team.can_join(paltman))

    def test_add_member_twice_does_not_duplicate(self):
        team = self._create_team()
        self.assertEqual(team.memberships.count(), 1)
        paltman = self.make_user("paltman")
        team.add_member(paltman)
        team.add_member(paltman, role=Membership.STATE_APPLIED)
        self.assertEqual(team.memberships.count(), 2)


class ManagerInviteMemberInvitationTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_INVITE
    MEMBER_ACCESS = Team.MEMBER_ACCESS_INVITATION

    def test_cannot_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        team.add_user(paltman, Membership.ROLE_MEMBER)
        self.assertFalse(team.can_apply(paltman))

    def test_can_apply(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_apply(paltman))

    def test_can_join_non_member(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        self.assertFalse(team.can_join(paltman))

    def test_can_join_invited(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_INVITED
        membership.save()
        self.assertTrue(team.can_join(User.objects.get(username="paltman")))

    def test_can_join_declined(self):
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)
        membership.state = Membership.STATE_DECLINED
        membership.save()
        self.assertFalse(team.can_join(paltman))


class ViewTests(BaseTeamTests):

    MANAGER_ACCESS = Team.MANAGER_ACCESS_INVITE
    MEMBER_ACCESS = Team.MEMBER_ACCESS_INVITATION

    def test_team_member_promote_view(self):
        """Ensure view returns 200"""
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)

        with self.login(self.user):
            response = self.post(
                "pinax_teams:team_member_promote",
                slug=team.slug,
                pk=membership.pk,
            )
            self.assertEqual(response.status_code, 200)

    def test_team_member_demote_view(self):
        """Ensure view returns 200"""
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)

        with self.login(self.user):
            response = self.post(
                "pinax_teams:team_member_demote",
                slug=team.slug,
                pk=membership.pk,
            )
            self.assertEqual(response.status_code, 200)

    def test_team_member_remove_view(self):
        """Ensure view returns 200"""
        team = self._create_team()
        paltman = self.make_user("paltman")
        membership = team.add_user(paltman, Membership.ROLE_MEMBER)

        with self.login(self.user):
            response = self.post(
                "pinax_teams:team_member_remove",
                slug=team.slug,
                pk=membership.pk,
            )
            self.assertEqual(response.status_code, 200)

    def test_team_member_resend_invite(self):
        """Ensure view returns 200"""
        team = self._create_team()
        membership = team.invite_user(self.user, "jiggy@widit.com", Membership.ROLE_MEMBER)

        with self.login(self.user):
            response = self.post(
                "pinax_teams:team_member_resend_invite",
                slug=team.slug,
                pk=membership.pk,
            )
            self.assertEqual(response.status_code, 200)

    def test_team_member_revoke_invite(self):
        """Ensure view returns 200"""
        team = self._create_team()
        membership = team.invite_user(self.user, "jiggy@widit.com", Membership.ROLE_MEMBER)

        with self.login(self.user):
            response = self.post(
                "pinax_teams:team_member_revoke_invite",
                slug=team.slug,
                pk=membership.pk,
            )
            self.assertEqual(response.status_code, 200)

    def test_team_member_invite(self):
        """Ensure view returns 200"""
        team = self._create_team()

        post_data = {
            "invitee": "jiggy@widit.com",
            "role": Membership.ROLE_MEMBER,
        }
        with self.login(self.user):
            response = self.post(
                "pinax_teams:team_invite",
                slug=team.slug,
                data=post_data,
            )
            self.assertEqual(response.status_code, 200)
            # convert content to a string, some Python versions do not accept `bytes`
            json_data = json.loads(self.last_response.content.decode("utf-8"))
            self.assertIn("html", json_data)
            self.assertIn("append-fragments", json_data)

    def test_team_member_invite_bad_data(self):
        """Ensure view returns 200"""
        team = self._create_team()

        post_data = {
            "invitee": "jiggy@widit.com",
            "role": "lackey",  # invalid role, believe it or not!
        }
        with self.login(self.user):
            response = self.post(
                "pinax_teams:team_invite",
                slug=team.slug,
                data=post_data,
            )
            self.assertEqual(response.status_code, 200)
            # convert content to a string, some Python versions do not accept `bytes`
            json_data = json.loads(self.last_response.content.decode("utf-8"))
            self.assertIn("html", json_data)
            self.assertNotIn("append-fragments", json_data)
