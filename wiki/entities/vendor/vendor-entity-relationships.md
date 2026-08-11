---
type: entity
nav_path: "Entity → Vendor → Relationships"
aliases: ["Vendor relationships", "Vendor product link", "Vendor vs category", "Vendor vs tags", "Vendor vs supplier", "Vendor discount link", "Vendor smart collection"]
tags: [entity, catalog, vendors, brands, relationships]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[vendor]]. See the hub for the other aspects (attributes, lifecycle, business rules).

# Vendor — Relationships

## Identity

How the [[vendor|Vendor (Brand)]] record connects to the rest of the catalog graph — its one-to-many link to [[product|Products]], the entities that reference a vendor (discounts, smart collections, SEO redirects), and the three neighbouring concepts merchants routinely confuse it with (tags, categories, and procurement-side suppliers). The Assistant cites this page for *"What's the difference between a brand and a tag?"*, *"Can a product have two brands?"*, and *"How does a vendor discount know which products it covers?"*.

## Aliases

- **Vendor relationships** — the entity graph around a vendor.
- **Vendor vs tag / category / supplier** — the three disambiguation pairs.

## Key Attributes

A Vendor:

- **Has many** [[product|Products]] via each product's `vendor_id` — one-to-many. Every product can have at most ONE vendor; one vendor can have many products. The link is **optional** — a product is NOT required to carry a vendor. (The one-vendor-per-product rule and its merchant implications are in [[vendor-entity-business-rules]].)
- **Is referenced by** [[discount|Discounts]] of the `product_type_discounts` shape that target **a specific vendor's products** — e.g., *"15% off all Apple products"*. The discount stores the vendor ID and applies to every product where `vendor_id` matches at evaluation time (the automatic re-evaluation behaviour is covered in [[vendor-entity-business-rules]]).
- **Is referenced by** [[smart-collection|Smart Collections]] rule conditions that include *Vendor =/!= X* — so a smart collection can dynamically group "all Bosch products" or "everything NOT made by us".
- **Maps to** a [[seo-redirect|SEO redirect]] when the merchant changes the vendor's `url_handle` (old → new permanent redirect to preserve search rankings).
- **Owns** a [[file-asset|file asset]] for its logo (and optionally a background banner).

A Vendor is **distinct from**:

- **[[products-tags|Product tags]]** — tags are free-form and many-per-product; a vendor is structured and exactly-one-per-product.
- **[[category|Categories]]** — categories group by what the product IS; vendors group by who made it. A product can sit in many categories but has at most one vendor.
- **Supplier records (procurement-side app)** — the supplier app tracks who the merchant orders restock from; that is internal-only and never shown on the storefront. Vendors are public, customer-facing.
- **The Brand-model app** — a separate app that adds device-compatibility metadata for accessory stores; it does not create or sync vendors (see [[vendor-entity-business-rules]] for the full separation).

## Where it appears

- [[product]] — the `vendor_id` link; the product editor's Vendor picker and the storefront brand line.
- [[marketing-discounts-fixed]] — vendor-targeted Fixed-price discounts store the vendor ID and resolve products at evaluation time.
- [[products-smart-collections]] — smart-collection rules can include *Vendor = X* / *Vendor != X*.
- [[seo-redirect]] — vendor `url_handle` changes create redirect entries.
- [[storefront-vendor]] — the public landing page that materialises the has-many-products relationship as the product grid.

## Related

- [[vendor]] — hub.
- [[product]] — one-to-many; the product carries `vendor_id`.
- [[category]] — sibling taxonomy (by WHAT vs by WHO).
- [[products-tags]] — free-form many-per-product alternative.
- [[discount]] — vendor-targeted discounts reference the vendor ID.
- [[smart-collection]] — vendor-aware collection rules.
- [[seo-redirect]] — URL-handle change redirects.
- [[file-asset]] — the logo / background image.

## Open Questions

None.
