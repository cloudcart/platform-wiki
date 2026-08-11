---
type: concept
nav_path: "Concept → Storefront themes catalog"
aliases: ["Storefront themes catalog", "Theme catalog", "Theme list", "Templates list", "Каталог теми", "Шаблони catalog"]
tags: [storefront, themes, catalog, reference]
created: 2026-06-08
updated: 2026-06-10
source_count: 1
---

# Storefront themes catalog

## Definition

The **storefront themes catalog** is the merchant-visible library of installable storefront templates surfaced in the admin at **Design → Themes** (`/admin/storefront/templates`, route `admin.templates.list`). Each merchant has exactly one **active theme** at any moment — the theme's `mapping` slug is stored on the site record and drives every page of the storefront: layout, default modules, page-builder block library, colour palette, typography, and the set of variables the Theme Editor can edit.

The catalog draws from the `cc_gate.templates` table. The page shows every template where `in_dev = 0` AND (`active = 'yes'` OR `coming_soon = 1`), grouped into **Free** and **Paid** tabs. A template's *Free vs Paid* status is computed at render time: a template with `price` null/0 behaves as **free** for any merchant; a template with `price > 0` is **paid** and requires an active subscription (`site_subscriptions` row keyed by `mapping`) — without one, the **Install** button silently redirects to the purchase flow at `admin.templates.purchase`.

The catalog is **not** the same as the set of all themes that exist on disk or in the DB. It is a curated subset filtered by three flags (`in_dev`, `active`, `coming_soon`), shadowed by the merchant's plan gates, and shaped by the inheritance fallback to the theme templates. The pages in this cluster decompose those mechanics aspect by aspect.

## Sub-pages (in this cluster)

This concept is split into 6 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[themes-catalog-data-source]] — the `cc_gate.templates` table, `in_dev` / `active` / `coming_soon` flags, why disk and DB diverge, `mapping` as canonical identity.
- [[themes-catalog-inheritance]] — base theme vs child variant; filesystem fallback to the theme templates; the `_default` view path; what a child must / must not ship.
- [[themes-catalog-pricing-tiers]] — `price` / `currency`, free vs paid resolution at render, `site_subscriptions` join, purchase-flow handoff.
- [[themes-catalog-base-themes]] — the catalogue of general-purpose base themes + the production-usage ranking; where to point a new merchant.
- [[themes-catalog-special-client]] — bespoke child variants for named merchants; do-not-promote rule; how to recognise them.
- [[themes-catalog-install-flow]] — install / change action, the transaction, side-effects (CSS recompile, translations, demo data, cache invalidation), plan gate.

## Why it matters to the merchant

The catalog is the merchant's only direct lever on the visual identity of their store. Three high-impact consequences:

- **Theme determines layout, not just colour.** Different bases (`flair` vs `themex` vs `knowledge`) ship different module sets and different page-builder block libraries. A "switch the theme" question is never just cosmetic — it changes which pages exist, which widgets are available, and which Theme Editor variables can be tuned. See [[themes-catalog-inheritance]] + [[theme-customization-themes]].
- **Some catalog rows are bespoke for one named merchant.** Installing `flair-bmw`, another custom theme, another custom theme, etc. on an unrelated store produces a layout aimed at the target client's brand. The catalog flags them only by name convention. See [[themes-catalog-special-client]].
- **The Install action is a transactional rewrite of the storefront.** It recompiles CSS, re-seeds landing pages, regenerates translations, and invalidates the per-tenant cache. There is no "try this theme" preview-without-commit path. See [[themes-catalog-install-flow]].

## Scope

What this cluster covers (across the 6 sub-pages):

- The DB-backed catalog (`cc_gate.templates`) + filtering rules.
- Theme inheritance via filesystem fallback to the theme templates.
- The `mapping` slug as canonical theme identity.
- Free vs paid status + the `site_subscriptions` link.
- The split between base themes (full template tree) and child variants (partial overrides).
- Production-usage signal — which themes are actually shipped.
- The install / change action and its side-effects.

What it does NOT cover:

- **Theme customisation surfaces** — variables, custom CSS/JS, modules — see [[theme-customization-layers]].
- **The Theme Editor variable model** — see [[theme-customization-editor]].
- **The page-builder block library exposed per theme** — see [[design-modules]].
- **The merchant-facing screen** (route, fields, install/purchase flow UI) — see [[design-themes]].
- **`in_dev = 1` templates** — work-in-progress / agency-private themes that never appear in the merchant catalog; reachable only with the `in_dev` cookie (a CloudCart-staff workflow).

## Contrasts

- **Base theme vs child variant** — base ships a full `templates/` tree; child ships only overrides and falls back to the theme templates for anything it doesn't ship. See [[themes-catalog-inheritance]].
- **Free vs paid** — every template has a nullable `price` and `currency`. Paid themes need a `site_subscriptions` row keyed by `mapping`. See [[themes-catalog-pricing-tiers]].
- **General vs special-client** — most catalog rows are safe to suggest to any merchant; a documented subset is bespoke for one named merchant and must not be promoted. See [[themes-catalog-special-client]].
- **Catalog-active vs business-recommended** — `active = 'yes'` makes a theme installable, NOT recommended. The catalog has no `recommended` flag. See [[themes-catalog-base-themes]] for the production-usage ranking used as a proxy.
- **Catalog visibility vs `in_dev`** — `in_dev = 1` hides the row from the catalog unless the staff member sets the `in_dev` cookie. See [[themes-catalog-data-source]].
- **Catalog vs disk** — a handful of `themes/<mapping>/` folders exist with no matching catalog DB row (legacy installs), and a handful of DB rows have no folder on disk (`active = 'no'` legacy retirees). See [[themes-catalog-data-source]].

## Where it applies

Every storefront page is rendered by the active theme's templates, with fallback to the theme templates for anything the active theme does not ship. The catalog therefore underpins every page in the [[storefront-architecture]] / storefront page index. Storefront pages reference the catalog via `themes_using` frontmatter:

- **Home** — every base theme ships `templates/home/home.tpl`.
- **Product listing / detail** — every base theme ships `templates/products/`.
- **Cart / Notifications / Static page / Blog** — every base theme ships these.
- **Wishlist / Compare / Contacts** — most base themes ship them; child variants frequently omit them and inherit through the `flair` fallback.
- **Layout / partials** — every theme ships `templates/layout/`; child variants override these for brand restyling.
- **`error.tpl`** — every base theme ships this; children inherit.

See [[themes-catalog-inheritance]] for the full fallback resolution rules.

## Related

- [[design-themes]] — the merchant-facing catalog screen (route, fields, install flow, purchase flow).
- [[design-theme-editor]] — the per-variable customisation surface.
- [[design-custom-assets]] — arbitrary Custom CSS / JS injection.
- [[theme-customization-layers]] — the 3-layer Theme → Theme Editor → Custom CSS/JS hierarchy.
- [[storefront-architecture]] — how the active theme is wired into request routing, view paths, and the `FrontTheme` model.
- [[design-modules]] — the module catalogue exposed per theme.
- [[plan-gates]] — the `change_theme` plan gate that controls who can install a new theme.

## Open Questions

- Which themes does CloudCart **actively promote** to new merchants in the sales conversation? The catalog has no `recommended` flag, so this cluster can only mark **general** vs **special-client** vs `(verify)` from naming + production usage; the canonical answer lives in marketing collateral, not in the DB.
- Whether any base theme has a hard inheritance declaration (e.g., a `parent` key in `theme.json`) or if inheritance is purely a filesystem fallback to the theme templates via the platform code's `_default` path — the inspection of `flair-bmw/config/theme.json` showed no `parent` key, but a definitive code path through the theme loader would lock this down. See [[themes-catalog-inheritance]] (verify).
- The translations table (`templates_translations`) was empty in this snapshot, so the merchant-facing BG/EN display names per theme couldn't be confirmed — the catalog UI likely falls back to the `mapping` slug or to a hard-coded string per theme. Needs a second pull on a populated tenant.
- Which themes opt into the page-builder system (`page_builder: true` in `theme.json`) — relevant to which themes expose Layer-1 page composition to the merchant. See [[design-themes]] for the broader question.
