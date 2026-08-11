---
type: feature
nav_path: "Design → Modules → Content → Banner"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Banner module", "Banner grid module", "Image banner module", "extra.banner", "Модул банер", "Банери", "homeSingleBanner", "bannersHomePage", "bannersTextPage", "pagesBanner", "productShowcaseBanners", "newProductsBanners", "bannerInSidebar"]
tags: [design, modules, content, banner, image, slider]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Banner module (`extra.banner`)

> Part of [[design-modules-content]].

## Purpose

The **Banner** module renders a grid (or slider) of 1–24 promotional image / script banners — homepage rows, sidebar promos, banners between product showcases, banners on static pages, and full-width hero banners. Each slot holds either an image (linked to a product, category, vendor, blog, article, page, section, or external URL) or a raw HTML / JS script for third-party banner code. The same module type backs many storefront instances, one per theme slot; the merchant edits each independently.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Images** group. Each banner instance has its own card; click it to open the side panel.

| Instance | Theme slot | Display name |
|----------|------------|--------------|
| `homeSingleBanner` | Single big homepage banner | **Homepage banner** |
| `bannersHomePage` | Multi-banner row on the homepage | **Banners - Index** |
| `bannersTextPage` | Banner on text pages | **Banners - Text page** |
| `pagesBanner` | Banner on static pages | **Banner in static pages** |
| `newProductsBanners` | Row near the "New products" section | **Banners in new products** |
| `bannerInSidebar` | Sidebar banner on category-listing pages | **Banners in the sidebar** |
| `productShowcaseBanners` | Row inside a product showcase | **Banners** |

The catalogue of instances depends on the active theme — switching themes via [[design-themes]] changes which appear. Older themes ship fewer slots (sometimes only `bannersHomePage` and `homeSingleBanner`); newer marketing-heavy themes ship 6+. On most themes `bannerInSidebar` is hidden on mobile.

## What the merchant can do here

- Set the number of slots (1–24) and how many render per row (1–12); add an optional title above the grid.
- Toggle **Enable slider** (horizontal carousel) and **Enable gallery** (clicks open a lightbox).
- Per banner: pick image OR script, image source (file manager / external URL), what clicking opens (8 link kinds), a caption, and whether the link opens in a new tab.
- Save (regenerates storefront cache) / Reset (theme defaults) / Cancel.

What the merchant CANNOT do here:

- Add a new banner instance — the theme decides which slots exist. For new placements, use [[marketing-landing-pages]] Dynamic pages.
- Exceed 24 slots per instance, or have CloudCart sanitise `script` content — it goes through as-is.

## Settings & fields

### Module-level settings

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | `bool` | on | Master on / off; off renders nothing. |
| `amount` | dropdown 1–24 | `int:1,24` | 1 | Number of banner slots. |
| `per_row` | dropdown 1–12 | `int:1,12` | 1 | Banners per row on the grid. |
| `title` | text | `char:0,100` | empty | Optional heading above the grid. |
| `enable_slider` | toggle | `bool` | off | Render the grid as a horizontal slider with arrows. |
| `enable_gallery` | toggle | `bool` | off | Clicking a banner opens a lightbox overlay. |
| `banners[]` | repeater | — | empty | Per-slot config (one row per slot up to `amount`). |

### Per-banner fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | select — **image** / **script** | Switches the slot between an image picker and a raw HTML / JS textarea. Default `image`. |
| `img_type` | select — **internal** / **external** | Image source (`type=image` only). **internal** opens the file manager; **external** takes a CDN URL. |
| `src` | text / file picker | Image URL; auto-filled from the file manager. |
| `link_type` | select — see "Link types" | What clicking the banner opens. |
| `link_value` | autocomplete or select | Target item (varies by `link_type`). |
| `caption` | text — max 200 chars | Overlay caption shown on hover or below. |
| `target` | select — **_self** / **_blank** | Open in same tab (`_self`) or new tab (`_blank`). |
| `script` | textarea (6 rows) | Raw HTML / JS (`type=script` only). No server-side sanitisation. |

### Link types

The `link_type` dropdown offers the same 8 options as [[design-navigation]] menu links:

| Value | What it links to | `link_value` picker |
|-------|------------------|---------------------|
| (empty) | No link — banner not clickable | — |
| `product` | A single product | Product autocomplete |
| `category` | A product category | Category select |
| `vendor` | A vendor (brand) | Vendor select |
| `blog` | A blog | Blog select |
| `article` | A single blog article | Article autocomplete |
| `page` | A static / dynamic page | Page autocomplete |
| `section` | A theme section anchor | Section select |
| `external` | A merchant-typed URL | Free-text URL |

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists the form; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults; one default banner re-injected | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

## Business rules

### One module type — many independent instances

`homeSingleBanner`, `bannersHomePage`, `bannerInSidebar`, etc. are separate instances of the same module, each with its own config. Editing one does NOT touch the others; the instance name tells which theme slot it fills.

### Hard 1–24 slot cap, 1–12 per row cap

Enforced server-side — `amount=25` or `per_row=13` is rejected before saving. To go beyond, add another instance via the page builder, or use multiple instances (theme-dependent).

### Slider mode replaces the static grid

With **Enable slider** on, the grid becomes a horizontal carousel with prev / next arrows, reusing `per_row` as the slides-per-view count. Arrows and autoplay inherit the theme's carousel styling.

### Gallery mode is image-click-to-lightbox

With **Enable gallery** on, clicking any `image` banner opens a lightbox cycling through all banners in that instance. This OVERRIDES the per-banner `link_type` and `target` — clicks open the lightbox, not the linked target.

### `script` slots accept raw HTML / JS — no sanitisation

A `script` slot renders its textarea contents directly into the page with no sanitisation, so a broken `<script>` or unclosed `<div>` cascades into the layout — the merchant owns valid markup. This is intentional: the escape hatch for embedding Google Ads, affiliate modules, and tracking pixels. The `script` and `image` types use separate, theme-overridable templates.

### Default placeholder until first save

A new instance auto-fills each slot with a placeholder image and a storefront overlay ("Click here to add your first banner"). First save replaces it.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache; the storefront reflects the change on the next request — no manual cache-clear needed.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme picker; controls which banner instances exist.
- [[design-navigation]] — same 8 link-kind picker semantics.
- [[marketing-landing-pages]] — Dynamic pages drop banners in arbitrary slots via the page builder.

## Open questions

- 📡 **Per-language banner content.** With `multylang`, banner captions and `src` accept per-language values via the language switcher.
- 📡 **Script-slot sanitisation.** No server-side sanitisation today (verify). A "warn before save" prompt on `<script>` tags could prevent accidental page breakage.
