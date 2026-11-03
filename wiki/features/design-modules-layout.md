---
type: feature
nav_path: "Design → Modules → Layout"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Layout modules", "Layout settings", "Header layout", "Footer layout", "Buttons layout", "Grid layout", "Layout модули"]
tags: [design, modules, layout]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Storefront Modules — Layout

## Purpose

The **Layout modules** are the four theme-wide presentation settings the merchant can tune from the Modules screen. Unlike content modules, they do not render a piece of content on a specific slot — they control how the WHOLE storefront looks: which header template is in use, which footer template is in use, the corner-radius of every button, and the width / spacing of the product grid. Picking the right combination here defines the visual identity of the store.

Each instance is bound to a specific layout aspect:

| Instance | Type | Controls |
|---------|------|----------|
| `headerConfiguration` | `layout.header` | Header template, menu type, mobile menu type, header behaviour |
| `footerConfiguration` | `layout.footer` | Footer template, footer column count |
| `buttonsConfiguration` | `layout.button` | Border-radius of every button on the storefront |
| `gridConfiguration` | `layout.grid` | Product grid width, desktop / mobile offset |

The Layout tab on the Modules screen renders these four cards (only the ones the active theme declares appear). Drill into the aspect that matches the question; the per-module pages document the backend-verified fields, validation rules, and theme dependencies.

## Sub-pages (in this cluster)

- [[design-module-header-settings]] — `headerConfiguration` (`layout.header`) — header template picker, menu type, mobile menu type, sticky / transparent toggles.
- [[design-module-footer-settings]] — `footerConfiguration` (`layout.footer`) — footer template picker + footer column count (theme-specific).
- [[design-module-buttons-settings]] — `buttonsConfiguration` (`layout.button`) — border-radius (four corners) for every button on the storefront.
- [[design-module-grid-settings]] — `gridConfiguration` (`layout.grid`) — product grid width, full-width toggle, desktop / mobile offsets.

## Where to find it

Sidebar → **Design** → **Modules** → **Layout** tab.

The route is `/admin/storefront/widgets`; the Layout tab key is `layout`. Each card opens the side-panel editor at `/admin/storefront/widgets/{mapping}` (e.g., `/admin/storefront/widgets/headerConfiguration`).

## What the merchant can do here

- Pick a header template from the image-preview select — image previews are theme-shipped.
- Pick a menu type (dropdown / vertical menu / mega-menu / mega-menu click) + a mobile menu type (sidemenu / dropdown).
- Pick a footer template — image-preview select identical to the header.
- Adjust the global button corner-radius (per corner — top-left, top-right, bottom-left, bottom-right).
- Adjust the product grid width (in `px`) or set it to full-width.
- Adjust desktop / mobile grid offset (margin-left / margin-right on the grid container).
- Save / Reset / Cancel — standard module actions.

## What the merchant cannot do here

- The merchant cannot change WHICH header / footer templates the theme ships — that is fixed by the active theme. To get more options, switch themes via [[design-themes]].
- The merchant cannot override per-button styling from here — these are global radii applied to every button.
- The merchant cannot disable the header or footer entirely from this screen (the master enable switch on the buttons / grid module only toggles whether the custom layout settings are applied — the header / footer modules are always on).

## Settings & fields

This hub does not document fields directly — see the aspect that owns the field:

- A field on the header template, menu type, or sticky / transparent header → [[design-module-header-settings]].
- A field on the footer template or footer column count → [[design-module-footer-settings]].
- A field on button border-radius → [[design-module-buttons-settings]].
- A field on grid width or offset → [[design-module-grid-settings]].

### Save / Reset / Cancel — standard buttons

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes panel | None | — |

## Business rules

### Layout modules do not surface text content

Unlike `extra.text`, `extra.banner`, etc., the Layout modules do NOT render content on the storefront — they are theme-wide presentation settings. Changes ripple across every page of the store immediately on save.

### Header / Footer template lists are theme-shipped

The image-preview select for the header / footer module pulls its options from the active theme's module class — `getHeaders` / `getFooters`. Switching themes via [[design-themes]] replaces both lists.

### Buttons + Grid carry a master enable switch

`layout.button` and `layout.grid` both have an `enabled` switch (default OFF). When OFF, the theme's built-in defaults apply; when ON, the merchant's per-corner radii / grid width override the theme defaults. This is unusual for Layout modules — `layout.header` and `layout.footer` are always on.

### Cache invalidation is automatic

Save and Reset both bump the per-site cache key, so the new layout is live on the next storefront request. No manual cache clear required.

### Plan-gating

None of the Layout modules are plan-gated. They are available on every plan and every theme.

## Related

- [[design-modules]] — parent module catalogue.
- [[design]] — pillar hub for Design.
- [[design-themes]] — theme picker; theme decides which header / footer templates are available.
- [[design-modules-content]] — sibling module category (content modules like text, banners, sliders).
- [[design-modules-utility]] — sibling module category (utility modules like filters, social, code).
- [[design-modules-page-builder]] — sibling module category (page-builder blocks used in Dynamic pages).
- [[design-navigation]] — header / footer menu trees; layout module configures the surrounding chrome.

## Open questions

None at the hub level — open questions are distributed to the aspects.
