---
title: Characters and accounts
description: How Seatplus maps EVE characters onto user accounts, what a main character is for, and how the entity picker decides which characters a page shows.
---

Almost every confusing thing about Seatplus becomes obvious once you understand its ownership model.
This page explains the difference between an account, a character and an affiliation, and how the
app decides whose data to put on a page.

{% .lead %}

---

## An account owns characters

When you sign in with EVE SSO for the first time, Seatplus creates a **user account** and links the
character you signed in with to it. Signing in again with a *different* character while already
logged in links that character to the same account, rather than creating a second one. That is how
you attach your alts.

One of your characters is the **main character**. It is what represents you throughout the interface — in
the reviewer queue, in Observation, in the control-group member list — and you can change which one it
is on your user settings page, reached by clicking your own character block at the very bottom of the
sidebar. It is not under the Settings menu.

An account is the unit that matters for most decisions:

- **Permissions belong to the account**, never to an individual character.
- A **whole account** job posting requires ESI scopes from every character you own.
- Control-group membership is per account.

{% figure src="/images/concepts/dashboard-multiple-characters.png" alt="The Seatplus dashboard showing a card for each character on the account" caption="The dashboard renders one card per character the account owns — not just the main." /%}

---

## Owned versus affiliated

Seatplus distinguishes two reasons you might be allowed to see a character or corporation:

**Owned** — the character is linked to your account. You always have access to your own characters'
data, subject only to whether the relevant ESI scope was granted.

**Affiliated** — someone has granted your account access to an entity you do not own. There are two
independent routes:

- **In-game corporation roles.** If one of your characters holds a role such as `Accountant` or
  `Director` in a corporation, your account inherits corporation-scoped access there. **Director
  implies every role**, so a Director gets everything a role-gated page offers.
- **Control groups.** A group holds permissions and declares which entities those permissions apply
  to. Being an active member of such a group grants you access to those entities. See
  [Permissions and control groups](/docs/concepts/permissions).

The distinction shows up literally in the interface: the update panel lists "Your characters" and
"Your corporations" separately from "Affiliated characters" and "Affiliated corporations".

{% callout type="note" title="Corporation roles need a scope of their own" %}
Seatplus can only read a character's in-game corporation roles if that character's token carries the
corporation-roles scope (`esi-characters.read_corporation_roles.v1`). Without it, a Director looks like an
ordinary member and gets no corporation access.

The SSO settings screen adds this scope for you whenever a selected scope's name contains
"corporation" — which covers the corporation scopes, and also catches the character *Contacts* group,
since that includes the corporation-contacts scope.
{% /callout %}

---

## The entity picker

Every character and corporation page defaults to showing **your own** entities. The **Select
character** / **Select corporation** button in the page header opens a picker so you can widen or
narrow that.

{% figure src="/images/concepts/entity-picker.png" alt="The entity selection slide-over listing the characters available to the current user" caption="The picker lists exactly the entities you are authorised to see for that page's permission — nothing more." /%}

The list is built from the permission the page requires, so it differs from page to page: the
corporation wallet picker offers corporations where you hold `Accountant`, `Junior_Accountant` or
`Director`, while the assets picker offers characters covered by the `assets` permission.

Your selection is stored in the page's URL, so a filtered view is shareable and survives a reload.

{% figure src="/images/concepts/entity-picker-applied.png" alt="A page showing the selected-entity summary after a picker selection has been applied" caption="Once applied, the selection is summarised in the page header and reflected in the URL." /%}

{% callout type="note" title="The picker is a filter, never an escalation" %}
Every page re-checks your selection against what you are actually authorised to see, so editing
`character_ids` in the URL by hand cannot show you someone else's data. If you select an entity and
see nothing, the cause is missing data or a missing ESI scope — not the picker.
{% /callout %}

---

## Why a page can be empty

There are four distinct reasons, and telling them apart saves a lot of time:

| Symptom | Cause |
| --- | --- |
| The sidebar entry is missing entirely | The entry requires a permission your account lacks, and none of your characters holds a qualifying in-game role. Note this never applies to the **Character** entries or the Job Portal — those carry no permission and are visible to everyone |
| The page loads but the picker offers only your own characters | The character screens are open to every signed-in user; the permission is what *widens* them to other people's characters. Without it you see only what you own |
| An entity is listed but its data is empty | The character's token does not carry the required ESI scope, so Seatplus never fetched that data. See [ESI scopes and compliance](/docs/concepts/sso-scopes) |
| Data is present but stale | The scheduled update has not run recently, or ESI's own cache has not expired. See [Updating data from ESI](/docs/updating-data) |

{% callout type="warning" title="Permission changes can take up to five minutes to appear" %}
Each account's resolved permissions are cached for about five minutes.

Some changes clear that cache immediately: adding or removing a group member, editing what a group
applies to, and changing SSO scope requirements. Two notable changes do **not**:

- **Changing which permissions a group grants** — up to five minutes.
- **Linking an additional character to your account** — the record of which characters your account owns
  stays stale for up to five minutes, so a newly added alt can be missing from pages and pickers.

If a change appears not to have taken effect, wait five minutes before troubleshooting anything else.
{% /callout %}
