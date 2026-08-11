---
type: feature
nav_path: "Settings → Files → Image playground"
route_name: files.playground
route_path: /admin/settings/files/playground
aliases: ["Image playground", "CDN transform preview", "the image delivery service parameters", "Crop gravity preview", "Pad colour preview"]
tags: [settings, files, image, cdn, the image delivery service, transform]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-files]]. See the hub for the other aspects (tabs, upload flow, storage quota, delete protection, allowed types, storage backend).

# Settings → Files — Image playground

## Purpose

An interactive previewer for CloudCart's CDN image transforms. The merchant pastes any filemanager image URL (or picks from a sample), tweaks width / height / crop / pad colour controls, and watches the transformed image render live in the right pane. The page generates the corresponding CDN URL (`?width=W&height=H&crop=X&pad_color=HEX`) so the merchant can copy-paste it into custom storefront templates, app webhooks, or external integrations without trial-and-error.

The same component is also embedded INSIDE the file-preview modal for image files on the Files tab — clicking an image row opens a preview with the full playground controls attached.

## Where to find it

- **Standalone**: Sidebar → Settings → **Files** → **Image playground** tab. Route `/admin/settings/files/playground`.
- **Embedded**: Files tab → click any image row → file-preview modal opens with the playground component mounted in `embedded=true` mode.

## What the merchant can do here

- Paste a filemanager image URL into the source field (standalone mode only).
- Pick a sample thumbnail from the auto-populated picker (up to 8 image files from the merchant's file manager, fetched via `apiSettingsFiles.index` filtered by `dir=image, perpage=8`). Pre-selects the first sample if no source URL given.
- Adjust transform controls and see the result in real time:
  - **Width** (0–4000 px)
  - **Height** (0–4000 px)
  - **Crop / gravity** mode
  - **Padding color** (hex picker)
- Click **Reset** to clear width / height / crop / pad-color (does NOT clear source URL).
- Click **Copy URL** to copy the generated CDN URL to the clipboard. Toast confirms *"URL copied to clipboard"* on success, *"Copy failed"* on clipboard permission denial.
- Read the full generated URL in the code block below the preview / controls grid — useful for understanding the URL parameter pattern.

### What the merchant CANNOT do here

- Transform an image that isn't in their file manager — only files served through CloudCart's CDN can be transformed. A privately-imported URL (one not yet uploaded to filemanager) will NOT work.
- Pick a Format or Quality parameter — those CDN parameters exist (`ex`, `q`) but are NOT exposed in this tab's control panel as of the May 2026 audit. Merchants who need format/quality experimentation must craft the URL by hand or use the developer docs.
- Save a transform preset — the playground is exploratory only.
- Upload from this tab (the Upload button is hidden on Image playground; see [[settings-files-upload-flow]]).

## Settings & fields

### Standalone vs embedded mode

| Mode | `embedded` prop | Source URL input | Sample thumbnails | Controls panel |
|------|-----------------|------------------|-------------------|----------------|
| **Standalone** (`/admin/settings/files/playground`) | `false` | Visible | Visible (up to 8 samples) | Visible |
| **Embedded** (inside the file-preview modal — see [[settings-files-tabs]]) | `true` | Hidden — source URL fixed via prop | Hidden | Visible |

### Controls panel (right side, 320 px wide on `lg+` screens)

| Field | Range / options | URL param emitted |
|-------|-----------------|-------------------|
| **Width** | 0–4000 (number), unit `px`, no inc/dec arrows | `width=N` |
| **Height** | 0–4000 (number), unit `px`, no inc/dec arrows | `height=N` |
| **Crop / gravity** | Dropdown: *fit (no crop)*, `center`, `top`, `bottom`, `left`, `right`, `top_left`, `top_right`, `bottom_left`, `bottom_right` | `crop=X` |
| **Padding color** | `CcColorPicker` (hex), help text *"Applies only when both width and height are set."* | `pad_color=HEX` (no `#`) |

Action buttons below the controls:

- **Reset** — clears width / height / crop / pad_color (does NOT clear source URL).
- **Copy URL** — primary button with clipboard icon → `navigator.clipboard.writeText(transformedUrl)` → toast *"URL copied to clipboard"* or *"Copy failed"*.

## Business rules

### Client-side URL composer — does NOT call backend for transforms

The Image playground composes the CDN URL with query parameters (`?width=W&height=H&crop=X&pad_color=HEX`) and lets the browser fetch the transformed image directly from CloudCart's CDN. The backend is **not** involved in the transform itself — the image delivery service + nginx-images handle it. Practical implications: playground previews count against CloudCart's CDN bandwidth (the merchant's CDN quota is technically consumed during exploration), the transform is reproducible by anyone with the URL, and privately-imported URLs (anything not in the merchant's filemanager) won't transform.

### Preview pane — checker pattern + loading spinner

The preview pane uses a **checker-pattern background** (CSS linear-gradients) so transparent areas in PNG / WebP are visually distinguishable from white pad colour. While the transformed image is loading a `CcSpinner` (size `large`) overlay covers the preview at 60% white opacity. Load failures show `toast.error("Preview failed — check the URL and params.")` instead of breaking silently.

### Padding-colour requires both width AND height

The help text *"Applies only when both width and height are set."* documents the image delivery service behaviour: pad colour applies only when both target dimensions are specified. Setting just one dimension + a pad colour has no effect.

### Embedded inside file-preview modal — full controls, fixed source

When the merchant clicks an image row on the Files tab, the preview modal mounts this same component with `embedded=true` and the source URL hard-coded. The merchant gets the full controls without leaving the table — useful for sanity-checking a particular image at typical storefront dimensions.

### Format negotiation + SVG bypass

Even though Format isn't a control here, the CDN auto-negotiates based on the browser's `Accept` header — modern browsers receive WebP / AVIF for JPEG sources without any URL hint, so the playground preview matches what the storefront customer sees. SVG files bypass the image delivery service entirely and are served as-is from S3, so width / height / crop / pad parameters on an SVG URL are silently ignored.

### CDN parameters — the full transform set (reference)

The Image playground exposes the common ones; the image delivery service backend supports more. Documented params: `width`, `height`, `ex` (format / extension), `crop` values (`ce`, `no`, `so`, `we`, `ea`, `face`, `sm`), `q` (quality 1–100), `pad_color=HEX`, pad-to-square (when the store has opted into square product images). Less common transforms (rotate, blur, watermark, sharpen, etc.) may or may not be wired through CloudCart's URL helpers — merchants writing custom storefront templates can experiment with the underlying the image delivery service URL spec but should not rely on undocumented parameters in production.

## Related

- [[settings-files]] — hub.
- [[settings-files-tabs]] — the file-preview modal where this component is also embedded.
- [[settings-files-storage-backend]] — the CDN architecture (Hetzner Object Storage + the image delivery service + nginx-images) the playground previews.
- [[settings-brand]] — uses the same CDN URL pattern for the OG-image two-step upload.

## Open questions

- The Format (`ex`) and Quality (`q`) controls are documented as supported by the image delivery service but NOT in this tab's control panel. (verify) whether they will be added in a future revision or remain raw-URL only.
