DEBUG = True
USE_TZ = True
TIME_ZONE = "UTC"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:"
    }
}
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware"
]
ROOT_URLCONF = "pinax.teams.tests.urls"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "account",
    "pinax.invitations",
    "pinax.teams",
]
SITE_ID = 1
SECRET_KEY = "notasecret"
