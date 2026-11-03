---
type: feature
nav_path: "Products → Favorite products"
route_name: products-favorite
route_path: /admin/products/favorite-products
aliases: ["Favorite products", "Wishlist insights", "Customer favorites", "Любими продукти", "Списък с желания"]
tags: [products, favorites, wishlist, insights]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 6
---
# Favorite products

## Purpose

A read-only **insight page** showing which products customers have added to their wishlist / favorites on the storefront. Each row aggregates one product with: how many customers have favorited it, the product's current stock quantity, and a quick action to reach the merchant's marketing campaign or notification tools.

The merchant uses this page to spot **demand patterns** — products that aren't selling fast but have many "wishlisting" customers may be priced wrong, out of stock too often, or simply ripe for a marketing push. It's a common starting point for promotional campaigns and inventory replenishment decisions.

## Where to find it

Sidebar → Products → **Favorite products**.

The page's breadcrumb reads "Products → Favorite products". The route is `/admin/products/favorite-products`. The header icon is the star icon.

## What the merchant can do here

- See all products with **at least one customer favorite** in a paginated table.
- Columns: **Name** (product name + thumbnail), **Quantity** (current stock), **Customers** (count of customers who favorited this product), **Actions**.
- Filter and search (standard table filters).
- Click the action button per row to reach a marketing follow-up — typically opens the notify-subscribers flow OR navigates to the product editor.
- Sort by name, quantity, or customers count.

### What the merchant CANNOT do here
- See WHICH specific customers favorited a product (no customer-list drill-in from this page). Customer privacy is preserved.
- Notify all favoriters at once with a single click — the merchant can use marketing campaigns / segments to target customers based on favorites (see [[marketing-campaigns]] / segment definitions).
- Edit the product from this page — clicking the name typically links to the product editor in [[products-products]].
- Delete or reset favorite-counts — favorites are customer-side actions; the merchant doesn't manage them directly.

### Action button — two states, no modal

The per-row Actions button is shared with [[products-missing-product]] and has exactly two states. No modal, popover, or inline editor opens — clicking either button just navigates away, with the favorites count shown in parentheses:

- **Product fully out of stock (quantity = 0)** — a ghost button *"Subscribers (N)"* opens [[marketing-subscribers]] in a new tab, pre-filtered to subscribers waiting on that variant: `/admin/subscribers?filters[subscribe_for_missing_product]={variant_id}`.
- **Product in stock (quantity > 0)** — a primary button *"Create a campaign (N)"* navigates same-tab to `/admin/campaigns` to start a new email campaign.

## Settings & fields

### List columns

| Column | Notes |
|--------|-------|
| **Name** | Product name + thumbnail. Click navigates to the product editor in [[products-products]]. |
| **Quantity** | Current stock count (aggregated across variants for variant-having products). |
| **Customers** | Count of distinct customers who have this product in their favorites. |
| **(actions)** | Per-row action — typically navigates to a marketing flow or notification trigger. |

## Business rules

### Read-only insight page

This page does not let the merchant modify favorites — those are owned by individual customers via the storefront wishlist UI. The merchant's role is to OBSERVE patterns and ACT on them (via marketing, restocking, promotions).

### Aggregate per-product, not per-variant

The Quantity column shows the aggregate stock for the product. If a product has variants, the count is the total across all variants. To see per-variant quantities, the merchant uses [[products-inventory]].

### Customers count = unique customers, not total favorites

A single customer can favorite a product only once, so the Customers count equals the number of distinct customer accounts that have this product in their favorites. The storefront wishlist requires a logged-in customer (anonymous clicks redirect to login), so in practice the count reflects only registered customers.

### Permission

This page sits under the standard products permission scope. Moderators without product access don't see the Favorite products sidebar entry.

### Read-only — no queue, no notifications

This page only READS the favorites aggregate. No background jobs, admin notifications, or webhooks fire here, and favoriting / unfavoriting a product fires no webhook either — the merchant learns about new favorites only by checking this page or the dashboard KPIs (below).

## Plan gates

This feature has **no plan-feature gate** — all plans (including free trial / staging stores) see the Favorite products page, governed only by the standard products permission scope.

Downstream surfaces have their own gating, but this page is plan-neutral. The **Create a campaign** button opens [[marketing-campaigns]], where campaign creation is gated by per-channel mappings (e.g. `campaign.channels.email`, `mailchimp`) — but those gates fire on the campaign screen, not here. See [[plan-gates]] for the concept.

## Related

- [[products]] — parent hub.
- [[products-products]] — clicking a product name navigates to its editor.
- [[products-missing-product]] — sibling insight page; tracks products customers want to be notified about when restocked.
- [[products-inventory]] — per-variant stock view.
- [[marketing-campaigns]] — segment-based email campaigns can target customers based on favorites (configured separately).
- [[customer]] — customers are the owners of favorites.
- [[product]] — entity page.

## How it works (verified against backend)

### Favorites are stored per customer, no time decay

Each favorite is one row per customer + product pair. There is no automatic pruning of "stale" favorites — a favorite stays in the count until the customer removes it from their wishlist on the storefront, or the customer / product is deleted. Deleting a customer or a product removes the related favorite-rows (cascade), and the Customers count drops accordingly.

### Login required; one-click toggle

The storefront wishlist hard-checks for a logged-in customer: a guest clicking the heart icon is redirected to login with `_redirect` pointing back to the product. The same action both adds and removes — re-clicking removes the favorite. The list shows no "favorited at" timestamp.

### Quantity column = sum across ALL variants

The Quantity number is the total stock summed across the product's variants, not the parent product's own quantity field. A multi-variant product with stocks Red=5, Blue=3, Green=0 shows **8** here. This can mislead: a product showing "0" might still be partly available if untracked variants exist — use [[products-inventory]] for the precise per-variant view.

### Sort order: descending by favorites count

The default sort puts the product with the MOST customer favorites first — highest-demand items at the top. The merchant can override with the table sort.

### Auxiliary favorites dashboard KPIs

A background job writes three site-wide KPIs to the marketing dashboard (not this list page):
- **Total favorites** — count of all favorites.
- **Amount** — sum of `price_from` across all favorited products (what the wishlists would be worth at list price).
- **Average** — average favorites-per-customer.

The "top 5 favorited products" mini-module on that dashboard is the same data ranked descending, limited to 5.

## Open questions
