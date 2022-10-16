---
title: Server Features
description: Learn how to configure your instance and all about settings and features available on seatplus.
---

## Schedules

By default, no schedules are created. You can create schedules using the create button. 
It is suggested to create schedules for the following tasks. Please not the advice in the description.

| Job                | Description                                                                                                                                                                                     |
|--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Update Character   | This will pull all character information from esi. Note that esi caches responses per endpoint to a min. of 60 minutes. Executing the job sooner then the cache time will not force an update   |
| Update Corporation | This will pull all corporation information from esi. Note that esi caches responses per endpoint to a min. of 60 minutes. Executing the job sooner then the cache time will not force an update |
| Maintenance Job    | This will update, clean up various internal tables                                                                                                                                              | 
| User Role Sync     | This will sync the user roles with the roles defined in the control group they belong                                                                                                           |

{% figure src="/images/settings/schedules.png" alt="Schedules overview" /%}

## SSO Setting

This is the place where you can configure the SSO settings. Either search for an *Alliance* or a *Corporation* and select all the scopes that you require from a character within that alliance or corporation.
Please note, that you can have varying for corporation within an alliance. The combination of required scopes will be enforced.

{% figure src="/images/settings/scope_setting.png" alt="Scope Setting" /%}


## Onboarding Wizard

{% callout type="note" title="Traefik" %}
You must add a new environmental variable to your .env in order to use the onboarding feature. Remember to restart the container after adding the variable.


```dotenv
ONBOARDING=true
```
{% /callout %}


When doing so new users (newer then 60 Minutes old) are required to complete the onboarding.
The steps are the following:

1) Welcome
2) (optional) open user-level enlistments
3) Add additional characters
4) (optional) open character-level enlistments

This way the experience for new users especially with open user-level enlistment is massively improved

{% figure src="/images/onboarding/step1.png" alt="Onboarding Wizard - Welcome" /%}
{% figure src="/images/onboarding/step2.png" alt="Onboarding Wizard - Enlistments" /%}
{% figure src="/images/onboarding/step3.png" alt="Onboarding Wizard - Characters" /%}