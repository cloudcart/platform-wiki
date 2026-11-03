---
type: concept
nav_path: "Concept → Theme customization layers → Layer 3 — Custom CSS/JS"
aliases: ["Theme customization Layer 3", "Custom CSS/JS", "Custom assets", "Raw code injection", "Custom head injection", "Storefront code escape hatch"]
tags: [design, theme, customization, css, javascript, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[theme-customization-layers]]. See the hub for the other aspects (themes, editor, cascade, plan gating, overlay).

# Theme customization — Layer 3 (Custom CSS/JS)

## Definition

**Layer 3 — Custom CSS/JS** is the raw-code escape hatch at `/admin/storefront/custom-assets`. The merchant pastes arbitrary HTML / CSS / JavaScript into a CodeMirror editor (`htmlmixed` mode — HTML, `<style>` blocks, and `<script>` blocks are all syntax-highlighted together). Whatever the merchant pastes is injected verbatim into the `<head>` of EVERY storefront page.

The code is stored as one row keyed by `parameter='custom-css-js'`, `type='custom'`, `template=<active-theme>`. So this layer is also per-theme — switching themes hides the previous theme's Custom CSS/JS and shows the new theme's (empty by default if first-time on that theme).

There is **no validation, no sanitisation, no preview, no rollback, no per-page targeting**. The merchant is fully trusted. A typo can break the entire storefront immediately.

## Scope

Covered:

- What Layer 3 is, where it's edited, and where it's stored.
- The verbatim-injection mechanic in the storefront `<head>`.
- The global-scope rule (no per-page targeting natively).
- Cache behaviour on Save (no explicit invalidation).
- The merchant-fully-trusted contract (no validation, no preview, no rollback).
- The "no reset endpoint" pattern (clear-and-save an empty string).

Not covered here:

- The variable system (Layer 2) — see [[theme-customization-editor]].
- Theme base + module slots (Layer 1) — see [[theme-customization-themes]].
- Render order and CSS specificity vs. Layer 2 — see [[theme-customization-cascade]].
- `store.builder` permission + plan gating — see [[theme-customization-plan-gating]].

## Contrasts

- **Layer 3 vs. Layer 2** — Layer 2 edits TOKEN VALUES the theme author declared; Layer 3 is arbitrary code, no token system. Use Layer 2 first; reach for Layer 3 only when the property isn't exposed as a variable.
- **Verbatim injection vs. sanitised input** — the merchant's code is rendered into the `<head>` without escaping or filtering. CloudCart does not validate that the code is well-formed or that it won't break the page.
- **Global scope vs. per-page scope** — Custom CSS/JS appears in the `<head>` of EVERY storefront page. To target a specific page-type, the merchant writes a client-side path guard.
- **Save behaviour** — Layer 2 Save bumps `stylesheet_version` (cache-busts the stylesheet URL). Layer 3 Save does NOT bump any cache key — the storefront's per-request read picks up the new content automatically.

## Where it applies

- [[design-custom-assets]] — `/admin/storefront/custom-assets`, the single-textarea screen.
- The CodeMirror editor uses `htmlmixed` mode (HTML / `<style>` / `<script>` highlighted together).
- The single `custom_assets` field is stored as one row per active theme (`parameter='custom-css-js'`).
- The storefront's `<head>` partial reads and injects this on every page render.

The injected code lands in the `<head>` AFTER the platform's CSS stylesheets (`css_global.tpl`, the theme's `header_assets.tpl`, the merchant's `theme.css` from S3, FontAwesome, the `google_fonts_url`, the `cc-analytics` setup script) — that ordering is what determines the specificity cascade in [[theme-customization-cascade]].

## How it works

### Injection on every storefront page render

On every storefront page render:

1. The storefront's `<head>` partial reads the merchant's custom code for the active theme (in-process cached for the duration of one request — so multiple page partials don't re-read the row).
2. The code is rendered verbatim into the `<head>` — no escaping, no sanitisation, AFTER the platform's stylesheets and analytics setup.

The injection is global — Custom CSS/JS appears on EVERY storefront page (homepage, category, product, cart, checkout, account, blog, 404, all of them). To run code only on certain pages, the merchant writes a client-side path guard, e.g.:

```js
if (location.pathname === '/cart') {
  // cart-only code
}
```

### Save behaviour — no explicit cache invalidation

Save does NOT explicitly invalidate any cache. The storefront picks up new code on the next page render because the head-injection partial re-reads from storage on each request.

There is no CDN purge step. If the merchant has Cloudflare or a CDN with longer-than-default caching applied to the storefront HTML, visitors may continue seeing the old code until their cache expires. For Custom CSS/JS that ships inside the HTML response, the page-cache TTL is the relevant variable; the merchant has to wait for it or purge externally.

### No reset endpoint — clear-and-save the empty string

There is no "reset Custom CSS/JS" button. To remove the custom code, the merchant clears the editor textarea and saves the empty string. The stored row's value becomes empty; the storefront's `<head>` injection renders nothing for it on the next page render.

### No size cap at the application layer

No size cap is enforced at the application layer; the underlying database column is `longText` (up to ~4 GB). The practical limit is whatever the storefront can deliver without performance regressions — large blobs add bytes to every storefront page.

### Concurrent editing — last-write-wins

Two staff editing the same Custom CSS/JS textarea simultaneously will lose one of their changes when saving. There is no locking and no optimistic-concurrency check.

## Key rules / Examples

### Rule: Custom CSS/JS is global — no per-page targeting

Whatever the merchant pastes appears in the `<head>` of EVERY storefront page. To run code only on certain pages, the merchant writes a client-side path guard (`if (location.pathname === '/cart') { ... }`).

### Rule: Save does not invalidate any cache

The storefront picks up the new content on the next request via the head-injection partial's per-request read. External CDN caches (Cloudflare, etc.) may continue to serve old HTML until their own TTL expires.

### Rule: No reset endpoint

To remove all custom code, clear the editor and save the empty string. There is no separate Reset action.

### Rule: Merchant fully trusted

No validation, no sanitisation, no preview, no rollback. A typo (unclosed `<script>`, malformed CSS) can break the entire storefront immediately. The merchant should test in a non-production storefront or be ready to roll back manually by clearing the editor.

### Example: Adding a box-shadow the theme doesn't expose as a variable

1. The merchant wants a box-shadow on the promo banner. The theme doesn't have a `_promo-bar-shadow_` variable.
2. The merchant goes to Custom CSS/JS → pastes:

   ```html
   <style>.promo-bar { box-shadow: 0 2px 4px rgba(0,0,0,0.2); }</style>
   ```

3. Save. The storefront's `<head>` now includes the `<style>` block on every page.
4. The promo banner now has the shadow alongside the Layer 2-driven background colour.

### Example: Cart-only client-side code

1. The merchant pastes a `<script>` block that wraps its logic in a path guard:

   ```html
   <script>
     if (location.pathname === '/cart') {
       // cart-only behaviour
     }
   </script>
   ```

2. Save. The script lands in the `<head>` on every page, but only runs the inner block on `/cart`.

## Related

- [[theme-customization-layers]] — hub.
- [[design-custom-assets]] — admin surface for Layer 3.
- [[theme-customization-editor]] — Layer 2 is the supported customisation surface; reach for Layer 3 only when Layer 2 doesn't expose the property.
- [[theme-customization-cascade]] — render order vs. Layers 1–2; "Layer 3 wins on equal specificity".
- [[theme-customization-themes]] — Layer 3 storage is also keyed by the active `template` slug.
- [[theme-customization-plan-gating]] — `store.builder` permission + no plan-feature gate.

## Open Questions

None.
