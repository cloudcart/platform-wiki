---
type: feature
nav_path: "Orders → Order details → Payment → Manual confirm + Change provider (API access)"
route_name: admin.orders.payment.manual
route_path: /admin/orders/action/payment/manual/:order_id
aliases: ["Manual confirm API", "Change provider API", "BNPL confirm programmatic", "API за ръчно потвърждение"]
tags: [orders, payment, manual-confirm, change-provider, api, json-api-v2]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-payment-manual]]. See the hub for related aspects (Mokka confirm, Klear confirm, change provider, lease).

# Manual confirm + Change provider — API access

## Purpose

This page documents the **programmatic-access boundary** for the manual-confirm and change-provider flows: what the JSON-API v2 payment resource exposes, and why both actions are **admin-panel-only**. The short answer — the API can READ the resulting payment state but cannot ORIGINATE either action.

## Where to find it

Payments are exposed as the [[api-order-payment]] resource on JSON-API v2 — read it to inspect an order's payment record(s): provider, status, `provider_data`, and the `mokka_confirm` meta flag. There is NO API endpoint for manual confirm or change provider. See [[json-api-v2]] for the overall API surface.

## What the merchant can do here

Via the API a merchant (or an integration) can:

- **Read** an order's payment record(s) — provider, status, `provider_data` (including the stored Klear transaction + capture, the Mokka document context), and `mokka_confirm` — useful for syncing payment STATE into external systems after the merchant has acted in the admin panel.

### What the merchant CANNOT do via the API

- **Originate a manual confirm** (Mokka `finish` / Klear capture).
- **Originate a change-provider** action.
- Trigger the order-hooks pipeline (status auto-flip, customer notification, invoice generation, webhook fan-out) that these admin actions run.

## Settings & fields

This page documents an API boundary, not a configuration form — no merchant-editable fields. The exposed read fields live on [[api-order-payment]] (provider, status, `provider_data`, `mokka_confirm`).

## Business rules

### Manual confirm is admin-panel-only

Manual confirm is a real-money BNPL provider commitment (Mokka's `finish` API with a document number; Klear's capture API with a checkout ID). The provider rejections, error handling, document-number validation, and the order-hooks pipeline (status auto-flip, customer notification, invoice generation, webhook fan-out) all live in admin code with provider-specific quirks — Mokka sends the CURRENT total not the original (see [[orders-payment-manual-mokka]]); Klear's error code is not checked before commit (see [[orders-payment-manual-klear]]). Exposing this via the API would bypass those validated paths.

### Change provider is admin-panel-only

Change provider is destructive on taxes — it deletes existing provider-scoped taxes and recomputes against the billing zone's payment-conditional taxes, creates a new payment record, may auto-adjust the shipping side meta when `is_seller_payer_shipping` is set on the new provider, and may re-initialise the gateway for offline providers via `purchase`. The full cascade requires validated admin paths. See [[orders-payment-manual-change-provider]].

### The API surfaces resulting STATE, not the action

After the merchant acts in the admin panel, the API reflects the new payment state (provider, status, `provider_data`, `mokka_confirm`) — useful for downstream sync — but does not allow originating the action. This follows the read-vs-mutate principle for payment actions described on [[json-api-v2]].

### No bulk change-provider

There is no bulk-action on [[orders]] for "change payment provider on selected orders". Merchants doing provider migrations must work order-by-order or script the change against validated admin paths.

## Related

- [[orders-payment-manual]] — hub.
- [[api-order-payment]] — read-only JSON-API v2 payment resource.
- [[json-api-v2]] — API overview + the read-vs-mutate principle on payment actions.
- [[orders-payment-manual-mokka]] — Mokka confirm (admin-only) quirks.
- [[orders-payment-manual-klear]] — Klear confirm (admin-only) quirks.
- [[orders-payment-manual-change-provider]] — change-provider (admin-only) cascade.

## Open questions

None.
