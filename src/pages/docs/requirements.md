---
title: Hard- & Software Requirements
description: 2 CPU, 2 GB RAM, 8-10 GB and docker-compose this what you need to start with seatplus.
---


As seatplus is a one-man project it will only be available as
docker-based installation. This ensures that users of seat-plus have the
same environment as the developers and allows for better support in any
case.

{% callout type="note" title="Traefik" %}
Seatplus ships with traefik as a reverse proxy server. If you wish to configure your own nginx or apache server you are
on yourself. If you have already traefik in use you may need to alter the external docker network inside the `docker-compose.yml` file.
{% /callout %}


## Hardware Requirements

| Type                    | up to 25 characters                             | Up to 500 Characters     |
|:------------------------|:------------------------------------------------|:-------------------------|
| CPU                     | 2 core                                          | 2 core                   |
| Memory                  | 2 GB of RAM (incl. swap)                        | 4 GB of RAM (incl. swap) |
| Local Space             | 8-10 GB                                         | 15-20 GB                 |

{% callout type="warning" title="Disk space" %}
Disk space requirements tend to grow the more character and the more history is persisted
{% /callout %}

## Software Requirements

| Type           | Requirement   |
|:---------------|:--------------|
| Docker         | ^ 20.10       |
| Docker Compose | ^ 1.29, ^2.10 |
| Git            | ^ 2.25        |

{% callout type="note" title="Docker compose version" %}
Docker Compose v2 brings Compose functionality into Docker itself. You’ll be able to use Compose wherever the latest Docker CLI is installed, no extra steps required. Underneath, Docker continues to use the features provided by the Compose project.

Existing docker-compose commands should map directly to their new docker compose counterparts. In most cases, you can drop the dash with no further changes required.

This documentation will use the old docker-compose commands. If you are using docker-compose v2 you may drop the dash.
{% /callout %}

### Installation of Docker & Docker Compose

1) Please follow the [official instructions](https://docs.docker.com/engine/install/) for installing docker on your system.
2) Please follow the [official instructions](https://docs.docker.com/compose/install/) for installing docker-compose on your system.

{% callout type="note" title="Convinience Scripts" %}
Alltough Docker does not reccomend to use the convenience scripts, we do. If you are using an ubuntu based system you may use the following script to install docker && docker compose in one go.

```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
{% /callout %}

### Installation of git

You may need to install it

```shell
sudo apt-get install git
```

