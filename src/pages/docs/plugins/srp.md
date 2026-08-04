---
title: Ship Replacement Program
description: An optional plugin that lets members submit their loss mails and lets SRP officers review, price and pay them out.
---

The Ship Replacement Program plugin lets members submit a loss mail for reimbursement, and lets SRP
officers price the loss, accept or reject it, and record the payout. It is a separate package, not part
of a default installation.

{% .lead %}

The plugin is developed at [seatplus/srp](https://github.com/seatplus/srp), where you will also find
its release notes and issue tracker.

---

## Installation

Install it inside the php container of your running instance. `composer require` adds the package to
your `src/composer.json`; `composer install` would not.

```shell
docker-compose exec php composer require seatplus/srp
```

Then run the migrations it ships:

```shell
docker-compose exec php php artisan migrate
```

Because the plugin adds new screens, restart the node container so its frontend assets are built:

```shell
docker-compose restart node
```

{% callout type="note" title="General package installation" %}
[Administration tasks](/docs/admin#add-a-package) covers adding packages in more detail, including
publishing assets and what to do when a package's UI does not appear.
{% /callout %}

Finally, grant the permissions. The plugin adds its own, including `can submit srp requests` for
members. Assign them through a control group as you would any other permission — see
[Permissions and control groups](/docs/concepts/permissions).

---

## Submitting a loss

Members need the `can submit srp requests` permission. Without it the submission form is unavailable
and an administrator has to grant it.

{% figure src="/images/plugins/srp/srp-overview.png" alt="The SRP overview page listing a member's submitted requests and their statuses" caption="The member's SRP overview. Submitted requests and their current status are listed here." /%}

To submit a loss you need its **external URL**, which EVE generates for you: in the client, go to
**Character Sheet → Interactions → Combat Log → Losses** and copy the external URL for the loss. Paste
it into the form, and add any context your SRP officers expect — doctrine, fleet, fitting notes.

{% figure src="/images/plugins/srp/submitted-killmail.png" alt="A submitted killmail showing the itemised loss with per-module prices" caption="The itemised loss. Review the module prices before submitting — they come from ESI market data and will not match your expectations exactly." /%}

{% callout type="note" title="Prices are ESI market prices, not your replacement value" %}
The plugin values modules from in-game market data, so the total is an estimate rather than a policy
figure. Officers can adjust both individual item prices and the total during review, which is where
your alliance's actual SRP policy gets applied.
{% /callout %}

Once submitted, track the status on the overview page.

---

## For SRP officers

Officers get a queue of submitted requests.

{% figure src="/images/plugins/srp/srp-admin-overview.png" alt="The SRP officer overview listing all submitted requests awaiting review" caption="The officer view: every submitted request across the instance." /%}

### Reviewing a request

Opening a request lets you:

- adjust individual item prices, which updates the total;
- override the total ISK amount outright;
- write a note, either to the submitter or for other reviewers;
- accept or reject the request.

{% figure src="/images/plugins/srp/review-killmail.png" alt="The review screen for a killmail with editable item prices and accept and reject actions" caption="Reviewing a loss. Both per-item prices and the total are editable, so alliance policy can override market value." /%}

### Payouts

Accepted requests are grouped **by user**, so you pay a person once rather than paying each loss
separately.

{% figure src="/images/plugins/srp/srp-payout.png" alt="The payout overview grouping accepted requests by user" caption="Payouts, grouped per user. Processing them together is what makes the receipt useful." /%}

When you process a user's open payouts you can copy a **receipt** to the clipboard and send it to them
in game, so they can see exactly what was reimbursed and for which losses.

{% figure src="/images/plugins/srp/receipt.png" alt="A payout receipt as the receiving member sees it" caption="The receipt the member receives, itemising what was paid and for what." /%}

### History

Every payout that has been made is listed, so past decisions and amounts stay auditable.

{% figure src="/images/plugins/srp/list-of-receipts.png" alt="The history list of all payouts made" caption="Payout history. Useful both for auditing and for answering “was I ever paid for this”." /%}
