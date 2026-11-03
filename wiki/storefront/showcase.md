---
type: storefront-page
route_name: site.showcase
route_path: /showcase/{slug}
themes_using: [child-themes-only]
tags: [storefront, showcase, curated, listing]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Showcase (`/showcase/{slug}`)

## Purpose

The showcase page is a **theme-specific promotional landing surface** for a curated product set. It is rendered only by themes that ship a `showcase/list.tpl` template — the base `flair` theme does NOT, so on most stores `/showcase/{slug}` returns a 404 ("not found") unless the merchant is on a theme that supports it (theme-dependent).

The showcase controller's logic is unusual: if a view lookup returns **true**, the controller throws a not-found error. If the view does NOT exist, it returns the showcase view. **This is inverted from intuition** — the most likely interpretation is a guard added to force a 404 on themes that DO have the view (the line `if(\Illuminate\Support\Facades\a view lookup)` was likely meant to be `!a view lookup). Behaviour to verify — see "Known issues" below.

## URL & route

- **Route name**: `site.showcase`
- **Route path**: `/showcase/{slug}`
- **Controller**: the showcase controller, the request handler
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:showcase`

## How it loads

1. The showcase controller checks a view lookup. If the view exists, it throws a not-found error (the "if" branch raises the 404).
2. If the view does NOT exist, it returns the platform code — which would itself trigger a view-not-found error.

In effect: the route returns **404 in every realistic case** unless the controller's logic is overridden by a custom theme deploying its own router. The route is wired up but the controller is currently a no-op / 404 surface (verify against production behaviour — themes that include `templates/showcase/list.tpl` may bypass the controller via a custom dispatch).

## What the customer sees

When the page does render (on a theme where the controller logic happens to fall through), the template is heavily themed — observed on themes that ship it:

- **Breadcrumb** — from the showcase module.
- **Section title** — the showcase's name from the platform code.
- **View-mode toggle** — `js-switch-compact` / `js-switch-full` (grid vs. list view).
- **Filter buttons** — `js-show-filters` / `js-hide-filters` (mobile-friendly filter pane toggle).
- **Filter pane + product grid** — themed differently from the standard `products/list.tpl` (typically more visual / hero-styled).
- **Product count** — `{$finder->countProducts}` — total products in the showcase.

## Storefront behaviour

- AJAX endpoint exists at `/ajax/showcase/{showcase}` (route `ajax.showcase`) and `/ajax-products/showcase/{showcase}` (route `ajax.products.showcase`) — used by themes that have a working showcase page for filter / pagination AJAX.
- The view-mode toggle (compact / full) likely persists in a cookie (verify per theme).
- The filter-pane toggle persists via the `show-filters` cookie.

## JavaScript behaviour

(From such a theme's `templates/showcase/list.tpl`.)

- `.js-switch-compact` / `.js-switch-full` — toggle grid vs. list view in the product showcase.
- `.js-show-filters` / `.js-hide-filters` — open / close the filter pane; reads / writes the `show-filters` cookie.
- AJAX endpoints (for themes where the page works):
  - `/ajax/showcase/{showcase}` — route `ajax.showcase` (full HTML).
  - `/ajax-products/showcase/{showcase}` — route `ajax.products.showcase` (products only).
  - `/filters-ts/showcase/{showcase}` — route `ajax.filters-ts.showcase` (filters only).

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Whether the showcase route works at all | Determined by the active theme — `flair` and many base themes ship no showcase template; child themes like a theme that ships it, another custom theme, another custom theme do |
| Products in a showcase | [[design-modules]] → Products showcase module (different mechanic from a [[selection]]) |
| Showcase name / title | [[design-modules]] → showcase module settings |
| Filter sidebar in showcase | [[design-modules]] → Products filters module |

## Theme variations

- **No showcase route** on themes that do not ship `templates/showcase/list.tpl` — most base themes (`flair`, `amber`, `bond`, `delicious`, `summer` non-SFA variants, `hades`) are in this bucket.
- **Showcase route works** on a theme that ships it, another custom theme, another custom theme, another custom theme, another custom theme, `knowledge-toysandgames`, another custom theme, another custom theme, `motivation-sports1`, another custom theme, another custom theme (verify the active theme).
- See [[storefront-themes-catalog]] for the per-theme support matrix.

## Known issues / by-design vs bug

- **Likely bug (verify)**: the controller's `if(a view lookup)` branch throws a not-found error. The most plausible reading is that this should be `if(!a view lookup)` (return 404 when the theme does NOT have the view). As written, the route is effectively a no-op for themes that ship the view and a view-not-found error for themes that don't. Production behaviour may be patched at theme-dispatcher level — verify before claiming this is a customer-facing bug. See [[storefront-known-issues]].
- **By design**: only some themes ship a working showcase template — most base themes don't.
- **By design**: showcases are module-driven (admin in [[design-modules]]) rather than entity-driven (no separate admin model like selections / categories).

## Related

- [[storefront-architecture]] — request lifecycle and theme inheritance.
- [[storefront-themes-catalog]] — per-theme showcase support matrix.
- [[selection]] — the entity-driven curated-collection alternative.
- [[products-list]] — the standard listing surface.
- [[design-modules]] — Products showcase module configuration.
- [[design-themes]] — choose a theme that supports showcases.
- [[widget-vs-page-builder-block]] — when to use a module vs. a page-builder block.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Verify the controller's the platform code branch — is it intentionally inverted, or is this a real bug? (And which production stores actually hit this route successfully?)
- Whether the platform code instance referenced in such a theme's template is hydrated by the controller or by a separate module-resolver middleware.
- The full per-theme support matrix — which themes deliver a working showcase page in production today.
