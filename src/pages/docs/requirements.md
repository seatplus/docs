---
title: Requirements
description: What you need before installing Seatplus — a Docker host, a public hostname, and enough CPU, memory and disk for the number of characters you track.
---

Seatplus is distributed only as a Docker installation. That keeps every instance on the same environment
as the developers run, which is what makes support possible for a project this size.

{% .lead %}

{% callout type="note" title="Traefik" %}
Seatplus ships with Traefik as its reverse proxy and orders TLS certificates for you. If you want to put
your own nginx or Apache in front of it instead, you are on your own. If you already run Traefik, you
will need to point the app at your existing external Docker network in `docker-compose.yml`.
{% /callout %}

---

## Hardware

The figures below are a starting point, not a hard limit. The left column is a small corporation
running Seatplus for its own members; the right column is an alliance-sized instance tracking several
hundred characters.

| Type        | Up to 25 characters      | Up to 500 characters     |
| :---------- | :----------------------- | :----------------------- |
| CPU         | 2 cores                  | 2 cores                  |
| Memory      | 2 GB of RAM (incl. swap) | 4 GB of RAM (incl. swap) |
| Local space | 8-10 GB                  | 15-20 GB                 |

Memory and CPU are mostly consumed by the queue workers that fetch data from ESI, so they scale with
how many characters you update and how often. Disk grows with the number of tracked characters and
with how much history you keep — assets, wallet journals and mails are all stored per character and
accumulate over time. Plan for the database to keep growing rather than to settle at a size.

{% callout type="warning" title="Watch your disk" %}
Running out of disk is the most common way a Seatplus instance breaks. Monitor free space on the volume
holding your Docker data, and size it for where you expect to be in a year.
{% /callout %}

---

## Software

| Type           | Requirement            |
| :------------- | :--------------------- |
| Docker Engine  | 24.0 or newer          |
| Docker Compose | v2 (any current release) |
| Git            | 2.25 or newer          |

{% callout type="note" title="Compose v2 and the missing dash" %}
Compose v1 (the standalone `docker-compose` Python tool) reached end of life and has been removed from
Docker. The current tool is Compose v2, which is a Docker CLI plugin invoked as `docker compose` with a
space.

Many installations still provide `docker-compose` as an alias for the v2 plugin, and the commands map
one to one. This documentation writes `docker-compose` throughout; if your host only has the plugin,
drop the dash and everything else stays the same.
{% /callout %}

---

## Network

The installation orders TLS certificates through Traefik, which means the certificate authority has to
be able to reach your server before you start. Have all of the following in place first:

- A hostname you control, for example `seatplus.yourdomain.com`.
- A DNS record for that hostname pointing at your server's public IP address, already propagated.
- Ports **80** and **443** reachable from the internet — open in your firewall and, if you are behind
  a router, forwarded to the host.
- An email address for the certificate authority. The Traefik bootstrap script asks for it.

If the hostname does not resolve or the ports are blocked, the certificate request fails and your
instance will not be reachable over HTTPS.

---

## Installing Docker and Git

1. Follow the [official Docker Engine instructions](https://docs.docker.com/engine/install/) for your
   distribution. The Docker Engine packages include the Compose v2 plugin.
2. If you need Compose separately, follow the
   [official Compose instructions](https://docs.docker.com/compose/install/).

{% callout type="note" title="Convenience script" %}
Docker does not recommend the convenience script for production hosts, but it installs Engine and the
Compose plugin in one step and we use it. On a Debian or Ubuntu based system:

```shell
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

{% /callout %}

Git is usually already present. If it is not:

```shell
sudo apt-get install git
```

Once all of this is in place, continue with
{% link href="/docs/installation" %}Installation{% /link %}.
