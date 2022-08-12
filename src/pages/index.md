---
title: Getting started
pageTitle: Seatplus - SeAT with a little plus.
description: Flexible EVE Online API with the intent of corporation management and recruitment.
---

Learn how to set up Seatplus in under thirty minutes.  {% .lead %}

{% quick-links %}

{% quick-link title="Installation" icon="installation" href="/docs/installation" description="Step-by-step guides to setting up your system and installing Seatplus." /%}

{% quick-link title="Features" icon="presets" href="/docs/ssoScopes" description="Learn what Seatplus offers to you and how it works." /%}

{% quick-link title="Plugins" icon="plugins" href="/docs/plugins/srp" description="Extend the application with third-party plugins or write your own." /%}

{% quick-link title="Contribution" icon="theming" href="/docs/how-to-contribute" description="Learn to easily customize and modify your app's visual design to fit your brand." /%}

{% /quick-links %}

Possimus saepe veritatis sint nobis et quam eos. Architecto consequatur odit perferendis fuga eveniet possimus rerum cumque. Ea deleniti voluptatum deserunt voluptatibus ut non iste.

---

## Introduction

Inspired by [SeAT](https://github.com/eveseat/seat), seatplus is a complete rewrite based on the most frequent user- and 
feature request. As such the complete role and affiliation concept has been designed from the drawing board aiming to support recruiters in their daily work for their corporation. 
No more SDE Issues, seat-plus does not have any dependency of SDE. 
Have Friends on your instance, only request esi-scopes when necessary. 
Have an overview of members compliance if scopes or refresh_tokens has been changed. 
No delays between role assignment and users capabilities. 
Allow recruiters to only review recruits without access to in-corp characters. 
Automatically assign roles to users based upon their corporation or alliance.

Currently, seat-plus is under development and required your feedback.
What do you like? What feature would you like to see? Any feedback is of
value.

| Channel                                        | Purpose                       |
|:-----------------------------------------------|:------------------------------|
| [GitHub](https://github.com/seatplus/seatplus) | Bug-Reports, Feature Requests |
| [Discord](https://discord.gg/3UR5uDDMjK)       | Social, Support               |

## Modern Design

Seatplus is designed mobile first. Whenever or wherever you access seat-plus you will have a great user experience.

## Robust Architecture

Seatplus is currently under development and used within [Amok.](https://zkillboard.com/corporation/1184675423/) alongside other tools for member life cycle management.
Functionalities of seatplus are tested in order to guarantee functionality. Auth Coverage aims for above  85% and eveapi coverage above 80%.
Noteable components are:
* [Seatplus/eveapi](https://github.com/seatplus/eveapi) - The main library for the application.
* [Seatplus/esi-client](https://github.com/seatplus/esi-client) - A standalone ESI (Eve Swagger Interface) Client Library using kevinrob/guzzle-cache-middleware.

{% callout type="note" title="One does not simply need the web interface" %}
If you wish to solely use the esi-client or the eveapi to interact with the ESI, you can do so. You mustn't use the web interface. 
You might even opt to write your own web interface. If you do so, you might want to have a look at [Seatplus/auth](https://github.com/seatplus/auth) to take advantage of the authentication features.
{% /callout %}