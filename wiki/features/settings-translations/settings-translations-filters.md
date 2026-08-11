---
type: feature
nav_path: "Settings → Translations → Filters"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["Translations filters", "Modified filter", "Section filter", "meta.sections", "Translation namespace filter"]
tags: [settings, translations, i18n, filters]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-translations]]. See the hub for related aspects (toggle, table, reset, scoping, side-effects, permissions).

# Translations — filters

## Purpose

The filter bar above the translations table narrows the visible rows by two axes: whether the merchant has already customised the row (**Modified / Not modified**), and which area of the storefront the row belongs to (**Section**). The Section dropdown is populated dynamically from the platform's translation namespaces plus the first dot-segment of wildcard-namespace keys — so as new translation domains ship, they appear automatically without manual section management.

## Where to find it

Sidebar → Settings → **Translations**. The filter bar sits above the translations table.

## What the merchant can do here

- Filter by **Modified** — show only rows with custom overrides applied.
- Filter by **Not modified** — show only rows still using platform defaults.
- Filter by **Section** with `Includes` or `Does not include` operator — narrow the table to (or away from) one or more storefront areas.
- Combine both filters with the standard table search.
- Clear filters to return to the full table.

## Settings & fields

### Modified filter (`translated`)

| Filter key | Type | Options |
|-----------|------|---------|
| **Modified** (`translated`) | Single-select | *"Modified"* (value `1`) / *"Not modified"* (value `0`). |

Backed by the row's `is_translated` flag (see [[settings-translations-table]] for what sets/clears the flag).

### Section filter (`section`)

| Filter key | Type | Options |
|-----------|------|---------|
| **Section** (`section`) | Multi-select with operator | Operator: *"Includes"* (`in`) / *"Does not include"* (`not_in`). Options: dynamic list from `meta.sections` (cart, checkout, order, product, email, validation, global, etc.). |

The dropdown options are populated dynamically from the server's `meta.sections` array — as new translation domains ship, new sections appear automatically.

## Business rules

### Section list is derived from namespace + label prefix

The Section dropdown reads sections from the platform's translation table. The derivation rule:

- **Real namespaces** (e.g., theme names) are used as-is.
- **Wildcard-namespace keys** (`*::...`) are sub-grouped by their **first dot-separated label segment**. So `*::cart.add_to_cart` reports section `cart`; `*::checkout.empty_cart` reports section `checkout`; `*::order.title` reports section `order`.

The dropdown options therefore include both real namespaces (theme names, the global `*` for built-in strings) and the leading segments of `*::` labels. Typical sections that show up in practice: `cart`, `checkout`, `order`, `product`, `category`, `customer`, `email`, `validation`, `global`. The exact list depends on which translation domains the platform has shipped — no manual section management.

### Section filter supports both inclusion and exclusion

The operator dropdown lets the merchant either include (`in`) or exclude (`not_in`) the selected sections. So a merchant translating everything **except** validation messages can pick "Does not include" + `validation` to hide that section.

### Modified filter reflects `is_translated`, not "ever edited"

The Modified filter checks the `is_translated` flag, which is true only when the current override **differs from the platform default**. A merchant who typed the platform default into a row by mistake (so override text equals default text) will see that row appear under **Not modified**, not **Modified** — see [[settings-translations-table]] for the flag semantics.

### Filters compose with bulk-select

When the merchant uses Section + Modified to narrow the table, the bulk-select checkbox column applies only to the visible rows — useful for "reset every override in the cart section" workflows by filtering to `Section: cart` + `Modified: 1`, selecting all, and bulk-resetting (see [[settings-translations-reset]]).

### Section options reflect server-side state — they are not editable

The merchant cannot add a section, rename a section, or remove a section from the list. Sections appear automatically as the platform ships new translation domains; sections disappear if the underlying domain is removed.

## Related

- [[settings-translations]] — hub.
- [[settings-translations-table]] — `is_translated` flag that drives the Modified filter; the underlying row data the filters operate on.
- [[settings-translations-reset]] — bulk-reset workflows that compose with filters.
- [[settings-translations-scoping]] — locale × theme context the filters operate within.

## Open questions

None.
