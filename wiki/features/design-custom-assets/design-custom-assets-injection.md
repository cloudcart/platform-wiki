---
type: feature
nav_path: "Design → Custom CSS/JS → Injection point"
route_name: design.custom-assets
route_path: /admin/design/custom-assets
aliases: ["Custom CSS/JS injection", "Custom code head injection", "Where custom code is injected", "Custom assets render order", "async defer custom script", "CSP custom script", "cookie consent tool in custom code", "Инжектиране на персонализиран код"]
tags: [design, custom, css, js, advanced]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---
> Part of [[design-custom-assets]]. See the hub for the other aspects (editor, storage & lifecycle).

# Custom CSS/JS — the injection point

## Purpose

This aspect answers the most common "why does my code behave like this?" question for [[design-custom-assets]]: **where on the storefront the pasted markup lands, when, and with what guarantees**. The short answer: verbatim into the `<head>` of *every* storefront page, after the platform's own head assets, with no sanitisation and no per-page filter.

## Where to find it

The merchant edits the code on the [[design-custom-assets]] screen (route `/admin/design/custom-assets`); there is no separate "injection settings" screen. The injection itself happens on the storefront, not in the admin panel — it is a render-time behaviour, not a configurable field.

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

Custom CSS needs `!important` (or a more specific selector) where a style comes **after** it or sits on the element itself:

- the **Buttons settings** corner radius and the **Grid settings** container width and offset, both printed later in the head ([[design-module-buttons-settings]], [[design-module-grid-settings]]);
- inline `style` attributes, which beat any stylesheet rule unless it carries `!important`: a Page Builder row's padding, margin and background ([[landing-pages-builder-rows]]), and other blocks' inline styles;
- style blocks a module prints in the page body. The Video slider's set its fonts, sizes and padding with `!important` on an id that changes with each render, so custom CSS practically cannot override them; use the block's own fields ([[design-module-video-slider]]).

### Order against the platform's scripts

Before the pasted code, the page head already holds the storefront settings (the GDPR configuration among them), the consent helper the built-in apps ask, the data layer, Google's consent default (all denied, only while the Google Consent Mode group is active), jQuery, the CloudCart Analytics setup, the styles and the theme's head assets. After it come the page body and, at its end, the theme's script bundle, the Consent Mode update and the apps file, which loads the built-in tracking apps (Google Analytics, the Google Tags container, Meta, TikTok and others) and the cookie bar **asynchronously**. So pasted code runs before any built-in tracking app has loaded.

### No async / defer control, no consent gating, no CSP

- The code is emitted exactly as pasted. Adding `async` or `defer` to its own `<script>` tags is the merchant's job; without them, a script blocks rendering while it loads.
- The GDPR app's consent does not gate pasted code: it runs whatever the visitor answered, unless the code checks consent itself ([[apps-gdpr-overview-script-gating]]).
- Neither the application nor the web-server configuration in the code base sets a Content-Security-Policy on storefront pages, so pasted scripts may load from any address (verify for the edge layer).

### No sanitisation — the merchant is fully trusted

The save handler stores the raw value of the `custom_assets` field without any HTML / JS sanitisation, tag-stripping, or content filtering, and the storefront renders it with no escaping. The merchant can include `<script>` tags pointing to arbitrary external domains, can paste server-altering markup, and can break the entire storefront with a single typo. This is by design — the screen is for advanced merchants who need direct head-injection.

### Read path — one read per request

The storefront's `<head>` partial (loaded by every theme's main template) calls a single helper that returns the merchant's saved code for the active theme. The helper uses an in-process static cache (one read per request), so a page render with multiple includes does not query storage multiple times. The output is rendered with the `nofilter` directive — i.e., no HTML-entity escaping is applied. Because it re-reads storage on each render, any page rendered after a save carries the new code; pages already in the full-page cache keep the old code until they expire (guests within 20 minutes) — see [[design-custom-assets-storage]].

## Related

- [[design-custom-assets]] — hub.
- [[design-custom-assets-editor]] — the editor where the injected markup is authored.
- [[design-custom-assets-storage]] — how the injected content is stored and how long cached pages keep the old code.
- [[storefront-architecture]] — the broader storefront render / cache picture.
- [[marketing-seo]] — for meta / tracking codes that have dedicated integration surfaces instead of raw head injection.
- [[apps-gdpr-overview-script-gating]] — consent and outside cookie-consent tools.

## Open questions

- ⏸️ **Conflict with dedicated app integrations.** Not detected by the platform — merchants who install an integration app (e.g., Facebook Pixel) AND paste the same pixel here will fire both. Avoid duplication manually.
