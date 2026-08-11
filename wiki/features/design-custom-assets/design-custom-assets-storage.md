---
type: feature
nav_path: "Design → Custom CSS/JS → Storage & lifecycle"
route_name: admin.custom.assets
route_path: /admin/storefront/custom-assets
aliases: ["Custom CSS/JS storage", "Custom code per theme", "Custom assets lifecycle", "custom-css-js row", "Persistiranе на персонализиран код"]
tags: [design, custom, css, js, advanced]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
> Part of [[design-custom-assets]]. See the hub for the other aspects (editor, injection point).

# Custom CSS/JS — storage & lifecycle

## Purpose

This aspect covers **how the custom code is persisted, scoped, and removed** on the [[design-custom-assets]] screen: the single per-theme storage row, why switching themes makes the code disappear, the empty-save "off switch", the absence of version history and cache invalidation, the plan / permission gating, and a server-side parse helper that exists but is currently disabled. These behaviours explain the "my custom code vanished" and "the old code is still showing" support tickets.

## Where to find it

The merchant manages the code on the [[design-custom-assets]] screen (route `/admin/storefront/custom-assets`). There is no separate storage / lifecycle screen, and no version-history or backup UI anywhere in the admin panel.

## What the merchant can do here

The lifecycle actions available to the merchant are limited to two: **Save** (replace the entire stored value) and **clear-and-save** (store an empty string, which removes all custom code). There is no rollback, no per-theme copy, and no enable/disable toggle. To carry code to a new theme, the merchant must re-paste it.

## Settings & fields

This aspect exposes no editable fields beyond the single `custom_assets` field documented on [[design-custom-assets-editor]]. The behaviours below are storage-layer rules, not configurable settings.

## Business rules

### Stored per active theme

The custom code is stored as a single `{parameter: 'custom-css-js', type: 'custom', template: <active-theme>}` row in the same per-theme variable store the Theme Editor uses ([[design-theme-editor]]). This means **switching themes via [[design-themes]] hides the current custom code** — the new theme has its own (empty by default) `custom-css-js` row. Switching back reveals the previously-saved code.

The same code can be carried to a new theme **only by re-pasting it** into the new theme's editor — there is no "import from previous theme" affordance.

### Save replaces the full content

There is only one storage row for custom code, keyed by `parameter='custom-css-js'`. Saving replaces the entire value; there is no append / merge / diff / patch. Save uses an upsert (`firstOrNew` + `fill` + `save`), so the very first save creates the row and every subsequent save updates it in place. The merchant must keep their own copy of the previous version if they want to roll back.

### Empty save removes all custom code

Saving with an empty editor stores an empty string in the custom-code row. The storefront's head-injection partial then renders nothing (the empty string is output verbatim — see [[design-custom-assets-injection]]). This is the only "off switch" — there is no toggle / status flag.

### No size cap enforced

The CodeMirror editor accepts any amount of text the merchant pastes. The server-side save does no length check beyond what the database column allows (typically large-text, accommodating tens of thousands of characters). The merchant should keep the code small — every byte is included in every storefront page response.

### No cache invalidation step

The save handler does NOT explicitly invalidate the merchant's site cache. The storefront still picks up the new code on the next page render because the head-injection partial re-reads from storage on each request (the read is cached statically in-process for the duration of a single request only — see [[design-custom-assets-injection]]). Visitors with cached pages, or external CDN / Cloudflare layers, may continue to see the previous code until their cache expires.

### No plan gate, no permission of its own

The route group has no `middleware('plan-feature:...')` attached, so every plan tier can use Custom CSS/JS. The sidebar link is inside the `store.builder` permission block — a staff role with `store.builder` (or the broader `store`) sees and can access the screen. There is no per-route middleware declaration for custom-assets specifically; access control is the standard admin-panel auth plus that sidebar permission gate. Whether the route enforces any auth beyond the standard admin-panel auth is unconfirmed `(verify)`.

### Server-side parse helper (not currently used by save)

The controller carries a helper method that can parse the submitted HTML and split it into three separate buckets — `cssContent` (everything in `<style>` tags), `jsContent` (everything in inline `<script>` tags without `src`), and `html` (everything else, with the `<style>` and inline-script tags stripped). This would allow targeted injection (CSS into a stylesheet block, inline JS into a script block, the rest in-place) but **it is currently disabled** (the parse call is commented out). For now, the save stores the merchant's raw input as one blob.

## Related

- [[design-custom-assets]] — hub.
- [[design-custom-assets-editor]] — the editor + the single `custom_assets` field.
- [[design-custom-assets-injection]] — why a save takes effect without a cache flush, and where the stored content is rendered.
- [[design-theme-editor]] — shares the same per-theme variable store the custom code is saved into.
- [[design-themes]] — the theme picker; switching themes hides the current custom code.

## Open questions

- ⏸️ **Cache invalidation after save.** Saving does not flush external caches. Storefront CDN / Cloudflare caches may serve the old page until the cache TTL expires; merchants making time-sensitive changes should flush their CDN manually.
- ⏸️ **Auth beyond standard admin-panel auth.** `(verify)` whether the custom-assets route enforces any auth beyond standard admin-panel auth + the `store.builder` sidebar permission.
