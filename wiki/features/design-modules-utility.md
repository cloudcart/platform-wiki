---
type: feature
nav_path: "Design → Modules → Utility"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Utility modules", "Vendors module", "Payment providers module", "Leasing module", "Authorize module", "Social icons module", "Filters module", "Category properties module", "Utilities module", "Page module", "Wishlist module", "Wishlist menu module", "Code module", "Store locations module", "Yotpo reviews module", "Brand model module", "Order details module", "Footer text module", "Checkout text module", "Header text module", "Модули - Помощни", "Модул вендори", "Модул филтри", "Модул социални мрежи"]
tags: [design, modules, storefront-customisation, utility]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Storefront Modules — Utility

## Purpose

The **Utility modules** are the catch-all category for storefront slots that don't fit cleanly into Navigation, Products, Blog, or Content. They cover four distinct interaction modes:

1. **System modules** that auto-render with no merchant settings — `vendors`, `providers`, `leasing`, `authorize`, `utilities`, `page`, `wishlist`, `wishlistMenu`, `categoryProperties`. Configured indirectly on other admin surfaces.
2. **Editable modules** with merchant settings on the Modules screen — `social` (social-network icons row), `filters` (the master product-listing settings module), and the three `extra.text` instances `footerText` / `checkoutText` / `headerText`.
3. **Page-builder-only blocks** — `code`, `store_locations`, `yotpo-reviews`, `brand-model`, `order-details`. Configured per Dynamic page in [[marketing-landing-pages]], absent from the Modules screen.
4. **The legacy storefront `yotpoReviews` module** — a single enable toggle used by the Yotpo integration to gate the reviews row on/off per theme.

Most utility modules do NOT appear on the Modules editor — they render automatically and pull their data from other admin surfaces (vendor catalogue, payment settings, app installs). The ones that DO appear are documented in [[design-modules-utility-editable]].

This page is the navigation pivot. Drill into the aspect that matches the question rather than reading every aspect.

## Sub-pages (in this cluster)

- [[design-modules-utility-catalogue]] — the full module list with one-liner per module; pick the right aspect by name.
- [[design-modules-utility-editable]] — `filters`, `social`, `footerText` / `checkoutText` / `headerText`, `yotpoReviews` legacy — all merchant-editable settings forms with field tables.
- [[design-modules-utility-system]] — `vendors`, `providers`, `leasing`, `authorize`, `utilities`, `page`, `wishlist`, `wishlistMenu`, `categoryProperties` — auto-rendered modules with NO editor form; configured on other admin surfaces.
- [[design-modules-utility-page-builder]] — `code`, `store_locations`, `yotpo-reviews`, `brand-model`, `order-details` — Dynamic-page-only blocks.
- [[design-modules-utility-storage]] — three-layer storage (theme JSON + sister-site overlay + merchant saves), three-cache stack, save / reset pipeline, edit-form gating, why system modules 404.

## Where to find it

Sidebar → **Design** → **Modules** — then look in:

| Where | Editable modules in this category |
|-------|----------------------------------|
| **Others** tab (extra category) | `social`, `footerText` / `checkoutText` / `headerText` (`extra.text` instances), `yotpoReviews` (legacy) |
| **Products** tab (store category) | `filters` (the product catalog settings card) |
| Not on Modules screen | `vendors`, `providers`, `leasing`, `authorize`, `utilities`, `page`, `wishlist`, `wishlistMenu`, `categoryProperties` (system modules) |
| Page builder only | `code`, `store_locations`, `yotpo-reviews`, `brand-model`, `order-details` (configured per Dynamic page in [[marketing-landing-pages]]) |

## What the merchant can do here

The Modules screen is the entry point. From the cards visible there the merchant can:

- Open an editable module side panel and adjust settings — see [[design-modules-utility-editable]] for fields.
- Save / Reset / Cancel — standard actions across every editable module (full pipeline in [[design-modules-utility-storage]]).
- Enable / disable the master toggle on each editable module.

For system modules there is nothing to edit on the Modules screen — see [[design-modules-utility-system]] for the right admin surface per module.

For page-builder modules, open a Dynamic page in [[marketing-landing-pages]] and add the block from the block picker — see [[design-modules-utility-page-builder]].

The merchant CANNOT:

- Add new editable system modules (e.g., expose `vendors` as a configurable card — it's always auto-rendered).
- Edit hidden fields (e.g., the legacy `yotpoReviews` form has only the enable toggle; deeper Yotpo settings live in [[apps-yotpo-settings]]).
- Override theme placement of these modules.

## Settings & fields

This hub does not document fields directly — every field table lives in the aspect that owns it. Use the catalogue to find the right aspect:

- A field on `filters`, `social`, `footerText` / `checkoutText` / `headerText`, or legacy `yotpoReviews` → [[design-modules-utility-editable]].
- A module with no merchant fields at all (`vendors`, `providers`, `leasing`, etc.) → [[design-modules-utility-system]].
- A field on `code`, `store_locations`, page-builder `yotpo-reviews`, `brand-model`, or `order-details` → [[design-modules-utility-page-builder]].

## Business rules

### Three interaction modes — pick the right aspect first

When a merchant asks about a utility module, the first triage question is *which mode* it is in (editable / system / page-builder). The interaction mode determines where the configuration lives — see [[design-modules-utility-catalogue]] for the master table.

### `filters` is the master catalog module

Despite the name suggesting it's just the filter sidebar, `filters` is the master settings module for EVERY product-listing page — category, search, vendor, smart collection, wishlist. It changes the entire catalog feel. See [[design-modules-utility-editable]] for the 40+ fields.

### System modules cannot be opened from the Modules screen

Trying to open the URL of a system module (`vendors`, `providers`, etc.) returns HTTP 404. The merchant must configure the data on the owning feature surface (vendors admin, payment-provider screens, [[customers-custom-fields]], etc.). The gating mechanics are in [[design-modules-utility-storage]].

### Page-builder blocks are app-gated

The `store_locations`, `yotpo-reviews`, and `brand-model` page-builder blocks only appear in the block picker when their respective apps are installed. The Page Builder URL itself is gated by the `storefront_builder` plan feature — see [[design-modules-utility-page-builder]].

### Cache invalidation is automatic

Save and Reset both bump a per-site cache key, so merchants see their changes on the very next storefront request. No manual cache clear required. Full pipeline in [[design-modules-utility-storage]].

### Plan-gating

None of the utility modules are plan-gated at the module level. Several depend on optional features (apps, payment providers, theme capabilities) — see the relevant aspect for each.

## Related

- [[design-modules]] — parent module catalogue (overview + tab structure).
- [[design]] — pillar hub for Design.
- [[design-themes]] — theme picker; theme decides which utility modules appear.
- [[design-modules-navigation]] — sibling module category (header / footer / search / logo).
- [[design-modules-products]] — sibling module category (product modules, including `productsDetails`).
- [[design-modules-blog]] — sibling module category (blog modules).
- [[design-modules-content]] — sibling module category (content modules).
- [[design-custom-assets]] — global HTML / JS / CSS injection (alternative to per-page `code` module).
- [[marketing-landing-pages]] — Dynamic pages host the page-builder-only modules.
- [[apps-yotpo-settings]] — Yotpo integration (gates the `yotpoReviews` modules).
- [[apps-store-locations]] — Store Locations app (gates the `store_locations` module).
- [[brand-model]] — Brand-Model app (gates the `brand-model` module).
- [[payment-providers]] — payment providers (drives the `providers` + `leasing` modules).
- [[settings-general]] — store SEO, social fallback URLs.
- [[customers-custom-fields]] — customer registration fields (drives `authorize` module).
- [[products-categories]] — category properties (drives `categoryProperties` module).

## Open questions

None at the hub level — open questions are distributed to the aspects that own them. See each aspect's own *Open questions* section.
