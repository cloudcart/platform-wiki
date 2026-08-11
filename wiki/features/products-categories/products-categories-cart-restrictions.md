---
type: feature
nav_path: "Products → Categories → Cart & checkout restrictions"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Per-category payment restrictions", "Per-category shipping restrictions", "Define custom payment methods", "Define custom shipping methods", "Technological delivery time", "make_interval", "Категория — методи на плащане", "Категория — методи на доставка"]
tags: [products, categories, taxonomy, cart, payment, shipping, checkout]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, edit modal, hierarchy rules, SEO/taxonomy, deletion rules, JSON-API/validation).

# Categories — Cart & checkout restrictions

## Purpose

The per-category overrides that change what the customer sees at checkout when their cart contains a product from a restricted category — specifically **which payment methods are offered**, **which shipping methods are offered**, and **how much production lead time (`make_interval`) the storefront's delivery-date picker must respect**. These are the most consequential merchant-facing rules on the Categories screen: a single toggle on the wrong category can show *"no payment methods available"* at checkout. They overlay the store-wide defaults from [[settings-cart]].

## Where to find it

Sidebar → Products → **Categories** → +Add category (or Edit on any row) → **Cart and checkout rules** section in the Add / Edit modal.

The lead-time field (Technological delivery time) is visible only when the store's `enabled_delivery_time` flag is on (a platform feature, not configurable from this page).

## What the merchant can do here

- Turn on **Define custom payment methods for this category** and pick which payment methods are allowed when the cart contains a product from this category.
- Turn on **Define custom shipping methods for this category** and pick which shipping methods are allowed.
- Set **Technological delivery time in hours** for products in this category — the customer-facing delivery-date picker at checkout will not offer dates earlier than `now + make_interval`.
- Leave both toggles OFF → all installed methods work for products in this category (the default).

### What the merchant CANNOT do here
- Define **per-product** payment or shipping restrictions from this screen (those live on the product itself; see [[products-products]]).
- Order the methods within the restriction list (the customer sees them in the order configured under [[settings-payment-providers]] / [[shipping]]).
- Conditionally apply restrictions (e.g., "only on orders over X" — that's a discount / cart-rule pattern via [[apps-cart-rules]]).

## Settings & fields

| Field | Backing field | What it does |
|-------|---------------|--------------|
| **Define custom payment methods** | `all_payment` (`0` = restricted, `1` = all) | Toggle. When ON (= `0`), only the picked methods are offered for orders touching this category. |
| **Payment methods** (when toggle is ON) | `payment` (array of provider IDs) | Multi-select from installed providers at [[settings-payment-providers]]. Required when `all_payment = 0`. |
| **Define custom shipping methods** | `all_shipping` (`0` = restricted, `1` = all) | Toggle. Same pattern as payment. |
| **Shipping methods** (when toggle is ON) | `shipping` (array of provider IDs) | Multi-select from installed providers at [[shipping]]. Required when `all_shipping = 0`. |
| **Technological delivery time** | `make_interval` (integer hours) | Hours of production lead time. Visible only with `enabled_delivery_time`. Required (min 0) when the [[apps-shipping-hours]] app is installed. |

### Modal warning shown when either restriction toggle is ON

The Cart-rules section displays this exact wording when payment or shipping restrictions are enabled:

> *"If you set a restriction to this category by payment method, and if a customer has at least one product from this category in his cart, the system will provide him with only the selected payment method option."*

The same wording is shown for shipping.

## Business rules

### Cart-restriction logic — AND-combined across cart products (the intersection)

The platform's rule for a customer's cart:

- A category with `Define custom payment methods = ON` and 3 selected methods means **for any order containing at least one product from this category, only those 3 payment methods are offered at checkout**.
- If the customer's cart contains products from **two** categories that both have restrictions, the **intersection** of the two sets is offered.
- If the intersection is empty, the customer is told no payment methods are available and the order cannot be completed.
- Same logic for shipping methods.

**Practical merchant pitfall**: defining restrictions on multiple categories can produce an empty intersection. Customers see *"no payment methods available"* at checkout for orders with products from incompatible categories. The merchant must coordinate restrictions carefully — OR keep restrictions on a single *"special"* category.

### Restrictions overlay the store-wide defaults

The store-wide list of installed payment / shipping methods is configured under [[settings-payment-providers]] and [[shipping]]. The per-category restriction can only **subtract** from that set — it cannot add a method that isn't installed at the store level.

### `make_interval` drives the checkout delivery-date picker

When products in a category have `make_interval > 0`, the customer's earliest delivery slot is pushed beyond the **maximum** `make_interval` of all cart products. This is the **build-to-order / custom-cut lead-time hook** used by [[apps-shipping-hours]]. With multiple cart products from different categories, the largest `make_interval` wins.

### `make_interval` is required when the Shipping Hours app is installed

When the [[apps-shipping-hours]] app is installed, the server-side validation on category save adds:

- `make_interval` — **required**, integer, min 0.

Without the app, the field is not validated and the platform treats a missing value as 0 (verify).

### Cart cache flushed on save

Saving cart-restriction changes triggers an immediate customer-cart cache flush so the next storefront request applies the new rules. Search re-index is also fired (see [[products-categories-edit-modal]]).

### Same logic on the JSON-API v2 path

PATCH through [[api-categories]] applies the same AND-combine intersection logic on the storefront — there is no per-actor bypass. Validation messages mirror the admin form; see [[products-categories-api-validation]].

### Permission

Editing the cart-rules section requires the products / categories permission.

## Related

- [[products-categories]] — hub.
- [[products-categories-edit-modal]] — where the toggles live.
- [[products-categories-api-validation]] — the validation rules that the modal enforces server-side.
- [[settings-payment-providers]] — installed payment providers picked from.
- [[shipping]] — installed shipping providers picked from.
- [[settings-cart]] — store-wide cart and checkout settings the restrictions overlay.
- [[apps-shipping-hours]] — consumes `make_interval` to push delivery slots; required for the field's validation.
- [[apps-cart-rules]] — pattern-based alternative for conditional checkout behaviour.

## Open questions

- Default value used when `make_interval` is null and the Shipping Hours app is not installed — assume `0`, but verify against the storefront-side picker behaviour.
- Whether the "no payment methods available" customer-facing message is configurable or fixed — verify.
