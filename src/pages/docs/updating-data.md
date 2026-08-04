---
title: Updating data from ESI
description: How Seatplus keeps its copy of EVE data fresh — the schedules you must create, the queue that runs them, and the on-demand update panel.
---

Seatplus does not read EVE's API when you open a page. It keeps its own copy of your characters' and
corporations' data and serves pages from that, refreshing it in the background. If a page looks
stale or empty, this is the machinery to look at.

{% .lead %}

---

## Schedule the four update jobs

**A fresh installation creates no schedules**, so almost nothing refreshes on its own and most pages
will drift out of date.

One thing does happen without any schedule: when a character authenticates and a new refresh token is
stored, a full character update is queued immediately. That is why your own data appears right after
you first sign in — and why an unscheduled instance looks like it works until the data ages.

Go to **Settings → Server Settings → Schedules** (superuser only) and add a schedule for each of the
four available jobs.

| Job | What it does |
| --- | --- |
| **UpdateCharacter** | Everything character-scoped: public info, corporation history, assets, corporation roles, contacts, wallet journal and transactions, balance, contracts, skills, skill queue, mail headers |
| **UpdateCorporation** | Corporation divisions, member tracking, corporation balance and wallet journal |
| **MaintenanceJob** | Fills in reference data other jobs referred to but did not have — item types, groups and categories, constellations, regions, locations, characters seen only in member tracking, and missing mail bodies |
| **RoleMemberSync** | Reconciles control-group membership: adds and removes automatic-group members, and switches memberships to inactive when an account stops being ESI-compliant |

{% callout type="warning" title="Without RoleMemberSync scheduled, automatic groups barely work" %}
This is the schedule everyone forgets, and it is the one that makes the permission model behave as
documented. Nothing else reconciles group membership on a timer — the only other trigger is a user
completing an EVE SSO login, or an administrator re-saving the group.

Leave it unscheduled and an automatic group will not pick up someone who joined your corporation, will
not drop someone who left, and will not deactivate a member whose ESI scopes went stale, until one of
those two things happens to occur. Schedule it.
{% /callout %}

Each job takes a cron expression, and the screen offers presets from every minute up to monthly. One
schedule per job class — saving a second schedule for the same job updates the first.

{% figure src="/images/settings/schedules.png" alt="The Schedules tab listing scheduled jobs with their cron expressions" caption="Schedules. A fresh install shows an empty list; add one entry per job." /%}

A reasonable starting point is **hourly** for UpdateCharacter and UpdateCorporation, **daily** for the
MaintenanceJob, and **every 15 minutes** for RoleMemberSync.

{% callout type="note" title="The job dropdown shows class names" %}
The create form lists the jobs by their fully-qualified PHP class name, such as
`Seatplus\Eveapi\Jobs\Seatplus\UpdateCharacter` and `Seatplus\Auth\Jobs\RoleMemberSync`. There is no
friendly label, so match on the last segment.
{% /callout %}

{% callout type="note" title="ESI caches, so scheduling more often does not help" %}
EVE's API caches most endpoints for at least an hour. Running Update Character every five minutes does
not get you fresher data — it gets you the same cached response, plus load on your server and on
CCP's. Match your cadence to the cache, not to your impatience.
{% /callout %}

Four things are scheduled for you and need no configuration: character affiliations refresh every five
minutes, a Horizon metrics snapshot is taken every five minutes, Horizon workers are restarted hourly,
and old queue batches are pruned daily.

---

## The queue is not optional

Every update runs as a queued job, so **Seatplus needs Laravel Horizon and Redis running**. If the queue
is not being worked, schedules fire and nothing happens — jobs pile up unprocessed and every page
stays stale.

The **Server Settings** page shows Horizon's worker load, error count and status at the top. If the
status reads anything other than active, fix that before investigating any data problem.

{% figure src="/images/administration/server-settings.png" alt="Server Settings showing Horizon worker stats with worker load, error count and status" caption="Horizon's worker load, error count and status. This is the first place to look when data stops updating." /%}

The number of workers comes from the `QUEUE_WORKERS` variable — see
[Configuration](/docs/configuration).

{% callout type="warning" title="The Horizon dashboard permission is misspelled in Seatplus" %}
The dashboard checks for a permission named `queue_manager` (underscore), but the only permission
Seatplus defines is `queue.manager` (dot). The two never match, so the dashboard is reachable by
superusers only. Granting `queue.manager` has no effect.
{% /callout %}

Scheduled character updates are staggered rather than fired all at once, and a scheduled batch
re-queues itself a few minutes after finishing. In practice the effective ceiling is **one refresh per
character per hour**: a rate limiter drops a character batch that arrives while that character has
already been updated within the hour, rather than queueing it for later.

---

## Updating one entity on demand

Every character and corporation page has an **Update** button in its header. It opens a panel listing
the entities you could refresh for that page's data, split into two sections:

- **Your characters** / **Your corporations** — entities you own, loaded immediately.
- **Affiliated characters** / **Affiliated corporations** — entities you have access to through a
  control group or an in-game role, loaded only when you expand the section.

{% figure src="/images/administration/dispatch-owned-character.png" alt="The dispatch update panel listing the user's own characters with a ready state" caption="The update panel for your own characters. A row shows ready when a job can be dispatched." /%}

{% figure src="/images/administration/dispatch-affiliated-character.png" alt="The dispatch update panel with the affiliated characters section expanded" caption="Affiliated entities are fetched only when you expand the section, so the panel opens fast even with a wide affiliation." /%}

{% figure src="/images/administration/dispatch-owned-corporation.png" alt="The dispatch update panel listing corporations available for a corporation-scoped update" caption="On a corporation page the panel lists corporations instead, filtered to those where you hold the required in-game role." /%}

Each row shows a state: **ready**, **pending** while a batch runs, **finished**, or **failures**.
Clicking a ready row queues the update and the row then polls for progress.

The panel only offers entities that can actually be updated for that page — a character whose token
lacks the relevant scope is not listed, and a corporation is only listed if you hold the in-game role
its data requires. Re-clicking within an hour reports that the job is already queued rather than
duplicating it.

---

## Why data is missing

Work through these in order:

1. **Is Horizon running?** Check the worker stats on Server Settings. No workers, no updates.
2. **Are there schedules?** A fresh install has none. Check all four, including `RoleMemberSync`.
3. **Does the token carry the scope?** Without the scope the job is never even queued, so the data
   was never requested. See [ESI scopes and compliance](/docs/concepts/sso-scopes).
4. **For corporation data, does the right character have the scope?** Member tracking needs a
   Director's token; the corporation wallet needs an `Accountant` or `Junior_Accountant` token.
   Requiring the scope of everyone does not help if no qualifying character granted it.
5. **Has enough time passed?** ESI's cache is at least an hour on most endpoints.

**Settings → Server Performance** lists completed update batches and their statistics, which is the
quickest way to confirm whether updates are running at all.

{% callout type="warning" title="Do not press Clear Cache to fix stale data" %}
**Clear Cache** on Server Settings is far more destructive than its name suggests. It flushes the
whole of Redis — which is also the queue backend — then truncates the job-batch table and deletes
pending batch-update records.

In practice that means it **destroys every queued and in-flight ESI job**, all Horizon metrics, and
the record of which updates were running. It also re-fetches nothing, so it cannot fix stale EVE
data.

It has legitimate uses when something is genuinely wedged, but it is not a routine tool. To pick up a
permission or scope change, just wait out the five-minute permission cache.
{% /callout %}
