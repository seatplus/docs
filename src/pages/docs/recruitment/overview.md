---
title: Recruitment overview
description: How Seatplus turns a corporation into a job posting, walks applicants through staged review, and hands the decision to the right recruiters.
---

Seatplus ships a complete recruitment pipeline: a corporation opens a **job posting**, applicants
find it in the **Job Portal**, and their applications move through an ordered list of **review
stages** until someone accepts or rejects them. This page explains the moving parts and the
vocabulary; the following three pages cover each role in detail.

{% .lead %}

---

## The four things you need to know

**A job posting belongs to a corporation, and there is exactly one per corporation.** You do not
create multiple openings with different titles — a posting is a switch that says "this corporation
is recruiting", plus the configuration for how applications to it are handled. Opening a posting
for a corporation that already has one simply updates it.

**A posting is either whole-account or single-character.** A *whole account* posting means every
character on the applicant's account has to satisfy the corporation's ESI scope requirements. A
*single character* posting means only the character (or characters) they applied with does. You
choose this when you open the posting, and it is shown as a badge everywhere the posting appears.

**Applications advance through stages, and each stage decides who reviews it.** A posting has an
ordered list of stages — the default is a single stage called `Open`. Each stage is either open to
*any recruiter* for that corporation, or restricted to the members of one **control group**. That
is how "junior HR screens, senior HR decides" is expressed: two stages, two control groups.

**Accepting an application does not put anyone in your corporation.** Seatplus has no way to issue an
in-game corporation invite. Accepting the final stage records the hire inside Seatplus and nothing more —
you still have to invite them in the EVE client yourself, and they will not appear in Observation until
they have actually joined in game.

---

## Vocabulary

| Term | What it means |
| --- | --- |
| **Job posting** | A corporation that has been opened for recruitment. One per corporation. |
| **Job Portal** | The applicant-facing list of every open posting, across all corporations. |
| **Review stage** | One ordered gate an application must pass. Has a name and, optionally, a control group that owns it. |
| **Control group** | A group of users. Used here to restrict a stage to specific reviewers. See [Permissions and control groups](/docs/concepts/permissions). |
| **Application** | One applicant's submission to one posting. Either account-wide or per character. |
| **Watchlist** | Items, regions and systems of interest. While reviewing an applicant, they get their own filtered sub-tab on Assets and Contracts. |
| **Observation** | The post-hire view of your members' compliance. See [Employment observation](/docs/personnel/observation). |

---

## The two permissions

Recruitment uses exactly two permissions. Both are also scoped to the corporations a user is
affiliated with, and both accept an in-game **Director** role as an alternative route in.

| Permission | Lets a user |
| --- | --- |
| `can open or close corporations for recruitment` | Open, configure and close postings for their corporations |
| `can accept or deny applications` | See the review queue and decide applications for their corporations |

Either the permission **or** a qualifying in-game corporation role is enough to pass the gate — they
are alternatives, not requirements to be combined. Which corporations you then actually see is decided
separately, by your affiliations and your characters' roles.

Being a recruiter is therefore two independent things: **permission** (which corporations you may
recruit for) and **control-group membership** (which stages you may decide). A user with the
permission but in none of the stage groups sees an empty queue.

{% callout type="warning" title="Two recruitment actions are not corporation-scoped" %}
Impersonating an applicant and triggering an on-demand character update are gated on the
`can accept or deny applications` permission alone, with no corporation check. A recruiter for one
corporation can use both against applicants of another. See
[Reviewing applications](/docs/recruitment/reviewing).
{% /callout %}

{% callout type="note" title="No permission is needed to apply" %}
The Job Portal is available to every signed-in user. Any user can browse every open posting and
apply. Only *managing* postings and *deciding* applications are gated.
{% /callout %}

---

## The flow end to end

1. An HR manager opens a posting for their corporation and configures its stages, watchlist and
   required ESI scopes. → [Job postings and review stages](/docs/recruitment/job-postings)
2. An applicant opens the Job Portal, picks the characters to apply with, and submits. Applying is
   what triggers the corporation's scope requirements against their account.
   → [Applying to a corporation](/docs/recruitment/applying)
3. Recruiters whose control group owns the application's current stage see it in their queue,
   inspect the applicant's assets, wallet, skills, contracts, contacts, mails and corporation
   history, and record a decision. → [Reviewing applications](/docs/recruitment/reviewing)
4. Each acceptance moves the application to the next stage. Accepting the **last** stage hires the
   applicant. Any rejection ends the application immediately.

{% callout type="warning" title="Nobody is notified of anything" %}
Seatplus sends no email, no in-app notification and no Discord message at any point in this flow.
Applicants find out they progressed by revisiting the Job Portal; recruiters find out they have
work by revisiting **Personnel → Reviews**. Plan your out-of-band comms accordingly.
{% /callout %}
