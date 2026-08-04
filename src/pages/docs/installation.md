---
title: Installation
description: Install Seatplus from the base-app repository with Docker Compose, from cloning the repository to running the first migration.
---

This page takes you from an empty Docker host to a running Seatplus instance. Work through the steps in
order — each one depends on the one before it.

{% .lead %}

---

## Preflight checks

Before you start, confirm the tooling is present.

- Docker and Docker Compose

  ```shell
  $ docker -v
  Docker version 24.0.6
  $ docker-compose -v
  Docker Compose version v2.21.0
  ```

- Git

  ```shell
  $ git --version
  git version 2.25.1
  ```

If anything is missing, or if you have not yet pointed a hostname at this server, go back to
{% link href="/docs/requirements" %}Requirements{% /link %}. The install orders TLS certificates, so
DNS and ports 80/443 need to be in place before you begin.

---

## Download base-app

Everything you need to run Seatplus lives in the `base-app` repository. Cloning it with Git is the option
we recommend, because it is also how you pick up changes to the Compose files later.

Create and enter the directory the app will live in:

```shell
mkdir /opt/seatplus && cd /opt/seatplus
```

Clone base-app into it:

```shell
git clone https://github.com/seatplus/base-app .
```

Every command on this page and in the rest of the administration documentation is run from this
directory.

---

## Start Traefik

{% callout type="warning" title="Assumptions" %}
This guide assumes no other web server or reverse proxy is running on the host. If you already use
Traefik, or plan to, you will want to change the Docker network the app attaches to.
{% /callout %}

1. Create the external Docker network:

   ```shell
   docker network create traefik
   ```

2. Traefik needs your email address to order TLS certificates. Run the bootstrap script inside the
   `traefik` directory and enter it:

   ```shell
   cd traefik && bash bootstrap.sh
   ```

3. Start Traefik from the same directory:

   ```shell
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

---

## Prepare your app

base-app ships a second bootstrap script, in the repository root, which creates your `.env` file from
`.env.example`. Run it and answer its questions:

```shell
cd .. && bash bootstrap.sh
```

The script refuses to run if a `.env` already exists, so it is safe to check before you start. It
generates a database password for you and asks you for the public URL of your instance and for the
`Client ID` and `Secret Key` of your EVE Online application. It writes those answers into `.env` and
sets the matching hostname in `docker-compose.prod.yml`.

If you do not have EVE application credentials yet, register the application first — the steps and
every other variable you can set are covered in
{% link href="/docs/configuration" %}Configuration{% /link %}. You can also edit `.env` by hand
afterwards; nothing the script writes is final.

---

## Prepare source files

Seatplus needs a `src` directory in the repository root holding the application's source code. Create it
with Composer inside the `php` container:

```shell
docker-compose run --rm php composer create-project seatplus/core . --prefer-dist --no-dev --no-ansi
```

Composer runs as root in the container, so the resulting files are owned by root and the application
cannot write to them. Hand them to the user the containers run as:

```shell
chown -R 1000:1000 src
```

{% callout type="note" title="Match the ownership to your PUID and PGID" %}
`1000:1000` is correct for the default `PUID` and `PGID` in `.env`. If you changed either of them — for
example to line up with an existing `www-data` user — chown to those values instead. Ownership that
does not match `PUID`/`PGID` shows up as permission errors from the application, not as an install
failure. See {% link href="/docs/configuration" %}Configuration{% /link %}.
{% /callout %}

---

## Start the app

```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Run the database migrations

The database starts empty. Build the schema:

```shell
docker-compose exec php php artisan migrate
```

---

## Next: first run

The containers are now running, and your instance is reachable — but it does nothing yet. A freshly
installed Seatplus has no administrator, requires no ESI scopes and has no schedules, which means it
fetches nothing from EVE and grants nobody access until you configure it.

Continue with {% link href="/docs/first-run" %}First run{% /link %}, which covers signing in, claiming
the `superuser` permission, creating the schedules and deciding which scopes you require.

{% callout type="note" title="Day-to-day administration" %}
Once you are up and running, {% link href="/docs/admin" %}Administration tasks{% /link %} covers
backups, restores, adding packages and reading logs.
{% /callout %}
