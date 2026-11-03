---
type: feature
nav_path: "Orders → Order details → Products → Fulfillment popover"
route_name: admin.orders.products.fulfillment-popover
route_path: /admin/orders/action/products/:order_id/fulfillment-popover/:line_id
aliases: ["Fulfilled line popover", "Per-line fulfillment info", "Tracking popover", "Order line fulfilled badge"]
tags: [orders, products, line-items, fulfillment, readonly]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[orders-products]]. See the hub for the other aspects (add, edit, delete, line discount, stock effects, side effects).

# Order products — Fulfillment popover

## Purpose

A small **read-only** popover that opens when the merchant clicks the *"Fulfilled"* badge on a line that has already been part of a generated waybill. Shows the line's tracking URL and fulfillment date. This is the only per-line view that's still available once a line is locked from edit / delete by an active waybill.

## Where to find it

[[orders-details]] → products table → on a fulfilled line, click the **Fulfilled** badge (the small badge that replaces the per-row cog when `order_fulfillment_id` is set). Opens as an `ajax-modal` with small size.

## What the merchant can do here

- **Read the tracking URL** for the line (clickable, opens in a new tab) — when present.
- **Read the fulfillment date** — when the line's waybill was generated.
- **Nothing else** — the popover has no interactive elements. The modal footer is CSS-hidden (`display: none`).

For full waybill detail, void, re-print, etc. the merchant uses [[orders-shipping-waybill]].

## Settings & fields

### Modal 6 — `product/fulfillment-popover.tpl`

| Element | Value | Notes |
|---|---|---|
| **Tracking URL** | Clickable link | Renders only when the waybill carries a tracking URL. Opens in a new tab. |
| **Fulfillment date** | Formatted timestamp | The date the waybill was generated. |

No forms, no inputs, no buttons. The modal footer is hidden via CSS.

## Business rules

### The popover is the ONLY per-line view for fulfilled lines

Once a line has a non-null `order_fulfillment_id` (it belongs to a generated waybill), the per-row cog (Edit / Add discount / Remove product) is hidden. The "Fulfilled" badge replaces it. Clicking the badge opens this popover.

### To change a fulfilled line, void the waybill first

The fulfillment popover does NOT let the merchant void or re-issue. To change a fulfilled line, the merchant:
1. Voids the waybill via [[orders-shipping-waybill]] → Remove action.
2. Now the cog returns on the line; edits or removes via [[orders-products-edit]] / [[orders-products-delete]].
3. Optionally re-generates the waybill.

This protects courier-side dispatch integrity — a package declared to the courier cannot be silently mutated.

### Digital lines render this popover too

Digital products are fulfilled instantly on add (when they go onto an all-digital order — see [[orders-products-add]]). The popover renders with the auto-fulfilment date but typically without a tracking URL — digital fulfilments have no courier handoff.

### No history entries on view

Opening the popover does NOT write to [[orders-history]] — it's purely a read.

## Related

- [[orders-products]] — hub.
- [[orders-products-add]] — adding a digital product to an all-digital order auto-creates a fulfillment that surfaces in this popover.
- [[orders-products-edit]] — cog → Edit is blocked on fulfilled lines; void the waybill first.
- [[orders-products-delete]] — cog → Remove is blocked on fulfilled physical lines; void the waybill first.
- [[orders-details-products]] — products table where the Fulfilled badge lives.
- [[orders-shipping-waybill]] — generate / void waybill (the source of `order_fulfillment_id`).

## Open questions

- Confirm whether a cross-order fulfilments listing page exists (verify).
