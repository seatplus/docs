---
title: Getting started
pageTitle: Seatplus — SeAT with a little plus.
description: Corporation management and recruitment for EVE Online, built around a permission model that fits how alliances actually work.
---

Seatplus is a self-hosted corporation-management tool for EVE Online: it keeps a copy of your members'
ESI data, decides who may see what, and runs your recruitment pipeline.  {% .lead %}

{% quick-links %}

{% quick-link title="Install it" icon="installation" href="/docs/requirements" description="Hardware and software requirements, then a step-by-step Docker install." /%}

{% quick-link title="First run" icon="lightbulb" href="/docs/first-run" description="The five steps a fresh instance needs before it does anything useful." /%}

{% quick-link title="Recruitment" icon="presets" href="/docs/recruitment/overview" description="Job postings, staged review, and how applications reach the right recruiters." /%}

{% quick-link title="Contribute" icon="theming" href="/docs/contributing/how-to-contribute" description="Set up a development environment and help build Seatplus." /%}

{% /quick-links %}

---

## Introduction

Inspired by [SeAT](https://github.com/eveseat/seat), Seatplus is a complete rewrite driven by the
feature requests SeAT received most often. The role and affiliation model was designed from scratch
around the work recruiters and HR teams actually do, rather than bolted on afterwards.

What that buys you in practice:

- **No static data export to maintain.** Seatplus resolves item and location data on demand as it
  encounters it, so a working instance needs no SDE import. An importer exists if you want to
  pre-populate that reference data in bulk, but nothing depends on you running it.
- **Only the scopes you need.** ESI scope requirements are configured per corporation, per alliance or
  globally, and can be scoped to whole accounts — so guests on your instance are not forced to hand
  over everything.
- **Compliance you can see.** When a member's scopes or refresh token change, it shows up in
  [Employment observation](/docs/personnel/observation) instead of silently producing empty pages.
- **Recruiters scoped to recruits.** A recruiter's access is granted by the application rather than by
  membership of your corporation, so you can let someone review candidates without handing them your
  members' data.
- **Membership that maintains itself.** An automatic control group adds and removes members as they
  join and leave your corporation or alliance in game, once its reconciliation job is scheduled.

Seatplus is under active development, and feedback shapes it.

| Channel | Purpose |
|:--- |:--- |
| [GitHub](https://github.com/seatplus/seatplus) | Bug reports, feature requests |
| [Discord](https://discord.gg/3UR5uDDMjK) | Social, support |

## Where to start

If you are **installing it**, read [Requirements](/docs/requirements), then
[Installation](/docs/installation), then [First run](/docs/first-run) — in that order. First run is
the one that matters: a fresh instance fetches nothing from EVE and grants nobody any access until you
configure it.

If someone has **already set it up for you** and you want to understand what you are looking at, start
with [Characters and accounts](/docs/concepts/characters-and-accounts) and
[ESI scopes and compliance](/docs/concepts/sso-scopes). Those two explain most of what appears
confusing at first, including why a page can be empty.

If you are **running recruitment**, go straight to
[Recruitment overview](/docs/recruitment/overview).

## Architecture

Seatplus is a set of Laravel packages assembled by a core application, which is what you install. It is
built mobile-first, so the interface works on a phone as well as a desktop, and it is used in
production by [Amok.](https://zkillboard.com/corporation/1184675423/) for member life-cycle
management.

The packages worth knowing about:

- [seatplus/eveapi](https://github.com/seatplus/eveapi) — the data layer: models, ESI jobs and scopes.
- [seatplus/auth](https://github.com/seatplus/auth) — authentication, permissions, control groups and
  affiliations.
- [seatplus/web](https://github.com/seatplus/web) — the web interface.
- [seatplus/esi-client](https://github.com/seatplus/esi-client) — a standalone ESI client library
  using `kevinrob/guzzle-cache-middleware`.

{% callout type="note" title="You do not have to use the web interface" %}
If you only want to talk to ESI from your own code, use `seatplus/esi-client` or `seatplus/eveapi`
directly — neither requires the web interface. If you would rather write your own front end,
`seatplus/auth` gives you the authentication, permission and affiliation model for free.
{% /callout %}
