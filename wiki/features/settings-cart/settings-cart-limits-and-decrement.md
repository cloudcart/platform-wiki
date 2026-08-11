---
type: feature
nav_path: "Settings → Cart and checkout → Order limits and stock decrement"
route_name: cart.settings
route_path: /admin/settings/cart
aliases: ["Min order amount", "Max order amount", "checkout_min_price", "checkout_max_price", "cart_max_products", "cart_max_quantity", "product_threshold", "order_status_for_quantity_decrease", "order_id_display", "order_complete", "Cart caps", "Stock decrement setting", "Order number format", "Auto-complete orders"]
tags: [settings, cart, checkout, orders, inventory, limits]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-cart]]. See the hub for the other aspects (accounts, abandoned reminder, payment/shipping defaults, checkout fields, UI behavior, Google Maps, marketing consent).

# Cart and checkout — Order limits and stock decrement

## Purpose

The box on the Cart and checkout page that controls **hard caps on cart contents**, **when stock decrements relative to the order's status**, the **low-stock email threshold**, the **order-number display format**, and the **auto-complete** behaviour for orders. This is the densest box on the page — every setting here directly affects whether a customer can complete checkout and what happens to inventory afterwards.

## Where to find it

Sidebar → Settings → **Cart and checkout** → box **Order and product quantities** (`order_quantity`).

## What the merchant can do here

- Set min/max order amount (store currency) — checkout blocked outside this range.
- Set per-customer caps: max units of a single SKU, max total cart items.
- Set a low-stock threshold that fires the `product_quantity_low` admin email.
- Pick when stock decrements: `paid` (paid + fulfilled) or `pending` (pending + fulfilled).
- Pick the order-number display: internal numeric ID or alphanumeric hash.
- Toggle auto-complete orders (skip manual mark-as-complete).

## Settings & fields

### Box: Order and product quantities (`order_quantity`)

| Field / Control | What it does | Notes |
|-----------------|--------------|-------|
| **Minimum amount for an order** (`checkout_min_price`) | Customer cannot check out below this total (store currency). | Blank = 0 (no minimum). Saved as currency (`floatval`). **No non-negative guard** — this field has **no** client `min` floor **and** no backend validation, so a **negative value can be entered in the form and saved** (see Business rules). |
| **Maximum amount of products in the cart** (`checkout_max_price`) | Hard cap on cart total. | Blank = 0 = no maximum. Form input floors at 0 (client `min: 0`), but **not** backend-validated — a negative could still be stored via the API. |
| **Maximum products quantity of a kind per customer** (`cart_max_products`) | Hard cap on quantity of a single SKU per customer. | Integer. Blank = 0 = no cap. Form floors at 0 (client `min: 0`); no backend non-negative validation. |
| **Maximum cart quantity of a kind per customer** (`cart_max_quantity`) | Hard cap on total items in the cart per customer. | Integer. Blank = 0 = no cap. Form floors at 0 (client `min: 0`); no backend non-negative validation. |
| **When the total quantity of a product decreases, send me an email** (`product_threshold`) | Low-stock alert threshold. Triggers the `product_quantity_low` admin notification when a product's stock crosses below this value. Recipient is `site_email` (see [[settings-admin-notifications]]). | Integer ≥ 1. Backend-validated (nullable, integer ≥ 0). |
| **I want to decrease product quantity when the status is** (`order_status_for_quantity_decrease`) | `paid` = stock decrements only when the order is paid AND fulfilled. `pending` = stock decrements when the order moves to pending AND fulfilled. | Affects whether oversells are possible while orders sit in the pending state. See [[inventory-decrement-timing]] for the deterministic decrement matrix. |
| **Order number** (`order_id_display`) | `id` = display the internal numeric system ID; `increment_hash` = display an alphanumeric hash that's shorter and customer-friendly. | Affects all places where order numbers appear: storefront, emails, invoices. |
| **Automatic completion of the order** (`order_complete`) | When ON, orders auto-complete (no manual "mark as complete" step in the admin). | |

## Business rules

### `paid` vs `pending` decrement timing — the most-asked operational question

The `order_status_for_quantity_decrease` setting is one of the highest-impact toggles on the whole Cart and checkout page. The two values create very different inventory behaviours:

- **`paid` (default)** — stock decrements only when the order is both **paid** and **fulfilled**. Customers who place orders that don't yet have payment do NOT block stock; two customers could race for the same last unit. Safest setting for stores where pending orders frequently abandon (e.g., Cash-on-delivery with high cancel rates).
- **`pending`** — stock decrements when the order moves to **pending** AND **fulfilled** — so the cart "reserves" stock as soon as the order is submitted, even before payment clears. Eliminates the race condition above, but ties up stock on abandoned/unpaid orders.

See [[inventory-decrement-timing]] for the full decrement matrix and merchant-guidance-per-payment-mix.

### Stock auto-restore on cancel / refund / void

When an order moves OUT of a "decrementing state" (cancelled, refunded, voided, failed, etc.), stock is **automatically returned to the variant** — a per-line tracking flag prevents double-counting. Full catalogue of triggers and edge cases: [[inventory-restock]].

### Low-stock threshold is per-variant with per-product override

The `product_threshold` field on this page is the **store-wide default**. Each individual product can override it via the per-product threshold field on the product Edit page — see [[inventory-variant-model]] for the override rules (including the `0` validation and the `tracking=no` interaction). The check fires during order placement, comparing against the resulting variant stock after the decrement. So a product with two variants where one drops below threshold and the other doesn't will trigger the low-stock notification for only the affected variant.

### Low-stock alert recipient and master gating

The `product_threshold` field defines WHEN the `product_quantity_low` admin notification fires. The recipient (the store's `site_email` from [[settings-general]]) and the master gating (`mail_product_quantity_low` + `administrator_email_notifications`) both live in [[settings-admin-notifications]] — either toggle OFF suppresses the alert at dispatch.

### Min/Max checks fire at checkout submit, not at add-to-cart

The `checkout_min_price` / `checkout_max_price` checks happen at order-submit time, not when the customer adds items to the cart. So a customer can browse a cart that violates the limits — they hit the validation error only when they try to place the order. The storefront usually surfaces this with an inline error message at the bottom of the checkout form.

### `cart_max_products` and `cart_max_quantity` are per-customer caps

These caps apply per **customer**, not per **order**. A repeat customer's accumulated history doesn't subtract from the cap — each cart-submission round starts fresh. The cap applies to the items in the current cart at submit time. Blank = 0 = no cap.

### `order_id_display` affects every customer-visible surface

Switching from `id` to `increment_hash` (or back) changes the order identifier shown to customers in: storefront order tracking, order-confirmation emails, status-change emails, invoices, and any place the merchant references the order from the customer's perspective. The internal numeric `id` is still used everywhere in the admin and in webhook payloads regardless of this setting — so the merchant and API integrations see the system ID; only the customer sees the alphanumeric hash.

### Auto-complete shortcut for fully-automated stores

`order_complete = ON` causes orders to skip the manual "mark as complete" step in the admin. Useful for fully-automated stores (digital goods, pre-fulfilled inventory, drop-ship). For stores with manual fulfillment processes, leaving this OFF keeps the order in a state where the merchant explicitly marks it complete after shipping.

### Numeric defaults on save

The save handler explicitly defaults `checkout_min_price`, `checkout_max_price`, `cart_max_products`, `cart_max_quantity`, and `product_threshold` to `0` if empty on submit. Clearing a field is equivalent to setting it to 0 (i.e., "no limit" for the first four; "no low-stock email" for the threshold). See the hub [[settings-cart]] for the cross-cutting save-handler rules.

### Non-negative validation is inconsistent (only `product_threshold` is guarded)

Only **`product_threshold`** is validated non-negative server-side (`nullable|sometimes|numeric|int|min:0`). The four order/cart caps have **no server-side non-negative validation** — the save handler only casts them (`checkout_min_price` / `checkout_max_price` via `floatval`, `cart_max_products` / `cart_max_quantity` via `intval`), which **preserve negatives**. So a value below 0 sent to those four (e.g. via the JSON-API / a crafted request) is stored as-is.

Client-side the admin form floors **`checkout_max_price`, `cart_max_products`, and `cart_max_quantity`** at 0 (input `min: 0`), so a merchant cannot type a negative there. But **`checkout_min_price` has no client `min` either** — so a **negative minimum-order amount can be entered directly in the form and saved**. Worth fixing at both layers (form `min: 0` on `checkout_min_price` + backend `min:0` validation on all four). `(verify the storefront checkout effect of a negative minimum-order amount.)`

## Related

- [[settings-cart]] — hub.
- [[inventory-tracking]] — overall stock-tracking concept.
- [[inventory-decrement-timing]] — the canonical reference for the `paid` vs `pending` decrement rule.
- [[inventory-restock]] — automatic stock return on cancel / refund / void.
- [[inventory-variant-model]] — per-product threshold override + the `tracking=no` interaction.
- [[settings-admin-notifications]] — `mail_product_quantity_low` master toggle + recipient gating.
- [[settings-general]] — `site_email` recipient + currency.
- [[settings-statuses]] — defines the order/payment statuses referenced by `order_status_for_quantity_decrease`.
- [[discount-stacking]] — discount application interacts with `checkout_min_price` / `checkout_max_price` (post-discount totals are what's compared).
- [[order]] — the order entity that carries the `id` and `increment_hash`.
- [[order-processing-pipeline]] — full status-transition pipeline that consumes `order_complete` and the decrement setting.

## Open questions

_None._
