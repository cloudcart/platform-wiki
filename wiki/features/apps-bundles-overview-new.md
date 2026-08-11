---
type: feature
nav_path: "Apps → Bundles → Overview (modern)"
route_name: apps.bundles.overview.new
route_path: /admin/products/bundles-new
aliases: ["Bundles Overview (modern)", "Bundles new", "no enable disable button", "app has no active toggle"]
tags: [apps, administration, bundles, overview, modern-vue]
plan_gates: ["bundles", "hidden_products"]
created: 2026-05-21
updated: 2026-08-06
source_count: 4
---
# Bundles → Overview (modern Vue)

## Purpose

The **modern Vue overview** for the Bundles app — landing page in the CcDomain pattern. Shows installation state, capabilities, navigation to the bundle list + creation flow.

For the full Bundles feature set, see [[bundles-list]].

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.
>
> What *can* be switched off is an individual **bundle** — each bundle carries its own Published / Unpublished (`active`) state on the bundle list, see [[bundles-list]].

## Where to find it

Sidebar → Apps → Bundles (modern Vue). Route: `/admin/products/bundles-new`.

Modern Vue components (per `CcDomain/Applications/Pages/Bundles/`):
- `ApplicationsBundlesMainPage.vue` — overview / hub.
- `ApplicationsBundlesListPage.vue` — list of defined bundles.
- `ApplicationsBundlesCreateOrEditPage.vue` — bundle CRUD editor.

## What the merchant can do here

- See install state + capabilities.
- Read description of what bundles do.
- Trigger Install / Uninstall.
- Click through to [[bundles-list]] for the list view.
- Click "+ Create bundle" to enter the editor.

### What the merchant CANNOT do here
- Edit specific bundles from this page — that's the editor.
- Modify settings — that's [[apps-bundles-settings-new]].

## Settings & fields

Read-only metadata + install action. Modern Vue uses CloudCart design system patterns.

## Business rules

### Modern Vue replaces legacy

This page supersedes any legacy overview. Bundles app is one of the modern-Vue-first apps.

### Permission
Standard apps permission scope.

## Plan gates

This overview hub inherits the same plan gates as the rest of the Bundles app (see [[bundles-list]] for the per-bundle details). Plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `bundles` | App-install URL gate + Numeric (max bundles) | App install at `/admin/apps/bundles/install` is access-gated. After install, the same mapping ALSO caps how many bundles the merchant can create. The modern Vue overview reads the `bundles` plan-feature meta — its `current` (allowed cap) vs `used` (count of `type = bundle` products) drives the `isAllowedCreateNewBundle` check. When `current > used`, the **+ Create bundle** CTA is enabled; when the cap is hit, the CTA is disabled and the merchant is funnelled to [[plan-features]] for a pack. Editing existing bundles always bypasses the cap. Per-plan add-on packs are available. |
| `hidden_products` | Boolean | Whether bundles can be marked Hidden via `PATCH /api/bundles/hidden/<id>`. Without the feature, the request returns HTTP 402 with the per-feature upsell payload — the same gating as regular products. |

Behaviour: numeric `bundles` cap → per-feature upsell modal at [[plan-features]] when exhausted; `hidden_products` boolean → plan-upgrade panel when the merchant tries to flip a bundle's hidden flag. See [[plan-vs-feature-pack]] for the pack-vs-upgrade decision.

## Related

- [[bundles-list]] — bundles list (Products → Bundles).
- [[apps-bundles-settings-new]] — modern Vue settings.
- [[apps-bundles-settings-new]] — legacy settings.
- [[products-products]] — constituent products.

## How it works (verified against backend)

### No tutorials or sample bundles shipped

The Bundles app installs an empty bundle list. There are no preloaded sample bundles, no built-in tutorial flow, and no walkthrough overlay. The merchant starts from the **+ Create bundle** CTA and builds their first bundle manually. CloudCart's separate help-centre documentation covers the workflow; nothing is embedded in this view.

### No per-bundle sales dashboard on this hub

This page surfaces install state plus a CTA to the bundle list. It does not show per-bundle revenue, units sold, conversion rates, or any other sales metrics. Per-bundle sales data lives in the merchant's general [[analytics]] (filtered by the bundle product) and in their [[orders]] list — not here. The Bundles app does not register its own analytics dashboard.

### Bundles count IS plan-feature-capped — silent cap check via `feature.current` vs `feature.used`

The Overview meta data includes a `bundles` plan feature with `current` (allowed cap) + `used` (current bundle count). The modern Vue editor uses these to compute `isAllowedCreateNewBundle`:
- If `current === null` or `current === true` (unlimited) → allowed.
- If `current > used` (cap not reached) → allowed.
- Editing an existing bundle (`id` present) → always allowed regardless of cap.

So **there is a hard plan-cap on the number of bundles the merchant can create**. When they hit the cap, the "+ Create bundle" CTA is disabled in the modern Vue UI. Editing existing bundles bypasses the cap; only NEW bundle creation is gated.

### Hidden bundles depend on `hidden_products` plan feature

When the merchant tries to toggle a bundle's hidden status to ON via `PATCH /api/bundles/hidden/1`, the platform checks the platform code. If the merchant's plan doesn't include the hidden_products feature, the request returns HTTP 402 (Payment Required) with the feature details. **Lower plans cannot make bundles hidden** — they can only have visible bundles. This matches the gating on regular products (where hidden_products is also a plan feature).

### Linked products and product-reviews relationships are loaded on view

The Bundle index endpoint optionally loads review-summary data from the [[apps-product-review]] integration. So when the merchant opens the Bundles list with the Product Review app installed + active, each bundle row shows aggregated star ratings + review counts (just like a regular product). When Product Review is NOT installed, the review summary column is empty.

### Bundle list pagination + filters via grid pattern

The modern Vue list uses the GridFilters pattern — supports column-based sorting (active, hidden, featured, new), search by name/SKU, date-range filtering. Same UX as the regular Products list. The bundles themselves are stored as products with a special `BundleProductType` scope (`bundle_id IS NOT NULL`).

## Open questions

