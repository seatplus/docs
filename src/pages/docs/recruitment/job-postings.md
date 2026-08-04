---
title: Job postings and review stages
description: Open a corporation for recruitment, design its staged review process, set the watchlist and required ESI scopes, and close it again.
---

Everything an HR manager does lives on one screen: **Personnel → Manage Recruitment**. This page
covers opening a posting, designing its review stages, the watchlist, the required ESI scopes, and
closing it again.

{% .lead %}

**Permission required:** `can open or close corporations for recruitment`, for the corporation you
are managing. An in-game **Director** role in that corporation works as an alternative. Superusers
bypass both.

---

## Opening a posting

1. Go to **Personnel → Manage Recruitment**.
2. Click **Open posting**.
3. Search for the corporation. The search goes through EVE's own ESI search, so you can pick a
   corporation Seatplus has never seen before — it is imported on demand so the posting can show its
   name, ticker and alliance.
4. Choose the type — **Whole account** or **Single character** (see below).
5. Click **Open posting**.

The new posting starts with a single review stage named `Open`, which any recruiter for the
corporation can decide. That is a working configuration; you only need the stage editor if you want
more than one gate.

Re-opening a posting for a corporation that already has one does not create a second posting — it
updates the existing one's type.

### Whole account or single character

This is the single most consequential setting on a posting, because it decides how much of an
applicant's account you require visibility into.

| Type | Applicant experience | Scope requirement |
| --- | --- | --- |
| **Whole account** | No character picker — they apply as an account | Every character on their account must satisfy the corporation's required ESI scopes |
| **Single character** | They tick which of their characters to apply with | Only the characters they applied with must satisfy them |

A whole-account posting is the right default for a corporation that wants to see alts. A
single-character posting is friendlier to applicants but tells you nothing about the rest of their
account.

{% figure src="/images/recruitment/manage-posting.png" alt="The Manage Recruitment screen showing a posting with two review stages, Screening assigned to Junior HR and Final assigned to Senior HR" caption="Manage Recruitment: one card per posting, with the ordered stage editor, the watchlist and required-scopes panels, and Close posting." /%}

---

## Designing the review stages

Stages are an ordered list. An application enters at stage 1 and advances one stage per acceptance;
accepting the final stage hires the applicant.

Each stage has two fields:

- **A name.** Free text, up to 255 characters, shown to recruiters *and* to applicants — the Job
  Portal lists every stage name on the posting card, so pick names you are happy for candidates to
  read ("Screening", "Interview", "Final"), not internal shorthand.
- **Who reviews it.** Either **Any recruiter (no group)** — anyone holding
  `can accept or deny applications` for this corporation — or a specific **control group**.

Use **+ Add stage** to append, the **×** on a row to remove it, and **Save posting** to persist. A
posting always keeps at least one stage; the remove button disappears when only one is left.

### How this expresses "junior and senior recruiters"

There is no junior-recruiter permission and no senior-recruiter permission. There is one permission
plus per-stage control groups:

1. Create two control groups, e.g. *Junior HR* and *Senior HR*
   (see [Permissions and control groups](/docs/concepts/permissions)).
2. Give every recruiter — junior and senior alike — the `can accept or deny applications`
   permission for the corporation.
3. Put the juniors in *Junior HR* and the seniors in *Senior HR*.
4. Set stage 1 to *Junior HR* and stage 2 to *Senior HR*.

A junior now sees an application only while it sits at stage 1. The moment they accept it, it
vanishes from their queue and appears in the seniors'. Both checks apply: a reviewer must hold the
permission for the corporation **and** be in the stage's group.

{% callout type="note" title="A group-less stage is the widest possible stage" %}
**Any recruiter (no group)** does not mean "anyone" — it means anyone who already holds
`can accept or deny applications` for this corporation. It is the correct choice for a single-stage
posting where you do not want to maintain groups at all.
{% /callout %}

{% callout type="warning" title="Saving replaces every stage, and positions are just numbers" %}
Saving a posting deletes its existing stages and recreates them from the form, numbering them by their
order in the list starting at zero. An application's progress is stored as a *count of decisions*, not
as a reference to a stage — so an application that has passed one stage sits at position 1, which is the
second stage. The interface adds one when it displays "Stage 2 of 2".

If you reorder or delete stages while applications are in flight, those applications do not move — but
the stage they now sit at may be a different one than before, possibly owned by a different control
group. Change a live posting's stage list only when its queue is empty, or accept that in-flight
applications will land wherever that position now happens to point.
{% /callout %}

---

## The watchlist

**Manage watchlist** on the posting card lets you register regions, solar systems, and item types,
groups or categories. During review, matching assets and contracts get their own filtered sub-tab —
which is how you answer "does this applicant own a supercapital" or "do they have assets in our staging
system" without a recruiter hunting for it. The badge on the disclosure shows how many entries are
configured.

{% callout type="warning" title="A watchlist changes what recruiters see first" %}
The watchlist does not highlight matches inside the full list — it filters them into a separate sub-tab,
**and that sub-tab becomes the default** on the Assets and Contracts tabs. Recruiters reviewing a
posting with a watchlist will land on a filtered, often empty view and may read it as missing data.

If you configure a watchlist, tell your recruiters to click **All Assets** / **All Contracts**. If you
do not need one, leaving it empty gives them the unfiltered list by default.
{% /callout %}

---

## Required ESI scopes

**Manage required SSO scopes** on the posting card sets the corporation's required scopes. Whatever you
select here is what applicants must grant, enforced against the whole account or the single character
according to the posting's type.

Two scopes are added implicitly, so do not go hunting for them: selecting any corporation scope also
requests the corporation-roles scope, and selecting either the corporation wallet or corporation assets
scope also requests the divisions scope.

{% callout type="warning" title="Saving here rewrites the setting's type to “default”" %}
This panel writes the same record as **Settings → Server Settings → SSO Setting**, but it always writes
it as the **default** type — "only characters within this corporation must satisfy these scopes".

If an administrator had configured that corporation as the **user** type — "every character on the
account of anyone in this corporation" — then pressing **Save posting** silently downgrades it to
default and narrows enforcement across your whole instance. If your corporation uses the user type,
manage its scopes from Server Settings and leave this panel alone.

There is a second trap in the picker itself: if the corporation-roles scope is not already selected, the
panel drops every corporation scope from the form when it opens, and **Save posting** then persists that
reduced set. Check the selection is what you expect before saving.
{% /callout %}

{% callout type="note" title="Clearing every scope can remove the corporation from Observation" %}
Employment observation only lists corporations that have SSO scopes configured — with no requirement
there is nothing to be compliant against. Clearing the last scope here therefore removes the
corporation from **Personnel → Observation**, *unless* its alliance has scopes configured, in which case
it stays.
{% /callout %}

For the full picture of how requirements are computed and what applicants see when they are missing
a scope, read [ESI scopes and compliance](/docs/concepts/sso-scopes).

---

## Closing a posting

**Close posting** removes the posting and its review stages. It does **not** touch applications.

Concretely, after closing:

- The corporation disappears from the Job Portal and nobody can apply to it any more.
- Applications that were already submitted still exist, still appear in the reviewer queue and
  history, and can still be decided.
- The stage configuration is gone. If you re-open the posting later you get a fresh single `Open`
  stage, and any application still in flight is evaluated against that new list.

{% callout type="warning" title="Closing a posting strands anyone who has applied to it" %}
The Job Portal renders a card per *open posting*, and an applicant's status lives on that card. Delete
the posting and the card goes with it — so applicants lose all visibility of where their application
stands **and** lose the **Withdraw application** button.

Their application stays open, which means the corporation's required ESI scopes keep being enforced
against their account, with no way for them to opt out. Only a recruiter can end it, by deciding it.

Decide every outstanding application before you close a posting. This is not a courtesy — it is the only
exit the applicant has.
{% /callout %}
