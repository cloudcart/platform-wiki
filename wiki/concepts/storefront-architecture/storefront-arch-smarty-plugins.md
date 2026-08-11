---
type: concept
nav_path: "Concept → Storefront architecture → Smarty plugins"
aliases: ["Smarty plugins", "Storefront Smarty plugins", "themeScript", "styleScript", "Smarty plugin catalogue", "route plugin", "site plugin", "money plugin"]
tags: [storefront, smarty, plugins, templates, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, theme inheritance, the search index read-side, JS bundles, CSS assets, caching).

# Storefront — Smarty plugin catalogue

## Definition

The platform code middleware registers a catalogue of Smarty plugins on **every storefront request**, so theme authors can use them in any `.tpl` file as `{plugin-name(args)}` calls or chained modifiers (`{$value|plugin-name}`). The catalogue spans URL helpers, asset URLs, site / configuration access, translation, formatting, session and auth, crawler detection, standard PHP helpers, and Google Maps helpers — plus a set of classes registered as Smarty-callable facades.

This is the **theme author's API** to the platform. It is the only sanctioned way for templates to reach into the application framework, the merchant's settings, the current customer's session, or the asset pipeline. A theme that needs platform behaviour goes through these plugins; bypassing them (e.g., embedding raw `<?php... ?>` in templates) is not supported because Smarty templates are not direct PHP.

## Scope

Covered:

- The full plugin catalogue registered platform-wide (URL, asset, site, translation, formatting, session, crawler detection, standard PHP helpers, Google Maps, misc).
- The Smarty-callable classes (facades) — `Site`, `Session`, `AdminPermissions`, `Currency`, `Format`, `Order`, `Comment`, `Template`.
- Where each plugin is most commonly used in `_global` and reference themes.

Not covered here:

- The per-tenant Smarty config that the plugins are registered against — see [[storefront-arch-request-lifecycle]].
- The template inheritance lookup that resolves `.tpl` files — see [[storefront-arch-theme-inheritance]].
- The asset URLs emitted by `themeScript` / `styleScript` and their cache-busting — see [[storefront-arch-css-assets]].

## Contrasts

- **Plugin (`{plugin}`) vs facade method (the platform code)** — plugins are platform-curated short-form helpers (`{route('product', ...)}`). Facade methods reach more deeply into the registered classes but require the full namespace; they are used less often in themes.
- **Platform-managed plugins vs theme-author plugins** — every plugin listed below is registered by the platform code for every request. Themes can register additional plugins via their own bootstrap (verify how), but the platform-managed catalogue is the cross-theme contract.

## Where it applies

Every Smarty `.tpl` file on the storefront. The most common usage sites:

- **Layout templates** (the theme templates and theme overrides) — call `themeScript` and `styleScript` to emit asset URLs; `csrf_token` to render the form token; `site` to read merchant settings; `__` for translation; `favicon` for the favicon URL.
- **Product detail and listing** — `route('product', ['slug' => $p->slug])`, `money($p->price)`, `noImage` fallback for missing images.
- **Cart and checkout** — `csrf_token`, `__`, `money`, `setting('cart.something')`.
- **Page-builder pages and modules** — `route`, `__`, `money`, asset URLs.

## How it works

### Plugin catalogue (registered on every storefront request)

**URL and routing**:

- `route` — resolve a named route to a URL.
- `routeExists` — boolean, route name is registered.
- `activeRoute` — boolean, current route matches.
- `routeParameter` — read a route parameter from the current request.
- `segment` — read a URL segment by index.

**Asset URLs**:

- `themeScript` — emits `themes/<theme>/js/scripts.min.js?<last_build>` (see [[storefront-arch-css-assets]] for the cache-buster).
- `styleScript` — emits `themes/<theme>/css/styles.min.css?<last_build>`.
- `asset` — generic asset URL helper.
- `favicon` — favicon URL with fallback.
- `noImage`, `noImageCategory`, `noImageVendor` — placeholder image URLs.
- `logo` — merchant logo URL.
- `asseticModule` — asset URL for modules.

**Site / configuration**:

- `site` — returns the current `Site` model (call `site('template')` to read the active theme slug, `site('name')` for merchant name).
- `config` — the application framework config helper.
- `app` — current app instance.
- `app_namespace` — app's namespace.
- `setting` — read a merchant setting key.
- `inDevelopment` — boolean, the storefront is in development mode.
- `gethostname` — server hostname.

**Translation**:

- `__` — translate string with parameters.
- `lang` — alias / variant.
- `trans_choice` — pluralisation.
- `locale` — current locale.

**Formatting**:

- `money` — format a number as the storefront's current currency.
- `date` — date formatting helper.
- `strtotime`, `sprintf`, `uniqid`, `str_random`, `md5`, `encrypt`.

**Session / auth**:

- `session` — read a session value.
- `csrf_token` — emit the CSRF token (required on every storefront form).
- `showPriceForUser` — visibility check for B2B price-hiding scenarios.

**Crawler detection**:

- `isCrawlerRequest` — boolean, request is from a known crawler.
- `isSearchEngine` — boolean, search engine specifically.

**Standard PHP helpers exposed**:

- `trim`, `rtrim`, `strtolower`, `strtoupper`, `str_replace`, `str_contains`, `strpos`, `strstr`, `implode`, `floatval`, `intval`, `boolval`, `is_scalar`, `is_null`, `is_numeric`, `is_string`, `is_object`, `get_class`, `array_first`, `array_last`, `mt_rand`, `rand`, `unserialize`, `sort`, `str_split`, `stringReverse`, `long2ip`.

**Google Maps**:

- `hasGoogleMapKey` — boolean, merchant configured a Maps key.
- `getGoogleMapKey` — the merchant's Maps key.
- `drawGoogleMapScript` — emits the Maps loader script tag.

**Misc helpers**:

- `supportNewSpinner` — feature flag for a newer spinner UI.
- `inputJsError`, `inputPrefix`, `inputIdPrefix` — form input helpers.
- `view` — render another view inline.
- `collect` — the application framework `collect` helper.
- `isZora` — special-client carve-out (ignore — verify scope).

### Smarty-callable classes (facades)

A set of classes is registered to Smarty so theme code can call methods as the platform code:

- `Site` — the merchant's `Site` model and helpers.
- `Session` — session access.
- `AdminPermissions` — permission checks (rarely useful in storefront).
- `Currency` — currency conversion and formatting.
- `Format` — format-helpers for prices, numbers, dates.
- `Order` — order-related helpers (used on order-tracking and account pages).
- `Comment` — comments / reviews helpers.
- `Template` — subscription / template helpers (verify scope).

Plus integration-specific facades that the registration list adds (the exact set varies — the platform code is the source of truth).

## Related

- [[storefront-architecture]] — hub.
- [[storefront-arch-request-lifecycle]] — the platform code is the step that registers all of these.
- [[storefront-arch-theme-inheritance]] — `.tpl` files where the plugins are called.
- [[storefront-arch-css-assets]] — `themeScript` / `styleScript` emit the cache-busted bundle URLs.

## Open Questions

- **Whether themes can register their own additional plugins** through a per-theme bootstrap, or whether the catalogue is fixed by the platform code (verify).
- **The exact full list of integration-specific facades** registered alongside `Site`, `Session`, `Currency`, `Format`, `Order`, `Comment`, `Template` — the platform code is the source of truth and the list above is partial (verify by reading the resolver).
- **Scope of `isZora`** — this is a known special-client carve-out helper. Should not be used on new themes (verify whether it can be safely ignored entirely or is still referenced from `_global`).
