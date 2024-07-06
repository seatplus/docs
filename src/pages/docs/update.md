---
title: Update
description: Update your app to the latest version
---

Whenever a new release of the underlying core packages is available, you may want to update your app to the latest version. This guide will help you to do so.

You may want to follow the [GitHub channel](https://discord.com/channels/569434366548115456/1092142035349295144) in Discord to get notified about new releases. Alternatively, you can watch the repositories on GitHub to get notified about new releases.

## Update (simple)

Here is a one to two liner to update your app to the latest version:

{% callout type="warning" title="Migration" %}
This command will update your app to the latest version. It will also run the migrations and restart the node and cron services.
If you have any custom changes in your app or you want to run the migrations manually, you should follow the detailed guide below.
{% /callout %}

On your host:
```shell
docker-compose exec php composer update --no-dev && \
docker-compose exec php php artisan migrate --force && \
docker-compose restart node && \
docker-compose restart worker
```

## Update (detailed)

Use this guide if you want to update your app to a specific version or if you have custom changes in your app.

### update the app using docker
```shell
docker-compose exec php composer update --no-dev
```

### run the migrations
```shell
docker-compose exec php php artisan migrate --force
```

### restart your node to build new web assets:
```shell
docker-compose restart node
```
### restart your worker service:
This is necessary to apply changes to the worker service. And new code changes to the worker service will not be applied until the worker service is restarted.
```shell
docker-compose restart worker
```

now seatplus should be up and running again.
### (optionally) Enter Shell for package installation:
```shell
docker-compose exec bash
```

---