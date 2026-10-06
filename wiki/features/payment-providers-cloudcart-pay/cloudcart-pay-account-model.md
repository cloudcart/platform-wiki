---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Account model"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay account model", "CloudCart Pay connected account", "CloudCart Pay sub-account", "Why CloudCart Pay", "CloudCart Pay vs third-party", "CloudCart Connect account", "Свързан акаунт CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (activation gate, checkout flow, express checkout, Apple Pay domain, refunds, saved card) and the six tabs.

# CloudCart Pay — account model

## Purpose

How a store is tied to CloudCart Pay: each merchant has a **connected account**, the store holds only a link to it, and there are no API keys for the merchant to manage. This page also covers sharing one account between stores, the test and live environments, the storefront label, and why CloudCart Pay is the recommended choice over third-party gateways.

## Where to find it

Settings → Payment methods → **CloudCart Pay**. The connected account's ID is shown on the [[payment-providers-cloudcart-pay-settings|Settings tab]] (**Connected Account** / **Свързан акаунт**) and in step 1 of the [[payment-providers-cloudcart-pay-onboarding|Onboarding tab]] (**Connected Account ID** / **ID на свързания акаунт**, with **Copy** and **Disconnect**). There is no separate screen for the account model.

## What the merchant can do here

- **Read the connected account ID** and copy it.
- **Link this store to an account created from another store** with **Connect Existing Account**.
- **Disconnect** the store from its account without deleting the account.
- **Rename the method at checkout** with the standard logo, title and description fields.

## Settings & fields

| Field | What it does | Default | Notes |
|---|---|---|---|
| **Connected Account** | Read-only ID of the merchant's account on CloudCart Pay. | Empty until onboarding | Shown on the Settings tab with **Manage Onboarding**, or **No connected account yet.** with **Start Onboarding**. |
| **Logo / Title / Description** | The method's label at checkout. | Provider defaults | Fully customisable: "CloudCart Pay" can be renamed, e.g. to "Pay by card". |

There are **no API-key fields** and no test/live switch for the merchant.

## Business rules

### One connected account per merchant

Onboarding creates a **connected account** for the business (the screen calls it a "CloudCart Connect account"). The store keeps only the link to that account and the onboarding progress; the business details, people, documents and bank accounts live on the account and are read live every time a tab opens. Editing them from another store that shares the account shows up here on the next load.

### No keys, one environment for the whole platform

CloudCart holds the credentials; every request is made on behalf of the merchant's connected account. Whether the store charges in the **test** or the **live** environment is set by CloudCart for the whole platform and shown in the read-only badge in the page header. An account created in one environment cannot be used in the other: the Onboarding tab then shows *"This store is linked to a CloudCart Pay account, but its details could not be loaded."* with a **Disconnect** button (see [[ccpay-onboarding-connect-disconnect]]).

### One account, several stores

**Connect Existing Account** links a store to an account that was created from another CloudCart store, by pasting its ID. It is refused only when the current store already has an account: *"An account is already connected. Disconnect first."* Disconnecting clears this store's link; the account itself keeps existing.

### Storefront label is not locked

The logo, title and payment-method description on the Settings tab are the same fields every payment method has. Nothing in them is fixed by CloudCart Pay.

### Why CloudCart Pay over third-party providers

Compared with external gateways such as iCard, Borica Way4, myPOS, Stripe or Mokka:

- **No separate negotiation** — sign-up happens in the admin panel; the agreement is accepted with ticks in step 5 of the onboarding ([[cloudcart-pay-merchant-terms]]).
- **0% transaction fee until 31 December 2026** — see [[cloudcart-pay-pricing]].
- **No API keys to manage** — the merchant owns only the onboarding and the checkout settings.
- **Onboarding inside the admin panel** — business details, people, documents, agreements and bank account in one wizard ([[payment-providers-cloudcart-pay-onboarding]]).
- **Apple Pay and Google Pay** next to the card form — see [[cloudcart-pay-checkout-flow]].
- **Payouts to the merchant's own IBAN** — see [[payment-providers-cloudcart-pay-payouts]].
- **Refunds and statuses handled in CloudCart** — see [[cloudcart-pay-refunds-webhooks]].
- **Quick approval** — a new account is approved from a few hours to 2 business days after submission, longer for a complicated company structure (operator statement; see [[ccpay-onboarding-review-alerts]]).

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — where the connected account ID and the label fields are shown.
- [[payment-providers-cloudcart-pay-onboarding]] — create, connect or disconnect the account.
- [[ccpay-onboarding-connect-disconnect]] — Connect Existing Account and Disconnect in detail.
- [[payment-provider-mechanism]] — how payment methods work on the platform.
- [[payment-provider]] — entity definition.

## Open questions

- Whether the payment platform itself limits how many stores may share one connected account (CloudCart's own check only refuses a store that already has an account).
