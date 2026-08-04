---
title: Applying to a corporation
description: How an applicant finds an open posting in the Job Portal, what applying commits them to, and how to follow or withdraw an application.
---

The **Job Portal** is where applicants live. It is available to every signed-in user — no
permission, no corporation membership, no invitation — and it lists every open posting on the
instance, not just the ones for your own alliance.

{% .lead %}

**Permission required:** none. Any signed-in user can browse and apply — though, like every page on the
instance, the portal still sits behind the global ESI-compliance check and the onboarding wizard, so a
user who is mid-onboarding or missing a globally required scope is redirected before they get there.

---

## Finding a posting

Open **Job Portal** in the sidebar. Each posting is a card showing:

- the corporation's logo, ticker, name and alliance;
- a **Whole account** or **Single character** badge;
- the **review process** — every stage name, in order, so you can see how many gates there are
  before you commit;
- an **Apply** button, or your current progress if you have already applied.

Postings for corporations you already belong to are sorted to the bottom of the list.

{% figure src="/images/recruitment/job-portal.png" alt="The Job Portal listing one open posting with a Whole account badge, a one-stage review process, and an Apply button" caption="The Job Portal. The badge tells you whether the posting inspects your whole account or only the characters you apply with." /%}

You can see each stage's *name*, but never who reviews it — the control group behind a stage is
deliberately not exposed to applicants.

---

## Applying

For a **single character** posting, tick the characters you want to apply with, then click **Apply**.
For a **whole account** posting there is no picker — you apply as an account and every character
comes along.

If you tick several characters at once they are submitted as a group: they are reviewed, decided and
withdrawn together, but each keeps its own scope compliance.

One exception worth knowing: a character that already has an open application to that corporation is
skipped rather than re-submitted. If that leaves only one new character, no group is formed — you end up
with separate applications that are reviewed and withdrawn independently.

### What applying commits you to

There is no consent dialog, no checkbox, no scope preview. **Applying *is* the consent.** The
moment your application exists, the corporation's — and its alliance's — required ESI scopes become
part of what your account must satisfy, and Seatplus will hold you to it:

- On a **whole account** posting, those scopes are required of **every character on your account**,
  including characters that have nothing to do with the application.
- On a **single character** posting, they are required only of the characters you applied with.

If any required scope is missing, Seatplus stops serving you normal pages and shows a screen listing
each affected character with a link that re-authenticates it against EVE SSO, adding the missing
scopes on top of what that character already granted. Nothing is ever silently removed.

The requirement disappears again as soon as the application is no longer open — accepted, rejected
or withdrawn.

{% callout type="warning" title="Only one whole-account application is ever enforced" %}
Nothing stops you holding open whole-account applications at several corporations at once, but Seatplus
only reads one of them when it works out what your account must grant. The others' scope requirements
are silently not enforced.

That matters to recruiters as much as applicants: an applicant can look fully compliant to your
corporation while never having granted the scopes you asked for, because a different corporation's
application is the one being evaluated. If compliance matters to your process, verify it on the
applicant's own characters rather than trusting the badge.
{% /callout %}

{% callout type="note" title="Scope enforcement only bites in production" %}
The middleware that blocks pages on missing scopes short-circuits outside a `production`
environment. On a development or staging instance you will not be prompted at all, and compliance
will look fine even when it is not. Test this behaviour on a production-mode instance.
{% /callout %}

For what the scopes mean and how requirements combine across global, corporation, alliance and
application sources, see [ESI scopes and compliance](/docs/concepts/sso-scopes).

---

## Following your application

Your progress appears inline on the same posting card in the Job Portal — there is no separate
"my applications" page. Once you have applied the card shows:

- a status pill — **Under review**, **Accepted** or **Not selected**;
- while under review, **Stage _n_ of _m_** and the current stage's name;
- a progress bar;
- which of your characters the application covers;
- a **timeline** of every decision so far: which stage it was, whether it passed or was rejected,
  who acted, and when.

{% figure src="/images/recruitment/my-application.png" alt="A Job Portal posting card for an application under review, showing the Under review pill and Stage 2 of 2" caption="An application that has cleared its first stage. Recruiters' internal comments are never shown here — only the decisions themselves." /%}

Recruiters can leave comments on your application while reviewing it. Those comments are internal
and are **never** surfaced in your timeline.

{% callout type="warning" title="Check back yourself — nothing will tell you" %}
There is no email, no in-app notification and no Discord integration. The Job Portal is the only
place your progress is visible, so revisit it. Likewise, a recruiter is not notified when you
apply.
{% /callout %}

---

## Withdrawing

**Withdraw application** appears on the card while the application is still under review. It
deletes the application outright — there is no "withdrawn" state kept on file. If you applied with
several characters as a group, withdrawing removes the whole group.

After withdrawing you can apply again immediately, and the corporation's scope requirement drops off
your account.

A **rejection** behaves differently: the application stays on record so the corporation keeps its
history, and your card shows **Not selected**.

{% callout type="warning" title="A rejection is final from the portal" %}
Once rejected, the posting card keeps showing your rejected application instead of an **Apply** form, and
**Withdraw application** is only offered while an application is open. So there is no way to clear it or
re-apply to that corporation from the Job Portal.

The server-side duplicate check only looks for *open* applications, so re-application is not blocked in
principle — but the interface offers you no route to it. If a corporation wants to reconsider you, ask
them; they can see your history in their Reviews screen.
{% /callout %}
