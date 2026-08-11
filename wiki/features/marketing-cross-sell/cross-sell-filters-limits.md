---
type: feature
nav_path: "Marketing → Cross-Sell & UpSell → Filters & limits"
route_name: admin.cross_sell.diagram
route_path: /admin/marketing-new/cross-sell/diagram/{id?}
aliases: ["Cross-Sell hide filters", "Cross-Sell hide cart products", "Cross-Sell hide out of stock", "Cross-Sell products limit", "Cross-Sell max user views", "Cross-Sell product settings"]
tags: [marketing, cross-sell, filters, limits, product-settings]
plan_gates: ["cross_sells"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[marketing-cross-sell]]. See the hub for the other aspects (offer form, trigger events, display modes & discounts, view tracking, engine comparison).

# Cross-Sell — filters & limits

## Purpose

These settings shape **which** products from the offer's action set actually appear, **how many** show, and **how often** a customer sees the offer. They live in **Box 5 — Product settings** of the [[cross-sell-offer-form]] (plus the `products_limit` field from Box 4). They're the merchant's tools against suggesting irrelevant products and against popup fatigue.

## Where to find it

Open a Cross-Sell offer → the **Product settings** box holds the hide filters + max-views cap; the **Products limit** dropdown sits in Box 4 (Action conditions). Both reached via the diagram side-panel (see [[cross-sell-offer-form]]).

## What the merchant can do here

### Hide filters (Box 5)

- **Hide out of stock** switch (`cross_sell[hide_out_of_stock]`) — don't suggest products that are out of stock.
- **Hide cart products** switch (`cross_sell[hide_cart_products]`) — don't suggest products already in the cart.
- (`hide_viewed` — "don't re-suggest products the customer already viewed" — is commented out in the current template and **not exposed** to merchants.)

### Max user views (Box 5)

- **Max user views** (`cross_sell[max_user_views]`, integer min 0) — caps how many times one customer sees this offer. **`0` = unlimited** (see Business rules), NOT zero views.

### Products limit (Box 4)

- **Products limit** dropdown (`cross_sell[products_limit]`) — how many offered products to show in one popup. Values **1 through 10**.

## Settings & fields

| Field | Key | Notes |
|---|---|---|
| Hide out of stock | `cross_sell[hide_out_of_stock]` | filters out-of-stock at render |
| Hide cart products | `cross_sell[hide_cart_products]` | `NOT IN` against current cart items |
| Max user views | `cross_sell[max_user_views]` | integer min 0; `0`/blank = unlimited |
| Products limit | `cross_sell[products_limit]` | integer 1-10, server-validated |

## Business rules

### Hide filters apply per page-load

Both hide filters are evaluated **at render time**, so the offered set adapts dynamically as the customer's cart changes:
- **`hide_cart_products`** — when ON, products already in the cart are filtered OUT of the suggested set via a SQL `NOT IN` against the current cart's items.
- **`hide_out_of_stock`** — when ON, out-of-stock products are filtered out at evaluation time.

### `products_limit` is hard-capped at 10 — no merchant override

The "Products limit" field is validated server-side as an integer **1-10**. The merchant cannot show more than 10 offered products in one popup, regardless of plan tier.

### `max_user_views = 0` means unlimited (NOT zero)

Setting Max user views to `0` is interpreted as **"no limit"** — the popup keeps firing for that customer for the lifetime of the view cookie. Validation enforces `integer|min:0`; blank or non-numeric values are persisted as `null` (same effect — unlimited). The view-cap enforcement mechanism (the cookie) is documented on [[cross-sell-view-tracking]].

### Auto-add display type force-locks both hide filters

When the merchant picks **Add matched to cart** as the display type (see [[cross-sell-display-discounts]]), the saving hook silently sets `hide_out_of_stock = 1` and `hide_cart_products = 1` regardless of what the merchant ticked — to prevent auto-adding an out-of-stock or already-in-cart product, which would break the cart flow.

### `hide_viewed` is not available

The third hide filter (`hide_viewed`) is commented out in the current template. Merchants cannot suppress products the customer already viewed.

## Related

- [[marketing-cross-sell]] — hub.
- [[cross-sell-offer-form]] — the form; Box 5 hosts the hide filters + max views.
- [[cross-sell-display-discounts]] — the auto-add display type that force-locks the hide filters; the `products_limit` field sits in its Box 4.
- [[cross-sell-view-tracking]] — how the `max_user_views` cap is enforced (cookie).
- [[inventory-in-stock-badge]] — the out-of-stock state that `hide_out_of_stock` reads against.

## Open questions

No outstanding questions.
