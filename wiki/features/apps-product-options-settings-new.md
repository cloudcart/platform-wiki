---
type: feature
nav_path: "Products → Options → Settings (modern)"
route_name: apps.product_options.settings.new
route_path: /admin/products/options-new
aliases: ["Product Options Settings (modern)", "Options settings new", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, product-options, settings, modern-vue]
plan_gates: []
created: 2026-05-21
updated: 2026-08-06
source_count: 3
---
# Product Options → Settings (modern Vue)

## Purpose

The **modern Vue version** of the Product Options Settings — replaces [[apps-product-options-settings-new]] (legacy) with a CcDomain-based UI. Equivalent functionality, refreshed UX.

For the full Product Options feature set, see [[products-options-overview]].

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **option** — every option in the options list has its own **Status** (Active) toggle, see [[products-options-overview]].

## Where to find it

Sidebar → Products → Options (modern Vue). The Settings (`apps.product_options.settings.new`) is the index route at `/admin/products/options-new`. Separately, the Overview tab (`apps.product_options.overview.new`) is at `/admin/products/options-new/overview`.

## What the merchant can do here

Same store-wide defaults configuration as [[apps-product-options-settings-new]] but with:
- Modern Vue components (CcSettingsBox / CcCard).
- Better mobile / accessibility patterns.
- Live validation feedback.

Field set is equivalent — refer to the legacy variant for the detailed list.

### What the merchant CANNOT do here
- Configure per-product option groups — those live in [[products-products]] per-product editor.

## Settings & fields

Modern Vue uses the CloudCart design system (`CcSettingsBox`, etc.) for consistent UX with other modern pages.

## Business rules

### Modern Vue rollout

This page is gradually replacing [[apps-product-options-settings-new]] across merchants. Both exist during the rollout window; eventually the legacy retires.

### Permission
Standard apps permission scope.

## Programmatic access

Product options can be **read** via **JSON-API v2** — see [[api-product-options]] for the endpoint and field map. The endpoint is **APP-GATED**: it returns 404 when the Product Options app is not installed.

The API surface is **read-only**: integrations can enumerate options (name, type, scope, values, storefront name) but cannot create, edit, sort, or delete options through the API — those operations require this admin screen and the per-option endpoints documented in the parent hub.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

- [[products-options-overview]] — Product Options hub.
- [[apps-product-options-settings-new]] — legacy variant.

## Open questions

_None — questions outstanding have been resolved or moved to the parent hub._

## How it works (verified against backend)

### Option creation validation — supported types

The platform validates the option's `type` to be ONE OF:
- `checkbox` — multi-select boolean choices.
- `select` — dropdown single-select.
- `radio` — radio button single-select.
- `text` — single-line text input.
- `textarea` — multi-line text input.
- `file` — file upload (image-mime restricted: jpg, jpeg, png, bmp, webp).
- `length` — length-with-unit input.
- `weight` — weight-with-unit input.
- `square` — area / square measurement.
- `image` — image-based option (e.g., colour swatch with thumbnail).

Other types are rejected at save time. So **the merchant can pick from a fixed set of 10 option types** — no custom types allowed.

### Option scoping — 4 mapping levels

Every option group is scoped to ONE of these mappings:
- `product` — applies to a specific product (the merchant picks the product).
- `category` — applies to all products in the chosen category.
- `vendor` — applies to all products from the chosen vendor.
- `selection` — applies to a custom selection (e.g., a smart collection).

The `mapping` field is REQUIRED at save time, and the matching field (`product` / `category` / `vendor` / `selection`) is required-if for the chosen mapping. So the merchant **cannot have an unscoped global option** — every option group needs a target.

### Option values: choice-types require values; text/file/measurement types don't

For `select`, `radio`, `checkbox` option types, the merchant must define at least one `value.*` entry with a `name` (required, max 191 chars). Each value can have a numeric `amount` (price modifier) and an optional `thumb` (image — jpg/jpeg/png/bmp/webp).

For `text`, `textarea`, `file`, `length`, `weight`, `square`, `image` types, no `value.*` entries are required — these are single-input fields, not choice lists.

### Option thumbnails accept ONLY specific image formats

When the merchant attaches a thumbnail to an option value (e.g., a colour swatch image), the file MUST be one of: jpg, jpeg, png, bmp, webp. **SVG and GIF are rejected** at upload time. The validation enforces this via the application framework's `mimes:jpg,jpeg,png,bmp,webp` rule.

### Storefront-name field is separate from internal name

The merchant defines two name fields:
- `name` — internal (admin-facing) name, required, max 191 chars.
- `storefront_name` — customer-facing name, optional, max 191 chars.

If `storefront_name` is empty, the option's internal name is used on the storefront. This lets the merchant use technical names (e.g., "S-XL Size Select") internally while showing "Choose your size" to customers.

### Option sort order via dedicated endpoint

The sort order is changed via `POST /api/product-options/sort` (not as part of the option edit). This lets the merchant drag-reorder options without re-saving each one. The `GET /api/product-options/sort` returns the current order.

### Status toggle endpoint per option

Each option has an active/inactive status, toggled via `GET /api/product-options/status/{status_id}/{status?}`. So merchants can disable an option temporarily without deleting it (preserving any historical orders that referenced it).

### Modern Vue route falls back to a redirect controller

The modern route `/admin/product-options/{any?}` actually redirects via the platform code rather than serving a Vue page directly. The Vue app is reached after the redirect resolves. This is a transitional pattern — the URL works, but internal navigation flows through a redirect layer.
