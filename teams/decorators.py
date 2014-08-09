from __future__ import unicode_literals

import functools

from django.shortcuts import get_object_or_404
from django.utils.decorators import available_attrs

from .models import Team


def team_required(func=None):
    """
    Decorator for views that require a team be supplied wither via a slug in the
    url pattern or already set on the request object from the TeamMiddleware
    """
    def decorator(view_func):
        @functools.wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            print "Calling manage", args, kwargs, hasattr(request, "team")
            slug = kwargs.pop("slug", None)
            if not getattr(request, "team", None):
                request.team = get_object_or_404(Team, slug=slug)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if func:
        return decorator(func)
    return decorator
