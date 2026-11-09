---
type: feature
nav_path: "Design → Modules → Cross-cutting → Cache invalidation"
route_name: admin.storefront.widget_save
route_path: /admin/storefront/widgets
aliases: ["Module cache", "Module cache invalidation", "Per-site cache key", "Storefront cache bump", "Modules cache pickup", "widgetsNew cache key", "theme-settings cache"]
tags: [design, modules, cache, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 2
---

# Storefront Modules — Cache invalidation

> Part of [[design-modules]]. See the hub for the other cross-cutting aspects (instance model, storage, tabs / groups, save / reset, gating).

## Purpose

How module changes propagate from the admin Save / Reset action to the live storefront — and why a guest can still get the old page for up to 20 minutes after a save. This aspect documents the cache stack and the per-site cache-key bump.

Use this aspect when investigating: *"I clicked Save but the storefront still shows the old banner"*, *"how long does it take for module changes to appear?"*, *"is there a Clear cache button I'm missing?"*, *"the staging copy of the store hasn't picked up the module edit"*.

## Where to find it

The cache layer is **invisible** to the merchant — no admin screen manages it directly. Through the [[admin-graphql-api]], `purgeStorefrontCache` clears the store's cached pages so the next visit renders fresh; it needs the `store`, `store.templates` or `store.builder` staff permission. Without it, guests get cached pages for up to 20 minutes after any change (module, theme, custom code, page, menu) and crawlers for 1–2 days. Save and Reset renew the module data, not the cached pages — see [[design-modules-cross-save-reset]].

## What the merchant can do here

- **Save** or **Reset** a module — renews the module data at once. A browser signed in to the admin, and signed-in customers, see the change on the next page load; guests within 20 minutes, crawlers within 1–2 days ([[storefront-arch-caching-invalidation]]).

The merchant CANNOT:

- Manually clear the module cache — there is no "Clear cache" button.
- See the current cache-key value or the cache state from any admin surface.
- Configure cache TTLs.

## Settings & fields

There are no settings on this aspect — it documents the cache stack.

### The three caches involved

| Cache | Key shape | TTL | Flushed by |
|-------|-----------|-----|------------|
| Parsed theme config | `theme-settings.<template>` (file driver) | `forever` | Code-level cache wipe or platform deploy bust. Not flushed by a module save. (verify) |
| Merged module rows per active site | `widgetsNew:<md5 of mapping list>` | `ttl_1h` | Per-site cache-key bump on any module Save / Reset. |
| Per-site cache tag | (microtime + site_id stamp under the per-site tag) | n/a (stamp value) | Save / Reset write a new microtime stamp. Every subsequent cached read against the tag misses, forcing a rebuild. |

### How Save / Reset busts the cache

Both Save and Reset call into a single per-site cache-key regenerator:

1. Write the new settings (Save) or delete the saved row (Reset). See [[design-modules-cross-storage]].
2. Write a new microtime + site_id value into the per-site cache tag.
3. Return success — *"Module successfully edited"* or *"Module successfully reset"*.

On the next request that renders a page (not one served from the full-page cache):

1. The storefront looks up the current per-site cache stamp.
2. The previously cached `widgetsNew:<...>` entry was keyed off the OLD stamp — so the lookup misses.
3. The module loader rebuilds the merged set from theme JSON + sister-site overlay + merchant saves (see [[design-modules-cross-storage]]).
4. The new merged set is cached under the new stamp.
5. The storefront renders with the updated module settings.

### Theme-settings cache lives outside the bump

The `theme-settings.<template>` cache is keyed by template name, not by the per-site stamp — so a module Save does NOT flush it. Theme JSON only changes on deploys / theme version updates, so this cache being long-lived is intentional. The merge happens AFTER the theme JSON is read, so module Saves bypass it. (verify cache name + driver)

## Business rules

### Save and Reset both bump the cache key

There is no "save without bust" mode. Every successful Save and every successful Reset bumps the per-site cache key, so every page rendered after it uses the new settings. Pages already held in the full-page cache are not rendered again until their copy expires.

### No manual cache-clear surface for modules

There is no admin "Clear cache" button for modules or pages. If a merchant reports stale modules despite saving, check in order: did the Save succeed (the success message); does the page answer `X-Cache: HIT` with an `X-Cache-Expires` time still ahead (the full-page cache — the change shows after that time); did the theme JSON get out of sync (a different cache).

### Pickup latency

A page rendered after the save shows the new settings at once, and the admin and signed-in customers always get a freshly rendered page. A guest gets one when the cached copy expires (20 minutes at most; the page's `X-Cache-Expires` header gives the time), a crawler within 1–2 days.

### Theme deploys flush the theme-settings cache separately

When CloudCart deploys a new theme version (or the merchant switches themes), the `theme-settings.<template>` cache is wiped by the deploy / theme-switch path — not by module Save. This is why a deploy can change module defaults globally without the merchant doing anything, and why the per-instance overlay layer is still respected after the deploy (the merchant's saved row wins per-field over the new theme default — see [[design-modules-cross-storage]]).

### The full-page cache is separate

The per-site cache key renews the module cache only. The platform's full-page cache is keyed without it, so a save never empties it; only the Admin GraphQL `purgeStorefrontCache` (or CloudCart staff) does — see [[storefront-arch-caching-invalidation]].

## Related

- [[design-modules]] — hub.
- [[design-modules-cross-save-reset]] — the actions that trigger the cache-key bump.
- [[design-modules-cross-storage]] — the storage layer the cache fronts.
- [[design-modules-cross-instance-model]] — how the cache key incorporates the mapping list.
- [[design-themes]] — theme switches that flush the long-lived theme-settings cache.

## Open questions

- 📡 **Exact cache-key names.** The `theme-settings.<template>` and `widgetsNew:<md5>` key shapes are documented from prior verification — re-confirm against current code. (verify)
- ✅ Resolved: module saves do not clear the full-page cache; guests get the change within 20 minutes.
- 📡 **Multi-region pickup.** In a multi-region deployment, whether the cache-key bump is synchronously visible across regions is unclear. (verify)
