---
type: entity
nav_path: "Entity → Vendor → Business rules"
aliases: ["Vendor business rules", "One vendor per product", "Reassign before delete vendor", "Has products filter", "Vendor discount coverage", "Vendor SEO", "Vendor landing page template", "Vendor plan gate"]
tags: [entity, catalog, vendors, brands, business-rules]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[vendor]]. See the hub for the other aspects (attributes, lifecycle, relationships).

# Vendor — Business rules

## Identity

The behavioural rules that govern how a [[vendor|Vendor (Brand)]] is used day-to-day: the one-vendor-per-product constraint, the reassign-before-delete cleanup workflow, the **Has products** filter, how vendor-targeted discounts resolve their coverage, per-vendor SEO behaviour, the minimal default landing-page template, the Vendor vs Brand-model-app separation, and the absence of a plan cap on vendor count. The Assistant cites this page for *"How do I clean up unused brands?"*, *"Why did adding a product extend my brand discount?"*, and *"Why does my brand page look so plain?"*.

## Aliases

- **Vendor business rules** — the operational constraints on vendor usage.
- **Reassign before delete** — the mandatory pre-deletion workflow.
- **Has products filter** — the unused-vendor cleanup tool.

## Key Attributes

### One vendor per product, many products per vendor

Each [[product|Product]] has at most ONE `vendor_id`. There is no many-to-many — a product cannot be tagged with two vendors. If the merchant needs to express "this product is made by Apple AND distributed by ABC", they pick one as the vendor (typically the brand the customer recognises) and put the other in a different field (description, tag, custom property).

### Delete is blocked at the model layer — reassign first

When the merchant attempts to delete a vendor that still has products, the model's `deleting` hook throws *"Cannot delete vendor — has products"* and the delete is REJECTED (see [[vendor-entity-lifecycle]]). The platform does NOT silently `SET NULL` the `vendor_id` on referencing products. The required workflow:

1. Filter products by the doomed vendor in [[products-products]].
2. Bulk-edit to reassign them to another vendor (or clear the vendor field).
3. Then delete the now-empty vendor.

For very large catalogues, a CSV export → re-import with the new vendor column is the alternative. (Earlier wiki revisions claimed the delete "clears product links automatically" — that is incorrect; the merchant must reassign first.)

### Has-products filter helps clean up unused vendors

The vendor list's **Has products: Yes / No** filter is the merchant's primary tool for identifying vendors that are no longer used (Has products = No) — typically discontinued brands or test entries. The vendor list supports row selection + **bulk delete** via the standard delete action, so the merchant can clear out dozens of legacy vendors at once. Because these vendors have zero products, the bulk delete passes the model-layer guard cleanly and no product loses data.

### Vendor-targeted discounts cover ALL of that vendor's products

A [[discount|Discount]] whose product-type filter is set to "vendor" with a specific vendor selected applies to **every** product whose `vendor_id` matches that vendor at evaluation time — not just the products selected when the discount was created. So adding new products to a vendor later automatically extends the discount to them; removing products from the vendor automatically excludes them. See [[marketing-discounts-fixed]] and other vendor-aware discount types.

Re-evaluation is **automatic**: the discount stores the vendor ID and at evaluation time queries the live product table. Moving a product from "Apple" to "Samsung" mid-discount-window IMMEDIATELY removes the Apple discount from that product and (if Samsung has its own discount) applies the Samsung discount on the next cart-add or storefront page-load. No re-publish step needed.

### Vendor pages have their own SEO

The merchant can set per-vendor `meta_title` and `meta_description` (see [[vendor-entity-attributes]]). When set, these render in the vendor landing page's `<title>` and `<meta>` tags; when empty, the platform falls back to the Name plus storefront SEO defaults. This lets the merchant optimise vendor pages for brand-specific searches (*"Buy Apple"*, *"Bosch in Bulgaria"*). Renaming a vendor's `url_handle` generates a 301 redirect from the old URL to the new one (recorded as a [[seo-redirect|SEO redirect]]), so bookmarks and search-engine results keep landing on the right page.

### Vendor landing-page design is templated

The default vendor landing page ([[storefront-vendor]]) renders Name + Logo + Description + the product grid. There is **NO banner image, intro section, or recommended-products module** out of the box — even though the record carries a `background` field (see [[vendor-entity-attributes]]). The page is theme-controlled — a custom theme can render any HTML around the vendor's data — but the default templates are minimal.

### Vendor vs Brand-model app — separate entities

A Vendor here is the customer-facing manufacturer label on the product detail page and the vendor landing page. The **Brand-model app** (a different app that adds device-compatibility metadata for accessory stores) is independent — installing it does NOT automatically create vendors for its brands, and creating a vendor does NOT register a brand-model entry. Merchants who need both maintain them independently.

### No plan gate on vendor count

Vendors are NOT plan-gated in the current model — the merchant can create as many as they want on any plan tier. (Contrast with [[customer-group|Customer Groups]] and [[product|Products]], which both have plan caps.)

## Where it appears

- [[products-vendors]] — the Has-products filter, bulk delete, and the Add / Edit flow that enforces these rules.
- [[products-products]] — the bulk-edit workflow for reassigning products before deleting a vendor.
- [[marketing-discounts-fixed]] — vendor-targeted discounts whose coverage these rules describe.
- [[storefront-vendor]] — the minimal default landing-page template.

## Related

- [[vendor]] — hub.
- [[product]] — one vendor per product; reassignment before delete.
- [[discount]] / [[marketing-discounts-fixed]] — vendor-targeted discount coverage + automatic re-evaluation.
- [[seo-redirect]] — URL-handle rename redirects.
- [[storefront-vendor]] — the default (minimal) landing-page template.
- [[plan-gates]] — vendor count is NOT plan-gated.
- [[customer-group]] — contrast: a plan-gated catalog entity.

## Open Questions

None.
