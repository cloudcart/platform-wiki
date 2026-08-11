---
type: concept
nav_path: "Concept → Storefront themes catalog → Install flow"
aliases: ["Themes catalog install flow", "Theme install transaction", "Theme change flow", "admin.templates.change", "Theme install side-effects"]
tags: [storefront, themes, catalog, install, reference]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[storefront-themes-catalog]]. See the hub for the other aspects (data source, inheritance, pricing tiers, base themes, special-client variants).

# Themes catalog — install + change flow

## Definition

The merchant changes the active theme by clicking **Install** on a catalog card at **Design → Themes** (`/admin/storefront/templates`). The Install action posts to `admin.templates.change/{mapping}` after a confirmation dialog. The change is a **single-transaction rewrite** of the storefront — it recompiles CSS, regenerates translations, re-seeds landing pages for the new theme, and invalidates the per-tenant cache.

There is **no preview-without-commit path**. Clicking Install commits the change immediately; the only way to "undo" is to install the prior theme again, which re-runs the same full transaction.

For a paid theme without a matching `site_subscriptions` row, the Install button silently redirects to `admin.templates.purchase/{mapping}` instead of running the change — see [[themes-catalog-pricing-tiers]]. For a theme that is `active = 'no'`, the change is rejected at the server-side visibility check even if the route is hand-crafted — see [[themes-catalog-data-source]].

## Scope

Covered:

- The Install / change action.
- The DB transaction (gate DB + tenant DB updates).
- The side-effects (CSS recompile, translations, demo data, cache).
- The `change_theme` plan gate.

Not covered here:

- The merchant-facing UI for the Install action — see [[design-themes-install]].
- The purchase flow for paid themes — see [[themes-catalog-pricing-tiers]] + [[design-themes-purchase]].
- The data-source filtering that decides which rows are installable — see [[themes-catalog-data-source]].

## Contrasts

- **Install vs Buy** — for a free theme (or a paid theme the merchant already owns), the button is labelled **Install** and hits the change action. For a paid theme without a subscription, the button is labelled **Buy** and hits the purchase action. See [[themes-catalog-pricing-tiers]] for the resolution rule.

- **Change vs Switch back to prior** — the platform stores per-`(site, theme)` customisations in `front_theme`. Switching to a new theme leaves the prior theme's `front_theme` row intact; switching back later restores those customisations. This means "trying" a theme is non-destructive to the prior theme's setup — but it does run the full transaction, which is not free (CSS recompile, translations regen). See [[theme-customization-overlay]].

- **Transactional vs preview** — there is no preview. The change is committed inside one DB transaction; a failure mid-transaction rolls back the gate-DB + tenant-DB writes (verify rollback semantics) but the side-effect commands (CSS recompile, translations) are NOT transactional. A failure after the transaction commits but before the side-effects complete leaves the storefront in a partially-recomposed state.

- **`change_theme` plan gate vs per-theme purchase** — `change_theme` is the plan-level gate controlling whether the merchant can run this action at all. Plans without it disable the Install button across every catalog row, regardless of free/paid status. See [[plan-gates]].

## Where it applies

The full Install / change sequence runs from the catalog screen. The merchant flow:

1. Sidebar **Design → Themes** opens `/admin/storefront/templates`.
2. Hover any catalog card → button reveals:
   - **Install** (free / already-purchased), OR
   - **Buy** (paid, not purchased) — redirects to purchase flow.
3. Click Install → confirmation dialog ("Are you sure?" with theme name).
4. Confirm → request goes to `admin.templates.change/{mapping}`.
5. Server-side: the platform re-validates the target row against the catalog visibility rules. If the row is missing, `in_dev = 1`, or `active = 'no'`, the request is rejected.
6. Server-side transaction:
   - Update `users_sites.template_id` in the gate DB.
   - Update `site.template` in the tenant DB.
   - Recompile storefront CSS via the theme renderer.
   - Run the `db:translation --force` command to regenerate translations.
   - If the previous theme was unpaid-cancelled, flip `unpaid_template` back to 0.
7. Post-transaction side-effects:
   - `js:data-generate` rebuilds `data.js`.
   - The demo-data installer's landing-page step re-seeds the landing-page set for the new theme.
   - The per-tenant cache key is regenerated, invalidating the cached pages (the storefront's the platform edge layer drops its cached pages on the next request).
8. The merchant is redirected back to the catalog screen with a success notification.

The full transaction typically completes in 5-15 seconds depending on theme size and number of translations. The platform edge cache drops are immediate; the first storefront request after the change pays a cold-cache cost.

**Side-effects that DO NOT happen on theme change**:

- The merchant's products, categories, customers, orders, settings — all unchanged.
- Custom CSS / Custom JS on the prior theme — left in place but no longer applied (they're scoped to the prior `(site, theme)` row in `front_theme`). Switching back later restores them. See [[theme-customization-custom-assets]].
- Theme Editor variables on the prior theme — same: preserved in `front_theme`, reactivated on switch-back. See [[theme-customization-editor]].
- Landing pages the merchant manually edited — preserved. The demo-data installer's landing-page step only seeds NEW landing pages for the new theme; it does NOT overwrite existing pages (verify).

## Related

- [[storefront-themes-catalog]] — hub.
- [[design-themes]] — merchant-facing catalog screen.
- [[design-themes-install]] — the merchant-facing UI for the Install action.
- [[design-themes-edge-cases]] — known edge cases on the Install flow.
- [[themes-catalog-data-source]] — the visibility flag check that gates this action.
- [[themes-catalog-pricing-tiers]] — paid themes divert to the purchase flow instead.
- [[theme-customization-overlay]] — what survives a theme change (per-theme `front_theme` overlay).
- [[plan-gates]] — `change_theme` plan-level feature gate.
- [[storefront-architecture]] — the per-tenant cache that gets invalidated.

## Open Questions

- Exact rollback semantics when the transaction fails mid-way — whether the gate-DB and tenant-DB writes roll back together (cross-DB transaction is not a native the application framework feature), and what state the storefront is left in if one DB rolls back but the other commits (verify).
- Whether the demo-data installer's landing-page step truly preserves merchant-edited pages or whether it can overwrite under any condition (verify).
- The exact relationship between `unpaid_template` and the install action — whether installing a paid theme on a merchant who previously cancelled the same theme's subscription clears the flag or re-flips it back on (verify).
- Whether the `change_theme` plan gate also blocks the purchase flow (the merchant being unable to install ANY new theme would also mean they can't purchase one) or only the change action (verify).
