---
type: feature
nav_path: "Suppliers → Products by orders → Suppliers app integration"
route_name: suppliers.products_by_orders
route_path: /admin/suppliers/products-by-orders
aliases: ["Products by orders suppliers column", "Cheapest supplier highlight", "Per-variant supplier", "Supplier filter quirk", "Suppliers app products by orders"]
tags: [orders, products, suppliers, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
> Part of [[orders-supplier-products]]. See the hub for the other aspects (overview, filters, aggregation, export).

# Products by orders — Suppliers app integration

## Purpose

Documents what the **Suppliers** app adds to the **Products by orders** screen — the supplier column, the supplier filter, the supplier-grouped default sort, and (most importantly) the cheapest-supplier highlight logic with its non-obvious in-stock / per-variant rules and the display-only filter quirk. The base screen is described on the hub [[orders-supplier-products]].

## Where to find it

On the **Products by orders** page (route `suppliers.products_by_orders`), the supplier features appear ONLY when the Suppliers app is installed AND active.

## What the merchant can do here

When the **Suppliers** app is installed:

- The **Supplier filter** dropdown appears (single-select of all configured suppliers).
- The **Suppliers column** appears in the table with supplier name(s) + cheapest-supplier highlight.
- The **default sort** flips to `supplier_name DESC` — products group by supplier.
- The per-product "suppliers info" template renders rich supplier metadata.

Without the app:

- The Supplier filter is hidden.
- The Suppliers column is hidden.
- Default sort is the standard product-name sort (typically `orders_products.id`).

## Settings & fields

The supplier metadata shown here comes from the per-VARIANT supplier configuration set in the product editor — each supplier row carries a `price` and an `in_stock` flag. These feed the cheapest-supplier highlight and the supplier filter. There are no settings on this page itself.

## Business rules

### Per-VARIANT supplier lookup — keyed on variant

Suppliers are assigned at the VARIANT level, not the product level — the cheapest-supplier lookup matches on `variant_id`. Different colors / sizes of the same shirt can have entirely different supplier lists. The merchant's supplier setup happens per-variant in the product editor. This matches the variant-axis grouping of the rows themselves (see [[orders-supplier-products-aggregation]]).

### "Cheapest supplier" = lowest unit price ASC

When a variant has multiple configured suppliers, the page highlights the one with the LOWEST current supplier `price` (ascending). It does NOT factor in:

- MOQ adjustments (Minimum Order Quantity discounts / uplifts).
- Currency conversion (assumes all suppliers' prices are in the same currency).
- Lead time / delivery cost.
- Bulk-tier breakpoints.

So a supplier with a high MOQ that beats a no-MOQ supplier on per-unit price will still be "cheapest" — even if the merchant won't actually order at that volume. Treat the highlight as a starting point and validate against the supplier's full terms.

### Cheapest supplier requires in-stock — out-of-stock suppliers EXCLUDED

The cheapest-supplier lookup ONLY considers supplier rows with `in_stock = 1`. So if the actually-cheapest supplier is currently out-of-stock per the supplier's own record, that supplier is HIDDEN from the cheapest-supplier highlight — even though it might be the right purchasing choice short-term. The merchant sees the cheapest IN-STOCK supplier, not the absolute cheapest. To compare full pricing including out-of-stock suppliers, the merchant drills into the product's supplier configuration directly.

### Supplier filter quirk — display-only string, NOT a SQL constraint on its own

The Supplier filter only sets the DISPLAY string (the filter chip shown in the UI). The actual scoping happens via a separate cheapest-supplier join inside the order-product list logic — computed in a different place from the chip. Two implications:

- **App uninstalled**: if the Suppliers app is uninstalled (or the cheapest-supplier join is gated off), the Supplier filter chip won't apply ANY constraint. The merchant might "filter by Supplier X" and silently see ALL products — the chip implies filtering that isn't happening.
- **In-stock coupling**: because the supplier scoping joins THROUGH the cheapest-supplier lookup (gated on `in_stock = 1`), filtering by Supplier X excludes products where Supplier X is currently out-of-stock — even if Supplier X is the only supplier on that product. The merchant filtering for "products from Supplier X" might see fewer rows than expected.

### Default sort flips with the app

With the Suppliers app installed AND no explicit grid sort, the default flips to `supplier_name DESC`. Without the app, default falls back to whatever the grid uses (typically `orders_products.id`). So the order of rows changes based on app-install state — same data, different ordering.

### Side effects

**None** — read view. The supplier highlight is a read-time computation.

## Related

- [[orders-supplier-products]] — hub.
- [[orders-supplier-products-filters]] — where the Supplier filter lives.
- [[orders-supplier-products-aggregation]] — variant-axis grouping the per-variant supplier lookup mirrors.
- [[apps]] — the Suppliers app catalogue entry.
- [[products-products]] — product editor where per-variant suppliers are configured.
- [[product]] — entity page.

## Open questions

- Exact label / location of the per-variant supplier configuration block in the current product editor `(verify)`.
