---
title: Administration tasks
description: The command-line tasks that keep a Seatplus instance running — logs, migrations, packages, the superuser command, and database backup and restore.
---

These are the things you do from the host rather than from the web interface. Every command is run from
your base-app checkout, the directory holding `docker-compose.yml`.

{% .lead %}

---

## Reading logs

Start here whenever something misbehaves. This follows the combined output of every container, which is
usually enough to see a container crash-looping or failing to start:

```shell
docker-compose logs --tail 10 -f
```

Container output is not the whole picture. Laravel writes its own log inside the `php` container, under
`storage/logs` in the application directory, and that is where application-level stack traces end up —
[enter the container](#enter-the-container) to read it.

Failed queue jobs do not appear in either place in a useful form. Those live in Horizon, which lists
failed jobs with their exceptions and lets you retry them. If data is not updating, Horizon is the place
to look — see {% link href="/docs/updating-data" %}Updating data from ESI{% /link %}.

---

## Enter the container

The application, its Composer dependencies and its `artisan` command all live in the `php` container.
Whenever documentation or a support thread tells you to run an `artisan` command, this is where you run
it:

```shell
docker-compose exec php bash
```

---

## Run migrations

Run this after any update or after installing a package that ships its own tables. If a page throws an
error about a missing column or table straight after an update, this is almost always what is missing:

```shell
docker-compose exec php php artisan migrate
```

---

## Add a package

Plugins are Composer packages. You can either edit `src/composer.json` directly or use Composer inside
the container:

```shell
docker-compose exec php composer require vendor/package
```

Most packages then need their migrations run and their assets published, so it is often less work to
[enter the container](#enter-the-container) and do all of it in one session. If the package adds
anything to the user interface, restart the node container afterwards so the web assets are rebuilt:

```shell
docker-compose restart node
```

---

## Assign the superuser

You need this exactly once, when setting up a new instance: the first administrator cannot be created
from the web interface. Run it [inside the container](#enter-the-container):

```shell
php artisan seatplus:assign:superuser "Character Name"
```

The command is interactive. It looks up the accounts matching the character name you passed, prints them
with their user ids, asks you which user id should become superuser, and asks you to confirm before
making the change.

{% callout type="warning" title="It refuses to run twice" %}
If a superuser already exists, the command does not run. It prints the accounts that currently hold the
`superuser` permission instead, so you can see who to ask. Further administrators are appointed from the
web interface by adding them to a control group that holds the permissions they need — see
{% link href="/docs/concepts/permissions" %}Permissions and control groups{% /link %}.
{% /callout %}

First-time setup, including this step in context, is covered in
{% link href="/docs/first-run" %}First run{% /link %}.

---

## Database backups

Take a backup before every {% link href="/docs/update" %}update{% /link %} and
{% link href="/docs/upgrade" %}upgrade{% /link %}, and on a schedule besides. The database holds
everything Seatplus has ever fetched, and much of it — historical wallet journals, mails, expired contracts
— cannot be fetched again from ESI once it is gone.

```shell
docker-compose exec mariadb sh -c 'exec mysqldump "$MARIADB_DATABASE" -u"$MARIADB_USER" -p"$MARIADB_PASSWORD"' | gzip > seatplus_backup.sql.gz
```

{% callout type="warning" title="A database dump alone is not a backup of your install" %}
Restoring from only a database dump leaves you unable to bring the instance back up. You also need:

- **`.env`** — it holds your database password and your EVE application credentials. Without it the
  restored database cannot be opened by a new install, and your users cannot log in.
- **the `src` directory** — the application source and the plugins you installed, plus anything you
  customised such as a logo in `src/public/img`. It can be recreated, but only if you know exactly which
  packages and versions you had.

Keep all three together, and keep at least one copy on a different machine than the one running Seatplus.
{% /callout %}

A few things worth doing that the command above does not do for you:

- **Automate it.** A cron job on the host that runs the dump and rotates the output is the minimum.
- **Keep more than one.** A single overwritten dump is one bad night away from being a backup of a
  broken database. Keep a rolling set — daily for a week, weekly for a month is a reasonable shape.
- **Verify a restore.** An untested backup is a guess. Restore into a throwaway instance occasionally
  and confirm you can sign in and see your data. Restoring is the only thing that proves a backup
  worked.

---

## Database restore

Run this against an instance whose containers are up but whose database you are willing to overwrite:

```shell
zcat seatplus_backup.sql.gz | docker-compose exec -T mariadb sh -c 'exec mysql "$MARIADB_DATABASE" -u"$MARIADB_USER" -p"$MARIADB_PASSWORD"'
```

Afterwards, run the [migrations](#run-migrations) — a dump from an older version may be behind the
schema your current code expects.

{% callout type="note" title="These commands assume base-app's MariaDB" %}
Both the backup and the restore command target the `mariadb` service and the `MARIADB_*` environment
variables that base-app's default `docker-compose.yml` provides. If you moved your database to an
external server or a different image, the commands will not work unchanged.
{% /callout %}
