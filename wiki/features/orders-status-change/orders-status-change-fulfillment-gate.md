---
type: feature
nav_path: "Orders → Order details → Status → Fulfillment gate"
route_name: admin.orders.change-status
route_path: /admin/orders/action/status/:order_id/:status
aliases: ["Fulfillment status gate", "Fulfilled / Not fulfilled dropdown", "External shipping fulfillment block", "Digital auto-fulfillment", "Payment authorization release on negative status"]
tags: [orders, status, fulfillment, shipping, payment-authorization]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-status-change]]. See the hub for the other aspects (pill, transition rules, side effects, notification, bulk, API).

# Order status change — Fulfillment + authorization gate

## Purpose

The same dropdown that changes order status (see [[orders-status-change-pill]]) also lists fulfillment statuses — but the platform applies special rules when the fulfillment side gets touched. This page covers four interlocking behaviours: the fulfillment dropdown being blocked for external-shipping orders, the automatic fulfillment reset on negative-status transitions, the Paid + digital-products auto-fulfillment record, and the payment-authorization auto-release on negative-status transitions. Together they keep the order's fulfillment + payment state coherent with the order status without forcing the merchant to manually undo upstream actions.

## Where to find it

- **Fulfillment dropdown rejection**: surfaces as an error toast when the merchant picks **Fulfilled** or **Not fulfilled** from the status pill dropdown on an order with an external waybill attached.
- **Fulfillment reset / authorization release / digital auto-fulfillment**: automatic — the merchant doesn't see a UI surface, only the side effects (fulfillment row flips, authorization disappears from the payment row, digital fulfillment row appears).

## What the merchant can do here

### Picking Fulfilled / Not fulfilled — blocked for external-shipping orders

When the order has an EXTERNAL shipping provider attached (Speedy, Econt, DPD, etc. — a waybill already created via [[orders-shipping-waybill]]), picking **Fulfilled** or **Not fulfilled** from the breadcrumb status dropdown is REJECTED with:

> *"For changing fulfillment status, use the Fulfill button"* (`order.err.for_change_fulfillment_status_use_button`).

The merchant must use the explicit **Fulfill** button in the order's product table — the dropdown path is blocked to prevent desyncing the shipping integration. The waybill flow owns the fulfillment state for external-shipping orders.

For orders WITHOUT an external shipping provider (digital-only, in-store pickup, manual / no shipping), the dropdown's Fulfilled / Not fulfilled selection works normally — it just flips the `status_fulfillment` field.

### Fulfillment auto-reset on negative-status transitions

If the merchant moves an order with `status_fulfillment = fulfilled` to ANY negative status (`Cancelled`, `Refunded`, `Voided`, `Failed`, `Disputed`, `Chargebacked`, `Timeouted`), the platform automatically resets the fulfillment flag to `not_fulfilled` at the same time. The merchant doesn't have to manually undo fulfillment first.

This is symmetric: if the merchant later moves the order back to a positive status (e.g., `Refunded → Paid` to reverse an erroneous refund), fulfillment does NOT automatically flip back to `fulfilled` — the merchant has to re-fulfill manually. The reset is one-way.

### Paid + digital products = auto-fulfillment record

When the merchant marks an order `Paid` AND the order contains digital products AND fulfillment is not already complete, the platform auto-creates a fulfillment record covering the digital line items. This is what makes the file-download email fire — the digital fulfillment record triggers the link-delivery flow.

The merchant does NOT need to manually fulfill digital line items. For mixed carts (digital + physical), the auto-fulfillment covers ONLY the digital items; physical items still require explicit fulfillment via [[orders-shipping-waybill]] or the Fulfill button.

If the order has BOTH digital products AND an external shipping provider, the dropdown remains blocked for Fulfilled / Not fulfilled — but the auto-fulfillment record for digital items still fires on Paid because it's a different code path (it creates a fulfillment row, doesn't change `status_fulfillment` to `fulfilled` unless the whole order is covered).

### Payment-authorization auto-release on negative-status transitions

If the order has a held payment authorization (e.g., Stripe two-phase capture) AND the merchant moves the order to ANY negative status, the platform automatically calls the payment gateway to RELEASE the authorization. The merchant doesn't have to manually void the authorization first via [[orders-payment-capture]].

This is part of the standard negative-status side-effect chain — see [[orders-status-change-side-effects]] for the full chain. The release happens synchronously as part of the status change; if the gateway call fails, the status change ABORTS and the merchant sees a gateway error.

### Mark Completed gate (full fulfillment required)

Marking `Completed` requires `status_fulfillment = fulfilled` (in addition to `paid`). See [[orders-status-change-transition-rules]] for the gate. So the typical "happy path" sequence is:

1. Customer pays → order goes to `Paid` (stock decrements, digital auto-fulfillment if applicable).
2. Merchant generates waybill / hands off physical goods → order's `status_fulfillment` becomes `fulfilled`.
3. Merchant clicks **Mark as completed** (from the pill OR the 3-dot dropdown OR the bulk action) → order goes to `Completed`.

If step 2 hasn't happened, step 3 is blocked with the *"Only paid and/or fulfilled orders can be marked as Completed"* error.

## Settings & fields

The fulfillment gate is NOT configurable. The merchant cannot, for example, override the "use the Fulfill button" block via a setting. The rules are code-level and apply uniformly.

## Business rules

- The fulfillment-dropdown block triggers based on whether the order has an EXTERNAL shipping provider attached, not based on whether a waybill is currently issued. So removing the waybill but leaving the provider attached still blocks the dropdown.
- The negative-status fulfillment reset is silent — no history entry specifically calls it out; the merchant infers from the fulfillment row showing `not_fulfilled` after the transition.
- The negative-status auto-release of payment authorization writes to the order's payment history (the authorization release IS logged), separate from the order-status history pair.
- Digital auto-fulfillment on Paid does NOT fire if fulfillment is already complete for those line items (e.g., merchant pre-fulfilled before payment). Idempotent.
- The blocks apply to BOTH the admin dropdown AND the JSON-API v2 PATCH. The API rejects the same fulfillment dropdown moves with the same error. See [[orders-status-change-api]].

## Programmatic access

JSON-API v2 PATCH of `status` runs the same fulfillment-gate logic — the API rejects Fulfilled / Not fulfilled changes for external-shipping orders with the same error, applies the same auto-reset on negative-status transitions, and triggers the same payment-authorization release. See [[orders-status-change-api]].

For explicit fulfillment management, JSON-API v2 exposes the `order-fulfillment` sub-resource — see [[api-order-fulfillment]]. The merchant / integrator can create / edit fulfillment records there directly, bypassing the status dropdown.

## Related

- [[orders-status-change]] — hub.
- [[orders-status-change-pill]] — the dropdown that surfaces the fulfillment-statuses + the block.
- [[orders-status-change-transition-rules]] — Completed requires Paid + Fulfilled.
- [[orders-status-change-side-effects]] — full negative-status side-effect chain.
- [[orders-status-change-api]] — API honours the same fulfillment-gate rules.
- [[orders-shipping-waybill]] — waybill flow that owns external-shipping fulfillment.
- [[orders-payment-capture]] — payment-authorization capture / cancel flow.
- [[api-order-fulfillment]] — fulfillment sub-resource for programmatic management.

## Open questions

- Whether removing the external-shipping provider AFTER waybill issue (apps-uninstall edge case) unblocks the dropdown immediately or requires a refresh `(verify)`.
