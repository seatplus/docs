---
title: Upgrade
description: Upgrade your app to the latest version
---

Whenever a major release in the underlying core packages is required. You must update your `/src` folder.
This is a rare occasion but could happen f.e. if the underlying framework (laravel) has a major update.

{% callout type="note" title="Backup" %}
In this guide we assume Docker installs only. These are the only one supported anyway.
Usually the `/src` folder contains not much of value, except for the installed packages and logs. Volumnes, Databases etc are always mounted and save from loss except if the volumne of your host ist damaged.
After the upgrade you must install your packages again.
{% /callout %}

## Update to v4.x

This is a major update. The underlying seatplus/web package has been updated to v4.0.0.

(untested yet)

On your host:

### navigate to the /src directory:
```shell
cd /src
```

### edit composer.json to require the latest version of seatplus/web:
```shell
"require": {
    "seatplus/web": "^4.0",
    ...
```

### navigate back to the root directory:
```shell
cd ..
```

### update the app using docker
```shell
docker-compose exec composer update --no-dev
```

### restart your node to build new web assets:
```shell
docker-compose restart node
```

now seatplus should be up and running again.

### (optionally) Enter Shell for package installation:
```shell
docker-compose exec bash
```

---

## Update to v3.x

(untested yet)

On your host:

### take your app down:
```shell
docker-compose down
```

### backup your `/src` folder:
```shell
mv /src /backup_src
```

### download the latest core package:
```shell
docker-compose run --rm php composer create-project seatplus/core . --prefer-dist --no-dev --no-ansi
```

### change file ownership:
change the user:group to whatever you have used originally.
```shell
chown -R 1000:1000 src
```

### Start the app again:
```shell
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Migrate:
```shell
docker-compose exec php php artisan migrate
```

### (optionally) Enter Shell for package installation:
```shell
docker-compose exec bash
```
