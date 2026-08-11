---
type: feature
nav_path: "Design → Themes → Switch effects"
route_name: admin.templates.change
route_path: /admin/storefront/templates/change/{mapping}
aliases: ["What is preserved on theme switch", "Demo pages reseed", "Theme switch preservation", "pages.json installer"]
tags: [design, themes, templates, switch, pages]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Themes — What changes on a theme switch (preserved vs lost)

> Part of [[design-themes]]. See the hub for related aspects (catalogue, install, purchase, unpaid-middleware, plan-gates, edge-cases).

## Purpose

This aspect documents **what data survives** a theme switch and **what can be silently lost** — including the demo-pages reseeding via the theme's `pages.json`, the per-theme customisations store, the page-history cap, and the merchant guidance on tuning the new theme.

## Where to find it

Triggered every time the merchant installs a different theme — see [[design-themes-install]] for the install action mechanics.

## What the merchant can do here

After a theme switch, the merchant typically follows up with:

- **Theme Editor** ([[design-theme-editor]]) — colours, fonts.
- **Modules** ([[design-modules]]) — homepage / category / product page layout.
- **Navigation** ([[design-navigation]]) — menus.

There is no dedicated "post-switch" screen — these are the same screens accessible at any time, but the merchant typically wants to revisit them after a switch.

## What the merchant cannot do here

- Cannot **revert** to the previous theme via undo — re-installing the previous theme is the only path back. Customisations are preserved per-theme, so re-installing restores the previously-saved Theme Editor variables, custom CSS, etc.
- Cannot **prevent demo-pages reseed** — the install always re-runs the theme's `pages.json` installer.
- Cannot **preview** the switch on their own data — only the public demo URL is available before install.

## Settings & fields

This aspect has no settings or fields — it documents the behaviour of the install transaction, which the merchant does not configure.

## Business rules

### What is preserved across a theme switch

- **Catalogue data** (products, categories, blog articles, customers, orders) — unaffected. Themes only control look-and-feel, not data.
- **Per-theme Theme Editor customisations** — each theme stores its own customisations (colour overrides, custom CSS/JS, layout tweaks). Switching from theme A to theme B and back to A restores theme A's saved customisations. Editor variables are stored as `{parameter, value, type, template}` rows keyed by the active theme's slug.
- **Pages, navigation, modules** — the underlying records (Static Pages, Navigation menus, Module instances) persist, but their **rendering** may change because the new theme may not have the same module slots, menu locations, or page templates.

### What can be lost on a theme switch

- **Theme-specific modules** the new theme does not ship — modules configured on the previous theme that have no equivalent in the new theme will simply not render until the merchant re-adds them.
- **Theme-specific page-builder blocks** — landing pages built with blocks the new theme does not ship may render with placeholders or fall back to a basic layout.
- **Default landing pages** — CloudCart re-seeds the theme's demo landing pages (About Us, Contact, etc.) on switch. Existing pages assigned to the same system-page slot are **unassigned** in favour of the new theme's defaults.

### Theme switch also reseeds DEMO data (`pages.json` installer)

After the gate / site record update + CSS recompile + translation regen, the install runs the demo-data landing-pages installer, which reads the new theme's `<theme>/resources/data/pages.json`. For each page record in that file:

- **If a page already exists** with the same `(template, source-id)` meta-data pair, the existing page's `system_page` slot + `active = yes` is reassigned (in production; in development the whole record is updated).
- **If no matching page exists**, ANY existing page assigned to the same `system_page` slot (e.g., `home`, `thank_you`, `error.404`) is **unassigned** (its `system_page` is set to null), then a new page is created from the theme's pages.json and assigned to that slot.

So after a theme switch, the previously-active **homepage** page may be silently unassigned in favour of the new theme's homepage page. The previous homepage page row still exists in the page list but is no longer the home page. The merchant has to manually reassign if they want their previous homepage back.

### Page-history cap on theme-installed Dynamic pages

If the theme's `pages.json` includes Dynamic (page-builder) pages, those pages are seeded with their default `page_history` row. The page-history table has a hard cap of **500 versions per page** (older versions auto-purged on save), uniformly applied to both legacy editor saves and Page Builder saves — see [[widget-vs-page-builder-block]] for the lifecycle.

### Per-theme customisation store survives across switches

Theme Editor variables (colours, fonts, custom CSS/JS) are stored keyed by the active theme's `template` slug. Switching to a different theme **hides** the current customisations because the new theme's variable list is different. Switching **back** to the original theme **reveals** the saved customisations again — they were never deleted, just inaccessible while the other theme was active. (See [[design-theme-editor]] for the variable-store details.)

### No instant rollback button

Switching back to the previous theme means reinstalling it from the catalogue — same install transaction, same delay, same demo-pages reseed. CloudCart does not stage previous themes for one-click rollback.

## Related

- [[design-themes]] — hub.
- [[design-themes-install]] — the install transaction that runs the reseed.
- [[design-theme-editor]] — per-theme customisations store.
- [[design-modules]] — theme-shipped modules that may disappear after a switch.
- [[design-custom-assets]] — custom CSS / JS that is also stored per-theme.
- [[marketing-landing-pages]] — Static Pages affected by the `pages.json` reseed.
- [[widget-vs-page-builder-block]] — page-history cap details.

## Open questions

None.
