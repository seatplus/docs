---
title: Dev environment
description: Set up a local Seatplus development environment using the same container architecture as production.
---

This section explains how to install the development environment. The development environment is a combination of a local docker-compose and a local traefik.
Seatplus aims to use the same container architecture as the production environment whilst enabling the best developer experience. 
This is why you need the base-app for development.

{% callout type="note" title="Assumptions" %}
This guide assumes you have docker and docker-compose installed. Furthermore, it assumes that you have git and php installed.
{% /callout %}

## Download base-app

Optionally create and navigate into your Seatplus directory where the app is going to be installed in

```shell
mkdir seatplus && cd seatplus
```

run
```shell
git clone https://github.com/seatplus/base-app .
```


## Start Traefik

1) create the external docker network

    ```shell
    docker network create traefik
    ```

2) start traefik
    ```shell
    docker-compose -f traefik/docker-compose.yml -f traefik/docker-compose.dev.yml up -d
    ```

## Bootstrap your app
We provided the base-app with a bootstrap shell script. It is designed for productive installations but you can use it for development as well.

```shell
bash bootstrap.sh
```

## Configure your development environment file

1) set `PUID` and `PGID` to your own user and group id
    On Linux, set these so files the containers create are owned by you rather than by root. Run
    `id -u` and `id -g` to find your values. See [Configuration](/docs/configuration).
2) turn on debug mode
    ```shell
    APP_DEBUG=true
    ```
3) change APP_ENV to local
    ```shell
    APP_ENV=local
    ```

## Configure your development environment container

Inside the `docker-compose.dev.yml` file you can find the following configuration:

* DB Port: 3306 (User and PW you can find in the `.env` file)

if needed change the port in the `docker-compose.dev.yml` file

## Prepare source files

Seatplus requires the `/src` directory to be present. This directory contains the source code of the app.

1) Inside the base-app create and navigate to the src folder
    ```shell
    mkdir src && cd src
    ```

2) Run the following command to create the application in the `/src` directory:

    ```shell
    php composer create-project seatplus/core . --prefer-dist --no-dev --no-ansi
    ```

## Start the app

```shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

{% callout type="note" title="Frontend assets" %}
The node container can stop and take the asset build with it. If the interface stops picking up your
changes, restart it: `docker-compose restart node`
{% /callout %}

## Next steps

A freshly created instance grants nobody any access and fetches nothing from EVE until it is
configured. Work through [First run](/docs/first-run) to claim `superuser`, create the update
schedules and set your ESI scope requirements.

Note that some behaviour differs in a development environment. In particular, the check that blocks
pages until a user has granted every required ESI scope **short-circuits outside a `production`
environment**, so with `APP_ENV=local` you will never be prompted and everything will look compliant.
Validate scope configuration against a production-mode instance.

[Administration tasks](/docs/admin) covers backups, restores, running migrations and installing
plugins. To work on the Seatplus packages themselves rather than just running the app, continue to
[Package development](/docs/contributing/packages).