---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Saved card"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay save card", "CloudCart Pay saved card", "CloudCart Pay save customer card", "CloudCart Pay stored card", "CloudCart Pay tokenization"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, refunds + webhooks) and the four lifecycle tabs.

# CloudCart Pay — saved card

## Purpose

This page documents the *Save customer card* behaviour — what the single setting does, who it applies to, how the saved card is re-used on later orders, and the safety net that prevents "No such customer" errors after an account is disconnected and reconnected. It is the page to read for "can my customers save their card?" or "why was a saved card lost?" questions.

## Where to find it

The single *Save customer card* switch lives on the [[payment-providers-cloudcart-pay-settings|Settings tab]] at Sidebar → **Payment Providers** → **CloudCart Pay** → **Settings**. The behaviour it controls happens on the storefront checkout (see [[cloudcart-pay-checkout-flow]]).

## What the merchant can do here

- **Turn saved cards ON or OFF** with one switch (no separate test / live toggles).
- **Let signed-in customers re-use a stored card** on later orders without re-entering details.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Save customer card** | When ON, signed-in customers can save their card during checkout and re-use it on future orders. | OFF | Single mode-agnostic switch on the Settings tab. Has no effect for guest (not-signed-in) checkouts. |

## Business rules

### Save card flow — single mode-agnostic setting

The historical UI had two separate "save card" toggles (one for test mode, one for live mode). The May 2026 refactor consolidated these into one switch on the [[payment-providers-cloudcart-pay-settings|Settings]] tab.

When enabled **and** the customer is signed in (not a guest), the checkout session is created with:

- `saved_payment_method_options.payment_method_save=enabled`
- `setup_future_usage` — `on_session` in **embedded** checkout (the default modern flow), `off_session` in **hosted** checkout. See [[cloudcart-pay-checkout-flow]] for the two checkout modes.

On a successful payment, the provider customer ID and payment-method ID are stored against the CloudCart [[customer]]; on subsequent orders the saved card can be selected without re-entering the details.

### Signed-in customers only

Saved cards require a signed-in customer. Guest checkouts never store a card even when the setting is ON — there is no customer record to attach the stored payment method to.

### Stale-customer safety net

If the stored provider customer ID is no longer valid for the current connected account (e.g., because an earlier connected account was disconnected and replaced — see [[cloudcart-pay-activation-gate]] for the disconnect cascade and [[cloudcart-pay-account-model]] for account scoping), the stale reference is dropped and a fresh provider customer is created on the next checkout. The customer experience continues without a "No such customer" error from the provider — the only visible effect is that the previously-saved card is no longer offered and must be entered again.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — the Settings tab that hosts the *Save customer card* switch.
- [[cloudcart-pay-checkout-flow]] — how the setting changes the checkout session (embedded vs hosted).
- [[cloudcart-pay-account-model]] — connected-account scoping that the stored customer ID is bound to.
- [[cloudcart-pay-activation-gate]] — disconnect cascade that can invalidate a stored customer ID.
- [[customer]] — the customer record the saved card is attached to.

## Open questions

(none)
