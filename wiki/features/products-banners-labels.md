---
type: feature
nav_path: "Products → Banners Labels"
route_name: product-banners.list
route_path: /admin/products/banners-labels
aliases: ["Banners and labels", "Product banners", "Product labels", "Image labels", "Text labels", "Банери", "Етикети"]
tags: [marketing, products, banners-labels]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 10
---
# Banners & Labels

## Purpose

The screen where the merchant creates **visual badges that appear on product cards** to attract attention — for example "Sale", "New", "Free shipping", or a custom holiday-themed image overlay. The page hosts two sibling badge types under one screen:

- **Banners** (image labels) — a small image overlay placed in a corner of the product card / detail page. Used for promo images, holiday badges, branded callouts.
- **Labels** (text labels) — a coloured text pill (e.g., "SALE", "BESTSELLER", "-20%") with custom background and text colour. Used for short text callouts.

Both share the same **target / condition system** — the merchant defines who the badge applies to and the platform auto-attaches the badge to every matching product. This page is the hub; the mechanics live in the three sub-pages below.

## Where to find it

Sidebar → Products → **Banners Labels** (or "Product banners" / "Product labels" — translation varies).

The page is a TAB CONTAINER with two tabs:

- **Product Banners** (default tab, route `product-banners.list`).
- **Text Labels list** (route `product-labels.list`).

The top-right "Create new" button opens a modal that asks the merchant to choose **Image label** (Banner) or **Text label** (Label). The full route table is on [[products-banners-labels-fields]].

## Sub-pages (in this cluster)

- [[products-banners-labels-fields]] — the create / edit forms for banners (image) vs labels (text): fields, positions, hex-colour + date validation, sub-screen routes.
- [[products-banners-labels-targeting]] — the conditions / record-type system (category / vendor / product / selection / discount / tag), auto-population on save, `ProductSaved` re-sync, bundle / draft / inactive exclusions, smart-collection sync.
- [[products-banners-labels-scheduling]] — storefront visibility scope (`status` + `active_from` + `active_to`), daily auto-disable on expiry, `products_banners` plan gate, staff permissions, delete cleanup.

## What the merchant can do here

On the list (both banners and labels):

- See all defined banners / labels in a paginated table with columns: **ID**, **Name**, **Active from**, **Active to**, **Products** (count of matched products), **Status** (toggle).
- Per-row toggle active / inactive, Edit, Delete.
- Filter by Active-from / Active-to dates, Status, Has-products, specific Product.
- Bulk actions: set status Active, set status Inactive, Delete.

Creating, editing, targeting and scheduling badges is documented on the three sub-pages. What the merchant **cannot** do: animate / use video banners (image-only), preview before saving, set per-language or per-**variant** badges (it's product-level — see [[products-banners-labels-fields]]), or add more than 2 condition rows (see [[products-banners-labels-targeting]]).

## Settings & fields

The badge definition splits across the three aspects:

| Aspect | Key fields / settings |
|--------|------------------------|
| [[products-banners-labels-fields]] | `name`, `description`, `image` (banner), `color` / `text_color` (label), `position` (`tl` / `tr` / `bl` / `br`) |
| [[products-banners-labels-targeting]] | `record_type` conditions (1-2 rows) + the auto-maintained product junction |
| [[products-banners-labels-scheduling]] | `status`, `active_from`, `active_to`, `products_banners` plan gate |

## Business rules

The detailed, backend-verified rules live on the sub-pages. In brief:

- **Auto-population** — saving a badge matches products by conditions, not by manual pick; `ProductSaved` re-syncs on every product edit. See [[products-banners-labels-targeting]].
- **Exclusions** — bundles, draft and inactive products are skipped by auto-population. See [[products-banners-labels-targeting]].
- **Visibility scope** — a badge shows only when `status = 1` AND `active_from` ≤ today AND `active_to` ≥ today, in the store timezone. See [[products-banners-labels-scheduling]].
- **Auto-disable** — a daily 02:00 UTC job deactivates badges more than 6 hours past `active_to`. See [[products-banners-labels-scheduling]].
- **Validation** — labels enforce `#RRGGBB` hex colours; `active_to` must be ≥ `active_from`. See [[products-banners-labels-fields]].
- **Plan + permissions** — new banners need the `products_banners` plan feature; sidebar visibility needs `products` + `products.banners` (or `products.labels`) staff permissions. See [[products-banners-labels-scheduling]].
- **No per-customer-group targeting** — every visitor sees the same badges. See [[products-banners-labels-targeting]].

## Related

- [[products]] — parent hub.
- [[products-products]] — products that get the badges; products list shows attached banners / labels.
- [[products-categories]] — `category` record type targets all products in a category.
- [[products-smart-collections]] — `selection` record type targets all members; smart-collection rules drive auto-population.
- [[marketing-discounts]] — `discount` record type targets all products linked to a discount.
- [[bundles-list]] — bundles are EXCLUDED from auto-population.
- [[product]] — entity page.

## Open questions

- How does the storefront handle two badges on the same position? Stacking order is theme-dependent. `(verify)`
- Does the storefront cache the banner-to-product mapping? Stale view possible if so. `(verify)`
