from django import template

from ..models import Team


register = template.Library()


@register.assignment_tag(takes_content=True)
def available_teams(context):
    teams = []
    request = context["request"]
    for team in Team.objects.all():
        state = team.state_for(request.user)
        if team.member_access == Team.MEMBER_ACCESS_OPEN and state is None:
            teams.append(team)
        elif request.user.is_staff and state is None:
            teams.append(team)
    return teams
