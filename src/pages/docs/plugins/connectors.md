---
title: Connectors
description: Plugins that integrate tribes and/or broadcasts and offers ability to sync members to channels and send out notifications.
---

This is page provides a collection of plugins that bring additional functionality to seatplus. The following list is not exhaustive and will be updated as new plugins are developed.
Packages marked as broadcast are able to send out notifications to connectors implementation of channels.
Packages marked as tribe are able to sync members to connectors implementation of channels.
This page also contains a general installation guide for all plugins with the example of `discord` plugin.

## Plugins

| Package | Version |                      Tribes                      |  Broadcasts  | Comments                              |
|---------|---------|:------------------------------------------------:|:------------:|---------------------------------------|
| [Discord](https://github.com/seatplus/discord) | [![Latest Version on Packagist](https://img.shields.io/packagist/v/seatplus/discord.svg?style=flat-square)](https://packagist.org/packages/seatplus/discord)     |                        ✅                         |      ✅       | Sample package maintained by seatplus |
|         |         |                                                  |              |                                       |
|         |         |                                                  |              |                                       |
|         |         |                                                  |              |                                       |


## General Installation Guide

### Setup

Before you usually start the installation process you should follow the instructions in the package documentation. 

For the `discord` package you should create a discord bot and invite it to your server. 

### Create a discord application

* Go to https://discord.com/developers/applications
* Create a new application and give it a name
* Go to OAuth2
    * Add a redirect url (e.g. {seatplus-public-url}/discord/callback)
* Go to Bot
    * Add a bot
    * Enable "require OAuth2 code grant"
    * Enable "Server Members Intent"

### Retrieve credentials

Below you find instructions on where to find the credentials and how to fill them into your .env file

* From the oauth2 tab copy the `client id`, `client secret` and `redirect uri` tab copy the `token` (sometimes you need to reset the token first)

```dotenv
DISCORD_CLIENT_ID=  // your discord client id
DISCORD_CLIENT_SECRET= // your discord client secret
DISCORD_BOT_TOKEN= // your discord bot token
DISCORD_REDIRECT_URI= // your discord redirect uri
```

In order to propagate the changes you need to up the docker containers:
```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Installation


{% callout type="note" title="How to install the package" %}
Please review the {% link href="admin#add-package" %}admin guide{% /link %} for information on how to add a package to seatplus
{% /callout %}


1) Install the package
    ```bash
    composer install seatplus/discord
    ```

2) Run migrations
    ```bash
    php artisan vendor:publish --tag="web"
    php artisan migrate
    ```
   
3) Restart the node container (do this outside of the container)
    ```bash
    docker-compose restart node
    ```

### Register the connector

1) On first login, the superuser will be prompted to connect their discord account.

{% figure src="/images/plugins/connectors/register.png" alt="Register connector" /%}

2) follow the connectors instructions to connect your discord account.

{% figure src="/images/plugins/connectors/connect_1.png" alt="Connect discord" /%}

{% figure src="/images/plugins/connectors/connect_2.png" alt="Approve preselects" /%}

3) After connecting your account you will be able to see the connector and enable it.

{% figure src="/images/plugins/connectors/enable.png" alt="Enable connector" /%}

## Usage

Note every plugin has its own usage instructions. Please refer to the package documentation for further information.

### Tribes

Discord plugin allows you to set nickname policies for your discord server. This is done by setting up a tribe. 

{% figure src="/images/plugins/connectors/tribe.png" alt="Tribe" /%}

Based on the control groups users are assigned to, the discord roles are assigned. This means channel access is controlled by the control groups.

### Broadcasts

Based on the available broadcasts you can send out notifications to discord channels. 

{% figure src="/images/plugins/connectors/broadcasts.png" alt="Broadcast" /%}

## Troubleshooting

If you believe the sync or broadcasts are not as quickly as you would like them to be, you can change the schedule in the server settings.

{% figure src="/images/plugins/connectors/schedule.png" alt="Schedule" /%}




