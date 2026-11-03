---
type: feature
nav_path: "Design → Theme Editor → Colours"
route_name: admin.css.builder
route_path: /admin/builder?colors
aliases: ["Theme colours", "Theme colors", "Colour picker", "Colour palette", "Brand colours", "Колорит", "Промяна на цветове", "Цветова палитра"]
tags: [design, theme, customization, colors, palette]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[design-theme-editor]]. See the hub for the other aspects (variables & types, typography, images, save & reset, CSS compile, live preview & deep-links).

# Theme Editor — Colours sub-tab

## Purpose

The **Colours** sub-tab is where the merchant changes every named colour the active theme exposes — background, text, titles, buttons, borders, accent links, etc. A typical theme ships **80-130 individual colour variables** organised into 10-18 accordion groups (Main, Promo Bar, Header, Footer, Products listing, Cart, Forms, Buttons, …). Each colour variable maps to a specific CSS rule in the theme's pre-built stylesheet; saving rewrites the storefront CSS to apply the merchant's chosen palette.

## Where to find it

`/admin/builder?colors` — the deep-link auto-opens the Colours sub-tab.

Otherwise: open `/admin/builder` (sidebar → **Design** → **Colors and typography**) and the Colours sub-tab is the default.

The sub-tab link is rendered whenever the active theme exposes any variable of `type: color` (effectively always — every CloudCart theme ships a colour palette).

## What the merchant can do here

- **Browse the colour variables grouped into accordion sections.** Group names are theme-authored (Main / Promo Bar / Header / Footer / Topbar / Slider / Products listing / Brands / Product details / Tags / Cart / Forms / Text boxes / Breadcrumb / Pagination / Buttons / Labels / Popups — the actual list is set by the active theme's `theme.json`). See [[design-theme-editor-variables]] for the full group catalogue.
- **Click any colour swatch** to open the inline colour picker — a Bootstrap colour picker with hex input, RGB input, and a slider (hue + saturation + brightness).
- **Type a hex code directly** (e.g., `#1A8B3F`) into the input next to the swatch.
- **See human-readable variable names** translated into the admin's language (e.g., "Background", "Text", "Title", "Button", "Border", "Active link" — and their Bulgarian equivalents "Фон", "Текст", "Заглавие", "Бутон", "Граница", "Активен линк").
- **Save the palette** via the bottom-right **Save theme** button — full mechanics in [[design-theme-editor-save-reset]].
- **Reset the palette** (along with all typography and image customisations — Reset is global, not per-tab) via the **Reset theme** button.
- **NOT save just one colour** — every save submits all variables of all types; partial-tab saves do not exist.
- **NOT preview a colour without saving** — the live-preview iframe shows the LIVE storefront, not a draft; the new colour appears only after Save recompiles the storefront CSS. See [[design-theme-editor-css-compile]].

## Settings & fields

### Colour variable storage

Each colour variable is stored as one row keyed by `{parameter, value, type, template}` (see [[design-theme-editor-variables]] for the full storage shape):

| Field | Example value |
|-------|----------------|
| `parameter` | `color-main-background`, `color-buttons-primary-text`, `color-header-link-hover`, etc. (variable name from `theme.json`). |
| `value` | A hex colour like `#FFFFFF`, `#1A8B3F`, `rgb(255, 255, 255)`. |
| `type` | `color`. |
| `template` | The active theme's slug — partitions storage per theme. |

### Per-variable label translation

Every variable name has an i18n label resolved at render time. Typical labels seen by the merchant:

| Variable name pattern | Typical EN label | Typical BG label |
|------------------------|------------------|-------------------|
| `color-*-background` | Background | Фон |
| `color-*-text` | Text | Текст |
| `color-*-title` | Title | Заглавие |
| `color-*-button` | Button | Бутон |
| `color-*-border` | Border | Граница |
| `color-*-active-link` | Active link | Активен линк |
| `color-*-hover` | Hover | На посочване |

Labels are theme-specific (a theme can override the platform's defaults); the platform ships a base catalogue that covers the common cases.

### Picker validation

The picker accepts:

- Hex codes — `#RGB`, `#RRGGBB`.
- RGB triples — `rgb(R, G, B)`.
- The internal slider produces hex output.

There is no per-variable validation against allowed ranges (e.g., the theme can't say "this variable must be a dark colour"). A hand-crafted POST with an invalid string would still save but the storefront may render badly. See [[design-theme-editor-save-reset]].

## Business rules

### Group order follows `theme.json`

The accordion section order in the sidebar is the order the groups appear in the theme's `theme.json` (verify). A theme with `main` first then `header` then `footer` renders the accordions in that order in every admin language.

### Variables without a `group` fall into a default accordion

Themes that don't declare a `group` for some variables render those variables in a default unnamed accordion at the bottom of the Colours sub-tab.

### A theme with zero colour variables hides the Colours sub-tab

In theory — in practice every shipped CloudCart theme declares at least one colour variable, so the sub-tab is always visible. The visibility check is "any `color`-type variable declared".

### Colour values are not language-specific

The `value` of a colour variable is one string regardless of storefront language. The variable LABEL is translated to the admin's language; the VALUE is not. See [[design-theme-editor-variables]].

### Picker is Bootstrap colour picker

The colour picker UI is a Bootstrap colour-picker widget — hex input + RGB input + a draggable hue / saturation / brightness slider (verify the exact widget version). Custom widgets are not supported.

### Live preview lags by one save

Because the live-preview iframe is the LIVE storefront (not a draft), colour changes appear in the preview only after **Save theme** runs and the storefront CSS is recompiled. See [[design-theme-editor-css-compile]] for the recompile pipeline and [[design-theme-editor-preview-deeplinks]] for the iframe auto-reload mechanics.

## Related

- [[design-theme-editor]] — hub.
- [[design-theme-editor-variables]] — variable types and group system that this sub-tab uses.
- [[design-theme-editor-typography]] — sibling sub-tab for font variables.
- [[design-theme-editor-images]] — sibling sub-tab for image-orientation variables.
- [[design-theme-editor-save-reset]] — Save / Reset flow (covers all sub-tabs, not just colours).
- [[design-theme-editor-css-compile]] — server-side stylesheet recompile that applies the new palette.
- [[design-custom-assets]] — raw CSS overrides for selectors the colour-variable system doesn't cover.

## Open questions

- The exact list of base label translations the platform ships (vs theme overrides) — verify against the canonical i18n file.
