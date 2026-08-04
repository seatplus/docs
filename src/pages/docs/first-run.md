---
title: First run
description: Sign in for the first time, claim the superuser permission, and do the five configuration steps that make a fresh instance actually work.
---

A freshly installed Seatplus starts up empty and inert: nobody is an administrator, no ESI scopes are
required, and nothing updates on its own. This page takes you from "the containers are running" to a
working instance.

{% .lead %}

Before you start, you need [installation](/docs/installation) complete and your EVE application's
`EVE_CLIENT_ID`, `EVE_CLIENT_SECRET` and `EVE_CALLBACK_URL` configured — see
[Configuration](/docs/configuration). If the client id or secret is missing the login page shows a
warning, but the Sign in button is still there and clicking it will fail against EVE SSO. A wrong
`EVE_CALLBACK_URL` is not checked at all and fails the same way, so verify all three before you start.

---

## 1. Sign in

Open your instance and click through EVE SSO with the character you want to administrate from.

{% figure src="/images/first-run/login.png" alt="The Seatplus login page with a Sign in button" caption="The login page. The first sign-in requests almost nothing — only public data plus whatever you later configure as globally required." /%}

You land on the dashboard, which shows one card per character on your account. Right now that is one
card, and the sidebar is nearly empty — you have no permissions yet.

{% figure src="/images/first-run/dashboard.png" alt="The Seatplus dashboard after first sign-in, showing a single character card" caption="The dashboard after first sign-in. Sidebar entries appear as you gain permissions." /%}

---

## 2. Claim superuser

The `superuser` permission has to be granted from the command line, once, by whoever controls the
server. Run this inside the php container:

```shell
docker-compose exec php php artisan seatplus:assign:superuser "Your Character Name"
```

The command is interactive. It prints the accounts matching that character name with their user ids,
asks which one should become superuser, and asks you to confirm. It then creates a managed control
group called *Superuser* holding the `superuser` permission and puts your account in it.

{% callout type="warning" title="This command works exactly once" %}
If a superuser already exists, the command refuses to run and instead prints the accounts that
currently hold `superuser`, so you know who to ask. Every subsequent administrator is appointed
through the web interface by adding them to a control group — see
[Permissions and control groups](/docs/concepts/permissions).
{% /callout %}

Reload the page. You now have the full sidebar, including **Settings**.

---

## 3. Create the schedules

This is the step people skip, and it is the reason instances look broken. **A fresh installation has no
schedules**, so once the data fetched at your first sign-in goes stale, nothing refreshes it.

Go to **Settings → Server Settings → Schedules** and add one entry for each job. The dropdown lists them
by full class name, so match on the last segment:

| Job | Suggested cadence |
| --- | --- |
| `UpdateCharacter` | hourly |
| `UpdateCorporation` | hourly |
| `MaintenanceJob` | daily |
| `RoleMemberSync` | every 15 minutes |

{% callout type="warning" title="Do not skip RoleMemberSync" %}
`RoleMemberSync` is the job that reconciles control-group membership — it adds and removes automatic-group
members and deactivates members whose ESI scopes have gone stale. Nothing else runs it on a timer.

Without it, the permission model only reconciles when a user happens to complete an EVE SSO login, so
automatic groups silently fail to track who joined or left your corporation.
{% /callout %}

Then confirm the queue is actually running: the **Horizon worker stats** at the top of Server Settings
must show an active status. If they do not, no scheduled job will ever execute.

Details and troubleshooting: [Updating data from ESI](/docs/updating-data).

---

## 4. Decide what ESI scopes you require

Out of the box Seatplus asks characters for almost nothing, which means almost every page is empty. You
decide what your members must grant under **Settings → Server Settings → SSO Setting**.

A sensible starting point for a corporation that wants visibility of its members:

- One **global** entry requiring the corporation-roles scope, so Seatplus can see who your Directors and
  Accountants are.
- One **default** or **user** entry for your corporation requiring the character scopes you actually
  care about — assets, wallet, skills, contracts.

Be deliberate here: every scope you require is something you are asking your members to hand over, and
requiring the whole account's compliance is a bigger ask than one character's. Read
[ESI scopes and compliance](/docs/concepts/sso-scopes) before you commit to a set — particularly the
difference between the *default*, *user* and *global* types.

{% callout type="note" title="Scope enforcement only bites in production" %}
The check that blocks pages until a user is compliant short-circuits outside a `production`
environment. On a staging instance nobody will ever be prompted, and everything will look compliant.
{% /callout %}

After changing scope requirements, sign out and in again with your own character to pick up the new
scopes — or use the step-up link the application offers you.

---

## 5. Set up access for everyone else

You are a superuser, so you see everything. Nobody else sees anything until you build control groups.

The minimum useful setup is one **automatic** group whose eligibility is your corporation or alliance and
which applies to that same corporation or alliance. Everyone eligible is then added and removed as they
join and leave in game — provided you scheduled `RoleMemberSync` in step 3.

Then add narrower groups for the teams that need more: HR, compliance, leadership.

{% callout type="warning" title="The data permissions are not offerable in the interface" %}
The permission picker only lists the six permissions the web package defines — `view member tracking`,
`view member compliance`, `member compliance: review user`, `view access control`, `superuser`,
`manage manual locations` — plus anything already in the database. The per-feature data permissions
(`assets`, `skills`, `wallet_journals` and the rest) are defined in other packages and never reach the
picker, so you cannot grant them here.

In practice, access to the character and corporation data screens comes from **in-game corporation
roles** — which is why your CEO and Directors can use the app before you have configured anything. See
[Permissions and control groups](/docs/concepts/permissions).
{% /callout %}

Full walkthrough, including a worked example:
[Permissions and control groups](/docs/concepts/permissions).

---

## Optional: turn on onboarding

If your instance is the front door for recruitment, enable the onboarding wizard so new users are
asked to add their alts and shown your open job postings during their first minutes. Add to your
`.env` and restart:

```dotenv
ONBOARDING=true
```

See [Server settings](/docs/server-settings).

---

## Checklist

- [ ] You can sign in with EVE SSO.
- [ ] Your account holds `superuser`.
- [ ] Schedules exist for `UpdateCharacter`, `UpdateCorporation`, `MaintenanceJob` and `RoleMemberSync`.
- [ ] Horizon reports an active status on Server Settings.
- [ ] ESI scope requirements are configured, and your own account is compliant.
- [ ] At least one control group grants ordinary members access.
- [ ] **Settings → Server Performance** shows completed update batches.

Once the last item is true, your data is flowing and the rest of the documentation applies.
