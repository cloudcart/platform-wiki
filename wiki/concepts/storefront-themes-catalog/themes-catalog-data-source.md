---
type: concept
nav_path: "Concept → Storefront themes catalog → Data source"
aliases: ["Themes catalog data source", "cc_gate.templates", "Templates DB table", "in_dev flag", "active flag", "coming_soon flag", "Mapping slug"]
tags: [storefront, themes, catalog, reference]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[storefront-themes-catalog]]. See the hub for the other aspects (inheritance, pricing tiers, base themes, special-client variants, install flow).

# Themes catalog — data source

## Definition

The catalog is rendered from rows in the `cc_gate.templates` table in the gate DB. The merchant catalog screen at **Design → Themes** (`/admin/storefront/templates`) shows every template where `in_dev = 0` AND (`active = 'yes'` OR `coming_soon = 1`), grouped into **Free** and **Paid** tabs. Three boolean-ish flags decide whether a row is in the catalog at all:

| Flag | Meaning | Effect |
|---|---|---|
| `in_dev` | Work-in-progress / agency-private | When `1`, the row is hidden from the merchant catalog unless the staff member sets the `in_dev` cookie. |
| `active` | Platform-installable | When `'no'`, the row is hidden from the catalog and not installable, but existing merchants on the theme keep rendering normally. |
| `coming_soon` | Pre-announce slot | When `1` (even with `active = 'yes'`), the row appears in the catalog as a non-installable preview card. |

The **canonical theme identity** is the **`mapping`** column — a unique slug. It is the folder name under `themes/`, the value persisted on the site record (`site.template` in the tenant DB and `users_sites.template_id` joined to `templates.mapping` in the gate DB), the parameter on every theme-related route, and the join key for theme-scoped tables (`front_theme`, `site_subscriptions`).

## Scope

Covered:

- The `cc_gate.templates` table as data source.
- The three visibility flags (`in_dev`, `active`, `coming_soon`).
- The `mapping` slug as canonical identity.
- The divergence between the disk (`themes/<mapping>/` folders) and the DB.

Not covered here:

- Theme inheritance + filesystem fallback — see [[themes-catalog-inheritance]].
- Free vs paid pricing computation — see [[themes-catalog-pricing-tiers]].
- Which themes are general-purpose vs special-client — see [[themes-catalog-base-themes]] / [[themes-catalog-special-client]].
- The install flow that consumes the `mapping` slug — see [[themes-catalog-install-flow]].

## Contrasts

- **Catalog visibility vs `in_dev`** — `in_dev = 1` is a private/agency flag. Rows with `in_dev = 1` are NOT in the catalog (examples: another custom theme, another custom theme, `motivation-hardware1`, another custom theme, another custom theme, another custom theme, `motivation-sports1`, another custom theme, another custom theme, another custom theme, `flair-clothesforyou`, `flair-electronicstore`, `echappe-software`, `knowledge-toysandgames`, `summer-blade`).
- **Catalog-active vs catalog-retired** — `active = 'no'` rows (`cream`, `default`, `diamond`, `em-design`, `freedom-liquid`, `hail`, `journey`, `lingerie`, `mclimate`, `natureface`, `ruby`, `zircon`, `zora-liquid`) are platform-retired; the DB row remains so legacy merchants on those themes keep rendering, but new merchants cannot install them. Many also have no folder on disk anymore.
- **Catalog DB vs disk** — three states are possible:
  - DB row + folder on disk → the normal case; row is installable if `active = 'yes'`.
  - DB row + no folder on disk → typically `active = 'no'` (retired); not installable.
  - Folder on disk + no catalog DB row → legacy folders (`flair-clothesforyou`, `flair-electronicstore`, another custom theme, another custom theme, etc.) whose DB rows are either `in_dev = 1` or absent. They cannot be installed from the catalog but may still render for a few legacy merchants whose `site.template` already points at them.
- **`mapping` vs the BG/EN display name** — the catalog UI shows a localised display name from `templates_translations`. When that table is empty, the UI falls back to the `mapping` slug or to a hard-coded string per theme (verify).

## Where it applies

The data-source rules apply everywhere theme identity is read or written:

- **The catalog screen** at `/admin/storefront/templates` runs the `in_dev = 0 AND (active = 'yes' OR coming_soon = 1)` filter.
- **The Install action** at `admin.templates.change/{mapping}` re-validates `active = 'yes'` server-side; this is why an `active = 'no'` theme cannot be switched to even if a URL is hand-crafted. See [[themes-catalog-install-flow]].
- **The Purchase action** at `admin.templates.purchase/{mapping}` similarly resolves the row by `mapping` and rejects `in_dev = 1` rows for non-staff sessions.
- **Routing + view path** — the active `mapping` becomes the segment in `themes/<mapping>/templates/` that the renderer searches first; missing templates fall through to the theme templates (see [[themes-catalog-inheritance]]).
- **Theme-scoped tables** — `front_theme` keys per-merchant variable overrides by `(site_id, mapping)`; `site_subscriptions` keys paid-theme purchases by `mapping`. Switching themes leaves the prior `(site_id, prev_mapping)` rows in place — they re-activate if the merchant ever switches back.

`coming_soon = 1` rows are a special case: they appear in the catalog but the Install action is suppressed in the UI. They function as a marketing slot for the next batch of templates the platform plans to ship.

## Related

- [[storefront-themes-catalog]] — hub.
- [[design-themes]] — the merchant-facing catalog screen (route, fields, install/purchase flow UI).
- [[themes-catalog-inheritance]] — what happens when `mapping` resolves to a folder that doesn't ship every template.
- [[themes-catalog-pricing-tiers]] — how `price` / `currency` on the same row decide free vs paid.
- [[themes-catalog-install-flow]] — how the `mapping` is consumed to change the active theme.
- [[storefront-architecture]] — the per-tenant `FrontTheme` model and request routing.

## Open Questions

- Whether `templates_translations` is reliably populated on production for the BG/EN display names per theme — the sandbox snapshot was empty (verify).
- Whether any other catalog flags exist (e.g., `recommended`, `featured`, `vertical_id`) beyond `template_category_id` — none were observed in the rendered catalog, but a full column dump of `cc_gate.templates` would lock this down (verify).
