---
title: How to contribute
description: Where the code lives, what skills are useful, and how to get a change from an idea into a merged pull request.
---

Seatplus is a hobby project by [Herpaderp Aldent](https://evewho.com/character/95725047). Help with
development, testing and documentation is genuinely wanted, and there is useful work at every level of
experience.

{% .lead %}

---

## Start here, whatever your background

| If you | Start with |
| --- | --- |
| Have not written code and do not intend to | File bug reports and feature requests on [GitHub](https://github.com/seatplus/seatplus/issues), and talk to us on [Discord](https://discord.gg/3UR5uDDMjK) |
| Want to help without setting up an instance | [Writing docs](/docs/contributing/writing-docs) — no PHP, no database, no EVE application needed |
| Know PHP and Laravel | The backend packages: `eveapi`, `auth`, `esi-client` |
| Know Vue but not PHP | The `web` package's Vue pages and components |
| Can write JavaScript tests | Frontend test coverage, which is the thinnest part of the project |
| Are learning either stack | Ask on Discord for something small and scoped — this is a good project to learn on |

The stack is Laravel with Inertia, Vue 3 and Tailwind CSS. Knowing any one of those is enough to be
useful.

---

## How the code is organised

Seatplus is not one repository. It is a set of Composer packages assembled by a core application, and
which repository you work in depends on what you are changing.

| Repository | Contains |
| --- | --- |
| [core](https://github.com/seatplus/core) | The Laravel application that assembles the packages. Where the app is actually run, built and browser-tested |
| [web](https://github.com/seatplus/web) | The web interface: routes, controllers, Inertia pages, Vue components |
| [eveapi](https://github.com/seatplus/eveapi) | The data layer: models, ESI jobs, scope definitions |
| [auth](https://github.com/seatplus/auth) | Authentication, permissions, control groups, affiliations |
| [esi-client](https://github.com/seatplus/esi-client) | A standalone ESI client library |
| [esi-schema](https://github.com/seatplus/esi-schema) | ESI schema handling |
| [docs](https://github.com/seatplus/docs) | This documentation site |
| [base-app](https://github.com/seatplus/base-app) | The Docker Compose setup end users install |

{% callout type="note" title="The web package cannot run on its own" %}
`web` has no `artisan` and no application to serve. To see a frontend change in a browser you need it
linked into a `core` checkout, which is also the only place the browser tests exist. Set that up with
[Dev environment](/docs/contributing/installation) and
[Package development](/docs/contributing/packages).
{% /callout %}

---

## Getting a change merged

1. **Talk about it first if it is not small.** Open an issue or ask on Discord. It saves you building
   something that will not be accepted, and it is how you find out whether someone is already on it.
2. **Work on a branch** in a fork, off the current development branch rather than a release tag.
3. **Write tests.** The backend packages use [Pest](https://pestphp.com), and each has its own
   `composer run test`. Coverage and type coverage are enforced in CI, so an untested addition will
   fail the build rather than merely be frowned upon.
4. **Run the linters** the package configures — the PHP packages use PHPStan and a code-style fixer;
   `web` and `docs` use ESLint.
5. **Open a pull request** against the repository you changed. If a change spans packages, say so in
   each pull request and link them, since they will need to be merged and released together.
6. **Expect review.** This is a small project; feedback is usually direct and quick.

If you are changing the web interface, note that CI validates the production frontend build inside
`core`, not inside `web` — a package has no application to build against. A change that lints cleanly
in `web` can still break the real build, so run it in `core` before you open the pull request.

---

## What makes a good bug report

Because Seatplus mirrors EVE's API into its own database, "it does not work" is nearly always one of a
few distinct things — and telling them apart in your report saves a round trip:

- **Is the queue running?** Check the Horizon worker stats on **Settings → Server Settings**. See
  [Updating data from ESI](/docs/updating-data).
- **Do schedules exist?** A fresh instance has none, so nothing updates.
- **Does the character's token carry the scope?** Without it the data was never fetched, so an empty
  page is expected. See [ESI scopes and compliance](/docs/concepts/sso-scopes).
- **Is it a permission problem?** Permissions are cached for about five minutes, and a member whose
  account is not compliant silently loses their group's permissions. See
  [Permissions and control groups](/docs/concepts/permissions).

Include your Seatplus version, whether you are running in production mode, and what the logs say.
Several behaviours — scope enforcement in particular — only apply in a production environment.

---

## Where to talk

| Channel | Purpose |
| --- | --- |
| [GitHub issues](https://github.com/seatplus/seatplus/issues) | Bug reports, feature requests |
| [Discord](https://discord.gg/3UR5uDDMjK) | Questions, support, deciding what to work on |
