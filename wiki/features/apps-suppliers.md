---
type: feature
nav_path: "Apps → Suppliers"
route_name: apps.suppliers.overview
route_path: /admin/apps/suppliers/overview
aliases: ["Suppliers", "Supplier management", "Wholesale suppliers", "Dropshipping suppliers", "Доставчици", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, suppliers, inventory, purchasing]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 1
---
# Suppliers (supplier management)

## Purpose

**Suppliers** integration — adds **supplier tracking** to products. Each product can be linked to one or more suppliers (with per-supplier price, lead time, MOQ, etc.). Used by merchants who:

- Buy products from multiple suppliers and want to track per-supplier costs.
- Run drop-shipping (orders trigger purchase from the supplier, who ships directly).
- Need purchase-order workflows (generate POs from sales data).
- Want to compare supplier prices for the same SKU.

When installed, the platform adds Suppliers UI to the products module + exposes the [[orders-supplier-products]] cross-order view for aggregating demand by supplier.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → Apps → install → **Suppliers**. See [[apps-suppliers]] hub + sub-pages.

## What the merchant can do here

- Manage supplier list ([[apps-suppliers-overview]]).
- Map products to suppliers ([[apps-suppliers-supplier-products]]).
- Per supplier: name, contact info, default lead time, payment terms.
- Per product-supplier link: supplier price, supplier SKU, lead time override, MOQ (minimum order quantity).
- Configure the "cheapest supplier" selector (which supplier is preferred when multiple match).

### What the merchant CANNOT do here
- Generate purchase orders directly (verify — may be a separate workflow OR external).
- Auto-pull stock levels from supplier APIs (depends on supplier; some apps like XmlSync handle that).

## Settings & fields

Manager exposes:
- `appInfo` — App Store metadata.
- `getMigrationsPath` — DB migrations for supplier tables.
- Per-product helper: renders `product_suppliers_in_edit_form` view on product editor showing mapped suppliers grouped by supplier_id.

The integration creates `supplier_products` table linking products to suppliers with per-link attributes.

## Business rules

### One-to-many product-to-supplier

A single product can have MULTIPLE suppliers (e.g., the merchant sources the same iPhone case from 3 different wholesalers at different prices). The product editor shows all linked suppliers, grouped by supplier_id.

### Cheapest-supplier highlighting

In [[orders-supplier-products]] (cross-order aggregated view) the platform highlights the cheapest supplier per product — driving purchase-order decisions.

### Order-line supplier attribution

When orders contain products with suppliers configured, the platform tracks which supplier "owns" each line — useful for:
- Calculating COGS (cost of goods sold) per order.
- Splitting fulfillment requests (when different suppliers ship different items).
- Reporting profitability per supplier.

### Side effects on install

Creates supplier tables, adds Suppliers sidebar entry, exposes Suppliers filter on [[orders]] list + [[orders-supplier-products]] page.

### Permission

Standard apps permission scope + suppliers-specific moderator grants (verify in [[settings-staff]]).

## Related

- [[fulfillment-and-warehouse]] — fulfillment & warehouse hub.
- [[apps]] — App Store.
- [[apps-suppliers-overview]] — supplier hub.
- [[apps-suppliers-supplier-products]] — product-to-supplier mapping.
- [[products-products]] — products gain a Suppliers section in the editor.
- [[orders]] — Suppliers filter on the orders list.
- [[orders-supplier-products]] — cross-order aggregation by supplier.
- [[apps-xml-sync]] / [[apps-xml-import]] — automated supplier feed import.
- [[apps-drop-shipping]] — drop-shipping workflow.

## How it works (verified against backend)

### Supplier model: minimal 3-field core

A supplier record holds just `name`, `email`, `phone`. That's it for the supplier record itself.

Plus an `address` relation (separate full-address record) and `records` + `products` relations.

No created/updated timestamps on supplier records.

### SupplierProducts: the many-to-many link table

Each link carries `supplier_id`, `product_id`, `variant_id`, `price`, `price_type`, `in_stock`, `identifier`.

Per-link fields explained:
- `supplier_id` + `product_id` + `variant_id` — the relationship triple. **Each supplier can have a per-variant mapping**, not just per-product.
- `price` — the cost from this supplier.
- `price_type` — likely the pricing model (fixed / percentage / variable — verify exact enum values).
- `in_stock` — supplier's current stock for this variant.
- `identifier` — the supplier's internal SKU/code for the variant (may differ from CloudCart SKU).

So per-product MOQ / lead-time fields are NOT in the simple model — those would be on a different table or extended later.

Supplier-product links also don't track created/updated timestamps.

### Per-product display module

The product editor includes a suppliers section that renders all supplier mappings for the product, GROUPED BY supplier.

So if a product has 3 variants and each maps to the same supplier, the editor shows the supplier ONCE (not three times). The merchant can drill in to see per-variant details.

### price_type values: common vs multiple

Per the API code, `price_type` accepts two values:

- **`common`** — one cost across all variants of the product (the form shows a single price input — the **Common price** option).
- **`multiple`** — per-variant cost (the form shows one price input per variant — the **Multiple prices** option).

No "percent" / "dynamic" type exists, no pricing tier per quantity, no MOQ field. Cost is a flat value per supplier-variant pairing.

### What the app is and isn't

The Suppliers app is a **catalog of suppliers + per-variant cost record**. The shipped feature set is:

- A list of suppliers (name, email, phone, optional address).
- A `(supplier, product, variant)` mapping with the supplier's price, supplier's identifier (their SKU), and an in-stock flag.
- A grouping on the product editor that lets the merchant see which suppliers cover the product.
- Filtering on the orders list by supplier.
- The cross-order [[orders-supplier-products]] aggregation view that highlights the cheapest supplier per product.

It is **not** any of these:

- A purchase-order generator — there is no PO creation, no PO emailing, no PO status tracking inside this app.
- A drop-shipping router — when an order contains products from supplier X, the platform does not automatically send anything to X. The merchant exports the supplier-products view manually (CSV format `Supplier → identifier → price` per the `csv_export_suppliers` translation) and forwards it.
- A supplier-portal login — suppliers have no account to view orders or update stock on their end. The `in_stock` flag is set manually by the merchant inside CloudCart.
- A lead-time tracker — the `supplier_products` table has no `lead_time` / `MOQ` / `incoterms` columns. Customer-facing "ships in X days" promises do not come from the supplier record.

### Multi-warehouse interaction

The supplier `in_stock` flag is independent of [[apps-store-locations]] warehouse stock. The Suppliers app does not write to per-location stock — it just records "this supplier has the variant available". Per-location stock comes from the Stores / Store Locations apps. The merchant uses the supplier list to plan a re-stock then enters the new stock into the warehouse manually.

### How the per-product module renders

When the Suppliers app is installed, the product editor calls `renderProductSuppliersInEditForm($product_id)`. That module queries `supplier_products` for the product, groups the rows by `supplier_id`, and shows each supplier once with their email/phone and a *"Change settings"* link that drills into per-variant prices and identifiers. The module does not appear when the app is uninstalled.

### In-stock toggle is per (supplier × product)

The "in stock" toggle on each (supplier × product) pairing is a yes/no — toggling it off marks the merchant's supplier as out-of-stock for that product, but does not change the storefront's stock. It is informational, used to plan re-orders.

## Open questions

