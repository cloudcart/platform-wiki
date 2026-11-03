---
type: feature
nav_path: "Orders → Order details → Receipt → Eligibility"
route_name: admin.orders.receipt
route_path: /admin/orders/receipt/:order_id
aliases: ["Receipt eligibility", "isReadyForReceipt", "When is a receipt generated", "Receipt 404", "Receipt requires N18 Audit", "Receipt only for paid orders"]
tags: [orders, receipt, eligibility, invoicing, n18-audit]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-receipt]]. See the hub for the other aspects (surfaces, numbering, rendering).

# Receipt — eligibility (per order)

## Purpose

Explains **the gates that decide whether a receipt exists for a given order** — the conditions an order must satisfy before the platform auto-assigns a receipt number and the link appears. This is the aspect to read for any *"why is there no receipt for this order / why does the receipt link return 404"* ticket.

## Where to find it

There is no merchant-facing settings screen for receipt eligibility — it is driven by the N18 Audit app being installed ([[apps-n18-audit]]), an active invoicing provider ([[settings-invoicing]]), and the order's status / fulfilment / content. The eligibility check is the same predicate used by the invoice flow.

## What the merchant can do here

Indirectly, the merchant influences eligibility by:

- Installing the **N18 Audit** app ([[apps-n18-audit]]) — without it, no receipts are ever generated.
- Configuring an active invoicing provider on [[settings-invoicing]].
- Moving the order into a payable / fulfilled state (mark paid, fulfil, or sell digital products), which is what makes `isReadyForReceipt` return true.

## Settings & fields

No dedicated fields. Eligibility is computed, not configured. The relevant inputs are the order's `status`, its `status_fulfillment`, and whether it contains digital products — all visible on [[orders-details]].

## Business rules

### Receipt requires the N18 Audit app installed

Receipt generation is gated by the N18 Audit app being installed. Without this app the receipt action is unavailable and the route returns 404. Receipts are primarily for Bulgarian accounting compliance (the Наредба № Н-18 audit format); merchants in other countries typically rely on the invoice flow instead. See [[apps-n18-audit]].

### Receipt only for paid / completed / fulfilled / digital-only orders

The receipt is generated only when the order is in one of: `status_fulfillment = fulfilled` OR `status IN (paid, completed)` OR the order contains digital products. So the merchant CANNOT obtain a receipt for an unpaid order — the platform refuses until the order reaches a payable state.

### `isReadyForReceipt` mirrors invoice eligibility

The "ready for receipt" check delegates to the SAME eligibility predicate as the invoice flow (`isReadyForInvoice`). A receipt therefore cannot be generated for any order that would not yet qualify for an invoice — paid/completed status, fulfilled, or digital-only content. If the invoice would not be issuable, neither will the receipt.

### Provider-gated visibility → 404

If the active Invoicing provider cannot produce a receipt for this order, the route returns HTTP 404 (no document available). So whether a receipt is obtainable depends on:

- Whether the merchant has an active invoicing provider.
- Whether that provider supports receipts (some external apps do not).
- Whether the order is in a state that warrants a receipt (typically paid / completed / fulfilled / digital-only).

### Receipt is gated only on app + state, not on a plan feature

Unlike the invoice surface (gated by the `invoices` plan feature — see [[orders-invoice]]), the receipt has no plan-feature gate of its own. Its availability is governed by the N18 Audit app installation and the order-state eligibility above.

## Related

- [[orders-receipt]] — hub.
- [[apps-n18-audit]] — the app whose installation is the hard gate for receipts.
- [[settings-invoicing]] — the active provider that must support receipts.
- [[orders-invoice]] — the invoice flow whose `isReadyForInvoice` predicate the receipt reuses.
- [[order-status-workflow]] — the statuses (`paid`, `completed`) and fulfilment state that satisfy eligibility.
- [[order]] — entity carrying `status`, `status_fulfillment`.

## Open questions

None.
