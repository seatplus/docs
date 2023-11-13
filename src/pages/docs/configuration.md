---
title: How to configure
description: Learn more about the various configuration options.
---

This section explains how to configure seatplus. Whenever you do change
the `.env` File, you should run the following command to pickup changes
within the docker containers:

``` shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

## PUID & PGID
These values are of relative importance regarding the file permissions. You should not be in need to change them

## QUEUE_WORKERS
These can be increased and decreased as much as you need. Just make sure your server is able to provide enough
computational power. Sometimes less is more.

## PHP Settings
Sometimes you need to  increase the memory limit and max execution time for heavy queries. You may achieve this by
altering the following settings.
```dotenv
PHP_MEMORY_LIMIT=256M
PHP_MAX_EXECUTION_TIME=99
```

## ESI

In order to be able to consume EVE Online related data you must register
your application in the
[EVE Online Developers portal](https://developers.eveonline.com/applications)

1. Register your application on the EVE Online Developers portal for
   both Authentication and API Access.
   * Select the connection type to be of `Authentication & API Access`
   * Select all Permissions (💡 these are all the scopes the application
     could theoretically access, which are used by the end of the day is
     configured later in seatplus).
   * Set your callback-url f.e.
     `https://seatplus.yourdomain.com/auth/eve/callback`

{% callout type="warning" title="Use your own values" %}
You must replace `https://seatplus.yourdomain.com` with *your* qualified
url which is accesible from the internet  
{% /callout %}

2. Configure your `EVE_CLIENT_ID`, `EVE_CLIENT_SECRET` and `EVE_CALLBACK_URL`
   in the .env configuration file

```{2-4}
# Eve Online SSO Configuration 
EVE_CLIENT_ID=null
EVE_CLIENT_SECRET=null
EVE_CALLBACK_URL=https://seatplus.yourdomain.com/auth/eve/callback
```

## Custom Logo / Favicon
You can replace the default logo and favicon by adding your files in the
`/src/public/img` folder. You may use any name you like. Just make sure not to 
name them `seat_plus.svg` or `seat_plus_logo.svg` as these are reserved for the default
and may be overwritten on updates.

Following requirements apply:
- Favicon: SVG Format, 1:1 Aspect Ratio, 52x52px
- Logo: SVG Format, 220x52px

add the following to your `.env` file:
```dotenv
LOGO_PATH=img/logo.svg
ICON_PATH=img/icon.svg
```

