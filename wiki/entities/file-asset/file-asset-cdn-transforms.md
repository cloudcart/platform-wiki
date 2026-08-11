---
type: entity
nav_path: "Entity → File / Asset → CDN transforms"
aliases: ["CDN transforms", "the image delivery service", "Image transforms", "Image playground", "Image resize", "Image crop", "Pad to square", "SVG bypass", "Обработка на изображения", "Преоразмеряване", "Кадриране"]
tags: [entity, settings, media, storage, files, cdn, the image delivery service, images]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[file-asset]]. See the hub for the other aspects (storage model, quota, lifecycle, customer uploads, image pickers).

# File / Asset — CDN transforms

## Identity

**CDN transforms** are the on-demand image manipulations CloudCart serves through **the image delivery service**. When a storefront template requests an image with query parameters (e.g., `?w=400&h=400&crop=center&q=80`), the image delivery service generates and serves the resized / cropped / re-formatted variant from the original stored file. The **Image playground** tab in [[settings-files]] is a client-side URL composer that lets the merchant preview these transforms. One important exception: **SVG files bypass the image delivery service entirely** and are served as-is.

## Aliases

- **CDN transforms** / **image transforms** — the image delivery service-served variants.
- **the image delivery service** — the transform backend.
- **Image playground** — the URL-composer tab.
- **Pad to square** / **SVG bypass** — specific behaviours.
- **Обработка на изображения** / **Преоразмеряване** / **Кадриране** — Bulgarian equivalents.

## Key Attributes

| Transform | Parameter(s) | Notes |
|-----------|--------------|-------|
| **Resize** | `w` (width), `h` (height), `ex` (extension / format) | Drives storefront thumbnails / gallery sizes. |
| **Crop / gravity** | `ce` (centre), `no` / `so` / `we` / `ea` (N/S/W/E), `face` (face-aware), `sm` (smart) | Controls which part survives the crop. |
| **Format** | jpg / png / webp / avif | Auto-negotiated from the browser's `Accept` header by default. |
| **Quality** | `q` (1–100) | Lower = smaller file, lower fidelity. |
| **Pad colour** | `bg:HEX` (e.g., `bg:FFFFFF`) | Fills letterbox areas. |
| **Pad-to-square** | (store option) | When the store opts into square product images, the image delivery service pads to 1:1. |
| **SVG** | — | Bypasses the image delivery service entirely; served as-is from S3. |

## Relationships

CDN transforms operate on top of the [[file-asset-storage-model]]:

- The **original** stored file is the source; the image delivery service reads it and emits a derived variant.
- **Image vs document** routing is decided by MIME type — images go through the image delivery service, documents are direct downloads (see the `file_mime` attribute on [[file-asset]]).
- **SVG** is both a transform exception here and a security concern — see [[file-asset-storage-model]] for the no-antivirus / embedded-script risk.

## Where it appears

- [[settings-files]] — the **Image playground** tab.
- Every storefront template that renders catalog / blog / CMS imagery composes these parameters automatically.

### Image playground is a client-side URL composer

The Image playground tab in [[settings-files]] does **NOT** call backend endpoints to transform. It composes the CDN URL with query parameters (`?w=300&h=200&crop=face&q=80&bg=FFFFFF&...`) and lets the merchant's browser fetch the transformed image directly from the CDN. **Playground previews consume real CDN bandwidth** — each preview is a live fetch of a freshly-rendered variant, not a cached mock.

### CDN transform parameters

The image delivery service backend supports a documented set of transforms used by CloudCart's storefront templates:

- **Resize** — `w` (width), `h` (height), `ex` (extension / format conversion).
- **Crop / gravity** — `ce` (centre), `no` / `so` / `we` / `ea` (north / south / west / east), `face` (face-aware crop), `sm` (smart crop).
- **Format** — jpg / png / webp / avif (also auto-negotiated based on the browser's `Accept` header by default).
- **Quality** — 1–100 via the `q` parameter.
- **Pad colour** — `bg:HEX` (e.g., `bg:FFFFFF`).
- **Pad-to-square** — when the store has opted into square product images, the image delivery service pads to 1:1.

### SVG files bypass the image delivery service entirely

**SVG files are served as-is from S3** — no resize / format conversion happens on SVG. This is why SVG is the recommended format for logos and icons that must stay crisp at any size, and also why SVG carries an elevated security concern: because it bypasses image processing and can embed scripts, customer-uploaded SVGs should be treated as potentially hostile. See [[file-asset-storage-model]] for the no-antivirus rule.

## Related

- [[file-asset]] — hub.
- [[file-asset-storage-model]] — the original stored file the image delivery service reads; SVG bypass + security context.
- [[settings-files]] — the Image playground tab.
- [[product]] — product images are the most common transform consumers.
- [[settings-brand]] — brand / OG image assets also transform through the image delivery service.

## Open Questions

- ⏸️ Whether the merchant can set a store-wide default quality / format policy independent of per-request parameters.
- ⏸️ The full list of the image delivery service parameters exposed (the documented set above may not be exhaustive).
