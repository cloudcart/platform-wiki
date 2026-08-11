---
type: feature
nav_path: "Design → Modules → Content → Text carousel"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Text carousel module", "extra.text-carousel", "Testimonials module", "Quotes module", "Rotating text module", "textCarousel", "Текстов карусел", "Ротация на цитати"]
tags: [design, modules, content, carousel, testimonials, text]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Text carousel module (`extra.text-carousel`)

> Part of [[design-modules-content]]. See the category page for the other content modules.

## Purpose

The **Text carousel** module is a rotating text-only slider — typically used for testimonials, customer quotes, rotating taglines, social-proof statements, or rotating marketing messages. Each slide is a rich-text block (TinyMCE) with an optional caption and an optional date schedule. The carousel cycles through them on a timer.

It is the natural choice when the merchant wants prominent rotating COPY without images — for image carousels use [[design-module-carousel]]; for full-screen video showcases use [[design-module-video-slider]].

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Text fields** or **Testimonials** group on the left sidebar (depending on theme).

Each text-carousel instance has its own card. The common instance is `textCarousel`. Some themes ship multiple instances (e.g., `testimonialsCarousel` for a testimonials section + `topCarousel` for a rotating header announcement).

## What the merchant can do here

- Set the number of slides (1–15).
- Toggle full-width vs constrained layout.
- Choose how many slides are visible at once (1–8).
- Toggle caption / controls (prev / next arrows) / indicators (pagination dots) visibility.
- Toggle autoplay + set the interval between auto-advances.
- Toggle cycle (loop back to first after last) and pause-on-hover.
- Set the space (in px) between visible slides.
- Per slide: enter the caption, the rich-text HTML body, a sort weight, and an optional From / To date schedule.
- Save / Reset / Cancel.

What the merchant CANNOT do here:

- Add images per slide — the slides are text-only. For image slides use [[design-module-carousel]].
- Link each slide to a target — the text-carousel has no per-slide link. Embed a link inside the HTML body instead.
- Exceed 15 slides per instance.

## Settings & fields

### Module-level settings

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | — | on | Master on / off. |
| `amount` | dropdown 1–15 | `in:1,2,3,...,15` | 2 | Number of slides. |
| `full_width` | dropdown — **yes** / **no** | `in:yes,no` | yes | Stretch to viewport edges or constrain to content width. |
| `slides_per_view` | dropdown 1–8 | `int:1,20` | 1 | How many slides are visible at once. |
| `caption` | dropdown — **yes** / **no** | `in:yes,no` | yes | Show per-slide caption. |
| `controls` | dropdown — **yes** / **no** | `in:yes,no` | yes | Show prev / next arrows. |
| `indicators` | dropdown — **yes** / **no** | `in:yes,no` | yes | Show pagination dots. |
| `autoplay` | dropdown — **yes** / **no** | `in:yes,no` | yes | Auto-advance slides on a timer. |
| `interval` | number (ms) | `int:1000,20000` | 5000 | Time between auto-advances. Range 1–20 seconds. |
| `cycle` | dropdown — **yes** / **no** | `in:yes,no` | yes | Loop back to slide 1 after the last. |
| `pause` | dropdown — **yes** / **no** | `in:yes,no` | yes | Pause autoplay on hover. |
| `space_between` | number (px) | `int:0,120` | 0 | Gap (in px) between visible slides. Useful when `slides_per_view > 1`. |
| `slides[]` | repeater | — | empty | Per-slide config. |

### Per-slide fields

| Field | Description |
|-------|-------------|
| `caption` | Short heading / caption for the slide. |
| `html` | Rich-text body (TinyMCE) — the main content. Supports headings, lists, links, inline images. |
| `sorting` | Sort weight — slides render in ascending order. |
| `from` / `to` | Optional schedule — outside the window the slide is hidden. |

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Persists settings; regenerates storefront cache | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme-shipped defaults (2 placeholder slides) | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes the panel without saving | None | — |

## Business rules

### Hard 1–15 slide cap

The `amount` value is restricted to 1–15. The platform internally allows `slides_per_view` up to 20 (the `int:1,20` restriction), but the form's dropdown caps at 8 — and even 8 makes sense only when slides are very narrow.

### Autoplay interval is 1–20 seconds

The `interval` value is restricted to 1000–20000 ms. Anything below 1 second is unreadable; anything above 20 seconds is effectively static. The platform rejects values outside this range on save.

### Per-slide From / To schedule

Each slide carries an optional `from` and `to` date — outside the window, the slide is hidden by the rendering code (not just visually — it's removed from the slide array before the carousel initialises). This is the standard pattern for scheduling time-limited testimonials, post-event customer feedback, or season-specific quotes.

### `space_between` only matters when `slides_per_view > 1`

When `slides_per_view = 1`, only one slide is visible at a time and `space_between` has no visible effect. Set it to 20–40 px when showing 2–3 slides side-by-side to give them visual breathing room.

### Same Swiper engine as the image carousel

The text carousel renders through the same Swiper-based JavaScript engine as [[design-module-carousel]]. Autoplay, pause-on-hover, navigation arrows, and pagination dots inherit the global theme styling.

### Rich-text HTML body — same restrictions as `extra.text`

The per-slide `html` field is a TinyMCE block. The allowed-tag list matches the [[design-module-text]] module — headings, lists, links, inline images, basic inline HTML. `<script>` and `<iframe>` are stripped.

### Cache invalidation on save / reset

Both **Save** and **Reset** regenerate the per-site cache key. The storefront picks up the new configuration on the very next request.

## Theme-specific notes

- **Universal in TYPE — instance-specific.** Most themes ship a `textCarousel` instance for the homepage testimonials slot. Some themes also use it for rotating header announcements (a substitute for [[design-module-banner]] script slots).
- **Testimonial-card styling** is theme-controlled. The module emits a clean `<div>` per slide; the theme stylesheet decides whether each slide gets a card border, a customer-avatar circle, or a quote-mark decoration.
- **Inline images** (customer photos) work via the TinyMCE image picker — but for many testimonials with photos the result is often better with a manually built page in [[marketing-landing-pages]].
- **`controls` and `indicators` toggle independently** — some themes hide indicators by default for editorial polish; the merchant can flip them back on.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[design-themes]] — theme picker; theme decides which text-carousel instances exist.
- [[design-module-carousel]] — image carousel (use this for image-based hero slides).
- [[design-module-text]] — single static text block (use this for non-rotating copy).
- [[design-module-video-slider]] — full-screen video carousel (plan-gated).

## Open questions

- 📡 **Per-language slide content.** With `multylang`, each slide's `caption` and `html` accept per-language entries via the language switcher. GraphQL-resolvable: query whether the `multylang` app is installed.
- 📡 **Accessibility — keyboard navigation.** Whether `controls` arrows are keyboard-focusable and slides are announced by screen readers (verify in the rendered Swiper config).
