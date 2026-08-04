---
title: Corporation wallet
description: The per-division view of a corporation's wallet journal, transactions and balance history, and what it takes for a division to appear at all.
---

**Corporation → Wallets** shows a corporation's money: one block per corporation **wallet division**,
each with its own journal, its own transaction list and its own balance chart. This page covers what
a block contains, which corporations you get to see, and the two ESI scopes that have to exist on
somebody's token before any of it is populated.

{% .lead %}

**Route:** `/corporation/wallet`

**Permission required:** `wallet_journals`, or an in-game corporation role of `Accountant` or
`Junior_Accountant` in the corporation. Either one is enough — the route accepts the permission *or*
the role. `Director` satisfies both roles.

**ESI scopes required:** `esi-wallet.read_corporation_wallets.v1` and
`esi-corporations.read_divisions.v1`, on the refresh token of **some member of that corporation** —
not necessarily yours. The wallet endpoints are answered by a token belonging to a character with
`Accountant`, `Junior_Accountant` or `Director`; the divisions endpoint needs a `Director`.

---

## What you see

{% figure src="/images/corporation/wallet.png" alt="The Corporation Wallets page showing a wallet division card with a balance chart, a journal list and a transaction list" caption="One block per wallet division: a heading, then three separate cards. The balance chart spans the full width; the journal and transactions sit side by side beneath it." /%}

The page header carries an **Update** button and a **Select Corporation** button. Below it, every
wallet division of every corporation you may see contributes a block to the page.

A block is **not one card**. It is a bare heading carrying the division's name, followed by **three
independent cards** with nothing enclosing them:

| Card | Contents |
| --- | --- |
| **Balance** | A line chart of the division's daily average balance, in ISK. Spans the full width |
| **Journal** | Date, type, amount and balance per entry, newest first |
| **Transaction** | Date, whether it was bought or sold, the item type, and the total |

{% callout type="warning" title="An unnamed division has no visible boundary" %}
That heading is the only thing separating one division's three cards from the next division's. EVE only
returns a name for a division that has been renamed in game, so the master wallet is normally stored with
an empty name — and its heading renders as an empty line.

With several divisions on the page and no card wrapping each group, it is easy to read one division's
journal next to another division's balance without noticing. Rename your divisions in game, or count
blocks from the top.
{% /callout %}

Journal and transaction rows both expand. A journal row reveals its **description**, its **reason**
if there is one, and the **sender** and **receiver** resolved to names. A transaction row reveals
**unit price**, **quantity**, whether it was a personal trade (**Is personal**), the **location** it
happened at, and the **client** on the other side — the same five fields as the
[character wallet](/docs/character/wallet).

Both lists scroll infinitely, and each division's list keeps its own scroll position — scrolling one
division's journal does not advance another's.

## One block per wallet division

The cards are driven by the **corporation divisions** Seatplus has stored, not by the wallet data
itself. A division only exists in Seatplus once the divisions endpoint has been read, and that endpoint
is only called when a character in the corporation holds `Director` **and** has granted
`esi-corporations.read_divisions.v1`.

{% callout type="warning" title="No Director token means no cards at all" %}
Wallet journal and transaction data can be fetched with an `Accountant` token, but the division list
cannot. If nobody in the corporation is a Director with the divisions scope, Seatplus has no divisions
to render and the page comes up empty — even though the journal rows may already be in the database.

The **Update** button cannot fix this, because it does not queue the divisions job. See
[Refreshing the data](/docs/corporation/wallet#refreshing-the-data).
{% /callout %}

An unnamed division is stored with an empty name, so its heading renders blank; the three cards under it
are still there and still correct, only the label is missing.

## Which corporations you see

By default the page lists **the corporations you operate**: those where one of your own characters is
a member and holds `Accountant`, `Junior_Accountant` or `Director`.

Corporations you can reach through a control group's `wallet_journals` permission — an alliance-wide
accountants group, for instance — are **not** in that default list. Use **Select Corporation** to
pick them; the picker writes your choice into the page URL, and the server honours a selection only
for corporations you are actually affiliated with, so a hand-edited URL gains you nothing.

Seatplus only knows a character's in-game roles if that character's token carries
`esi-characters.read_corporation_roles.v1`. Without it, your Accountant looks role-less and their
corporation never appears. See [ESI scopes and compliance](/docs/concepts/sso-scopes) and
[Permissions and control groups](/docs/concepts/permissions).

{% callout type="warning" title="The sidebar entry and the page disagree" %}
The page itself accepts the `wallet_journals` permission, but the **Corporation → Wallets** menu
entry is shown for the permission named `wallets` or for an `Accountant` / `Junior_Accountant` /
`Director` role. If you give a group `wallet_journals` and nothing else, its members can open
`/corporation/wallet` directly but will not find a link to it in the sidebar.
{% /callout %}

## The balance chart

The chart plots the **average balance per calendar day**, taken from the division's journal entries,
for the most recent 30 days that have entries. It is not read from EVE's wallet balance endpoint, so
a division with a stored balance but no journal rows yet charts as nothing. Quiet divisions produce a
sparse line: days without journal entries contribute no point.

## Refreshing the data

Corporation wallet data arrives with the scheduled **UpdateCorporation** job, which reads the divisions,
then the per-division balances, and from those queues one journal job and one transaction job per
division. Nothing is fetched when you open the page.

{% callout type="warning" title="The Update button does not fetch divisions" %}
**Update** in the header does **not** queue the UpdateCorporation batch. It dispatches the corporation
wallet job set, which is exactly two jobs: the corporation wallet journal job and the corporation balance
job. The divisions job is queued **only** by the scheduled UpdateCorporation batch.

That matters, because the failure mode described above — no cards at all — is a *divisions* problem, and
**Update** cannot touch it. Press it on an empty page and the panel will report a queued, finished job
while the page stays exactly as empty as before.

What that page needs is for **UpdateCorporation to run for that corporation**: add the schedule if it is
missing, or wait for the next run of an existing one. See
[Updating data from ESI](/docs/updating-data).
{% /callout %}

The panel behind **Update** only lists corporations where you hold the required in-game role, and
re-clicking within the hour reports that the job is already queued rather than duplicating it. For
scheduling, the queue and the usual reasons data goes missing, see
[Updating data from ESI](/docs/updating-data).

{% callout type="note" title="The amber scope banner nags every character" %}
The missing-scopes banner on this page compares **each of your own characters** against the
corporation wallet scopes plus `esi-characters.read_corporation_roles.v1`. Alts who will never be
accountants are listed too. Only one qualifying character per corporation actually has to grant the
wallet scopes; the banner is not a list of what is required of you.
{% /callout %}
