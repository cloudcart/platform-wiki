---
type: feature
nav_path: "Products"
route_name: products
route_path: /admin/products
aliases: []
tags: [products, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# Products

## Purpose

Hub page for the **Products** area of the CloudCart admin panel. Lists the screens that live under this section.

## Where to find it

Products (top-level sidebar entry).

## What the merchant can do here

- Navigate to any sub-screen listed in `## Related`.

## Settings & fields

Not applicable — this is a navigation hub, not a screen with its own settings.

## Business rules

### Permission

All Products endpoints are gated by `hasApiPermission:products,products.*` — moderators need either the broad **Products** permission OR a granular child permission from [[settings-staff]]. The child permissions in the platform's permission tree are:

- `products.products` — main products list / CRUD.
- `products.categories` — Categories sub-screen.
- `products.vendors` — Vendors sub-screen.
- `products.selections` — Smart Collections.
- `products.inventory` — Inventory adjustments.
- `products.statuses` — Product Statuses.
- `products.variants` — Variants management.
- `products.properties` — Category Properties.
- `products.parameters` — Parameter values.
- `products.banners` — Banners (sliders).
- `products.labels` — Labels.
- `products.bundles` — Product Bundles.
- `products.favorite-products` — Favorite products.
- `products.missing-products` — Expected (missing) products.
- `products.options` — Product Options app.

Owners always pass. Moderators with only the broad `products` grant can access every sub-screen; granting only a specific child (e.g., `products.categories`) restricts the moderator to that sub-screen plus the hub.

## How it works (verified against backend)

### Bundles are NOT counted against the products plan quota

The store's "products used / max" count excludes products of type "bundle". Plan-quota math counts catalog products only (simple, multi-variant, digital). Bundles have their own separate plan quota — a merchant who maxes the products quota can still create bundles if their bundle quota has headroom.

### "Imported with" filter values are import-source identifiers, not free-text labels

Each import flow stamps a fixed identifier on the products it creates (e.g., `csv`, `brandsdistribution-<batch>`, `versus`, `olx`, `etsy`, `gensoft`, `microinvest`, `workflow`, `colibri`, `also`, `it4profit`, `polycomp`, `xml-import-<id>`, `duplicate_product-<source_id>`). The Imported With filter pulls from these stamped values. Bulk-duplicated products carry `duplicate_product-<source-id>` — useful to find or reverse a bulk duplication.

## Related

- [[products-products]] — the actual Products list / editor screen the merchant works on.
- [[products-categories]] — manage the category tree that products are filed under.
- [[products-vendors]] — manage product vendors / brands and assign them to products.
- [[products-variants-options]] — define variant parameters (colour, size, etc.) that produce per-SKU variants.
- [[products-options-overview]] — per-product custom Options the customer picks at the cart row (without producing extra SKUs).
- [[products-property]] — define product properties used for filters and structured-data SEO.
- [[products-inventory]] — stock tracking, low-stock thresholds, and bulk inventory edits.
- [[products-statuses]] — merchant-defined custom statuses for products (active / archive / promo / etc.).
- [[product-visibility]] — the "why isn't my product showing?" checklist (active / draft / hidden / publish-window / stock / geo / category / index-sync).
- [[products-banners-labels]] — image and text labels overlaid on product cards on the storefront.
- [[products-favorite-products]] — analytics of which products customers have added to their wishlist.
- [[products-missing-product]] — back-in-stock subscriber list per product.
- [[products-smart-collections]] — rule-based product collections that populate automatically as catalog changes.
- [[bundles-list]] — the bundles list (a different product type — multiple SKUs sold as one unit).
- [[apps-bundles-overview-new]] — bundles app overview screen for managing bundle products.
- [[apps-bundles-settings-new]] — bundles app settings (pricing model, stock model, display rules).
- [[apps-product-options-settings-new]] — product-options app settings (option types, validation, display).
- [[background-queue-inventory]] — catalogue of all background processes; covers the async CSV / XML / ERP product-import jobs, image-pipeline jobs (fetch from URL, color detection, variant-image generation), and the daily "New" / "Featured" badge cleanup jobs.

**Concepts (the models behind these screens):**

- [[variants-model]] — the Parameter / Option / Variant data model behind multi-variant products.
- [[inventory-tracking]] — the stock model: tracking flag, thresholds, decrement timing, restock, oversell.
- [[import-pipeline]] — how products load in bulk from CSV / XML / ERP feeds (the "Imported with" provenance).
- [[digital-products]] — the `digital` product type (downloadable, no shipping, auto-fulfill on paid).
- [[product-compatibility]] — product fitment / compatibility (brand-model) relationships.
- [[seo-handling]] — per-product meta / canonical / structured-data SEO.

## Open questions

(none — sidebar entry label is "Products", verified against the platform's sidebar translation `sidebar.products`.)
