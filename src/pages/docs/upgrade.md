---
title: Upgrade
description: Cross a major version of the Seatplus core packages, including the community-contributed procedures for v4.x and v3.x.
---

An upgrade crosses a major version of the underlying core packages — usually because the framework
Seatplus is built on, Laravel, has had a major release of its own. Staying on the same major version and
picking up the latest release is an {% link href="/docs/update" %}update{% /link %} and is much less
involved; come here only when the major number changes.

{% .lead %}

{% callout type="warning" title="Read this before you run anything below" %}
These procedures are community-contributed. They are not covered by automated testing, and nobody
verifies them against a fresh instance before each release, so treat them as a starting point rather
than a guarantee.

**Take a full backup first** — the database, your `.env` and your `src` directory — and confirm you know
how to restore it. See {% link href="/docs/admin" %}Administration tasks{% /link %}. Some steps below
move or replace your `src` directory, and there is no undo. If you are running an instance other people
depend on, do the upgrade at a time when you can afford for it to be down while you restore.
{% /callout %}

---

## Which version are you on?

There is no version banner in the interface to read this off, and we would rather point you at a file
than hand you a command we cannot verify against your install. Open `src/composer.json` in your base-app
directory and look at the `require` section. The constraint on `seatplus/web` is the major version your
instance is pinned to:

```json
"require": {
    "seatplus/web": "^3.0",
    ...
```

That tells you which of the procedures below applies. Upgrade one major version at a time — do not skip a
major by editing the constraint straight to the newest.

`src/composer.lock` in the same directory records the exact versions Composer actually installed, if you
need more detail than the constraint gives you.

---

## Upgrading to v4.x

This raises `seatplus/web` to v4.0. The `src` directory is kept in place; only the dependency constraint
changes.

On your host:

1. Change into the `src` directory:

   ```shell
   cd ./src
   ```

2. Edit `composer.json` and require the new major version of `seatplus/web`:

   ```json
   "require": {
       "seatplus/web": "^4.0",
       ...
   ```

3. Change back to the base-app directory:

   ```shell
   cd ..
   ```

4. Update the app:

   ```shell
   docker-compose exec php composer update --no-dev
   ```

5. Restart node so the web assets are rebuilt:

   ```shell
   docker-compose restart node
   ```

6. Run the migrations:

   ```shell
   docker-compose exec php php artisan migrate --force
   ```

7. Restart the worker so queued jobs run the new code:

   ```shell
   docker-compose restart worker
   ```

If you need to reinstall packages afterwards, enter the container:

```shell
docker-compose exec php bash
```

Then work through [after the upgrade](#after-the-upgrade).

---

## Upgrading to v3.x

This procedure replaces the `src` directory rather than editing it, which is why the backup matters
more here. Your database, volumes and `.env` are untouched — but the packages you installed and anything
you customised inside `src`, such as a logo in `src/public/img`, are in the directory being moved aside.
Write down which packages you have before you start; you reinstall them at the end.

On your host, from your base-app directory:

1. Take the app down:

   ```shell
   docker-compose down
   ```

2. Move your existing `src` directory aside:

   ```shell
   mv ./src ./backup_src
   ```

3. Install the new core package into a fresh `src`:

   ```shell
   docker-compose run --rm php composer create-project seatplus/core . --prefer-dist --no-dev --no-ansi
   ```

4. Fix the file ownership. Use the same user and group you used originally — `1000:1000` unless you
   changed `PUID`/`PGID` in your `.env`, see
   {% link href="/docs/configuration" %}Configuration{% /link %}:

   ```shell
   chown -R 1000:1000 src
   ```

5. Start the app again:

   ```shell
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

6. Run the migrations:

   ```shell
   docker-compose exec php php artisan migrate
   ```

7. Reinstall your packages, entering the container if that is easier:

   ```shell
   docker-compose exec php bash
   ```

Keep `./backup_src` until the instance is verified working. It is the only copy of your previous
install's source, and comparing its `composer.json` against the new one is the quickest way to work out
which packages you are missing.

---

## After the upgrade

Check all three before you call it done:

1. **The app loads and you can sign in.**
2. **Horizon is processing jobs.** Open **Settings → Server Settings** and confirm the worker status is
   active. See {% link href="/docs/updating-data" %}Updating data from ESI{% /link %}.
3. **Your plugins are back.** A replaced `src` directory means every package you added is gone until you
   reinstall it — see {% link href="/docs/admin#add-a-package" %}Add a package{% /link %}.

If something is broken and the logs do not explain it, restore the backup you took at the start rather
than debugging a half-upgraded instance.
