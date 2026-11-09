---
type: feature
nav_path: "Design → Modules → Content → Video slider"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Video slider module", "Video carousel module", "Reels module", "extra.videoSlider", "videoSlider", "Слайдър с видео", "Видео слайдер", "Видео карусел"]
tags: [design, modules, content, video, slider, plan-gated]
plan_gates: ["video_slider_widget"]
created: 2026-06-10
updated: 2026-11-09
source_count: 3
---

# Video slider module (`extra.videoSlider`)

> Part of [[design-modules-content]]. See the hub for the other content modules.

## Purpose

The **Video slider** is a multi-slide video carousel with arrows, dots, a progress bar, a mute button and per-slide buttons. Each slide plays a full-width video (or image), with an optional separate mobile file, under an overlay of up to three headings, a description and a button. It is plan-gated by `video_slider_widget`.

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Slider** group on the left sidebar. The instance name is `videoSlider`. Most themes do NOT ship it by default — see **Where the module comes from** under Business rules for how merchants add it.

## What the merchant can do here

- Toggle autoplay (2–15 s), arrows, dots, progress bar, mute button and pause-on-hover; set desktop (200–1000 px) and mobile (200–800 px) heights.
- Add, copy and remove slides, each with its own video, overlay and button.

What the merchant CANNOT do here:

- Use a YouTube or Vimeo link. The slide plays its address in the browser's own video player, so it must point to a video file (the field's hint names MP4), picked **От хранилище** (the store's files) or typed as **Външен URL**.

## Settings & fields

### Module-level settings

All toggles below are `yes` / `no` (validation `in:yes,no`).

| Field | Type | Restriction | Default | What it controls |
|-------|------|-------------|---------|------------------|
| `enabled` | toggle | — | on | Master on / off. |
| `autoplay` | toggle | — | yes | Auto-advance slides. |
| `interval` | number (ms) | `int:2000,15000` | 5000 | Time between advances (2–15 s). |
| `show_arrows` | toggle | — | yes | Prev / next arrows. |
| `show_dots` | toggle | — | yes | Pagination dots. |
| `show_progress` | toggle | — | yes | Per-slide progress bar. |
| `show_mute_btn` | toggle | — | yes | Customer mute button. |
| `pause_on_hover` | toggle | — | no | Pause autoplay on hover. |
| `height_desktop` | number (px) | `int:200,1000` | 700 | Desktop carousel height. |
| `height_mobile` | number (px) | `int:200,800` | 600 | Mobile carousel height. |
| `slides[]` | repeater | — | empty | Per-slide config — see below. |

### Per-slide fields

| Field | Type | Description |
|-------|------|-------------|
| `tab_title` | text (max 80) | Editor-only slide label. |
| `bg_type` | select | Fallback: `video` (default) or `image` poster. |
| `video_src` | URL (required) | Desktop video URL. |
| `video_mobile` | URL (optional) | Mobile video URL. |
| `video_src_type` / `video_mobile_type` | select | **От хранилище** / **Външен URL**. |
| `h1` / `h2` / `h3` | text | Three overlay heading lines. |
| `description` | text | Overlay sub-heading. |
| `h1_color` / `h2_color` / `h3_color` | colour | Heading colours. |
| `h1_size` / `h2_size` / `h3_size` | number (8–200) | Heading sizes — desktop. |
| `h1_size_mobile` / `h2_size_mobile` / `h3_size_mobile` | number (8–200) | Heading sizes — mobile. |
| `h1_font` / `h2_font` / `h3_font` | select | Font family — installed store fonts only. |
| `h1_weight` / `h2_weight` / `h3_weight` | select | Font weight `100`–`900`. |
| `h1_as_text` | toggle | Render H1 as plain text (avoids a second page H1). |
| `padding_x` / `padding_y` / `padding_x_mobile` / `padding_y_mobile` | number (0–500) | Overlay padding (px). |
| `overlay_color` | colour | Dimming-overlay colour. |
| `overlay_opacity` | number (0–100) | Overlay opacity %. |
| `text_align` | select | Horizontal: `left` / `center` / `right`. |
| `vertical_align` | select | Vertical: `top` / `middle` / `bottom`. |
| `button_label` | text | CTA label. |
| `button_href` | URL | CTA target. |
| `button_target` | select | `_self` (same tab) / `_blank` (new tab). |
| `button_size` | select | `small` / `medium` / `large`. |
| `button_style` | select | `fill` / `border`. |
| `button_bg` / `button_color` | colour | Button background / text colour. |
| `button_font_size` / `button_font_size_mobile` | number (8–200) | Button font size (px). |
| `button_weight` | select | Font weight `100`–`900`. |

Bulgarian labels in the editor: **Височина** with a laptop icon (desktop) and with a phone icon (mobile); per slide **Тип медия** (Видео / Изображение), **URL на фон (десктоп)** and **URL на фон (мобилен, по избор)**, each with **От хранилище** / **Външен URL** and **Източник**.

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Plan check first, then saves and regenerates storefront cache. | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults. | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes without saving. | None | — |

## Business rules

### PLAN-GATED — `video_slider_widget` required

Gated by the `video_slider_widget` plan feature in [[plan-gates]]. Without it the edit panel shows an upgrade prompt, saving fails and the storefront hides the module. A downgraded store keeps its saved slides but cannot edit or show them until it upgrades again.

### Every slide must have a desktop video URL

A slide with no desktop video URL is silently dropped on save. If that leaves zero slides, the save is rejected with an invalid-request error. Both video URLs are validated as URLs — an invalid value raises a field-level error on the offending slide.

### Enum and range coercion

Invalid values are corrected on save: alignments fall back to centre / middle, padding clamps to 0–500 px, font sizes to 8–200 px, overlay opacity to 0–100.

### Fonts are restricted to installed store fonts

A heading font not among the store's installed fonts is silently cleared; add it via **Storefront fonts** first.

### Defaults and cache

Default heights are 700 px desktop, 600 px mobile. Save and Reset renew the module cache; guests see changes within 20 minutes ([[storefront-arch-caching-invalidation]]).

### How the video fits the slider

The slider spans the full width of the area it sits in; its height is the desktop **Височина** value, or the mobile one at screen widths of 768 px or less. Each video (or image) is scaled to cover the whole frame and centred, so whatever does not match the frame's shape is cropped, never letterboxed. The platform sets no recommended ratio or file size: the frame's shape is that width divided by the height set, so keep the important part in the middle. Without a mobile URL, phones get the desktop video. Videos play muted and loop; the mute button unmutes. Every slide's video is marked to preload when the page opens, so keep files small and give phones a lighter file.

### Where the module comes from

Most themes do NOT ship a `videoSlider` instance. The merchant typically drops the **Слайдър с видео** block onto a Dynamic page in [[marketing-landing-pages]]; [[apps-video-slider-widget]] is the app that unlocks it.

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[apps-video-slider-widget]] — richer dedicated video-slide editor.
- [[design-module-carousel]] — image / mixed carousel (no plan gate).
- [[plan-gates]] — `video_slider_widget` gating.
- [[marketing-landing-pages]] — Dynamic pages can drop the Video Slider block in.

## Open questions

- 📡 **Plan-gate scope.** Whether `video_slider_widget` is on / off only, or whether higher plans allow more slides. (verify)
- 📡 **Per-language overlay copy.** Whether overlay text and button label store separate values per storefront language. (verify)
