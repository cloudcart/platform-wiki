---
type: feature
nav_path: "Orders → Order details → Status"
route_name: admin.orders.change-status
route_path: /admin/orders/action/status/:order_id/:status
aliases: ["Change order status", "Update order status", "Bulk status change", "Order status pill", "Промяна на статус на поръчка"]
tags: [orders, status, notification, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 9
---

# Order status change

## Purpose

The flow for **changing the status of one or many orders** — the status pill in the breadcrumb of [[orders-details]] (per-order, single click) AND the bulk status action on the [[orders]] list (multi-select). Status changes drive multiple downstream effects: customer email notifications, stock decrement / restore, invoice generation, fulfillment cascade, payment-authorization release, and `order.updated` webhooks.

The platform's order status taxonomy is defined in [[settings-statuses]]; the dropdown lists the merchant-pickable statuses (built-in + merchant-defined) plus the two fulfillment values. But not every visible target is reachable from every starting state — the platform enforces hard transition gates for `Completed` and `Cancelled`, locks archived orders entirely, permanently locks a cancelled / refunded order once a reversal has been recorded against it, and refuses **any** status change on an order whose payment authorisation is smaller than its total.

## Where to find it

### Per-order (single change)
From [[orders-details]] → **breadcrumb status badge** (colour-coded pill). Click → opens an inline Select2 dropdown listing the available statuses. Pick one → applies immediately.

Routes:
- `admin.orders.status.load` (GET) — loads the status dropdown HTML (lazy load via `data-box-ajax`).
- `admin.orders.change-status` (GET) — applies a specific status to this order.

The 3-dot dropdown on [[orders-details]] also exposes one-click **Mark as completed** and **Cancel order** shortcuts. Their visibility is cosmetic — the Cancel shortcut hides when a line can no longer be given back cleanly — but the status pill still cancels the order in that case. Both shortcuts route through the same change-status pipeline.

### Bulk (from list)
From [[orders]] list → bulk action **Mark as completed**. Route: `admin.orders.bulk-status` (POST).

The bulk action dropdown exposes exactly three actions: **Archive**, **Unarchive**, **Mark as completed**. There is NO bulk Cancel / Paid / Refunded — those require per-order changes. See [[orders-status-change-bulk]] for the fail-fast transaction behaviour.

## Sub-pages (in this cluster)

This page is split into seven aspect pages. The Assistant should drill into the aspect that matches the merchant's question, not read every page.

- [[orders-status-change-pill]] — the breadcrumb status pill UI: lazy-loaded dropdown, badge colours, dropdown contents (which statuses are exposed and which are hidden), draft-order single-option dropdown.
- [[orders-status-change-transition-rules]] — the hard transition gates the platform enforces (Completed / Cancelled / archived lock / reversal lock / authorised-amount check); correction of the older "any-to-any" framing.
- [[orders-status-change-side-effects]] — the full side-effect chain on every status change: stock, invoice / receipt numbers, webhook, customer email, history rows, discount recount, authorisation release, the auto-created return, and the gateway paths that suppress most of it.
- [[orders-status-change-notification]] — the three switches on the single status-change email (`notify_customer` flag + the template's own active flag + store-wide `customer_email_notifications`); queue delay + double-flip risk.
- [[orders-status-change-fulfillment-gate]] — fulfillment dropdown blocked for external-shipping orders; automatic fulfillment reset on negative status; Paid + digital auto-fulfillment; payment-authorization auto-release on negative status.
- [[orders-status-change-bulk]] — bulk-status processor on [[orders]]: 3 exposed actions, fail-fast DB transaction (whole batch rolls back on first error), customer-notification multiplier risk.
- [[orders-status-change-api]] — JSON-API v2 PATCH of `status`: same hard gates, same side effects, history namespace `api2`, the five hidden gateway statuses.

## What the merchant can do here

In summary: change one order's status from the breadcrumb pill, change many orders' status (only to Completed) from the list bulk action, or PATCH the status programmatically via JSON-API v2. Each aspect page above documents one slice of the surface. The merchant CANNOT skip customer notification on a per-change basis (it's controlled by `notify_customer`, the template's active flag, and the store-wide kill switch — see [[orders-status-change-notification]]) and CANNOT bypass the transition gates (see [[orders-status-change-transition-rules]]).

## Settings & fields

The status-change flow itself owns no settings — it consumes settings owned by other pages:

- [[settings-statuses]] — the canonical status taxonomy (rename built-ins, add custom). It carries no notification settings.
- [[settings-cart]] — `order_status_for_quantity_decrease` (controls when stock decrements / restocks, snapshotted onto each order at placement; see [[inventory-decrement-timing]]).
- [[marketing-omnichannel-mails-list]] — the single status-change email template + its active flag + the store-wide `customer_email_notifications` kill switch.
- [[settings-hooks]] — `order.updated` webhook fires on every status change.

## Business rules

The platform enforces hard transition gates for canonical statuses (see [[orders-status-change-transition-rules]]), runs a deterministic side-effect chain on every change (see [[orders-status-change-side-effects]]), and gates customer notifications through three independent switches (see [[orders-status-change-notification]]). The bulk processor is fail-fast: the first failing order rolls back the whole batch (see [[orders-status-change-bulk]]).

## Programmatic access

Order `status` can be PATCHed via **JSON-API v2** — see [[api-orders]] for the request shape. The API runs the SAME pipeline as the admin pill (history rows with `api2` namespace + customer notification + stock + webhook), and also sets the order's `manual` marker, after which gateway events stop moving its status. The five gateway-driven statuses (`chargebacked`, `disputed`, `timeouted`, `failed`, `voided`) are NOT settable via the API for the same reason they're hidden from the dropdown — they're owned by the payment-provider integration. Full coverage on [[orders-status-change-api]].

## Related

- [[orders-details]] — parent page hosting the status pill.
- [[orders]] — list with bulk "Mark as completed" action.
- [[settings-statuses]] — status taxonomy (source of truth for names).
- [[settings-cart]] — `order_status_for_quantity_decrease` (decrement timing).
- [[marketing-omnichannel-mails-list]] — status-change email template + global notification kill switch.
- [[settings-hooks]] — `order.updated` webhook.
- [[orders-payment-capture]] — what happens at capture, after the authorised-amount check passes.
- [[orders-notify-customer]] — the per-order `notify_customer` flag (a flag only — the control sends no email).
- [[orders-history]] — every status change appears as a history event.
- [[orders-credit]] — Refunded status may trigger credit-note flow.
- [[orders-invoice]] — Paid status may trigger invoice generation.
- [[orders-shipping-waybill]] — fulfillment cascade interacts with waybill flow.
- [[api-orders]] — JSON-API v2 endpoint for status PATCH.
- [[json-api-v2]] — API overview.
- [[order-processing-pipeline]] — the full status-transition pipeline.
- [[inventory-decrement-timing]] — decrement / restock timing setting.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
