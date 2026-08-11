---
type: feature
nav_path: "Settings → Brand settings → Favicon"
route_name: brand.settings
route_path: /admin/settings/brand
aliases: ["Favicon upload", "Browser tab icon", "Favicon cache-busting", "favicon_image", "favicon_time"]
tags: [settings, brand, favicon, cache-busting]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-brand]]. See the hub for related aspects (slots, upload flow, OG image, errors, cache & storage, limitations).

# Brand settings — Favicon

## Purpose

The Favicon slot — the browser tab icon, bookmark icon, and mobile home-screen icon. It is the only slot of the seven that uses a dedicated storage model (`FavIcon`) instead of the shared `Logo` model, and it is the only slot that clears extra settings on save (`favicon_image` and `favicon_time`) to defeat aggressive browser favicon caching.

## Where to find it

Sidebar → Settings → **Brand settings** → the **"Favicon"** card.

The card uses the same drag-and-drop UI as the other slots (see [[settings-brand-upload-flow]]). The recommended size is a square up to **240 × 240 px**. Browsers downscale to 16×16 / 32×32 for tab rendering — uploading at the full recommended size gives the platform headroom for high-DPI displays and mobile home-screen icons.

## What the merchant can do here

- Upload a square image (PNG / JPG / SVG / WebP) as the favicon.
- Re-upload to replace.
- Delete to revert to no-favicon state (browser falls back to its default favicon).
- Preview the favicon in the inline preview module (the favicon card DOES render the preview, unlike OG image).

## Settings & fields

### Storage backend — separate `FavIcon` model

The favicon does NOT share the `Logo` model used by `main`, `invoice`, `mail`, `default_image`, and `checkout`. Instead it has its own `FavIcon` model with its own row. The reasons:

- The favicon has independent dimension validation (the model rejects oversized or non-square images at the storage layer).
- The favicon's cache lifecycle is decoupled from the other logos because browsers cache favicons differently from regular images.
- Historical — the favicon predates the unified Logo model.

The merchant doesn't see this storage split; the card looks and behaves like the other six.

### Cache-busting on save / delete

Saving a favicon (or deleting one) clears **two** extra settings beyond the per-slot cache key flushed by every brand-asset save:

| Setting | What it does |
|---------|--------------|
| `favicon_image` | The cached favicon URL used by the page-rendering layer. Clearing forces a re-fetch on the next page render. |
| `favicon_time` | A versioned timestamp appended to the favicon URL (cache-bust suffix). Clearing forces the page-rendering layer to generate a fresh timestamp on the next request, which appears as a new URL to the browser. |

Without these two clears, the merchant would upload a new favicon, refresh the storefront, and still see the OLD favicon for hours or days because browsers cache favicons aggressively (often ignoring standard HTTP cache headers). The per-slot cache flush on its own (see [[settings-brand-cache-and-storage]]) is not enough — the browser-side cache also needs defeating.

### Recommended size

| Property | Value |
|----------|-------|
| **Recommended size** | Square, up to 240 × 240 px |
| **Backend label** | "Favicon" |
| **Storage backend** | `FavIcon` model (separate from `Logo`) |
| **Cache-bust side-effects on save** | Clears `favicon_image` + `favicon_time` settings |
| **Preview module** | Yes — renders the favicon in the browser-tab context |

### Accepted file formats

The `allowed_mimetypes` for the favicon slot defaults to `jpeg, jpg, jpe, png, svg, webp` (same as other slots, minus GIF). PNG with transparent background is the most common choice — it renders cleanly on both light and dark browser themes. SVG is accepted by the upload path but browser favicon support for SVG is inconsistent — PNG is the safer choice. See [[settings-brand-errors]] for the security note on SVG uploads.

## Business rules

### Delete behaviour — full row + file deletion

Deleting the favicon removes the `FavIcon` model row AND deletes the underlying file from the platform's file storage. This is different from:

- The other five logos (Logo model) — same behaviour: model row + file both deleted.
- The OG image (setting value) — only the setting value clears; the file becomes orphan storage and is pruned later by background sweep. See [[settings-brand-og-image]].

After delete, the storefront renders no `<link rel="icon">` tag (or falls back to a platform default depending on the theme), and the browser shows its default tab icon.

### Why browsers cache favicons aggressively

Standard HTTP cache headers are often ignored by browsers for favicons. Chrome, Firefox, and Safari each maintain their own favicon cache with TTLs measured in days or weeks. The platform's `favicon_image` + `favicon_time` cache-bust trick works by changing the favicon URL itself (via the appended timestamp), forcing the browser to treat it as a NEW file with a different URL.

This is why merchants who upload a new favicon and don't see the change should:

1. First, refresh the page — the new versioned URL should defeat the browser cache.
2. If the old favicon persists, the browser may have aggressively cached the OLD URL — a hard refresh (Ctrl+Shift+R / Cmd+Shift+R) or clearing the browser's cache for the site usually fixes it.
3. As a last resort, the merchant can close the tab and reopen — the new tab usually re-fetches.

### Dimension validation on the `FavIcon` model

The `FavIcon` model has its own dimension validation in its upload handler. Files that exceed the platform's favicon size limit (or that aren't square within tolerance) are rejected at upload time with a 422 response. The error message surfaces on the global error banner (see [[settings-brand-errors]]).

### No special handling beyond cache-busting

The favicon upload uses the same modern the request handler endpoint (`POST /admin/api/core/settings/logos/favicon`) as the other five non-OG slots. The only distinguishing behaviour is:

- Writes to the `FavIcon` model instead of the `Logo` model.
- Clears `favicon_image` + `favicon_time` settings on save / delete.
- Independent dimension validation rules.

The per-card UI (drag-and-drop, progress bar, re-upload, delete confirm) is identical to other slots — see [[settings-brand-upload-flow]].

## Related

- [[settings-brand]] — hub.
- [[settings-brand-slots]] — the Favicon slot's place in the seven-slot inventory.
- [[settings-brand-upload-flow]] — the per-card UI used by the Favicon card.
- [[settings-brand-cache-and-storage]] — per-slot cache flushing on every brand-asset save; this aspect documents the Favicon's additional cache-bust side-effects.
- [[settings-brand-errors]] — global error banner used when dimension validation fails.
- [[settings-brand-og-image]] — the OG image's different storage backend (setting value vs `FavIcon` model).

## Open questions

None.
