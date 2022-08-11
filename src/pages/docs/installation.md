---
title: Installation
description: Learn how to install Seatplus.
---

This section explains how to install Seatplus.

## Download base-app
You have several options to download the base app which you need to start Seatplus. Whereas git is probably the best
as it will allow you to update the base-app more easily.

1) git
2) wget
3) curl


Optionally create and navigate into your Seatplus directory where the app is going to be installed in

```shell
mkdir /opt/seatplus && cd /opt/seatplus
```

### git

{% callout type="note" title="Requirements" %}
if you haven't installed git you may need to install it `sudo apt-get install git`
{% /callout %}

run
```shell
git clone https://github.com/seatplus/base-app .
```

### wget
```shell
curl -LO https://github.com/seatplus/base-app/archive/refs/heads/main.zip
unzip main.zip
```

## Start Traefik
{% callout type="warning" title="Assumptions" %}
This guide assumes that no other webserver or forwardproxy is used.
If you have traefik already installed on your server or plan to use it, you might want to change the used docker-network.
{% /callout %}

1) create the external docker network

    ```shell
    docker network create traefik
    ```

2) in order to order SSL certificates for using https you must provide your email
    ```shell
    # It might be easier for some to alter the ./traefik/docker-compose.prod.yml file directly instead of the sed command
    # maybe use nano, vim or vi to do so.
    
    # If you wish you can use the sed below, just make sure to replace the second arguments email
    # only replace the part including the curly brackets 
    sed -i -- 's,      - "--certificatesresolvers.myresolver.acme.email=your@mail.com",      - "--certificatesresolvers.myresolver.acme.email={your@mail.com}",g' ./traefik/docker-compose.prod.yml
    ```
3) start traefik
    ```shell
    docker-compose -f traefik/docker-compose.yml -f traefik/docker-compose.prod.yml up -d
    ```

## Configure your app
We provided the base-app with a bootstrap shell script. Simply run it and enter the required information:
```shell
bash bootstraph.sh
```
Please refer to {% link href="configuration" %}Configuration{% /link %} in order to get more information of the available settings.


## Start the App
to start the app simply run
```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

Please refer to {% link href="admin" %}Admin{% /link %} for further information and guides of administrating your Seatplus install.
Topics may be: Superuser, Backup, Restore, Plugin Installation etc.

