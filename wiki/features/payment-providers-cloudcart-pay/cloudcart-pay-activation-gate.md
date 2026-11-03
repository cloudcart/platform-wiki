---
type: feature
nav_path: "Settings → Payment methods → CloudCart Pay → Activation gate"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay activation gate", "CloudCart Pay cannot activate", "CloudCart Pay deactivated", "CloudCart Pay auto-deactivation", "CloudCart Pay disconnect cascade", "CloudCart Pay не се активира", "CloudCart Pay се изключи"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-06-10
updated: 2026-10-06
source_count: 2
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, checkout flow, express checkout, Apple Pay domain, refunds, saved card) and the six tabs.

# CloudCart Pay — activation gate

## Purpose

Every reason the CloudCart Pay method refuses to switch on, or switches itself off: the checks behind the **Active** switch, the exact messages the merchant sees, the automatic deactivation when the configuration breaks, and what **Disconnect** does to the method. It is the page for "I can't activate CloudCart Pay" and "CloudCart Pay turned itself off".

## Where to find it

The **Active** switch is in the header of Settings → Payment methods → **CloudCart Pay**. **Disconnect** is in step 1 of the [[payment-providers-cloudcart-pay-onboarding|Onboarding tab]]. Automatic-deactivation notices appear in the admin [[notifications]].

## What the merchant can do here

- **Switch the method on** — it succeeds only when every check below passes.
- **Read the message** that explains why it was refused.
- **See an admin notification** when the method was switched off automatically.
- **Onboard again or link an account**, then switch the method back on.

## Settings & fields

| Control | What it does | Default | Notes |
|---|---|---|---|
| **Active** switch (header) | Turns CloudCart Pay on or off at checkout. | Off | Checked by the server each time it is switched on, from the switch or from a settings save. A refusal shows one of the messages below. |

## Business rules

### What must be true before the method can be switched on

The switch is refused when any of these holds:

- the store has no connected account (onboarding not started, or the account was disconnected);
- CloudCart's own CloudCart Pay credentials are missing on the platform;
- the connected account cannot be read;
- card payments are not active on the connected account yet.

The messages, verbatim:

- "Connect a CloudCart Pay account before enabling this payment method."
- "CloudCart Pay system API key is not configured."
- "Could not verify the CloudCart Pay account status: <reason>"
- "Could not verify the CloudCart Pay account. Please try again later."
- "CloudCart Pay payments are not active on the connected account yet. Complete onboarding and wait for payments to be activated before enabling this payment method."

Card payments become active only after the account is approved. Approval takes from a few hours to 2 business days after submission, longer for a complicated company structure (operator statement). The current state is on the **Status** step of the onboarding as the **Payments** card (**Active** / **Pending** / **Inactive**) — see [[ccpay-onboarding-status-capabilities]]. When it changes, the store owner also gets an admin notification and an email — see [[ccpay-onboarding-review-alerts]].

### Automatic deactivation when the configuration breaks

Before a payment, a refund or a status check, the system checks its configuration. If something is missing it **switches the method off** and raises an admin notification:

- *"CloudCart Pay error: system API key is not configured. CloudCart Pay is deactivated."*
- *"CloudCart Pay error: no connected account — complete onboarding first. CloudCart Pay is deactivated."*
- *"CloudCart Pay error: <reason>. CloudCart Pay is deactivated."*

These notices go to the admin [[notifications]] only, not by email.

### Disconnect switches the method off

**Disconnect** on the Onboarding tab clears this store's link to the account and its onboarding progress. Because the method may not run without a connected account, it is **switched off at the same time**, and the header switch flips to off without a reload. The confirmation asks first: *"Disconnect this account? The account will still exist on CloudCart but this store will stop referencing it and the payment method will be turned off."*

The account itself is not deleted. The merchant can link it again (here or from another store) with **Connect Existing Account**, or start a new onboarding; the method then has to be switched on again. See [[ccpay-onboarding-connect-disconnect]].

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding and the Disconnect action.
- [[ccpay-onboarding-status-capabilities]] — the Payments and Payouts cards.
- [[ccpay-onboarding-review-alerts]] — approval time and account alerts.
- [[cloudcart-pay-account-model]] — the connected account the checks read.
- [[settings-payment-providers]] — activation of payment methods in general.
- [[notifications]] — where deactivation notices appear.

## Open questions

(none)
