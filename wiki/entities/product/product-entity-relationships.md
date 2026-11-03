---
type: entity
nav_path: "Entity → Product → Relationships"
aliases: ["Product relationships", "Product associations", "Product to category", "Product to variant", "Product to bundle"]
tags: [entity, catalog, products, relationships]
plan_gates: ["products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product]]. See the hub for the other aspects (attributes, lifecycle, business rules, side effects and API).

# Product — Relationships

## Identity

The complete relationship graph for a [[product|Product]]: which entities own it, which entities it owns, which it cross-references, and which it appears inside. This page is the navigation pivot when a merchant asks *"Where do tags / images / discounts / smart collections come from?"* or *"What happens to the product if its category / vendor / variant is deleted?"*.

## Aliases

- **Product relationships** / **Product associations** — the cross-table graph.
- **Linked products** — the merchant-managed manual cross-sell list.
- **Bundle children** — the curated list of products that make up a [[bundle]].

## Key Attributes

The FK and pivot fields are documented in [[product-entity-attributes]] (`category_id`, `vendor_id`, `image_id`, `status_id`, `out_of_stock_id`, `default_variant_id`, `p1_id` / `p2_id` / `p3_id`). This page describes what each relationship means and how it behaves.

## Ownership: what the Product has

A Product:

- **Has many** [[variant|Variants]] — every sellable unit. A simple product has exactly one underlying variant; a multiple-variant product has 1-N (capped by parameter combinations, max **500 variants per product**). SKU, barcode, price, quantity, weight, dimensions, unit info — all live on the variant, NEVER on the Product. See [[variants-model]] + [[product-entity-business-rules]].
- **Has 0-3** variant parameters (p1, p2, p3) — each one is a parameter (e.g., "Color") whose options drive the variant matrix. The platform caps this at **3 parameters per product** as a hard data-model limit. See [[products-variants-options]].
- **Has many** product-level tags for filtering / search / segmentation (see [[products-tags]]).
- **Has many** images via the image gallery (one is the primary thumbnail, picked by `image_id`).
- **Has many** [[file-asset|File assets]] — digital downloads, public attachments, non-public attachments grouped per product. (verify)
- **Has many** [[seo-meta|SEO meta]] entries for additional structured-data fields beyond the inline `seo_title` / `seo_description`.
- **Has many** [[smart-collection|Smart Collection]] memberships — rule-based or manual product groupings.
- **Has many** Product Banners + Product Labels (when the Banners-and-Labels app is installed — see [[products-banners-labels]]).
- **Has many** [[discount|Discounts]] applied via the product↔discount pivot (read-only on the Product edit page — the merchant manages discounts separately on [[marketing-discounts]]).

## Membership: what the Product belongs to

- **Belongs to many** [[category|Categories]] via a category pivot — a primary `category_id` plus additional categories. **Active products must have at least one category** (publish is blocked at save time otherwise — see [[product-entity-business-rules]]).
- **Belongs to one** [[vendor|Vendor (Brand)]] (optional) via `vendor_id`.
- **Belongs to many** other products via the **Linked products** list (manual cross-sells), and via **[[bundle|Bundle]]** parent-child links when the product is part of a bundle.

## References (lookups)

- **References** in-stock and out-of-stock [[product-status|Product Statuses]] (custom labels + button-text per stock state).
- **Maps to** category-bound properties from [[products-property|Category Properties]] — the merchant fills the property values inline on the Product edit page after picking a category that defines them.

## Appearance: where the Product shows up

- **Appears in** [[order|Orders]] through the order line-item pivot — one Product can be in many Orders.
- **Appears in** the customer's favorites when customers favorite it (see [[products-favorite-products]]).
- **Appears in** subscriber back-in-stock waitlists when the merchant runs [[products-missing-product]].
- **Appears in** active and abandoned [[cart|Carts]] via the cart line-items.

## Bundle-specific structure

A Bundle product (`type = bundle`) doesn't own its own variants in the traditional sense — its sellable content is a curated list of OTHER products. The relationships that matter:

- The bundle's child products form a one-to-many ownership where each line carries quantity + (optionally) the locked-in variant choice.
- When one of the bundle's child products is **deactivated**, the bundle is **auto-deactivated** in the same save. When the child is reactivated, the bundle is NOT auto-reactivated (merchant must do that manually). See [[product-entity-business-rules]].
- `individual_price = yes/no` controls whether the bundle's price is the SUM of children's current prices (live) or a fixed bundle-level price — see [[product-entity-attributes]].
- Bundle stock derives from minimum-available across child Variants — see [[inventory-bundle-stock]].

## FK-cleanup behaviour

Deleting a referenced [[category]], [[vendor]], [[product-status]], default [[variant]], or primary image **silently nulls** the FK on the Product (`ON DELETE SET NULL`) — the product survives but falls back to defaults (first remaining variant, next image, no status label, etc.). See [[product-entity-attributes]] for the full FK list. (verify)

## Where it appears

- [[products-products]] — the central screen where the relationships are surfaced (category picker, vendor picker, tag input, image gallery, variants matrix, linked-products list).
- [[products-categories]] — category management.
- [[products-vendors]] — vendor / brand management.
- [[products-tags]] — tag management.
- [[products-statuses]] — custom in-stock / out-of-stock status definitions.
- [[products-smart-collections]] — smart-collection assignments.
- [[products-banners-labels]] — banners and labels overlays.
- [[products-favorite-products]] — favorites by customers.
- [[products-missing-product]] — back-in-stock waitlists.

## Related

- [[product]] — hub.
- [[variant]] — sellable unit; SKU / barcode / price / quantity live here.
- [[category]] / [[vendor]] / [[product-status]] / [[file-asset]] / [[seo-meta]] / [[smart-collection]] — directly referenced entities.
- [[bundle]] — bundle-type Product structure.
- [[discount]] — product↔discount pivot.
- [[order]] / [[cart]] — Products appear as line items.
- [[customer]] — customers favorite and order products.
- [[products-variants-options]] — parameter and option model.
- [[products-property]] — category-bound properties.
- [[variants-model]] — Parameter / Option / Variant / Matrix composition.
- [[inventory-bundle-stock]] — bundle stock derivation.

## Open Questions

- Confirm whether `ProductFilesGroups`-style attachment grouping is exposed in the merchant UI today or is a legacy internal structure (verify).
