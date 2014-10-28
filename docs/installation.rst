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
        "kaleo",
        "teams",
        # ...
    )


* Add urls:

    # urls.py
    url(r"^teams/", include("teams.urls")),


.. _dependencies:

Dependencies
============

