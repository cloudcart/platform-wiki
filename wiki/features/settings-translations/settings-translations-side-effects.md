---
type: feature
nav_path: "Settings → Translations → Side effects & cache"
route_name: translations.settings
route_path: /admin/settings/translations
aliases: ["Translation cache", "Translation Artisan commands", "db:translation append", "db:translation replace", "js:data-generate", "Translation cache TTL", "Translation cache flush"]
tags: [settings, translations, i18n, cache, performance]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-translations]]. See the hub for related aspects (toggle, table, filters, reset, scoping, permissions).

# Translations — side effects & cache

## Purpose

Every save / reset / master-toggle on the [[settings-translations]] page triggers a chain of side-effects that run **synchronously** inside the request: a translation cache flush by tag, plus one or two server-side rebuild tasks (a translation-table rebuild and a storefront data-asset regeneration). None run via the background queue. This is why translation saves feel slower than a typical "save and continue" UX and why a mass-edit session is chatty.

This page catalogues the side-effect chain per operation so the Assistant can answer "why is this slow?" and "what does each save actually do?" correctly. (The rebuild tasks are named — translation-table rebuild, storefront data-asset regeneration — for cross-reference precision.)

## Where to find it

These behaviours fire from the [[settings-translations]] screen on every save / reset / toggle. They are not configurable from the UI — they are platform-internal.

## What the merchant can do here

The merchant doesn't control these side-effects directly. What they CAN do:

- Observe the spinner that indicates the synchronous rebuild tasks are running.
- Reduce overhead by planning edits — see Business rules.
- Wait briefly between successive saves on slow networks (no batching is offered).

## Settings & fields

This aspect has no UI controls — it documents the implicit chain triggered by other actions on the page.

### Side-effect chain per action

| Action | Translation-table rebuild | Data-asset regeneration | Cache flush by tag |
|--------|---------------------------|-------------------------|--------------------|
| **Save a plain edit** (override text changed) | Not run | Yes | Yes (`translation` tag) |
| **Per-row reset** | Append mode (merges defaults back) | Yes | Yes |
| **Bulk reset** (selected rows) | Append mode | Yes | Yes |
| **Reset all to default** | Replace mode (full truncate + reload) | Yes | Yes |
| **Master toggle** (enable / disable system labels) | Not run | Not run `(verify)` | Yes |
| **Storefront-language change** (from [[settings-general]]) | Append mode | Yes `(verify)` | Yes |

The data-asset regeneration rebuilds the storefront's pre-built data asset that bundles translations + currency + miscellaneous front-end constants for the storefront to consume without an extra request. It runs synchronously on every edit, reset, and reset-all.

### Cache mechanics

| Property | Value |
|----------|-------|
| **Storage** | Internal translation cache |
| **Cache-key prefix** | `new-translation:` |
| **TTL** | 7200 seconds (2 hours) |
| **Flush mechanism** | By tag (`translation`) — every save / reset / toggle flushes via tag, not by key |
| **Scope of flush** | All translation cache entries for the site, not just the affected `(locale, theme)` |

## Business rules

### Saves are synchronous — no queue, no background batching

The save handler runs the rebuild tasks inline. The merchant's request waits for the data-asset regeneration (and the translation-table rebuild, on resets) before responding. On a store with many translations this can take a noticeable second or two per edit. No queued jobs are dispatched — the work is not deferred.

### The translation-table rebuild only runs on reset paths, not on plain text edits

A plain text edit that updates an override does NOT run the translation-table rebuild. That step only fires when:

- A row is reset to default (per-row or bulk) → append mode (merges defaults back).
- All overrides are reset → replace mode (full truncate + reload).
- The storefront language is changed in [[settings-general]] → append mode.

Plain saves still regenerate the storefront data asset and flush the translation cache — but they skip the translation-table rebuild. This makes plain saves slightly faster than resets.

### Every save flushes the entire translation cache, not just the affected key

The save / reset / toggle endpoints flush the translation cache by tag for every operation — so a merchant making 100 successive single-row edits triggers 100 cache flushes and 100 data-asset regenerations. There is no batching. Practical implication: **large translation campaigns are slower than they could be**, and the storefront experiences brief cache rebuilds on each save.

For mass translation work, the merchant is better off applying a planned list of changes in a single focused session, accepting the per-row overhead, rather than interleaving translation edits with other work that could also trigger cache flushes.

### The data-asset regeneration rebuilds the asset site-wide, not per-locale

The cache key and storage scope for a single translation row are `(site_id, locale, theme)` — but the regeneration step rebuilds the storefront's data asset for the WHOLE site, not just the current locale/theme. So even when the merchant edits one translation for one language × one theme combination, the storefront's data asset is rebuilt for all locales of that site.

Net effect on the merchant: no functional difference (the storefront still picks the right translation per locale at runtime), but the rebuild work is larger than the edit suggests. The runtime cost is paid in the request that triggered the save.

### Cache flush is site-wide via the `translation` tag

The cache flush uses the `translation` tag, which sweeps every translation-related cache entry for the site at once. Other tagged caches are unaffected. This means storefront pages whose rendering depends on translations will rebuild their cached fragments on the next page request after a save.

### CDN cache is NOT flushed automatically

If a CDN sits in front of the storefront, the merchant may still see the old wording briefly until the CDN cache for that page expires. The platform's translation cache flush happens at the application layer; CDN behaviour is independent. The Assistant should warn merchants who report "I saved my translation but the site still shows the old text" to first hard-reload (bypassing CDN) before assuming the save failed.

### No webhooks, no admin notifications, no audit trail

Translation changes do NOT fire any webhooks (no equivalent of the `product.updated` event), do not send admin notification emails, and are not recorded in any audit log accessible to the merchant. Overrides are written in place — the previous value is not retained. There is no "who changed which translation when" log accessible from the admin panel.

### Reset-all is the highest-impact save — flushes + truncates + reloads + regenerates

The "Reset all to default" path runs the translation-table rebuild in replace mode (which truncates and reloads from disk) plus the data-asset regeneration plus the cache flush. On a large store this is the slowest single operation on the page. The Assistant should warn merchants of the duration before they click — see [[settings-translations-reset]].

## Related

- [[settings-translations]] — hub.
- [[settings-translations-toggle]] — master toggle that flushes the cache.
- [[settings-translations-table]] — every per-row Save triggers the side-effect chain.
- [[settings-translations-reset]] — reset paths trigger the translation-table rebuild.
- [[settings-translations-scoping]] — `(locale, theme)` key the cache uses.
- [[settings-general]] — storefront-language change runs the translation-table rebuild in append mode.

## Open questions

- Does the master toggle invoke the data-asset regeneration in addition to the cache flush? `(verify)` — current behaviour suggests cache-flush only, but the storefront data asset may need to know whether overrides are active.
