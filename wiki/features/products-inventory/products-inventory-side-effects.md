---
type: feature
nav_path: "Products → Inventory → Side effects"
route_name: products_inventory
route_path: /admin/products/inventory
aliases: ["Inventory save side effects", "Inventory webhooks", "Inventory search re-index", "Inventory plan gates", "Inventory JSON-API parity"]
tags: [products, inventory, webhooks, search, plan-gates, api]
plan_gates: ["products", "multi_variants", "digital_products", "hidden_products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[products-inventory]]. See the hub for the other aspects (table, quantity editing, price editing, oversell toggle).

# Inventory — save side effects, API parity & plan gates

## Purpose

Saving a row on the Inventory screen is never just a number change — it ripples through search indexing, storefront caches, webhooks, and (selectively) admin notifications. This page documents **what fires on save**, the one notification that pointedly does NOT fire, how the same edits behave through **JSON-API v2** (and the one place they differ), and the **plan gates** that govern which SKUs the screen even shows.

## Where to find it

Sidebar → Products → **Inventory** (`/admin/products/inventory`). These effects fire on any per-row Save or bulk action (quantity, price, or selling-toggle). The programmatic equivalent is JSON-API v2 — see [[json-api-v2]].

## What the merchant can do here

Nothing additional to configure — this page explains the consequences of the edits made on the sibling aspects ([[products-inventory-quantity-editing]], [[products-inventory-price-editing]], [[products-inventory-oversell-toggle]]) and how to perform them programmatically.

## Settings & fields

There are no fields on this aspect. The relevant configuration lives elsewhere:

- `product_threshold` (low-stock level) on [[settings-cart]].
- `product_quantity_low` notification gating on [[settings-admin-notifications]].
- `product.updated` webhook subscriptions on [[settings-hooks]].
- The product-level plan gates on [[plan-gates]] / [[plan-features]].

## Business rules

### What a save fires

Each row save (price, quantity, bulk selling-toggle) dispatches a search-sync and a product-updated event keyed on the **parent product id**:

- **Search re-index** — the affected product re-indexes; quantity changes that move a SKU between in-stock / out-of-stock states are reflected on storefront search results once the queue processes. See [[background-queue-inventory]].
- **Storefront cache invalidation** — affected product and category pages flush their caches.
- **`product.updated` webhook** — dispatched for any product whose stock or price changed, so receivers subscribed via [[settings-hooks]] are notified.

The bulk-update path is keyed on item_id so each product is touched exactly **once per save batch** — not per Variant. Updating 50 Variants on the **same** product fires 1 webhook for that product; updating 50 Variants across 50 **distinct** products fires 50 webhooks.

### What a save does NOT fire — the low-stock email

The `product_quantity_low` and `product_out_of_stock` admin emails fire only on the order-decrement code paths (order placement, status change, manual quantity edit through the order edit screen). Bulk imports and bulk Update-quantities through this Inventory screen update the Variant `quantity` directly **without** invoking the threshold check — so the merchant gets no flood of emails after a bulk restock or write-down. (The `threshold` itself is configured per-product or store-wide — see [[settings-cart]] and [[settings-admin-notifications]].)

### Programmatic access via JSON-API v2 — same effects, one difference

The data this screen manages can also be read, created, updated, or deleted via **JSON-API v2** — see [[api-products]] for the product (with `tracking` / `continue_selling` flags), [[api-variants]] for per-variant `quantity` / `price`, and [[api-store-quantity]] for the multi-location stock pivot if [[apps-store-locations]] is installed.

**Same side effects apply.** A PATCH on a variant's `quantity` through JSON-API v2 fires the search-sync and the product-updated event keyed on the parent product, exactly like an inline Save here.

**One important difference**: the bulk Update-quantities action in admin clamps results to ≥ 0 (see [[products-inventory-quantity-editing]]); **JSON-API v2 does NOT clamp** — a PATCH can drive a variant into negative inventory directly (subject to the `continue_selling = yes` + `tracking = yes` gate). And as on the admin screen, the low-stock / out-of-stock emails fire only on order-decrement code paths — neither this screen NOR JSON-API v2 quantity edits trigger them.

The product change-log records `api2` as the Initiator when the change came from JSON-API v2 — useful when investigating "stock changed without my doing anything" support tickets (see [[products-change-log]]). See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

### Plan gates

The Inventory grid lists SKUs governed by the platform's product-level plan gates (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]). The grid itself is not gated, but the products it manages are:

| Mapping | Shape | What it controls |
|---|---|---|
| `products` | Numeric (max products) | Per-plan product cap. Hitting the cap blocks new product creation from [[products-products]] and from CSV / XML imports. Top-up packs via [[plan-features]]. |
| `multi_variants` | Boolean | Whether variants are available at all. Without it the merchant cannot turn ON variant rows, so the per-Variant rows the table shows can only come from a plan that allows variants. |
| `digital_products` | Boolean | Whether a product can be marked digital (file delivery). Inventory rows for digital products only exist on plans that allow them. |
| `hidden_products` | Boolean | Whether a product can be marked Hidden (B2B / catalog-only). Setting status to `hidden` returns HTTP 402 with the feature payload on plans that don't allow it. |

Hitting the `products` numeric cap surfaces the per-feature upsell modal at [[plan-features]] on new-product creation. The three boolean gates redirect to plan-upgrade panels when the merchant tries to flip the corresponding toggle on the product editor. See [[plan-vs-feature-pack]] for the pack-vs-upgrade decision.

## Related

- [[products-inventory]] — hub.
- [[json-api-v2]] — auth, rate limit, side-effects principle.
- [[api-products]] / [[api-variants]] / [[api-store-quantity]] — the programmatic equivalents.
- [[settings-hooks]] — `product.updated` webhook fires on inventory changes.
- [[settings-cart]] — `product_threshold` for low-stock notifications.
- [[settings-admin-notifications]] — gates the `product_quantity_low` notification.
- [[products-change-log]] — records `api2` as Initiator for API-driven changes.
- [[background-queue-inventory]] — the search re-index queue chain.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — the product-level plan gates.
- [[apps-store-locations]] — multi-location stock pivot.

## Open questions

None.
