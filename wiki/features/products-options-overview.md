---
type: feature
nav_path: "Products → Options"
route_name: apps.product_options.overview.new
route_path: /admin/products/options-new
aliases: ["Product Options", "Per-product Options", "Custom product options", "Опции"]
tags: [apps, administration, products, options, customisation]
plan_gates: ["product_options"]
created: 2026-05-22
updated: 2026-06-10
source_count: 7
---
# Product Options

## Purpose

**Product Options** is an installable app that adds **per-product customisation options** the customer fills in at the cart / checkout level. Unlike variants ([[products-variants-options]]) — which are pre-defined SKU variations that split stock — Product Options are infinite customisation possibilities of the **same** stock unit. Typical uses:

- **Customer-input fields**: "Enter the engraving text", "Choose a font", "Provide a delivery date".
- **Add-on toggles with price impact**: "Add gift wrap (+5 BGN)", "Express shipping insurance".
- **Built-to-measure pricing**: cut-to-length cable, custom curtains by area.

Each option has its own input type, a required flag, an optional price impact, and an assignment scope that decides which storefront products show it. This page is the **hub** for the Product Options cluster — drill into the aspect that matches the question.

## Where to find it

Sidebar → Products → **Options** (visible only when the Product Options app is installed). Sub-pages of the app itself:

| Sub-page | Route |
|----------|-------|
| Options list (default) | `apps.product_options.settings.new` (index route at `/admin/products/options-new`) |
| Overview | `apps.product_options.overview.new` (`/admin/products/options-new/overview`) |
| Add / Edit option | `apps.product_options.edit.new` (path `:type/:id?` — `type=create` or `type=edit` + `id`) |

## What the merchant can do here

- See all defined product options across the catalogue (Options list).
- Create new options (per option: name, input type, possible values, price impact, assignment scope).
- Edit / delete existing options; toggle Active inline; drag-reorder for storefront sort priority.
- Assign options to products, categories, vendors, or smart collections.

The merchant **cannot** use Product Options to create distinct SKUs or to split stock — that is what variants ([[products-variants-options]]) are for. Options never affect inventory.

## Settings & fields

App identifier: `product_options`.

The **Options list** shows: Name (with badges), **Type** (text label, e.g. "Dropdown menu"), **Values** count, **Required** (Yes / No), **Status** (Active toggle, switches the option ON / OFF inline), **Sort priority** (drag-handle + numeric, controls storefront order), and a per-row **(remove)** delete button. The header has a **+ Create new option** button. Drag-and-drop reorder commits to a single Sort API call; toast *"Sorted successfully"*.

The **Add / Edit option form** is a route-based full-page editor (NOT a modal), divided into three collapsible cards:

1. **Basic settings** — Active toggle; **Title (For internal use)** (required, max 191 chars); **Title (Will be visible in store)** (optional, max 191 chars, falls back to internal Title when empty).
2. **General settings** — the required toggle, **Field type** picker, and all the type-conditional price controls. See [[products-options-types]] for the type catalogue and [[products-options-pricing]] for the price-impact controls.
3. **Appearance / Applicable products** — the assignment scope picker + target multi-tag picker. See [[products-options-assignment]].

The **Save** button (sticky `SubmitChanges` bar) sends a single multipart/form-data PATCH or POST; validation errors surface inline per field.

## Business rules

### Options vs variants — the critical distinction

| Concept | Stock impact | Customer sees |
|---------|--------------|---------------|
| [[products-variants-options]] (variants) | Each variant has separate stock | Pre-purchase selector (Size + Colour) |
| **Product Options** (this app) | NO stock split (one stock count) | Cart-level customisation form |

Variants create distinct SKUs the merchant stocks separately. Options are customisation of the SAME stock unit — see [[inventory-variant-model]] for why stock lives on the Variant, never the option. A single "Engraved Pen" with a free-text engraving option has ONE stock count regardless of what the customer types.

- **Field type is LOCKED on edit** — once an option is created, the type select is disabled. See [[products-options-types]].
- **Required options block checkout** — a Required option prevents Add-to-cart until filled. See [[products-options-order-handling]].
- **Deleting a file-type option also deletes the customer file uploads** on past cart / order items — irreversible. See [[products-options-order-handling]].
- **Uninstalling the app** keeps option records + per-product assignments in the database (they reappear on reinstall) but the storefront stops rendering them. JSON-API v2 read access is disabled while uninstalled.

Standard apps permission scope applies.

## Sub-pages (in this cluster)

- [[products-options-types]] — the 10 supported input types (text, textarea, select, radio, checkbox, file, image, length, weight, square), their storefront UI, the value-required rule, and the type-LOCKED-on-edit rule.
- [[products-options-pricing]] — price-impact mechanics: `amount`, `amount_type` (flat / percent / per-quantity), `per_item`, `allow_negative`, `apply_over_price_type`, `min_square`, and the measure-based pricing for length / weight / square.
- [[products-options-assignment]] — the four assignment scopes (product / category / vendor / selection), the mapping-target pickers, and the Appearance card.
- [[products-options-order-handling]] — customer-entered values stored on the order line, the file-upload cascade on option delete, Required-blocks-checkout enforcement, uninstall behaviour, and JSON-API v2 parity.

## Related

- [[apps]] — App Store (install / uninstall).
- [[apps-product-options-settings-new]] — settings sub-page.
- [[products-variants-options]] — DISTINCT concept (stock-determining choices).
- [[variants-model]] — the Parameter / Option / Variant model; explains why per-product Options never split stock the way Variants do.
- [[products-products]] — products that get options assigned.
- [[product-option]] — the underlying option entity.
- [[orders]] / [[orders-details]] — order lines carry customer option values.
- [[api-product-options]] — JSON-API v2 endpoint for option CRUD.
- [[inventory-variant-model]] — why options never split stock.

## Open questions

None.
