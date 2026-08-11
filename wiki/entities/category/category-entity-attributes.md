---
type: entity
nav_path: "Entity → Category → Key attributes"
aliases: ["Category attributes", "Category fields", "Category record fields"]
tags: [entity, catalog, categories, attributes]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[category]]. See the hub for the other aspects (lifecycle, relationships, business rules, side effects and API).

# Category — Key attributes

## Identity

The full per-field schema for the [[category|Category]] record — every attribute the merchant configures on the Add / Edit modal on [[products-categories]], with its purpose, allowed values, and notes. This is the page the AI Assistant cites when a merchant asks *"What goes in field X on the category form?"* or *"What's the difference between SEO title and category name?"*.

## Aliases

- **Category attributes** / **Category fields** — the per-record field definitions.
- **Add / Edit modal fields** — the merchant-facing labels on the Categories screen.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Name** | Display name | Required. The label everywhere — list, edit header, storefront breadcrumbs, search facets. Free text. Must be unique among direct siblings — see [[category-entity-business-rules]]. |
| **Parent category** (`parent_id`) | The category one level up in the tree | Optional. Empty = top-level category. Searchable dropdown of all other categories on the edit form. Subject to the 6-level depth cap — see [[category-entity-lifecycle]]. |
| **Description** | Long-form HTML | Rich-text. Shown on the storefront category landing page (top of the product list). |
| **Display subcategories** (`display_child`) | yes / no toggle | When ON, the storefront category page shows products from this category AND all descendant subcategories (recursive). When OFF, only products directly assigned to this category. See [[category-entity-business-rules]]. |
| **Category image** | Single image upload | Drag-or-click. Shown on category cards in storefront listings and in some marketing surfaces. Stored in [[settings-files]]. Protected from mass-assignment — uploads go through the dedicated upload pipeline on the edit modal, not via bulk-edit / API patches. |
| **Google Product Taxonomy** (`taxonomy_id`) | FK to `google_product_category` node | Optional. Picks a node from Google's official Product Taxonomy (~5,500 entries, e.g. "Apparel & Accessories > Clothing > Dresses"). Read by Google Shopping, Meta / Facebook Catalog, Criteo and the storefront search index. Informational only — does NOT restrict products. **Products inherit this from their category** — they have no `taxonomy_id` of their own. See [[products-categories-taxonomy]]. |
| **Define custom payment methods** | yes / no toggle | When ON, only the merchant-picked payment methods are offered at checkout for orders containing a product from this category. When OFF, all installed methods work. |
| **Allowed payment methods** | Multi-select list | Visible when "Define custom payment methods" is ON. Picks from installed [[payment-provider|Payment Providers]]. AND-combined across cart products — see [[category-entity-business-rules]]. |
| **Define custom shipping methods** | yes / no toggle | Same pattern as above for shipping. |
| **Allowed shipping methods** | Multi-select list | Visible when "Define custom shipping methods" is ON. Picks from installed [[shipping-provider|Shipping Providers]]. |
| **Technological delivery time** (`make_interval`) | Integer hours | Production / lead time in hours. When set, the customer's earliest delivery slot at checkout is pushed beyond the max `make_interval` of all cart products. Drives build-to-order / custom-cut logic via [[apps-shipping-hours]]. Visible only when the platform's delivery-time flag is enabled. |
| **SEO title** | `<title>` tag override | Falls back to the category name when empty. |
| **SEO description** | `<meta name="description">` override | Falls back to a truncation of the description when empty. |
| **URL handle** | URL slug for the category page | Auto-generated from the name (lowercase, hyphens, accent-stripped) when empty. Prefixed with `/category/` on the storefront (`/category/<slug>`). Must be unique across all categories. Renames generate 301 redirects — see [[category-entity-business-rules]]. |
| **Sort order** | Integer | Position within siblings on storefront listings and admin organize tab. Lower = earlier. Tie-break by ID. Auto-assigned to `MAX(siblings) + 1` on create. |
| **Color** | Color tag | Optional admin-UI / icon color (not customer-facing). |
| **Icon** (`icon` / `icon_data`) | Icon file + metadata | Optional icon shown on storefront menu navigation (depending on theme). |
| **Image dimensions** (`width`, `height`, `max_thumb_size`) | Per-category image hint | Merchant-controlled — defines recommended image dimensions for this category. Not a hard cap. |
| **Background** | Background asset | Storefront category landing image. |
| **SEO generated through spinner** (`seo_generated_through_spinner`) | yes / no | Marker that the SEO description came from [[apps-seo-spinner]] — used to count Spinner-generated content against that app's plan cap. |
| **Products count** (`real_products_count`) | Read-only count | How many products are directly assigned to this category. Shown as a column on [[products-categories]]. Computed as DISTINCT product IDs to avoid duplicate counting when a product is in multiple categories. |
| **Properties count** (`properties_count`) | Read-only count | How many [[category-property|Category Properties]] are attached to this category. |
| **Path level** (`category_path.level`) | Per-category depth row | Materialised path table stores one row per (descendant, ancestor) pair with the level. Drives breadcrumbs, descendant filtering, and the 6-level depth cap. Rebuilt on every parent change for the whole subtree — see [[category-entity-side-effects-and-api]]. |

## Required-field validation

- **Name** — required. Save fails with *"This field is required"* when empty.
- **Name uniqueness** — validated against direct siblings only (same `parent_id`). Save fails with *"This name is already taken"* on duplicate.
- **URL handle uniqueness** — globally unique across all categories. On the Add / Edit modal, duplicates are REJECTED with a validation error. On the CSV / XML import path, the platform silently appends `-1`, `-2`, ... — see [[category-entity-business-rules]].
- **Depth cap** — moving / creating beyond 6 levels fails with *"category.err.max_depth_is_6"* / *"Max depth is 6"*. The platform's `category_max_level = 6` constant blocks the save.
- **Parent must not be self or own descendant** — the parent dropdown filters these out; the drag-drop reorder validates it transactionally. (verify)

## Multi-language storage

For multi-language stores ([[multi-language]]), the Name, Description, SEO title, SEO description, and URL handle are stored **per-locale**. The Google Shopping taxonomy assignment is **store-wide** (not per-language). The image, sort order, icon, and color are also store-wide. See [[category-entity-business-rules]].

## Where it appears

- [[products-categories]] — the Add / Edit modal where these fields are surfaced.
- [[products-products]] — the product editor's category-picker shows the Name + breadcrumb path.
- [[apps-csv-import]] — CSV / XML imports write to these fields (with the duplicate-handle auto-suffix exception).
- [[apps-google-shopping]] — reads `taxonomy_id` for the feed.
- [[apps-seo-spinner]] — writes the SEO description and sets `seo_generated_through_spinner`.
- [[api-categories]] — JSON-API v2 read / write surface.

## Related

- [[category]] — hub.
- [[category-entity-business-rules]] — display-subcategory toggle, payment / shipping intersection, name uniqueness, URL-handle redirects, sort-order auto-assignment, multi-language scope, SEO defaults.
- [[category-entity-lifecycle]] — depth cap, name uniqueness, URL-handle redirects (lifecycle context).
- [[category-entity-relationships]] — what other entities link to these fields.
- [[category-entity-side-effects-and-api]] — what fires when these fields are saved.
- [[category-property]] — the per-category properties referenced by `properties_count`.
- [[payment-provider]] / [[shipping-provider]] — referenced by the per-category restriction fields.
- [[settings-files]] — where the image lives.

## Open Questions

- Confirm parent-must-not-be-self-or-own-descendant validation against current admin form behaviour (verify).
