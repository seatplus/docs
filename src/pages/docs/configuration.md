---
title: Configuration
description: The environment variables in your .env file that you are most likely to change, and how to register the EVE application Seatplus authenticates against.
---

Seatplus is configured through the `.env` file in the root of your base-app checkout. The bootstrap script
you ran during {% link href="/docs/installation" %}installation{% /link %} created it and filled in the
essentials; this page covers the variables you are most likely to change afterwards.

{% .lead %}

Whenever you change `.env`, recreate the containers so they pick the new values up:

```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

---

## Variables covered here

This is not the complete list of variables in `.env` — it is the set this page explains. Where a
default is shown as **—**, base-app does not ship one and the value comes from the container image or
the application, so check your own `.env` rather than assuming.

| Variable                 | Purpose                                                        | Default            |
| :----------------------- | :------------------------------------------------------------- | :----------------- |
| `PUID`                   | User id the containers run as; must own the `src` directory     | `1000`             |
| `PGID`                   | Group id the containers run as                                  | `1000`             |
| `QUEUE_WORKERS`          | Number of queue workers processing ESI update jobs              | —                  |
| `PHP_MEMORY_LIMIT`       | PHP memory limit inside the container                           | —                  |
| `PHP_MAX_EXECUTION_TIME` | PHP maximum execution time inside the container                 | —                  |
| `EVE_CLIENT_ID`          | Client id of your EVE Online application                        | `null`             |
| `EVE_CLIENT_SECRET`      | Secret key of your EVE Online application                       | `null`             |
| `EVE_CALLBACK_URL`       | SSO callback URL; must match the one registered with CCP        | `null`             |
| `ONBOARDING`             | Enables the onboarding wizard for new users                     | off                |
| `LOGO_PATH`              | Path to a custom logo, relative to `src/public`                 | built-in logo      |
| `ICON_PATH`              | Path to a custom favicon, relative to `src/public`              | built-in icon      |

Everything not listed here — `APP_URL`, `APP_ENV`, the `DB_*` and `REDIS_*` variables — is set by the
bootstrap script or by base-app's defaults, and you should have a reason before changing it.

---

## PUID and PGID

These control which user and group the containers run as, and therefore which user has to own the
`src` directory on the host. They default to `1000:1000` and most installations never need to change
them. If you do change them, `chown -R` the `src` directory to match, or the application will fail with
permission errors it cannot explain to you.

---

## QUEUE_WORKERS

Every piece of data Seatplus holds is fetched by a queued job, so this variable directly controls how fast
your instance updates. Increase it if update batches are backing up, decrease it if the host is
struggling — more workers on a machine that cannot feed them is slower, not faster.

The queue only runs if Laravel Horizon and Redis are running. If they are not, schedules fire and
nothing happens: jobs pile up and every page stays stale. Check Horizon's status before you touch this
number. See {% link href="/docs/updating-data" %}Updating data from ESI{% /link %}.

---

## PHP settings

Heavy queries — large asset lists, long wallet histories — can exceed PHP's defaults. Raise them in
`.env`:

```dotenv
PHP_MEMORY_LIMIT=256M
PHP_MAX_EXECUTION_TIME=99
```

---

## ONBOARDING

Off by default. When enabled, new users are walked through a wizard on first sign-in that asks them to
add their other characters and shows them your open job postings — useful if your instance is the front
door for recruitment.

```dotenv
ONBOARDING=true
```

See {% link href="/docs/server-settings" %}Server settings{% /link %} for the rest of the
instance-wide switches.

---

## ESI

To read EVE Online data, Seatplus authenticates as an application you own. Register it in the
[EVE Online Developers portal](https://developers.eveonline.com/applications).

1. Register your application for both authentication and API access.
   - Set the connection type to `Authentication & API Access`.
   - Select all permissions. These are the scopes your application *could* request; which ones your
     members are actually asked for is configured inside Seatplus later — see
     {% link href="/docs/concepts/sso-scopes" %}ESI scopes and compliance{% /link %}.
   - Set the callback URL, for example
     `https://seatplus.yourdomain.com/auth/eve/callback`.
2. Put the resulting `EVE_CLIENT_ID`, `EVE_CLIENT_SECRET` and `EVE_CALLBACK_URL` into your `.env`:

   ```dotenv
   # Eve Online SSO Configuration
   EVE_CLIENT_ID=null
   EVE_CLIENT_SECRET=null
   EVE_CALLBACK_URL=https://seatplus.yourdomain.com/auth/eve/callback
   ```

{% callout type="warning" title="Use your own values" %}
Replace `https://seatplus.yourdomain.com` with *your* fully qualified URL, the one reachable from the
internet. The callback URL in `.env` and the one registered with CCP must match exactly, or SSO will
refuse the login.
{% /callout %}

---

## Custom logo and favicon

Put your own files in `src/public/img`. Any filename works, except `seat_plus.svg` and
`seat_plus_logo.svg` — those are the defaults and may be overwritten when you update.

These requirements apply:

- Favicon: SVG, 1:1 aspect ratio, 52x52px
- Logo: SVG, 220x52px

Then point `.env` at them:

```dotenv
LOGO_PATH=img/logo.svg
ICON_PATH=img/icon.svg
```
