---
type: feature
nav_path: "Apps → OLX → Products → Pipeline"
route_name: apps.olx.products
route_path: /admin/apps/olx/products
aliases: ["OLX Products pipeline", "OLX products data table", "OLX Add advert modal"]
tags: [apps, olx, marketplace, products, publishing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# OLX → Products — the publishing pipeline UI

> Part of [[apps-olx-products]]. See the hub for the other aspects (validation, sync, payload formatting).

## Purpose

This aspect covers the **Products tab UI itself** — the data table, filters, empty state, the **+ Add advert** picker modal, and the bulk-publish loop that turns a multi-product selection into individual OLX adverts. Each row shows a CloudCart product and its OLX publication state.

## Where to find it

Sidebar → Apps → OLX → **Products tab**. Route: `/admin/apps/olx/products`. The Vue uses `app-name="olx"` for the data-table state.

## What the merchant can do here

### Add advert (`modalAdvert`)

The top-level **+ Add advert** button (icon `far fa-plus`, label `translations['Add advert']`) opens the `Helpers/addAdvert.vue` modal — a **single-screen** picker (no wizard, no steps):

| UI element | Behaviour |
|---|---|
| **Choose products** multi-select (`products`) | Tag-mode autocomplete (`SelectWithAjax mode="tags"`) backed by `/admin/api/olx/products/autocomplete`. Label: *"Choose products to be published in OLX. Only those products that belong to configured categories are visible."* The autocomplete pre-filters the dropdown — see [[apps-olx-products-validation]] for exactly which products are excluded. |
| **Cancel** button | Closes the modal and resets state. Disabled while `isLoading = true`. |
| **Submit** button | Disabled when `products.length < 1` OR `isLoading`. Calls `POST /admin/api/olx/products/upload` with `{ids: products}` and emits `upload` on success. |

The modal is **deliberately minimal** — there is NO per-product category override, NO per-product parameter override, NO image picker, NO title editor. Every selected product is pushed with the auto-generated payload (see [[apps-olx-products-formatting]]).

After a successful publish, the listing refreshes via the `@upload="updateTable"` event handler.

### Products data table

| Column | Source component |
|---|---|
| **Product name** (`ProductName` / `TableProductName`) | CloudCart product name + thumbnail. |
| **Created date** (`ProductCreated` / `TableProductCreated`) | When the OLX advert was created. |
| **Valid** (`ProductValid` / `TableProductValid`) | Whether the product passes OLX's validation rules — checkmark / X icon. See [[apps-olx-products-validation]]. |
| **Status** (`ProductUpdateStatus` / `TableProductChangeStatus`) | OLX advert status — Active / Pending / Rejected / Expired, with a toggle action. |
| **Actions** (`ProductAction` / `TableProductActions`) | Re-publish, edit, view on OLX, delete. |
| **Delete** (`TableDelete`) | Remove from the OLX publishing pipeline. |

### Filter / search

Standard filter UI: by product name, by validation status, by OLX status, by date.

### Empty state

When no products are added yet, the tab shows a friendly empty state with a prominent **+ Add advert** button.

### What the merchant CANNOT do here

- Add products without category mapping ([[apps-olx-configuration]]) — they are pre-filtered from the picker.
- Add products in an OLX-restricted category (alcohol, weapons, etc. — varies by country).
- Bulk-publish more products than OLX's daily publish-limit allows (verify rate limits per country).
- Override an OLX rejection — the merchant must fix the underlying issue and re-publish.

## Settings & fields

The tab carries no settings of its own; toggles live on [[apps-olx-settings]]. The `upload` endpoint returns `{uploaded, errors, total, data}`. The post-submit toast displays:

- If `errors === total`: error toast *"An error occurred while adding products to OLX, you can find more information in the Product Events section"*.
- Otherwise: success toast *"Added {uploaded} products out of {total}, {errors} products with errors"*.

After Submit the modal closes regardless of outcome — the merchant must open [[apps-olx-history]] to see per-product error detail.

## Business rules

### Bulk publish — backend loops per product

The merchant selects N products and clicks Upload. The platform loops the product IDs, publishes each advert to OLX one at a time, and returns `{errors, uploaded, total, data}`. So the merchant queues 100 products from one action, but each is published as a separate OLX API call — there is no native batch endpoint.

### Each product is one advert

Each product publishes as a SEPARATE OLX advert. When the `merge_product` setting is on, a single product can fan out into one advert PER variant — see [[apps-olx-products-formatting]] for the variant-split behaviour.

### Permission

Standard apps permission scope.

## Related

- [[apps-olx-products]] — hub.
- [[apps-olx]] — OLX feature hub.
- [[apps-olx-adverts]] — active adverts on OLX (sister view).
- [[apps-olx-history]] — per-product error detail after a publish.
- [[apps-olx-settings]] — the sync + formatting toggles referenced by the table actions.
- [[products-products]] — source CloudCart products.

## Open questions

- Per-country OLX daily publish-limit / rate limits (verify).
