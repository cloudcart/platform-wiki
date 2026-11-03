---
type: entity
nav_path: "Entity → Product"
route_name: (none)
route_path: (none)
aliases: ["Product", "Catalog item", "Catalog product", "SKU parent", "Продукт", "Артикул", "Стока"]
tags: [entity, catalog, products, core]
plan_gates: ["products", "bundles"]
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---

# Product

## Identity

A **Product** is a sellable item in the merchant's catalog — the central thing a customer sees on the storefront, adds to a cart, and pays for. Each product is identified by a name + URL handle, lives inside one or more [[category|Categories]], may carry a single [[vendor|Vendor (Brand)]], and is the parent record under which the actual sellable units — [[variant|Variants]] — exist.

A product without explicit variant parameters still has exactly one variant under the hood (the "single-variant" case), so **SKU, barcode, price, and quantity always live on the [[variant|Variant]]**, not on the Product. The Product carries descriptive content (name, descriptions, images, SEO), the publish window (Active, Draft, Hidden, publish / expiry dates), the relationship graph (categories, vendor, tags, smart collections, linked products), and the type (`simple` / `multiple` / `digital` / `bundle` / `physically`).

Products are plan-gated — the merchant's plan caps how many **non-bundle** products the catalog can contain via the `products` plan-feature key. A separate `bundles` cap covers bundle-type products. Every product save fires a search-engine re-index, a smart-collection re-evaluation, and (where subscribed) a `product.created` / `product.updated` webhook to [[settings-hooks]] — see [[product-entity-side-effects-and-api]].

## Aliases

- **Product** — the standard merchant-facing term in the admin UI.
- **Catalog item** / **Catalog product** — used in some import / sync contexts.
- **SKU parent** — informal merchant phrasing when discussing multi-variant products (each variant has its own SKU).
- **Артикул** / **Продукт** / **Стока** — Bulgarian terms used interchangeably.

## Key Attributes

The Product is a multi-faceted record split across **five well-scoped aspects**. The AI Assistant should drill into the aspect that matches the question, not read every page.

- [[product-entity-attributes]] — the full per-field schema (identity, publish flags, FK references, p1 / p2 / p3 parameter slots, computed price range, descriptions, SEO, import provenance, tags, validation caps — 191-char `name`, 250,000-char `description`, max 100 tags, max 3 parameters, max 500 variants).
- [[product-entity-lifecycle]] — the eight named states (Draft, Scheduled, Visible, Hidden, Expired, Out of stock, Soft-deleted, Hard-deleted), save-time transitions, the 10-day soft-delete window, "Save and publish" flow, duplicate-to-Draft behaviour, URL-handle 301 redirects.
- [[product-entity-relationships]] — variants, categories, vendor, tags, images, file assets, SEO meta, smart collections, discounts, banners-and-labels, linked products, bundle child-products, order line items, customer favorites, back-in-stock waitlists; FK-cleanup behaviour (`ON DELETE SET NULL`).
- [[product-entity-business-rules]] — variants own SKU / barcode / price / quantity (not the Product); publish requires a category; Hidden vs Draft; publish window in store timezone; oversell + threshold gating on `tracking`; bundle auto-deactivation; `physically` filter alias; legacy `sale` field; plan-gated `products` vs `bundles` counts.
- [[product-entity-side-effects-and-api]] — save side effects (search re-index, `product.updated` chattiness, smart-collection re-evaluation, cache invalidation, change-log entry); `product.created` / `product.updated` / `product.deleted` webhooks; JSON-API v2 access via [[api-products]] / [[api-variants]]; hard-delete cascade; webhook caveat (admin-only fires).

## Why it matters to the merchant

The Product record is where **catalog identity, publish state, inventory configuration, and storefront discoverability** intersect. Five high-impact behaviours the merchant should understand:

- **Quantity, price, SKU, and barcode are per-Variant — not per-Product.** Even a "simple" product has one underlying Variant. See [[product-entity-business-rules]] + [[variants-model]].
- **Hidden ≠ Draft.** Hidden is published-but-unlisted (direct URL works). Draft is unpublished (direct URL returns 404). Merchants conflate the two often. See [[product-entity-business-rules]].
- **Publish requires a category, and bundles silently auto-deactivate when a child deactivates.** The reverse direction (re-activating the child) does NOT auto-re-activate the bundle. See [[product-entity-business-rules]].
- **`product.updated` is chatty.** Any field change — including post-order stock decrements — fires the webhook. Receivers must be idempotent. See [[product-entity-side-effects-and-api]].
- **Soft-delete holds for 10 days, then hard-purges silently.** The merchant gets one tooltip warning during the window and no follow-up notification on hard-purge. See [[product-entity-lifecycle]].

## Where it appears

- [[products-products]] — the core list + edit screen for products.
- [[products-inventory]] — inventory-focused view (stock per variant, low-stock alerts).
- [[products-categories]] — category management; products belong to categories here.
- [[products-vendors]] — vendor (brand) management.
- [[products-variants-options]] — variant parameters and options.
- [[products-property]] — category-bound property values shown inline on the Edit page.
- [[products-tags]] — product tag management.
- [[products-statuses]] — custom in-stock / out-of-stock statuses (the `status_id` / `out_of_stock_id` references).
- [[products-banners-labels]] — banners and labels overlaid on products on the storefront.
- [[products-smart-collections]] — smart-collection assignments.
- [[products-favorite-products]] — customers' favorited products.
- [[products-missing-product]] — back-in-stock waitlist subscribers.
- [[products-change-log]] — per-product audit trail; first stop for "stock changed and we didn't change it" tickets.

## Related

### Related entities

- [[variant]] — the sellable unit under a Product. SKU, barcode, price, quantity all live here.
- [[product-option]] — parameter option (Red, Large, Cotton); the parameter-and-option model is described in [[products-variants-options]].
- [[category]] — required for publish; product can belong to many.
- [[vendor]] — at most one per product.
- [[product-status]] — custom in-stock / out-of-stock status labels and button text.
- [[bundle]] — bundle-type product (groups other products).
- [[order]] — orders contain product line items.
- [[discount]] — discount records targeting products.
- [[smart-collection]] — rule-based or manual product groupings.
- [[file-asset]] — file storage (images, digital downloads, attachments).
- [[seo-meta]] / [[seo-redirect]] — SEO metadata; URL-handle changes create redirects.
- [[customer]] — customers favorite products and place orders that contain product line items.

### Cross-cutting concepts

- [[variants-model]] — how product + variants + parameters + options compose.
- [[inventory-tracking]] — stock tracking, oversell, low-stock thresholds.
- [[multi-language]] — how descriptions, names, and SEO are translated.
- [[multi-currency]] — how variant prices are converted for storefront display.
- [[plan-gates]] — the `products` / `bundles` count caps.
- [[seo-handling]] — URL handles, redirects, meta tags.
- [[checkout-flow]] — how products are validated at cart and checkout.
- [[import-pipeline]] — CSV / XML / app imports populating the catalog.

### Settings & webhooks

- [[settings-cart]] — `order_status_for_quantity_decrease` controls when stock decrements; `product_threshold` triggers low-stock notifications.
- [[settings-hooks]] — `product.created`, `product.updated`, `product.deleted` webhook events.
- [[json-api-v2]] — programmatic-access hub.

## Open Questions

Distributed to aspect pages. See:

- [[product-entity-attributes]] — FK `ON DELETE SET NULL` behaviour across all referenced tables.
- [[product-entity-lifecycle]] — Scheduled products and the storefront sitemap.
- [[product-entity-business-rules]] — 500-variant cap on row count vs active variants.
- [[product-entity-relationships]] — current status of `ProductFilesGroups`-style attachment grouping.
- [[product-entity-side-effects-and-api]] — which JSON-API v2 endpoints fire `product.*` webhooks vs which bypass them; stock-decrement-only saves and the chatty `product.updated` stream.
