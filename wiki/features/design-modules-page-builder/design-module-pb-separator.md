---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Separator"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Separator module", "HR module", "Divider block", "Horizontal line block", "Модул разделител"]
tags: [design, modules, page-builder, separator, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Separator block (`separator`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Separator** block renders a horizontal rule between sections of a Dynamic page — a styled `<hr>` with configurable style, colour, height, width, position, and top / bottom margins. Used for visual breathing room between content blocks on landing pages, hero separators between marketing sections, and as a stylised divider in long-form content.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Separator** from the block picker.

## What the merchant can do here

- Pick the line **style** — `solid` / `dashed` / `dotted` / `double`.
- Pick the line **position** — `left` / `center` / `right` (horizontal alignment within the row).
- Set the line **colour** (free-form hex).
- Set the line **height** (border-top thickness, in `px`).
- Set the line **width** (in percent of the row width).
- Set the **margin top** (in `px`) — space above the line.
- Set the **margin bottom** (in `px`) — space below the line.
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot add a custom CSS class or per-side border style — the block is one-line, single-border.
- The merchant cannot use the block as a vertical separator — it's only horizontal.
- The merchant cannot use units other than `px` / `%` — the form is `<input type="number">` and the storefront appends the correct unit.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `style` | select | `solid` | `solid` / `dashed` / `dotted` / `double` — CSS `border-style`. |
| `position` | select | `center` | `center` / `left` / `right` — horizontal alignment within the row. |
| `color` | text input (hex) | `#000` | Line colour. When blank, defaults to `transparent`. |
| `height` | number (px) | `4` | Line thickness in pixels. |
| `width` | number (%) | `100` | Line width as a percent of the row width. |
| `margin_top` | number (px) | `0` | Space above the line in pixels. |
| `margin_bottom` | number (px) | `0` | Space below the line in pixels. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Renders as a styled `<hr>` tag

The storefront output is a single `<hr>` element with inline `style="..."` — the CSS uses `border-style`, `border-color`, `border-top-width`, `width`, and `margin` to build the visual line. No `<div>` wrappers, no extra DOM nodes.

### Position determines the `margin-left` / `margin-right` pair

When the line is narrower than the row (`width < 100%`), the `position` setting controls where the line sits:

| Position | margin-left | margin-right |
|----------|-------------|--------------|
| `center` | auto | auto |
| `left` | 0 | auto |
| `right` | auto | 0 |

This lets the merchant render a 60%-wide line aligned to either side or centred.

### Blank colour → transparent

If the merchant leaves `color` blank, the line renders with `border-color: transparent` — effectively a blank space, useful for adding pure vertical spacing without a visible line.

### Width is a percent, height is a pixel

The width is intentionally a percent so the separator scales with the row's container width on different screen sizes. The height is in pixels because thickness doesn't usually scale with viewport.

### No theme dependency

The block ships with no theme dependencies — it renders the same `<hr>` regardless of the active theme. Themes can still override via CSS targeting the block's wrapping container.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-title]] — sibling: section title block (often used near separators).
- [[design-custom-assets]] — custom CSS for advanced separator styling.
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Per-side border style.** The block uses `border-top-width` only — confirm there is no plan to add per-side controls. (verify)
- 📡 **Theme overrides.** Some themes may inject a wrapping `<div>` with extra spacing — confirm whether the merchant needs to account for theme padding when setting `margin_top` / `margin_bottom`. (verify)
