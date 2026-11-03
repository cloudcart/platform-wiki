---
type: feature
nav_path: "Payment Providers → Stripe → Refunds, sync & capture"
route_name: apps.stripe.settings
route_path: /admin/payment-providers/stripe
aliases: ["Stripe refund", "Stripe refunds", "Stripe sync", "Stripe status verification", "Stripe webhook", "Stripe capture", "Stripe auto-capture", "Stripe Connect", "Stripe subscriptions", "Stripe self-deactivation", "Stripe reconciliation"]
tags: [paymentproviders, payment-providers, stripe, refunds, sync, capture, reconciliation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-stripe]]. See the hub for related aspects (settings, checkout flow, save card).

# Stripe — Refunds, sync & capture

## Purpose

This aspect documents the back-end lifecycle of a Stripe payment after it is initiated: how the payment status reaches the store (**webhook, the shopper's return, a background check**), how **refunds** work, the **auto-capture-only** behaviour, the absence of Stripe Subscriptions and Stripe Connect, and the **self-deactivation** safeguard when credentials go bad at runtime.

## Where to find it

This aspect is mostly runtime / back-end. The one merchant-facing action is the **Refund** button on an order's payment record — see [[orders-payment-refund]]. Status reconciliation, capture mode, Connect and self-deactivation are invisible to the merchant; the results surface on [[orders-details]].

## What the merchant can do here

- **Issue a refund** from the order's payment record (full), or a partial one through an order return — see [[orders-payment-refund]] and [[orders-payment-refund-partial-refunds]].
- **Manage the webhook** on the settings page — see [[stripe-webhook]].
- **Observe self-deactivation** — if a live key goes bad, the provider flips itself off and the admin is notified; the merchant fixes the key on [[stripe-settings-fields]] and re-enables.
- There is **no** manual capture action for Stripe (auto-capture only) — the [[orders-payment-capture]] button does not apply.

## Settings & fields

This aspect does not expose its own fields. Refunds and capture are runtime behaviours; credentials and mode are configured on [[stripe-settings-fields]].

## Business rules

### Three ways the status arrives

- **Webhook.** Stripe sends Checkout Session events to the store's endpoint, registered on the merchant's Stripe account when the settings are saved. Each event's session is read back from Stripe with the store's own key. See [[stripe-webhook]].
- **The shopper's return.** Coming back from Stripe Checkout reads the outcome.
- **A background check.** It starts 10 minutes after the redirect and repeats every 5 minutes. At 3 hours it closes the session at Stripe and marks a payment still open as timed out, so the order does not stay "requested". A session paid in the meantime is settled instead.

What the session or payment reports decides the payment status: paid → `completed`, expired → `timeouted`, still open → `pending`, otherwise `cancelled`. The order then follows [[order-status-auto-transitions]].

### Refunds

Supported. The merchant clicks Refund on the order's payment record (see [[orders-payment-refund]]), which refunds the **full** captured amount; on success the payment status flips to `refunded`. A **partial** refund runs through an order return's refund-to-card action and leaves the payment `completed` — see [[orders-payment-refund-partial-refunds]].

### Capture mode — auto-capture only

The integration always uses Stripe's default capture flow (Stripe charges and captures simultaneously on payment success). There is **no** manual-authorize / capture-later mode for Stripe in the current configuration — the [[orders-payment-capture]] action does not apply. The source code has commented-out scaffolding for `capture_method: manual`, but it is disabled.

### Recurring / subscriptions

The integration uses Stripe Checkout in `mode: payment` (one-off) — not `mode: subscription` (see [[stripe-checkout-flow]]). The Save-Card flow enables one-click repeat purchases via off-session charges (see [[stripe-save-card]]), but there is **no** scheduled-billing / Stripe Subscriptions integration at this layer.

### Stripe Connect — not supported

CloudCart's Stripe integration is **single-account-per-store** — each store wires up its own publishable/secret key pair. There is no marketplace / Connect / managed-account flow at the CloudCart level. With [[payment-providers-cloudcart-pay|CloudCart Pay]] the store's payment account is created through CloudCart's own onboarding instead of the merchant's keys ([[cloudcart-pay-account-model]]).

### Self-deactivation on invalid credentials

If Stripe throws an exception when initializing the Stripe client at runtime (typically an invalid API key), CloudCart catches it, sends an admin notification ("Stripe error: ... Stripe is deactivated"), and **flips the provider's Active flag to OFF automatically**. The merchant must fix the keys on [[stripe-settings-fields]] and re-enable. (This is the runtime counterpart to the save-time live key ping documented on [[stripe-settings-fields]], which prevents a broken key from being saved in the first place.)

## How it works (verified against backend)

- A customer who closed the browser mid-redirect still gets a resolved status from the webhook or the background check.
- A full refund that Stripe reports as succeeded moves the payment to `refunded`.

## Related

- [[payment-providers-stripe]] — hub.
- [[stripe-checkout-flow]] — the session whose outcome is read here.
- [[stripe-webhook]] — the webhook card.
- [[stripe-save-card]] — the off-session charge.
- [[stripe-settings-fields]] — credentials + the save-time key ping that complements runtime self-deactivation.
- [[orders-payment-refund]] — the merchant-facing Refund action.
- [[orders-payment-capture]] — manual capture flow (not used by Stripe).
- [[payment-providers-cloudcart-pay]] — the connected-account alternative for marketplace models.
- [[payment-status]] — completed / cancelled / refunded values.
- [[orders-details]] — where reconciled status surfaces.

## Open questions

(none)
