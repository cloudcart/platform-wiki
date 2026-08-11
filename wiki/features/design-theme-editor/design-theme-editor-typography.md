---
type: feature
nav_path: "Design → Theme Editor → Typography"
route_name: admin.css.builder
route_path: /admin/builder?typography
aliases: ["Theme typography", "Theme fonts", "Google Fonts", "Font family picker", "Font weight picker", "Font size picker", "Промяна на шрифтове", "Шрифтове"]
tags: [design, theme, customization, fonts, typography, google-fonts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[design-theme-editor]]. See the hub for the other aspects (variables & types, colours, images, save & reset, CSS compile, live preview & deep-links).

# Theme Editor — Typography sub-tab

## Purpose

The **Typography** sub-tab is where the merchant changes every named **font variable** the active theme exposes — font family, font style, font weight, font size — for distinct surfaces (main body text, titles, buttons, product-listing titles, etc.). The platform ships a curated catalogue of ~88 Google Fonts and the picker filters style / weight options to whatever the chosen family actually supports. Save bundles the merchant's font selections into a single Google Fonts URL stored as a setting that the storefront then injects into every page's `<head>`.

## Where to find it

`/admin/builder?typography` — the deep-link auto-opens the Typography sub-tab.

Otherwise: open `/admin/builder` (sidebar → **Design** → **Colors and typography**) and click the **Typography** sub-tab in the sidebar.

The sub-tab link is rendered **only** if the active theme exposes at least one variable of `type: font-family` / `font-style` / `font-weight` / `font-size`. Themes that ship only a colour palette do not render this sub-tab.

## What the merchant can do here

- **Browse font variables grouped into accordion sections** (typical groups: **Main** / **Titles** / **Buttons** / **Listing product**). Group names are theme-authored and translated into the admin's language.
- **Pick a font family** from a dropdown of ~88 Google Fonts — each option is rendered in its own font face so the merchant sees the font preview inline before clicking. Selecting a family lazily loads its Google Fonts CSS so the family also appears in the preview iframe after save.
- **Pick a font style** — `normal`, `italic`, etc. — filtered to the styles the chosen family supports.
- **Pick a font weight** — `100` (Thin) / `200` (Extra Light) / `300` (Light) / `400` (Regular) / `500` (Medium) / `600` (Semi Bold) / `700` (Bold) / `800` (Extra Bold) / `900` (Black) — filtered to the weights the chosen family supports.
- **Pick a font size** — a dropdown from `10px` to `72px` in 1px increments.
- **Save the typography** via the bottom-right **Save theme** button (saves all sub-tabs at once — see [[design-theme-editor-save-reset]]).
- **NOT upload a custom font.** Only Google Fonts from the platform's curated catalogue are selectable. Self-hosted webfonts require [[design-custom-assets]] (paste a `@font-face` rule + the font file).
- **NOT pick from outside the curated catalogue.** A merchant who wants e.g. Adobe Fonts must again use [[design-custom-assets]].

## Settings & fields

### Variable shapes

Every font variable has `type` set to one of the four font types — each renders a different control. See [[design-theme-editor-variables]] for the full type catalogue.

| Type | Control | Allowed values |
|------|---------|------------------|
| `font-family` | Google-Fonts dropdown with live preview per option | One of the ~88 Google Fonts the platform ships. |
| `font-style` | Style dropdown (filtered to family's supported styles) | `normal`, `italic`, etc. |
| `font-weight` | Weight dropdown (filtered to family's supported weights) | `100`, `200`, `300`, `400`, `500`, `600`, `700`, `800`, `900`. |
| `font-size` | Size dropdown — `10px` to `72px` integer values | `10px`, `11px`, …, `72px`. |

### Typical font variables per theme

A typical CloudCart theme declares font variables across these groups (group keys + variable names verbatim from `theme.json`):

| Group | Typical variable names |
|-------|-------------------------|
| `font-main` | `font-family-main`, `font-family-secondary`, `font-size-main` |
| `font-titles` | `font-family-titles`, `font-size-heading-1` through `font-size-heading-6` |
| `font-buttons` | `font-family-buttons`, `font-size-buttons` |
| `font-product-list` | `font-family-product-list-title`, `font-size-product-list-title` |

### Font-weight value → label map

The weight dropdown shows numeric values mapped to canonical English labels:

| Value | Label |
|-------|-------|
| `100` | Thin |
| `200` | Extra Light |
| `300` | Light |
| `400` | Regular |
| `500` | Medium |
| `600` | Semi Bold |
| `700` | Bold |
| `800` | Extra Bold |
| `900` | Black |

### Google Fonts catalogue

The platform pre-registers ~88 Google Fonts including Alice, Andika, Anonymous Pro, Arimo, Arsenal, Bad Script, Comfortaa, Cormorant, Montserrat, Open Sans, Roboto, …. Each entry carries:

- The font's supported subsets (`latin`, `cyrillic`, `latin-ext`, …).
- The font's supported styles (`normal`, `italic`, …).
- The font's supported weights (subset of `100`-`900`).

The picker uses these capability lists to filter the style and weight dropdowns to whatever the chosen family actually supports.

### `google_fonts_url` setting

When the merchant saves, the controller builds one Google Fonts URL spanning every font-family chosen across all variables:

```
https://fonts.googleapis.com/css?family=Family1:weight|Family2:weight|...
```

The URL is stored in the merchant's `google_fonts_url` setting. The storefront reads this setting and injects the Google Fonts stylesheet `<link>` into every page's `<head>`. This avoids re-computing the URL on every request and ensures only the fonts the merchant actually uses are loaded.

## Business rules

### Catalogue is platform-curated

The font catalogue is a static list registered at the platform level — a merchant cannot expand it from the admin. New families enter the catalogue only when CloudCart adds them to the underlying registry.

### Style and weight options are family-specific

The picker filters the style + weight dropdowns to whatever the chosen family supports. A font family that ships only `normal` `400` and `700` weights will show only those two options in the weight dropdown after selection — picking another weight is impossible without switching to a richer family.

### Sub-tab visibility is type-driven

The Typography sub-tab renders only if the active theme declares at least one `font-family` / `font-style` / `font-weight` / `font-size` variable. A theme that ships only colour and image variables hides the sub-tab entirely. See [[design-theme-editor-variables]] for the visibility rule across all three sub-tabs.

### Save bundles all chosen fonts into one URL

Every save rebuilds `google_fonts_url` from scratch by walking every variable of `type: font-family` and including its chosen value with its associated weight(s). Fonts that aren't in any current variable are dropped from the URL — the storefront stops loading them on the next page render.

### Live preview lags by one save

Because the live-preview iframe is the LIVE storefront (not a draft), font changes appear in the preview only after **Save theme** runs and the storefront CSS recompiles + the `google_fonts_url` setting updates. See [[design-theme-editor-css-compile]].

### Custom font upload requires a separate screen

There is no native upload hook in the Theme Editor — merchants who need a font outside the curated Google Fonts catalogue must use [[design-custom-assets]] with `@font-face`. The Theme Editor will NOT recognise the custom face in its dropdowns.

### Font-size values are bounded by the dropdown

The size dropdown offers integer `px` values from `10px` to `72px`. There is no per-variable validation server-side — a hand-crafted POST with `200px` would still save but the storefront might render badly. See [[design-theme-editor-save-reset]] for the save handler's validation gap.

## Related

- [[design-theme-editor]] — hub.
- [[design-theme-editor-variables]] — variable types and group system that this sub-tab uses.
- [[design-theme-editor-colors]] — sibling sub-tab for colour variables.
- [[design-theme-editor-images]] — sibling sub-tab for image-orientation variables.
- [[design-theme-editor-save-reset]] — Save / Reset flow that rebuilds `google_fonts_url` on every save.
- [[design-theme-editor-css-compile]] — server-side stylesheet recompile that applies the new typography.
- [[design-custom-assets]] — `@font-face` route for self-hosted webfonts or non-Google catalogues.

## Open questions

- The exact size of the catalogue ("~88 Google Fonts") — verify against the canonical registry.
- Whether the lazy-load of the chosen font's preview CSS happens per option-hover or only on selection (verify).
