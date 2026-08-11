---
type: feature
nav_path: "Design → Modules → Content → Carousel"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Carousel module", "Slider module", "Hero slider", "Slideshow module", "Homepage carousel", "Модул карусел", "Модул слайдер"]
tags: [design, modules, content, carousel, slider]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Content modules — Carousel

> Part of [[design-modules-content]]. See the hub for banners, text blocks, video, page-builder modules, and storage mechanics.

## Purpose

The `carousel` module renders the **big marketing slider** at the top of the homepage — the prominent above-the-fold slideshow that rotates through campaigns, new arrivals, and brand messaging. Each slide is a desktop / mobile image, an external image URL, or an embedded video, with optional caption, HTML overlay, link target, and a per-slide schedule.

This is the most-edited content module on most stores. Every theme ships at least one `carousel` instance; some themes also use it on category pages or as a section divider.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Slider** group → **Slider** card.

Click the card to open the edit panel — the module map is `extra.carousel`.

## What the merchant can do here

- Toggle the carousel on/off via the master `enabled` switch.
- Set the number of slides (`amount`, 1-15) and the global transitions / controls.
- Configure per-slide images (desktop + mobile), HTML overlays, captions, link targets, and schedule.
- Save / Reset / Cancel — full pipeline in [[design-modules-content-storage]].

The merchant CANNOT add a NEW `carousel` instance from this screen — only the instances declared by the active theme exist. A dedicated landing-page slider can be built via the page builder in [[marketing-landing-pages]].

## Settings & fields

### Top-level controls

| Field | Type | Description / Validation | Default |
|-------|------|--------------------------|---------|
| `enabled` | toggle | Master on/off | on |
| `amount` | dropdown 1-15 | Number of slides to display | 2 |
| `full_width` | dropdown — **yes** / **no** | Stretch the carousel to viewport edges (vs constrained to content width) | yes |
| `caption` | dropdown — **yes** / **no** | Show the per-slide caption overlay | yes |
| `controls` | dropdown — **yes** / **no** | Show previous / next arrows | yes |
| `indicators` | dropdown — **yes** / **no** | Show pagination dots | yes |
| `animate` | dropdown — **Slide** (no) / **Fade** (yes) | Transition effect between slides | Slide |
| `autoplay` | dropdown — **yes** / **no** | Auto-advance slides on a timer | yes |
| `interval` | number (ms, range 1000-20000) | Time between auto-advances | 5000 |
| `cycle` | dropdown — **yes** / **no** | Loop back to the first slide after the last | yes |
| `pause` | dropdown — **yes** / **no** | Pause auto-advance when the customer hovers | yes |
| `slides_per_view` | dropdown 1-8 | Number of slides visible at once (only on the a theme that ships it theme) | 1 |
| `is_homepage_slider` | dropdown — **yes** / **no** | Flag for homepage placement (only on the a theme that ships it theme) | no |

### Per-slide fields (repeat 1-15 times based on `amount`)

| Field | Description |
|-------|-------------|
| `caption` | Short text overlay shown on the slide |
| `img_type` | **Internal** (file manager) / **External** (URL) / **Video** (YouTube / Vimeo / Wistia URL) |
| `src` | The image URL (auto-filled when picking from file manager) |
| `img_type_mobile` / `src_mobile` | Separate mobile-optimised image (recommended) |
| `html` | Optional HTML overlay — rich text positioned over the slide |
| `horizontal_position` / `vertical_position` | Caption / HTML positioning (left / center / right; top / middle / bottom) |
| `link_type` | What clicking the slide opens — 8 options: **Product**, **Product Category**, **Vendor**, **Blog**, **Blog Article**, **Page**, **Section**, **External**, or none |
| `link_value` | The target (autocomplete or select varying by `link_type`) |
| `link_caption` | Optional label for the CTA |
| `target` | **_self** (same tab) / **_blank** (new tab) |
| `sorting` | Sort order — slides render in ascending sorting weight |
| `from` / `to` | Schedule the slide — outside the window, the slide is hidden |

## Business rules

### Per-slide scheduling

Set `from` and `to` per slide to plan campaigns weeks ahead — a Black Friday slide configured three weeks before the date will auto-appear and auto-disappear without merchant intervention. Outside the window the slide is hidden from the storefront.

### Desktop + mobile images

The merchant should upload BOTH a desktop and a mobile image — many themes render at very different aspect ratios on phones, and a desktop-only image crops awkwardly. The `img_type_mobile` / `src_mobile` pair is per-slide.

### Image source — Internal vs External

`img_type=Internal` picks from the CloudCart file manager. `img_type=External` accepts a CDN URL — faster page speed, but the merchant is responsible for keeping the image alive on the third-party server.

### Video slides embed via iframe

When `img_type=Video`, the carousel embeds an iframe pointing at the watch URL (YouTube / Vimeo / Wistia). Autoplay / muting follows browser policy — usually requires `muted` to autoplay. If autoplay isn't kicking in, check the storefront markup.

### a theme that ships it theme exposes extra controls

`slides_per_view` and `is_homepage_slider` only render in the form on the a theme that ships it theme. On other themes the controls don't appear — the underlying settings are still stored but ignored at render time.

### Plan-gating

The `carousel` module is universally available — no plan feature is required.

## Tips

- For better page-speed scores, use **External** image type with a CDN URL rather than uploading huge files to the file manager.
- Use ascending `sorting` to reorder slides without re-uploading — small numbers render first.
- For video slides, ensure the embed URL is the full watch URL — the module parses the ID at render time.
- Keep the carousel ≤ 5 slides for above-the-fold homepages; longer slideshows hurt LCP and rarely get viewed past slide 3.

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-banners]] — sibling banner modules share the link-picker model.
- [[design-modules-content-text]] — `textCarousel` shares the same scheduling + autoplay shape.
- [[design-modules-content-video]] — `videoSlider` for Reels-style video carousel.
- [[design-modules-content-storage]] — Save / Reset pipeline + cache invalidation.
- [[design-themes]] — theme decides which `carousel` instances exist and which extra fields render.

## Open questions

None.
