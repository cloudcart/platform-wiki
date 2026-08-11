---
type: feature
nav_path: "Design → Modules → Content → Banners"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Banner module", "Banner grid", "Homepage banners", "Sidebar banner", "Single banner", "Promo banner module", "Banner showcase", "Script banner", "Модул банери", "Модул банер"]
tags: [design, modules, content, banners]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Content modules — Banners

> Part of [[design-modules-content]]. See the hub for the carousel hero, text blocks, video, page-builder modules, and storage mechanics.

## Purpose

The banner module family renders **grids of 1-24 image banners** (or scripts) used for secondary promotional placements: homepage banner rows, sidebar banners, banners between product showcases, banners on static pages. Each banner links to a product / category / vendor / blog / article / page / section / external URL — or carries raw HTML / JS for third-party embed code.

Banners are the workhorse of secondary marketing. Where the `carousel` hero owns the above-the-fold campaign slot, banners populate every other promotional surface the theme provides.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Images** group. The set of named banner instances depends on the active theme — most themes ship between 2 and 8 banner cards.

All banner instances share the same underlying module map: `extra.banner`.

## What the merchant can do here

- Open any banner card to edit its grid (1-24 slots).
- Switch a slot between **image** banners and **script** banners.
- Link each banner to one of 8 destinations.
- Toggle slider mode (`enable_slider`) to convert the grid into a horizontal slider.
- Toggle lightbox mode (`enable_gallery`) so clicking opens an image gallery.
- Save / Reset / Cancel — full pipeline in [[design-modules-content-storage]].

The merchant CANNOT add a NEW banner instance — only the named instances the active theme ships are exposed. For a brand-new banner slot, build a Dynamic page in [[marketing-landing-pages]].

## Settings & fields

### Banner instances (theme-named)

Each instance is independent — `bannersHomePage` and `bannerInSidebar` are completely separate rows of stored JSON. The naming convention tells the merchant which slot it fills:

- `homeSingleBanner` — one big banner on the homepage.
- `bannersHomePage` — multi-banner row on the homepage.
- `pagesBanner` — banner on static pages.
- `bannerInSidebar` — sidebar banner on category-listing pages.
- `newProductsBanners` — banner row near the "New products" section.
- `productShowcaseBanners` — banner row inside a product showcase.
- `bannersTextPage` — banner on text / blog-style pages.

### Top-level controls (shared by every banner instance)

| Field | Type | Description / Validation | Default |
|-------|------|--------------------------|---------|
| `enabled` | toggle | Master on/off | on |
| `amount` | dropdown 1-24 | How many banner slots to render | 1 |
| `per_row` | dropdown 1-12 | Banners per row (responsive grid) | 1 |
| `title` | text (0-100 chars) | Optional heading shown above the banner grid | empty |
| `enable_slider` | toggle | Treat the banners as a slider instead of a static grid | off |
| `enable_gallery` | toggle | Open the banner image in a lightbox gallery on click | off |
| `banners[]` | repeater (1-24 slots) | Per-banner config — see below | empty |

### Per-banner fields (1-24 slots)

| Field | Description |
|-------|-------------|
| `type` | **image** (default) or **script** — switches the form between an image picker and a raw HTML / JS textarea |
| `img_type` | **Internal** (file manager) / **External** (URL) — only when `type=image` |
| `src` | Image URL |
| `link_type` | 8 options: **(no link)**, **Product**, **Product Category**, **Vendor**, **Blog**, **Blog Article**, **Page**, **Section**, **External** |
| `link_value` | The target (autocomplete or select varying by `link_type`) |
| `caption` | Short text overlay (≤200 chars) shown on hover or below the banner |
| `blank` | Open in new tab toggle (`_blank`) |
| `script` | Only when `type=script` — raw HTML / JS pasted into a 6-row textarea. Useful for embedding third-party banner scripts |

## Business rules

### Grid layout — `amount` × `per_row`

`per_row` lets the merchant build a clean N-column grid (e.g., 6 banners at 3 per row gives two rows of three). At `amount=1` the grid degenerates to a single banner.

### Slider mode vs grid

`enable_slider` converts the static grid into a horizontal slider — useful when there are more banners than fit on one row, or when the merchant wants horizontal scroll on mobile.

### Lightbox / gallery mode

`enable_gallery` makes clicking a banner open it in a lightbox gallery — useful for image-heavy banners where the click destination is the image itself rather than a product page.

### Script banners — no sanitisation

The `script` banner type accepts raw HTML / JS with **no server-side sanitisation**. Useful for Google Ads, third-party affiliate modules, or custom JavaScript embeds — but a broken script can break the page. The merchant is fully responsible for valid markup.

### Image source — Internal vs External

For `type=image`, the merchant picks the file manager (Internal) or a CDN URL (External). Same trade-off as the carousel — see [[design-modules-content-carousel]].

### `htmlLine` is a related but distinct module

The `htmlLine` promo strip looks like a "banner" but is classified under Navigation because it sits in the header / footer chrome. Its settings live on [[design-modules-navigation]] — this aspect doesn't document them. The dual classification exists because `htmlLine` carries a marketing message + CTA (Content-style) inside a chrome slot (Navigation-style).

### Plan-gating

All banner modules are universally available — no plan feature required.

## Tips

- Upload all banners in the same aspect ratio — the grid renders cleanly when sizes match.
- The same banner module map (`extra.banner`) powers multiple instances — picking the right INSTANCE matters more than picking the right module type.
- For mobile-responsive layouts, set `per_row` to a number that divides evenly into 12 (the underlying responsive grid).
- The `script` type is the right escape hatch for affiliate networks, A/B-test snippets, and one-off third-party embeds.

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-carousel]] — hero slider; banners share the link-picker model.
- [[design-modules-content-text]] — sibling for written marketing copy.
- [[design-modules-content-storage]] — Save / Reset pipeline + script sanitisation note.
- [[design-modules-navigation]] — owns the `htmlLine` promo-strip settings.
- [[products-banners-labels]] — product-level promotional badges (a different feature with the same word "banner").
- [[design-themes]] — theme decides which banner instances exist.

## Open questions

None.
