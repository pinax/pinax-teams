from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("pinax.teams.urls", namespace="pinax_teams")),
]
