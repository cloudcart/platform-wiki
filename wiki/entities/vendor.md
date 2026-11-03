---
type: entity
nav_path: "Entity → Vendor (Brand)"
aliases: ["Vendor", "Brand", "Manufacturer", "Supplier brand", "Vendor brand", "Производител", "Бранд", "Марка", "Доставчик (бранд)"]
tags: [entity, catalog, products, vendors, brands]
created: 2026-05-23
updated: 2026-06-10
source_count: 1
---

# Vendor (Brand)

## Identity

A **Vendor** (also called a **Brand** or **Manufacturer**, depending on the merchant's terminology) is the customer-facing supplier or brand label associated with products in the catalog — *"Apple"*, *"Samsung"*, *"Nike"*, *"Bosch"*, *"Lego"*. The merchant maintains a list of vendors on [[products-vendors]] and assigns **one** vendor per [[product|Product]] from the product editor; the platform then builds a public storefront landing page for that vendor where customers browse every product carrying that label. A vendor is therefore a **catalog-level taxonomy** — it groups products by who made them, in the same spirit that a [[category|Category]] groups them by what they are.

A Vendor is distinct from two other CloudCart concepts the merchant might confuse it with: the **Brand-model app** (which adds device-compatibility metadata like *"compatible with iPhone 13"* — useful for accessory stores) and the **Supplier app** (which is procurement-side — who the merchant buys their stock from). Vendors here are the **public, customer-facing manufacturer list** displayed on the storefront. The merchant treats them as marketing entities: each carries a logo, a description shown on the vendor landing page, SEO metadata, and a URL handle for the public URL.

## Aliases

- **Vendor** — the canonical merchant-facing term in CloudCart admin UI ("Vendors" sidebar item).
- **Brand** — the most common merchant-facing synonym; "Brand" is what storefront customers see on the product detail page.
- **Manufacturer** — used by some merchant types (electronics, automotive parts) where "brand" feels marketing-flavoured but "manufacturer" feels factual.
- **Vendor brand** / **Supplier brand** — informal phrasing distinguishing the customer-facing vendor from the procurement-side supplier.
- Bulgarian: **Производител** (standard for "manufacturer"), **Бранд** / **Марка** (for "brand"), **Доставчик (бранд)** (informal).

## Key Attributes

The Vendor is a multi-faceted record split across **four well-scoped aspects**. The AI Assistant should drill into the aspect that matches the question, not read every page.

- [[vendor-entity-attributes]] — the full per-field schema: per-language Name / Description / SEO title / SEO description, single-file Logo, optional Background banner, `url_handle`, image-processing hints (`width`, `height`, `max_thumb_size`, `image_processed`), `seo_generated_through_spinner` marker, vendor-scope custom fields (Options morph), the auto-computed products count, and timestamps.
- [[vendor-entity-lifecycle]] — the merchant-controlled states (Created → Live → Empty → Pre-delete → Deleted); the absence of any `active` / `is_active` toggle; delete **blocked at the model layer** while products reference the vendor (`vendor.err.cannot_delete_vendor_has_products`); the save / delete events fired to [[settings-hooks]] (`vendor.created` / `vendor.updated` / `vendor.deleted`) plus the internal the application framework events.
- [[vendor-entity-relationships]] — has-many [[product|Products]] via `vendor_id` (one-to-many, optional); referenced by vendor-targeted [[discount|Discounts]] and [[smart-collection|Smart Collection]] rules; mapped to a [[seo-redirect|SEO redirect]] on URL-handle change; how a vendor differs from [[products-tags|tags]], [[category|categories]], and procurement-side supplier records; logo as a [[file-asset|file asset]].
- [[vendor-entity-business-rules]] — one-vendor-per-product; reassign-before-delete (no auto `SET NULL`); the **Has products: Yes / No** cleanup filter + bulk delete; vendor-targeted discounts covering ALL of the vendor's products with automatic re-evaluation; per-vendor SEO with fallbacks + 301 redirects; minimal default landing-page template; Vendor vs Brand-model app separation; **no plan gate** on vendor count.

## Where it appears

- [[products-vendors]] — the main vendor list + Add / Edit modal. Where the merchant creates, edits, deletes vendors and assigns logos and SEO.
- [[product]] — every Product's edit page has a Vendor picker that selects from the active vendor list. The product detail page on the storefront renders the brand line and links to the vendor landing page.
- [[storefront-vendor]] — the public `/vendor/<url_handle>` landing page that lists every product attributed to the vendor.
- [[marketing-discounts-fixed]] — Fixed-price discounts can target a vendor's products. The discount applies to ALL products with that `vendor_id` at evaluation time.
- [[products-smart-collections]] — smart-collection rules can include *Vendor = X* to dynamically group all products by a brand.
- [[seo-redirect]] — vendor URL-handle changes create redirect entries automatically.
- [[api-vendors]] — JSON-API v2 CRUD on the vendor list.

## Related

### Related entities

- [[product]] — products are the things that carry a vendor; one-to-many relationship.
- [[category]] — sibling taxonomy (categories group by WHAT the product is; vendors group by WHO made it).
- [[products-tags]] — free-form alternative tagging for cases where a vendor doesn't fit.
- [[discount]] — vendor-targeted discounts use the `product_type_discounts` shape to apply to all of a vendor's products.
- [[smart-collection]] — vendor-aware collection rules.
- [[file-asset]] — the vendor's logo image is a file asset.

### Cross-cutting concepts

- [[multi-language]] — vendor name, description, SEO title, and SEO description are translatable per active storefront language.
- [[seo-handling]] — vendor pages have their own SEO metadata; URL-handle changes generate 301 redirects.
- [[variants-model]] — vendors live at the Product level, not the Variant level (all variants of a product share the same vendor).
- [[plan-gates]] — vendor count is NOT plan-gated, in contrast to several other catalog entities.

## Open Questions

No outstanding questions — all items resolved or removed.
