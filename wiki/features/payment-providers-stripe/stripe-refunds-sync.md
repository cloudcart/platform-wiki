---
type: feature
nav_path: "Payment Providers → Stripe → Refunds, sync & capture"
route_name: apps.stripe.settings
route_path: /admin/payment-providers/stripe
aliases: ["Stripe refund", "Stripe refunds", "Stripe sync", "Stripe status verification", "Stripe webhook", "Stripe capture", "Stripe auto-capture", "Stripe Connect", "Stripe subscriptions", "Stripe self-deactivation", "Stripe reconciliation"]
tags: [paymentproviders, payment-providers, stripe, refunds, sync, capture, reconciliation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-stripe]]. See the hub for related aspects (settings, checkout flow, save card).

# Stripe — Refunds, sync & capture

## Purpose

This aspect documents the back-end lifecycle of a Stripe payment after it is initiated: how status is reconciled (the webhook-less **pull-based `sync`**), how **refunds** work (full only), the **auto-capture-only** behaviour, the absence of Stripe Subscriptions and Stripe Connect, and the **self-deactivation** safeguard when credentials go bad at runtime.

## Where to find it

This aspect is mostly runtime / back-end. The one merchant-facing action is the **Refund** button on an order's payment record — see [[orders-payment-refund]]. Status reconciliation, capture mode, Connect and self-deactivation are invisible to the merchant; the results surface on [[orders-details]].

## What the merchant can do here

- **Issue a refund** from the order's payment record (full refund of the captured amount) — see [[orders-payment-refund]].
- **Observe self-deactivation** — if a live key goes bad, the provider flips itself off and the admin is notified; the merchant fixes the key on [[stripe-settings-fields]] and re-enables.
- There is **no** manual capture action for Stripe (auto-capture only) — the [[orders-payment-capture]] button does not apply.

## Settings & fields

This aspect does not expose its own fields. Refunds and capture are runtime behaviours; credentials and mode are configured on [[stripe-settings-fields]].

## Business rules

### Sync — webhook-less status verification

The Stripe integration is **pull-based** (sync), not push-based (webhook). On the customer's return to CloudCart, the `sync` method fetches the latest status by inspecting the `provider_reference_id` prefix:

- `cs_*` (Checkout Session) → fetch the session; if it has a `payment_intent`, switch to fetching that.
- `pi_*` (PaymentIntent) → fetch and confirm if needed; `succeeded` → `completed`, else → `cancelled`.
- `ch_*` (Charge) → fetch; map by Stripe charge status (succeeded / refunded / pending / failed).

CloudCart logs every API call (request + response) to `PaymentLogs` for traceability.

### No Stripe-specific webhook handler

Despite `payments.webhook` being the platform's generic webhook route, the Stripe integration does **not** register a handler for it. Every status update is reconciled by the sync (pull) flow when the customer returns from Stripe Checkout, or via the periodic payment-sync queue. A merchant configuring webhooks in their Stripe Dashboard will see no effect on CloudCart.

### Refunds

Supported. The merchant clicks Refund on the order's payment record (see [[orders-payment-refund]]). CloudCart calls Stripe's `refunds.create` with the saved `payment_intent` or `charge` ID. On success (`status: succeeded`), the payment status flips to `refunded`. Partial refunds are technically possible at the Stripe API level, but this integration issues a **full refund** of the captured amount — there is no partial-refund input.

### Capture mode — auto-capture only

The integration always uses Stripe's default capture flow (Stripe charges and captures simultaneously on payment success). There is **no** manual-authorize / capture-later mode for Stripe in the current configuration — the [[orders-payment-capture]] action does not apply. The source code has commented-out scaffolding for `capture_method: manual`, but it is disabled.

### Recurring / subscriptions

The integration uses Stripe Checkout in `mode: payment` (one-off) — not `mode: subscription` (see [[stripe-checkout-flow]]). The Save-Card flow enables one-click repeat purchases via off-session charges (see [[stripe-save-card]]), but there is **no** scheduled-billing / Stripe Subscriptions integration at this layer.

### Stripe Connect — not supported

CloudCart's Stripe integration is **single-account-per-store** — each store wires up its own publishable/secret key pair. There is no marketplace / Connect / managed-account flow at the CloudCart level. A merchant needing a Connect-style multi-vendor model would use [[payment-providers-cloudcart-pay|CloudCart Pay]] (itself a Paypercut-managed connected-account model) or build their own.

### Self-deactivation on invalid credentials

If Stripe throws an exception when initializing the Stripe client at runtime (typically an invalid API key), CloudCart catches it, sends an admin notification ("Stripe error: ... Stripe is deactivated"), and **flips the provider's Active flag to OFF automatically**. The merchant must fix the keys on [[stripe-settings-fields]] and re-enable. (This is the runtime counterpart to the save-time live key ping documented on [[stripe-settings-fields]], which prevents a broken key from being saved in the first place.)

## How it works (verified against backend)

- The `sync` reference-ID dispatch is purely prefix-based (`cs_` / `pi_` / `ch_`), so the same method reconciles a payment regardless of which point in the flow it reached.
- The periodic payment-sync queue re-runs `sync` for payments still in a non-final state, which is how a customer who closed the browser mid-redirect eventually gets a resolved status without any Stripe webhook.
- Refund maps Stripe's `refunds.create` result `status: succeeded` to the platform `refunded` status; the `payment_intent` / `charge` ID needed for the refund call is the one stored as `provider_reference_id` during the checkout flow.

## Related

- [[payment-providers-stripe]] — hub.
- [[stripe-checkout-flow]] — produces the `cs_*` / `pi_*` reference IDs this sync reconciles.
- [[stripe-save-card]] — the off-session charge whose status this sync resolves.
- [[stripe-settings-fields]] — credentials + the save-time key ping that complements runtime self-deactivation.
- [[orders-payment-refund]] — the merchant-facing Refund action.
- [[orders-payment-capture]] — manual capture flow (not used by Stripe).
- [[payment-providers-cloudcart-pay]] — the connected-account alternative for marketplace models.
- [[payment-status]] — completed / cancelled / refunded values.
- [[orders-details]] — where reconciled status surfaces.

## Open questions

(none)
