---
type: feature
nav_path: "Settings → Payment methods → Stripe → Webhook"
route_name: apps.stripe.settings
route_path: /admin/payment-providers/stripe
aliases: ["Stripe webhook", "Stripe webhook card", "Stripe webhook not registered", "Stripe webhook disabled", "Stripe payment not confirmed", "Stripe No access", "Уебхук Stripe", "Stripe не потвърждава плащането"]
tags: [paymentproviders, payment-providers, stripe, webhook, sync]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 1
---

> Part of [[payment-providers-stripe]]. See the hub for related aspects (settings, checkout flow, save card, refunds).

# Stripe — Webhook

## Purpose

The **Webhook** card on the Stripe settings page shows whether Stripe tells the store about a payment the moment it completes. With the webhook active, a payment is confirmed straight away, even if the shopper never returns to the store. Without it, the payment is confirmed when the shopper returns, or by a background check up to 10 minutes later. This page covers the card, its badges and messages, and how the status of a Stripe payment reaches the order.

## Where to find it

Settings → **Payment methods** → **Stripe** → the **Webhook** card at the top of the settings page. Address: `/admin/payment-providers/stripe`.

## What the merchant can do here

- **Read the webhook's status** for the environment the store is in.
- **Register** the webhook, **re-register** it, or **activate** it after a deactivation.
- **Deactivate** it.

## Settings & fields

| Element | What it shows or does |
|---|---|
| **Webhook endpoint** | The address Stripe sends events to. Read-only. |
| Badge | The status, see the table below. |
| **Register webhook** / **Re-register** / **Activate** | One button, named by the state. Shown when the webhook is not healthy or was deactivated. |
| **Deactivate** | Shown while the webhook is registered and enabled. Asks for confirmation. |

| Badge | Message on the card |
|---|---|
| **Active** | *"Stripe notifies your store the moment a payment completes."* |
| **Not registered** | *"Without the webhook, a payment is confirmed when the customer returns to the store, or up to 10 minutes later if they do not."* |
| **Disabled** | *"Stripe has disabled this webhook, usually after repeated failed deliveries. Re-register to enable it again."* |
| **Incomplete** | *"The webhook is missing some events. Re-register to subscribe to all of them."* |
| **Deactivated** | *"The webhook is deactivated. Payments are confirmed when the customer returns to the store, or up to 10 minutes later if they do not."* |
| **No access** | *"This restricted key cannot manage webhooks. Give it write access to Webhook Endpoints in your Stripe Dashboard, or use a secret key, then register the webhook."* |

Before any secret key is saved the card reads *"Save your secret key first, then register the webhook."*

## Business rules

### Registered on save

Saving the Stripe settings registers the endpoint on the merchant's Stripe account for the selected mode, or reuses and repairs the one already there. A key that may not manage webhooks does not stop the save: the settings are stored and the card shows **No access**. A webhook the merchant deactivated stays deactivated on later saves.

### Events

The webhook subscribes to four Checkout Session events: `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `checkout.session.expired`. Each event only names a session; the store then reads that session from Stripe with its own key to learn the outcome.

### Shared between stores on one Stripe account

Every store connected to the same Stripe account uses one webhook. **Deactivate** therefore disables the endpoint rather than deleting it, and its confirmation says so: *"Payments will be confirmed only when the customer returns to the store, or up to 10 minutes later if they do not. Stores connected to the same Stripe account share this webhook and lose instant updates too."*

### Status is read from Stripe

The badge is read from Stripe each time the page opens, because Stripe can disable an endpoint on its own after repeated failed deliveries, and the merchant can edit or delete it in the Stripe Dashboard.

### The other two ways a payment is confirmed

With or without the webhook, the payment also updates when the shopper returns to the store, and through a background check that starts 10 minutes after the redirect and repeats every 5 minutes. See [[stripe-refunds-sync]] and, for the session's time limits, [[stripe-checkout-flow]].

## Related

- [[payment-providers-stripe]] — hub.
- [[stripe-settings-fields]] — keys and the mode the webhook follows.
- [[stripe-refunds-sync]] — the three ways a status arrives, and refunds.
- [[stripe-checkout-flow]] — the session a webhook event names.
- [[payment-status]] — payment statuses.

## Open questions

- Bulgarian labels of the card and its badges (production translation table).
