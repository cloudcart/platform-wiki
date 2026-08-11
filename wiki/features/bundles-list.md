---
type: feature
nav_path: "Products → Bundles"
route_name: bundles-list.new
route_path: /admin/products/bundles-new
aliases: ["Bundles", "Product Bundles", "Bundle list", "Kit products", "Бундли"]
tags: [apps, administration, products, bundles, cross-sell]
plan_gates: ["bundles", "hidden_products"]
created: 2026-05-22
updated: 2026-06-10
source_count: 9
---
# Bundles (product bundles)

## Purpose

**Product Bundles** — an apps integration that lets the merchant sell **multiple products as a single SKU at a bundled price** (typically discounted vs the sum of individual prices). The bundle has its own listing page, image and price, but its stock is drawn from the constituent products' inventory.

Merchants use bundles for:
- **Combos**: "Camera + lens + bag" for 10% off vs individual purchase.
- **Bundles with a free item**: "Buy laptop + get free mouse".
- **Kit sales**: "Beginner skateboarding kit" (board + helmet + pads).
- **Subscription boxes**: curated product collections.

A bundle is itself a Product (`type = bundle`) under the hood — its row lives in the same catalogue as regular products, linked to the constituent products via per-item rows. So bundles fire the same save / search-index / webhook hooks as ordinary products. The entity model is documented separately under [[bundle]]; this cluster covers the **admin screen** the merchant uses to manage bundle definitions.

When the Bundles app is installed, the platform adds a top-level entry under Products → Bundles. See [[apps-bundles-overview-new]] for the app landing page and [[apps-bundles-settings-new]] for the app's configuration screen.

## Where to find it

Sidebar → Products → **Bundles** (when the Bundles app is installed). Sub-pages:

| Sub-page | Route | Path |
|----------|-------|------|
| Bundles list | `bundles-list.new` | `/admin/products/bundles-new` |
| Add bundle | `bundles-add.new` | `/admin/products/bundles-new/add` |
| Edit bundle | `bundles-edit.new` | `/admin/products/bundles-new/edit/:id` |

## What the merchant can do here

- See all defined bundles in a paginated table.
- Click **+ Add bundle** to create a bundle (name, image, price/discount, included products, per-item overrides).
- Edit / delete / duplicate existing bundles.
- Publish / unpublish bundles (set `active`), individually or via bulk-select.

The detailed mechanics live in the four aspect pages below.

### What the merchant CANNOT do here

- Generate bundles automatically from product associations (manual setup only).
- Set per-customer-group bundle pricing (single price per bundle).
- Maintain an independent "bundle stock" count — stock is always derived from the constituents (see [[bundles-list-stock]]).

## Settings & fields

The Bundles app installs under app-key `bundles` and creates the `bundles`, `bundle_products`, and `bundle_images` tables. The per-item configuration (qty, optional, individual price, visibility toggles, title/description overrides) lives on the per-item rows — see [[bundles-list-creation]] for the full field catalogue.

## Business rules

The substance of this feature is split across four aspect pages. Read the one that matches the question rather than all four.

## Sub-pages (in this cluster)

- [[bundles-list-creation]] — list view, the Add/Edit form, per-item override fields, time-window scheduling, bulk actions, and the server-side validation rules.
- [[bundles-list-pricing]] — the two pricing modes (`price` fixed vs `percent` discount), the fixed-price-blocked-on-variants rule, and the auto-derived `individual_price` total.
- [[bundles-list-stock]] — how bundle availability is derived from constituents (MIN of tracked stock), the skipped "Out of stock" overlay, max-buy-quantity cap, and cart cleanup on delete.
- [[bundles-list-plan-gates]] — the `bundles` app-install + numeric cap, the `hidden_products` boolean gate, storefront sync events, and exclusion from banner/label auto-population.

## Related

- [[apps]] — App Store.
- [[apps-bundles-overview-new]] — Bundles app landing page.
- [[apps-bundles-settings-new]] — Bundles app settings.
- [[bundle]] — the bundle entity model.
- [[products-products]] — constituent products + shared product validation.
- [[products-categories]] — bundles may be categorised.
- [[marketing-discounts]] — alternative way to give "buy X get Y discount" without creating a bundle.
- [[products-smart-collections]] — alternative grouping concept (collection vs bundle).
- [[products-inventory]] — constituent product stock drives bundle availability.
- [[inventory-bundle-stock]] — the inventory-side concept page for bundle stock derivation.

## Open questions

None — substantive content distributed to the four aspect pages.
