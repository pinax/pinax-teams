from django import forms

from django.contrib.auth.models import User

from .hooks import hookset
from .models import Membership, Team, create_slug


class TeamForm(forms.ModelForm):

    def clean_name(self):
        slug = create_slug(self.cleaned_data["name"])
        if self.instance.pk is None and Team.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Team with this name already exists")
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

    invitee = forms.EmailField(label="Person to invite")
    role = forms.ChoiceField(choices=Membership.ROLE_CHOICES, widget=forms.RadioSelect)

    def clean_invitee(self):
        try:
            return User.objects.get(email=self.cleaned_data["invitee"])
        except User.DoesNotExist:
            return self.cleaned_data["invitee"]

    def __init__(self, *args, **kwargs):
        self.team = kwargs.pop("team")
        super(TeamInviteUserForm, self).__init__(*args, **kwargs)
        self.fields["invitee"].widget.attrs["data-autocomplete-url"] = hookset.build_team_url(
            "team_autocomplete_users",
            self.team.slug
        )
        self.fields["invitee"].widget.attrs["placeholder"] = "email address"
