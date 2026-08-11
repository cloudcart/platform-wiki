---
type: feature
nav_path: "Design → Modules → Navigation → Search"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Search module", "search", "extra.search", "Storefront search bar", "Header search module", "Autocomplete module", "Модул търсене", "Лента за търсене"]
tags: [design, modules, navigation, search, header]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Storefront Modules — Search (`search`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Search** module renders the storefront's search bar — usually in the header — and powers the autocomplete dropdown that appears as the customer types. It also drives the dedicated search-results page (`/search`).

Behind the module is the platform's storefront search service: native full-text search by default; the Algolia integration when the merchant has installed and configured the Algolia app; the in-house Advanced Search engine when enabled. The module itself only configures the input's BEHAVIOUR (autocomplete, search-in-description, UTM tracking on/off) — search-index settings live elsewhere.

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Header — exact placement (input vs icon-trigger vs floating button) depends on the active theme |
| Admin edit card | Sidebar → **Design** → **Modules** → **Others** tab → **Search** card |
| Search-engine settings | Algolia integration → [[apps-algolia]]; Advanced Search → its own app surface |
| Search-page settings (per-page count, sections) | Stored in the module JSON but NOT exposed in the merchant form — adjust via support |

The underlying module mapping is `extra.search`; the instance name is usually `search`.

## What the merchant can do here

- **Toggle the master enable / disable** switch — when off, most themes still render the search bar (only themes that allow disabling honour it).
- **Toggle autocomplete** — show / hide the suggestions dropdown as the customer types.
- **Toggle search-in-product-description** — also match against the product description text, not just title + tags. (Stored in global settings, not in the module JSON.)
- **Toggle search-add-utm** — append UTM tags to clicked search-result links. (Only visible when the Algolia integration is installed and enabled. Stored in global settings.)
- **Save / Reset / Cancel** standard buttons.

What the merchant CANNOT do from this module: change the per-page result count, choose which result sections appear, reorder section priority, set the autocomplete row count, or change the result-link target. All of these live in the module JSON but have no form control — see the table below. To adjust them, contact support or install the Advanced Search app, which exposes its own settings UI.

## Settings & fields

### Settings exposed in the merchant form

| Setting key | Type | Default | Allowed values | Notes |
|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | `yes` / off | Master on/off. Most themes don't surface the disable toggle (they always render the bar) |
| `autocomplete` | bool (switch) | `true` | `yes` / off | Whether to show the suggestion dropdown as the customer types |
| `search_in_product_description` | bool (switch) | `true` | `yes` / off | Saved to GLOBAL settings, not the module JSON — affects every search query |
| `search_add_utm` | bool (switch) | `true` | `yes` / off | Saved to GLOBAL settings. Only visible in the form when Algolia is installed AND enabled |

### Settings stored in module JSON but NOT in the merchant form

These fields live in the saved module JSON but have no form control. They can be adjusted via the JSON API or by support.

| Setting key | Type | Default | Allowed values | Limits | Notes |
|---|---|---|---|---|---|
| `per_page` | int | `15` | any integer 2-50 | `int:2,50` | Results per page on the dedicated `/search` page |
| `per_page_options` | int[] | `[15, 30, 50]` | 2-10 entries, each integer 2-50 | `array:2,10\|int:2,50` | The picker options the customer sees on the search-results page |
| `search_sections` | string[] | `['product', 'category', 'vendor', 'article']` | subset of those 4 strings | `array:2,20\|in:product,category,vendor,article` | Which result sections the search-results page renders |
| `priority` | string[] | `['product', 'article', 'category', 'vendor']` | subset of those 4 strings | `array:2,20\|in:product,vendor,category,article` | Order of sections in the autocomplete + results page |
| `initial_results` | int | `5` | 3-10 | `int:3,10` | Number of result rows shown in the autocomplete dropdown before "see all" |
| `item_target` | string | `_blank` | `_blank` / `_self` | `in:_blank,_self` | Result-link target attribute |
| `section_target` | string | `_blank` | `_blank` / `_self` | `in:_blank,_self` | "See all results in X" link target attribute |

### Theme-specific notes

- **Whether the disable toggle is shown.** The `enabled` switch only renders if the theme allows disabling; many themes hard-code their header to always render the search bar regardless. Verify per theme.
- **Search-engine routing.** The form auto-selects its template by active engine: Advanced Search if enabled, else Algolia if installed and enabled, else native search.
- **Theme-specific icon.** Most themes use a regular search icon; the `knowledge-freedom` theme uses a light-weight variant. This is hard-coded in the theme, not configurable.

## Business rules

### Search-engine selection is global, not per-module

The module renders whatever search engine the storefront has globally enabled (Advanced Search, Algolia, native search). Switching engines is done in the corresponding app's settings, not here.

### `search_in_product_description` is GLOBAL across the store

Despite being in the module form, this toggle writes to a global setting. Turning it on/off affects every search across the storefront, including future modules or API calls. There is no per-module override. On stores with thousands of long descriptions it measurably slows the native search (it scans a larger column); Algolia is unaffected — it indexes descriptions natively.

### `search_add_utm` is GLOBAL across the store and Algolia-specific

The UTM toggle is only meaningful when Algolia is the search engine, and it writes to a global setting. When the customer clicks a search result, Algolia's tracking appends `utm_source=algolia` etc. to the URL.

### Autocomplete is JS-driven on the storefront

The dropdown is rendered by the theme's JavaScript and depends on the storefront's JS bundle loading correctly. If it doesn't appear despite the toggle being ON, check the browser's JS console for errors first.

### Save, cache, and reset

Save updates the module JSON and (for the two global toggles) the global settings; the storefront cache regenerates and the new behaviour applies on the next request. **Reset module** restores the module JSON to the defaults shown above but does NOT roll back the two global settings — those keep their prior value.

### No plan-gating

`extra.search` is not a paid widget — available on every plan.

## Related

- [[design-modules-navigation]] — hub.
- [[apps-algolia]] — Algolia integration; when installed, the module routes searches to Algolia and exposes the UTM toggle.
- [[settings-general]] — broader search-related global settings (site name, SEO).
- [[design-modules]] — parent module catalogue.

## Open questions

- 📡 **Active search engine.** Determines whether the module uses native search, Algolia, or Advanced Search — resolvable by checking which search apps are installed and enabled.
- 📡 **Hidden fields accessibility.** The module-JSON fields not exposed in the form can be inspected via the JSON API for the `search` instance.
- ⏸️ **Disable toggle per theme.** Verify in each theme whether the disable toggle is honoured or the search bar is hard-rendered.
