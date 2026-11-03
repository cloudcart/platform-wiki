---
type: feature
nav_path: "Design → Modules → Navigation → Navigation links"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Navigation links module", "navigationLinks", "footerLinks1", "footerLinks2", "footerLinks3", "navigationLinksPage", "navigation.links", "Footer columns module", "Top-bar links module", "Навигационни връзки", "Долни връзки"]
tags: [design, modules, navigation, footer, header, links]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Storefront Modules — Navigation links (`navigationLinks`, `footerLinks1-3`, `navigationLinksPage`)

> Part of [[design-modules-navigation]]. See the category page for the other navigation modules.

## Purpose

The **Navigation links** module type (`navigation.links`) renders a SIMPLE, FLAT list of links — no nesting, no mega-menu, no banners. Used to fill secondary navigation slots that don't need the richness of the main / footer menu trees:

- `navigationLinks` — top-bar shortcuts above the header (Blog, Brands, Contacts).
- `footerLinks1` / `footerLinks2` / `footerLinks3` — extra footer columns next to [[design-module-navigation-footer]].
- `navigationLinksPage` — links shown in the static page menu sidebar.

Each instance is an independent flat list with its own enable toggle, optional title, and links — edited via its own card on the Modules screen. The same module type can appear multiple times on one storefront.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab.

Each instance appears as its own card. Click the card to open the side panel form.

| Instance | Typical slot | Display name |
|----------|--------------|--------------|
| `navigationLinks` | Top-bar above the header | **Navigation Links** |
| `footerLinks1` | Footer column 2 | **Footer navigation links 1** |
| `footerLinks2` | Footer column 3 | **Footer navigation links 2** |
| `footerLinks3` | Footer column 4 | **Footer navigation links 3** |
| `navigationLinksPage` | Page menu sidebar | **Page menu - Pages** |

The exact instance names a theme ships depend on the theme's `theme.json`; the merchant only sees cards for instances the active theme declares.

## What the merchant can do here

- **Set an optional title** above the link list (e.g., "Company", "Support", "Customer service").
- **Add up to N links** (no hard cap — typical use is 3-8 per column) via the **+ Add link** button.
- **Pick a link type per row** — Product, Product Category, Vendor, Blog, Blog Article, Page, Section, External URL.
- **Pick a target value** — autocomplete or select, scoped to the link type.
- **Override the caption** — defaults to the target's name when blank, but the merchant can overwrite.
- **Pick an icon** (FontAwesome class) — only when the active theme advertises `functions.navigations.icon.status`.
- **Toggle `open in new tab`** per row.
- **Delete individual rows** via the **Delete** button on each row.
- **Master enable / disable** the whole module — when off, nothing renders.

## Settings & fields

### Top-level fields

| Setting key | Type | Default | Allowed values | Limits | Validation | Notes |
|---|---|---|---|---|---|---|
| `enabled` | bool (switch) | `true` | `yes` / off | — | — | Master on/off for the instance |
| `title` | string | `null` | free text | 0-100 chars (lint: `char:0,100`) | optional | Heading shown above the link list |
| `links[]` | repeater | `[]` | array of link rows (see per-link table) | empty array NOT allowed on save | required: at least one row, else save errors | Each row is one link |

### Per-link fields (each row in `links[]`)

| Setting key | Type | Default | Allowed values | Validation | Notes |
|---|---|---|---|---|---|
| `link_type` | enum (select) | `product` | `product` / `category` / `vendor` / `blog` / `article` / `page` / `section` / `external` | required, must be one of the 8 enum values | Drives which `link_value` picker the form shows |
| `link_value` | mixed (depends on `link_type`) | — | target ID; section key; raw URL | required; validated against the chosen `link_type`'s existence check, or URL format for `external` | Free-form URL only for `external`; otherwise autocomplete or select |
| `link_caption` | string | "" | free text | required (cannot be empty) | Label the customer sees; no auto-fallback — merchant must fill it |
| `class` | string | "" | FontAwesome class | optional | Only shown when theme enables `functions.navigations.icon.status` |
| `blank` | bool (checkbox) | `false` | `true` / `false` | — | Open in `_blank` |

### Validation behaviour

On save, every link row is validated independently. Validation errors:

| Error | Trigger | Form-field key |
|-------|---------|----------------|
| *"Invalid request"* | `link_type` not in the 8 allowed values, or `links[]` array is missing/empty | top-level |
| *"Link value is required"* | `link_value` empty | `links[N][link_value]` |
| *"Link caption is required"* | `link_caption` empty | `links[N][link_caption]` |
| *"Invalid URL"* | `link_type: external` and URL not a valid format | `links[N][link_value]` |
| *"Product / Category / Vendor / Blog / Article / Page no longer exists"* | the chosen `link_type`'s target ID (or, for `section`, the section key) is not found | row-level |

### Theme-specific notes

- **Icon column visibility.** The `class` (icon) input only appears when the active theme advertises `functions.navigations.icon.status = true` in its theme config. Themes without this flag never expose the icon picker, and an icon class sent via the API is dropped on save.
- **Default link sets per theme.** Each theme ships its own DEFAULT link set (e.g., Echappe's `navigationLinks` defaults to Blog + Contacts shortcuts). Resetting reverts to those theme defaults.
- **Per-instance availability.** Not every theme ships every instance. Most themes ship `navigationLinks`; multi-column-footer themes also ship `footerLinks1-3`; only themes with a static-page menu ship `navigationLinksPage`.

## Business rules

### Flat lists only — distinct from `main` / `footer` menu trees

`navigation.links` is a flat list with 8 link types and NO nesting. The `main` / `footer` trees in [[design-navigation]] are richer: 4-level nesting plus 12 link types (the same 8 plus Snippet, Mega-menu, Banner, Heading). Use the trees for the headline menus; use this module for top-bar shortcuts and extra footer columns.

### Saving is destructive — no partial update

Each instance is stored independently. On **Save module**, the platform deletes ALL existing links for that instance and re-inserts the rows currently in the form. There is no partial update and no undo: if the merchant removes one row and saves, that link is gone. The storefront picks up the new links on the next request — save / Reset refresh the cache automatically.

### Empty `links[]` array on save → error

If the merchant clicks **Save module** with NO link rows, the save fails with *"Invalid request"*. To "disable" the module without losing all links, the merchant flips the `enabled` toggle off instead.

### Per-language captions via multylang

When the `multylang` app is installed, `link_caption` accepts per-language entries via the language switcher. Without it, only one caption is stored per row.

### No plan-gating

`navigation.links` is not in the `paid_widgets` allowlist — available on every plan.

### `mailto:` / `tel:` URLs work via `external` link type

For "Email us" or "Call us" links, the merchant picks `external` and enters `mailto:support@store.com` or `tel:+359...`. These validate as URLs and render with the protocol intact.

## Related

- [[design-modules-navigation]] — hub.
- [[design-navigation]] — the richer menu trees (`main` and `footer`).
- [[design-module-navigation-main]] — main menu module (renders the `main` tree).
- [[design-module-navigation-footer]] — footer menu module (renders the `footer` tree).
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme controls which instances appear and whether icons are exposed.

## Open questions

- 📡 **Icon picker availability.** Depends on the active theme's `functions.navigations.icon.status` setting; query the theme's settings to confirm whether the icon column is exposed.
- 📡 **Per-language link captions.** Captions store per-language sub-keys only when the `multylang` app is installed.
- ⏸️ **Maximum link count.** No hard cap — practical limit is theme rendering width. Test very long lists above ~20 rows.
