---
title: Update
description: Update a running instance to the latest release within the same major version, run the migrations and verify the queue is working again.
---

When a new release of the underlying core packages lands, you update your instance to pick it up. This
page covers updates within the same major version. Crossing a major version is a different, larger
procedure — see {% link href="/docs/upgrade" %}Upgrade{% /link %}.

{% .lead %}

To hear about releases, watch the repositories on GitHub or join the
[Seatplus Discord](https://discord.gg/3UR5uDDMjK).

---

## Before you update

Take a backup. Composer will replace the application's dependencies and the migrations will alter your
database, and neither step has an undo. Follow
{% link href="/docs/admin#database-backups" %}Database backups{% /link %}, and keep your `.env` and
`src` directory alongside the dump — a database dump on its own is not enough to bring the instance
back.

Read the release notes for the versions you are skipping over before you start, so an intentional
breaking change does not arrive as a surprise.

---

## Update, in one go

{% callout type="warning" title="This runs migrations" %}
The command below updates the app, runs the database migrations and restarts the node and worker
services. If you have custom changes in your app, or you want to run the migrations yourself and look at
them first, use the step-by-step version below instead.
{% /callout %}

On your host:

```shell
docker-compose exec php composer update --no-dev && \
docker-compose exec php php artisan migrate --force && \
docker-compose restart node && \
docker-compose restart worker
```

Then jump to [verify the update](#verify-the-update).

---

## Update, step by step

Use this if you want control over each step, or if you are updating to a specific version rather than
the latest.

### Update the app

```shell
docker-compose exec php composer update --no-dev
```

### Run the migrations

```shell
docker-compose exec php php artisan migrate --force
```

### Restart node to rebuild the web assets

```shell
docker-compose restart node
```

### Restart the worker

The worker holds the old code in memory. Until you restart it, the new code is not applied to any queued
job.

```shell
docker-compose restart worker
```

### Optional: enter the shell to install packages

```shell
docker-compose exec php bash
```

---

## Verify the update

An update that appears to have finished can still have left the instance broken. Check both of these:

1. **The app loads.** Open your instance and sign in. A blank page or a 500 usually means the
   migrations did not complete, or the node container has not finished rebuilding the assets — give it a
   minute, then read the logs with `docker-compose logs --tail 10 -f`.
2. **The queue is processing jobs.** Open **Settings → Server Settings** and confirm Horizon reports an
   active status with workers running. If the worker did not come back up, nothing will update from ESI
   even though every page loads. See
   {% link href="/docs/updating-data" %}Updating data from ESI{% /link %}.

If either check fails and the logs do not explain it, restore your backup rather than leaving the
instance half-updated.
