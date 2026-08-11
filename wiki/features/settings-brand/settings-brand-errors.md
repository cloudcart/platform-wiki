---
type: feature
nav_path: "Settings → Brand settings → Errors & validation"
route_name: brand.settings
route_path: /admin/settings/brand
aliases: ["Brand upload errors", "Brand settings 422", "Brand global error banner", "SVG sanitisation", "Allowed extensions brand"]
tags: [settings, brand, errors, validation, security]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-brand]]. See the hub for related aspects (slots, upload flow, OG image, favicon, cache & storage, limitations).

# Brand settings — Errors & validation

## Purpose

How the Brand settings page surfaces upload errors and enforces per-slot validation rules. All errors render in a single top-of-page red banner — there is no per-card inline error display. This aspect also documents the SVG security note (uploaded SVG files are NOT sanitised) and the per-slot extension whitelist that drives the file-picker `accept` attribute.

## Where to find it

The error banner is rendered above the asset grid on the Brand settings page (`/admin/settings/brand`). It appears whenever any of the seven asset cards has a failed upload. The banner persists until the next successful upload OR until the merchant manually triggers another upload that resets the error state.

## What the merchant can do here

The merchant cannot dismiss or interact with the error banner directly. It clears automatically when:

- The next upload on any card succeeds.
- The next upload attempt resets the error state (even if that attempt also fails — a new error message replaces the old).

The merchant CAN inspect the error message text to diagnose the failure — typical errors include:

- File extension not in the slot's `allowed_extensions`.
- File MIME type not in the slot's `allowed_mimetypes`.
- File too large (storage adapter limit or platform upload size limit).
- For Favicon: dimensions disallowed (see [[settings-brand-favicon]]).
- For OG image step 1 / step 2 failures (see [[settings-brand-og-image]]).

## Settings & fields

### Global error banner (top-of-page)

NOT a modal — a red horizontal banner that appears above the asset grid whenever any upload fails. Driven by the page's `errorStore.responseErrors`. Shows:

- A red error icon.
- The platform error message (`errors.image[0]` from the response body) OR the fallback *"This file type is not allowed."* when the backend returns no message.

The banner persists across cards — the merchant uploading to the `main` card then to the `invoice` card will see banner updates that reflect the most recent error. Per-card inline error display does NOT exist; all errors surface here.

### 422 response shape

When the platform rejects a brand-asset upload, the response is HTTP 422 with body:

```json
{
  "message": "...",
  "errors": {
    "image": ["The specific error message"]
  }
}
```

The Vue page's `errorStore` reads `errors.image` (singular key) and promotes it to the top-of-page banner. Multiple back-to-back errors all surface on the banner one at a time — only the most recent renders.

### Per-slot extension whitelist

Each slot exposes two arrays in its backend response:

| Field | Drives | Default fallback |
|-------|--------|------------------|
| `allowed_extensions` | The merchant-facing "Accepted file formats" copy in the card description, AND the validation rejection logic. | `jpeg, jpg, jpe, gif, png, svg, webp` |
| `allowed_mimetypes` | The hidden `<input>`'s `accept` attribute (drives which files the OS file-picker shows). | `image/jpeg, image/jpg, image/png, image/svg+xml, image/webp` (gif filtered) |

The `gif` extension is explicitly filtered out everywhere — no slot accepts GIF, even when config includes it. In principle a CloudCart deployment could restrict (say) the Mail logo to PNG-only without code changes — but for standard merchants the seven slots all accept the same default set.

### Per-slot validation rules

| Slot | Validation rules beyond extension / MIME |
|------|-----------------------------------------|
| `main` | Standard image size limits. |
| `favicon` | Square aspect within tolerance + max 240 × 240 px enforced by the dedicated storage model — see [[settings-brand-favicon]]. |
| `invoice` | Modern path accepts SVG (legacy path does not — see [[settings-brand-cache-and-storage]]). |
| `mail` | Standard image size limits. |
| `default_image` | Standard image size limits. |
| `checkout` | Standard image size limits. |
| `og_image_url` | Step 1 enforces standard upload limits; step 2 validates non-empty URL — see [[settings-brand-og-image]]. |

## Business rules

### SVG uploads are NOT sanitised — treat as security-sensitive

The platform does NOT run uploaded SVG files through any sanitiser (no `svg-sanitize`, `enshrined`, or equivalent package is wired in). Files are stored and served as-is. For storefront and admin contexts where the file is rendered through an `<img>` tag, embedded `<script>` inside the SVG is neutralised by browsers' image-context rules — `<img src="evil.svg">` does NOT execute scripts. But any context that inlines the SVG (e.g., a custom storefront template that injects the SVG source into the DOM, or a third-party PDF renderer that processes the file unsafely) would execute embedded scripts.

Practical guidance for merchants:

- Only upload SVG from trusted sources.
- Avoid using SVG for the `mail` (email) and `invoice` (PDF) slots if the merchant uses a third-party SMTP relay or PDF tool — those may process SVG content directly.
- For storefront-only logos (header / checkout) SVG is fine because the platform renders them inside `<img>` tags.

### Error message text comes straight from the backend

The error message displayed in the banner is the verbatim string from `errors.image[0]` in the 422 response. The page does NOT translate or rephrase it. So merchants may see technical-sounding messages (e.g., "The file failed to upload" or storage-adapter-specific phrasing). The fallback *"This file type is not allowed."* only displays when the backend returns no message at all.

### `gif` is filtered everywhere — even when config includes it

The platform's defensive filter strips `gif` and `image/gif` from the allowed lists before they're used. This is a platform-wide policy decision (animated GIFs are not appropriate for brand assets in any of the seven slots). A deployment that configures `allowed_extensions` to include `gif` will still find that GIFs are rejected at upload time.

### Banner is the only error surface — no toast, no inline

The page does NOT use the standard toast notification system for upload errors. The banner is the only surface. This is a deliberate design choice — the banner stays visible long enough for the merchant to read the message and adjust the file, whereas toasts auto-dismiss after a few seconds.

(Exception: the OG image's Step 1 failure DOES surface as a toast in addition to the banner, because Step 1 uses the generic file-upload endpoint which has its own toast handling. See [[settings-brand-og-image]].)

### Validation runs server-side — client-side is best-effort

The `accept` attribute on the file picker is a hint, not a guarantee. A merchant can drag-and-drop a `.txt` file onto a card whose `accept` is image-only, and the browser will accept the drop. The server-side 422 then catches it. Client-side filtering only blocks the file-picker dialog from showing non-matching files; it doesn't validate the file actually uploaded.

## Related

- [[settings-brand]] — hub.
- [[settings-brand-upload-flow]] — where the file-picker `accept` attribute and the per-card UI are wired up.
- [[settings-brand-og-image]] — Step 1 / Step 2 failure handling for the OG image.
- [[settings-brand-favicon]] — additional dimension validation specific to the Favicon model.
- [[settings-brand-slots]] — per-slot recommended sizes that inform the merchant's choice; oversized files trigger banner errors.
- [[settings-brand-cache-and-storage]] — the legacy-vs-modern endpoint split (legacy rejects SVG on `invoice`; modern does not).

## Open questions

None.
