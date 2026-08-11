---
type: feature
nav_path: "Settings → Brand settings → OG image"
route_name: brand.settings
route_path: /admin/settings/brand
aliases: ["OpenGraph image", "OG image upload", "Cover image for sharing", "og_image_url", "Facebook share image", "Twitter share image"]
tags: [settings, brand, og-image, opengraph, social-sharing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-brand]]. See the hub for related aspects (slots, upload flow, favicon, errors, cache & storage, limitations).

# Brand settings — OG image

## Purpose

The OG image slot (`og_image_url`) is the only one of the seven brand-asset slots that does NOT save into a logo model row. Instead it stores a public URL string in the platform's settings — the URL is then exposed in the storefront's `<meta property="og:image">` tag for Facebook, Twitter, and other social-platform scrapers. Because the OG image needs a stable public URL reachable by external scrapers, the upload flow is two-step instead of one and the slot does NOT show the inline preview module the other six slots do.

## Where to find it

Sidebar → Settings → **Brand settings** → the **"Cover image for sharing"** card (the OG image slot — `og_image_url`).

The card uses the same drag-and-drop UI as the other slots (see [[settings-brand-upload-flow]] for the per-card UI) — but the underlying upload is a two-call sequence, not a single POST.

## What the merchant can do here

- Drop or pick an image file to upload as the OG image.
- See a single progress bar that animates through both backend calls — the merchant doesn't see that two HTTP requests happen.
- Delete the OG image (clears the URL setting; the underlying file becomes orphan storage — pruned later by a background sweep).
- Re-upload to replace the OG image (re-runs both steps).

What the merchant CANNOT do here:

- Preview the OG image in context — the OG card is the ONE slot that does NOT render the `SettingsBrandPreviewLogoAppearance` module. The merchant must use Facebook's Sharing Debugger or Twitter's Card Validator to preview externally.
- Upload more than one OG image at a time.

## Settings & fields

### Two-step upload flow

When the merchant drops or picks a file on the OG image card, the page makes TWO sequential HTTP calls:

| Step | Endpoint | What it does |
|------|----------|--------------|
| **Step 1** | `POST /admin/api/core/settings/files/upload?value=og_image_url` with the raw file. | Stores the file on the platform's file storage and returns `{status, url, msg}`. If `status === 'error'`, the toast surfaces `msg`, the upload halts, nothing is committed. |
| **Step 2** | `POST /admin/api/core/settings/logos/og_image_url` with form data `og_image_url=<url from step 1>`. | Persists the URL in `setting('og_image_url')`. The backend validates that the URL is non-empty. |

The merchant sees a single progress bar that animates through both calls. Failure in either step shows the global error banner (see [[settings-brand-errors]]) and the card reverts to its previous state.

This is the ONLY slot using this two-step pattern. The other six slots are a SINGLE `POST /admin/api/core/settings/logos/{slot}` with the (client-side-resized) file — see [[settings-brand-upload-flow]].

### NO client-side resize for OG image

Unlike the other six slots, the OG image file does NOT pass through the client-side resize helper. The raw file is sent as-is in Step 1. The reason: the OG image needs to remain at the merchant's intended dimensions for accurate rendering on Facebook / Twitter previews — resizing in-browser could distort or under-size the image for share contexts.

Recommended dimensions: **200 × 240 px** (the platform default). Facebook recommends at least 1200 × 630 px for high-resolution rendering; merchants targeting large share previews should upload at that size or larger and rely on the social platforms' own scaling.

### Recommended size and storage path

| Property | Value |
|----------|-------|
| **Recommended size** | 200 × 240 px (the platform default — merchants targeting Facebook/Twitter previews can upload larger) |
| **Storage backend** | Setting value (`setting('og_image_url')`), a URL string — NOT a logo model row |
| **Underlying file location** | The platform's file storage; the URL is returned by step 1 |
| **No preview module** | The OG card does NOT render the inline preview the other six slots do |

## Business rules

### `og_image_url` lacks the in-place preview module

By design, the OG image card does NOT render the inline preview module. The other six slots do — they show the merchant how the uploaded asset will appear in its actual context (storefront header, invoice header, email header, etc.). The OG image, being an external-platform asset (Facebook etc.), is hard to preview accurately in-app and so is omitted. Merchants verify the OG image externally via Facebook's Sharing Debugger (`developers.facebook.com/tools/debug`) or equivalent.

### Orphan-file pruning on delete

When the merchant deletes the OG image, the platform clears the setting value but does NOT immediately delete the underlying file from storage. The file remains accessible at its original URL because:

- Social platforms (Facebook, Twitter, LinkedIn) cache OG image URLs for days or weeks. Hard-deleting the file would break already-cached previews on social feeds.
- A platform-wide background sweep (`CleanupOrphanFilemanagerFilesCommand`) periodically scans the platform's file storage for files no longer referenced in the database and removes them. The orphan OG image file gets cleaned up on the next sweep cycle.

The merchant doesn't need to do anything — quota is reclaimed automatically. The practical implication: the orphan file may stay accessible at its original URL for some time after deletion, then disappears once the sweep runs.

### Two-step failure handling

If Step 1 fails (e.g., file too large, network error, invalid mimetype), Step 2 never runs and nothing is committed. The error message comes from `msg` in the Step 1 response and is promoted to the toast + the global error banner. The card reverts to its previous state.

If Step 1 succeeds but Step 2 fails (rare — Step 2 just persists a URL), the platform ends up with an orphan file in storage but no `og_image_url` setting set. The same background sweep cleans this up. The card reverts to its previous state and the merchant sees the error banner.

### URL persistence on deactivation / theme switch

Because the OG image is stored as a setting value (URL string), it survives storefront theme switches without re-upload. The URL points to a stable file in the platform's storage and is rendered into every theme's storefront HTML via the meta tag. Deactivating a theme does NOT clear the OG image setting.

### Single OG image per store — no per-storefront variants

The OG image setting is store-scoped, not storefront-scoped. A merchant running multiple storefronts (multi-language, multi-region) shares the same OG image across all of them. See [[settings-brand-limitations]] for the broader no-per-storefront-variants rule.

## Related

- [[settings-brand]] — hub.
- [[settings-brand-slots]] — the OG image slot's place in the seven-slot inventory.
- [[settings-brand-upload-flow]] — the one-call flow used by the other six slots; this aspect documents how the OG image deviates.
- [[settings-brand-errors]] — global error banner used to surface OG image step 1 / step 2 failures.
- [[settings-brand-cache-and-storage]] — the orphan-file sweep that eventually reclaims deleted OG images.
- [[settings-files]] — generic file upload screen reused as Step 1 of the OG image flow.

## Open questions

None.
