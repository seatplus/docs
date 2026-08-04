---
title: Contacts
description: How the character contacts screen shows a character's own standings side by side with the corporation and alliance standings for the same entity.
---

**Contacts** lists a character's personal contact list, and — this is the point of the screen — puts
the corporation's and the alliance's standing towards the same entity on the same row. That is what
makes it useful for spotting a pilot who is blue to something their corporation has set red.

{% .lead %}

**Permission required:** `contacts`, and only to look at characters other than your own.
`/character/contacts` carries no permission middleware, so every signed-in user reaches it and sees
their own characters; the permission is what widens the picker.

**ESI scopes required:** all three of the following. The last two are not optional extras — without
them the corporation and alliance columns have nothing to read.

| Scope | What it fills |
| --- | --- |
| `esi-characters.read_contacts.v1` | the character's own contacts and labels |
| `esi-corporations.read_contacts.v1` | the **Corporation standing** column |
| `esi-alliances.read_contacts.v1` | the **Alliance standing** column |

---

## What you see

The page header is **Character Contacts**, with **Select Character** and **Update** buttons. Below it
there is one card per character, headed by that character with a filter control on the right.

The table inside each card has five columns:

| Column | Content |
| --- | --- |
| Contact | the contacted entity — character, corporation, alliance or faction — with its portrait |
| Labels | the contact's labels from in-game, as chips |
| Standing | the standing **this character** has set |
| Corporation standing | what the character's corporation has set for the same entity |
| Alliance standing | what the character's alliance has set for the same entity |

Rows are sorted on three keys in order — the character's own **Standing**, then **Corporation
standing**, then **Alliance standing** — and the sorted result is reversed. So the highest personal
standings come first, and ties on that break on the corporation's value and then the alliance's. The
card scrolls internally rather than growing without limit.

{% figure src="/images/character/contacts.png" alt="A Character Contacts card for one character with a five-column table: Contact, Labels, Standing, Corporation standing, Alliance standing" caption="One card per character. The last two columns are the corporation's and alliance's own standings towards the same contact." /%}

## How the corporation and alliance standings are found

The two right-hand columns are not part of the character's contact list. Seatplus looks up the contact
lists belonging to the character's **current corporation** and its alliance, and then tries to find
the contact there by walking the contacted entity's affiliation in this order: alliance, then
corporation, then faction, then character. The first hit wins.

That has a consequence worth understanding before you act on the numbers:

{% callout type="warning" title="A corporation standing may not be about the contact itself" %}
Because the lookup starts at the contact's *alliance*, the value in **Corporation standing** is
whatever your corporation set for the first of the contact's affiliations it has an entry for. A
character contact can therefore show a corporation standing that your corporation actually set
against that character's alliance, not against the character. Treat the column as "what my
corporation thinks about this pilot's affiliation chain", not "what my corporation set for this
pilot".
{% /callout %}

`N.A.` in either column means no entry was found — either the corporation or alliance genuinely has
no standing on that chain, or those contact lists have never been fetched because the corp/alliance
scopes are missing.

## Filtering to disagreements

The control in each card header switches between **All contacts** and **Only With Standing Offset**.

*Only With Standing Offset* keeps a contact only when all of the following hold: at least one of the
corporation and alliance standings is known, the character's own standing is not zero, and that
standing differs from **both** the corporation and the alliance value (an unknown one counts as
zero). In other words it hides everything the character and their organisation agree on, and leaves
the disagreements.

## What "No contacts" means

*No contacts* is **not** the empty-contact-list state. A character with no stored contacts never gets a
card at all, as described below. The message appears inside a card whose **filtered** row list came out
empty, which happens for two reasons:

- **Only With Standing Offset** is selected and has removed every row. This is the usual one: the filter
  is strict, and a character who agrees with their corporation and alliance on everything filters down
  to nothing at all.
- The contacts have not arrived yet. They load after the page frame, so for a moment the card exists
  with an empty list.

Switch the filter back to **All contacts** before concluding anything from it.

## Characters with no contacts

The screen only builds a card for a character that has at least one stored contact. A character with
none — never fetched, or a genuinely empty contact list — produces no card at all, rather than an
empty one.

{% callout type="note" title="An empty page is not an error" %}
If the whole page below the header is blank, none of the selected characters has a single stored
contact. That is almost always a missing scope or an update that has not run yet, not a bug.
{% /callout %}

## Selecting characters

By default you see **your own characters** only. **Select Character** widens that, and the selection is
a filter rather than an escalation: an id you are not authorised for is dropped before anything is read.

Two things about the picker's contents are worth knowing:

- **A character with no stored contacts is not offered.** The candidate list is filtered to characters
  that already have at least one stored contact — the same condition that decides whether a card is
  built. A character you are authorised for but who has never been updated is absent from the picker.
- **Characters with an open application to you are offered anyway**, whether or not a role grants you
  `contacts` over them.

See [Characters and accounts](/docs/concepts/characters-and-accounts).

## Refreshing the data

The page renders stored data only. **Update** queues a contacts update for one character — the
character's own contacts plus, where the scopes allow, its corporation's and alliance's lists — and
refuses a re-queue within the hour. See [Updating data from ESI](/docs/updating-data).

A **Missing scopes warning** banner names each of *your own* characters lacking one of the three contact
scopes, with a **Fix** button that sends it through SSO. A missing scope means the data was never
fetched, so the column or the whole card is legitimately empty — see
[ESI scopes and compliance](/docs/concepts/sso-scopes).
