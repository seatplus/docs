---
title: Server settings
description: The superuser-only settings area — queue health, the user list and impersonation, SSO scope requirements, schedules, and server performance.
---

**Settings → Server Settings** is the administrator's console. Everything on it requires the
`superuser` permission, and it is where the instance-wide switches live.

{% .lead %}

---

## What is on the page

{% figure src="/images/administration/server-settings.png" alt="The Server Settings page with Horizon worker stats, a Clear Cache button, and the Available Settings tabs" caption="Server Settings: queue health at the top, then the Available Settings tabs — User List, SSO Setting and Schedules." /%}

**Horizon worker stats** across the top — worker load, error count and status. This is the health
check for the background queue that every ESI update depends on. If the status is not active, no data
is being refreshed anywhere in the application.

{% callout type="warning" title="Clear Cache destroys your queued jobs" %}
**Clear Cache** does much more than its name implies. It flushes the entire Redis instance — which is
also where the queue lives — then truncates the job-batch table and deletes pending batch-update
records. Every queued and in-flight ESI job is lost, along with all Horizon metrics and batch history.
It re-fetches nothing.

Reach for it only when the queue or cache is genuinely wedged. To pick up a permission or scope change,
wait out the five-minute permission cache instead.
{% /callout %}

Below that, **Available Settings** with three tabs.

---

## User List

Every account on the instance, searchable by character name, showing each account's main character.
Each row has an **Impersonate** button.

Impersonating an account shows you Seatplus exactly as that user sees it — the same sidebar, the same
permissions, the same empty pages. It is the fastest way to answer "why can this person not see X".
Leave impersonation through **Stop impersonating**.

{% callout type="warning" title="Impersonation is unaudited" %}
Impersonating a user is not logged or announced anywhere, and while impersonating you act with that
user's permissions. Treat it as an administrative capability with real reach, and be deliberate about
who holds `superuser`.
{% /callout %}

---

## SSO Setting

The instance-wide ESI scope requirements: which corporations and alliances must grant which scopes,
and whether a requirement applies to characters in that entity, to whole accounts, or to everyone.

This tab is covered in full on [ESI scopes and compliance](/docs/concepts/sso-scopes) — including how
requirements combine, how compliance is computed, and what a non-compliant user experiences.

---

## Schedules

The cron schedules that keep your copy of EVE's data current. **A fresh installation has none**, and
until you add them very little updates on its own.

This tab is covered in full on [Updating data from ESI](/docs/updating-data).

---

## Server Performance

**Settings → Server Performance** is a separate sidebar entry listing completed update batches and
their statistics. It is the quickest way to confirm whether background updates are actually running,
and to see how long they take on your hardware.

---

## Manual Locations

**Settings → Manual Locations** is also in this area but is *not* superuser-only — it needs the
`manage manual locations` permission. It is where you review the structure names users have suggested
for private Upwell structures that EVE's API will not name.

See [Manual locations](/docs/corporation/manual-locations).

---

## The onboarding wizard

New users can be walked through a short setup flow instead of being dropped straight onto the
dashboard. It is off by default; enable it by adding this to your `.env` and restarting the
containers:

```dotenv
ONBOARDING=true
```

Once enabled, accounts created less than an hour ago are required to complete it. The steps, in order,
are: a welcome; any open whole-account job postings; adding your other characters; and then any open
single-character job postings. The job-posting steps are skipped when there is nothing open of that kind,
so most instances show a shorter wizard than the four steps above.

{% figure src="/images/onboarding/step1.png" alt="The first step of the onboarding wizard, a welcome screen" caption="Step one: the welcome screen." /%}

{% figure src="/images/onboarding/step2.png" alt="An onboarding step offering open job postings the new user can apply to" caption="Open job postings are offered inline, so a new recruit can apply immediately." /%}

{% figure src="/images/onboarding/step3.png" alt="An onboarding step prompting the user to add their additional characters" caption="Adding alts during onboarding is what makes whole-account scope requirements satisfiable from the start." /%}

{% callout type="note" title="Worth enabling if you recruit through Seatplus" %}
The wizard's value is that it asks new users to add their alts and apply before they wander off. If
your instance is the front door for recruitment, turn it on.
{% /callout %}
