---
title: Reviewing applications
description: The reviewer queue, why you only see some applications, the eight inspection tabs, and what accepting or rejecting actually does.
---

Recruiters work from **Personnel → Reviews**. This page covers why your queue contains what it
contains, how to inspect an applicant, and exactly what happens when you submit a decision.

{% .lead %}

**Permission required:** `can accept or deny applications`, for the applicant's corporation. An
in-game **Director** role in that corporation works as an alternative. On top of that, you must be
in the control group that owns the application's current stage.

---

## Your queue only shows your stages

The Reviews screen lists applications **waiting at a stage your control group reviews** — not every
open application for your corporations. Two independent checks decide whether an application reaches
you:

1. **Corporation scope.** Do you hold `can accept or deny applications` for the applicant's
   corporation (or are you a Director there)?
2. **The stage gate.** Is the application's *current* stage assigned to a control group you belong
   to? A stage set to *Any recruiter (no group)* passes for everyone who cleared check 1.

Each row shows the applicant, whether the application is account-wide or how many characters it
covers, the corporation, a **Stage _n_ of _m_: name** pill, and a **Review** button. Below the
pending list, a **History** section holds the past decisions for your corporations.

### The same application, seen by three people

This is the clearest way to understand the stage gate. One posting with two stages — *Screening*
owned by *Junior HR*, *Final* owned by *Senior HR* — and one application from Jane Applicant.

A junior recruiter, with the application still at stage 1:

{% figure src="/images/recruitment/reviews-junior.png" alt="The Reviews queue for a junior recruiter showing Jane Applicant at Stage 1 of 2, Screening" caption="Junior HR sees the application while it sits at Screening, the stage their group owns." /%}

The same junior recruiter, after the application has cleared stage 1 and moved to *Final*:

{% figure src="/images/recruitment/reviews-junior-empty.png" alt="The Reviews queue for a junior recruiter showing the empty state, Nothing to review" caption="The application still exists and is still open — it has simply moved to a stage this reviewer's group does not own." /%}

And a senior recruiter, looking at that very same application at that very same moment:

{% figure src="/images/recruitment/reviews-senior.png" alt="The Reviews queue for a senior recruiter showing Jane Applicant at Stage 2 of 2, Final" caption="Senior HR picks it up at Final. Nothing was reassigned — the queue is computed per viewer." /%}

{% callout type="note" title="An empty queue is usually correct" %}
"Nothing to review" almost always means the applications are parked at stages your groups do not
own, not that something is broken. If you expect to see everything, either put yourself in every
stage's group or set the stages to *Any recruiter (no group)*.
{% /callout %}

---

## Inspecting an applicant

**Review** opens the application detail: the inspection tabs on the left, the decision card on the
right. The tabs cover every character the application covers, not just the main.

{% figure src="/images/recruitment/review-detail.png" alt="The application detail screen with the Log tab active and the decision card on the right" caption="The detail screen opens on the Log tab. The decision card on the right carries the Update controls, the Accept/Reject choice and Submit review." /%}

### The eight tabs

| Tab | What it shows |
| --- | --- |
| **Log** | The activity log — who applied, every decision, and every recruiter comment. This is also where you leave a comment. |
| **Assets** | The applicant's assets by location, with sub-tabs for watchlisted assets, all assets, and assets in unknown locations. |
| **Contracts** | Their contracts, with watchlisted and all-contracts sub-tabs. |
| **Wallets** | Wallet journal, transactions and balance. |
| **Contacts** | Their personal contacts, compared against the recruiting corporation and its alliance. |
| **Corporation History** | Their employment history. |
| **Skills** | Trained skills by group, plus the skill queue. |
| **Mails** | Their mail headers; the body of each mail is fetched by a background job. |

{% callout type="warning" title="With a watchlist configured, Assets and Contracts open pre-filtered" %}
The watchlist does not highlight matching items — it **filters** them into their own sub-tab. And when
a posting has a watchlist, that filtered sub-tab is the one selected by default.

So the first thing a recruiter sees under **Assets** and **Contracts** is not the applicant's assets,
it is the subset matching your watchlist — which is frequently empty, and looks exactly like missing
data. Click **All Assets** or **All Contracts** to see everything.

With no watchlist configured there are no sub-tabs on Contracts at all, and Assets still offers all
assets and assets in unknown locations.
{% /callout %}

{% figure src="/images/recruitment/review-tab-skills.png" alt="The Skills tab of an application, showing the applicant's trained skills grouped by skill group" caption="The Skills tab. Screenshots on this page use data seeded by the browser test suite, so the figures are illustrative." /%}

{% figure src="/images/recruitment/review-tab-wallets.png" alt="The Wallets tab of an application showing the applicant's wallet journal" caption="Wallets: journal, transactions and balance for each covered character." /%}

{% figure src="/images/recruitment/review-tab-assets.png" alt="The Assets tab of an application showing the applicant's assets by location" caption="Assets, grouped by location. This posting has no watchlist, so the tab opens on all assets rather than a filtered subset." /%}

{% figure src="/images/recruitment/review-tab-corporation-history.png" alt="The Corporation History tab of an application showing previous corporations" caption="Corporation History. Corporation names resolve asynchronously, so rows may appear briefly before their names do." /%}

{% figure src="/images/recruitment/review-tab-contracts.png" alt="The Contracts tab of an application showing the applicant's contracts" caption="Contracts. This posting has no watchlist, so no sub-tab bar is rendered and every contract is listed." /%}

An empty tab has three possible causes, in the order worth checking:

1. **A watchlist sub-tab is selected** — see the warning above. Switch to the all-items sub-tab.
2. **The applicant's token does not carry the relevant ESI scope**, so Seatplus never fetched that data.
   That is a compliance question rather than a bug; check the posting's required scopes.
3. **They genuinely have nothing** of that kind.

### Refreshing an applicant's data

The decision card shows, per covered character, when it was last updated and an **Update** button —
offered when that character has never been updated, or when its last update is more than an hour old.
Clicking it queues an immediate ESI refresh so you are not deciding on stale numbers. For a brand-new
applicant the never-updated case is the usual one.

{% figure src="/images/recruitment/review-update-character.png" alt="The application detail with a character's Update control switched to its updating state" caption="Update queues an on-demand ESI refresh for that character. The control shows updating while the batch runs." /%}

### Comments

The Log tab has a **Leave a comment** box. Comments are internal — applicants never see them — and
they do **not** advance the application. Only a decision does.

### Impersonate

For an account-wide application that is still open, the header offers **Impersonate**, which lets you
view Seatplus as the applicant sees it. A banner appears at the bottom of the screen while you are
impersonating; leave through its **Stop** link. It is not offered for single-character applications or
for settled ones.

{% callout type="warning" title="Impersonation is not scoped to your corporation" %}
Unlike every other action on this screen, impersonation performs **no corporation check**. Anyone
holding `can accept or deny applications` — for any corporation at all — can impersonate any applicant
with an open whole-account application anywhere on the instance, and then acts with that person's full
permissions.

This is the widest capability the recruitment permission carries. Grant it deliberately, and prefer
narrower control groups over handing it out broadly.
{% /callout %}

---

## Submitting a decision

On the decision card, choose **Accept application** or **Reject application**, then **Submit
review**. Rejecting requires an **explanation** — it is a mandatory field, and it is stored with the
decision so future recruiters can see the reasoning behind a past call.

What each outcome does:

| Outcome | Effect |
| --- | --- |
| **Accept**, and there are more stages | The application stays open and moves to the next stage. It leaves your queue and enters that stage's group's queue. |
| **Accept** on the final stage | The application is marked accepted and the applicant is recorded as **hired**. |
| **Reject**, at any stage | The application is marked rejected immediately. Remaining stages are skipped. |

If the application covers several characters as a group, your single decision applies to all of them.

### What acceptance does and does not do

Accepting the final stage creates an employment record with status *active*, hired now — one for the
**account** on a whole-account posting, or one per character on a single-character posting. That is the
whole of it. Specifically, it does **not**:

- grant any permission;
- add anyone to a control group;
- change any in-game corporation role;
- send the applicant an in-game corporation invite.

{% callout type="warning" title="You still have to invite them in game" %}
Seatplus cannot issue corporation invites — EVE's API does not offer it. Accepting an application is a
record-keeping and access step inside Seatplus only. The review screen reminds you of this, and it is
the single most common recruitment mistake.
{% /callout %}

### What happens to your access afterwards

Deciding an application does **not** close your window into the applicant's data.

Two different access paths are at work, and they behave differently:

- The **general fallback** that lets a recruiter read an applicant's character pages without the usual
  per-feature permission is limited to applications that are still open, and is cached for 15 minutes.
- The **application detail screen itself** — this page, with its assets, wallet, mails, contacts and
  skills tabs — is gated only on the application id plus your affiliation with the corporation. There
  is no status check. A rejected or accepted application remains fully openable, indefinitely, and the
  **History** list on the Reviews screen links straight to it with a **View** button.

{% callout type="warning" title="Rejecting an applicant does not revoke your access to their data" %}
If you tell your members that a rejected application ends recruiters' visibility of their wallet,
mails and assets, that promise is not true. Any recruiter affiliated with the corporation can reopen a
settled application and browse the same inspection tabs, for as long as the application row exists.

Treat `can accept or deny applications` as a lasting grant over everyone who has ever applied, and
scope who holds it accordingly.
{% /callout %}

Visibility of a hired member as an *employee* is a separate thing, through **Personnel → Observation**
and the `view member compliance` permission. Note that Observation lists members by their **in-game
corporation affiliation**, not by the employment record — so an applicant you accepted who has not yet
actually joined your corporation in game will not appear there at all, no matter what permissions the
recruiter holds. They show up once they join and the next affiliation refresh runs.

Permission changes themselves are cached for about five minutes.
