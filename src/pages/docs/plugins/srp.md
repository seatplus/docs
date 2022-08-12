---
title: Ship Replacement Program
description: A plugin that offers the ability for users to submit their loss mail.
---

This plugin offers the ability for users to submit their loss mail and SRP Officers to handle payouts if loss is accepted.

[![Latest Version on Packagist](https://img.shields.io/packagist/v/seatplus/srp.svg?style=flat-square)](https://packagist.org/packages/seatplus/srp)
[![GitHub Tests Action Status](https://img.shields.io/github/workflow/status/seatplus/srp/Laravel?label=Tests)](https://github.com/seatplus/srp/actions?query=workflow%3Alaravel+branch%3Adev)
[![GitHub Code Style Action Status](https://img.shields.io/github/workflow/status/seatplus/srp/Check%20&%20fix%20styling?label=code%20style)](https://github.com/seatplus/srp/actions?query=workflow%3A"Check+%26+fix+styling"+branch%3Adev)
[![Total Downloads](https://img.shields.io/packagist/dt/seatplus/srp.svg?style=flat-square)](https://packagist.org/packages/seatplus/srp)

For more information on the plugin please visit the [Github - seatplus/srp](https://github.com/seatplus/srp).

## Installation


{% callout type="note" title="How to install the package" %}
Please review the {% link href="admin#add-package" %}admin guide{% /link %} for information on how to add a package to seatplus
{% /callout %}

1) Install the package
    ```bash
    composer install seatplus/srp
    ```

2) Run migrations
    ```bash
    php artisan migrate
    ```

## Usage

As a user with the necessary permission you can submit your loss mail. If you are not able to so please ask an administrator to assign you the `can submit srp requests` permission.

{% figure src="/images/plugins/srp/srp-overview.png" alt="SRP Overview" /%}

You must paste the external URL (Character Sheet -> Interactions -> Combat Log -> Losses -> External URL) into the box. You may also add some additional information to the loss that may required by the SRP Officers.

{% figure src="/images/plugins/srp/submitted-killmail.png" alt="Killmail" /%}

Please review the prices for the modules. Seatplus is using prices from ingame/ESI so the prices may be slightly different. 
Whenever you are ready submit your request. 
You will see the status of your request in the table on the overview page.

## SRP Officers

As a SRP Officer you can handle the payouts for the SRP requests.

{% figure src="/images/plugins/srp/srp-admin-overview.png" alt="SRP Admin Overview" /%}

### Review
As SRP officer you may:
* modify item prices (this will update the total)
* modify the total ISK amount.
* write a note to the user who submitted the request or for reviewers.
* accept or reject the SRP requests.

{% figure src="/images/plugins/srp/review-killmail.png" alt="Review Killmail" /%}

### Payouts

Processed and accepted srp requests are collected by user. 
{% figure src="/images/plugins/srp/srp-payout.png" alt="Payout overview" /%}

if you opt to process all open payouts you will have the option to copy a receipt to the clipboard. Which you then can send to the user.
The receiver will see the following:
{% figure src="/images/plugins/srp/receipt.png" alt="Payout receipt" /%}

### History
There is also a list with the all the payouts made.
{% figure src="/images/plugins/srp/list-of-receipts.png" alt="List of receipts" /%}

