---
type: feature
nav_path: "Design → Theme Editor → Images"
route_name: admin.css.builder
route_path: /admin/builder?images
aliases: ["Theme image orientation", "Product image aspect ratio", "Image orientation picker", "Portrait landscape square custom", "Image aspect ratio"]
tags: [design, theme, customization, images, aspect-ratio]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[design-theme-editor]]. See the hub for the other aspects (variables & types, colours, typography, save & reset, CSS compile, live preview & deep-links).

# Theme Editor — Images sub-tab

## Purpose

The **Images** sub-tab exposes the small set of `image`-type variables the active theme declares — currently the **product-image orientation** (the aspect-ratio of product thumbnails across product listings, category pages, search results, and similar listing surfaces). The merchant picks from four presets — PORTRAIT, LANDSCAPE, SQUARE, CUSTOM — and the chosen value is saved as a percentage that the theme's CSS uses to drive the thumbnail's `padding-bottom`-as-aspect-ratio trick.

## Where to find it

`/admin/builder?images` — the deep-link auto-opens the Images sub-tab.

Otherwise: open `/admin/builder` (sidebar → **Design** → **Colors and typography**) and click the **Images** sub-tab in the sidebar.

The sub-tab link is rendered **only** if the active theme exposes at least one variable of `type: image`. Most CloudCart themes do not — so this sub-tab is the rarest of the three.

## What the merchant can do here

- **Pick an image-orientation preset** for product photos from four presets — PORTRAIT, LANDSCAPE, SQUARE, CUSTOM.
- **Enter a custom aspect-ratio** via Width and Height number fields when the CUSTOM preset is chosen (the resulting percentage is computed automatically — `(height / width × 100)%`).
- **See the change apply to the storefront's product-listing thumbnails** after Save runs (the live-preview iframe reloads to show the new aspect-ratio). See [[design-theme-editor-css-compile]].
- **NOT change the aspect-ratio of every image on the storefront** — only product-listing thumbnails (the variables the theme exposes). Hero banners, brand logos, social-share images, and similar surfaces have their own dedicated screens ([[settings-brand]] for brand assets; the page-builder modules for hero banners; etc.).
- **NOT pick an arbitrary percentage outside the preset → custom flow.** The picker is a dropdown with the four presets; CUSTOM reveals the two number fields. There is no free-text percentage input.
- **NOT see this sub-tab at all** if the active theme has no `image`-type variables — common for minimal themes.

## Settings & fields

### Image-orientation presets

The picker stores one percentage value per preset:

| Preset | Stored value | Visual outcome |
|--------|--------------|----------------|
| **PORTRAIT** | `133.33%` | Taller than wide (e.g., fashion thumbnails). |
| **LANDSCAPE** | `75%` | Wider than tall (e.g., gadget thumbnails). |
| **SQUARE** | `100%` | Equal sides (default for most themes). |
| **CUSTOM** | Computed as `(height / width × 100)%` from the two number fields. | Whatever ratio the merchant dials in. |

The stored value is a CSS-compatible percentage string. The theme's CSS uses this as the `padding-bottom` on the thumbnail wrapper to drive the intrinsic aspect-ratio (the merchant doesn't need to know this — they pick from presets and CloudCart wires up the rest).

### Variable storage row

Image variables share the same storage shape as colour and font variables (see [[design-theme-editor-variables]]):

| Field | Example value |
|-------|----------------|
| `parameter` | `image-orientation` (or similar variable name from `theme.json`). |
| `value` | `133.33%`, `75%`, `100%`, or a computed percentage from CUSTOM. |
| `type` | `image`. |
| `template` | The active theme's slug. |

### CUSTOM-only fields

When the merchant selects **CUSTOM**, two number fields appear:

| Field | Constraint |
|-------|------------|
| **Width** | Positive integer; participates in the ratio computation. |
| **Height** | Positive integer; participates in the ratio computation. |

The picker computes the stored value on selection / form change as `(height / width × 100)%`. The merchant sees the live percentage in the editor as they tweak the numbers.

## Business rules

### Sub-tab visibility is type-driven

The Images sub-tab renders **only** if the active theme declares at least one `image`-type variable. A theme that ships only colour and font variables hides the sub-tab entirely. See [[design-theme-editor-variables]] for the visibility rule across all three sub-tabs.

### Storage is the same as colour and font variables

Image variables are written to `front_theme` rows just like every other variable type. The save handler dispatches on `type` and writes the percentage string. See [[design-theme-editor-save-reset]] for the full save mechanics (including the "save replaces the full customisation set" rule).

### Affects product-listing surfaces, not standalone product photos

The `image-orientation` variable drives the aspect-ratio of product-listing thumbnails — category pages, search results, related-product carousels, brand product lists. The product-detail page's main photo and gallery are typically NOT governed by this variable (those have their own native gallery layout). Themes can theoretically apply the variable to other surfaces by referencing the `_<variable>_` token in their pre-built CSS, but the merchant cannot extend the variable's coverage from the admin.

### CUSTOM stores the computed percentage, not the raw width / height

Once saved, the storage row holds the percentage (e.g., `87.50%`) — the original Width / Height numbers are NOT round-tripped. Re-opening the editor shows the merchant the CUSTOM preset selected with the percentage visible; the original `4 × 3.5` input may not be reconstructed exactly (verify whether the editor stores the inputs separately or only reverse-engineers them from the percentage).

### No validation against extreme ratios

A merchant who dials in `width = 1, height = 999` gets a `99900%` value saved without warning. The storefront will render extremely tall thumbnails — visually broken but not blocked. See [[design-theme-editor-save-reset]] for the save handler's validation gap.

### Live preview lags by one save

Because the live-preview iframe is the LIVE storefront (not a draft), aspect-ratio changes appear in the preview only after **Save theme** runs and the storefront CSS is recompiled. See [[design-theme-editor-css-compile]].

## Related

- [[design-theme-editor]] — hub.
- [[design-theme-editor-variables]] — variable types and group system that this sub-tab uses.
- [[design-theme-editor-colors]] — sibling sub-tab for colour variables.
- [[design-theme-editor-typography]] — sibling sub-tab for font variables.
- [[design-theme-editor-save-reset]] — Save / Reset flow (covers all sub-tabs, not just images).
- [[design-theme-editor-css-compile]] — server-side stylesheet recompile that applies the new aspect-ratio.
- [[settings-brand]] — logo / favicon / social-share images (separate from the product-listing image variable).

## Open questions

- Whether the editor stores the Width / Height inputs separately when CUSTOM is chosen, or only reverse-engineers them from the saved percentage when re-opening (verify).
