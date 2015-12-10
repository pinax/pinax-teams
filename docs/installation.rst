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


* Add urls:

    # urls.py
    url(r"^teams/", include("pinax.teams.urls")),


.. _dependencies:

Dependencies
============
