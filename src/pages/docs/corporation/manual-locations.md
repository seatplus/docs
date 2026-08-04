---
title: Manual locations
description: How a private Upwell structure that ESI will not name gets a name anyway — the unknown, suggest, review and resolved stages of the manual location flow.
---

Some structures EVE's API will not name for you. They show up across Seatplus as **Unknown Structure
(1234567890)** — an id with no name and no system. Manual locations are the way out: any signed-in
user can suggest what a location actually is, and a reviewer picks the suggestion that becomes the
name everybody sees.

{% .lead %}

**Suggesting a name:** no permission. Any signed-in account can submit one.

**Reviewing suggestions:** the `manage manual locations` permission, at
`/configuration/manual_locations` (**Settings → Manual Locations**).

**ESI scope behind the problem:** `esi-universe.read_structures.v1`. Manual locations exist precisely
because no token carrying that scope can read the structure in question.

---

## Why a location shows as unknown

When Seatplus meets a location id it does not know, it tries two resolvers in order: stations first,
then structures. Station ids resolve from public data. Anything with an id of 100,000,000 or above is
treated as a possible Upwell structure, and reading a structure's name from ESI needs **a token that
both carries `esi-universe.read_structures.v1` and belongs to a character with docking access to that
structure**.

To find such a token, Seatplus works through the characters it knows, in this order: tokens that already
resolved this location successfully, then characters with assets there, then corporation member
tracking, then contracts, then wallet transactions, then any token at all with the scope, and finally
tokens that failed before. Every candidate is filtered on the scope.

If none of them can read it — a private citadel belonging to somebody else, typically — Seatplus records
the location id with no name attached and moves on. That is what you are looking at here:

{% figure src="/images/corporation/manual-locations-1-unknown.png" alt="The character assets view with a location card headed Unknown Structure and a numeric location id" caption="An unresolved location on the assets page. The id is real; only the name could not be fetched." /%}

The same id turns up wherever a location is named — asset cards, contract endpoints, transaction
details, member tracking. See [Assets](/docs/character/assets).

## Anyone can suggest a name

A location card that Seatplus could not resolve carries an **Add location information** button. Clicking
it opens a modal titled *Add location information for unknown structure (id)* asking for two things:

- **Structure name** — free text, whatever the thing is actually called.
- **Search** — the solar-system field, despite the label. It is labelled only `Search`; the string
  telling you what it is for is the placeholder, *Search for a solar system*. It queries EVE's own
  search live, so you pick a real system rather than typing one, and the placeholder disappears as
  soon as you start typing.

{% figure src="/images/corporation/manual-locations-2-suggest.png" alt="The Add location information modal with a structure name field and a solar system search field" caption="The suggestion modal. The solar system field queries EVE's search endpoint, so it needs a working connection to ESI." /%}

Submitting stores the suggestion against your account and queues a job to resolve the system's name.
No permission is involved and there is no limit of one suggestion per location — several users can
suggest competing names for the same id, which is what the review screen exists to settle.

The button is deliberately absent from the asset tabs inside a recruitment review or an employment
inspection. A reviewer looking at somebody else's assets cannot file suggestions from there.

{% callout type="warning" title="A location Seatplus has already recorded is rejected, silently" %}
The submit endpoint validates the location id as **not yet present** in Seatplus's locations table. When
a row already exists for that id — which is the normal state for a location whose resolution has been
attempted and failed — the submission is rejected on that field, and the modal renders validation
messages only for the name and solar system fields. The modal stays open with nothing to explain
itself. If your suggestion appears to do nothing, this is why.
{% /callout %}

## Reviewing suggestions

**Settings → Manual Locations** lists every outstanding suggestion, grouped by location id, with
locations that have no accepted name yet sorted to the top.

{% figure src="/images/corporation/manual-locations-3-review.png" alt="The Manual Locations review screen with a location's competing suggestions as a radio list" caption="Competing suggestions for one location, as a radio list. Locations still awaiting a decision are listed first." /%}

Each group is headed with the name currently in force — `Unknown (id)` while nothing has been
accepted, or `System - Name (id)` once something has. On the right sits the radio list of competing
suggestions. Each option shows:

| Part of the option | What it is |
| --- | --- |
| Title | The suggested `System - Name`, or `? - Name` while the system is still being resolved |
| Description | The submitting account's main character, that account's other characters in brackets, and how long ago it was submitted |

Pick one and press **Save**.

## What accepting does

Accepting is destructive, and worth understanding before you click it:

1. The chosen suggestion is marked as **selected**.
2. A locations row is created for that id pointing at the chosen suggestion, which is what makes the
   name render everywhere assets, contracts and transactions are listed.
3. **Every competing suggestion for that location is deleted.** Not archived — deleted.

{% figure src="/images/corporation/manual-locations-4-resolved.png" alt="The assets view showing the accepted structure name in place of the previous Unknown Structure heading" caption="After acceptance the location renders as system plus name, exactly like a structure ESI had resolved itself." /%}

The accepted suggestion stays on the review screen as the group's only, pre-selected option, so you
can see what is in force. Because its underlying record is a manual location rather than a real
structure, the **Add location information** button also stays on the asset card.

{% callout type="note" title="ESI wins if it ever catches up" %}
Every time the review screen loads, suggestions whose location has since been resolved to a real
station or structure are deleted. If somebody later joins with docking access and a structures scope,
the genuine name takes over and the manual entries disappear on their own.
{% /callout %}

## What each user sees while a suggestion waits

Names are resolved per viewer, which explains why two people can look at the same location and read
different things. The order is:

1. **Location id 2004** short-circuits to **Asset Safety** before anything else is considered.
2. If a suggestion has been **accepted**, everyone sees that one.
3. Otherwise, if **you** submitted a suggestion for this location, you see your own.
4. Otherwise you see the **most recently submitted** suggestion.
5. With no suggestions at all, you see `Unknown Structure (id)`.

So a suggester gets the benefit of their own work immediately, while it waits for review, and
everybody else sees the newest guess until a reviewer settles it.

## Refreshing the data

Nothing about this flow needs a data refresh — acceptance takes effect on the next page load. What
does depend on the background jobs is the automatic resolution that makes manual locations
unnecessary in the first place: the **Maintenance Job** walks assets, contracts, wallet transactions
and member tracking looking for location ids it has no name for and queues a resolution attempt for
each. If that job has never run, you will see far more unknown locations than you should.

See [Updating data from ESI](/docs/updating-data).
