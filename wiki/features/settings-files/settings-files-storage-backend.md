---
type: feature
nav_path: "Settings → Files → Storage backend"
route_name: files.settings
route_path: /admin/settings/files
aliases: ["File storage backend", "Hetzner Object Storage", "the image delivery service", "nginx-images", "CDN URL", "Public file URLs", "Replace image everywhere"]
tags: [settings, files, cdn, hetzner, the image delivery service, infrastructure]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-files]]. See the hub for the other aspects (tabs, upload flow, storage quota, delete protection, image playground, allowed types).

# Settings → Files — storage backend and public URLs

## Purpose

Where the bytes actually live, what URL the merchant gets, what serving path their customers hit, and the security / workflow consequences of those choices. This page is the "what's behind the screen" view of the Files page — useful when a merchant asks why CDN URLs look the way they do, why cached images take a few minutes to update, why files are public, or why there's no "replace image everywhere" button.

## Where to find it

This page documents infrastructure behaviour that's invisible in the admin UI. The merchant interacts with it through:

- The `url` accessor that appears on every Filemanager row (Files tab + User files tab).
- CDN-served fetches of every image, video, doc, etc., from `cdncloudcart.com`.
- The behaviour described below shows up when the merchant asks "why didn't my replaced image update everywhere?" or "is this file private?".

## What the merchant can do here

- Copy the per-file URL from the table and paste it into custom storefront templates, app webhook payloads, or external integrations.
- Use the cache-busted variant `url_time` (the URL with a `?{unix_timestamp}` query) when they need to force a re-fetch — e.g., after rotating a logo.

### What the merchant CANNOT do

- Set a file as "private" or "owner-only" — there is no per-file privacy flag in the admin UI.
- Generate a signed / time-limited URL for a file.
- Replace a file's bytes at the same URL — every upload creates a new row with a new URL.
- Use the raw Hetzner Object Storage URL — only the `cdncloudcart.com` path is supported.
- Trigger a CDN purge manually after a delete or replace — the merchant waits for cache TTL.

## Settings & fields

This page surfaces no merchant-configurable settings. The relevant facts are infrastructural:

| Item | Value |
|------|-------|
| Storage backend (code disk name) | `'s3'` |
| Storage backend (actual provider) | **Hetzner Object Storage** at `hcp.cloudcart.net` (production) |
| Bucket name | `cloudcart-images` |
| CDN host | `cdncloudcart.com` |
| Image transform layer | the image delivery service behind nginx-images |
| Doc / video / archive / text / font / audio | S3 passthrough — no transform |
| Per-file URL pattern | `cdncloudcart.com/{site_id}/files/{dir}/{name}` |
| Cache-busted URL pattern | `cdncloudcart.com/{site_id}/files/{dir}/{name}?{unix_timestamp}` |

## Business rules

### Storage backend — Hetzner Object Storage in production

The S3 disk used by Filemanager is named `'s3'` in code but points at **Hetzner Object Storage** (`hcp.cloudcart.net`) in production. CloudCart's CDN (`cdncloudcart.com`) sits in front of the image delivery service + nginx-images and proxies fetches to the underlying Hetzner bucket. The bucket name in code is `cloudcart-images`.

Merchants should not need to know this, but it explains:

- Why files load through `cdncloudcart.com/{site_id}/files/{dir}/{name}` URLs and not Amazon S3 URLs.
- Why CDN cache invalidation may take a few minutes after a file is replaced — Cloudflare and nginx-images caches sit in the path.

### Per-file URL is the canonical merchant-visible path

The `url` accessor on the Filemanager model emits `cdncloudcart.com/{site_id}/files/{dir}/{name}` — this is the URL merchants should use everywhere (storefront templates, external integrations, app webhook payloads). The cache-busted variant `url_time` appends `?{unix_timestamp}` so browsers and crawlers refetch when the file rotates.

Both forms route through nginx-images:

- **Image directories** → S3 + the image delivery service (resize / format / quality transform on the fly).
- **Doc / video / archive / text / font / audio directories** → S3 passthrough (no transform).

Merchants who paste direct Hetzner Object Storage URLs into their storefront WOULD bypass Cloudflare cache, the image delivery service resizing, and the platform's per-IP throttle protection. The CDN URL is the only supported way.

### All filemanager files are public (CDN URL is openable by anyone)

Every file uploaded via this page is stored on S3 and served publicly through CloudCart's CDN. There is no per-file privacy flag, no signed-URL option, and no way to mark a file as "owner-only access" from the admin UI. Anyone with the URL can fetch the file.

Order-attached customer uploads served through the platform's order-download endpoint are also public — they are at obscure URLs but not authenticated. Merchants who must store genuinely confidential files (e.g., signed contracts, ID scans, customer KYC documents) should **NOT** use this filemanager; they should host such files elsewhere with proper access control.

### No antivirus / malware scanning

The platform does NOT scan uploaded files for viruses or malware before storing or serving them. This applies to both admin uploads and customer uploads — see [[settings-files-allowed-types]] for the defensive layers that ARE in place (extension whitelist) and the residual risk areas (SVG, Office docs, archives).

### No one-click "replace image everywhere" workflow

To swap a product image (or any binding), the merchant uploads a new file, binds it to the product from the product editor, and removes the old file. There is no "replace this file" action that rewrites every reference — each reference must be re-pointed individually.

Hint for merchants: if a file is heavily referenced and they want to replace it without re-binding everywhere, the easier path is to:

1. Delete the OLD file — this will FAIL because of [[settings-files-delete-protection|in-use protection]], confirming all the consumers.
2. Upload a new one with a similar name.
3. Manually swap bindings on each consumer (product editor, blog editor, CMS page editor, etc.).
4. Now the old file's reference count drops to 0 and it can be deleted.

### CDN cache TTL

After a file is deleted or replaced, Cloudflare and nginx-images caches may keep serving the old version for a few minutes. The `url_time` cache-busted accessor (with `?{unix_timestamp}` query) bypasses cache — useful in app integrations that need to be certain they're getting the current file. The merchant cannot trigger a manual purge from the admin UI.

### CDN parameters — full reference

The Image playground exposes the common transforms; the image delivery service backend supports a larger set not all exposed in the UI. See [[settings-files-image-playground]] for the full reference list.

**Note on SVG**: SVG files bypass the image delivery service entirely and are served as-is from S3. Transform query parameters on an SVG URL are silently ignored.

### Storage statistics endpoint

The polymorphic `system_storage` table tracking every file-attached object across the platform is what powers the [[settings-files-storage-quota|quota module]]. The "Used" number is the platform code over this table — including filemanager files plus product images, logos, vendor images, page assets, fiscal-printer audit files, etc. So a single filemanager delete may not free as much quota as the merchant expected if their bottleneck is in another category — the statistics modal shows the full breakdown.

## Related

- [[settings-files]] — hub.
- [[settings-files-upload-flow]] — how bytes get to S3.
- [[settings-files-storage-quota]] — quota is counted across all `system_storage` rows, not just filemanager.
- [[settings-files-delete-protection]] — what happens when a delete is allowed.
- [[settings-files-image-playground]] — CDN-transform URL composer that uses these paths.
- [[settings-files-allowed-types]] — extension whitelist (the primary defensive layer in the absence of malware scanning).
- [[storefront-architecture]] — wider CDN architecture context.

## Open questions

None.
