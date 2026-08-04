---
title: Mails
description: How the character mails screen merges every authorised character's mail into one list and what happens when you open a mail whose body has not been fetched yet.
---

**Mails** is a single inbox across every character you are authorised to see: one list of headers,
newest first, with a reading pane beside it. It is the screen for reading what a pilot was told, and
for reconstructing a quoted thread.

{% .lead %}

**Permission required:** `mails`, and only for characters other than your own. Neither the list nor
the mail-content route carries permission middleware; instead the queries are scoped, so a signed-in
user always sees their own characters' mail, and the permission is what widens that set.

**ESI scope required:** `esi-mail.read_mail.v1`.

---

## What you see

The page header is **Character Mails**, with **Select Character** and **Update** buttons. On a window
1280 px wide or more, the mail list sits in its own column beside the page content and the reading pane
occupies the main area; nothing is selected when the page opens, so the pane starts empty — click a
header to fill it. Narrower windows behave differently, and one band of widths shows no list at all:
see [Viewport breakpoints](/docs/character/mails#viewport-breakpoints).

Each header row shows the sender's portrait and name, a relative timestamp, and the subject. That is
all it shows.

{% figure src="/images/character/mails.png" alt="The Character Mails page with a scrolling column of mail headers on the left, each with a timestamp and subject, and an empty reading area on the right" caption="Mail headers scroll in their own column; the reading pane stays empty until you select one." /%}

The list paginates as you scroll, and its scroll position is preserved when the next page merges in.

## One list, not one list per character

Unlike assets, contracts or wallets, this screen does **not** group by character. It is one query:
every stored mail that has a recipient among the authorised characters, ordered by timestamp
descending.

Two consequences follow, and both surprise people:

- A mail sent to two of your characters appears **once**, not twice. Mails are stored per mail id,
  not per recipient.
- The list does not tell you **which** of your characters received a mail. You have to open it and
  read the recipients.

The list also shows no read/unread state. Whether a mail was read in game is stored, but the header
row does not use it.

## Reading a mail

Selecting a header fetches that mail and renders the whole **thread**, not just the top message. The
stored body is split on EVE's quote separator, so a forwarded or replied-to chain becomes a stack of
messages. Each message in the stack renders five things:

- **Subject** — as that message's own heading, above the fields below it. The top message uses the
  stored subject; a quoted message's comes from the first line of its quoted block, so it can be blank
  or odd if EVE laid the quote out differently than expected;
- **From** — the sender as a resolved entity;
- **Received** — the timestamp in UTC, plus a relative time;
- **Recipients** — every recipient as a resolved entity;
- **Message** — the mail body, rendered as the EVE mail HTML it is.

The first message in the stack uses the stored header data. The quoted ones only carry *names* in the
body text, so those names are resolved to ids against ESI at the moment you open the mail. A name
that cannot be resolved is dropped from the recipient list of that quoted message.

Authorisation is enforced on this fetch too: unless you are a superuser, a mail is only returned if
one of its recipients is a character you are authorised for. Anything else is a 404.

## When the body has not been fetched yet

Mail headers and mail bodies arrive separately. The header update stores subjects, senders,
timestamps and recipients, and then queues a **separate body job per mail** that has no body yet. A
mail can therefore exist in the list — correct sender, correct subject — with no body stored.

{% callout type="warning" title="The body may say it has not been fetched yet" %}
If you open a mail before its body job has run, the message renders literally as
*mail body has not been fetched yet.* That is not an error and not a permission problem: the header
arrived and the body job is still queued (or failed). Give the queue time, or check it. Because the
thread splitting works on the body, such a mail also shows no quoted messages.
{% /callout %}

## Viewport breakpoints

The list exists twice — an accordion and a column in the layout's aside — and the two copies do not
meet. The accordion is hidden from **1024 px** upwards. The aside only appears from **1280 px**. The
reading pane appears from **768 px**.

| Window width | What renders |
| --- | --- |
| below 768 px | the accordion. Each header expands in place and fetches its mail on expand |
| 768 px – 1023 px | the accordion. The reading pane's slot is present but the accordion never fills it, so it stays invisible |
| 1024 px – 1279 px | **no list at all** |
| 1280 px and up | the aside list plus the reading pane. Clicking a header fills the pane |

{% callout type="warning" title="Between 1024 px and 1280 px there is no mail list" %}
In that band the accordion has already been hidden and the aside column has not yet been shown, so the
page renders its header, the scope banner, and nothing else. There is no error and no empty state to
explain it.

It is not a permission problem and not missing data. Widen the window past 1280 px, or narrow it below
1024 px, and the mail comes back. A half-width window on a 2560 px display lands squarely in this band,
which is how most people meet it.
{% /callout %}

Only the aside list can fill the reading pane. The accordion renders each mail inside its own expanded
row instead, so on anything below 1280 px the main reading area is never used.

## Selecting characters

By default the list covers **your own characters**. **Select Character** widens that; an id you are not
authorised for is dropped before any mail is read.

Two things about the picker's contents are worth knowing:

- **A character with no stored mail is not offered.** The candidate list is filtered to characters that
  already have at least one stored mail, so a character you are authorised for but who has never been
  updated does not appear in the picker at all.
- **Characters with an open application to you are offered anyway**, whether or not a role grants you
  `mails` over them.

See [Characters and accounts](/docs/concepts/characters-and-accounts).

## Refreshing the data

Headers and bodies are both stored data. **Update** queues a mail-header update for one character, which
then queues the missing bodies, and refuses a re-queue within the hour. See
[Updating data from ESI](/docs/updating-data).

A **Missing scopes warning** banner names each of *your own* characters lacking `esi-mail.read_mail.v1`,
with a **Fix** button that sends it through SSO. Until that happens nothing was ever fetched for that
character, so its mail is legitimately absent from the list — see
[ESI scopes and compliance](/docs/concepts/sso-scopes).
