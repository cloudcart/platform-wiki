---
type: feature
nav_path: "Design → Modules → Layout → Grid settings"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/gridConfiguration
aliases: ["Grid settings module", "Grid layout", "Product grid spacing", "Модул грид", "Настройки на грида"]
tags: [design, modules, layout, grid]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Grid settings module (`layout.grid`)

> Part of [[design-modules-layout]]. See the category page for the other layout modules.

## Purpose

The **Grid settings** module (`gridConfiguration` — instance of `layout.grid`) controls the width and margin of the storefront's main grid container — the wrapper that holds the category listings, product cards, content blocks, and most other page-level layouts. The merchant chooses a fixed width (default 1170 px) or switches to full-width, and sets the desktop / mobile gutter offset.

## Where to find it

Sidebar → **Design** → **Modules** → **Layout** tab → **Grid settings** card.

The route is `/admin/storefront/widgets/gridConfiguration`. Changes apply to every grid-bound page on the storefront on the next request.

## What the merchant can do here

- Toggle the master **enabled** switch — when OFF, the theme's default grid width applies; when ON, the merchant's values override the theme defaults.
- Set **Grid width** in pixels (`int:800,2000`) — the fixed grid container width on desktop.
- Toggle **Full width** — when ON, the grid stretches to the viewport width and disables the **Grid width** input.
- Set **Desktop offset** in pixels (`int:0,80`) — gutter (margin-left / margin-right) around the grid on desktop.
- Set **Mobile offset** in pixels (`int:0,40`) — gutter on mobile breakpoints.
- Save / Reset / Cancel — standard module actions.

## What the merchant cannot do here

- The merchant cannot configure per-section grid widths (e.g., wider for the hero, narrower for content) — the grid is a single global container.
- The merchant cannot pick the grid background colour, padding, or shadow from this module — those are theme settings configured in [[design-theme-editor]].
- The merchant cannot use units other than `px` — inputs are plain numbers and the storefront appends `px` automatically.

## Settings & fields

| Field | Type | Validation | Default | Notes |
|-------|------|------------|---------|-------|
| `enabled` | toggle | `bool` | OFF | Master switch — when OFF, theme defaults apply (the values are still saved but inert). |
| `grid_width` | number (px) | `int:800,2000` | 1170 | Fixed grid container width on desktop. Disabled in the form when `grid_width_full` is ON. |
| `grid_width_full` | toggle | `bool` | OFF | When ON, the grid stretches to viewport width (overrides `grid_width`). |
| `offset_desktop` | number (px) | `int:0,80` | 15 | Desktop gutter (margin-left / margin-right). |
| `offset_mobile` | number (px) | `int:0,40` | 15 | Mobile gutter. |

### Save / Reset / Cancel

Standard module actions — see [[design-modules-layout]].

## Business rules

### Defaults are OFF — theme decides

By default the master `enabled` switch is OFF, so the theme's built-in grid width applies. The module only overrides the theme when the merchant explicitly enables it. This means turning it OFF returns the grid to whatever the theme designer specified — useful for reverting an accidental override.

### `grid_width_full` disables `grid_width`

The form's JS disables the **Grid width** input when **Full width** is toggled ON — there is no point setting a fixed width if the grid will stretch to the viewport. The fixed width is preserved in the JSON blob, just inactive while full-width is on.

### Range 800-2000 px for fixed width

The validation cap is 800-2000 px:

- 800 px is the smallest fixed width that still looks reasonable on desktop.
- 2000 px is wide enough for any reasonable monitor.

Most merchants pick somewhere in 1140-1440 px.

### Desktop / mobile gutters are separate

The `offset_desktop` and `offset_mobile` settings let the merchant set tighter gutters on mobile (e.g., 10 px) and roomier gutters on desktop (e.g., 30 px). Both default to 15 px — the standard Bootstrap-style gutter.

### Applies to grid-bound pages only

Pages that use the master layout pick up the grid settings; Dynamic pages (see [[marketing-landing-pages]]) that disable the master layout do not — those use the per-row grid settings inside the page builder.

### Cache invalidation

Save and Reset bump the per-site cache key — the new grid settings are live on the next storefront request.

## Related

- [[design-modules-layout]] — hub.
- [[design-module-buttons-settings]] — sibling: button border-radius.
- [[design-modules]] — parent catalogue.
- [[design-theme-editor]] — colour palette + typography (the other half of storefront styling).
- [[marketing-landing-pages]] — Dynamic pages with their own per-row grid settings.

## Open questions

- 📡 **Per-row grid override.** Dynamic pages use the page-builder's per-row container width controls (not this module). Confirm the override hierarchy. (verify)
