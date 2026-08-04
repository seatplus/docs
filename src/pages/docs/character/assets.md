---
title: Assets
description: How the character assets screen lists locations, searches and filters them, drills into containers, and deals with asset safety and unresolvable structures.
---

**Assets** answers one question: where is the stuff? It lists every location that holds an asset
belonging to the characters you are looking at, and lets you open each container down to the
individual module. Pilots use it to find their own hulls; recruiters and auditors use it, through the
character picker, on the characters they are authorised for.

{% .lead %}

**Permission required:** `assets` — but only to look at characters other than your own.
`/character/assets` carries no permission middleware: every signed-in user reaches it and sees their
own characters. The `assets` permission is what puts other people's characters into the picker, and
what the single-item page checks before it shows an item owned by a character you do not own.

**ESI scopes required:** `esi-assets.read_assets.v1` and `esi-universe.read_structures.v1`. The
second one is what lets Seatplus put a name on a player structure; without it, stations still resolve
but structures stay unknown.

---

## What you see

The page header is **Character Assets**, with **Select Character** and **Update** buttons. Below it
sits one filter card (search, region, solar system, compact-view toggle, and the currently selected
entities), and below that the location list.

Each location is a card: the location name as the heading, an item count underneath, and the
location's top-level items as rows. A row shows the item's own name, its type, its group — with
`(packaged)` appended when the item is not assembled — and its volume. When **your own account** owns
more than one character, a second portrait next to the item icon names the character holding the item.

{% figure src="/images/character/assets.png" alt="A scrolled list of asset location cards, each with a location heading, an item count and one item row" caption="The location list. Each card is one location; the rows under it are that location's top-level items." /%}

{% callout type="warning" title="The owner portrait depends on your account, not on the list" %}
That second portrait is shown when the signed-in account owns more than one character. That is the
whole condition — it ignores how many characters the list actually covers.

So a recruiter whose account has a single character, looking at five affiliated characters, gets **no**
owner portrait on any row and no way to tell whose asset is whose from the list. Meanwhile a two-alt
pilot looking at one character gets a redundant portrait on every row. If you need attribution and do
not have it, select one character at a time.
{% /callout %}

## The location list and infinite scroll

Locations are matched **flat**, not by walking a tree. Every asset carries the id of the location it
ultimately sits in, so a location shows up if it holds a matching asset *at any depth* — a module
inside a container inside a ship inside a hangar puts that hangar in the list.

The list is paginated and loads the next page as you scroll. The items inside a card are fetched
separately, per location, when that card comes within about 300 pixels of the viewport; until then
you see a placeholder instead of rows. Long locations paginate internally too, loading more rows as
you scroll through the card.

Locations are ordered by their EVE location id. That is neither alphabetical, nor by system, nor by
distance — do not read anything into the order.

{% callout type="note" title="The item count is the top-level count" %}
The count under a location heading is the number of *top-level* items there — the things sitting
directly in that hangar or bay. Everything nested inside them is not counted. When a filter is
active, the count is the number of top-level items that match.
{% /callout %}

## Search

The search box matches against four things per asset: the item's own name (the name you gave a
container or ship), its type name, its group name and its category name.

Matching is a **prefix** match, not a substring match. `rift` finds a Rifter; `ifter` finds nothing.
Terms are split on spaces and each term is matched on its own, so several terms broaden the result
rather than narrowing it.

{% callout type="warning" title="A term containing a space can never match anything" %}
The four columns the search runs against are stored with every non-alphanumeric character stripped
out, spaces included — *Blue Ice* is indexed as `BlueIce`. A term with a space in it therefore cannot
match any stored value, ever.

Quoting does hold a phrase together as one term, which is exactly what makes it useless here: the
quoted term keeps its space and matches nothing. Single words are the only thing that works. Search
`blue`, or `ice`, and let the two terms broaden the result.
{% /callout %}

Searching only fires once you have typed three characters (or cleared the box), and is debounced by
half a second. While the reload is in flight the list dims and an *updating…* pill appears over it.

{% figure src="/images/character/assets-search.png" alt="The assets filter card with the term herp typed into the search box and a single matching location card below" caption="A search reduces the list to locations that hold a matching asset, and each card to the top-level items whose subtree contains the match." /%}

A search does two things at once: it decides which locations appear, and it decides which top-level
items appear inside them. A container is shown when something *inside it* matches, so you may see a
container whose own name and type mean nothing to your search term — the match is deeper in.

## Region and system filters

**Region** and **Solar System** are multiselects, not free-text fields. Their options are built from
the locations that the currently selected characters actually have assets in, so an empty option
list means those characters have nothing anywhere resolvable. Selecting a value reloads immediately,
without the search box's three-character or debounce rules.

{% figure src="/images/character/assets-region-filter.png" alt="The Region multiselect open with one option selected and highlighted, and the filtered location list below" caption="The region and system filters only offer regions and systems that appear in the selected characters' own locations." /%}

Both filters work through the location's resolved station or structure and its solar system. A
location Seatplus cannot resolve has no system, so **any** region or system filter removes every
unknown structure from the list. If you are hunting for assets in a structure you no longer have
docking access to, clear these two filters.

{% callout type="warning" title="Filters are not written into the URL, but they are read from it" %}
Selections you make in the filter card are sent to the server and kept out of the browser URL — the
address stays `/character/assets`. So the UI gives you no shareable filtered view, and a reload starts
from an unfiltered list. The character selection is the exception: that one does live in the URL.

Hand-written query parameters are a different matter. The controller reads `search`, `systems`,
`regions`, `types`, `groups`, `categories` and `only_unknown_locations` off the query string, so
`?regions[]=10000002` really is honoured and really does filter the list.

What does not happen is the controls catching up. Only `search` hydrates its box; the region and system
multiselects always initialise empty. A bookmarked or pasted filter link therefore gives you a filtered
list with **no chips showing why**, and the only way to clear a filter you cannot see is to edit the
URL.
{% /callout %}

## Looking inside a container

A row whose type name is rendered in indigo, with an indigo chevron on the right, has contents.
Clicking anywhere on the row opens a **Contents** modal with one level down, fetched on demand. Rows
inside the modal behave the same way, so you can keep drilling.

{% figure src="/images/character/assets-contents-modal.png" alt="A Contents modal over the dimmed assets page, listing one item found inside the clicked container" caption="Clicking a row with contents opens one level of that container. The modal shows everything inside — it is not narrowed by your search." /%}

The modal is not filtered. Even when a search is active, opening a container shows all of its
contents, not just the matching ones.

## Deep links to a single item

The clickable row is a real anchor, and its target is a shareable URL for that one item:
`/character/assets/{character_id}/item/{item_id}`. Clicking it in the app opens the modal described
above; visiting the URL directly — pasting it to someone, or opening it in a new tab — renders a
full **item page** instead. Same link, two presentations.

The item page lays the contents out by slot rather than as a flat list: high, mid, low and rig slots,
subsystems, fighter tubes, fleet and ship hangars, specialized holds, the drone/fighter bay, and
everything else under **Cargo**. That makes it a fitting view for a ship. A breadcrumb takes you back
to Character Assets, and — when the item is itself inside another container — to that container.

{% figure src="/images/character/assets-deeplink.png" alt="The full item page for a single asset, showing its name, a Character Assets breadcrumb and a Cargo section with one item" caption="Visiting an item URL directly renders the full item page, with contents grouped by fitting slot and hold." /%}

This page is permission-checked per character. Your own characters always work; someone else's
requires the `assets` permission over that character, or the recruiter or member-compliance
fallbacks.

## Asset safety

**Asset Safety** is a virtual location. It has no row in the locations table and no system, so the
normal location query can never return it; instead it is prepended to the first page of the list
whenever one of the selected characters has an asset rooted there. It therefore always appears at
the very top.

{% figure src="/images/character/assets-asset-safety.png" alt="The assets page with an Asset Safety card at the top of the list holding one packaged Battleship" caption="Asset safety is injected as a virtual location at the top of page one whenever a matching asset is rooted in it." /%}

{% callout type="warning" title="Asset safety ignores the region and system filters" %}
The check that injects the Asset Safety card applies the character selection and your search term,
but *not* the region or system filters — it has no system to filter on. So a filtered list can still
be topped by an Asset Safety card that has nothing to do with the region you picked. That is
expected, not a stale render.
{% /callout %}

## Compact view

The **Compact view** toggle swaps the roomy rows for a dense table: Quantity, Type, Volume, Group,
and the drill-in chevron. Containers still open the same way; the type name is indigo when there is
something inside.

The choice is remembered in your browser's local storage (key `assets.compactView`) for a year, and
refreshed every time you flip it. It is per browser, not per account — it does not follow you to
another machine, and it is not part of the shared URL.

## Unknown structures

When Seatplus cannot resolve a location to a station or a structure, the card is headed
`Unknown Structure (<location id>)` and offers an **Add location information** button. It opens a
small form for a structure name plus a solar-system search, and files your answer as a suggestion.

Suggestions do not take effect on their own: someone holding the `manage manual locations`
permission has to accept one. Until then you see your own suggestion, and everyone else sees theirs
or the accepted one. See [Manual locations](/docs/corporation/manual-locations) for the review side.

If the structure later becomes resolvable through ESI, the manual entry is dropped and the real name
takes over.

## Selecting characters

The screen defaults to **your own characters** — nothing else, even if you are a director.
**Select Character** widens that, and writes `character_ids` into the URL; on this page the result is
also listed under **Selected Entities** in the filter card. Selecting is a filter, never an escalation:
an id you are not authorised for is dropped by the query, on the location list and on the per-location
item fetch alike.

Two things about what the picker offers are worth knowing, because they explain most "why can I not see
this character" questions:

- **A character with no stored assets is not in the picker.** The candidate list is filtered to
  characters that already have at least one stored asset, so a character you are fully authorised for
  but who has never been updated does not appear at all. This is the common case, and it looks
  identical to a permission problem.
- **Characters with an open application to you appear anyway.** Anyone whose account has an open
  application to a corporation you can accept or deny for is added to the list regardless of whether
  any role grants you `assets` over them.

See [Characters and accounts](/docs/concepts/characters-and-accounts) and
[Permissions and control groups](/docs/concepts/permissions).

## Refreshing the data

Nothing here reads ESI live — the page renders what the last update stored. **Update** queues an asset
update (the asset job plus the asset-name job) for one character, and refuses to re-queue the same
update for that character within the hour. See [Updating data from ESI](/docs/updating-data).

A **Missing scopes warning** banner names each of **your own** characters missing
`esi-assets.read_assets.v1` or `esi-universe.read_structures.v1`, with a **Fix** button that sends it
back through SSO. A missing scope means the data was never fetched at all, so the screen is
legitimately empty rather than broken — see [ESI scopes and compliance](/docs/concepts/sso-scopes). The
banner ignores characters you merely have permission over, so those can be missing scopes with no
warning here.
