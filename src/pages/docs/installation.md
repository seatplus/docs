---
title: Installation
description: Learn how to install Seatplus.
---

This section explains how to install Seatplus.

## Preflight checks

Before you start the installation process, please make sure that you have the following requirements met:

* Docker and Docker Compose installed
```shell
$ docker -v
Docker version 20.10.18, build b40c2f6
$ docker-compose -v
docker-compose version 1.29.2, build 5becea4c
```
* git
```shell
$ git --version
git version 2.25.1
```
If you miss any of these requirements, please review the {% link href="requirements" %}requirements{% /link %} section where you can find instructions on how to install them.


## Download base-app
You have several options to download the base app which you need to start Seatplus. Whereas git is probably the best
as it will allow you to update the base-app more easily.

Optionally create and navigate into your Seatplus directory where the app is going to be installed in

```shell
mkdir /opt/seatplus && cd /opt/seatplus
```

clone the base-app into the seatplus folder:
```shell
git clone https://github.com/seatplus/base-app .
```

## Start Traefik
{% callout type="warning" title="Assumptions" %}
This guide assumes that no other webserver or reverse proxy is used.
If you have traefik already installed on your server or plan to use it, you might want to change the used docker-network.
{% /callout %}

1) create the external docker network

    ```shell
    docker network create traefik
    ```

2) in order to order SSL certificates for using https you must provide your email.
    Run the bootstrap script within the traefik folder and provide your email address
    ```shell
    cd traefik && bash bootstrap.sh
    ```
3) start traefik from within the traefik folder
    ```shell
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    ```

## Prepare your app
We provided the base-app with a bootstrap shell script. Simply run it and enter the required information:
```shell
cd .. && bash bootstraph.sh
```

Please refer to {% link href="configuration" %}Configuration{% /link %} in order to get more information of the available settings.

### Prepare source files

Seatplus requires the `/src` directory to be present. This directory contains the source code of the app.
Run the following command to create the application in the `/src` directory:

```shell
docker-compose run --rm php composer create-project seatplus/core . --prefer-dist --no-dev --no-ansi
```

Since files are owned by root, you need to change the ownership of the files. Traditionally, you would do this for www-data, 
but since we are using a docker container, we use an arbitary user 1000 in usergroup 1000. If your setup has already a www-data user,
you might change the PUID and PGID inside the `.env` to match your setup. For all other users the command below will suffice.

```shell
chown -R 1000:1000 src
```

### Start the App
to start the app simply run
```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Run the database migrations
```shell
docker-compose exec php php artisan migrate
```

now seatplus is ready to use.

### Assign superuser
After you have created your first user, you need to assign the superuser role to it. Learn how to do this in the  {% link href="admin#create-superuser" %}Admin{% /link %} section.

{% callout type="note" title="Administration" %}
Please refer to {% link href="admin" %}Admin{% /link %} for further information and guides of administrating your Seatplus install.
Topics may be: Superuser, Backup, Restore, Plugin Installation etc.
{% /callout %}


