---
type: feature
nav_path: "Apps → Brand-Model"
route_name: apps.brand_model.overview
route_path: /admin/brand_model
aliases: ["Brand Model", "Brand-Model catalog", "Device compatibility", "Brand & Model", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, catalog, brands, models, compatibility]
plan_gates: ["brand_model"]
created: 2026-05-22
updated: 2026-08-06
source_count: 12
---
# Brand-Model (device compatibility catalog)

## Purpose

**Brand-Model** is an installable app that adds a **two-level brand + model catalog**, used by merchants who sell by device compatibility. Classic use case: a phone-accessories shop where each product (case, screen protector, charger) is filtered by phone brand (Apple / Samsung) → specific model (iPhone 15 Pro / Galaxy S24). The same pattern fits car parts, laptop accessories, photography gear — anything compatibility-driven.

When installed, the merchant manages a Brand → Model taxonomy and products gain a "Brand-Model" assignment field; the storefront then exposes a brand-then-model filter on category pages.

This page is the **hub**. The two list screens live on their own pages — drill into the one that matches the question.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **brand or model** — each row has its own Active toggle in the list grid, and an inactive entry drops out of the storefront filter while its product links stay intact.

## Where to find it

Sidebar → Apps → install → **Brand-Model**. Route `/admin/brand_model`. Two sub-pages:

- [[brand-model-brand]] — manage the top-level brand catalog (Apple, Samsung, Toyota).
- [[brand-model-model]] — manage models per brand (iPhone 15 Pro, Galaxy S24); reached by clicking a brand row.

## What the merchant can do here

- Create / edit / delete brands — see [[brand-model-brand]] for the grid, filters, and modal fields.
- Create / edit / delete models per brand — see [[brand-model-model]].
- Tag products with brand + model combinations via a multi-select picker on the product editor (see [[products-products]] "Brand-Model" section). The picker is really a **model-picker** — the brand is derived from the chosen model.
- Soft-disable a brand or model via its **Active status** toggle (retire without losing product-link history).
- Bulk import / export brand-model data via [[apps-csv-import]] / [[apps-xml-import]] (verify field mapping).

### What the merchant CANNOT do here

- Use Brand-Model and [[products-vendors]] interchangeably — vendors are a flat list (single vendor per product); Brand-Model is hierarchical (brand → model) and allows multi-assignment.
- Auto-detect compatibility from product data — mapping is manual.
- Nest a third level. Brand → Model is the cap; finer distinctions (iPhone 15 Pro 128GB vs 256GB) use product variants — see [[products-variants-options]].

## Settings & fields

The brand and model edit forms share the **same three fields** (see [[brand-model-brand]] / [[brand-model-model]] for the full per-field tables):

- **Title** (required, ≤ 191 chars, unique store-wide) — labelled "Brand name" or "Model name".
- **Logo** — single image upload.
- **Description** — rich-text editor; its content is also written into `seo_description` on save.
- **Active** toggle — set from the list grid, not from the modal.

Both brand and model carry their own SEO metadata (`seo_title`, `seo_description`, `url_handle`), producing storefront URLs `/brand/<handle>/` and `/model/<handle>/` with independent meta tags. **`url_handle` and `seo_title` are auto-derived from Title** — the modal does not expose them for editing; customising a handle or SEO title needs an importer / API path (verify).

There are **no** fields for parent-brand nesting, sort priority, year, or category mapping — earlier wiki claims to that effect were incorrect; the schema is flat (Brand → Model only). Models also carry an optional `background` hex colour column that no admin field surfaces — see [[brand-model-model]].

## Business rules

### Two-level hierarchy

- **Brand** = manufacturer (Apple, Samsung, Toyota).
- **Model** = specific product line (iPhone 15 Pro, Galaxy S24, Camry 2024).

Each brand has many models; each model belongs to exactly one brand. There is no third level.

### Multi-assignment per product

A single product (e.g. a USB-C charger) can be tagged with many combinations — compatible with iPhone 15 Pro **and** Galaxy S24 **and** Pixel 8. This drives the storefront compatibility filter.

### Storefront filter

When the app is installed, category pages expose a **two-step** filter: customer picks brand (Apple) → picks model (iPhone 15 Pro) → listing narrows to compatible products. The filter scopes to **active** brands and models only — an inactive brand or model disappears from the public filter while its product links stay intact internally. Re-activation restores visibility immediately.

### Brand is derived from the model

Products link to **models**, not brands directly. On every product save the brand reference is silently set from the chosen model's parent brand — so the merchant only ever selects models; brands appear in the picker tree as parents for selection convenience.

### Product change history

Brand-model edits are recorded in the product's [[products-change-log|Change log]]: attached / detached entries formatted as "Apple: iPhone 15 Pro", so the merchant can see compatibility changes per row.

### Delete blocks when products attach

Deleting a brand or model that still has products linked is **blocked** (HTTP 422, with a message listing the blocked titles). The merchant must first reassign or remove those product links from [[products-products]]. A brand with **models but no products** deletes cleanly — child models and their product-link rows cascade away. Full mechanics on [[brand-model-brand]] / [[brand-model-model]].

### Soft-disable vs delete

Toggling **Active** to off keeps every model and product link intact and only hides the entry from the storefront filter. This is the recommended way to retire a brand or model (a manufacturer no longer carried, an end-of-life model) while preserving SEO URLs and product history.

### Distinct from Vendors

[[products-vendors]] is a **flat** taxonomy, one vendor per product, answering "made by X". Brand-Model is **hierarchical** (Brand → Model), many per product, answering "compatible with model X".

### Search index integration

Brand-model changes propagate to the storefront search index automatically: renaming a **model** re-syncs every linked product, and deleting a model removes it. **Brand** renames are not listened to (only model changes fire), so after a brand rename the merchant may need to nudge each model or wait for the next re-index. See [[apps-listing-engine]].

### Catalog-only, not order-lifecycle

Brand-Model is purely a catalog hierarchy: it runs only when a product is saved, never on the order timeline. It does not touch stock, fulfilment, or order status.

### Permission

All brand and model admin operations sit behind the generic `apps` permission **and** require the app to be **installed** — uninstalling blocks every operation even with data tables intact (install is the only exception).

## Plan gates

This app is gated by the plan-feature below (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `brand_model` | Access gate (install URL) | The install URL `/admin/apps/brand_model/install` is blocked when the plan lacks the feature, and the app is hidden from the Apps catalog for those plans. |

Lower plans cannot install the app. Existing installs keep working on plan downgrade until the merchant cancels — see [[plan-vs-feature-pack]] for downgrade rules.

## Related

- [[product-compatibility]] — the compatibility / fitment concept this app powers.
- [[apps]] — App Store.
- [[brand-model-brand]] — brands sub-page (grid, filters, modal, delete rules).
- [[brand-model-model]] — models sub-page (grid, filters, per-model SEO).
- [[products-products]] — products tagged with brand-model.
- [[products-variants-options]] — sub-model distinctions like storage / colour.
- [[products-vendors]] — distinct flat vendor taxonomy.
- [[products-categories]] — products are still categorised separately.
- [[apps-listing-engine]] — search index that brand-model changes propagate to.
- [[apps-csv-import]] / [[apps-xml-import]] — bulk import path.

## Open questions

- Bulk-import field mapping for brands / models via [[apps-csv-import]] / [[apps-xml-import]] — verify.
- Whether any current theme reads the per-model `background` hex colour column.
- Whether customising `url_handle` / `seo_title` independently of Title is possible via importer or API.
