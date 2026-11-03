---
type: feature
nav_path: "Design → Modules → Content → Background image"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Background image module", "extra.backgroundImage", "homeTextBackground", "footerTextBackground", "newProductsBackground", "categoryShowcaseBackground", "headerImage1", "headerImage2", "pageLoader", "Фон модул", "Заден фон"]
tags: [design, modules, content, background, image]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Background image module (`extra.backgroundImage`)

> Part of [[design-modules-content]]. See the category page for the other content modules.

## Purpose

The **Background image** module renders a single image as the background of a theme-defined slot — typically the slot behind a text block, behind the header, behind the homepage video section, or as the page-load indicator. It is a thin, single-image module with no link, no caption, and no per-slide structure — just an image picker plus an enable toggle.

Like the other content modules, the SAME module TYPE is instanced many times under different names — each instance fills a specific theme slot. The merchant edits each instance independently.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab.

Each background-image instance has its own card. Common instances on default-style themes:

| Instance | Theme slot | Display name |
|----------|------------|--------------|
| `homeTextBackground` | Background behind the homepage text block | **Homepage text - background** |
| `homeText1Background` / `homeText2Background` / `homeText3Background` | Backgrounds for the three homepage text blocks | **Homepage text 1 / 2 / 3 - photo** |
| `headerImage1` / `headerImage2` | Header background images | **Heather Image 1 / 2** |
| `homeTopBackground` | Background of the top banner section | **Banner text background at the top of the homepage** |
| `homeTopAfterCategoryBackground` | Background of the after-category-showcase banner | **Banner text background after categories** |
| `homeVideoBackgroundImage` | Homepage video section background | **Picture of the video section of the homepage.** |
| `latestNewsBackground` | Latest news section background | **Latest News - Background** |
| `categoryShowcaseBackground` | Category showcase background | **Showcase with categories - Background** |
| `newProductsBackground` | New products section background | **New products - Background** |
| `footerTextBackground` | Footer text section background | **Footer text - Background** |
| `pageLoader` | Page load indicator image | **Page load indicator** |

The exact list depends on the active theme.

## What the merchant can do here

- Toggle the background image on / off (enable / disable).
- Pick an image — Internal (file manager) or External (CDN URL).
- Save / Reset / Cancel.

What the merchant CANNOT do here:

- Link the image to anything — there is NO link field. Background images are decorative only.
- Set a caption, hover effect, focal point, or aspect ratio override.
- Specify separate desktop / mobile images. For responsive images use the [[design-module-banner]] or [[design-module-carousel]] modules instead.

## Settings & fields

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | `bool` | on | Master on / off. When off, the slot renders no background image. |
| `type` | select — **internal** / **external** | `in:internal,external` | external | Image source. **Internal** opens the file manager; **external** accepts a CDN URL. |
| `src` | text / file picker | `char:5,300` | empty | The image URL (file-manager picker auto-fills it). |

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists the image URL; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme-shipped defaults (typically a blank / placeholder image) | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

## Business rules

### Decorative only — no link, no caption

Background images are rendered as a CSS background on the theme's containing slot. They are NOT clickable. The theme decides which slot covers — the module only swaps the `src`. If the merchant wants a clickable promotional image, use [[design-module-banner]] instead.

### Min 5 chars / max 300 chars on `src`

The `src` field is validated as 5–300 characters. Short URLs and data-URLs under 5 chars are rejected; very long signed URLs above 300 chars are rejected. CDN URLs sit comfortably in this range.

### `pageLoader` is suppressed for Lighthouse audits

The `pageLoader` instance specifically hides itself when the request comes from a Lighthouse audit (the speed-test bot). This keeps the page-load indicator out of Lighthouse screenshots and prevents it from inflating the LCP (Largest Contentful Paint) score.

### Storage URL normalisation on save

On save, the platform passes the `src` through a storage URL writer that converts absolute CloudCart-storage URLs to a portable internal format. On read, the inverse runs to produce an absolute URL again. This is transparent to the merchant but means hand-crafted POSTs with raw absolute URLs are still accepted.

### Default content placeholder

A freshly-spawned background-image instance starts empty (`src=''`) — the theme either renders no image (when `enabled=true` but `src` empty) or falls back to a CSS gradient defined in the theme stylesheet, depending on the theme.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache key. The new image shows up on the very next storefront request.

## Theme-specific notes

- **The same `extra.backgroundImage` TYPE is used by ~10–15 instances on a default theme.** Each fills a different slot.
- **Mobile rendering** is theme-dependent. Most themes use the same background image on desktop and mobile, scaled / cropped via CSS `background-size: cover`. A few themes hide background images below a viewport-width breakpoint to keep mobile pages light.
- **Image format.** JPEG / PNG / WebP all work. Animated GIFs render but suffer high CPU cost — recommend static images.
- **No focal point / no aspect-ratio override.** If a tall image lands in a short slot, the theme's `background-position` rule decides the crop (usually `center center`). The merchant cannot adjust this from the module — they would need to crop the image themselves before uploading.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme picker; theme decides which slots use background images.
- [[design-module-banner]] — use this instead when the image needs a link or caption.
- [[design-module-text]] — paired with background-image instances on the same theme slot (text content + photo background).

## Open questions

- 📡 **Per-language background images.** With `multylang`, the `src` field could in principle accept per-language values (e.g., different copy-burnt-into-image per locale). GraphQL-resolvable: query whether the `multylang` app is installed (verify whether the module supports this).
- 📡 **WebP auto-conversion.** Whether the file manager auto-generates a WebP variant for uploads here, and whether the theme picks it up via `<picture>` — (verify) against the file-manager pipeline.
