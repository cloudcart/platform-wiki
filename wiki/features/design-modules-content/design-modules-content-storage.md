---
type: feature
nav_path: "Design → Modules → Content → Storage and caching"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Content module storage", "Content module cache", "Content module save pipeline", "Content module reset", "front_widget content rows", "Theme JSON content layer", "Sister-site overlay content"]
tags: [design, modules, content, storage, cache, plan-gates]
plan_gates: ["video_slider_widget", "storefront_builder", "static_pages"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Content modules — Storage, caching, and plan gates

> Part of [[design-modules-content]]. See the hub for catalogue, carousel, banners, text, video, and page-builder aspects.

## Purpose

How a content module the merchant sees on the Modules screen actually resolves at request time, what happens on Save / Reset, and how the platform enforces the plan gates that bound this cluster.

Use this aspect for: *"why did my module setting not stick?"*, *"why did switching themes lose my homepage carousel?"*, *"why does the storefront still show the old banner?"*, *"why can I see the Video Slider card but can't open it?"*, *"why did the page builder redirect me to an upsell?"*

The storage mechanics here are **shared across every module category**; the cross-cluster generic version lives in [[design-modules-utility-storage]].

## Where to find it

Sidebar → **Design** → **Modules** — the merchant's interaction surface. The underlying storage is invisible to the merchant; this page documents it for support investigation.

## What the merchant can do here

- **Save** — upserts the per-site row + bumps the cache key.
- **Reset** — deletes the merchant's row (theme defaults take over) + bumps the cache key.
- See changes on the next storefront request — no manual cache clear required.

The merchant CANNOT manage storage / cache directly — there is no admin "Clear module cache" button.

## Settings & fields

No settings on this aspect — it documents the layering and pipelines.

### Storage — three sources merged at read time

A content module instance is the merge of THREE layers:

1. **Theme JSON** (`themes/<template>/config/theme.json`) — declares each instance, its underlying module `map` (e.g., `extra.carousel`, `extra.text`, `extra.banner`), default `settings`, and the `editable` flag.
2. **Sister-site overlay** (`config('site_widgets.site_<site_id>')`) — per-store override applied on top of the theme JSON. Adds or replaces instances without forking the theme.
3. **Merchant saves** (`front_widget` table) — one row per instance keyed by `mapping`, with settings as JSON. Reset deletes; Save upserts.

Effective settings are the layered merge — **last write wins per field**.

### Caching — two caches stack

- Parsed `theme.json` is cached `forever` as `theme-settings.<template>` — flushed only by a code-level cache wipe or a platform deploy.
- Merchant-saved module rows are cached `ttl_1h` under `widgetsNew:<md5 of mapping list>` — flushed by the per-site cache-key bump.
- Save and Reset both regenerate the per-site cache key (writes a new microtime+site_id into the per-site cache tag). Subsequent reads miss and rebuild — merchant changes are visible on the very next storefront request.

### Edit-form gating — `editable` flag + `paid_widgets`

Two conditions block the edit panel:

- `editable: 'no'` in the theme JSON → HTTP 404 on the settings URL AND the card is hidden from the Modules screen.
- Underlying `map` is in the controller's `paid_widgets` allowlist AND the plan lacks the feature → `PlanFeaturePaymentRequired` on BOTH open and save. For content modules, only `extra.videoSlider` (gated by `video_slider_widget`) is on that list. The paid check runs BEFORE settings load — a lower-plan merchant cannot even pre-fill the form.

### Save pipeline — schema-derived validation

Save validates the POST against the module's declared restriction rules — dot-flattened where the schema has nested arrays (slides, banners). Unknown fields are **silently dropped**. The validated array is upserted into `front_widget`, the per-site cache key is bumped, and *"Module successfully edited"* is returned.

### Reset pipeline

Reset deletes the merchant's `front_widget` row for that mapping. For modules exposing a shared `Configuration` group (rare — typically `productsRelated`; no content modules do), reset also re-seeds that group with defaults. For content modules reset is strictly per-instance.

### Page-builder block rendering

Content modules used in Dynamic pages (`title`, `separator`, `video`, plus `carousel`, `banner`, `text`, `text-carousel`, `code`, `video-slider` via the builder) go through a separate rendering pass. Pages are stored as a tree of rows → columns → modules with per-module `settings` JSON; rendered HTML is cached on the page row. See [[design-modules-content-page-builder]].

### Plan gates that bound this cluster

| Mapping | Shape | What it controls |
|---|---|---|
| `video_slider_widget` | Boolean | Gates `extra.videoSlider` via `paid_widgets` pre-flight on BOTH open and save — `PlanFeaturePaymentRequired` surfaces the upgrade prompt. Storefront hides the module when plan is inactive. See [[design-modules-content-video]]. |
| `storefront_builder` | Callback gate | Gates the Page Builder URL at `marketing/pages/builder/%` (where `title`, `separator`, `video` are reached). The path-check delegates to a callback. Lower plans see the upsell on the builder URL. See [[design-modules-content-page-builder]]. |
| `static_pages` | Numeric quota | Caps how many static / landing / FAQ pages the merchant can create. Past the cap surfaces the HTTP 402 paywall modal. Extends via packs ([[plan-vs-feature-pack]]). |

Lower plans get redirected to the per-feature upsell at [[plan-features]]. All other content modules (carousel, banners, text blocks, text carousel) are universally available.

### Translation merge — per-language string fields

Instance-level metadata (`name`, `description`) picks the current locale's value from the theme JSON if it ships per-language values, else falls back to `module.<setting>.<map>`. Merchant content (`text` body, slide captions, HTML overlays) becomes per-language when the `multylang` app is active — the saved JSON gains per-language sub-keys. Without multylang, only one body is stored.

## Business rules

### Settings keyed by INSTANCE name — not theme

Switching themes orphans the saved JSON for instances the new theme doesn't ship. Switching BACK re-exposes them intact. The platform never garbage-collects orphaned `front_widget` rows — accidental theme-switch shouldn't wipe years of configuration.

### `videoSlider` data is preserved across plan downgrade

A merchant who configures a `videoSlider`, then downgrades off `video_slider_widget`, keeps the saved JSON. Admin cannot reopen, storefront stays hidden, but re-upgrading restores both. See [[design-modules-content-video]].

### Cache invalidation is automatic

Save and Reset both bump the per-site cache key. New settings are visible on the very next page load — no manual cache-clear button.

### Schema-derived validation silently drops unknown fields

Merchants pasting an "exported" module JSON from a different theme may lose fields the current theme's schema doesn't accept. The validator runs from the module's declared restrictions; anything outside the schema disappears at save time without warning.

### Hidden quirks affecting merchant behavior

- Banner `script` type — no server-side sanitisation; a broken snippet can break the storefront page. See [[design-modules-content-banners]].
- `code` page-builder module renders inside `<iframe srcdoc>` with auto-height — embedded scripts cannot reach the parent DOM without `postMessage`. Analytics belongs in [[design-custom-assets]].
- Same module TYPE under different INSTANCE names is fully independent — `homeText1`/`homeText2`/`homeText3` are three rows; copy does NOT propagate. See [[design-modules-content-text]].

## Related

- [[design-modules-content]] — hub.
- [[design-modules-content-catalogue]] — full module list.
- [[design-modules-content-carousel]] — `carousel` field reference.
- [[design-modules-content-banners]] — banner modules + `script` sanitisation note.
- [[design-modules-content-text]] — text modules + multylang per-language behaviour.
- [[design-modules-content-video]] — `videoSlider` plan-gate and data preservation.
- [[design-modules-content-page-builder]] — page-builder access gate (`storefront_builder`) and page count quota (`static_pages`).
- [[design-modules-utility-storage]] — the cross-cluster generic storage description (same mechanics, different cluster).
- [[design-themes]] — theme JSON is the first layer of module storage.
- [[marketing-landing-pages]] — per-page module overrides via Dynamic pages.
- [[design-custom-assets]] — alternative to per-page `code` module for store-wide HTML / JS / CSS.
- [[plan-gates]] — the three plan features that bound this cluster.

## Open questions

- Per-language carousel / banner content. With `multylang`, each slide / caption supports per-language entry via the language switcher in the editor. GraphQL-resolvable: query whether the `multylang` app is installed on this merchant's store. (verify)
