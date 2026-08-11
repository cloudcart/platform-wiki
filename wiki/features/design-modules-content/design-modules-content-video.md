---
type: feature
nav_path: "Design → Modules → Content → Video"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Video module", "Video slider module", "videoSlider module", "Reels module", "Storefront video", "Video carousel", "Модул видео", "Модул видео слайдер"]
tags: [design, modules, content, video, plan-gated]
plan_gates: ["video_slider_widget"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Content modules — Video and Video slider

> Part of [[design-modules-content]]. See the hub for the carousel hero, banners, text blocks, page-builder modules, and storage mechanics.

## Purpose

Two distinct modules:

1. **`videoSlider`** — a multi-slide video carousel (Instagram-Reels-style) with text overlays, navigation arrows, dots, progress bars, and mute / pause controls. Each slide is one video plus text + CTA overlay. **Plan-gated** by `video_slider_widget`.
2. **`video`** (page-builder block) — a single-video embed that goes inside a Dynamic page. Supports YouTube / Vimeo / Vbox7 / raw embed code / HTML5 direct media. Not plan-gated. Settings documented inline below; placement mechanics in [[design-modules-content-page-builder]].

The two share no settings or storage — they exist as separate modules that both happen to render video. This page documents both because they answer the same merchant question (*"how do I put a video on my storefront?"*).

## Where to find it

### `videoSlider`

Sidebar → **Design** → **Modules** → **Others** tab → **Slider** group → **Video slider** card.

The card is only clickable on plans that include the `video_slider_widget` feature. Without it, clicking surfaces a plan-upgrade prompt. The module map is `extra.videoSlider`.

### `video` (page-builder)

Only inside a Dynamic page in [[marketing-landing-pages]]. Open the page builder, add a `video` block from the block picker. Not exposed on the Modules screen.

## What the merchant can do here

For `videoSlider`:

- Toggle the slider on/off.
- Configure global controls — autoplay, interval, arrows, dots, progress bar, mute button, hover-pause, desktop / mobile height.
- Configure each slide — desktop + mobile video URLs, fallback image, text overlay, CTA link.
- Save / Reset / Cancel.

For the page-builder `video` block:

- Pick the source platform (YouTube / Vimeo / Vbox7 / Embed / HTML5).
- Paste the URL or embed code.
- Toggle autoplay, controls (HTML5 only), loop (HTML5 only).
- Live-preview the embed in the edit panel.

What the merchant CANNOT do:

- Edit `videoSlider` without the `video_slider_widget` plan feature.
- Add a NEW `videoSlider` instance from the Modules screen — only the instances declared by the active theme appear (many themes ship none).
- Place a `video` block outside a Dynamic page — `video` is page-builder-only.

## Settings & fields

### `videoSlider` — top-level controls

| Field | Type | Description / Validation | Default |
|-------|------|--------------------------|---------|
| `enabled` | toggle | Master on/off | on |
| `autoplay` | toggle — **yes** / **no** | Auto-advance between slides | yes |
| `interval` | number (ms, 2000-15000) | Time between auto-advances | 5000 |
| `show_arrows` | toggle — **yes** / **no** | Show previous / next arrows | yes |
| `show_dots` | toggle — **yes** / **no** | Show pagination dots | yes |
| `show_progress` | toggle — **yes** / **no** | Show the per-slide progress bar | yes |
| `show_mute_btn` | toggle — **yes** / **no** | Show the customer-facing mute button | yes |
| `pause_on_hover` | toggle — **yes** / **no** | Pause auto-advance when the customer hovers | no |
| `height_desktop` | number (px, 200-1000) | Carousel height on desktop | 700 |
| `height_mobile` | number (px, 200-800) | Carousel height on mobile | 600 |
| `slides[]` | repeater | Per-slide config — see below | |

### `videoSlider` — per-slide fields

| Field | Description |
|-------|-------------|
| `video_src` | Desktop video URL (required, validated as URL) |
| `video_mobile` | Mobile video URL (optional, validated as URL) |
| `bg_type` | **video** (default) or **image** — fallback when video can't autoplay |
| `text_align` | **center** / **left** / **right** |
| `vertical_align` | **top** / **middle** / **bottom** |
| Heading / sub-heading / CTA text + link | Overlay copy (per-slide) |

### Page-builder `video` block — fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `type` | dropdown — **YouTube** / **Vimeo** / **VBOX7** / **Embed** / **HTML5** | Source platform — picks the URL parsing / embed strategy | YouTube |
| `src` | text input OR textarea | The video URL (YouTube / Vimeo / Vbox7 watch link) OR raw embed code (when `type=Embed`) OR direct media URL (when `type=HTML5`) | empty |
| `autoplay` | toggle | Auto-play the video on page load (subject to browser policy — usually requires `muted` too) | off |
| `controls` | toggle | Show play / pause / volume controls (only for `HTML5`) | on |
| `loop` | toggle | Restart the video when it ends (only for `HTML5`) | off |

## Business rules

### `videoSlider` plan-gating

Gated by the `video_slider_widget` plan feature. The check runs in BOTH the module-open and module-save controller actions — merchants without the plan-feature can neither open the edit panel nor POST a save. The module is also HIDDEN from the storefront when the plan is inactive.

Saved `videoSlider` data is **preserved** across plan downgrades. The merchant can't edit it and the storefront doesn't show it, but re-upgrading restores both. See [[design-modules-content-storage]] for the per-instance preservation rule.

### Mobile vs desktop video

Always provide BOTH desktop and mobile video URLs on `videoSlider`. Mobile bandwidth and aspect ratios differ markedly from desktop — using the same file on both yields poor playback and cropping.

### Browser autoplay policy

Most modern browsers block autoplay unless the video is `muted`. Both `videoSlider` and the page-builder `video` block respect this — silent slides autoplay; slides with audio require a customer click. Keep videos short (5-15 seconds) and silent by default.

### Fallback image on `videoSlider`

Setting `bg_type=image` provides a poster image for slides where the video can't autoplay (slow connection, blocked autoplay). The poster shows while the video loads or in place of the video on devices that refuse to autoplay.

### Page-builder `video` source types

- **YouTube** / **Vimeo** / **VBOX7** — paste the full watch URL; the module parses the video ID.
- **Embed** — accepts raw `<iframe>` code from any video host.
- **HTML5** — direct media URL (`.mp4`, `.webm`) — host the file yourself or use a CDN. Only `HTML5` exposes `controls` and `loop`.

### Plan-gating summary

| Module | Plan feature | Effect when missing |
|--------|--------------|---------------------|
| `videoSlider` | `video_slider_widget` | Edit blocked, storefront hidden; data preserved |
| `video` (page-builder) | None (the Page Builder URL is gated by `storefront_builder` — see [[design-modules-content-page-builder]]) | n/a |

## Tips

- For the dedicated app-style configuration of `videoSlider`, see [[apps-video-slider-widget]].
- Use a 9:16 aspect ratio for `videoSlider` mobile slides — matches phone screens and the Reels aesthetic.
- Use the `bg_type=image` fallback liberally — many customers visit on slow networks where video can't autoplay quickly enough.
- For `video` HTML5 mode, host on a CDN — origin-served `.mp4` files murder page-load times.

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-carousel]] — sibling `carousel` hero slider.
- [[design-modules-content-page-builder]] — the page-builder `video` placement rules.
- [[design-modules-content-storage]] — plan-gate enforcement + data preservation on downgrade.
- [[apps-video-slider-widget]] — dedicated app surface for the Video Slider module.
- [[plan-gates]] — `video_slider_widget` plan feature.
- [[marketing-landing-pages]] — Dynamic pages host the page-builder `video` block.

## Open questions

None.
