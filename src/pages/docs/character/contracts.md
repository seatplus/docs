---
title: Contracts
description: How the character contracts screen lists issuers, assignees and acceptors, what the details column shows, and how contract contents open as a modal or a full page.
---

**Contracts** lists the contracts each character is party to — issued, assigned, or accepted — with
price, reward, collateral, volume and status on the row, and the item list one click away. It is the
screen to reach for when you need to see what a pilot moved, to whom, and for how much.

{% .lead %}

**Permission required:** `contracts`, and only for characters other than your own. The list route
carries no permission middleware, so any signed-in user reaches `/character/contracts` and sees their
own characters. The permission widens the picker, and it is checked before the contract-details route
will show a contract belonging to a character you do not own.

**ESI scope required:** `esi-contracts.read_character_contracts.v1`.

---

## What you see

The page header is **Character Contracts**, with **Select Character** and **Update** buttons. Below
it, one card per character, each with its own scrolling table. Every card paginates independently and
loads the next page as you scroll inside it, so a character with thousands of contracts does not slow
down the others.

The table has four visible columns — **Issuer**, **Assignee**, **Type**, **Details** — plus an
unlabelled last column holding the expand control.

{% figure src="/images/character/contracts.png" alt="A Character Contracts card with a table of contracts showing issuer, assignee, contract type and a details column with status, price, reward and volume" caption="One card per character, each scrolling and paginating on its own. The Details column packs status, price, reward, title, collateral and volume." /%}

## Issuer, assignee and acceptor

**Both** of these columns can hold two entities, and the second one means something different in each.

**Issuer** shows one entity for a personal contract: the issuing character. For a contract issued **on
behalf of a corporation** it shows the issuing **corporation** first, and beneath it, smaller, the
**character who created it**. That smaller entity is what you want when you are asking who inside a
corporation set a contract up — the corporation is the party to the contract, the character is its
author.

**Assignee** shows the assignee first, and adds a second, smaller entity beneath it for the
**acceptor** — but only when there is an acceptor (a non-zero id) and it differs from the assignee. A
public contract nobody has taken, or one accepted by the entity it was assigned to, shows a single
entity.

{% figure src="/images/character/contracts-assignee-acceptor.png" alt="Contract rows where the Assignee cell shows a large primary entity and a smaller second entity beneath it" caption="The smaller entity under the assignee is the acceptor. It only appears when someone other than the assignee accepted the contract." /%}

So a smaller second line reads as *"issued for this corporation, by this character"* under **Issuer**,
and as *"accepted by someone other than the assignee"* under **Assignee**. Same visual treatment, two
unrelated meanings — check which column you are in before drawing a conclusion.

## Type and locations

The **Type** cell shows the raw ESI contract type — `item_exchange`, `courier`, `auction`, `loan` —
and the location it concerns:

- for everything except a courier contract, one location: where the contract sits;
- for a courier contract, two: **Start** and **End**.

A location Seatplus cannot resolve renders as `unknown`. Since courier contracts are exactly the case
where you care about both endpoints, an unresolved structure hurts most here.

## The details column

The **Details** cell stacks whichever of these apply to the contract:

| Field | When it appears |
| --- | --- |
| status | always — the raw ESI status, e.g. `outstanding`, `in_progress` |
| Price | always; rendered in red when the price is zero |
| Reward | only when greater than zero |
| title | only when the contract has one |
| Collateral | only when greater than zero |
| Volume | only when greater than zero |

Because the zero-valued fields are omitted rather than shown as `0`, two rows can look structurally
different while describing the same kind of contract.

## Contract contents

The expand icon in the last column appears **only when the contract has items**. Clicking it fetches
the contract and opens a **Contract Details** modal with the item list.

That icon is also a real link, to `/character/contracts/{character_id}/contract/{contract_id}`.
Visiting that URL directly — a pasted link, or a new tab — renders a full **Contract Details** page
with a breadcrumb back to Character Contracts, instead of the modal. Same anchor, two presentations.

{% callout type="note" title="An item-less contract has no expand control and an empty detail page" %}
A contract with no items (a plain ISK loan, for instance) shows no expand icon at all — the row is
the whole story. Navigating to its detail URL by hand also renders nothing but the page header,
because the details component is only mounted when the contract has items.
{% /callout %}

## Characters with no contracts

A card is only built for a character that has at least one stored contract. A character with none
produces no card, so a page that is empty below the header means nothing has been fetched (or nothing
exists) for any of the selected characters.

## Selecting characters

You see **your own characters** by default. **Select Character** widens that, and a submitted id you are
not authorised for is dropped by the query rather than honoured.

Two things about the picker's contents catch people out:

- **A character with no stored contracts is not offered.** The candidate list is filtered to characters
  that already have at least one stored contract, so a character you are authorised for but who has
  never been updated is missing from the picker — the same symptom as the empty page described above,
  one step earlier.
- **Characters with an open application to you are offered anyway**, whether or not a role grants you
  `contracts` over them.

See [Characters and accounts](/docs/concepts/characters-and-accounts).

## Refreshing the data

The list is stored data, never a live ESI read. **Update** queues a contracts update for one character
and refuses a re-queue for that character within the hour. See
[Updating data from ESI](/docs/updating-data).

A **Missing scopes warning** banner names each of *your own* characters missing
`esi-contracts.read_character_contracts.v1`, with a **Fix** button that sends it through SSO. A missing
scope means the contracts were never fetched, so an empty screen is legitimate — see
[ESI scopes and compliance](/docs/concepts/sso-scopes).
