---
type: feature
nav_path: "Design → Theme Editor → CSS compile pipeline"
route_name: admin.css.builder
route_path: /admin/builder
aliases: ["Theme CSS compile", "Stylesheet recompile", "theme.css recompile", "S3 stylesheet upload", "stylesheet_version cache buster", "CDN stylesheet"]
tags: [design, theme, css, s3, cdn, cache-invalidation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[design-theme-editor]]. See the hub for the other aspects (variables & types, colours, typography, images, save & reset, live preview & deep-links).

# Theme Editor — CSS compile pipeline

## Purpose

Every Save and Reset in the [[design-theme-editor]] triggers a server-side recompile of the merchant's storefront stylesheet. The Theme Editor doesn't generate CSS rules from scratch — it **fills in** placeholder tokens in the theme's pre-built `theme.css` file with the merchant's chosen values, uploads the result to S3, and stamps a fresh cache-buster on the storefront's `<link rel="stylesheet">` URL. This aspect documents that pipeline end-to-end and the storage / serving layers that make it work.

## Where to find it

The pipeline is server-side — there is no admin UI to inspect it directly. The merchant sees only the success message after Save / Reset and the recompiled CSS applied to the storefront. The pipeline is observable via:

- The storefront's `<link rel="stylesheet">` tag in page source — the `href` is `/cdn/css/theme.css?<stylesheet_version>` for S3-backed tenants.
- The merchant's `stylesheet_version` setting — a UNIX timestamp stamped on every Save / Reset.
- The merchant's `stylesheet_storage_backend` setting — `s3` for tenants migrated to the S3 backend.

## What the merchant can do here

This aspect is operational background, not a merchant-controllable surface. The merchant sees:

- The recompile happens automatically on every Save / Reset.
- Browser / Cloudflare caches invalidate the moment Save / Reset succeed (the cache-buster takes care of it).
- The recompile completes synchronously — the success toast and iframe-reload (see [[design-theme-editor-preview-deeplinks]]) only fire after the recompile finishes.
- There is no manual "recompile" button — recompile only fires from Save and Reset.
- There is no FTP / SFTP fallback for stylesheet writes — S3 is the only write target for new saves.

## Settings & fields

### Settings that drive the pipeline

| Setting | What it carries | Stamped on |
|---------|------------------|--------------|
| `stylesheet_version` | UNIX timestamp of the last Save / Reset. Appended to the storefront's `<link>` URL as `?<timestamp>`. | Every Save and every Reset. |
| `stylesheet_storage_backend` | Storage backend slug — `s3` for migrated tenants, otherwise legacy. Drives the URL format. | Stamped on Save when writing to S3 (so the marker and the bytes converge regardless of which side runs first). |
| `google_fonts_url` | The single Google Fonts URL spanning every font-family chosen across all `font-family` variables. The storefront injects this URL's `<link>` into every page's `<head>`. | Rebuilt on every Save; cleared on Reset to the theme's default font set. |

### Theme file inputs

| Input | What it carries |
|-------|------------------|
| `assets/styles/theme.css` (in the theme bundle) | Pre-built CSS file authored by the theme author, with `_<variable-name>_` tokens as placeholders (e.g., `background: _color-main-background_;`). |
| `theme.json` `settings.variables` block | The variable schema + defaults. Merged with the merchant's saved customisations on every editor load and on every recompile. See [[design-theme-editor-variables]]. |

### S3 output

| Output | What it is |
|--------|--------------|
| S3 key: `<site_id>/css/theme.css` | The recompiled CSS for the merchant. One file per merchant per Save / Reset. |
| Storefront URL: `/cdn/css/theme.css?<stylesheet_version>` | The URL the storefront `<link>` points to for S3-backed tenants. Served by nginx-images reading from the S3 bucket. |
| Legacy URL: `cdncloudcart.com/<site_id>/stylesheets/theme.css?<stylesheet_version>` | The URL for tenants still on the legacy backend (pre-S3-migration). |

## Business rules

### Save / Reset both recompile the full stylesheet

There is no incremental compile — every Save and every Reset reads the theme's `theme.css`, replaces every `_<variable>_` token with the merchant's saved value (or the theme default if the merchant has not customised that variable), and uploads the resulting CSS to S3 as the merchant's `<site_id>/css/theme.css`. The whole file is rewritten regardless of which variables actually changed.

### Token replacement is a string-replace, not a CSS parse

The compile reads the theme's pre-built `theme.css` (with `_<variable-name>_` tokens) and runs string-replace for every variable's token → value. There is no CSS parsing — token replacement is purely textual. This is why the theme author authors the placeholders consistently (e.g., `background: _color-main-background_;`) and why merchants cannot rewrite CSS rules from the Theme Editor (the structure is fixed; only the values change).

### `stylesheet_version` is a UNIX timestamp cache-buster

Save and Reset stamp the current UNIX timestamp on the merchant's `stylesheet_version` setting. The storefront appends this to every `<link rel="stylesheet">` URL as `?<timestamp>` — guaranteeing that browser caches and Cloudflare's edge cache both invalidate the moment the merchant saves. There is no manual "purge cache" step.

### `stylesheet_storage_backend` drives the URL format

The storefront's stylesheet URL is built by a helper that checks the per-tenant `stylesheet_storage_backend` setting:

- `stylesheet_storage_backend = s3` (every tenant who has saved at least once after the S3 migration) → `/cdn/css/theme.css?<stylesheet_version>` served by the merchant's own host (nginx-images reads from the S3 bucket).
- Legacy backend (pre-migration tenants who haven't saved since) → `cdncloudcart.com/<site_id>/stylesheets/theme.css?<stylesheet_version>`.

Saves stamp both the version (a UNIX timestamp) and the backend (`s3`) on every write, so the marker and the bytes converge regardless of which side runs first.

### Recompile fires the variable cache-invalidation event

Save / Reset trigger a remote cache-invalidation event on the variable read model (the back-end's cached variable read is flushed). Combined with the `stylesheet_version` timestamp bump, this means the merchant's admin view, the storefront's CSS, and any backed caching layer all converge to the new state on the next read.

### Reset wraps in a DB transaction with rollback on error

The reset endpoint catches any exception during the delete / recompile flow and rolls back the transaction, then returns a JSON `{status: 'error', msg: <exception message>}` to the front-end so the toast notifier can show the failure. The merchant's customisations are NOT lost mid-failure. See [[design-theme-editor-save-reset]] for the full Reset flow.

### No FTP fallback for stylesheet writes

S3 is the only write target for new saves. Legacy tenants who haven't saved since the migration still serve from the legacy URL, but the moment they Save once, they migrate to the S3 path permanently (the `stylesheet_storage_backend` setting is stamped to `s3`).

### Recompile is synchronous

The Save / Reset HTTP response is returned only AFTER the recompile + S3 upload + setting writes have completed. The merchant's success toast and iframe reload (see [[design-theme-editor-preview-deeplinks]]) fire only on the response — there is no background queue.

### Storefront serves the recompiled CSS via the merchant's own host

For S3-backed tenants, the storefront does NOT serve the CSS directly from the S3 public URL. Instead, the merchant's own host (e.g., `mystore.com/cdn/css/theme.css`) is the visible URL, served by nginx-images reading from the S3 bucket. This keeps the CSS under the merchant's domain (better caching, no cross-origin nuance) and centralises the cache-busting via `stylesheet_version`.

## Related

- [[design-theme-editor]] — hub.
- [[design-theme-editor-save-reset]] — the Save / Reset surface that triggers this pipeline.
- [[design-theme-editor-variables]] — variable rows that the recompile reads.
- [[design-theme-editor-typography]] — the `google_fonts_url` setting that the storefront's `<head>` reads alongside the recompiled CSS.
- [[design-theme-editor-preview-deeplinks]] — the live-preview iframe that auto-reloads after recompile finishes.
- [[design-custom-assets]] — raw CSS / JS overrides served independently of this recompile pipeline.

## Open questions

- Whether the migration to S3 is now 100 % complete or whether any legacy tenants remain (verify).
- The exact CDN cache behaviour for S3-backed tenants — whether nginx-images caches the CSS in front of S3 or proxies every request (verify).
