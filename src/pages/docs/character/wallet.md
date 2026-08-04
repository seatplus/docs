---
title: Wallet
description: How the character wallets screen shows the journal, market transactions and a balance chart, and how the ref-type filter narrows the journal.
---

**Wallets** is the ISK view of a character: the wallet journal, the market transactions, and a balance
chart, one set per character. It is where you check where the money came from and what it was spent on.

{% .lead %}

**Permission required:** `wallet_journals` — note the name, it is not `wallet` — and only for
characters other than your own. `/character/wallets` carries no permission middleware, so every
signed-in user reaches it and sees their own characters; the permission is what widens the picker.

**ESI scope required:** `esi-wallet.read_character_wallet.v1`.

For corporation wallets — a different permission, different scopes and a corporation role requirement —
see [Corporation wallet](/docs/corporation/wallet).

---

## What you see

The page header is **Character Wallets**, with **Select Character** and **Update** buttons. Below it a
single filter card, then one set of three cards per character: a full-width **Balance** chart, and under
it the **Journal** and **Transaction** cards side by side.

{% figure src="/images/character/wallet.png" alt="The Character Wallets page showing a ref-type filter, a balance line chart in ISK, and Journal and Transaction tables side by side" caption="Per character: a balance chart above, the journal and the market transactions below it." /%}

## The journal

The journal table has four columns — **Date**, **Type**, **Amount**, **Balance** — newest entry first,
and loads more rows as you scroll inside the card. The **Type** column is the entry's ESI ref type run
through Seatplus's translations; in English the translation is the raw ref type string, so you see
`bounty`, `insurance`, `contract_price` and the like.

Expanding a row with the chevron reveals what does not fit on it:

| Field | Content |
| --- | --- |
| Description | the journal entry's description |
| Reason | only shown when the entry has one |
| Sender | the first party of the transaction, as a resolved entity |
| Receiver | the second party, as a resolved entity |

## Filtering the journal by ref type

The filter card at the top of the page filters journals **by ref type**. Type into the box to narrow the
option list, then click an option to add it as a chip; the chip's × removes it again. Several chips
widen the result — an entry matching any selected ref type is kept.

The option list is neither free text nor every ref type EVE has. The server sends the distinct ref types
actually present in the journals you can see, sorted alphabetically, and the box narrows that list in
the browser.

A ref type you expected can be absent for four different reasons, and only the first is about your data:

- nothing in the journals you can see uses it;
- **you have not typed anything yet.** The list is not rendered at all while the box is empty, so an
  empty box shows no options rather than all of them. There is no way to browse the full list;
- your text does not appear in the ref type. The narrowing is a case-insensitive **substring** match, so
  `price` does find `contract_price` — but a typo finds nothing;
- the list is **cut to the first 20 matches**. A short term such as `c` can push what you want off the
  end; type more of it.

Ref types you have already added as a chip are removed from the options, so a selected one will not
reappear.

{% figure src="/images/character/wallet-filter.png" alt="The wallet page with the ref type filter holding a bounty chip and the journal below showing only bounty entries" caption="Selecting a ref type reloads every character's journal to only that type. The chip below the box is the active filter." /%}

{% callout type="note" title="The filter is page-wide, and journal-only" %}
There is one filter for the whole page, not one per character: adding a chip re-filters **every**
character's journal card at once. It also touches nothing else — the transactions table and the balance
chart are not filtered, so a journal narrowed to `bounty` still sits next to a complete transaction list
and an unchanged chart.
{% /callout %}

## Transactions

The transaction table covers market transactions, newest first, with its own infinite scroll and no
filter. Its columns are the date, whether the character **Bought** or **Sold**, the item type with its
group, and the **Total** — computed as quantity × unit price rather than taken from ESI.

Expanding a row shows the **Unit Price**, the **Quantity**, whether the transaction was personal
(**Is personal**), the **Location** it happened in, and the **Client** on the other side.

## The balance chart

The chart is a line of ISK over time, built from the journal rather than from a series of balance
snapshots. It is a SQL union of two selects — and the **30-row cap is applied to the union**, not to each
side:

- the journal side is one row per day on which the journal has entries, whose value is the **average** of
  the balances recorded by that day's entries, newest day first, itself limited to 30; and
- the balance side is a single row for the character's currently stored wallet balance.

Because the cap sits on the union, the current-balance row **competes for one of the 30 slots** rather
than being added on top. The chart is therefore at most 30 points in total: the most recent journal days,
minus whichever row the balance displaces. The union carries no outer ordering, so which row loses out is
up to the database rather than something you can predict from the page.

Two things follow. A day the character made no wallet-affecting action produces no point, so the line
jumps across gaps; and a wallet with no journal activity charts as almost nothing even though the balance
is known. The chart loads after the rest of the page, so it appears a moment late.

## Selecting characters

By default you get **your own characters**, one set of cards each. **Select Character** is meant to widen
that to the characters a role grants you `wallet_journals` over — plus, as on every character page, any
character with an **open application to you**, which needs no role at all.

{% callout type="warning" title="The character picker on this page cannot build its list" %}
The picker narrows its candidates by looking up a relation named after the permission string, which is
also what normally hides characters with no stored data of that type from the list. On this page the
permission is `wallet_journals` while the relation on the character model is `walletJournals`, and
nothing maps one name to the other — so there is no relation for the filter to resolve.

Expect the picker's list request to **fail** rather than return characters. The page itself is unaffected
and still shows your own characters. In the meantime you can reach a wallet you are authorised for by
putting `character_ids` in the URL by hand: the query still authorises every id it is given, so this
grants you nothing you were not already entitled to.
{% /callout %}

Whatever route you take, the selection is only a filter — a `character_id` you are not authorised for is
dropped by the query. See [Characters and accounts](/docs/concepts/characters-and-accounts).

## Refreshing the data

Journal, transactions and balance are all stored data. **Update** queues a wallet update for one
character — journal, transactions and balance together — and refuses a re-queue for that character within
the hour. See [Updating data from ESI](/docs/updating-data).

A **Missing scopes warning** banner names each of *your own* characters missing
`esi-wallet.read_character_wallet.v1`, with a **Fix** button that sends it through SSO. Until that happens
nothing was ever fetched for that wallet, so an empty journal, an empty transaction list and a flat chart
are all legitimate. See [ESI scopes and compliance](/docs/concepts/sso-scopes).
