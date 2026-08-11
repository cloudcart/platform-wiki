---
type: feature
nav_path: "Orders → Order details → Payment → Capture / Cancel → Provider matrix"
route_name: admin.orders.payment.capture
route_path: /admin/orders/action/payment/capture-authorization/:payment_id
aliases: ["Capture provider matrix", "Authorized-state gateways", "Two-phase gateways", "Borica WAY4 authorize", "DSK authorize", "Stripe manual capture commented out"]
tags: [orders, payment, capture, authorization, providers, gateway]
plan_gates: ["authorize_payment"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-payment-capture]]. See the hub for the other aspects (buttons & visibility, amount-exceeds rule, side effects, automatic triggers, API access).

# Payment capture — provider matrix

## Purpose

Only a verified subset of card gateways ever produces a CloudCart payment in **Authorized** state. This page is the definitive list of which providers can show the Capture / Cancel buttons and which never can — so a support agent can tell a merchant "your gateway doesn't do two-phase" without guessing.

## Where to find it

The matrix governs whether the Capture / Cancel buttons can appear at all on [[orders-details]]. Two-phase mode is configured per gateway on [[settings-payment-providers]] and gated by the `authorize_payment` plan feature (see [[orders-payment-capture-api-access]]).

## What the merchant can do here

The merchant cannot change which providers support two-phase — capability is set internally by each gateway integration. The merchant's only lever is choosing / configuring a supporting gateway with authorize mode enabled at setup time.

## Settings & fields

### Gateways that DO produce Authorized state (verified set)

These are the only card gateways that create CloudCart payments in **Authorized** state, so this is the complete list of providers where the Capture / Cancel buttons can appear:

- **Borica WAY4** — Bulgarian merchant cards via Borica's WAY4 platform.
- **DSK Bank** — DSK card processor.
- **Btepos** — Borica's POS-issued e-commerce flow.
- **Raiffeisen** — RBI card processor.
- **Monri** — Croatian / regional card processor.
- **Revolut Business** — when Revolut returns `authorised` state.

### Gateways that NEVER produce Authorized state

**Stripe, PayPal, CloudCart Pay, Mollie, Mokka, Klear, Iute** go straight from Pending to Completed — they never reach Authorized, so the Capture / Cancel buttons never appear. For these providers the Refund flow ([[orders-payment-refund]]) is the only post-charge reversal available.

A notable detail: **Stripe's `capture_method = manual` flag exists in the code but is commented out**, so two-phase Stripe is NOT available in CloudCart today `(verify)`. A merchant expecting Stripe pre-auth will not get it on the current platform.

## Business rules

### Two-phase is gateway-driven, not platform-driven

Whether a payment goes through two-phase depends on:

- The gateway integration's configuration (e.g. a card processor's authorize-then-capture mode).
- The merchant's choice at gateway setup time — some merchants opt into pre-auth for fraud protection, others use immediate capture.

The platform doesn't unilaterally decide — the gateway returns the payment in **Authorized** state only if it is configured for two-phase. Without that, the order skips straight to a charged / Completed payment and there is nothing to capture or cancel.

### Capability check is the second of three gates

Provider support is gate #2 of the three Capture-visibility gates (status Authorized → provider supports capture → `allow_capture_authorization === true`). Even on a supporting provider, the button still hides if the per-payment property says no — see [[orders-payment-capture-buttons]].

### Loyalty-split providers

**Btepos and BoricaWay4** can split a purchase into a loyalty / points portion plus a cash portion, which makes their capture / cancel a two-call sequence. That mechanic is documented on [[orders-payment-capture-side-effects]].

## Related

- [[orders-payment-capture]] — hub.
- [[orders-payment-capture-buttons]] — the three visibility gates (provider support is gate #2).
- [[orders-payment-capture-side-effects]] — Btepos / BoricaWay4 loyalty split-call detail.
- [[settings-payment-providers]] — where two-phase mode is configured per gateway.
- [[orders-payment-refund]] — the only reversal for providers that never reach Authorized.
- [[orders-details]] — where the buttons render (or not).

## Open questions

- Confirm Stripe two-phase remains disabled (the `capture_method = manual` flag is commented out) `(verify)`.
