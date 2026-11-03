---
type: feature
nav_path: "Apps → Local Pickup (Stores) → Products (per-store stock)"
route_name: apps.stores.overview
route_path: /admin/stores
aliases: ["Per-store stock", "Local Pickup quantities", "Store products tab", "Sum the quantities in the product", "Per-store inventory"]
tags: [apps, stores, local-pickup, inventory, stock, quantity, pricing]
plan_gates: ["stores"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Local Pickup — per-store stock

## Purpose

> Part of [[apps-stores]]. See the hub for the other aspects (managing locations, shipping + payment methods).

Documents how Local Pickup tracks **stock per physical store**: each store has its own product list with quantities, an optional one-time toggle to sum those quantities back into the master product, the rule that blocks pickup when a store is out of stock, the absence of per-store pricing, and the JSON-API per-store stock surface.

## Where to find it

Sidebar → Apps → install → **Local Pickup** → open a store → **Products** tab (legacy route `/admin/stores`, reached via the `RedirectOldApp` wrapper).

## What the merchant can do here

- View the per-store **Products** tab (`products`).
- **Add a product** to a store (`products.add`).
- **Delete** a product from a store (`delete.product.confirm`: *"Are you sure you want to delete the selected product from the store?"*).
- Open the **Quantity change** modal (`quantity.modal.update`) to set stock per store. Success: *"Quantities successfully updated"* (`quantity.success.update`).
- Turn on **Sum the quantities in the product** to roll per-store quantities up into the master product quantity.

### What the merchant CANNOT do here
- Set a per-store price — pricing is product-level across all stores (see Business rules).
- Auto-recalculate the summed master quantity on every order — the sum is a one-time action (see Business rules).

## Settings & fields

### Per-store quantity

The **Quantity change** modal adds a quantity from the per-store Products tab, with two options:

- **Quantity only for product** — one row at product level (no variant).
- **Quantities for each variant** — one row per variant.

Stock per physical store is tracked in `products_quantities` rows keyed by `(shop_id, product_id, variant_id)`.

### "Sum the quantities in the product" toggle

Helper text: *"The quantities will be updated only for the products for which you have added a quantity by option."*

- **Off (default)** — per-store quantities live alongside the master quantity. The customer-facing stock is the master quantity. Local Pickup just shows the per-store breakdown.
- **On** — turning it on runs a one-time UPDATE that sets each variant's master quantity to the **sum** of its per-shop rows. Editing one is no longer independent.

## Business rules

### The sum is one-time, not continuous

When the merchant clicks save with the toggle on, the platform runs a single sync that sets each variant's master quantity to the sum of its per-shop rows (`quantity = (select sum(qty) from products_quantities where products_variants.id = products_quantities.variant_id)`). It does **not** auto-recalculate on every order; the merchant has to re-run it after re-stocks. See [[inventory-variant-model]] for how the master per-variant `quantity` drives storefront in-stock logic.

### Customer cannot order pickup if the store is out of stock

The platform checks per-store stock at the moment the customer picks Local Pickup — if the product has zero quantity in the chosen store, the checkout flow blocks the selection. There is **no** automatic switch to a different store; the customer has to choose another store or another shipping method. This is the eligibility check referenced from [[apps-stores-main-shipping-payment]].

### No multi-store visibility filter on the storefront

The storefront does **not** filter the public product list by the customer's nearest store. The customer sees every product the catalog has; the per-store check happens only when Local Pickup is chosen at checkout. There is no "show me what's in stock at store X" filter on the listing pages.

### No per-store pricing

The Stores app does not store per-location prices. A product has one price + one discount across all stores. To run a different price per location, the merchant uses another approach (separate products, [[apps-multilang]] sister stores, or [[customers-custom-groups]] for customer-group-based pricing).

### Programmatic access

Per-store stock is exposed through a SEPARATE JSON-API v2 resource — see [[api-store-quantity]] — keyed on the `(shop_id, product_id, variant_id)` triple. That resource exposes full CRUD for ERP integrations syncing per-warehouse inventory levels. The store resource itself (the physical locations) is **read-only** via the API — see [[api-stores]]. Both endpoints are app-gated. See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

- [[apps-stores]] — hub.
- [[inventory-variant-model]] — how the master per-variant `quantity` drives in-stock logic (the "Sum" toggle writes into this).
- [[inventory-tracking]] — the platform-wide inventory model.
- [[products-products]] — products linked to stores.
- [[api-store-quantity]] — JSON-API v2 per-store stock resource (full CRUD).
- [[api-stores]] — JSON-API v2 store-location resource (read-only).
- [[apps-multilang]] / [[customers-custom-groups]] — alternatives for per-location / per-group pricing.

## Open questions

None.
