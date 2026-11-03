---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Video"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Video module", "Video embed block", "YouTube embed", "Vimeo embed", "Модул видео"]
tags: [design, modules, page-builder, video, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Video block (`video`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Video** block embeds a video on a Dynamic page. The merchant picks the source (YouTube / Vimeo / VBOX7 / raw embed / HTML5 file) + the URL or embed code, and the block renders the video inline. Used for hero videos on landing pages, product launch videos, brand stories, and tutorial embeds.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Video** from the block picker.

## What the merchant can do here

- Pick the video **type**: `youtube` / `vimeo` / `vbox7` / `embed` / `html5`.
- Set the video **source** (`src`):
  - For YouTube / Vimeo / VBOX7: paste the video URL.
  - For Embed: paste the raw `<iframe>` snippet.
  - For HTML5: paste the URL of a hosted MP4 / WebM file.
- Toggle **Autoplay** — when ON, the video starts playing automatically (typically muted on autoplay, per platform).
- Toggle **Controls** (HTML5 only) — when ON, the browser's video controls show.
- Toggle **Loop** (HTML5 only) — when ON, the video restarts when it ends.
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot upload a video file directly from this block — for HTML5, the merchant must host the file elsewhere and paste the URL.
- The merchant cannot configure the video poster, thumbnail, or pre-roll ad — those are properties of the source platform.
- The merchant cannot pick the player skin — YouTube / Vimeo / VBOX7 each render their own player.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `type` | select | `youtube` | `youtube` / `vimeo` / `vbox7` / `embed` / `html5`. |
| `src` | text input + textarea | `''` | Video URL or `<iframe>` embed code. Single-line input for URL types; multi-line textarea for `embed` and `html5`. |
| `autoplay` | toggle | `false` | Autoplay on page load (typically muted). |
| `controls` | toggle | `true` | (HTML5 only) Show browser video controls. |
| `loop` | toggle | `false` | (HTML5 only) Restart when ended. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Type-specific URL parsing

The module extracts the video ID from the source URL via regex per type:

| Type | Pattern | Renders |
|------|---------|---------|
| `youtube` | `youtube.com/watch?v=ID` or `youtu.be/ID` (11-char ID) | `<iframe src="https://youtube.com/embed/{ID}?mute=1[&autoplay=1]" ...>` |
| `vimeo` | `vimeo.com/ID` or `player.vimeo.com/video/ID` | `<iframe src="https://player.vimeo.com/video/{ID}?muted=1[&autoplay=1]" ...>` |
| `vbox7` | `vbox7.com:tag:ID` (verify exact format) | `<iframe src="https://www.vbox7.com/emb/external.php?vid={ID}&mute=1[&autoplay=1]" ...>` |
| `embed` | Raw HTML | Renders verbatim — merchant pastes a full `<iframe>` block. |
| `html5` | URL to a hosted file | `<video><source src="{URL}"></video>` with the autoplay / controls / loop toggles applied. |

Invalid URLs result in an empty iframe — the merchant gets no error, just a broken video frame.

### Muted-by-default for autoplay compliance

YouTube / Vimeo / VBOX7 / HTML5 all force `mute=1` (or `muted` attribute) so autoplay is allowed by browser policy. The merchant cannot start an unmuted autoplay video — the policy is browser-enforced.

### `embed` is raw HTML

For the `embed` type, the merchant pastes the FULL `<iframe>` snippet (e.g., the share-embed code from a hosting platform). The module renders it verbatim — no rewriting. The merchant is responsible for valid HTML.

### `html5` toggles only matter for HTML5

`controls`, `loop`, and the per-video `autoplay` flag only affect the `html5` type. For YouTube / Vimeo / VBOX7, the autoplay flag is added to the iframe URL but `controls` and `loop` are ignored — those are controlled by the platform.

### Wrapping container

The storefront renders the video inside `<div class="textbox-iframe">` — themes target this class for sizing / aspect-ratio constraints (typically 16:9 with a `max-width: 100%`).

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-code]] — sibling: raw HTML / JS block (alternative for non-standard video embeds).
- [[design-modules]] — theme-wide `extra.videoSlider` module (paid; multi-video carousel).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **VBOX7 URL format.** The regex splits on `:` then takes the last element — confirm the exact share URL format VBOX7 produces. (verify)
- 📡 **HLS / DASH live streams.** Confirm whether the `html5` type supports live HLS / DASH manifests, or only progressive MP4 / WebM files. (verify)
