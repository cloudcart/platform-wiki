---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Activation gate"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay activation gate", "CloudCart Pay cannot activate", "CloudCart Pay deactivated", "CloudCart Pay auto-deactivation", "CloudCart Pay disconnect cascade"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, checkout flow, refunds + webhooks, saved card) and the four lifecycle tabs.

# CloudCart Pay — activation gate

## Purpose

This page documents every reason CloudCart Pay refuses to turn on at checkout — the server-side activation prerequisites, the verbatim error messages the merchant sees, the automatic deactivation that fires when the configuration breaks, and the Disconnect cascade. It is the page to read for any "I can't activate CloudCart Pay" or "CloudCart Pay turned itself off" support ticket.

## Where to find it

The **Active** switch sits in the header of the CloudCart Pay overview at Sidebar → **Payment Providers** → **CloudCart Pay**. Disconnect lives on the [[payment-providers-cloudcart-pay-onboarding|Onboarding tab]]. Auto-deactivation notices surface in the admin notification panel (see [[notification-delivery]]).

## What the merchant can do here

- **Try to activate** the payment method — succeeds only when all prerequisites are met.
- **Read the validation error** explaining exactly why activation was refused.
- **See an admin notification** when the system forcibly deactivates the method.
- **Re-onboard or re-link** an account after a disconnect, then re-activate.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Active** switch (header) | Turns CloudCart Pay ON / OFF at checkout. | OFF | Server-checked; returns HTTP 422 with a validation error on the `active` field when any prerequisite below fails. |

## Business rules

### Activation gate — payments must be active on the connected account

The activation switch is checked server-side. It refuses activation (HTTP 422, validation error on the `active` field) when ANY of these is true:

- No `connected_account_id` is stored in the provider configuration (i.e., onboarding has not been started).
- The platform-wide CloudCart Pay system API key is not configured at the host level.
- The connected account cannot be loaded from the provider API.
- The connected account's `payments_enabled` flag is not `true` AND `capabilities.card_payments` is not `active`.

The validation error messages the merchant sees verbatim:

- "Connect a CloudCart Pay account before enabling this payment method."
- "CloudCart Pay system API key is not configured."
- "Could not verify the CloudCart Pay account status: <provider message>"
- "Could not verify the CloudCart Pay account. Please try again later."
- "CloudCart Pay payments are not active on the connected account yet. Complete onboarding and wait for payments to be activated before enabling this payment method."

The `card_payments` capability becomes `active` only after KYB approval on the platform side — see [[payment-providers-cloudcart-pay-onboarding]] for the onboarding wizard and [[payment-providers-cloudcart-pay-payouts]] for the related capability surfaces.

### Auto-deactivation on configuration errors

A configuration check runs before every payment / refund / sync call. It will **forcibly deactivate the payment method** (set the provider row to `active=no`) and raise an admin notification if any of these is detected at request time:

- The platform system API key is missing → notice: *"CloudCart Pay error: system API key is not configured. CloudCart Pay is deactivated."*
- No connected account is on file → notice: *"CloudCart Pay error: no connected account — complete onboarding first. CloudCart Pay is deactivated."*
- The provider client cannot be constructed → notice: *"CloudCart Pay error: <message>. CloudCart Pay is deactivated."*

Each notice is sent through the payment-provider notification manager (the same surface other payment-provider errors use, on the `cloudcart_pay_error` channel) and surfaces in the admin notification panel — see [[notification-delivery]].

### Disconnect auto-deactivates the method too

Clicking **Disconnect** on the Onboarding tab (see [[payment-providers-cloudcart-pay-onboarding]]) clears `connected_account_id` and the onboarding progress counter, then — because the activation prerequisite is now gone — it also flips the payment-provider `active` flag to `no`. The full disconnect cascade:

1. Strips obsolete legacy config keys (`tax_id`, `bank_iban`, `doc_identity`, etc.).
2. Sets `connected_account_id=null` and `onboarding_completed_steps=[]`.
3. **Forcibly deactivates the payment method** (provider row `active=no`).
4. Returns `{disconnected: true}` so the admin layer can push `active=no` into cached app settings immediately.

The connected account itself still exists on the payment platform — only the local link is cleared. The same account can be re-linked from another store via *Connect Existing Account* (see [[cloudcart-pay-account-model]]). The merchant must re-onboard (or link an existing account) and re-activate before the storefront sees CloudCart Pay again.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-onboarding]] — onboarding wizard + the Disconnect action that triggers the cascade.
- [[payment-providers-cloudcart-pay-payouts]] — capability status surfaces.
- [[cloudcart-pay-account-model]] — the connected-account scoping the gate checks against.
- [[notification-delivery]] — admin notification panel where deactivation notices appear.
- [[payment-provider]] — entity definition.

## Open questions

(none)
