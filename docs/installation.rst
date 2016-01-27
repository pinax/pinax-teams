.. _installation:

============
Installation
============

* Install the development version::

    pip install pinax-teams

* Add ``teams`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # ...
        "reversion",
        "account",
        "pinax.invitations",
        "pinax.teams",
        # ...
    )

* add ``TEAM_NAME_BLACKLIST``to your settings::

    TEAM_NAME_BLACKLIST = ['black_listed_name1', 'blacklisted_name_2]

or if you don't want to blacklist any team name::

    TEAM_NAME_BLACKLIST = []


* Add entry to your ``urls.py``::

    url(r"^teams/", include("pinax.teams.urls")),




.. _dependencies:

Dependencies
============
