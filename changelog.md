# Change Log

## 0.12.2
* BI: Move `WSGITeamMiddleware` to it's own module to resolve issues with the custom app label.
This BI change was made in 0.12.2 as `WSGITeamMiddleware` had not been documented or demonstrated.

## 0.12.1
* Update `context_urls.py` to reference the correct views

## 0.12
* Add `SimpleTeam` and `SimpleMembership` models [PR #46](https://github.com/pinax/pinax-teams/pull/46)

## 0.11.5

* Add initiating user to membership signals [PR #42](https://github.com/pinax/pinax-teams/pull/42)
* Refactor TeamManageView and TeamInviteView as CBVs [PR #43](https://github.com/pinax/pinax-teams/pull/43)
* Remove assumptions around auth.User model [PR #40](https://github.com/pinax/pinax-teams/pull/40)
* Fix invitee to call to_user_email method [PR #41](https://github.com/pinax/pinax-teams/pull/41)
* Fix Membership verbose names in model meta [PR #45](https://github.com/pinax/pinax-teams/pull/45)
* Ensure team exists in template context [PR #44](https://github.com/pinax/pinax-teams/pull/44)

**Backwards Incompatible Changes**

* `TEAM_NAME_BLACKLIST` has been renamed to `TEAMS_NAME_BLACKLIST` for consistency with other application settings