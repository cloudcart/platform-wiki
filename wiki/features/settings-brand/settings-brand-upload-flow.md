---
type: feature
nav_path: "Settings → Brand settings → Upload flow"
route_name: brand.settings
route_path: /admin/settings/brand
aliases: ["Brand upload flow", "Drag-and-drop logo upload", "Logo upload UI", "Re-upload icon", "Brand asset progress bar"]
tags: [settings, brand, upload, drag-and-drop, ui]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-brand]]. See the hub for related aspects (slots, OG image, favicon, errors, cache & storage, limitations).

# Brand settings — Upload flow

## Purpose

The per-card upload UI used by six of the seven brand-asset slots — drag-and-drop, click-to-upload, progress bar, re-upload (↻) icon, delete (trash) icon, and the "Remove logo?" confirmation modal. Plus the client-side image resize step that runs before any file leaves the browser. The OG image slot uses a different flow — see [[settings-brand-og-image]].

## Where to find it

Sidebar → Settings → **Brand settings**. Each slot is rendered as an independent card. The upload UI lives inside each card and operates per-slot — there is no bulk-upload mode.

## What the merchant can do here

- **Drag-and-drop** an image file onto the empty placeholder, OR click anywhere on the placeholder to open the file picker.
- **Re-upload** an existing asset by clicking the sync (↻) icon to the right of the asset name — opens the file picker. Disabled when no asset is currently set.
- **Delete** an asset by clicking the trash icon — opens the "Remove logo?" confirmation modal. Disabled when no asset is currently set.
- See the **upload progress bar** animate while the file uploads.
- See the **preview module** below the upload area (all slots except OG image) showing the asset rendered in its actual usage context.
- See the recommended size + accepted file formats in the card description.

## Settings & fields

### Per-card UI elements

| Element | Behaviour |
|---------|-----------|
| **Drop zone** (when empty) | Dashed border. Hover → solid border. Drag-over → highlighted background. Click → opens file picker. The hidden file input has `accept` set to the slot's `allowed_mimetypes` array (default `jpeg, jpg, jpe, gif, png, svg, webp` — `gif` is filtered out everywhere in practice). |
| **Thumbnail** (when populated) | Shows the current asset rendered inside the 160×100 frame. Click anywhere on the thumbnail also re-uploads. |
| **Progress bar** | Animates from 5% to 90% in 5%-increments every 100ms while uploading; jumps to 100% on success; clears after 600ms. |
| **Re-upload (↻)** | Tooltip: *"Upload image"*. Disabled state when no asset exists (cursor: not-allowed, greyed). |
| **Delete (trash)** | Disabled state when no asset exists. On click → confirm modal *"Remove logo?"* with **Remove** button. |
| **Preview module** | Shown below the upload area for all slots except `og_image_url`. Renders the asset in its actual usage context (e.g., the storefront-header card shows the logo as it appears in the public site header). |

### "Remove logo?" confirmation modal

Opened when the merchant clicks the trash-can icon next to any asset card. Implemented via the shared `CcDeleteComponent`. Fields:

| Element | Content |
|---------|---------|
| **Label** | *"Remove logo?"* |
| **Confirm button** | *"Remove"* (danger styling) |
| **Cancel** | Closes the modal — no change. |
| **Loader** | Spinner on the Remove button while the delete request is in-flight. |
| **Disabled state** | The trash icon is greyed out (cursor: not-allowed) when the slot has no asset. The merchant can't open the modal in that state. |

On confirm: the card reverts to empty drop-zone state. The deletion side-effects differ per slot — see [[settings-brand-cache-and-storage]] for the per-slot cleanup rules and [[settings-brand-og-image]] for the OG image's orphan-file behaviour.

## Business rules

### Single file per upload, never bulk

The hidden file input does NOT have the `multiple` attribute. Dropping or picking multiple files only consumes the first. Bulk-import of multiple slots in one operation is not supported — the merchant uploads each slot's asset in its own card.

### Client-side resize before upload

For all slots except `og_image_url`, the file passes through a shared resize helper (`resizeImageIfNeeded`) before being added to the form data. The helper:

- **Preserves aspect ratio** — only the max dimension is capped.
- Operates entirely in the browser — no server round-trip for resize.
- Keeps uploads small even when the source file is 4K or larger.

A merchant uploading a 4000×4000 source PNG will see the file shrink (in the browser) to a sensible upload size before the network transfer starts. The merchant's local file is NOT modified — only the in-memory copy that gets POSTed.

### Per-slot extension whitelist drives the file-picker `accept`

Each slot's `allowed_mimetypes` and `allowed_extensions` arrays come from the backend response and drive both the file-picker `accept` attribute and the merchant-facing "Accepted file formats" text. Default fallback if the backend doesn't specify: `jpeg, jpg, jpe, gif, png, svg, webp`. The `gif` extension is explicitly filtered out everywhere — no slot accepts GIF, even when config includes it. See [[settings-brand-errors]] for the rejection messages when an invalid file type is submitted.

### POST endpoint is `/admin/api/core/settings/logos/{slot}` for six slots

Six slots POST the resized file to a single endpoint with the slot ID in the URL — a one-call upload that returns a `150x150` image URL on success. The OG image is the exception — see [[settings-brand-og-image]].

The legacy upload path (still present on older admin templates) posts to a different endpoint — see [[settings-brand-cache-and-storage]] for the legacy-vs-modern endpoint split.

### Upload errors surface globally, not per-card

The cards do NOT show inline error messages. All upload failures surface on the top-of-page red banner — see [[settings-brand-errors]] for the response shape and per-error rendering rules.

### No queue / no notifications / no webhooks fired

Uploading or deleting via this flow is purely synchronous: file → resize → DB write → cache clear → UI update. No background jobs, no admin notifications, no `*.updated` webhooks fired from this page.

### Re-upload replaces in place

The re-upload (↻) icon does NOT delete first; it directly overwrites the existing asset row. The new file replaces the old one, the per-slot cache flushes (see [[settings-brand-cache-and-storage]]), and the storefront serves the new asset on the next page load.

## Related

- [[settings-brand]] — hub.
- [[settings-brand-slots]] — the seven slots that all share this upload flow (except OG image).
- [[settings-brand-og-image]] — the slot that uses a different two-step file → URL flow.
- [[settings-brand-favicon]] — additional cache-busting on top of this flow for the Favicon slot.
- [[settings-brand-errors]] — global error banner + 422 response shape; what the merchant sees on rejection.
- [[settings-brand-cache-and-storage]] — what happens after a successful upload (cache flush, `boarding_settings` flag, legacy-vs-modern endpoints).

## Open questions

None.
