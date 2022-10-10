---
title: Administration
description: Learn how to administrate Seatplus.
---

In this section you will find some tips on how to administrate Seatplus.

## Live Container Logs

``` shell
docker-compose logs --tail 10 -f
```

## Add package

You can either directly alter the `/src/composer.json` file or you use the dependency manager insider the container:
```shell
docker-compose exec php composer require vendor/package
```

anyway most often you need to run migrations or publish assets afterwards so it might be worthwhile to directly enter
the container (see below). If a new UI will be introduced by the package don't forget to restart the node container
after the publishing of the package assets. 

```shell
docker-compose restart node
```

## Run migrations

```shell
docker-compose exec php php artisan migrate
```

## Enter the container

Whenever you are being asked or have the need to run an artisan command
you may enter the seatplus container with the following command

``` shell
docker-compose exec php bash
```

## Create superuser

Execute the following command followed by the characters name [inside the container](#enter-the-container)
``` shell
// replace the character_name including the curly brackets with your character name
php artisan s:a:s {character_name}
```

## Database Backups 
To create a backup run
``` shell
docker-compose exec mariadb sh -c 'exec mysqldump "$MARIADB_DATABASE" -u"$MARIADB_USER" -p"$MARIADB_PASSWORD"' | gzip > seatplus_backup.sql.gz
```

## Database Restore
```shell
zcat seatplus_backup.sql.gz | docker-compose exec -T mariadb sh -c 'exec mysql "$MARIADB_DATABASE" -u"$MARIADB_USER" -p"$MARIADB_PASSWORD"'
```