---
type: feature
nav_path: "Design → Modules → Layout → Header settings"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/headerConfiguration
aliases: ["Header settings module", "Header layout", "Header configuration", "Модул хедър", "Настройки на хедъра"]
tags: [design, modules, layout, header]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Header settings module (`layout.header`)

> Part of [[design-modules-layout]]. See the category page for the other layout modules.

## Purpose

The **Header settings** module (`headerConfiguration` — instance of `layout.header`) controls how the storefront header looks on every page. The merchant picks a header template, a main-menu type, a mobile-menu type, and a handful of behaviour toggles (sticky / transparent / full-width / menu position). It is the largest single dial in the storefront's visual identity — changing the header template typically reshuffles the whole top of the page.

## Where to find it

Sidebar → **Design** → **Modules** → **Layout** tab → **Header settings** card.

The route is `/admin/storefront/widgets/headerConfiguration`. The module renders on every storefront page that uses the theme's master layout.

## What the merchant can do here

- Pick a **Header template** from an image-preview select — the available options come from the active theme's `getHeaders` method (e.g., `headers/header-one.tpl`, `headers/header-two.tpl`, `headers/header-four.tpl`). The selected template's preview image appears next to the dropdown.
- Pick a **Menu type** — dropdown / vertical menu / mega-menu / mega-menu two / mega-menu click. Each option has its own image preview.
- Pick a **Mobile menu type** — sidemenu (off-canvas drawer) or dropdown.
- Toggle **Full width** — when ON, the header spans the full viewport width regardless of grid width.
- Toggle **Toggle on scroll** — when ON (and the chosen template supports it), the header collapses / re-shows on scroll. Only visible for `headers/header-two.tpl`.
- Toggle **Transparent** — when ON (and the chosen template supports it), the header background is transparent over the hero. Only visible for `headers/header-one.tpl` and `headers/header-four.tpl`.
- Pick a **Menu position** — left / center / right. Only visible for `headers/header-two.tpl`.
- Save / Reset / Cancel — standard module actions.

## What the merchant cannot do here

- The merchant cannot add a custom header template — the list is fixed by the theme. Switch themes via [[design-themes]] for more options.
- The merchant cannot configure menu CONTENT here — that lives in [[design-navigation]] (the `main` menu tree).
- The merchant cannot configure the header text / logo / search bar from this module — those are separate `extra.text` / `logo` / `search` modules on the same Modules screen.

## Settings & fields

| Field | Type | Validation | Default | Notes |
|-------|------|------------|---------|-------|
| `header` | image-preview select | — (free string, options sourced from theme `getHeaders`) | `headers/header-four.tpl` | Active header template; image preview swaps as the merchant changes the selection. |
| `menu_type` | image-preview select | `in:dropdown,vertical_menu,megamenu,megamenu_two,megamenu_click` | `megamenu` | Main-menu rendering style. |
| `menu_mobile_type` | select | `in:sidemenu,dropdown` | `sidemenu` | Mobile menu behaviour. |
| `full_width` | toggle | `bool` | OFF | Stretches the header to the viewport width. |
| `transparent` | toggle | `bool` | OFF | Transparent header over the hero. Only renders for `headers/header-one.tpl` and `headers/header-four.tpl`. |
| `toggle_on_scroll` | toggle | `bool` | OFF | Collapse / re-show header on scroll. Only renders for `headers/header-two.tpl`. |
| `menu_position` | select | `in:left,center,right` | `center` | Main-menu horizontal position. Only renders for `headers/header-two.tpl`. |

### Save / Reset / Cancel

Standard module actions — see [[design-modules-layout]].

## Business rules

### The conditional toggles depend on the chosen template

The **Transparent**, **Toggle on scroll**, and **Menu position** fields are hidden by default and only slide in when the merchant picks a header template that supports them. The mapping is hard-coded on the form template:

| Field | Visible when `header` is |
|-------|-------------------------|
| Transparent | `headers/header-one.tpl` or `headers/header-four.tpl` |
| Toggle on scroll | `headers/header-two.tpl` |
| Menu position | `headers/header-two.tpl` |

Changing the header template in the dropdown immediately shows / hides the relevant rows via inline JS.

### Header template list is theme-shipped

The dropdown options come from the active theme — `getHeaders` returns a list of `{template, title, image}` entries. Themes ship at least two; some ship five or more. Switching themes via [[design-themes]] replaces the list and the merchant's previous template choice is silently dropped if the new theme doesn't ship the same template path.

### Menu type label translations

The four menu type labels translate via `embed.menu_type_*` translation keys — the storefront renders the matching template under the hood. The mega-menu variants are richer (multi-column dropdowns); the dropdown menu is the simplest.

### Always-on module

The header module has no enable / disable toggle — the header is always rendered on every storefront page that uses the master layout. The merchant cannot turn the header off; to remove it the merchant must use a Dynamic page in [[marketing-landing-pages]] that does NOT include the master layout.

### Mobile menu types

The `menu_mobile_type` setting controls how the menu collapses on mobile:

- `sidemenu` — slides in from the side as an off-canvas drawer.
- `dropdown` — collapses inline as a stacked dropdown.

This is independent of `menu_type` (the desktop menu).

## Related

- [[design-modules-layout]] — hub.
- [[design-module-footer-settings]] — sibling: footer layout.
- [[design-modules]] — parent catalogue.
- [[design-navigation]] — main / footer menu trees configured here.
- [[design-themes]] — theme picker; theme determines the header template list.

## Open questions

- 📡 **Theme-specific header list.** The exact templates available depend on the active theme; merchants on different themes see different options. GraphQL-resolvable: query the active theme + its declared header templates.
- ⏸️ **Settings carry-over on theme switch.** Settings persist by key — if the new theme ships the same template path, the choice carries over; otherwise the merchant reconfigures.
