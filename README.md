![](http://pinaxproject.com/pinax-design/patches/pinax-teams.svg)

# Pinax Teams

[![](https://img.shields.io/pypi/v/pinax-teams.svg)](https://pypi.python.org/pypi/pinax-teams/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.python.org/pypi/pinax-teams/)

[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-teams.svg)](https://codecov.io/gh/pinax/pinax-teams)
[![CircleCI](https://circleci.com/gh/pinax/pinax-teams.svg?style=svg)](https://circleci.com/gh/pinax/pinax-teams)
![](https://img.shields.io/github/contributors/pinax/pinax-teams.svg)
![](https://img.shields.io/github/issues-pr/pinax/pinax-teams.svg)
![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-teams.svg)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)

`pinax-teams` is an app for Django sites that supports open, by invitation, and by application teams.


## Installation

* Install the development version:

```
pip install pinax-teams
```

* Add `pinax.teams` (and `pinax.invitations` to your `INSTALLED_APPS` setting:

```python
    INSTALLED_APPS = (
        # ...
        "reversion",
        "account",
        "pinax.invitations",
        "pinax.teams",
        # ...
    )
```

* Add urls:

```python
    # urls.py
    url(r"^teams/", include("pinax.teams.urls")),
```

This will add the `pinax-teams` urls under the namespace `pinax_teams`.

---


## Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates.
This collection can be found at http://pinaxproject.com.

This app was developed as part of the Pinax ecosystem but is just a Django app and can be used independently of other Pinax apps.


## Running the Tests

```
$ pip install detox
$ detox
```


## Contribute

See our How to Contribute (http://pinaxproject.com/pinax/how_to_contribute/) section for an overview on how contributing to Pinax works. For concrete contribution ideas, please see our Ways to Contribute/What We Need Help With (http://pinaxproject.com/pinax/ways_to_contribute/) section.

In case of any questions we recommend you join our Pinax Slack team (http://slack.pinaxproject.com) and ping us there instead of creating an issue on GitHub. Creating issues on GitHub is of course also valid but we are usually able to help you faster if you ping us in Slack.

We also highly recommend reading our Open Source and Self-Care blog post (http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a code of conduct, which can be found here  http://pinaxproject.com/pinax/code_of_conduct/. We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Pinax Project Blog and Twitter

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.


