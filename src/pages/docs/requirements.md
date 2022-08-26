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

| Type           | Requirement |
|:---------------|:------------|
| Docker         | ^ 20.10     |
| Docker Compose | ^ 1.29      |

