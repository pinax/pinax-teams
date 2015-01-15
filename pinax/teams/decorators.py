from __future__ import unicode_literals

import functools

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import available_attrs

from account.decorators import login_required

from .models import Team, Membership


def team_required(func=None):
    """
    Decorator for views that require a team be supplied wither via a slug in the
    url pattern or already set on the request object from the TeamMiddleware
    """
    def decorator(view_func):
        @functools.wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            slug = kwargs.pop("slug", None)
            if not getattr(request, "team", None):
                request.team = get_object_or_404(Team, slug=slug)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if func:
        return decorator(func)
    return decorator


def manager_required(func=None):
    """
    Decorator for views that require not only a team but also that a user be
    logged in and be the manager or owner of that team.
    """
    def decorator(view_func):
        @team_required
        @login_required
        @functools.wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            role = request.team.role_for(request.user)
            if role not in [Membership.ROLE_MANAGER, Membership.ROLE_OWNER]:
                raise Http404()
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if func:
        return decorator(func)
    return decorator
