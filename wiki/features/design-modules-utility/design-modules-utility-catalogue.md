---
type: feature
nav_path: "Design → Modules → Utility → Catalogue"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Utility modules catalogue", "Utility module list", "Утилити модули списък"]
tags: [design, modules, storefront-customisation, catalogue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Utility modules — Catalogue

> Part of [[design-modules-utility]]. See the hub for editable settings, system rendering rules, page-builder blocks, and storage.

## Purpose

A single-glance table of every module that lives under **Design → Modules → Utility**, sorted by how the merchant interacts with it. Use this page to find the module by name and jump to the aspect that documents how it works.

## Where to find it

Sidebar → **Design** → **Modules** — then look in:

| Where on the Modules screen | Editable modules in this category |
|-------|----------------------------------|
| **Others** tab (extra category) | `social`, `footerText` / `checkoutText` / `headerText` (`extra.text` instances), `yotpoReviews` (legacy) |
| **Products** tab (store category) | `filters` (the product catalog settings card) |
| Not on Modules screen | `vendors`, `providers`, `leasing`, `authorize`, `utilities`, `page`, `wishlist`, `wishlistMenu`, `categoryProperties` (all system modules) |
| Page builder only | `code`, `store_locations`, `yotpo-reviews`, `brand-model`, `order-details` (configured per Dynamic page in [[marketing-landing-pages]]) |

## What the merchant can do here

- Open the Modules screen and identify which utility modules are even editable.
- Recognise that most utility modules are **invisible system plumbing** — they auto-render from data managed elsewhere.
- Identify which modules only exist inside the Dynamic page builder.
- Pick the right aspect page to drill into.

## Settings & fields

There are no settings here — this page is the catalogue. Each module has its own row in the right aspect (editable / system / page-builder).

### Master catalogue table

| Module key | Map | Category | Drill into |
|------------|-----|----------|------------|
| `filters` | `product.filters` | Editable — Products tab | [[design-modules-utility-editable]] |
| `social` | `extra.social` | Editable — Others tab | [[design-modules-utility-editable]] |
| `footerText` | `extra.text` | Editable — Others tab | [[design-modules-utility-editable]] |
| `checkoutText` | `extra.text` | Editable — Others tab | [[design-modules-utility-editable]] |
| `headerText` | `extra.text` | Editable — Others tab | [[design-modules-utility-editable]] |
| `yotpoReviews` (legacy) | `extra.yotpoReviews` | Editable — Others tab | [[design-modules-utility-editable]] |
| `vendors` | `product.vendors` | System (auto-render) | [[design-modules-utility-system]] |
| `providers` | `payment.providers` | System (auto-render) | [[design-modules-utility-system]] |
| `leasing` | `store.leasing` | System (auto-render) | [[design-modules-utility-system]] |
| `authorize` | `user.authorize` | System (auto-render) | [[design-modules-utility-system]] |
| `utilities` | `base.utilities` | System (auto-render) | [[design-modules-utility-system]] |
| `page` | `extra.page` | System (auto-render) | [[design-modules-utility-system]] |
| `wishlist` | `wishlist.listing` | System (auto-render) | [[design-modules-utility-system]] |
| `wishlistMenu` | `wishlist.menu` | System (auto-render) | [[design-modules-utility-system]] |
| `categoryProperties` | `product.categoryProperties` | System (auto-render) | [[design-modules-utility-system]] |
| `code` | (page-builder) | Page builder only | [[design-modules-utility-page-builder]] |
| `store_locations` | (page-builder) | Page builder only | [[design-modules-utility-page-builder]] |
| `yotpo-reviews` | (page-builder) | Page builder only | [[design-modules-utility-page-builder]] |
| `brand-model` | (page-builder) | Page builder only | [[design-modules-utility-page-builder]] |
| `order-details` | (page-builder) | Page builder only | [[design-modules-utility-page-builder]] |

### One-line summary per module

**Editable modules:**

- `filters` — master settings module for EVERY product-listing page (per-page count, per-row, sort options, filter chips, card display toggles, price ranges).
- `social` — row of social-network icons (Facebook, X, Instagram, Pinterest, YouTube, LinkedIn, TikTok) with per-network URL + show toggle.
- `footerText` / `checkoutText` / `headerText` — three `extra.text` instances pointing at different theme slots (footer / checkout summary / header tagline).
- `yotpoReviews` (legacy) — single enable toggle to gate the Yotpo review block per theme; deeper Yotpo configuration in [[apps-yotpo-settings]].

**System modules (no editor form):**

- `vendors` — storefront vendor / brand list at `/vendors`; data from the Vendors admin.
- `providers` — payment-method icon row in footer / checkout; data from active payment providers.
- `leasing` — credit / leasing badges + calculators on product pages; data from CREDIT-type providers.
- `authorize` — `/login`, `/register`, `/forgotten-password`, `/reset-password` forms; behaviour from Customers admin.
- `utilities` — homepage + global-context container; SEO from [[settings-general]].
- `page` — static merchant page renderer at `/page/{slug}`; content from [[marketing-landing-pages]] static pages.
- `wishlist` — full wishlist page at `/site/account/wishlist`; per-customer state.
- `wishlistMenu` — header wishlist dropdown / counter; reads last N favourites.
- `categoryProperties` — category-specific filter facets on listing pages; properties defined per category.

**Page-builder modules (Dynamic pages only):**

- `code` — raw HTML / JS embed inside an `<iframe srcdoc>`; up to 3,000,000 characters.
- `store_locations` — list of physical shops from the Store Locations app.
- `yotpo-reviews` — Yotpo reviews block with per-site or per-product mode.
- `brand-model` — vehicle / device compatibility picker from the Brand-Model app.
- `order-details` — order receipt block for custom thank-you pages.

## Business rules

### Three interaction modes — pick the right aspect first

When a merchant asks about a utility module, the first question is *which mode* it is in:

- **Editable** → open the Modules screen, find the card under Others / Products, edit settings, Save. See [[design-modules-utility-editable]].
- **System** → there is NO card on the Modules screen. The merchant configures it indirectly on the relevant feature surface. See [[design-modules-utility-system]].
- **Page-builder** → only available inside a Dynamic page in [[marketing-landing-pages]]. See [[design-modules-utility-page-builder]].

### Trying to open a system module URL returns 404

The module controller's `checkWidget` allows the edit panel only when the instance carries a `class` declaration OR its map is on the editable-mapping allowlist — system modules fail both checks. The merchant cannot force-open the editor by typing the module URL. See [[design-modules-utility-storage]] for the gating mechanics.

### Theme exposes a different subset

Each theme decides which module instances exist via its `theme.json`. Switching themes can add, remove, or replace utility module instances. Settings for instances the new theme doesn't ship remain in the database but are non-editable until that instance is re-introduced.

### Plan gating

None of the utility modules are plan-gated at the module level. Several depend on optional apps or features (see the table in [[design-modules-utility-system]] and [[design-modules-utility-page-builder]]).

## Related

- [[design-modules-utility]] — hub.
- [[design-modules]] — parent module catalogue (all module categories).
- [[design-themes]] — theme decides which module instances ship.
- [[marketing-landing-pages]] — Dynamic pages host the page-builder-only modules.

## Open questions

None — this is a catalogue page.
