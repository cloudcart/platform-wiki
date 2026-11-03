---
type: feature
nav_path: "Settings → Brand settings → Cache & storage"
route_name: brand.settings
route_path: /admin/settings/brand
aliases: ["Brand cache invalidation", "Brand boarding_settings flag", "Brand legacy vs modern endpoint", "Brand orphan file cleanup", "Logo cache flush"]
tags: [settings, brand, cache, storage, infrastructure]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-brand]]. See the hub for related aspects (slots, upload flow, OG image, favicon, errors, limitations).

# Brand settings — Cache & storage

## Purpose

What happens behind the scenes when a brand asset is saved or deleted — the per-slot cache flush, the `boarding_settings` flag bump that signals onboarding progress, the two-endpoint legacy-vs-modern split (only the modern path is used by the Vue Brand settings page), and the background orphan-file pruning that reclaims storage from deleted OG images. This aspect catalogues the side-effects merchants and support agents need to know about but don't see directly in the UI.

## Where to find it

The side-effects documented here fire automatically on every successful upload or delete on the Brand settings page (`/admin/settings/brand`). The merchant doesn't trigger them explicitly — they happen as part of the save flow. Support agents diagnosing "the new logo doesn't show up" or "onboarding still says we haven't set up branding" should check these mechanisms.

## What the merchant can do here

The merchant doesn't directly control cache or storage behaviour. What they observe:

- Uploaded logos appear in the storefront / admin immediately on the next page load (per-slot cache flush makes this feel "instant").
- The onboarding wizard's branding step gets marked complete after the first successful upload (the `boarding_settings` flag).
- Favicons may take a hard refresh to appear due to browser-side caching (see [[settings-brand-favicon]]).
- Deleted OG images may remain accessible at their original URL for some time before the background sweep removes them (see [[settings-brand-og-image]]).

## Settings & fields

### Per-slot cache flush

Every successful logo save flushes ONLY the cache entry for that specific slot via a tagged-cache removal (`logo.<slot>`). Saving the main store logo does NOT bust the invoice logo cache. Each slot's cache is independent. This is what makes uploads feel "instant" — the storefront / admin sees the new logo on the next page load without waiting for any global cache invalidation cycle.

### `boarding_settings` flag

Every successful logo save also bumps `setting('boarding_settings')` to 1. This flag is read by the onboarding wizard to decide whether the merchant has completed the branding step. Practical implications:

- A merchant going through onboarding will see the branding step marked complete after the first successful upload to ANY of the seven slots.
- The flag is set per-store, not per-slot. Saving a second or third logo does NOT change the flag (it's already 1).
- Deleting all brand assets does NOT reset the flag back to 0 — the merchant is considered "post-onboarding" once they've completed the step.

### Two endpoints serve this page — legacy vs modern, same slots

There are TWO separate controllers handling the seven brand-asset slots:

| Path | Endpoint pattern | Used by | Notes |
|------|------------------|---------|-------|
| **Modern** | `POST /admin/api/core/settings/logos/{type}` | The Vue Brand settings page documented in this wiki | Returns `150x150` image URL on success. Handles `og_image_url` (the two-step flow). No SVG rejection on invoice. |
| **Legacy** | `POST /admin/api/core/settings/general/logo/{type}` | Older admin templates (rare today) | Returns `300x300` image URL on success. Does NOT handle `og_image_url`. Rejects SVG on the `invoice` slot with *"settings.logo_image_upload_error_svg"*. |

Both paths write to the same underlying `Logo` and `FavIcon` model storage — so the result is interchangeable, but error messages and slot acceptance differ. Practical implication: a merchant uploading through the modern Brand settings UI may successfully upload an SVG to the Invoice slot, but the legacy upload path would reject it. The PDF invoicing pipeline may not render SVG correctly regardless — recommendation: use PNG or JPG for the Invoice slot. See [[settings-invoicing]].

### Storage backends

Three storage backends total across the seven slots:

| Backend | Slots using it | What it stores |
|---------|---------------|----------------|
| `Logo` model | `main`, `invoice`, `mail`, `default_image`, `checkout` | Model row with `type=<slot>` + the underlying file in the platform's file storage. |
| `FavIcon` model | `favicon` only | Separate model row + the file. See [[settings-brand-favicon]] for the cache-busting side-effects. |
| Setting value | `og_image_url` only | URL string in `setting('og_image_url')`; the file lives on the platform's file storage. See [[settings-brand-og-image]]. |

## Business rules

### Orphan-file pruning for OG image

When the merchant deletes the OG image, the platform clears the setting value but does NOT immediately delete the underlying file from storage (the file might still be referenced from Facebook / Twitter cached previews). Cleanup is handled by a platform-wide background command (`CleanupOrphanFilemanagerFilesCommand`) that periodically sweeps storage for files no longer referenced in the database and removes them.

Practical implication: the orphan OG image file may stay accessible at its original URL for some time after the merchant deletes it from the OG slot, then disappears once the sweep runs. The merchant doesn't need to do anything — quota is reclaimed automatically on the next sweep cycle.

Other six slots delete both the row and the underlying file synchronously, so no orphan accumulates.

### Cache flush is per-slot, not global

There is no "flush all brand caches" operation. Each slot's cache key (`logo.<slot>`) is independent. This makes single-slot uploads fast (no broad invalidation) at the cost that, in theory, a bug in one slot's save couldn't somehow corrupt another slot's cache.

For Favicon specifically, the per-slot cache flush is supplemented by clearing `favicon_image` + `favicon_time` to defeat browser-side favicon caching — see [[settings-brand-favicon]].

### No queue / no notifications / no webhooks fired

Saving / deleting any brand asset is purely synchronous: file upload → DB write → cache clear → response. No background jobs, no admin notifications, no `*.updated` webhooks fired from this page. This is different from product or order writes which broadcast extensively. The reason: brand assets are merchant-internal configuration — there is no external consumer that needs to know.

### Delete restores empty state

Deleting:

- For `og_image_url`: the saved URL is cleared but the underlying file in storage is NOT deleted (becomes orphan; pruned by background sweep).
- For `favicon`: the `FavIcon` model row + the underlying file are both deleted.
- For all other logos: the `Logo` model row + the underlying file are both deleted.

The card returns to the empty drop-zone state; the merchant can upload a replacement immediately. The per-slot cache is cleared on delete just as on save.

### Storefront serves new asset on next page render

Because the per-slot cache flush is synchronous with the save, the next storefront page render after a save pulls the fresh logo (cache miss → DB read → re-cache). No propagation delay — the merchant can save and immediately refresh the storefront to see the change. (Exception: the favicon, due to browser-side caching outside the platform's control — see [[settings-brand-favicon]].)

## Related

- [[settings-brand]] — hub.
- [[settings-brand-favicon]] — Favicon's additional cache-bust side-effects (`favicon_image` + `favicon_time`).
- [[settings-brand-og-image]] — the OG image's orphan-file pruning mechanism in detail.
- [[settings-brand-upload-flow]] — the upload sequence whose final step triggers everything documented here.
- [[settings-brand-errors]] — 422 response handling and the legacy-vs-modern SVG acceptance difference.

## Open questions

None.
