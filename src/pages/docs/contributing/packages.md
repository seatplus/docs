---
title: Packages
description: Seatplus uses packages for core and for plugins. Learn how to set packages up in your development environment.
---

After you have installed the development environment this is how your folder structure should look like:

```shell
├── base-app
    ├── src         # Source files 
    ├── traefik     # Traefik docker compose files
    ├── packages    # Packages 
    ├── ...         
```

By default the `composer.json` located in the `/src` directory requires the core packages

* seatplus/eveapi
* seatplus/web
* seatplus/auth

from packagist.org.

```json
{
  "require": {
    "seatplus/eveapi": "^1.0",
    "seatplus/web": "^1.0",
    "seatplus/auth": "^1.0"
  }
}
```

In oder to use your local repository you will need to create the local repository and then alter the `composer.json` to simlink the local repository.
In this guide we will create a local repository for the web package.

## create local project in packages folder

Use git to clone the repository inside the packages folder

```shell
    git clone https://github.com/seatplus/web .
```

## update composer.json

Change the composer.json to use the local repository
    
```json
    {
      "repositories": [
        {
          "type": "path",
          "url": "../packages/web"
        }
      ],
      "require": {
        "seatplus/eveapi": "^1.0",
        "seatplus/web": "*",
        "seatplus/auth": "^1.0"
      }
    }
``` 
   
## (Optional) Update webpack.config.js for frontend development

If the package contains vue components you will need to update the webpack.config.js in the base-app folder.

add the following to the webpack.mix.js file:

```js
    mix.copyWatched(
        'vendor/seatplus/web/resources/js/**/*.{vue,js}',
        'resources/js',
        {base: 'vendor/seatplus/web/resources/js'}
    );
```

## Folder Structure

This is how the base-app folder structure should look like after adding a package

```shell
    .
    ├── ...
    ├── src                     # src folder
    │   ├── composer.json       
    │   └── webpack.mix.js      
    ├── packages                
    │   ├── web                 # The added package
    │   └── ...                
    └── ...
```

## Develop your own package

We offer a skeleton for your own package development:

[Package Skeleton](https://github.com/seatplus/package-skeleton/)