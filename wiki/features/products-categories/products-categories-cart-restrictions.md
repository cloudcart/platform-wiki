---
type: feature
nav_path: "Products → Categories → Cart & checkout restrictions"
route_name: categories.settings
route_path: /admin/products/categories
aliases: ["Per-category payment restrictions", "Per-category shipping restrictions", "Define custom payment methods", "Define custom shipping methods", "Technological delivery time", "make_interval", "Категория — методи на плащане", "Категория — методи на доставка", "Restriction inheritance to subcategories", "Main vs additional category restrictions"]
tags: [products, categories, taxonomy, cart, payment, shipping, checkout]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[products-categories]]. See the hub for the other aspects (list & organize, edit modal, hierarchy rules, SEO/taxonomy, deletion rules, JSON-API/validation).

# Categories — Cart & checkout restrictions

## Purpose

The per-category overrides that change what the customer sees at checkout when their cart contains a product from a restricted category — specifically **which payment methods are offered**, **which shipping methods are offered**, and **how much production lead time (`make_interval`) the storefront's delivery-date picker must respect**. A single toggle on the wrong category can leave checkout with no payment method.

## Where to find it

Sidebar → Products → **Categories** → +Add category (or Edit on any row) → **Cart and checkout rules** section in the Add / Edit modal.

The lead-time field (Technological delivery time) is visible only when the store's `enabled_delivery_time` flag is on (a platform feature, not configurable from this page).

## What the merchant can do here

- Turn on **Define custom payment methods for this category** and pick which payment methods are allowed when the cart contains a product from this category.
- Turn on **Define custom shipping methods for this category** and pick which shipping methods are allowed.
- Set **Technological delivery time in hours** for products in this category — the customer-facing delivery-date picker at checkout will not offer dates earlier than `now + make_interval`.
- Leave both toggles OFF → all installed methods work for products in this category (the default).

### What the merchant CANNOT do here
- Define **per-product** payment or shipping restrictions — they do not exist anywhere. A product follows its **main category**'s restriction; to restrict one product, move it to a category of its own.
- Order the methods within the restriction list (the customer sees them in the order configured under [[settings-payment-providers]] / [[shipping]]).
- Conditionally apply restrictions (e.g., "only on orders over X"). Payment methods have their own order-amount limits; [[apps-cart-rules|Cart Rules]] only discount and never hide a method.

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

**Pitfall**: restrictions on several categories can intersect to nothing; coordinate them, or keep restrictions on a single *"special"* category.

### Only the product's main category counts, with no inheritance

- **Main (primary) category only.** Each cart product is checked against the restriction of its **main category**. Its **additional categories** are ignored, restricted or not.
- **No inheritance.** A restriction on a parent category does not reach its subcategories: a product whose main category is a subcategory follows that subcategory's own setting (none means all methods). To restrict a branch, set it on each subcategory that is a main category.
- **Where it applies:** only the payment and shipping lists of the storefront checkout (headless storefronts included). The **Fast Order** app's form always places a **cash on delivery** order and does not check category restrictions; orders created in the admin or through the API are not checked either.
- **Checked when the list is built.** The final submit re-checks the payment method against the apps' rules only, not the category restriction.

### Restrictions overlay the store-wide defaults

The store-wide list of installed payment / shipping methods is configured under [[settings-payment-providers]] and [[shipping]]. The per-category restriction can only **subtract** from that set — it cannot add a method that isn't installed at the store level.

### `make_interval` drives the checkout delivery-date picker

With `make_interval > 0`, the earliest delivery slot is pushed past the **largest** `make_interval` among the cart's products (the lead-time hook of [[apps-shipping-hours]]).

### `make_interval` is required when the Shipping Hours app is installed

When the [[apps-shipping-hours]] app is installed, the server-side validation on category save adds:

- `make_interval` — **required**, integer, min 0.

Without the app, the field is not validated and the platform treats a missing value as 0 (verify).

### Cart cache flushed on save

Saving cart-restriction changes triggers an immediate customer-cart cache flush so the next storefront request applies the new rules. Search re-index is also fired (see [[products-categories-edit-modal]]).

### Same logic on the JSON-API v2 path

Restrictions saved through [[api-categories]] work the same; validation mirrors the admin form ([[products-categories-api-validation]]).

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
