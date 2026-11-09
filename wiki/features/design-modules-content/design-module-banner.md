---
type: feature
nav_path: "Design → Modules → Content → Banner"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Изображения", "Images block", "Banner module", "Banner grid module", "Image banner module", "extra.banner", "Модул банер", "Банери", "homeSingleBanner", "bannersHomePage", "bannersTextPage", "pagesBanner", "productShowcaseBanners", "newProductsBanners", "bannerInSidebar"]
tags: [design, modules, content, banner, image, slider]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

# Banner module (`extra.banner`)

> Part of [[design-modules-content]].

## Purpose

The **Banner** module renders a grid (or slider) of 1–24 image banners: homepage rows, sidebar promos, banners on static pages, hero banners. Each slot holds an image, optionally linked to a product, category, vendor, blog, article, page, section or external URL. The same module backs many theme slots, each edited independently, and is the page builder's **Изображения** (Images) block on Dynamic pages, with the same editor.

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

Which instances exist depends on the active theme ([[design-themes]]); older themes ship fewer. On most themes `bannerInSidebar` is hidden on mobile.

## What the merchant can do here

- Set the number of slots (**Брой**, 1–24) and how many show per row (**Брой изображения на ред**, 1–12).
- Toggle **Покажи като слайдер** and **Покажи изображенията, който са без линк, в галерия**.
- Per slot (**Изображение 1**, **2**, …): **Избери изображение** (**От мястото за съхранение** / **Външно**), **Линк**, **Заглавие** (caption) and **Отвори в нов прозорец**.

What the merchant CANNOT do here:

- Add a new banner instance — the theme decides which slots exist. For new placements, use [[marketing-landing-pages]] Dynamic pages.
- Exceed 24 slots, or delete, hide or reorder a single slot — see **Slots: count, order and removal**.

## Settings & fields

### Module-level settings

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | `bool` | on | Master on / off; off renders nothing. |
| `amount` | dropdown 1–24 | `int:1,24` | 1 | Number of banner slots. |
| `per_row` | dropdown 1–12 | `int:1,12` | 1 | Banners per row on the grid. |
| `title` | text | `char:0,100` | empty | Accepted on save; the current editor has no field for it. |
| `enable_slider` | toggle | `bool` | off | Render the grid as a horizontal slider with arrows. |
| `enable_gallery` | toggle | `bool` | off | Clicking an image without a link opens a lightbox. |
| `banners[]` | repeater | — | empty | Per-slot config (one row per slot up to `amount`). |

### Per-banner fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | **image** / **script** | The current editor saves every slot as `image`; a `script` slot saved earlier still renders (verify). |
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

`homeSingleBanner`, `bannersHomePage`, `bannerInSidebar`, etc. are separate instances, each with its own config; editing one does not touch the others.

### Hard 1–24 slot cap, 1–12 per row cap

Enforced server-side. To go beyond, add another Images block on a Dynamic page.

### Slider mode replaces the static grid

With the slider on, the grid becomes a carousel with arrows, showing `per_row` slides at a time.

### Gallery mode applies to unlinked images only

With the gallery switch on, clicking an image **without a link** opens a lightbox cycling through the block's unlinked images. Images with a link still open their link; the gallery never overrides it.

### Slots: count, order and removal

There is no per-slot delete, hide or reorder control. **Брой** shows the first N slots, and lowering it drops the highest-numbered slots when you save. To remove a middle image, move the later images up one slot (re-pick image, link and caption) and lower the count. Every slot up to the count needs an image: saving with an empty one is refused with *"Източник на външното изображение е задължителен."*, so an empty slot never reaches the storefront. The switch beside the block's name turns the whole block on or off; **Заглавие** is the slot's caption and alt text. On a Dynamic page the block has no width or margin control of its own: it fills its column, and full width and spacing come from the row settings. It is removed with its round remove button (tooltip *Remove widget*, English only); edits go live after **Publish changes** ([[landing-pages-builder-rows]]).

### Default placeholder until first save

A new instance auto-fills each slot with a placeholder image and a storefront overlay ("Click here to add your first banner"). First save replaces it.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache; pages rendered afterwards show the change, while guests may get a cached page for up to 20 minutes ([[storefront-arch-caching-invalidation]]).

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme picker; controls which banner instances exist.
- [[design-navigation]] — same 8 link-kind picker semantics.
- [[marketing-landing-pages]] — Dynamic pages drop banners in arbitrary slots via the page builder.

## Open questions

- 📡 **Per-language banner content.** With `multylang`, banner captions and `src` accept per-language values via the language switcher.
