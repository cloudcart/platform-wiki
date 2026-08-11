---
type: feature
nav_path: "Design → Themes → Edge cases"
route_name: admin.templates.list
route_path: /admin/storefront/templates
aliases: ["Theme edge cases", "Demo user theme behaviour", "Coming-soon themes", "In-dev themes", "Demo URL fallback"]
tags: [design, themes, templates, edge-cases]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

# Themes — Edge cases & special-case behaviour

> Part of [[design-themes]]. See the hub for related aspects (catalogue, install, purchase, unpaid-middleware, switch-effects, plan-gates).

## Purpose

This aspect collects the special-case behaviours that don't belong to any single flow — the demo-user short-circuit, the coming-soon teaser cards, the in-dev CloudCart-staff-only themes, and the slug-driven demo-URL fallback that ensures every theme card has a working **View** link even without a manually-set `demo_url`.

## Where to find it

These behaviours manifest on `/admin/storefront/templates`.

## What the merchant can do here

This aspect documents behaviours, not actions. The merchant interacts with cards and buttons via the other aspects ([[design-themes-catalogue]], [[design-themes-install]], [[design-themes-purchase]]).

## What the merchant cannot do here

- Cannot install or change themes as the **demo user** — the install action is short-circuited.
- Cannot install a **coming-soon** theme — no buttons on coming-soon cards.
- Cannot see **in-dev** themes on a production environment without the `in_dev` cookie.

## Settings & fields

This aspect has no merchant-editable fields.

## Business rules

### Demo theme accounts cannot change themes

If the logged-in user is CloudCart's demo user (`demo.user_id` from config), the install action is **short-circuited** — the demo account does not actually change the site's theme even on free themes. Paid-theme install for the demo user is also short-circuited at the unpaid-theme middleware level: the demo account is redirected to the `redirect_after_install` URL without going through checkout. See [[design-themes-unpaid-middleware]] for the middleware short-circuit.

### Coming-soon themes are preview-only

A theme card flagged `coming_soon = 1` is rendered as a teaser — thumbnail dimmed, "Coming Soon" ribbon shown, no View / Install / Buy buttons. Coming-soon themes are listed in **BOTH** the Free and Paid tabs depending on their price (if any) — the listing query treats them as visible regardless of `active` so that the merchant can see what is upcoming.

### In-dev themes are CloudCart-staff-only

Themes with `in_dev = 1` are hidden from the catalogue **unless** either the platform is running in `development` environment OR the requesting browser carries the `in_dev` cookie. Merchants on production never see in-dev themes. This is how CloudCart staff QA new themes before flipping them live.

### Demo URL has a slug-driven fallback (no manually-set `demo_url`)

If a theme has no `demo_url` translation stored, the controller derives one from the theme's mapping slug:

- For themes with `id >= 126`, the fallback uses `https://<mapping>.cloudcart.net` for Bulgarian admin and `https://<mapping>-<locale>.cloudcart.net` for other locales (or it strips a `<prefix>-` from the mapping if present).
- For older themes (`id < 126`), it uses `https://<mapping><locale>.cloudcart.net`.
- The `freedom` theme is hard-aliased to `motivation` in the fallback.

This means every active theme card has a working **View** link even without an explicitly-set demo URL.

### Current theme is never hidden from the merchant

The current-theme panel at the top uses a separate query (the platform code) and continues to render even if the active theme has `active = no` (unpublished) or `coming_soon = 1`. The current theme is NEVER hidden from the merchant just because CloudCart unpublished it. See [[design-themes-catalogue]] for the separate-query mechanic.

### Installing the already-active theme returns an error

The card's normal Install button is hidden for the active theme (the **Current** badge is shown instead). Trying to install the already-active theme via the AJAX endpoint directly returns: *"This is already your current theme."*. Only reachable by URL manipulation. See [[design-themes-install]].

### Custom themes cannot be uploaded

Only CloudCart's catalogue themes are installable from this screen. There is no "upload a theme zip" or "paste a theme manifest" feature. To get a custom theme, the merchant must either commission CloudCart staff or work with a CloudCart-approved theme developer (out of scope of this screen).

## Related

- [[design-themes]] — hub.
- [[design-themes-catalogue]] — listing rules that incorporate `coming_soon` / `in_dev` / current-theme query.
- [[design-themes-install]] — short-circuit detail for the demo user.
- [[design-themes-unpaid-middleware]] — demo-user short-circuit in the middleware.

## Open questions

None.
