---
type: feature
nav_path: "Design → Modules → Cross-cutting → Cache invalidation"
route_name: admin.storefront.widget_save
route_path: /admin/storefront/widgets
aliases: ["Module cache", "Module cache invalidation", "Per-site cache key", "Storefront cache bump", "Modules cache pickup", "widgetsNew cache key", "theme-settings cache"]
tags: [design, modules, cache, storefront]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

# Storefront Modules — Cache invalidation

> Part of [[design-modules]]. See the hub for the other cross-cutting aspects (instance model, storage, tabs / groups, save / reset, gating).

## Purpose

How module changes propagate from the admin Save / Reset action to the live storefront — and why merchants typically see their changes on the very next storefront request without any manual cache clear. This aspect documents the cache stack and the per-site cache-key bump.

Use this aspect when investigating: *"I clicked Save but the storefront still shows the old banner"*, *"how long does it take for module changes to appear?"*, *"is there a Clear cache button I'm missing?"*, *"the staging copy of the store hasn't picked up the module edit"*.

## Where to find it

The cache layer is **invisible** to the merchant — no admin surface manages it directly. This page documents it for support-investigation purposes. Save and Reset on `/admin/storefront/widgets/{mapping}` are the only merchant-driven cache busts — see [[design-modules-cross-save-reset]].

## What the merchant can do here

- **Save** any editable module — automatically bumps the per-site cache key. Storefront picks up the change on the next request.
- **Reset** any editable module — same effect: per-site cache key bumps, storefront picks up the change on the next request.
- See changes immediately after refresh on the storefront.

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

On the next storefront request:

1. The storefront looks up the current per-site cache stamp.
2. The previously cached `widgetsNew:<...>` entry was keyed off the OLD stamp — so the lookup misses.
3. The module loader rebuilds the merged set from theme JSON + sister-site overlay + merchant saves (see [[design-modules-cross-storage]]).
4. The new merged set is cached under the new stamp.
5. The storefront renders with the updated module settings.

### Theme-settings cache lives outside the bump

The `theme-settings.<template>` cache is keyed by template name, not by the per-site stamp — so a module Save does NOT flush it. Theme JSON only changes on deploys / theme version updates, so this cache being long-lived is intentional. The merge happens AFTER the theme JSON is read, so module Saves bypass it. (verify cache name + driver)

## Business rules

### Save and Reset both bump the cache key

There is no "save without bust" mode. Every successful Save and every successful Reset bumps the per-site cache key. So the merchant always sees changes on the next storefront request.

### No manual cache-clear surface for modules

There is no admin "Clear module cache" button — the bump is automatic and reliable enough that one isn't needed. If a merchant reports stale modules despite saving, the investigation path is upstream: did the Save actually succeed (check the success message), did the storefront request hit a CDN / browser cache (different layer entirely), did the theme JSON get out of sync (different cache). (verify CDN behaviour)

### Pickup latency is one storefront request

The pickup is effectively immediate — the next storefront request after a successful Save rebuilds the cache and renders with the new settings. There is no propagation delay across services or queues. (verify, especially for multi-region deployments)

### Theme deploys flush the theme-settings cache separately

When CloudCart deploys a new theme version (or the merchant switches themes), the `theme-settings.<template>` cache is wiped by the deploy / theme-switch path — not by module Save. This is why a deploy can change module defaults globally without the merchant doing anything, and why the per-instance overlay layer is still respected after the deploy (the merchant's saved row wins per-field over the new theme default — see [[design-modules-cross-storage]]).

### CDN / edge caches are out of scope

The per-site cache key only flushes the application-level module cache. CDN-level page caches (if any) are flushed by a separate edge-purge path — not documented here. (verify)

## Related

- [[design-modules]] — hub.
- [[design-modules-cross-save-reset]] — the actions that trigger the cache-key bump.
- [[design-modules-cross-storage]] — the storage layer the cache fronts.
- [[design-modules-cross-instance-model]] — how the cache key incorporates the mapping list.
- [[design-themes]] — theme switches that flush the long-lived theme-settings cache.

## Open questions

- 📡 **Exact cache-key names.** The `theme-settings.<template>` and `widgetsNew:<md5>` key shapes are documented from prior verification — re-confirm against current code. (verify)
- ⏸️ **CDN propagation.** Whether CloudCart's CDN layer (if configured) requires a separate purge for module changes is unclear. (verify)
- 📡 **Multi-region pickup.** In a multi-region deployment, whether the cache-key bump is synchronously visible across regions is unclear. (verify)
