---
type: feature
nav_path: "Design → Modules → Content → Video slider"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets
aliases: ["Video slider module", "Video carousel module", "Reels module", "extra.videoSlider", "videoSlider", "Видео слайдер", "Видео карусел"]
tags: [design, modules, content, video, slider, plan-gated]
plan_gates: ["video_slider_widget"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Video slider module (`extra.videoSlider`)

> Part of [[design-modules-content]]. See the hub for the other content modules.

## Purpose

The **Video slider** is a multi-slide video carousel — Instagram-Reels-style — with navigation arrows, pagination dots, progress bars, mute / pause controls, and per-slide CTAs. Each slide plays a full-bleed video (with a separate mobile video and an image fallback) plus a typographic overlay (H1 / H2 / H3 + description + button). It is plan-gated by `video_slider_widget` (see **Business rules**).

## Where to find it

Sidebar → **Design** → **Modules** → **Others** tab → **Slider** group on the left sidebar. The instance name is `videoSlider`. Most themes do NOT ship it by default — see **Where the module comes from** under Business rules for how merchants add it.

## What the merchant can do here

- Toggle the slider on / off, autoplay (interval 2–15 s), arrows, dots, progress bar, mute button, and pause-on-hover.
- Set desktop (200–1000 px) and mobile (200–800 px) carousel heights.
- Add and configure slides — each with its own video, text overlay and CTA button (full list under **Settings & fields**).
- Save / Reset / Cancel.

What the merchant CANNOT do here:

- Open or save the module on a plan without `video_slider_widget` — see **Business rules**.
- Use an unsupported video host — the URL is validated only as a URL, so the merchant must host the video where the browser can stream it (YouTube, Vimeo, a CDN-hosted MP4, etc.).
- Have CloudCart auto-generate poster images — the merchant supplies the image fallback.

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
| `video_src_type` / `video_mobile_type` | text | Optional media-type hint. |
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

### Save / Reset / Cancel

| Button | Action | Confirmation | Success message |
|--------|--------|--------------|------------------|
| **Save module** | Plan check first, then saves and regenerates storefront cache. | None | *"Module successfully edited"* |
| **Reset module** | Reverts to theme defaults. | *"Are you sure you want to reset this module?"* | *"Module successfully reset"* |
| **Cancel** | Closes without saving. | None | — |

## Business rules

### PLAN-GATED — `video_slider_widget` required

Gated by the `video_slider_widget` plan feature in [[plan-gates]]. Without it, opening the edit panel shows a plan-upgrade prompt, a save fails before validation, and the module is hidden from the storefront. A merchant who saved on a higher plan and then downgrades keeps the saved configuration (not deleted) but loses view / edit access and storefront rendering until re-upgrading.

### Every slide must have a desktop video URL

A slide with no desktop video URL is silently dropped on save. If that leaves zero slides, the save is rejected with an invalid-request error. Both video URLs are validated as URLs — an invalid value raises a field-level error on the offending slide.

### Enum and range coercion

Invalid values are corrected automatically: fallback type to `video`, text alignment to `center`, vertical alignment to `middle`. Padding clamps to 0–500 px, font sizes to 8–200 px, overlay opacity to 0–100. Heading weights must be blank or `100`–`900`.

### Fonts are restricted to installed store fonts

A heading font not in the store's installed-fonts list is silently reset to empty. The merchant adds fonts via **Storefront fonts** first.

### Defaults and cache

Default heights are 700 px desktop, 600 px mobile. Both **Save** and **Reset** regenerate the storefront cache, so changes show on the next storefront request.

### Autoplay and mobile bandwidth

Browsers block autoplay of videos with audio, so videos play muted by default; customers tap the mute button for sound. Video files are large — always provide a mobile-optimised mobile video URL (lower resolution / bitrate) so mobile customers don't burn data.

### Where the module comes from

Most themes do NOT ship a `videoSlider` instance. The merchant typically adds it via a Dynamic page in [[marketing-landing-pages]] — drop the Video Slider block onto the page. A richer dedicated editor lives at [[apps-video-slider-widget]]. (verify whether the two surfaces share saved data.)

## Related

- [[design-modules-content]] — hub.
- [[design-modules]] — parent module catalogue.
- [[apps-video-slider-widget]] — richer dedicated video-slide editor.
- [[design-module-carousel]] — image / mixed carousel (no plan gate).
- [[design-module-text-carousel]] — text-only rotating carousel.
- **Storefront fonts** — source of the H1 / H2 / H3 font choices.
- [[plan-gates]] — `video_slider_widget` gating.
- [[marketing-landing-pages]] — Dynamic pages can drop the Video Slider block in.

## Open questions

- 📡 **Plan-gate scope.** Whether `video_slider_widget` is on / off only, or whether higher plans allow more slides. (verify)
- 📡 **Per-language overlay copy.** Whether overlay text and button label store separate values per storefront language. (verify)
- 📡 **Mobile video aspect ratio.** Whether the module crops mobile videos to fill or letterboxes off-ratio ones. (verify)
