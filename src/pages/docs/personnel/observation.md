---
title: Employment observation
description: The account-level view of a corporation's members — scope compliance, last activity and employment status — and why a corporation with no configured scopes never appears.
---

**Personnel → Observation** is the account-level view of the people in your corporations: how many of
each account's characters have granted the scopes you require, when those characters were last in
game, and where they stand in their employment. This is the feature older documentation called
**Corporation Member Compliance** — same job, reorganised around the account and the employment
record rather than the character.

{% .lead %}

**Route:** `/employment`

**Permission required:** `view member compliance`, or an in-game `Director` role. Either one is
enough — the route accepts the permission *or* the role.

**ESI scope required:** none for compliance itself, which is read from stored tokens. The **last
logon** column comes from corporation member tracking, so it needs
`esi-corporations.track_members.v1` on a `Director`'s token in each corporation — without it, every
character reads *(no activity)*.

---

## A corporation with no required scopes does not appear

This is the first thing to check when a corporation is missing, and it catches nearly everyone.

The index only lists a corporation if **that corporation, or its alliance, has SSO scopes
configured**. The reasoning is that compliance is measured against a requirement: with no required
scopes there is nothing to be compliant against, and every member would show as trivially compliant
forever. Rather than fill the page with that noise, Seatplus leaves the corporation out entirely.

With none of your corporations configured you get the empty state — *Nothing to observe*, with the
explanation that no corporation or alliance SSO scopes are configured for the corporations you manage.
The fix is not a permission change; it is to configure a scope requirement. See
[ESI scopes and compliance](/docs/concepts/sso-scopes).

Beyond that filter, the list is scoped to the corporations you may observe: those where one of your
characters holds `Director`, **plus** those reachable through a control group carrying
`view member compliance`. Unlike the corporation wallet and member tracking pages, affiliated
corporations show up here without you having to select them. A superuser sees every corporation that
has scopes configured.

## What you see

{% figure src="/images/personnel/observation.png" alt="The Observation page showing a corporation card with member rows, each with a compliance count, a status pill and a missing-scopes badge" caption="One card per observable corporation, each with a search box and a row per member account." /%}

Each card is headed with the corporation's ticker and name, and on the right an **unlabelled** text input.
There is no visible label at all — the only hint is its placeholder, *Search member…*, which disappears
the moment you type. It filters the loaded list case-insensitively against the main character's name or
any of the listed characters' names.

The member list is loaded after the cards, so you will briefly see *Loading members…*. If the list comes
back empty — because your search matched nothing, or because the corporation has no observable member
accounts — the card reads *No members found.* instead.

A row is an **account**, not a character:

| Part of the row | What it shows |
| --- | --- |
| Portrait and name | The account's main character |
| Compliance count | `N/M characters compliant` — of that account's characters **in this corporation** |
| Per-character note | Each of those characters by name, with their last logon as *(today)*, *(Nd ago)* — no space before the `d` — or *(no activity)* |
| Status pill | The employment status for this account in this corporation, if there is a record |
| Compliance badge | **Compliant**, or a count of what is missing |
| **Inspect** | Opens the inspection view for this account |

Only the account's characters **in that corporation** are counted and listed. An alt in an unrelated
corporation does not appear in the row — though, as described below, it can still affect what the
listed characters are required to grant.

{% callout type="warning" title="The badge counts characters, not scopes" %}
The amber badge reads *N missing scopes*, but the number is the count of **characters with at least
one scope missing**, not the number of missing scopes. An account showing *2 missing scopes* has two
non-compliant characters, which between them might be short one scope or twenty. Open **Inspect** or
the account's own scope prompt to see the actual scope list.
{% /callout %}

## Employment status

The pill shows the status of the employment record for that account in that corporation. Three values
exist:

| Status | Meaning |
| --- | --- |
| `active` | Currently employed. Written when an application clears its final review stage |
| `suspended` | Employment suspended |
| `alumni` | Former member |

Only `active` is written by the application today — it is set when
[a review is accepted at the final stage](/docs/recruitment/reviewing). Nothing in the current release
transitions a record to `suspended` or `alumni`.

{% callout type="note" title="No pill is normal" %}
The status lookup only matches **account-level** employment records. A member who was hired through a
single-character application has a character-level record instead, and a member who was already in the
corporation before Seatplus knew about them has no record at all. Both render with no pill, and both are
otherwise observed exactly like everyone else.
{% /callout %}

## How compliance is computed

Per character, Seatplus builds a required set and compares it against what the token actually carries.

**Required** is the union of:

- the **global** scope entry, which applies to the whole instance;
- the scopes configured on that **character's corporation**;
- the scopes configured on that corporation's **alliance**;
- every **`user`-type** scope entry attached to *any* corporation or alliance of *any* character on
  the account;
- while an application is open, the applied-to corporation's and its alliance's scopes.

**Granted** is the scope list on the character's current refresh token. **Missing** is required minus
granted, and a character is compliant when nothing is missing.

The fourth item is the one that surprises people. It is how a requirement reaches characters in
corporations you have never configured: if one character on an account sits in a corporation with a
`user`-type entry, every character on that account inherits it — which is exactly what the `user`
type is for, and exactly why a member can be non-compliant on an alt in a corporation you do not run.

{% callout type="warning" title="No token means no scopes" %}
A character with no refresh token counts as having granted **nothing**, so every required scope is
missing for them. Revoking or losing a token makes a character maximally non-compliant rather than
exempt.
{% /callout %}

See [ESI scopes and compliance](/docs/concepts/sso-scopes) for how to configure the three requirement
types, and [Characters and accounts](/docs/concepts/characters-and-accounts) for what an account is.

## Inspecting a member

**Inspect** opens `/employment/{corporation_id}/member/{user}` and re-checks that you may observe that
corporation. It then reuses the **same inspection tabs as recruitment review** — Log, Assets,
Contracts, Wallets, Contacts, Corporation History, Skills and Mails — over the account's characters in
this corporation.

{% figure src="/images/personnel/observation-inspect.png" alt="The employment inspect view with the inspection tab bar above a member's data" caption="The inspection tabs, identical to the ones a recruiter uses. Assets and Contracts are the two a watchlist affects; the Wallets tab has none." /%}

Two differences from the recruitment version are worth knowing:

- The view opens on the **Log** tab, and that tab is **empty here**. The log belongs to an
  application, and an employed member is not an applicant. Switch to Assets, Wallets or Contracts.
- Assets and Contracts are compared against **the corporation's watchlist**, which is the watchlist
  from that corporation's job posting. A corporation with no posting has no watchlist. See
  [Job postings and review stages](/docs/recruitment/job-postings).

The **Wallets** tab has no watchlist behind it at all. It renders the ref-type filter, the balance chart,
the journal and the transactions for each character, exactly as the
[character wallet page](/docs/character/wallet) does.

A tab can be empty for a legitimate reason: if the character's token never carried the relevant scope,
that data was never fetched. That is a compliance finding, not a fault.

### Sub-tabs on the Assets and Contracts tabs

The two tabs handle the watchlist differently, and both are easy to misread.

**Assets** always has a sub-tab bar, watchlist or not. It always offers **All Assets** and **Assets in
Unknown Locations**; when the corporation has a watchlist, **Watchlisted Assets** is added in front of
those two.

**Contracts** has a sub-tab bar **only** when there is a watchlist, offering **Watchlisted Contracts** and
**All Contracts**. Without one there is no bar at all and you get every contract.

{% callout type="warning" title="With a watchlist you land on a filtered, often-empty view" %}
On both tabs the watchlisted sub-tab is not merely added — it is placed **first and selected by default**.
So the moment a corporation has a job posting with a watchlist, opening **Assets** or **Contracts** shows
you only the watchlisted items, and a member who happens to own none of them shows an empty tab.

That reads exactly like missing data or a missing scope, and it is neither. Click **All Assets** or
**All Contracts** before concluding anything about a member.
{% /callout %}

## The review-user permission is not a route gate

`member compliance: review user` grants access to no page. It is a **fallback inside the
authorisation check on two detail routes**:

- `/character/assets/{character_id}/item/{item_id}`
- `/character/contracts/{character_id}/contract/{contract_id}`

Those routes normally demand the `assets` or `contracts` permission for the character in question.
When that check fails, holding `member compliance: review user` lets the request through anyway,
provided the character belongs to an account that (a) has a character in a corporation or alliance
carrying a `global`- or `user`-type scope entry, and (b) falls inside your affiliated set for that
permission — or you are a Director there.

In practice: give it to reviewers so they can drill into a single item or a single contract while
observing, without handing them the blanket `assets` and `contracts` permissions. Without it the
inspection lists still render; only the per-item and per-contract detail views are refused.

## Refreshing the data

Two different pipelines feed this page.

- **Compliance** is computed live from stored refresh tokens and your scope configuration. It needs no
  update job, and a scope configuration change takes effect immediately.
- **Last logon** comes from corporation member tracking, which the **Update Corporation** job pulls.
  If every character reads *(no activity)*, member tracking has not run for that corporation — or no
  Director has granted `esi-corporations.track_members.v1`. See
  [Member tracking](/docs/personnel/member-tracking).

Everything on the inspection tabs comes from the **Update Character** job for the characters
concerned. This page has no Update button of its own; refresh those characters from their own pages or
from the review screen.

See [Updating data from ESI](/docs/updating-data).
