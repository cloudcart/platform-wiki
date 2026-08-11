---
type: feature
nav_path: "Apps → Brand"
route_name: apps.brand_model.settings
route_path: /admin/brand_model/brand
aliases: ["Brands", "Brand list", "Brand catalog"]
tags: [administration, brandmodel, brand-model, brand]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 9
---
# Brand

## Purpose

The Brand list page of the [[brand-model]] app — where the merchant maintains the **top-level brand catalog** (Apple, Samsung, Toyota, Canon) that products are sold by compatibility against. Each row is a brand with a logo, description, and SEO metadata; clicking a row opens the [[brand-model-model]] sub-page for that brand. Brands are the parent of models in the two-level brand → model hierarchy.

This page is only available when the Brand-Model app is installed (see [[brand-model]]).

## Where to find it

Sidebar → Apps → Brand-Model (after install) → **Brands** tab.

The route is `/admin/brand_model/brand`.

## What the merchant can do here

### Brand list grid
- See all brands in a paginated table: ID, Brand name, Models count, Products count, Active status — plus a per-row edit (click name) and delete affordance.
- Sort by `id`, `title`, `models_count`, `products_count`, `active`. Default sort: `id DESC` (newest first).
- Bulk-select rows for bulk-delete via the standard table actions.

### Filters
The list filter bar exposes:
- **Status** — Active / Inactive (the `active` toggle on each brand).
- **Has models** — Yes / No (cleanup helper: find brands that have no models attached yet).
- **Has products** — Yes / No (cleanup helper: brands never linked to a product).
- **Product** — IS / IS NOT a specific product → "show me all brands referenced by THIS product (or NOT)".
- **Free text search** on the brand title (`query` parameter).

### Add / Edit modal — fields

Clicking **Add new Brand** or any row opens a right-side modal (`b-modal` class `modal-right`, size `lg`, `no-close-on-backdrop=true`) with:
- **Brand name** (`title`) — required, unique store-wide. Validation messages: *"Title is required"*, *"Title max characters is 191"*, *"Title must be unique"*.
- **Brand logo** — `LogoSection` single image upload (drag-and-drop or click-to-pick) bound to `has_image` + `imageFile`.
- **Description** — `TextEditor` rich-text editor. The editor's `update-text` event also writes the same content into the brand's `seo_description` automatically.

That's the entire form. There is no parent-brand picker, no sort priority, no year, no category mapping.

The modal header shows **Add new Brand** (create) or the brand's title (edit). Header buttons: **Cancel** (closes) and **Save** (spinner during submit). Body is a `b-card` containing the three fields above. On success the toast reads *"Successfully created"* / *"Successfully edited"* (or *"Saved successfully"*).

#### Endpoints used by the modal
- Create — `POST /admin/api/brand_model/create` (multipart/form-data).
- Edit — `POST /admin/api/brand_model/edit/{id}` (multipart/form-data).

### Status toggle

Each brand has an **Active status** column on the grid — a switch that flips the brand between active and inactive without leaving the list. Inactive brands are hidden from the storefront filter but their product links and child models remain intact.

### What the merchant CANNOT do here
- See the brand's child models without clicking through to [[brand-model-model]].
- Reassign products from one brand to another in bulk (the link is stored per model, not per brand directly).
- Merge two brands (e.g., "Apple" + "Apple Inc.") — must manually reassign all child models, products, then delete the empty brand.
- Set the URL handle or SEO title separately from the brand name — both are auto-derived.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Brand name** (`title`) | Display name; appears on storefront brand pages, model picker, breadcrumbs | empty | Required; max 191 chars; unique per store (case-sensitive at DB level, error: "Title must be unique") |
| **Brand logo** | Logo shown on the storefront brand page and category cards | none | Single image; stored in `brands/images/` |
| **Description** | Body copy for the brand storefront page | empty | Rich-text editor; stored as HTML |
| **Active status** | Controls visibility on the storefront filter | `1` (active) | Toggle from the grid; does NOT delete data |
| **URL handle** | Slug for `/brand/<handle>` storefront URL | auto-derived from title | Not editable from the modal — the platform writes `url_handle = title` on save |
| **SEO title** | `<title>` for the storefront brand page | auto = brand name | Not editable from the modal — the platform writes `seo_title = title` on save |
| **SEO description** | `<meta description>` for the brand page | description text | Set from the description editor; max ~text-column length |

## Business rules

### Two-level hierarchy

Brand is the top level of the [[brand-model]] hierarchy. Brand → Model. There is no third level — to express variants like "iPhone 15 Pro 128GB" vs "256GB", the merchant uses Brand=Apple, Model=iPhone 15 Pro and then product **variants** (see [[products-variants-options]]) for storage capacity.

### Delete is blocked when products attach

Deleting a brand that still has products linked (via its models) returns HTTP 422 — "Some brands still has products: {brand titles}". The merchant must reassign or remove those products via [[products-products]] (Brand-Model section) first.

If the brand has **models but no products**, deletion proceeds and:
- Every child model is hard-deleted via the brand's `deleted` lifecycle hook.
- All `ProductToBrandModel` rows for those models are removed in the same hook.
- A `CASCADE` foreign key on the `models` table reinforces the cleanup at the DB layer.

Bulk-delete follows the same rules — one blocked brand fails the batch.

### Soft-disable via Active status

Toggling Active to `0` from the grid:
- Keeps every model and product link intact.
- Hides the brand from the storefront brand list and the brand-model filter.
- Allows quick re-activation without re-creating data.

This is the recommended way to "retire" a brand (e.g., a manufacturer the store no longer carries) while preserving SEO URLs and product history.

### URL handle uniqueness

Storefront brand URLs use `/brand/<url-handle>/`. Two brands cannot share a handle. Because the platform writes `url_handle = title`, brands with identical titles fail uniqueness at the title level first.

### Listing engine integration

Renaming a brand title does NOT trigger a brand-specific listing-engine re-index — only **model renames** are listened to (see [[brand-model]]). Brand-name changes propagate naturally on the next variant sync.

### Permission

This page is gated by the generic `apps` API permission. The middleware also checks that the Brand-Model app is **installed**; if uninstalled, every brand endpoint returns 403/404 except `install`.

## Related

- [[brand-model]] — parent overview page.
- [[brand-model-model]] — child models of each brand.
- [[products-products]] — products linked to brand → model combinations.
- [[products-vendors]] — distinct flat vendor taxonomy (don't confuse).
- [[apps-listing-engine]] — search index that brand changes propagate to.

## Open questions

- Bulk-import path for brands (CSV / XML) — exists via [[apps-csv-import]] / [[apps-xml-import]]? Verify field mapping.
- Whether brand storefront pages support landing copy / hero block beyond the description rich-text.
- Whether the "Has models" filter is intended for cleanup or for product attribution — current copy treats it as cleanup-only.
