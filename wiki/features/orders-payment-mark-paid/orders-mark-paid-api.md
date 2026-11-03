---
type: feature
nav_path: "Orders → Order details → Payment → Mark as paid → API & plan gates"
route_name: admin.orders.payment.mark_paid
route_path: /admin/orders/action/payment/mark_paid/:payment_id
aliases: ["Mark-paid API access", "Mark-paid programmatic", "Payment mutate endpoint", "Mark-paid plan gate", "Read-only payment resource"]
tags: [orders, payment, manual-payment, api, plan-gates]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-mark-paid]]. See the hub for the other aspects (form & visibility, post-paid pipeline, status-flip rules, adjacent actions).

# Mark as paid — API access & plan gates

## Purpose

This page answers two questions an integration developer or a plan-conscious merchant will ask: *Can I mark a payment paid through the API?* (no) and *Does this action consume / require a plan feature?* (no per-action gate). It documents the read-only position of payments in JSON-API v2 and the exact plan-gate reasoning verified against the backend.

## Where to find it

Programmatic access is via the [[json-api-v2]] surface (the `/api/v2/` JSON-API), specifically the read-only [[api-order-payment]] resource. There is no admin screen for this page's content — it describes API and plan-gate behaviour rather than a UI.

## What the merchant can do here

Via JSON-API v2 the merchant (or their integration) can **read** the order's payment record(s) — provider, amount, status, `provider_reference_id`, capture amount, timestamps — useful for syncing payment status into ERP / accounting integrations. The merchant CANNOT originate the mark-as-paid action through the API; it is admin-panel-only.

## Settings & fields

The [[api-order-payment]] resource exposes (read-only) the payment fields, including `provider_reference_id` set via [[orders-mark-paid-form]]. No mutate/action endpoint exists. Plan-gate configuration for the action lives in the platform's the platform code (the mark-paid route is NOT listed there — see Business rules).

## Business rules

### Mark-as-paid is admin-panel-only — no API mutate endpoint

Payments are exposed as the **read-only** [[api-order-payment]] resource on JSON-API v2 — useful for fetching the order's payment record(s) including provider, amount, status, `provider_reference_id`, capture amount, and timestamps.

The API does NOT expose a payment action endpoint — the merchant cannot trigger payment status transitions (mark-as-paid, refund, capture, cancel, manual confirm) through JSON-API v2. The rationale: payment actions are financially impactful and the platform requires them to flow through validated admin paths with the appropriate permission gates (`orders.refund`, etc.), the heavyweight cascade (customer notification, invoice generation, receipt generation, stock decrement, status auto-flip with precedence rules, customer income recalculation, webhook fan-out — see [[orders-mark-paid-pipeline]]), and the audit-log capture of the acting admin.

The API surfaces the resulting payment STATE after the merchant marks paid in the admin — useful for syncing payment status into ERP / accounting integrations — but does not allow originating the mark-paid action.

For programmatic offline-payment confirmation (e.g., a payment gateway integration auto-detecting a bank transfer), the integration typically uses the platform's gateway-webhook pipeline (see [[settings-payment-providers]]) rather than mimicking the admin mark-as-paid action through an API.

See [[json-api-v2]] for the read-vs-mutate principle on payment actions.

### No per-action plan gate

**This action does NOT carry its own plan-feature gate.** Verified against backend:

- The mark-paid controller methods do not call the plan-enabled / plan-allow-create / plan-can-create-by-map checks.
- The route `/admin/orders/action/payment/mark_paid/...` is NOT registered under `restrict.access` or `restrict.path` in the plan config.
- The action is gated only by staff-permission (the standard `orders` permission section per [[settings-staff]]).

### Page-level gates still apply (indirectly)

**Reaching this button** requires the merchant to first land on the order detail page — which IS path-gated by `orders_amount`, `orders_revenue`, and `users_traffic` (see [[orders-details]] for the page-level plan gates). So a merchant whose order count / revenue / traffic cap has been hit cannot reach this action because they cannot open the order detail page. Mark-as-paid itself has no per-action gate beyond that.

See [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] for the platform's plan-feature model.

## Related

- [[orders-payment-mark-paid]] — hub.
- [[orders-mark-paid-pipeline]] — the cascade the API deliberately does not let external callers originate.
- [[api-order-payment]] — read-only JSON-API v2 payment resource.
- [[json-api-v2]] — API overview + read-vs-mutate principle.
- [[settings-payment-providers]] — gateway-webhook pipeline for programmatic confirmation.
- [[settings-staff]] — `orders` permission section that gates the action.
- [[orders-details]] — page-level plan gates that apply indirectly.
- [[plan-gates]] / [[plan-vs-feature-pack]] / [[plan-features]] — the plan-feature model.

## Open questions

None.
