---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Refunds & webhooks"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay refunds", "CloudCart Pay webhooks", "CloudCart Pay status mapping", "CloudCart Pay sync", "CloudCart Pay refunded status"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (account model, activation gate, checkout flow, saved card) and the four lifecycle tabs.

# CloudCart Pay — refunds & webhooks

## Purpose

This page documents how a CloudCart Pay charge changes status after the customer pays — how refunds are issued from the order, how incoming webhook events map to platform payment statuses, and the sync poll that fills the gaps. It is the page to read for "I refunded but the order still says succeeded" or "why is the payment status not updating?" tickets.

## Where to find it

Refunds are issued from the order details page (see [[orders-payment-refund]]); the resulting status appears on the order and on the [[payment-providers-cloudcart-pay-transactions|Transactions tab]] at Sidebar → **Payment Providers** → **CloudCart Pay**. Webhook handling and sync are automatic and have no merchant-facing screen.

## What the merchant can do here

- **Issue a full or partial refund** for a CloudCart Pay charge from the order.
- **See the resulting status** (Refunded / partially refunded) on the order and the Transactions tab.
- **Rely on automatic status updates** as the provider pushes webhook events.

## Settings & fields

There are no merchant-facing fields for refunds or webhooks — the refund amount is entered on the order details refund dialog (see [[orders-payment-refund]]), and webhook delivery is fully automatic. Status values surface on [[payment-status]] and the Transactions tab.

## Business rules

### Refunds run through CloudCart Pay

Clicking **Refund payment** on an order (see [[orders-payment-refund]]) for a CloudCart Pay charge posts a refund through the provider's `/v1/refunds` endpoint scoped to the connected account, with `payment_intent` referencing the stored `provider_reference_id`. A successful refund flips the platform's payment status to `Refunded` (see [[payment-status]]). The amount refunded appears on the transaction row in the Transactions tab.

**Important provider quirk:** the underlying payment intent's `status` field stays `succeeded` after a refund; the refund is reflected in the separate `amount_refunded` / `latest_operation=refund` markers. The UI maps these to the `refunded` / `partially_refunded` pseudo-statuses — see [[payment-providers-cloudcart-pay-transactions]] for how this surfaces in the ledger. This is why a refunded charge can still look "succeeded" at the provider level while CloudCart correctly shows it as Refunded.

### Webhook events the platform listens for

The provider's webhook dispatch hits the platform's `payments.webhook` endpoint (`<cc_payments_domain>/webhook/cloudcart_pay`) with `provider=cloudcart_pay`. The platform maps these event types to platform payment statuses:

| Provider event | Mapped CloudCart status |
|-----------------|--------------------------|
| `checkout_session.completed` | Completed |
| `payment_intent.succeeded` | Completed |
| `payment_intent.payment_failed` | Failed |
| `charge.failed` | Failed |
| `charge.refunded` | Refunded |
| `payment_intent.canceled` | Canceled |
| (any other type) | falls back to a polled sync against the checkout / payment-intent |

The full payload of every webhook is appended to the order's payment log so support staff can audit the transition history.

### Sync as a fallback

A `sync` operation is called for unknown event types and from the order details page. It fetches the live payment intent (`GET /v1/payment_intents/{id}`) from the provider with the `Paypercut-Account` header (see [[cloudcart-pay-account-model]]) and re-maps to the platform status. This means support can force a status refresh from the order page even if a webhook was missed.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[orders-payment-refund]] — where a refund is initiated.
- [[payment-providers-cloudcart-pay-transactions]] — how refund markers surface in the ledger.
- [[payment-status]] — Completed / Refunded / Failed / Canceled status definitions.
- [[cloudcart-pay-account-model]] — the connected-account scoping used by refund / sync calls.
- [[cloudcart-pay-checkout-flow]] — where `provider_reference_id` (the refunded payment intent) is set.
- [[settings-hooks]] — store-side webhooks (distinct from the provider → platform webhook described here).

## Open questions

(none)
