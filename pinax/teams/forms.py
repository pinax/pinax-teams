from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model

from account.forms import SignupForm

from .conf import settings
from .hooks import hookset
from .models import Membership, Team, create_slug


MESSAGE_STRINGS = hookset.get_message_strings()


class TeamSignupForm(SignupForm):

    team = forms.CharField(label=_("Team"), max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super(TeamSignupForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            "team",
            "username",
            "password",
            "password_confirm",
            "email",
            "code"
        ]


class TeamForm(forms.ModelForm):

    def clean_name(self):
        slug = create_slug(self.cleaned_data["name"])
        if self.instance.pk is None and Team.objects.filter(slug=slug).exists():
            raise forms.ValidationError(MESSAGE_STRINGS["slug-exists"])
        if self.cleaned_data["name"].lower() in settings.TEAMS_NAME_BLACKLIST:
            raise forms.ValidationError(MESSAGE_STRINGS["on-team-blacklist"])
        return self.cleaned_data["name"]

    class Meta:
        model = Team
        fields = [
            "name",
            "avatar",
            "description",
            "member_access",
            "manager_access"
        ]


class TeamInviteUserForm(forms.Form):

    invitee = forms.CharField(label="Person to invite")
    role = forms.ChoiceField(choices=Membership.ROLE_CHOICES, widget=forms.RadioSelect)

    def clean_invitee(self):
        User = get_user_model()
        try:
            invitee = User.objects.get(email=self.cleaned_data["invitee"])
            if self.team.is_on_team(invitee):
                raise forms.ValidationError(MESSAGE_STRINGS["user-member-exists"])
        except User.DoesNotExist:
            try:
                # search by USERNAME_FIELD
                params = {User.USERNAME_FIELD: self.cleaned_data["invitee"]}
                invitee = User.objects.get(**params)
                if self.team.is_on_team(invitee):
                    raise forms.ValidationError(MESSAGE_STRINGS["user-member-exists"])
            except User.DoesNotExist:
                invitee = self.cleaned_data["invitee"]
                if self.team.memberships.filter(invite__signup_code__email=invitee).exists():
                    raise forms.ValidationError(MESSAGE_STRINGS["invitee-member-exists"])
        return invitee

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(TeamInviteUserForm, self).__init__(*args, **kwargs)
        self.fields["invitee"].widget.attrs["data-autocomplete-url"] = hookset.build_team_url(
            "team_autocomplete_users",
            self.team.slug
        )
        self.fields["invitee"].widget.attrs["placeholder"] = "email address"
