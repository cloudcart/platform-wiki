---
type: feature
nav_path: "Design → Modules → Layout → Buttons settings"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/buttonsConfiguration
aliases: ["Buttons settings module", "Buttons layout", "Button border radius", "Модул бутони", "Настройки на бутоните"]
tags: [design, modules, layout, buttons]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Buttons settings module (`layout.button`)

> Part of [[design-modules-layout]]. See the category page for the other layout modules.

## Purpose

The **Buttons settings** module (`buttonsConfiguration` — instance of `layout.button`) controls the border-radius of every button on the storefront. The merchant picks four corner radii (top-left, top-right, bottom-left, bottom-right) and a master enable toggle. With the toggle ON, the merchant's radii override the theme defaults globally — Add-to-cart, Buy now, Sign-in, Checkout, every CTA button gets the same corners.

## Where to find it

Sidebar → **Design** → **Modules** → **Layout** tab → **Buttons settings** card.

The route is `/admin/storefront/widgets/buttonsConfiguration`. Changes apply to every button on the storefront on the next request.

## What the merchant can do here

- Toggle the master **enabled** switch — when OFF, the theme's default button radius applies; when ON, the four merchant-set radii override the theme defaults.
- Set **Top-left radius** in pixels (`int:0,100`).
- Set **Top-right radius** in pixels (`int:0,100`).
- Set **Bottom-left radius** in pixels (`int:0,100`).
- Set **Bottom-right radius** in pixels (`int:0,100`).
- Save / Reset / Cancel — standard module actions.

## What the merchant cannot do here

- The merchant cannot change button colours, padding, font-size, or hover style from this module — those live in [[design-theme-editor]] (CSS variables) or [[design-custom-assets]] (custom CSS).
- The merchant cannot configure per-button-type radii (e.g., different radius on Add-to-cart vs. Sign-in). The four radii are global to every button.
- The merchant cannot use units other than `px` — the input is a plain number and the storefront appends `px` automatically.

## Settings & fields

| Field | Type | Validation | Default | Notes |
|-------|------|------------|---------|-------|
| `enabled` | toggle | `bool` | OFF | Master switch — when OFF, theme defaults apply (the four radii are still saved but inert). |
| `border_top_left_radius` | number (px) | `int:0,100` | 0 | Top-left corner radius in pixels. |
| `border_top_right_radius` | number (px) | `int:0,100` | 0 | Top-right corner radius in pixels. |
| `border_bottom_left_radius` | number (px) | `int:0,100` | 0 | Bottom-left corner radius in pixels. |
| `border_bottom_right_radius` | number (px) | `int:0,100` | 0 | Bottom-right corner radius in pixels. |

### Save / Reset / Cancel

Standard module actions — see [[design-modules-layout]].

## Business rules

### Defaults are OFF — theme decides

By default the master `enabled` switch is OFF, so the theme's built-in radii apply. The module only overrides the theme when the merchant explicitly enables it. This means turning it OFF returns the buttons to whatever the theme designer specified — useful for reverting an accidental override.

### Per-corner radii (not a single value)

The module exposes four separate corner radii because that is what CSS supports — a button can be a rounded-pill on the left and a square on the right, for example. The most common merchant settings:

| Style | Top-L | Top-R | Bottom-L | Bottom-R |
|-------|-------|-------|----------|----------|
| Square (sharp) | 0 | 0 | 0 | 0 |
| Slightly rounded | 4 | 4 | 4 | 4 |
| Rounded | 8 | 8 | 8 | 8 |
| Pill (very rounded) | 50 | 50 | 50 | 50 |

Asymmetric radii (e.g., 0 / 8 / 0 / 8) are valid but rarely used — most merchants set all four corners to the same value.

### Range 0-100 px

The validation cap is 100 px — enough to render any reasonable button as a pill. Larger values are rejected on save with a field-level error.

### Applies globally — no per-button override

The radii apply to EVERY button on the storefront (Add-to-cart, Buy now, Sign-in, Checkout, even page-builder button modules). There is no per-button-type override. Page-builder Button modules (see [[design-module-pb-button]]) pick up the global radius unless the merchant overrides via [[design-custom-assets]] CSS.

### Cache invalidation

Save and Reset bump the per-site cache key — the new radii are live on the next storefront request.

## Related

- [[design-modules-layout]] — hub.
- [[design-module-grid-settings]] — sibling: product grid width / offset.
- [[design-module-pb-button]] — sibling page-builder module: per-page Button block (picks up the radii set here).
- [[design-theme-editor]] — colour palette + typography (the other half of storefront styling).
- [[design-custom-assets]] — custom CSS / JS for per-button overrides.

## Open questions

- 📡 **Cross-module interaction with the Button page-builder block.** The page-builder Button module renders an `<a class="_button...">`; this module's radii apply via global CSS to that class. Confirm there is no per-button overriding mechanism. (verify)
