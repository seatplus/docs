---
title: Permissions and control groups
description: The complete permission model — control groups, the four join methods, affiliations, moderators, membership states, and how in-game corporation roles fit in.
---

Seatplus has one mechanism for granting access, and it does two jobs at once: it says **what** a user
may do and **whose data** they may do it to. Understanding that split is the whole of this page.

{% .lead %}

---

## Two questions, one group

Every access decision in Seatplus answers two questions:

1. **What may you do?** — a *permission*, such as `wallet_journals` or `view member tracking`.
2. **To whom?** — an *affiliation*, such as "the corporations in our alliance".

A **control group** carries both. It is a named group of users that holds a set of permissions and
declares the entities those permissions apply to. Grant `wallet_journals` without an affiliation and
the holder can see nobody's wallet; declare an affiliation without the permission and nothing
happens either. You always need both halves.

Control groups appear in the interface as the **Group hub** (**Control Groups** in the sidebar).

{% callout type="note" title="Groups and roles are the same thing" %}
The interface says "group"; the underlying model and some older documentation say "role". They are
one object. Nothing in Seatplus has both a group and a role.
{% /callout %}

---

## The Group hub

**Control Groups** in the sidebar opens the hub. It has up to three sections:

- **My groups** — every group you have any membership row in, including ones you only moderate.
- **All groups** — every other group. Only shown to administrators.
- **Available to join** — self-service and request-to-join groups whose eligibility criteria include
  one of your corporations or alliances, and that you are not already in.

{% figure src="/images/control-groups/hub-admin.png" alt="The Group hub as seen by an administrator, showing All groups and a Create group button" caption="The Group hub as an administrator sees it: every group is listed, each card has a Configure gear, and Create group is available." /%}

Reaching the hub at all requires the `view access control` permission, the
`administrate access control groups` permission, or being a moderator of at least one group.
Superusers bypass every check on this page.

### What each group card shows

The group's name, a badge for its join method, a one-line description of what that method means, its
member count, a status chip if you are a member or have a request pending, and — where applicable — a
**Join**, **Request to join** or **Leave** button. A gear icon appears if you can configure the group
(administrators) or manage its members (moderators).

### The same hub, four different people

Visibility is computed per viewer, so the hub looks materially different depending on who you are.

A **moderator** of one group — no permissions at all, just a moderator flag:

{% figure src="/images/control-groups/hub-moderator.png" alt="The Group hub as seen by a moderator, with the moderated group under My groups" caption="A moderator sees their group under My groups with a gear that leads to member management, not configuration. There is no Create group button." /%}

An ordinary **member**:

{% figure src="/images/control-groups/hub-member.png" alt="The Group hub as seen by an ordinary member, showing the group with a Leave action and no gear" caption="A member gets the group and a Leave action, and no gear at all." /%}

Someone who is **eligible but not a member**:

{% figure src="/images/control-groups/hub-eligible.png" alt="The Group hub showing a group under Available to join with a Join button" caption="Eligible non-members find the group under Available to join, with Join or Request to join depending on the group's method." /%}

And someone **neither eligible nor a member**:

{% figure src="/images/control-groups/hub-nonmember.png" alt="The Group hub for a user with no groups and no eligibility, showing only the heading" caption="A user who is not eligible does not see the group at all — and opening its URL directly returns 403." /%}

---

## The four join methods

A group's **join method** (its *type*) decides how people become members. It is the single most
important choice when creating a group.

| Method | How membership works | Eligibility | Moderators |
| --- | --- | --- | --- |
| **Automatic** | Everyone who meets the criteria is added, and anyone who stops meeting them is removed, whenever reconciliation runs. | Required | Not supported |
| **Managed** | Moderators add and remove members by hand. There are no criteria. | Not used | Supported |
| **Request to join** | Eligible users apply; a moderator approves or denies each request. | Required | Supported |
| **Self-service** | Eligible users join instantly, no approval. | Required | Supported |

**Automatic** is the right choice for anything that should mirror in-game reality — "everyone in our
alliance gets these permissions".

**Managed** is the right choice for a hand-picked team such as HR or leadership, where there is no
rule you could express as criteria.

{% callout type="warning" title="Reconciliation is not continuous" %}
An automatic group's membership is only recalculated when the `RoleMemberSync` job runs, or when an
administrator re-saves the group. Nothing runs it on a timer unless you schedule it — see
[Updating data from ESI](/docs/updating-data). Without that schedule, its only other trigger is a user
completing an EVE SSO login.

So an automatic group will not notice that someone joined or left your corporation until one of those
things happens. If you rely on automatic groups, schedule `RoleMemberSync`.
{% /callout %}

{% callout type="warning" title="Changing a group's join method wipes its memberships and its criteria" %}
Switching a group from one method to another deletes every membership row on it — members, pending
requests, moderator flags, **and** the corporation/alliance eligibility criteria. The Configure form
resubmits the criteria as part of the same save, which is the only reason they appear to survive.

Decide the method when you create the group. Switching *to* automatic repopulates the member list
immediately from the criteria; switching to any other method leaves you rebuilding it by hand.
{% /callout %}

{% callout type="note" title="Hand-adding a member to an automatic group silently does nothing" %}
Removing a member from an automatic group is refused with an error, as you would expect. **Adding** one
is not: the request succeeds, reports success, and is then immediately undone by the same reconciliation
that keeps the group in sync. The member never appears, and nothing tells you why.
{% /callout %}

---

## Eligibility

Eligibility ("Membership" on the Configure screen) answers *who is allowed to become a member*. You
select corporations and alliances; a user is eligible if any character on their account is in one of
them.

There is also an **anyone can join** toggle, which makes every user eligible. In the create wizard it is
the option that skips entity selection entirely.

{% callout type="warning" title="An “anyone can join” group is invisible under Available to join" %}
The **Available to join** section matches groups whose eligibility criteria name one of *your* actual
corporations or alliances. "Anyone can join" is stored as a criterion against a placeholder corporation
that no real character belongs to, so it matches nobody — and the group never appears in that section
even though everyone is eligible and the join button works.

If you create an open group, distribute its URL yourself; users will not discover it in the hub.
{% /callout %}

{% figure src="/images/control-groups/create-wizard.png" alt="The create-group wizard on its eligibility step, selecting which corporations may join" caption="The create wizard walks through name, join method, eligibility, what the group applies to, and permissions before a single submit." /%}

{% figure src="/images/control-groups/create-wizard-everyone.png" alt="The create-group wizard with the anyone-can-join option selected" caption="With 'anyone can join', eligibility is unrestricted and no member is ever pruned for failing criteria." /%}

Eligibility is re-checked, not only evaluated at join time — but only when reconciliation runs, as above.
For a request-to-join group, approving someone who has since become ineligible fails and removes their
membership.

---

## Affiliations — what the group applies to

Affiliations ("Applies to" / "Authorization" on the Configure screen) answer *whose data the group's
permissions cover*. There are three kinds, and they combine:

| Kind | Label | Meaning |
| --- | --- | --- |
| Allowed | **Only these** | Grants exactly the listed entities |
| Inverse | **Everyone except** | Grants everything *other than* the listed entities |
| Forbidden | **Never (exclude)** | Removes the listed entities, whatever else says |

The effective set is *(allowed ∪ everything-except-the-inverse-list) minus forbidden*, and
**forbidden always wins**. Use it as a hard carve-out: "everyone except our renters, and never these
two corporations" is one inverse entry plus two forbidden entries.

Affiliations expand downwards:

- Naming a **corporation** also covers every character in it.
- Naming an **alliance** also covers its corporations *and* their characters.

There is also an **Everything** toggle, which grants the group's permissions across the whole instance.
It is **mutually exclusive** with the three lists — turning it on hides them, so you cannot combine
"everything" with a forbidden carve-out. To express "everything except X", leave the toggle off and use
an **Everyone except** entry naming X instead.

{% figure src="/images/control-groups/configure-admin.png" alt="The Configure tab of a group showing name, membership, authorization and permissions cards" caption="The Configure tab. Name, join method plus eligibility, the three affiliation lists, and the permission picker — all saved together." /%}

---

## Members and moderators

The **Members** tab is available to administrators and to a group's moderators.

{% figure src="/images/control-groups/members-admin.png" alt="The Members tab of a group as an administrator sees it, with member and moderator pickers" caption="As an administrator: pending requests, the member list with a search-by-character picker, and the moderator list." /%}

{% figure src="/images/control-groups/members-moderator.png" alt="The Members tab as a moderator sees it, with the moderator list read-only" caption="As a moderator: the same member management, but the moderator list is read-only — only administrators may appoint moderators." /%}

A **moderator** is a membership row carrying a moderator flag — which does *not* require being a member.
Appointing someone a moderator leaves their membership status empty, so they moderate the group while
showing as "Not a member", and demoting a member preserves their row rather than deleting it. Moderators
exist on managed, request-to-join and self-service groups, and **never** on automatic ones.

A moderator may:

- see the Members tab for that group;
- approve and deny join requests;
- add a member by hand;
- remove a member.

A moderator may **not** configure the group, delete it, or appoint other moderators. Only
`administrate access control groups` (or superuser) can do those. Moderators do see the Control
Groups entry in the sidebar even without any view permission.

### Membership states

| State | Meaning |
| --- | --- |
| **Active** | A full member. This is the only state that grants the group's permissions, and the only one the Members tab lists. |
| **Pending** | A request-to-join application awaiting moderation. Shown under pending applications. |
| **Inactive** | A member whose account is not ESI-compliant. The group's permissions no longer apply, and they are **not shown anywhere in the interface**. |
| *(none)* | A row that exists without a membership status — most often a moderator who is not also a member. Shown as "Not a member". |

{% callout type="warning" title="Inactive is the answer to “I am in the group but lost access”" %}
When a membership is re-checked and the account is not ESI-compliant, it flips to **inactive**: the
group's permissions stop applying, silently and with no notification.

The confusing part is that inactive members are **filtered out of the Members tab entirely**. There is
no "inactive" badge and no greyed-out row — from an administrator's point of view the person has simply
vanished from the group, while their membership record still exists. If someone insists they were in a
group and you cannot find them, this is almost always why.

The fix is always the same: bring the account back into compliance. See
[ESI scopes and compliance](/docs/concepts/sso-scopes).

Note that this re-check only runs when the `RoleMemberSync` job runs — which, unless you have scheduled
it, means only when that user next completes an EVE SSO login. See
[Updating data from ESI](/docs/updating-data).
{% /callout %}

{% figure src="/images/control-groups/overview-admin.png" alt="The Overview tab of a group showing eligibility, applies-to and permissions summaries" caption="The Overview tab summarises a group's eligibility, affiliations and permissions in read-only form." /%}

{% figure src="/images/control-groups/overview-member.png" alt="The Overview tab as a member sees it, with a Leave action and no configuration" caption="Members get the same Overview without any management affordances." /%}

---

## In-game corporation roles

Control groups are not the only way to gain access. If a character on your account holds an in-game
corporation role, your account inherits corporation-scoped access there without any group at all.

The rules worth knowing:

- **Director implies every role.** A Director satisfies any corporation-role requirement.
- Role-gated pages name the roles they accept — the corporation wallet accepts `Accountant` or
  `Junior_Accountant`, member tracking and recruitment management require `Director`.
- Seatplus only knows a character's roles if that character's token carries
  `esi-characters.read_corporation_roles.v1`.

This is why a brand-new instance is usable before anyone has built a single group: the CEO signs in,
their Director role is picked up, and corporation pages start working.

---

## The permission reference

{% callout type="warning" title="Most of these cannot currently be granted through the interface" %}
The Configure screen's permission picker offers only the six permissions defined in the web package's
own configuration — `view member tracking`, `view member compliance`,
`member compliance: review user`, `view access control`, `superuser`, `manage manual locations` —
plus any permission already stored in the database.

The data permissions (`assets`, `contracts`, `wallet_journals`, …) and the recruitment and queue
permissions are defined in the other packages, and those definitions are never loaded into the picker.
Because a permission only reaches the database by being saved from that picker, there is no route by
which they appear: they are documented, checked at runtime, and unofferable.

In practice that means access to the character and corporation data screens comes from **in-game
corporation roles** or `superuser`, not from these permissions, unless someone inserts them into the
database directly. The tables below describe what each permission *would* grant, and are accurate about
what the code checks — treat them as a reference, not as a menu.
{% /callout %}

### Feature and data permissions

| Permission | Grants |
| --- | --- |
| `assets` | Character and corporation assets |
| `contacts` | Contacts |
| `contracts` | Contracts |
| `wallet_journals` | Character and corporation wallets |
| `skills` | Skills and skill queue |
| `mails` | Mails |
| `corporation_history` | Corporation history |
| `members` | Corporation member tracking data |

### Feature-area permissions

| Permission | Grants |
| --- | --- |
| `view member tracking` | The Member tracking screen |
| `view member compliance` | Employment observation |
| `member compliance: review user` | Opening an individual character's item or contract detail while reviewing compliance, without the matching data permission |
| `manage manual locations` | Reviewing and accepting manual location suggestions |
| `can open or close corporations for recruitment` | Managing job postings |
| `can accept or deny applications` | The review queue and deciding applications |
| `queue.manager` | Intended for the Horizon queue dashboard — but the dashboard checks a differently-spelled name (`queue_manager`), so this permission currently grants nothing and Horizon is superuser-only |

### Administrative permissions

| Permission | Grants |
| --- | --- |
| `view access control` | Viewing the Group hub |
| `administrate access control groups` | Creating, configuring and deleting groups, and appointing moderators |
| `view access control groups` | Defined in configuration; the Group hub itself checks `view access control` |
| `superuser` | Everything, bypassing all other checks |

{% callout type="note" title="Permissions appear in the picker once they have been used" %}
There is no seeding step. The feature and data permissions are created in the database the first time
they are saved onto a group, and the `seatplus:assign:superuser` command creates the `superuser`
permission along with a managed group to hold it. On a brand-new instance the list is therefore
shorter than the reference above; entries appear as they are first used.
{% /callout %}

---

## Worked example: an alliance-wide compliance team

The goal: a group who can see employment observation for every corporation in your alliance, without any
of them being a Director.

This example uses `view member compliance` deliberately — it is one of the six permissions the picker
actually offers, so the walkthrough can be completed as written. See the warning above for why the data
permissions cannot be used this way today.

1. **Control Groups → Create group.**
2. **Name** it *Alliance Compliance*.
3. **Join method**: *Managed*, so you pick the members by hand.
4. **Applies to**: *Only these* → your alliance. (Naming the alliance covers its corporations
   automatically.)
5. **Permissions**: `view member compliance`.
6. Create the group, then add the team on the **Members** tab.

What each person now needs for the page to show anything:

- Their account must be ESI-compliant, or their membership silently goes inactive and they disappear
  from the group.
- The corporations must have ESI scope requirements configured, or they do not appear in Observation at
  all. See [Employment observation](/docs/personnel/observation).

Allow up to five minutes for the permission change to take effect. Note that changing *which permissions*
a group grants is one of the changes that does **not** invalidate the cache early, so this wait is real.

{% callout type="warning" title="Most other pages need the corporation picked explicitly" %}
Observation is unusual in listing permission-reachable corporations straight away. The corporation wallet
and member tracking screens instead default to only the corporations where one of *your own* characters
holds the relevant in-game role — a group-granted corporation shows nothing until the user picks it with
**Select Corporation**.

Do not generalise from one page to the other when you are debugging "the permission is granted but the
page is empty".
{% /callout %}

{% callout type="warning" title="Some sidebar entries are gated on undefined permissions" %}
The **Corporation → Wallets** entry is gated on a permission string — `wallets` — that is not defined
anywhere in Seatplus. Nothing can hold it, so that entry only appears for a superuser or for someone whose
character holds `Accountant`, `Junior_Accountant` or `Director` in game.

Someone authorised for the page can therefore have no link to it. Give them the direct URL
`/corporation/wallet`.
{% /callout %}
