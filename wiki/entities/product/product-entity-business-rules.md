---
type: entity
nav_path: "Entity → Product → Business rules"
aliases: ["Product business rules", "Product publish rules", "Product hidden vs draft", "Bundle auto-deactivation", "Product physically filter", "Maximum variants per product", "Maximum parameters per product"]
tags: [entity, catalog, products, rules, validation, plan-gates]
plan_gates: ["products", "bundles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product]]. See the hub for the other aspects (attributes, lifecycle, relationships, side effects and API).

# Product — Business rules

## Identity

The hard rules and edge cases that govern [[product|Product]] saves — what is required, capped, silently transformed, and what ripples to dependent records. All are server-enforced: admin, JSON-API v2, and CSV import share one validation path.

## Aliases

- **Product business rules** — the core invariants.
- **Hidden vs Draft** — the most-confused merchant distinction.
- **Bundle auto-deactivation** — the silent ripple from child-product deactivation.
- **`physically` filter alias** — a search-filter value, not a stored type.

## Key Attributes

This page covers behaviour, not fields — see [[product-entity-attributes]] for the field schema. The rules below reference those fields by name.

## Rules

### Variants own SKU, barcode, price, and quantity — not the Product

Even a "simple" product with no merchant-defined variant parameters gets exactly **one** backing variant holding SKU / barcode / price / quantity / weight / dimensions. The "Product price" on the Edit page is that variant's price. For multi-variant products, the list's **Quantity** column shows the SUM across variants, and product-level quantity editing is disabled (set per variant). SKU and barcode are always per-[[variant|Variant]], never per-Product.

### Publish requires at least one category

A product cannot be `active = yes` without `category_id` set; the save rejects the publish. Drafts can exist without a category. The Bulk Publish action on [[products-products]] detects category-less drafts in the selection and forces the merchant to pick a category in a popup before proceeding.

### Maximum 3 variant parameters per product

A product can have at most 3 variant parameters (`p1`, `p2`, `p3`) — a hard data-model cap, not a configuration. Total SKU count = product of value counts across them (e.g., 10 colors × 5 sizes × 3 materials = 150 SKUs). The picker disables adding a 4th, so there is no error message — the UI prevents the attempt. A 4th parameter injected via API is silently ignored.

### Hard cap: 500 variants per product

Beyond the 3-parameter cap, save enforces a hard **500-variant** cap per product. A product at 10 colours × 5 sizes × 10 materials = 500 SKUs is at the wall — adding an 11th colour fails with *"Maximum 500 variants exceeded"*. This is save-time validation, not just a UI hint; admin, API, and CSV import all enforce it.

### Hidden vs Draft — the key distinction merchants confuse

- **Hidden** (`is_hidden = 1`, `active = yes`): product IS published but listed nowhere on the storefront. Customers can still reach it by direct URL (e.g., from a marketing email).
- **Draft** (`active = no`): product is NOT published. Direct URL returns the storefront's 404 page.

When a customer reports "I followed the link but the product doesn't open", check **both** flags.

### Publish window: `publish_date` + `active_to` define a visibility window

A future `publish_date` keeps the product as Draft until that time, then auto-flips it Visible. An `active_to` flips it out of Visible once that time passes. Both dates use the **store's timezone**, normalised to UTC at minute precision before comparison. See [[product-entity-lifecycle]].

### Quantity tracking and oversell

- `tracking = no` → variant `quantity` is ignored; product is always in stock.
- `tracking = yes` + `continue_selling = no` → "out of stock" when `quantity = 0` (uses the `out_of_stock_id` status's label + button text).
- `tracking = yes` + `continue_selling = yes` → stays buyable even at `quantity = 0`, but variant `quantity` clamps at 0 on decrement; see [[inventory-oversell]].

See [[inventory-tracking]] for the full per-Variant model and [[inventory-decrement-timing]] for decrement timing (driven by [[settings-cart]] `order_status_for_quantity_decrease`).

### Threshold requires tracking

A low-stock `threshold` is **only allowed when `tracking = yes`**; otherwise save fails with *"Cannot have threshold if not tracked"*. Likewise `continue_selling = yes` requires `tracking = yes`. A non-tracked product cannot oversell or alert.

### URL handle changes generate 301 redirects

When the merchant edits `url_handle`, the previous handle is recorded as a redirect entry. The storefront then serves a permanent redirect from the old URL to the new one, so search engines and bookmarked links keep working. See [[seo-redirect]].

### Bundle: `individual_price` controls live vs fixed pricing

A Bundle product (`type = bundle`) uses `individual_price = yes/no`:

- `yes` → price is the **SUM of its children's current prices** (live; reacts as children change).
- `no` → the bundle has its own **fixed bundle-level price** independent of children.

A Bundle doesn't own variants in the traditional sense — see [[product-entity-relationships]] + [[inventory-bundle-stock]].

### Auto-deactivation of bundles when a child product is deactivated

When the merchant deactivates a regular product (`active` → `no`), every Bundle that includes it as a component is **silently auto-deactivated** in the same save — no confirmation dialog, and the Bundles disappear from the storefront immediately. Re-activating the product later does NOT auto-re-activate those Bundles; the merchant must toggle each Bundle's `active` back on. The reverse is intentional: Bundle deactivation does not propagate to its constituent products.

### Plan-gated count: `products` (non-bundle) vs `bundles`

- Plan-feature key `products` counts all non-bundle products.
- Plan-feature key `bundles` counts bundle-type products separately.

At the plan cap, the **+ New product** button still opens the create dialog, but save fails with a plan-upgrade prompt. Existing products keep working — only NEW additions are blocked. See [[plan-gates]].

### `physically` is a filter alias, not a stored type

The `physically` value in product-search and storefront product-showcase module filters is a **filter alias** — it expands to `type IN (simple, multiple)` (all non-digital, non-bundle products). No product is ever saved with `type = physically`; the word appears only in filter dropdowns (e.g., "Show physical products only").

### `sale` field is legacy

The `sale` field exists in the schema but is **not applied on save**. Modern sale handling routes through [[discount|Discount]] records exclusively. The merchant never sets or sees this field today.

### SEO Spinner cap frees up immediately on soft-delete

The `seo_generated_through_spinner` flag marks a product whose content the SEO Spinner app generated. Deleting such a product (soft OR hard) removes the flag with the row. The Spinner cap is computed from live products at lookup time, so it frees up **immediately** on soft-delete (the row is excluded from active queries) — no delay.

### Import provenance is preserved

Products created via importers (CSV, XML, JSON, ERP integrations) carry `app_import` + `imported = yes`. The "Imported with" filter on [[products-products]] surfaces this, letting the merchant find all products from a specific import (e.g., to reverse a bad import).

## Where it appears

- [[products-products]] — where most rules surface (validation toasts, blocked saves, popups).
- [[products-bulk-actions]] — bulk publish + the category-required popup.
- [[products-variants-matrix]] — where the 3-parameter and 500-variant caps surface.
- [[settings-cart]] — `order_status_for_quantity_decrease` + `product_threshold` settings.
- [[marketing-discounts]] — where merchants manage discounts now (replacing the legacy `sale` field).

## Related

- [[product]] — hub.
- [[product-entity-attributes]] — fields the rules validate.
- [[product-entity-lifecycle]] — state machine that publishes / unpublishes.
- [[product-entity-relationships]] — bundle child-product structure.
- [[product-entity-side-effects-and-api]] — what fires when rules pass.
- [[variant]] — the per-SKU record carrying SKU / barcode / price / quantity.
- [[bundle]] — bundle-type Product.
- [[discount]] — modern replacement for the legacy `sale` field.
- [[plan-gates]] — `products` / `bundles` count caps.
- [[seo-redirect]] — 301 redirects on URL-handle change.
- [[inventory-tracking]] / [[inventory-decrement-timing]] / [[inventory-oversell]] / [[inventory-bundle-stock]] — stock semantics.

## Open Questions

- Confirm whether the **500-variant cap** counts **all variant rows** (disabled / archived still consuming a slot) or **active variants only** (verify).
