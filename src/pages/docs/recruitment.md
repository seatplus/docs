---
title: Recruitment
description: How to use the recruitment feature.
---

## Configuration

To be able to view the recruitment page you need the following permission: `recruitment.view`. 
If you plan to use the recruitment feature you need to configure it. 

{% figure src="/images/createEnlistment.png" alt="Create Enlistment" /%}

First select the corporation for which you want to create an enlistment. Secondly, you can choose between the following types of enlistments:

| Type      | Description                                                                                                                                                                                        |
|:----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Character | Only the applying characters must supply requested esi scopes. This might be useful if you are using seatplus as alliance tool where the same user may be part of various corporations             |
| User      | Every character belonging to the user must supply the requested scopes. This might be useful for corporations enforcing full compliance to their members                                           |

lastly you can enter the names of your review process steps. These steps will be enforced for recruits and will be displayed in the recruitment table.

### Practical Example:
Amok. does have multiple steps to review an application. Firstly a front door review is done. After this the recruit can be accepted and in a later step a senior HR officer can review the application in a backdoor application prior to resolving the application.

## Usage for users
Potential recruits can find an overview of all open enlistments in the home tab. This is the very first page that is displayed when you login.

{% callout type="note" title="User wide SSO Scopes" %}
If you plan to enforce user wise SSO Scopes, advice your recruits to first apply to a job posting.
{% /callout %}

{% figure src="/images/enlistment.png" alt="Enlistments view" /%}

As soon as a recruit applies to a job posting, the recruit is automatically enlisted and must fulfill the required scopes (see {% link href="ssoScopes" %}SSO Scopes{% /link %}).

## Usage for recruiters

Recruiters can find an overview of all pending applications in their current status at the corporation recruitment page.
{% figure src="/images/corporateRecruitment.png" alt="Corporation Recruitment view" /%}

Seatplus supports the concept of junior and senior HR officers. F.e. junior HR officers can review pending applications only, while senior HR officers can also review closed applications.

{% figure src="/images/reviewRecruit.png" alt="Review Recruits" /%}

As recruiter, you can opt to write notes in a log, select a category to review such as assets, contacts, contracts, wallets, skills, etc. 
Furthermore, you can impersonate the user if the enlistment is of the user type. 
Lastly a recruiter can dispatch an update job for characters to update their assets, contacts, contracts, wallets, skills, etc.