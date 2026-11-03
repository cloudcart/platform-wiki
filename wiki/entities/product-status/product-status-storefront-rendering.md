---
type: entity
nav_path: "Entity → Product Status → Storefront rendering"
aliases: ["Product Status badge", "Storefront Product Status", "Per-channel Product Status", "Bulk change product status", "Real-time Status sync", "Status decrement timing"]
tags: [entity, catalog, products, statuses, storefront, customer-facing]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Product Status — Storefront rendering

> Part of [[product-status]]. See the hub for related aspects (attributes, Conditional vs Non-conditional, evaluation precedence, action behaviour, lifecycle).

## Identity

This page covers **how a resolved Product Status reaches the customer** — what renders on the product card / detail page, why the badge is store-wide (no per-channel overrides), how stock-decrement timing affects when status transitions appear, and the merchant tooling for bulk Non-conditional updates from [[products-products]].

## Aliases

- **Status badge** — the visual element rendered on the storefront.
- **Bulk change product status** — the multi-select action on [[products-products]].
- **Real-time Status sync** — the immediate re-evaluation after a stock change.

## Key Attributes

### Status sync runs in real-time

When an order changes stock, the product's status is re-evaluated immediately. The customer browsing the storefront sees the new status on the next page load — **no merchant action needed**. The stock-decrement timing is configured via [[settings-cart]]'s `order_status_for_quantity_decrease` (default `paid`).

There is no scheduled / batched status recompute; every stock-mutating event (order placement, cancellation, refund, restock import, manual adjustment from [[products-inventory]]) triggers re-evaluation against the live stock count.

### Stock decrement timing affects when statuses fire

The store setting `order_status_for_quantity_decrease` in [[settings-cart]] picks which order status triggers stock decrement (default `paid`). Conditional statuses re-evaluate based on the live stock count — so changing this setting affects WHEN status transitions appear to customers. Setting it to `pending` means stock decrements at order placement (before payment), causing the product's status to flip sooner.

See [[inventory-decrement-timing]] for the full matrix of (status × fulfillment × setting) outcomes and the merchant guidance for picking between `paid` and `pending`.

### Status badges are store-wide, NOT per-channel

The stock count drives a single Status per product regardless of channel. The storefront badge looks the same across every channel the merchant publishes to — there are no per-channel badge overrides. If a merchant runs multiple [[channel|channels]] on one store, all of them see the same badge.

### Theme controls visual styling

The storefront theme reads:

- **`name`** — rendered as text (the badge label).
- **`type`** — drives whether the Buy button shows.
- **`button_text`** — the substitute CTA label when Buy is hidden.

Visual styling (colour, icon, position on the card, font) is fully theme-controlled — there is **no per-status colour / icon field** in the data model. To restyle a badge, the merchant works in the theme editor.

### One status per product (not per variant)

The Conditional status is evaluated against the product's **aggregate stock** (sum across variants). A single status badge displays on the storefront product card / detail. To indicate per-variant stock state to customers, the merchant uses the variant picker UI itself (the theme shows greyed-out / unavailable variants based on per-variant quantity); **there is no per-variant Product Status badge**.

### Bulk-change product status (Non-conditional only)

The bulk action **"Change product status"** on [[products-products]] supports multi-product Non-conditional status updates. The merchant:

1. Selects multiple products on the products list.
2. Picks the bulk action *"Change product status"*.
3. Picks Available / Out of stock (or any Non-conditional status from the taxonomy).
4. The platform writes the new status to every selected product — populating `status_id` or `out_of_stock_id` depending on the picked status's `type`.

Conditional statuses do not need bulk-changing — they auto-apply based on stock. This bulk action is purely for forcing an override via the Non-conditional slot.

### Storefront sees the next status on next page load

Because Conditional rules evaluate against the live database stock count on every storefront query, the customer sees the updated badge on the **next page load** after the underlying stock change. There is no client-side polling — the merchant cannot make the badge update without a refresh.

For products fetched via storefront API (PWA / headless integrations), the response carries the resolved Status name + `type` at the moment of the request; downstream clients are responsible for re-fetching if they want to see updates.

### Performance: Status cache + Conditional evaluation

The full Status taxonomy is cached in-memory per request (see [[product-status-lifecycle-management]] — 24-hour TTL). On each storefront query, the platform iterates the cached Conditional table in `sorting` order against the product's stock count — no extra DB hit per product beyond fetching the cached taxonomy once.

## Where it appears

- Storefront product card — the badge renders next to / on top of the product image.
- Storefront product detail page — the badge renders next to the price; the Buy button area renders the action substitute (Request / Subscribe button) when applicable.
- Storefront category / collection / search listing pages — same badge as on the product card.
- [[products-products]] — the bulk *"Change product status"* action lives here.
- Storefront JSON API responses — carry the resolved Status name + `type`.

## Related

- [[product-status]] — hub.
- [[products-products]] — bulk *"Change product status"* operation.
- [[settings-cart]] — `order_status_for_quantity_decrease` decides when stock decrements (and therefore when statuses flip).
- [[inventory-decrement-timing]] — full timing matrix.
- [[inventory-in-stock-badge]] — concept page covering badge logic across the broader inventory model.
- [[channel]] — channels share one Status per product.
- [[settings-hooks]] — `product.updated` fires on stock changes that trigger status re-evaluation.

## Open Questions

None.
