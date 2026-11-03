---
type: feature
nav_path: "Design → Custom CSS/JS → Injection point"
route_name: admin.custom.assets
route_path: /admin/storefront/custom-assets
aliases: ["Custom CSS/JS injection", "Custom code head injection", "Where custom code is injected", "Custom assets render order", "Инжектиране на персонализиран код"]
tags: [design, custom, css, js, advanced]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---
> Part of [[design-custom-assets]]. See the hub for the other aspects (editor, storage & lifecycle).

# Custom CSS/JS — the injection point

## Purpose

This aspect answers the most common "why does my code behave like this?" question for [[design-custom-assets]]: **where on the storefront the pasted markup lands, when, and with what guarantees**. The short answer: verbatim into the `<head>` of *every* storefront page, after the platform's own head assets, with no sanitisation and no per-page filter.

## Where to find it

The merchant edits the code on the [[design-custom-assets]] screen (route `/admin/storefront/custom-assets`); there is no separate "injection settings" screen. The injection itself happens on the storefront, not in the admin panel — it is a render-time behaviour, not a configurable field.

## What the merchant can do here

The merchant controls *what* gets injected (the pasted markup — see [[design-custom-assets-editor]]) but not *where* or *when*. The only lever over targeting is client-side: because the code runs on every page, the merchant must guard page-specific logic in JavaScript (e.g., `if (location.pathname === '/cart') { ... }`).

## Settings & fields

This aspect has no editable fields of its own — the single `custom_assets` field is documented on [[design-custom-assets-editor]]. The injection behaviour is fixed and not configurable.

## Business rules

### Injection point — `<head>` of every storefront page

The saved content is rendered verbatim (no escaping, no sanitisation) inside the storefront's `<head>` element, immediately after the platform's other head-injected assets (the theme's stylesheet, the Google Fonts URL, the FontAwesome stylesheet, the `cc-analytics` setup script, etc.) — i.e., the custom code sees the storefront's globals already defined and can hook into them.

The injection happens on EVERY rendered storefront page, including:

- Homepage and all dynamic / static landing pages.
- Category / product list / product detail pages.
- Cart and checkout pages.
- Blog category / article pages.
- Account / login / register / order-history pages.
- 404 and other system pages.

There is no per-page-type filter — if the merchant only wants the code on, say, the cart page, they must guard it client-side (`if (location.pathname === '/cart') { ... }`).

### Render order — custom CSS wins over the theme stylesheet

The custom code partial is included in the storefront's `<head>` right after the platform's CSS stylesheets (`css_global.tpl`, the theme's `header_assets.tpl`, and the theme's pre-built `theme.css`). This means the merchant's CSS overrides any rules in the theme's stylesheet — later rules win on equal specificity, so a custom rule with the same selector as a theme rule takes effect without needing `!important`.

### No sanitisation — the merchant is fully trusted

The save handler stores the raw value of the `custom_assets` field without any HTML / JS sanitisation, tag-stripping, or content filtering, and the storefront renders it with no escaping. The merchant can include `<script>` tags pointing to arbitrary external domains, can paste server-altering markup, and can break the entire storefront with a single typo. This is by design — the screen is for advanced merchants who need direct head-injection.

### Read path — one read per request

The storefront's `<head>` partial (loaded by every theme's main template) calls a single helper that returns the merchant's saved code for the active theme. The helper uses an in-process static cache (one read per request), so a page render with multiple includes does not query storage multiple times. The output is rendered with the `nofilter` directive — i.e., no HTML-entity escaping is applied. The fact that this re-reads from storage on each request is why a save takes effect on the next page render with no explicit cache-flush step — see [[design-custom-assets-storage]] for the cache caveat with external CDNs.

## Related

- [[design-custom-assets]] — hub.
- [[design-custom-assets-editor]] — the editor where the injected markup is authored.
- [[design-custom-assets-storage]] — how the injected content is stored and why a save takes effect without a cache flush.
- [[storefront-architecture]] — the broader storefront render / cache picture.
- [[marketing-seo]] — for meta / tracking codes that have dedicated integration surfaces instead of raw head injection.

## Open questions

- ⏸️ **Conflict with dedicated app integrations.** Not detected by the platform — merchants who install an integration app (e.g., Facebook Pixel) AND paste the same pixel here will fire both. Avoid duplication manually.
