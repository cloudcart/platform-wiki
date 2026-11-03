---
type: feature
nav_path: "Apps → Model"
route_name: apps.brand_model.model
route_path: /admin/brand_model/:id/model
aliases: ["Models", "Model list", "Brand models"]
tags: [administration, brandmodel, brand-model, model]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 9
---
# Model

## Purpose

The Model list page of the [[brand-model]] app — where the merchant manages **specific models under a single parent brand** (iPhone 15 Pro, Galaxy S24, Camry 2024). Each model row carries its own logo, description, SEO data, and active toggle. Products are attached to models from the product editor; each model belongs to exactly one brand.

This page is reached by clicking a brand row from [[brand-model-brand]]; the URL contains the brand ID (`/admin/brand_model/:brand_id/model`).

## Where to find it

Sidebar → Apps → Brand-Model (after install) → Brands → click a brand row → **Models** tab for that brand.

## What the merchant can do here

### Model list grid
- See all models belonging to the parent brand: ID, Model name, Products count, Active status — plus a per-row edit (click name) and delete affordance.
- Sort by `id`, `title`, `products_count`, `active`. Default sort: `id DESC` (newest first).
- Bulk-select for bulk-delete.
- See the parent brand's name + logo as a header (meta-context on the page).

### Filters
- **Status** — Active / Inactive.
- **Has products** — Yes / No (cleanup helper: models never used).
- **Product** — IS / IS NOT a specific product → "show me all models referenced by THIS product (or NOT)".
- **Free text search** on the model title.

### Add / Edit modal — fields

Clicking **Add new Model** or any row opens a right-side modal that does not close on backdrop click, with:
- **Model name** (`title`) — required, unique across all models in the store (not just this brand). Validation messages: *"Title is required"*, *"Title max characters is 191"*, *"Title must be unique"*.
- **Model logo** — single image upload.
- **Description** — rich-text editor; whatever is typed here is also written into the model's `seo_description` automatically.

The form is identical in structure to the Brand modal (see [[brand-model-brand]]) but labelled "Model" instead of "Brand". There is no year picker, no compatibility hint, no SKU pattern field. The modal header shows **Add new Model** (create) or the model's title (edit); header buttons are **Cancel** + **Save**.

### Status toggle

Each model has an **Active status** toggle on the grid — flipping a model between visible and hidden in the storefront filter without losing the product links.

### What the merchant CANNOT do here
- Move a model to a different brand (no "Change brand" action — recreate the model under the new brand and re-link products).
- Define which categories a model is restricted to.
- Specify a year or release date as a structured field (only free-text description).
- Edit the URL handle or SEO title independently from the model name — both are auto-derived.
- See which specific products are linked to this model from this page (the Products count is informational; drill in via [[products-products]] filter on Brand-Model).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Model name** (`title`) | Display name in the storefront filter and product editor picker | empty | Required; max 191 chars; unique store-wide across all models |
| **Model logo** | Image shown next to the model on the storefront filter / model landing page | none | Single image upload |
| **Description** | Body copy for the model storefront page | empty | Rich-text editor |
| **Active status** | Controls visibility on the storefront filter | `1` (active) | Toggle from the grid |
| **Brand** (auto, from URL) | Parent brand the model belongs to | derived from `:brand_id` route param | Cannot be changed after create — to move, recreate + re-link |
| **URL handle** | Slug for `/model/<handle>` storefront URL | auto = title | Not editable from the modal |
| **SEO title** | `<title>` for storefront model page | auto = title | Not editable from the modal |
| **SEO description** | `<meta description>` | description text | Auto-set from description on save |
| **Background colour** | Optional per-model background colour (`background` hex column on the table) | none | Stored as a 7-char hex string; not exposed in the create/edit modal — may be used by some storefront themes |

## Business rules

### Belongs to ONE brand

Every model belongs to exactly one brand. When the parent brand is removed, all of its models are removed with it. Models cannot be shared across brands; if "iPhone 15 Pro" also makes sense under another brand label, the merchant must duplicate it.

### Delete is blocked when products attach

Deleting a model that still has products linked returns HTTP 422 — *"Some brand models still has products: {model titles}"*. The merchant must remove or reassign those product links from [[products-products]] (Brand-Model section) first. If the model has **no products**, deletion proceeds. Bulk-delete follows the same rule — one blocked model fails the batch.

### Soft-disable via Active status

Toggling Active to `0` keeps every product link intact, hides the model from the storefront filter, but still shows it in the admin Models list (filter by `active=0` to find disabled models). This is the recommended path for retiring a model (e.g., iPhone 12) without losing historical product associations.

### Title uniqueness across ALL models

The `title` uniqueness check is **store-wide across all models**, not scoped per brand. Two brands cannot both have a model called exactly "Pro". The merchant typically disambiguates with a brand-specific prefix (e.g., "iPhone Pro" vs "Galaxy Pro").

### Brand reference follows the model

In the product editor the merchant only ever picks a model; the brand reference follows automatically from that model's own brand on every save. Linked products always stay attached to the model's current brand.

### Storefront filter updates on rename

Renaming a model's `title` re-syncs every linked product variant so storefront filter labels reflect the new name immediately; deleting a model removes it from those filter labels (after a few seconds' delay). Changing only the logo, description, or SEO fields does NOT trigger this re-sync — only `title` changes do. See [[apps-listing-engine]].

### Storefront URL pattern

Each model has its own landing page at `/model/<url-handle>`, separate from the parent brand page. SEO meta tags come from the model's own `seo_title` / `seo_description` (defaulting to the title).

### Permission

This page requires the Brand-Model app to be **installed** and the merchant to have the `apps` permission.

## Related

- [[brand-model]] — parent overview.
- [[brand-model-brand]] — parent brand catalog.
- [[products-products]] — products linked to models.
- [[products-variants-options]] — for sub-model distinctions like storage / colour.
- [[apps-listing-engine]] — search index that propagates model changes.

## Open questions

- Whether the `background` hex colour column is exposed in any current theme — it exists on the DB row but no admin field surfaces it.
- Whether moving a model between brands is supported through any path (API, importer) other than recreate.
- Whether per-brand uniqueness for model titles is on any roadmap — current global uniqueness can be surprising for stores carrying many overlapping product lines.
