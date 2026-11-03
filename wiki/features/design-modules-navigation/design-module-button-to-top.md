---
type: feature
nav_path: "Design → Modules → Navigation → Back to top button"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Back to top button", "buttonToTop", "Up button module", "Scroll-to-top module", "Бутон до горе", "Модул връщане в началото"]
tags: [design, modules, navigation, footer, utility]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Back-to-top button (`buttonToTop`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Back-to-top** module renders a small floating "scroll to top" button that fades in once the customer scrolls down the page. Clicking it smooth-scrolls them back to the top of the current page. Useful on long product-listing pages, long content pages (blog articles, FAQ), and on mobile where browser scroll-to-top affordances are limited.

Internally, the module is an INSTANCE of the generic `extra.text` module — the underlying schema has a title and a rich-text body — but the merchant form HIDES those fields for this specific instance name. The merchant only sees the master enable toggle.

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Fixed-position floating button, usually bottom-right of the viewport, above the chat module when a chat app is installed |
| Admin edit card | Sidebar → **Design** → **Modules** → **Others** tab → **Button "To top"** card |

The underlying module mapping is `extra.text`; the instance name is `buttonToTop`. The render path is controlled by the theme's footer template — themes call `$module->buttonToTop->isEnabled` and conditionally include a `<button class="_to-top js-to-top">` element.

## What the merchant can do here

- **Master enable / disable** the button. That is the entire merchant control surface.

What the merchant CANNOT do from this module:

- Change the button's position (bottom-right is the only option in most themes).
- Change the button's icon / colour / size (theme-controlled CSS).
- Set a custom scroll-trigger threshold (when the button starts fading in) — theme-controlled JS.
- Change the destination (always the top of the current page — `window.scrollTo(0, 0)`).

The module is intentionally minimal — a "set and forget" toggle.

## Settings & fields

Although `buttonToTop` is internally an `extra.text` module (with `title` + `text` fields), the merchant form HIDES the title and text inputs for this specific instance via a template guard (`if $module->getWidgetName !== 'buttonToTop'`). Only the enable toggle is rendered.

### Visible fields (in the merchant form)

| Setting key | Type | Default | Allowed values | Limits | Validation | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool (switch) | `false` (per-theme; some themes default to true) | `yes` / off | — | `bool` | Master on/off — when off, the button never appears on the storefront |

### Hidden underlying fields (saved with the module JSON but not editable here)

| Setting key | Underlying type | Notes |
|---|---|---|
| `title` | string | `extra.text` parent schema; hidden by the form for `buttonToTop` — saved value remains untouched |
| `text` | rich-text | Same — hidden by the form |

### Theme-specific notes

- **Theme support is not universal.** Only themes that ship a `buttonToTop` block in their `theme.json` AND a footer template that calls `$module->buttonToTop->isEnabled` render the button. Verified themes that ship it:
  - `echappe`
  - `themex`
  - another custom theme
  - another custom theme
  - `flair-electronicstore`
  - another custom theme

  Other themes — verify in the theme's own override. If the theme doesn't include the conditional render, toggling this module on has no effect.

- **CSS hook for theming.** The button renders with class `_to-top js-to-top` — themes can target this for custom positioning, sizing, or hover effects. Merchant cannot edit the CSS from the admin panel.

- **Visibility threshold.** Each theme's JS picks its own scroll-distance trigger (typically 200-500 px from the top of the page). The button is INVISIBLE until the customer scrolls past that threshold. If the button doesn't appear after enabling, the merchant scrolls further down the page to test.

## Business rules

### Single boolean — no other state

The module has effectively ONE merchant-controllable bit: enabled. There are no positioning, colour, animation, or threshold settings. Tuning anything beyond the toggle requires theme CSS customisation (CloudCart support).

### Render is theme-gated

Even when the merchant enables the module, the button only appears on themes whose footer template includes the `$module->buttonToTop->isEnabled` check. Themes that don't include this check ignore the toggle. The module itself doesn't render anything on the storefront — it just exposes its `isEnabled` state to the theme.

### Cache invalidation

Save / Reset regenerate the storefront cache key. The button appears / disappears on the next page load.

### Reset behaviour

**Reset module** restores the underlying `extra.text` module defaults: `enabled = true`, `title = 'Example title'`, `text = 'Example text'`. But because the merchant form hides title and text, those defaults are never seen by the merchant. The visible effect is "the toggle goes ON". (Per-theme override in `theme.json` may set a different default — most themes ship `enabled: false`.)

### No plan-gating

The module is not in the `paid_widgets` allowlist — available on every plan.

### Why is it an `extra.text` instance internally?

Historical reason — the platform reused the generic text-block module for this slot rather than create a dedicated `extra.buttonToTop` module type. The text block's storage schema supports an enable-able JSON blob with arbitrary content, which is enough to drive the conditional render. The form template's `if module name !== buttonToTop` guard is the only place the special-casing lives.

### Customisation paths

Merchants who want a different position, icon, or threshold currently must:

1. Ask CloudCart support for theme CSS customisation, OR
2. Switch to a theme whose default `buttonToTop` rendering already matches what they want.

There is no self-service customisation surface.

## Related

- [[design-modules-navigation]] — hub.
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme controls whether the module renders and its visual styling.

## Open questions

- ⏸️ **Theme support audit.** Confirmed 6 themes ship `buttonToTop`; verify whether newer themes (e.g., 2026 launches) also include the conditional render in their footer template.
- 📡 **Scroll threshold per theme.** Each theme's JS picks its own visibility threshold; an inventory of these values would let support set expectations for merchants asking "why doesn't the button show on the first viewport?".
- ⏸️ **Custom CSS override.** Some merchants want bottom-LEFT positioning (for left-to-right languages) or specific brand colours — currently support-only. Worth exploring an aspect of [[design-themes]] for per-store CSS overrides.
