import json

from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from django.contrib.auth.models import User
from django.contrib import messages

from account.decorators import login_required
from account.mixins import LoginRequiredMixin

from .forms import TeamInviteUserForm, TeamForm
from .models import Team, Membership


class TeamCreateView(LoginRequiredMixin, CreateView):

    form_class = TeamForm
    model = Team

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TeamUpdateView(LoginRequiredMixin, UpdateView):

    form_class = TeamForm
    model = Team

    def get(self, request, *args, **kwargs):
        response = super(TeamUpdateView, self).get(request, *args, **kwargs)
        if not self.object.is_owner_or_manager(request.user):
            response = HttpResponseForbidden()
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_owner_or_manager(request.user):
            return HttpResponseForbidden()
        return super(TeamUpdateView, self).post(request, *args, **kwargs)


class TeamListView(ListView):

    model = Team
    context_object_name = "teams"


@login_required
def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug)
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


@login_required
def team_manage(request, slug):
    team = get_object_or_404(Team, slug=slug)
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


@login_required
def team_join(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.state_for(request.user)
    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_join(request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = Membership.STATE_MEMBER
        membership.save()
        messages.success(request, "Joined team.")
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_leave(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.state_for(request.user)
    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_leave(request.user) and request.method == "POST":
        membership = Membership.objects.get(team=team, user=request.user)
        membership.delete()
        messages.success(request, "Left team.")
        return redirect("dashboard")
    else:
        return redirect("team_detail", slug=slug)


@login_required
def team_apply(request, slug):
    team = get_object_or_404(Team, slug=slug)
    state = team.state_for(request.user)
    if team.manager_access == Team.MEMBER_ACCESS_INVITATION and \
       state is None and not request.user.is_staff:
        raise Http404()

    if team.can_apply(request.user) and request.method == "POST":
        membership, created = Membership.objects.get_or_create(team=team, user=request.user)
        membership.state = Membership.STATE_APPLIED
        membership.save()
        messages.success(request, "Applied to join team.")
        return redirect("team_detail", slug=slug)
    else:
        return redirect("team_detail", slug=slug)


@login_required
@require_POST
def team_accept(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if membership.accept(by=request.user):
        messages.success(request, "Accepted application.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
@require_POST
def team_reject(request, pk):
    membership = get_object_or_404(Membership, pk=pk)
    if membership.reject(by=request.user):
        messages.success(request, "Rejected application.")
    return redirect("team_detail", slug=membership.team.slug)


@login_required
@require_POST
def team_invite(request, slug):
    team = get_object_or_404(Team, slug=slug)
    role = team.role_for(request.user)
    if role not in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
        raise Http404()
    form = TeamInviteUserForm(request.POST, team=team)
    if form.is_valid():
        user_or_email = form.cleaned_data["invitee"]
        role = form.cleaned_data["role"]
        if isinstance(user_or_email, basestring):
            membership = team.invite_user(request.user, user_or_email, role)
        else:
            membership = team.add_user(user_or_email, role)
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
        data = {
            "html": render_to_string(
                "teams/_invite_form.html",
                {
                    "invite_form": TeamInviteUserForm(team=team),
                    "team": team
                },
                context_instance=RequestContext(request)
            ),
            "append-fragments": {
                fragment_class: render_to_string(
                    "teams/_membership.html",
                    {
                        "membership": membership
                    },
                    context_instance=RequestContext(request)
                )
            }
        }
    else:
        data = {
            "html": render_to_string("teams/_invite_form.html", {
                "invite_form": form,
                "team": team
            }, context_instance=RequestContext(request))
        }
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def autocomplete_users(request, slug):
    team = get_object_or_404(Team, slug=slug)
    role = team.role_for(request.user)
    if role not in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
        raise Http404()
    users = User.objects.exclude(pk__in=[
        x.user.pk for x in team.memberships.exclude(user__isnull=True)
    ])
    q = request.GET.get("query")
    results = []
    if q:
        results.extend([
            {"pk": x.pk, "email": x.email, "name": x.get_full_name()}
            for x in users.filter(
                Q(email__icontains=q) |
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        ])
    return HttpResponse(json.dumps(results), content_type="application/json")
