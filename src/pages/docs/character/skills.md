---
title: Skills
description: How the character skills screen shows trained skills grouped by skill group alongside the remaining skill queue.
---

**Skills** shows what a character can fly and what it is training: every trained skill grouped by
skill group, with skillpoint totals, next to the remaining skill queue. Recruiters use it to check a
claim; pilots use it to see where their skillpoints went.

{% .lead %}

**Permission required:** `skills`, and only for characters other than your own. `/character/skills`
carries no permission middleware — every signed-in user reaches it and sees their own characters — so
the permission is what widens the picker.

**ESI scopes required:** both `esi-skills.read_skills.v1` (trained skills and skillpoints) and
`esi-skills.read_skillqueue.v1` (the queue). They are separate scopes: a character can legitimately
show a full skill list and an empty queue because only the first one was granted.

---

## What you see

The page header is **Character Skills**, with **Select Character** and **Update** buttons. Below it,
one block per character: the character on top, then a **Skill Queue** card on the left and the trained
skills to the right of it.

Trained skills are grouped into one card per skill group — Gunnery, Spaceship Command and so on. Each
card header carries the group name, the group's total skillpoints, and a legend explaining the two star
styles: filled for **active**, outline for **trained**.

{% figure src="/images/character/skills.png" alt="The Character Skills page with a Skill Queue card on the left showing one entry finishing in 3 days, and Gunnery and Spaceship Command cards on the right" caption="One block per character: the remaining queue on the left, trained skills grouped by skill group on the right." /%}

There is no search box and no filter on this screen. Groups and skills are all there is.

## The skill queue

The queue card lists entries in queue order, each with the skill name and a relative finish time. An
entry with **no finish date** shows **Unknown** instead of a time. That is what a **paused** queue looks
like: ESI reports no finish date for an entry that is not counting down.

Seatplus only checks whether the date is null, so it cannot tell you *why* it is missing. Read **Unknown**
as "this entry is not currently ticking down" — most often a paused queue — rather than as a rendering
fault.

The queue is filtered to entries that are **not yet finished**: an entry only appears while its finish
date is in the future, or when it has no finish date at all.

{% callout type="note" title="The queue empties itself without an update" %}
Because finished entries are filtered out at render time, the card can go empty purely through the
passage of time — the last entry's finish date slid into the past. That does not mean the pilot
stopped training or that the queue in game is empty; it means nothing in the stored queue is still in
the future. Only a fresh queue fetch will tell you what has been queued since, and the **Update**
button is not that fetch — see below.
{% /callout %}

{% callout type="warning" title="The Update button does not refresh the skill queue" %}
**Update** on this page queues exactly one job, and it is the trained-skills job. Nothing in it touches
the skill queue. The queue is fetched by a separate job that runs **only** as part of the scheduled
character update batch.

So pressing **Update** on a character whose queue card is empty or stale reports success and changes
nothing about the queue. To refresh a queue you need the scheduled character update to run for that
character — schedule it if it is not scheduled, or wait for the next run. See
[Updating data from ESI](/docs/updating-data).
{% /callout %}

When there is nothing left to show, the card says **No skills in training.** with the note *This
character's skill queue is empty.*

{% figure src="/images/character/skills-empty-queue.png" alt="The Character Skills page with the Skill Queue card showing the empty state No skills in training, next to a Gunnery card" caption="The empty-queue state. It means no stored queue entry is still unfinished — trained skills are unaffected." /%}

## Trained and active levels

Each skill row renders one star per **trained** level, and a star is filled when its zero-based position
is less than **or equal to** the active skill level. So the number of filled stars is the active level
**plus one**, capped at the number of trained levels — not the active level itself.

Read the outline stars rather than counting the filled ones. An Alpha clone capped at level 3 in a skill
it has trained to 5 shows **four filled stars and one outline**: five stars for five trained levels,
positions 0 through 3 filled. A skill whose active level has caught up with its trained level is all
filled stars. Any outline star at all means trained is ahead of active.

The number next to each group heading is the sum of the skillpoints in that group's skills, so it
reflects what has actually been trained rather than what is usable.

## Empty states

If a character has no stored skills at all, the right-hand side shows **No skills found.** with the
note *This character has no trained skills yet, or the data has not been fetched.* In practice the
second half of that sentence is the usual cause.

Both the skills and the queue load after the page frame, so you will briefly see placeholder cards on
a slow connection.

## Selecting characters

You see **your own characters** by default, one block each. **Select Character** widens that, and the
selection is only ever a filter — an id you have no claim on is dropped by the query.

Two things about the picker's contents explain most surprises:

- **A character with no stored skills is not offered.** The candidate list is filtered to characters
  that already have at least one stored skill, so a character you are authorised for but who has never
  been updated is absent from the picker entirely — which looks exactly like a permission problem.
- **Characters with an open application to you are offered anyway**, whether or not a role grants you
  `skills` over them.

See [Characters and accounts](/docs/concepts/characters-and-accounts).

## Refreshing the data

Everything here is stored data. **Update** queues the trained-skills job — and only that job, as the
callout above explains — for one character, and refuses a re-queue within the hour. See
[Updating data from ESI](/docs/updating-data).

A **Missing scopes warning** banner names each of *your own* characters missing either skills scope,
with a **Fix** button that sends it through SSO. A missing scope means that half of the screen was
never fetched, so an empty queue card next to a full skill list — or an empty screen entirely — is
legitimate. See [ESI scopes and compliance](/docs/concepts/sso-scopes).
