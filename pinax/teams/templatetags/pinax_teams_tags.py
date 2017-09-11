from django import template

from ..models import Team, Membership


register = template.Library()


class AvailableTeamsNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 3 and bits[1] == "as":
            return cls(bits[2])
        else:
            raise template.TemplateSyntaxError("%r takes 'as var'" % bits[0])

    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        request = context["request"]
        teams = []
        for team in Team.objects.all():
            state = team.state_for(request.user)
            if team.member_access == Team.MEMBER_ACCESS_OPEN and state is None:
                teams.append(team)
            elif request.user.is_staff and state is None:
                teams.append(team)
        context[self.context_var] = teams
        return ""


@register.tag
def available_teams(parser, token):
    """
    {% available_teams as available_teams %}
    """
    return AvailableTeamsNode.handle_token(parser, token)


@register.assignment_tag(takes_context=True)
def ancestors_for(context, team=None):
    """
    Retrives the ancestors for a given team and indicates
    if the user can manage each ancestor
    """
    if team is None:
        team = context["team"]

    ancestors = []
    for ancestor in team.ancestors:
        ancestors.append({
            "team": ancestor,
            "can_manage": is_managed_by(ancestor, context["user"])
        })
    context["ancestors"] = ancestors
    return ancestors


@register.assignment_tag(takes_context=True)
def children_for(context, team=None):
    """
    Retrieves the children of a given team and indicates
    if the user can manage each child
    """
    if team is None:
        team = context["team"]

    children = []
    for child in team.children.order_by("slug"):
        children.append({
            "team": child,
            "can_manage": is_managed_by(child, context["user"])
        })
    return children


# @@@ document template
@register.inclusion_tag("pinax/teams/_breadcrumbs.html", takes_context=True)
def get_team_breadcrumbs(context):
    context["ancestors"] = ancestors_for(context)
    return context


def is_managed_by(team, user):
    return team.role_for(user) in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]


@register.filter(name="is_managed_by")
def is_managed_by_as_filter(team, user):
    return is_managed_by(team, user)
