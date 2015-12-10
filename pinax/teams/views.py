import json

from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from django.views.generic import ListView

from django.contrib import messages
from django.contrib.auth import get_user_model

from account.decorators import login_required
from account.mixins import LoginRequiredMixin
from account.views import SignupView
from six import string_types

from .decorators import team_required, manager_required
from .forms import TeamInviteUserForm, TeamForm, TeamSignupForm
from .hooks import hookset
from .models import Team, Membership


MESSAGE_STRINGS = hookset.get_message_strings()


class TeamSignupView(SignupView):

    template_name = "teams/signup.html"

    def get_form_class(self):
        if self.signup_code:
            return self.form_class
        return TeamSignupForm

    def after_signup(self, form):
        if not self.signup_code:
            self.created_user.teams_created.create(
                name=form.cleaned_data["team"]
            )
        super(TeamSignupView, self).after_signup(form)


class TeamCreateView(LoginRequiredMixin, CreateView):

    form_class = TeamForm
    model = Team

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TeamListView(ListView):

    model = Team
    context_object_name = "teams"


@team_required
@login_required
def team_update(request):
    team = request.team
    if not team.is_owner_or_manager(request.user):
        return HttpResponseForbidden()
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect(team.get_absolute_url())
    else:
        form = TeamForm(instance=team)
    return render(request, "teams/team_form.html", {"form": form, "team": team})


@team_required
@login_required
def team_detail(request):
    team = request.team
    state = team.state_for(request.user)
    role = team.role_for(request.user)
    if team.member_access == Team.MEMBER_ACCESS_INVITATION and state is None:
        raise Http404()
    return render(request, "teams/team_detail.html", {
        "team": team,
        "state": state,
        "role": role,
        "invite_form": TeamInviteUserForm(team=team),
        "can_join": team.can_join(request.user),
        "can_leave": team.can_leave(request.user),
        "can_apply": team.can_apply(request.user),
    })


@team_required
@login_required
def team_manage(request):
    team = request.team
    state = team.state_for(request.user)
    role = team.role_for(request.user)
    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    return render(request, "teams/team_manage.html", {
        "team": team,
        "state": state,
        "role": role,
        "invite_form": TeamInviteUserForm(team=team),
        "can_join": team.can_join(request.user),
        "can_leave": team.can_leave(request.user),
        "can_apply": team.can_apply(request.user),
    })


@team_required
@login_required
def team_join(request):
    team = request.team
    state = team.state_for(request.user)

    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_join(request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.role = Membership.ROLE_MEMBER
        membership.state = Membership.STATE_AUTO_JOINED
        membership.save()
        messages.success(request, MESSAGE_STRINGS["joined-team"])
    return redirect("team_detail", slug=team.slug)


@team_required
@login_required
def team_leave(request):
    team = request.team
    state = team.state_for(request.user)
    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_leave(request.user) and request.method == "POST":
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        messages.success(request, MESSAGE_STRINGS["left-team"])
        return redirect("dashboard")
    else:
        return redirect("team_detail", slug=team.slug)


@team_required
@login_required
def team_apply(request):
    team = request.team
    state = team.state_for(request.user)
    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_apply(request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = Membership.STATE_APPLIED
        membership.save()
        messages.success(request, MESSAGE_STRINGS["applied-to-join"])
    return redirect("team_detail", slug=team.slug)


@login_required
@require_POST
def team_accept(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if membership.accept(by=request.user):
        messages.success(request, MESSAGE_STRINGS["accepted-application"])
    return redirect("team_detail", slug=membership.team.slug)


@login_required
@require_POST
def team_reject(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if membership.reject(by=request.user):
        messages.success(request, MESSAGE_STRINGS["rejected-application"])
    return redirect("team_detail", slug=membership.team.slug)


@team_required
@login_required
@require_POST
def team_invite(request):
    team = request.team
    role = team.role_for(request.user)
    if role not in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
        raise Http404()
    form = TeamInviteUserForm(request.POST, team=team)
    if form.is_valid():
        user_or_email = form.cleaned_data["invitee"]
        role = form.cleaned_data["role"]
        if isinstance(user_or_email, string_types):
            membership = team.invite_user(request.user, user_or_email, role)
        else:
            membership = team.add_user(user_or_email, role)
        data = {
            "html": render_to_string(
                "teams/_invite_form.html",
                {
                    "invite_form": TeamInviteUserForm(team=team),
                    "team": team
                },
                context_instance=RequestContext(request)
            )
        }
        if membership is not None:
            if membership.state == Membership.STATE_APPLIED:
                fragment_class = ".applicants"
            elif membership.state == Membership.STATE_INVITED:
                fragment_class = ".invitees"
            elif membership.state in (Membership.STATE_AUTO_JOINED, Membership.STATE_ACCEPTED):
                fragment_class = {
                    Membership.ROLE_OWNER: ".owners",
                    Membership.ROLE_MANAGER: ".managers",
                    Membership.ROLE_MEMBER: ".members"
                }[membership.role]
            data.update({
                "append-fragments": {
                    fragment_class: render_to_string(
                        "teams/_membership.html",
                        {
                            "membership": membership
                        },
                        context_instance=RequestContext(request)
                    )
                }
            })
    else:
        data = {
            "html": render_to_string("teams/_invite_form.html", {
                "invite_form": form,
                "team": team
            }, context_instance=RequestContext(request))
        }
    return HttpResponse(json.dumps(data), content_type="application/json")


@manager_required
@require_POST
def team_member_revoke_invite(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.remove()
    data = {
        "html": ""
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@manager_required
@require_POST
def team_member_resend_invite(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.resend_invite()
    data = {
        "html": render_to_string(
            "teams/_membership.html",
            {
                "membership": membership
            },
            context_instance=RequestContext(request)
        )
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@manager_required
@require_POST
def team_member_promote(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.promote(by=request.user)
    data = {
        "html": render_to_string(
            "teams/_membership.html",
            {
                "membership": membership
            },
            context_instance=RequestContext(request)
        )
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@manager_required
@require_POST
def team_member_demote(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.demote(by=request.user)
    data = {
        "html": render_to_string(
            "teams/_membership.html",
            {
                "membership": membership
            },
            context_instance=RequestContext(request)
        )
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@manager_required
@require_POST
def team_member_remove(request, pk):
    membership = get_object_or_404(request.team.memberships.all(), pk=pk)
    membership.remove()
    data = {
        "html": ""
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@team_required
@login_required
def autocomplete_users(request):
    team = request.team
    role = team.role_for(request.user)
    if role not in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
        raise Http404()
    User = get_user_model()
    users = User.objects.exclude(pk__in=[
        x.user.pk for x in team.memberships.exclude(user__isnull=True)
    ])
    q = request.GET.get("query")
    results = []
    if q:
        results.extend([
            hookset.get_autocomplete_result(x)
            for x in hookset.search_queryset(q, users)
        ])
    return HttpResponse(json.dumps(results), content_type="application/json")
