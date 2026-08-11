---
type: feature
nav_path: "Design → Modules → Content → Carousel"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Carousel module", "Slider module", "Homepage slider", "Hero slider", "extra.carousel", "carousel", "homepageCarousel", "Слайдер", "Модул слайдер", "Карусел"]
tags: [design, modules, content, carousel, slider, homepage]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Carousel / Slider module (`extra.carousel`)

> Part of [[design-modules-content]]. See the category page for the other content modules.

## Purpose

The **Carousel** module renders the homepage hero slider — a 1–15 slide animated carousel of images or videos with captions, HTML overlays, links, and per-slide schedules. It is the marketing centrepiece above the fold on most stores.

Each slide can be a desktop image, a mobile-optimised image, or an embedded video; can carry an HTML overlay positioned via horizontal / vertical alignment; can link to any of the 8 standard link kinds; and can be auto-shown / auto-hidden by a From–To date range.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Slider** group on the left sidebar.

The main instance is `carousel` (display name **Slider**). Some themes ship additional instances (e.g., `homepageCarousel` for a secondary slider mid-page).

## What the merchant can do here

- Set how many slides display (1–15).
- Toggle full-width vs constrained layout; toggle caption / arrows / pagination dots.
- Pick **Slide** vs **Fade** transition.
- Toggle autoplay + interval (1–20 s); toggle cycle (loop) + pause-on-hover.
- Per slide: pick desktop image (internal / external / video URL) and mobile image, write the caption, add and position an HTML overlay, pick a link target + label, set open-in-new-tab, set sort weight, and set a From / To schedule.
- Save / Reset / Cancel.

What the merchant CANNOT do here:

- Exceed 15 slides. For more, use multiple carousel instances or [[marketing-landing-pages]].
- Set a per-slide animation effect or autoplay interval — both are module-wide.

## Settings & fields

### Module-level settings

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | — | on | Master on / off. |
| `amount` | dropdown 1–15 | `in:1,2,3,...,15` | 2 | Number of slides. |
| `full_width` | **yes** / **no** | `in:yes,no` | yes | Stretch to viewport edges. |
| `caption` | **yes** / **no** | `in:yes,no` | yes | Show per-slide captions. |
| `controls` | **yes** / **no** | `in:yes,no` | yes | Show prev / next arrows. |
| `indicators` | **yes** / **no** | `in:yes,no` | yes | Show pagination dots. |
| `animate` | **Slide** / **Fade** | `in:yes,no` | Slide (`no`) | Transition style. |
| `autoplay` | **yes** / **no** | `in:yes,no` | yes | Auto-advance on a timer. |
| `interval` | number (ms) | `int:1000,20000` | 5000 | Time between auto-advances (1–20 s). |
| `cycle` | **yes** / **no** | `in:yes,no` | yes | Loop back to first slide after last. |
| `pause` | **yes** / **no** | `in:yes,no` | yes (hover) | Pause autoplay on hover. |
| `slides_per_view` | dropdown 1–8 | `int:1,20` | 1 | Slides visible at once. a theme that ships it only (`verify`). |
| `is_homepage_slider` | **yes** / **no** | `in:yes,no` | no | Homepage-placement flag. a theme that ships it only (`verify`). |
| `slides[]` | repeater | — | empty | Per-slide config. |

### Per-slide fields

| Field | Description |
|-------|-------------|
| `caption` | Short overlay caption shown on the slide. |
| `img_type` | **Internal** (file manager) / **External** (URL) / **Video** (YouTube / Vimeo / Wistia URL). |
| `src` | The desktop image URL — auto-filled when picking from the file manager. |
| `img_type_mobile` | Same options as `img_type` — for the mobile image. |
| `src_mobile` | The mobile image URL. Recommended even when matching the desktop image, for smaller responsive variants. |
| `html` | Optional rich-text HTML overlay positioned over the slide. |
| `horizontal_position` | **left** / **center** / **right** — overlay horizontal anchor. |
| `vertical_position` | **top** / **middle** / **bottom** — overlay vertical anchor. |
| `link_type` | What clicking the slide opens — 8 options: (empty), **product**, **category**, **vendor**, **blog**, **article**, **page**, **section**, **external**. Same picker semantics as [[design-module-banner]]. |
| `link_value` | The target item (varies by `link_type`). |
| `link_caption` | Optional CTA label on the overlay. |
| `target` | **_self** (same tab) / **_blank** (new tab). |
| `sorting` | Sort weight — slides render in ascending order. |
| `from` / `to` | Optional schedule — outside the window the slide is hidden. |

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme-shipped defaults (typically 2 placeholder slides) | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

## Business rules

### Hard 1–15 slide cap

`amount` is capped at 15 — larger numbers are rejected on save. For more visual content, use multiple carousel instances or Dynamic pages.

### Autoplay interval is 1–20 seconds

`interval` is bounded at 1000–20000 ms (1–20 s). Values outside this range are rejected on save.

### Per-slide From / To schedule auto-shows / auto-hides slides

Each slide carries an optional `from` and `to` date. Outside the window the slide is removed before the carousel initialises — not just hidden via CSS. This is the standard tool for scheduling Black Friday, Christmas, Easter, and other time-bound campaigns weeks in advance.

### Default content placeholder

A freshly-spawned carousel auto-fills each slide with a placeholder image plus the helper overlay ("Click here to add your first slide"). On first save, the placeholder is replaced.

### Mobile image is recommended, not required

If `src_mobile` is empty, the carousel falls back to `src` (the desktop image) on mobile, which often crops badly given different aspect ratios. Always supply both desktop and mobile images.

### Video slides — autoplay caveats

When `img_type=video`, the slide embeds a YouTube / Vimeo / Wistia player. Browser autoplay policy requires the video to be muted to start without user interaction. If a merchant says "my video isn't autoplaying", check that mute is on.

### Transition is module-wide

`animate=yes` is fade; `animate=no` (default) is slide. The merchant cannot pick different effects per slide.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache key. The storefront picks up the new configuration on the very next request.

### Theme-controlled rendering

Every theme ships at least one `carousel` instance (typically `carousel` on the homepage). Some rendering is theme-specific: `horizontal_position` / `vertical_position` are translated to CSS classes by the theme, and older themes only honour vertical (`top / middle / bottom`) positioning. Full-width mode also varies — most themes stretch edge-to-edge, some keep a small margin under a fixed-width header. The `slides_per_view` and `is_homepage_slider` controls appear only on the a theme that ships it theme.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme picker; theme decides which carousel instances exist.
- [[design-module-banner]] — same 8 link-kind picker semantics; use for static banner grids instead of sliding hero.
- [[design-module-text-carousel]] — text-only rotating carousel (testimonials).
- [[design-module-video-slider]] — full-screen video showcase carousel (plan-gated).
- [[marketing-landing-pages]] — Dynamic pages let the merchant drop a carousel into any slot via the page builder.

## Open questions

- 📡 **Per-language slide content.** With `multylang`, each slide's `caption`, `html`, and `link_caption` accept per-language entries via the language switcher. GraphQL-resolvable: query whether the `multylang` app is installed.
- 📡 **a theme that ships it extra controls.** Whether `slides_per_view` and `is_homepage_slider` are restricted to the a theme that ships it theme — (verify).
