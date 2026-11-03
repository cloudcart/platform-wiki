---
type: feature
nav_path: "Design → Modules → Navigation → Logo"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Logo module", "logo", "extra.logo", "Store logo module", "Модул лого", "Лого на магазина"]
tags: [design, modules, navigation, header, logo, branding]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Storefront Modules — Logo (`logo`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Logo** module renders the store's logo image in the header — usually top-left or top-center — wrapped in a link to the homepage (`/`). The image itself is uploaded in [[settings-general]] (Logo section) and reused across the whole storefront, including email templates, PDF order documents, and progressive-web-app icons (on themes that ship a PWA manifest).

This module is a SYSTEM module — it's injected by the module helper even when the active theme doesn't declare it in its `theme.json`. The merchant always has a logo slot.

## Where to find it

| Surface | Location |
|---------|----------|
| Storefront slot | Header — placement (top-left / top-center / top-right) controlled by the active theme |
| Image upload | Sidebar → **Settings** → **General** → Logo section (see [[settings-general]]) |
| Admin edit card | None — the module has no card on the Modules screen |

The underlying module mapping is `extra.logo`; the instance name is `logo`. The module is in the platform's hard-coded `system_widgets` list, alongside `userControls`, `filters`, `page`, `vendors`, etc.

## What the merchant can do here

Because this module has no Modules-screen card, the merchant configures it indirectly:

- **Upload / replace the logo image** in [[settings-general]] (the merchant's only direct touchpoint).
- **Set the store name** (`site_name`) in [[settings-general]] — used as the `alt` attribute fallback (defaults to *"Store logo"* if unset).
- **Pick a header template** in **Header settings** (`headerConfiguration`) that hides or repositions the logo, when a theme supports multiple logo placements.

What the merchant CANNOT do:

- Upload a different logo per page, per theme, or per language — there is ONE logo per store and it's reused everywhere.
- Configure logo dimensions / aspect ratio — theme controls responsive sizing.
- Have a separate FOOTER logo — themes that show a footer logo reuse the same image; merchants who want a different footer mark contact CloudCart support.
- Upload separate dark / light variants for theme-mode switching — not a self-service feature.

## Settings & fields

The `extra.logo` module itself has NO merchant-editable settings (no restrictions array, no defaults array). The module reads its data at render time from:

| Read from | Value | Notes |
|-----------|-------|-------|
| `logo` helper | URL of the uploaded logo image | Falls back to the platform default image if no logo uploaded |
| `setting('site_name')` | Store name | Used as the `alt` attribute fallback; if empty, falls back to the translation key `sf.global.logo_alt` |

The module exposes a `getHelperData` method that returns a URL pointing to [[settings-general]] — used by the admin UI to offer a "configure logo" shortcut when the module is being inspected.

### Theme-specific notes

- **Default-image detection.** The module exposes `isDefaultContent` → `hasLogoByType`. Themes can use this to render a "placeholder logo" treatment when the merchant has not uploaded one, or to nudge the merchant to upload via an empty-state banner.
- **Multiple logo variants per theme.** Some themes (e.g., Themex) ship multiple header template variants, each placing the logo differently. To change placement, the merchant picks a different **Header template** in **Header settings**.
- **Logo + site name combos.** A few themes render the site name as text ALONGSIDE the logo image (e.g., logo icon + word-mark). These themes read `site_name` separately and require the merchant to fill both [[settings-general]] fields.

## Business rules

### One logo per store, reused everywhere

The same uploaded image is used in:

- Header (this module)
- Email templates (order confirmations, abandoned cart, password reset, etc.)
- PDF order documents (invoice, packing slip)
- PWA mobile icon (themes that ship a `manifest.json`)
- Schema.org `Organization` JSON-LD (SEO metadata)

There is no per-surface logo override at the module level.

### Logo is INJECTED as a system module

`logo` is in the hard-coded `system_widgets` list. Even themes that DON'T declare it in their `theme.json` get a working logo slot — the module helper injects it. The merchant never has to worry about a theme "forgetting" the logo.

### No save / reset surface

Because there's no Modules-screen card, there's no Save / Reset / Cancel pipeline for this module. The "save" surface is the [[settings-general]] form; saving there regenerates the storefront cache.

### `alt` attribute behaviour

The `alt` attribute on the rendered `<img>` tag is, in order of preference:

1. `setting('site_name')` — if set
2. Translation key `sf.global.logo_alt` — usually translates to *"Store logo"* in EN, *"Лого на магазина"* in BG

Custom `alt` text per language requires the `multylang` app and is set via the language switcher in [[settings-general]].

### Cache invalidation on logo upload

Uploading a new logo via [[settings-general]] regenerates the storefront cache key. Customers see the new logo on the next page load — no manual cache-clear needed.

### No plan-gating

`extra.logo` is not in the `paid_widgets` allowlist — available on every plan.

### Logo URL is served from the merchant's media storage

The `logo` helper resolves to the image URL in the merchant's media storage (S3-backed in production). The image is served with a cache-busting query string when re-uploaded — old cached references self-invalidate on the next page load.

## Related

- [[design-modules-navigation]] — hub.
- [[settings-general]] — upload the logo image + set the store name (the `alt` fallback).
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme controls logo placement / sizing.

## Open questions

- 📡 **Per-language logo upload.** With `multylang` installed, [[settings-general]] exposes per-language logo upload (e.g., a Cyrillic logo for BG, Latin for EN). GraphQL-resolvable: query whether the `multylang` app is installed.
- ⏸️ **Dark / light logo variants.** Themes with dark-mode support typically need a second logo — currently a support-only workflow. Verify which themes (if any) auto-detect dark mode.
- ⏸️ **PWA icon vs header logo.** Some themes use a separate PWA icon (`manifest.json` `icons`) — confirm whether the upload is shared with the header logo or stored separately per theme.
