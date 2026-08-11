---
type: feature
nav_path: "Apps → OLX → Configuration"
route_name: apps.olx.configuration
route_path: /admin/apps/olx/configuration
aliases: ["OLX Configuration", "OLX Category mapping", "OLX category map"]
tags: [apps, olx, marketplace, category-mapping, taxonomy]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 2
---
# OLX → Configuration (Category mapping)

## Purpose

The **Configuration** tab is where the merchant maps **CloudCart categories to OLX categories**. OLX has its own product taxonomy (per country) — every advert published to OLX MUST be classified into an OLX category. Since CloudCart's categories don't match OLX's structure 1:1, the merchant manually defines which CloudCart category corresponds to which OLX category, AND which OLX parameters apply.

Without category mapping, products from those CloudCart categories cannot be published to OLX (the publish would fail with `err.category_not_choosen` per [[apps-olx]]).

The page builds a table of all defined mappings. Per row:
- The CloudCart category.
- The mapped OLX category.
- Parameters configured for that mapping ([[apps-olx-parameters]]).

For the OLX feature set, see [[apps-olx]].

## Where to find it

Sidebar → Apps → OLX → **Configuration tab**. Route: `/admin/apps/olx/configuration`.

## What the merchant can do here

### Category mappings list

Standard data table with pagination + search. Per row:

| Column | Source component |
|---|---|
| **CloudCart category** (`SiteName` / `TableSiteCategoryName`) | The store-side category. |
| **OLX category** (`OlxName` / `TableOlxCategoryName`) | The OLX-side category it maps to. |
| **Parameters** (`TableParameters`) | Indicator showing if parameters are mapped — link to [[apps-olx-parameters]]. |
| **Actions** (`TableDelete`) | Delete the mapping. |

### Add a category mapping

Click **+ Add category** (`translations['Add category']`) — opens the `TableEditMapping` modal which:
1. Picks a CloudCart category (autocomplete from the catalog).
2. Picks the corresponding OLX category (autocomplete from OLX's taxonomy via the connected API).
3. Saves the mapping.
4. Triggers redirect to [[apps-olx-parameters]] for the new mapping so the merchant can map parameters.

### Edit a category mapping

Clicking an existing row opens the same modal pre-filled. The merchant can change the OLX category, which typically resets the parameter mapping (different OLX categories have different required parameters).

### Delete a category mapping

Per-row delete via `TableDelete`. Removing a mapping means products in that CloudCart category cannot publish to OLX anymore.

### What the merchant CANNOT do here
- Publish a product without mapping its CloudCart category to OLX (publishing surfaces `err.category_not_choosen`).
- Map ONE CloudCart category to MULTIPLE OLX categories (1:1 model — each CloudCart category has exactly one OLX mapping).
- Skip parameter mapping for OLX categories that require parameters — the platform will refuse publishing.

## Settings & fields

### Mapping data structure (per row)

| Field | Notes |
|---|---|
| **CloudCart category ID** | From the merchant's catalog. |
| **OLX category ID** | From OLX's API category tree. |
| **OLX category path** | The full path (e.g., "Electronics > Phones > Smartphones"). |
| **Required parameters** | OLX may declare some attributes mandatory for this category (Brand, Condition, etc.) — surfaced in [[apps-olx-parameters]]. |

### Table actions

- `TableEditMapping` modal — create / edit mapping.
- `TableParameters` — link / indicator for the per-mapping parameters configuration.
- `TableDelete` — remove mapping with confirmation.

## Business rules

### Per-mapping parameter requirement

OLX's API publishes each advert with category + parameters. Different OLX categories have different REQUIRED parameter sets:
- "Electronics > Phones" requires Brand + Condition + Memory.
- "Real Estate" requires Square meters + Number of rooms + Build year.
- "Cars" requires Brand + Model + Year + Mileage + Fuel type.

Once the merchant picks the OLX category, the platform fetches its required parameters and surfaces them in [[apps-olx-parameters]] for mapping.

### Cascade behavior

Changing a CloudCart category's mapping:
- Re-syncs the parameter list (new OLX category may have different required parameters).
- Existing OLX adverts in that mapping STAY active (they keep their original category) but new publishes use the new mapping.

### Side effects on save
- The new mapping is persisted.
- The merchant is typically redirected to [[apps-olx-parameters]] for the new mapping to set up parameters.

### Permission
Standard apps permission scope.

## Related

- [[apps-olx]] — OLX hub.
- [[apps-olx-parameters]] — per-mapping parameter setup (next step after Configuration).
- [[apps-olx-parameters-values]] — per-parameter value mapping.
- [[apps-olx-products]] — products published using these mappings.
- [[products-categories]] — source CloudCart categories.

## How it works (verified against backend)

### OLX category tree auto-refreshes every 30 days

The OLX category-populate interval is 2,592,000 seconds = 30 days. The OLX category tree is fetched via a background populate job and only re-fetched after the 30-day interval lapses. Categories added on OLX's side mid-month do not appear immediately.

### Each OLX country has its own category tree

The country selected in Settings determines which OLX category tree the merchant sees. Switching country (after disconnect/reconnect) shows a different category taxonomy.

### Restricted-category warning surfaces from OLX

Per the lang key `err.invalid_category` — "This category requires additional product information. Please add the advert through the OLX's website." Some OLX categories (vehicles, real-estate) require advert fields that CloudCart's integration cannot fill — the merchant gets directed to use OLX's UI for those.

### Subcategory required — top-level rejection

Per the lang key `err.parent_category` — "Choose a subcategory". OLX only accepts leaf-category mappings. Picking a parent (non-leaf) category triggers this error.

### Category list refreshable

The `PopulateCategories` / `PopulateCategoryAttributes` jobs can be triggered through the queue mapping (`olx_categories`, `olx_categories_attribute`). The merchant cannot manually re-trigger from the UI — refresh happens monthly via the populate jobs.

### No bulk import for category mappings

There is no CSV / file import for category mappings. Every CloudCart category that the merchant wants to publish has to be mapped one at a time using the **+ Add category** modal. For a store with 100 categories, that means 100 separate save operations.

### No auto-suggest by category name

The platform does not auto-suggest an OLX category based on the CloudCart category name. The merchant has to find the matching OLX category manually for each mapping, even when the names are very close.

### Category mappings scoped by endpoint_id — different per country

The `CategoryMap` model uses an `Endpoint` scope — every query is automatically filtered by the current `endpoint_id`. So when the merchant switches countries (disconnect + reconnect to a different OLX country), the mappings from the previous country don't appear and don't apply. This is why disconnect-truncate makes sense: mappings are country-specific.

### Categories carry an OLX picture_limit per category

Each OLX category has its own `picture_limit` (the max number of photos allowed for an advert in that category). This is fetched as part of the OLX category metadata and stored locally. The product formatter respects this limit when uploading images — different categories accept different counts (e.g., real estate may allow more than electronics).

### Mapping save is per-mapping — no transactional batch

Each "Add category" submission saves one mapping at a time. There is no transactional batch where the merchant configures 50 mappings client-side and submits them in one go. Bigger catalogs require sequential save operations, which makes initial onboarding slow.

## Open questions
