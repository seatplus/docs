---
title: ESI scopes and compliance
description: What ESI scopes are, the three ways to require them, how compliance is computed, and what a user sees when a scope is missing.
---

Seatplus can only show you what EVE's API lets it read, and EVE only grants access to what a character
explicitly consented to. Those grants are **ESI scopes**. This page explains how to require them,
what happens when they are missing, and why "compliance" is the word Seatplus uses for having them.

{% .lead %}

---

## What a scope is

A scope is one permission on an EVE SSO token, such as `esi-assets.read_assets.v1`. When a character
authenticates, Seatplus asks EVE for a specific set of scopes; EVE shows the character's owner what is
being requested, and the resulting token carries exactly what they approved.

Two consequences follow, and both surprise people:

- **Seatplus cannot fetch data it has no scope for.** If a character never granted the skills scope,
  their Skills page is empty. This is not a bug and no amount of refreshing fixes it.
- **Initial login requests almost nothing.** Signing in only asks for `publicData` plus whatever you
  have configured as globally required. Every additional scope arrives through a later re-authentication.

---

## What Seatplus can request

The scope catalogue is fixed in the application — you pick from it rather than typing scope strings.

| Group | Feature | Scopes requested |
| --- | --- | --- |
| Minimum | Sign-in | `publicData` |
| Character | Assets | `esi-assets.read_assets.v1`, `esi-universe.read_structures.v1` |
| Character | Corporation roles | `esi-characters.read_corporation_roles.v1` |
| Character | Contacts | character, corporation and alliance contact scopes |
| Character | Wallet | `esi-wallet.read_character_wallet.v1` |
| Character | Contracts | `esi-contracts.read_character_contracts.v1` |
| Character | Skills | `esi-skills.read_skills.v1`, `esi-skills.read_skillqueue.v1` |
| Character | Mails | `esi-mail.read_mail.v1` |
| Character | Title | character title scope |
| Corporation | Assets | corporation assets plus `esi-corporations.read_divisions.v1` |
| Corporation | Member tracking | `esi-corporations.track_members.v1` |
| Corporation | Contracts | corporation contracts |
| Corporation | Wallet | `esi-wallet.read_corporation_wallets.v1`, `esi-corporations.read_divisions.v1` |

Two additions happen implicitly, so do not go looking for them in the picker:

- Selecting a scope whose name contains "corporation" also requests the corporation-roles scope. That
  covers every corporation scope — and, because of the string match, also the character **Contacts**
  group, which includes the corporation-contacts scope.
- Selecting the corporation wallet or corporation assets scope also requests the divisions scope.

{% callout type="note" title="A corporation scope still needs the right character" %}
Corporation endpoints are not satisfied by just anyone's token. Member tracking needs a Director's
token, and the corporation wallet needs an `Accountant` or `Junior_Accountant` token. Requiring the
scope of every member does not help if no qualifying character has granted it.
{% /callout %}

---

## The three ways to require scopes

Requirements are configured under **Settings → Server Settings → SSO Setting** (superuser only), or
for a single corporation from its job posting. Each entry has a **type**, and the type is what
decides who the requirement lands on:

| Type | Applies to |
| --- | --- |
| **Default** | Only characters inside the selected corporation or alliance |
| **User** | Every character on the account of anyone who has a character in the selected corporation or alliance — including alts elsewhere |
| **Global** | Every character on the entire instance. There is one global entry, with no entity attached |

The **user** type is the one worth thinking about carefully. It is how you say "if you fly with us,
we want to see your whole account, not just the character in our corp" — and it is also how a
requirement quietly spreads to characters in unrelated corporations.

A fourth source exists implicitly: **applying to a job posting** adds that corporation's and its
alliance's scopes to the applicant for as long as the application is open. On a whole-account posting
those land on every character. See [Applying to a corporation](/docs/recruitment/applying).

---

## How compliance is computed

For each character on an account:

1. **Required** is the union of the global scopes, the character's corporation's scopes, its
   alliance's scopes, every *user*-type entry attached to any corporation or alliance of any
   character on the account, and — while an application is open — the application's corporation and
   alliance scopes.
2. **Granted** is read out of the character's current refresh token.
3. **Missing** is required minus granted.

An account is compliant when every one of its characters has nothing missing.

{% callout type="warning" title="No token means no scopes" %}
A character with no refresh token at all counts as having granted nothing, so it is non-compliant
against any requirement. Removing a character's token does not exempt them.
{% /callout %}

---

## What a non-compliant user experiences

Two prompts exist:

**The hard gate.** Instead of the page they asked for, the user gets a screen listing each affected
character, its corporation, and a link that re-authenticates that character against EVE SSO. The
link requests the character's existing scopes **plus** the missing ones, so nothing they previously
granted is lost.

{% figure src="/images/step-up.png" alt="The missing required scopes screen listing affected characters with a link to re-authenticate each" caption="The step-up screen. It appears in place of whatever page the user requested until every character is compliant." /%}

**The soft banner.** An amber "missing scopes" notice on feature pages, with a per-character link to
the same re-authentication flow.

During re-authentication the user must pick the **same character** on EVE's side. Choosing a
different one is rejected with an explanatory message, as is a grant that comes back short of what
was requested.

{% callout type="warning" title="The hard gate only applies in production" %}
The middleware that blocks pages on missing scopes short-circuits entirely outside a `production`
environment. On a development or staging instance nobody is ever prompted, and everything looks
compliant. If you are validating your scope configuration, do it on a production-mode instance.
{% /callout %}

---

## The knock-on effect on permissions

Compliance is not only about empty pages. Control-group membership is re-evaluated against it: a
member whose account becomes non-compliant has their membership switched to **inactive**, which
keeps them on the group's member list but **removes the group's permissions from them** until they
fix their scopes.

This is the usual explanation for "I am still in the group but lost access" — and because the Members tab
lists only active memberships, an inactive member disappears from the group entirely rather than showing
as deactivated. See [Permissions and control groups](/docs/concepts/permissions).

The re-check only runs when the `RoleMemberSync` job runs, which is not scheduled by default — see
[Updating data from ESI](/docs/updating-data).

---

## Configuring scopes

1. Go to **Settings → Server Settings** and open the **SSO Setting** tab.
2. Create an entry, choose its type, and — for default and user types — select the corporations or
   alliances it applies to.
3. Select the scopes.

A corporation or alliance has at most one entry, so saving replaces whatever was there. Deleting it drops
the requirement, and also removes that corporation from
[Employment observation](/docs/personnel/observation) — unless its alliance still has an entry, which
keeps the corporation observable.

{% callout type="warning" title="Saving a job posting overwrites the corporation's entry" %}
The **Manage required SSO scopes** panel on a job posting writes this same record, and always writes it as
the **default** type. So editing a posting silently converts a `user`-type requirement to `default`,
narrowing enforcement from the whole account to just the characters in that corporation — and saving a
posting with no scopes selected **deletes the entry outright**.

If you configure a corporation as the user type here, manage its scopes from this screen only. See
[Job postings and review stages](/docs/recruitment/job-postings).
{% /callout %}

{% figure src="/images/scope-setting.png" alt="The SSO scope settings screen with scope checkboxes grouped by character and corporation" caption="The scope picker, grouped into character and corporation scopes. Requirements take effect on the next request." /%}

Changing scope settings invalidates every account's cached permissions immediately, so scope changes
do not suffer the usual five-minute lag.
