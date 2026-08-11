---
type: concept
nav_path: "Concept → Storefront architecture → CSS and assets"
aliases: ["Storefront CSS", "theme.css", "Theme Editor variables", "stylesheet_version", "last_build", "Asset cache-busting", "Storefront head asset order", "styles.min.css"]
tags: [storefront, css, assets, theme-editor, cache, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, theme inheritance, the search index read-side, JS bundles, Smarty plugins, caching).

# Storefront — CSS and asset pipeline

## Definition

Storefront CSS comes from **multiple layered sources** that the storefront `<head>` includes in a deliberate order, so later rules win on equal specificity. The most visible per-merchant layer is the theme's pre-built the theme's own override with placeholder tokens of the form `_<variable-name>_` (e.g., `_color-buttons-primary_`). On every Theme Editor save, the platform substitutes every token with the merchant's saved value (or the theme's default), uploads the resulting CSS to S3 under `<site_id>/css/theme.css`, and stamps the merchant's `stylesheet_version` setting with a fresh UNIX timestamp.

Asset URLs use two cache-busters: the platform-wide `?<last_build>` query string (flips on every deploy) for theme-author-shipped bundles, and the per-merchant `?<stylesheet_version>` for the S3-hosted `theme.css`. So a platform deploy invalidates every storefront's bundles at once; a single merchant's colour change invalidates only their `theme.css`.

## Scope

Covered:

- The 6-entry storefront `<head>` asset order.
- The theme's own override token file + Theme Editor variable substitution.
- The S3 upload to `<site_id>/css/theme.css` + the `stylesheet_version` setting.
- The `last_build` cache-buster — how it's resolved in production vs development.
- The interaction between the platform-wide and per-merchant cache-busters.

Not covered here:

- The CSS rules a theme author writes inside `styles.min.css` or `theme.css` — theme-author concern.
- The Theme Editor UI variables and their groupings — see [[design-theme-editor]].
- Custom CSS/JS as a customisation layer — see [[design-custom-assets]] and [[theme-customization-layers]].
- the platform edge / CDN caching — see [[storefront-arch-caching-invalidation]].

## Contrasts

- **`styles.min.css` vs `theme.css`** — the theme's own override is the theme author's compiled CSS (LESS/SCSS-built, theme-author-controlled, ships with the theme). `<site_id>/css/theme.css` on S3 is the **merchant's** Theme-Editor-substituted CSS — same template file (`assets/styles/theme.css`), per-merchant variable values.
- **`last_build` vs `stylesheet_version`** — `last_build` is platform-wide (one value across all merchants, flips on deploy). `stylesheet_version` is per-merchant (one value per merchant, flips on Theme Editor save). Both serve as cache-busters but at different scopes.
- **Production `last_build` vs development `last_build`** — production resolves to the platform code. Development resolves to the platform code (fresh every request, useful for theme authors).
- **Theme `assets/styles/theme.css` vs S3 `<site_id>/css/theme.css`** — the file in the theme directory is the **template** with `_token_` placeholders. The file on S3 is the **substituted** output per merchant.

## Where it applies

- Every storefront page render — the `<head>` emits the 6 asset entries below.
- Every Theme Editor save ([[design-theme-editor]]) — re-substitutes the merchant's `theme.css` to S3 and bumps `stylesheet_version`.
- Every platform-wide deploy — flips `last_build` and invalidates all storefronts' bundle URLs.

## How it works

### The storefront `<head>` asset order

The storefront's `<head>` includes (in this order):

1. `themes/<theme>/css/styles.min.css?<last_build>` — the theme's compiled CSS (LESS/SCSS-built, theme-author-controlled).
2. `themes/_global/css/checkout.min.css?<last_build>` — shared checkout CSS (only on checkout pages).
3. `<site_id>/css/theme.css?<stylesheet_version>` — the merchant's Theme-Editor-substituted CSS, hosted on S3.
4. `site/css/build.min.css?<last_build>` — platform-level shared CSS (Font Awesome, common utility classes, third-party plugins).
5. The Google Fonts URL the platform built from the merchant's Theme Editor typography selections.
6. The merchant's **Custom CSS/JS** payload (rendered verbatim — see [[design-custom-assets]] and [[theme-customization-layers]] Layer 3).

The order matters: later rules win on equal CSS specificity. So Custom CSS/JS overrides everything else, which is intentional — that's the merchant's escape hatch.

### `theme.css` + Theme Editor variable substitution

Each theme ships a pre-built the theme's own override with placeholder tokens of the form `_<variable-name>_` (for example, `_color-buttons-primary_`, `_color-background_`, `_font-family-headings_`). Theme authors choose which variables to expose by sprinkling these tokens through the CSS source.

On every [[design-theme-editor]] save, the platform:

1. Reads the theme's `assets/styles/theme.css` token file.
2. Replaces every `_token_` with the merchant's saved value (from the `front_theme` table) or the theme's default if the merchant hasn't customised it.
3. Uploads the resulting CSS to S3 at `<site_id>/css/theme.css`.
4. Stamps the merchant's `stylesheet_version` setting with a fresh UNIX timestamp.
5. Clears the `front_theme` per-merchant cache.

The next storefront request emits `<site_id>/css/theme.css?<stylesheet_version>` — the new timestamp busts the browser cache for this one merchant only.

The theme's compiled `styles.min.css` (and JS bundle) are NOT recompiled on a Theme Editor save — those are theme-author-shipped binaries. Only the variable-substituted `theme.css` is regenerated.

### `last_build` — platform-wide cache-buster

The platform exposes a singleton `last_build` (verified — registered in an app service provider). Resolution:

- **Production**: the platform code.
- **Development**: the platform code (fresh every request — useful for theme authors editing CSS / JS locally).

The Smarty helpers `themeScript` and `styleScript` ([[storefront-arch-smarty-plugins]]) append `?<last_build>` to every theme asset URL, so every platform-wide deploy invalidates every storefront's JS / CSS bundle URLs in one go.

### `stylesheet_version` — per-merchant cache-buster

`stylesheet_version` is a per-merchant setting stamped on every Theme Editor save (and on a theme switch — see [[storefront-arch-caching-invalidation]]). It busts only the S3-hosted `theme.css` for that one merchant; the platform-wide bundles are untouched.

### Why two cache-busters

Splitting platform-wide vs per-merchant invalidation means:

- A platform deploy doesn't force every merchant's `theme.css` to be re-fetched (it's still on S3 with the same URL).
- A merchant's colour change doesn't invalidate other merchants' caches or the shared platform bundles.
- The two scopes are independent and can flip at different cadences (deploys per week vs Theme Editor saves per day per merchant).

## Related

- [[storefront-architecture]] — hub.
- [[storefront-arch-caching-invalidation]] — what else happens on a Theme Editor save / theme switch.
- [[storefront-arch-smarty-plugins]] — `themeScript` and `styleScript` emit the bundle URLs.
- [[storefront-arch-theme-inheritance]] — paired template inheritance model.
- [[storefront-arch-js-bundles]] — paired per-theme JS bundle.
- [[design-theme-editor]] — the visual variable editor at `/admin/builder`.
- [[design-custom-assets]] — the raw HTML/CSS/JS injection at `/admin/storefront/custom-assets`.
- [[theme-customization-layers]] — the 3-layer customisation stack.

## Open Questions

- **Whether `theme.css` substitution runs synchronously on save or via a queued job** — the merchant clicking Save in Theme Editor expects an immediate storefront update; verify whether the substitution is in-request or deferred.
- **Whether the platform-level `site/css/build.min.css` is per-theme or truly shared** across every storefront — naming suggests shared but verify against the actual asset path.
- **The complete set of Theme Editor variables** exposed across all themes — each theme picks which `_token_` names it uses; no central registry (verify).
