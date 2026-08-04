---
title: Member tracking
description: The raw ESI member roster for a corporation — who joined when, when they last logged in, where they were and what they were flying.
---

**Corporation → Member Tracking** is EVE's own member roster, stored and rendered. One card per
corporation, one row per member, with the five facts ESI gives you about each of them. It is a
tracking screen, not a compliance screen — it knows nothing about whether an account has granted the
scopes you require of it.

{% .lead %}

**Route:** `/corporation/tracking`

**Permission required:** `view member tracking`, or an in-game `Director` role in the corporation.
Either one is enough to open the route — but see the warning below, because a second permission string
gates what you can actually do once you are in.

**ESI scope required:** `esi-corporations.track_members.v1`, on the refresh token of a character in
that corporation who holds `Director`. No other role satisfies this endpoint.

{% callout type="warning" title="Two different permission strings gate this page" %}
The route middleware checks `view member tracking`. Everything *inside* the page checks a different
permission: **`members`**, which is the permission the member-tracking model is registered under. That
covers both the **Select Corporation** picker and the server-side guard deciding whether a
`?corporation_ids=` selection is honoured.

A control group granted only `view member tracking` therefore opens the page and finds it useless: no
corporations in the default list, an empty picker, and a hand-written `?corporation_ids=` dropped without
a message. Grant such a group **both** `view member tracking` and `members`.

An in-game `Director` satisfies both sides on its own, which is why this only bites permission-based
access — and why it is invisible to whoever set the group up, if they happen to be a Director.
{% /callout %}

---

## What you see

{% figure src="/images/personnel/member-tracking.png" alt="The Corporation Member Tracking page showing a corporation card with a member list of names, locations, ships, join dates and last logins" caption="One card per corporation, with an infinitely scrolling member list. The header row stays pinned while you scroll." /%}

The card header identifies the corporation. Below it, a pinned header row and then the members:

| Column | Field it comes from |
| --- | --- |
| **Name** | The member's character, with portrait. Characters Seatplus has not yet fetched public info for render from their id alone |
| **Last Location** | The member's location, resolved to a station or structure name — `Unknown Location` when it could not be resolved |
| **Ship** | The ship type they were last in, with its icon |
| **Joined** | When they joined the corporation, to the second |
| **Last Login** | Their last logon, to the second |

The list loads more members as you scroll, and each corporation's list keeps its own scroll position.
On narrow screens the same rows render stacked instead of as a grid.

That is the whole of the data. There is no compliance state, no employment status and no account
grouping here — a member with five characters in the corporation is five rows. For the account-level
view, see [Employment observation](/docs/personnel/observation).

## Which corporations you see

By default the page lists **the corporations you operate**: those where one of your own characters is
a member and holds `Director`. Only corporations that actually have stored members are listed at all.

Corporations you can reach through a control group are **not** in that default list. Use
**Select Corporation** to pick them — which is where the `members` permission described above matters:
both the picker's contents and the server's acceptance of your selection are decided by `members`, not by
`view member tracking`. The server honours a selection only for corporations you are genuinely affiliated
with under that permission.

Seatplus only knows a character holds `Director` if that character's token carries
`esi-characters.read_corporation_roles.v1`. See
[Permissions and control groups](/docs/concepts/permissions).

## Locations and ships fill in afterwards

The member tracking endpoint returns ids, not names. After storing the roster, the update job queues
follow-up work for everything it does not have a name for: public info for unknown characters, a
location resolution for every unknown location id, and a type lookup for every unknown ship type. So
a freshly updated corporation can briefly show rows whose location or ship is still blank.

Location resolution is attempted with **the same Director token** that read the roster. If that
character cannot read a private structure, the location stays unresolved and the row reads
`Unknown Location`. That is the case [manual locations](/docs/corporation/manual-locations) exist to
fix — once a suggestion is accepted, these rows pick up the name.

## Members who have left

Each update replaces the roster wholesale: members ESI no longer reports are deleted from Seatplus's
tracking table. Member tracking is therefore always a snapshot of the corporation as it is now, and
carries no history of who used to be in it. If you need departures to persist, that is what the
employment records behind [Employment observation](/docs/personnel/observation) are for.

## Refreshing the data

Member tracking is pulled by the scheduled **UpdateCorporation** job. Nothing is fetched when you open the
page, so an out-of-date roster means that job has not run recently — or has never run.

{% callout type="warning" title="The Update button queues one job, not the corporation batch" %}
**Update** in the header does not run UpdateCorporation. It dispatches the member-tracking job set, which
is exactly one job: the corporation member-tracking job.

For *this* page that is the job you want — the roster is all this screen shows, so **Update** does refresh
it. Do not expect it to do anything else UpdateCorporation covers, though: wallet divisions, corporation
balances and corporation journals are untouched, so pressing it here will not repair
[Corporation wallet](/docs/corporation/wallet).
{% /callout %}

The panel only offers corporations where you hold the required in-game role, and re-clicking within the
hour reports that the job is already queued rather than duplicating it. See
[Updating data from ESI](/docs/updating-data) for scheduling and for the usual reasons a page stays empty.

{% callout type="note" title="One Director's token covers the whole corporation" %}
This endpoint is answered per corporation, not per member, so exactly one Director needs to have
granted `esi-corporations.track_members.v1`. Requiring the scope of every member changes nothing if
no Director has granted it — and satisfies the endpoint the moment one has.
{% /callout %}
