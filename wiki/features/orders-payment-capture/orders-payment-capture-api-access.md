---
type: feature
nav_path: "Orders → Order details → Payment → Capture / Cancel → API access & plan gate"
route_name: admin.orders.payment.capture
route_path: /admin/orders/action/payment/capture-authorization/:payment_id
aliases: ["Capture API access", "Capture read-only API", "authorize_payment plan gate", "Fulfillment indirect capture API", "No mutate capture endpoint"]
tags: [orders, payment, capture, authorization, api, plan-gate]
plan_gates: ["authorize_payment"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-payment-capture]]. See the hub for the other aspects (buttons & visibility, provider matrix, amount-exceeds rule, side effects, automatic triggers).

# Payment capture — API access & plan gate

## Purpose

Documents the programmatic surface of capture / cancel — which is **read-only** for direct capture, the one indirect API path that does capture (via fulfillment), and the `authorize_payment` plan feature that controls whether two-phase mode can exist at all.

## Where to find it

Programmatic access is via JSON-API v2 (see [[json-api-v2]]). The plan gate is evaluated on the gateway-config form on [[settings-payment-providers]] and during checkout — not on [[orders-details]] directly. See [[plan-gates]].

## What the merchant can do here

- **Read** a payment's authorization state via the [[api-order-payment]] resource — fetch `authorize_amount`, `provider_reference_id`, and status to sync the post-capture state into external systems.
- **Indirectly capture** by creating an `order-fulfillment` (see [[api-order-fulfillment]]) on a two-phase order whose gateway supports `captureAutomaticAuthorization`.

What the merchant CANNOT do via the API: originate a direct capture or cancel.

## Settings & fields

### JSON-API v2 is read-only for payment actions

Payments are exposed as the **read-only** [[api-order-payment]] resource on JSON-API v2 — useful for fetching the payment's authorization state, `authorize_amount`, `provider_reference_id`, and status.

**Capture and Cancel Authorization are admin-panel-only.** The API does NOT expose endpoints to capture or cancel a payment authorization — these are real-money actions against the gateway (the supported providers being Borica WAY4, DSK, Btepos, Raiffeisen, Monri, Revolut Business — see [[orders-payment-capture-provider-matrix]]). The platform requires them to flow through validated admin paths with the appropriate permission gates, the gateway-call retry behaviour, the loyalty / cash split-call handling, and the post-capture cascade (see [[orders-payment-capture-side-effects]]).

The API surfaces the resulting payment STATE — useful for syncing the post-capture status into external systems — but does not allow originating the capture or cancel action. See [[json-api-v2]] for the read-vs-mutate principle on payment actions.

### Fulfillment-add indirect capture (the one supported API path)

Capture IS automatically triggered when an `order-fulfillment` is created (via [[api-order-fulfillment]]) for orders whose gateway supports `captureAutomaticAuthorization`. So creating a fulfillment through the API on a two-phase order will **indirectly capture** the funds — that path IS available. Direct manual capture without fulfillment is not. See [[orders-payment-capture-auto-triggers]] for the same trigger from the admin UI.

## Business rules

### Plan gate — `authorize_payment`

This feature is gated by the `authorize_payment` plan feature (see [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `authorize_payment` | Boolean (cast restriction — default ON via `restrict.defaults`) | Whether the merchant's plan ALLOWS two-phase (authorize-then-capture) configuration on the supported card gateways (Borica WAY4 / DSK / Btepos / Raiffeisen / Monri). |

The plan check runs in **two** places:

1. **On each gateway's configuration form** — when the merchant tries to enable `authorize_payment` mode on the gateway, the validator REJECTS the save with *"Your plan does not support authorized payments"*.
2. **During checkout** — when processing a checkout against a gateway configured for auth, the service refuses to enter auth mode if the plan no longer supports it.

With this gate active (feature not in the plan), the two-phase flow cannot be configured, so the **Capture / Cancel authorization** buttons never appear on any order.

When the gate is hit, the merchant gets an **inline validation error on the payment-provider config form** rather than a separate upsell redirect. `authorize_payment` is a boolean — it requires a plan that includes the feature; it does NOT extend via feature packs (see [[plan-vs-feature-pack]]). The default in `restrict.defaults` is **restricted (`1`)** — i.e. this feature is OFF by default on plans that don't explicitly include it.

### Chargebacks are separate

Chargebacks are gateway-initiated via webhook (a separate flow), NOT triggered through the capture / cancel API. See [[orders-payment-refund]] for the broader gateway-initiated reversal context.

## Related

- [[orders-payment-capture]] — hub.
- [[orders-payment-capture-provider-matrix]] — the supported-provider set referenced by the read-only note.
- [[orders-payment-capture-auto-triggers]] — the fulfillment-add capture trigger from the admin UI.
- [[orders-payment-capture-side-effects]] — the post-capture cascade the API state reflects.
- [[api-order-payment]] — read-only JSON-API v2 payment resource.
- [[api-order-fulfillment]] — writable; fulfillment add can auto-capture.
- [[json-api-v2]] — API overview (read-vs-mutate principle).
- [[plan-gates]] — plan-feature gating model.
- [[plan-vs-feature-pack]] — boolean plan feature vs feature-pack extension.
- [[plan-features]] — plan-feature catalogue.
- [[settings-payment-providers]] — where the `authorize_payment` validation fires.

## Open questions

None.
