---
type: feature
nav_path: "Design → Modules → Utility → Storage and caching"
route_name: admin.storefront.widgets
route_path: /admin/storefront/widgets
aliases: ["Module storage", "Module cache", "Module save pipeline", "Module reset pipeline", "Per-site cache key"]
tags: [design, modules, storefront-customisation, storage, cache]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Utility modules — Storage and caching

> Part of [[design-modules-utility]]. See the hub for the catalogue, editable modules, system modules, and page-builder blocks.

## Purpose

How a module on the Modules screen resolves at request time, and what happens on Save or Reset. Use this aspect when investigating: *"why did my module setting not stick?"*, *"why did switching themes lose my footer text?"*, *"why does the module cache look stale?"*, or *"why can't I open the vendors module settings?"*.

This applies to ALL module categories (utility, products, navigation, blog, content) — the storage layer is shared.

## Where to find it

Sidebar → **Design** → **Modules** — the merchant's interaction surface. The underlying storage is invisible to the merchant; this page documents it for support investigation only.

## What the merchant can do here

- **Save** an editable module — stores the new values for the active site, then bumps the per-site cache key.
- **Reset** an editable module — deletes the merchant's saved values, falling back to theme defaults; bumps the per-site cache key.
- See changes on the next storefront request — no manual cache clear required.

The merchant CANNOT manage the underlying storage / cache directly — there is no admin "Clear module cache" button.

## Settings & fields

There are no settings on this aspect — it documents the layering and pipelines.

### Storage — three sources merged at read time

A module instance on the Modules screen is the merge of THREE layers:

1. **Theme defaults** — the active theme declares the instance name, the underlying module map (e.g. `extra.social`, `product.filters`, `extra.text`), the default settings, and the `editable` flag.
2. **Platform overlay** — a per-store override deployed by the platform team that can ADD or REPLACE instances for one store. This is how carve-outs sit on top of theme defaults without forking the theme.
3. **Merchant saves** — one stored row per instance. Reset deletes it; Save upserts it.

On open, the platform reads theme defaults, merges the overlay, then layers the merchant's saved values on top — **last write wins per field**. Settings for an instance the active theme no longer ships stay stored but are never read (orphaned).

### Caching — three caches stack together

- Parsed theme settings are cached indefinitely per theme — only cleared by a platform deploy.
- The merged module rows for the active site are cached for about an hour — cleared by the per-site cache-key bump on any Save / Reset.
- Save and Reset both bump that cache key, so every subsequent read rebuilds. Changes show on the very next storefront request — there is no merchant-facing "Clear cache" button.

### Edit-form gating — `editable` + paid modules

The edit panel is blocked in two cases:

- If the theme declares `editable: 'no'` for the instance, opening returns HTTP 404 and the card is hidden from the Modules screen.
- If the underlying map is a paid module AND the plan lacks the feature, opening and saving both fail with a payment-required error. Currently only `extra.videoSlider` (gated by `video_slider_widget`) is paid — no utility module here is plan-gated at the module level.

### Save pipeline — schema-derived validation

Save validates submitted values against the module's declared field rules. Fields not in the schema are **silently dropped** — a hand-crafted submission with extra keys can't widen the stored data. The row is then upserted, the cache key bumped, and the message *"Module successfully edited"* is returned.

### Reset pipeline — can re-seed shared Configuration group

Reset deletes the merchant's stored row. For modules that expose a shared Configuration group (rare — typically the `productsRelated` module shares one across instances), reset also re-creates that group with the defaults, restoring settings at the global level too. No utility module in this cluster uses it, but the pattern exists.

### System modules bypass the edit form entirely

The system module set (`vendors`, `providers`, `leasing`, `authorize`, `utilities`, `page`, `wishlist`, `wishlistMenu`, `categoryProperties`, `productsDetails`, etc. — see [[design-modules-utility-system]]) is injected as map-only stubs with no editable declaration and isn't in the editable-mapping allowlist. Opening their settings URL returns 404.

### Page-builder modules are a separate registry

The page-builder modules (`code`, `store_locations`, `yotpo-reviews`, `brand-model`, `order-details` — see [[design-modules-utility-page-builder]]) come from a separate registry. A module loads only if its required app is installed — `yotpo-reviews` needs the Yotpo app, `store_locations` the Store Locations app, `brand-model` the Brand-Model app. Missing the app means the module is absent from the picker entirely, not just disabled.

### Page-builder access gating

The Page Builder itself is gated by the `storefront_builder` plan feature. Lower plans are redirected to the upsell when they open the per-page builder. Once inside, all utility-category page-builder modules are available (none have their own paid gate).

### Translation merge — per-language string fields

For instances that ship per-language values in the theme (`name`, `description`, sometimes per-field defaults), the current locale's value is used if present, otherwise the platform translation fallback. For merchant-entered content the per-language behaviour comes from the `multylang` app — text modules store per-language bodies; without the app, only one body is stored.

## Business rules

### Settings are keyed by INSTANCE name, not theme

Saved settings are keyed by instance name. Switching themes orphans the settings for instances the new theme doesn't ship; switching BACK re-exposes them intact, because the platform never deletes orphaned rows on theme switch. This is intentional — an accidental switch shouldn't wipe years of configuration — but long-running stores accumulate dead settings for themes they tried years ago.

### Cache invalidation is automatic

Save and Reset both bump the per-site cache key, so new settings reach customers on the very next page load. No manual cache-clear is required and no admin button exists for it.

### Platform overlays are configuration, not data

The platform-overlay layer is deployed by the platform team, not a merchant-editable surface. Merchants on those carve-out stores cannot edit it directly, but they CAN still save their own values on top, which win per field.

### Hidden quirks affecting merchant behavior

- `social` module URL fields fall back to general-settings keys (`facebook_link`, `instagram_link`, etc.) when blank — the module renders social icons even on instances the merchant never opened, as long as the general-settings URLs are filled. See [[settings-general]] and [[design-modules-utility-editable]].
- `filters` module is keyed under a single instance — there is no per-listing-page override at the module level. Per-page customisation needs a Dynamic page in [[marketing-landing-pages]].
- `code` module HTML renders inside an isolated, auto-height frame — its scripts can't reach the parent page unless they use `postMessage`. See [[design-modules-utility-page-builder]].
- Validation silently drops unknown fields — merchants who paste in an "exported" module configuration from a different theme may lose fields the current theme's schema doesn't accept.

## Related

- [[design-modules-utility]] — hub.
- [[design-modules-utility-catalogue]] — full module list.
- [[design-modules-utility-editable]] — editable module cards + Save / Reset flow.
- [[design-modules-utility-system]] — why system modules 404.
- [[design-modules-utility-page-builder]] — separate page-builder registry.
- [[design-themes]] — theme JSON is the first layer of module storage.
- [[settings-general]] — social URL fallbacks for `social` module.
- [[marketing-landing-pages]] — per-page module overrides via Dynamic pages.

## Open questions

None — storage and caching mechanics are verified against backend.
