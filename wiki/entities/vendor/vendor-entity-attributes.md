---
type: entity
nav_path: "Entity → Vendor → Key attributes"
aliases: ["Vendor attributes", "Vendor fields", "Vendor record fields", "Brand fields", "Vendor logo", "Vendor SEO meta"]
tags: [entity, catalog, vendors, brands, attributes]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[vendor]]. See the hub for the other aspects (lifecycle, relationships, business rules).

# Vendor — Key attributes

## Identity

The full per-field schema for the [[vendor|Vendor (Brand)]] record — every attribute the merchant configures on the Add / Edit modal on [[products-vendors]], with its purpose, allowed values, and notes. This is the page the AI Assistant cites when a merchant asks *"What goes in field X on the vendor / brand form?"*, *"Where do I upload the brand logo?"*, or *"How do I set a custom SEO title for a brand page?"*.

## Aliases

- **Vendor attributes** / **Vendor fields** / **Brand fields** — the per-record field definitions.
- **Add / Edit modal fields** — the merchant-facing labels on the Vendors screen.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Name** (per-language) | Required — the vendor's display name | Translatable: a multi-language store can set a different name per active storefront language. Shown on the vendor landing page header, in the product card's brand line, and on the product detail page. |
| **Description** (per-language) | Long-form HTML body | Rich-text — supports HTML and embedded images. Surfaces on the vendor's storefront landing page. Translatable per active storefront language. |
| **Logo** | Image upload (single file) | Stored as a [[file-asset|file asset]]; thumbnailed for the vendor list grid and the product card; full-resolution version shown on the vendor landing page. Optional but strongly recommended — customers expect to see brand logos. |
| **URL handle** (`url_handle`) | URL slug for the storefront vendor page | Drives `/vendor/<slug>` on the storefront — see [[storefront-vendor]]. Auto-derived from Name on create; editable. Renaming generates a 301 redirect from the old handle — see [[vendor-entity-business-rules]]. |
| **SEO title** (`meta_title`) | Per-language SEO `<title>` | Falls back to Name + storefront SEO defaults when empty. |
| **SEO description** (`meta_description`) | Per-language SEO `<meta name="description">` | Falls back to a truncated Description when empty. |
| **Image dimensions / processing** (`width`, `height`, `max_thumb_size`, `image_processed`) | Optional pixel dimensions + processed marker | Per-vendor display hints that drive how the logo is rendered on cards / vendor page. `image_processed = 1` means the platform has already generated the thumbnail variants for this image. |
| **Background image** (`background`) | Optional banner image | A second image distinct from the logo, intended as a landing-page banner. Theme support varies — the default template does not render it (see [[vendor-entity-business-rules]]). |
| **SEO Spinner marker** (`seo_generated_through_spinner`) | yes / no | Set when [[apps-seo-spinner]] generated the SEO description for this vendor; counts toward that app's plan cap. |
| **Custom fields** (Options morph) | M2M via `form_field_mapping` | A vendor can have its own custom fields ([[product-option|Product Options]] attached at vendor scope). When attached at vendor scope, the field auto-applies to every product of that vendor. See [[product-option]]'s "Options can be attached at multiple scopes". |
| **Products count** | Auto-computed | Number of [[product|Products]] currently assigned to this vendor. Shown on the [[products-vendors]] list and used for the **Has products: Yes / No** filter — see [[vendor-entity-business-rules]]. |
| **Created at** / **Updated at** | Timestamps | Surface on the vendor list grid for sorting. |

## Where it appears

- [[products-vendors]] — the Add / Edit modal where every field above is set, the logo uploaded, and SEO metadata entered.
- [[storefront-vendor]] — the public `/vendor/<url_handle>` page that renders Name + Logo + Description + the product grid.
- [[product]] — the product editor's Vendor picker selects from the active vendor list; the storefront product detail page renders the vendor's Name as the brand line.
- [[marketing-seo-meta]] — the per-vendor `meta_title` / `meta_description` fields are the per-entity SEO override; the SEO screen only supplies the fallback defaults.
- [[api-vendors]] — JSON-API v2 exposes the same attribute set (Name, Description, logo, SEO meta, `url_handle`) for CRUD by integrations.

## Related

- [[vendor]] — hub.
- [[product]] — the entity that references a vendor via `vendor_id`.
- [[file-asset]] — the logo (and background banner) image is stored as a file asset.
- [[product-option]] — vendor-scope custom fields are Product Options attached at vendor scope.
- [[apps-seo-spinner]] — generates the SEO description and sets `seo_generated_through_spinner`.
- [[multi-language]] — Name, Description, SEO title, and SEO description are translatable per active storefront language.

## Open Questions

None.
