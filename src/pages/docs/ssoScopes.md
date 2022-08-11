---
title: SSO Scopes
description: Learn how you can leverage various SSO Scopes with Seatplus.
---

This is the default login screen for anyone visiting seatplus.

{% figure src="/images/login.png" alt="Login view" /%}

By default, seatplus only requests as single scope: `publicData`

{% figure src="/images/minimal-login.png" alt="Minimal scopes" /%}

However, an admin may set up certain required scopes:
* Default (Character)
* User
* Global

{% figure src="/images/scope-setting.png" alt="Scope Settings" /%}

Following these rules, per selected corporation or alliance users are
being asked to supply a new refresh_token with the required scopes

{% figure src="/images/step-up.png" alt="Step Up Screen" /%}