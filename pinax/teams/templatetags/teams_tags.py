from django import template

from ..models import Team


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
