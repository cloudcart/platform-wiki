---
type: feature
nav_path: "Design → Modules → Layout → Foot settings"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/footerConfiguration
aliases: ["Footer settings module", "Footer layout", "Footer configuration", "Foot settings", "Модул футър", "Настройки на футъра"]
tags: [design, modules, layout, footer]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Footer settings module (`layout.footer`)

> Part of [[design-modules-layout]]. See the category page for the other layout modules.

## Purpose

The **Foot settings** module (`footerConfiguration` — instance of `layout.footer`) picks the footer template the storefront uses on every page. The merchant chooses from the active theme's shipped footer templates (each with an image preview). Some themes also expose a footer column-count setting so the merchant can decide how many columns of footer links / contact / text render.

## Where to find it

Sidebar → **Design** → **Modules** → **Layout** tab → **Foot settings** card.

The route is `/admin/storefront/widgets/footerConfiguration`. The module renders on every storefront page that uses the theme's master layout.

## What the merchant can do here

- Pick a **Footer template** from an image-preview select — options come from the active theme's `getFooters` method (e.g., `footers/footer-one.tpl`, `footers/footer-two.tpl`). The selected template's preview image appears next to the dropdown.
- Pick a **Footer column count** — 4, 5, or 6. (Only renders for the `knowledge-freedom` theme; on other themes the value is hard-fixed at 4 via a hidden field.) (verify — currently only the `knowledge-freedom` theme exposes the column-count control)
- Save / Reset / Cancel — standard module actions.

## What the merchant cannot do here

- The merchant cannot add a custom footer template — the list is fixed by the theme. Switch themes via [[design-themes]] for more options.
- The merchant cannot configure the footer link columns from this module — those are separate `navigation.links` module instances (`footerLinks1`, `footerLinks2`, `footerLinks3`) on the same Modules screen.
- The merchant cannot configure the footer text from this module — `footerText` (an `extra.text` instance) handles that.

## Settings & fields

| Field | Type | Validation | Default | Notes |
|-------|------|------------|---------|-------|
| `footer` | image-preview select | — (free string, options sourced from theme `getFooters`) | `footers/footer-two.tpl` | Active footer template; image preview swaps as the merchant changes the selection. |
| `footer_max_cols_count` | select | `int:4,6` | `4` | Footer column count. Only exposed in the `knowledge-freedom` theme; on other themes the value is fixed at 4 via a hidden field. |

### Save / Reset / Cancel

Standard module actions — see [[design-modules-layout]].

## Business rules

### Footer template list is theme-shipped

The dropdown options come from the active theme — `getFooters` returns a list of `{template, title, image}` entries. Themes ship at least one footer; some ship three or more. Switching themes via [[design-themes]] replaces the list and the merchant's previous footer choice is silently dropped if the new theme doesn't ship the same template path.

### Column-count control is theme-specific

The `footer_max_cols_count` select only renders for themes whose Smarty footer template checks `site('template') == 'knowledge-freedom'` (the legacy condition lives in the footer settings template). All other themes hide the control and force the value to 4. (verify — the column-count gating may be relaxed in newer themes)

### Always-on module

The footer module has no enable / disable toggle — the footer is always rendered on every storefront page that uses the master layout. To remove the footer, the merchant must use a Dynamic page in [[marketing-landing-pages]] that does NOT include the master layout.

### Footer text and links are separate modules

Footer content is the responsibility of three separate module types:

- **Layout** (this module): which footer TEMPLATE renders + how many columns.
- **`extra.text` instance `footerText`**: the static footer copy (about, contact summary, legal blurb).
- **`navigation.links` instances `footerLinks1` / `footerLinks2` / `footerLinks3`**: the link columns.

To change footer content, the merchant edits those instances; this module only changes the footer's visual structure.

## Related

- [[design-modules-layout]] — hub.
- [[design-module-header-settings]] — sibling: header layout.
- [[design-modules]] — parent catalogue.
- [[design-navigation]] — `footer` menu tree (independent of the footer module instances).
- [[design-themes]] — theme picker; theme determines the footer template list.

## Open questions

- 📡 **Theme-specific footer list.** The exact templates available depend on the active theme; merchants on different themes see different options. GraphQL-resolvable: query the active theme + its declared footer templates.
- ⏸️ **Why is `footer_max_cols_count` only on `knowledge-freedom`?** Likely a temporary carve-out — the column-count control may be promoted to other themes in future updates. (verify with theme maintainers)
