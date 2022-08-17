---
title: Dev Environment
description: Learn how to setup a development environment.
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
bash bootstraph.sh
```

## Configure your development environment file

1) define PID and PGID
    This might be useful if you are working with a linux system.
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

## Start the App
to start the app simply run
```shell
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```


Please refer to {% link href="admin" %}Admin{% /link %} for further information and guides of administrating your Seatplus install.
Topics may be: Superuser, Backup, Restore, Plugin Installation etc.

{% callout type="note" title="Build Frontend Assets" %}
It might happen that the node container stops running and stops the webpack build. 
If this happens restart the container and run the following command: `docker-compose restart node`
{% /callout %}