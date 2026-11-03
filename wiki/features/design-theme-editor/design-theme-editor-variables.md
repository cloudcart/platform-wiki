---
type: feature
nav_path: "Design → Theme Editor → Variables & types"
route_name: admin.css.builder
route_path: /admin/builder
aliases: ["Theme variables", "theme.json variables", "Variable types", "Variable groups", "Theme settings.variables"]
tags: [design, theme, customization, variables, theme-json]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[design-theme-editor]]. See the hub for the other aspects (colours, typography, images, save & reset, CSS compile, live preview & deep-links).

# Theme Editor — variables & types

## Purpose

Every editable field in the [[design-theme-editor]] is one **variable** declared by the active theme in its `theme.json` file under `settings.variables`. The editor doesn't generate UI from scratch — it reads the variable list, picks a control per variable `type`, and groups the controls into accordion sections by the variable's `group` key. This aspect documents the **type system** (which `type` values exist and which control each renders) and the **group system** (how the accordion sections are produced and labelled).

## Where to find it

Variables surface across all three sub-tabs of `/admin/builder`:

- **Colours** sub-tab — every `color`-type variable.
- **Typography** sub-tab — every `font-family` / `font-style` / `font-weight` / `font-size` variable.
- **Images** sub-tab — every `image`-type variable.

A theme that declares zero variables of a given type hides the corresponding sub-tab entirely.

## What the merchant can do here

The merchant doesn't see "variables" as a tab — they see the controls one type at a time. Across all three tabs, every control is one variable.

- **See every variable the active theme exposes** (typically 80-130 colour variables + 5-15 font variables + 1 image variable).
- **Edit any variable's value** with the type-appropriate control (colour picker, font dropdown, etc.).
- **NOT add new variables** — the variable list is fixed by the active theme's `theme.json`. To extend it, switch to a richer theme via [[design-themes]] or paste raw CSS via [[design-custom-assets]].
- **NOT change a variable's `type` or `group`** — those are theme-author decisions baked into `theme.json`.

## Settings & fields

### Variable types — the seven classes the editor renders

Every variable declared in `theme.json` carries a `type` key that controls how the editor renders it:

| Type | Editor control | Allowed values |
|------|---------------|-----------------|
| `color` | Hex colour picker (Bootstrap colour picker with hex / RGB / slider input) | Any hex / RGB colour. |
| `font-family` | Google-Fonts dropdown with live preview per option | One of the ~88 Google Fonts the platform ships. |
| `font-style` | Style dropdown (filtered to family's supported styles) | `normal`, `italic`, etc. |
| `font-weight` | Weight dropdown (filtered to family's supported weights) | `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900` (mapped to Thin / Extra Light / Light / Regular / Medium / Semi Bold / Bold / Extra Bold / Black). |
| `font-size` | Size dropdown — `10px` to `72px` integer values | `10px`, `11px`, …, `72px`. |
| `image` | Aspect-ratio preset dropdown (PORTRAIT / LANDSCAPE / SQUARE / CUSTOM) plus optional Width / Height fields when CUSTOM | A percentage (e.g., `100%`) or a computed ratio from custom width × height. |
| `custom` | (not editable from this screen — used for the theme's `custom-css-js` variable) | See [[design-custom-assets]]. |

The save handler dispatches purely on `type` — a variable with an unrecognised `type` is silently ignored.

### Variable groups — the section accordions

Every variable can advertise a `group` key in `theme.json`. The editor groups variables by `group` value and renders one accordion section per group. Group keys are translated into the admin's language at render time. A typical theme's colour groups:

| Group key | Typical EN label | Typical BG label |
|-----------|------------------|-------------------|
| `main` | Main | Основни |
| `promo_bar` | Promo Bar | Промо лента |
| `header` | Header | Хедър |
| `footer` | Footer | Футър |
| `topbar` | Topbar | Заглавна лента |
| `slider` | Slider | Слайдър |
| `products-listing` | Products listing | Списък с продукти |
| `brands` | Brands | Марки |
| `product-details` | Product details | Детайли на продукта |
| `tags` | Tags | Етикети |
| `cart` | Cart | Кошница |
| `forms` | Forms | Форми |
| `text-boxes` | Text boxes | Текстови кутии |
| `breadcrumb` | Breadcrumb | Хлебни трохи |
| `pagination` | Pagination | Странициране |
| `buttons` | Buttons | Бутони |
| `labels` | Labels | Етикети |
| `popups` | Popups | Попъпи |

Typical font groups: `font-main` (Main), `font-titles` (Titles), `font-buttons` (Buttons), `font-product-list` (Listing product). Variables without a `group` fall under a default unnamed accordion.

### Per-variable storage row

Each variable is stored as one row in `front_theme` keyed by `{parameter, value, type, template}`:

| Column | What it carries |
|--------|------------------|
| `parameter` | Variable name (e.g., `color-main-background`, `font-family-titles`). |
| `value` | The merchant's chosen value (hex code, font name, percentage, etc.). |
| `type` | One of the seven types above. |
| `template` | The active theme's slug — partitions storage per theme so switching themes hides but doesn't delete the rows. |

This shape is what makes per-theme customisations work and survive theme-switch-and-switch-back. See [[design-theme-editor-save-reset]] for the full save mechanics.

## Business rules

### Variable list is theme-authored, not merchant-authored

A merchant cannot add or remove variables — the variable schema is the theme's responsibility, declared in `theme.json` under `settings.variables`. Themes that ship a richer palette expose more variables; minimal themes expose fewer. To extend the palette without switching themes, the merchant uses [[design-custom-assets]] for raw CSS overrides.

### Group order and labels come from theme.json

The accordion section order in the sidebar is the order the groups appear in the theme's `theme.json` (verify). Each group's visible label is taken from the language file under the group key (e.g., the `main` key resolves to "Main" in English admin, "Основни" in Bulgarian admin).

### Variables without a group still render

A variable that doesn't declare a `group` key falls into a default unnamed accordion at the bottom of the sub-tab. Themes that don't use groups at all render every variable in this default accordion.

### Type-driven sub-tab visibility

The Typography sub-tab is rendered **only** if the active theme declares at least one `font-family` / `font-style` / `font-weight` / `font-size` variable. The Images sub-tab is rendered **only** if at least one `image`-type variable exists. The Colours sub-tab is always visible if any `color`-type variable exists — themes virtually always declare colours, so this sub-tab is effectively always shown. See [[design-theme-editor-colors]], [[design-theme-editor-typography]], [[design-theme-editor-images]] for the per-tab details.

### Variable values are not language-specific

A variable's stored value is one string regardless of which storefront language the visitor uses. The variable LABEL is translated into the admin's language; the variable VALUE is not. A merchant cannot, for example, set a different `color-main-background` per storefront language.

### `quantity` of variables per theme (typical)

A typical CloudCart theme ships:

- **80-130 colour variables** across 10-18 groups.
- **5-15 font variables** (font-family / font-style / font-weight / font-size).
- **0-1 image variables** (only themes with merchant-configurable product-image aspect-ratio).
- **1 `custom`-type variable** (`custom-css-js`) that is NOT editable from the Theme Editor — see [[design-custom-assets]].

## Related

- [[design-theme-editor]] — hub.
- [[design-themes]] — theme picker; the active theme's `theme.json` decides the variable schema.
- [[design-custom-assets]] — raw CSS / JS overrides for cases the variable system can't reach (custom font upload, custom selectors, etc.); also the home of the `custom-css-js` variable.
- [[design-theme-editor-colors]] — colour-variable sub-tab.
- [[design-theme-editor-typography]] — font-variable sub-tab.
- [[design-theme-editor-images]] — image-variable sub-tab.
- [[design-theme-editor-save-reset]] — how variable rows are written / wiped.

## Open questions

- The exact iteration order of accordion sections when the theme declares groups in a non-standard order (verify whether `theme.json` order, alphabetical order, or another canonical order wins).
