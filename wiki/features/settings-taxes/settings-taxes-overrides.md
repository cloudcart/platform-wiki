---
type: feature
nav_path: "Settings → Taxes and fees → Per-category and per-region overrides"
route_name: taxes.create
route_path: /admin/settings/taxes/tax/:id?
aliases: ["Tax overrides", "Per-category override", "Per-region override", "Override precedence", "Books at 9%", "Tax overrides storage", "Category override ladder"]
tags: [settings, taxes, overrides, categories, regions, vat]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-taxes]]. See the hub for the other aspects (VAT rules, fees, pricing display, OSS / no-VAT, validation, integrations).

# Taxes and fees — per-category and per-region overrides

## Purpose

Documents how a single Tax row can carry a list of **rate overrides** — exceptions that swap in a different rate for a specific product category, a specific region within the parent zone, or both. Common pattern: a 20% VAT base with a 9% override for the Books category. Both override types share ONE storage table (`tax_overrides`) and are distinguished by which columns are populated. The override-matching ladder is **NOT** what merchants typically expect — a category override silently beats a region override on the same line item — so this page captures the exact precedence the engine uses.

## Where to find it

Inside the Tax / Fee edit form: the **Regions exceptions** section (row builder for per-region overrides) and the **Categories exceptions** section (row builder for per-category overrides). Form route: `/admin/settings/taxes/:type/:id?`.

The two sections render via separate `CcSettingsBox` slots (`regionsExceptions`, `categoriesExceptions`) but the data goes into the **same** underlying storage on save.

## What the merchant can do here

### Categories exceptions section

A repeating row builder. Bottom of the section has an **+ Add override** link that appends a new blank row. Per row:

| Column | Notes |
|--------|-------|
| **Description** | Required free-text. Used as the line description on the customer's invoice when this override is applied. |
| **Region** | Only shown when (a) the parent tax targets a regional zone AND (b) the store has a Google Maps API key. Uses Google Places autocomplete (legacy or new API depending on `google_map_api_version`). Captures `text`, `country_name`, `state_iso_2`, `admin_zone_1_name`, `admin_zone_1_iso`, `locality`, `city_id`, `lat`, `lng`, `timezone` from the chosen place. |
| **Category** | Required dropdown — searchable via `/admin/api/core/product-categories/search`. |
| **Amount** | Percent input, 2-digit precision. Required. |
| **Remove (×)** | Per-row delete icon. No confirmation. |

### Regions exceptions section

Same row-builder pattern but per-region (no Category column) — used for taxes that have one base rate plus a few region-specific deviations within the same zone.

## Settings & fields

### Shared `tax_overrides` storage

The merchant configures sub-region overrides via the `regions[]` array and per-category overrides via the `categories[]` array on the same form. **Both arrays are merged into one set on save and persisted to a SINGLE `tax_overrides` storage**, distinguished only by which columns are populated:

- **Region-only override row** — `state_iso_2` is populated (from Google Places' `admin_zone_1_iso` field captured during the place lookup), `text` is the place name, `category_id` is `null`. Used for *"this state inside the EU zone has a different VAT rate than the rest of the EU"*.
- **Category-only override row** — `category_id` is populated, `state_iso_2` is `null`. Used for *"books at 9% VAT while the rest of the catalog is at 20%"*.
- **Combined category + region override row** — both `category_id` AND `state_iso_2` are populated. Used for *"books in California at 0% sales tax while books in Texas are at the standard rate"*.

Each override row carries:

| Column | Purpose |
|--------|---------|
| `tax` | The override rate (stored ×100 internally, see [[settings-taxes-validation]]). |
| `type` | `percent` / `flat`. |
| `description` | Rendered on the invoice line for that category's tax breakdown. |
| `text` | The place display name when applicable. |
| `category_id` | FK to the matching product category. |
| `state_iso_2` | The ISO-2 admin-zone code (from Google Places). |
| `tax_id` | FK to the parent Tax row. |

## Business rules

### Save-time filter — empty rows silently dropped

Any row in the merged set that has neither `category_id` nor `state_iso_2` populated is silently dropped — empty rows do not persist.

### Per-category uniqueness check on save

A Tax cannot have two overrides for the same category within the same region. The save validator throws **"Category already in use"** if the merchant submits two override rows with the same `category_id` + same `admin_zone_1_iso` (or both with no region, when the parent tax has no zone).

The validation row-builder also rejects partial sub-rows: `regions[].text` and `regions[].tax` are required when a `regions[]` row is submitted, and `categories[].description` is required when `categories[].category_id` is provided.

### Override precedence ladder at checkout — category beats region

The engine sorts the override rows by `category_id` DESC (so category-bearing rows come first) and picks the FIRST match in this order:

1. **Combined category + region match** — override where `category_id` matches the line item's category AND `state_iso_2` matches the customer's state (or `state_iso_2` is null). Fires FIRST because the sort puts category-bearing rows ahead.
2. **Category-only match** — override where `category_id` matches the line item's category AND `state_iso_2` is null. Fires SECOND, only if no combined match was found.
3. **Region-only match (no category)** — override where `category_id` is null AND `state_iso_2` matches the customer's state. Fires THIRD — **only reached when NO category override matched the line's category at all** (because the category-DESC sort runs category rows first and the loop short-circuits on the first match).
4. **Base rate** — the parent Tax's `tax` value applies when no override matches.

**Important nuance:** a region-only override does NOT fire when a category override on the same line matches — the category override wins outright. Merchants who set both expect them to **combine**; they don't. To make region-only overrides effective on a given line, the merchant must ensure no category override targets the same product category.

Without a customer address, only category-only overrides (with `state_iso_2 = null`) can apply. Region-only overrides are skipped entirely.

### Zero-rate overrides still render on the invoice

An override with computed amount of 0 STILL renders on the invoice (e.g., *"Books at 0%: 0.00 EUR"*) — so customers see the breakdown even when the math nets out to zero. Without this carve-out, zero-VAT overrides would silently disappear from the invoice.

### Auto-Global companion copies the overrides

When the platform auto-creates the *"- Global"* companion tax on a merchant's first regional VAT (see [[settings-taxes-vat-rules]]), per-category and per-region overrides are copied too — with their descriptions suffixed *"- Global"*. So a *"Books"* category override on the regional tax becomes *"Books - Global"* on the companion. The merchant can then edit / delete either copy independently.

### Common merchant pattern

A 20% VAT base, with a 9% override for the books category (no region filter) that fires for every customer regardless of which state they're in. The override row stores `category_id = books`, `state_iso_2 = null`, `tax = 9`, `description = "Books"`.

## Related

- [[settings-taxes]] — hub.
- [[settings-taxes-vat-rules]] — auto-Global companion duplicates these overrides.
- [[settings-taxes-validation]] — *"Category already in use"* error + the `regions[]` / `categories[]` row-builder constraints.
- [[settings-cart]] — Google Maps API key (controls whether the Region column appears in the row builder).
- [[settings-general]] — `google_map_api_version` (legacy vs new Places API).
- [[category]] — entity page (the dropdown source).
- [[product]] — products carry the category memberships that drive the per-category match.
- [[tax-computation]] — concept page on the full checkout-time math.

## Open questions

None.
